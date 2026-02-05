# Oliver and the Game

## Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Oliver and Bob are playing Hide and Seek in the city of Byteland. The city has N houses connected by roads forming a tree structure with the King's Mansion at node 1 as the root.

Oliver hides in house X and Bob starts from house Y. Bob can either move:
- **Type 0**: Towards the King's Mansion (up the tree towards root)
- **Type 1**: Away from the King's Mansion (down the tree away from root)

Given Q queries, determine if Bob can find Oliver (reach house X from house Y) given the movement direction.

## Input Format
- First line: N (total houses)
- Next N-1 lines: A B (road between houses A and B)
- Next line: Q (number of queries)
- Next Q lines: type X Y (0/1, Oliver's house, Bob's house)

## Output Format
For each query, print "YES" if Bob can find Oliver, "NO" otherwise.

## Solution

### Approach
Use DFS to compute entry and exit times (Euler tour) for each node:
- Node A is ancestor of B if: entry[A] ≤ entry[B] and exit[A] ≥ exit[B]

For query (type, X, Y):
- **Type 0** (towards root): Bob can reach X only if X is an ancestor of Y
- **Type 1** (away from root): Bob can reach X only if X is a descendant of Y (Y is ancestor of X)

### Python Solution

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200000)

def solve():
  n = int(input())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  # DFS to compute entry and exit times
  entry = [0] * (n + 1)
  exit_time = [0] * (n + 1)
  timer = [0]

  def dfs(u, parent):
    timer[0] += 1
    entry[u] = timer[0]

    for v in adj[u]:
      if v != parent:
        dfs(v, u)

    timer[0] += 1
    exit_time[u] = timer[0]

  # Root the tree at node 1 (King's Mansion)
  dfs(1, -1)

  def is_ancestor(a, b):
    """Check if a is ancestor of b"""
    return entry[a] <= entry[b] and exit_time[a] >= exit_time[b]

  q = int(input())
  results = []

  for _ in range(q):
    query_type, x, y = map(int, input().split())

    if query_type == 0:
      # Moving towards mansion: X must be ancestor of Y
      if is_ancestor(x, y) and x != y:
        results.append("YES")
      else:
        results.append("NO")
    else:
      # Moving away from mansion: X must be descendant of Y (Y is ancestor of X)
      if is_ancestor(y, x) and x != y:
        results.append("YES")
      else:
        results.append("NO")

  print('\n'.join(results))

if __name__ == "__main__":
  solve()
```

### Iterative DFS Solution

```python
from collections import defaultdict

def solve():
  n = int(input())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  # Iterative DFS for entry/exit times
  entry = [0] * (n + 1)
  exit_time = [0] * (n + 1)

  timer = 0
  stack = [(1, -1, False)]  # (node, parent, processed)

  while stack:
    node, parent, processed = stack.pop()

    if processed:
      timer += 1
      exit_time[node] = timer
    else:
      timer += 1
      entry[node] = timer
      stack.append((node, parent, True))

      for child in adj[node]:
        if child != parent:
          stack.append((child, node, False))

  def is_ancestor(a, b):
    return entry[a] <= entry[b] and exit_time[a] >= exit_time[b]

  q = int(input())

  for _ in range(q):
    t, x, y = map(int, input().split())

    if t == 0:
      # Towards root: x must be ancestor of y
      print("YES" if x != y and is_ancestor(x, y) else "NO")
    else:
      # Away from root: x must be descendant of y
      print("YES" if x != y and is_ancestor(y, x) else "NO")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N) for DFS preprocessing, O(1) per query
- **Space Complexity:** O(N) for storing entry/exit times

### Key Insight
Using Euler tour (entry/exit times), we can check ancestor-descendant relationships in O(1):
- A is ancestor of B iff entry[A] ≤ entry[B] and exit[A] ≥ exit[B]

Moving "towards mansion" means moving up to ancestors, and "away from mansion" means moving down to descendants.
