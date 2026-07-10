"""
data.py
========
تحميل بيانات الشموع من Binance باستخدام CCXT.

Author: Mustafa Tariq
"""

import ccxt
import pandas as pd


exchange = ccxt.binance({
    "enableRateLimit": True
})


def load_data(
    symbol="BTC/USDT",
    timeframe="1h",
    limit=1000
):
    """
    تحميل بيانات OHLCV من Binance.

    Parameters
    ----------
    symbol : str
        مثال: BTC/USDT

    timeframe : str
        مثال: 1m, 5m, 15m, 1h, 4h, 1d

    limit : int
        عدد الشموع

    Returns
    -------
    pandas.DataFrame
    """

    ohlcv = exchange.fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit
    )

    df = pd.DataFrame(
        ohlcv,
        columns=[
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    )

    df["Date"] = pd.to_datetime(
        df["Date"],
        unit="ms"
    )

    df.set_index("Date", inplace=True)

    return df
