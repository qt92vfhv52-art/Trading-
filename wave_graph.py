from dataclasses import dataclass, field
from typing import List, Dict

from price_wave import Wave


@dataclass
class WaveVertex:

    id: int

    wave: Wave

    parents: List[int] = field(default_factory=list)

    children: List[int] = field(default_factory=list)

    score: float = 0.0

    level: int = 0


@dataclass
class WaveEdge:

    source: int

    target: int

    relation: str

    weight: float = 1.0


class WaveGraph:

    def __init__(self):

        self.vertices: Dict[int, WaveVertex] = {}

        self.edges: List[WaveEdge] = []

    # -----------------------------

    def add_wave(self, wave):

        idx = len(self.vertices)

        self.vertices[idx] = WaveVertex(

            id=idx,

            wave=wave,

        )

        return idx

    # -----------------------------

    def add_relation(

        self,

        source,

        target,

        relation,

        weight=1.0,

    ):

        self.edges.append(

            WaveEdge(

                source,

                target,

                relation,

                weight,

            )

        )

        self.vertices[source].children.append(target)

        self.vertices[target].parents.append(source)

    # -----------------------------

    def get(self, idx):

        return self.vertices[idx]

    # -----------------------------

    def all_vertices(self):

        return list(self.vertices.values())

    # -----------------------------

    def all_edges(self):

        return self.edges

    # -----------------------------

    def print_graph(self):

        print("=" * 60)

        print("VERTICES")

        print("=" * 60)

        for vertex in self.vertices.values():

            wave = vertex.wave

            print(

                f"[{vertex.id}] "

                f"{wave.direction.name} "

                f"{wave.start.index}->{wave.end.index} "

                f"{wave.start.price:.2f}->{wave.end.price:.2f}"

            )

        print()

        print("=" * 60)

        print("EDGES")

        print("=" * 60)

        for edge in self.edges:

            print(

                edge.source,

                "--",

                edge.relation,

                "-->",

                edge.target,

                f"(w={edge.weight:.2f})"

            )
