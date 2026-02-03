# Problem from Codeforces
# http://codeforces.com/problemset/problem/580/C
#
# Problem: Kefa and Park
#
# Kefa wants to visit restaurants located at the leaves of a tree. The tree
# has n vertices rooted at vertex 1. Each vertex either has a cat (1) or not (0).
# Kefa is afraid of cats and won't go through a path with more than m consecutive
# vertices containing cats.
#
# Count the number of restaurants (leaf nodes) Kefa can reach from the root
# without passing through more than m consecutive cats.
#
# Input:
# - Line 1: n m (vertices count, max consecutive cats allowed)
# - Line 2: n integers a[i] (1 if vertex i has a cat, 0 otherwise)
# - Next n-1 lines: u v (edge between vertices u and v)
#
# Output: Number of restaurants (leaves) Kefa can visit
#
# Approach: BFS/DFS from root, tracking consecutive cats on each path


import queue


def bfs_count_possible_leaves(n, m, a, graph):

    consecutive_cats = [-1 for i in range(n+9)]

    total_restaurants = 0

    consecutive_cats[1] = a[0]

    q = queue.Queue()
    q.put(1)

    while not q.empty():
        u = q.get()
        if len(graph[u]) == 1 and u != 1:
            total_restaurants += 1
        else:
            for v in graph[u]:
                if consecutive_cats[v] == -1:
                    if a[v-1] == 0:
                        consecutive_cats[v] = 0
                    else:
                        consecutive_cats[v] = consecutive_cats[u] + 1
                    if consecutive_cats[v] <= m:
                        q.put(v)
    return total_restaurants


def solution():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    graph = [[] for i in range(n + 1)]
    root = -1
    for i in range(1, n):
        s, e = map(int, input().split())
        graph[s].append(e)
        graph[e].append(s)

    print(bfs_count_possible_leaves(n, m, a, graph))


solution()


