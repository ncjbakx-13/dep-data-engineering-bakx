# Philippine Hospital Capacity and Utilization Analysis

## Problem Statement
I want to answer: "Based on historical pandemic data (2020-2023), which regions in the Philippines experienced the highest hospital bed utilization rates, and how did regional population impact patient crowding during health surges?"

## Audience
This project is for the Department of Health (DOH) Regional Directors and hospital administrators who need to analyze past capacity bottlenecks to better allocate medical supplies and prepare for future health crises.

## KPI or Key Metric
The main metrics I want to track are the Regional Bed Utilization Rate (%) and Hospital Bed Density (Beds per 1,000 population).

## Data Source Notes

1. Hospital Utilization Data
Name: DOH DataDrop (via Kaggle)
URL: https://www.kaggle.com/datasets/cvronao/covid19-philippine-dataset
Format: CSV
Coverage: Philippines (Regional and Facility level), daily records from 2020 to 2023.
Why it fits the problem: It contains the exact daily counts of vacant and occupied COVID/non-COVID beds needed to calculate the primary KPI (Bed Utilization Rate).
Known limitations: It relies on manual daily reporting by individual hospitals, meaning there will likely be missing values (nulls) or delayed reporting during extreme surges or weekends.

2. Population Data
Name: PSA 2020 Census of Population and Housing
URL: https://psa.gov.ph/statistics/population-and-housing/node/164786
Format: XLSX
Coverage: Philippines (Regional level), static count as of May 1, 2020.
Why it fits the problem: Provides the official regional population denominators required to calculate the secondary KPI (Hospital Bed Density per 1,000 population).
Known limitations: It is a static snapshot (does not account for 2021-2023 population growth). Additionally, the Excel format requires programmatic data cleaning to isolate just the bolded regional totals from the sub-province data.

## Setup and ingestion

This project uses Python 3.11+ and the packages pinned in `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import requests; print(requests.__version__)"
```

After activation, `Get-Command python` should show a path containing `.venv`.
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process
Bypass` for the current terminal, then run the activation command again.

The repository already includes the raw extracts used for the project. To fetch
the API extract only (the safe default), run:

```powershell
python scripts/ingest.py
```

The script does not overwrite an existing raw file. Add `--force` only when you
intentionally want to refresh the API extract:

```powershell
python scripts/ingest.py --force
```

To reproduce the manual source imports, first download and extract the DOH
DataDrop Kaggle archive and download the PSA workbook. Then provide their local
locations explicitly—these paths are intentionally not stored in the code:

```powershell
python scripts/ingest.py `
  --kaggle-source-dir "C:\path\to\extracted-kaggle-files" `
  --psa-source-file "C:\path\to\PSA 2020 Census of Population and Housing.xlsx"
```

Use `--skip-api` to run only the manual-file import while offline. Source URLs,
download dates, and descriptions are recorded in `data/raw/source_log.csv`.

## Possible Final Dashboard
The dashboard should help the audience quickly see a regional breakdown of historical bed availability vs. occupied beds, supporting decisions on where to deploy emergency funding or build new facilities for future preparedness.

## Updates 
1. Added raw data from kaggle and psa census data.
2. Add API ingestion, raw data, and guide comments for future reference.
3. (Path C) Added `data/raw/source_log.csv` documenting the source URL and download date for every raw file. All DOH DataDrop files retain their original timestamped filenames for reproducibility.
