def roll_row_east(row: str) -> str:
    """Roll all round rocks west on this row."""
    # Slightly silly, but simple.
    # If this becomes inefficient, memoize it.
    while 'O.' in row:
        row = row.replace('O.', '.O')
    return row

def roll_platform_east(platform: list) -> list:
    """Roll all round rocks west on this platform."""
    return [roll_row_east(row) for row in platform]

def rotate_clockwise(platform: list) -> list:
    """Rotate the given platform clockwise."""
    return [''.join(row) for row in zip(*platform[::-1])]

def apply_spin_cycle(platform: list) -> list:
    """Roll the plaform North, then West, then South, then East."""
    # Put North to the east, then roll east.
    # Continue with West, South, and East.
    for _ in range(4):
        platform = rotate_clockwise(platform)
        platform = roll_platform_east(platform)
    return platform

def find_load_on_north(platform: list) -> int:
    """Find the total weight on the north beams (see problem description)."""
    height = len(platform)
    total = 0
    for i, row in enumerate(platform):
        total += (height - i) * row.count('O')
    return total

def weight_on_north_after_N_cycles(platform: list, n: int) -> int:
    """Find the weight on the north after N spin cycles."""
    # Record each platform arrangement we've seen,
    # and how many spin-cycles had completed at that point.
    # We'll use this to find the start and length of the cycle.
    past_platforms = {tuple(platform): 0}
    for r in range(n):
        platform = apply_spin_cycle(platform)
        if tuple(platform) in past_platforms:
            cycle_start = past_platforms[tuple(platform)]
            cycle_length = r+1 - cycle_start
            break
        past_platforms[tuple(platform)] = r+1
    # Now that we know the cycle, we can find a much lower n
    # which results in the same answer as our actual n.
    equivalent_n = cycle_start + (n - cycle_start) % cycle_length
    for platform2, r in past_platforms.items():
        if r == equivalent_n:
            return find_load_on_north(platform2)

if __name__ == '__main__':
    platform = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            platform.append(line)

    # Part 1: roll north, then find load
    platform1 = platform.copy()
    platform1 = rotate_clockwise(platform1)
    platform1 = roll_platform_east(platform1)
    platform1 = rotate_clockwise(platform1)
    platform1 = rotate_clockwise(platform1)
    platform1 = rotate_clockwise(platform1)
    print("Part 1:", find_load_on_north(platform1))

    # Part 2: a billion spin cycles, then find load
    platform2 = platform.copy()
    print("Part 2:", weight_on_north_after_N_cycles(platform2, 1000000000))