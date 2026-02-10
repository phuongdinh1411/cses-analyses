# Problem from LightOJ
# http://www.lightoj.com/volume_showproblem.php?problem=1074
#
# Problem Name: Extended Traffic
#
# Problem Description:
# Dhaka city has junctions with "busyness" values. The cost to travel from
# junction u to v is (busyness[v] - busyness[u])^3, which can be negative.
# Find the minimum cost from junction 1 to query junctions.
# If cost < 3 or unreachable or affected by negative cycle, output "?".
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N: number of junctions
#   - N busyness values
#   - M: number of roads
#   - M lines with u v: directed road from u to v
#   - Q: number of queries
#   - Q query junction numbers
#
# Output Format:
# - For each case: "Case X:" followed by minimum cost for each query (or "?")
#
# Key Approach/Algorithm:
# - Bellman-Ford algorithm to handle negative edge weights
# - Edge weight = (busyness[v] - busyness[u])^3 (CUBED!)
# - Detect negative cycles and propagate to all reachable nodes
# - Output "?" for unreachable, negative cycle affected, or cost < 3

import sys


class InputTokenizer:
    def __init__(self):
        self._tokens = sys.stdin.read().split()[::-1]

    def next(self):
        return self._tokens.pop()


inp = InputTokenizer()

INF = float('inf')


def bellman_ford(n, edges, queries, case_number):
    dist = [INF] * (n + 1)
    affected_by_neg_cycle = [False] * (n + 1)

    print(f'Case {case_number}:')

    dist[1] = 0  # Start from junction 1

    # Standard Bellman-Ford: N-1 iterations
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Fixed: Run N-1 more iterations to propagate negative cycle effects
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                affected_by_neg_cycle[v] = True
            if affected_by_neg_cycle[u]:
                affected_by_neg_cycle[v] = True

    # Answer queries
    for q in queries:
        if affected_by_neg_cycle[q] or dist[q] < 3 or dist[q] == INF:
            print('?')
        else:
            print(dist[q])


def solution():
    T = int(inp.next())
    for t in range(T):
        N = int(inp.next())
        busyness = [0] * (N + 1)
        for i in range(1, N + 1):
            busyness[i] = int(inp.next())

        M = int(inp.next())
        edges = []
        for _ in range(M):
            u = int(inp.next())
            v = int(inp.next())
            # Fixed: Edge weight is the CUBE of the difference
            weight = (busyness[v] - busyness[u]) ** 3
            edges.append((u, v, weight))

        num_queries = int(inp.next())
        queries = []
        for _ in range(num_queries):
            queries.append(int(inp.next()))

        bellman_ford(N, edges, queries, t + 1)


solution()
