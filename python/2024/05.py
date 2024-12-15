
ans = 0
rules = []

with open('05.input', 'r') as file:
    din = file.read().splitlines()

for line in din:
    line = line.strip()
    if '|' in line:
        rules.append(line.split('|'))
    elif line != '':
        line = line.split(',')
        for rule in rules:
            if rule[0] in line and rule[1] in line and line.index(rule[0]) > line.index(rule[1]):
                break
        else:
            ans += int(line[len(line) // 2])
print(ans)

from functools import cmp_to_key
def cmp(a, b):
    for r in rules:
        if (r[0], r[1]) == (a, b):
            return -1
        if (r[1], r[0]) == (a, b):
            return 1
    return 0

ans = 0
rules = []
for line in din:
    line = line.strip()
    if '|' in line:
        rules.append(line.split('|'))
    elif line != '':
        line = line.split(',')
        line_sorted = sorted(line, key=cmp_to_key(cmp))
        if line != line_sorted:
            ans += int(line_sorted[len(line) // 2])
print(ans)