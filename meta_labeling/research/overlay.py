"""Long meta-labeling overlay: buy & hold'a karşı ön-kayıtlı, kilitli test.

Neden? Önceki sistem (EMA 10/40 long/short + meta filtre) AAPL'de B&H'ye yenildi:
zamanın ~%42'sinde piyasadaydı, short tarafı yükselen bir hissede sistematik
zarar üretti ve öznitelikler placebo testlerinde bilgi taşımadı. Meta-labeling
literatürü (López de Prado 2018; Joubert 2022; Meyer, Barziy & Joubert 2023)
iyileşmeyi BİRİNCİL STRATEJİYE göre ölçer: meta-model, birincil modelin
recall'ından precision'a takas yapar. B&H'yi geçmek için birincil stratejinin
kendisinin hisse senedi risk primine maruz olması gerekir.

Tasarım (ön-kayıt: docs/preregistration/long_overlay.md):

1. Birincil model ``AlwaysLong``: her CUSUM olayında long önerisi (maks. recall).
2. Meta-model (LightGBM, purged walk-forward, isotonic kalibrasyon) Joubert'in
   dört bilgi grubunu kullanır:
     * genel öngörücü veri   : çekirdek rejim öznitelikleri (``features.py``)
     * birincil model karnesi : son N KAPANMIŞ işlemde isabet oranı / ort. getiri
     * piyasa rejimi          : endeks (SPY / XU100) trend, momentum, vol oranı
     * birincil model gücü    : yönlü trend öznitelikleri (12-1 momentum, SMA200
                                uzaklığı, zirveden düşüş, EMA farkı)
3. Kitap VARSAYILAN olarak tam long'dur. Olay i'nin karar penceresinde [t0, t1)
   maruziyet m_i = clip(conformal Kelly f_i, 0, 1) olur (μ̂ ≤ 0 -> 0); eşzamanlı
   olayların ortalaması alınır (avgActiveSignals). Meta-modelin görüşü olmayan
   barlarda (ısınma / aktif olay yok) maruziyet ``default_exposure``'dır.
4. Volatilite tavanı: maruziyet x min(1, σ_ref/σ_t), σ_ref = σ_t'nin genişleyen
   medyanı (Harvey vd. 2018: vol hedefleme hisse senetlerinde Sharpe'ı artırır;
   Cederburg vd. 2020: OOS'ta çoğu zaman artırmaz -> ablation ile ayrıştırılır).

Kanıt standardı: nokta tahmini ΔSharpe > 0 "geçti" demek için yeterli DEĞİLDİR;
eşli durağan bootstrap ile ΔSharpe'ın güven aralığı, meta kararlarının olaylar
arasında karıştırıldığı placebo ve ablation (vol tavanı tek başına / meta tek
başına) birlikte raporlanır. Kaldıraç yoktur; işlem sayısı azaltılmaz (kitap
varsayılan olarak piyasadadır).
"""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field, replace
from pathlib import Path

import numpy as np
import pandas as pd

from ..data import validate_ohlcv
from ..features import build_feature_matrix
from .conformal import conformal_kelly
from .execution import adv_value, segment_trades, simulate_portfolio
from .leakage import run_leakage_audit
from .metrics import deflated_sharpe, performance_metrics, sharpe, stationary_bootstrap_indices
from .modeling import (
    EventDataset,
    build_event_dataset,
    build_market_state,
    calibrate_walk_forward,
    sample_candidate_events,
    walk_forward,
)
from .settings import ResearchConfig

log = logging.getLogger("meta_labeling.research")

SYSTEM = "Meta overlay x vol tavanı (sistem)"
BH = "Buy&Hold"


# ------------------------------------------------------------------ öznitelikler
def trend_features(ohlcv: pd.DataFrame, prefix: str = "") -> pd.DataFrame:
    """Yönlü trend / momentum öznitelikleri (yalnızca t kapanışına kadar veri).

    mom_12_1     : zaman serisi momentumu (Moskowitz, Ooi & Pedersen 2012), son ay hariç, vol ile ölçekli
    dist_sma200  : kapanış / SMA(200) - 1
    dd_252       : kapanış / 252 günlük en yüksek kapanış - 1
    ema_spread_z : (EMA10 - EMA40) / EMA40 / σ  (trend takipçisi birincil modelin "güveni")
    ret_5_z      : 5 günlük log getiri / (σ √5)  (kısa vadeli yönlü hareket)
    """
    close = ohlcv["Close"]
    lr = np.log(close).diff()
    vol = lr.ewm(span=50, min_periods=50).std()
    ema_f = close.ewm(span=10, adjust=False, min_periods=10).mean()
    ema_s = close.ewm(span=40, adjust=False, min_periods=40).mean()
    out = pd.DataFrame(
        {
            "mom_12_1": np.log(close.shift(21) / close.shift(252)) / (vol * np.sqrt(231)),
            "dist_sma200": close / close.rolling(200).mean() - 1.0,
            "dd_252": close / close.rolling(252).max() - 1.0,
            "ema_spread_z": (ema_f - ema_s) / ema_s / vol,
            "ret_5_z": np.log(close / close.shift(5)) / (vol * np.sqrt(5)),
        },
        index=ohlcv.index,
    )
    return out.add_prefix(prefix).replace([np.inf, -np.inf], np.nan)


def market_features(market: pd.DataFrame, index: pd.DatetimeIndex) -> pd.DataFrame:
    """Piyasa endeksinden rejim öznitelikleri; hisse takvimine as-of (yalnızca geçmiş) hizalanır."""
    lr = np.log(market["Close"]).diff()
    f = trend_features(market, prefix="mkt_")
    f["mkt_vol_ratio"] = lr.ewm(span=10, min_periods=10).std() / lr.ewm(span=50, min_periods=50).std()
    f = f.replace([np.inf, -np.inf], np.nan)
    union = f.index.union(index)
    return f.reindex(union).ffill().reindex(index)


def track_record_features(events: pd.DataFrame, window: int) -> pd.DataFrame:
    """Birincil modelin karnesi: t0_i'den ÖNCE kapanmış (label_end < t0_i) son ``window`` işlem.

    tr_hit_rate : meta-etiket (net getiri > 0) ortalaması
    tr_mean_ret : ortalama net getiri / σ_t0 (σ biriminde)
    Yeterli kapanmış işlem yoksa NaN (olay eğitimden düşer).
    """
    ev = events.sort_index()
    t0 = ev.index.to_numpy()
    land = pd.DatetimeIndex(ev["label_end"]).to_numpy()
    y = ev["bin"].to_numpy(dtype=float)
    x = (ev["exec_net_ret"] / ev["trgt"]).to_numpy(dtype=float)
    order = np.argsort(land, kind="stable")
    hit, ret = np.full(len(ev), np.nan), np.full(len(ev), np.nan)
    qy: deque[float] = deque(maxlen=window)
    qx: deque[float] = deque(maxlen=window)
    k = 0
    for i in range(len(ev)):
        while k < len(ev) and land[order[k]] < t0[i]:
            qy.append(y[order[k]])
            qx.append(x[order[k]])
            k += 1
        if len(qy) == window:
            hit[i], ret[i] = float(np.mean(qy)), float(np.mean(qx))
    return pd.DataFrame({"tr_hit_rate": hit, "tr_mean_ret": ret}, index=ev.index).reindex(events.index)


def expanding_base_rate(events: pd.DataFrame) -> pd.Series:
    """Modelsiz olasılık: t0_i'den ÖNCE kapanmış tüm işlemlerin isabet oranı (genişleyen, nedensel)."""
    ev = events.sort_index()
    t0 = ev.index.to_numpy()
    land = pd.DatetimeIndex(ev["label_end"]).to_numpy()
    y = ev["bin"].to_numpy(dtype=float)
    order = np.argsort(land, kind="stable")
    out = np.full(len(ev), np.nan)
    k, hits = 0, 0.0
    for i in range(len(ev)):
        while k < len(ev) and land[order[k]] < t0[i]:
            hits += y[order[k]]
            k += 1
        if k:
            out[i] = hits / k
    return pd.Series(out, index=ev.index, name="base_rate").reindex(events.index)


def audit_extra_features(ohlcv: pd.DataFrame, market: pd.DataFrame | None, n_points: int,
                         rng: np.random.Generator) -> list[dict]:
    """Kesme testi: öznitelikler t'ye kadar kesilmiş veriyle yeniden hesaplandığında t satırı değişmemeli."""
    full = _bar_features(ohlcv, market, core=False)
    lo = min(300, len(ohlcv) - 1)
    points = np.sort(rng.choice(np.arange(lo, len(ohlcv)), size=min(n_points, len(ohlcv) - lo), replace=False))
    rows = []
    for p in points:
        t = ohlcv.index[p]
        cut = _bar_features(ohlcv.loc[:t], None if market is None else market.loc[:t], core=False).iloc[-1]
        ref = full.loc[t]
        ok = np.allclose(cut.to_numpy(dtype=float), ref.to_numpy(dtype=float), equal_nan=True, rtol=1e-9, atol=1e-12)
        bad = [c for c in full.columns
               if not np.isclose(cut[c], ref[c], equal_nan=True, rtol=1e-9, atol=1e-12)]
        rows.append({"timestamp": t, "status": "PASS" if ok else "FAIL", "features": ", ".join(bad) or "-"})
    return rows


def _bar_features(ohlcv, market, core: bool, cfg: ResearchConfig | None = None) -> pd.DataFrame:
    parts = [build_feature_matrix(ohlcv, cfg.features)] if core else []
    parts.append(trend_features(ohlcv))
    if market is not None:
        parts.append(market_features(market, ohlcv.index))
    return pd.concat(parts, axis=1)


# ------------------------------------------------------------------ maruziyet
def overlay_exposure(index: pd.DatetimeIndex, t0: pd.DatetimeIndex, t1: pd.Series, m: pd.Series,
                     default: float) -> pd.Series:
    """Karar barı bazında maruziyet: olay i [t0_i, t1_i) boyunca m_i önerir; eşzamanlılar ortalanır.

    m_i NaN olan (görüşü olmayan) olaylar yok sayılır; hiçbir olayın aktif olmadığı barlarda ``default``.
    """
    m = m.reindex(t0)
    ok = m.notna().to_numpy()
    start = index.get_indexer(t0[ok])
    end = index.get_indexer(pd.DatetimeIndex(t1.reindex(t0).to_numpy()[ok]))
    if (start < 0).any() or (end < 0).any():
        raise ValueError("olay zamanları fiyat indeksinde bulunamadı")
    n = len(index)
    s, c = np.zeros(n + 1), np.zeros(n + 1)
    vals = m.to_numpy()[ok]
    np.add.at(s, start, vals)
    np.add.at(s, end, -vals)
    np.add.at(c, start, 1.0)
    np.add.at(c, end, -1.0)
    s, c = np.cumsum(s)[:n], np.cumsum(c)[:n]
    active = c > 0.5
    out = np.full(n, float(default))
    out[active] = s[active] / c[active]
    return pd.Series(np.clip(out, 0.0, 1.0), index=index, name="exposure")


def vol_cap_series(vol: pd.Series, min_history: int) -> pd.Series:
    """min(1, σ_ref / σ_t); σ_ref = σ'nın t'ye kadarki genişleyen medyanı (geleceğe bakmaz)."""
    ref = vol.expanding(min_periods=min_history).median()
    return (ref / vol).clip(upper=1.0).fillna(1.0).rename("vol_cap")


# ------------------------------------------------------------------ çalışma
@dataclass
class OverlayStudyResult:
    ticker: str
    mode: str                                  # "dev" | "holdout"
    window: tuple[pd.Timestamp, pd.Timestamp]
    table: pd.DataFrame                        # strateji -> metrikler
    delta: dict[str, float]                    # sistem - B&H Sharpe, bootstrap CI ve p
    placebo: dict[str, float]
    diagnostics: dict[str, float]
    leakage: list[dict]
    returns: pd.DataFrame                      # günlük getiriler (strateji sütunları)
    exposure: pd.Series
    path: Path | None = None
    extras: dict = field(default_factory=dict)


def _simulate(target: pd.Series, ohlcv: pd.DataFrame, window, cfg: ResearchConfig, adv: pd.Series):
    win = ohlcv.loc[window[0]:window[1]]
    port = simulate_portfolio(target.reindex(win.index).fillna(0.0), win, cfg.execution, cfg.costs, cfg.risk, adv)
    return port, performance_metrics(port, segment_trades(port), cfg.execution.periods_per_year)


def paired_sharpe_bootstrap(a: pd.Series, b: pd.Series, reps: int, block: int, rng: np.random.Generator,
                            ppy: int) -> dict[str, float]:
    """Eşli durağan bootstrap: aynı gün blokları iki seriye birlikte uygulanır (korelasyon korunur)."""
    df = pd.concat([a, b], axis=1, join="inner").dropna().to_numpy()
    n = len(df)
    diffs = np.empty(reps)
    for r in range(reps):
        idx = stationary_bootstrap_indices(n, block, rng)
        diffs[r] = sharpe(df[idx, 0], ppy) - sharpe(df[idx, 1], ppy)
    point = sharpe(df[:, 0], ppy) - sharpe(df[:, 1], ppy)
    lo, hi = np.quantile(diffs, [0.025, 0.975])
    return {"ΔSharpe": point, "CI 2.5%": float(lo), "CI 97.5%": float(hi),
            "P(ΔSharpe ≤ 0)": float(np.mean(diffs <= 0)), "Tekrar": reps, "Blok": block}


def run_overlay_study(cfg: ResearchConfig, ticker: str, ohlcv: pd.DataFrame, market: pd.DataFrame | None,
                      *, dev: bool, out_dir: str | Path | None = None, dev_trials: int = 0,
                      write: bool = True) -> OverlayStudyResult:
    oc = cfg.overlay
    hs = pd.Timestamp(oc.holdout_start)
    ohlcv = validate_ohlcv(ohlcv)
    if market is not None:
        market = validate_ohlcv(market)
    if dev:  # kilitli test verisi HİÇ yüklenmez
        ohlcv = ohlcv.loc[ohlcv.index < hs]
        market = None if market is None else market.loc[market.index < hs]
    ocfg = replace(cfg, primary=replace(cfg.primary, kind="long"),
                   meta_model=replace(cfg.meta_model, use_side_feature=False))
    adv = adv_value(ohlcv, ocfg.costs.adv_window)
    ms = build_market_state(ohlcv, ocfg, adv)
    extra = []
    if oc.trend_features:
        extra.append(trend_features(ohlcv))
    if market is not None:
        extra.append(market_features(market, ohlcv.index))
    if extra:
        ms.features = pd.concat([ms.features, *extra], axis=1)

    ds = build_event_dataset(ms, ocfg, sample_candidate_events(ms, ocfg))
    tr = track_record_features(ds.events, oc.track_record_window)
    X = ds.X.join(tr)
    valid = X.notna().all(axis=1)
    ds = EventDataset(events=ds.events.loc[valid].copy(), X=X.loc[valid], market=ms)

    oos = walk_forward(ds, ocfg)
    cal = calibrate_walk_forward(oos, ds.y, ds.label_end, "isotonic", ocfg.calibration.min_history)
    rng = np.random.default_rng(ocfg.experiment.seed + 104729)
    leak_rows = audit_extra_features(ohlcv, market, 8, rng)
    core_leak = run_leakage_audit(
        ohlcv, ocfg, dataset=ds,
        splits={"walk_forward": (ds.label_end, [(trn, te) for _, trn, te in oos.splits], True)},
        calibration_windows={"isotonic": cal.fit_windows}, strict=False,
    )
    leak_rows += [{"timestamp": r["timestamp"], "status": r["status"], "features": f"{r['check']}: {r['item']}"}
                  for r in core_leak.findings.to_dict("records")]

    ev = ds.events.loc[oos.proba.notna()].copy()
    p = cal.proba.reindex(ev.index).fillna(oos.proba.reindex(ev.index))
    index = ohlcv.index
    vcap = vol_cap_series(ms.vol, oc.vol_cap_min_history) if oc.vol_cap else pd.Series(1.0, index=index)

    def kelly_exposure(prob: pd.Series):
        ck_ = conformal_kelly(prob, ev, ocfg.sizing.conformal, cap=1.0, threshold=-1.0, dial=False)
        opinion_ = ck_.q_eff.notna() & ck_.mu.notna()
        m_ = ck_.size_undialed.where(opinion_)
        return overlay_exposure(index, ev.index, ev["t1"], m_, oc.default_exposure), ck_, opinion_, m_

    meta_exp, ck, opinion, m = kelly_exposure(p)
    base_p = expanding_base_rate(ds.events).reindex(ev.index)
    base_exp = kelly_exposure(base_p)[0]
    system = meta_exp * vcap

    if dev:
        window = (ev.index[opinion.to_numpy()].min() if opinion.any() else ev.index.min(), index[-1])
    else:
        window = (index[index >= hs][0], index[-1])
    targets = {
        BH: pd.Series(1.0, index=index),
        "B&H x vol tavanı": vcap,
        "Kelly overlay, modelsiz (geçmiş isabet oranı) x vol tavanı": base_exp * vcap,
        "Meta overlay (vol tavanı yok)": meta_exp,
        SYSTEM: system,
    }
    ppy = ocfg.execution.periods_per_year
    rows, rets = {}, {}
    for name, tgt in targets.items():
        port, met = _simulate(tgt, ohlcv, window, ocfg, adv)
        rows[name] = met
        rets[name] = port.returns
    table = pd.DataFrame(rows).T
    returns = pd.DataFrame(rets)

    # Placebo: meta-modelin OLASILIKLARI olaylar arasında karıştırılır; σ_t0, ödeme geçmişi ve
    # vol tavanı aynı kalır. Model olasılığı bilgi taşımıyorsa gerçek sistem placebo'lardan ayrışmaz.
    ph = []
    pv = p.to_numpy()
    for _ in range(oc.placebo_reps):
        shuffled = pd.Series(rng.permutation(pv), index=ev.index)
        tgt = kelly_exposure(shuffled)[0] * vcap
        ph.append(_simulate(tgt, ohlcv, window, ocfg, adv)[1]["Sharpe"])
    ph = np.asarray(ph)
    real = float(table.loc[SYSTEM, "Sharpe"])
    placebo = {"Gerçek Sharpe": real, "Placebo medyan": float(np.median(ph)) if len(ph) else np.nan,
               "p-değeri": (1 + int(np.sum(ph >= real))) / (1 + len(ph)) if len(ph) else np.nan,
               "Tekrar": len(ph)}

    delta = paired_sharpe_bootstrap(returns[SYSTEM], returns[BH], oc.bootstrap_reps, oc.bootstrap_block, rng, ppy)
    trial_srs = np.array([r.mean() / r.std() for r in returns.T.values if np.std(r) > 0])
    n_trials = len(targets) + dev_trials
    dsr = deflated_sharpe(returns[SYSTEM], trial_srs, n_trials)

    in_win = (ev.index >= window[0]) & (ev.index <= window[1])
    evw, pw = ev.loc[in_win], p.loc[in_win]
    from sklearn.metrics import roc_auc_score
    exp_w = system.loc[window[0]:window[1]]
    diag = {
        "OOS olay (pencere)": int(in_win.sum()),
        "Long olay isabet oranı (baz)": float(evw["bin"].mean()) if len(evw) else np.nan,
        "AUC (kalibre p)": float(roc_auc_score(evw["bin"], pw)) if evw["bin"].nunique() == 2 else np.nan,
        "Görüş bildirilen olay": int(opinion.loc[in_win].sum()),
        "Çıkış önerilen olay (m=0)": int(((m == 0) & opinion).loc[in_win].sum()),
        "Ort. maruziyet (sistem)": float(exp_w.mean()),
        "Tam piyasada bar oranı (≥0.99)": float((exp_w >= 0.99).mean()),
        "Piyasa dışı bar oranı (≤0.01)": float((exp_w <= 0.01).mean()),
        "DSR (sistem)": float(dsr),
        "Deneme sayısı (DSR)": n_trials,
        "Kapsama (conformal)": ck.coverage_summary()["Gerçekleşen kapsama"],
        "Son b̂ = W̄/L̄": ck.coverage_summary()["Son ampirik b̂ = W̄/L̄"],
    }
    res = OverlayStudyResult(ticker, "dev" if dev else "holdout", window, table, delta, placebo, diag,
                             leak_rows, returns, system, extras={"placebo_sharpes": ph, "events": ev, "proba": p})
    if write:
        res.path = write_overlay_report(res, ocfg, out_dir or Path(ocfg.experiment.output_dir) / "overlay")
    return res


# ------------------------------------------------------------------ rapor
def _pct(x: float) -> str:
    return "n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:.1f}%"


def write_overlay_report(res: OverlayStudyResult, cfg: ResearchConfig, out_dir: str | Path) -> Path:
    out = Path(out_dir) / res.ticker
    out.mkdir(parents=True, exist_ok=True)
    cols = ["Sharpe", "CAGR", "Ann. Volatility", "Max Drawdown", "Sortino", "Calmar", "Trades", "Turnover", "Exposure"]
    t = res.table[[c for c in cols if c in res.table.columns]]
    pct = {"CAGR", "Ann. Volatility", "Max Drawdown", "Exposure"}
    lines = [f"# Long meta-labeling overlay — {res.ticker} ({'GELİŞTİRME' if res.mode == 'dev' else 'KİLİTLİ TEST'})\n",
             f"Pencere: {res.window[0].date()} → {res.window[1].date()} · maliyet {cfg.costs.commission_bps} bps/yön "
             f"+ spread {cfg.costs.spread_bps} bps · execution {cfg.execution.mode} · kaldıraç yok\n",
             "| Strateji | " + " | ".join(t.columns) + " |", "|" + "---|" * (len(t.columns) + 1)]
    for name, row in t.iterrows():
        cells = [_pct(v) if c in pct else (f"{int(v):,}" if c == "Trades" else f"{v:.3f}") for c, v in row.items()]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    d = res.delta
    lines += ["", "## Sistem − Buy&Hold Sharpe farkı (eşli durağan bootstrap)\n",
              f"ΔSharpe = {d['ΔSharpe']:+.3f}, %95 GA [{d['CI 2.5%']:+.3f}, {d['CI 97.5%']:+.3f}], "
              f"P(ΔSharpe ≤ 0) = {d['P(ΔSharpe ≤ 0)']:.3f} ({d['Tekrar']} tekrar, ort. blok {d['Blok']} gün)\n",
              "## Placebo: model olasılıkları olaylar arasında karıştırıldı (σ, ödeme geçmişi ve vol tavanı sabit)\n",
              f"Gerçek Sharpe {res.placebo['Gerçek Sharpe']:.3f} · placebo medyan {res.placebo['Placebo medyan']:.3f} · "
              f"p = {res.placebo['p-değeri']:.3f} ({res.placebo['Tekrar']} tekrar)\n",
              "## Teşhis\n", "| Ölçüt | Değer |", "|---|---|"]
    for k, v in res.diagnostics.items():
        lines.append(f"| {k} | {v if isinstance(v, (int, np.integer)) else f'{v:.3f}'} |")
    n_fail = sum(r["status"] == "FAIL" for r in res.leakage)
    lines += ["", f"## Sızıntı denetimi: {len(res.leakage)} kontrol, {n_fail} FAIL\n"]
    for r in res.leakage:
        if r["status"] == "FAIL":
            lines.append(f"- FAIL {r['timestamp']}: {r['features']}")
    path = out / f"overlay_{res.mode}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    res.table.to_csv(out / f"overlay_{res.mode}.csv")
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 7), height_ratios=[3, 1], sharex=True)
        for name in res.returns.columns:
            eq = (1 + res.returns[name]).cumprod()
            a1.plot(eq.index, eq, lw=1.3 if name in (SYSTEM, BH) else 0.9, label=f"{name} x{eq.iloc[-1]:.2f}")
        a1.set_yscale("log")
        a1.legend(frameon=False, fontsize=8)
        a1.set_title(f"{res.ticker} — long meta-labeling overlay ({res.mode})")
        exp = res.exposure.loc[res.window[0]:res.window[1]]
        a2.fill_between(exp.index, exp, step="post", alpha=0.5)
        a2.set_ylabel("Maruziyet")
        a2.set_ylim(0, 1.05)
        fig.tight_layout()
        fig.savefig(out / f"overlay_{res.mode}.png", dpi=110)
        plt.close(fig)
    except ImportError:  # pragma: no cover
        pass
    return path


def load_csv_ohlcv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return validate_ohlcv(df[["Open", "High", "Low", "Close", "Volume"]])


__all__ = [
    "OverlayStudyResult", "audit_extra_features", "market_features", "overlay_exposure", "paired_sharpe_bootstrap",
    "run_overlay_study", "track_record_features", "trend_features", "vol_cap_series",
]
