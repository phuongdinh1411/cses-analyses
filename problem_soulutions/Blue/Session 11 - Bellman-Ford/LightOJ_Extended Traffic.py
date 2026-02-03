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
# - Edge weight = busyness[v] - busyness[u] (cube computed implicitly in problem)
# - Detect negative cycles and mark affected nodes
# - Output "?" for unreachable, negative cycle affected, or cost < 3

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


def bellman_ford(N, M, E, q, case_number):
    dist = [INF for i in range(N + 1)]
    flag = [False for i in range(N + 1)]

    print('Case ' + str(case_number) + ':')

    dist[1] = 0
    for i in range(0, N-1):
        for j in range(M):
            u = E[j][0]
            v = E[j][1]
            w = E[j][2]
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for j in range(M):
        u = E[j][0]
        v = E[j][1]
        w = E[j][2]
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            flag[v] = True

    for cq in q:
        if flag[cq] or dist[cq] < 3 or dist[cq] == INF:
            print('?')
        else:
            print(dist[cq])


def solution():
    T = int(inp.next())
    for t in range(T):
        N = int(inp.next())
        busyness = [0 for x in range(N + 1)]
        counter = 1
        for x in range(N):
            busyness[counter] = int(inp.next())
            counter += 1

        M = int(inp.next())
        E = []
        for m in range(M):
            i = int(inp.next())
            j = int(inp.next())
            E.append([i, j, busyness[j] - busyness[i]])
        nq = int(inp.next())
        q = []
        for x in range(nq):
            q.append(int(inp.next()))

        bellman_ford(N, M, E, q, t + 1)


solution()


