from __future__ import annotations

import re
from typing import Any

import pandas as pd


MONTHLY_PATTERN = re.compile(r"^\d{4}/\d{2}$")
ANNUAL_PATTERN = re.compile(r"^\d{4}$")


TABLE_TITLE_COLUMNS = {
    "全國": "3-02發電量（全國）_Electricity Generation (Nationwide)",
    "台電": "3-02發電量（台電）_Electricity Generation (Taipower)",
    "民營電廠": "3-02發電量（民營電廠）_Electricity Generation (IPP)",
    "自用發電設備": "3-02發電量（自用發電設備）_Electricity Generation (Self-Use Power Generation Equipment)",
}


COLUMN_MAP = {
    "全國": {
        "Column2": "total_gwh",
        "Column3": "pumped_storage_gwh",
        "Column4": "pumped_storage_share_pct",
        "Column5": "thermal_total_gwh",
        "Column6": "thermal_total_share_pct",
        "Column7": "coal_gwh",
        "Column8": "coal_share_pct",
        "Column9": "oil_gwh",
        "Column10": "oil_share_pct",
        "Column11": "lng_gwh",
        "Column12": "lng_share_pct",
        "Column13": "nuclear_gwh",
        "Column14": "nuclear_share_pct",
        "Column15": "renewable_total_gwh",
        "Column16": "renewable_total_share_pct",
        "Column17": "hydro_gwh",
        "Column18": "hydro_share_pct",
        "Column19": "geothermal_gwh",
        "Column20": "geothermal_share_pct",
        "Column21": "solar_pv_gwh",
        "Column22": "solar_pv_share_pct",
        "Column23": "wind_gwh",
        "Column24": "wind_share_pct",
        "Column25": "biomass_gwh",
        "Column26": "biomass_share_pct",
        "Column27": "waste_gwh",
        "Column28": "waste_share_pct",
        "Column29": "period",
    },
    "台電": {
        "Column2": "total_gwh",
        "Column3": "total_share_pct",
        "Column4": "pumped_storage_gwh",
        "Column5": "pumped_storage_share_pct",
        "Column6": "thermal_total_gwh",
        "Column7": "thermal_total_share_pct",
        "Column8": "coal_gwh",
        "Column9": "coal_share_pct",
        "Column10": "oil_gwh",
        "Column11": "oil_share_pct",
        "Column12": "lng_gwh",
        "Column13": "lng_share_pct",
        "Column14": "nuclear_gwh",
        "Column15": "nuclear_share_pct",
        "Column16": "renewable_total_gwh",
        "Column17": "renewable_total_share_pct",
        "Column18": "hydro_gwh",
        "Column19": "hydro_share_pct",
        "Column20": "geothermal_gwh",
        "Column21": "geothermal_share_pct",
        "Column22": "solar_pv_gwh",
        "Column23": "solar_pv_share_pct",
        "Column24": "wind_gwh",
        "Column25": "wind_share_pct",
        "Column26": "period",
    },
    "民營電廠": {
        "Column2": "total_gwh",
        "Column3": "total_share_pct",
        "Column4": "thermal_total_gwh",
        "Column5": "thermal_total_share_pct",
        "Column6": "coal_gwh",
        "Column7": "coal_share_pct",
        "Column8": "lng_gwh",
        "Column9": "lng_share_pct",
        "Column10": "renewable_total_gwh",
        "Column11": "renewable_total_share_pct",
        "Column12": "hydro_gwh",
        "Column13": "hydro_share_pct",
        "Column14": "geothermal_gwh",
        "Column15": "geothermal_share_pct",
        "Column16": "solar_pv_gwh",
        "Column17": "solar_pv_share_pct",
        "Column18": "wind_gwh",
        "Column19": "wind_share_pct",
        "Column20": "period",
    },
}


def normalize_table(section_name: str, rows: list[dict[str, Any]]) -> pd.DataFrame:
    title_col = TABLE_TITLE_COLUMNS.get(section_name)
    column_map = COLUMN_MAP.get(section_name)

    if title_col is None or column_map is None:
        return pd.DataFrame()

    records = []

    for row in rows:
        period = row.get(column_map.get("Column29", "Column29")) or row.get("Column29")

        # 不同區塊 period 欄位位置不同，所以從 mapping 反查
        period_col = next((k for k, v in column_map.items() if v == "period"), None)
        period = row.get(period_col) if period_col else None

        if not isinstance(period, str):
            continue

        if not (MONTHLY_PATTERN.match(period) or ANNUAL_PATTERN.match(period)):
            continue

        record = {
            "source_section": section_name,
            "roc_period": row.get(title_col),
            "period": period,
        }

        for raw_col, clean_col in column_map.items():
            if clean_col == "period":
                continue
            record[clean_col] = row.get(raw_col)

        records.append(record)

    df = pd.DataFrame(records)

    if df.empty:
        return df

    numeric_cols = [c for c in df.columns if c not in ["source_section", "roc_period", "period"]]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def transform_payload(payload: dict[str, list[dict[str, Any]]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames = []

    for section_name, rows in payload.items():
        if not isinstance(rows, list):
            continue

        df = normalize_table(section_name, rows)
        if not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame(), pd.DataFrame()

    all_df = pd.concat(frames, ignore_index=True)

    monthly_df = all_df[all_df["period"].str.match(MONTHLY_PATTERN)].copy()
    annual_df = all_df[all_df["period"].str.match(ANNUAL_PATTERN)].copy()

    monthly_df = monthly_df.sort_values(["source_section", "period"]).reset_index(drop=True)
    annual_df = annual_df.sort_values(["source_section", "period"]).reset_index(drop=True)

    return monthly_df, annual_df
