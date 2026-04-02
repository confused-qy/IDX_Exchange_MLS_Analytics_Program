import re
from pathlib import Path
from typing import Dict, List

import pandas as pd

START_MONTH = 202401
END_MONTH = 202603


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
            if START_MONTH <= month_key <= END_MONTH and month_key not in files:
                files[month_key] = path

    return dict(sorted(files.items()))


def coalesce_columns(df: pd.DataFrame, primary: str, fallback: str) -> None:
    if primary in df.columns and fallback in df.columns:
        df[primary] = df[primary].combine_first(df[fallback])
        df.drop(columns=[fallback], inplace=True)
    elif fallback in df.columns:
        df[primary] = df[fallback]
        df.drop(columns=[fallback], inplace=True)


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
    files = find_monthly_files("CRMLSListing", root)

    if not files:
        raise SystemExit("No listing CSV files found in the expected directories.")

    missing_months = [m for m in iter_months(START_MONTH, END_MONTH) if m not in files]
    if missing_months:
        print("Missing listing months:", missing_months)

    frames = []
    for month_key, path in files.items():
        df = pd.read_csv(path, low_memory=False)
        df["source_month"] = month_key
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)

    duplicate_pairs = [
        ("PropertyType", "PropertyType.1"),
        ("ListAgentFirstName", "ListAgentFirstName.1"),
        ("DaysOnMarket", "DaysOnMarket.1"),
        ("LivingArea", "LivingArea.1"),
        ("Longitude", "Longitude.1"),
        ("Latitude", "Latitude.1"),
        ("ListPrice", "ListPrice.1"),
        ("CloseDate", "CloseDate.1"),
        ("ListAgentLastName", "ListAgentLastName.1"),
        ("BuyerOfficeName", "BuyerOfficeName.1"),
        ("UnparsedAddress", "UnparsedAddress.1"),
    ]
    for primary, fallback in duplicate_pairs:
        coalesce_columns(df, primary, fallback)

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

    df["listing_year"] = df["ListingContractDate"].dt.year
    df["listing_month"] = df["ListingContractDate"].dt.month
    df["listing_year_month"] = df["ListingContractDate"].dt.strftime("%Y-%m")

    df["list_price_per_sqft"] = df["ListPrice"] / df["LivingArea"]
    df["close_price_per_sqft"] = df["ClosePrice"] / df["LivingArea"]
    df["list_to_original_ratio"] = df["ListPrice"] / df["OriginalListPrice"]
    df["close_to_list_ratio"] = df["ClosePrice"] / df["ListPrice"]

    df["property_age"] = df["listing_year"] - df["YearBuilt"]

    df["has_garage"] = (
        (df.get("GarageSpaces", 0).fillna(0) > 0)
        | yn_to_bool(df.get("AttachedGarageYN", pd.Series(index=df.index)))
    ).astype(int)

    df["has_fireplace"] = (
        (df.get("FireplacesTotal", 0).fillna(0) > 0)
        | yn_to_bool(df.get("FireplaceYN", pd.Series(index=df.index)))
    ).astype(int)

    df["has_new_construction"] = yn_to_bool(df.get("NewConstructionYN", pd.Series(index=df.index))).astype(int)

    keep_columns = [
        "ListingKey",
        "ListingId",
        "ListingKeyNumeric",
        "MlsStatus",
        "ListingContractDate",
        "PurchaseContractDate",
        "ContractStatusChangeDate",
        "CloseDate",
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
        "CoListOfficeName",
        "CoListAgentFirstName",
        "CoListAgentLastName",
        "BuyerOfficeName",
        "BuyerOfficeAOR",
        "BuyerAgentMlsId",
        "BuyerAgentFirstName",
        "BuyerAgentLastName",
        "CoBuyerAgentFirstName",
        "BuyerAgencyCompensation",
        "BuyerAgencyCompensationType",
        "source_month",
        "listing_year",
        "listing_month",
        "listing_year_month",
        "list_price_per_sqft",
        "close_price_per_sqft",
        "list_to_original_ratio",
        "close_to_list_ratio",
        "property_age",
        "has_garage",
        "has_fireplace",
        "has_new_construction",
    ]

    keep_columns = [col for col in keep_columns if col in df.columns]
    df = df[keep_columns]

    rename_map = {
        "ListingKey": "listing_key",
        "ListingId": "listing_id",
        "ListingKeyNumeric": "listing_key_numeric",
        "MlsStatus": "mls_status",
        "ListingContractDate": "listing_contract_date",
        "PurchaseContractDate": "purchase_contract_date",
        "ContractStatusChangeDate": "contract_status_change_date",
        "CloseDate": "close_date",
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
        "CoListOfficeName": "co_list_office_name",
        "CoListAgentFirstName": "co_list_agent_first_name",
        "CoListAgentLastName": "co_list_agent_last_name",
        "BuyerOfficeName": "buyer_office_name",
        "BuyerOfficeAOR": "buyer_office_aor",
        "BuyerAgentMlsId": "buyer_agent_mls_id",
        "BuyerAgentFirstName": "buyer_agent_first_name",
        "BuyerAgentLastName": "buyer_agent_last_name",
        "CoBuyerAgentFirstName": "co_buyer_agent_first_name",
        "BuyerAgencyCompensation": "buyer_agency_compensation",
        "BuyerAgencyCompensationType": "buyer_agency_compensation_type",
        "source_month": "source_month",
        "listing_year": "listing_year",
        "listing_month": "listing_month",
        "listing_year_month": "listing_year_month",
        "list_price_per_sqft": "list_price_per_sqft",
        "close_price_per_sqft": "close_price_per_sqft",
        "list_to_original_ratio": "list_to_original_ratio",
        "close_to_list_ratio": "close_to_list_ratio",
        "property_age": "property_age",
        "has_garage": "has_garage",
        "has_fireplace": "has_fireplace",
        "has_new_construction": "has_new_construction",
    }

    df = df.rename(columns=rename_map)

    sort_cols = ["listing_contract_date", "listing_key"]
    sort_cols = [c for c in sort_cols if c in df.columns]
    if sort_cols:
        ascending = [c != "listing_key" for c in sort_cols]
        df = df.sort_values(sort_cols, ascending=ascending)

    output_path = root / "IDX_Exchange" / "Week1" / "Listed_Final.csv"
    df.to_csv(output_path, index=False)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
