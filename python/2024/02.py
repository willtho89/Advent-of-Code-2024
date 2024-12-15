with open('02.input', 'r') as file:
    din = file.read()


sanitized_input = [line.split() for line in din.splitlines()]


def is_safe(line):
    all_increasing = True
    all_decreasing = True

    for i in range(len(line) - 1):
        if not (-3 <= (int(line[i+1]) - int(line[i])) <= -1):
            all_decreasing = False
            break

    for i in range(len(line) - 1):
        if not (1 <= (int(line[i+1]) - int(line[i])) <= 3):
            all_increasing = False
            break

    return all_decreasing or all_increasing


ans = 0
for line in sanitized_input:
    if is_safe(line):
        ans += 1

print(ans)

# two
ans = 0
for line in sanitized_input:
    if is_safe(line):
        ans += 1
        continue

    for i in range(len(line)):
        line_copy = line.copy()
        del line_copy[i]
        if is_safe(line_copy):
            ans += 1
            break

print(ans)