# Week5 Recap and Week6 Tableau Variable Plan

## 1. What Week5 Delivered (from code and outputs)
- Input data: `Listed_Cleaned.csv`, `Sold_Cleaned.csv`
- Core scripts:
  - `feature_engineering.py`: required-field checks, type standardization, data-quality checks, engineered metrics
  - `segment_summary.py`: grouped summary stats (`count/mean/median/min/max`)
  - `sample_output.py`: validation sample output
- Produced outputs (in `week5_output/`):
  - Feature-level tables: `Listed_Week5_Features.csv`, `Sold_Week5_Features.csv`
  - Data quality report: `Week5_DataQuality_Check.csv`
  - Grouped summaries: 5 SegmentSummary files

## 2. Match Against Tableau Requirements
- Time range: data actually covers `2024-01` through `2026-03` (meets “January 2024 through latest month available”)
- Geo filters: `city`, `county_or_parish`, `postal_code` are highly complete and usable
- Property subtype filter: `property_sub_type` is available
- Office competitive analysis: `list_office_name` is available
- Agent competitive analysis: `list_agent_full_name` is now available in both `Listed_Week5_Features.csv` and `Sold_Week5_Features.csv`

## 3. Recommended Tableau Source Tables
- `Sold_Week5_Features.csv`: primary fact table for closed-sale metrics
- `Listed_Week5_Features.csv`: primary fact table for new-listing metrics

Recommended Tableau structure:
- `fact_sold`
- `fact_listed`

## 4. Full Variable List to Bring into Tableau

### 4.1 Dimension Fields
- Time:
  - `close_date`
  - `listing_contract_date`
  - `yrmo`
  - `year`, `month`
- Geography:
  - `city`
  - `county_or_parish`
  - `postal_code` (zip code)
  - `latitude`, `longitude` (for mapping)
- Property:
  - `property_type`
  - `property_sub_type`
  - `mls_area_major`
- Brokerage/office:
  - `list_agent_full_name`
  - `list_office_name`
  - `buyer_office_name`
- Keys:
  - `listing_key`
  - `listing_id`
  - `listing_key_numeric`

### 4.2 Measure Fields
- Price and size:
  - `close_price`
  - `original_list_price`
  - `list_price`
  - `living_area`
  - `price_per_sqft` (engineered)
  - `close_price_per_sqft` (already in upstream data)
  - `list_price_per_sqft` (already in upstream data)
- Market speed/timeline:
  - `days_on_market`
  - `listing_to_contract_days`
  - `contract_to_close_days`
- Pricing performance ratios:
  - `close_to_original_list_ratio` (engineered)
  - `price_ratio` (equivalent to above; keep one if needed)
  - `close_to_list_ratio` (already in upstream data)
- Counting basis:
  - `listing_key` (for `COUNTD`)

### 4.3 Data-Quality / Risk Flags (recommended for filter controls)
- Numeric-quality flags:
  - `invalid_close_price_flag`
  - `invalid_living_area_flag`
  - `invalid_days_on_market_flag`
  - `invalid_numeric_flag`
- Timeline-quality flags:
  - `listing_after_close_flag`
  - `purchase_after_close_flag`
  - `negative_timeline_flag`
  - `date_inconsistency_flag`
- Geo-quality flags:
  - `coord_missing_flag`
  - `coord_zero_flag`
  - `positive_longitude_flag`
  - `implausible_coord_flag`
  - `geo_invalid_flag`

## 5. Metric Definitions for the Two TWBX Files

## 5.1 `market_analysis.twbx`
- Shared filters:
  - `city` / `county_or_parish` / `postal_code`
  - `property_sub_type`
  - Month (`MONTH([Date])`)

Required dashboards:
1. Monthly median close price
- Source: `fact_sold`
- Calc: `MEDIAN([close_price])`
- Time axis: `DATETRUNC('month',[close_date])`

2. Average days on market
- Source: `fact_sold`
- Calc: `AVG([days_on_market])`
- Suggested filter: exclude `invalid_days_on_market_flag = 1`

3. Average close-to-original-list price ratio
- Source: `fact_sold`
- Calc: `AVG([close_to_original_list_ratio])`
- Strong recommendation for robust version:
  - `ratio_clean = IF [close_to_original_list_ratio] >= 0.5 AND [close_to_original_list_ratio] <= 1.5 THEN [close_to_original_list_ratio] END`
  - Use `AVG([ratio_clean])` in the dashboard
  - Reason: current data includes extreme outliers that can distort means

4. New listings
- Source: `fact_listed`
- Calc: `COUNTD([listing_key])`
- Time axis: `DATETRUNC('month',[listing_contract_date])`

5. Closed sales
- Source: `fact_sold`
- Calc: `COUNTD([listing_key])`
- Time axis: `DATETRUNC('month',[close_date])`

Custom market-analysis dashboard (recommended):
- “Months of Supply / Absorption Balance”
- Calc: `new_listings / closed_sales` by month
- Value: shows supply vs. demand balance over time

## 5.2 `competitive_analysis.twbx`
Required dashboards:
1. Top 100 listing agents by sales volume and units
- Dimension: `list_agent_full_name`
- Metrics:
  - Sales volume: `SUM([close_price])`
  - Units: `COUNTD([listing_key])`
- Filters: `city`, `county_or_parish`, `postal_code`, `property_sub_type`
- Optional data-quality filter: exclude null/blank agent names

2. Top 100 listing offices by sales volume and units
- Dimension: `list_office_name`
- Metrics:
  - Sales volume: `SUM([close_price])`
  - Units: `COUNTD([listing_key])`
- Filters: `city`, `county_or_parish`, `postal_code`, `property_sub_type`

3. Zip code heat map of median close prices
- Geo dimension: `postal_code`
- Metric: `MEDIAN([close_price])`
- Filters: month, `city`, `county_or_parish`, `postal_code`, `property_sub_type`

4. Zip code heat map of homes sold
- Geo dimension: `postal_code`
- Metric: `COUNTD([listing_key])`
- Filters: same as above

Custom competitive-analysis dashboard (recommended):
- “Office Share Trend by Month”
- Metrics: `SUM([close_price])` and/or `COUNTD([listing_key])`
- Dimensions: `list_office_name` + month
- View: market-share trend of top-N offices

## 6. Tableau Calculated Fields to Add
- `month_close = DATETRUNC('month',[close_date])`
- `month_list = DATETRUNC('month',[listing_contract_date])`
- `closed_sales = COUNTD([listing_key])`
- `new_listings = COUNTD([listing_key])` (use in listed source)
- `sales_volume = SUM([close_price])`
- `median_close_price = MEDIAN([close_price])`
- `avg_dom = AVG([days_on_market])`
- `ratio_clean = IF [close_to_original_list_ratio] >= 0.5 AND [close_to_original_list_ratio] <= 1.5 THEN [close_to_original_list_ratio] END`
- `avg_ratio_clean = AVG([ratio_clean])`
- `months_of_supply = [new_listings] / [closed_sales]`

## 7. Key Risks and Mitigations
- Risk 1: extreme `close_to_original_list_ratio` outliers can dominate averages
  - Mitigation: default to `ratio_clean`; keep raw ratio for audit view
- Risk 2: timeline fields include implausible spans in some records
  - Mitigation: add reasonable bounds/filters for `listing_to_contract_days` and `contract_to_close_days`
- Risk 3: agent-name standardization issues can split the same agent into multiple labels
  - Mitigation: create a cleaned Tableau field like `UPPER(TRIM([list_agent_full_name]))` and use it for ranking
