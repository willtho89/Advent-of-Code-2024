import sys
from collections import deque
from time import perf_counter

sys.setrecursionlimit(10**6)

with open('09.input', 'r') as file:
    din = file.read().strip()

def solve(part2):
    A = deque()
    SPACE = deque()
    file_id = 0
    FINAL = []
    pos = 0

    for i, c in enumerate(din):
        if i % 2 == 0:
            count = int(c)
            if part2:
                A.append((pos, count, file_id))
            for _ in range(count):
                FINAL.append(file_id)
                if not part2:
                    A.append((pos, 1, file_id))
                pos += 1
            file_id += 1
        else:
            SPACE.append((pos, int(c)))
            for _ in range(int(c)):
                FINAL.append(None)
                pos += 1

    for pos, sz, file_id in reversed(A):
        for space_i, (space_pos, space_sz) in enumerate(SPACE):
            if space_pos < pos and sz <= space_sz:
                for i in range(sz):
                    assert FINAL[pos + i] == file_id, f'{FINAL[pos + i]=}'
                    FINAL[pos + i] = None
                    FINAL[space_pos + i] = file_id
                SPACE[space_i] = (space_pos + sz, space_sz - sz)
                break

    return sum(i * c for i, c in enumerate(FINAL) if c is not None)

p1_start = perf_counter()
print(f"Part One: {solve(False)}")
p1_end = perf_counter()
p1_elapsed = p1_end - p1_start

p2_start = perf_counter()
print(f"Part Two: {solve(True)}")
p2_end = perf_counter()
p2_elapsed = p2_end - p2_start

print(f"Elapsed Time (Part One): {p1_elapsed:0.2f}s")
print(f"Elapsed Time (Part Two): {p2_elapsed:0.2f}s")