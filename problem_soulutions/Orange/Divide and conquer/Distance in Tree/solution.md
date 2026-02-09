# Distance in Tree

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a tree with n vertices and a positive number k, find the number of distinct pairs of vertices which have a distance of exactly k between them. Note that pairs (u, v) and (v, u) are the same.

## Input Format
- First line: n and k (1 ≤ n ≤ 50000, 1 ≤ k ≤ 500)
- Next n-1 lines: edges aᵢ bᵢ (1 ≤ aᵢ, bᵢ ≤ n)

## Output Format
Print the number of distinct pairs with distance exactly k.

## Example
```
Input:
5 2
1 2
2 3
3 4
4 5

Output:
3
```
Tree is a path: 1-2-3-4-5. Pairs at distance exactly 2: (1,3), (2,4), (3,5). Total = 3.

## Solution

### Approach
Use Centroid Decomposition or simple DFS with counting:
1. For each node, count pairs passing through it
2. Use DFS to find distances from each node
3. Count pairs with distance sum = k

For small k (≤ 500), we can use DP on the tree.

### Python Solution (Tree DP)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(100000)

def solve():
  n, k = map(int, input().split())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  total_pairs = 0

  # cnt[v][d] = number of nodes at distance d in subtree of v
  # We'll compute this via DFS

  def dfs(u, parent):
    nonlocal total_pairs

    # cnt[d] = count of nodes at distance d from u in u's subtree
    cnt = [0] * (k + 1)
    cnt[0] = 1  # u itself at distance 0

    for v in adj[u]:
      if v == parent:
        continue

      # Get counts from child subtree
      child_cnt = dfs(v, u)

      # Count pairs: one node from previous subtrees, one from this child
      for d1 in range(k + 1):
        d2 = k - d1 - 1  # -1 because edge u-v adds 1
        if 0 <= d2 <= k and d2 < len(child_cnt):
          total_pairs += cnt[d1] * child_cnt[d2]

      # Merge child counts (shifted by 1 for edge u-v)
      for d in range(k):
        if d < len(child_cnt):
          cnt[d + 1] += child_cnt[d]

    return cnt

  dfs(1, -1)
  print(total_pairs)

if __name__ == "__main__":
  solve()
```

### Alternative Solution (Centroid Decomposition concept)

```python
from collections import defaultdict, deque

def solve():
  n, k = map(int, input().split())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  result = 0

  # For each node as root, count paths of length k passing through it
  visited = [False] * (n + 1)

  def count_at_dist(start, parent, dist):
    """Count nodes at each distance from start"""
    counts = defaultdict(int)
    queue = deque([(start, 0)])

    while queue:
      node, d = queue.popleft()
      if d > k:
        continue
      counts[d] += 1

      for neighbor in adj[node]:
        if neighbor != parent and not visited[neighbor]:
          queue.append((neighbor, d + 1))

    return counts

  # Simple O(n * k) approach
  for root in range(1, n + 1):
    cnt = [0] * (k + 2)
    cnt[0] = 1

    for child in adj[root]:
      # Get distances in child subtree
      child_dist = defaultdict(int)
      stack = [(child, root, 1)]

      while stack:
        node, par, d = stack.pop()
        if d <= k:
          child_dist[d] += 1
          for nxt in adj[node]:
            if nxt != par:
              stack.append((nxt, node, d + 1))

      # Count pairs
      for d, c in child_dist.items():
        if k - d >= 0:
          result += cnt[k - d] * c

      # Merge
      for d, c in child_dist.items():
        if d <= k:
          cnt[d] += c

  print(result // 2)  # Each pair counted twice

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × K) with tree DP
- **Space Complexity:** O(N × K) for DP arrays

### Key Insight
For each node u, count paths of length k passing through u by combining distances from different subtrees. If one subtree has nodes at distance d from u, and another has nodes at distance k-d, they form pairs at distance k.
