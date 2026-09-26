"""Teşhis analizleri: placebo testleri neden başarısız oluyor?

Bu modül yeni bir strateji varyantı SEÇMEZ; yalnızca mevcut ex-ante sistemin
davranışını parçalarına ayırır. Buradaki sonuçlara bakarak öznitelik, eşik
veya büyüklük seçmek OOS verisini model seçimine sızdırır.

1. Öznitelik bazında karıştırma: Her öznitelik TEK BAŞINA karıştırılıp model
   yeniden (walk-forward) eğitilir. Sharpe / CAGR / isabet oranı / turnover /
   AUC değişimi, model tohumu gürültüsüyle (karıştırma olmadan farklı tohumlar)
   karşılaştırılır. Gürültü bandının içinde kalan değişim = bilgi yok.
2. Olay zamanı placebo'su: CUSUM → rastgele zaman → tüm barlar → rastgele zaman
   + rastgele yön şemaları aynı modelle karşılaştırılır. Böylece getiri;
   zamanlama (CUSUM), yön (birincil model) ve filtre (meta-model) katkılarına
   ayrıştırılır.
3. Meta-model sınıflandırma kalitesi: precision, recall, PR-AUC, koşullu
   beklenti (alınan vs reddedilen işlemlerin net getirisi), kalibrasyon ve
   olasılık dilimleri (decile). Sharpe'tan bağımsız olarak "P(Y=1) gelecekteki
   koşullu getiriyi sıralıyor mu?" sorusunu yanıtlar.
4. Long / short ayrı modeller: Her yön için ayrı walk-forward meta-model;
   ortak (pooled) modelle ve yalnızca birincil sinyalle karşılaştırma.
5. Pozisyon büyüklüğü duyarlılığı: Mevcut sizing çıktısı 0.25x … 1.25x ile
   ölçeklenir (max_position üstü kırpılır; kaldıraç yok).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score

from .modeling import EventDataset, build_event_dataset, calibration_metrics, position_sizes, walk_forward

if TYPE_CHECKING:  # pragma: no cover
    from .session import ResearchSession

log = logging.getLogger("meta_labeling.research")


@dataclass
class DiagnosticsResult:
    seed_noise: dict[str, float]
    feature_randomization: pd.DataFrame
    event_time: pd.DataFrame
    classification: dict[str, float]
    conditional: pd.DataFrame
    deciles: pd.DataFrame
    long_short: pd.DataFrame
    sizing: pd.DataFrame
    explanations: list[str]
    markdown: str = ""
    path: Path | None = None
    figures: dict[str, Path] = field(default_factory=dict)


def _safe_auc(y, p) -> float:
    from sklearn.metrics import roc_auc_score

    mask = p.notna()
    return float(roc_auc_score(y[mask], p[mask])) if y[mask].nunique() == 2 else float("nan")


def _meta_metrics(s: ResearchSession, p: pd.Series, ev: pd.DataFrame, window=None) -> dict[str, float]:
    run = s.run_signal("diag", s.meta_signal(p, ev), ev["t1"], window=window)
    m = run.metrics
    return {"Sharpe": m["Sharpe"], "CAGR": m["CAGR"], "Hit rate": m["Win Rate"], "Turnover": m["Turnover"],
            "Trades": m["Trades"], "AUC": _safe_auc(ev["bin"], p)}


def _ensure_stages(s: ResearchSession) -> None:
    for step in (s.validate_data, s.build_features, s.sample_events, s.triple_barrier, s.walk_forward,
                 s.calibration, s.benchmarks, s.transaction_costs, s.feature_importance, s.statistical_tests):
        step()


# --------------------------------------------------------------------- 1
def seed_noise(s: ResearchSession) -> tuple[dict[str, float], list[dict]]:
    """Karıştırma olmadan yalnızca model tohumu değişince metrikler ne kadar oynuyor?

    Tohumlar öznitelik karıştırma tekrarlarıyla AYNIDIR (seed + r); böylece karıştırılmış ve
    karıştırılmamış modeller eşleştirilmiş tohumlarla karşılaştırılır. r=0 ana modeldir.
    """
    ds, ev, cfg = s.dataset, s.oos_events, s.cfg
    reps = max(cfg.diagnostics.seed_noise_reps, cfg.diagnostics.feature_shuffle_reps)
    runs = []
    for r in range(reps):
        p = walk_forward(ds, cfg, seed=cfg.experiment.seed + r).proba.reindex(ev.index)
        runs.append(_meta_metrics(s, p, ev))
    df = pd.DataFrame(runs)
    out = {f"{k} mean": float(df[k].mean()) for k in df.columns}
    out.update({"Sharpe sd": df["Sharpe"].std(ddof=1) if len(df) > 1 else np.nan,
                "AUC sd": df["AUC"].std(ddof=1) if len(df) > 1 else np.nan, "reps": len(df),
                "Ana model Sharpe": float(df["Sharpe"].iloc[0])})
    return out, runs


def feature_randomization(s: ResearchSession, noise: dict[str, float]) -> pd.DataFrame:
    ds, ev, cfg = s.dataset, s.oos_events, s.cfg
    # Referans: aynı tohumlarla eğitilmiş KARIŞTIRILMAMIŞ modellerin ortalaması (tek bir şanslı/şanssız
    # tohuma göre kıyaslamak farkları şişirir)
    base = {k: noise[f"{k} mean"] for k in ("Sharpe", "CAGR", "Hit rate", "Turnover", "AUC")}
    imp = s.results.get("importance", pd.DataFrame())
    band = 2 * noise["Sharpe sd"] if np.isfinite(noise["Sharpe sd"]) else np.nan
    rows = {}
    for j, col in enumerate(ds.X.columns):
        vals = []
        for r in range(cfg.diagnostics.feature_shuffle_reps):
            rng = s.rng(9000 + 100 * j + r)
            Xp = ds.X.copy()
            Xp[col] = rng.permutation(Xp[col].to_numpy())
            p = walk_forward(ds, cfg, X=Xp, seed=cfg.experiment.seed + r).proba.reindex(ev.index)
            vals.append(_meta_metrics(s, p, ev))
        v = pd.DataFrame(vals).mean()
        d_sharpe = v["Sharpe"] - base["Sharpe"]
        rows[col] = {
            "Sharpe (karıştırılmış)": v["Sharpe"],
            "ΔSharpe": d_sharpe,
            "ΔCAGR": v["CAGR"] - base["CAGR"],
            "ΔHit rate": v["Hit rate"] - base["Hit rate"],
            "ΔTurnover": v["Turnover"] - base["Turnover"],
            "ΔAUC": v["AUC"] - base["AUC"],
            "Permutation ΔAUC": imp["Permutation (ΔAUC)"].get(col, np.nan) if "Permutation (ΔAUC)" in imp else np.nan,
            "SHAP": imp.iloc[:, 2].get(col, np.nan) if imp.shape[1] >= 3 else np.nan,
            "MDI": imp["MDI"].get(col, np.nan) if "MDI" in imp else np.nan,
            "Bilgi taşıyor mu?": ("evet" if np.isfinite(band) and -d_sharpe > band
                                  else "hayır (gürültü bandında)" if np.isfinite(band) else "belirsiz"),
        }
    return pd.DataFrame(rows).T.sort_values("ΔSharpe")


# --------------------------------------------------------------------- 2
def _scheme(s: ResearchSession, t_events: pd.DatetimeIndex, market, seed: int) -> dict[str, float]:
    cfg = s.cfg
    ds_r = build_event_dataset(market, cfg, t_events, s.member_mask)
    oos = walk_forward(ds_r, cfg, seed=seed)
    ev_r = ds_r.events.loc[oos.proba.notna()].copy()
    ev_r["proba"] = oos.proba[oos.proba.notna()]
    if len(ev_r) < 20:
        raise ValueError("yetersiz OOS olayı")
    win = (ev_r.index.min(), ev_r["exit_time"].max())
    prim = s.run_signal("scheme_primary", ev_r["side"].astype(float), ev_r["t1"], window=win).metrics
    meta = s.run_signal("scheme_meta", s.meta_signal(ev_r["proba"], ev_r), ev_r["t1"], window=win).metrics
    return {"Olay": len(ds_r.events), "OOS olay": len(ev_r), "Y=1 oranı": ev_r["bin"].mean(),
            "Primary Sharpe": prim["Sharpe"], "Meta Sharpe": meta["Sharpe"],
            "Meta − Primary": meta["Sharpe"] - prim["Sharpe"], "AUC": _safe_auc(ev_r["bin"], ev_r["proba"])}


def event_time_placebo(s: ResearchSession) -> pd.DataFrame:
    cfg, ev = s.cfg, s.oos_events
    reps = cfg.diagnostics.event_placebo_reps
    pool = s.event_pool()
    n = min(len(s.t_events), len(pool))
    out: dict[str, list[dict]] = {}
    out["A) CUSUM olayları (gerçek sistem)"] = [{
        "Olay": len(s.dataset.events), "OOS olay": len(ev), "Y=1 oranı": ev["bin"].mean(),
        "Primary Sharpe": s._runs["Primary"].metrics["Sharpe"], "Meta Sharpe": s._runs["Meta"].metrics["Sharpe"],
        "Meta − Primary": s._runs["Meta"].metrics["Sharpe"] - s._runs["Primary"].metrics["Sharpe"],
        "AUC": _safe_auc(ev["bin"], ev["proba"])}]
    schemes = {
        "B) Rastgele zaman, birincil yön": lambda rng: (pool[np.sort(rng.choice(len(pool), n, replace=False))], s.market),
        "C) Rastgele zaman + rastgele yön": lambda rng: _random_side(s, pool[np.sort(rng.choice(len(pool), n, replace=False))], rng),
    }
    for name, make in schemes.items():
        out[name] = []
        for r in range(reps):
            rng = s.rng(11000 + 100 * len(out) + r)
            t_ev, market = make(rng)
            try:
                out[name].append(_scheme(s, t_ev, market, cfg.experiment.seed + r))
            except ValueError as exc:
                log.warning("%s tekrar %d atlandı: %s", name, r, exc)
    try:
        out["D) Tüm uygun barlar (yoğun örnekleme)"] = [_scheme(s, pool, s.market, cfg.experiment.seed)]
    except ValueError as exc:
        log.warning("Yoğun örnekleme atlandı: %s", exc)
    rows = {}
    for name, runs in out.items():
        if not runs:
            continue
        df = pd.DataFrame(runs)
        row = df.mean().to_dict()
        row["Tekrar"] = len(df)
        row["Meta Sharpe sd"] = df["Meta Sharpe"].std(ddof=1) if len(df) > 1 else np.nan
        row["Primary Sharpe sd"] = df["Primary Sharpe"].std(ddof=1) if len(df) > 1 else np.nan
        rows[name] = row
    return pd.DataFrame(rows).T


def _random_side(s: ResearchSession, t_ev: pd.DatetimeIndex, rng: np.random.Generator):
    side = pd.Series(0, index=s.ohlcv.index, dtype=int)
    side.loc[t_ev] = rng.choice([-1, 1], size=len(t_ev))
    return t_ev, replace(s.market, side=side)


# --------------------------------------------------------------------- 3
def classification_quality(s: ResearchSession) -> tuple[dict[str, float], pd.DataFrame, pd.DataFrame]:
    ev, cfg = s.oos_events, s.cfg
    thr = cfg.meta_model.threshold
    y, p, r = ev["bin"], ev["proba"], ev["exec_net_ret"]
    taken = p > thr
    cal, _ = calibration_metrics(p, y, cfg.calibration.n_bins)
    base = float(y.mean())
    pr_auc = float(average_precision_score(y, p)) if y.nunique() == 2 else np.nan
    rho, rho_p = stats.spearmanr(p, r)
    metrics = {
        "OOS olay": len(ev), "Baz oran (birincil precision)": base, "ROC-AUC": _safe_auc(y, p),
        "PR-AUC": pr_auc, "PR-AUC / baz oran": pr_auc / base if base > 0 else np.nan,
        f"Precision (p>{thr})": float(precision_score(y, taken, zero_division=0)),
        f"Recall (p>{thr})": float(recall_score(y, taken, zero_division=0)),
        f"F1 (p>{thr})": float(f1_score(y, taken, zero_division=0)),
        "Kapsama (alınan oran)": float(taken.mean()),
        "Brier": cal["Brier"], "ECE": cal["ECE"],
        "Spearman ρ (p, net getiri)": float(rho), "Spearman p-değeri": float(rho_p),
    }

    def grp(mask):
        g = r[mask]
        return {"n": int(mask.sum()), "İsabet": float(y[mask].mean()) if mask.any() else np.nan,
                "Ort. net getiri": float(g.mean()) if len(g) else np.nan,
                "Medyan net getiri": float(g.median()) if len(g) else np.nan,
                "Toplam net getiri": float(g.sum())}

    cond = pd.DataFrame({f"Alınan (p>{thr})": grp(taken), f"Reddedilen (p≤{thr})": grp(~taken),
                         "Tümü (birincil)": grp(pd.Series(True, index=ev.index))}).T
    if taken.sum() > 2 and (~taken).sum() > 2:
        t, pv = stats.ttest_ind(r[taken], r[~taken], equal_var=False)
        metrics["Koşullu beklenti farkı (alınan − reddedilen)"] = float(r[taken].mean() - r[~taken].mean())
        metrics["Welch t"], metrics["Welch p-değeri"] = float(t), float(pv)

    n = cfg.diagnostics.n_deciles
    q = pd.qcut(p.rank(method="first"), n, labels=range(1, n + 1))
    dec = pd.DataFrame({"p": p, "y": y, "r": r, "d": q}).groupby("d", observed=True).agg(
        n=("y", "size"), p_min=("p", "min"), p_max=("p", "max"), p_ort=("p", "mean"),
        isabet=("y", "mean"), ort_net_getiri=("r", "mean"))
    dec.index.name = "Dilim (1=düşük p)"
    dec["üstten kümülatif ort. getiri"] = (
        dec["ort_net_getiri"].mul(dec["n"])[::-1].cumsum() / dec["n"][::-1].cumsum())[::-1]
    mono, mono_p = stats.spearmanr(dec.index.astype(int), dec["ort_net_getiri"])
    metrics["Dilim monotonluğu ρ"], metrics["Dilim monotonluğu p"] = float(mono), float(mono_p)
    return metrics, cond, dec


# --------------------------------------------------------------------- 4
def long_short_models(s: ResearchSession) -> pd.DataFrame:
    ds, ev, cfg = s.dataset, s.oos_events, s.cfg
    rows = {}
    for label, sgn in (("Long", 1), ("Short", -1)):
        mask = ds.events["side"] == sgn
        sub = EventDataset(ds.events[mask], ds.X[mask], ds.market)
        ev_side = ev[ev["side"] == sgn]
        try:
            p_side = walk_forward(sub, cfg).proba.reindex(ev_side.index)
        except ValueError as exc:
            log.warning("%s modeli eğitilemedi: %s", label, exc)
            continue
        evc = ev_side.loc[p_side.notna()]
        if len(evc) < 20:
            continue
        pc = p_side.loc[evc.index]
        thr = cfg.meta_model.threshold
        for kind, sig, prob in (
            ("birincil sinyal", evc["side"].astype(float), None),
            ("ortak meta-model", s.meta_signal(evc["proba"], evc), evc["proba"]),
            ("ayrı meta-model", s.meta_signal(pc, evc), pc),
        ):
            m = s.run_signal(f"{label} {kind}", sig, evc["t1"]).metrics
            taken = prob > thr if prob is not None else pd.Series(True, index=evc.index)
            rows[f"{label} — {kind}"] = {
                "OOS olay": len(evc), "İşlem": m["Trades"], "İsabet": m["Win Rate"], "Sharpe": m["Sharpe"],
                "CAGR": m["CAGR"], "Max Drawdown": m["Max Drawdown"],
                "AUC": _safe_auc(evc["bin"], prob) if prob is not None else np.nan,
                "PR-AUC": float(average_precision_score(evc["bin"], prob))
                if prob is not None and evc["bin"].nunique() == 2 else np.nan,
                "Precision": float(evc["bin"][taken].mean()) if taken.any() else np.nan,
                "Baz oran": float(evc["bin"].mean()),
            }
    bh = s._runs["Buy&Hold"].metrics
    rows["Referans — Buy & Hold"] = {"İşlem": 1, "Sharpe": bh["Sharpe"], "CAGR": bh["CAGR"],
                                     "Max Drawdown": bh["Max Drawdown"]}
    return pd.DataFrame(rows).T


# --------------------------------------------------------------------- 5
def sizing_sensitivity(s: ResearchSession) -> pd.DataFrame:
    ev, cfg = s.oos_events, s.cfg
    cap = cfg.risk.max_position
    base = position_sizes(cfg.sizing.method, ev["proba"], ev, cfg)
    taken = base > 0
    rows = {}
    eq = s._runs["Meta"].metrics
    rows["Referans: eşit büyüklük (1.0)"] = {"Ort. büyüklük": 1.0, "Maks. büyüklük": 1.0, "Kırpılan %": 0.0,
                                             **{k: eq[k] for k in ("Exposure", "Turnover", "CAGR", "Sharpe",
                                                                   "Max Drawdown", "Calmar")}}
    for mult in cfg.diagnostics.sizing_multipliers:
        raw = base * mult
        size = raw.clip(upper=cap)
        m = s.run_signal(f"sizing x{mult}", ev["side"] * size, ev["t1"]).metrics
        rows[f"{cfg.sizing.method} x {mult:g}"] = {
            "Ort. büyüklük": float(size[taken].mean()) if taken.any() else 0.0,
            "Maks. büyüklük": float(size.max()),
            "Kırpılan %": float((raw[taken] > cap).mean()) if taken.any() else 0.0,
            **{k: m[k] for k in ("Exposure", "Turnover", "CAGR", "Sharpe", "Max Drawdown", "Calmar")},
        }
    return pd.DataFrame(rows).T


# --------------------------------------------------------------------- açıklamalar
def explanations(s: ResearchSession, noise, feats, events, cls, ls, sizing) -> list[str]:
    out = []
    informative = feats.index[feats["Bilgi taşıyor mu?"] == "evet"].tolist()
    band = 2 * noise["Sharpe sd"]
    main, mean = noise["Ana model Sharpe"], noise["Sharpe mean"]
    if np.isfinite(band) and abs(main - mean) > noise["Sharpe sd"]:
        out.append(f"Model tohumu hassasiyeti: raporlanan Meta Sharpe ({main:.2f}), {noise['reps']} tohumun ortalamasından "
                   f"({mean:.2f}) belirgin biçimde {'yüksek' if main > mean else 'düşük'}. Tek tohumlu sonuçlar "
                   "yorumlanırken bu belirsizlik hesaba katılmalı.")
    placebo = s.results.get("placebo")
    d_row = placebo.loc[[i for i in placebo.index if i.startswith("D)")]] if placebo is not None else None
    d_pass = (d_row is not None and len(d_row) and d_row["p-value"].iloc[0] < s.cfg.criteria.placebo_alpha)
    if not informative and d_pass:
        out.append(f"Hiçbir öznitelik TEK BAŞINA karıştırıldığında Sharpe tohum gürültü bandının (±{band:.2f}) dışında "
                   "düşmüyor, ancak TÜM öznitelikler birlikte karıştırıldığında (Placebo D) performans düşüyor. "
                   "Bilgi, birbirini ikame eden ilişkili özniteliklere yayılmış görünüyor (tek bir özniteliğe bağlı değil).")
    elif not informative:
        out.append(f"Hiçbir öznitelik tek başına karıştırıldığında Sharpe, model tohumu gürültü bandının "
                   f"(±{band:.2f}) dışında düşmüyor ve Placebo D de geçmedi: model bu özniteliklerden ayırt "
                   "edilebilir bilgi almıyor.")
    else:
        out.append(f"Bilgi taşıyan öznitelikler (karıştırılınca Sharpe gürültü bandından fazla düşüyor): "
                   f"{', '.join(informative)}.")
    cus = events.iloc[0]
    rnd = events.loc[events.index.str.startswith("B)")]
    if len(rnd):
        r = rnd.iloc[0]
        gap = cus["Primary Sharpe"] - r["Primary Sharpe"]
        sd = r.get("Primary Sharpe sd", np.nan)
        out.append(
            f"Zamanlama katkısı (CUSUM − rastgele zaman, birincil sinyal): {gap:+.2f} Sharpe "
            f"(rastgele şema sd {sd:.2f}). " + ("CUSUM zamanlaması rastgele zamanlamadan ayrışmıyor; Placebo C "
                                                "başarısızlığı bununla açıklanabilir." if np.isfinite(sd) and abs(gap) < 2 * sd
                                                else "CUSUM zamanlaması rastgele zamanlamadan ayrışıyor."))
        out.append(f"Filtre katkısı (Meta − Primary): CUSUM olaylarında {cus['Meta − Primary']:+.2f}, rastgele "
                   f"zamanlarda {r['Meta − Primary']:+.2f} Sharpe.")
    rs = events.loc[events.index.str.startswith("C)")]
    if len(rs) and len(rnd):
        out.append(f"Yön katkısı (birincil yön − rastgele yön, rastgele zamanlarda): "
                   f"{rnd.iloc[0]['Primary Sharpe'] - rs.iloc[0]['Primary Sharpe']:+.2f} Sharpe.")
    rho, rho_p = cls["Dilim monotonluğu ρ"], cls["Dilim monotonluğu p"]
    out.append(f"P(Y=1) dilimleri koşullu getiriyi {'monoton biçimde sıralıyor' if rho > 0.6 and rho_p < 0.05 else 'güvenilir biçimde sıralamıyor'} "
               f"(ρ={rho:.2f}, p={rho_p:.3f}); PR-AUC / baz oran = {cls['PR-AUC / baz oran']:.2f} "
               "(1.0 = rastgele).")
    if "Welch p-değeri" in cls:
        out.append(f"Alınan − reddedilen işlem net getiri farkı {100 * cls['Koşullu beklenti farkı (alınan − reddedilen)']:+.2f}% "
                   f"(Welch p={cls['Welch p-değeri']:.3f}).")
    if {"Long — ayrı meta-model", "Short — ayrı meta-model"} <= set(ls.index):
        lsr, ssr = ls.loc["Long — birincil sinyal", "Sharpe"], ls.loc["Short — birincil sinyal", "Sharpe"]
        out.append(f"Yön asimetrisi: birincil sinyal Long SR {lsr:.2f}, Short SR {ssr:.2f}. "
                   + ("Short tarafı negatif; getiri long-only yapıyla ve piyasa trendiyle ilişkili olabilir. "
                      "Açığa satış kısıtları (ör. BIST) varsa long-only değerlendirme daha gerçekçidir."
                      if ssr < 0 < lsr else ""))
    ab = s.results["alpha_beta"].loc["Meta"]
    out.append(f"Piyasa maruziyeti: Meta beta {ab['beta']:.2f}, yıllık alpha {100 * ab['alpha_ann']:.1f}% "
               f"(t={ab['alpha_t']:.2f}), Buy&Hold Sharpe {s._runs['Buy&Hold'].metrics['Sharpe']:.2f}.")
    unit = [i for i in sizing.index if i.endswith("x 1")]
    if unit:
        u = sizing.loc[unit[0]]
        sr = sizing.iloc[1:]["Sharpe"].astype(float)
        out.append(f"Pozisyon büyüklüğü: {s.cfg.sizing.method} yöntemi alınan işlemlerde ortalama {u['Ort. büyüklük']:.2f} "
                   f"büyüklük üretiyor (eşit büyüklük = 1.0). Çarpanlar arasında Sharpe {sr.min():.2f}–{sr.max():.2f} "
                   "aralığında kalırken CAGR büyüklükle ölçekleniyor: düşük CAGR edge kaybından çok düşük "
                   "maruziyetin sonucudur. Çarpan OOS'a bakarak seçilmemelidir.")
    return out


# --------------------------------------------------------------------- rapor
def run_diagnostics(s: ResearchSession) -> DiagnosticsResult:
    _ensure_stages(s)
    log.info("Teşhis: tohum gürültüsü")
    noise, _ = seed_noise(s)
    log.info("Teşhis: öznitelik bazında karıştırma")
    feats = feature_randomization(s, noise)
    log.info("Teşhis: olay zamanı placebo'su")
    events = event_time_placebo(s)
    log.info("Teşhis: sınıflandırma kalitesi")
    cls, cond, dec = classification_quality(s)
    log.info("Teşhis: long/short modelleri")
    ls = long_short_models(s)
    log.info("Teşhis: sizing duyarlılığı")
    sizing = sizing_sensitivity(s)
    res = DiagnosticsResult(noise, feats, events, cls, cond, dec, ls, sizing,
                            explanations(s, noise, feats, events, cls, ls, sizing))
    if s.cfg.experiment.save_figures:
        res.figures = _plots(s, res)
    res.markdown = _markdown(s, res)
    s.out_dir.mkdir(parents=True, exist_ok=True)
    res.path = s.out_dir / "diagnostics_report.md"
    res.path.write_text(res.markdown, encoding="utf-8")
    log.info("Teşhis raporu: %s", res.path)
    return res


def _markdown(s: ResearchSession, res: DiagnosticsResult) -> str:
    from .report import md_table

    pct = {"CAGR", "ΔCAGR", "ΔHit rate", "Hit rate", "İsabet", "Y=1 oranı", "Max Drawdown", "Exposure",
           "Kırpılan %", "Precision", "Baz oran", "isabet", "Ort. net getiri", "Medyan net getiri",
           "ort_net_getiri", "üstten kümülatif ort. getiri", "Toplam net getiri"}
    cls = pd.DataFrame({"Değer": res.classification}).rename_axis("Metrik")
    L = [f"# Teşhis raporu — {s.ticker}\n",
         "> Yalnızca raporlama: bu sonuçlara bakarak öznitelik, eşik veya büyüklük seçilmemelidir.\n",
         "## Olası açıklamalar (otomatik)\n", *[f"- {x}" for x in res.explanations], "",
         "## 1. Öznitelik bazında karıştırma\n",
         f"Her öznitelik tek başına karıştırılıp model yeniden eğitildi ({s.cfg.diagnostics.feature_shuffle_reps} tekrar "
         f"ortalaması). Δ değerleri, AYNI tohumlarla eğitilmiş karıştırılmamış modellerin ortalamasına göredir "
         f"(Sharpe ort. {res.seed_noise['Sharpe mean']:.2f}, sd {res.seed_noise['Sharpe sd']:.3f}, "
         f"{res.seed_noise['reps']} tohum; ana model {res.seed_noise['Ana model Sharpe']:.2f}). "
         "'Bilgi taşıyor' = Sharpe düşüşü > 2 sd. Az tohumla sd tahmini kaba bir göstergedir.\n",
         md_table(res.feature_randomization, pct),
         "## 2. Olay zamanı placebo'su (CUSUM → rastgele → model)\n",
         "Zamanlama katkısı = A − B (Primary Sharpe); yön katkısı = B − C; filtre katkısı = Meta − Primary.\n",
         md_table(res.event_time, pct),
         "## 3. Meta-model sınıflandırma kalitesi (OOS)\n", md_table(cls, set()),
         "### Koşullu beklenti\n", md_table(res.conditional, pct),
         "### Olasılık dilimleri\n", md_table(res.deciles, pct),
         "## 4. Long / short ayrı modeller\n", md_table(res.long_short, pct),
         "## 5. Pozisyon büyüklüğü duyarlılığı\n",
         f"Çarpan x mevcut `{s.cfg.sizing.method}` büyüklüğü; max_position={s.cfg.risk.max_position} üstü kırpılır "
         "(kaldıraç yok). Yalnızca duyarlılık; çarpan OOS'a göre seçilmez.\n",
         md_table(res.sizing, pct)]
    for key, alt in (("deciles", "deciles"), ("features", "feature randomization")):
        if key in res.figures:
            L.append(f"\n![{alt}]({res.figures[key].relative_to(s.out_dir).as_posix()})\n")
    return "\n".join(L)


def _plots(s: ResearchSession, res: DiagnosticsResult) -> dict[str, Path]:
    try:
        from .plots import INK, INK_MUTED, LOSS, SURFACE, WIN, _plt, _style
        plt = _plt()
    except ImportError:
        return {}
    fig_dir = s.out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    out = {}

    dec = res.deciles
    fig, ax = plt.subplots(figsize=(10, 4.2), facecolor=SURFACE)
    vals = dec["ort_net_getiri"].to_numpy() * 100
    x = np.arange(len(dec))
    ax.bar(x, vals, width=0.5, color=[WIN if v >= 0 else LOSS for v in vals], edgecolor=SURFACE, linewidth=2)
    for xi, v, h in zip(x, vals, dec["isabet"]):
        ax.annotate(f"{v:+.2f}%\nisabet {100 * h:.0f}%", xy=(xi, v), xytext=(0, 4 if v >= 0 else -24),
                    textcoords="offset points", ha="center", fontsize=7.5, color=INK)
    ax.axhline(0, color=INK_MUTED, lw=1)
    ax.set_xticks(x, [f"{i}\n{lo:.2f}–{hi:.2f}" for i, lo, hi in zip(dec.index, dec["p_min"], dec["p_max"])], fontsize=8)
    _style(ax, f"{s.ticker}: P(Y=1) dilimlerine göre ortalama net işlem getirisi (OOS)", "Ort. net getiri (%)")
    ax.set_xlabel("Olasılık dilimi (1 = en düşük P(Y=1)) ve aralığı", color=INK_MUTED, fontsize=9)
    fig.tight_layout()
    out["deciles"] = fig_dir / "diagnostics_deciles.png"
    fig.savefig(out["deciles"], dpi=120, facecolor=SURFACE)
    plt.close(fig)

    fr = res.feature_randomization
    fig, ax = plt.subplots(figsize=(9, 0.42 * len(fr) + 1.5), facecolor=SURFACE)
    band = 2 * res.seed_noise["Sharpe sd"]
    y = np.arange(len(fr))
    d = fr["ΔSharpe"].astype(float).to_numpy()
    if np.isfinite(band):
        ax.axvspan(-band, band, color=INK_MUTED, alpha=0.12, lw=0)
        ax.annotate("tohum gürültüsü ±2 sd", xy=(band, len(fr) - 0.5), xytext=(4, 0), textcoords="offset points",
                    fontsize=8, color=INK_MUTED, va="center")
    ax.barh(y, d, height=0.5, color=[LOSS if v < 0 else WIN for v in d], edgecolor=SURFACE, linewidth=2)
    for yi, v in zip(y, d):
        ax.annotate(f"{v:+.2f}", xy=(v, yi), xytext=(4 if v >= 0 else -4, 0), textcoords="offset points",
                    ha="left" if v >= 0 else "right", va="center", fontsize=8, color=INK)
    ax.axvline(0, color=INK_MUTED, lw=1)
    ax.set_yticks(y, fr.index, fontsize=9)
    ax.grid(axis="x", color="#e6e5e0", lw=1)
    _style(ax, f"{s.ticker}: öznitelik tek başına karıştırılınca Meta Sharpe değişimi", None)
    ax.set_xlabel("ΔSharpe (negatif = model bu öznitelikten bilgi alıyor)", color=INK_MUTED, fontsize=9)
    fig.tight_layout()
    out["features"] = fig_dir / "diagnostics_features.png"
    fig.savefig(out["features"], dpi=120, facecolor=SURFACE)
    plt.close(fig)
    return out
