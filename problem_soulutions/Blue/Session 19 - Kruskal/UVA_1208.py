# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3649
#
# Problem: Oreon (UVA 1208)
#
# Description:
# Given a weighted adjacency matrix of cities, find and print all edges
# in the Minimum Spanning Tree. Cities are labeled A, B, C, etc.
# Output edges in sorted order (by source, then by weight).
#
# Input:
# - Number of test cases
# - For each test case:
#   - Number of cities
#   - Adjacency matrix (comma-separated, 0 means no edge)
#
# Output:
# - "Case X:" followed by MST edges in format "A-B W"
#
# Approach:
# - Parse adjacency matrix to create edge list
# - Apply Kruskal's algorithm with edges sorted by (weight, source)
# - Print MST edges with city letters


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for i in range(V + 1)]


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
    graph.sort(key=lambda _edge: (_edge.weight, _edge.source))
    i = 0
    while len(dist) != number_of_cities - 1:
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)


def print_MST():
    ans = 0
    for e in dist:
        source = chr(e.source + 65)
        target = chr(e.target + 65)
        print("{0}-{1} {2}".format(source, target, e.weight))
        ans += e.weight


def solution():

    number_of_test_cases = int(input())

    for t in range(number_of_test_cases):
        global graph, dist
        graph = []
        dist = []
        number_of_cities = int(input())
        for i in range(number_of_cities):
            securities = input().split(', ')
            for j in range(i):
                security = int(securities[j])
                if security > 0:
                    graph.append(Triad(j, i, security))
        make_set(number_of_cities)
        kruskal(number_of_cities)
        print('Case {0}:'.format(t + 1))
        print_MST()


solution()
