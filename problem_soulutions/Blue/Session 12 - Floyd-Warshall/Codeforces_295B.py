# Problem from Codeforces
# http://codeforces.com/problemset/problem/295/B
#
# Problem Name: Greg and Graph
#
# Problem Description:
# Given a weighted directed graph and an order of vertex deletions, compute
# the sum of all shortest paths after each deletion (in reverse, after each
# vertex is added back). Process deletions in reverse order to build the graph.
#
# Input Format:
# - N: number of vertices
# - N x N adjacency matrix with edge weights
# - Deletion order: sequence of N vertices to be deleted
#
# Output Format:
# - N integers: sum of all shortest paths after adding vertices in reverse
#   deletion order (i.e., before each deletion in original order)
#
# Key Approach/Algorithm:
# - Reverse the deletion order to process as additions
# - Use incremental Floyd-Warshall: when adding vertex k, update all pairs (i,j)
#   considering k as intermediate vertex
# - After adding each vertex, sum all current shortest paths
# - Output results in reverse (corresponding to original deletion order)

INF = float(1e9)
# sys.stdout = open("file.txt", "w+")


def floyd_warshall(N, matrix, del_list):

    ans = [0 for i in range(N + 1)]

    for k in range(N, 0, -1):
        c = del_list[k]
        for i in range(k + 1, N + 1):
            a = del_list[i]
            for j in range(k, N + 1):
                b = del_list[j]
                matrix[c][a] = min(matrix[c][a], matrix[c][b] + matrix[b][a])
                matrix[a][c] = min(matrix[a][c], matrix[a][b] + matrix[b][c])

        for i in range(k, N + 1):
            a = del_list[i]
            for j in range(k, N + 1):
                b = del_list[j]
                if a == b:
                    continue
                matrix[a][b] = min(matrix[a][b], matrix[a][c] + matrix[c][b])

        for i in range(k, N + 1):
            a = del_list[i]
            for j in range(k, N + 1):
                b = del_list[j]
                ans[k] += matrix[a][b]

    return ans[1:N+1]


def solution():
    N = int(input().strip())
    matrix = [[]]
    for i in range(N):
        new_line = [0] + list(map(int, input().strip().split()))
        matrix.append(new_line)

    del_list = [0] + list(map(int, input().strip().split()))

    print(*floyd_warshall(N, matrix, del_list), sep=' ')


solution()


