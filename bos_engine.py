from dc_event import DCType


class BOSEngine:

    def __init__(self, waves):

        self.waves = waves

    def detect(self):

        bos = []

        last_high = None
        last_low = None

        for wave in self.waves:

            # موجة صاعدة
            if wave.direction.name == "UP":

                if last_high is None:

                    last_high = wave.end.price
                    continue

                if wave.end.price > last_high:

                    bos.append(
                        {
                            "type": "Bullish BOS",
                            "index": wave.end.index,
                            "price": wave.end.price,
                            "wave": wave,
                        }
                    )

                    last_high = wave.end.price

            # موجة هابطة
            else:

                if last_low is None:

                    last_low = wave.end.price
                    continue

                if wave.end.price < last_low:

                    bos.append(
                        {
                            "type": "Bearish BOS",
                            "index": wave.end.index,
                            "price": wave.end.price,
                            "wave": wave,
                        }
                    )

                    last_low = wave.end.price

        return bos
      
