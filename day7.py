import operator
import re

def cat(n1, n2):
    return int(str(n1)+str(n2))

basic_ops = [operator.add, operator.mul]
all_ops = basic_ops + [cat]

type Equation = tuple[int, list[int]]

def gen_permutations(vals, ops=basic_ops, total=None):
    if not vals:
        if not total is None:
            yield total
        return
    val, *rest = vals
    if total is None:
        yield from gen_permutations(rest, ops=ops, total=val)
    else:
        for op in ops:
            yield from gen_permutations(rest, ops=ops, total=op(total, val))

def equation_can_work(outp, inp, ops=basic_ops):
    return any(outp == perm for perm in gen_permutations(inp, ops))

def parse_input(inp) -> list[Equation]:
    splitter = re.compile(r":?\s+")
    def parse_line(l) -> Equation:
        parts_str = splitter.split(l)
        parts = list(map(int, parts_str))
        return parts[0], parts[1:]
    return [parse_line(l) for l in inp.splitlines()]

def total_calibration(equations: list[Equation], ops=basic_ops):
    return sum(e[0] for e in equations if equation_can_work(*e, ops=ops))
