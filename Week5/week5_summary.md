# Week 5 Summary

## 1. Objective
Using the Week4 cleaned datasets, build Tableau-ready engineered metrics and segment summaries, then provide a validation sample output.

Input files:
- `Listed_Cleaned.csv`
- `Sold_Cleaned.csv`

Output directory (project root):
- `week5_output/`

---

## 2. Scripts and Responsibilities

### `feature_engineering.py`
Responsibilities:
- Validate required fields:
  - `close_price`
  - `original_list_price`
  - `living_area`
  - `days_on_market`
  - `close_date`
  - `purchase_contract_date`
  - `listing_contract_date`
- Standardize data types:
  - Date columns to `datetime`
  - Numeric columns to `numeric`
- Run missing/zero-value checks and export data-quality output:
  - `Week5_DataQuality_Check.csv`
- Engineer required metrics:
  - `price_ratio = close_price / original_list_price`
  - `close_to_original_list_ratio = close_price / original_list_price`
  - `price_per_sqft = close_price / living_area`
  - `year`, `month`, `yrmo` (derived from `close_date`)
  - `listing_to_contract_days = purchase_contract_date - listing_contract_date`
  - `contract_to_close_days = close_date - purchase_contract_date`

Outputs:
- `Listed_Week5_Features.csv`
- `Sold_Week5_Features.csv`
- `Week5_DataQuality_Check.csv`

### `segment_summary.py`
Responsibilities:
- Read `Sold_Week5_Features.csv`
- Build grouped summary statistics (`count/mean/median/min/max`) for:
  - `close_price`
  - `price_ratio`
  - `price_per_sqft`
  - `days_on_market`
- Group by:
  - `property_type`
  - `county_or_parish`
  - `property_sub_type`
  - `county_or_parish + mls_area_major`
  - `list_office_name + buyer_office_name`

Outputs:
- `SegmentSummary_PropertyType.csv`
- `SegmentSummary_CountyOrParish.csv`
- `SegmentSummary_PropertySubType.csv`
- `SegmentSummary_County_MLSAreaMajor.csv`
- `SegmentSummary_ListOffice_BuyerOffice.csv`

### `sample_output.py`
Responsibilities:
- Read `Sold_Week5_Features.csv`
- Generate a validation sample table containing all key engineered columns
- Sample across price tiers (`low/mid/high`) to show variation across price ranges

Output:
- `Week5_SampleOutput.csv`

---

## 3. Example Output

Example fields from `week5_output/Week5_SampleOutput.csv`:
- `listing_key`
- `close_date`
- `close_price`
- `original_list_price`
- `living_area`
- `days_on_market`
- `price_ratio`
- `close_to_original_list_ratio`
- `price_per_sqft`
- `year`, `month`, `yrmo`
- `listing_to_contract_days`
- `contract_to_close_days`
- `property_type`
- `county_or_parish`

Example rows (simplified):
- `close_price=186500`, `original_list_price=184500`  
  `price_ratio=1.01084`, `price_per_sqft=124.00`, `yrmo=2024-01`
- `close_price=370000`, `original_list_price=399000`  
  `price_ratio=0.927318`, `price_per_sqft=395.30`, `yrmo=2024-01`

---

## 4. Requirement Coverage

- Field checks: completed (required-column validation)
- Type checks: completed (date and numeric standardization)
- Missing/zero checks: completed (data-quality report exported)
- Metric engineering: completed (all requested fields created)
- Sample output: completed (`Week5_SampleOutput.csv`)
- Segment analysis: completed (includes `PropertyType` and extended segments)

---

## 5. Discussion Points (Current Concerns)

These are the main data-quality risks to discuss:

1. Extreme outliers in `price_ratio` are inflating means  
- Example: very large `price_ratio_max` values appear in `SegmentSummary_PropertyType.csv`.  
- This usually indicates source-level price anomalies (near-zero denominators or data-entry/unit issues).

2. Very large day-difference values in timeline metrics  
- `listing_to_contract_days` includes extremely large values in some records, suggesting historical date errors or invalid entries.

