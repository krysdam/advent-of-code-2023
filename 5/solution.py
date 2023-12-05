def apply_map(map: list, x: int) -> int:
    """Apply this map to the given starting value.
    
    map: a list of (dest, source, len) map-ranges.
    x: a value (eg, a seed number or a soil number).
    """
    for dest, source, length in map:
        if source <= x < source + length:
            return dest + (x - source)
    return x

def apply_maps(maps: list, x: int) -> int:
    """Apply all maps to the given starting value."""
    for map in maps:
        x = apply_map(map, x)
    return x

def pull_numbers(s: str) -> list:
    """Pull the numbers out of the given string."""
    return [int(x) for x in s.split() if x.isdigit()]

if __name__ == '__main__':
    # Store the maps
    maps = []
    current_map = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if line == '':
                continue

            # Read the seeds
            if line.startswith('seeds:'):
                seeds = pull_numbers(line)

            # If a line starts with a digit, it's a mapping line
            if line[0].isdigit():
                # Parse the mapping line
                dest, source, length = pull_numbers(line)
                current_map.append((dest, source, length))
            
            # If it starts with anything else, that map is done
            else:
                maps.append(current_map)
                current_map = []

        # At EOF, append the last map
        maps.append(current_map)

    # Apply the maps to the seeds
    locations = [apply_maps(maps, seed) for seed in seeds]
    # After applying all maps, these values are the locations

    # Part 1: the minimum location
    print("Part 1:", min(locations))

    # Part 2: the seeds have ranges
    seed_range_starts = seeds[::2]
    seed_range_lens = seeds[1::2]

    # Find the minimum outcome of applying the maps to each seed range
    min_so_far = None
    for start, length in zip(seed_range_starts, seed_range_lens):
        print("map")
        for seed in range(start, start+length):
            if (seed-start) % 1000000 == 0:
                print("Percent: ", (seed-start) / (length) * 100)
            location = apply_maps(maps, seed)
            if min_so_far is None or location < min_so_far:
                min_so_far = location
    print("Part 2:", min_so_far)