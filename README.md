# IDX Exchange MLS Analytics Program

This repository contains the internship project work for building a progressive MLS analytics pipeline. Each phase builds on the previous one, from data cleaning through market insights.

## Program Overview
The internship is structured as a progressive pipeline:
- Data Cleaning: Prepare raw data for reliable analysis
- Market Analytics: Engineer key housing market metrics
- Competitive Intelligence: Identify top agents and brokerages
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

## Outputs (Latest)
- `Listed_Final.csv`
- `Sold_Final.csv`
- `Week2/missing_value_analysis.md`
- `Week2/Numeric_Distribution/numeric_distribution.md`
- `Week2/Numeric_Distribution/analysis.md`
