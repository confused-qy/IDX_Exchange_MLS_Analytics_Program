# Week 2 Missing Value Analysis

Run date: 2026-04-08

Missing values include nulls and empty/whitespace-only strings.

## Listed_Final

### Columns With Missing >= 90% (Drop)
- business_type
- above_grade_finished_area
- covered_spaces
- fireplaces_total
- tax_annual_amount
- tax_year
- elementary_school_district
- middle_or_junior_school_district
- below_grade_finished_area
- co_buyer_agent_first_name
- builder_name
- lot_size_dimensions
- building_area_total

### Full Review (Sorted by Missing % Desc)
| Column | Missing Count | Missing % | Decision |
| --- | --- | --- | --- |
| business_type | 540,417 | 100.00% | drop (>=90% missing) |
| above_grade_finished_area | 540,417 | 100.00% | drop (>=90% missing) |
| covered_spaces | 540,417 | 100.00% | drop (>=90% missing) |
| fireplaces_total | 540,417 | 100.00% | drop (>=90% missing) |
| tax_annual_amount | 540,417 | 100.00% | drop (>=90% missing) |
| tax_year | 540,417 | 100.00% | drop (>=90% missing) |
| elementary_school_district | 540,417 | 100.00% | drop (>=90% missing) |
| middle_or_junior_school_district | 540,417 | 100.00% | drop (>=90% missing) |
| below_grade_finished_area | 537,391 | 99.44% | drop (>=90% missing) |
| co_buyer_agent_first_name | 526,178 | 97.37% | drop (>=90% missing) |
| builder_name | 515,183 | 95.33% | drop (>=90% missing) |
| lot_size_dimensions | 512,204 | 94.78% | drop (>=90% missing) |
| building_area_total | 492,354 | 91.11% | drop (>=90% missing) |
| elementary_school | 476,067 | 88.09% | retain |
| middle_or_junior_school | 475,940 | 88.07% | retain |
| buyer_agency_compensation | 461,424 | 85.38% | drop (PII / low analytic value) |
| buyer_agency_compensation_type | 461,404 | 85.38% | drop (PII / low analytic value) |
| high_school | 455,963 | 84.37% | retain |
| co_list_agent_first_name | 419,868 | 77.69% | drop (PII / low analytic value) |
| co_list_agent_last_name | 419,467 | 77.62% | drop (PII / low analytic value) |
| co_list_office_name | 419,382 | 77.60% | drop (PII / low analytic value) |
| close_price_per_sqft | 396,890 | 73.44% | retain |
| close_price | 396,812 | 73.43% | retain (core) |
| close_to_list_ratio | 396,812 | 73.43% | retain |
| buyer_office_aor | 395,460 | 73.18% | drop (PII / low analytic value) |
| buyer_office_name | 385,411 | 71.32% | drop (PII / low analytic value) |
| buyer_agent_first_name | 383,909 | 71.04% | drop (PII / low analytic value) |
| buyer_agent_mls_id | 383,296 | 70.93% | drop (PII / low analytic value) |
| buyer_agent_last_name | 383,188 | 70.91% | drop (PII / low analytic value) |
| close_date | 376,526 | 69.67% | retain (core) |
| subdivision_name | 341,427 | 63.18% | retain |
| association_fee_frequency | 309,489 | 57.27% | retain |
| purchase_contract_date | 275,626 | 51.00% | retain |
| main_level_bedrooms | 246,525 | 45.62% | retain |
| high_school_district | 162,590 | 30.09% | retain |
| association_fee | 129,916 | 24.04% | retain |
| stories | 94,479 | 17.48% | retain |
| attached_garage_yn | 94,457 | 17.48% | retain |
| latitude | 80,155 | 14.83% | retain (core) |
| longitude | 80,155 | 14.83% | retain (core) |
| mls_area_major | 73,100 | 13.53% | retain |
| levels | 58,276 | 10.78% | retain |
| list_agent_email | 47,235 | 8.74% | drop (PII / low analytic value) |
| lot_size_acres | 44,558 | 8.25% | retain |
| lot_size_square_feet | 43,894 | 8.12% | retain (core) |
| lot_size_area | 43,719 | 8.09% | retain |
| new_construction_yn | 37,131 | 6.87% | retain |
| garage_spaces | 30,037 | 5.56% | retain |
| contract_status_change_date | 6,053 | 1.12% | retain |
| list_agent_first_name | 4,238 | 0.78% | drop (PII / low analytic value) |
| property_sub_type | 1,251 | 0.23% | retain (core) |
| year_built | 934 | 0.17% | retain (core) |
| property_age | 934 | 0.17% | retain |
| original_list_price | 770 | 0.14% | retain (core) |
| list_to_original_ratio | 770 | 0.14% | retain |
| unparsed_address | 681 | 0.13% | retain |
| city | 576 | 0.11% | retain (core) |
| fireplace_yn | 572 | 0.11% | retain |
| living_area | 552 | 0.10% | retain (core) |
| list_price_per_sqft | 552 | 0.10% | retain |
| bedrooms_total | 147 | 0.03% | retain (core) |
| list_agent_full_name | 90 | 0.02% | drop (PII / low analytic value) |
| bathrooms_total_integer | 55 | 0.01% | retain (core) |
| state_or_province | 54 | 0.01% | retain (core) |
| list_agent_last_name | 39 | 0.01% | drop (PII / low analytic value) |
| parking_total | 20 | 0.00% | retain |
| postal_code | 13 | 0.00% | retain (core) |
| listing_key | 0 | 0.00% | retain (core) |
| listing_id | 0 | 0.00% | retain (core) |
| listing_key_numeric | 0 | 0.00% | retain (core) |
| mls_status | 0 | 0.00% | retain (core) |
| listing_contract_date | 0 | 0.00% | retain (core) |
| list_price | 0 | 0.00% | retain (core) |
| days_on_market | 0 | 0.00% | retain (core) |
| property_type | 0 | 0.00% | retain (core) |
| county_or_parish | 0 | 0.00% | retain |
| list_office_name | 0 | 0.00% | drop (PII / low analytic value) |
| source_month | 0 | 0.00% | retain (core) |
| listing_year | 0 | 0.00% | retain (core) |
| listing_month | 0 | 0.00% | retain (core) |
| listing_year_month | 0 | 0.00% | retain (core) |
| has_garage | 0 | 0.00% | retain |
| has_fireplace | 0 | 0.00% | retain |
| has_new_construction | 0 | 0.00% | retain |

### Drop Columns (All)
- business_type
- above_grade_finished_area
- covered_spaces
- fireplaces_total
- tax_annual_amount
- tax_year
- elementary_school_district
- middle_or_junior_school_district
- below_grade_finished_area
- co_buyer_agent_first_name
- builder_name
- lot_size_dimensions
- building_area_total
- buyer_agency_compensation
- buyer_agency_compensation_type
- co_list_agent_first_name
- co_list_agent_last_name
- co_list_office_name
- buyer_office_aor
- buyer_office_name
- buyer_agent_first_name
- buyer_agent_mls_id
- buyer_agent_last_name
- list_agent_email
- list_agent_first_name
- list_agent_full_name
- list_agent_last_name
- list_office_name

### Columns To Keep
- `elementary_school`: School zone segmentation if used.
- `middle_or_junior_school`: School zone segmentation if used.
- `high_school`: School zone segmentation if used.
- `close_price_per_sqft`: Normalization for price comparisons.
- `close_price`: Final price used for pricing outcomes.
- `close_to_list_ratio`: Measures negotiation outcome.
- `close_date`: Final transaction date for sold/closed analyses.
- `subdivision_name`: Neighborhood-level grouping.
- `association_fee_frequency`: HOA fee cadence.
- `purchase_contract_date`: Captures contract timing for pipeline analysis.
- `main_level_bedrooms`: Accessibility/functional layout indicator.
- `high_school_district`: District-level school segmentation.
- `association_fee`: HOA cost impact on pricing.
- `stories`: Home layout indicator.
- `attached_garage_yn`: Garage type/amenity indicator.
- `latitude`: Geospatial analysis and mapping.
- `longitude`: Geospatial analysis and mapping.
- `mls_area_major`: Geographic segmentation.
- `levels`: Home layout detail.
- `lot_size_acres`: Alternate land size measure.
- `lot_size_square_feet`: Land size normalization and comparisons.
- `lot_size_area`: Land size as provided by source.
- `new_construction_yn`: New build segmentation.
- `garage_spaces`: Amenity affecting pricing and desirability.
- `contract_status_change_date`: Measures status transitions and timing.
- `property_sub_type`: Finer property segmentation.
- `year_built`: Used to compute property age and vintage effects.
- `property_age`: Captures age effect on value.
- `original_list_price`: Needed for price change and ratio metrics.
- `list_to_original_ratio`: Measures price movement from original.
- `unparsed_address`: Useful for geocoding or QA if needed.
- `city`: Primary location dimension.
- `fireplace_yn`: Amenity indicator.
- `living_area`: Essential for size normalization and price per sqft.
- `list_price_per_sqft`: Normalization for price comparisons.
- `bedrooms_total`: Core property attribute for comparability.
- `bathrooms_total_integer`: Core property attribute for comparability.
- `state_or_province`: Primary location dimension.
- `parking_total`: Parking capacity indicator.
- `postal_code`: Fine-grained location segmentation.
- `listing_key`: Primary unique identifier for joining and de-duplication.
- `listing_id`: Secondary listing identifier useful for cross-referencing.
- `listing_key_numeric`: Numeric ID helpful for sorting and joins.
- `mls_status`: Tracks listing status for lifecycle analysis.
- `listing_contract_date`: Anchor date for time-series and days-on-market context.
- `list_price`: Core pricing metric used across analyses.
- `days_on_market`: Key market liquidity metric.
- `property_type`: Core segmentation field.
- `county_or_parish`: Regional segmentation.
- `source_month`: Tracks monthly source file for QC.
- `listing_year`: Derived time dimension for listings.
- `listing_month`: Derived time dimension for listings.
- `listing_year_month`: Derived time dimension for listings.
- `has_garage`: Amenity indicator.
- `has_fireplace`: Amenity indicator.
- `has_new_construction`: Amenity/segment indicator.

### Core Columns
- listing_key
- listing_id
- listing_key_numeric
- mls_status
- listing_contract_date
- close_date
- list_price
- original_list_price
- close_price
- days_on_market
- property_type
- property_sub_type
- living_area
- bedrooms_total
- bathrooms_total_integer
- year_built
- lot_size_square_feet
- city
- state_or_province
- postal_code
- latitude
- longitude
- source_month
- listing_year
- listing_month
- listing_year_month

## Sold_Final

### Columns With Missing >= 90% (Drop)
- business_type
- above_grade_finished_area
- covered_spaces
- fireplaces_total
- tax_annual_amount
- tax_year
- elementary_school_district
- middle_or_junior_school_district
- waterfront_yn
- below_grade_finished_area
- basement_yn
- lot_size_dimensions
- builder_name
- building_area_total
- co_buyer_agent_first_name
- originating_system_name
- originating_system_sub_name

### Full Review (Sorted by Missing % Desc)
| Column | Missing Count | Missing % | Decision |
| --- | --- | --- | --- |
| business_type | 397,307 | 100.00% | drop (>=90% missing) |
| above_grade_finished_area | 397,307 | 100.00% | drop (>=90% missing) |
| covered_spaces | 397,307 | 100.00% | drop (>=90% missing) |
| fireplaces_total | 397,307 | 100.00% | drop (>=90% missing) |
| tax_annual_amount | 397,307 | 100.00% | drop (>=90% missing) |
| tax_year | 397,307 | 100.00% | drop (>=90% missing) |
| elementary_school_district | 397,307 | 100.00% | drop (>=90% missing) |
| middle_or_junior_school_district | 397,307 | 100.00% | drop (>=90% missing) |
| waterfront_yn | 397,059 | 99.94% | drop (>=90% missing) |
| below_grade_finished_area | 395,017 | 99.42% | drop (>=90% missing) |
| basement_yn | 389,535 | 98.04% | drop (>=90% missing) |
| lot_size_dimensions | 378,002 | 95.14% | drop (>=90% missing) |
| builder_name | 377,789 | 95.09% | drop (>=90% missing) |
| building_area_total | 369,547 | 93.01% | drop (>=90% missing) |
| co_buyer_agent_first_name | 361,311 | 90.94% | drop (>=90% missing) |
| originating_system_name | 358,351 | 90.19% | drop (>=90% missing) |
| originating_system_sub_name | 358,351 | 90.19% | drop (>=90% missing) |
| elementary_school | 344,347 | 86.67% | retain |
| middle_or_junior_school | 343,995 | 86.58% | retain |
| high_school | 328,085 | 82.58% | retain |
| co_list_agent_first_name | 306,382 | 77.11% | drop (PII / low analytic value) |
| co_list_agent_last_name | 306,147 | 77.06% | drop (PII / low analytic value) |
| co_list_office_name | 303,292 | 76.34% | drop (PII / low analytic value) |
| subdivision_name | 249,687 | 62.84% | retain |
| association_fee_frequency | 231,888 | 58.36% | retain |
| main_level_bedrooms | 166,692 | 41.96% | retain |
| flooring | 142,464 | 35.86% | retain |
| high_school_district | 108,741 | 27.37% | retain |
| association_fee | 90,917 | 22.88% | retain |
| stories | 61,464 | 15.47% | retain |
| attached_garage_yn | 60,628 | 15.26% | retain |
| mls_area_major | 53,077 | 13.36% | retain |
| buyer_agent_aor | 49,070 | 12.35% | drop (PII / low analytic value) |
| list_agent_aor | 46,186 | 11.62% | drop (PII / low analytic value) |
| levels | 38,553 | 9.70% | retain |
| pool_private_yn | 34,421 | 8.66% | retain |
| view_yn | 33,838 | 8.52% | retain |
| lot_size_acres | 31,321 | 7.88% | retain |
| lot_size_square_feet | 30,943 | 7.79% | retain (core) |
| lot_size_area | 30,820 | 7.76% | retain |
| new_construction_yn | 29,422 | 7.41% | retain |
| list_agent_email | 28,716 | 7.23% | drop (PII / low analytic value) |
| buyer_office_aor | 21,425 | 5.39% | drop (PII / low analytic value) |
| garage_spaces | 17,028 | 4.29% | retain |
| latitude | 15,814 | 3.98% | retain (core) |
| longitude | 15,814 | 3.98% | retain (core) |
| buyer_office_name | 6,535 | 1.64% | drop (PII / low analytic value) |
| list_agent_first_name | 2,999 | 0.75% | drop (PII / low analytic value) |
| buyer_agent_first_name | 1,954 | 0.49% | drop (PII / low analytic value) |
| property_sub_type | 776 | 0.20% | retain (core) |
| original_list_price | 716 | 0.18% | retain (core) |
| contract_status_change_date | 589 | 0.15% | retain |
| buyer_agent_mls_id | 503 | 0.13% | drop (PII / low analytic value) |
| parking_total | 426 | 0.11% | retain |
| unparsed_address | 360 | 0.09% | retain |
| year_built | 356 | 0.09% | retain (core) |
| property_age | 356 | 0.09% | retain |
| fireplace_yn | 316 | 0.08% | retain |
| city | 310 | 0.08% | retain (core) |
| close_price_per_sqft | 230 | 0.06% | retain |
| living_area | 228 | 0.06% | retain (core) |
| list_price_per_sqft | 228 | 0.06% | retain |
| purchase_contract_date | 194 | 0.05% | retain |
| buyer_agent_last_name | 167 | 0.04% | drop (PII / low analytic value) |
| list_agent_full_name | 85 | 0.02% | drop (PII / low analytic value) |
| bathrooms_total_integer | 69 | 0.02% | retain (core) |
| list_agent_last_name | 40 | 0.01% | drop (PII / low analytic value) |
| bedrooms_total | 11 | 0.00% | retain (core) |
| close_price | 2 | 0.00% | retain (core) |
| postal_code | 2 | 0.00% | retain (core) |
| close_to_list_ratio | 2 | 0.00% | retain |
| close_minus_list | 2 | 0.00% | retain |
| listing_contract_date | 1 | 0.00% | retain (core) |
| listing_key | 0 | 0.00% | retain (core) |
| listing_id | 0 | 0.00% | retain (core) |
| listing_key_numeric | 0 | 0.00% | retain (core) |
| mls_status | 0 | 0.00% | retain (core) |
| close_date | 0 | 0.00% | retain (core) |
| list_price | 0 | 0.00% | retain (core) |
| days_on_market | 0 | 0.00% | retain (core) |
| property_type | 0 | 0.00% | retain (core) |
| county_or_parish | 0 | 0.00% | retain |
| state_or_province | 0 | 0.00% | retain (core) |
| list_office_name | 0 | 0.00% | drop (PII / low analytic value) |
| source_month | 0 | 0.00% | retain (core) |
| close_year | 0 | 0.00% | retain (core) |
| close_month | 0 | 0.00% | retain (core) |
| close_year_month | 0 | 0.00% | retain (core) |
| has_garage | 0 | 0.00% | retain |
| has_fireplace | 0 | 0.00% | retain |
| has_pool | 0 | 0.00% | retain |
| has_view | 0 | 0.00% | retain |
| has_waterfront | 0 | 0.00% | retain |
| has_basement | 0 | 0.00% | retain |
| has_new_construction | 0 | 0.00% | retain |

### Drop Columns (All)
- business_type
- above_grade_finished_area
- covered_spaces
- fireplaces_total
- tax_annual_amount
- tax_year
- elementary_school_district
- middle_or_junior_school_district
- waterfront_yn
- below_grade_finished_area
- basement_yn
- lot_size_dimensions
- builder_name
- building_area_total
- co_buyer_agent_first_name
- originating_system_name
- originating_system_sub_name
- co_list_agent_first_name
- co_list_agent_last_name
- co_list_office_name
- buyer_agent_aor
- list_agent_aor
- list_agent_email
- buyer_office_aor
- buyer_office_name
- list_agent_first_name
- buyer_agent_first_name
- buyer_agent_mls_id
- buyer_agent_last_name
- list_agent_full_name
- list_agent_last_name
- list_office_name

### Columns To Keep
- `elementary_school`: School zone segmentation if used.
- `middle_or_junior_school`: School zone segmentation if used.
- `high_school`: School zone segmentation if used.
- `subdivision_name`: Neighborhood-level grouping.
- `association_fee_frequency`: HOA fee cadence.
- `main_level_bedrooms`: Accessibility/functional layout indicator.
- `flooring`: Interior feature detail (if used).
- `high_school_district`: District-level school segmentation.
- `association_fee`: HOA cost impact on pricing.
- `stories`: Home layout indicator.
- `attached_garage_yn`: Garage type/amenity indicator.
- `mls_area_major`: Geographic segmentation.
- `levels`: Home layout detail.
- `pool_private_yn`: Amenity indicator.
- `view_yn`: Amenity indicator.
- `lot_size_acres`: Alternate land size measure.
- `lot_size_square_feet`: Land size normalization and comparisons.
- `lot_size_area`: Land size as provided by source.
- `new_construction_yn`: New build segmentation.
- `garage_spaces`: Amenity affecting pricing and desirability.
- `latitude`: Geospatial analysis and mapping.
- `longitude`: Geospatial analysis and mapping.
- `property_sub_type`: Finer property segmentation.
- `original_list_price`: Needed for price change and ratio metrics.
- `contract_status_change_date`: Measures status transitions and timing.
- `parking_total`: Parking capacity indicator.
- `unparsed_address`: Useful for geocoding or QA if needed.
- `year_built`: Used to compute property age and vintage effects.
- `property_age`: Captures age effect on value.
- `fireplace_yn`: Amenity indicator.
- `city`: Primary location dimension.
- `close_price_per_sqft`: Normalization for price comparisons.
- `living_area`: Essential for size normalization and price per sqft.
- `list_price_per_sqft`: Normalization for price comparisons.
- `purchase_contract_date`: Captures contract timing for pipeline analysis.
- `bathrooms_total_integer`: Core property attribute for comparability.
- `bedrooms_total`: Core property attribute for comparability.
- `close_price`: Final price used for pricing outcomes.
- `postal_code`: Fine-grained location segmentation.
- `close_to_list_ratio`: Measures negotiation outcome.
- `close_minus_list`: Absolute negotiation outcome.
- `listing_contract_date`: Anchor date for time-series and days-on-market context.
- `listing_key`: Primary unique identifier for joining and de-duplication.
- `listing_id`: Secondary listing identifier useful for cross-referencing.
- `listing_key_numeric`: Numeric ID helpful for sorting and joins.
- `mls_status`: Tracks listing status for lifecycle analysis.
- `close_date`: Final transaction date for sold/closed analyses.
- `list_price`: Core pricing metric used across analyses.
- `days_on_market`: Key market liquidity metric.
- `property_type`: Core segmentation field.
- `county_or_parish`: Regional segmentation.
- `state_or_province`: Primary location dimension.
- `source_month`: Tracks monthly source file for QC.
- `close_year`: Derived time dimension for sales.
- `close_month`: Derived time dimension for sales.
- `close_year_month`: Derived time dimension for sales.
- `has_garage`: Amenity indicator.
- `has_fireplace`: Amenity indicator.
- `has_pool`: Amenity indicator.
- `has_view`: Amenity indicator.
- `has_waterfront`: Amenity indicator.
- `has_basement`: Amenity indicator.
- `has_new_construction`: Amenity/segment indicator.

### Core Columns
- listing_key
- listing_id
- listing_key_numeric
- mls_status
- close_date
- listing_contract_date
- list_price
- original_list_price
- close_price
- days_on_market
- property_type
- property_sub_type
- living_area
- bedrooms_total
- bathrooms_total_integer
- year_built
- lot_size_square_feet
- city
- state_or_province
- postal_code
- latitude
- longitude
- source_month
- close_year
- close_month
- close_year_month
