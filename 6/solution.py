def pull_numbers(s: str) -> list:
    """Pull the numbers out of the given string."""
    return [int(x) for x in s.split() if x.isdigit()]

def round_up(x: float) -> int:
    """Round x up to the next integer."""
    i = int(x)
    if x > i: i += 1
    return i

def how_many_ways(time: int, dist: int) -> int:
    """How many ways can I beat this record distance in this time?"""
    # i * (time - i) >= dist
    # i * time - i^2 >= dist
    # i^2 - i * time + dist <= 0
    # i = (time +/- sqrt(time^2 - 4 * dist)) / 2
    root1 = (time - (time**2 - 4 * dist)**0.5) / 2
    root2 = (time + (time**2 - 4 * dist)**0.5) / 2

    # root1 is the first integer that wins.
    root1 = round_up(root1)
    # root2 is the last integer that wins.
    root2 = int(root2)
    return root2 - root1 + 1

if __name__ == '__main__':
    # Read the times and distances
    times = []
    distances = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('Time:'):
                times = pull_numbers(line)
            elif line.startswith('Distance:'):
                distances = pull_numbers(line)

    # Part 1: four separate races
    ways = [how_many_ways(time, dist) for time, dist in zip(times, distances)]
    product = 1
    for way in ways:
        product *= way
    print("Part 1:", product)

    # Part 2: one big race
    time = int(''.join(str(x) for x in times))
    dist = int(''.join(str(x) for x in distances))
    print("Part 2:", how_many_ways(time, dist))