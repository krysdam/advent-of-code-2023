def pull_numbers(s: str) -> list:
    """Pull the numbers out of the given string."""
    return [int(x) for x in s.split() if x.isdigit()]

def find_empty_rows_and_columns(map: list) -> tuple:
    """Find the empty rows and columns in the map."""
    empty_rows = []
    empty_columns = []

    for i, row in enumerate(map):
        if '#' not in row:
            empty_rows.append(i)
    for i, column in enumerate(zip(*map)):
        if '#' not in column:
            empty_columns.append(i)

    return empty_rows, empty_columns

def shortest_path_length(map: list, y1: int, x1: int, y2: int, x2: int, empty_rows: list, empty_columns: list) -> int:
    """Find the shortest path length."""
    path_length = 0
    y, x = y1, x1
    while y != y2:
        if y < y2:
            y += 1
        else:
            y -= 1
        path_length += 1
        if y in empty_rows:
            path_length += 999999

    while x != x2:
        if x < x2:
            x += 1
        else:
            x -= 1
        path_length += 1
        if x in empty_columns:
            path_length += 999999
    return path_length

def find_galaxies(map: list) -> list:
    """Find the galaxies in the map."""
    galaxies = []
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell == '#':
                galaxies.append((i, j))
    return galaxies


if __name__ == '__main__':
    map = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            map.append(line)

    empty_rows, empty_columns = find_empty_rows_and_columns(map)

    total_length = 0
    galaxies = find_galaxies(map)
    for i1, g1 in enumerate(galaxies):
        for i2, g2 in enumerate(galaxies):
            if i1 >= i2:
                continue
            if g1 == g2:
                continue
            path_length = shortest_path_length(map, g1[0], g1[1], g2[0], g2[1], empty_rows, empty_columns)
            total_length += path_length
    print(total_length)