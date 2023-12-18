DIRECTION_NAMES_TO_DYDX = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
DIRECTION_NUMS_TO_DYDX = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def find_trench_points(instructions: list) -> dict:
    """The corners on the path."""
    y, x = 0, 0
    trench = []
    for dy, dx, dist in instructions:
        y += dy * dist
        x += dx * dist
        trench.append((y, x))
    return trench

def determinant(x1, x2, y1, y2) -> int:
    """The determinant of a 2x2 matrix."""
    return x1 * y2 - x2 * y1

def shoelace_area(points: list) -> int:
    """The area of a polygon, using the shoelace formula.
    
    points: the corners of the polygon"""
    area = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % len(points)]
        area += determinant(x1, x2, y1, y2)
    return abs(area) / 2

def area(points: list) -> int:
    """The number of tiles in or on a polygon.
    
    points: the corners of the polygon"""
    # Start with the shoelace area.
    area = shoelace_area(points)
    # But now we're missing part of each tile on the edge.
    # How much of those tiles?
    # Half of the ones on the edge, and either 1/4 or 3/4 of the ones on the corners.
    # The total winding number is 1, so these 1/4 and 3/4 tiles cancel out.
    # So we just need to add 1/2 of the tiles on the edge, plus 1 (the winding number).
    for p1, p2 in zip(points, points[1:] + [points[0]]):
        segment = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        area += segment / 2
    area += 1
    return area

def color_to_instruction(color: str) -> tuple:
    """Interpret a hex color string as a direction and distance."""
    # Strip punctuation.
    color = color[2:-1]
    # Direction is given in the last digit.
    dir_index = int(color[-1])
    dy, dx = DIRECTION_NUMS_TO_DYDX[dir_index]
    # Distance is the rest.
    dist = int(color[:-1], 16)
    return dy, dx, dist

if __name__ == '__main__':
    instructions = []

    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()

            dir, dist, color = line.split()
            dy, dx = DIRECTION_NAMES_TO_DYDX[dir]
            dist = int(dist)
            instructions.append((dy, dx, dist, color))

    # Part 1: instructions dir and dist
    instructions1 = [(dy, dx, dist) for dy, dx, dist, color in instructions]
    trench = find_trench_points(instructions1)
    print("Part 1:", area(trench))

    # Part 2: instructions are hidden in 'color'
    instructions2 = [color_to_instruction(color) for dy, dx, dist, color in instructions]
    trench = find_trench_points(instructions2)
    print("Part 2:", str(int(area(trench))))