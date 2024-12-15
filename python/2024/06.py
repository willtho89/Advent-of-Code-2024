from itertools import cycle

from matrix import Matrix

with open('06.input', 'r') as file:
    din = file.read()

lines = din.splitlines()

ROWS = len(lines)
COLS = len(lines[0])

directions = {">": (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
loop = cycle(directions)

def reset_loop(loop, char):
    while next(loop) != char:
        continue

matrix = Matrix((ROWS, COLS), default=None)

for i in range(ROWS):
    for j in range(COLS):
        matrix.set((i, j), lines[i][j])

initial_pos = ()
d = ()
for i in range(ROWS):
    for j in range(COLS):
        if matrix.get((i, j)) in directions:
            initial_pos = (i, j)
            d = directions[matrix.get((i, j))]
            reset_loop(loop, matrix.get((i, j)))

def is_inside(matrix, pos):
    return 0 <= pos[0] < matrix.size[0] and 0 <= pos[1] < matrix.size[1]

def walk(matrix, pos, d, obstacle, d_loop):
    i, j = pos
    x, y = d
    new_pos = (x + i, y + j)
    if is_inside(matrix, new_pos) and \
            (matrix.get(new_pos) == '#' or new_pos == obstacle):
        return pos, directions[next(d_loop)]
    return new_pos, d

def evaluate_path(matrix, initial_pos, initial_d, obstacle, d_loop):
    inside = True
    in_loop = False
    pos = initial_pos
    d = initial_d
    walked = set()
    loop_detec = set()
    while inside and not in_loop:
        walked.add(pos)
        loop_detec.add((pos, d))
        pos, d = walk(matrix, pos, d, obstacle, d_loop)
        in_loop = (pos, d) in loop_detec
        inside = is_inside(matrix, pos)
    return len(walked), in_loop

print("locs_visited: ", evaluate_path(matrix, initial_pos, d, None, loop)[0])

# P2 brute force?
loop_count = 0
for row in range(ROWS):
    for col in range(COLS):
        reset_loop(loop, matrix.get(initial_pos))
        size, in_loop = evaluate_path(matrix, initial_pos, d, (row, col), loop)
        loop_count += 1 if in_loop else 0
        percentage = int((row * ROWS + col) / (ROWS * COLS) * 100)
        print(f'{percentage}%', end='\r')

print('100%')
print('loop_count: ', loop_count)