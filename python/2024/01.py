with open('01.input', 'r') as file:
    din = file.read()

# Split the contents on line endings
lines = din.splitlines()


left = []
right = []

ans = 0
for line in lines:
    line = line.split()
    left.append(int(line[0]))
    right.append(int(line[1]))

left = sorted(left)
right = sorted(right)

for i in range(len(left)):
    ans += abs(left[i] - right[i])

print(f"A: {ans}")

ans = 0

left = sorted(left)
right = sorted(right)

for i in range(len(left)):
    ans += left[i] * right.count(left[i])

print(f"B: {ans}")