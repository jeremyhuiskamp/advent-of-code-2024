import functools


def mapf(map_func):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return map_func(func(*args, **kwargs))

        return wrapped

    return wrapper


def transpose(strings):
    return ["".join(cs) for cs in zip(*strings)]


@mapf("".join)
def diagonal(strings, row, col):
    while row < len(strings) and col < len(strings[row]):
        yield strings[row][col]
        row += 1
        col += 1


@mapf(list)
def diagonals(strings):
    for row in range(1, len(strings)):
        yield diagonal(strings, row, 0)
    for col in range(len(strings[0])):
        yield diagonal(strings, 0, col)


def count_occurrences(big, small):
    # assumes overlaps are impossible:
    return len(big.split(small)) - 1


def count_forward_occurrences(strings, small):
    return sum(count_occurrences(big, small) for big in strings)


def count_all_occurrences(strings, small):
    verticals = transpose(strings)
    lr_diags = diagonals(strings)
    rl_diags = diagonals(list(reversed(strings)))

    total = 0
    for ss in [strings, verticals, lr_diags, rl_diags]:
        total += count_forward_occurrences(ss, small)
        total += count_forward_occurrences(ss, "".join(reversed(small)))

    return total


def parse_input(input):
    return input.strip().splitlines()


def find_A_locs(strings):
    for row in range(1, len(strings) - 1):
        for col in range(1, len(strings[row]) - 1):
            if strings[row][col] == "A":
                yield row, col


def get_Xs(strings, centers):
    for row, col in centers:
        yield "".join(
            (
                strings[row - 1][col - 1],
                strings[row - 1][col + 1],
                strings[row + 1][col - 1],
                strings[row + 1][col + 1],
            )
        )


def valid_Xs(xs):
    valid = "SSMM", "SMSM", "MMSS", "MSMS"
    return filter(lambda x: x in valid, xs)


def count_X_MAS(strings):
    return len(list(valid_Xs(get_Xs(strings, find_A_locs(strings)))))
