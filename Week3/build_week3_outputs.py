import pandas as pd


LISTED_KEEP_COLS = [
    "elementary_school",
    "middle_or_junior_school",
    "high_school",
    "close_price_per_sqft",
    "close_price",
    "close_to_list_ratio",
    "close_date",
    "subdivision_name",
    "association_fee_frequency",
    "purchase_contract_date",
    "main_level_bedrooms",
    "high_school_district",
    "association_fee",
    "stories",
    "attached_garage_yn",
    "latitude",
    "longitude",
    "mls_area_major",
    "levels",
    "lot_size_acres",
    "lot_size_square_feet",
    "lot_size_area",
    "new_construction_yn",
    "garage_spaces",
    "contract_status_change_date",
    "property_sub_type",
    "year_built",
    "property_age",
    "original_list_price",
    "list_to_original_ratio",
    "unparsed_address",
    "city",
    "fireplace_yn",
    "living_area",
    "list_price_per_sqft",
    "bedrooms_total",
    "bathrooms_total_integer",
    "state_or_province",
    "parking_total",
    "postal_code",
    "listing_key",
    "listing_id",
    "listing_key_numeric",
    "mls_status",
    "listing_contract_date",
    "list_price",
    "days_on_market",
    "property_type",
    "county_or_parish",
    "source_month",
    "listing_year",
    "listing_month",
    "listing_year_month",
    "has_garage",
    "has_fireplace",
    "has_new_construction",
]

LISTED_CORE_COLS = [
    "listing_key",
    "listing_id",
    "listing_key_numeric",
    "mls_status",
    "listing_contract_date",
    "close_date",
    "list_price",
    "original_list_price",
    "close_price",
    "days_on_market",
    "property_type",
    "property_sub_type",
    "living_area",
    "bedrooms_total",
    "bathrooms_total_integer",
    "year_built",
    "lot_size_square_feet",
    "city",
    "state_or_province",
    "postal_code",
    "latitude",
    "longitude",
    "source_month",
    "listing_year",
    "listing_month",
    "listing_year_month",
]

SOLD_KEEP_COLS = [
    "elementary_school",
    "middle_or_junior_school",
    "high_school",
    "subdivision_name",
    "association_fee_frequency",
    "main_level_bedrooms",
    "flooring",
    "high_school_district",
    "association_fee",
    "stories",
    "attached_garage_yn",
    "mls_area_major",
    "levels",
    "pool_private_yn",
    "view_yn",
    "lot_size_acres",
    "lot_size_square_feet",
    "lot_size_area",
    "new_construction_yn",
    "garage_spaces",
    "latitude",
    "longitude",
    "property_sub_type",
    "original_list_price",
    "contract_status_change_date",
    "parking_total",
    "unparsed_address",
    "year_built",
    "property_age",
    "fireplace_yn",
    "city",
    "close_price_per_sqft",
    "living_area",
    "list_price_per_sqft",
    "purchase_contract_date",
    "bathrooms_total_integer",
    "bedrooms_total",
    "close_price",
    "postal_code",
    "close_to_list_ratio",
    "close_minus_list",
    "listing_contract_date",
    "listing_key",
    "listing_id",
    "listing_key_numeric",
    "mls_status",
    "close_date",
    "list_price",
    "days_on_market",
    "property_type",
    "county_or_parish",
    "state_or_province",
    "source_month",
    "close_year",
    "close_month",
    "close_year_month",
    "has_garage",
    "has_fireplace",
    "has_pool",
    "has_view",
    "has_waterfront",
    "has_basement",
    "has_new_construction",
]

SOLD_CORE_COLS = [
    "listing_key",
    "listing_id",
    "listing_key_numeric",
    "mls_status",
    "close_date",
    "listing_contract_date",
    "list_price",
    "original_list_price",
    "close_price",
    "days_on_market",
    "property_type",
    "property_sub_type",
    "living_area",
    "bedrooms_total",
    "bathrooms_total_integer",
    "year_built",
    "lot_size_square_feet",
    "city",
    "state_or_province",
    "postal_code",
    "latitude",
    "longitude",
    "source_month",
    "close_year",
    "close_month",
    "close_year_month",
]


def select_columns(df, columns, label):
    missing = [c for c in columns if c not in df.columns]
    if missing:
        print(f"[WARN] {label}: missing {len(missing)} columns: {missing}")
    keep = [c for c in columns if c in df.columns]
    return df[keep]


def main():
    root = "/Users/confused_qy/coding/IDXExchange"

    listed_path = f"{root}/Listed_Final.csv"
    sold_path = f"{root}/Sold_Final.csv"

    listed_df = pd.read_csv(listed_path, low_memory=False)
    sold_df = pd.read_csv(sold_path, low_memory=False)

    listed_keep = select_columns(listed_df, LISTED_KEEP_COLS, "Listed_KeepCols")
    listed_core = select_columns(listed_df, LISTED_CORE_COLS, "Listed_CoreCols")
    sold_keep = select_columns(sold_df, SOLD_KEEP_COLS, "Sold_KeepCols")
    sold_core = select_columns(sold_df, SOLD_CORE_COLS, "Sold_CoreCols")

    listed_keep.to_csv(f"{root}/Listed_KeepCols.csv", index=False)
    listed_core.to_csv(f"{root}/Listed_CoreCols.csv", index=False)
    sold_keep.to_csv(f"{root}/Sold_KeepCols.csv", index=False)
    sold_core.to_csv(f"{root}/Sold_CoreCols.csv", index=False)

    print("Done. Wrote 4 files to IDXExchange root.")


if __name__ == "__main__":
    main()
