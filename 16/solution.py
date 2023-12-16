def process_grid(grid: list, starting_beam: tuple) -> set:
    maxy, maxx = len(grid), len(grid[0])

    def add_beam(y, x, dy, dx):
        #print("about to append", y, x, dy, dx)
        if 0 <= y < maxy and 0 <= x < maxx:
            beam = (y, x, dy, dx)
            if beam not in beams:
                beams.append(beam)
            #print("appended")
    visited = set()

    beams = [starting_beam]

    for beam in beams:
        y, x, dy, dx = beam

        visited.add((y, x))
        ch = grid[y][x]
        match ch:
            case '.':
                add_beam(y + dy, x + dx, dy, dx)
            case '/':
                add_beam(y - dx, x - dy, -dx, -dy)
            case '\\':
                add_beam(y + dx, x + dy, dx, dy)
            case '|':
                if dx == 0:
                    add_beam(y + dy, x + dx, dy, dx)
                elif dy == 0:
                    add_beam(y+1, x, 1, 0)
                    add_beam(y-1, x, -1, 0)
            case '-':
                if dx == 0:
                    add_beam(y, x+1, 0, 1)
                    add_beam(y, x-1, 0, -1)
                elif dy == 0:
                    add_beam(y, x + dx, dy, dx)
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
        print(y)
        possibilities.append(process_grid(grid, (y, 0, 0, 1)))
        possibilities.append(process_grid(grid, (y, len(grid[0])-1, 0, -1)))
    for x in range(len(grid[0])):
        print(x)
        possibilities.append(process_grid(grid, (0, x, 1, 0)))
        possibilities.append(process_grid(grid, (len(grid)-1, x, -1, 0)))
    print(max(possibilities))   