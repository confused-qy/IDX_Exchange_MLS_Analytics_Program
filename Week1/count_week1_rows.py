from pathlib import Path


def count_rows(path: Path) -> int:
    with path.open('r', encoding='utf-8', errors='ignore') as f:
        return sum(1 for _ in f) - 1  # minus header


def main() -> None:
    root = Path(__file__).resolve().parents[1].parent
    raw = root / 'raw'

    listed_files = sorted(raw.glob('CRMLSListing*.csv')) + [
        root / 'CRMLSListing202602.csv',
        root / 'CRMLSListing202603.csv',
    ]
    sold_files = sorted(raw.glob('CRMLSSold*.csv')) + [
        root / 'CRMLSSold202602.csv',
        root / 'CRMLSSold202603.csv',
    ]

    listed_files = [p for p in listed_files if p.exists()]
    sold_files = [p for p in sold_files if p.exists()]

    listed_counts = [(p.name, count_rows(p)) for p in listed_files]
    sold_counts = [(p.name, count_rows(p)) for p in sold_files]

    listed_total = sum(c for _, c in listed_counts)
    sold_total = sum(c for _, c in sold_counts)

    print('Listed total rows:', f'{listed_total:,}')
    print('Sold total rows:  ', f'{sold_total:,}')
    print('')
    print('Listed monthly row counts:')
    for name, c in listed_counts:
        print(f'{name}  {c}')
    print('')
    print('Sold monthly row counts:')
    for name, c in sold_counts:
        print(f'{name}  {c}')


if __name__ == '__main__':
    main()
