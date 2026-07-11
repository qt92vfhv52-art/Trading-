class MarketStructure:

    def __init__(self, waves):

        self.waves = waves

    def _extract_highs(self):

        highs = []

        for wave in self.waves:

            if wave.direction.name == "UP":

                highs.append({
                    "wave": wave,
                    "price": wave.end.price
                })

        return highs

    def _extract_lows(self):

        lows = []

        for wave in self.waves:

            if wave.direction.name == "DOWN":

                lows.append({
                    "wave": wave,
                    "price": wave.end.price
                })

        return lows

    def build(self):

        swings = []

        highs = self._extract_highs()
        lows = self._extract_lows()

        # -------- Swing High --------

        for i in range(1, len(highs) - 1):

            prev = highs[i - 1]
            cur = highs[i]
            nxt = highs[i + 1]

            if (
                cur["price"] > prev["price"]
                and
                cur["price"] > nxt["price"]
            ):

                swings.append({
                    "type": "HIGH",
                    "wave": cur["wave"]
                })

        # -------- Swing Low --------

        for i in range(1, len(lows) - 1):

            prev = lows[i - 1]
            cur = lows[i]
            nxt = lows[i + 1]

            if (
                cur["price"] < prev["price"]
                and
                cur["price"] < nxt["price"]
            ):

                swings.append({
                    "type": "LOW",
                    "wave": cur["wave"]
                })

        swings.sort(
            key=lambda x: x["wave"].end.index
        )

        return swings
