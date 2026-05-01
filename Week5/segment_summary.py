from pathlib import Path

import pandas as pd


ROOT = Path("/Users/confused_qy/coding/IDXExchange")
OUTPUT_DIR = ROOT / "week5_output"
INPUT_PATH = OUTPUT_DIR / "Sold_Week5_Features.csv"

METRIC_COLS = [
    "close_price",
    "price_ratio",
    "price_per_sqft",
    "days_on_market",
]

AGG_FUNCS = ["count", "mean", "median", "min", "max"]


def summarize(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame | None:
    valid_group_cols = [c for c in group_cols if c in df.columns]
    if len(valid_group_cols) != len(group_cols):
        return None
    out = (
        df.groupby(valid_group_cols, dropna=False)[METRIC_COLS]
        .agg(AGG_FUNCS)
        .round(4)
        .reset_index()
    )
    out.columns = [
        "_".join(col).strip("_") if isinstance(col, tuple) else col for col in out.columns
    ]
    return out


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input not found: {INPUT_PATH}. Run Week5/feature_engineering.py first."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    tables = {
        "SegmentSummary_PropertyType.csv": ["property_type"],
        "SegmentSummary_CountyOrParish.csv": ["county_or_parish"],
        "SegmentSummary_PropertySubType.csv": ["property_sub_type"],
        "SegmentSummary_County_MLSAreaMajor.csv": ["county_or_parish", "mls_area_major"],
        "SegmentSummary_ListOffice_BuyerOffice.csv": [
            "list_office_name",
            "buyer_office_name",
        ],
    }

    written = []
    skipped = []
    for filename, group_cols in tables.items():
        summary_df = summarize(df, group_cols)
        if summary_df is None:
            skipped.append((filename, group_cols))
            continue
        output_path = OUTPUT_DIR / filename
        summary_df.to_csv(output_path, index=False)
        written.append(output_path)

    print("Wrote summary files:")
    for p in written:
        print(f"- {p}")

    if skipped:
        print("\nSkipped (missing group columns):")
        for filename, cols in skipped:
            print(f"- {filename}: {cols}")


if __name__ == "__main__":
    main()
