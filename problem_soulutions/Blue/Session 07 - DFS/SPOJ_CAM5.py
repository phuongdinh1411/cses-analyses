#  Problem from SPOJ
#  https://www.spoj.com/problems/CAM5/
#
# Problem: CAM5 - Connected Components (Friendship Problem)
#
# Given N people (numbered 0 to N-1) and E friendship pairs, find the number
# of friend groups (connected components). Two people are in the same group
# if they are friends directly or through other friends.
#
# Input:
# - Line 1: T (number of test cases)
# - For each test case:
#   - Line 1: N (number of people)
#   - Line 2: E (number of friendship pairs)
#   - Next E lines: u v (friendship between person u and v)
#
# Output: For each test case, print the number of friend groups
#
# Approach: DFS to count connected components in undirected graph


def calc_disjoint_sets(Ni, graph):
    result = 0
    visited = [False for i in range(Ni)]

    for i in range(Ni):
        if visited[i]:
            continue
        stack = [i]
        visited[i] = True

        while len(stack) > 0:
            u = stack[-1]
            stack.pop()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        result += 1

    return result


def solution():
    results = []
    while True:
        new_line = input().strip()
        if new_line:
            t = int(new_line)
            break
    for i in range(t):
        while True:
            new_line = input().strip()
            if new_line:
                Ni = int(new_line)
                break
        ei = int(input())
        graph = [[] for jj in range(Ni)]
        for j in range(ei):
            start, end = map(int, input().split())
            graph[start].append(end)
            graph[end].append(start)

        results.append(calc_disjoint_sets(Ni, graph))

    print(*results, sep='\n')


solution()
