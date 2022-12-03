import numpy as np
from start_day import AdventOfCodeDay

aoc = AdventOfCodeDay(2)

data = aoc.load_strings()
strategy = [x.split() for x in data]

code_to_index_him = {"A": 0, "B": 1, "C": 2}
code_to_index_me = {"X": 0, "Y": 1, "Z": 2}

shape_value = [1, 2, 3]

outcome_value = {"lose": 0, "draw": 3, "win": 6}

ORDER = "XYZ"


def outcome_f(him, me):
    if him == me:
        return "draw"
    elif him == (me + 1) % 3:
        return "lose"
    elif him == (me - 1) % 3:
        return "win"


def score(rd):
    him, me = rd
    him_idx, me_idx = code_to_index_him[him], code_to_index_me[me]
    outcome = outcome_f(him_idx, me_idx)
    return outcome_value[outcome] + shape_value[me_idx]


def score2(rd):
    him, outcome = rd
    him_index = code_to_index_him[him]
    if outcome == "Y":
        return score((him, ORDER[him_index]))
    elif outcome == "Z":
        return score((him, ORDER[(him_index + 1) % 3]))
    elif outcome == "X":
        return score((him, ORDER[(him_index - 1) % 3]))


print("Solution")
print("  1.", sum([score(rd) for rd in strategy]))
print("  2.", sum([score2(rd) for rd in strategy]))
