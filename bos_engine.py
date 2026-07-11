class BOSEngine:

    def __init__(self, waves, min_percent=2.0):

        self.waves = waves
        self.min_percent = min_percent

    def detect(self):

        bos = []

        last_bull = None
        last_bear = None

        for wave in self.waves:

            move = abs(wave.percent_change)

            if move < self.min_percent:
                continue

            # اتجاه صاعد
            if wave.direction.name == "UP":

                if last_bull is None:

                    last_bull = wave
                    continue

                if wave.end.price > last_bull.end.price:

                    bos.append({
                        "type": "Bullish BOS",
                        "wave": wave,
                        "price": wave.end.price,
                        "index": wave.end.index,
                        "strength": move,
                    })

                    last_bull = wave

            # اتجاه هابط
            else:

                if last_bear is None:

                    last_bear = wave
                    continue

                if wave.end.price < last_bear.end.price:

                    bos.append({
                        "type": "Bearish BOS",
                        "wave": wave,
                        "price": wave.end.price,
                        "index": wave.end.index,
                        "strength": move,
                    })

                    last_bear = wave

        return bos
