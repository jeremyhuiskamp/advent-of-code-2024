from queue import Queue
from collections.abc import Iterable
from collections import defaultdict


class Plot(tuple):
    def __new__(self, x, y):
        return tuple.__new__(Plot, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def neighbours(self):
        return (
            Plot(self.x + 1, self.y),
            Plot(self.x, self.y + 1),
            Plot(self.x - 1, self.y),
            Plot(self.x, self.y - 1),
        )


class Region(frozenset[Plot]):
    def fencing_price(self, discount):
        multiplier = self.count_edges() if discount else self.perimeter()
        return multiplier * len(self)

    def perimeter(self):
        ret = 0
        for plot in self:
            ret += sum(1 for n in plot.neighbours if n not in self)
        return ret

    def count_edges(self) -> int:
        """
        Examine every horizontal and vertical line between plots that
        may touch the region.
        """
        minx = min(self, key=lambda p: p.x).x
        miny = min(self, key=lambda p: p.y).y
        maxx = max(self, key=lambda p: p.x).x
        maxy = max(self, key=lambda p: p.y).y

        vertical_edges = 0
        for x in range(minx - 1, maxx + 1):
            boundaries = []
            for y in range(miny - 1, maxy + 1):
                left = Plot(x, y) in self
                right = Plot(x + 1, y) in self
                boundaries.append((left, right))
            vertical_edges += distinct_edges(boundaries)

        horizontal_edges = 0
        for y in range(miny - 1, maxy + 1):
            boundaries = []
            for x in range(minx - 1, maxx + 1):
                top = Plot(x, y) in self
                bottom = Plot(x, y + 1) in self
                boundaries.append((top, bottom))
            horizontal_edges += distinct_edges(boundaries)

        return vertical_edges + horizontal_edges

    def segment(self):
        """
        Break a set of plots up into continuous regions.
        Useful only during initial parsing when we've grouped
        plots by label but haven't yet figure out which areas
        are contiguous.
        """
        plots = set(self.copy())
        while plots:
            q = Queue[Plot]()
            q.put(plots.pop())
            region = set()
            while not q.empty():
                p = q.get()
                region.add(p)
                for n in p.neighbours:
                    if n in plots:
                        plots.remove(n)
                        q.put(n)
            yield Region(frozenset(region))


class Regions(set[Region]):
    def containing(self, plot) -> Region:
        try:
            return next(filter(lambda r: plot in r, self))
        except StopIteration:
            raise ValueError(f"unknown {plot=}")

    @staticmethod
    def _segment(plots_by_label):
        for p in plots_by_label.values():
            yield from Region(p).segment()

    @staticmethod
    def parse(inp) -> "Regions":
        plots_by_label = defaultdict(lambda: set())
        for y, line in enumerate(inp.strip().splitlines()):
            for x, label in enumerate(line):
                plots_by_label[label].add(Plot(x, y))

        return Regions(Regions._segment(plots_by_label))

    def fencing_price(self, *, discount=False):
        return sum(r.fencing_price(discount=discount) for r in self)


def distinct_edges(boundaries: Iterable[tuple[bool, bool]]) -> int:
    """
    A boundary is two plots adjacent to each other that are either
    in a region or out of it.

    An edge is a run of consecutive boundaries that are the same.
    """
    edges = 0
    prev, cur = None, None
    for b in boundaries:
        prev, cur = cur, b
        if prev != cur and cur[0] ^ cur[1]:
            edges += 1
    return edges
