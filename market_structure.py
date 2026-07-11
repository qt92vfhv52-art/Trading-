from wave_degree import WaveDegree


class MarketStructure:

    def __init__(self, roots):

        self.roots = roots

    def _collect(self, node, degree, out):

        if node.degree == degree:
            out.append(node)

        for child in node.children:
            self._collect(child, degree, out)

    def get_degree_waves(self, degree):

        waves = []

        for root in self.roots:
            self._collect(root, degree, waves)

        waves.sort(
            key=lambda w: w.start.index
        )

        return waves

    def build(self, degree):

        waves = self.get_degree_waves(degree)

        swings = []

        highs = [
            w for w in waves
            if w.direction.name == "UP"
        ]

        lows = [
            w for w in waves
            if w.direction.name == "DOWN"
        ]

        for i in range(1, len(highs) - 1):

            if (
                highs[i].end.price > highs[i - 1].end.price
                and
                highs[i].end.price > highs[i + 1].end.price
            ):

                swings.append({
                    "type": "HIGH",
                    "wave": highs[i]
                })

        for i in range(1, len(lows) - 1):

            if (
                lows[i].end.price < lows[i - 1].end.price
                and
                lows[i].end.price < lows[i + 1].end.price
            ):

                swings.append({
                    "type": "LOW",
                    "wave": lows[i]
                })

        swings.sort(
            key=lambda s: s["wave"].end.index
        )

        return swings
