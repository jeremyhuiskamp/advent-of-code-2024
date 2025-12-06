from util import mapl
import functools


def parse_input(inp):
    return mapl(int, inp.split())


def count_stones(ns, blinks):
    # This is intractably slow if we do all the calculations for each
    # number, but it turns out that the vast majority of the computations
    # are duplicated, so memo-izing make it quite fast.
    # Embed to throw away cache after each run.
    @functools.cache
    def _blink(n, blinks):
        if blinks == 0:
            return 1

        blinks -= 1

        if n == 0:
            return _blink(1, blinks)

        numstr = str(n)
        numstrlen = len(numstr)
        if numstrlen % 2 == 0:
            half = int(numstrlen / 2)
            h1 = int(numstr[:half])
            h2 = int(numstr[half:])
            return _blink(h1, blinks) + _blink(h2, blinks)

        return _blink(n * 2024, blinks)

    return sum(_blink(n, blinks) for n in ns)
