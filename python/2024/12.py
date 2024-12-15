from time import perf_counter
from matrix import Matrix


def part1(matrix: Matrix) -> int:

    def find_region(i: int, j: int) -> tuple[set[tuple[int, int]], int]:
        plant: str = matrix[[i, j]]
        visited: set[tuple[int, int]] = set()
        fence: int = 0
        queue: list[tuple[int, int]] = [(i, j)]
        while queue:
            x, y = queue.pop()
            if (x, y) in visited:
                continue
            if not matrix._is_in_bounds([x, y]) or matrix[[x, y]] != plant:
                fence += 1
                continue
            visited.add((x, y))
            for nx, ny in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
                if (nx, ny) not in visited:
                    queue.append((nx, ny))
        return visited, len(visited) * fence

    total: int = 0
    visited: set[tuple[int, int]] = set()
    for i in range(m):
        for j in range(n):
            if (i, j) not in visited:
                region, cost = find_region(i, j)
                visited |= region
                total += cost

    return total

def part2(matrix: Matrix) -> int:

    for i in range(m):
        for j in range(n):
            matrix[[i, j]] = matrix_lines[i][j]

    def is_same(i: int, j: int, plant: str) -> bool:
        return matrix._is_in_bounds([i, j]) and matrix[[i, j]] == plant

    def get_corners(i: int, j: int) -> int:
        plant: str = matrix[[i, j]]
        NW = is_same(i - 1, j - 1, plant)
        N  = is_same(i - 1, j,     plant)
        NE = is_same(i - 1, j + 1, plant)
        W  = is_same(i,     j - 1, plant)
        E  = is_same(i,     j + 1, plant)
        SW = is_same(i + 1, j - 1, plant)
        S  = is_same(i + 1, j,     plant)
        SE = is_same(i + 1, j + 1, plant)

        return sum([
            (N and W and not NW),
            (N and E and not NE),
            (S and W and not SW),
            (S and E and not SE),
            (not (N or W)),
            (not (N or E)),
            (not (S or W)),
            (not (S or E)),
        ])

    def find_region(i: int, j: int) -> tuple[set[tuple[int, int]], int]:
        plant: str = matrix[[i, j]]
        region: set[tuple[int, int]] = set()
        queue: set[tuple[int, int]] = {(i, j)}
        while queue:
            x, y = queue.pop()
            region.add((x, y))
            for nx, ny in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
                if is_same(nx, ny, plant) and (nx, ny) not in region and (nx, ny) not in queue:
                    queue.add((nx, ny))
        corners: int = sum(get_corners(x, y) for x, y in region)
        return region, corners * len(region)

    total: int = 0
    visited: set[tuple[int, int]] = set()
    for i in range(m):
        for j in range(n):
            if (i, j) not in visited:
                region, cost = find_region(i, j)
                total += cost
                visited |= region

    return total

with open('12.input', 'r') as file:
    din: str = file.read()

matrix_lines = din.strip().split('\n')
m: int = len(matrix_lines)
n: int = len(matrix_lines[0])

matrix = Matrix([m, n], default='.')

for i in range(m):
    for j in range(n):
        matrix[[i, j]] = matrix_lines[i][j]



p1_start: float = perf_counter()
print(f"Part One: {part1(matrix)}")
p1_end: float = perf_counter()
p1_elapsed: float = p1_end - p1_start

p2_start: float = perf_counter()
print(f"Part Two: {part2(matrix)}")
p2_end: float = perf_counter()
p2_elapsed: float = p2_end - p2_start

print(f"Elapsed Time (Part One): {p1_elapsed:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.2f}s")