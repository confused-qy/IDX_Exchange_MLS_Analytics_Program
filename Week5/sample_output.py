from pathlib import Path

import pandas as pd


ROOT = Path("/Users/confused_qy/coding/IDXExchange")
OUTPUT_DIR = ROOT / "week5_output"
INPUT_PATH = OUTPUT_DIR / "Sold_Week5_Features.csv"
OUTPUT_PATH = OUTPUT_DIR / "Week5_SampleOutput.csv"

SAMPLE_COLS = [
    "listing_key",
    "close_date",
    "close_price",
    "original_list_price",
    "living_area",
    "days_on_market",
    "purchase_contract_date",
    "listing_contract_date",
    "price_ratio",
    "close_to_original_list_ratio",
    "price_per_sqft",
    "year",
    "month",
    "yrmo",
    "listing_to_contract_days",
    "contract_to_close_days",
    "property_type",
    "county_or_parish",
]


def build_sample(df: pd.DataFrame, n_per_bin: int = 3) -> pd.DataFrame:
    work = df.copy()
    work["close_date"] = pd.to_datetime(work["close_date"], errors="coerce")
    work["close_price"] = pd.to_numeric(work["close_price"], errors="coerce")

    candidates = work.dropna(
        subset=[
            "close_date",
            "close_price",
            "price_ratio",
            "close_to_original_list_ratio",
            "price_per_sqft",
            "listing_to_contract_days",
            "contract_to_close_days",
        ]
    ).copy()

    # Create price bins so the sample demonstrates different price ranges.
    candidates["price_bin"] = pd.qcut(
        candidates["close_price"], q=3, labels=["low", "mid", "high"], duplicates="drop"
    )
    sampled = (
        candidates.sort_values(["close_date", "close_price"])
        .groupby("price_bin", dropna=False, observed=False)
        .head(n_per_bin)
    )

    return sampled


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input not found: {INPUT_PATH}. Run Week5/feature_engineering.py first."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    sample_df = build_sample(df, n_per_bin=3)
    keep_cols = [c for c in SAMPLE_COLS if c in sample_df.columns]
    out = sample_df[keep_cols].copy()

    out.to_csv(OUTPUT_PATH, index=False)

    print(f"Wrote: {OUTPUT_PATH}")
    print("\nPreview:")
    print(out.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
