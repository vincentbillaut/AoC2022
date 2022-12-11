import math
import re
from start_day import AdventOfCodeDay


monkey_reg = re.compile(r"Monkey (\d+):")
starting_reg = re.compile(r"  Starting items: (.+)")
operation_reg = re.compile(r"  Operation: new = (.+)")
test_reg = re.compile(r"  Test: divisible by (\d+)")
condition_true_reg = re.compile(r"    If true: throw to monkey (\d+)")
condition_false_reg = re.compile(r"    If false: throw to monkey (\d+)")


class Monkey:
    def __init__(self, n):
        self.number = n
        self.starting_items = None
        self.operation = None
        self.test_divisible = None
        self.throw_if_true = None
        self.throw_if_false = None
        self.inspections = 0

    def increment_inspections(self):
        self.inspections += 1


def initialize_monkeys(data):
    monkeys = {}
    for i in range((len(data) + 1) // 7):
        monkey_number = int(re.match(monkey_reg, data[7 * i]).group(1))
        current_monkey = Monkey(monkey_number)
        current_monkey.starting_items = list(map(int, re.match(starting_reg, data[7 * i + 1]).group(1).split(", ")))
        current_monkey.operation = re.match(operation_reg, data[7 * i + 2]).group(1)
        current_monkey.test_divisible = int(re.match(test_reg, data[7 * i + 3]).group(1))
        current_monkey.throw_if_true = int(re.match(condition_true_reg, data[7 * i + 4]).group(1))
        current_monkey.throw_if_false = int(re.match(condition_false_reg, data[7 * i + 5]).group(1))
        monkeys[monkey_number] = current_monkey
    return monkeys


def run_one_round(monkeys, with_worry_division, max_number):
    for n, monkey in monkeys.items():
        for old in monkey.starting_items:
            new = eval(monkey.operation)  # operation references "old"
            if with_worry_division:
                new = int(new / 3)
            new = new % max_number  # keep scale under control without impacting tests
            throw_to = monkey.throw_if_false if new % monkey.test_divisible else monkey.throw_if_true
            monkeys[throw_to].starting_items.append(new)
            monkey.increment_inspections()
        monkey.starting_items = []


def run_n_rounds(monkeys, n, with_worry_division, max_number):
    for i in range(n):
        run_one_round(monkeys, with_worry_division, max_number)


def monkey_business(monkeys, n, with_worry_division):
    max_number = math.prod([m.test_divisible for m in monkeys.values()])
    run_n_rounds(monkeys, n, with_worry_division, max_number)
    sorted_inspections = list(sorted([m.inspections for m in monkeys.values()]))
    return sorted_inspections[-1] * sorted_inspections[-2]


if __name__ == "__main__":
    aoc = AdventOfCodeDay(11, overwrite=True)

    print("Solution")
    monkeys = initialize_monkeys(aoc.load_strings(strip=False))
    print("  1.", monkey_business(monkeys, 20, True))
    monkeys = initialize_monkeys(aoc.load_strings(strip=False))
    print("  2.", monkey_business(monkeys, 10000, False))
