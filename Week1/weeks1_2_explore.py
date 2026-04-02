import os
import pandas as pd
import numpy as np

RAW_DIR = 'raw'
FILES = {
    'Listing 2024-01': 'CRMLSListing202401.csv',
    'Listing 2024-02': 'CRMLSListing202402.csv',
    'Sold 2024-01': 'CRMLSSold202401.csv',
    'Sold 2024-02': 'CRMLSSold202402.csv',
}

KEY_FIELDS = [
    'ListPrice',
    'ClosePrice',
    'LivingArea',
    'BedroomsTotal',
    'BathroomsTotalInteger',
    'PropertyType',
    'ListAgentFullName',
    'ListOfficeName',
    'DaysOnMarket',
]

NUMERIC_FIELDS = [
    'ListPrice',
    'ClosePrice',
    'LivingArea',
    'BedroomsTotal',
    'BathroomsTotalInteger',
    'DaysOnMarket',
]


def load_df(filename: str) -> pd.DataFrame:
    path = os.path.join(RAW_DIR, filename)
    return pd.read_csv(path, low_memory=False)


def summarize_df(df: pd.DataFrame) -> dict:
    summary = {
        'rows': len(df),
        'cols': len(df.columns),
        'missing': {},
        'describe': pd.DataFrame(),
    }

    for col in KEY_FIELDS:
        if col in df.columns:
            summary['missing'][col] = df[col].isna().mean()

    numeric = [c for c in NUMERIC_FIELDS if c in df.columns]
    if numeric:
        desc = df[numeric].describe().T
        desc['median'] = df[numeric].median(numeric_only=True)
        desc = desc[['count', 'mean', 'median', 'min', 'max']]
        summary['describe'] = desc

    return summary


def format_number(x, digits=2):
    if pd.isna(x):
        return ''
    if isinstance(x, (int, np.integer)):
        return f'{x:,d}'
    if isinstance(x, (float, np.floating)):
        return f'{x:,.{digits}f}'
    return str(x)


def df_to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return '_No numeric fields found._\n'

    headers = ['Field'] + list(df.columns)
    lines = []
    lines.append('| ' + ' | '.join(headers) + ' |')
    lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')

    for idx, row in df.iterrows():
        row_vals = [str(idx)] + [format_number(row[col]) for col in df.columns]
        lines.append('| ' + ' | '.join(row_vals) + ' |')

    return '\n'.join(lines)


def main():
    summaries = {}
    all_columns = {}

    for label, fname in FILES.items():
        df = load_df(fname)
        summaries[label] = summarize_df(df)
        all_columns[label] = set(df.columns)

    listing_cols = set().union(all_columns['Listing 2024-01'], all_columns['Listing 2024-02'])
    sold_cols = set().union(all_columns['Sold 2024-01'], all_columns['Sold 2024-02'])

    common_cols = listing_cols & sold_cols
    listing_only = sorted(list(listing_cols - sold_cols))
    sold_only = sorted(list(sold_cols - listing_cols))

    md_lines = []
    md_lines.append('# Weeks 1–2 Dataset Exploration Summary')
    md_lines.append('')
    md_lines.append('## Datasets')
    for label, fname in FILES.items():
        md_lines.append(f'- `{fname}` ({label})')

    md_lines.append('')
    md_lines.append('## Basic Shape')
    md_lines.append('| Dataset | Rows | Columns |')
    md_lines.append('| --- | ---: | ---: |')
    for label in FILES.keys():
        s = summaries[label]
        md_lines.append(f"| {label} | {s['rows']:,} | {s['cols']:,} |")

    md_lines.append('')
    md_lines.append('## Key Field Availability (Missing %)')
    md_lines.append('Percent of missing values for key fields present in each dataset.')

    for label in FILES.keys():
        md_lines.append('')
        md_lines.append(f'### {label}')
        missing = summaries[label]['missing']
        if not missing:
            md_lines.append('_No key fields found in this dataset._')
            continue
        md_lines.append('| Field | Missing % |')
        md_lines.append('| --- | ---: |')
        for col, pct in missing.items():
            md_lines.append(f'| `{col}` | {pct*100:.2f}% |')

    md_lines.append('')
    md_lines.append('## Numeric Field Summary')
    md_lines.append('Count, mean, median, min, and max for key numeric fields found.')

    for label in FILES.keys():
        md_lines.append('')
        md_lines.append(f'### {label}')
        desc = summaries[label]['describe']
        md_lines.append(df_to_md(desc))

    md_lines.append('')
    md_lines.append('## Listing vs. Sold Columns')
    md_lines.append(f'- Common columns: {len(common_cols)}')
    md_lines.append(f'- Listing-only columns: {len(listing_only)}')
    md_lines.append(f'- Sold-only columns: {len(sold_only)}')

    md_lines.append('')
    md_lines.append('### Sample Listing-only Columns')
    md_lines.append(', '.join(f'`{c}`' for c in listing_only[:20]) or '_None_')

    md_lines.append('')
    md_lines.append('### Sample Sold-only Columns')
    md_lines.append(', '.join(f'`{c}`' for c in sold_only[:20]) or '_None_')

    out_path = 'weeks1_2_analysis.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
