import re
from start_day import AdventOfCodeDay

pattern_op = re.compile(r"([a-z]+): ([a-z]+) ([\*/\+-]) ([a-z]+)")
pattern_base = re.compile(r"([a-z]+): (\d+)")


def compute_root(base, operations):
    value_dict = base.copy()

    def compute_node(node):
        if node in value_dict:
            return value_dict[node]
        a, b, op = operations[node]
        va, vb = compute_node(a), compute_node(b)
        match op:
            case "*":
                value = va * vb
            case "+":
                value = va + vb
            case "-":
                value = va - vb
            case "/":
                value = va // vb
        value_dict[node] = value
        return value

    return compute_node("root")


def make_regex_processing(reg, func, int_left):
    def process(to_split, right_value):
        left, right = re.match(reg, to_split).group(1), re.match(reg, to_split).group(2)
        value = int(left) if int_left else int(right)
        remain = right if int_left else left
        return remain, func(value, right_value)

    return process


REGEX_LIST = [
    (re.compile(r"^\((.+) - (\d+)\)$"), lambda v, right: right + v, False),
    (re.compile(r"^\((\d+) - (.+)\)$"), lambda v, right: v - right, True),
    (re.compile(r"^\((.+) \+ (\d+)\)$"), lambda v, right: right - v, False),
    (re.compile(r"^\((\d+) \+ (.+)\)$"), lambda v, right: right - v, True),
    (re.compile(r"^\((.+) \* (\d+)\)$"), lambda v, right: right // v, False),
    (re.compile(r"^\((\d+) \* (.+)\)$"), lambda v, right: right // v, True),
    (re.compile(r"^\((.+) / (\d+)\)$"), lambda v, right: right * v, False),
    (re.compile(r"^\((\d+) / (.+)\)$"), lambda v, right: v // right, True),
]


def solve_equation(eq):
    left, right = eq.split(" = ")[0], int(eq.split(" = ")[1])
    if left == "x":
        return int(right)
    for regex, func, int_left in REGEX_LIST:
        if re.match(regex, left):
            processing = make_regex_processing(regex, func, int_left)
            remain, new_right = processing(left, right)
            return solve_equation(f"{remain} = {new_right}")
    print("NO MATCH")


def compute_hmn(base, operations):
    value_dict = base.copy()
    del value_dict["humn"]

    def compute_if_possible(node):
        if node in value_dict:
            return True, value_dict[node]
        if node == "humn":
            return False, None
        a, b, op = operations[node]
        pa, va = compute_if_possible(a)
        if not pa:
            return False, None
        pb, vb = compute_if_possible(b)
        if not pb:
            return False, None
        match op:
            case "*":
                value = va * vb
            case "+":
                value = va + vb
            case "-":
                value = va - vb
            case "/":
                value = int(va / vb)
        value_dict[node] = value
        return True, value

    for node in operations:
        compute_if_possible(node)
    # value_dict is as full as possible
    # print(f"{len(value_dict)} / {len(base) + len(operations)}")

    def compute_string(node):
        if node in value_dict:
            return str(value_dict[node])
        if node == "humn":
            return "x"
        a, b, op = operations[node]
        va, vb = compute_string(a), compute_string(b)
        match op:
            case "*":
                value = f"({va} * {vb})"
            case "+":
                value = f"({va} + {vb})"
            case "-":
                value = f"({va} - {vb})"
            case "/":
                value = f"({va} / {vb})"
        return value

    left, right, _ = operations["root"]
    equation = f"{compute_string(left)} = {compute_string(right)}"
    return solve_equation(equation)


if __name__ == "__main__":
    aoc = AdventOfCodeDay(21, overwrite=False)
    op_dict = {s: (a, b, op) for s, a, op, b in aoc.load_regex(pattern_op, 4)}
    base_dict = {s: int(v) for s, v in aoc.load_regex(pattern_base, 2)}

    print("Solution")
    print("  1.", compute_root(base_dict, op_dict))
    print("  2.", compute_hmn(base_dict, op_dict))
