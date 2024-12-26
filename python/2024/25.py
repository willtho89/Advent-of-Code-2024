from time import perf_counter
from typing import List, Tuple

def parse_schematics(lines: List[str]) -> Tuple[List[List[int]], List[List[int]], int]:
    schematics = []
    schematic = []
    for line in lines:
        if line.strip() == '':
            if schematic:
                schematics.append(schematic)
                schematic = []
        else:
            schematic.append(line.strip())
    if schematic:
        schematics.append(schematic)

    locks = []
    keys = []
    available_space = 0
    for schematic in schematics:
        # Determine if lock or key
        top_row = schematic[0]
        bottom_row = schematic[-1]
        if top_row == '#' * len(top_row) and bottom_row == '.' * len(bottom_row):
            # It's a lock
            locks.append(schematic)
        elif top_row == '.' * len(top_row) and bottom_row == '#' * len(bottom_row):
            # It's a key
            keys.append(schematic)
        else:
            # Shouldn't happen
            pass
        # Set available_space (same for all schematics)
        available_space = len(schematic) - 2  # Exclude top and bottom rows

    lock_heights = []
    for lock in locks:
        heights = []
        for col in range(len(lock[0])):
            height = 0
            # Start from row 1 (exclude top row)
            for row in range(1, len(lock)-1):
                if lock[row][col] == '#':
                    height += 1
                else:
                    break
            heights.append(height)
        lock_heights.append(heights)

    key_heights = []
    for key in keys:
        heights = []
        for col in range(len(key[0])):
            height = 0
            # Start from bottom-1 row (exclude bottom row), go upwards
            for row in range(len(key)-2, 0, -1):
                if key[row][col] == '#':
                    height += 1
                else:
                    break
            heights.append(height)
        key_heights.append(heights)

    return lock_heights, key_heights, available_space

def count_valid_pairs(lock_heights: List[List[int]], key_heights: List[List[int]], available_space: int) -> int:
    count = 0
    for l_heights in lock_heights:
        for k_heights in key_heights:
            fits = True
            for lh, kh in zip(l_heights, k_heights):
                if lh + kh > available_space:
                    fits = False
                    break
            if fits:
                count += 1
    return count

with open('25.input', 'r') as file:
    lines = [line.rstrip('\n') for line in file]

p1_start = perf_counter()
lock_heights, key_heights, available_space = parse_schematics(lines)
num_valid_pairs = count_valid_pairs(lock_heights, key_heights, available_space)
p1_end = perf_counter()

print(f"Part One: {num_valid_pairs}")
print(f"Elapsed Time (Part One): {p1_end - p1_start:.6f} seconds")