"""Command-line interface for local synthetic reconciliation."""
import argparse
import csv
import json
from pathlib import Path
from .reconcile import reconcile


def _load_csv(path: str) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconcile synthetic internal and counterparty trade CSV files")
    parser.add_argument("internal", help="Path to internal trade CSV")
    parser.add_argument("external", help="Path to external trade CSV")
    args = parser.parse_args()
    results = reconcile(_load_csv(args.internal), _load_csv(args.external))
    print(json.dumps([result.__dict__ for result in results], indent=2))


if __name__ == "__main__":
    main()
