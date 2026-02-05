---
layout: simple
title: "Code Templates"
permalink: /quick_reference/code_templates
---

# Code Templates

Ready-to-use templates for common algorithms and data structures.

## Table of Contents
1. [Binary Search](#binary-search)
2. [Two Pointers & Sliding Window](#two-pointers--sliding-window)
3. [Graph Algorithms](#graph-algorithms)
4. [Dynamic Programming](#dynamic-programming)
5. [Data Structures](#data-structures)
6. [Tree Algorithms](#tree-algorithms)
7. [String Algorithms](#string-algorithms)
8. [Math & Number Theory](#math--number-theory)

---

## Binary Search

### Standard Binary Search
```python
def binary_search(arr, target):
  """Find target in sorted array. Returns index or -1."""
  left, right = 0, len(arr) - 1
  while left <= right:
    mid = left + (right - left) // 2  # Avoid overflow
    if arr[mid] == target:
      return mid
    elif arr[mid] < target:
      left = mid + 1
    else:
      right = mid - 1
  return -1
```

### Lower Bound (First >= target)
```python
def lower_bound(arr, target):
  """Find first index where arr[i] >= target."""
  left, right = 0, len(arr)
  while left < right:
    mid = (left + right) // 2
    if arr[mid] >= target:
      right = mid
    else:
      left = mid + 1
  return left

# Using bisect
from bisect import bisect_left
idx = bisect_left(arr, target)
```

### Upper Bound (First > target)
```python
def upper_bound(arr, target):
  """Find first index where arr[i] > target."""
  left, right = 0, len(arr)
  while left < right:
    mid = (left + right) // 2
    if arr[mid] > target:
      right = mid
    else:
      left = mid + 1
  return left

# Using bisect
from bisect import bisect_right
idx = bisect_right(arr, target)
```

### Binary Search on Answer
```python
def binary_search_on_answer(lo, hi, is_feasible):
  """
  Find minimum value satisfying condition.
  is_feasible(x) returns True if x satisfies condition.
  """
  while lo < hi:
    mid = (lo + hi) // 2
    if is_feasible(mid):
      hi = mid  # Answer could be mid or smaller
    else:
      lo = mid + 1  # Need larger value
  return lo

# Example: Minimum time to complete n tasks
def min_time(machines, n):
  def can_complete(time):
    return sum(time // m for m in machines) >= n

  lo, hi = 1, max(machines) * n
  return binary_search_on_answer(lo, hi, can_complete)
```

---

## Two Pointers & Sliding Window

### Two Sum (Sorted Array)
```python
def two_sum_sorted(arr, target):
  """Find two numbers that sum to target in sorted array."""
  left, right = 0, len(arr) - 1
  while left < right:
    current_sum = arr[left] + arr[right]
    if current_sum == target:
      return [left, right]
    elif current_sum < target:
      left += 1
    else:
      right -= 1
  return [-1, -1]
```

### Fixed Size Sliding Window
```python
def max_sum_subarray_k(arr, k):
  """Maximum sum of subarray of size k."""
  if len(arr) < k:
    return 0

  window_sum = sum(arr[:k])
  max_sum = window_sum

  for i in range(k, len(arr)):
    window_sum += arr[i] - arr[i - k]  # Add new, remove old
    max_sum = max(max_sum, window_sum)

  return max_sum
```

### Variable Size Sliding Window
```python
def longest_subarray_with_sum_at_most_k(arr, k):
  """Longest subarray with sum <= k."""
  left = 0
  current_sum = 0
  max_length = 0

  for right in range(len(arr)):
    current_sum += arr[right]

    while current_sum > k and left <= right:
      current_sum -= arr[left]
      left += 1

    max_length = max(max_length, right - left + 1)

  return max_length
```

### Longest Substring Without Repeating
```python
def longest_unique_substring(s):
  """Length of longest substring without repeating characters."""
  char_index = {}
  left = 0
  max_length = 0

  for right, char in enumerate(s):
    if char in char_index and char_index[char] >= left:
      left = char_index[char] + 1
    char_index[char] = right
    max_length = max(max_length, right - left + 1)

  return max_length
```

### Sliding Window with Hash Map
```python
def subarrays_with_k_distinct(arr, k):
  """Count subarrays with exactly k distinct elements."""
  def at_most_k(k):
    count = {}
    left = result = 0
    for right, num in enumerate(arr):
      count[num] = count.get(num, 0) + 1
      while len(count) > k:
        count[arr[left]] -= 1
        if count[arr[left]] == 0:
          del count[arr[left]]
        left += 1
      result += right - left + 1
    return result

  return at_most_k(k) - at_most_k(k - 1)
```

---

## Graph Algorithms

### BFS (Shortest Path in Unweighted Graph)
```python
from collections import deque

def bfs(graph, start, target):
  """Find shortest path from start to target."""
  if start == target:
    return 0

  visited = {start}
  queue = deque([(start, 0)])  # (node, distance)

  while queue:
    node, dist = queue.popleft()

    for neighbor in graph[node]:
      if neighbor == target:
        return dist + 1
      if neighbor not in visited:
        visited.add(neighbor)
        queue.append((neighbor, dist + 1))

  return -1  # Not reachable
```

### DFS (Connected Components)
```python
def count_components(n, edges):
  """Count connected components in undirected graph."""
  graph = [[] for _ in range(n)]
  for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

  visited = [False] * n
  components = 0

  def dfs(node):
    visited[node] = True
    for neighbor in graph[node]:
      if not visited[neighbor]:
        dfs(neighbor)

  for i in range(n):
    if not visited[i]:
      dfs(i)
      components += 1

  return components
```

### Dijkstra's Algorithm
```python
import heapq

def dijkstra(graph, start):
  """
  Shortest paths from start to all nodes.
  graph[u] = [(v, weight), ...]
  """
  n = len(graph)
  dist = [float('inf')] * n
  dist[start] = 0
  pq = [(0, start)]  # (distance, node)

  while pq:
    d, u = heapq.heappop(pq)

    if d > dist[u]:
      continue  # Skip outdated entries

    for v, weight in graph[u]:
      if dist[u] + weight < dist[v]:
        dist[v] = dist[u] + weight
        heapq.heappush(pq, (dist[v], v))

  return dist
```

### Bellman-Ford (Negative Edges)
```python
def bellman_ford(n, edges, start):
  """
  Shortest paths with negative edges.
  edges = [(u, v, weight), ...]
  Returns distances or None if negative cycle exists.
  """
  dist = [float('inf')] * n
  dist[start] = 0

  # Relax all edges n-1 times
  for _ in range(n - 1):
    for u, v, w in edges:
      if dist[u] != float('inf') and dist[u] + w < dist[v]:
        dist[v] = dist[u] + w

  # Check for negative cycles
  for u, v, w in edges:
    if dist[u] != float('inf') and dist[u] + w < dist[v]:
      return None  # Negative cycle detected

  return dist
```

### Floyd-Warshall (All Pairs)
```python
def floyd_warshall(n, edges):
  """All pairs shortest paths. O(n^3)"""
  INF = float('inf')
  dist = [[INF] * n for _ in range(n)]

  for i in range(n):
    dist[i][i] = 0

  for u, v, w in edges:
    dist[u][v] = w

  for k in range(n):
    for i in range(n):
      for j in range(n):
        if dist[i][k] + dist[k][j] < dist[i][j]:
          dist[i][j] = dist[i][k] + dist[k][j]

  return dist
```

### Topological Sort (Kahn's Algorithm)
```python
from collections import deque

def topological_sort(n, edges):
  """
  Topological sort using BFS (Kahn's).
  Returns sorted list or empty if cycle exists.
  """
  graph = [[] for _ in range(n)]
  indegree = [0] * n

  for u, v in edges:
    graph[u].append(v)
    indegree[v] += 1

  queue = deque([i for i in range(n) if indegree[i] == 0])
  result = []

  while queue:
    node = queue.popleft()
    result.append(node)

    for neighbor in graph[node]:
      indegree[neighbor] -= 1
      if indegree[neighbor] == 0:
        queue.append(neighbor)

  return result if len(result) == n else []  # Empty = cycle
```

### Union-Find (Disjoint Set Union)
```python
class UnionFind:
  def __init__(self, n):
    self.parent = list(range(n))
    self.rank = [0] * n

  def find(self, x):
    """Find with path compression."""
    if self.parent[x] != x:
      self.parent[x] = self.find(self.parent[x])
    return self.parent[x]

  def union(self, x, y):
    """Union by rank. Returns True if merged."""
    px, py = self.find(x), self.find(y)
    if px == py:
      return False

    if self.rank[px] < self.rank[py]:
      px, py = py, px
    self.parent[py] = px
    if self.rank[px] == self.rank[py]:
      self.rank[px] += 1
    return True

  def connected(self, x, y):
    return self.find(x) == self.find(y)
```

---

## Dynamic Programming

### 1D DP: Fibonacci Pattern
```python
def climb_stairs(n):
  """Number of ways to climb n stairs (1 or 2 steps)."""
  if n <= 2:
    return n

  prev2, prev1 = 1, 2
  for i in range(3, n + 1):
    curr = prev1 + prev2
    prev2, prev1 = prev1, curr

  return prev1
```

### 1D DP: Coin Change (Minimum Coins)
```python
def min_coins(coins, amount):
  """Minimum coins to make amount."""
  dp = [float('inf')] * (amount + 1)
  dp[0] = 0

  for i in range(1, amount + 1):
    for coin in coins:
      if coin <= i:
        dp[i] = min(dp[i], dp[i - coin] + 1)

  return dp[amount] if dp[amount] != float('inf') else -1
```

### 1D DP: Count Ways (Permutations)
```python
def count_ways_permutations(coins, target):
  """Count ordered ways to make target (order matters)."""
  MOD = 10**9 + 7
  dp = [0] * (target + 1)
  dp[0] = 1

  for i in range(1, target + 1):
    for coin in coins:
      if coin <= i:
        dp[i] = (dp[i] + dp[i - coin]) % MOD

  return dp[target]
```

### 1D DP: Count Ways (Combinations)
```python
def count_ways_combinations(coins, target):
  """Count unordered ways to make target (order doesn't matter)."""
  MOD = 10**9 + 7
  dp = [0] * (target + 1)
  dp[0] = 1

  for coin in coins:  # Coin loop OUTER for combinations
    for i in range(coin, target + 1):
      dp[i] = (dp[i] + dp[i - coin]) % MOD

  return dp[target]
```

### 2D DP: Grid Paths
```python
def unique_paths(m, n):
  """Count paths from (0,0) to (m-1,n-1) moving right/down."""
  dp = [[1] * n for _ in range(m)]

  for i in range(1, m):
    for j in range(1, n):
      dp[i][j] = dp[i-1][j] + dp[i][j-1]

  return dp[m-1][n-1]

# Space optimized
def unique_paths_optimized(m, n):
  dp = [1] * n
  for i in range(1, m):
    for j in range(1, n):
      dp[j] += dp[j-1]
  return dp[n-1]
```

### 2D DP: Longest Common Subsequence
```python
def lcs(s1, s2):
  """Length of longest common subsequence."""
  m, n = len(s1), len(s2)
  dp = [[0] * (n + 1) for _ in range(m + 1)]

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if s1[i-1] == s2[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1
      else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

  return dp[m][n]
```

### 0/1 Knapsack
```python
def knapsack(weights, values, capacity):
  """Maximum value with given capacity."""
  n = len(weights)
  dp = [[0] * (capacity + 1) for _ in range(n + 1)]

  for i in range(1, n + 1):
    for w in range(capacity + 1):
      dp[i][w] = dp[i-1][w]  # Don't take item i
      if weights[i-1] <= w:
        dp[i][w] = max(dp[i][w],
               dp[i-1][w-weights[i-1]] + values[i-1])

  return dp[n][capacity]
```

### Longest Increasing Subsequence (O(n log n))
```python
from bisect import bisect_left

def lis(arr):
  """Length of longest increasing subsequence."""
  tails = []  # tails[i] = smallest tail of LIS of length i+1

  for num in arr:
    pos = bisect_left(tails, num)
    if pos == len(tails):
      tails.append(num)
    else:
      tails[pos] = num

  return len(tails)
```

---

## Data Structures

### Monotonic Stack
```python
def next_greater_element(arr):
  """For each element, find next greater element index."""
  n = len(arr)
  result = [-1] * n
  stack = []  # Stack of indices, decreasing values

  for i in range(n):
    while stack and arr[stack[-1]] < arr[i]:
      idx = stack.pop()
      result[idx] = i
    stack.append(i)

  return result
```

### Prefix Sum
```python
def build_prefix_sum(arr):
  """Build prefix sum array."""
  prefix = [0] * (len(arr) + 1)
  for i, num in enumerate(arr):
    prefix[i + 1] = prefix[i] + num
  return prefix

def range_sum(prefix, left, right):
  """Sum of arr[left:right+1] using prefix sum."""
  return prefix[right + 1] - prefix[left]
```

### Segment Tree (Range Sum)
```python
class SegmentTree:
  def __init__(self, arr):
    self.n = len(arr)
    self.tree = [0] * (4 * self.n)
    self._build(arr, 1, 0, self.n - 1)

  def _build(self, arr, node, start, end):
    if start == end:
      self.tree[node] = arr[start]
    else:
      mid = (start + end) // 2
      self._build(arr, 2*node, start, mid)
      self._build(arr, 2*node+1, mid+1, end)
      self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

  def update(self, idx, val, node=1, start=0, end=None):
    if end is None: end = self.n - 1
    if start == end:
      self.tree[node] = val
    else:
      mid = (start + end) // 2
      if idx <= mid:
        self.update(idx, val, 2*node, start, mid)
      else:
        self.update(idx, val, 2*node+1, mid+1, end)
      self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

  def query(self, l, r, node=1, start=0, end=None):
    if end is None: end = self.n - 1
    if r < start or l > end:
      return 0
    if l <= start and end <= r:
      return self.tree[node]
    mid = (start + end) // 2
    return (self.query(l, r, 2*node, start, mid) +
        self.query(l, r, 2*node+1, mid+1, end))
```

### Fenwick Tree (Binary Indexed Tree)
```python
class FenwickTree:
  def __init__(self, n):
    self.n = n
    self.tree = [0] * (n + 1)

  def update(self, i, delta):
    """Add delta to index i (1-indexed)."""
    while i <= self.n:
      self.tree[i] += delta
      i += i & (-i)

  def query(self, i):
    """Sum of elements [1, i]."""
    total = 0
    while i > 0:
      total += self.tree[i]
      i -= i & (-i)
    return total

  def range_query(self, l, r):
    """Sum of elements [l, r]."""
    return self.query(r) - self.query(l - 1)
```

---

## Tree Algorithms

### LCA with Binary Lifting
```python
import math

class LCA:
  def __init__(self, n, edges, root=0):
    self.n = n
    self.LOG = int(math.log2(n)) + 1
    self.parent = [[-1] * n for _ in range(self.LOG)]
    self.depth = [0] * n

    # Build tree
    graph = [[] for _ in range(n)]
    for u, v in edges:
      graph[u].append(v)
      graph[v].append(u)

    # DFS to set parent[0] and depth
    stack = [(root, -1, 0)]
    while stack:
      node, par, d = stack.pop()
      self.parent[0][node] = par
      self.depth[node] = d
      for neighbor in graph[node]:
        if neighbor != par:
          stack.append((neighbor, node, d + 1))

    # Build sparse table
    for k in range(1, self.LOG):
      for v in range(n):
        if self.parent[k-1][v] != -1:
          self.parent[k][v] = self.parent[k-1][self.parent[k-1][v]]

  def lca(self, u, v):
    if self.depth[u] < self.depth[v]:
      u, v = v, u

    # Bring to same depth
    diff = self.depth[u] - self.depth[v]
    for k in range(self.LOG):
      if (diff >> k) & 1:
        u = self.parent[k][u]

    if u == v:
      return u

    # Binary search for LCA
    for k in range(self.LOG - 1, -1, -1):
      if self.parent[k][u] != self.parent[k][v]:
        u = self.parent[k][u]
        v = self.parent[k][v]

    return self.parent[0][u]
```

### Tree Diameter
```python
def tree_diameter(n, edges):
  """Find diameter of tree (longest path)."""
  from collections import deque

  graph = [[] for _ in range(n)]
  for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

  def bfs_farthest(start):
    visited = [-1] * n
    visited[start] = 0
    queue = deque([start])
    farthest = start

    while queue:
      node = queue.popleft()
      for neighbor in graph[node]:
        if visited[neighbor] == -1:
          visited[neighbor] = visited[node] + 1
          queue.append(neighbor)
          if visited[neighbor] > visited[farthest]:
            farthest = neighbor

    return farthest, visited[farthest]

  # BFS from any node to find one end
  end1, _ = bfs_farthest(0)
  # BFS from end1 to find diameter
  _, diameter = bfs_farthest(end1)

  return diameter
```

---

## String Algorithms

### KMP Pattern Matching
```python
def kmp_search(text, pattern):
  """Find all occurrences of pattern in text."""
  def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
      if pattern[i] == pattern[length]:
        length += 1
        lps[i] = length
        i += 1
      elif length != 0:
        length = lps[length - 1]
      else:
        lps[i] = 0
        i += 1
    return lps

  lps = build_lps(pattern)
  matches = []
  i = j = 0

  while i < len(text):
    if pattern[j] == text[i]:
      i += 1
      j += 1

    if j == len(pattern):
      matches.append(i - j)
      j = lps[j - 1]
    elif i < len(text) and pattern[j] != text[i]:
      if j != 0:
        j = lps[j - 1]
      else:
        i += 1

  return matches
```

### Z-Algorithm
```python
def z_function(s):
  """Build Z-array: z[i] = length of longest substring starting at i
  that matches prefix of s."""
  n = len(s)
  z = [0] * n
  l = r = 0

  for i in range(1, n):
    if i < r:
      z[i] = min(r - i, z[i - l])

    while i + z[i] < n and s[z[i]] == s[i + z[i]]:
      z[i] += 1

    if i + z[i] > r:
      l, r = i, i + z[i]

  z[0] = n
  return z
```

---

## Math & Number Theory

### Modular Arithmetic
```python
MOD = 10**9 + 7

def mod_add(a, b):
  return (a + b) % MOD

def mod_sub(a, b):
  return (a - b + MOD) % MOD

def mod_mul(a, b):
  return (a * b) % MOD

def mod_pow(base, exp, mod=MOD):
  """Fast exponentiation: base^exp mod mod."""
  result = 1
  base %= mod
  while exp > 0:
    if exp & 1:
      result = result * base % mod
    exp >>= 1
    base = base * base % mod
  return result

def mod_inv(a, mod=MOD):
  """Modular inverse using Fermat's little theorem (mod must be prime)."""
  return mod_pow(a, mod - 2, mod)
```

### Sieve of Eratosthenes
```python
def sieve(n):
  """Return list of primes up to n."""
  is_prime = [True] * (n + 1)
  is_prime[0] = is_prime[1] = False

  for i in range(2, int(n**0.5) + 1):
    if is_prime[i]:
      for j in range(i*i, n + 1, i):
        is_prime[j] = False

  return [i for i in range(n + 1) if is_prime[i]]
```

### GCD and LCM
```python
from math import gcd

def lcm(a, b):
  return a * b // gcd(a, b)

# Extended GCD
def extended_gcd(a, b):
  """Returns (gcd, x, y) such that a*x + b*y = gcd."""
  if b == 0:
    return a, 1, 0
  g, x, y = extended_gcd(b, a % b)
  return g, y, x - (a // b) * y
```

### Combinatorics
```python
def precompute_factorials(n, mod=MOD):
  """Precompute factorials and inverse factorials."""
  fact = [1] * (n + 1)
  for i in range(1, n + 1):
    fact[i] = fact[i-1] * i % mod

  inv_fact = [1] * (n + 1)
  inv_fact[n] = mod_pow(fact[n], mod - 2, mod)
  for i in range(n - 1, -1, -1):
    inv_fact[i] = inv_fact[i + 1] * (i + 1) % mod

  return fact, inv_fact

def nCr(n, r, fact, inv_fact, mod=MOD):
  """Compute nCr using precomputed factorials."""
  if r < 0 or r > n:
    return 0
  return fact[n] * inv_fact[r] % mod * inv_fact[n-r] % mod
```

---

## I/O Template

```python
import sys
from collections import defaultdict, deque
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from functools import lru_cache

input = sys.stdin.readline
MOD = 10**9 + 7

def solve():
  n = int(input())
  arr = list(map(int, input().split()))
  # Your solution here
  print(result)

if __name__ == "__main__":
  t = int(input())  # For multiple test cases
  for _ in range(t):
    solve()
```
