"""Long meta-labeling overlay: nedensellik, maruziyet, kilitli test disiplini."""

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from meta_labeling.data import simulate_ohlcv
from meta_labeling.research.overlay import (
    SYSTEM,
    audit_extra_features,
    expanding_base_rate,
    overlay_exposure,
    paired_sharpe_bootstrap,
    run_overlay_study,
    track_record_features,
    vol_cap_series,
)
from meta_labeling.research.settings import ConfigError, ResearchConfig, config_from_dict


@pytest.fixture(scope="module")
def prices():
    cfg = ResearchConfig()
    stock = simulate_ohlcv(replace(cfg.data.simulation, n_bars=2600, seed=11))
    market = simulate_ohlcv(replace(cfg.data.simulation, n_bars=2600, seed=12))
    return stock, market


def _events(n=300, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2012-01-02", periods=n + 20)
    t0 = idx[:n]
    hold = rng.integers(1, 12, n)
    return pd.DataFrame({"label_end": idx[np.arange(n) + hold], "bin": rng.integers(0, 2, n),
                         "exec_net_ret": rng.normal(0, 0.02, n), "trgt": 0.01}, index=t0)


def test_extra_features_do_not_look_ahead(prices):
    stock, market = prices
    rows = audit_extra_features(stock, market, 6, np.random.default_rng(0))
    assert rows and all(r["status"] == "PASS" for r in rows)


@pytest.mark.parametrize("fn", [lambda e: track_record_features(e, 20), expanding_base_rate])
def test_event_level_features_use_only_closed_labels(fn):
    ev = _events()
    base = fn(ev)
    i = 150
    t = ev.index[i]
    ev2 = ev.copy()
    later = ev2["label_end"] >= t                      # t anında henüz kapanmamış etiketler
    ev2.loc[later, "bin"] = 1 - ev2.loc[later, "bin"]
    ev2.loc[later, "exec_net_ret"] *= -3
    alt = fn(ev2)
    pd.testing.assert_frame_equal(pd.DataFrame(base).iloc[: i + 1], pd.DataFrame(alt).iloc[: i + 1])
    assert not pd.DataFrame(base).iloc[i + 20:].equals(pd.DataFrame(alt).iloc[i + 20:])


def test_overlay_exposure_defaults_averages_and_ignores_no_opinion():
    idx = pd.bdate_range("2020-01-01", periods=8)
    t0 = idx[[1, 2, 5]]
    t1 = pd.Series(idx[[4, 3, 7]], index=t0)
    m = pd.Series([0.0, 1.0, np.nan], index=t0)       # üçüncü olayın görüşü yok
    e = overlay_exposure(idx, t0, t1, m, default=1.0)
    # [t0, t1) aktif: bar1 {0} -> 0 ; bar2 {0, 1} -> 0.5 ; bar3 {0} -> 0 ; bar4.. görüş yok -> 1
    assert e.tolist() == pytest.approx([1.0, 0.0, 0.5, 0.0, 1.0, 1.0, 1.0, 1.0])


def test_vol_cap_is_causal_bounded_and_neutral_during_warmup(prices):
    stock, _ = prices
    vol = np.log(stock["Close"]).diff().ewm(span=50, min_periods=50).std()
    cap = vol_cap_series(vol, 252)
    assert cap.between(0, 1).all() and (cap.iloc[:252] == 1).all()
    binding = np.flatnonzero((cap < 0.999).to_numpy())
    assert len(binding) > 20
    for p in binding[:: max(1, len(binding) // 15)]:   # tavanın bağlayıcı olduğu barlarda kesme testi
        assert vol_cap_series(vol.iloc[: p + 1], 252).iloc[-1] == pytest.approx(cap.iloc[p])


def test_paired_bootstrap_of_identical_series_is_centered():
    r = pd.Series(np.random.default_rng(1).normal(0.0005, 0.01, 800))
    d = paired_sharpe_bootstrap(r, r, 200, 20, np.random.default_rng(2), 252)
    assert d["ΔSharpe"] == 0 and d["CI 2.5%"] == 0 and d["CI 97.5%"] == 0


def test_dev_mode_never_sees_holdout_data(prices, tmp_path):
    stock, market = prices
    hs = stock.index[1900]
    cfg = ResearchConfig()
    cfg = replace(cfg,
                  experiment=replace(cfg.experiment, output_dir=str(tmp_path), log_level="WARNING"),
                  meta_model=replace(cfg.meta_model, n_estimators=40),
                  cv=replace(cfg.cv, n_splits=4, min_train_events=50),
                  sizing=replace(cfg.sizing, conformal=replace(cfg.sizing.conformal, min_scores=20,
                                                               min_payoff_events=10)),
                  overlay=replace(cfg.overlay, holdout_start=str(hs.date()), placebo_reps=3, bootstrap_reps=50))
    res = run_overlay_study(cfg, "SIM", stock, market, dev=True, write=True)
    assert res.window[1] < hs and res.returns.index.max() < hs and res.exposure.index.max() < hs
    assert SYSTEM in res.table.index and len(res.table) == 5
    assert res.exposure.between(0, 1).all()
    assert all(r["status"] == "PASS" for r in res.leakage)
    assert res.path.exists() and "GELİŞTİRME" in res.path.read_text(encoding="utf-8")
    hold = run_overlay_study(cfg, "SIM", stock, market, dev=False, write=False)
    assert hold.window[0] >= hs


def test_overlay_config_block_parses_and_validates():
    cfg = config_from_dict({"overlay": {"market_file": "data/SPY.csv", "robustness_tickers": ["MSFT"]}})
    assert cfg.overlay.market_file == "data/SPY.csv" and cfg.overlay.robustness_tickers == ("MSFT",)
    with pytest.raises(ConfigError):
        config_from_dict({"overlay": {"default_exposure": 1.5}})
    with pytest.raises(ConfigError):
        config_from_dict({"overlay": {"holdout": "2014-01-01"}})
