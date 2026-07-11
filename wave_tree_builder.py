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

    # الموجة التي تمثل هذه العقدة
    wave: Wave

    # مستوى العقدة
    level: WaveLevel

    # الأب
    parent: Optional["WaveNode"] = None

    # الأبناء
    children: List["WaveNode"] = field(default_factory=list)

    # درجة القوة
    score: float = 0.0

    # عمق العقدة
    depth: int = 0

    # -------------------------

    @property
    def start(self):

        return self.wave.start.index

    @property
    def end(self):

        return self.wave.end.index

    @property
    def start_price(self):

        return self.wave.start.price

    @property
    def end_price(self):

        return self.wave.end.price

    @property
    def size(self):

        return abs(self.wave.price_change)

    @property
    def duration(self):

        return self.wave.candle_count

    @property
    def direction(self):

        return self.wave.direction

    @property
    def slope(self):

        return self.wave.slope

    @property
    def strength(self):

        return self.wave.strength

    # -------------------------

    def add_child(self, child: "WaveNode"):

        child.parent = self

        child.depth = self.depth + 1

        self.children.append(child)

    # -------------------------

    def is_leaf(self):

        return len(self.children) == 0

    # -------------------------

    def descendants(self):

        nodes = []

        for child in self.children:

            nodes.append(child)

            nodes.extend(child.descendants())

        return nodes

    # -------------------------

    def print_tree(self, indent=0):

        print(
            " " * indent +
            f"{self.level.name} | "
            f"{self.direction.name} | "
            f"{self.size:.2f} | "
            f"Score={self.score:.2f}"
        )

        for child in self.children:

            child.print_tree(indent + 4)

    # -------------------------

    def __repr__(self):

        return (
            f"<WaveNode "
            f"{self.level.name} "
            f"{self.direction.name} "
            f"Size={self.size:.2f} "
            f"Strength={self.strength:.2f}>"
        )
