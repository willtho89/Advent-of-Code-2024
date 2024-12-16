from time import perf_counter
from heapq import heappush, heappop
from matrix import Matrix


MOVE_COST = 1
TURN_COST = 1000

def get_neighbors(pos, direction, maze):
    # Possible movements: move forward, turn left, turn right
    directions = ['N', 'E', 'S', 'W']
    dir_idx = directions.index(direction)
    movements = []

    # Move forward
    delta = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    new_i = pos[0] + delta[direction][0]
    new_j = pos[1] + delta[direction][1]
    if 0 <= new_i < maze.size[0] and 0 <= new_j < maze.size[1]:
        if maze.get([new_i, new_j]) != '#':
            movements.append(((new_i, new_j), direction, MOVE_COST))

    # Turn left
    new_dir_idx = (dir_idx - 1) % 4
    new_direction = directions[new_dir_idx]
    movements.append((pos, new_direction, TURN_COST))

    # Turn right
    new_dir_idx = (dir_idx + 1) % 4
    new_direction = directions[new_dir_idx]
    movements.append((pos, new_direction, TURN_COST))

    return movements


def find_minimum_score(maze, start_pos, end_pos, part_2 = False):
    from collections import defaultdict
    directions = ['N', 'E', 'S', 'W']
    start_direction = 'E'  # Starting facing East

    heap = []
    heappush(heap, (0, start_pos, start_direction))
    visited = dict()
    predecessors = defaultdict(list)

    while heap:
        cost, pos, direction = heappop(heap)
        state = (pos, direction)

        if state in visited and visited[state] < cost:
            continue

        visited[state] = cost

        for next_pos, next_direction, move_cost in get_neighbors(pos, direction, maze):
            next_state = (next_pos, next_direction)
            total_cost = cost + move_cost

            if (next_state not in visited) or (total_cost < visited[next_state]):
                # Found a better path to next_state
                visited[next_state] = total_cost
                predecessors[next_state] = [state]
                heappush(heap, (total_cost, next_pos, next_direction))
            elif total_cost == visited[next_state]:
                # Found an alternative path with the same minimal cost
                predecessors[next_state].append(state)
                # already visted, no heappush

    # find minmal path
    min_total_cost = 9999999999
    end_states = []
    for direction in directions:
        state = (end_pos, direction)
        if state in visited:
            cost = visited[state]
            if cost < min_total_cost:
                min_total_cost = cost
                end_states = [state]
            elif cost == min_total_cost:
                end_states.append(state)

    if not part_2:
        return min_total_cost

    # Part 2
    # Backtrack to find all positions that are on any minimal path
    tiles_on_min_paths = set()
    visited_backtracking = set()

    def backtrack(state):
        if state in visited_backtracking:
            return
        visited_backtracking.add(state)
        pos, direction = state
        tiles_on_min_paths.add(pos)
        for pred_state in predecessors[state]:
            backtrack(pred_state)

    for end_state in end_states:
        backtrack(end_state)

    return tiles_on_min_paths


with open('16.input', 'r') as file:
    lines = [line.rstrip('\n') for line in file]

    size = [len(lines), len(lines[0])]
    maze = Matrix(size, default='#')
    start_pos = None
    end_pos = None

    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            maze.set([i, j], ch)
            if ch == 'S':
                start_pos = (i, j)
            elif ch == 'E':
                end_pos = (i, j)

# Part One
p1_start = perf_counter()
min_score = find_minimum_score(maze, start_pos, end_pos)
print(f"Part One: {min_score}")
p1_end = perf_counter()

# Part Two
p2_start = perf_counter()
tiles_on_min_paths = find_minimum_score(maze, start_pos, end_pos, part_2=True)
num_tiles_on_min_paths = len(tiles_on_min_paths)
print(f"Part Two: {num_tiles_on_min_paths}")
p2_end = perf_counter()

print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")
