from day11 import parse_input, count_stones

test_input = "125 17"


def test_blink_25_times():
    numbers = parse_input(test_input)
    assert count_stones(numbers, 25) == 55312


real_input = "5 89749 6061 43 867 1965860 0 206250"


def test_real_blink_25_times():
    numbers = parse_input(real_input)
    assert count_stones(numbers, 25) == 203609


def test_real_blink_75_times():
    numbers = parse_input(real_input)
    assert count_stones(numbers, 75) == 240954878211138
