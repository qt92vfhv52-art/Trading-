"""
=============================================================
Market Geometry Engine
Version : 1.0

Author : Mustafa Tariq

فلسفة المشروع
--------------

لا نعتمد على المؤشرات.

لا نعتمد على Pivot ثابت.

السوق عبارة عن حركة هندسية.

الشموع
    ↓
Movement
    ↓
Legs
    ↓
Pivots
    ↓
Market Structure
    ↓
Trading Signals

=============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

import numpy as np
import pandas as pd


# ============================================================
# CONSTANTS
# ============================================================

ATR_PERIOD = 14

VOLATILITY_PERIOD = 20

RETURN_PERIOD = 1

EPSILON = 1e-9


# ============================================================
# ENUMS
# ============================================================

class Direction(Enum):

    UP = 1

    DOWN = -1

    SIDEWAYS = 0


class Trend(Enum):

    UNKNOWN = 0

    BULLISH = 1

    BEARISH = -1

    RANGE = 2


class PivotType(Enum):

    HIGH = "HIGH"

    LOW = "LOW"


class PivotStrength(Enum):

    WEAK = 0

    NORMAL = 1

    STRONG = 2

    MAJOR = 3


# ============================================================
# PIVOT
# ============================================================

@dataclass

class Pivot:

    index: int

    time: pd.Timestamp

    price: float

    pivot_type: PivotType

    strength: PivotStrength = PivotStrength.NORMAL

    score: float = 0.0

    confirmed: bool = False

    metadata: dict = field(default_factory=dict)


# ============================================================
# LEG
# ============================================================

@dataclass

class Leg:

    start_index: int

    end_index: int

    start_price: float

    end_price: float

    direction: Direction

    bars: int

    length: float

    velocity: float = 0.0

    acceleration: float = 0.0

    angle: float = 0.0


# ============================================================
# ENGINE
# ============================================================

class MarketGeometry:

    def __init__(self, df: pd.DataFrame):

        self.df = df.copy()

        self.pivots: List[Pivot] = []

        self.legs: List[Leg] = []

        self.trend = Trend.UNKNOWN

    def reset(self):

        self.pivots.clear()

        self.legs.clear()

        self.trend = Trend.UNKNOWN


# ============================================================
# TRUE RANGE
# ============================================================

def true_range(df):

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


# ============================================================
# ATR
# ============================================================

def atr(

    df,

    period=ATR_PERIOD,

):

    tr = true_range(df)

    return tr.rolling(period).mean()


# ============================================================
# VOLATILITY
# ============================================================

def volatility(

    df,

    period=VOLATILITY_PERIOD,

):

    returns = df["Close"].pct_change()

    return returns.rolling(period).std()


# ============================================================
# MOMENTUM
# ============================================================

def momentum(df):

    return df["Close"].diff()


# ============================================================
# VELOCITY
# ============================================================

def velocity(df):

    return momentum(df)


# ============================================================
# ACCELERATION
# ============================================================

def acceleration(df):

    return velocity(df).diff()


# ============================================================
# SLOPE
# ============================================================

def slope(series):

    return series.diff()


# ============================================================
# NORMALIZE
# ============================================================

def normalize(series):

    minimum = series.min()

    maximum = series.max()

    if maximum - minimum < EPSILON:

        return pd.Series(

            np.zeros(len(series)),

            index=series.index,

        )

    return (

        series - minimum

    ) / (

        maximum - minimum

    )


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(df):

    data = df.copy()

    data["ATR"] = atr(data)

    data["Volatility"] = volatility(data)

    data["Momentum"] = momentum(data)

    data["Velocity"] = velocity(data)

    data["Acceleration"] = acceleration(data)

    data["Return"] = data["Close"].pct_change()

    data["Normalized ATR"] = normalize(

        data["ATR"].fillna(0)

    )

    data["Normalized Volatility"] = normalize(

        data["Volatility"].fillna(0)

    )

    return data


# ============================================================
# VALIDATE DATA
# ============================================================

def validate_data(df):

    required = [

        "Open",

        "High",

        "Low",

        "Close",

        "Volume",

    ]

    for column in required:

        if column not in df.columns:

            raise ValueError(

                f"Missing column: {column}"

            )

    if len(df) < 50:

        raise ValueError(

            "Dataset is too small."

        )

    return True
    
