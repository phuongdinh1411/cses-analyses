#  Problem from LightOJ
#  http://lightoj.com/volume_showproblem.php?problem=1174
#
# Problem: Commandos
#
# A group of commandos starts at building S. They must visit ALL N buildings
# to complete their mission, then gather at building D. All commandos move
# simultaneously and take optimal paths.
#
# The total time is determined by the last commando to reach D. Find the
# minimum time for all commandos to complete the mission.
#
# Input:
# - Line 1: T (test cases)
# - For each test case:
#   - Line 1: N (buildings)
#   - Line 2: R (roads)
#   - Next R lines: u v (bidirectional road)
#   - Last line: S D (start and destination buildings)
#
# Output: Maximum of (dist[S][i] + dist[i][D]) for all buildings i
#
# Approach: Run Dijkstra once from S and once from D (reversed), then find
#           max(dist_from_S[i] + dist_from_D[i]) for all buildings i


import heapq
import sys
from collections import defaultdict


class InputTokenizer:
    def __init__(self):
        self._tokens = sys.stdin.read().split()[::-1]

    def next(self):
        return self._tokens.pop()


inp = InputTokenizer()


def dijkstra(n, source, graph):
    """Run Dijkstra from source, return distances to all nodes."""
    dist = [-1] * (n + 1)
    dist[source] = 0
    pqueue = [(0, source)]

    while pqueue:
        d, u = heapq.heappop(pqueue)

        # Skip if we've already found a better path
        if dist[u] != -1 and d > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = d + weight
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pqueue, (new_dist, v))

    return dist


def solution():
    T = int(inp.next())
    results = []

    for case in range(1, T + 1):
        N = int(inp.next())
        R = int(inp.next())

        graph = defaultdict(list)
        for _ in range(R):
            A = int(inp.next())
            B = int(inp.next())
            # Bidirectional edges with weight 1
            graph[A].append((B, 1))
            graph[B].append((A, 1))

        S = int(inp.next())
        D = int(inp.next())

        # Run Dijkstra from S and from D
        dist_from_S = dijkstra(N, S, graph)
        dist_from_D = dijkstra(N, D, graph)

        # Find maximum time: max(dist_from_S[i] + dist_from_D[i]) for all reachable i
        max_time = 0
        for i in range(N):
            if dist_from_S[i] != -1 and dist_from_D[i] != -1:
                max_time = max(max_time, dist_from_S[i] + dist_from_D[i])

        results.append(f'Case {case}: {max_time}')

    print(*results, sep='\n')


solution()
