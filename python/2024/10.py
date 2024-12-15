import sys
from time import perf_counter
from matrix import Matrix

with open('10.input', 'r') as file:
    din = file.read().splitlines()
matrix_data = [[int(x) for x in line.strip()] for line in din]
matrix_size = (len(matrix_data), len(matrix_data[0]))
matrix = Matrix(matrix_size)

for i, line in enumerate(matrix_data):
    for j, value in enumerate(line):
        matrix[(i, j)] = value


def dfs(matrix, i, j, target, prev=-1, count_paths=False):
    if not matrix._is_in_bounds((i, j)):
        return set() if not count_paths else 0
    value = matrix[(i, j)]
    if value != prev + 1:
        return set() if not count_paths else 0
    if value == target:
        return {(i, j)} if not count_paths else 1
    result = set() if not count_paths else 0
    for neighbor_value, (ni, nj) in matrix.neighbors((i, j)):
        if count_paths:
            result += dfs(matrix, ni, nj, target, value, count_paths)
        else:
            result.update(dfs(matrix, ni, nj, target, value))
    return result

def count_paths(matrix, target, count_paths=False):
    path_count = 0
    for (i, j), value in matrix:
        if value == 0:
            if count_paths:
                path_count += dfs(matrix, i, j, target, count_paths=True)
            else:
                path_count += len(dfs(matrix, i, j, target))
    return path_count


# Part 1
p1_start = perf_counter()
part_one_result = count_paths(matrix, 9)
p1_end = perf_counter()
print(f"Part One: {part_one_result}")
print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")

# Part 2
p2_start = perf_counter()
part_two_result = count_paths(matrix, 9, count_paths=True)
p2_end = perf_counter()
print(f"Part Two: {part_two_result}")
print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")
