"""
market_geometry.py
==================

Market Geometry Engine

هذا الملف مسؤول عن فهم حركة السوق
وليس مجرد حساب مؤشرات.

Author: Mustafa Tariq
"""

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# Swing Detection
# ==========================================================

def find_swings(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """
    اكتشاف القمم والقيعان باستخدام نافذة منزلقة.

    Parameters
    ----------
    df : DataFrame
        يجب أن يحتوي على High و Low.

    window : int
        حجم النافذة ويجب أن يكون عدداً فردياً.

    Returns
    -------
    DataFrame
    """

    if window % 2 == 0:
        raise ValueError("window must be an odd number.")

    df = df.copy()

    df["Swing High"] = False
    df["Swing Low"] = False

    half = window // 2

    highs = df["High"].values
    lows = df["Low"].values

    for i in range(half, len(df) - half):

        high_window = highs[i-half:i+half+1]
        low_window = lows[i-half:i+half+1]

        if highs[i] == high_window.max():
            df.iloc[i, df.columns.get_loc("Swing High")] = True

        if lows[i] == low_window.min():
            df.iloc[i, df.columns.get_loc("Swing Low")] = True

    return df


# ==========================================================
# Swing Filter
# ==========================================================

def filter_swings(
    df: pd.DataFrame,
    min_distance: float = 0.007
) -> pd.DataFrame:
    """
    إزالة القمم والقيعان المتقاربة.

    Parameters
    ----------
    min_distance : float

    مثال:

    0.007 = 0.7%
    """

    df = df.copy()

    # --------------------------------------------------
    # HIGHS
    # --------------------------------------------------

    highs = df[df["Swing High"]]

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

            if price > last_price:

                keep[-1] = idx

                last_price = price

    df["Swing High"] = False

    if len(keep):

        df.loc[keep, "Swing High"] = True

    # --------------------------------------------------
    # LOWS
    # --------------------------------------------------

    lows = df[df["Swing Low"]]

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

            if price < last_price:

                keep[-1] = idx

                last_price = price

    df["Swing Low"] = False

    if len(keep):

        df.loc[keep, "Swing Low"] = True

    return df

# ==========================================================
# Build Pivot Table
# ==========================================================

def build_pivots(df: pd.DataFrame) -> pd.DataFrame:
    """
    تحويل القمم والقيعان إلى جدول مرتب زمنياً.

    Returns
    -------
    DataFrame

    الأعمدة:

    Time
    Type
    Price
    """

    pivots = []

    for index, row in df.iterrows():

        if row["Swing High"]:

            pivots.append(
                {
                    "Time": index,
                    "Type": "H",
                    "Price": row["High"]
                }
            )

        if row["Swing Low"]:

            pivots.append(
                {
                    "Time": index,
                    "Type": "L",
                    "Price": row["Low"]
                }
            )

    pivots = pd.DataFrame(pivots)

    if pivots.empty:
        return pivots

    pivots.sort_values(
        "Time",
        inplace=True
    )

    pivots.reset_index(
        drop=True,
        inplace=True
    )

    return pivots


# ==========================================================
# Plot Swings
# ==========================================================

def plot_swings(
    df: pd.DataFrame,
    last: int = 250
):
    """
    رسم السعر مع القمم والقيعان.
    """

    data = df.tail(last)

    plt.figure(figsize=(18,8))

    plt.plot(
        data.index,
        data["Close"],
        linewidth=1.3,
        label="Close"
    )

    highs = data[data["Swing High"]]

    plt.scatter(
        highs.index,
        highs["High"],
        marker="^",
        s=90,
        label="Swing High"
    )

    lows = data[data["Swing Low"]]

    plt.scatter(
        lows.index,
        lows["Low"],
        marker="v",
        s=90,
        label="Swing Low"
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()


# ==========================================================
# Plot ZigZag
# ==========================================================

def plot_zigzag(
    df: pd.DataFrame,
    last: int = 250
):
    """
    رسم ZigZag بين القمم والقيعان.
    """

    data = df.tail(last)

    pivots = build_pivots(data)

    plt.figure(figsize=(18,8))

    plt.plot(
        data.index,
        data["Close"],
        linewidth=1,
        alpha=0.6,
        label="Close"
    )

    if len(pivots) > 1:

        plt.plot(
            pivots["Time"],
            pivots["Price"],
            linewidth=2,
            label="ZigZag"
        )

        highs = pivots[pivots["Type"] == "H"]

        lows = pivots[pivots["Type"] == "L"]

        plt.scatter(
            highs["Time"],
            highs["Price"],
            marker="^",
            s=100,
            label="High"
        )

        plt.scatter(
            lows["Time"],
            lows["Price"],
            marker="v",
            s=100,
            label="Low"
        )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()
    
