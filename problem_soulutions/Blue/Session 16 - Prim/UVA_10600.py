# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1541
#
# Problem: ACM Contest and Blackout (UVA 10600)
#
# Description:
# Find both the Minimum Spanning Tree (MST) and the Second-Best MST for
# a given graph. The second-best MST differs by exactly one edge from the MST.
#
# Input:
# - T (test cases)
# - For each test case:
#   - N (nodes), M (edges)
#   - M lines: A, B, C (edge between A and B with weight C)
#
# Output:
# - For each test case: two integers - MST weight and second-best MST weight
#
# Approach:
# - First, find the MST using Prim's algorithm (track the path/edges used)
# - For second-best MST: try removing each MST edge one at a time
# - Recompute MST without that edge, verify the graph remains connected
# - Find minimum among all valid such trees


import heapq


def prim(n, graph):
    """Run Prim's algorithm, return (parent array, MST cost, connected count)."""
    dist = [-1] * (n + 1)
    parent = [-1] * (n + 1)
    visited = [False] * (n + 1)

    dist[1] = 0
    pqueue = [(0, 1)]
    connected = 0

    while pqueue:
        d, u = heapq.heappop(pqueue)

        if visited[u]:
            continue
        visited[u] = True
        connected += 1

        for v in range(1, n + 1):
            w = graph[u][v]
            if w != -1 and not visited[v] and (dist[v] == -1 or w < dist[v]):
                dist[v] = w
                parent[v] = u
                heapq.heappush(pqueue, (w, v))

    mst_cost = sum(d for d in dist[1:n+1] if d != -1)
    return parent, mst_cost, connected


def solution():
    T = int(input())

    for _ in range(T):
        N, M = map(int, input().strip().split())

        graph = [[-1] * (N + 1) for _ in range(N + 1)]
        for _ in range(M):
            A, B, C = map(int, input().strip().split())
            # Handle multiple edges between same nodes - keep minimum
            if graph[A][B] == -1 or C < graph[A][B]:
                graph[A][B] = C
                graph[B][A] = C

        # Find first MST
        mst_parent, mst_cost, _ = prim(N, graph)

        # Find second-best MST by removing each MST edge
        second_mst_cost = float('inf')

        for i in range(1, N + 1):
            if mst_parent[i] != -1:
                # Temporarily remove this MST edge
                u, v = i, mst_parent[i]
                tmp_weight = graph[u][v]
                graph[u][v] = -1
                graph[v][u] = -1

                # Recompute MST
                _, new_cost, connected = prim(N, graph)

                # Fixed: Only consider if graph is still connected (all N nodes reached)
                if connected == N and new_cost < second_mst_cost:
                    second_mst_cost = new_cost

                # Restore edge
                graph[u][v] = tmp_weight
                graph[v][u] = tmp_weight

        print(mst_cost, second_mst_cost)


solution()
