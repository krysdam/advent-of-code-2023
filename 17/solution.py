def grid_to_graph(grid: list) -> dict:
    """Convert a grid to a graph.
    
    The graph has four vertices per tile: one for each direction,
    representing the direction the path must go from that tile.

    Each vertex is represented as a tuple: (y, x, dy, dx).
    (y, x) is the point on the grid.
    (dy, dx) is the direction to travel from that point.

    The start and end vertices have no required direction,
    so they're represented as (y, x).
    """
    maxy = len(grid)
    maxx = len(grid[0])
    dydx_options = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Build the graph of (y, x, dy, dx) vertices.
    graph = {}
    for y in range(maxy):
        for x in range(maxx):
            for dy, dx in dydx_options:
                vertex = (y, x, dy, dx)
                reachable = []
                seg_weight = 0
                for seg_len in [1, 2, 3]:
                    newy = y + dy * seg_len
                    newx = x + dx * seg_len
                    # Don't return to start
                    if (newy, newx) == (0, 0):
                        continue
                    if 0 <= newy < maxy and 0 <= newx < maxx:
                        seg_weight += grid[newy][newx]
                        reachable.append( (seg_weight, (newy, newx,  dx,  dy)) )
                        reachable.append( (seg_weight, (newy, newx, -dx, -dy)) )
                graph[vertex] = reachable

    # Collapse all (0, 0, A, B) vertices into just (0, 0).
    start = (0, 0)
    graph[start] = graph[(0, 0, 1, 0)] + graph[(0, 0, 0, 1)]
    del graph[(0, 0, 1, 0)]
    del graph[(0, 0, 0, 1)]

    for v in graph:
        for w, v2 in graph[v]:
            if v2[:2] == start:
                graph[v].remove((w, v2))

    # Collapse all (maxy-1, maxx-1, A, B) vertices into just (maxy-1, maxx-1).
    end = (maxy-1, maxx-1)
    graph[end] = []
    del graph[(maxy-1, maxx-1, 1, 0)]
    del graph[(maxy-1, maxx-1, 0, 1)]

    for v in graph:
        for w, v2 in graph[v]:
            if v2[:2] == end:
                graph[v].remove((w, v2))
                graph[v].append((w, end))

    return graph

def shortest_path_weight(graph: dict, start: tuple, end: tuple) -> int:
    """What's the least path weight from start to end in this graph?"""
    visited = set()
    shortest_known_paths = {v: float('inf') for v in graph}
    shortest_known_paths[start] = 0
    while True:
        if len(visited) % 1000 == 0:
            print(len(visited) / len(graph), shortest_known_paths[end])
        if end in visited:
            break
        # Find the unvisited vertex with the shortest known path.
        shortest = float('inf')
        shortest_vertex = None
        for v in graph:
            if v not in visited and shortest_known_paths[v] < shortest:
                shortest = shortest_known_paths[v]
                shortest_vertex = v
        if shortest_vertex is None:
            # No unvisited vertices left.
            break
        # Visit this vertex.
        visited.add(shortest_vertex)
        for w, v2 in graph[shortest_vertex]:
            if v2 not in visited:
                shortest_known_paths[v2] = min(shortest_known_paths[v2], shortest + w)
    return shortest_known_paths[end]


if __name__ == '__main__':
    grid = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            nums = [int(ch) for ch in line]
            grid.append(nums)

    start = (0, 0)
    end = (len(grid)-1, len(grid[0])-1)    

    graph = grid_to_graph(grid)
    print("Part 1:", shortest_path_weight(graph, start, end))