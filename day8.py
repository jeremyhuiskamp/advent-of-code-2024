from collections import defaultdict
from itertools import chain, takewhile, count


class City:
    def __init__(self, freqs, bounds, repeating_antinodes):
        self.freqs = freqs
        self.bounds = bounds
        self.repeating_antinodes = repeating_antinodes

    def is_in_bounds(self, p):
        x, y = p
        maxx, maxy = self.bounds
        return 0 <= x <= maxx and 0 <= y <= maxy

    @property
    def _multipliers(self):
        if self.repeating_antinodes:
            return count()
        return (1,)

    def _one_dir_antinodes(self, a, b):
        xa, ya = a
        xb, yb = b
        delta_x = xa - xb
        delta_y = ya - yb
        candidates = ((m * delta_x + xa, m * delta_y + ya) for m in self._multipliers)
        return takewhile(self.is_in_bounds, candidates)

    def antinodes(self, a, b):
        n1 = set(self._one_dir_antinodes(a, b))
        n2 = set(self._one_dir_antinodes(b, a))
        return n1 | n2

    def pairs(self, nodes):
        nodes = nodes.copy()
        while nodes:
            n = nodes.pop()
            for other in nodes:
                yield n, other

    def antinodes_for_freq(self, freq):
        freqs = self.freqs[freq]  # set[xy]
        ps = self.pairs(freqs)  # seq[frozenset[xy]]
        return set(chain.from_iterable(self.antinodes(p[0], p[1]) for p in ps))

    def all_antinodes(self):
        ret = set()
        for freq in self.freqs:
            ret |= self.antinodes_for_freq(freq)
        return ret

    @staticmethod
    def from_input(inp, repeating_antinodes=False):
        freqs = defaultdict(set)
        bounds = 0, 0
        for rownum, row in enumerate(inp.splitlines()):
            for colnum, c in enumerate(row):
                if c.isalnum():
                    freqs[c].add((colnum, rownum))
                bounds = colnum, rownum

        return City(dict(freqs), bounds, repeating_antinodes)
