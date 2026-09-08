"""Ingest raw data for the Philippine hospital-capacity project.

The DOH DataDrop and PSA sources require a manual download. Pass the local
download paths as options when importing them; no personal paths are stored in
this script. The public disease.sh API extract is fetched by default.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
API_URL = "https://disease.sh/v3/covid-19/historical/PHL"
API_FILENAME = "phl_covid_cases_api_raw.json"
PSA_FILENAME = "psa_population_2020.xlsx"


def copy_file(source: Path, destination: Path, force: bool) -> bool:
    """Copy one source file without silently replacing an existing extract."""
    if destination.exists() and not force:
        print(f"  -> SKIPPED: {destination.name} already exists (use --force to replace it).")
        return False

    shutil.copy2(source, destination)
    print(f"  -> SAVED: {destination.name}")
    return True


def copy_kaggle_csvs(source_dir: Path, force: bool) -> int:
    """Copy CSV files from an extracted Kaggle download into ``data/raw``."""
    if not source_dir.is_dir():
        raise ValueError(f"Kaggle source directory does not exist: {source_dir}")

    csv_files = sorted(source_dir.rglob("*.csv"))
    if not csv_files:
        raise ValueError(f"No CSV files were found in: {source_dir}")

    copied = sum(copy_file(path, RAW_DATA_DIR / path.name, force) for path in csv_files)
    print(f"  -> Kaggle CSVs copied: {copied}/{len(csv_files)}")
    return copied


def copy_psa_workbook(source_file: Path, force: bool) -> bool:
    """Copy a manually downloaded PSA workbook using the project's stable name."""
    if not source_file.is_file():
        raise ValueError(f"PSA source file does not exist: {source_file}")
    return copy_file(source_file, RAW_DATA_DIR / PSA_FILENAME, force)


def fetch_covid_api_data(force: bool) -> bool:
    """Fetch Philippine historical COVID-19 data from the public disease.sh API."""
    destination = RAW_DATA_DIR / API_FILENAME
    if destination.exists() and not force:
        print(f"  -> SKIPPED: {destination.name} already exists (use --force to refresh it).")
        return False

    try:
        response = requests.get(
            API_URL,
            params={"lastdays": "all"},
            headers={"Accept": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        with destination.open("w", encoding="utf-8") as file:
            json.dump(response.json(), file, indent=2)
        print(f"  -> SAVED: {destination.name}")
        return True
    except requests.RequestException as error:
        print(f"  -> API ERROR: {error}")
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--kaggle-source-dir",
        type=Path,
        help="Directory containing CSV files extracted from the Kaggle DOH DataDrop download.",
    )
    parser.add_argument(
        "--psa-source-file",
        type=Path,
        help="Path to the manually downloaded PSA 2020 population workbook.",
    )
    parser.add_argument(
        "--skip-api",
        action="store_true",
        help="Do not call disease.sh; useful when working offline.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing raw files with files from the supplied sources/API.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if args.kaggle_source_dir:
        print("Copying Kaggle DOH DataDrop CSVs...")
        copy_kaggle_csvs(args.kaggle_source_dir, args.force)

    if args.psa_source_file:
        print("Copying PSA population workbook...")
        copy_psa_workbook(args.psa_source_file, args.force)

    if not args.skip_api:
        print("Fetching disease.sh API extract...")
        fetch_covid_api_data(args.force)

    print(f"Ingestion finished. Raw data location: {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()
