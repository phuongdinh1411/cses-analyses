# Problem from Codeforces
# http://codeforces.com/problemset/problem/103/B
#
# Problem: Cthulhu
#
# Description:
# Determine if a given graph represents "Cthulhu" - a connected graph with
# exactly one cycle (i.e., the number of edges equals the number of vertices
# and all vertices are connected).
#
# Input:
# - First line: n (vertices), m (edges)
# - Next m lines: a, b (edge between vertices a and b)
#
# Output:
# - "FHTAGN!" if the graph is a Cthulhu
# - "NO" otherwise
#
# Approach:
# - A graph is Cthulhu iff: n == m AND all vertices are in one component
# - Use Disjoint Set Union (DSU) to check connectivity
# - If n != m, immediately return NO
# - Check if all vertices have the same parent (single component)


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

    m, n = map(int, input().split())
    if m != n:
        print('NO')
        return

    make_set(m)
    for i in range(m):
        a, b = map(int, input().split())
        union_set(a, b)

    top_parent = find_set(1)
    for i in range(2, m):
        if find_set(i) != top_parent:
            print('NO')
            return

    print('FHTAGN!')


solution()
