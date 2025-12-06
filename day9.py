from util import mapl
from itertools import repeat


class DiskMap:
    """DiskMap implements fragmenting compaction"""

    def __init__(self, data):
        self.data = data

    @property
    def blocks_used(self):
        return sum(file_len for i, file_len in enumerate(self.data) if i % 2 == 0)

    @property
    def num_files(self):
        return int((len(self.data) + 1) / 2)

    def blocks(self):
        fnum = 0
        for chunk_num, chunk_len in enumerate(self.data):
            is_file = chunk_num % 2 == 0
            val = fnum if is_file else None
            yield from repeat(val, chunk_len)
            if is_file:
                fnum += 1

    def _reversed_used_blocks(self):
        return (b for b in reversed(list(self.blocks())) if b is not None)

    def compact(self):
        """Yields the sequence of compacted blocks"""
        limit = self.blocks_used
        blocks_from_end = self._reversed_used_blocks()
        for i, b in enumerate(self.blocks()):
            if i >= limit:
                break
            if b is not None:
                yield b
            else:
                yield next(blocks_from_end)

    def checksum(self):
        return sum(i * fnum for i, fnum in enumerate(self.compact()))

    @staticmethod
    def parse(inp: str):
        data = mapl(int, inp)
        return DiskMap(data)


class Disk:
    """Disk implements non-fragmenting compaction"""

    @staticmethod
    def from_map(dm: DiskMap) -> "Disk":
        return Disk(list(dm.blocks()))

    def __init__(self, blocks: list[int | None]):
        self.blocks = blocks

    def _find_free_space(self, size: int, before: int) -> int | None:
        space_start: int | None = None
        for p in range(before):
            if self.blocks[p] is None:
                if space_start is None:
                    space_start = p
                if p - space_start + 1 >= size:
                    return space_start
            else:
                space_start = None
        return None

    def _swap(self, size, starta, startb):
        a, b = starta, startb
        for i in range(size):
            self.blocks[a + i], self.blocks[b + i] = (
                self.blocks[b + i],
                self.blocks[a + i],
            )

    def compact(self):
        """Modifies self to compacted form"""
        p = len(self.blocks) - 1
        while p >= 0:
            file_id = self.blocks[p]
            file_end = p
            p -= 1
            if file_id is None:
                continue
            while p >= 0 and self.blocks[p] == file_id:
                p -= 1
            file_size = file_end - p
            free_space = self._find_free_space(file_size, p + 1)
            if free_space is not None:
                self._swap(file_size, free_space, p + 1)

    def checksum(self):
        return sum(
            i * file_id for i, file_id in enumerate(self.blocks) if file_id is not None
        )

    def __str__(self):
        # will be a bit weird with file_id > 9
        return "".join("." if b is None else str(b) for b in self.blocks)
