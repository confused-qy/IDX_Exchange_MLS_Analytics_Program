# Week 7 Summary - Outlier Detection and Data Quality

## 1. Goal

Week 7 focused on identifying and controlling extreme numeric values that could distort market analytics. The main target fields were:

- `close_price`
- `living_area`
- `days_on_market`

The goal was not to permanently delete records. Instead, the work created a full flagged dataset for auditability and a separate clean filtered dataset for analysis.

## 2. Input Data

The Week 7 process used the Week 5 feature-engineered datasets as inputs:

- `week5_output/Sold_Week5_Features.csv`
- `week5_output/Listed_Week5_Features.csv`

This is the right processing layer because the Week 5 files already contain cleaned numeric fields, quality flags, date fields, and engineered metrics needed for Tableau analysis.

## 3. Method

The script applies the Interquartile Range method to each numeric field:

```python
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
```

A record is flagged as an IQR outlier when the field value is lower than the lower bound or higher than the upper bound.

Percentiles were also calculated for context:

- `p01`
- `p99`

These percentiles help explain whether the IQR bounds are reasonable compared with the broader distribution.

## 4. Processing Steps

The Week 7 script is located at:

- `IDX_Exchange/Week7/outlier_detection_iqr.py`

The script performs the following steps:

1. Reads the sold and listed Week 5 feature datasets.
2. Converts `close_price`, `living_area`, and `days_on_market` to numeric values.
3. Calculates IQR bounds for each target field.
4. Adds field-level outlier flags:
   - `close_price_iqr_outlier_flag`
   - `living_area_iqr_outlier_flag`
   - `days_on_market_iqr_outlier_flag`
5. Adds a combined outlier flag:
   - `any_iqr_outlier_flag`
6. Preserves existing business-rule invalid flags from earlier cleaning:
   - `invalid_close_price_flag`
   - `invalid_living_area_flag`
   - `invalid_days_on_market_flag`
   - `invalid_numeric_flag`
7. Adds final analysis exclusion logic:
   - `business_rule_invalid_flag`
   - `exclude_from_week7_analysis_flag`
8. Saves both full flagged datasets and clean filtered datasets.
9. Saves a CSV and Markdown comparison report.

## 5. Output Files

All Week 7 outputs were written to the root-level `week7_output/` folder.

Full flagged datasets:

- `week7_output/Sold_Week7_Flagged.csv`
- `week7_output/Listed_Week7_Flagged.csv`

Clean filtered datasets:

- `week7_output/Sold_Week7_Clean_Filtered.csv`
- `week7_output/Listed_Week7_Clean_Filtered.csv`

Comparison reports:

- `week7_output/Week7_Outlier_Comparison.csv`
- `week7_output/week7_outlier_comparison.md`

## 6. Dataset Size Results

| Dataset | Rows Before | Rows After | Rows Removed | Removed % |
| --- | ---: | ---: | ---: | ---: |
| sold | 397,358 | 335,289 | 62,069 | 15.62% |
| listed | 539,650 | 464,181 | 75,469 | 13.98% |

The filtered datasets remove records where either:

- `invalid_numeric_flag = True`
- `any_iqr_outlier_flag = True`

The full flagged datasets keep all records and should be used for audit or data quality review.

## 7. Median and Mean Results

### Sold Dataset

| Field | Median Before | Median After | Mean Before | Mean After | IQR Outlier Count |
| --- | ---: | ---: | ---: | ---: | ---: |
| `close_price` | 820,000 | 785,000 | 1,184,821.70 | 898,068.21 | 29,348 |
| `living_area` | 1,641 | 1,568 | 1,905.06 | 1,673.56 | 17,562 |
| `days_on_market` | 19 | 16 | 37.34 | 26.38 | 30,240 |

### Listed Dataset

| Field | Median Before | Median After | Mean Before | Mean After | IQR Outlier Count |
| --- | ---: | ---: | ---: | ---: | ---: |
| `close_price` | 855,000 | 825,000 | 1,201,685.39 | 947,564.41 | 10,452 |
| `living_area` | 1,669 | 1,610 | 1,981.29 | 1,740.91 | 26,731 |
| `days_on_market` | 11 | 10 | 19.54 | 13.01 | 45,099 |

The means changed more than the medians, especially for `close_price` and `days_on_market`. This confirms that extreme values were pulling averages upward.

## 8. IQR Bounds

| Dataset | Field | Lower Bound | Upper Bound | P01 | P99 |
| --- | --- | ---: | ---: | ---: | ---: |
| sold | `close_price` | -512,500 | 2,387,500 | 203,275 | 5,528,900 |
| sold | `living_area` | -205.5 | 3,670.5 | 609 | 5,280 |
| sold | `days_on_market` | -52 | 108 | 0 | 229 |
| listed | `close_price` | -525,000 | 2,475,000 | 215,000 | 5,500,000 |
| listed | `living_area` | -330 | 3,878 | 593 | 6,300 |
| listed | `days_on_market` | -22 | 50 | 0 | 139 |

Some lower bounds are negative because the IQR formula is statistical and does not know the business meaning of the field. This is why business-rule flags are still necessary. For example, `close_price <= 0`, `living_area <= 0`, and `days_on_market < 0` should always be treated as invalid regardless of IQR.

## 9. Tableau Readiness

The Week 7 clean filtered datasets are appropriate for Tableau analysis:

- `week7_output/Sold_Week7_Clean_Filtered.csv`
- `week7_output/Listed_Week7_Clean_Filtered.csv`

These files are better Tableau sources than the full flagged files because they already exclude invalid numeric records and IQR outliers. This reduces distortion in average price, average days on market, price per square foot, and other aggregate metrics.

Recommended Tableau usage:

- Use `Sold_Week7_Clean_Filtered.csv` for closed-sale metrics:
  - median close price
  - average days on market
  - sales volume
  - price per square foot
  - close-to-list or close-to-original-list ratios
- Use `Listed_Week7_Clean_Filtered.csv` for listing-side metrics:
  - new listings
  - listing price trends
  - listing inventory analysis
  - listing-side days on market
- Use `Week7_Outlier_Comparison.csv` for documentation or a data quality appendix.
- Use the full flagged files only when building a data quality dashboard or explaining excluded records.

## 10. Tableau Caveats

The files are Tableau-ready, but the sold and listed datasets should not be used interchangeably.

For sale-price dashboards, the sold dataset should be the primary source. The listed dataset contains a `close_price` field, but listed records are not the correct source for final closed-sale price analysis.

For new-listing dashboards, the listed dataset should be used. Metrics such as new listings, listing price, listing month, city, county, ZIP code, and property subtype are appropriate from the listed file.

The clean filtered datasets are best for final dashboards. The flagged datasets are useful for QA, but using them directly as the main Tableau source would allow outliers to remain in aggregate calculations.

## 11. Final Assessment

The Week 7 outputs satisfy the assignment requirements:

- IQR filtering was applied to key numeric fields.
- Outlier flag columns were added instead of permanently deleting records.
- Full flagged datasets were saved.
- Clean filtered datasets were saved.
- Dataset size and median values were compared before and after filtering.
- The outputs are suitable for Tableau when the clean filtered files are used as the main analytical sources.
