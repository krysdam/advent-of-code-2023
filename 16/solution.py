
import functools

# This revisits the same configurations many times,
# but memoizing only helps a little.
@functools.lru_cache(maxsize=None)
def propogate_beam(grid: tuple, beam: tuple) -> list:
    """Where is this beam, one tick in the future, in this grid?"""
    to_add = []

    maxy, maxx = len(grid), len(grid[0])
    def add_beam(y, x, dy, dx):
        # Add the given beam to the queue of active beams,
        # If the new beam is in-bounds and not a repeat.
        if 0 <= y < maxy and 0 <= x < maxx:
            to_add.append((y, x, dy, dx))

    y, x, dy, dx = beam

    # React to the current tile.
    match grid[y][x]:
        case '.':
            # Dots are blank ground. Sail on.
            add_beam(y + dy, x + dx, dy, dx)
        case '/':
            # This type of mirror: dy, dx becomes -dx, -dy.
            add_beam(y - dx, x - dy, -dx, -dy)
        case '\\':
            # This type of mirror: dy, dx becomes dx, dy.
            add_beam(y + dx, x + dy, dx, dy)
        case '|':
            # Splitter for horizontal beams.
            # If we're moving vertically, sail on.
            if dx == 0:
                add_beam(y + dy, x + dx, dy, dx)
            # If we're moving horizontally, split.
            elif dy == 0:
                add_beam(y+1, x, 1, 0)
                add_beam(y-1, x, -1, 0)
        case '-':
            # Splitter for vertical beams.
            # If we're moving vertically, split.
            if dx == 0:
                add_beam(y, x+1, 0, 1)
                add_beam(y, x-1, 0, -1)
            # If we're moving horizontally, sail on.
            elif dy == 0:
                add_beam(y, x + dx, dy, dx)
    return to_add

def process_grid(grid: list, starting_beam: tuple) -> set:
    """How many tiles are touched by the beam starting at the given beam?"""
    active_beams = [starting_beam]
    processed_beams = set()
    touched_tiles = set()

    for beam in active_beams:
        y, x, _, _ = beam
        processed_beams.add(beam)
        touched_tiles.add((y, x))

        # Propogate the beam.
        to_add = propogate_beam(grid, beam)
        for new_beam in to_add:
            # If this beam is new, add it to the queue.
            if new_beam not in processed_beams:
                active_beams.append(new_beam)

    # Number of tiles touched by any beam.
    return len(touched_tiles)

if __name__ == '__main__':
    grid = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            grid.append(line)
    grid = tuple(grid)

    # Part 1: Start in top left, heading right
    print("Part 1:", process_grid(grid, (0, 0, 0, 1)))
            
    # Part 2: Find optimal start on the boundary moving inwards.
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
    print("Part 2:", max(possibilities))