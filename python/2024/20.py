from collections import defaultdict
from time import perf_counter
import heapq
from matrix import Matrix

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def dijkstra(grid, start_pos, end_pos):
    dist = Matrix(grid.size, default=float('inf'))
    dist[start_pos] = 0
    parent = {}
    queue = []
    heapq.heappush(queue, (0, *start_pos))

    while queue:
        d, ci, cj = heapq.heappop(queue)
        for di, dj in directions:
            ni, nj = ci + di, cj + dj
            if grid.get((ni, nj)) == '#' or not grid._is_in_bounds((ni, nj)):
                continue
            if d + 1 < dist[(ni, nj)]:
                dist[(ni, nj)] = d + 1
                parent[(ni, nj)] = (ci, cj)
                heapq.heappush(queue, (dist[(ni, nj)], ni, nj))

    # Trace back the path from end to start
    stack = [end_pos]
    visited = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) not in parent:
            break
        stack.append(parent[(x, y)])

    return visited, dist


# Define cheat space
cheat_space = defaultdict(list)
for i in range(-20, 21):
    for j in range(-20, 21):
        if abs(i) + abs(j) <= 20 and (abs(i) >= 2 or abs(j) >= 2):
            cheat_space[abs(i) + abs(j)].append((i, j))

# Part 1
def part1():
    shortcuts = defaultdict(int)
    for ci, cj in original_path:
        for di, dj in directions:
            ni, nj = ci + 2 * di, cj + 2 * dj
            if not dist._is_in_bounds((ni, nj)) or dist[(ni, nj)] == float('inf'):
                continue
            if dist[(ci, cj)] + 2 < dist[(ni, nj)]:
                shortcuts[dist[(ni, nj)] - (dist[(ci, cj)] + 2)] += 1

    cheats = sum(shortcuts[key] for key in shortcuts if key >= 100)
    print(f"Part One: {cheats}")

# Part 2
def part2():
    cheats = defaultdict(int)

    def best_in_cheat_space(cord):
        ci, cj = cord
        for key in cheat_space:
            for i, j in cheat_space[key]:
                ni, nj = ci + i, cj + j
                if not dist._is_in_bounds((ni, nj)) or dist[(ni, nj)] == float('inf'):
                    continue
                if dist[(ci, cj)] + key < dist[(ni, nj)]:
                    cheats[dist[(ni, nj)] - (dist[(ci, cj)] + key)] += 1

    for cord in original_path:
        best_in_cheat_space(cord)

    part2_result = sum(cheats[cheat] for cheat in sorted(cheats, reverse=True) if cheat >= 100)
    print(f"Part Two: {part2_result}")


input_data = []
with open('20.input') as file:
    for i, line in enumerate(file):
        row = list(line.strip())
        input_data.append(row)
        for j, ch in enumerate(row):
            if ch == 'S':
                start_pos = (i, j)
            elif ch == 'E':
                end_pos = (i, j)

    # Create a matrix to hold the input data
    matrix_size = (len(input_data), len(input_data[0]))
    grid = Matrix(matrix_size, default='#')

    # Populate the matrix
    for i, row in enumerate(input_data):
        for j, value in enumerate(row):
            grid.set((i, j), value)


# Run Dijkstra's algorithm
original_path, dist = dijkstra(grid, start_pos, end_pos)
total_distance = dist[end_pos]

# Measure execution time for each part
p1_start = perf_counter()
part1()
p1_end = perf_counter()

p2_start = perf_counter()
part2()
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p1_end:.2f}s")
print(f"Total Execution Time: {p2_end - p1_start:.2f}s")