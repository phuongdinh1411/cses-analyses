# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2678
#
# Problem: Dark Roads (UVA 11631)
#
# Description:
# A city wants to save electricity by turning off some street lights.
# They need to keep lights on only for roads in the MST (to maintain
# connectivity). Calculate how much power can be saved.
#
# Input:
# - Multiple test cases until m=n=0
# - m (junctions), n (roads)
# - n lines: x, y, z (road from x to y with power cost z)
#
# Output:
# - Total power saved = (sum of all edges) - (MST weight)
#
# Approach:
# - Use Kruskal's algorithm to find MST
# - Sum weights of edges not in MST (edges that form cycles)
# - This gives the total power that can be saved


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


def kruskal(number_of_cities):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    saved = 0
    while len(dist) != number_of_cities - 1:
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
        else:
            saved += edge.weight

    for j in range(i, len(graph)):
        saved += graph[j].weight

    return saved


def solution():

    while True:
        global graph, dist
        graph = []
        dist = []
        m, n = map(int, input().split())
        if m == 0:
            break
        for _ in range(n):
            x, y, z = map(int, input().split())
            graph.append(Triad(x, y, z))

        make_set(m)

        print(kruskal(m))


solution()
