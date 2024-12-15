import re

with open('03.input', 'r') as file:
    din = file.read()

pattern = r'mul\((\d+),(\d+)\)'
matches = re.findall(pattern, din)

total_sum = 0

for match in matches:
    num1, num2 = map(int, match)
    total_sum += num1 * num2

print("Total sum:", total_sum)


# Input string
# din = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
do_pattern = re.compile(r'do\(\)')
dont_pattern = re.compile(r"don't\(\)")

enabled = True
total_sum = 0

tokens = re.split(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', din)

for token in tokens:
    if not token:
        continue
    if do_pattern.fullmatch(token):
        enabled = True
    elif dont_pattern.fullmatch(token):
        enabled = False
    
    # Check for mul instructions
    elif enabled and (match := mul_pattern.fullmatch(token)):
        num1, num2 = map(int, match.groups())
        total_sum += num1 * num2

print("Total sum:", total_sum)