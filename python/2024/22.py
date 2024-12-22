from time import perf_counter

MOD = 16777216  # 2^24

def next_secret(secret_number: int) -> int:
    value1 = secret_number * 64
    secret_number ^= value1
    secret_number %= MOD

    value2 = secret_number // 32  # Integer division, rounds down
    secret_number ^= value2
    secret_number %= MOD

    value3 = secret_number * 2048
    secret_number ^= value3
    secret_number %= MOD

    return secret_number

def generate_secrets(initial_secret: int, iterations: int) -> list[int]:
    secrets = []
    secret_number = initial_secret
    for _ in range(iterations):
        secret_number = next_secret(secret_number)
        secrets.append(secret_number)
    return secrets

def generate_prices(initial_secret: int, num_prices: int) -> list[int]:
    prices = []
    secret_number = initial_secret
    for _ in range(num_prices):
        price = secret_number % 10  # Ones digit
        prices.append(price)
        secret_number = next_secret(secret_number)
    return prices



with open('22.input', 'r') as file:
    content = file.read()
    initial_secrets: list[int] = [
        int(line.strip()) for line in content.strip().split('\n') if line.strip()
    ]

# Part One
p1_start = perf_counter()
total_sum = 0
for initial_secret in initial_secrets:
    # Simulate 2000 iterations for each buyer
    secret_number = initial_secret
    for _ in range(2000):
        secret_number = next_secret(secret_number)
    total_sum += secret_number
p1_end = perf_counter()
print(f"Part One: {total_sum}")

# Part Two
sequence_totals: dict[tuple[int, int, int, int], int] = {}

for initial_secret in initial_secrets:
    num_prices = 2001  # Initial price plus 2000 more
    secret_number = initial_secret
    prices = []
    for _ in range(num_prices):
        price = secret_number % 10  # Ones digit
        prices.append(price)
        secret_number = next_secret(secret_number)

    # Generate price changes
    price_changes = [
        prices[i + 1] - prices[i] for i in range(len(prices) - 1)
    ]

    # Record earliest occurrence of each sequence for this buyer
    buyer_sequences: dict[tuple[int, int, int, int], int] = {}
    for i in range(len(price_changes) - 3):
        sequence = (
            price_changes[i],
            price_changes[i + 1],
            price_changes[i + 2],
            price_changes[i + 3],
        )
        if sequence not in buyer_sequences:
            sell_price = prices[i + 4]
            buyer_sequences[sequence] = sell_price

    # Update global sequence totals
    for sequence, sell_price in buyer_sequences.items():
        if sequence in sequence_totals:
            sequence_totals[sequence] += sell_price
        else:
            sequence_totals[sequence] = sell_price

# Find the sequence with the maximum total bananas collected
max_bananas = 0
best_sequence = None
for sequence, total_bananas in sequence_totals.items():
    if total_bananas > max_bananas:
        max_bananas = total_bananas
        best_sequence = sequence

p2_end = perf_counter()
print(f"Part Two: {max_bananas}")

print(f"Elapsed Time (Part One): {p1_end - p1_start:.2f}s")
print(f"Elapsed Time (Part Two): {p2_end - p1_end:.2f}s")
print(f"Total Execution Time: {p2_end - p1_start:.2f}s")
