import numpy as np


class VolatilityEngine:

    def __init__(self, candles, period=14):
        self.candles = candles
        self.period = period

    def atr(self):

        trs = []

        for i in range(len(self.candles)):

            c = self.candles[i]

            if i == 0:
                trs.append(c.high - c.low)
                continue

            p = self.candles[i - 1]

            tr = max(
                c.high - c.low,
                abs(c.high - p.close),
                abs(c.low - p.close),
            )

            trs.append(tr)

        atr = []

        for i in range(len(trs)):

            start = max(0, i - self.period + 1)

            atr.append(np.mean(trs[start:i + 1]))

        return atr

    def adaptive_threshold(self):

        atr = self.atr()

        thresholds = []

        for i, value in enumerate(atr):

            price = self.candles[i].close

            thresholds.append(value / price)

        return thresholds
