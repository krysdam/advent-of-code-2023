DIRECTION_NAMES_TO_DYDX = {'U': (-1, 0),
                           'R': (0, 1),
                           'D': (1, 0),
                           'L': (0, -1)}

# For interpreting colors as instructions.
# 0 is right, 1 is down, 2 is left, 3 is up.
DIRECTION_NUMS_TO_DYDX = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def motions_to_vertices(instructions: list) -> dict:
    """Given a list of motions, find the vertices of the resulting polygon."""
    y, x = 0, 0
    vertices = []
    for dy, dx, dist in instructions:
        y += dy * dist
        x += dx * dist
        vertices.append((y, x))
    return vertices

def determinant(x1, x2, y1, y2) -> int:
    """The determinant of a 2x2 matrix."""
    return x1 * y2 - x2 * y1

def shoelace_area(vertices: list) -> int:
    """Given the vertices of a polygon, find its area."""
    area = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1) % len(vertices)]
        area += determinant(x1, x2, y1, y2)
    return abs(area) / 2

def perimeter(vertices: list) -> int:
    """The number of tiles on the edge of a polygon."""
    perimeter = 0
    for i in range(len(vertices)):
        y1, x1 = vertices[i]
        y2, x2 = vertices[(i+1) % len(vertices)]
        segment = abs(x1 - x2) + abs(y1 - y2)
        perimeter += segment
    return perimeter

def area(vertices: list) -> int:
    """The number of tiles in or on a polygon."""
    # Start with the shoelace area.
    area = shoelace_area(vertices)
    # But now we're missing part of each tile on the path itself.
    # Each tile on an edge contributes 1/2 its area.
    # Tiles on convex corners contribute 3/4, and concave ones contribute 1/4.
    # The winding number is 1, so we have 4 more convex corners than concave.
    # So the total area of these partial tiles is (perimeter/2) + 1.
    area += perimeter(vertices) / 2 + 1
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
    trench_vertices = motions_to_vertices(instructions1)
    trench_area = area(trench_vertices)
    print("Part 1:", str(int(trench_area)))

    # Part 2: instructions are hidden in 'color'
    instructions2 = [color_to_instruction(color) for dy, dx, dist, color in instructions]
    trench_vertices = motions_to_vertices(instructions2)
    trench_area = area(trench_vertices)
    print("Part 2:", str(int(trench_area)))