import math
from copy import deepcopy
from start_day import AdventOfCodeDay


def compare_packets(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None  # no decision
        return left < right
    if isinstance(left, list) and isinstance(right, list):
        if len(left) == 0 and len(right) == 0:
            return None  # no decision
        if len(left) == 0:
            return True
        if len(right) == 0:
            return False
        comparison = compare_packets(left[0], right[0])
        return comparison if comparison is not None else compare_packets(left[1:], right[1:])
    if isinstance(left, list):
        return compare_packets(left, [right])
    if isinstance(right, list):
        return compare_packets([left], right)


def sort_packets_in_place(p_list):
    # bubble sort
    i, n = 0, len(p_list)
    while i < n - 1:
        if compare_packets(p_list[i], p_list[i + 1]):
            i += 1
        else:  # swap
            temp = p_list[i]
            p_list[i] = p_list[i + 1]
            p_list[i + 1] = temp
            i = max(0, i - 1)


def decoder_key(packets):
    all_packets = deepcopy(packets)
    all_packets.extend([[[2]], [[6]]])  # divider packets
    sort_packets_in_place(all_packets)
    return math.prod([i + 1 for i, p in enumerate(all_packets) if p == [[2]] or p == [[6]]])


if __name__ == "__main__":
    aoc = AdventOfCodeDay(13, overwrite=True, display=False)
    data = aoc.load_strings()
    input_packet_pairs = [(eval(data[3 * i]), eval(data[3 * i + 1])) for i in range(len(data) // 3 + 1)]
    input_packets = [eval(l) for l in data if l != ""]

    print("Solution")
    print("  1.", sum([i + 1 for i, pair in enumerate(input_packet_pairs) if compare_packets(*pair)]))
    print("  2.", decoder_key(input_packets))
