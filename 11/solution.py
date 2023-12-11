def find_empty_rows_and_columns(galaxies: list) -> tuple:
    """Find the empty rows and columns in the map."""
    # Find the occupied rows and columns.
    occupied_rows = {y for y, x in galaxies}
    occupied_columns = {x for y, x in galaxies}
    # Empty rows and columns are the rest.
    empty_rows = set(range(max(occupied_rows))) - occupied_rows
    empty_columns = set(range(max(occupied_columns))) - occupied_columns
    return empty_rows, empty_columns

def expand_map(galaxies: list, empty_rows: list, empty_columns: list, factor: int) -> list:
    """Expand the map's empty rows and columns by a factor."""
    new_galaxies = []
    for y, x in galaxies:
        newy, newx = y, x
        # For every row or column before this galaxy,
        # that row or column counts 'factor' times as much.
        for r in empty_rows:
            if r < y:
                newy += factor - 1
        for c in empty_columns:
            if c < x:
                newx += factor - 1
        new_galaxies.append((newy, newx))
    return new_galaxies

def find_galaxies(map: list) -> list:
    """Find the galaxies in the map."""
    galaxies = []
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell == '#':
                galaxies.append((i, j))
    return galaxies

def find_total_distance(galaxies: list) -> int:
    """Find the total distance between all galaxies."""
    total_length = 0
    for i, (y1, x1) in enumerate(galaxies):
        for y2, x2 in galaxies[i+1:]:
            # Manhattan distance.
            total_length += abs(y1 - y2) + abs(x1 - x2)
    return total_length

if __name__ == '__main__':
    map = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            map.append(line)

    # Find galaxies and empty rows and columns.
    galaxies = find_galaxies(map)
    empty_rows, empty_columns = find_empty_rows_and_columns(galaxies)

    # Part 1: expand by a factor of two
    galaxies2 = expand_map(galaxies, empty_rows, empty_columns, 2)
    print("Part 1:", find_total_distance(galaxies2))

    # Part 2: expand by a factor of 1000000
    galaxies1000000 = expand_map(galaxies, empty_rows, empty_columns, 1000000)
    print("Part 2:", find_total_distance(galaxies1000000))