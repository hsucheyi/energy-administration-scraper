from __future__ import annotations

import re
from typing import Any

import pandas as pd

MONTHLY_PATTERN = re.compile(r"^\d{4}/\d{2}$")
ANNUAL_PATTERN = re.compile(r"^\d{4}$")


POWER_GENERATION_SECTION_MAPS = {
    "全國": {
        "Column2": "total",
        "Column3": "pumped_storage",
        "Column4": "pumped_storage_share_pct",
        "Column5": "thermal_total",
        "Column6": "thermal_total_share_pct",
        "Column7": "coal",
        "Column8": "coal_share_pct",
        "Column9": "oil",
        "Column10": "oil_share_pct",
        "Column11": "lng",
        "Column12": "lng_share_pct",
        "Column13": "nuclear",
        "Column14": "nuclear_share_pct",
        "Column15": "renewable_total",
        "Column16": "renewable_total_share_pct",
        "Column17": "hydro",
        "Column18": "hydro_share_pct",
        "Column19": "geothermal",
        "Column20": "geothermal_share_pct",
        "Column21": "solar_pv",
        "Column22": "solar_pv_share_pct",
        "Column23": "wind",
        "Column24": "wind_share_pct",
        "Column25": "biomass",
        "Column26": "biomass_share_pct",
        "Column27": "waste",
        "Column28": "waste_share_pct",
        "Column29": "period",
    },
    "台電": {
        "Column2": "total",
        "Column3": "total_share_pct",
        "Column4": "pumped_storage",
        "Column5": "pumped_storage_share_pct",
        "Column6": "thermal_total",
        "Column7": "thermal_total_share_pct",
        "Column8": "coal",
        "Column9": "coal_share_pct",
        "Column10": "oil",
        "Column11": "oil_share_pct",
        "Column12": "lng",
        "Column13": "lng_share_pct",
        "Column14": "nuclear",
        "Column15": "nuclear_share_pct",
        "Column16": "renewable_total",
        "Column17": "renewable_total_share_pct",
        "Column18": "hydro",
        "Column19": "hydro_share_pct",
        "Column20": "geothermal",
        "Column21": "geothermal_share_pct",
        "Column22": "solar_pv",
        "Column23": "solar_pv_share_pct",
        "Column24": "wind",
        "Column25": "wind_share_pct",
        "Column26": "period",
    },
    "民營電廠": {
        "Column2": "total",
        "Column3": "total_share_pct",
        "Column4": "thermal_total",
        "Column5": "thermal_total_share_pct",
        "Column6": "coal",
        "Column7": "coal_share_pct",
        "Column8": "lng",
        "Column9": "lng_share_pct",
        "Column10": "renewable_total",
        "Column11": "renewable_total_share_pct",
        "Column12": "hydro",
        "Column13": "hydro_share_pct",
        "Column14": "geothermal",
        "Column15": "geothermal_share_pct",
        "Column16": "solar_pv",
        "Column17": "solar_pv_share_pct",
        "Column18": "wind",
        "Column19": "wind_share_pct",
        "Column20": "period",
    },
    "自用發電設備": {
        "Column2": "total",
        "Column3": "total_share_pct",
        "Column4": "thermal_total",
        "Column5": "thermal_total_share_pct",
        "Column6": "coal",
        "Column7": "coal_share_pct",
        "Column8": "oil",
        "Column9": "oil_share_pct",
        "Column10": "lng",
        "Column11": "lng_share_pct",
        "Column12": "renewable_total",
        "Column13": "renewable_total_share_pct",
        "Column14": "hydro",
        "Column15": "hydro_share_pct",
        "Column16": "geothermal",
        "Column17": "geothermal_share_pct",
        "Column18": "solar_pv",
        "Column19": "solar_pv_share_pct",
        "Column20": "wind",
        "Column21": "wind_share_pct",
        "Column22": "biomass",
        "Column23": "biomass_share_pct",
        "Column24": "waste",
        "Column25": "waste_share_pct",
        "Column26": "period",
    },
}


RENEWABLE_ELECTRICITY_GENERATION_MAP = {
    "Column2": "total",
    "Column3": "hydro",
    "Column4": "hydro_share_pct",
    "Column5": "geothermal",
    "Column6": "geothermal_share_pct",
    "Column7": "solar_pv",
    "Column8": "solar_pv_share_pct",
    "Column9": "wind_total",
    "Column10": "wind_total_share_pct",
    "Column11": "wind_onshore",
    "Column12": "wind_onshore_share_pct",
    "Column13": "wind_offshore",
    "Column14": "wind_offshore_share_pct",
    "Column15": "biomass_total",
    "Column16": "biomass_total_share_pct",
    "Column17": "biomass_solid",
    "Column18": "biomass_solid_share_pct",
    "Column19": "biomass_biogas",
    "Column20": "biomass_biogas_share_pct",
    "Column21": "waste",
    "Column22": "waste_share_pct",
    "Column23": "period",
}


RENEWABLE_INSTALLED_CAPACITY_MAP = {
    "Column2": "total",
    "Column3": "hydro",
    "Column4": "hydro_share_pct",
    "Column5": "geothermal",
    "Column6": "geothermal_share_pct",
    "Column7": "solar_pv",
    "Column8": "solar_pv_share_pct",
    "Column9": "wind_total",
    "Column10": "wind_total_share_pct",
    "Column11": "wind_onshore",
    "Column12": "wind_onshore_share_pct",
    "Column13": "wind_offshore",
    "Column14": "wind_offshore_share_pct",
    "Column15": "biomass_total",
    "Column16": "biomass_total_share_pct",
    "Column17": "biomass_solid",
    "Column18": "biomass_solid_share_pct",
    "Column19": "biomass_biogas",
    "Column20": "biomass_biogas_share_pct",
    "Column21": "waste",
    "Column22": "waste_share_pct",
    "Column23": "solar_water_heater_area_1000m2",
    "Column24": "period",
}


def infer_roc_period_column(row: dict[str, Any]) -> str | None:
    """
    API 的第一欄名稱會隨資料表改變，例如：
    - 3-02發電量（全國）_Electricity Generation (Nationwide)
    - 3-03發電裝置容量（全國）_Installed Capacity (Nationwide)
    - 4-01再生能源發電量_Renewable energy electricity generation
    - 4-02再生能源裝(設)置容量_Renewable Energy Installed Capacity

    但它通常不是 Column2, Column3...，所以可以用這個方式自動找出。
    """
    for key in row.keys():
        if not key.startswith("Column"):
            return key
    return None


def get_column_map(section_name: str, value_unit: str) -> dict[str, str] | None:
    """
    3-02 / 3-03 的 section_name 是「全國、台電、民營電廠、自用發電設備」。
    4-01 / 4-02 的 section_name 都是「再生能源」，但欄位不同：
    - 4-01 value_unit = MWh，Period 在 Column23
    - 4-02 value_unit = MW，Period 在 Column24，且 Column23 是太陽能熱水器面積
    """
    if section_name in POWER_GENERATION_SECTION_MAPS:
        return POWER_GENERATION_SECTION_MAPS[section_name]

    if section_name == "再生能源":
        normalized_unit = value_unit.strip().lower()

        if normalized_unit == "mwh":
            return RENEWABLE_ELECTRICITY_GENERATION_MAP

        if normalized_unit == "mw":
            return RENEWABLE_INSTALLED_CAPACITY_MAP

    return None


def add_unit_suffix(column_name: str, value_unit: str) -> str:
    """
    將數值欄位依 dataset 單位加上 suffix：
    - 3-02: total_gwh, coal_gwh
    - 3-03: total_mw, coal_mw
    - 4-01: total_mwh, solar_pv_mwh
    - 4-02: total_mw, solar_pv_mw

    share_pct 欄位維持不變。
    已內含單位的特殊欄位，例如 solar_water_heater_area_1000m2，不再追加 MW。
    """
    if column_name in {"source_section", "roc_period", "period"}:
        return column_name

    if column_name.endswith("_share_pct"):
        return column_name

    if column_name.endswith("_1000m2"):
        return column_name

    return f"{column_name}_{value_unit.lower()}"


def normalize_table(
    section_name: str,
    rows: list[dict[str, Any]],
    value_unit: str,
) -> pd.DataFrame:
    column_map = get_column_map(section_name, value_unit)

    if column_map is None:
        return pd.DataFrame()

    period_col = next((k for k, v in column_map.items() if v == "period"), None)

    if period_col is None:
        return pd.DataFrame()

    records = []

    for row in rows:
        period = row.get(period_col)

        if not isinstance(period, str):
            continue

        period = period.strip()

        # 只保留月頻與年頻。
        #
        # 會排除：
        # - YYYY/01-03 累計列
        # - Compared with ... 比較列
        # - 註解列
        # - 季資料，例如 2025 Q1
        if not (MONTHLY_PATTERN.match(period) or ANNUAL_PATTERN.match(period)):
            continue

        roc_period_col = infer_roc_period_column(row)

        record = {
            "source_section": section_name,
            "roc_period": row.get(roc_period_col) if roc_period_col else None,
            "period": period,
        }

        for raw_col, clean_col in column_map.items():
            if clean_col == "period":
                continue

            clean_col_with_unit = add_unit_suffix(clean_col, value_unit)
            record[clean_col_with_unit] = row.get(raw_col)

        records.append(record)

    df = pd.DataFrame(records)

    if df.empty:
        return df

    numeric_cols = [
        c for c in df.columns
        if c not in ["source_section", "roc_period", "period"]
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def transform_payload(
    payload: dict[str, list[dict[str, Any]]],
    value_unit: str = "GWh",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames = []

    for section_name, rows in payload.items():
        if not isinstance(rows, list):
            continue

        df = normalize_table(
            section_name=section_name,
            rows=rows,
            value_unit=value_unit,
        )

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
