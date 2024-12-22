from functools import lru_cache
from time import perf_counter

def count_ways_to_form_design(towels: list[str], design: str) -> int:
    @lru_cache(None)
    def helper(sub_design: str) -> int:
        if sub_design == "":
            return 1

        total_ways = 0
        for towel in towels:
            if sub_design.startswith(towel):
                total_ways += helper(sub_design[len(towel):])

        return total_ways

    return helper(design)

def sum_of_ways(towel_patterns: list[str], designs: list[str]) -> int:
    total_count = 0
    for design in designs:
        total_count += count_ways_to_form_design(towel_patterns, design)
    return total_count

def can_form_design(towels: list[str], design: str, memo: dict) -> bool:
    if design in memo:
        return memo[design]
    if design == "":
        return True

    for towel in towels:
        if design.startswith(towel):
            if can_form_design(towels, design[len(towel):], memo):
                memo[design] = True
                return True

    memo[design] = False
    return False

def count_possible_designs(towel_patterns: list[str], designs: list[str]) -> int:
    memo = {}
    possible_count = 0
    for design in designs:
        if can_form_design(towel_patterns, design, memo):
            possible_count += 1
    return possible_count

with open('19.input', 'r') as file:
    lines = [line.rstrip('\n') for line in file]

# Read the towel patterns
towel_patterns = lines[0].split(", ")

# Read the desired designs
designs = lines[2:]

# Part One
p1_start = perf_counter()
possible_designs_count = count_possible_designs(towel_patterns, designs)
print(f"Part One: {possible_designs_count}")
p1_end = perf_counter()

# Part Two
p2_start = perf_counter()
total_ways_count = sum_of_ways(towel_patterns, designs)
print(f"Part Two: {total_ways_count}")
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p1_end:.2f}s")
print(f"Total Execution Time: {p2_end - p1_start:.2f}s")