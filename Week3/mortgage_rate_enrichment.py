import io
import os
import subprocess
import tempfile
import urllib.request

import pandas as pd


FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"


def fetch_mortgage_csv():
    try:
        import certifi
        import ssl

        context = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(FRED_URL, context=context) as response:
            data = response.read()
        return pd.read_csv(io.BytesIO(data), parse_dates=["observation_date"])
    except Exception as exc:
        print(f"[WARN] HTTPS fetch failed, falling back to curl: {exc}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp_path = tmp.name
        try:
            subprocess.run(["curl", "-L", FRED_URL, "-o", tmp_path], check=True)
            return pd.read_csv(tmp_path, parse_dates=["observation_date"])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


def load_mortgage_monthly():
    mortgage = fetch_mortgage_csv()
    mortgage.columns = ["date", "rate_30yr_fixed"]
    mortgage["year_month"] = mortgage["date"].dt.to_period("M")
    mortgage_monthly = (
        mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index()
    )
    return mortgage_monthly


def add_year_month(df, date_col):
    df = df.copy()
    df["year_month"] = pd.to_datetime(df[date_col], errors="coerce").dt.to_period("M")
    return df


def main():
    root = "/Users/confused_qy/coding/IDXExchange"

    listed_path = f"{root}/Listed_KeepCols.csv"
    sold_path = f"{root}/Sold_KeepCols.csv"

    listed = pd.read_csv(listed_path, low_memory=False)
    sold = pd.read_csv(sold_path, low_memory=False)

    mortgage_monthly = load_mortgage_monthly()

    listed = add_year_month(listed, "listing_contract_date")
    sold = add_year_month(sold, "close_date")

    listed_with_rates = listed.merge(mortgage_monthly, on="year_month", how="left")
    sold_with_rates = sold.merge(mortgage_monthly, on="year_month", how="left")

    print("listed null rates:", listed_with_rates["rate_30yr_fixed"].isnull().sum())
    print("sold null rates:", sold_with_rates["rate_30yr_fixed"].isnull().sum())

    listed_with_rates.to_csv(f"{root}/Listed_KeepCols_WithRates.csv", index=False)
    sold_with_rates.to_csv(f"{root}/Sold_KeepCols_WithRates.csv", index=False)

    print("Done. Wrote 2 files to IDXExchange root.")


if __name__ == "__main__":
    main()
