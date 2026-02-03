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
# - Run one more iteration to detect nodes affected by negative cycles
# - Nodes that can still be relaxed are affected by negative cycles

import sys


class input_tokenizer:
    __tokens = None

    def has_next(self):
        return self.__tokens != [] and self.__tokens != None

    def next(self):
        token = self.__tokens[-1]
        self.__tokens.pop()
        return token

    def __init__(self):
        self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


INF = int(1e9)


def bellman_ford(N, M, E, q):
    dist = [INF for i in range(N + 1)]
    flag = [False for i in range(N + 1)]

    dist[0] = 0
    for i in range(1, N):
        for j in range(M):
            u = E[j][0]
            v = E[j][1]
            w = E[j][2]
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # for i in range(N):
    for j in range(M):
        u = E[j][0]
        v = E[j][1]
        w = E[j][2]
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            flag[v] = True

    for cq in q:
        if flag[cq]:
            print('-Infinity')
        elif dist[cq] == INF:
            print('Impossible')
        else:
            print(dist[cq])


def solution():
    while True:
        N = int(inp.next())
        if N == 0:
            break
        M = int(inp.next())
        Q = int(inp.next())
        S = int(inp.next())

        E = []
        for m in range(M):
            i = int(inp.next())
            j = int(inp.next())
            w = int(inp.next())
            E.append([i, j, w])
        q = []
        for x in range(Q):
            q.append(int(inp.next()))

        bellman_ford(N, M, E, q)
        print()


solution()


