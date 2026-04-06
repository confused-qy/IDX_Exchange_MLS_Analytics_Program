import re
from datetime import date
from pathlib import Path
from typing import Dict, List

import pandas as pd

START_MONTH = 202401


def most_recent_completed_month(today: date | None = None) -> int:
    current = today or date.today()
    year = current.year
    month = current.month - 1
    if month == 0:
        year -= 1
        month = 12
    return year * 100 + month


def month_key_from_name(prefix: str, filename: str) -> int | None:
    match = re.search(rf"{re.escape(prefix)}(\d{{6}})\.csv$", filename)
    if not match:
        return None
    return int(match.group(1))


def iter_months(start_month: int, end_month: int) -> List[int]:
    start_year, start_m = divmod(start_month, 100)
    end_year, end_m = divmod(end_month, 100)

    months = []
    year, month = start_year, start_m
    while (year, month) <= (end_year, end_m):
        months.append(year * 100 + month)
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    return months


def find_monthly_files(prefix: str, root: Path) -> Dict[int, Path]:
    raw_dir = root / "raw"
    week1_dir = root / "IDX_Exchange" / "Week1"
    search_dirs = [raw_dir, root, week1_dir]

    files: Dict[int, Path] = {}
    for directory in search_dirs:
        if not directory.exists():
            continue
        for path in directory.glob(f"{prefix}*.csv"):
            month_key = month_key_from_name(prefix, path.name)
            if not month_key:
                continue
            if START_MONTH <= month_key <= most_recent_completed_month() and month_key not in files:
                files[month_key] = path

    return dict(sorted(files.items()))


def to_datetime(df: pd.DataFrame, columns: List[str]) -> None:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")


def to_numeric(df: pd.DataFrame, columns: List[str]) -> None:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


def yn_to_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.upper().isin(["Y", "YES", "TRUE", "1"])


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    files = find_monthly_files("CRMLSSold", root)

    if not files:
        raise SystemExit("No sold CSV files found in the expected directories.")

    end_month = most_recent_completed_month()
    missing_months = [m for m in iter_months(START_MONTH, end_month) if m not in files]
    if missing_months:
        print("Missing sold months:", missing_months)

    frames = []
    pre_concat_rows = 0
    for month_key, path in files.items():
        df = pd.read_csv(path, low_memory=False)
        pre_concat_rows += len(df)
        df["source_month"] = month_key
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)
    # Row count before concatenation (sum of monthly files).
    print(f"Sold rows before concat: {pre_concat_rows:,}")
    # Row count after concatenation.
    print(f"Sold rows after concat:  {len(df):,}")

    if "PropertyType" not in df.columns:
        raise SystemExit("PropertyType column not found; cannot filter Residential rows.")
    # Row count before Residential filter.
    pre_filter_rows = len(df)
    df = df[df["PropertyType"].astype(str).str.strip().str.casefold() == "residential"]
    # Row count after Residential filter.
    print(f"Sold rows before Residential filter: {pre_filter_rows:,}")
    print(f"Sold rows after Residential filter:  {len(df):,}")

    date_cols = [
        "CloseDate",
        "ContractStatusChangeDate",
        "PurchaseContractDate",
        "ListingContractDate",
    ]
    to_datetime(df, date_cols)

    numeric_cols = [
        "OriginalListPrice",
        "ClosePrice",
        "ListPrice",
        "DaysOnMarket",
        "LivingArea",
        "AboveGradeFinishedArea",
        "BelowGradeFinishedArea",
        "BuildingAreaTotal",
        "BedroomsTotal",
        "BathroomsTotalInteger",
        "YearBuilt",
        "LotSizeSquareFeet",
        "LotSizeAcres",
        "LotSizeArea",
        "MainLevelBedrooms",
        "GarageSpaces",
        "CoveredSpaces",
        "ParkingTotal",
        "FireplacesTotal",
        "AssociationFee",
        "TaxAnnualAmount",
        "TaxYear",
        "Latitude",
        "Longitude",
    ]
    to_numeric(df, numeric_cols)

    df["close_year"] = df["CloseDate"].dt.year
    df["close_month"] = df["CloseDate"].dt.month
    df["close_year_month"] = df["CloseDate"].dt.strftime("%Y-%m")

    df["list_price_per_sqft"] = df["ListPrice"] / df["LivingArea"]
    df["close_price_per_sqft"] = df["ClosePrice"] / df["LivingArea"]
    df["close_to_list_ratio"] = df["ClosePrice"] / df["ListPrice"]
    df["close_minus_list"] = df["ClosePrice"] - df["ListPrice"]

    df["property_age"] = df["close_year"] - df["YearBuilt"]

    df["has_garage"] = (
        (df.get("GarageSpaces", 0).fillna(0) > 0)
        | yn_to_bool(df.get("AttachedGarageYN", pd.Series(index=df.index)))
    ).astype(int)

    df["has_fireplace"] = (
        (df.get("FireplacesTotal", 0).fillna(0) > 0)
        | yn_to_bool(df.get("FireplaceYN", pd.Series(index=df.index)))
    ).astype(int)

    df["has_pool"] = yn_to_bool(df.get("PoolPrivateYN", pd.Series(index=df.index))).astype(int)
    df["has_view"] = yn_to_bool(df.get("ViewYN", pd.Series(index=df.index))).astype(int)
    df["has_waterfront"] = yn_to_bool(df.get("WaterfrontYN", pd.Series(index=df.index))).astype(int)
    df["has_basement"] = yn_to_bool(df.get("BasementYN", pd.Series(index=df.index))).astype(int)
    df["has_new_construction"] = yn_to_bool(df.get("NewConstructionYN", pd.Series(index=df.index))).astype(int)

    keep_columns = [
        "ListingKey",
        "ListingId",
        "ListingKeyNumeric",
        "MlsStatus",
        "CloseDate",
        "ListingContractDate",
        "PurchaseContractDate",
        "ContractStatusChangeDate",
        "ListPrice",
        "OriginalListPrice",
        "ClosePrice",
        "DaysOnMarket",
        "PropertyType",
        "PropertySubType",
        "BusinessType",
        "LivingArea",
        "AboveGradeFinishedArea",
        "BelowGradeFinishedArea",
        "BuildingAreaTotal",
        "BedroomsTotal",
        "BathroomsTotalInteger",
        "YearBuilt",
        "LotSizeSquareFeet",
        "LotSizeAcres",
        "LotSizeArea",
        "LotSizeDimensions",
        "MainLevelBedrooms",
        "Stories",
        "Levels",
        "GarageSpaces",
        "CoveredSpaces",
        "ParkingTotal",
        "AttachedGarageYN",
        "FireplacesTotal",
        "FireplaceYN",
        "NewConstructionYN",
        "SubdivisionName",
        "BuilderName",
        "AssociationFee",
        "AssociationFeeFrequency",
        "TaxAnnualAmount",
        "TaxYear",
        "MLSAreaMajor",
        "CountyOrParish",
        "City",
        "StateOrProvince",
        "PostalCode",
        "UnparsedAddress",
        "Latitude",
        "Longitude",
        "ElementarySchool",
        "ElementarySchoolDistrict",
        "MiddleOrJuniorSchool",
        "MiddleOrJuniorSchoolDistrict",
        "HighSchool",
        "HighSchoolDistrict",
        "ListOfficeName",
        "ListAgentFullName",
        "ListAgentFirstName",
        "ListAgentLastName",
        "ListAgentEmail",
        "ListAgentAOR",
        "BuyerAgentMlsId",
        "BuyerAgentFirstName",
        "BuyerAgentLastName",
        "BuyerAgentAOR",
        "BuyerOfficeName",
        "BuyerOfficeAOR",
        "CoListOfficeName",
        "CoListAgentFirstName",
        "CoListAgentLastName",
        "CoBuyerAgentFirstName",
        "Flooring",
        "ViewYN",
        "WaterfrontYN",
        "BasementYN",
        "PoolPrivateYN",
        "OriginatingSystemName",
        "OriginatingSystemSubName",
        "source_month",
        "close_year",
        "close_month",
        "close_year_month",
        "list_price_per_sqft",
        "close_price_per_sqft",
        "close_to_list_ratio",
        "close_minus_list",
        "property_age",
        "has_garage",
        "has_fireplace",
        "has_pool",
        "has_view",
        "has_waterfront",
        "has_basement",
        "has_new_construction",
    ]

    keep_columns = [col for col in keep_columns if col in df.columns]
    df = df[keep_columns]

    rename_map = {
        "ListingKey": "listing_key",
        "ListingId": "listing_id",
        "ListingKeyNumeric": "listing_key_numeric",
        "MlsStatus": "mls_status",
        "CloseDate": "close_date",
        "ListingContractDate": "listing_contract_date",
        "PurchaseContractDate": "purchase_contract_date",
        "ContractStatusChangeDate": "contract_status_change_date",
        "ListPrice": "list_price",
        "OriginalListPrice": "original_list_price",
        "ClosePrice": "close_price",
        "DaysOnMarket": "days_on_market",
        "PropertyType": "property_type",
        "PropertySubType": "property_sub_type",
        "BusinessType": "business_type",
        "LivingArea": "living_area",
        "AboveGradeFinishedArea": "above_grade_finished_area",
        "BelowGradeFinishedArea": "below_grade_finished_area",
        "BuildingAreaTotal": "building_area_total",
        "BedroomsTotal": "bedrooms_total",
        "BathroomsTotalInteger": "bathrooms_total_integer",
        "YearBuilt": "year_built",
        "LotSizeSquareFeet": "lot_size_square_feet",
        "LotSizeAcres": "lot_size_acres",
        "LotSizeArea": "lot_size_area",
        "LotSizeDimensions": "lot_size_dimensions",
        "MainLevelBedrooms": "main_level_bedrooms",
        "Stories": "stories",
        "Levels": "levels",
        "GarageSpaces": "garage_spaces",
        "CoveredSpaces": "covered_spaces",
        "ParkingTotal": "parking_total",
        "AttachedGarageYN": "attached_garage_yn",
        "FireplacesTotal": "fireplaces_total",
        "FireplaceYN": "fireplace_yn",
        "NewConstructionYN": "new_construction_yn",
        "SubdivisionName": "subdivision_name",
        "BuilderName": "builder_name",
        "AssociationFee": "association_fee",
        "AssociationFeeFrequency": "association_fee_frequency",
        "TaxAnnualAmount": "tax_annual_amount",
        "TaxYear": "tax_year",
        "MLSAreaMajor": "mls_area_major",
        "CountyOrParish": "county_or_parish",
        "City": "city",
        "StateOrProvince": "state_or_province",
        "PostalCode": "postal_code",
        "UnparsedAddress": "unparsed_address",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "ElementarySchool": "elementary_school",
        "ElementarySchoolDistrict": "elementary_school_district",
        "MiddleOrJuniorSchool": "middle_or_junior_school",
        "MiddleOrJuniorSchoolDistrict": "middle_or_junior_school_district",
        "HighSchool": "high_school",
        "HighSchoolDistrict": "high_school_district",
        "ListOfficeName": "list_office_name",
        "ListAgentFullName": "list_agent_full_name",
        "ListAgentFirstName": "list_agent_first_name",
        "ListAgentLastName": "list_agent_last_name",
        "ListAgentEmail": "list_agent_email",
        "ListAgentAOR": "list_agent_aor",
        "BuyerAgentMlsId": "buyer_agent_mls_id",
        "BuyerAgentFirstName": "buyer_agent_first_name",
        "BuyerAgentLastName": "buyer_agent_last_name",
        "BuyerAgentAOR": "buyer_agent_aor",
        "BuyerOfficeName": "buyer_office_name",
        "BuyerOfficeAOR": "buyer_office_aor",
        "CoListOfficeName": "co_list_office_name",
        "CoListAgentFirstName": "co_list_agent_first_name",
        "CoListAgentLastName": "co_list_agent_last_name",
        "CoBuyerAgentFirstName": "co_buyer_agent_first_name",
        "Flooring": "flooring",
        "ViewYN": "view_yn",
        "WaterfrontYN": "waterfront_yn",
        "BasementYN": "basement_yn",
        "PoolPrivateYN": "pool_private_yn",
        "OriginatingSystemName": "originating_system_name",
        "OriginatingSystemSubName": "originating_system_sub_name",
        "source_month": "source_month",
        "close_year": "close_year",
        "close_month": "close_month",
        "close_year_month": "close_year_month",
        "list_price_per_sqft": "list_price_per_sqft",
        "close_price_per_sqft": "close_price_per_sqft",
        "close_to_list_ratio": "close_to_list_ratio",
        "close_minus_list": "close_minus_list",
        "property_age": "property_age",
        "has_garage": "has_garage",
        "has_fireplace": "has_fireplace",
        "has_pool": "has_pool",
        "has_view": "has_view",
        "has_waterfront": "has_waterfront",
        "has_basement": "has_basement",
        "has_new_construction": "has_new_construction",
    }

    df = df.rename(columns=rename_map)

    sort_cols = ["listing_contract_date", "listing_key"]
    sort_cols = [c for c in sort_cols if c in df.columns]
    if sort_cols:
        ascending = [c != "listing_key" for c in sort_cols]
        df = df.sort_values(sort_cols, ascending=ascending)

    output_path = root / "Sold_Final.csv"
    df.to_csv(output_path, index=False)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
