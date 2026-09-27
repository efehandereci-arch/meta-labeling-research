"""``python -m meta_labeling.paper --config paper/config.yaml [--csv-dir DIR --as-of YYYY-MM-DD]``"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

from .config import load_paper_config
from .data import CsvProvider, YFinanceProvider
from .engine import run_day


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="BIST 30 paper trading (sanal para)")
    parser.add_argument("--config", default="paper/config.yaml")
    parser.add_argument("--csv-dir", default=None, help="yfinance yerine yerel CSV'ler (prova / test)")
    parser.add_argument("--as-of", default=None, help="--csv-dir ile: veriyi bu tarihte kes (geriye dönük prova)")
    parser.add_argument("--state-dir", default=None, help="Varsayılan: config'deki state_dir")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg_path = Path(args.config)
    pc = load_paper_config(cfg_path)
    rc = pc.research()                  # research_config yolu çalışma dizinine göre (depo kökü)
    provider = (CsvProvider(args.csv_dir, pd.Timestamp(args.as_of) if args.as_of else None) if args.csv_dir
                else YFinanceProvider(pc.history_period))
    result = run_day(pc, rc, provider, args.state_dir or pc.state_dir)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
