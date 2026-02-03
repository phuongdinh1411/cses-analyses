# Problem from URI
# https://www.urionlinejudge.com.br/judge/en/problems/view/1610
#
# Problem: Dudu - Cycle Detection
#
# Given a directed graph with N nodes and M edges, determine if there is a
# cycle in the graph. Output "SIM" (yes) if a cycle exists, "NAO" (no) otherwise.
#
# Input:
# - Line 1: T (number of test cases)
# - For each test case:
#   - Line 1: N M (nodes, edges)
#   - Next M lines: A B (directed edge from A to B)
#
# Output: For each test case, print "SIM" if cycle exists, "NAO" otherwise
#
# Approach: DFS with cycle detection (check if we revisit a node in current path)


def sim_nao(N, graph):
    global_visited = [False for i in range(N+1)]

    for i in range(1, N + 1):
        if not global_visited[i]:
            visited = [False for l in range(N + 1)]
            s = [i]
            global_visited[i] = True
            visited[i] = True
            path = [0] * (N+1)
            while len(s) > 0:
                u = s[-1]
                s.pop()
                for v in graph[u]:
                    if not visited[v]:
                        visited[v] = True
                        if not global_visited[v]:
                            s.append(v)
                            global_visited[u] = True
                    else:
                        return 'SIM'

    return 'NAO'


def solution():
    results = []
    T = int(input())
    for i in range(T):

        while True:
            new_line = input().strip()
            if new_line:
                N, M = map(int, new_line.split())
                break

        graph = [[] for i in range(N + 1)]
        for j in range(M):
            while True:
                new_line = input().strip()
                if new_line:
                    A, B = map(int, new_line.split())
                    if not B in graph[A]:
                        graph[A].append(B)
                    break
        results.append(sim_nao(N, graph))

    print(*results, sep='\n')


solution()


