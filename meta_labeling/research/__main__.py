"""``python -m meta_labeling.research --config config.yaml [--ticker SASA] [--universe | --frequency-study]``"""

from __future__ import annotations

import argparse

import pandas as pd

from .frequency import run_frequency_study
from .session import ResearchSession, run_universe
from .settings import load_research_config


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Meta-labeling research framework")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--ticker", default=None, help="Varsayılan: config'deki ilk hisse")
    parser.add_argument("--universe", action="store_true", help="Tüm config hisselerinde çekirdek OOS testi")
    parser.add_argument("--diagnostics", action="store_true",
                        help="Tam rapora ek olarak placebo teşhis analizlerini çalıştır")
    parser.add_argument("--frequency-study", action="store_true",
                        help="Aynı sistemi düşük/orta/yüksek frekansta çalıştır (varsayılan hisse: AAPL)")
    args = parser.parse_args(argv)
    cfg = load_research_config(args.config)
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        if args.frequency_study:
            study = run_frequency_study(cfg, args.ticker)
            print(study.table.drop(columns=["Rapor"], errors="ignore").to_string())
            print(f"\nÖzet: {study.path}")
            return
        if args.universe:
            print(run_universe(cfg).round(3).to_string())
            return
        session = ResearchSession(cfg, args.ticker)
        report = session.run_all()
        if args.diagnostics:
            diag = session.diagnostics()
            print("\n".join(f"- {x}" for x in diag.explanations))
            print(f"Teşhis raporu: {diag.path}\n")
        print(report.final_table.to_string())
        print()
        print(report.robustness_table.to_string(index=False))
        print(f"\nKARAR: {report.verdict}\nRapor: {report.path}")


if __name__ == "__main__":
    main()
