"""
data.py
========
Historical data loader from Binance Vision.

Author: Mustafa Tariq
"""

from pathlib import Path
import zipfile
import requests
import pandas as pd


# ============================================
# إعدادات المشروع
# ============================================

DATASET_DIR = Path("datasets")
DOWNLOAD_DIR = DATASET_DIR / "downloads"
CSV_DIR = DATASET_DIR / "csv"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)


# ============================================
# تحميل شهر واحد
# ============================================

def download_month(symbol, interval, year, month):

    month = f"{month:02d}"

    filename = f"{symbol}-{interval}-{year}-{month}.zip"

    url = (
        "https://data.binance.vision/data/"
        f"spot/monthly/klines/"
        f"{symbol}/{interval}/{filename}"
    )

    zip_path = DOWNLOAD_DIR / filename

    if zip_path.exists():
        return zip_path

    print(f"Downloading {filename}")

    r = requests.get(url, timeout=120)

    r.raise_for_status()

    with open(zip_path, "wb") as f:
        f.write(r.content)

    return zip_path


# ============================================
# فك الضغط
# ============================================

def extract_zip(zip_path):

    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        zip_ref.extractall(CSV_DIR)

    csv_name = zip_path.stem + ".csv"

    return CSV_DIR / csv_name


# ============================================
# قراءة CSV
# ============================================

def read_csv(csv_path):

    df = pd.read_csv(
        csv_path,
        header=None
    )

    df.columns = [
        "Open Time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close Time",
        "Quote Asset Volume",
        "Number Of Trades",
        "Taker Buy Base",
        "Taker Buy Quote",
        "Ignore"
    ]

    df = df[
        [
            "Open Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    ]

    df["Open Time"] = pd.to_datetime(
        df["Open Time"],
        unit="ms"
    )

    df.rename(
        columns={
            "Open Time": "Date"
        },
        inplace=True
    )

    df.set_index(
        "Date",
        inplace=True
    )

    return df


# ============================================
# تحميل فترة كاملة
# ============================================

def load_data(
    symbol="BTCUSDT",
    interval="1h",
    start_year=2024,
    start_month=1,
    end_year=2024,
    end_month=3
):

    frames = []

    year = start_year
    month = start_month

    while True:

        zip_file = download_month(
            symbol,
            interval,
            year,
            month
        )

        csv_file = extract_zip(zip_file)

        df = read_csv(csv_file)

        frames.append(df)

        if year == end_year and month == end_month:
            break

        month += 1

        if month > 12:
            month = 1
            year += 1

    df = pd.concat(frames)

    df = df.sort_index()

    return df
