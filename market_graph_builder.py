from wave_graph import WaveGraph


class MarketGraphBuilder:

    def __init__(self, waves):

        self.waves = waves

    def build(self):

        graph = WaveGraph()

        ids = []

        for wave in self.waves:

            ids.append(graph.add_wave(wave))

        # ربط كل موجة بالتي بعدها
        for i in range(len(ids) - 1):

            graph.add_relation(

                ids[i],

                ids[i + 1],

                "NEXT",

                1.0,

            )

        return graph
