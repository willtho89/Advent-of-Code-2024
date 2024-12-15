from time import perf_counter
from matrix import Matrix

with open('15.input', 'r') as file:
    din = file.read()

def parse_input(input):
    matrix_str, moves_str = input.split('\n\n')
    # Determine the size of the matrix
    matrix_lines = matrix_str.splitlines()
    rows, cols = len(matrix_lines), len(matrix_lines[0])

    # Create a matrix of the appropriate size
    matrix = Matrix(size=(rows, cols), default=' ')

    for y, line in enumerate(matrix_lines):
        for x, char in enumerate(line):
            matrix.set((y, x), char)

    # Parse moves
    moves = [{'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}[m] for m in moves_str.replace('\n', '')]
    return matrix, moves

def move_robot(matrix, moves):
    # robot start
    pos = next((y, x) for (y, x), v in matrix if v == '@')

    for dy, dx in moves:
        to_move = []
        q = [pos]
        while q:
            y, x = q.pop()
            if matrix.get((y, x)) in ['#', ' ']:
                break
            elif matrix.get((y, x)) != '.':
                to_move.append((y, x))
                ny, nx = y + dy, x + dx
                q.append((ny, nx))
                if dx == 0 and matrix.get((ny, nx)) == '[':
                    q.append((ny, nx + 1))
                if dx == 0 and matrix.get((ny, nx)) == ']':
                    q.append((ny, nx - 1))
        else:
            seen = set()
            for y, x in reversed(to_move):
                if (y, x) not in seen:
                    seen.add((y, x))
                    matrix[y, x], matrix[y + dy, x + dx] = matrix[y + dy, x + dx], matrix[y, x]
            pos = (pos[0] + dy, pos[1] + dx)

def calculate_gps(matrix: Matrix, control_char: str) -> int:
    return int(sum(y * 100 + x for (y, x), v in matrix if v == control_char))

p1_start = perf_counter()
matrix, moves = parse_input(din)
move_robot(matrix, moves)
print(f"Part One: {calculate_gps(matrix, 'O')}")
p1_end = perf_counter()
p1_elapsed = p1_end - p1_start

p2_start = perf_counter()
matrix, moves = parse_input(din.replace('O', '[]').replace('.', '..').replace('#', '##').replace('@', '@.'))
move_robot(matrix, moves)
print(f"Part Two: {calculate_gps(matrix, '[')}")
p2_end = perf_counter()
p2_elapsed = p2_end - p2_start

print(f"Elapsed Time (Part One): {p1_elapsed:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.2f}s")