#  Problem from SPOJ
#  https://www.spoj.com/problems/TRAFFICN/
#
# Problem: TRAFFICN - Traffic Network
#
# A city has N junctions connected by M one-way roads. The mayor can build
# ONE new bidirectional road from a list of K proposals. Find the minimum
# shortest path from junction S to T after optimally choosing which new
# road to build (or not building any).
#
# Input:
# - Line 1: T (test cases)
# - For each test case:
#   - Line 1: N M K S T
#   - Next M lines: u v w (existing one-way road)
#   - Next K lines: u v w (proposed bidirectional road)
#
# Output: Minimum shortest path S to T, or -1 if unreachable
#
# Approach: Dijkstra from S and reverse Dijkstra from T, try each new road


import heapq
import sys


class InputTokenizer:
    def __init__(self):
        self._tokens = sys.stdin.read().split()[::-1]

    def next(self):
        return self._tokens.pop()


inp = InputTokenizer()


def dijkstra(n, source, graph):
    """Run Dijkstra from source, return distances to all nodes."""
    dist = [-1] * (n + 1)
    dist[source] = 0
    pqueue = [(0, source)]

    while pqueue:
        d, u = heapq.heappop(pqueue)

        # Skip stale entries
        if dist[u] != -1 and d > dist[u]:
            continue

        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pqueue, (new_dist, v))

    return dist


def solution():
    T = int(inp.next())

    for _ in range(T):
        n = int(inp.next())
        m = int(inp.next())
        k = int(inp.next())
        s = int(inp.next())
        t = int(inp.next())

        graph = [[] for _ in range(n + 1)]
        rev_graph = [[] for _ in range(n + 1)]

        for _ in range(m):
            A = int(inp.next())
            B = int(inp.next())
            W = int(inp.next())
            graph[A].append((B, W))
            rev_graph[B].append((A, W))

        proposed_roads = []
        for _ in range(k):
            A = int(inp.next())
            B = int(inp.next())
            W = int(inp.next())
            proposed_roads.append((A, B, W))

        dist_from_s = dijkstra(n, s, graph)
        dist_from_t = dijkstra(n, t, rev_graph)

        # Start with the original shortest path (without any new road)
        minimum_path = dist_from_s[t]

        # Try each proposed road (bidirectional)
        for u, v, w in proposed_roads:
            # Try using the new road u -> v
            if dist_from_s[u] != -1 and dist_from_t[v] != -1:
                new_path = dist_from_s[u] + w + dist_from_t[v]
                if minimum_path == -1 or new_path < minimum_path:
                    minimum_path = new_path

            # Try using the new road v -> u (bidirectional)
            if dist_from_s[v] != -1 and dist_from_t[u] != -1:
                new_path = dist_from_s[v] + w + dist_from_t[u]
                if minimum_path == -1 or new_path < minimum_path:
                    minimum_path = new_path

        print(minimum_path)


solution()
