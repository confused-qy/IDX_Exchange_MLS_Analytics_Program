from pathlib import Path

import pandas as pd


ROOT = Path("/Users/confused_qy/coding/IDXExchange")
INPUTS = {
    "sold": ROOT / "week5_output" / "Sold_Week5_Features.csv",
    "listed": ROOT / "week5_output" / "Listed_Week5_Features.csv",
}
OUTPUT_DIR = ROOT / "week7_output"

OUTLIER_FIELDS = ["close_price", "living_area", "days_on_market"]
BUSINESS_RULE_FLAGS = [
    "invalid_close_price_flag",
    "invalid_living_area_flag",
    "invalid_days_on_market_flag",
    "invalid_numeric_flag",
]


def to_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series.fillna(False)
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def check_required_columns(df: pd.DataFrame, dataset_name: str) -> None:
    missing = [col for col in OUTLIER_FIELDS if col not in df.columns]
    if missing:
        raise ValueError(f"{dataset_name} missing required columns: {missing}")


def calculate_iqr_bounds(series: pd.Series) -> dict[str, float]:
    numeric = pd.to_numeric(series, errors="coerce")
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": q1 - 1.5 * iqr,
        "upper_bound": q3 + 1.5 * iqr,
        "p01": numeric.quantile(0.01),
        "p99": numeric.quantile(0.99),
    }


def add_iqr_flags(df: pd.DataFrame, dataset_name: str) -> tuple[pd.DataFrame, list[dict]]:
    out = df.copy()
    comparison_rows = []

    for col in OUTLIER_FIELDS:
        out[col] = pd.to_numeric(out[col], errors="coerce")
        bounds = calculate_iqr_bounds(out[col])
        flag_col = f"{col}_iqr_outlier_flag"

        has_value = out[col].notna()
        out[flag_col] = has_value & (
            (out[col] < bounds["lower_bound"]) | (out[col] > bounds["upper_bound"])
        )

        comparison_rows.append(
            {
                "dataset": dataset_name,
                "field": col,
                "rows": len(out),
                "non_null_count": int(has_value.sum()),
                "q1": bounds["q1"],
                "q3": bounds["q3"],
                "iqr": bounds["iqr"],
                "lower_bound": bounds["lower_bound"],
                "upper_bound": bounds["upper_bound"],
                "p01": bounds["p01"],
                "p99": bounds["p99"],
                "outlier_count": int(out[flag_col].sum()),
                "outlier_pct_of_non_null": (
                    (out[flag_col].sum() / has_value.sum()) * 100
                    if has_value.sum()
                    else 0
                ),
            }
        )

    iqr_flag_cols = [f"{col}_iqr_outlier_flag" for col in OUTLIER_FIELDS]
    out["any_iqr_outlier_flag"] = out[iqr_flag_cols].any(axis=1)

    for col in BUSINESS_RULE_FLAGS:
        if col in out.columns:
            out[col] = to_bool(out[col])

    out["business_rule_invalid_flag"] = (
        out["invalid_numeric_flag"] if "invalid_numeric_flag" in out.columns else False
    )
    out["exclude_from_week7_analysis_flag"] = (
        out["business_rule_invalid_flag"] | out["any_iqr_outlier_flag"]
    )

    return out, comparison_rows


def build_filtered_dataset(flagged: pd.DataFrame) -> pd.DataFrame:
    return flagged[~flagged["exclude_from_week7_analysis_flag"]].copy()


def build_before_after_rows(
    dataset_name: str,
    flagged: pd.DataFrame,
    filtered: pd.DataFrame,
    bounds_rows: list[dict],
) -> list[dict]:
    bounds_by_field = {row["field"]: row for row in bounds_rows}
    rows = []

    for col in OUTLIER_FIELDS:
        before = pd.to_numeric(flagged[col], errors="coerce")
        after = pd.to_numeric(filtered[col], errors="coerce")
        bounds = bounds_by_field[col]

        rows.append(
            {
                "dataset": dataset_name,
                "field": col,
                "before_rows": len(flagged),
                "after_rows": len(filtered),
                "removed_rows": len(flagged) - len(filtered),
                "removed_pct": (
                    ((len(flagged) - len(filtered)) / len(flagged)) * 100
                    if len(flagged)
                    else 0
                ),
                "before_non_null": int(before.notna().sum()),
                "after_non_null": int(after.notna().sum()),
                "before_median": before.median(),
                "after_median": after.median(),
                "before_mean": before.mean(),
                "after_mean": after.mean(),
                "iqr_lower_bound": bounds["lower_bound"],
                "iqr_upper_bound": bounds["upper_bound"],
                "p01": bounds["p01"],
                "p99": bounds["p99"],
                "field_outlier_count": bounds["outlier_count"],
                "field_outlier_pct_of_non_null": bounds["outlier_pct_of_non_null"],
            }
        )

    return rows


def format_markdown_value(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append(
            "| "
            + " | ".join(format_markdown_value(row[col]) for col in headers)
            + " |"
        )
    return "\n".join(lines)


def write_markdown_report(comparison: pd.DataFrame, output_path: Path) -> None:
    dataset_summary = (
        comparison[
            ["dataset", "before_rows", "after_rows", "removed_rows", "removed_pct"]
        ]
        .drop_duplicates()
        .sort_values("dataset")
    )

    lines = [
        "# Week 7 Outlier Detection and Data Quality",
        "",
        "Method: IQR filtering on `close_price`, `living_area`, and `days_on_market`.",
        "The full flagged datasets preserve all records. The clean filtered datasets exclude business-rule invalid records and IQR outliers for analysis.",
        "",
        "## Dataset Size Comparison",
        "",
        dataframe_to_markdown(dataset_summary),
        "",
        "## Median and Mean Comparison",
        "",
        dataframe_to_markdown(
            comparison[
                [
                    "dataset",
                    "field",
                    "before_median",
                    "after_median",
                    "before_mean",
                    "after_mean",
                    "field_outlier_count",
                ]
            ]
        ),
        "",
        "## IQR Bounds",
        "",
        dataframe_to_markdown(
            comparison[
                [
                    "dataset",
                    "field",
                    "iqr_lower_bound",
                    "iqr_upper_bound",
                    "p01",
                    "p99",
                ]
            ]
        ),
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def process_dataset(dataset_name: str, input_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    df = pd.read_csv(input_path, low_memory=False)
    check_required_columns(df, dataset_name)

    flagged, bounds_rows = add_iqr_flags(df, dataset_name)
    filtered = build_filtered_dataset(flagged)

    label = dataset_name.capitalize()
    flagged.to_csv(OUTPUT_DIR / f"{label}_Week7_Flagged.csv", index=False)
    filtered.to_csv(OUTPUT_DIR / f"{label}_Week7_Clean_Filtered.csv", index=False)

    comparison_rows = build_before_after_rows(
        dataset_name=dataset_name,
        flagged=flagged,
        filtered=filtered,
        bounds_rows=bounds_rows,
    )
    return flagged, filtered, comparison_rows


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_comparison_rows = []
    for dataset_name, input_path in INPUTS.items():
        _, _, comparison_rows = process_dataset(dataset_name, input_path)
        all_comparison_rows.extend(comparison_rows)

    comparison = pd.DataFrame(all_comparison_rows)
    comparison.to_csv(OUTPUT_DIR / "Week7_Outlier_Comparison.csv", index=False)
    write_markdown_report(
        comparison=comparison,
        output_path=OUTPUT_DIR / "week7_outlier_comparison.md",
    )

    print("Wrote Week 7 outputs to:")
    print(f"- {OUTPUT_DIR / 'Sold_Week7_Flagged.csv'}")
    print(f"- {OUTPUT_DIR / 'Sold_Week7_Clean_Filtered.csv'}")
    print(f"- {OUTPUT_DIR / 'Listed_Week7_Flagged.csv'}")
    print(f"- {OUTPUT_DIR / 'Listed_Week7_Clean_Filtered.csv'}")
    print(f"- {OUTPUT_DIR / 'Week7_Outlier_Comparison.csv'}")
    print(f"- {OUTPUT_DIR / 'week7_outlier_comparison.md'}")


if __name__ == "__main__":
    main()
