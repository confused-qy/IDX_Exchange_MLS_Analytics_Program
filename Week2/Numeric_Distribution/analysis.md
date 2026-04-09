# Numeric Distribution Analysis

Data source: `Sold_Final.csv`

## Close proces: Median v.s. Average
- Median close price: 820,000.00
- Average close price: 1,186,328.12
Analysis:
- Average is much higher than median, indicating a right-skewed price distribution with high-end outliers pulling the mean up.
- Median is a more stable “typical” price for market-level reporting.

## About the Days on Market distribution
- Distribution is right-skewed with long upper tail.
- Percentiles: 5th=1, 25th=8, 50th=19, 75th=48, 95th=131, 99th=229.
- Negative values and extreme highs suggest data quality or special cases that should be reviewed before modeling.
Analysis:
- Most homes sell quickly (median 19 days), while a small subset drives a long tail.
- Negative DOM values imply data errors or backdated records that should be corrected or excluded.

## Percentage of homes sold above vs. below list price
Based on 397,305 valid records (non-missing close and list price):
- Above list price: 159,382 (40.12%)
- Below list price: 169,028 (42.54%)
- Exactly at list price: 68,895 (17.34%)
- The split is fairly balanced, suggesting mixed market conditions rather than a strongly seller- or buyer-dominated period.
- A sizable “at list” share indicates consistent pricing strategy or MLS practices in some areas.

## Apparent date consistency issues (e.g., close date before listing date)
- Close date before listing contract date: 58 records out of 397,306 valid pairs (0.0146%).
- Issue rate is very low, so it won’t materially affect aggregates, but those records should be fixed or removed for time-based analysis.

## Counties with the highest median prices
Top 10 by median close price:

| County | Median Close Price |
| --- | --- |
| Del Norte | 2,485,000 |
| Other County | 2,462,500 |
| San Mateo | 1,700,000 |
| Santa Clara | 1,600,000 |
| Santa Cruz | 1,200,000 |
| San Francisco | 1,180,000 |
| Orange | 1,175,000 |
| Marin | 1,170,000 |
| Alameda | 1,135,000 |
| Alpine | 1,100,000 |

Notes:
- "Other County" appears as a placeholder category and should be reviewed before reporting.

Analysis:
- High-median counties cluster in coastal/urban markets, consistent with California pricing patterns.
- Placeholder or miscoded county categories should be normalized to avoid skewed rankings.
