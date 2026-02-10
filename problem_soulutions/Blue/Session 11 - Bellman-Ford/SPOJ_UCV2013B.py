# Problem from SPOJ
# https://www.spoj.com/problems/UCV2013B/
#
# Problem Name: Babylon Tours
#
# Problem Description:
# Given N monuments in Babylon with travel costs between them (can be negative),
# find the shortest path for multiple tour queries. Detect if a query path
# is affected by a negative cycle.
#
# Input Format:
# - Multiple test cases until N=0
# - For each test case:
#   - N: number of monuments
#   - N lines: monument name followed by N costs (0 means no direct path)
#   - Q: number of queries
#   - Q lines with source and destination monument indices
#
# Output Format:
# - For each case: "Case #X:" followed by results for each query
#   - "monument1-monument2 cost" or "NOT REACHABLE" or "NEGATIVE CYCLE"
#
# Key Approach/Algorithm:
# - Bellman-Ford algorithm for each unique source in queries
# - Handle negative edge weights and detect negative cycles
# - Propagate negative cycle effects to all reachable nodes

from collections import defaultdict

INF = float('inf')


def bellman_ford(n, edges, source):
    dist = [INF] * n
    affected_by_neg_cycle = [False] * n

    dist[source] = 0

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

    return dist, affected_by_neg_cycle


def solution():
    case_number = 1
    while True:
        N = int(input())
        if N == 0:
            break

        edges = []
        monuments = []
        for i in range(N):
            line = input().split()
            monuments.append(line[0])
            for j in range(1, N + 1):
                cost = int(line[j])
                if cost != 0 or (cost < 0):
                    # Add edge if cost is non-zero, or if it's negative (cost 0 to self is ok)
                    if cost != 0 or i != j - 1:
                        edges.append((i, j - 1, cost))

        num_queries = int(input())
        queries = []
        unique_sources = set()
        for _ in range(num_queries):
            pair = list(map(int, input().split()))
            queries.append(pair)
            unique_sources.add(pair[0])

        print(f'Case #{case_number}:')

        # Compute Bellman-Ford for each unique source
        results = {}
        for source in unique_sources:
            results[source] = bellman_ford(N, edges, source)

        # Answer queries
        for src, dst in queries:
            dist, affected = results[src]
            if affected[dst]:
                print("NEGATIVE CYCLE")
            elif dist[dst] == INF:
                print(f"{monuments[src]}-{monuments[dst]} NOT REACHABLE")
            else:
                print(f"{monuments[src]}-{monuments[dst]} {dist[dst]}")

        case_number += 1


solution()
