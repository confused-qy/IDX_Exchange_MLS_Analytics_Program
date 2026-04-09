from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

os.environ.setdefault("MPLCONFIGDIR", str(Path("/tmp") / "matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "IDX_Exchange" / "Week2" / "Numeric_Distribution"
HIST_DIR = OUTPUT_DIR / "histograms"
BOX_DIR = OUTPUT_DIR / "boxplots"
REPORT_MD = OUTPUT_DIR / "numeric_distribution.md"

DATASETS = {
    "Listed_Final": ROOT / "Listed_Final.csv",
    "Sold_Final": ROOT / "Sold_Final.csv",
}

FIELDS = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
]

PERCENTILES = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]

FIELD_ALIASES = {
    "ClosePrice": ["close_price"],
    "ListPrice": ["list_price"],
    "OriginalListPrice": ["original_list_price"],
    "LivingArea": ["living_area"],
    "LotSizeAcres": ["lot_size_acres"],
    "BedroomsTotal": ["bedrooms_total"],
    "BathroomsTotalInteger": ["bathrooms_total_integer"],
    "DaysOnMarket": ["days_on_market"],
    "YearBuilt": ["year_built"],
}


@dataclass
class FieldSummary:
    field: str
    column: str
    count: int
    missing: int
    mean: float
    median: float
    percentiles: Dict[float, float]
    outlier_low: float
    outlier_high: float
    outlier_count: int
    outlier_min: float | None
    outlier_max: float | None


def normalize_columns(df: pd.DataFrame) -> Dict[str, str]:
    return {col.lower(): col for col in df.columns}


def resolve_column(df: pd.DataFrame, field: str) -> str | None:
    col_map = normalize_columns(df)
    direct = col_map.get(field.lower())
    if direct:
        return direct
    for alias in FIELD_ALIASES.get(field, []):
        mapped = col_map.get(alias.lower())
        if mapped:
            return mapped
    return None


def summarize_field(series: pd.Series, field: str, column: str) -> FieldSummary:
    missing = int(series.isna().sum())
    clean = series.dropna()
    if clean.empty:
        return FieldSummary(
            field=field,
            column=column,
            count=0,
            missing=missing,
            mean=float("nan"),
            median=float("nan"),
            percentiles={p: float("nan") for p in PERCENTILES},
            outlier_low=float("nan"),
            outlier_high=float("nan"),
            outlier_count=0,
            outlier_min=None,
            outlier_max=None,
        )

    quantiles = clean.quantile(PERCENTILES)
    q1 = clean.quantile(0.25)
    q3 = clean.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = clean[(clean < lower) | (clean > upper)]
    outlier_min = float(outliers.min()) if not outliers.empty else None
    outlier_max = float(outliers.max()) if not outliers.empty else None

    return FieldSummary(
        field=field,
        column=column,
        count=int(clean.shape[0]),
        missing=missing,
        mean=float(clean.mean()),
        median=float(clean.median()),
        percentiles={p: float(quantiles.loc[p]) for p in PERCENTILES},
        outlier_low=float(lower),
        outlier_high=float(upper),
        outlier_count=int(outliers.shape[0]),
        outlier_min=outlier_min,
        outlier_max=outlier_max,
    )


def save_histogram(series: pd.Series, title: str, path: Path) -> None:
    clean = series.dropna()
    if clean.empty:
        return
    x_min = clean.quantile(0.01)
    x_max = clean.quantile(0.99)
    clipped = clean[(clean >= x_min) & (clean <= x_max)]
    plt.figure(figsize=(7, 4))
    plt.hist(clipped, bins=50, color="#2d6a4f", edgecolor="white")
    plt.title(title)
    plt.xlabel(title)
    plt.ylabel("Count")
    plt.xlim(float(x_min), float(x_max))
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=140)
    plt.close()


def save_boxplot(series: pd.Series, title: str, path: Path) -> None:
    plt.figure(figsize=(4.5, 4))
    plt.boxplot(series.dropna(), vert=True, showfliers=True)
    plt.title(title)
    plt.ylabel(title)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=140)
    plt.close()


def print_summary(dataset: str, summaries: List[FieldSummary]) -> None:
    print(f"\n== {dataset} ==")
    for summary in summaries:
        print(f"\n{summary.field} ({summary.column})")
        print(f"  non-missing: {summary.count:,}")
        print(f"  missing:     {summary.missing:,}")
        print(f"  mean:        {summary.mean:.2f}")
        print(f"  median:      {summary.median:.2f}")
        pct_parts = [
            f"{int(p*100):>2}th: {summary.percentiles[p]:.2f}"
            for p in PERCENTILES
        ]
        print("  percentiles: " + ", ".join(pct_parts))
        print(
            "  outliers: "
            f"{summary.outlier_count:,} "
            f"(low<{summary.outlier_low:.2f}, high>{summary.outlier_high:.2f})"
        )
        if summary.outlier_count > 0:
            print(
                f"  outlier range: {summary.outlier_min:.2f} to {summary.outlier_max:.2f}"
            )


def write_report(
    dataset: str, summaries: List[FieldSummary], rel_hist_dir: Path, rel_box_dir: Path
) -> List[str]:
    lines: List[str] = []
    lines.append(f"## {dataset}")
    lines.append("")
    for summary in summaries:
        lines.append(f"### {summary.field}")
        lines.append("")
        lines.append(f"- Source column: `{summary.column}`")
        lines.append(f"- Non-missing: {summary.count:,}")
        lines.append(f"- Missing: {summary.missing:,}")
        lines.append(f"- Mean: {summary.mean:.2f}")
        lines.append(f"- Median: {summary.median:.2f}")
        lines.append(
            "- Percentiles: "
            + ", ".join(
                f"{int(p*100)}th={summary.percentiles[p]:.2f}" for p in PERCENTILES
            )
        )
        lines.append(
            "- Outliers (IQR rule): "
            f"{summary.outlier_count:,} "
            f"(low<{summary.outlier_low:.2f}, high>{summary.outlier_high:.2f})"
        )
        if summary.outlier_count > 0:
            lines.append(
                f"- Outlier range: {summary.outlier_min:.2f} to {summary.outlier_max:.2f}"
            )
        lines.append("")
        hist_path = rel_hist_dir / f"{summary.field.lower()}.png"
        box_path = rel_box_dir / f"{summary.field.lower()}.png"
        lines.append(f"![{summary.field} histogram]({hist_path.as_posix()})")
        lines.append("")
        lines.append(f"![{summary.field} boxplot]({box_path.as_posix()})")
        lines.append("")
    return lines


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    BOX_DIR.mkdir(parents=True, exist_ok=True)

    report_lines: List[str] = []
    report_lines.append("# Numeric Distribution Analysis")
    report_lines.append("")
    report_lines.append(
        "Fields analyzed: ClosePrice, ListPrice, OriginalListPrice, LivingArea, "
        "LotSizeAcres, BedroomsTotal, BathroomsTotalInteger, DaysOnMarket, YearBuilt."
    )
    report_lines.append("")

    for dataset, path in DATASETS.items():
        if not path.exists():
            print(f"Missing dataset file: {path}")
            continue

        df = pd.read_csv(path, low_memory=False)
        summaries: List[FieldSummary] = []

        hist_subdir = HIST_DIR / dataset
        box_subdir = BOX_DIR / dataset
        hist_subdir.mkdir(parents=True, exist_ok=True)
        box_subdir.mkdir(parents=True, exist_ok=True)

        for field in FIELDS:
            column = resolve_column(df, field)
            if column is None:
                print(f"[{dataset}] Column not found for field: {field}")
                continue
            series = pd.to_numeric(df[column], errors="coerce")
            summary = summarize_field(series, field, column)
            summaries.append(summary)

            save_histogram(series, f"{dataset} - {field}", hist_subdir / f"{field.lower()}.png")
            save_boxplot(series, f"{dataset} - {field}", box_subdir / f"{field.lower()}.png")

        print_summary(dataset, summaries)

        rel_hist_dir = Path("histograms") / dataset
        rel_box_dir = Path("boxplots") / dataset
        report_lines.extend(write_report(dataset, summaries, rel_hist_dir, rel_box_dir))

    REPORT_MD.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"\nWrote report: {REPORT_MD}")


if __name__ == "__main__":
    main()
