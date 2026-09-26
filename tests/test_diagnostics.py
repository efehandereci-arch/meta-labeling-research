"""Teşhis analizleri: yapı, eşleştirilmiş tohum referansı, breakeven ve alpha/beta."""

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from meta_labeling.research import ResearchConfig, ResearchSession
from meta_labeling.research.metrics import alpha_beta, trade_breakeven_bps


@pytest.fixture(scope="module")
def session(tmp_path_factory):
    cfg = ResearchConfig()
    cfg = replace(
        cfg,
        experiment=replace(cfg.experiment, output_dir=str(tmp_path_factory.mktemp("diag")), log_level="ERROR"),
        data=replace(cfg.data, simulation=replace(cfg.data.simulation, n_bars=1500, seed=3)),
        meta_model=replace(cfg.meta_model, n_estimators=40),
        cv=replace(cfg.cv, n_splits=4, min_train_events=50),
        cpcv=replace(cfg.cpcv, n_groups=4, n_test_groups=2),
        benchmarks=replace(cfg.benchmarks, random_entry_reps=3),
        analysis=replace(cfg.analysis, bootstrap_n=30, placebo_label_reps=1, placebo_feature_reps=1,
                         placebo_return_reps=1, placebo_timestamp_reps=1, permutation_repeats=1,
                         leakage_samples=4, min_oos_events=30),
        diagnostics=replace(cfg.diagnostics, feature_shuffle_reps=2, seed_noise_reps=2, event_placebo_reps=2),
    )
    s = ResearchSession(cfg)
    s.run_all()
    s.diagnostics()
    return s


def test_diagnostics_tables_and_report(session):
    d = session.results["diagnostics"]
    assert set(d.feature_randomization.index) == set(session.dataset.X.columns)
    assert d.event_time.index[0].startswith("A)") and len(d.event_time) >= 3
    assert len(d.deciles) == session.cfg.diagnostics.n_deciles
    assert d.deciles["n"].sum() == len(session.oos_events)
    assert {"PR-AUC", "ROC-AUC", "Brier", "ECE"} <= set(d.classification)
    assert any(i.startswith("Long") for i in d.long_short.index)
    assert d.path.exists() and d.explanations


def test_feature_deltas_use_matched_seed_reference(session):
    d = session.results["diagnostics"]
    ref = d.seed_noise["Sharpe mean"]
    fr = d.feature_randomization
    assert np.allclose(fr["Sharpe (karıştırılmış)"] - fr["ΔSharpe"], ref)
    assert d.seed_noise["reps"] == 2


def test_sizing_never_exceeds_max_position(session):
    sz = session.results["diagnostics"].sizing
    assert (sz["Maks. büyüklük"].astype(float) <= session.cfg.risk.max_position + 1e-12).all()


def test_trade_breakeven_is_finite_and_consistent():
    ledger = pd.DataFrame({"gross": [0.01, -0.004, 0.006], "size": [1.0, 1.0, 1.0]})
    be = trade_breakeven_bps(ledger)
    assert be == pytest.approx(1e4 * 0.004 / 2)
    net = ledger["gross"] - 2 * be / 1e4 * ledger["size"]
    assert net.mean() == pytest.approx(0.0, abs=1e-12)


def test_alpha_beta_recovers_known_relationship():
    rng = np.random.default_rng(0)
    m = pd.Series(rng.normal(0.0005, 0.01, 3000))
    s = 0.0002 + 0.7 * m + pd.Series(rng.normal(0, 0.002, 3000))
    ab = alpha_beta(s, m, 252)
    assert ab["beta"] == pytest.approx(0.7, abs=0.02)
    assert ab["alpha_ann"] == pytest.approx(0.0002 * 252, abs=0.02)
