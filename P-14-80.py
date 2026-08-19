"""
P-14.80: Maze generation via minimum spanning tree, and solving.

Construction (as described in the assignment):
    1. Start with nxn grid; each cell is bounded by 4 unit walls.
    2. Every interior wall (shared between two adjacent cells) is assigned
    random weight. This defines a "dual" graph G: one vertex per grid cell,
    one edge per shared wall, edge weight = wall weight.
    3. Compute a minimum spanning tree T of G.
    4. "Carve" the maze by removing every wall whose edge is in T. Since a spanning
    tree touches all n^2 cells with zero cycles, there is guarenteed
    to be exactly one simple path between any two cells.
    5. Remove two boundary walls to create the start and finish.

We build T with Jarnk-Prim's algorithm (adjacency list + min-heap),
which fits the grid's sparse structure well: growing the tree one cell
at a time by always absorbing the cheapest edge leaving the current tree.

Once built, the maze itself is an unweighted tree, so solving it (start -> finish)
is just a graph traversal -- I am using BFS, since tree has no cycles to
worry about and BFS gives the (unique) path directly.
"""

import argparse
import heapq
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Grid/cell indexing helpers
def cell_id(r, c, n):
    """ Map a (row, col) cell to a single integer 0...n*n-1."""
    return r * n + c
def cell_rc(cell, n):
    """Inverse of cell_id."""
    return divmod(cell, n)

#Step 1-2: build the weighted dual graph as an adjacency list
def build_dual_graph(n, rng):
    """Return adj: dict mapping cell -> list of (neighbor cell, weight), 
    one entry per interior wall (shared edge between adjacent cells).
    """
    adj = {cell_id(r, c, n): [] for r in range(n) for c in range(n)}

    for r in range(n):
        for c in range(n):
            here = cell_id(r, c, n)
            if c + 1 < n:           #wall to the right neighbor
                right = cell_id(r, c + 1, n)
                w = rng.random()
                adj[here].append((right, w))
                adj[right].append((here, w))
            if r + 1 < n:           #wall to the neighbor below
                below = cell_id(r + 1, c, n)
                w = rng.random()
                adj[here].append((below, w))
                adj[below].append((here, w))
    return adj

# Step 3: Jarnik-Prim minimum spanning tree
def jarnik_prim_mst(adj, n, start=0):
    """Returns a set of MST edges as (min_cell, max_cell) tupples.
    Each MST edge represents a wall that gets removed (an open passage).
    """
    total_cells = n*n
    visited = {start}
    mst_edges = set()
    heap = []       #entries: (weight, from_cell, to_cell)
    for neighbor, w in adj[start]:
        heapq.heappush(heap, (w, start, neighbor))
    while heap and len(visited) < total_cells:
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue                # would create a cycle
        visited.add(v)
        mst_edges.add((min(u, v), max(u, v)))
        for neighbor, w2 in adj[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (w2, v, neighbor))

    return mst_edges

#  Step 6: solve the maze (BFS on the now unweighted spanning tree)
def solve_maze(n, mst_edges, start=0, goal=None):
    """Returns the list of cells from start to goal, 
    walking through open passages (MST edges).
    """
    if goal is None:
        goal = n*n - 1

    tree_adj = {cell: [] for cell in range(n*n)}
    for a, b in mst_edges:
        tree_adj[a].append(b)
        tree_adj[b].append(a)

    from collections import deque
    parent = {start: None}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell == goal:
            break
        for neighbor in tree_adj[cell]:
            if neighbor not in parent:
                parent[neighbor] = cell
                queue.append(neighbor)

    if goal not in parent:
        raise ValueError("No path found: This should be impossible for spanning tree")
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

# Steps 4-5, 7: draw the maze and (optionally) the solution path
def draw_maze(n, mst_edges, path=None, filename="maze.png", entrance=(0, 0), exit_=None):
    """
    Render the maze to a PNG file. Grid coordinates: cell (r, c) occupies the 
    unit square with corners (c, r)-(c + 1, r + 1). Walls are drawn as line
    segments. MST edges (open passages) are simply not drawn as walls.
    """
    if exit_ is None:
        exit_ = (n - 1, n - 1)
    def edge_open(a, b):
        return (min(a, b), max(a, b)) in mst_edges

    segments = []

    # Horizontal wall segments, at row-boundaries r = 0...n, each spanning
    # one columns width
    for r in range(n + 1):
        for c in range(n):
            if r == 0 and (r, c) == (entrance[0], entrance[1]) and entrance[0] == 0:
                continue        #entrance gap on the top boundary
            if r == n and (n -1, c) == (exit_[0], exit_[1]) and exit_[0] == n-1:
                continue        #exit gap on the bottom boundary
            if 0 < r < n:
                a, b = cell_id(r - 1, c, n), cell_id(r, c, n)
                if edge_open(a, b):
                    continue        #open passage: no wall drawn
            segments.append([(c, r), (c + 1, r)])
    # Vertical wall segments, at column-boundaries c=0...n, each spanning 
    #one row's hight
    for c in range(n + 1):
        for r in range(n):
            if 0 < c < n:
                a, b = cell_id(r, c - 1, n), cell_id(r, c, n)
                if edge_open(a, b):
                    continue
            segments.append([(c, r), (c, r + 1)])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.add_collection(LineCollection(segments, colors="black", linewidths=1.5))

    if path is not None:
        xs, ys = [], []
        for cell in path:
            r, c = cell_rc(cell, n)
            xs.append(c + 0.5)
            ys.append(r + 0.5)
        ax.plot(xs, ys, color="red", linewidth=2.5, alpha=0.8, zorder=3, label="solution path")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02))

    ax.set_xlim(-0.2, n + 0.2)
    ax.set_ylim(-0.2, n + 0.2)
    ax.invert_yaxis()       # row 0 at the top
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{n} x {n} maze (Jarn\u00edk-Prim MST)")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)

#Driver
def main():
    parser = argparse.ArgumentParser(description="Generate and solve an MST-based maze.")
    parser.add_argument("-n", type=int, default=15, help="grid size (n x n cells)")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")
    parser.add_argument("-o", "--output", default="maze.png", help="output image filename")
    args = parser.parse_args()
 
    rng = random.Random(args.seed)
 
    adj = build_dual_graph(args.n, rng)
    mst_edges = jarnik_prim_mst(adj, args.n, start=0)
    path = solve_maze(args.n, mst_edges, start=0, goal=args.n * args.n - 1)
 
    draw_maze(args.n, mst_edges, path=path, filename=args.output)
    print(f"Generated a {args.n}x{args.n} maze with {len(mst_edges)} open passages "
          f"(spanning tree edges).")
    print(f"Solution path length: {len(path)} cells.")
    print(f"Saved to {args.output}")
 
 
if __name__ == "__main__":
    main()

