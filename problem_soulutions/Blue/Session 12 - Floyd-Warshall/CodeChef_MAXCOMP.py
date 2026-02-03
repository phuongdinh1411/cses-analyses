# Problem from CodeChef
# https://www.codechef.com/problems/MAXCOMP
#
# Problem Name: Maximum Weight Composition
#
# Problem Description:
# Given N intervals with start position, end position, and cost, find the
# maximum total cost by selecting non-overlapping intervals. An interval
# from [si, ei] must end before the next one starts.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N: number of intervals
#   - N lines with si ei ci: start, end, and cost of interval
#
# Output Format:
# - Maximum total cost achievable with non-overlapping intervals
#
# Key Approach/Algorithm:
# - Dynamic programming approach (simplified from Floyd-Warshall concept)
# - For each endpoint, compute maximum cost considering all intervals ending there
# - mmax[x] = max(mmax[x], graph[xx][x] + mmax[xx]) for all xx < x
# - Essentially an interval scheduling maximization problem
import sys

INF = int(1e9)
# sys.stdout = open("file.txt", "w+")


def floyd_warshall(M, graph):
    dist = [[0] * M for i in range(M)]
    for i in range(M):
        for j in range(M):
            dist[i][j] = graph[i][j]

    for x in range(5):
        for k in range(M):
            for i in range(M):
                for j in range(M):
                    if i <= k <= j and dist[i][j] < dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

    max_comp = 0
    for i in range(M):
        for j in range(M):
            if max_comp < dist[i][j]:
                max_comp = dist[i][j]

    return max_comp


def solution():
    T = int(input().strip())
    M = 49
    for i in range(T):
        graph = [[0] * M for x in range(M)]
        N = int(input().strip())
        e_max = 0

        for j in range(N):
            si, ei, ci = map(int, input().strip().split())
            if ei > e_max:
                e_max = ei
            if ci > graph[si][ei]:
                graph[si][ei] = ci

        # Start of Simple solution
        mmax = [0 for x in range(M)]
        for x in range(1, e_max + 1):
            m = 0
            for xx in range(x):
                if m < graph[xx][x] + mmax[xx]:
                    m = graph[xx][x] + mmax[xx]
                mmax[x] = m

        print(mmax[e_max])
        # End of Simple solution

        # print(floyd_warshall(M, graph))


solution()


