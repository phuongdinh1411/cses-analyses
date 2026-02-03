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
# - Recompute MST without that edge, find minimum among all such trees
# - Time complexity: O(V * E log V)


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph):

    dist = [-1 for x in range(N+1)]
    path = [-1 for x in range(N + 1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for i in range(1, N + 1):
            v = i
            w = graph[u][i]
            if not visited[v] and w != -1 and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                path[v] = u
                heapq.heappush(pqueue, Node(v, w))

    mst_cost = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            mst_cost += dist[i]

    return path, mst_cost


def solution():

    T = int(input())
    for i in range(T):
        N, M = map(int, input().strip().split())

        graph = [[-1 for j in range(N + 1)] for i in range(N + 1)]
        for i in range(M):
            A, B, C = map(int, input().strip().split())
            graph[A][B] = C
            graph[B][A] = C

        mst, mst_cost = prim(N, graph)

        second_mst_cost = 1e9
        for i in range(len(mst)):
            if mst[i] != -1:
                tmp_weight = graph[i][mst[i]]
                graph[i][mst[i]] = -1
                graph[mst[i]][i] = -1
                current_mst, current_mst_cost = prim(N, graph)
                if current_mst_cost < second_mst_cost:
                    second_mst_cost = current_mst_cost
                graph[i][mst[i]] = tmp_weight
                graph[mst[i]][i] = tmp_weight

        print(mst_cost, second_mst_cost)


solution()

