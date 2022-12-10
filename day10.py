from start_day import AdventOfCodeDay


class Signal:
    def __init__(self):
        self.value = 1
        self.value_list = []

    def addx(self, v):
        self.value_list.extend([self.value, self.value])
        self.value += v

    def noop(self):
        self.value_list.append(self.value)

    def strength(self):
        return sum((i + 1) * v for i, v in enumerate(self.value_list) if i % 40 == 19)

    def draw(self):
        for i in range(6):
            print("".join(["#" if k - 1 <= self.value_list[i * 40 + k] <= k + 1 else " " for k in range(40)]))


def process_data(instructions):
    signal = Signal()
    for instruction in instructions:
        match instruction.split():
            case ["noop"]:
                signal.noop()
            case ["addx", v]:
                signal.addx(int(v))
    return signal


if __name__ == "__main__":
    aoc = AdventOfCodeDay(10, overwrite=True)
    data_input = aoc.load_strings()
    signal = process_data(data_input)

    print("Solution")
    print("  1.", signal.strength())
    print("  2:")
    signal.draw()
