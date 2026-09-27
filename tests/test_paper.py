"""Paper trading motoru: muhasebe, dolum zamanlaması, bölünme, temettü, olay yaşam döngüsü."""

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

import meta_labeling.paper.engine as engine
from meta_labeling.paper.config import ConfigError, PaperConfig, load_paper_config
from meta_labeling.paper.data import adjusted_ohlcv, normalize
from meta_labeling.paper.engine import BUYHOLD, SYSTEM, PaperState, run_day
from meta_labeling.paper.signals import Decision, event_active
from meta_labeling.research.settings import ResearchConfig

DAYS = pd.bdate_range("2026-01-05", periods=6)


def frame(opens, closes, splits=None, divs=None):
    n = len(opens)
    return normalize(pd.DataFrame({"Open": opens, "High": np.maximum(opens, closes), "Low": np.minimum(opens, closes),
                                   "Close": closes, "Volume": 1e6, "Adj Close": closes,
                                   "Dividends": divs or [0.0] * n, "Stock Splits": splits or [0.0] * n},
                                  index=DAYS[:n]))


class Fake:
    def __init__(self, data):
        self.data = data

    def fetch(self, symbols):
        return {s: df for s, df in self.data.items() if s in symbols}


def cut(data, k):
    return Fake({s: df.iloc[:k] for s, df in data.items()})


@pytest.fixture
def const_decision(monkeypatch):
    """Model yerine sabit maruziyet: vol tavanı 1, olay yok -> maruziyet = default (1.0)."""
    def fake(adj, market, cfg, min_history_bars):
        return Decision(adj.index[-1], 1.0, 0.02, False)
    monkeypatch.setattr(engine, "decide", fake)


def pc(**kw):
    return replace(PaperConfig(capital=10_000.0, tickers=("AAA", "BBB"), suffix="", market_index="MKT",
                               benchmark_index="IDX", commission_bps=10.0, slippage_bps=0.0, min_trade_frac=0.0), **kw)


def data(**over):
    d = {"AAA": frame([10, 10, 11, 12, 12, 13], [10, 10.5, 11.5, 12, 12.5, 13]),
         "BBB": frame([20, 20, 19, 18, 18, 17], [20, 19.5, 18.5, 18, 17.5, 17]),
         "MKT": frame([100] * 6, [100, 101, 102, 103, 104, 105]),
         "IDX": frame([100] * 6, [100, 101, 102, 103, 104, 105])}
    d.update(over)
    return d


def test_orders_fill_next_open_with_costs_and_books_balance(tmp_path, const_decision):
    p, rc, dd = pc(), ResearchConfig(), data()
    r0 = run_day(p, rc, cut(dd, 1), tmp_path)             # ilk gün: yalnızca karar, dolum yok
    assert r0["trades"] == 0
    st = PaperState.load(tmp_path / "state.json", p.capital)
    assert st.books[SYSTEM].pending == {"AAA": 499, "BBB": 249}   # 5000 TL / (kapanış x 1.001)
    run_day(p, rc, cut(dd, 2), tmp_path)
    tr = pd.read_csv(tmp_path / "trades.csv")
    sysb = tr[tr.portfolio == SYSTEM].set_index("ticker")
    assert sysb.loc["AAA", "price"] == 10 and sysb.loc["BBB", "price"] == 20   # 2. günün AÇILIŞI
    assert sysb["cost"].sum() == pytest.approx(0.001 * (499 * 10 + 249 * 20))
    st = PaperState.load(tmp_path / "state.json", p.capital)
    eq = pd.read_csv(tmp_path / "equity.csv").iloc[-1]
    for name in (SYSTEM, BUYHOLD):
        b = st.books[name]
        v = b.cash + b.positions.get("AAA", 0) * 10.5 + b.positions.get("BBB", 0) * 19.5
        assert v == pytest.approx(eq[name]) and b.cash >= 0
    assert run_day(p, rc, cut(dd, 2), tmp_path)["status"] == "no-new-day"   # aynı gün tekrar -> değişiklik yok


def test_catch_up_processes_every_missed_day_but_decides_once(tmp_path, const_decision):
    p, rc, dd = pc(), ResearchConfig(), data()
    run_day(p, rc, cut(dd, 1), tmp_path)
    r = run_day(p, rc, cut(dd, 5), tmp_path)
    assert r["days"] == [str(d.date()) for d in DAYS[1:5]]
    eq = pd.read_csv(tmp_path / "equity.csv")
    assert len(eq) == 5
    dec = pd.read_csv(tmp_path / "decisions.csv")
    assert set(dec.date) == {str(DAYS[0].date()), str(DAYS[4].date())}


def test_split_scales_shares_and_dividend_goes_to_prefill_holders(tmp_path, const_decision):
    p, rc = pc(), ResearchConfig()
    dd = data(AAA=frame([10, 10, 5, 5, 5, 5], [10, 10, 5, 5, 5, 5], splits=[0, 0, 2.0, 0, 0, 0],
                        divs=[0, 0, 0, 0.5, 0, 0]),
              BBB=frame([20] * 6, [20] * 6))            # BBB sabit: değer değişimi yalnızca AAA'dan
    run_day(p, rc, cut(dd, 1), tmp_path)
    run_day(p, rc, cut(dd, 2), tmp_path)                  # 499 lot AAA alındı
    st = PaperState.load(tmp_path / "state.json", p.capital)
    assert st.books[BUYHOLD].positions["AAA"] == 499
    run_day(p, rc, cut(dd, 3), tmp_path)                  # bölünme günü
    st = PaperState.load(tmp_path / "state.json", p.capital)
    assert st.books[BUYHOLD].positions["AAA"] == 998
    cash_before = st.books[BUYHOLD].cash
    run_day(p, rc, cut(dd, 4), tmp_path)                  # temettü günü
    st = PaperState.load(tmp_path / "state.json", p.capital)
    assert st.books[BUYHOLD].cash == pytest.approx(cash_before + 998 * 0.5)
    eq = pd.read_csv(tmp_path / "equity.csv")["buyhold"]
    assert eq.iloc[2] == pytest.approx(eq.iloc[1])        # bölünme (10 -> 5, lot x2) değeri değiştirmez


def test_buys_are_scaled_down_when_cash_is_short(tmp_path, monkeypatch):
    p, rc, dd = pc(), ResearchConfig(), data()
    calls = {"n": 0}

    def fake(adj, market, cfg, min_history_bars):
        return Decision(adj.index[-1], 1.0, 0.02, False)
    monkeypatch.setattr(engine, "decide", fake)
    run_day(p, rc, cut(dd, 1), tmp_path)
    st = PaperState.load(tmp_path / "state.json", p.capital)
    st.books[SYSTEM].pending = {"AAA": 2000, "BBB": 2000}   # nakitten fazla
    st.save(tmp_path / "state.json")
    run_day(p, rc, cut(dd, 2), tmp_path)
    st = PaperState.load(tmp_path / "state.json", p.capital)
    b = st.books[SYSTEM]
    assert b.cash >= 0 and 0 < b.positions["AAA"] < 2000 and 0 < b.positions["BBB"] < 2000
    assert b.positions["AAA"] * 10 + b.positions["BBB"] * 20 <= 10_000
    assert calls["n"] == 0


def test_event_lifecycle_matches_triple_barrier():
    cfg = ResearchConfig()
    idx = pd.bdate_range("2026-01-01", periods=15)
    flat = pd.Series(100.0, index=idx)
    assert event_active(flat.iloc[:5], idx[0], 0.01, cfg)                      # 4 bar, temas yok
    assert not event_active(flat.iloc[:11], idx[0], 0.01, cfg)                 # 10 bar: dikey bariyer
    up = flat.copy()
    up.iloc[3] = 102.5                                                          # +2.5% >= 2 x 1%
    assert not event_active(up.iloc[:5], idx[0], 0.01, cfg)
    assert event_active(up.iloc[:3], idx[0], 0.01, cfg)                         # temas henüz yok


def test_adjusted_prices_remove_dividend_gaps():
    raw = frame([10, 10, 9.5], [10, 10, 9.5])
    raw["Adj Close"] = [9.5, 9.5, 9.5]                                          # temettü düzeltmesi
    adj = adjusted_ohlcv(raw)
    assert adj["Close"].pct_change().iloc[-1] == pytest.approx(0.0)


def test_paper_config_validates(tmp_path):
    good = tmp_path / "c.yaml"
    good.write_text("capital: 5000\ntickers: [AAA]\n", encoding="utf-8")
    assert load_paper_config(good).tickers == ("AAA",)
    bad = tmp_path / "b.yaml"
    bad.write_text("capitall: 5000\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_paper_config(bad)
    assert len(load_paper_config("paper/config.yaml").tickers) == 30
