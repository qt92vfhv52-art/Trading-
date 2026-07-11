from wave_graph import WaveGraph


class ContainmentEngine:

    def __init__(self, graph: WaveGraph):

        self.graph = graph

    def build(self):

        vertices = self.graph.all_vertices()

        for parent in vertices:

            for child in vertices:

                if parent.id == child.id:
                    continue

                if self.contains(parent, child):

                    self.graph.add_relation(

                        parent.id,

                        child.id,

                        "CONTAINS",

                        self.weight(parent, child),

                    )

        return self.graph

    def contains(self, parent, child):

        if parent.wave.candle_count <= child.wave.candle_count:
            return False

        start_ok = (
            parent.wave.start.index
            <=
            child.wave.start.index
        )

        end_ok = (
            parent.wave.end.index
            >=
            child.wave.end.index
        )

        return start_ok and end_ok

    def weight(self, parent, child):

        duration = (
            child.wave.candle_count
            /
            parent.wave.candle_count
        )

        movement = (
            abs(child.wave.price_change)
            /
            abs(parent.wave.price_change)
        )

        return (duration + movement) / 2
