# Problem from Codeforces
# http://codeforces.com/problemset/problem/217/A
#
# Problem: Ice Skating
#
# Description:
# Bajtek wants to visit all snow drifts in a field. He can move from one
# drift to another if they share the same x-coordinate OR y-coordinate.
# Find the minimum number of extra paths (not along same x or y) needed
# to connect all drifts.
#
# Input:
# - First line: n (number of snow drifts)
# - Next n lines: x, y (coordinates of each drift)
#
# Output:
# - Minimum number of extra paths needed (= number of connected components - 1)
#
# Approach:
# - Use DSU to group drifts that share x or y coordinates
# - Count the number of distinct connected components
# - Answer is (number of components - 1)


parent = dict()
ranks = dict()


def make_set(N):
    global parent, ranks
    parent = [i for i in range(N + 5)]
    ranks = [0 for i in range(N + 5)]


def find_set(u):
    if parent[u] != u:
        parent[u] = find_set(parent[u])
    return parent[u]


def union_set(u, v):
    up = find_set(u)
    vp = find_set(v)

    if up == vp:
        return
    if ranks[up] > ranks[vp]:
        parent[vp] = up
    elif ranks[up] < ranks[vp]:
        parent[up] = vp
    else:
        parent[up] = vp
        ranks[vp] += 1


def solution():

    n_drifts = int(input())
    make_set(n_drifts)
    drifts = []
    for i in range(n_drifts):
        x, y = map(int, input().split())
        drifts.append([x, y])

    for i in range(n_drifts - 1):
        for j in range(i + 1, n_drifts):
            if drifts[i][0] == drifts[j][0] or drifts[i][1] == drifts[j][1]:
                union_set(i, j)

    leaders = dict()
    for i in range(n_drifts):
        leader = find_set(i)
        if leaders.get(leader) is not None:
            leaders[leader] += 1
        else:
            leaders[leader] = 1

    print(len(leaders) - 1)


solution()
