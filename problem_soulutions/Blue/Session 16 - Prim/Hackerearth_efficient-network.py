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
# - Use Prim's algorithm with priority queue to find MST
# - Sort MST edge weights and free connection costs
# - Greedily replace expensive MST edges with cheaper free connections


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph, C):

    dist = [-1 for x in range(N+1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for neighbor in graph[u]:
            v = neighbor.id
            w = neighbor.dist
            if not visited[v] and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                heapq.heappush(pqueue, Node(v, w))

    dist.sort()
    C.sort()

    for i in range(len(C)):
        if i <= N + 1:
            if dist[-i - 1] > C[i]:
                dist[-i - 1] = C[i]
            else:
                break
        else:
            break

    result = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            result += dist[i]

    return result


def solution():

    N, M = map(int, input().split())

    graph = [[] for i in range(N + 1)]
    for i in range(M):
        A, B, W = map(int, input().split())

        graph[A].append(Node(B, W))
        graph[B].append(Node(A, W))

    Q = int(input())
    C = []
    if Q > 0:
        C = list(map(int, input().strip().split()))

    result = prim(N, graph, C)

    print(result)


solution()

