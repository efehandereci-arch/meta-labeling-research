"""Paper trading ayarları (``paper/config.yaml``). Bilinmeyen anahtarlar hata verir."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from pathlib import Path

from ..research.settings import ConfigError, ResearchConfig, load_research_config

# BIST 30, 1 Ekim - 31 Aralık 2026 dönemi (Borsa İstanbul 22.09.2026 duyurusu: DSTKF çıktı, TRMET girdi)
BIST30_2026Q4 = (
    "AEFES", "AKBNK", "ASELS", "ASTOR", "BIMAS", "EKGYO", "ENKAI", "EREGL", "FROTO", "GARAN",
    "GUBRF", "ISCTR", "KCHOL", "KRDMD", "MGROS", "PETKM", "PGSUS", "SAHOL", "SASA", "SISE",
    "TAVHL", "TCELL", "THYAO", "TOASO", "TRALT", "TRMET", "TTKOM", "TUPRS", "VAKBN", "YKBNK",
)


@dataclass(frozen=True)
class PaperConfig:
    capital: float = 1_000_000.0             # sanal başlangıç sermayesi (TL)
    tickers: tuple[str, ...] = BIST30_2026Q4
    suffix: str = ".IS"                      # yfinance sembol eki
    market_index: str = "XU100.IS"           # meta-model piyasa rejimi öznitelikleri
    benchmark_index: str = "XU030.IS"        # kıyas endeksi
    commission_bps: float = 10.0             # tek yön komisyon (BSMV dahil kabaca)
    slippage_bps: float = 5.0                # açılış fiyatına göre kayma
    min_trade_frac: float = 0.02             # hisse başı tahsisin %2'sinden küçük emirler atlanır
    research_config: str = "config.yaml"     # model / bariyer / overlay ayarları buradan
    state_dir: str = "paper"                 # state.json, equity.csv, trades.csv, decisions.csv, REPORT.md
    history_period: str = "max"
    min_history_bars: int = 750              # daha kısa geçmişte model görüşü yok -> tam long (B&H)

    def __post_init__(self):
        if self.capital <= 0:
            raise ValueError("capital > 0 olmalı")
        if not self.tickers:
            raise ValueError("tickers boş olamaz")
        if not 0 <= self.min_trade_frac < 1:
            raise ValueError("min_trade_frac [0, 1) aralığında olmalı")

    def research(self, base: Path | None = None) -> ResearchConfig:
        path = Path(self.research_config)
        if base is not None and not path.is_absolute():
            path = base / path
        return load_research_config(path)


def load_paper_config(path: str | Path) -> PaperConfig:
    import yaml

    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    names = {f.name for f in dataclasses.fields(PaperConfig)}
    unknown = set(raw) - names
    if unknown:
        raise ConfigError(f"paper config: bilinmeyen anahtar(lar) {sorted(unknown)}")
    if "tickers" in raw:
        raw["tickers"] = tuple(raw["tickers"])
    try:
        return PaperConfig(**raw)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"paper config: {exc}") from exc


__all__ = ["BIST30_2026Q4", "PaperConfig", "load_paper_config"]
