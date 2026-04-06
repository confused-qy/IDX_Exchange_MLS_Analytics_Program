# Week 2 Missing Value Analysis

Missing values include nulls and empty/whitespace-only strings.

## Listed_Final

| Column | Missing Count | Missing % | >90% Missing | Proposed Action |
| --- | --- | --- | --- | --- |
| business_type | 540,417 | 100.00% | True | drop (high missing) |
| above_grade_finished_area | 540,417 | 100.00% | True | drop (high missing) |
| covered_spaces | 540,417 | 100.00% | True | drop (high missing) |
| fireplaces_total | 540,417 | 100.00% | True | drop (high missing) |
| tax_annual_amount | 540,417 | 100.00% | True | drop (high missing) |
| tax_year | 540,417 | 100.00% | True | drop (high missing) |
| elementary_school_district | 540,417 | 100.00% | True | drop (high missing) |
| middle_or_junior_school_district | 540,417 | 100.00% | True | drop (high missing) |
| below_grade_finished_area | 537,391 | 99.44% | True | drop (high missing) |
| co_buyer_agent_first_name | 526,178 | 97.37% | True | drop (high missing) |
| builder_name | 515,183 | 95.33% | True | drop (high missing) |
| lot_size_dimensions | 512,204 | 94.78% | True | drop (high missing) |
| building_area_total | 492,354 | 91.11% | True | drop (high missing) |
| elementary_school | 476,067 | 88.09% | False | retain |
| middle_or_junior_school | 475,940 | 88.07% | False | retain |
| buyer_agency_compensation | 461,424 | 85.38% | False | retain |
| buyer_agency_compensation_type | 461,404 | 85.38% | False | retain |
| high_school | 455,963 | 84.37% | False | retain |
| co_list_agent_first_name | 419,868 | 77.69% | False | retain |
| co_list_agent_last_name | 419,467 | 77.62% | False | retain |
| co_list_office_name | 419,382 | 77.60% | False | retain |
| close_price_per_sqft | 396,890 | 73.44% | False | retain |
| close_price | 396,812 | 73.43% | False | retain |
| close_to_list_ratio | 396,812 | 73.43% | False | retain |
| buyer_office_aor | 395,460 | 73.18% | False | retain |
| buyer_office_name | 385,411 | 71.32% | False | retain |
| buyer_agent_first_name | 383,909 | 71.04% | False | retain |
| buyer_agent_mls_id | 383,296 | 70.93% | False | retain |
| buyer_agent_last_name | 383,188 | 70.91% | False | retain |
| close_date | 376,526 | 69.67% | False | retain |
| subdivision_name | 341,427 | 63.18% | False | retain |
| association_fee_frequency | 309,489 | 57.27% | False | retain |
| purchase_contract_date | 275,626 | 51.00% | False | retain |
| main_level_bedrooms | 246,525 | 45.62% | False | retain |
| high_school_district | 162,590 | 30.09% | False | retain |
| association_fee | 129,916 | 24.04% | False | retain |
| stories | 94,479 | 17.48% | False | retain |
| attached_garage_yn | 94,457 | 17.48% | False | retain |
| latitude | 80,155 | 14.83% | False | retain |
| longitude | 80,155 | 14.83% | False | retain |
| mls_area_major | 73,100 | 13.53% | False | retain |
| levels | 58,276 | 10.78% | False | retain |
| list_agent_email | 47,235 | 8.74% | False | retain |
| lot_size_acres | 44,558 | 8.25% | False | retain |
| lot_size_square_feet | 43,894 | 8.12% | False | retain |
| lot_size_area | 43,719 | 8.09% | False | retain |
| new_construction_yn | 37,131 | 6.87% | False | retain |
| garage_spaces | 30,037 | 5.56% | False | retain |
| contract_status_change_date | 6,053 | 1.12% | False | retain |
| list_agent_first_name | 4,238 | 0.78% | False | retain |
| property_sub_type | 1,251 | 0.23% | False | retain |
| year_built | 934 | 0.17% | False | retain |
| property_age | 934 | 0.17% | False | retain |
| original_list_price | 770 | 0.14% | False | retain |
| list_to_original_ratio | 770 | 0.14% | False | retain |
| unparsed_address | 681 | 0.13% | False | retain |
| city | 576 | 0.11% | False | retain |
| fireplace_yn | 572 | 0.11% | False | retain |
| living_area | 552 | 0.10% | False | retain |
| list_price_per_sqft | 552 | 0.10% | False | retain |
| bedrooms_total | 147 | 0.03% | False | retain |
| list_agent_full_name | 90 | 0.02% | False | retain |
| bathrooms_total_integer | 55 | 0.01% | False | retain |
| state_or_province | 54 | 0.01% | False | retain |
| list_agent_last_name | 39 | 0.01% | False | retain |
| parking_total | 20 | 0.00% | False | retain |
| postal_code | 13 | 0.00% | False | retain |
| listing_key | 0 | 0.00% | False | retain |
| listing_id | 0 | 0.00% | False | retain |
| listing_key_numeric | 0 | 0.00% | False | retain |
| mls_status | 0 | 0.00% | False | retain |
| listing_contract_date | 0 | 0.00% | False | retain |
| list_price | 0 | 0.00% | False | retain |
| days_on_market | 0 | 0.00% | False | retain |
| property_type | 0 | 0.00% | False | retain |
| county_or_parish | 0 | 0.00% | False | retain |
| list_office_name | 0 | 0.00% | False | retain |
| source_month | 0 | 0.00% | False | retain |
| listing_year | 0 | 0.00% | False | retain |
| listing_month | 0 | 0.00% | False | retain |
| listing_year_month | 0 | 0.00% | False | retain |
| has_garage | 0 | 0.00% | False | retain |
| has_fireplace | 0 | 0.00% | False | retain |
| has_new_construction | 0 | 0.00% | False | retain |

Proposed drops (high missing, non-core):
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

## Sold_Final

| Column | Missing Count | Missing % | >90% Missing | Proposed Action |
| --- | --- | --- | --- | --- |
| business_type | 397,307 | 100.00% | True | drop (high missing) |
| above_grade_finished_area | 397,307 | 100.00% | True | drop (high missing) |
| covered_spaces | 397,307 | 100.00% | True | drop (high missing) |
| fireplaces_total | 397,307 | 100.00% | True | drop (high missing) |
| tax_annual_amount | 397,307 | 100.00% | True | drop (high missing) |
| tax_year | 397,307 | 100.00% | True | drop (high missing) |
| elementary_school_district | 397,307 | 100.00% | True | drop (high missing) |
| middle_or_junior_school_district | 397,307 | 100.00% | True | drop (high missing) |
| waterfront_yn | 397,059 | 99.94% | True | drop (high missing) |
| below_grade_finished_area | 395,017 | 99.42% | True | drop (high missing) |
| basement_yn | 389,535 | 98.04% | True | drop (high missing) |
| lot_size_dimensions | 378,002 | 95.14% | True | drop (high missing) |
| builder_name | 377,789 | 95.09% | True | drop (high missing) |
| building_area_total | 369,547 | 93.01% | True | drop (high missing) |
| co_buyer_agent_first_name | 361,311 | 90.94% | True | drop (high missing) |
| originating_system_name | 358,351 | 90.19% | True | drop (high missing) |
| originating_system_sub_name | 358,351 | 90.19% | True | drop (high missing) |
| elementary_school | 344,347 | 86.67% | False | retain |
| middle_or_junior_school | 343,995 | 86.58% | False | retain |
| high_school | 328,085 | 82.58% | False | retain |
| co_list_agent_first_name | 306,382 | 77.11% | False | retain |
| co_list_agent_last_name | 306,147 | 77.06% | False | retain |
| co_list_office_name | 303,292 | 76.34% | False | retain |
| subdivision_name | 249,687 | 62.84% | False | retain |
| association_fee_frequency | 231,888 | 58.36% | False | retain |
| main_level_bedrooms | 166,692 | 41.96% | False | retain |
| flooring | 142,464 | 35.86% | False | retain |
| high_school_district | 108,741 | 27.37% | False | retain |
| association_fee | 90,917 | 22.88% | False | retain |
| stories | 61,464 | 15.47% | False | retain |
| attached_garage_yn | 60,628 | 15.26% | False | retain |
| mls_area_major | 53,077 | 13.36% | False | retain |
| buyer_agent_aor | 49,070 | 12.35% | False | retain |
| list_agent_aor | 46,186 | 11.62% | False | retain |
| levels | 38,553 | 9.70% | False | retain |
| pool_private_yn | 34,421 | 8.66% | False | retain |
| view_yn | 33,838 | 8.52% | False | retain |
| lot_size_acres | 31,321 | 7.88% | False | retain |
| lot_size_square_feet | 30,943 | 7.79% | False | retain |
| lot_size_area | 30,820 | 7.76% | False | retain |
| new_construction_yn | 29,422 | 7.41% | False | retain |
| list_agent_email | 28,716 | 7.23% | False | retain |
| buyer_office_aor | 21,425 | 5.39% | False | retain |
| garage_spaces | 17,028 | 4.29% | False | retain |
| latitude | 15,814 | 3.98% | False | retain |
| longitude | 15,814 | 3.98% | False | retain |
| buyer_office_name | 6,535 | 1.64% | False | retain |
| list_agent_first_name | 2,999 | 0.75% | False | retain |
| buyer_agent_first_name | 1,954 | 0.49% | False | retain |
| property_sub_type | 776 | 0.20% | False | retain |
| original_list_price | 716 | 0.18% | False | retain |
| contract_status_change_date | 589 | 0.15% | False | retain |
| buyer_agent_mls_id | 503 | 0.13% | False | retain |
| parking_total | 426 | 0.11% | False | retain |
| unparsed_address | 360 | 0.09% | False | retain |
| year_built | 356 | 0.09% | False | retain |
| property_age | 356 | 0.09% | False | retain |
| fireplace_yn | 316 | 0.08% | False | retain |
| city | 310 | 0.08% | False | retain |
| close_price_per_sqft | 230 | 0.06% | False | retain |
| living_area | 228 | 0.06% | False | retain |
| list_price_per_sqft | 228 | 0.06% | False | retain |
| purchase_contract_date | 194 | 0.05% | False | retain |
| buyer_agent_last_name | 167 | 0.04% | False | retain |
| list_agent_full_name | 85 | 0.02% | False | retain |
| bathrooms_total_integer | 69 | 0.02% | False | retain |
| list_agent_last_name | 40 | 0.01% | False | retain |
| bedrooms_total | 11 | 0.00% | False | retain |
| close_price | 2 | 0.00% | False | retain |
| postal_code | 2 | 0.00% | False | retain |
| close_to_list_ratio | 2 | 0.00% | False | retain |
| close_minus_list | 2 | 0.00% | False | retain |
| listing_contract_date | 1 | 0.00% | False | retain |
| listing_key | 0 | 0.00% | False | retain |
| listing_id | 0 | 0.00% | False | retain |
| listing_key_numeric | 0 | 0.00% | False | retain |
| mls_status | 0 | 0.00% | False | retain |
| close_date | 0 | 0.00% | False | retain |
| list_price | 0 | 0.00% | False | retain |
| days_on_market | 0 | 0.00% | False | retain |
| property_type | 0 | 0.00% | False | retain |
| county_or_parish | 0 | 0.00% | False | retain |
| state_or_province | 0 | 0.00% | False | retain |
| list_office_name | 0 | 0.00% | False | retain |
| source_month | 0 | 0.00% | False | retain |
| close_year | 0 | 0.00% | False | retain |
| close_month | 0 | 0.00% | False | retain |
| close_year_month | 0 | 0.00% | False | retain |
| has_garage | 0 | 0.00% | False | retain |
| has_fireplace | 0 | 0.00% | False | retain |
| has_pool | 0 | 0.00% | False | retain |
| has_view | 0 | 0.00% | False | retain |
| has_waterfront | 0 | 0.00% | False | retain |
| has_basement | 0 | 0.00% | False | retain |
| has_new_construction | 0 | 0.00% | False | retain |

Proposed drops (high missing, non-core):
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

## Additional Drop Candidates (Not Missing-Driven)
These are not flagged by missingness, but are often removed in analytics-focused datasets to reduce noise or PII exposure. 

Listed_Final candidates:
- `list_agent_email` (PII, typically not used for market analysis)
- `list_agent_first_name`
- `list_agent_last_name`
- `list_agent_full_name`
- `list_office_name`
- `co_list_agent_first_name`
- `co_list_agent_last_name`
- `co_list_office_name`
- `buyer_agent_first_name`
- `buyer_agent_last_name`
- `buyer_agent_mls_id`
- `buyer_office_name`
- `buyer_office_aor`
- `co_buyer_agent_first_name`
- `buyer_agency_compensation`
- `buyer_agency_compensation_type`

Sold_Final candidates:
- `list_agent_email` (PII, typically not used for market analysis)
- `list_agent_first_name`
- `list_agent_last_name`
- `list_agent_full_name`
- `list_agent_aor`
- `list_office_name`
- `co_list_agent_first_name`
- `co_list_agent_last_name`
- `co_list_office_name`
- `buyer_agent_first_name`
- `buyer_agent_last_name`
- `buyer_agent_mls_id`
- `buyer_agent_aor`
- `buyer_office_name`
- `buyer_office_aor`
- `co_buyer_agent_first_name`

