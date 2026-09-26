"""Profesyonel quant research katmanı: leakage audit, benchmark'lar, kalibrasyon,
maliyet/execution modeli, rejim analizi, CPCV, placebo testleri ve otomatik rapor.

Kullanım:
    >>> from meta_labeling.research import ResearchSession
    >>> session = ResearchSession.from_yaml("config.yaml")
    >>> report = session.run_all()
    >>> print(report.verdict)
"""

from .diagnostics import DiagnosticsResult, run_diagnostics
from .frequency import FrequencyStudyResult, run_frequency_study
from .leakage import LeakageError, LeakageReport, run_leakage_audit
from .session import InsufficientDataError, ResearchSession, run_universe
from .settings import ConfigError, ResearchConfig, config_from_dict, load_research_config
from .tracking import reproduce
from .universe import DEFAULT_BIST_TICKERS

__all__ = [
    "DEFAULT_BIST_TICKERS",
    "ConfigError",
    "DiagnosticsResult",
    "FrequencyStudyResult",
    "InsufficientDataError",
    "LeakageError",
    "LeakageReport",
    "ResearchConfig",
    "ResearchSession",
    "config_from_dict",
    "load_research_config",
    "reproduce",
    "run_diagnostics",
    "run_frequency_study",
    "run_leakage_audit",
    "run_universe",
]
