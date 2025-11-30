from enum import IntEnum
from collections import defaultdict

class Dir(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

    def turn_right(self):
        return Dir((self+1) % 4)

    def move_from(self, pos):
        match self:
            case Dir.Up:
                return Pos(pos.x, pos.y-1)
            case Dir.Right:
                return Pos(pos.x+1, pos.y)
            case Dir.Down:
                return Pos(pos.x, pos.y+1)
            case Dir.Left:
                return Pos(pos.x-1, pos.y)

    def to_char(self):
        return {Dir.Up: '^',
                Dir.Right: '>',
                Dir.Down: 'v',
                Dir.Left: '<'}[self]

    @staticmethod
    def of_char(c):
        return {'^': Dir.Up,
                '>': Dir.Right,
                'v': Dir.Down,
                '<': Dir.Left}[c]

class Pos(tuple):
    def __new__(self, x, y):
        return tuple.__new__(Pos, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def move(self, dir):
        return Pos(dir.move_from(self))

    def within(self, lab_map):
        return (0 <= self.x < lab_map.cols and
                0 <= self.y < lab_map.rows)


class LabMap:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.obstructions = set()
        self.guard_pos = None
        self.guard_dir = None
        self.visited = set()
        # (guard_pos, guard_dir) -> times visisted
        self.visited_with_dir = defaultdict(lambda: 0)

    def count_visited(self):
        return len(self.visited)

    def _visit_cur(self):
        self.visited.add(self.guard_pos)
        self.visited_with_dir[(self.guard_pos, self.guard_dir)] += 1

    def guard_on_map(self):
        return self.guard_pos.within(self)

    def guard_in_loop(self):
        return self.visited_with_dir[(self.guard_pos, self.guard_dir)] > 1

    def _next_pos(self):
        return self.guard_dir.move_from(self.guard_pos)

    def move_guard(self):
        next_pos = self._next_pos()
        if next_pos in self.obstructions:
            self.guard_dir = self.guard_dir.turn_right()
        else:
            self.guard_pos = next_pos
        if self.guard_on_map():
            self._visit_cur()

    def move_guard_while_possible(self):
        while self.guard_on_map() and not self.guard_in_loop():
            self.move_guard()

    def copy(self):
        lab_map = LabMap()
        lab_map.rows = self.rows
        lab_map.cols = self.cols
        lab_map.obstructions = self.obstructions.copy()
        lab_map.guard_pos = self.guard_pos
        lab_map.guard_dir = self.guard_dir
        lab_map.visited = self.visited.copy()
        return lab_map

    def obstructable_positions(self):
        guard_done = self.copy()
        guard_done.move_guard_while_possible()
        assert not guard_done.guard_on_map()
        assert not guard_done.guard_in_loop()

        return guard_done.visited - {self.guard_pos}

    def with_additional_obstruction(self, pos):
        lab_map = self.copy()
        lab_map.obstructions.add(pos)
        return lab_map

    def positions_that_cause_loops(self):
        assert len(self.visited) == 1, "this only works when the guard hasn't moved yet"

        for pos in self.obstructable_positions():
            candidate_map = self.with_additional_obstruction(pos)
            candidate_map.move_guard_while_possible()
            if candidate_map.guard_in_loop():
                yield pos

    def __str__(self):
        def char_at(pos):
            if pos in self.obstructions:
                return "#"
            if pos == self.guard_pos:
                return self.guard_dir.to_char()
            if pos in self.visited:
                return "x"
            return "."
        def row(r):
            return "".join(char_at((c, r)) for c in range(self.cols))
        return "\n".join(row(r) for r in range(self.rows))


def parse_input(input):
    lab_map = LabMap()
    rows = [l for l in input.splitlines() if l]
    lab_map.rows = len(rows)
    lab_map.cols = max((len(r) for r in rows), default=0)
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell == "#":
                lab_map.obstructions.add(Pos(x, y))
            elif cell in "^>v<":
                lab_map.guard_pos = Pos(x, y)
                lab_map.guard_dir = Dir.of_char(cell)
                lab_map._visit_cur()

    return lab_map
