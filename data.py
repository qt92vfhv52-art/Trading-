"""
data.py
========
Historical Data Loader for Binance Vision

Features
--------
✓ Download historical data automatically
✓ Extract ZIP files
✓ Read CSV files
✓ Merge multiple months
✓ Clean data
✓ Remove duplicates
✓ Return ready-to-use DataFrame

Author: Mustafa Tariq
"""

from pathlib import Path
import zipfile
import requests
import pandas as pd


# ======================================================
# Project Directories
# ======================================================

DATASET_DIR = Path("datasets")
DOWNLOAD_DIR = DATASET_DIR / "downloads"
CSV_DIR = DATASET_DIR / "csv"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)


# ======================================================
# Download One Month
# ======================================================

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

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with open(zip_path, "wb") as f:
        f.write(response.content)

    return zip_path


# ======================================================
# Extract ZIP
# ======================================================

def extract_zip(zip_path):

    csv_path = CSV_DIR / (zip_path.stem + ".csv")

    if csv_path.exists():
        return csv_path

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(CSV_DIR)

    return csv_path


# ======================================================
# Read CSV
# ======================================================

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

    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    df[numeric_columns] = df[numeric_columns].astype(float)

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


# ======================================================
# Load Historical Data
# ======================================================

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

    df = df[~df.index.duplicated()]

    df = df.sort_index()

    return df


# ======================================================
# Example
# ======================================================

if __name__ == "__main__":

    df = load_data(
        symbol="BTCUSDT",
        interval="1h",
        start_year=2024,
        start_month=1,
        end_year=2024,
        end_month=2
    )

    print(df.head())
    print(df.tail())
    print(df.shape)
