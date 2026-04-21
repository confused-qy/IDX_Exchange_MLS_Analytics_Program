# Week 4 Data Cleaning Report

Source files:
- `Listed_KeepCols_WithRates.csv`
- `Sold_KeepCols_WithRates.csv`

Output files:
- `Listed_Cleaned.csv`
- `Sold_Cleaned.csv`

## 1. Cleaning Scope and Transformations

### Datetime conversion
Converted the following fields to datetime format (`errors='coerce'`):
- `close_date`
- `purchase_contract_date`
- `listing_contract_date`
- `contract_status_change_date`

### Numeric typing
Converted the following fields to numeric type (`errors='coerce'`):
- `close_price`
- `living_area`
- `days_on_market`
- `bedrooms_total`
- `bathrooms_total_integer`
- `latitude`
- `longitude`
- `rate_30yr_fixed`

### Invalid numeric checks
Flagged records with:
- `close_price <= 0`
- `living_area <= 0`
- `days_on_market < 0`
- `bedrooms_total < 0`
- `bathrooms_total_integer < 0`

### Date consistency checks
Created and counted:
- `listing_after_close_flag`
- `purchase_after_close_flag`
- `negative_timeline_flag`

### Geographic quality checks
Created and counted:
- `coord_missing_flag` (`latitude` or `longitude` is null)
- `coord_zero_flag` (`latitude == 0` or `longitude == 0`)
- `positive_longitude_flag` (`longitude > 0`)
- `implausible_coord_flag` (outside CA-appropriate coordinate bounds)
- `geo_invalid_flag` (any geo issue)

### Row filtering applied for cleaned outputs
Removed records where any of these are true:
- `invalid_numeric_flag`
- `coord_zero_flag`
- `positive_longitude_flag`

### Redundant columns removed
- Listed cleaned output: `listing_year`, `listing_month`, `listing_year_month`
- Sold cleaned output: `close_year`, `close_month`, `close_year_month`

## 2. Before/After Row Counts

### Listed dataset
- Before: `540,183`
- After: `539,650`
- Removed: `533`

### Sold dataset
- Before: `397,603`
- After: `397,358`
- Removed: `245`

## 3. Data Type Confirmation (Post-cleaning)

### Listed
- `close_price`: `float64`
- `living_area`: `float64`
- `days_on_market`: `int64`
- `bedrooms_total`: `float64`
- `bathrooms_total_integer`: `float64`
- `latitude`: `float64`
- `longitude`: `float64`
- `rate_30yr_fixed`: `float64`
- `close_date`: `datetime64[ns]`
- `purchase_contract_date`: `datetime64[ns]`
- `listing_contract_date`: `datetime64[ns]`
- `contract_status_change_date`: `datetime64[ns]`

### Sold
- `close_price`: `float64`
- `living_area`: `float64`
- `days_on_market`: `int64`
- `bedrooms_total`: `float64`
- `bathrooms_total_integer`: `float64`
- `latitude`: `float64`
- `longitude`: `float64`
- `rate_30yr_fixed`: `float64`
- `close_date`: `datetime64[ns]`
- `purchase_contract_date`: `datetime64[ns]`
- `listing_contract_date`: `datetime64[ns]`
- `contract_status_change_date`: `datetime64[ns]`

## 4. Date Consistency Flag Counts

### Listed
- `listing_after_close_flag`: `72`
- `purchase_after_close_flag`: `265`
- `negative_timeline_flag`: `271`

### Sold
- `listing_after_close_flag`: `58`
- `purchase_after_close_flag`: `240`
- `negative_timeline_flag`: `261`

## 5. Geographic Data Quality Summary

### Listed
- `coord_missing_flag`: `80,145`
- `coord_zero_flag`: `60`
- `positive_longitude_flag`: `85`
- `implausible_coord_flag`: `227`
- `geo_invalid_flag`: `80,432`

### Sold
- `coord_missing_flag`: `15,822`
- `coord_zero_flag`: `25`
- `positive_longitude_flag`: `29`
- `implausible_coord_flag`: `59`
- `geo_invalid_flag`: `15,906`

## 6. Invalid Numeric Summary

### Listed
- `invalid_close_price_flag`: `0`
- `invalid_living_area_flag`: `359`
- `invalid_days_on_market_flag`: `29`
- `invalid_bedrooms_flag`: `0`
- `invalid_bathrooms_flag`: `0`
- `invalid_numeric_flag`: `388`

### Sold
- `invalid_close_price_flag`: `1`
- `invalid_living_area_flag`: `144`
- `invalid_days_on_market_flag`: `46`
- `invalid_bedrooms_flag`: `0`
- `invalid_bathrooms_flag`: `0`
- `invalid_numeric_flag`: `191`

## 7. Deliverable Artifacts
- Script: `IDX_Exchange/Week4/data_cleaning_preparation.py`
- Report: `IDX_Exchange/Week4/data_cleaning_report.md`
- Cleaned datasets:
  - `Listed_Cleaned.csv`
  - `Sold_Cleaned.csv`
