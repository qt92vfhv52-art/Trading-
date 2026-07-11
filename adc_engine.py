from typing import List

import matplotlib.pyplot as plt

from candle import Candle
from dc_event import DCEvent, DCType
from volatility_engine import VolatilityEngine


class ADCEngine:

    def __init__(
        self,
        candles: List[Candle],
        threshold: float = 0.01,
        adaptive: bool = True,
    ):

        self.candles = candles
        self.threshold = threshold
        self.adaptive = adaptive

        if adaptive:
            self.thresholds = VolatilityEngine(
                candles
            ).adaptive_threshold()
        else:
            self.thresholds = [threshold] * len(candles)

    def detect(self):

        if len(self.candles) == 0:
            return []

        events = []

        mode = None

        extreme_price = self.candles[0].close
        extreme_index = 0

        for i, candle in enumerate(self.candles[1:], 1):

            price = candle.close

            current_threshold = self.thresholds[i]

            # تحديد أول اتجاه

            if mode is None:

                if price >= extreme_price * (1 + current_threshold):

                    mode = "UP"
                    extreme_price = price
                    extreme_index = i

                elif price <= extreme_price * (1 - current_threshold):

                    mode = "DOWN"
                    extreme_price = price
                    extreme_index = i

                continue

            # الاتجاه الصاعد

            if mode == "UP":

                if price > extreme_price:

                    extreme_price = price
                    extreme_index = i

                elif price <= extreme_price * (1 - current_threshold):

                    events.append(

                        DCEvent(

                            index=extreme_index,
                            price=extreme_price,
                            threshold=current_threshold,
                            event_type=DCType.HIGH,

                        )

                    )

                    mode = "DOWN"
                    extreme_price = price
                    extreme_index = i

            # الاتجاه الهابط

            else:

                if price < extreme_price:

                    extreme_price = price
                    extreme_index = i

                elif price >= extreme_price * (1 + current_threshold):

                    events.append(

                        DCEvent(

                            index=extreme_index,
                            price=extreme_price,
                            threshold=current_threshold,
                            event_type=DCType.LOW,

                        )

                    )

                    mode = "UP"
                    extreme_price = price
                    extreme_index = i

        return events


def plot_events(df, events):

    plt.figure(figsize=(18, 7))

    plt.plot(
        df.index,
        df["Close"],
        linewidth=1,
        color="black",
        alpha=0.7,
    )

    highs_x = []
    highs_y = []

    lows_x = []
    lows_y = []

    for event in events:

        if event.event_type == DCType.HIGH:

            highs_x.append(df.index[event.index])
            highs_y.append(event.price)

        else:

            lows_x.append(df.index[event.index])
            lows_y.append(event.price)

    plt.scatter(
        highs_x,
        highs_y,
        marker="^",
        s=80,
        color="red",
        label="DC High",
        zorder=3,
    )

    plt.scatter(
        lows_x,
        lows_y,
        marker="v",
        s=80,
        color="green",
        label="DC Low",
        zorder=3,
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()
