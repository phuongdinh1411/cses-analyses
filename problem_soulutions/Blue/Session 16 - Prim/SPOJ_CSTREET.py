# Problem from SPOJ
# https://www.spoj.com/problems/CSTREET/
#
# Problem: Cobbled Streets (SPOJ CSTREET)
#
# Description:
# A town needs to pave roads between junctions. The cost per meter is p,
# and you're given road lengths. Find the minimum total cost to connect
# all junctions so everyone can reach everyone else.
#
# Input:
# - First line: T (test cases)
# - For each test case:
#   - p (cost per meter)
#   - n (number of junctions)
#   - m (number of possible roads)
#   - m lines: a, b, c (road from junction a to b with length c)
#
# Output:
# - For each test case: minimum total cost (MST weight * p)
#
# Approach:
# - Use Prim's algorithm to find MST
# - Multiply MST total edge weight by price per meter p


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph):

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

    result = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            result += dist[i]

    return result


def solution():

    t = int(input())
    for j in range(t):
        p = int(input())
        n = int(input())
        m = int(input())
        graph = [[] for i in range(n + 1)]
        for i in range(m):
            a, b, c = map(int, input().strip().split())
            graph[a].append(Node(b, c))
            graph[b].append(Node(a, c))

        result = prim(n, graph)

        print(result * p)


solution()

