#  Problem from UVA
#  https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=3296
#
# Problem: UVA 12144 - Almost Shortest Path
#
# Find the "almost shortest path" from S to D. This is the shortest path
# that does NOT use any edge that appears in ANY shortest path from S to D.
#
# Input:
# - Multiple test cases until n=0 m=0
# - For each test case:
#   - Line 1: n m (nodes, edges)
#   - Line 2: S D (source, destination)
#   - Next m lines: A B W (directed edge from A to B with weight W)
#
# Output: Almost shortest path length, or -1 if impossible
#
# Approach:
# 1. Run Dijkstra from S to get dist_from_S
# 2. Run Dijkstra from D on reversed graph to get dist_from_D
# 3. For each edge (u, v, w), if dist_from_S[u] + w + dist_from_D[v] == shortest,
#    mark it as part of a shortest path and remove it
# 4. Run Dijkstra again from S avoiding removed edges


import heapq
import sys


class InputTokenizer:
    def __init__(self):
        self._tokens = sys.stdin.read().split()[::-1]

    def has_next(self):
        return len(self._tokens) > 0

    def next(self):
        return self._tokens.pop()


inp = InputTokenizer()


def dijkstra(n, source, graph, removed_edges):
    """Run Dijkstra from source, avoiding removed edges."""
    dist = [-1] * n
    dist[source] = 0
    pqueue = [(0, source)]

    while pqueue:
        d, u = heapq.heappop(pqueue)

        if dist[u] != -1 and d > dist[u]:
            continue

        for v, w in graph[u]:
            if (u, v) in removed_edges:
                continue
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pqueue, (new_dist, v))

    return dist


def solution():
    while True:
        n = int(inp.next())
        m = int(inp.next())

        if n == 0 and m == 0:
            break

        s = int(inp.next())
        d = int(inp.next())

        graph = [[] for _ in range(n)]
        rev_graph = [[] for _ in range(n)]
        edges = []

        for _ in range(m):
            A = int(inp.next())
            B = int(inp.next())
            W = int(inp.next())

            graph[A].append((B, W))
            rev_graph[B].append((A, W))
            edges.append((A, B, W))

        # Run Dijkstra from S
        dist_from_S = dijkstra(n, s, graph, set())

        # Run Dijkstra from D on reversed graph
        dist_from_D = dijkstra(n, d, rev_graph, set())

        shortest = dist_from_S[d]

        if shortest == -1:
            print(-1)
            continue

        # Fixed: Find ALL edges that lie on ANY shortest path
        # An edge (u, v, w) is on a shortest path if:
        # dist_from_S[u] + w + dist_from_D[v] == shortest
        removed_edges = set()
        for u, v, w in edges:
            if (dist_from_S[u] != -1 and dist_from_D[v] != -1 and
                dist_from_S[u] + w + dist_from_D[v] == shortest):
                removed_edges.add((u, v))

        # Run Dijkstra again avoiding removed edges
        almost_shortest = dijkstra(n, s, graph, removed_edges)[d]
        print(almost_shortest)


solution()
