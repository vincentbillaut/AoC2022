from start_day import AdventOfCodeDay

DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
SYMBOLS = ["0", "1", "2", "=", "-"]


def convert_snafu(s, power=1):
    if s == "":
        return 0
    return DIGITS[s[-1]] * power + convert_snafu(s[:-1], power * 5)


def convert_to_snafu(n):
    if n <= 2:
        return SYMBOLS[n]
    return convert_to_snafu(n // 5 + int(n % 5 >= 3)) + SYMBOLS[n % 5]


total_fuel = lambda l: convert_to_snafu(sum(convert_snafu(s) for s in l))

if __name__ == "__main__":
    aoc = AdventOfCodeDay(25, overwrite=False, display=False)
    print("Solution")
    print("  1/2.", total_fuel(aoc.load_strings()))
