import os
from typing import List, Tuple
import re
from time import perf_counter, sleep
from copy import deepcopy

MAP_WIDTH = 101
MAP_HEIGHT = 103

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Robot:
    def __init__(self, position: Tuple[int, int], velocity: Tuple[int, int]):
        self.position: Tuple[int, int] = position
        self.velocity: Tuple[int, int] = velocity

    @classmethod
    def from_line(cls, line: str) -> "Robot":
        match = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
        if match:
            x_str, y_str, vx_str, vy_str = match.groups()
            x, y, vx, vy = int(x_str), int(y_str), int(vx_str), int(vy_str)
            return cls((x, y), (vx, vy))
        else:
            raise ValueError(f"Cannot parse line: {line}")

    def move(self) -> None:
        x, y = self.position
        vx, vy = self.velocity
        x = (x + vx) % MAP_WIDTH
        y = (y + vy) % MAP_HEIGHT
        self.position = (x, y)

def part1(robots: List[Robot]) -> int:
    robots = deepcopy(robots)  # To avoid modifying the original list
    mid_x = MAP_WIDTH // 2   # 50
    mid_y = MAP_HEIGHT // 2  # 51

    for _ in range(100):
        for robot in robots:
            robot.move()

    q1 = q2 = q3 = q4 = 0
    for robot in robots:
        x, y = robot.position
        if x == mid_x or y == mid_y:
            continue  # Ignore robots on middle lines
        elif x > mid_x and y < mid_y:
            q1 += 1
        elif x < mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        elif x > mid_x and y > mid_y:
            q4 += 1
    safety_factor = q1 * q2 * q3 * q4
    return safety_factor

def part2(robots: List[Robot]) -> int:
    robots = deepcopy(robots)  # To avoid modifying the original list
    t = 0
    last_area = None
    while True:
        for robot in robots:
            robot.move()
        t += 1

        xs = [robot.position[0] for robot in robots]
        ys = [robot.position[1] for robot in robots]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        area = (max_x - min_x) * (max_y - min_y)

        grid = [['.' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
        for robot in robots:
            x, y = robot.position
            grid[y - min_y][x - min_x] = '#'
        grid_str = '\n'.join(''.join(row) for row in grid)
        if '##########' in grid_str:
            print(grid_str)
            return t

        if last_area is not None and area > last_area:
            pass  # Continue searching
        last_area = area

    return t

if __name__ == "__main__":
    with open('14.input', 'r') as file:
        din: str = file.read()
        lines = din.strip().split('\n')
        robots: List[Robot] = [Robot.from_line(line) for line in lines]

    # Measure time for Part One
    p1_start = perf_counter()
    print(f"Part One: {part1(robots)}")
    p1_end = perf_counter()

    # Measure time for Part Two
    p2_start = perf_counter()
    print(f"Part Two: {part2(robots)}")
    p2_end = perf_counter()

    print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")
    print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")