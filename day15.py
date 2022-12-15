import re
import time
from start_day import AdventOfCodeDay

pattern = r"Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)"


def no_beacon_row(positions, y):
    impossible_x = set()
    for (sx, sy), (bx, by) in positions:
        distance = abs(sx - bx) + abs(sy - by)
        distance_left = distance - abs(y - sy)
        if distance_left >= 0:
            for i in range(sx - distance_left, sx + distance_left + 1):
                impossible_x.add(i)
    beacon_x_at_y = set([bx for (_, _), (bx, by) in positions if by == y])
    return len(impossible_x - beacon_x_at_y)


def get_sensor_dead_zone(sensor, beacon):
    zone = {}
    distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    for y in range(sensor[1] - distance, sensor[1] + distance + 1):
        distance_left = distance - abs(y - sensor[1])
        zone[y] = [(sensor[0] - distance_left, sensor[0] + distance_left)]
    return zone


def compress_intervals(intervals):
    if len(intervals) <= 1:
        return intervals
    (a, b), (c, d) = intervals[0], intervals[1]  # assumes input is sorted, so a <= c
    if c <= b + 1:
        return compress_intervals([(a, max(b, d))] + intervals[2:])
    else:
        return [(a, b)] + compress_intervals(intervals[1:])


def merge_zones(zone1, zone2):
    merged = zone1.copy()
    for y in zone2:
        if y in zone1:
            all_intervals = list(sorted(zone1[y] + zone2[y], key=lambda x: x[0]))
            merged[y] = compress_intervals(all_intervals.copy())
        else:
            merged[y] = zone2[y]
    return merged


def collect_all_dead_zones(init_positions):
    dead_zones = {}
    print("Collecting from")
    ref = time.time()
    for i, (sensor, beacon) in enumerate(init_positions):
        dead_zones = merge_zones(dead_zones, get_sensor_dead_zone(sensor, beacon))
        checkpoint = time.time()
        print(f"  ... sensor {i} (done in {int(checkpoint - ref)}s)")
        ref = checkpoint
    return dead_zones


def crop_row(row, bounds):
    if len(row) == 0:
        return []
    a, b = row[0]
    if b < bounds[0]:
        return crop_row(row[1:], bounds)
    if a < bounds[0]:
        return [(bounds[0], min(b, bounds[1]))] + crop_row(row[1:], bounds)
    if a > bounds[1]:
        return []
    if b > bounds[1]:
        return [(a, bounds[1])]
    return [(a, b)] + crop_row(row[1:], bounds)


def tuning_frequency(init_positions, bounds):
    dead_zones = collect_all_dead_zones(init_positions)
    for y in range(bounds[0], bounds[1] + 1):
        if len(dead_zones[y]) >= 2 and len(cropped_zone := crop_row(dead_zones[y], bounds)) == 2:
            return 4000000 * (cropped_zone[0][1] + 1) + y


if __name__ == "__main__":
    aoc = AdventOfCodeDay(15, overwrite=True)
    data = aoc.load_regex(pattern, 4, strip=True)
    input_positions = [((int(a), int(b)), (int(c), int(d))) for a, b, c, d in data]

    print("Solution")
    print("  1.", no_beacon_row(input_positions, 2000000))
    print("  2.", tuning_frequency(input_positions, (0, 4000000)))
