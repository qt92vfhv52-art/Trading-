from wave_tree import WaveNode, WaveLevel


class WaveTreeBuilder:

    def __init__(self, waves):

        self.waves = waves

    # =====================================================

    def build(self):

        if len(self.waves) == 0:
            return []

        nodes = []

        # إنشاء عقد MICRO

        for wave in self.waves:

            node = WaveNode(

                wave=wave,

                level=WaveLevel.MICRO,

            )

            node.score = self.score_wave(wave)

            nodes.append(node)

        current_nodes = nodes

        levels = [

            WaveLevel.MINOR,

            WaveLevel.INTERMEDIATE,

            WaveLevel.MAJOR,

            WaveLevel.PRIMARY,

            WaveLevel.CYCLE,

        ]

        for level in levels:

            if len(current_nodes) <= 1:
                break

            current_nodes = self.merge_level(

                current_nodes,

                level,

            )

        return current_nodes

    # =====================================================

    def score_wave(self, wave):

        score = 0.0

        # قوة الحركة

        score += abs(wave.price_change) * 0.40

        # نسبة الحركة

        score += wave.percent_change * 120

        # الزمن

        score += wave.candle_count * 5

        # الميل

        score += abs(wave.slope) * 0.30

        # القوة المحسوبة سابقاً

        score += wave.strength

        return score

    # =====================================================

    def merge_level(

        self,

        nodes,

        new_level,

    ):

        merged = []

        i = 0

        while i < len(nodes):

            if i == len(nodes) - 1:

                nodes[i].level = new_level

                merged.append(nodes[i])

                break

            left = nodes[i]

            right = nodes[i + 1]

            # اختيار الأقوى

            if left.score >= right.score:

                parent = left

                child = right

            else:

                parent = right

                child = left

            parent.level = new_level

            parent.add_child(child)

            parent.score += child.score * 0.5

            merged.append(parent)

            i += 2

        return merged

    # =====================================================

    def print_tree(self, nodes):

        for node in nodes:

            node.print_tree()

    # =====================================================

    def flatten(self, nodes):

        result = []

        for node in nodes:

            result.append(node)

            result.extend(

                self.flatten(node.children)

            )

        return result

    # =====================================================

    def statistics(self, nodes):

        all_nodes = self.flatten(nodes)

        stats = {}

        for level in WaveLevel:

            stats[level.name] = 0

        for node in all_nodes:

            stats[node.level.name] += 1

        return stats
