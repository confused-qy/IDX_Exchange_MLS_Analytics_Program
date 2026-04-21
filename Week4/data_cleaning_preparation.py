from pathlib import Path

import pandas as pd


ROOT = Path("/Users/confused_qy/coding/IDXExchange")

INPUTS = {
    "listed": ROOT / "Listed_KeepCols_WithRates.csv",
    "sold": ROOT / "Sold_KeepCols_WithRates.csv",
}

OUTPUTS = {
    "listed": ROOT / "Listed_Cleaned.csv",
    "sold": ROOT / "Sold_Cleaned.csv",
}

DATE_COLS = [
    "close_date",
    "purchase_contract_date",
    "listing_contract_date",
    "contract_status_change_date",
]

NUMERIC_COLS = [
    "close_price",
    "living_area",
    "days_on_market",
    "bedrooms_total",
    "bathrooms_total_integer",
    "latitude",
    "longitude",
    "rate_30yr_fixed",
]

REDUNDANT_COLS = {
    # Derived from listing_contract_date and no longer needed after standardizing date columns.
    "listed": ["listing_year", "listing_month", "listing_year_month"],
    # Derived from close_date and no longer needed after standardizing date columns.
    "sold": ["close_year", "close_month", "close_year_month"],
}


def safe_to_datetime(df: pd.DataFrame, cols: list[str]) -> None:
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")


def safe_to_numeric(df: pd.DataFrame, cols: list[str]) -> None:
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


def build_flags(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Invalid numeric values requested by handbook.
    out["invalid_close_price_flag"] = out["close_price"] <= 0
    out["invalid_living_area_flag"] = out["living_area"] <= 0
    out["invalid_days_on_market_flag"] = out["days_on_market"] < 0
    out["invalid_bedrooms_flag"] = out["bedrooms_total"] < 0
    out["invalid_bathrooms_flag"] = out["bathrooms_total_integer"] < 0
    out["invalid_numeric_flag"] = (
        out["invalid_close_price_flag"]
        | out["invalid_living_area_flag"]
        | out["invalid_days_on_market_flag"]
        | out["invalid_bedrooms_flag"]
        | out["invalid_bathrooms_flag"]
    )

    # Date consistency checks.
    out["listing_after_close_flag"] = (
        out["listing_contract_date"].notna()
        & out["close_date"].notna()
        & (out["listing_contract_date"] > out["close_date"])
    )
    out["purchase_after_close_flag"] = (
        out["purchase_contract_date"].notna()
        & out["close_date"].notna()
        & (out["purchase_contract_date"] > out["close_date"])
    )
    out["negative_timeline_flag"] = (
        out["listing_contract_date"].notna()
        & out["purchase_contract_date"].notna()
        & (out["purchase_contract_date"] < out["listing_contract_date"])
    )
    out["date_inconsistency_flag"] = (
        out["listing_after_close_flag"]
        | out["purchase_after_close_flag"]
        | out["negative_timeline_flag"]
    )

    # Geographic quality checks.
    out["coord_missing_flag"] = out["latitude"].isna() | out["longitude"].isna()
    out["coord_zero_flag"] = (out["latitude"] == 0) | (out["longitude"] == 0)
    out["positive_longitude_flag"] = out["longitude"] > 0
    out["implausible_coord_flag"] = (
        out["latitude"].notna()
        & out["longitude"].notna()
        & (~out["coord_zero_flag"])
        & (
            (out["latitude"] < 32.0)
            | (out["latitude"] > 42.5)
            | (out["longitude"] < -125.0)
            | (out["longitude"] > -113.0)
        )
    )
    out["geo_invalid_flag"] = (
        out["coord_missing_flag"]
        | out["coord_zero_flag"]
        | out["positive_longitude_flag"]
        | out["implausible_coord_flag"]
    )

    return out


def clean_dataset(df: pd.DataFrame, dataset_name: str) -> tuple[pd.DataFrame, dict]:
    before_rows = len(df)

    safe_to_datetime(df, DATE_COLS)
    safe_to_numeric(df, NUMERIC_COLS)

    flagged = build_flags(df)

    # For analysis-ready output, remove invalid numeric records and severe coordinate issues.
    cleaned = flagged[
        (~flagged["invalid_numeric_flag"])
        & (~flagged["positive_longitude_flag"])
        & (~flagged["coord_zero_flag"])
    ].copy()

    drop_cols = [c for c in REDUNDANT_COLS[dataset_name] if c in cleaned.columns]
    if drop_cols:
        cleaned = cleaned.drop(columns=drop_cols)

    summary = {
        "before_rows": before_rows,
        "after_rows": len(cleaned),
        "removed_rows": before_rows - len(cleaned),
        "dtype_confirmation": cleaned[NUMERIC_COLS + DATE_COLS]
        .dtypes.astype(str)
        .to_dict(),
        "date_flags": {
            "listing_after_close_flag": int(flagged["listing_after_close_flag"].sum()),
            "purchase_after_close_flag": int(flagged["purchase_after_close_flag"].sum()),
            "negative_timeline_flag": int(flagged["negative_timeline_flag"].sum()),
        },
        "geo_summary": {
            "coord_missing_flag": int(flagged["coord_missing_flag"].sum()),
            "coord_zero_flag": int(flagged["coord_zero_flag"].sum()),
            "positive_longitude_flag": int(flagged["positive_longitude_flag"].sum()),
            "implausible_coord_flag": int(flagged["implausible_coord_flag"].sum()),
            "geo_invalid_flag": int(flagged["geo_invalid_flag"].sum()),
        },
        "numeric_invalid_summary": {
            "invalid_close_price_flag": int(flagged["invalid_close_price_flag"].sum()),
            "invalid_living_area_flag": int(flagged["invalid_living_area_flag"].sum()),
            "invalid_days_on_market_flag": int(
                flagged["invalid_days_on_market_flag"].sum()
            ),
            "invalid_bedrooms_flag": int(flagged["invalid_bedrooms_flag"].sum()),
            "invalid_bathrooms_flag": int(flagged["invalid_bathrooms_flag"].sum()),
            "invalid_numeric_flag": int(flagged["invalid_numeric_flag"].sum()),
        },
    }
    return cleaned, summary


def print_summary(name: str, summary: dict) -> None:
    print(f"\n=== {name.upper()} SUMMARY ===")
    print(f"Before rows: {summary['before_rows']:,}")
    print(f"After rows:  {summary['after_rows']:,}")
    print(f"Removed:     {summary['removed_rows']:,}")

    print("\nDtype confirmation:")
    for k, v in summary["dtype_confirmation"].items():
        print(f"- {k}: {v}")

    print("\nDate consistency flags:")
    for k, v in summary["date_flags"].items():
        print(f"- {k}: {v:,}")

    print("\nGeographic quality summary:")
    for k, v in summary["geo_summary"].items():
        print(f"- {k}: {v:,}")

    print("\nInvalid numeric summary:")
    for k, v in summary["numeric_invalid_summary"].items():
        print(f"- {k}: {v:,}")


def main() -> None:
    listed = pd.read_csv(INPUTS["listed"], low_memory=False)
    sold = pd.read_csv(INPUTS["sold"], low_memory=False)

    listed_cleaned, listed_summary = clean_dataset(listed, "listed")
    sold_cleaned, sold_summary = clean_dataset(sold, "sold")

    listed_cleaned.to_csv(OUTPUTS["listed"], index=False)
    sold_cleaned.to_csv(OUTPUTS["sold"], index=False)

    print_summary("listed", listed_summary)
    print_summary("sold", sold_summary)

    print("\nOutput files:")
    print(f"- {OUTPUTS['listed']}")
    print(f"- {OUTPUTS['sold']}")


if __name__ == "__main__":
    main()
