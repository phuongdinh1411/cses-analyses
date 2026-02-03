# BLUE_LEC18P04
"""
Problem: Connecting Freckles / Minimum Spanning Tree on Points

Description:
Given N points (freckles) on a 2D plane with their (x, y) coordinates, find the minimum
total length of ink needed to connect all freckles. You can connect any two freckles
with a straight line, and the goal is to connect all freckles using minimum total distance.

This is the classic Minimum Spanning Tree (MST) problem where:
- Nodes are the freckle positions
- Edge weights are Euclidean distances between points
- We need to find a tree connecting all nodes with minimum total edge weight

Input Format:
- Line 1: Integer N (number of test cases)
- For each test case:
  - Blank line
  - Integer: number of freckles
  - Next lines: x y coordinates (floating point) for each freckle

Output Format:
- For each test case: The minimum total distance (2 decimal places)
- Blank line between test cases

Algorithm/Approach:
1. Build a complete graph where each pair of freckles has an edge with weight = Euclidean distance
2. Apply Kruskal's algorithm:
   - Sort all edges by weight
   - Use Union-Find to avoid cycles
   - Add edges to MST until (V-1) edges are selected
3. Return the sum of edge weights in the MST
"""
import math


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

    return mst


def calculate_distance(freckle1, freckle2):
    x1, y1 = freckle1
    x2, y2 = freckle2
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def solution():

    N = int(input())
    for t in range(N):
        input()
        global graph, dist
        graph = []
        dist = []
        freckles_number = int(input())
        freckles = []

        for i in range(freckles_number):
            x, y = map(float, input().split())
            freckles.append((x, y))

        for i in range(freckles_number):
            for j in range(i + 1, freckles_number):
                graph.append(Triad(i, j, calculate_distance(freckles[i], freckles[j])))

        make_set(freckles_number)

        print('%.2f' % kruskal(freckles_number))
        if t != N - 1:
            print()


solution()
