# IDX Exchange MLS Analytics Program

This repository contains the internship project work for building a progressive MLS analytics pipeline. Each phase builds on the previous one, from raw MLS file preparation through feature engineering, outlier control, and Tableau-ready market analytics datasets.

## Program Overview
The internship is structured as a progressive pipeline:
- Data Cleaning: Prepare raw data for reliable analysis
- Market Analytics: Engineer key housing market metrics
- Competitive Intelligence: Identify top agents and brokerages
- Data Quality: Flag invalid values and statistical outliers without overwriting source records
- Dashboard Development: Build interactive Tableau dashboards
- Market Insights: Communicate findings through reports and presentations

## Program Details
- Primary tools: Python (Pandas), Tableau Desktop
- Data source: CoreLogic Trestle API via IDX Exchange pipeline
- Dataset types: Monthly MLS Listing and Sold transaction CSV files
- Final deliverables: Tableau dashboards + 1-page market intelligence report + presentation

## Repo Structure
- `Week1/`: Monthly file aggregation, cleaning, and feature engineering
- `Week2/`: Missing value analysis, column retention decisions, and numeric distribution EDA
- `Week3/`: Mortgage rate enrichment and weekly output generation
- `Week4/`: Data cleaning preparation, type standardization, invalid-value flags, date checks, and coordinate checks
- `Week5/`: Feature engineering, sample outputs, and segment summary tables
- `Week6/`: Tableau variable planning and dashboard metric definitions
- `Week7/`: IQR outlier detection, full flagged datasets, clean filtered datasets, and Tableau readiness review

## Typical Workflow
1. Place monthly `CRMLSListingYYYYMM.csv` and `CRMLSSoldYYYYMM.csv` files at repo root or `raw/`.
2. Run Week 1 scripts to generate combined datasets:
   - `Week1/concat_clean_fe_listed.py`
   - `Week1/concat_clean_fe_sold.py`
3. Run Week 2 missing value analysis:
   - `Week2/missing_value_analysis.py`
4. Run Week 2 numeric distribution analysis:
   - `Week2/Numeric_Distribution/numeric_distribution.py`
   - Review `Week2/Numeric_Distribution/analysis.md`
5. Run Week 4 cleaning preparation:
   - `Week4/data_cleaning_preparation.py`
   - Outputs: `Listed_Cleaned.csv`, `Sold_Cleaned.csv`
6. Run Week 5 feature engineering:
   - `Week5/feature_engineering.py`
   - Outputs: `week5_output/Listed_Week5_Features.csv`, `week5_output/Sold_Week5_Features.csv`
7. Run Week 5 segment summaries:
   - `Week5/segment_summary.py`
   - Outputs: `week5_output/SegmentSummary_*.csv`
8. Review Week 6 Tableau variable plan:
   - `Week6/week6_tableau_variables.md`
9. Run Week 7 IQR outlier detection:
   - `Week7/outlier_detection_iqr.py`
   - Outputs: `week7_output/`

## Current Tableau-Ready Files
Use the Week 7 clean filtered datasets as the main Tableau sources:

- `week7_output/Sold_Week7_Clean_Filtered.csv`
- `week7_output/Listed_Week7_Clean_Filtered.csv`

Recommended use:

- Sold dataset: median close price, average days on market, sales volume, price per square foot, close-to-list metrics, agent and office production.
- Listed dataset: new listings, listing price trends, listing-side inventory analysis, geography and property subtype filters.

The full flagged files should be kept for audit and data quality review, but they should not be the primary Tableau source for final dashboards because they retain invalid numeric records and IQR outliers.
