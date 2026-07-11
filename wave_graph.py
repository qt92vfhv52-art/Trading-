from dataclasses import dataclass, field
from enum import Enum

from price_wave import Wave


class EdgeType(Enum):

    NEXT = "NEXT"

    PREVIOUS = "PREVIOUS"

    OVERLAP = "OVERLAP"

    CONTAIN = "CONTAIN"


@dataclass
class WaveEdge:

    source: int

    target: int

    relation: EdgeType

    weight: float = 1.0


@dataclass
class WaveGraph:

    waves: list[Wave]

    edges: list[WaveEdge] = field(default_factory=list)

    def build(self):

        self.edges.clear()

        self.build_next_edges()

        self.build_overlap_edges()

        self.build_containment_edges()

        return self

    # ----------------------------------------------------

    def build_next_edges(self):

        for i in range(len(self.waves) - 1):

            self.edges.append(

                WaveEdge(

                    source=i,

                    target=i + 1,

                    relation=EdgeType.NEXT,

                )

            )

            self.edges.append(

                WaveEdge(

                    source=i + 1,

                    target=i,

                    relation=EdgeType.PREVIOUS,

                )

            )

    # ----------------------------------------------------

    def build_overlap_edges(self):

        n = len(self.waves)

        for i in range(n):

            a = self.waves[i]

            for j in range(i + 1, n):

                b = self.waves[j]

                if (

                    a.start.index <= b.end.index

                    and

                    b.start.index <= a.end.index

                ):

                    self.edges.append(

                        WaveEdge(

                            source=i,

                            target=j,

                            relation=EdgeType.OVERLAP,

                        )

                    )

    # ----------------------------------------------------

    def build_containment_edges(self):

        n = len(self.waves)

        for i in range(n):

            a = self.waves[i]

            for j in range(n):

                if i == j:

                    continue

                b = self.waves[j]

                if (

                    a.start.index <= b.start.index

                    and

                    a.end.index >= b.end.index

                ):

                    self.edges.append(

                        WaveEdge(

                            source=i,

                            target=j,

                            relation=EdgeType.CONTAIN,

                        )

                    )

    # ----------------------------------------------------

    def neighbors(self, index, relation=None):

        result = []

        for edge in self.edges:

            if edge.source != index:

                continue

            if relation is not None:

                if edge.relation != relation:

                    continue

            result.append(edge.target)

        return result

    # ----------------------------------------------------

    def print_graph(self):

        print("=" * 60)

        print("GRAPH")

        print("=" * 60)

        for edge in self.edges:

            print(

                f"{edge.source} "

                f"-- {edge.relation.name} --> "

                f"{edge.target}"

            )
