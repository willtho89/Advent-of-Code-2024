from itertools import permutations
from matrix import Matrix

# Read the input file
with open("08.input", "r") as file:
    lines = file.readlines()

r = len(lines)
c = len(lines[0].strip())

# Initialize the matrices
matrix = Matrix((r, c), default=".")
cmatrix = Matrix((r, c), default=".")

# Populate the matrix with input data
for i, line in enumerate(lines):
    for j, char in enumerate(line.strip()):
        matrix.set((i, j), char)

# Create a dictionary to hold the positions of alphanumeric characters
antenna_dict = {}
for i in range(r):
    for j in range(c):
        pointer = matrix.get((i, j))
        if pointer.isalnum():
            antenna_dict[pointer] = antenna_dict.get(pointer, []) + [(i, j)]

# First method: Calculate antinodes and update cmatrix directly
ans = 0
for key, value in antenna_dict.items():
    for pair in permutations(value, 2):
        n1, n2 = pair
        diffx = n1[0] - n2[0]
        diffy = n1[1] - n2[1]
        antinodes = (
            (n1[0] + diffx, n1[1] + diffy),
            (n2[0] - diffx, n2[1] - diffy),
        )
        for node in antinodes:
            if 0 <= node[0] < r and 0 <= node[1] < c:
                if cmatrix.get(node) != "#":
                    cmatrix.set(node, "#")
                    ans += 1

print(ans)


ans = 0
cmatrix = Matrix((r, c), default=".")  # Reset cmatrix

def check_antinodes(starting_point, diffx, diffy):
    node = starting_point
    while 0 <= node[0] < r and 0 <= node[1] < c:
        cmatrix.set(node, "#")
        node = (node[0] + diffx, node[1] + diffy)

for key, value in antenna_dict.items():
    for pair in permutations(value, 2):
        n1, n2 = pair
        diffx = n1[0] - n2[0]
        diffy = n1[1] - n2[1]
        check_antinodes(n1, diffx, diffy)
        check_antinodes(n2, -diffx, -diffy)

ans = sum(1 for pos, val in cmatrix if val == "#")
print(ans)