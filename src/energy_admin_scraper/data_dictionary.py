from __future__ import annotations

import pandas as pd

BASE_DESCRIPTIONS = {
    "source_section": {
        "description": "資料區塊名稱",
        "unit": "",
        "original_column": "",
        "note": "例如：全國、台電、民營電廠、自用發電設備、再生能源",
    },
    "roc_period": {
        "description": "民國年/月期間",
        "unit": "",
        "original_column": "各區塊第一欄",
        "note": "例如：114年、01月",
    },
    "period": {
        "description": "西元期間",
        "unit": "",
        "original_column": "各區塊 Period 欄位",
        "note": "monthly 為 YYYY/MM；annual 為 YYYY",
    },

    "total": {
        "description": "總計",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "total_share_pct": {
        "description": "總計占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "部分區塊才有",
    },

    "pumped_storage": {
        "description": "抽蓄水力",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "pumped_storage_share_pct": {
        "description": "抽蓄水力占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "",
    },

    "thermal_total": {
        "description": "火力合計",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "thermal_total_share_pct": {
        "description": "火力合計占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "",
    },

    "coal": {
        "description": "燃煤",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "coal_share_pct": {
        "description": "燃煤占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "",
    },

    "oil": {
        "description": "燃油",
        "original_column": "依 source_section 而異",
        "note": "部分區塊可能沒有此欄",
    },
    "oil_share_pct": {
        "description": "燃油占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "部分區塊可能沒有此欄",
    },

    "lng": {
        "description": "燃氣",
        "original_column": "依 source_section 而異",
        "note": "原始表頭為燃氣 / LNG-Fired",
    },
    "lng_share_pct": {
        "description": "燃氣占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "原始表頭為燃氣 / LNG-Fired",
    },

    "nuclear": {
        "description": "核能",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "nuclear_share_pct": {
        "description": "核能占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "",
    },

    "renewable_total": {
        "description": "再生能源合計",
        "original_column": "依 source_section 而異",
        "note": "3-02 / 3-03 使用",
    },
    "renewable_total_share_pct": {
        "description": "再生能源合計占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "3-02 / 3-03 使用",
    },

    "hydro": {
        "description": "慣常水力",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "hydro_share_pct": {
        "description": "慣常水力占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "",
    },

    "geothermal": {
        "description": "地熱",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "geothermal_share_pct": {
        "description": "地熱占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "",
    },

    "solar_pv": {
        "description": "太陽光電",
        "original_column": "依 source_section 而異",
        "note": "",
    },
    "solar_pv_share_pct": {
        "description": "太陽光電占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "",
    },

    "wind": {
        "description": "風力",
        "original_column": "依 source_section 而異",
        "note": "3-02 / 3-03 使用",
    },
    "wind_share_pct": {
        "description": "風力占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "3-02 / 3-03 使用",
    },

    "wind_total": {
        "description": "風力小計",
        "original_column": "Column9",
        "note": "4-01 / 4-02 使用",
    },
    "wind_total_share_pct": {
        "description": "風力小計占比",
        "unit": "%",
        "original_column": "Column10",
        "note": "4-01 / 4-02 使用",
    },
    "wind_onshore": {
        "description": "陸域風力",
        "original_column": "Column11",
        "note": "4-01 / 4-02 使用",
    },
    "wind_onshore_share_pct": {
        "description": "陸域風力占比",
        "unit": "%",
        "original_column": "Column12",
        "note": "4-01 / 4-02 使用",
    },
    "wind_offshore": {
        "description": "離岸風力",
        "original_column": "Column13",
        "note": "4-01 / 4-02 使用",
    },
    "wind_offshore_share_pct": {
        "description": "離岸風力占比",
        "unit": "%",
        "original_column": "Column14",
        "note": "4-01 / 4-02 使用",
    },

    "biomass": {
        "description": "生質能",
        "original_column": "依 source_section 而異",
        "note": "3-02 / 3-03 使用",
    },
    "biomass_share_pct": {
        "description": "生質能占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "3-02 / 3-03 使用",
    },

    "biomass_total": {
        "description": "生質能小計",
        "original_column": "Column15",
        "note": "4-01 / 4-02 使用",
    },
    "biomass_total_share_pct": {
        "description": "生質能小計占比",
        "unit": "%",
        "original_column": "Column16",
        "note": "4-01 / 4-02 使用",
    },
    "biomass_solid": {
        "description": "固態生質能",
        "original_column": "Column17",
        "note": "4-01 / 4-02 使用",
    },
    "biomass_solid_share_pct": {
        "description": "固態生質能占比",
        "unit": "%",
        "original_column": "Column18",
        "note": "4-01 / 4-02 使用",
    },
    "biomass_biogas": {
        "description": "氣態生質能",
        "original_column": "Column19",
        "note": "4-01 / 4-02 使用；原始英文表頭為 Biogas",
    },
    "biomass_biogas_share_pct": {
        "description": "氣態生質能占比",
        "unit": "%",
        "original_column": "Column20",
        "note": "4-01 / 4-02 使用",
    },

    "waste": {
        "description": "廢棄物",
        "original_column": "依 source_section 而異",
        "note": "部分區塊可能沒有此欄",
    },
    "waste_share_pct": {
        "description": "廢棄物占比",
        "unit": "%",
        "original_column": "依 source_section 而異",
        "note": "部分區塊可能沒有此欄",
    },

    "solar_water_heater_area": {
        "description": "太陽能熱水器裝設面積",
        "original_column": "Column23",
        "note": "4-02 使用；原始欄位為太陽能熱水器裝設面積",
    },
}


def split_column_name(column_name: str) -> tuple[str, str]:
    if column_name.endswith("_gwh"):
        return column_name.removesuffix("_gwh"), "GWh"

    if column_name.endswith("_mw"):
        return column_name.removesuffix("_mw"), "MW"

    if column_name.endswith("_mwh"):
        return column_name.removesuffix("_mwh"), "MWh"

    if column_name.endswith("_1000m2"):
        return column_name.removesuffix("_1000m2"), "千平方公尺"

    return column_name, ""


def build_data_dictionary(available_columns: list[str] | None = None) -> pd.DataFrame:
    if available_columns is None:
        available_columns = list(BASE_DESCRIPTIONS.keys())

    rows = []

    for column_name in available_columns:
        base_name, inferred_unit = split_column_name(column_name)
        meta = BASE_DESCRIPTIONS.get(base_name, {})

        rows.append(
            {
                "sheet": "monthly / annual",
                "column_name": column_name,
                "description": meta.get("description", ""),
                "unit": meta.get("unit", inferred_unit),
                "original_column": meta.get("original_column", ""),
                "note": meta.get("note", ""),
            }
        )

    return pd.DataFrame(rows)
