from pathlib import Path

import pandas as pd


ROOT = Path("/Users/confused_qy/coding/IDXExchange")
INPUTS = {
    "listed": ROOT / "Listed_Cleaned.csv",
    "sold": ROOT / "Sold_Cleaned.csv",
}
OUTPUT_DIR = ROOT / "week5_output"

REQUIRED_COLS = [
    "close_price",
    "original_list_price",
    "living_area",
    "days_on_market",
    "close_date",
    "purchase_contract_date",
    "listing_contract_date",
]

DATE_COLS = [
    "close_date",
    "purchase_contract_date",
    "listing_contract_date",
]

NUMERIC_COLS = [
    "close_price",
    "original_list_price",
    "living_area",
    "days_on_market",
]


def assert_required_columns(df: pd.DataFrame, dataset_name: str) -> None:
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"{dataset_name} missing required columns: {missing}")


def run_type_checks(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in DATE_COLS:
        out[col] = pd.to_datetime(out[col], errors="coerce")
    for col in NUMERIC_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def build_quality_report(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    rows = []
    for col in REQUIRED_COLS:
        rows.append(
            {
                "dataset": dataset_name,
                "column": col,
                "dtype": str(df[col].dtype),
                "missing_count": int(df[col].isna().sum()),
                "zero_count": int((df[col] == 0).sum()) if col in NUMERIC_COLS else None,
            }
        )
    return pd.DataFrame(rows)


def engineer_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Avoid divide-by-zero by replacing 0 with NA.
    safe_original = out["original_list_price"].replace(0, pd.NA)
    safe_living = out["living_area"].replace(0, pd.NA)

    out["price_ratio"] = out["close_price"] / safe_original
    out["close_to_original_list_ratio"] = out["close_price"] / safe_original
    out["price_per_sqft"] = out["close_price"] / safe_living

    out["year"] = out["close_date"].dt.year
    out["month"] = out["close_date"].dt.month
    out["yrmo"] = out["close_date"].dt.strftime("%Y-%m")

    out["listing_to_contract_days"] = (
        out["purchase_contract_date"] - out["listing_contract_date"]
    ).dt.days
    out["contract_to_close_days"] = (
        out["close_date"] - out["purchase_contract_date"]
    ).dt.days

    return out


def process_one(dataset_name: str, input_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(input_path, low_memory=False)
    assert_required_columns(df, dataset_name)
    typed = run_type_checks(df)
    report = build_quality_report(typed, dataset_name)
    featured = engineer_metrics(typed)
    return featured, report


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    listed_featured, listed_report = process_one("listed", INPUTS["listed"])
    sold_featured, sold_report = process_one("sold", INPUTS["sold"])

    listed_featured.to_csv(OUTPUT_DIR / "Listed_Week5_Features.csv", index=False)
    sold_featured.to_csv(OUTPUT_DIR / "Sold_Week5_Features.csv", index=False)

    quality = pd.concat([listed_report, sold_report], ignore_index=True)
    quality.to_csv(OUTPUT_DIR / "Week5_DataQuality_Check.csv", index=False)

    print("Wrote:")
    print(f"- {OUTPUT_DIR / 'Listed_Week5_Features.csv'}")
    print(f"- {OUTPUT_DIR / 'Sold_Week5_Features.csv'}")
    print(f"- {OUTPUT_DIR / 'Week5_DataQuality_Check.csv'}")


if __name__ == "__main__":
    main()
