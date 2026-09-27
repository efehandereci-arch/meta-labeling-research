"""Veri sağlayıcıları: işlem fiyatları (ham), model fiyatları (düzeltilmiş), bölünme ve temettüler.

Yahoo'nun ``Close`` sütunu bölünmelere göre geriye dönük düzeltilir, temettülere göre düzeltilmez.
``Adj Close`` ikisine göre de düzeltilir. Bu yüzden:

* İşlem/değerleme: günün ham Open/Close'u (o gün gerçekten işlem gören fiyat).
* Model: düzeltilmiş OHLC = ham x (Adj Close / Close). Getiriler temettü ve bölünmeden bağımsızdır.
* Bölünme (BIST'te bedelsiz sermaye artırımı sık): ``Stock Splits`` oranı kadar lot artar.
* Temettü: ``Dividends`` x lot, hak kullanım günü nakde eklenir.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Protocol

import numpy as np
import pandas as pd

log = logging.getLogger("meta_labeling.paper")
RAW_COLUMNS = ["Open", "High", "Low", "Close", "Volume", "Adj Close", "Dividends", "Stock Splits"]


class Provider(Protocol):
    def fetch(self, symbols: list[str]) -> dict[str, pd.DataFrame]: ...


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Eksik aksiyon sütunlarını doldurur, tarihleri tz'siz güne indirger, boş satırları atar."""
    out = df.copy()
    if "Adj Close" not in out:
        out["Adj Close"] = out["Close"]
    for c in ("Dividends", "Stock Splits"):
        if c not in out:
            out[c] = 0.0
    out = out[RAW_COLUMNS].astype(float)
    idx = pd.DatetimeIndex(pd.to_datetime(out.index))
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    out.index = idx.normalize()
    out = out[~out.index.duplicated(keep="last")].sort_index()
    out = out.dropna(subset=["Open", "High", "Low", "Close"])
    out = out[(out["Close"] > 0) & (out["Open"] > 0)]
    out[["Dividends", "Stock Splits"]] = out[["Dividends", "Stock Splits"]].fillna(0.0)
    out["Volume"] = out["Volume"].fillna(0.0)
    out["Adj Close"] = out["Adj Close"].fillna(out["Close"])
    return out


def adjusted_ohlcv(raw: pd.DataFrame) -> pd.DataFrame:
    """Model için temettü + bölünme düzeltilmiş OHLCV."""
    f = (raw["Adj Close"] / raw["Close"]).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    adj = raw[["Open", "High", "Low", "Close"]].mul(f, axis=0)
    adj["Volume"] = raw["Volume"]
    return adj


class YFinanceProvider:
    """Tek toplu indirme + eksik semboller için sınırlı yeniden deneme (Yahoo hız sınırı)."""

    def __init__(self, period: str = "max", retries: int = 3, pause: float = 20.0):
        self.period, self.retries, self.pause = period, retries, pause

    def fetch(self, symbols: list[str]) -> dict[str, pd.DataFrame]:
        import yfinance as yf

        out: dict[str, pd.DataFrame] = {}
        todo = list(symbols)
        for attempt in range(self.retries):
            if not todo:
                break
            raw = yf.download(todo, period=self.period, auto_adjust=False, actions=True, group_by="ticker",
                              threads=True, progress=False)
            for s in list(todo):
                try:
                    df = raw[s] if isinstance(raw.columns, pd.MultiIndex) else raw
                    df = normalize(df.dropna(how="all"))
                except (KeyError, ValueError):
                    continue
                if len(df):
                    out[s] = df
                    todo.remove(s)
            if todo and attempt < self.retries - 1:
                log.warning("Eksik semboller %s; %ss sonra yeniden denenecek", todo, self.pause)
                time.sleep(self.pause)
        if todo:
            log.warning("Veri alınamadı: %s", todo)
        return out


class CsvProvider:
    """Çevrimdışı / geriye dönük prova: ``{data_dir}/{sembol}.csv``; ``as_of`` sonrası kesilir."""

    def __init__(self, data_dir: str | Path, as_of: pd.Timestamp | None = None):
        self.data_dir, self.as_of = Path(data_dir), as_of

    def fetch(self, symbols: list[str]) -> dict[str, pd.DataFrame]:
        out = {}
        for s in symbols:
            path = self.data_dir / f"{s}.csv"
            if not path.exists():
                continue
            df = normalize(pd.read_csv(path, index_col=0, parse_dates=True))
            if self.as_of is not None:
                df = df.loc[: self.as_of]
            if len(df):
                out[s] = df
        return out
