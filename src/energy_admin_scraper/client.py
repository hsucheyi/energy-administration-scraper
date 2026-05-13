from __future__ import annotations

import json
import warnings
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from requests.exceptions import SSLError
from urllib3.exceptions import InsecureRequestWarning


TAIPEI_TZ = ZoneInfo("Asia/Taipei")


def fetch_json(url: str, timeout: int = 60) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": "application/json,text/plain,*/*",
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()

    except SSLError:
        print("SSL verification failed. Retrying with verify=False for this API endpoint.")

        warnings.simplefilter("ignore", InsecureRequestWarning)

        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            verify=False,
        )
        response.raise_for_status()
        return response.json()


def save_raw_json(payload: dict, raw_dir: str | Path) -> Path:
    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d")
    output_path = raw_dir / f"response_{today}.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return output_path
