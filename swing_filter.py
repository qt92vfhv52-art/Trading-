from copy import deepcopy

from dc_event import DCType


class SwingFilter:

    def __init__(
        self,
        events,
        merge_distance=0.007,
    ):

        self.events = deepcopy(events)

        self.merge_distance = merge_distance

    def filter(self):

        events = self.events

        changed = True

        while changed:

            changed = False

            result = []

            i = 0

            while i < len(events):

                if i >= len(events) - 2:

                    result.extend(events[i:])
                    break

                a = events[i]
                b = events[i + 1]
                c = events[i + 2]

                # High - Low - High

                if (
                    a.event_type == DCType.HIGH
                    and b.event_type == DCType.LOW
                    and c.event_type == DCType.HIGH
                ):

                    distance = abs(a.price - c.price) / max(a.price, c.price)

                    if distance < self.merge_distance:

                        if a.price >= c.price:

                            result.append(a)

                        else:

                            result.append(c)

                        i += 3
                        changed = True
                        continue

                # Low - High - Low

                if (
                    a.event_type == DCType.LOW
                    and b.event_type == DCType.HIGH
                    and c.event_type == DCType.LOW
                ):

                    distance = abs(a.price - c.price) / max(a.price, c.price)

                    if distance < self.merge_distance:

                        if a.price <= c.price:

                            result.append(a)

                        else:

                            result.append(c)

                        i += 3
                        changed = True
                        continue

                result.append(a)

                i += 1

            events = result

        return events


    def score_events(self, events):

        scores = []

        for i, event in enumerate(events):

            score = 0.0

            # ========= حركة السعر =========

            if i > 0:

                previous = events[i - 1]

                move = abs(event.price - previous.price)

                score += move * 0.45

            # ========= الزمن =========

            if i > 0:

                candles = event.index - previous.index

                score += candles * 4.0

            # ========= Threshold =========

            score += event.threshold * 10000 * 0.25

            # ========= Overshoot =========

            score += event.overshoot * 150

            scores.append(score)

        return scores


    def remove_weak(self, events, scores, minimum_score=250):

        result = []

        for event, score in zip(events, scores):

            if score >= minimum_score:

                result.append(event)

        return result


    def process(self):

        filtered = self.filter()

        scores = self.score_events(filtered)

        filtered = self.remove_weak(

            filtered,

            scores,

            minimum_score=250,

        )

        return filtered
      
