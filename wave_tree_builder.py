from typing import List

from wave_tree import WaveNode, WaveLevel


class WaveTreeBuilder:

    def __init__(self, waves):

        self.waves = waves

    def build(self):

        if len(self.waves) == 0:

            return []

        # إنشاء المستوى الأول (MICRO)

        nodes = []

        for wave in self.waves:

            node = WaveNode(

                wave=wave,

                level=WaveLevel.MICRO,

            )

            node.score = self.score_wave(wave)

            nodes.append(node)

        current = nodes

        level = WaveLevel.MINOR

        # دمج الموجات تدريجياً حتى يبقى جذر واحد

        while len(current) > 1:

            current = self.merge_level(

                current,

                level,

            )

            if level != WaveLevel.CYCLE:

                level = WaveLevel(level.value + 1)

            else:

                break

        return current

    def score_wave(self, wave):

        score = 0.0

        score += abs(wave.price_change) * 0.55

        score += wave.length * 6

        score += wave.velocity * 0.35

        return score
      
    def merge_level(

        self,

        nodes,

        new_level,

    ):

        if len(nodes) <= 1:

            return nodes

        merged = []

        i = 0

        while i < len(nodes):

            # إذا بقي عنصر واحد

            if i == len(nodes) - 1:

                nodes[i].level = new_level

                merged.append(nodes[i])

                break

            left = nodes[i]

            right = nodes[i + 1]

            # اختيار الموجة الأقوى كالأب

            if left.score >= right.score:

                parent = left

                child = right

            else:

                parent = right

                child = left

            parent.level = new_level

            parent.add_child(child)

            parent.score += child.score * 0.45

            merged.append(parent)

            i += 2

        return merged
      
