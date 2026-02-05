---
layout: simple
title: "Road Construction - Online Connectivity with Union-Find"
permalink: /problem_soulutions/graph_algorithms/road_construction_analysis
difficulty: Easy
tags: [graph, union-find, dsu, online-connectivity]
cses_link: https://cses.fi/problemset/task/1676
---

# Road Construction - Online Connectivity with Union-Find

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Track components as roads are added |
| Pattern | Union-Find with size tracking |
| Difficulty | Easy |
| Key Operations | Union, Find, Track component count & max size |
| Time Complexity | O(m * alpha(n)) approximately O(m) |

## Learning Goals

1. **Union-Find with Size Tracking**: Maintain component sizes during union operations
2. **Online Queries**: Answer queries after each modification (no preprocessing all edges)
3. **Path Compression + Union by Size**: Achieve near-constant time per operation

## Problem Statement

There are `n` cities and initially no roads. You are given `m` roads to be constructed one by one. After adding each road, output:
- Number of connected components
- Size of the largest component

**Input:**
- Line 1: `n m` (cities and roads)
- Next m lines: `a b` (road connects cities a and b)

**Output:** m lines, each with two integers: component count and largest component size.

**Constraints:** 1 <= n, m <= 10^5

**Example:**
```
Input:
5 3
1 2
1 3
4 5

Output:
4 2
3 3
2 3
```

## Key Insight

Use Union-Find (Disjoint Set Union) with:
1. **Path compression** in `find()` - flattens tree structure
2. **Union by size** - attach smaller tree under larger tree
3. **Track two values globally:**
   - `num_components`: starts at n, decreases by 1 on each successful union
   - `max_size`: update when a union creates a larger component

## Algorithm Design

### What We Track

```
Global State:
- parent[i]: parent of node i (initially parent[i] = i)
- size[i]: size of component rooted at i (initially all 1)
- num_components: number of distinct components (initially n)
- max_size: size of largest component (initially 1)
```

### Union-Find Operations

```
find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression
    return parent[x]

union(x, y):
    root_x = find(x)
    root_y = find(y)

    if root_x == root_y:
        return  # Already connected, no change

    # Union by size: smaller under larger
    if size[root_x] < size[root_y]:
        swap(root_x, root_y)

    parent[root_y] = root_x
    size[root_x] += size[root_y]

    num_components -= 1
    max_size = max(max_size, size[root_x])
```

## Visual Diagram

```
Initial: 5 cities, 0 roads
Components: {1}, {2}, {3}, {4}, {5}
num_components = 5, max_size = 1

   1    2    3    4    5
   o    o    o    o    o

After road 1-2:
Components: {1,2}, {3}, {4}, {5}
num_components = 4, max_size = 2

   1         3    4    5
   |
   2

After road 1-3:
Components: {1,2,3}, {4}, {5}
num_components = 3, max_size = 3

     1       4    5
    / \
   2   3

After road 4-5:
Components: {1,2,3}, {4,5}
num_components = 2, max_size = 3

     1         4
    / \        |
   2   3       5
```

## Dry Run

```
n=5, m=3, roads: [(1,2), (1,3), (4,5)]

Initial State:
  parent = [_, 1, 2, 3, 4, 5]  (1-indexed)
  size   = [_, 1, 1, 1, 1, 1]
  num_components = 5
  max_size = 1

Road 1: (1, 2)
  find(1) = 1, find(2) = 2
  Different roots -> union them
  size[1]=1, size[2]=1 -> attach 2 under 1
  parent[2] = 1, size[1] = 2
  num_components = 4, max_size = 2
  Output: 4 2

Road 2: (1, 3)
  find(1) = 1, find(3) = 3
  Different roots -> union them
  size[1]=2 > size[3]=1 -> attach 3 under 1
  parent[3] = 1, size[1] = 3
  num_components = 3, max_size = 3
  Output: 3 3

Road 3: (4, 5)
  find(4) = 4, find(5) = 5
  Different roots -> union them
  size[4]=1, size[5]=1 -> attach 5 under 4
  parent[5] = 4, size[4] = 2
  num_components = 2, max_size = max(3, 2) = 3
  Output: 2 3
```

## Python Solution

```python
import sys
from sys import stdin

def main():
    input = stdin.readline
    n, m = map(int, input().split())

    parent = list(range(n + 1))  # 1-indexed
    size = [1] * (n + 1)
    num_components = n
    max_size = 1

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    results = []
    for _ in range(m):
        a, b = map(int, input().split())

        root_a = find(a)
        root_b = find(b)

        if root_a != root_b:
            # Union by size
            if size[root_a] < size[root_b]:
                root_a, root_b = root_b, root_a

            parent[root_b] = root_a
            size[root_a] += size[root_b]

            num_components -= 1
            max_size = max(max_size, size[root_a])

        results.append(f"{num_components} {max_size}")

    print('\n'.join(results))

if __name__ == "__main__":
    main()
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Not updating max_size on union | Reports stale maximum | Update `max_size = max(max_size, size[root])` after every union |
| Off-by-one in component count | Wrong initial count | Start with `num_components = n`, decrement on successful union only |
| Forgetting path compression | TLE on large inputs | Always update `parent[x] = find(parent[x])` in find |
| Union without size check | Unbalanced trees | Always attach smaller tree under larger |
| Updating count when already connected | Double counting | Check `root_a != root_b` before decrementing |

## Complexity Analysis

| Operation | Time | Notes |
|-----------|------|-------|
| find(x) | O(alpha(n)) | With path compression, alpha is inverse Ackermann |
| union(x,y) | O(alpha(n)) | Dominated by two find operations |
| Total | O(m * alpha(n)) | For m operations, effectively O(m) |

**Space Complexity:** O(n) for parent and size arrays

**Why alpha(n) is effectively constant:** The inverse Ackermann function grows extremely slowly. For any practical input size (even n = 10^80), alpha(n) <= 4.

## Related Problems

- [CSES Building Roads](https://cses.fi/problemset/task/1666) - Make graph connected
- [LeetCode 547: Number of Provinces](https://leetcode.com/problems/number-of-provinces/)
- [LeetCode 684: Redundant Connection](https://leetcode.com/problems/redundant-connection/)
