"""
=========================================================
candle.py
=========================================================

Author : Mustafa Tariq

يمثل شمعة واحدة داخل السوق.

لا يخزن بيانات OHLC فقط،
بل يحسب الخصائص الهندسية للشمعة.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import math
import pandas as pd


# ==========================================================
# Candle
# ==========================================================

@dataclass
class Candle:

    index: int

    time: pd.Timestamp

    open: float

    high: float

    low: float

    close: float

    volume: float

    atr: float = 0.0

    velocity: float = 0.0

    acceleration: float = 0.0

    # ------------------------------------------------------

    @property
    def body(self) -> float:
        return abs(self.close - self.open)

    # ------------------------------------------------------

    @property
    def range(self) -> float:
        return self.high - self.low

    # ------------------------------------------------------

    @property
    def upper_wick(self) -> float:
        return self.high - max(self.open, self.close)

    # ------------------------------------------------------

    @property
    def lower_wick(self) -> float:
        return min(self.open, self.close) - self.low

    # ------------------------------------------------------

    @property
    def body_percent(self) -> float:

        if self.range == 0:
            return 0.0

        return self.body / self.range

    # ------------------------------------------------------

    @property
    def upper_wick_percent(self) -> float:

        if self.range == 0:
            return 0.0

        return self.upper_wick / self.range

    # ------------------------------------------------------

    @property
    def lower_wick_percent(self) -> float:

        if self.range == 0:
            return 0.0

        return self.lower_wick / self.range

    # ------------------------------------------------------

    @property
    def midpoint(self) -> float:
        return (self.high + self.low) / 2

    # ------------------------------------------------------

    @property
    def typical_price(self) -> float:
        return (
            self.high +
            self.low +
            self.close
        ) / 3

    # ------------------------------------------------------

    @property
    def weighted_price(self) -> float:
        return (
            self.high +
            self.low +
            2 * self.close
        ) / 4

    # ------------------------------------------------------

    @property
    def bullish(self) -> bool:
        return self.close > self.open

    # ------------------------------------------------------

    @property
    def bearish(self) -> bool:
        return self.close < self.open

    # ------------------------------------------------------

    @property
    def doji(self) -> bool:

        if self.range == 0:
            return True

        return self.body_percent < 0.10

    # ------------------------------------------------------

    @property
    def marubozu(self) -> bool:
        return (
            self.body_percent > 0.90
        )

    # ------------------------------------------------------

    @property
    def hammer(self) -> bool:

        return (

            self.lower_wick >

            self.body * 2

            and

            self.upper_wick < self.body

        )

    # ------------------------------------------------------

    @property
    def inverted_hammer(self) -> bool:

        return (

            self.upper_wick >

            self.body * 2

            and

            self.lower_wick < self.body

        )

    # ------------------------------------------------------

    @property
    def energy(self) -> float:
        """
        طاقة تقريبية للشمعة.

        سنطورها لاحقاً.
        """

        return self.range * max(self.volume, 1)

    # ------------------------------------------------------

    @property
    def angle(self) -> float:
        """
        زاوية الجسم.
        """

        if self.body == 0:
            return 0.0

        return math.degrees(

            math.atan(

                self.body

            )

        )

    # ------------------------------------------------------

    def to_dict(self):

        return {

            "Time": self.time,

            "Open": self.open,

            "High": self.high,

            "Low": self.low,

            "Close": self.close,

            "Volume": self.volume,

            "ATR": self.atr,

            "Velocity": self.velocity,

            "Acceleration": self.acceleration,

        }

    # ------------------------------------------------------

    def __repr__(self):

        direction = "Bull" if self.bullish else "Bear"

        return (

            f"Candle("

            f"{self.time}, "

            f"{direction}, "

            f"O={self.open:.2f}, "

            f"H={self.high:.2f}, "

            f"L={self.low:.2f}, "

            f"C={self.close:.2f}"

            f")"

        )
