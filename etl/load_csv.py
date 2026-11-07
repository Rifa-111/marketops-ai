"""Local CSV ETL practice: run python -m etl.load_csv."""
import csv
from pathlib import Path
from app.reconcile import reconcile

def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for item in reconcile(load(root / "data/internal.csv"), load(root / "data/external.csv")):
        print(item)
