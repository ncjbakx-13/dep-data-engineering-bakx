"""
Phase 2 — Data Ingestion
Replace this template with your own ingestion logic.
"""

import os
import shutil
from pathlib import Path

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def ingest():
    print("Starting Kaggle data indestion...")

    source_folder = Path(r"C:\Users\NCJ Bakx\Documents\DEP_Cohort_2026_Data\archive")

    if not source_folder.exists():
        print(f"Error: Could not find the folder at {source_folder}")
    else:
        csv_files = list(source_folder.rglob("*.csv"))
        if not csv_files:
            print("No CSV files found in the source folder")
        else:
            files_copied = 0
            for file_path in csv_files:
                destination_file = os.path.join(RAW_DATA_DIR, file_path.name)
                shutil.copy(file_path, destination_file)
                files_copied += 1
            print(f"Success: Copied {files_copied} Kaggle CSV files.\n")

    print("Starting PSA Census data indestions")

    psa_source_file = Path(r"C:\Users\NCJ Bakx\Documents\DEP_Cohort_2026_Data\PSA 2020 Census of Population and Housing.xlsx")

    if not psa_source_file.exists():
        print(f"Error: Could not find the file at {psa_source_file}")
    else:
        psa_destination = os.path.join(RAW_DATA_DIR, "psa_population_2020.xlsx")
        shutil.copy(psa_source_file, psa_destination)
        print(f"Success: Copied PSA Census data to {psa_destination}\n")


if __name__ == "__main__":
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    ingest()
    print("Ingestion complete. Check data/raw/ for output.")
