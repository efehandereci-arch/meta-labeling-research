"""Conformal Kelly (arXiv:2608.01494): nedensellik, kapsama, sınırlar ve konfigürasyon."""

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from meta_labeling.research.conformal import conformal_kelly, conformal_quantile
from meta_labeling.research.modeling import position_sizes
from meta_labeling.research.settings import (
    ConfigError,
    ConformalKellySettings,
    ResearchConfig,
    config_from_dict,
)

CS = ConformalKellySettings(window=200, min_scores=30, min_payoff_events=15, dial_window=10)


def synthetic_events(n=800, seed=0, hold=5):
    """σ ölçekli işlem getirileri: x = r/σ = ±2 + gürültü; y ~ Bernoulli(p), yani p kalibre."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2015-01-01", periods=n + hold + 5)
    t0 = idx[:n]
    trgt = rng.uniform(0.008, 0.03, n)
    p = np.clip(rng.beta(5, 5, n), 0.01, 0.99)
    y = rng.random(n) < p
    x = np.where(y, 2.0, -2.0) + rng.normal(0, 0.8, n)
    holds = rng.integers(1, hold + 1, n)
    label_end = idx[np.arange(n) + holds]
    ev = pd.DataFrame({"trgt": trgt, "label_end": label_end, "exec_net_ret": x * trgt,
                       "side": 1.0, "t1": label_end}, index=t0)
    return ev, pd.Series(p, index=t0, name="proba")


def test_conformal_quantile_uses_finite_sample_index():
    s = np.arange(1, 11, dtype=float)                     # n = 10
    assert conformal_quantile(s, 0.25) == 9.0             # ⌈11·0.75⌉ = 9. en küçük
    assert conformal_quantile(s, 0.01) == 10.0            # n'de kırpılır
    assert np.isnan(conformal_quantile(np.array([]), 0.25))


def test_sizes_are_bounded_and_warmup_is_flat():
    ev, p = synthetic_events()
    r = conformal_kelly(p, ev, CS, cap=1.0, threshold=0.5, dial=True)
    assert r.size.between(0, 1).all() and r.size_undialed.between(0, 1).all()
    assert r.dial.between(CS.dial_floor, 1).all()
    assert (r.size <= r.size_undialed + 1e-12).all()      # kadran yalnızca küçültür
    assert (r.size[r.q_eff.isna()] == 0).all()            # ısınmada pozisyon yok
    assert (r.size[r.mu <= 0] == 0).all()                  # negatif beklentiye bahis yok
    assert (r.size[p <= 0.5] == 0).all()                  # eşik kapısı
    assert (r.size > 0).sum() > 50


def test_future_information_never_changes_a_decision():
    """i kararından sonra kapanan işlemlerin getirisi / sonraki olasılıklar değişse de size_i değişmemeli."""
    ev, p = synthetic_events(seed=1)
    base = conformal_kelly(p, ev, CS, cap=5.0, threshold=0.0, dial=True)
    rng = np.random.default_rng(9)
    for i in (150, 400, 700):
        t = ev.index[i]
        future_landing = ev["label_end"] >= t
        ev2 = ev.copy()
        ev2.loc[future_landing, "exec_net_ret"] = rng.normal(0, 0.2, int(future_landing.sum()))
        p2 = p.copy()
        p2[p2.index > t] = rng.random(int((p2.index > t).sum()))
        alt = conformal_kelly(p2, ev2, CS, cap=5.0, threshold=0.0, dial=True)
        cols = ("size", "size_undialed", "mu", "sigma", "dial")
        for c in cols:
            a, b = getattr(base, c).iloc[: i + 1], getattr(alt, c).iloc[: i + 1]
            pd.testing.assert_series_equal(a, b, check_names=False)
        # ve bir etiket kapanır kapanmaz (label_end < t0) bilgi kullanılır: sonuçlar değişmeli
        assert not base.size.iloc[i + 30:].equals(alt.size.iloc[i + 30:])


def test_realized_coverage_is_near_nominal_on_exchangeable_data():
    ev, p = synthetic_events(n=3000, seed=2)
    r = conformal_kelly(p, ev, replace(CS, anchor_lambda=0.0), cap=1.0, threshold=0.0, dial=False)
    cov = r.coverage_summary()
    se = cov["Std. hata (iid)"]
    assert abs(cov["Gerçekleşen kapsama"] - 0.75) < 4 * se
    assert cov["Alt ihlal oranı"] + cov["Üst ihlal oranı"] == pytest.approx(1 - cov["Gerçekleşen kapsama"])


def test_vol_units_scale_size_inversely_with_current_volatility():
    ev, p = synthetic_events(seed=3)
    r = conformal_kelly(p, ev, CS, cap=100.0, threshold=0.0, dial=False)
    i = int(np.flatnonzero((r.size_undialed > 0).to_numpy())[-1])
    ev2 = ev.copy()
    ev2.iloc[i, ev2.columns.get_loc("trgt")] *= 2.0  # yalnızca i'nin σ_t0'ı (kendi getirisi i kararına girmez)
    ev2.iloc[i, ev2.columns.get_loc("exec_net_ret")] *= 2.0
    r2 = conformal_kelly(p, ev2, CS, cap=100.0, threshold=0.0, dial=False)
    assert r2.size_undialed.iloc[i] == pytest.approx(r.size_undialed.iloc[i] / 2.0)
    raw = replace(CS, score_units="raw")
    a = conformal_kelly(p, ev, raw, cap=100.0, threshold=0.0, dial=False).size_undialed.iloc[i]
    b = conformal_kelly(p, ev2, raw, cap=100.0, threshold=0.0, dial=False).size_undialed.iloc[i]
    assert a == pytest.approx(b)                          # ham birimde σ_t0'dan bağımsız


def test_empirical_payoff_ratio_replaces_barrier_assumption():
    ev, p = synthetic_events(seed=4)
    ev["exec_net_ret"] = np.where(ev["exec_net_ret"] > 0, ev["exec_net_ret"] * 0.5, ev["exec_net_ret"])
    r = conformal_kelly(p, ev, CS, cap=1.0, threshold=0.0, dial=False)
    assert r.payoff_ratio.dropna().iloc[-1] == pytest.approx(0.5, abs=0.1)
    # b̂ ≈ 0.5 iken kırılma noktası p* = 1/(1+b̂) ≈ 0.67: altındaki olasılıklara bahis yok
    assert (r.size_undialed[p < 0.6] == 0).all()


def test_rejects_labels_that_end_before_they_start():
    ev, p = synthetic_events(n=50)
    ev.iloc[3, ev.columns.get_loc("label_end")] = ev.index[3]
    with pytest.raises(ValueError):
        conformal_kelly(p, ev, CS, cap=1.0, threshold=0.0, dial=False)


def test_position_sizes_dispatch_and_dial_only_shrinks():
    ev, p = synthetic_events(seed=5)
    cfg = ResearchConfig()
    cfg = replace(cfg, sizing=replace(cfg.sizing, conformal=CS))
    plain = position_sizes("conformal_kelly", p, ev, cfg, threshold=0.5)
    dialed = position_sizes("conformal_kelly_dial", p, ev, cfg, threshold=0.5)
    assert plain.max() <= cfg.risk.max_position and (dialed <= plain + 1e-12).all()
    assert (plain[p <= 0.5] == 0).all()


def test_config_parses_and_validates_conformal_block():
    cfg = config_from_dict({"sizing": {"method": "conformal_kelly_dial",
                                       "conformal": {"alpha": 0.2, "window": 300, "score_units": "raw"}}})
    assert cfg.sizing.method == "conformal_kelly_dial"
    assert cfg.sizing.conformal.alpha == 0.2 and cfg.sizing.conformal.score_units == "raw"
    for bad in ({"conformal": {"alpha": 1.5}}, {"conformal": {"score_units": "log"}},
                {"conformal": {"window": 0}}, {"conformal": {"alfa": 0.2}}, {"method": "kelly2"}):
        with pytest.raises(ConfigError):
            config_from_dict({"sizing": bad})
