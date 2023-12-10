# Note on coordinates:
# y = row number. Positive is down.
# x = column number. Positive is right.

# For each pipe type,
# Which relative coordinates does it attach to?
CONNECTIONS = {'|': [(-1, 0), (1, 0)],
               '-': [(0, -1), (0, 1)],
               'L': [(-1, 0), (0, 1)],
               'J': [(-1, 0), (0, -1)],
               '7': [(1, 0), (0, -1)],
               'F': [(1, 0), (0, 1)],
               # Ground connects to nothing
               '.': [],
               # S connects to anything
               'S': [(-1, 0), (1, 0), (0, -1), (0, 1)]
            }

def is_in_bounds(map: list, y: int, x: int) -> bool:
    """Is the given coordinate in bounds?"""
    return 0 <= y < len(map) and 0 <= x < len(map[0])

def find_adjacent_tiles(map: list, tiles: list, loop: list) -> list:
    """Find all tiles with paths to the given tiles, not crossing the loop."""
    for y, x in tiles:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                candidate_y = y + dy
                candidate_x = x + dx
                # If it's out of bounds, skip it
                if not is_in_bounds(map, candidate_y, candidate_x):
                    continue
                # If it's already checked, skip it
                if (candidate_y, candidate_x) in tiles:
                    continue
                # If it's on the loop, skip it
                if (candidate_y, candidate_x) in loop:
                    continue
                # Else, add it
                tiles.append((candidate_y, candidate_x))
    return tiles

def are_connected_pipes(map: list, y1: int, x1: int, y2: int, x2: int) -> bool:
    """In the given map, are the given tiles connected pipes?"""
    # If either part is out of bounds, they aren't connected
    if not is_in_bounds(map, y1, x1) or not is_in_bounds(map, y2, x2):
        return False
    # Else, find the pipe types
    part1 = map[y1][x1]
    part2 = map[y2][x2]
    # Find the relative coordinates
    dy = y2 - y1
    dx = x2 - x1
    # Part 1 must connect to part 2,
    # and part 2 must connect to part 1
    return (dy, dx) in CONNECTIONS[part1] and (-dy, -dx) in CONNECTIONS[part2]

def find_loop_parts(map: list) -> list:
    """Given a map, find all coordinates on the big loop (see puzzle).
    
    Output is guaranteed to be in connectivity order."""
    loop_parts = []
    # Find the starting "S"
    for y, row in enumerate(map):
        for x, char in enumerate(row):
            if char == 'S':
                loop_parts.append((y, x))
    # Expand from there
    for party, partx in loop_parts:
        part = map[party][partx]
        connections = CONNECTIONS[part]
        for dy, dx in connections:
            candidate_y = party + dy
            candidate_x = partx + dx
            # If it's out of bounds, skip it
            if not is_in_bounds(map, candidate_y, candidate_x):
                continue
            # If it's already checked, skip it
            if (candidate_y, candidate_x) in loop_parts:
                continue
            # If it's not connected, skip it
            if not are_connected_pipes(map, party, partx, candidate_y, candidate_x):
                continue
            # Else, add it to the list
            loop_parts.append((candidate_y, candidate_x))
            # If the current part is S, only connect once from it
            # (This ensures the loop is listed in connectivity order)
            if part == 'S':
                break
    return loop_parts
    
def count_enclosed_area(map: list, loop_parts: list) -> int:
    """Given a map and a list of loop parts, count the tiles inside the loop."""
    # Walk around the loop in one direction,
    # recording all non-loop tiles to the "right" of the loop's path,
    # relative to the direction of travel.
    # In general, the inside might be the left or the right.
    # Determining which is tricky.
    # But I know that for this input, it's the right.
    tiles_on_right = set()
    # We'll use those to find all the other enclosed tiles.
    for p, (party, partx) in enumerate(loop_parts):
        # Find the tile to my right, as I enter this tile
        prevy, prevx = loop_parts[(p - 1) % len(loop_parts)]
        dy = party - prevy
        dx = partx - prevx
        righty = party + dx
        rightx = partx - dy
        tiles_on_right.add((righty, rightx))

        # Find the tile to my right, as I exit this tile
        nexty, nextx = loop_parts[(p + 1) % len(loop_parts)]
        dy = nexty - party
        dx = nextx - partx
        righty = party + dx
        rightx = partx - dy
        tiles_on_right.add((righty, rightx))
    # Remove tiles on the loop.
    tiles_on_right = tiles_on_right - set(loop_parts)
    # Now we have every enclosed tile that touches the loop.
    # Use these to find every enclosed tile.
    enclosed_tiles = find_adjacent_tiles(map, list(tiles_on_right), loop_parts)
    return len(enclosed_tiles)

if __name__ == '__main__':
    maze = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            maze.append(line)

    loop = find_loop_parts(maze)

    # Part 1: diameter of the loop
    # (4 components means 2, and 3 components means 1)
    print("Part 1:", len(loop) // 2)

    # Part 2: area inside the loop
    print("Part 2:", count_enclosed_area(maze, loop))