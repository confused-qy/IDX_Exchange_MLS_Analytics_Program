# Week 3 Summary

## Work Completed

### 1) Created four filtered base datasets
Based on the Week2 missing-value analysis, kept “Columns To Keep” and “Core Columns,” and generated
four new files from the root `Listed_Final.csv` and `Sold_Final.csv`:
- `Listed_KeepCols.csv`
- `Listed_CoreCols.csv`
- `Sold_KeepCols.csv`
- `Sold_CoreCols.csv`

How it was done:
- Read the raw CSVs with a single script.
- Selected columns by fixed lists (prints a warning if any column is missing but continues).
- Wrote outputs to the repository root for downstream use.

### 2) Mortgage Rate Enrichment
Merged the FRED 30-year fixed mortgage rate series (`MORTGAGE30US`) onto the combined listings and
sold datasets, then output new files with the rate column:
- `Listed_KeepCols_WithRates.csv`
- `Sold_KeepCols_WithRates.csv`

Steps:
1. Fetch weekly mortgage rate data from FRED.
2. Resample weekly rates to monthly averages.
3. Create a `year_month` key on MLS data:
   - Listings use `listing_contract_date`
   - Sold use `close_date`
4. Left-merge the monthly rates onto MLS data by `year_month`.
5. Validate with null checks to ensure every row matched a rate.

What data was added and why it matters:
- **Added data**: `rate_30yr_fixed` (monthly average of the U.S. 30-year fixed mortgage rate).
- **Why it matters**:
  - Acts as a macroeconomic factor explaining shifts in pricing and demand.
  - Enables analysis of how rate changes affect volume, pricing, and days on market.
  - Serves as an exogenous variable for modeling, improving interpretability and prediction.
  - Helps control for month-level rate regimes in time-series analysis.

## Scripts
- `IDX_Exchange/Week3/build_week3_outputs.py`
- `IDX_Exchange/Week3/mortgage_rate_enrichment.py`

## Outputs (Root Directory)
- `Listed_KeepCols.csv`
- `Listed_CoreCols.csv`
- `Sold_KeepCols.csv`
- `Sold_CoreCols.csv`
- `Listed_KeepCols_WithRates.csv`
- `Sold_KeepCols_WithRates.csv`
