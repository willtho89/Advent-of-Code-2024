
import sys
from collections import Counter, defaultdict
from time import perf_counter

sys.setrecursionlimit(100000)
FILE = sys.argv[1] if len(sys.argv) > 1 else "11.input"


with open('11.input', 'r') as file:
    din = file.read()

lines = []
for line in din.splitlines():
    lines.append([int(val) for val in line.split()])


def blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    s = str(stone)
    if len(s) % 2 == 0:
        return [int(s[: (len(s) // 2)]), int(s[(len(s) // 2) :])]

    return [stone * 2024]


def solve(times: int = 25):
    answer = 0

    stones = Counter(lines[0])
    for _ in range(times):
        new_stones = defaultdict(int)
        for rock, count in stones.items():
            blink_result = blink(rock)
            for blink_result_rock in blink_result:
                new_stones[blink_result_rock] += count

        stones = Counter(new_stones)

    return sum(stones.values())


p1_start = perf_counter()
print(f"Part One: {solve()}")
p1_end = perf_counter()
p1_elapsed = p1_end - p1_start

p2_start = perf_counter()
print(f"Part Two: {solve(75)}")
p2_end = perf_counter()
p2_elapsed = p2_end - p2_start

print(f"Elapsed Time (Part One): {p1_elapsed:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.2f}s")