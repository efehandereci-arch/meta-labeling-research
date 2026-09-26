"""Frekans çalışması: aynı sistem, üç veri frekansı (düşük / orta / yüksek).

Kural: Strateji parametreleri (EMA pencereleri, CUSUM, bariyer katsayıları, dikey
bariyer, öznitelik pencereleri, eşik, model) BAR cinsinden birebir aynı kalır.
Yalnızca veri frekansı ve Sharpe yıllıklandırması (``periods_per_year``)
değişir. Böylece "aynı ex-ante sistem farklı zaman ölçeklerinde ne yapıyor?"
sorusu, frekansa özel parametre ayarı (= overfitting) yapılmadan yanıtlanır.

Dikkat:
* Dikey bariyer 10 bar = günlükte ~2 hafta, saatlikte ~1.5 gün, 5 dakikalıkta
  50 dakikadır. Aynı parametre farklı ekonomik ufuklar demektir.
* yfinance intraday geçmişi kısadır (1h: ~730 gün, 5m: ~60 gün). Örneklem
  uzunlukları farklı olduğu için Sharpe tahminlerinin belirsizliği de farklıdır;
  güven aralıklarına bakılmalıdır.
* "Yüksek frekans" burada 5 dakikalık bar demektir; tick verisi, mikro-saniye
  gecikme ve emir defteri modellemesi gerektiren gerçek HFT değildir.
* ``min_target`` (0.002) bar volatilitesiyle karşılaştırılır. 5 dakikalık bar
  volatilitesi çoğu zaman bunun altındadır; bu kural "beklenen hareket
  maliyeti karşılamıyorsa işlem yapma" anlamına gelir ve bilerek değiştirilmez.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

from .report import _fmt
from .session import InsufficientDataError, ResearchSession
from .settings import FrequencyProfile, ResearchConfig

log = logging.getLogger("meta_labeling.research")


@dataclass
class FrequencyStudyResult:
    table: pd.DataFrame
    sessions: dict[str, ResearchSession | None]
    markdown: str
    path: Path
    figure: Path | None


def profile_config(cfg: ResearchConfig, profile: FrequencyProfile, ticker: str) -> ResearchConfig:
    fs = cfg.frequency_study
    return replace(
        cfg,
        data=replace(cfg.data, source="yfinance", tickers=(ticker,), yfinance_suffix=fs.yfinance_suffix,
                     yfinance_interval=profile.interval, yfinance_period=profile.period, start=None, end=None),
        execution=replace(cfg.execution, periods_per_year=profile.periods_per_year),
        experiment=replace(cfg.experiment,
                           output_dir=str(Path(cfg.experiment.output_dir) / f"freq_{profile.name}")),
    )


def _row(session: ResearchSession, profile: FrequencyProfile, root: Path) -> dict:
    rep = session.results["report"]
    runs = session._runs
    st = session.results["stats"]
    d = session.results["data"]
    return {
        "Bar": profile.bar_duration,
        "Veri": f"{d['start']} → {d['end']}",
        "Bar sayısı": d["bars"],
        "Olay": len(session.dataset.events),
        "OOS olay": session.results["oos"]["n_oos"],
        "Tutma ufku": f"{session.cfg.barriers.max_holding_bars} × {profile.bar_duration}",
        "AUC": session.results["oos"]["auc"],
        "Primary Sharpe": runs["Primary"].metrics["Sharpe"],
        "Meta Sharpe": runs["Meta"].metrics["Sharpe"],
        "Meta+Sizing Sharpe": runs["Meta+Sizing"].metrics["Sharpe"],
        "Buy&Hold Sharpe": runs["Buy&Hold"].metrics["Sharpe"],
        "Meta Sharpe %95 CI": f"[{st.loc['Meta', 'Block CI low']:.2f}, {st.loc['Meta', 'Block CI high']:.2f}]",
        "Meta DSR": st.loc["Meta", "DSR"],
        "Meta işlem": runs["Meta"].metrics["Trades"],
        "Karar": rep.verdict,
        "Rapor": rep.path.relative_to(root).as_posix() if rep.path.is_relative_to(root) else str(rep.path),
    }


def run_frequency_study(
    cfg: ResearchConfig,
    ticker: str | None = None,
    data: dict[str, pd.DataFrame] | None = None,
) -> FrequencyStudyResult:
    """Config'deki her frekans profili için tam araştırma çalıştırması ve karşılaştırma tablosu.

    Args:
        cfg: Temel konfigürasyon (strateji parametreleri değiştirilmez).
        ticker: Varsayılan ``frequency_study.ticker`` (AAPL).
        data: {profil_adı: OHLCV} verilirse indirme yerine bu veri kullanılır (çevrimdışı/test).
    """
    fs = cfg.frequency_study
    ticker = ticker or fs.ticker
    root = Path(cfg.experiment.output_dir)
    rows, sessions = {}, {}
    for profile in fs.profiles:
        pcfg = profile_config(cfg, profile, ticker)
        log.info("=== %s: %s (%s, %s) ===", ticker, profile.label, profile.interval, profile.period)
        session = None
        try:
            if data is not None and profile.name in data:
                session = ResearchSession.from_ohlcv(pcfg, ticker, data[profile.name],
                                                     source=f"custom ({profile.interval})")
            else:
                session = ResearchSession(pcfg, ticker)
            session.run_all()
            rows[profile.label] = _row(session, profile, root)
            if cfg.diagnostics.run_in_frequency_study:
                diag = session.diagnostics()
                rows[profile.label]["Teşhis"] = (diag.path.relative_to(root).as_posix()
                                                 if diag.path.is_relative_to(root) else str(diag.path))
        except InsufficientDataError as exc:
            log.warning("%s: yetersiz veri — %s", profile.label, exc)
            bars = len(session.ohlcv) if session is not None and session.ohlcv is not None else np.nan
            rows[profile.label] = {"Bar": profile.bar_duration, "Bar sayısı": bars,
                                   "Karar": f"Test edilemedi — yetersiz veri: {exc}"}
        sessions[profile.label] = session
    table = pd.DataFrame(rows).T
    table.index.name = "Frekans"

    root.mkdir(parents=True, exist_ok=True)
    stem = root / f"frequency_study_{ticker}"
    table.to_csv(f"{stem}.csv")
    figure = _plot(table, ticker, Path(f"{stem}.png")) if cfg.experiment.save_figures else None
    markdown = _markdown(table, ticker, cfg, figure, root)
    path = Path(f"{stem}.md")
    path.write_text(markdown, encoding="utf-8")
    log.info("Frekans çalışması: %s", path)
    return FrequencyStudyResult(table, sessions, markdown, path, figure)


def _markdown(table: pd.DataFrame, ticker: str, cfg: ResearchConfig, figure: Path | None, root: Path) -> str:
    b, m = cfg.barriers, cfg.meta_model
    cols = ["Bar", "Veri", "OOS olay", "Tutma ufku", "AUC", "Primary Sharpe", "Meta Sharpe",
            "Meta+Sizing Sharpe", "Buy&Hold Sharpe", "Meta Sharpe %95 CI", "Meta DSR", "Karar"]
    cols = [c for c in cols if c in table.columns]
    header = "| Frekans | " + " | ".join(cols) + " |"
    lines = [header, "|" + "---|" * (len(cols) + 1)]
    for idx, row in table.iterrows():
        cells = [_fmt(row.get(c), False, c in {"OOS olay"}) for c in cols]
        lines.append(f"| {idx} | " + " | ".join(cells) + " |")
    img = f"\n![Sharpe by frequency]({figure.relative_to(root).as_posix()})\n" if figure else ""
    return "\n".join([
        f"# Frekans çalışması — {ticker}\n",
        "> Araştırma/backtest çıktısıdır; yatırım tavsiyesi değildir ve gelecek getiri tahmini içermez.\n",
        f"Aynı ex-ante sistem (EMA {cfg.primary.ema_fast}/{cfg.primary.ema_slow}, CUSUM, bariyer "
        f"{b.pt_mult}σ/{b.sl_mult}σ, dikey bariyer {b.max_holding_bars} bar, eşik {m.threshold}, "
        f"maliyet {cfg.cost_per_side * 1e4:.0f} bps/yön, execution {cfg.execution.mode}) üç veri frekansında "
        "çalıştırıldı. Strateji parametreleri bar cinsinden aynıdır; yalnızca veri frekansı ve Sharpe "
        "yıllıklandırması değişir.\n",
        "\n".join(lines),
        img,
        "## Yorumlarken dikkat\n",
        "- Örneklem uzunlukları farklıdır (yfinance intraday geçmişi kısadır); kısa örneklemde Sharpe güven "
        "aralığı geniştir.",
        "- Aynı bar sayısı farklı ekonomik ufuklar demektir (dikey bariyer: bkz. 'Tutma ufku').",
        "- 5 dakikalık barlar 'yüksek frekans' olarak etiketlenmiştir; tick verisi ve emir defteri "
        "modellemesi gerektiren gerçek HFT değildir.",
        "- Sabit bps maliyet, intraday'de işlem sayısı arttıkça sonuca daha fazla etki eder.",
        "- Sonuçlar tek bir hisseye aittir ve hisse ex-post seçilmiştir (seçim yanlılığı).",
        "- Her frekansın ayrıntılı 25 bölümlük raporu 'Rapor', placebo teşhisleri 'Teşhis' sütunundaki dosyadadır.\n",
    ])


def _plot(table: pd.DataFrame, ticker: str, path: Path) -> Path | None:
    try:
        from .plots import INK, INK_MUTED, STRATEGY_COLORS, SURFACE, _plt, _style
        plt = _plt()
    except ImportError:
        return None
    # Test edilebilen tüm frekanslar gösterilir; işlem olmayan strateji "n/a" olarak etiketlenir
    ok = table[table["Primary Sharpe"].notna()] if "Primary Sharpe" in table else table.iloc[:0]
    if ok.empty:
        return None
    names = list(STRATEGY_COLORS)
    x = np.arange(len(ok))
    width, step = 0.075, 0.095
    fig, ax = plt.subplots(figsize=(10, 4.6), facecolor=SURFACE)
    for i, name in enumerate(names):
        vals = ok[f"{name} Sharpe"].astype(float).to_numpy()
        pos = x + (i - 1.5) * step
        ax.bar(pos, np.nan_to_num(vals), width=width, color=STRATEGY_COLORS[name], edgecolor=SURFACE,
               linewidth=2, label=name)
        for px, v in zip(pos, vals):
            text, y = (f"{v:.2f}", v) if np.isfinite(v) else ("n/a", 0.0)
            ax.annotate(text, xy=(px, y), xytext=(0, 3 if y >= 0 else -11), textcoords="offset points",
                        ha="center", fontsize=8, color=INK)
    ax.axhline(0, color=INK_MUTED, lw=1)
    ax.set_xticks(x, [f"{idx}\n({ok.loc[idx, 'Veri']})" for idx in ok.index], fontsize=9)
    _style(ax, f"{ticker}: örneklem dışı Sharpe oranı — aynı sistem, üç frekans", "Yıllıklandırılmış Sharpe")
    ax.legend(frameon=False, fontsize=9, labelcolor=INK, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    fig.tight_layout()
    fig.savefig(path, dpi=130, facecolor=SURFACE)
    plt.close(fig)
    return path
