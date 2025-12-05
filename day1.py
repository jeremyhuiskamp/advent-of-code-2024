
def parse_input(input):
    left, right = [], []
    for line in input.splitlines():
        l, r = line.split()
        left.append(int(l))
        right.append(int(r))
    return left, right

def distance(left, right):
    return sum(abs(l-r)
               for l, r in
               zip(sorted(left),
                   sorted(right),
                  )
              )

def similarity_score(left, right):
    from collections import defaultdict
    right_counts = defaultdict(lambda: 0)
    for r in right:
        right_counts[r] += 1
    return sum(l * right_counts[l]
               for l in left)
