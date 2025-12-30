from dataclasses import dataclass
import re


def _is_valid_press(presses):
    """
    You can't press a button fewer than 0 times,
    or a fractional number of times.
    """
    return 0 <= presses and presses == int(presses)


vector_pattern = re.compile(r"X[+=](?P<x>\d+), Y[+=](?P<y>\d+)")


class Vector(tuple):
    def __new__(self, x, y):
        if x <= 0 or y <= 0:
            # input doesn't include these, and it makes life easier:
            raise ValueError((x, y))
        return tuple.__new__(Vector, (x, y))

    @classmethod
    def parse(cls, line):
        m = vector_pattern.search(line)
        if not m:
            raise ValueError(line)
        return cls(int(m["x"]), int(m["y"]))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def _brute_force_cost(self, buttonA: "Vector", buttonB: "Vector"):
        """
        Try various combinations of the buttons until we find a solution.
        Assumes that all three vectors point in the same direction and
        that their x component is non-zero.
        """
        # efficient, not efficient
        eff, neff = buttonB, buttonA
        effCost, neffCost = 1, 3
        if buttonA.x > buttonB.x * 3:
            eff, neff = neff, eff
            effCost, neffCost = neffCost, effCost

        countEff = int(self.x / eff.x)
        while countEff >= 0:
            neffDist = self.x - (eff.x * countEff)
            countNeff = neffDist / neff.x
            if countNeff == int(countNeff):
                return effCost * countEff + neffCost * countNeff
            countEff -= 1

        return None

    def same_dir_as(self, other: "Vector"):
        return self.x * other.y == self.y * other.x

    def cost(self, buttonA: "Vector", buttonB: "Vector"):
        # start with:
        # Ax*a + Bx*b = Px
        # Ay*a + By+b = Py
        # then solve for b to get bpresses below,
        # and pick one of the intermediate forms for apresses.
        try:
            bpresses = (self.x * buttonA.y - self.y * buttonA.x) / (
                buttonB.x * buttonA.y - buttonB.y * buttonA.x
            )
            apresses = (self.x - buttonB.x * bpresses) / buttonA.x

        except ZeroDivisionError:
            if self.same_dir_as(buttonA):
                return self._brute_force_cost(buttonA, buttonB)
            return None

        if _is_valid_press(bpresses) and _is_valid_press(apresses):
            return 3 * apresses + bpresses

        return None


@dataclass
class Machine:
    prize: Vector
    buttonA: Vector
    buttonB: Vector

    def with_corrected_prize(self):
        prize = Vector(self.prize.x + 10000000000000, self.prize.y + 10000000000000)
        return Machine(prize, self.buttonA, self.buttonB)

    def cost(self):
        return self.prize.cost(self.buttonA, self.buttonB)

    @classmethod
    def parse(cls, inputstr):
        vectors = [Vector.parse(l) for l in inputstr.splitlines()]
        buttonA, buttonB, prize = vectors
        return cls(prize, buttonA, buttonB)

    @classmethod
    def parse_many(cls, inputstr):
        return [cls.parse(m) for m in inputstr.split("\n\n")]


def fewest_tokens_for_all_possible_prizes(machines: list[Machine]):
    return sum(m.cost() or 0 for m in machines)
