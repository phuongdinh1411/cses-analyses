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


from collections import deque


def bfs_count_possible_leaves(n, m, has_cat, graph):
    # Fixed: Handle edge case where n=1 (single node is both root and leaf)
    if n == 1:
        # Single node: it's a restaurant if it doesn't exceed cat limit
        return 1 if has_cat[0] <= m else 0

    consecutive_cats = [-1] * (n + 1)
    consecutive_cats[1] = has_cat[0]  # has_cat is 0-indexed

    # If root already exceeds limit, no restaurants reachable
    if consecutive_cats[1] > m:
        return 0

    total_restaurants = 0

    q = deque()
    q.append(1)

    while q:
        u = q.popleft()

        # Count neighbors (excluding parent via consecutive_cats check)
        children_count = sum(1 for v in graph[u] if consecutive_cats[v] == -1)

        # A leaf is a node with no unvisited children (and not the root if it has edges)
        if children_count == 0 and u != 1:
            total_restaurants += 1
        elif children_count == 0 and u == 1 and len(graph[1]) == 0:
            # Root with no edges (shouldn't happen for n > 1)
            total_restaurants += 1
        else:
            for v in graph[u]:
                if consecutive_cats[v] == -1:
                    if has_cat[v - 1] == 0:
                        consecutive_cats[v] = 0
                    else:
                        consecutive_cats[v] = consecutive_cats[u] + 1

                    if consecutive_cats[v] <= m:
                        q.append(v)

    return total_restaurants


def solution():
    n, m = map(int, input().split())
    has_cat = list(map(int, input().split()))
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        s, e = map(int, input().split())
        graph[s].append(e)
        graph[e].append(s)

    print(bfs_count_possible_leaves(n, m, has_cat, graph))


solution()
