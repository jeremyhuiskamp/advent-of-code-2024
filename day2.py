def pairwise(things):
    return zip(things, things[1:])


def is_safe(levels):
    diffs = [b - a for a, b in pairwise(levels)]
    sized_ok = all(1 <= abs(d) <= 3 for d in diffs)
    same_direction = all((a > 0) == (b > 0) for a, b in pairwise(diffs))
    return sized_ok and same_direction


def is_safe_with_dampener(levels):
    return any(is_safe(p) for p in remove_1_permutations(levels))


def parse_input(input):
    return [list(map(int, l.split())) for l in input.splitlines() if l]


def count_safe(reports, checker=is_safe):
    return sum(checker(r) for r in reports)


def remove_1_permutations(report):
    yield report
    for i in range(len(report)):
        yield report[:i] + report[i + 1 :]
