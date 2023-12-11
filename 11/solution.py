def find_empty_rows_and_columns(galaxies: list, height: int, width: int) -> tuple:
    """Find the empty rows and columns in the map."""
    # Find the occupied rows and columns.
    occupied_rows = set()
    occupied_columns = set()
    for y, x in galaxies:
        occupied_rows.add(y)
        occupied_columns.add(x)
    # Empty rows and columns are the rest.
    empty_rows = [y for y in range(height) if y not in occupied_rows]
    empty_columns = [x for x in range(width) if x not in occupied_columns]
    return empty_rows, empty_columns

def shortest_path_length(y1: int, x1: int, y2: int, x2: int, empty_rows: list, empty_columns: list, factor: int) -> int:
    """Find the shortest path length, expanding empty rows and columns by a factor."""
    path_length = 0
    # Start at point 1
    y, x = y1, x1

    # Move vertically.
    # (This is guaranteed to be optimal,
    # because we can't be in an empty column.)
    direction = 1 if y2 > y1 else -1
    while y != y2:
        y += direction
        if y in empty_rows:
            path_length += factor
        else:
            path_length += 1

    # Now move horizontally.
    # (Again optimal, because we can't be in an empty row.)
    direction = 1 if x2 > x1 else -1
    while x != x2:
        x += direction
        if x in empty_columns:
            path_length += factor
        else:
            path_length += 1
    return path_length

def find_galaxies(map: list) -> list:
    """Find the galaxies in the map."""
    galaxies = []
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell == '#':
                galaxies.append((i, j))
    return galaxies

def find_total_distance(galaxies: list, empty_rows: list, empty_columns: list, factor: int) -> int:
    """Find the total distance between all galaxies."""
    total_length = 0
    for i, (y1, x1) in enumerate(galaxies):
        for y2, x2 in galaxies[i+1:]:
            total_length += shortest_path_length(y1, x1, y2, x2, empty_rows, empty_columns, factor)
    return total_length

if __name__ == '__main__':
    map = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            map.append(line)

    # Find galaxies and empty rows and columns.
    galaxies = find_galaxies(map)
    map_height, map_width = len(map), len(map[0])
    empty_rows, empty_columns = find_empty_rows_and_columns(galaxies, map_height, map_width)

    # Find the total distance.
    print("Part 1:", find_total_distance(galaxies, empty_rows, empty_columns, 2))
    print("Part 2:", find_total_distance(galaxies, empty_rows, empty_columns, 1000000))