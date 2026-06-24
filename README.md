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

## Possible Final Dashboard
The dashboard should help the audience quickly see a regional breakdown of historical bed availability vs. occupied beds, supporting decisions on where to deploy emergency funding or build new facilities for future preparedness.