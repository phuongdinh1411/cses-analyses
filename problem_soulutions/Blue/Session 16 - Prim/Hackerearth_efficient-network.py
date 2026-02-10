# Problem from Hackerearth
# https://www.hackerearth.com/challenges/hiring/globalsoft-backend-hiring-challenge/algorithm/efficient-network/
#
# Problem: Efficient Network
#
# Description:
# Build an efficient network connecting N nodes using M weighted edges.
# Additionally, you have Q "free" connections with costs C[i] that can
# replace the most expensive edges in the MST to minimize total cost.
#
# Input:
# - First line: N (nodes), M (edges)
# - Next M lines: A, B, W (edge from A to B with weight W)
# - Next line: Q (number of free connections)
# - Next line: Q space-separated costs C[i]
#
# Output:
# - Minimum total cost to connect all nodes
#
# Approach:
# - Use Prim's algorithm to find MST and collect edge weights
# - Sort MST edge weights in descending order
# - Sort free connection costs in ascending order
# - Greedily replace expensive MST edges with cheaper free connections


import heapq


def prim(n, graph):
    """Run Prim's algorithm, return list of MST edge weights (excluding source)."""
    dist = [-1] * (n + 1)
    visited = [False] * (n + 1)

    dist[1] = 0
    pqueue = [(0, 1)]
    mst_edges = []

    while pqueue:
        d, u = heapq.heappop(pqueue)

        if visited[u]:
            continue
        visited[u] = True

        # Record edge weight (except for source node)
        if d > 0:
            mst_edges.append(d)

        for v, w in graph[u]:
            if not visited[v] and (dist[v] == -1 or w < dist[v]):
                dist[v] = w
                heapq.heappush(pqueue, (w, v))

    return mst_edges


def solution():
    N, M = map(int, input().split())

    graph = [[] for _ in range(N + 1)]
    for _ in range(M):
        A, B, W = map(int, input().split())
        graph[A].append((B, W))
        graph[B].append((A, W))

    Q = int(input())
    free_costs = []
    if Q > 0:
        free_costs = list(map(int, input().strip().split()))

    # Get MST edge weights
    mst_edges = prim(N, graph)

    # Sort MST edges descending (most expensive first)
    mst_edges.sort(reverse=True)

    # Sort free costs ascending (cheapest first)
    free_costs.sort()

    # Fixed: Greedily replace expensive MST edges with cheaper free connections
    # Only replace if free connection is actually cheaper
    for i in range(min(len(free_costs), len(mst_edges))):
        if free_costs[i] < mst_edges[i]:
            mst_edges[i] = free_costs[i]
        else:
            # Free connections are sorted, so no point continuing
            break

    print(sum(mst_edges))


solution()
