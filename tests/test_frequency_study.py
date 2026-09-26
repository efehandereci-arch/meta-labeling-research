"""Frekans çalışması: intraday veri, otomatik dönemler, yetersiz veri ve config ayrıştırma."""

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from meta_labeling.data import simulate_ohlcv
from meta_labeling.research import InsufficientDataError, ResearchConfig, ResearchSession, config_from_dict
from meta_labeling.research.frequency import profile_config, run_frequency_study
from meta_labeling.research.settings import FrequencyProfile, FrequencyStudySettings


def intraday(n_days: int, bars_per_day: int, minutes: int, start: str, vol: float, seed: int) -> pd.DataFrame:
    days = pd.bdate_range(start, periods=n_days)
    idx = pd.DatetimeIndex([d + pd.Timedelta(hours=9, minutes=30 + minutes * k)
                            for d in days for k in range(bars_per_day)])
    sim = simulate_ohlcv(replace(ResearchConfig().data.simulation, n_bars=len(idx), long_run_vol=vol,
                                 trend_drift=vol / 10, seed=seed))
    sim.index = idx
    return sim


def fast(tmp_path) -> ResearchConfig:
    cfg = ResearchConfig()
    return replace(
        cfg,
        experiment=replace(cfg.experiment, output_dir=str(tmp_path), log_level="ERROR"),
        meta_model=replace(cfg.meta_model, n_estimators=40),
        cv=replace(cfg.cv, n_splits=4, min_train_events=50),
        cpcv=replace(cfg.cpcv, n_groups=4, n_test_groups=2),
        benchmarks=replace(cfg.benchmarks, random_entry_reps=3),
        analysis=replace(cfg.analysis, bootstrap_n=30, placebo_label_reps=1, placebo_feature_reps=1,
                         placebo_return_reps=1, placebo_timestamp_reps=1, permutation_repeats=1,
                         leakage_samples=4, min_oos_events=30),
        frequency_study=FrequencyStudySettings(profiles=(
            FrequencyProfile("medium", "Orta", "1h", "730d", 1764, "1 saat"),
            FrequencyProfile("high", "Yüksek", "5m", "60d", 19656, "5 dakika"),
        )),
    )


def test_profile_changes_only_data_and_annualization(tmp_path):
    cfg = fast(tmp_path)
    p = cfg.frequency_study.profiles[1]
    pc = profile_config(cfg, p, "AAPL")
    assert pc.data.yfinance_interval == "5m" and pc.data.yfinance_suffix == "" and pc.data.source == "yfinance"
    assert pc.execution.periods_per_year == 19656
    for section in ("primary", "cusum", "barriers", "features", "meta_model", "costs", "sizing", "risk"):
        assert getattr(pc, section) == getattr(cfg, section)  # strateji parametreleri değişmez


def test_frequency_study_runs_and_reports_each_profile(tmp_path):
    cfg = fast(tmp_path)
    data = {
        "medium": intraday(260, 7, 60, "2030-01-02", 0.015 / np.sqrt(7), 1),
        "high": intraday(12, 78, 5, "2030-06-03", 0.015 / np.sqrt(78) / 4, 2),  # çok düşük vol -> olay yok
    }
    res = run_frequency_study(cfg, "TEST", data=data)
    assert list(res.table.index) == ["Orta", "Yüksek"]
    medium = res.sessions["Orta"]
    assert medium.results["periods_auto"]  # 2030 config dönemlerinde yok -> otomatik dönemler
    assert len(medium.results["periods"]) == cfg.analysis.auto_period_count
    assert np.isfinite(res.table.loc["Orta", "Primary Sharpe"])
    assert res.table.loc["Yüksek", "Karar"].startswith("Test edilemedi")
    assert res.path.exists() and "Frekans çalışması" in res.markdown


def test_insufficient_events_raise_clear_error(tmp_path):
    cfg = fast(tmp_path)
    s = ResearchSession.from_ohlcv(cfg, "X", intraday(8, 78, 5, "2030-01-02", 0.0005, 3))
    with pytest.raises(InsufficientDataError):
        s.validate_data(), s.build_features(), s.sample_events(), s.triple_barrier()


def test_profiles_parse_from_yaml_dicts():
    cfg = config_from_dict({"frequency_study": {"ticker": "MSFT", "profiles": [
        {"name": "low", "label": "Günlük", "interval": "1d", "period": "10y", "periods_per_year": 252,
         "bar_duration": "1 gün"}]}})
    assert cfg.frequency_study.ticker == "MSFT"
    assert isinstance(cfg.frequency_study.profiles[0], FrequencyProfile)
