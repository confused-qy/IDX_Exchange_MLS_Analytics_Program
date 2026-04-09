from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
LISTED_PATH = ROOT / "Listed_Final.csv"
SOLD_PATH = ROOT / "Sold_Final.csv"


CORE_LISTED = {
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
}

CORE_SOLD = {
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
}


def normalize_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    obj_cols = df.select_dtypes(include=["object"]).columns
    if len(obj_cols) > 0:
        df[obj_cols] = df[obj_cols].replace(r"^\s*$", pd.NA, regex=True)
    return df


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df)
    missing_count = df.isna().sum()
    missing_pct = (missing_count / total).fillna(0) * 100
    summary = (
        pd.DataFrame(
            {
                "missing_count": missing_count,
                "missing_pct": missing_pct.round(2),
            }
        )
        .sort_values(["missing_pct", "missing_count"], ascending=False)
        .reset_index()
        .rename(columns={"index": "column"})
    )
    return summary


PII_LISTED = {
    "list_agent_email",
    "list_agent_first_name",
    "list_agent_last_name",
    "list_agent_full_name",
    "list_office_name",
    "co_list_agent_first_name",
    "co_list_agent_last_name",
    "co_list_office_name",
    "buyer_agent_first_name",
    "buyer_agent_last_name",
    "buyer_agent_mls_id",
    "buyer_office_name",
    "buyer_office_aor",
    "co_buyer_agent_first_name",
    "buyer_agency_compensation",
    "buyer_agency_compensation_type",
}

PII_SOLD = {
    "list_agent_email",
    "list_agent_first_name",
    "list_agent_last_name",
    "list_agent_full_name",
    "list_agent_aor",
    "list_office_name",
    "co_list_agent_first_name",
    "co_list_agent_last_name",
    "co_list_office_name",
    "buyer_agent_first_name",
    "buyer_agent_last_name",
    "buyer_agent_mls_id",
    "buyer_agent_aor",
    "buyer_office_name",
    "buyer_office_aor",
    "co_buyer_agent_first_name",
}


def print_section(title: str, summary: pd.DataFrame) -> None:
    print(f"\n== {title} ==")
    print("Columns with missing >= 90%:")
    drops_90 = summary.loc[summary["missing_pct"] >= 90, "column"].tolist()
    if drops_90:
        for col in drops_90:
            print(f"- {col}")
    else:
        print("- None")
    print("\nMissing summary (sorted by missing % desc):")
    for _, row in summary.iterrows():
        print(
            f"{row['column']}: {int(row['missing_count']):,} "
            f"missing ({row['missing_pct']:.2f}%)"
        )


def main() -> None:
    if not LISTED_PATH.exists() or not SOLD_PATH.exists():
        raise SystemExit("Listed_Final.csv or Sold_Final.csv not found at repo root.")

    listed = normalize_missing(pd.read_csv(LISTED_PATH, low_memory=False))
    sold = normalize_missing(pd.read_csv(SOLD_PATH, low_memory=False))

    listed_summary = missing_summary(listed)
    sold_summary = missing_summary(sold)

    print(f"Run date: {date.today().isoformat()}")
    print("Missing values include nulls and empty/whitespace-only strings.")

    print_section("Listed_Final", listed_summary)
    print_section("Sold_Final", sold_summary)


if __name__ == "__main__":
    main()
