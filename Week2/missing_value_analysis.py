from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
LISTED_PATH = ROOT / "Listed_Final.csv"
SOLD_PATH = ROOT / "Sold_Final.csv"
OUTPUT_MD = ROOT / "IDX_Exchange" / "Week2" / "missing_value_analysis.md"


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


def add_actions(summary: pd.DataFrame, core_cols: set[str]) -> pd.DataFrame:
    def decide(row: pd.Series) -> str:
        if row["missing_pct"] >= 90 and row["column"] not in core_cols:
            return "drop (high missing)"
        return "retain"

    summary = summary.copy()
    summary["flag_gt_90"] = summary["missing_pct"] >= 90
    summary["proposed_action"] = summary.apply(decide, axis=1)
    return summary


def write_section(lines: list[str], title: str, summary: pd.DataFrame) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| Column | Missing Count | Missing % | >90% Missing | Proposed Action |")
    lines.append("| --- | --- | --- | --- | --- |")
    for _, row in summary.iterrows():
        lines.append(
            f"| {row['column']} | {int(row['missing_count']):,} | "
            f"{row['missing_pct']:.2f}% | {str(row['flag_gt_90'])} | "
            f"{row['proposed_action']} |"
        )
    lines.append("")
    drops = summary.loc[summary["proposed_action"] == "drop (high missing)", "column"].tolist()
    lines.append("Proposed drops (high missing, non-core):")
    if drops:
        for col in drops:
            lines.append(f"- {col}")
    else:
        lines.append("- None")
    lines.append("")


def main() -> None:
    if not LISTED_PATH.exists() or not SOLD_PATH.exists():
        raise SystemExit("Listed_Final.csv or Sold_Final.csv not found at repo root.")

    listed = normalize_missing(pd.read_csv(LISTED_PATH, low_memory=False))
    sold = normalize_missing(pd.read_csv(SOLD_PATH, low_memory=False))

    listed_summary = add_actions(missing_summary(listed), CORE_LISTED)
    sold_summary = add_actions(missing_summary(sold), CORE_SOLD)

    lines: list[str] = []
    lines.append("# Week 2 Missing Value Analysis")
    lines.append("")
    lines.append(f"Run date: {date.today().isoformat()}")
    lines.append("")
    lines.append("Missing values include nulls and empty/whitespace-only strings.")
    lines.append("")

    write_section(lines, "Listed_Final", listed_summary)
    write_section(lines, "Sold_Final", sold_summary)

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
