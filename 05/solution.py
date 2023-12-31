class Map:
    """A map from one range of numbers to another, per the problem."""
    def __init__(self, dest_source_lens: list):
        """Initialize this map from a list of (dest, source, len) tuples."""
        # We're given a map as a list of (dest, source, len) tuples.
        # But instead,
        # Represent it as a list of (start, end, delta) tuples.
        # If x is in the range [start, end), then apply(x) = x + delta.
        # This makes it simpler to apply the map to a range.
        segments = []
        for dest, source, length in dest_source_lens:
            segments.append((source, source+length, dest-source))

        # Sort by start value
        segments.sort(key=lambda x: x[0])

        # Fill in any gaps with segments that add zero
        last_end = 0
        new_segments = []
        for start, end, delta in segments:
            if start > last_end:
                new_segments.append((last_end, start, 0))
            new_segments.append((start, end, delta))
            last_end = end
        new_segments.append((last_end, float('inf'), 0))

        self.segments = new_segments

    def apply(self, x: int) -> int:
        """Apply this map to the given starting value."""
        for start, end, delta in self.segments:
            if start <= x < end:
                return x + delta
        return x
    
    def apply_to_ranges(self, ranges: list) -> list:
        """Apply this map to the given ranges."""
        # First, break each range into smaller ranges,
        # Such that each part is entirely within some mapping segment.
        # Then map each of these ranges through directly.
        mapped_ranges = []
        for start, end in ranges:
            # Break on all segment-starts within this range.
            break_points = [s for s, e, d in self.segments if start < s < end]
            # Also break on the range start and end.
            break_points = [start] + break_points + [end]
            # Break the range on these break points.
            range_parts = [(break_points[i], break_points[i+1]) for i in range(len(break_points)-1)]
            # Map the smaller ranges.
            mapped_range_parts = []
            for part_start, part_end in range_parts:
                # Map the first value directly.
                mapped_part_start = self.apply(part_start)
                # The last actual value is (end - 1)
                # So map that, then add one for the new "end."
                mapped_part_end = self.apply(part_end - 1) + 1
                mapped_range_parts.append((mapped_part_start, mapped_part_end))
            mapped_ranges.extend(mapped_range_parts)
        return mapped_ranges

def apply_maps(maps: list, x: int) -> int:
    """Apply all maps to the given starting value."""
    for map in maps:
        x = map.apply(x)
    return x

def apply_maps_to_ranges(maps: list, ranges: list) -> list:
    """Apply all maps to the given ranges."""
    for map in maps:
        ranges = map.apply_to_ranges(ranges)
    return ranges

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
            if line == '':
                continue

            # Read the seeds
            if line.startswith('seeds:'):
                seeds = pull_numbers(line)

            # If a line starts with a digit, it's a mapping line
            if line[0].isdigit():
                dest, source, length = pull_numbers(line)
                current_map.append((dest, source, length))
            
            # If it starts with anything else, that map is done
            else:
                maps.append(Map(current_map))
                current_map = []

        # At EOF, append the last map
        maps.append(Map(current_map))

    # Part 1: the seeds are starting values
    # Apply all maps to all seeds to get the list of locations
    locations = [apply_maps(maps, seed) for seed in seeds]
    print("Part 1:", min(locations))

    # Part 2: the seeds are ranges
    # The seed numbers are really (start, length) pairs.
    seed_ranges = [(seeds[i], seeds[i] + seeds[i+1]) for i in range(0, len(seeds), 2)]
    # Apply the maps to the ranges.
    ranges = apply_maps_to_ranges(maps, seed_ranges)
    # Find the smallest value of any of these ranges.
    total_min = min([start for start, end in ranges])

    print("Part 2:", total_min)