from util import mapl
from collections import defaultdict


def maybe_int(val):
    try:
        return int(val)
    except Exception:
        return None


class Map:
    def __init__(self, map_str):
        self.grid = [mapl(maybe_int, line) for line in map_str.strip().splitlines()]

        self.positions_by_value = defaultdict(lambda: set())
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                self.positions_by_value[val].add((x, y))

    def __getitem__(self, pos):
        x, y = pos
        return self.grid[y][x]

    def __contains__(self, pos):
        x, y = pos
        return (0 <= y < len(self.grid)) and (0 <= x < len(self.grid[y]))

    def neighbours(self, pos):
        x, y = pos
        return [
            p
            for p in (
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            )
            if p in self
        ]

    def __str__(self):
        return "\n".join(str(l) for l in self.grid)

    def map_reachability(self):
        """
        Calculates which positions in the grid can reach
        which destinations.

        position -> [destination positions]
        """
        pos_by_val = self.positions_by_value
        reachability = defaultdict(lambda: set())

        for nine in pos_by_val[9]:
            reachability[nine] = {nine}

        for n in range(9, -1, -1):
            for pos in pos_by_val[n]:
                smaller = pos_by_val[n - 1]
                for neighbour in self.neighbours(pos):
                    if neighbour in smaller:
                        reachability[neighbour].update(reachability[pos])

        return reachability

    def trailheads_and_dests(self):
        reachability = self.map_reachability()
        zeros = self.positions_by_value[0]
        return {zero: reachability[zero] for zero in zeros}

    def sum_of_scores(self):
        trailheads = self.trailheads_and_dests()
        return sum(len(dests) for dests in trailheads.values())

    def trails_from(self, pos):
        count = 0
        val = self[pos]
        for n in self.neighbours(pos):
            nval = self[n]
            if nval != val + 1:
                continue
            if nval == 9:
                count += 1
            else:
                count += self.trails_from(n)
        return count

    def sum_of_trailhead_ratings(self):
        trailheads = self.positions_by_value[0]
        return sum(self.trails_from(t) for t in trailheads)
