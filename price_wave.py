from dataclasses import dataclass
from enum import Enum

from dc_event import DCEvent


class WaveType(Enum):
    IMPULSE = "IMPULSE"
    CORRECTION = "CORRECTION"


class Trend(Enum):
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


@dataclass
class Wave:

    start: DCEvent
    end: DCEvent

    direction: Trend

    wave_type: WaveType = WaveType.IMPULSE

    price_change: float = 0.0
    percent_change: float = 0.0

    candle_count: int = 0

    slope: float = 0.0

    strength: float = 0.0

    valid: bool = True

    parent=None

    children=None

    def __post_init__(self):

        self.price_change = self.end.price - self.start.price

        self.percent_change = abs(
            self.price_change / self.start.price
        ) * 100

        self.candle_count = (
            self.end.index - self.start.index
        )

        if self.candle_count > 0:
            self.slope = (
                self.price_change /
                self.candle_count
            )

        self.children = []
