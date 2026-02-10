# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2833
#
# Problem: Airports (UVA 11733)
#
# Description:
# Connect N cities using either airports or roads. Each city needs either
# an airport OR road connection to an airport city. Building an airport
# costs A, and each road has its own cost. Minimize total cost.
#
# Input:
# - T (test cases)
# - For each test case:
#   - N (cities), M (possible roads), A (airport cost)
#   - M lines: x, y, z (road from x to y with cost z)
#
# Output:
# - "Case #X: cost airports" (total cost and number of airports built)
#
# Approach:
# - Modified Kruskal's algorithm
# - Only add edge to MST if its cost < airport cost A
# - Each connected component needs exactly one airport
# - Count final number of components


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


def kruskal(n, edges, airport_cost):
    """
    Modified Kruskal: only use edges cheaper than airport cost.
    Returns (total_cost, number_of_airports).
    """
    edges_sorted = sorted(edges, key=lambda e: e.weight)
    parent, rank = make_set(n)

    road_cost = 0

    for edge in edges_sorted:
        # Fixed: Only add edge if it's cheaper than building an airport
        if edge.weight >= airport_cost:
            break  # Sorted by weight, so remaining edges are also >= airport_cost

        u = find_set(parent, edge.source)
        v = find_set(parent, edge.target)
        if u != v:
            union_set(parent, rank, u, v)
            road_cost += edge.weight

    # Count number of connected components (each needs an airport)
    roots = set()
    for i in range(1, n + 1):
        roots.add(find_set(parent, i))
    num_airports = len(roots)

    total_cost = road_cost + num_airports * airport_cost
    return total_cost, num_airports


def solution():
    T = int(input())

    for t in range(T):
        N, M, A = map(int, input().split())

        edges = []
        for _ in range(M):
            x, y, z = map(int, input().split())
            edges.append(Edge(x, y, z))

        cost, num_airports = kruskal(N, edges, A)
        print(f'Case #{t + 1}: {cost} {num_airports}')


solution()
