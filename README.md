# Energy Administration Scraper

自動抓取經濟部能源署「應用程式介面（API）專區」資料，整理成 Excel，並透過 GitHub Actions 每月定期更新。

目前支援兩個資料集：

1. `3-02 發電量`
2. `3-03 發電裝置容量`

兩個資料集都會輸出 Excel，並依資料頻率分成：

- `monthly`：月頻資料
- `annual`：年頻資料
- `data_dictionary`：欄位說明

---

## 資料來源

資料來源為經濟部能源署 API：

| dataset_id | 資料名稱 | API |
|---|---|---|
| `zone_monthly_3_02` | 3-02 發電量 | `https://ea01.moeaea.gov.tw/a0303/02/api/v1/zone/monthly/3/2` |
| `zone_monthly_3_03` | 3-03 發電裝置容量 | `https://ea01.moeaea.gov.tw/a0303/02/api/v1/zone/monthly/3/3/` |

---

## 目前功能

### 1. 抓取 3-02 發電量

輸出檔案：

```text
output/zone_monthly_3_02/electricity_generation_3_02.xlsx
```

原始 JSON 保存位置：

```text
data/raw/zone_monthly_3_02/response_YYYY-MM-DD.json
```

資料單位：

| 欄位類型 | 單位 |
|---|---|
| 發電量 | GWh |
| 占比 | % |

Excel 工作頁：

| sheet | 說明 |
|---|---|
| `monthly` | 僅保留 `period` 格式為 `YYYY/MM` 的月頻資料 |
| `annual` | 僅保留 `period` 格式為 `YYYY` 的年頻資料 |
| `data_dictionary` | 欄位名稱、單位與說明 |

---

### 2. 抓取 3-03 發電裝置容量

輸出檔案：

```text
output/zone_monthly_3_03/installed_capacity_3_03.xlsx
```

原始 JSON 保存位置：

```text
data/raw/zone_monthly_3_03/response_YYYY-MM-DD.json
```

資料單位：

| 欄位類型 | 單位 |
|---|---|
| 裝置容量 | MW |
| 占比 | % |

Excel 工作頁：

| sheet | 說明 |
|---|---|
| `monthly` | 僅保留 `period` 格式為 `YYYY/MM` 的月頻資料 |
| `annual` | 僅保留 `period` 格式為 `YYYY` 的年頻資料 |
| `data_dictionary` | 欄位名稱、單位與說明 |

補充說明：

`3-03 發電裝置容量` 是存量資料，因此沒有累計值；年度資料代表當年度 12 月數值。

---

## 專案結構

```text
energy-administration-scraper/
├─ .github/
│  └─ workflows/
│     └─ monthly_energy_admin_api.yml
├─ configs/
│  └─ datasets.yml
├─ data/
│  └─ raw/
│     ├─ zone_monthly_3_02/
│     └─ zone_monthly_3_03/
├─ output/
│  ├─ zone_monthly_3_02/
│  │  └─ electricity_generation_3_02.xlsx
│  └─ zone_monthly_3_03/
│     └─ installed_capacity_3_03.xlsx
├─ scripts/
│  └─ run_dataset.py
├─ src/
│  └─ energy_admin_scraper/
│     ├─ __init__.py
│     ├─ client.py
│     ├─ data_dictionary.py
│     ├─ excel.py
│     └─ transform.py
├─ requirements.txt
└─ README.md
```

---

## 資料處理邏輯

能源署 API 回傳格式接近「Excel 表格轉 JSON」，不是乾淨的一列一筆資料格式。

每個資料區塊通常包含：

- 前幾列：表頭、分類、單位
- 中間資料列：年資料與月資料
- 後面資料列：比較列、註解列

本專案處理時會：

1. 讀取 API JSON
2. 保存原始 JSON 到 `data/raw/`
3. 從各資料區塊中擷取有效資料列
4. 依 `period` 欄位判斷資料頻率
5. 分別輸出月頻與年頻 Excel 工作頁

頻率判斷規則：

| period 格式 | 判定 | 輸出 sheet |
|---|---|---|
| `YYYY/MM` | 月頻資料 | `monthly` |
| `YYYY` | 年頻資料 | `annual` |
| `YYYY/MM-MM` | 累計資料 | 目前排除 |
| `Compared with ...` | 比較資料 | 目前排除 |
| 註解列 | 說明文字 | 目前排除 |

---

## 輸出欄位命名規則

整理後欄位使用英文 snake_case。

### 共通欄位

| 欄位 | 說明 |
|---|---|
| `source_section` | 資料區塊，例如：全國、台電、民營電廠、自用發電設備 |
| `roc_period` | 原始民國年/月期間，例如：114年、01月 |
| `period` | 西元期間，例如：2025、2025/01 |

### 3-02 發電量欄位

3-02 的數值欄位以 `_gwh` 結尾，例如：

| 欄位 | 說明 |
|---|---|
| `total_gwh` | 總發電量 |
| `thermal_total_gwh` | 火力發電量合計 |
| `coal_gwh` | 燃煤發電量 |
| `oil_gwh` | 燃油發電量 |
| `lng_gwh` | 燃氣發電量 |
| `nuclear_gwh` | 核能發電量 |
| `renewable_total_gwh` | 再生能源發電量合計 |
| `hydro_gwh` | 慣常水力發電量 |
| `geothermal_gwh` | 地熱發電量 |
| `solar_pv_gwh` | 太陽光電發電量 |
| `wind_gwh` | 風力發電量 |
| `biomass_gwh` | 生質能發電量 |
| `waste_gwh` | 廢棄物發電量 |

占比欄位以 `_share_pct` 結尾，例如：

```text
coal_share_pct
solar_pv_share_pct
renewable_total_share_pct
```

---

### 3-03 發電裝置容量欄位

3-03 的數值欄位以 `_mw` 結尾，例如：

| 欄位 | 說明 |
|---|---|
| `total_mw` | 總裝置容量 |
| `thermal_total_mw` | 火力裝置容量合計 |
| `coal_mw` | 燃煤裝置容量 |
| `oil_mw` | 燃油裝置容量 |
| `lng_mw` | 燃氣裝置容量 |
| `nuclear_mw` | 核能裝置容量 |
| `renewable_total_mw` | 再生能源裝置容量合計 |
| `hydro_mw` | 慣常水力裝置容量 |
| `geothermal_mw` | 地熱裝置容量 |
| `solar_pv_mw` | 太陽光電裝置容量 |
| `wind_mw` | 風力裝置容量 |
| `biomass_mw` | 生質能裝置容量 |
| `waste_mw` | 廢棄物裝置容量 |

占比欄位以 `_share_pct` 結尾，例如：

```text
coal_share_pct
solar_pv_share_pct
renewable_total_share_pct
```

---

## 設定檔

所有資料集設定放在：

```text
configs/datasets.yml
```

目前設定範例：

```yaml
datasets:
  zone_monthly_3_02:
    name: electricity_generation_3_02
    description: "3-02 發電量"
    url: "https://ea01.moeaea.gov.tw/a0303/02/api/v1/zone/monthly/3/2"
    output_dir: "output/zone_monthly_3_02"
    raw_dir: "data/raw/zone_monthly_3_02"
    excel_file: "electricity_generation_3_02.xlsx"
    dataset_type: "electricity_generation"
    value_unit: "GWh"

  zone_monthly_3_03:
    name: installed_capacity_3_03
    description: "3-03 發電裝置容量"
    url: "https://ea01.moeaea.gov.tw/a0303/02/api/v1/zone/monthly/3/3/"
    output_dir: "output/zone_monthly_3_03"
    raw_dir: "data/raw/zone_monthly_3_03"
    excel_file: "installed_capacity_3_03.xlsx"
    dataset_type: "installed_capacity"
    value_unit: "MW"
```

新增其他能源署 API 時，原則上只需要在 `datasets.yml` 新增一組 dataset 設定，並確認欄位結構是否能沿用目前的轉換邏輯。

---

## 本機執行

安裝套件：

```bash
pip install -r requirements.txt
```

執行 3-02 發電量：

```bash
PYTHONPATH=src python scripts/run_dataset.py --dataset zone_monthly_3_02
```

執行 3-03 發電裝置容量：

```bash
PYTHONPATH=src python scripts/run_dataset.py --dataset zone_monthly_3_03
```

---

## GitHub Actions 自動更新

本專案使用 GitHub Actions 每月定期抓取資料。

Workflow 檔案位置：

```text
.github/workflows/monthly_energy_admin_api.yml
```

排程：

```yaml
cron: "15 1 15 * *"
```

對應台灣時間：

```text
每月 15 號 09:15
```

目前 workflow 會執行：

```bash
PYTHONPATH=src python scripts/run_dataset.py --dataset zone_monthly_3_02
PYTHONPATH=src python scripts/run_dataset.py --dataset zone_monthly_3_03
```

若資料有更新，GitHub Actions 會自動 commit 並 push：

```text
data/raw/
output/
```

---

## GitHub Actions 權限設定

Workflow 需要寫入 repository，請確認 workflow 設定中有：

```yaml
permissions:
  contents: write
```

如果遇到無法 push 的問題，請到 GitHub repo 設定確認：

```text
Settings
→ Actions
→ General
→ Workflow permissions
→ Read and write permissions
```

---

## SSL 憑證問題

能源署 API 在 GitHub Actions 環境中可能出現 SSL 憑證鏈驗證失敗：

```text
SSLCertVerificationError: certificate verify failed
```

本專案的抓取邏輯會先使用正常 SSL 驗證；如果遇到 SSL 驗證錯誤，才會針對該 API endpoint 以 `verify=False` 重新嘗試。

這是為了處理特定政府網站憑證鏈在 GitHub Actions 環境中無法完整驗證的情況。

---

## 輸出檔案

目前預期輸出：

```text
output/
├─ zone_monthly_3_02/
│  └─ electricity_generation_3_02.xlsx
└─ zone_monthly_3_03/
   └─ installed_capacity_3_03.xlsx
```

原始 JSON：

```text
data/
└─ raw/
   ├─ zone_monthly_3_02/
   │  └─ response_YYYY-MM-DD.json
   └─ zone_monthly_3_03/
      └─ response_YYYY-MM-DD.json
```

---

## 資料版本控管策略

本專案同時保留：

1. 原始 API JSON
2. 整理後 Excel

原始 JSON 用於：

- 追蹤 API 回傳格式是否改變
- Debug 資料轉換問題
- 保留每次排程抓取的原始紀錄

整理後 Excel 用於：

- 一般分析
- 人工檢查
- 後續匯入其他分析流程

---

## 後續擴充方向

未來可以繼續接其他經濟部能源署 API，例如：

```text
zone_monthly_3_04
zone_monthly_3_05
...
```

建議擴充原則：

1. 每支 API 在 `configs/datasets.yml` 新增一個 dataset
2. 原始資料放在 `data/raw/{dataset_id}/`
3. 整理後資料放在 `output/{dataset_id}/`
4. Excel 內維持 `monthly`、`annual`、`data_dictionary` 的工作頁設計
5. 若資料結構與目前不同，再擴充 `transform.py`

---

## License

此專案僅作為公開資料自動化整理使用。資料來源與資料授權依經濟部能源署公告為準。
