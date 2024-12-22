from time import perf_counter
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_n_A(args: tuple[int, int, int, int, int, int, int, int]) -> int | None:
    n_A, dx_A, dy_A, dx_B, dy_B, prize_x, prize_y, restrict_range = args
    for n_B in range(restrict_range):
        x = n_A * dx_A + n_B * dx_B
        y = n_A * dy_A + n_B * dy_B
        if x == prize_x and y == prize_y:
            cost = 3 * n_A + n_B
            return cost  # Return immediately when a result is found
    return None

class Machine:
    def __init__(self, data: str) -> None:
        # Parse the input data to extract machine parameters
        lines = data.strip().splitlines()

        # Parse dx_A and dy_A
        dx_A_str, dy_A_str = lines[0].split(':')[1].split(',')
        self.dx_A = int(dx_A_str.strip()[2:])
        self.dy_A = int(dy_A_str.strip()[2:])

        # Parse dx_B and dy_B
        dx_B_str, dy_B_str = lines[1].split(':')[1].split(',')
        self.dx_B = int(dx_B_str.strip()[2:])
        self.dy_B = int(dy_B_str.strip()[2:])

        # Parse prize_x and prize_y
        prize_x_str, prize_y_str = lines[2].split(':')[1].split(',')
        self.prize_x = int(prize_x_str.strip()[2:])
        self.prize_y = int(prize_y_str.strip()[2:])

    def update_prize(self, prize_offset: int) -> None:
        """Apply an offset to the prize coordinates."""
        self.prize_x += prize_offset
        self.prize_y += prize_offset


    def find_min_cost(self, restrict_range: int = 100) -> int | None:
        """Find the cost to reach the prize coordinates using multi-core processing."""
        dx_A = self.dx_A
        dy_A = self.dy_A
        dx_B = self.dx_B
        dy_B = self.dy_B
        prize_x = self.prize_x
        prize_y = self.prize_y

        with ProcessPoolExecutor() as executor:
            futures = []
            for n_A in range(restrict_range):
                args = (n_A, dx_A, dy_A, dx_B, dy_B, prize_x, prize_y, restrict_range)
                future = executor.submit(process_n_A, args)
                futures.append(future)

            for future in as_completed(futures):
                cost = future.result()
                if cost is not None:
                    # Cancel remaining futures since we found a result
                    for f in futures:
                        f.cancel()
                    return cost  # Return immediately when a result is found

        return None

    def smart_find_min_cost(self) -> int | None:
        """Find the minimum cost to reach the prize coordinates using Diophantine equations."""
        # spoiled by reddit
        dx_A, dy_A = self.dx_A, self.dy_A
        dx_B, dy_B = self.dx_B, self.dy_B
        prize_x, prize_y = self.prize_x, self.prize_y

        # Compute the determinant
        D = dx_A * dy_B - dy_A * dx_B

        if D == 0:
            # The system has no unique solution
            return None

        # Compute n_A
        numerator_n_A = prize_x * dy_B - prize_y * dx_B
        if numerator_n_A % D != 0:
            # No integer solution
            return None
        n_A = numerator_n_A // D

        # Check if n_A is non-negative
        if n_A < 0:
            return None

        # Compute n_B
        numerator_n_B = dx_A * prize_y - dy_A * prize_x
        if numerator_n_B % D != 0:
            # No integer solution
            return None
        n_B = numerator_n_B // D

        # Check if n_B is non-negative
        if n_B < 0:
            return None

        # Compute cost
        cost = 3 * n_A + n_B

        return cost

def part1(machines: list[Machine], smart: bool) -> int:
    """Calculate total minimum cost for all machines without prize offset."""
    total_cost = 0
    for machine in machines:
        if smart:
            min_cost = machine.smart_find_min_cost()
        else:
            min_cost = machine.find_min_cost()
        if min_cost is not None:
            total_cost += min_cost
    return total_cost

def part2(machines: list[Machine], smart: bool) -> int:
    """Calculate total minimum cost for all machines with a prize offset."""
    prize_offset = 10_000_000_000_000
    total_cost = 0
    for machine in machines:
        machine.update_prize(prize_offset)
        if smart:
            min_cost = machine.smart_find_min_cost()
        else:
            min_cost = machine.find_min_cost(restrict_range=10**6)

        if min_cost is not None:
            total_cost += min_cost
    return total_cost

with open('13.input', 'r') as file:
    din: str = file.read()
    machines_data = din.strip().split('\n\n')
    machines: list[Machine] = [Machine(data) for data in machines_data]

# Measure time for Part One
p1_start = perf_counter()
print(f"Part One (Smart): {part1(machines, True)}")
p1_end = perf_counter()
print(f"Elapsed Time (Part One (Smart)): {p1_end - p1_start:0.2f}s")

# Measure time for Part One (dumb)
p1_start = perf_counter()
print(f"Part One: {part1(machines, False)}")
p1_end = perf_counter()
print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")

# Measure time for Part Two
p2_start = perf_counter()
print(f"Part Two (Smart): {part2(machines, True)}")
p2_end = perf_counter()
print(f"Elapsed Time (Part Two (Smart)): {p2_end - p2_start:0.2f}s")

# Measure time for Part Two (dumb)
p2_start = perf_counter()
print(f"Part Two: {part2(machines, False)}")
p2_end = perf_counter()
print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")

