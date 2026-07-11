from typing import List

from dc_event import DCType
from wave import Wave, Trend


class WaveEngine:

    def __init__(self, events):

        self.events = events

        self.waves: List[Wave] = []

    # =====================================================

    def build(self):

        self.waves.clear()

        if len(self.events) < 2:
            return []

        for i in range(len(self.events) - 1):

            start = self.events[i]
            end = self.events[i + 1]

            # LOW → HIGH
            if (
                start.event_type == DCType.LOW
                and
                end.event_type == DCType.HIGH
            ):

                direction = Trend.UP

            # HIGH → LOW
            elif (
                start.event_type == DCType.HIGH
                and
                end.event_type == DCType.LOW
            ):

                direction = Trend.DOWN

            else:
                continue

            wave = Wave(
                start=start,
                end=end,
                direction=direction
            )

            self.waves.append(wave)

        self._calculate_strength()

        return self.waves

    # =====================================================

    def _calculate_strength(self):

        for wave in self.waves:

            length = abs(wave.price_change)

            duration = max(
                wave.candle_count,
                1
            )

            speed = length / duration

            score = (
                length * 0.45 +
                duration * 0.20 +
                speed * 0.35
            )

            wave.strength = score

    # =====================================================

    def strongest(self, n=10):

        return sorted(

            self.waves,

            key=lambda w: w.strength,

            reverse=True

        )[:n]
      import matplotlib.pyplot as plt


def plot_waves(df, waves):

    plt.figure(figsize=(18,7))

    plt.plot(df.index, df["Close"])

    for wave in waves:

        x = [
            df.index[wave.start.index],
            df.index[wave.end.index]
        ]

        y = [
            wave.start.price,
            wave.end.price
        ]

        if wave.direction == Trend.UP:

            color = "green"

        else:

            color = "red"

        plt.plot(
            x,
            y,
            linewidth=2,
            color=color
        )

    plt.grid(True)

    plt.tight_layout()

    plt.show()
