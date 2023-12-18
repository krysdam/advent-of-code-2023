DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

def find_trench_points(instructions: list) -> dict:
    y, x = 0, 0
    trench = []
    for dir, dist in instructions:
        dy, dx = DIRECTIONS[dir]
        dy, dx = dy * dist, dx * dist
        y += dy
        x += dx
        trench.append((y, x))
    return trench

def determinant(x1, x2, y1, y2) -> int:
    return x1 * y2 - x2 * y1

def shoelace_area(points: list) -> int:
    area = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % len(points)]
        area += determinant(x1, x2, y1, y2)
    return abs(area) / 2

def area(points: list) -> int:
    area = shoelace_area(points)
    for p1, p2 in zip(points, points[1:] + [points[0]]):
        segment = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        area += segment / 2
    area += 1
    return area


def color_to_instruction(color: str) -> tuple:
    color = color[2:-1]
    dir = 'RDLU'[int(color[-1])]
    dist = int(color[:-1], 16)
    return dir, dist

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
    trench = find_trench_points(instructions1)
    print("Part 1:", area(trench))

    # Part 2: instructions are swapped
    instructions2 = [color_to_instruction(color) for dir, dist, color in instructions]
    trench = find_trench_points(instructions2)
    print("Part 2:", str(int(area(trench))))