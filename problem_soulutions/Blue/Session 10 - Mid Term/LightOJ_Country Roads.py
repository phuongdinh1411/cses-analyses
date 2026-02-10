#  Problem from LightOJ
#  http://lightoj.com/volume_showproblem.php?problem=1002
#
# Problem Name: Country Roads
#
# Problem Description:
# Given an undirected weighted graph representing cities and roads,
# find the minimum "maximum edge weight" path from a source city to all other cities.
# The cost of a path is the maximum edge weight along that path (minimax path problem).
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N M: number of nodes and edges
#   - M lines with A B W: edge from A to B with weight W
#   - t: the source node
#
# Output Format:
# - For each test case: "Case X:" followed by the minimum maximum edge weight
#   to reach each city (0 to N-1), or "Impossible" if unreachable
#
# Key Approach/Algorithm:
# - Modified Dijkstra's algorithm
# - Instead of summing weights, track the maximum edge weight on the path
# - For relaxation: new_dist = max(dist[u], edge_weight), update if smaller than current dist[v]


import heapq
import sys


class InputTokenizer:
    def __init__(self):
        self._tokens = sys.stdin.read().split()[::-1]

    def next(self):
        return self._tokens.pop()


inp = InputTokenizer()


def dijkstra_minimax(n, source, graph):
    """Modified Dijkstra for minimax path problem."""
    dist = [-1] * n
    dist[source] = 0
    pqueue = [(0, source)]  # (max_edge_weight_so_far, node)

    while pqueue:
        d, u = heapq.heappop(pqueue)

        # Skip stale entries
        if dist[u] != -1 and d > dist[u]:
            continue

        for v, w in graph[u]:
            # New distance is the max of current path's max and this edge
            new_dist = max(d, w)
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pqueue, (new_dist, v))

    return dist


def solution():
    T = int(inp.next())

    for case_num in range(1, T + 1):
        N = int(inp.next())
        M = int(inp.next())

        graph = [[] for _ in range(N)]
        for _ in range(M):
            A = int(inp.next())
            B = int(inp.next())
            W = int(inp.next())
            graph[A].append((B, W))
            graph[B].append((A, W))

        source = int(inp.next())

        dist = dijkstra_minimax(N, source, graph)

        print(f'Case {case_num}:')
        # Fixed: Only print N values (nodes 0 to N-1), not N+1
        for i in range(N):
            if dist[i] != -1:
                print(dist[i])
            else:
                print('Impossible')


solution()
