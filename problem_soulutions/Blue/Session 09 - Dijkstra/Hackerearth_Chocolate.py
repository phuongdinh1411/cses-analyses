#  Problem from Hackerearth
#  https://www.hackerearth.com/practice/algorithms/graphs/shortest-path-algorithms/practice-problems/algorithm/successful-completion-of-project/
#
# Problem: Chocolate Journey
#
# There are N cities connected by M bidirectional roads. K cities have
# chocolate shops. You need to travel from city A to city B, but must
# buy chocolate from one of the K cities. The chocolate expires after
# X time units, so you must reach B within X time from the chocolate city.
#
# Find the minimum time to go from A to a chocolate city and then to B,
# such that the chocolate city to B takes at most X time.
#
# Input:
# - Line 1: N M K X (cities, roads, chocolate cities, max time for chocolate)
# - Line 2: K integers (chocolate city IDs)
# - Next M lines: u v w (bidirectional road with weight w)
# - Last line: A B (start and destination)
#
# Output: Minimum total time, or -1 if impossible
#
# Approach: Run Dijkstra from A and from B, find best chocolate city


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


def dijkstra(N, A, graph):

    dist = [-1 for x in range(N+1)]
    pqueue = []
    heapq.heappush(pqueue, Node(A, 0))
    dist[A] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        w = top.dist
        for neighbor in graph[u]:
            if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
                dist[neighbor.id] = w + neighbor.dist
                heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))

    return dist


def solution():

    N = int(inp.next())
    M = int(inp.next())
    k = int(inp.next())
    x = int(inp.next())

    chocolate_cities = []
    for i in range(k):
        chocolate_cities.append(int(inp.next()))

    graph = [[] for i in range(N + 1)]
    for i in range(M):
        A = int(inp.next())
        B = int(inp.next())
        W = int(inp.next())

        graph[B].append(Node(A, W))
        graph[A].append(Node(B, W))

    A = int(inp.next())
    B = int(inp.next())

    dist_from_b = dijkstra(N, B, graph)
    found_chocolate_city_to_b = False
    for i in range(k):
        if x >= dist_from_b[chocolate_cities[i]] >= 0:
            found_chocolate_city_to_b = True
            break

    if not found_chocolate_city_to_b:
        print(-1)
        return

    dist_from_a = dijkstra(N, A, graph)

    found_chocolate_city_to_a = False
    for i in range(k):
        if dist_from_a[chocolate_cities[i]] >= 0:
            found_chocolate_city_to_a = True
            break

    if not found_chocolate_city_to_a:
        print(-1)
        return

    min_time = -1

    for i in range(k):
        if x >= dist_from_b[chocolate_cities[i]] >= 0 and dist_from_a[chocolate_cities[i]] >= 0:
            if min_time == -1 or min_time > dist_from_b[chocolate_cities[i]] + dist_from_a[chocolate_cities[i]]:
                min_time = dist_from_b[chocolate_cities[i]] + dist_from_a[chocolate_cities[i]]

    print(min_time)


solution()
