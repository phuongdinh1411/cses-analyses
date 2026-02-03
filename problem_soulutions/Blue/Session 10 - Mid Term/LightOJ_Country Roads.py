#  Problem from LightOJ
#  http://lightoj.com/volume_showproblem.php?problem=1002
#
# Problem Name: Country Roads
#
# Problem Description:
# Given an undirected weighted graph representing cities and roads,
# find the minimum "maximum edge weight" path from a source city to all other cities.
# The cost of a path is the maximum edge weight along that path (minimax path problem).
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N M: number of nodes and edges
#   - M lines with A B W: edge from A to B with weight W
#   - t: the source node
#
# Output Format:
# - For each test case: "Case X:" followed by the minimum maximum edge weight
#   to reach each city (0 to N-1), or "Impossible" if unreachable
#
# Key Approach/Algorithm:
# - Modified Dijkstra's algorithm
# - Instead of summing weights, track the maximum edge weight on the path
# - For relaxation: dist[v] = max(dist[u], edge_weight) if this is smaller than current dist[v]

import heapq
import sys


class input_tokenizer:
    __tokens = None

    def has_next(self):
        return self.__tokens != [] and self.__tokens != None

    def next(self):
        token = self.__tokens[-1]
        self.__tokens.pop()
        return token

    def __init__(self):
        self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def dijkstra(n, t, graph):

    dist = [-1 for x in range(n+1)]
    pqueue = []
    heapq.heappush(pqueue, Node(t, 0))
    dist[t] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        w = top.dist
        for neighbor in graph[u]:
            if (neighbor.dist < dist[neighbor.id] and dist[u] < dist[neighbor.id]) or dist[neighbor.id] == -1:
                dist[neighbor.id] = max(neighbor.dist, dist[u])
                heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))

    return dist


def solution():

    T = int(inp.next())
    case_number = 0

    for i in range(T):
        case_number += 1
        N = int(inp.next())
        M = int(inp.next())
        graph = [[] for x in range(N + 1)]
        for j in range(M):
            A = int(inp.next())
            B = int(inp.next())
            W = int(inp.next())

            graph[B].append(Node(A, W))
            graph[A].append(Node(B, W))

        t = int(inp.next())

        print('Case ' + str(case_number) + ':')
        dist = dijkstra(N, t, graph)
        for d in dist:
            if d > -1:
                print(d)
            else:
                print('Impossible')


solution()
