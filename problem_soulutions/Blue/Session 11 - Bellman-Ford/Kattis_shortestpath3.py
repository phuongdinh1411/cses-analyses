# Problem from Kattis
# https://open.kattis.com/problems/shortestpath3
#
# Problem Name: Single source shortest path, negative weights
#
# Problem Description:
# Given a directed weighted graph with possible negative edge weights,
# find the shortest path from source to multiple query nodes.
# Handle negative cycles by reporting "-Infinity" for affected nodes.
#
# Input Format:
# - Multiple test cases until n=0
# - For each test case:
#   - n m q s: nodes, edges, queries, source
#   - m lines with u v w: directed edge from u to v with weight w
#   - q query nodes
#
# Output Format:
# - For each query:
#   - Shortest distance, or "Impossible" if unreachable, or "-Infinity" if affected by negative cycle
#
# Key Approach/Algorithm:
# - Bellman-Ford algorithm for single-source shortest path with negative weights
# - Run N-1 iterations for standard relaxation
# - Run N-1 MORE iterations to propagate negative cycle effects to all reachable nodes

import sys


class InputTokenizer:
    def __init__(self):
        self._tokens = sys.stdin.read().split()[::-1]

    def next(self):
        return self._tokens.pop()


inp = InputTokenizer()

INF = float('inf')


def bellman_ford(n, edges, source, queries):
    dist = [INF] * n
    affected_by_neg_cycle = [False] * n

    # Fixed: Use the actual source from input, not hardcoded 0
    dist[source] = 0

    # Standard Bellman-Ford: N-1 iterations
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Fixed: Run N-1 more iterations to propagate negative cycle effects
    # Any node that can still be relaxed is affected by a negative cycle,
    # as is any node reachable from such a node
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                affected_by_neg_cycle[v] = True
            if affected_by_neg_cycle[u]:
                affected_by_neg_cycle[v] = True

    # Answer queries
    for q in queries:
        if affected_by_neg_cycle[q]:
            print('-Infinity')
        elif dist[q] == INF:
            print('Impossible')
        else:
            print(dist[q])


def solution():
    while True:
        N = int(inp.next())
        if N == 0:
            break
        M = int(inp.next())
        Q = int(inp.next())
        S = int(inp.next())  # Source node

        edges = []
        for _ in range(M):
            u = int(inp.next())
            v = int(inp.next())
            w = int(inp.next())
            edges.append((u, v, w))

        queries = []
        for _ in range(Q):
            queries.append(int(inp.next()))

        bellman_ford(N, edges, S, queries)
        print()


solution()
