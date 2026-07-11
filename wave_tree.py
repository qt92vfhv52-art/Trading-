from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from price_wave import Wave


class WaveLevel(Enum):

    MICRO = 0

    MINOR = 1

    INTERMEDIATE = 2

    MAJOR = 3

    PRIMARY = 4

    CYCLE = 5


@dataclass
class WaveNode:

    wave: Wave

    level: WaveLevel

    parent: Optional["WaveNode"] = None

    children: List["WaveNode"] = field(default_factory=list)

    score: float = 0.0

    depth: int = 0

    def add_child(self, child):

        child.parent = self

        child.depth = self.depth + 1

        self.children.append(child)

    @property
    def start(self):

        return self.wave.start_index

    @property
    def end(self):

        return self.wave.end_index

    @property
    def size(self):

        return abs(self.wave.price_change)

    @property
    def duration(self):

        return self.wave.length

    def __repr__(self):

        return (
            f"{self.level.name} "
            f"{self.wave.trend.name} "
            f"{self.size:.2f}"
        )
