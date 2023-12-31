import heapq

def grid_to_graph(grid: list, min_segment: int, max_segment: int) -> dict:
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
                for seg_len in range(1, max_segment+1):
                    newy = y + dy * seg_len
                    newx = x + dx * seg_len
                    # Don't return to start
                    if (newy, newx) == (0, 0):
                        continue
                    if 0 <= newy < maxy and 0 <= newx < maxx:
                        seg_weight += grid[newy][newx]
                        if min_segment <= seg_len <= max_segment:
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
    # Using Dijkstra's algorithm.
    visited = set()
    shortest_known_paths = {v: float('inf') for v in graph}
    shortest_known_paths[start] = 0
    queue = [(0, start)]
    heapq.heapify(queue)
    while True:
        if end in visited:
            break
        # Find the unvisited vertex with the shortest known path.
        if len(queue) == 0:
            break
        w, v = heapq.heappop(queue)
        if v in visited:
            continue
        # Visit this vertex.
        visited.add(v)
        for w2, v2 in graph[v]:
            if v2 not in visited:
                shortest_known_paths[v2] = min(shortest_known_paths[v2], w + w2)
                heapq.heappush(queue, (shortest_known_paths[v2], v2))
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

    graph1 = grid_to_graph(grid, 1, 3)
    print("Part 1:", shortest_path_weight(graph1, start, end))

    graph2 = grid_to_graph(grid, 4, 10)
    print("Part 2:", shortest_path_weight(graph2, start, end))