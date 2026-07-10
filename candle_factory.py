"""
=========================================================
candle_factory.py
=========================================================

يقوم بتحويل DataFrame إلى قائمة من Candle Objects.

Author : Mustafa Tariq
=========================================================
"""

from __future__ import annotations

from typing import List

import pandas as pd

from candle import Candle


# ==========================================================
# TRUE RANGE
# ==========================================================

def true_range(df: pd.DataFrame):

    previous_close = df["Close"].shift(1)

    tr = pd.concat(
        [
            df["High"] - df["Low"],
            (df["High"] - previous_close).abs(),
            (df["Low"] - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    return tr


# ==========================================================
# ATR
# ==========================================================

def atr(df: pd.DataFrame, period: int = 14):

    tr = true_range(df)

    return tr.rolling(period).mean()


# ==========================================================
# PREPARE DATA
# ==========================================================

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    data = df.copy()

    data["ATR"] = atr(data)

    data["Velocity"] = data["Close"].diff()

    data["Acceleration"] = data["Velocity"].diff()

    return data


# ==========================================================
# DATAFRAME -> CANDLES
# ==========================================================

def dataframe_to_candles(
    df: pd.DataFrame,
) -> List[Candle]:

    data = prepare_dataframe(df)

    candles: List[Candle] = []

    for i, (time, row) in enumerate(data.iterrows()):

        candle = Candle(

            index=i,

            time=time,

            open=float(row["Open"]),

            high=float(row["High"]),

            low=float(row["Low"]),

            close=float(row["Close"]),

            volume=float(row["Volume"]),

            atr=float(row["ATR"]) if pd.notna(row["ATR"]) else 0.0,

            velocity=float(row["Velocity"]) if pd.notna(row["Velocity"]) else 0.0,

            acceleration=float(row["Acceleration"]) if pd.notna(row["Acceleration"]) else 0.0,

        )

        candles.append(candle)

    return candles


# ==========================================================
# GET SINGLE CANDLE
# ==========================================================

def get_candle(
    candles: List[Candle],
    index: int,
):

    return candles[index]


# ==========================================================
# TO DATAFRAME
# ==========================================================

def candles_to_dataframe(
    candles: List[Candle],
):

    rows = []

    for candle in candles:

        rows.append(candle.to_dict())

    return pd.DataFrame(rows)
