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

INF = int(1e9)


def bellman_ford(N, M, E):
    dist = [INF for i in range(N)]

    dist[0] = 0
    for i in range(0, N-1):
        for j in range(M):
            u = E[j][0]
            v = E[j][1]
            w = E[j][2]
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    max = 0
    for di in dist:
        if di > max:
            max = di

    return max


def solution():
    N = int(input())
    E = []
    for i in range(N - 1):
        line = list(map(str, input().strip().split()))
        for j in range(i + 1):
            if line[j] is not 'x':
                E.append([i + 1, j, int(line[j])])
                E.append([j, i + 1, int(line[j])])

    print(bellman_ford(N, len(E), E))


solution()


