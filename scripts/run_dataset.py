from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from energy_admin_scraper.client import fetch_json, save_raw_json
from energy_admin_scraper.transform import transform_payload
from energy_admin_scraper.excel import write_excel


def load_config(dataset_id: str, config_path: str = "configs/datasets.yml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    datasets = config.get("datasets", {})
    if dataset_id not in datasets:
        available = ", ".join(datasets.keys())
        raise ValueError(f"Unknown dataset_id: {dataset_id}. Available: {available}")

    return datasets[dataset_id]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    dataset = load_config(args.dataset)

    payload = fetch_json(dataset["url"])
    raw_path = save_raw_json(payload, dataset["raw_dir"])

    monthly_df, annual_df = transform_payload(
        payload,
        value_unit=dataset.get("value_unit", "GWh"),
    )

    output_path = Path(dataset["output_dir"]) / dataset["excel_file"]
    write_excel(monthly_df, annual_df, output_path)

    print(f"Saved raw JSON: {raw_path}")
    print(f"Saved Excel: {output_path}")
    print(f"Monthly rows: {len(monthly_df)}")
    print(f"Annual rows: {len(annual_df)}")


if __name__ == "__main__":
    main()
