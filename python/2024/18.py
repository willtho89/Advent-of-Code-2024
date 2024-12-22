from collections import deque
from time import perf_counter
from matrix import Matrix


def find_minimum_score(maze: Matrix, start: tuple[int, int], end: tuple[int, int]) -> int:
    """
    Use BFS to find the minimum steps from start to end. Return -1 if no path exists.
    """
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start, 0)])  # [(position, steps)]
    visited = set()

    while queue:
        current, steps = queue.popleft()

        if current == end:
            return steps

        if current in visited:
            continue
        visited.add(current)

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if maze._is_in_bounds(neighbor) and maze.get(neighbor) == '.' and neighbor not in visited:
                queue.append((neighbor, steps + 1))

    return -1  # No path found


def find_first_blocking_byte(falls: list[tuple[int, int]], size: tuple[int, int]) -> tuple[int, int]:
    """
    Simulates the falling of bytes and finds the first byte that blocks the start-to-end path.
    """
    maze = Matrix(size, default='.')
    start_pos = (0, 0)
    end_pos = (size[0] - 1, size[1] - 1)

    for (x, y) in falls:
        maze.set((y, x), '#')  # Set corrupted position; note: (y, x) due to grid orientation
        if find_minimum_score(maze, start_pos, end_pos) == -1:
            return x, y  # First byte to block the path

    return None


with open('18.input', 'r') as file:
    falls = [tuple(map(int, line.strip().split(','))) for line in file]

# Define memory grid dimensions (0-70 inclusive)
grid_size = (71, 71)
start_pos = (0, 0)
end_pos = (70, 70)

# Part One
p1_start = perf_counter()
maze = Matrix(grid_size, default='.')
for i, (x, y) in enumerate(falls[:1024]):  # Simulate the first kilobyte
    maze.set((y, x), '#')
min_score = find_minimum_score(maze, start_pos, end_pos)
p1_end = perf_counter()
print(f"Part One: {min_score}")

# Part Two
p2_start = perf_counter()
first_blocking_byte = find_first_blocking_byte(falls, grid_size)
p2_end = perf_counter()

print(f"Part Two: {first_blocking_byte[0]},{first_blocking_byte[1]}")
print(f"Elapsed Time (Part One): {p1_end - p1_start:.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p1_end:.2f}s")
print(f"Total Execution Time: {p2_end - p1_start:.2f}s")