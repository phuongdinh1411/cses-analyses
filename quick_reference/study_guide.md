---
layout: simple
title: "Study Guide"
permalink: /quick_reference/study_guide
---

# DSA Study Guide

A comprehensive guide covering learning paths, pattern recognition, and interview preparation.

## Learning Path

```
Phase 1: Foundations (Weeks 1-4)
    Arrays, Strings, Math, Bit Manipulation

Phase 2: Core Patterns (Weeks 5-12)
    Binary Search, Two Pointers, Sliding Window, Hash Maps, Stacks

Phase 3: Intermediate (Weeks 13-24)
    Dynamic Programming, Graph Algorithms, Tree Algorithms

Phase 4: Advanced (Weeks 25-36)
    Segment Trees, String Algorithms, Geometry, Number Theory
```

### Phase 1: Foundations

| Week | Topics | Key Problems |
|------|--------|--------------|
| 1-2 | Arrays, Prefix Sums | Two Sum, Running Sum, Subarray Sum |
| 3-4 | Math, Bit Manipulation | GCD, Modular Arithmetic, Single Number |

### Phase 2: Core Patterns

| Week | Topics | Key Problems |
|------|--------|--------------|
| 5-6 | Binary Search | Find Element, Binary Search on Answer |
| 7-8 | Two Pointers | Two Sum Sorted, 3Sum, Container With Water |
| 9-10 | Sliding Window | Max Sum Subarray, Longest Substring |
| 11-12 | Hash Maps, Stacks | Frequency Count, Next Greater Element |

### Phase 3: Intermediate

| Week | Topics | Key Problems |
|------|--------|--------------|
| 13-16 | Dynamic Programming | Coin Change, LCS, Knapsack, Grid Paths |
| 17-20 | Graph Algorithms | BFS, DFS, Dijkstra, Topological Sort |
| 21-24 | Tree Algorithms | Tree DP, LCA, Path Queries |

### Phase 4: Advanced

| Week | Topics | Key Problems |
|------|--------|--------------|
| 25-28 | Range Queries | Segment Tree, Fenwick Tree |
| 29-32 | String Algorithms | KMP, Z-Algorithm, Suffix Array |
| 33-36 | Geometry, Advanced Graph | Convex Hull, Max Flow |

---

## Pattern Recognition

### By Input Type

| Input | Think | Algorithm |
|-------|-------|-----------|
| Sorted array | Binary search | `bisect_left/right` |
| Unsorted array + pairs | Hash map | `dict/set` |
| Subarray/substring | Sliding window | Two pointers |
| Next greater/smaller | Monotonic stack | Stack |
| Shortest path (unweighted) | BFS | `deque` |
| Shortest path (weighted) | Dijkstra | `heapq` |
| All pairs shortest | Floyd-Warshall | 3 nested loops |
| Connected components | DFS/Union-Find | `find/union` |
| Count ways/optimize | DP | `dp[i] = ...` |
| Dependencies/ordering | Topological Sort | Kahn's algorithm |

### By Keywords

| Keyword | Algorithm | Confidence |
|---------|-----------|------------|
| "shortest path" | BFS/Dijkstra | Very High |
| "connected" | DFS/Union-Find | Very High |
| "next greater element" | Monotonic Stack | Very High |
| "longest increasing" | DP + Binary Search | Very High |
| "minimum spanning tree" | Kruskal/Prim | Very High |
| "topological order" | Kahn's/DFS | Very High |
| "subarray" | Sliding Window/Prefix Sum | High |
| "palindrome" | Two Pointers/DP | High |
| "intervals" | Sort + Greedy | High |
| "count ways" | DP | High |

### By Constraints

| Constraint | Max Complexity | Suitable Algorithms |
|------------|----------------|---------------------|
| n <= 10 | O(n!) | Brute force, permutations |
| n <= 20 | O(2^n) | Bitmask DP, backtracking |
| n <= 500 | O(n^3) | Floyd-Warshall, interval DP |
| n <= 5000 | O(n^2) | Simple DP, nested loops |
| n <= 10^5 | O(n log n) | Sorting, segment tree |
| n <= 10^6 | O(n) | Linear scan, two pointers |
| n <= 10^9 | O(log n) | Binary search, math formula |

---

## Top 15 Interview Patterns

### 1. Two Pointers
**When**: Sorted arrays, finding pairs, palindromes

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target: return [left, right]
        elif s < target: left += 1
        else: right -= 1
    return [-1, -1]
```

### 2. Sliding Window
**When**: Subarray/substring with constraints

```python
def longest_unique_substring(s):
    seen = {}
    left = max_len = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

### 3. Binary Search
**When**: Sorted data, finding boundaries, optimization

```python
def binary_search_answer(lo, hi, is_feasible):
    while lo < hi:
        mid = (lo + hi) // 2
        if is_feasible(mid): hi = mid
        else: lo = mid + 1
    return lo
```

### 4. BFS/DFS
**When**: Graph traversal, shortest path, connected components

```python
def bfs(graph, start, target):
    from collections import deque
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        if node == target: return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1
```

### 5. Dynamic Programming
**When**: Optimization, counting, overlapping subproblems

```python
# Coin Change
def min_coins(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

### 6. Backtracking
**When**: Generate all combinations, permutations

```python
def backtrack(path, choices, results):
    if is_solution(path):
        results.append(path.copy())
        return
    for choice in choices:
        if is_valid(choice):
            path.append(choice)
            backtrack(path, remaining_choices, results)
            path.pop()
```

### 7. Heap / Priority Queue
**When**: K-th largest/smallest, merge sorted lists

```python
import heapq
# K-th largest: min-heap of size k
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]
```

### 8. Union-Find
**When**: Connected components, cycle detection

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
```

### 9. Monotonic Stack
**When**: Next greater/smaller element

```python
def next_greater(arr):
    result = [-1] * len(arr)
    stack = []
    for i, num in enumerate(arr):
        while stack and arr[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(i)
    return result
```

### 10. Trie
**When**: Prefix matching, autocomplete

### 11. Intervals
**When**: Scheduling, merging, overlapping
- Sort by start or end time
- Greedy for maximum non-overlapping

### 12. Tree Traversal
**When**: Tree problems, path finding
- Preorder, Inorder, Postorder
- Binary Lifting for LCA

### 13. Topological Sort
**When**: Dependencies, ordering constraints

```python
from collections import deque
def topo_sort(n, edges):
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
    return result if len(result) == n else []
```

### 14. Bit Manipulation
**When**: Subsets, XOR properties

```python
x & (x - 1)    # Remove lowest set bit
x & (-x)       # Get lowest set bit
x | (1 << i)   # Set i-th bit
x & ~(1 << i)  # Clear i-th bit
(x >> i) & 1   # Get i-th bit
```

### 15. Math & Combinatorics
**When**: Counting, probability, number theory

```python
MOD = 10**9 + 7

def mod_pow(base, exp, mod=MOD):
    result = 1
    while exp > 0:
        if exp & 1: result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

def mod_inv(a, mod=MOD):
    return mod_pow(a, mod - 2, mod)
```

---

## Algorithm Reference

### Graph Algorithms

| Problem | Algorithm | Time | Space |
|---------|-----------|------|-------|
| Shortest (unweighted) | BFS | O(V+E) | O(V) |
| Shortest (weighted) | Dijkstra | O((V+E)logV) | O(V) |
| Shortest (negative) | Bellman-Ford | O(VE) | O(V) |
| All pairs | Floyd-Warshall | O(V^3) | O(V^2) |
| MST | Kruskal/Prim | O(ElogE) | O(V) |
| SCC | Kosaraju/Tarjan | O(V+E) | O(V) |

### Dynamic Programming

| Pattern | Time | Space | Key |
|---------|------|-------|-----|
| Fibonacci | O(n) | O(1) | `dp[i] = dp[i-1] + dp[i-2]` |
| Coin Change | O(n*amount) | O(amount) | `dp[i] = min(dp[i], dp[i-coin]+1)` |
| LCS | O(m*n) | O(m*n) | `dp[i][j] = dp[i-1][j-1]+1 or max(...)` |
| LIS | O(nlogn) | O(n) | Binary search on tails |
| Knapsack | O(n*W) | O(W) | `dp[w] = max(dp[w], dp[w-wt]+val)` |
| Grid Paths | O(m*n) | O(n) | `dp[j] += dp[j-1]` |

### Data Structures

| Structure | Insert | Delete | Search | Use Case |
|-----------|--------|--------|--------|----------|
| Array | O(n) | O(n) | O(n) | Sequential access |
| Hash Map | O(1) | O(1) | O(1) | Key-value lookup |
| Heap | O(logn) | O(logn) | O(n) | Priority queue |
| BST | O(logn) | O(logn) | O(logn) | Sorted data |
| Segment Tree | O(logn) | O(logn) | O(logn) | Range queries |
| Trie | O(m) | O(m) | O(m) | Prefix matching |

---

## Interview Framework

### Step 1: Understand (3-5 min)
- Repeat problem in your own words
- Ask clarifying questions
- Note constraints

### Step 2: Examples (2-3 min)
- Walk through given examples
- Create edge case examples

### Step 3: Approach (5-10 min)
- Start with brute force
- Identify pattern
- Propose optimized solution
- Discuss complexity

### Step 4: Code (15-20 min)
- Write clean, readable code
- Handle edge cases

### Step 5: Test (5 min)
- Trace through examples
- Test edge cases

---

## Daily Practice

### Weekday (1-2 hours)
- 30 min: Review concepts
- 45 min: 1-2 new problems
- 15 min: Study solutions

### Weekend (3-4 hours)
- 1 hour: Timed practice
- 1 hour: Learn new technique
- 1 hour: Medium/hard problems
- 1 hour: Review notes

### Progress Checkpoints

**Beginner**: Solve array/string problems in O(n), understand Big-O

**Intermediate**: Identify DP problems, implement BFS/DFS, binary search on answer

**Advanced**: Segment tree with lazy propagation, multiple graph algorithms, string algorithms
