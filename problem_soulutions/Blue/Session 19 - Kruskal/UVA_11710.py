# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2757
#
# Problem: Expensive Subway (UVA 11710)
#
# Description:
# Calculate the minimum cost to build a subway system connecting all stations.
# Stations are given as names (strings). If impossible to connect all stations,
# output "Impossible".
#
# Input:
# - Multiple test cases until s=c=0
# - s (stations), c (connections)
# - s station names
# - c lines: station1 station2 cost
# - End station name (ignored)
#
# Output:
# - MST weight or "Impossible" if graph is disconnected
#
# Approach:
# - Map station names to indices using dictionary
# - Apply Kruskal's algorithm to find MST
# - Check if MST spans all stations (exactly s-1 edges)


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
    mst = 0
    while len(dist) != number_of_cities - 1 and i < len(graph):
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
            mst += edge.weight

    if len(dist) == number_of_cities - 1:
        return mst
    else:
        return 'Impossible'


def solution():

    while True:
        global graph, dist
        graph = []
        dist = []
        station_dictionary = {}
        s, c = map(int, input().split())
        if s == 0:
            break

        for i in range(s):
            station = input().strip()
            station_dictionary[station] = i
        for _ in range(c):
            x, y, z = input().split()
            graph.append(Triad(station_dictionary[x], station_dictionary[y], int(z)))

        input()

        make_set(s)

        print(kruskal(s))


solution()
