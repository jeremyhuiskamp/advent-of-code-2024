import re

mul_call = re.compile("mul\\(([0-9]{,3}),([0-9]{,3})\\)")
do_dont = re.compile("(do|don't)\\(\\)")

def parse_input(input) -> list[(int,int)]:
    return [(int(m[0]), int(m[1])) for m in mul_call.findall(input)]

def enabled_input(input):
    def enabled_chunks(input):
        enabled = True
        while m := do_dont.search(input):
            if enabled:
                yield input[:m.start()]
            enabled = (m[0] == "do()")
            input = input[m.end():]
        if enabled:
            yield input
    return "".join(enabled_chunks(input))


def calculate(nums):
    return sum(a*b for a, b in nums)
