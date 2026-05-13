from __future__ import annotations

from pathlib import Path

import pandas as pd

from energy_admin_scraper.data_dictionary import build_data_dictionary


def write_excel(monthly_df: pd.DataFrame, annual_df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data_dictionary_df = build_data_dictionary()

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        monthly_df.to_excel(writer, sheet_name="monthly", index=False)
        annual_df.to_excel(writer, sheet_name="annual", index=False)
        data_dictionary_df.to_excel(writer, sheet_name="data_dictionary", index=False)

    return output_path
