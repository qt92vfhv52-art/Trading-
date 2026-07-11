from typing import List

from candle import Candle
from dc_event import DCEvent, DCType


class ADCEngine:

    def __init__(self, candles: List[Candle], threshold=0.01):

        self.candles = candles

        self.threshold = threshold

    def detect(self):

        if len(self.candles) == 0:

            return []

        events = []

        mode = None

        extreme_price = self.candles[0].close

        extreme_index = 0

        for i, candle in enumerate(self.candles[1:], 1):

            price = candle.close

            # أول اتجاه
            if mode is None:

                if price >= extreme_price * (1 + self.threshold):

                    mode = "UP"

                    extreme_price = price

                    extreme_index = i

                elif price <= extreme_price * (1 - self.threshold):

                    mode = "DOWN"

                    extreme_price = price

                    extreme_index = i

                continue

            # اتجاه صاعد
            if mode == "UP":

                if price > extreme_price:

                    extreme_price = price

                    extreme_index = i

                elif price <= extreme_price * (1 - self.threshold):

                    events.append(

                        DCEvent(

                            index=extreme_index,

                            price=extreme_price,

                            threshold=self.threshold,

                            event_type=DCType.HIGH,

                        )

                    )

                    mode = "DOWN"

                    extreme_price = price

                    extreme_index = i

            # اتجاه هابط
            else:

                if price < extreme_price:

                    extreme_price = price

                    extreme_index = i

                elif price >= extreme_price * (1 + self.threshold):

                    events.append(

                        DCEvent(

                            index=extreme_index,

                            price=extreme_price,

                            threshold=self.threshold,

                            event_type=DCType.LOW,

                        )

                    )

                    mode = "UP"

                    extreme_price = price

                    extreme_index = i

        return events

import matplotlib.pyplot as plt


def plot_events(df, events):

    plt.figure(figsize=(18,7))

    plt.plot(df.index, df["Close"], linewidth=1)

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
        label="DC High",
    )

    plt.scatter(
        lows_x,
        lows_y,
        marker="v",
        s=80,
        label="DC Low",
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()
