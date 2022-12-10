import numpy as np
from start_day import AdventOfCodeDay

aoc = AdventOfCodeDay(1)

data = aoc.load_strings()

elves = []
t = 0
for cal in data:
    if cal == "":
        elves.append(t)
        t = 0
    else:
        t += int(cal)

print("Solution")
print("  1.", max(elves))
print("  2.", np.sort(elves)[-3:].sum())
