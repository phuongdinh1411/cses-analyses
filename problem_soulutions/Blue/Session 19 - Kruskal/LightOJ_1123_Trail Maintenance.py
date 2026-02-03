# Problem from LightOJ
# http://lightoj.com/volume_showproblem.php?problem=1123
#
# Problem: Trail Maintenance (LightOJ 1123)
#
# Description:
# A park has N fields connected by trails. Trails are added one by one.
# After each trail is added, compute the MST weight. Output -1 if the
# graph is not yet connected (before N-1 edges are added).
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
# - Return -1 until at least N-1 edges connect all nodes


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for _ in range(V + 1)]


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


def kruskal(number_of_fields):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    mst = 0
    while len(dist) != number_of_fields - 1 and i < len(graph):
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
            mst += edge.weight

    if len(dist) == number_of_fields - 1:
        return mst
    else:
        return -1


def solution():

    T = int(input())

    for t in range(T):
        global graph, dist
        graph = []
        N, M = map(int, input().split())
        print('Case {0}:'.format(t + 1))
        for i in range(M):
            x, y, z = map(int, input().split())
            graph.append(Triad(x, y, z))
            if i < N - 1:
                print(-1)
            else:
                dist = []
                make_set(N)
                minimum_distance = kruskal(N)
                print(minimum_distance)


solution()
