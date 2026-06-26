"""
Phase 2 — Data Ingestion
Replace this template with your own ingestion logic.
"""

import os
import shutil
import json
import requests
from pathlib import Path

# os.path.dirname(__file__) gets the folder where THIS script lives.
# ".." means "go up one folder level".
# This builds a dynamic path to your data/raw folder so it works on any computer!
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def fetch_covid_api_data():
    """Fetches historical COVID-19 case data for the Philippines from a JSON API."""
    print("Starting API data ingestion (disease.sh)...")
    
    # This is the web address we are requesting data from
    url = "https://disease.sh/v3/covid-19/historical/PHL"
    
    # Parameters act like a filter for the API. Here we ask for "all" historical days.
    params = {"lastdays": "all"}
    
    # Headers tell the server what format we expect back. We want JSON format.
    headers = {"Accept": "application/json"}

    try:
        # requests.get() actually visits the URL and downloads the data.
        # timeout=30 means "if the server takes longer than 30 seconds, give up."
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        # This checks if the server gave us an error (like a 404 Not Found or 500 Server Error)
        response.raise_for_status()
        
        # We convert the raw text response from the server into a Python dictionary (JSON)
        payload = response.json()
        
        # We define exactly what the new file should be named and where it should go
        output_file = Path(RAW_DATA_DIR) / "phl_covid_cases_api_raw.json"
        
        # 'w' means "write mode". We open the file, dump our JSON data into it, and format it nicely with indent=4
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
            
        print(f"  -> SUCCESS: Saved API extract to {output_file}\n")
        
    # If anything goes wrong (no internet, bad URL), it jumps down here instead of crashing the program
    except requests.exceptions.RequestException as e:
        print(f"  -> API Error: Could not fetch data. Details: {e}\n")

def ingest():
    # ---------------------------------------------------------
    # STEP 1: Ingest DOH COVID DataDrop (Kaggle)
    # ---------------------------------------------------------
    print("Starting Kaggle data ingestion...")
    
    # ACTION REQUIRED: Update this path to where your Kaggle files are!
    # The 'r' outside the string means "raw string" so Python doesn't get confused by Windows backslashes (\)
    source_folder = Path(r"C:\Users\NCJ Bakx\Documents\DEP_Cohort_2026_Data\archive")

    # .exists() checks if the folder is actually there on your computer
    if not source_folder.exists():
        print(f"  -> Error: Could not find the folder at {source_folder}")
    else:
        # .rglob("*.csv") recursively searches inside the folder for any file ending in .csv
        csv_files = list(source_folder.rglob("*.csv"))
        
        if not csv_files:
            print("  -> No CSV files found in the source folder!")
        else:
            files_copied = 0
            
            # This loop grabs one file path at a time from our list of found CSVs
            for file_path in csv_files:
                
                # file_path.name extracts JUST the file name (e.g., 'data.csv') from the long folder path
                # Then it joins it with our raw data folder path
                destination_file = os.path.join(RAW_DATA_DIR, file_path.name)
                
                # shutil.copy does the actual copy-pasting of the file
                shutil.copy(file_path, destination_file)
                files_copied += 1
                
            # The 'f' outside the string lets us inject variables directly into the text using {curly braces}
            print(f"  -> SUCCESS: Copied {files_copied} Kaggle CSV files.\n")

    # ---------------------------------------------------------
    # STEP 2: Ingest PSA Population Data
    # ---------------------------------------------------------
    print("Starting PSA Census data ingestion...")
    
    # ACTION REQUIRED: Update this path to your downloaded Excel file!
    psa_source_file = Path(r"C:\Users\NCJ Bakx\Documents\DEP_Cohort_2026_Data\PSA 2020 Census of Population and Housing.xlsx")

    if not psa_source_file.exists():
        print(f"  -> Error: Could not find the file at {psa_source_file}")
    else:
        # We specify a clean, new name for the file as it copies over
        psa_destination = os.path.join(RAW_DATA_DIR, "psa_population_2020.xlsx")
        
        # Copy-paste the Excel file
        shutil.copy(psa_source_file, psa_destination)
        print(f"  -> SUCCESS: Copied PSA Census Excel file to {psa_destination}\n")

    # ---------------------------------------------------------
    # STEP 3: API Ingestion (Bootcamp Week 5 Requirement)
    # ---------------------------------------------------------
    # Now we call the custom function we created at the top of the file
    fetch_covid_api_data()

# This is a standard Python safety check. 
# It ensures this script only runs if you run it directly from the terminal.
if __name__ == "__main__":
    # os.makedirs creates the data/raw folders if they don't exist yet. exist_ok=True prevents errors if they do.
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # Run the big ingest function that holds all our logic
    ingest()
    print("Ingestion complete. Check data/raw/ for output.")
