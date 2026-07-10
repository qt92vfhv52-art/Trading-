"""
indicators.py
==============

Mathematical indicators.

Author: Mustafa Tariq
"""

import pandas as pd


def find_swings(df: pd.DataFrame, window: int = 5):

    if window % 2 == 0:
        raise ValueError("window must be odd")

    df = df.copy()

    df["Swing High"] = False
    df["Swing Low"] = False

    half = window // 2

    highs = df["High"].values
    lows = df["Low"].values

    for i in range(half, len(df) - half):

        high_window = highs[i-half:i+half+1]

        if highs[i] == high_window.max():
            df.iloc[i, df.columns.get_loc("Swing High")] = True

        low_window = lows[i-half:i+half+1]

        if lows[i] == low_window.min():
            df.iloc[i, df.columns.get_loc("Swing Low")] = True

    return df

def filter_swings(df, min_distance=0.005):
    """
    إزالة القمم والقيعان المتقاربة.

    min_distance = أقل فرق سعري (مثلاً 0.005 = 0.5%)
    """

    df = df.copy()

    highs = df[df["Swing High"]].copy()

    keep = []

    last_price = None

    for idx, row in highs.iterrows():

        price = row["High"]

        if last_price is None:
            keep.append(idx)
            last_price = price
            continue

        change = abs(price - last_price) / last_price

        if change >= min_distance:
            keep.append(idx)
            last_price = price

        else:
            # احتفظ بالأعلى
            if price > last_price:
                keep[-1] = idx
                last_price = price

    df["Swing High"] = False
    df.loc[keep, "Swing High"] = True

    # -----------------------

    lows = df[df["Swing Low"]].copy()

    keep = []

    last_price = None

    for idx, row in lows.iterrows():

        price = row["Low"]

        if last_price is None:
            keep.append(idx)
            last_price = price
            continue

        change = abs(price - last_price) / last_price

        if change >= min_distance:
            keep.append(idx)
            last_price = price

        else:
            # احتفظ بالأقل
            if price < last_price:
                keep[-1] = idx
                last_price = price

    df["Swing Low"] = False
    df.loc[keep, "Swing Low"] = True

    return df
    

import matplotlib.pyplot as plt


def plot_swings(df, last=300):
    """
    رسم السعر مع القمم والقيعان.
    """

    data = df.tail(last)

    plt.figure(figsize=(18, 8))

    # السعر
    plt.plot(
        data.index,
        data["Close"],
        linewidth=1.2,
        label="Close"
    )

    # القمم
    highs = data[data["Swing High"]]

    plt.scatter(
        highs.index,
        highs["High"],
        marker="^",
        s=80,
        label="Swing High"
    )

    # القيعان
    lows = data[data["Swing Low"]]

    plt.scatter(
        lows.index,
        lows["Low"],
        marker="v",
        s=80,
        label="Swing Low"
    )

    plt.title("Swing Detection")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()
