# Problem from LightOJ
# http://lightoj.com/volume_showproblem.php?problem=1123
#
# Problem: Trail Maintenance (LightOJ 1123)
#
# Description:
# A park has N fields connected by trails. Trails are added one by one.
# After each trail is added, compute the MST weight. Output -1 if the
# graph is not yet connected.
#
# Input:
# - T (test cases)
# - For each test case:
#   - N (fields), M (trails to add)
#   - M lines: x, y, z (trail from field x to y with length z)
#
# Output:
# - After each trail addition: MST weight or -1 if not connected
#
# Approach:
# - Incrementally add edges to the graph
# - After each addition, run Kruskal's algorithm to find MST
# - Use DSU for cycle detection in Kruskal's
# - Return -1 if fewer than N-1 edges form the MST (graph not connected)


import sys
sys.setrecursionlimit(10000)


class Edge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight


def make_set(n):
    return list(range(n + 1)), [0] * (n + 1)


def find_set(parent, u):
    if parent[u] != u:
        parent[u] = find_set(parent, parent[u])
    return parent[u]


def union_set(parent, rank, u, v):
    up = find_set(parent, u)
    vp = find_set(parent, v)
    if up == vp:
        return False
    if rank[up] > rank[vp]:
        parent[vp] = up
    elif rank[up] < rank[vp]:
        parent[up] = vp
    else:
        parent[up] = vp
        rank[vp] += 1
    return True


def kruskal(n, edges):
    """Run Kruskal's algorithm. Return MST weight or -1 if not connected."""
    edges_sorted = sorted(edges, key=lambda e: e.weight)
    parent, rank = make_set(n)

    mst_weight = 0
    edges_used = 0

    for edge in edges_sorted:
        if edges_used == n - 1:
            break
        u = find_set(parent, edge.source)
        v = find_set(parent, edge.target)
        if u != v:
            union_set(parent, rank, u, v)
            mst_weight += edge.weight
            edges_used += 1

    # Fixed: Check if we have enough edges to connect all nodes
    if edges_used == n - 1:
        return mst_weight
    return -1


def solution():
    T = int(input())

    for t in range(T):
        N, M = map(int, input().split())
        print(f'Case {t + 1}:')

        edges = []
        for i in range(M):
            x, y, z = map(int, input().split())
            edges.append(Edge(x, y, z))

            # Fixed: Always run Kruskal and let it determine if connected
            # Don't assume first N-1 edges can't form a connected graph
            result = kruskal(N, edges)
            print(result)


solution()
