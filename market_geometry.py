"""
market_geometry.py
==================

Market Geometry Engine

يقوم بتحويل بيانات OHLC
إلى هيكل هندسي للسوق.

Author: Mustafa Tariq
"""

import pandas as pd

def get_swings(df):

    highs = df[df["Swing High"]].copy()

    lows = df[df["Swing Low"]].copy()

    return highs, lows

def build_pivots(df):
    """
    دمج القمم والقيعان
    داخل DataFrame واحد.
    """

    pivots = []

    for index, row in df.iterrows():

        if row["Swing High"]:

            pivots.append({
                "Time": index,
                "Type": "H",
                "Price": row["High"]
            })

        if row["Swing Low"]:

            pivots.append({
                "Time": index,
                "Type": "L",
                "Price": row["Low"]
            })

    pivots = pd.DataFrame(pivots)

    pivots.sort_values("Time", inplace=True)

    pivots.reset_index(drop=True, inplace=True)

    return pivots
