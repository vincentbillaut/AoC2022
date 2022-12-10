import re
from start_day import AdventOfCodeDay

pattern_dir = re.compile(r"dir (.+)")
pattern_file = re.compile(r"(\d+) (.+)")
pattern_command = re.compile(r"\$ (cd|ls)(.*)")
MAX_SIZE = 40000000


def parse_instructions(lines):
    all_instructions = []
    result_list = []
    for line in lines:
        # command
        if re.match(pattern_command, line):
            # finish previous ls
            if result_list != []:
                all_instructions.append(("ls", result_list))
                result_list = []
            instruction = re.match(pattern_command, line).group(1)
            if instruction == "cd":
                all_instructions.append(("cd", re.match(pattern_command, line).group(2).strip()))
        elif re.match(pattern_file, line):
            match = re.match(pattern_file, line)
            result_list.append(("file", match.group(2), int(match.group(1))))
        elif re.match(pattern_dir, line):
            result_list.append(("dir", re.match(pattern_dir, line).group(1)))
    if result_list != []:
        all_instructions.append(("ls", result_list))
    return all_instructions


def build_file_system(instructions):
    """
    We assume that the first instruction is cd /
    """
    file_system = Tree("/", parent=None, is_file=False)
    current_node = file_system

    for instruction, content in instructions[1:]:
        if instruction == "cd":
            assert content in current_node.children
            current_node = current_node.children[content]
        elif instruction == "ls":
            for element in content:
                if element[0] == "dir":
                    current_node.add_child(element[1], is_file=False)
                else:
                    current_node.add_child(element[1], is_file=True, size=element[2])
    return file_system


def find_dir_to_delete(dirs, size):
    size_to_free = dirs["/"] - size
    dirs_big_enough = {k: v for k, v in dirs.items() if v >= size_to_free}
    return min(dirs_big_enough.values())


class Tree:
    def __init__(self, name, parent, is_file, size=None):
        self.name = name
        self.parent = parent
        self.is_file = is_file
        self.size = size
        self.children = {"..": self.parent}

    def add_child(self, name, is_file, size=None):
        child = Tree(name, self, is_file, size)
        self.children[name] = child

    @property
    def total_size(self):
        if self.size is None:
            self.size = sum(child.total_size for name, child in self.children.items() if name != "..")
        return self.size

    def enumerate_dir_sizes(self):
        if self.is_file:
            return {}
        dir_sizes = {self.name: self.total_size}
        for child in self.children:
            if child != "..":
                child_dir = self.children[child].enumerate_dir_sizes()
                dir_sizes.update({f"{self.name}/{k}": v for k, v in child_dir.items()})
        return dir_sizes


if __name__ == "__main__":
    aoc = AdventOfCodeDay(7, overwrite=True)
    data = aoc.load_strings()

    all_instructions = parse_instructions(data)
    file_system = build_file_system(all_instructions)
    dir_sizes = file_system.enumerate_dir_sizes()

    print("Solution")
    print("  1.", sum(v for v in dir_sizes.values() if v <= 100000))
    print("  2.", find_dir_to_delete(dir_sizes, MAX_SIZE))
