from collections import deque
from time import perf_counter

def initialize_dicts():
    keys = ["A"] + [str(y) for y in range(10)]
    keypad_locations = {
        "7": (0, 3), "8": (1, 3), "9": (2, 3),
        "4": (0, 2), "5": (1, 2), "6": (2, 2),
        "1": (0, 1), "2": (1, 1), "3": (2, 1),
        "0": (1, 0), "A": (2, 0)
    }
    arrow_locations = {
        "<": (0, 0), ">": (2, 0), "V": (1, 0),
        "^": (1, 1), "A": (2, 1)
    }
    directions = {"^": (0, 1), "V": (0, -1), "<": (-1, 0), ">": (1, 0)}
    return keys, keypad_locations, arrow_locations, directions

def bfs_key(start, finish, loc_dict, directions):
    start_point = loc_dict[start]
    end_point = loc_dict[finish]
    frontier = deque([(0, start_point, "")])
    score = None
    return_list = []

    while frontier:
        distance, location, history = frontier.popleft()
        if score is not None and distance > score:
            break
        if location == end_point:
            history += "A"
            score = distance
            return_list.append(history)
            continue
        if location not in loc_dict.values():
            continue

        x, y = location
        for c in directions:
            dx, dy = directions[c]
            new_loc = (x + dx, y + dy)
            if new_loc not in loc_dict.values():
                continue
            new_history = history + c
            frontier.append((distance + 1, new_loc, new_history))

    return tuple(return_list)

def build_keypad_dict(keys, keypad_locations, directions):
    keypad_dict = {}
    for c in keys:
        for d in keys:
            key_pair = c + d
            if c == d:
                keypad_dict[key_pair] = ("A",)
                continue
            path_tuple = bfs_key(c, d, keypad_locations, directions)
            keypad_dict[key_pair] = path_tuple
    return keypad_dict

def build_arrow_dict(arrow_locations, directions):
    arrow_dict = {}
    for c in arrow_locations:
        for d in arrow_locations:
            key_pair = c + d
            if c == d:
                arrow_dict[key_pair] = ("A",)
                continue
            path_tuple = bfs_key(c, d, arrow_locations, directions)
            arrow_dict[key_pair] = path_tuple

    # Adjustments for specific arrow paths
    arrow_dict.update({
        "<A": ('>>^A',), ">^": ('<^A',), "VA": ('^>A',),
        "^>": ('V>A',), "A<": ('V<<A',), "AV": ('<VA',)
    })
    for a in arrow_dict:
        arrow_dict[a] = arrow_dict[a][0]
    return arrow_dict

def button_presses(string, cypher, last, keypad_dict, arrow_dict):
    string = "A" + string
    return_list = [""]
    last_count = 0
    for t in range(len(string) - 1):
        string_pair = string[t:t + 2]
        if cypher == "Keypad":
            branch_tuple = keypad_dict[string_pair]
        else:
            new_string = arrow_dict[string_pair]

        if last:
            last_count += len(new_string)
            return_list[0] += new_string
            continue

        if cypher == "Keypad":
            new_return_list = []
            for g in branch_tuple:
                for r in return_list:
                    new_return_list.append(r + g)
            return_list = new_return_list
        else:
            return_list[0] += new_string

    if last:
        return last_count, return_list
    return tuple(return_list)

def process_code_list(code_list, keypad_dict, arrow_dict, part2_dict):
    part1_answer = 0
    part2_answer = 0

    for code in code_list:
        first_set = set(button_presses(code, "Keypad", False, keypad_dict, arrow_dict))

        second_set = set()
        for c in first_set:
            new_set = set(button_presses(c, "Arrows", False, keypad_dict, arrow_dict))
            second_set |= new_set

        min_length = float('inf')
        third_set = set()
        for c in second_set:
            new_len, _ = button_presses(c, "Arrows", True, keypad_dict, arrow_dict)
            if new_len < min_length:
                min_length = new_len
                third_set = {c}
            elif new_len == min_length:
                third_set.add(c)

        final_len = float('inf')
        for f in third_set:
            code_dict = {a: 0 for a in arrow_dict}
            new_string = button_presses(f, "Arrows", False, keypad_dict, arrow_dict)[0]
            for t in range(len(new_string) - 1):
                substring = new_string[t:t + 2]
                code_dict[substring] += 1
            first_letter = new_string[0]

            for _ in range(23):
                new_dict = {a: 0 for a in arrow_dict}
                first_string = "A" + first_letter
                code_dict[first_string] += 1
                first_letter = part2_dict[first_string][0][1]
                remove_string = part2_dict[first_string][0]
                for c in code_dict:
                    for g in part2_dict[c]:
                        new_dict[g] += code_dict[c]
                new_dict[remove_string] -= 1
                code_dict = new_dict.copy()

            new_len = sum(code_dict.values()) + 1
            if new_len < final_len:
                final_len = new_len

        integer = int(code[:-1])
        part1_answer += integer * min_length
        part2_answer += integer * final_len

    return part1_answer, part2_answer

with open("21.input", "r") as data:
     code_list = [line.strip() for line in data]
keys, keypad_locations, arrow_locations, directions = initialize_dicts()

# Build dictionaries
keypad_dict = build_keypad_dict(keys, keypad_locations, directions)
arrow_dict = build_arrow_dict(arrow_locations, directions)

# Prepare Part2Dict
part2_dict = {}
for a in arrow_dict:
    new_list = []
    string = arrow_dict[a]
    if len(string) == 1:
        part2_dict[a] = ("AA",)
        continue
    for t in range(len(string)):
        substring = "A" + string[0] if t == 0 else string[t-1:t+1]
        new_list.append(substring)
    part2_dict[a] = tuple(new_list)

# Measure performance
start_time = perf_counter()
part1_answer, part2_answer = process_code_list(code_list, keypad_dict, arrow_dict, part2_dict)
end_time = perf_counter()

print(f"Part 1 Answer: {part1_answer}")
print(f"Part 2 Answer: {part2_answer}")
print(f"Total Execution Time: {end_time - start_time:.2f}s")