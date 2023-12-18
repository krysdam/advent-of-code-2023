DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

def find_trench(instructions: list) -> dict:
    y, x = 0, 0
    trench = set()
    for dir, dist in instructions:
        dy, dx = DIRECTIONS[dir]
        for _ in range(dist):
            trench.add((y, x))
            y += dy
            x += dx
        print(len(trench))
    return trench

def find_area(trench: set) -> int:
    miny, minx, maxy, maxx = 0, 0, 0, 0
    for y, x in trench:
        miny = min(miny, y)
        minx = min(minx, x)
        maxy = max(maxy, y)
        maxx = max(maxx, x)
    area = 0
    #for y in range(miny, maxy+1):
    #    for x in range(minx, maxx+1):
    #        print('X' if (y, x) in trench else '.', end='')
    #    print()
    #print()
    for y in range(miny, maxy+1):
        print(y / maxy)
        inside = False
        for x in range(minx, maxx+1):
            if (y, x) in trench and (y-1, x) in trench:
                inside = not inside
            if inside or ((y, x) in trench):
    #            print('X', end='')
                area += 1
    #        else:
    #            print('.', end='')
    #    print() 
    return area

def pull_int_from_color(color: str) -> int:
    color = color[2:-1]
    return int(color, 16)


if __name__ == '__main__':
    instructions = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            dir, dist, color = line.split()
            dist = int(dist)
            instructions.append((dir, dist, color))

    # Find the loop
    # Part 1: instructions are correct
    instructions1 = [(dir, dist) for dir, dist, color in instructions]
    trench = find_trench(instructions1)
    print(find_area(trench))

    # Part 2: instructions are swapped
    #instructions2 = [(dir, pull_int_from_color(color)) for dir, dist, color in instructions]
    #trench = find_trench(instructions2)
    #print("trench found")
    #print(find_area(trench))