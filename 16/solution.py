def process_grid(grid: list, starting_beam: tuple) -> set:
    """Find how many tiles are visited by the beam starting at the given beam."""
    # Bounds of the grid
    maxy, maxx = len(grid), len(grid[0])

    beams = [starting_beam]

    def add_beam(y, x, dy, dx):
        # Add the given beam to the queue of active beams,
        # If the new beam is in-bounds and not a repeat.
        if 0 <= y < maxy and 0 <= x < maxx:
            beam = (y, x, dy, dx)
            if beam not in beams:
                beams.append(beam)

    # Track which tiles are touched.
    visited = set()

    # Traverse the queue of active beams.
    for beam in beams:
        y, x, dy, dx = beam
        visited.add((y, x))

        # React to the current tile.
        match grid[y][x]:
            case '.':
                # Sail on.
                add_beam(y + dy, x + dx, dy, dx)
            case '/':
                # Swap dy and dx, and invert.
                add_beam(y - dx, x - dy, -dx, -dy)
            case '\\':
                # Swap dy and dx.
                add_beam(y + dx, x + dy, dx, dy)
            case '|':
                # If we're moving vertically, sail on.
                if dx == 0:
                    add_beam(y + dy, x + dx, dy, dx)
                # If we're moving horizontally, split.
                elif dy == 0:
                    add_beam(y+1, x, 1, 0)
                    add_beam(y-1, x, -1, 0)
            case '-':
                # If we're moving vertically, split.
                if dx == 0:
                    add_beam(y, x+1, 0, 1)
                    add_beam(y, x-1, 0, -1)
                # If we're moving horizontally, sail on.
                elif dy == 0:
                    add_beam(y, x + dx, dy, dx)
    # Number of tiles touched by any beam.
    return len(visited)

if __name__ == '__main__':
    grid = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            grid.append(line)

    # Part 1: Start in top left, heading right
    print("Part 1:", process_grid(grid, (0, 0, 0, 1)))
            
    # Part 2: Find optimal start
    possibilities = []
    for y in range(len(grid)):
        # Start along the left edge, heading right.
        possibilities.append(process_grid(grid, (y, 0, 0, 1)))
        # Start along the right edge, heading left.
        possibilities.append(process_grid(grid, (y, len(grid[0])-1, 0, -1)))
    for x in range(len(grid[0])):
        # Start along the top edge, heading down.
        possibilities.append(process_grid(grid, (0, x, 1, 0)))
        # Start along the bottom edge, heading up.
        possibilities.append(process_grid(grid, (len(grid)-1, x, -1, 0)))
    print(max(possibilities))   