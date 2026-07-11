class MarketStructure:

    def __init__(self, waves):

        self.waves = waves

    def build(self):

        swings = []

        for i in range(1, len(self.waves) - 1):

            prev = self.waves[i - 1]
            cur = self.waves[i]
            nxt = self.waves[i + 1]

            if cur.direction.name == "UP":

                if (
                    cur.end.price > prev.end.price
                    and
                    cur.end.price > nxt.end.price
                ):

                    swings.append({
                        "type": "HIGH",
                        "wave": cur
                    })

            else:

                if (
                    cur.end.price < prev.end.price
                    and
                    cur.end.price < nxt.end.price
                ):

                    swings.append({
                        "type": "LOW",
                        "wave": cur
                    })

        return swings
