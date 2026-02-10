# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=364
#
# Problem Name: MPI Maelstrom (UVA 423)
#
# Problem Description:
# N processors are connected in a network. The communication time between
# processors is given in a lower triangular matrix format. Some connections
# may not exist (marked as 'x'). Find the minimum time to broadcast a message
# from processor 0 to all other processors (maximum shortest path from source).
#
# Input Format:
# - N: number of processors
# - Lower triangular matrix of communication times ('x' means no connection)
#
# Output Format:
# - Maximum shortest path distance from processor 0 (broadcast completion time)
#
# Key Approach/Algorithm:
# - Bellman-Ford algorithm (or Dijkstra/Floyd-Warshall would also work)
# - Build undirected graph from lower triangular matrix
# - Find shortest paths from processor 0 to all others
# - Return the maximum of all shortest path distances

INF = float('inf')


def bellman_ford(n, edges):
    dist = [INF] * n
    dist[0] = 0

    # Standard Bellman-Ford: N-1 iterations
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Find maximum distance (broadcast completion time)
    max_dist = 0
    for d in dist:
        if d != INF and d > max_dist:
            max_dist = d

    return max_dist


def solution():
    N = int(input())
    edges = []

    for i in range(1, N):
        line = input().strip().split()
        for j in range(i):
            # Fixed: Use != instead of 'is not' for string comparison
            if line[j] != 'x':
                weight = int(line[j])
                # Bidirectional edges
                edges.append((i, j, weight))
                edges.append((j, i, weight))

    print(bellman_ford(N, edges))


solution()
