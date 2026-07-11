from dataclasses import dataclass
from typing import List

from dc_event import DCEvent, DCType
@dataclass
class Swing:

    event: DCEvent

    strength: float

    left_distance: int

    right_distance: int

    price_move: float

    major: bool = False
  
  class SwingStrengthEngine:

    def __init__(self, events: List[DCEvent]):

        self.events = events

        def calculate(self):

        swings = []

        n = len(self.events)

        for i, event in enumerate(self.events):

            left = 0
            right = 0

            if i > 0:
                left = event.index - self.events[i - 1].index

            if i < n - 1:
                right = self.events[i + 1].index - event.index

            move = 0.0

            if i > 0:
                move = abs(event.price - self.events[i - 1].price)

            strength = (
                left * 0.35 +
                right * 0.35 +
                move * 0.0003
            )

            swings.append(
                Swing(
                    event=event,
                    strength=strength,
                    left_distance=left,
                    right_distance=right,
                    price_move=move,
                )
            )

        return swings
      
