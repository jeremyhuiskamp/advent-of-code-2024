from collections import defaultdict

def parse_input(input):
    order_str, pages_str = input.split("\n\n")

    order = defaultdict(set)
    for l in order_str.splitlines():
        lo, hi = l.split("|")
        order[int(lo)].add(int(hi))

    page_lines = [l.split(",") for l in pages_str.splitlines()]
    pages = [list(map(int, s))
                  for s in
                  page_lines]

    return order, pages

def order_ok(order, head, tail):
    return set(tail).issubset(order[head])

def all_order_ok(order, pages):
    return all(order_ok(order, pages[i], pages[i+1:])
               for i in
               range(len(pages)))

def sum_of_middles(things):
    middles = map(lambda p: p[len(p)//2], things)
    return sum(middles)

def sum_of_middles_of_oks(order, pages):
    oks = filter(lambda p: all_order_ok(order, p), pages)
    return sum_of_middles(oks)

def fix_order(order, pages):
    # this would probably blow up badly if the order
    # was inconsistent in any way
    def cmp(a, b):
        if a == b:
            return 0
        if b in order[a]:
            return -1
        return 1
    from functools import cmp_to_key
    key = cmp_to_key(cmp)
    return sorted(pages, key=key)

def sum_of_middles_of_fixeds(order, pages):
    not_oks = filter(lambda p: not all_order_ok(order, p), pages)
    fixed = map(lambda p: fix_order(order, p), not_oks)
    return sum_of_middles(fixed)

