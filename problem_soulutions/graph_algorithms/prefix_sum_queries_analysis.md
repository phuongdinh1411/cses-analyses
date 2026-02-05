---
title: "Prefix Sum Queries - Range Sum with Updates"
cses_link: https://cses.fi/problemset/task/2166
category: Range Queries
difficulty: Medium
---

# Prefix Sum Queries - Range Sum with Updates

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Support point updates and prefix maximum queries |
| Operations | Update: set arr[k] = u; Query: max prefix sum ending at or before position k |
| Input | n elements, q queries |
| Constraints | 1 <= n, q <= 2*10^5 |
| Key Technique | Segment Tree with prefix sum tracking |

## Problem Description

Given an array, support two operations:
1. **Update(k, u):** Set arr[k] = u
2. **Query(k):** Find the maximum prefix sum among all prefixes ending at positions 1 to k

**Example:**
```
Initial array: [1, -2, 3, -1, 2]

Prefix sums: [1, -1, 2, 1, 3]
            pos 1: 1
            pos 2: 1 + (-2) = -1
            pos 3: 1 + (-2) + 3 = 2
            pos 4: 1 + (-2) + 3 + (-1) = 1
            pos 5: 1 + (-2) + 3 + (-1) + 2 = 3

Query(3): max(1, -1, 2) = 2
Query(5): max(1, -1, 2, 1, 3) = 3

Update(2, 5): array becomes [1, 5, 3, -1, 2]
New prefix sums: [1, 6, 9, 8, 10]

Query(3): max(1, 6, 9) = 9
```

## Algorithm: Segment Tree for Prefix Maximum

**Key Insight:** We need to track both:
1. The sum of each segment
2. The maximum prefix sum within each segment

**For each segment, store:**
- `sum`: total sum of the segment
- `prefix_max`: maximum prefix sum within the segment

**Merge operation:**
```
For segments A (left) and B (right):
- merged.sum = A.sum + B.sum
- merged.prefix_max = max(A.prefix_max, A.sum + B.prefix_max)
```

The second formula says: the best prefix in the merged segment is either:
- Entirely within A (A.prefix_max)
- Spans all of A plus some prefix of B (A.sum + B.prefix_max)

## Implementation

### Python Solution
```python
import sys
from sys import stdin

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        # Each node stores (sum, prefix_max)
        self.tree = [(0, float('-inf'))] * (4 * self.n)
        self.build(arr, 1, 0, self.n - 1)

    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = (arr[start], arr[start])
        else:
            mid = (start + end) // 2
            self.build(arr, 2 * node, start, mid)
            self.build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.merge(self.tree[2 * node],
                                          self.tree[2 * node + 1])

    def merge(self, left, right):
        """Merge two segments."""
        sum_val = left[0] + right[0]
        prefix_max = max(left[1], left[0] + right[1])
        return (sum_val, prefix_max)

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = (val, val)
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node, start, mid, idx, val)
            else:
                self.update(2 * node + 1, mid + 1, end, idx, val)
            self.tree[node] = self.merge(self.tree[2 * node],
                                          self.tree[2 * node + 1])

    def query(self, node, start, end, l, r):
        """Query max prefix sum in range [l, r]."""
        if r < start or end < l:
            return (0, float('-inf'))  # Identity element
        if l <= start and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        left = self.query(2 * node, start, mid, l, r)
        right = self.query(2 * node + 1, mid + 1, end, l, r)
        return self.merge(left, right)

    def point_update(self, idx, val):
        self.update(1, 0, self.n - 1, idx, val)

    def prefix_max_query(self, k):
        """Max prefix sum among positions 0 to k."""
        result = self.query(1, 0, self.n - 1, 0, k)
        return result[1]


def solve():
    input = stdin.readline
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    st = SegmentTree(arr)
    result = []

    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 1:
            # Update: 1 k u (1-indexed)
            k, u = query[1] - 1, query[2]
            st.point_update(k, u)
        else:
            # Query: 2 k (1-indexed)
            k = query[1] - 1
            result.append(st.prefix_max_query(k))

    print('\n'.join(map(str, result)))

solve()
```

### Visual Walkthrough

```
Array: [1, -2, 3, -1, 2]

Segment Tree (each node stores sum, prefix_max):

                    [3, 3]          <- root: sum=3, best prefix ending anywhere = 3
                   /      \
            [-1, 1]        [4, 4]
            /     \        /    \
        [1,1] [-2,-2]  [3,3]  [1, 2]
                              /    \
                         [-1,-1] [2,2]

Query(2) = max prefix among positions 0,1,2:
- Need [1,1], [-2,-2], [3,3]
- merge([1,1], [-2,-2]) = [1-2=-1, max(1, 1+(-2))=1]
- merge([-1,1], [3,3]) = [-1+3=2, max(1, -1+3)=2]
- Answer: 2

Update(1, 5): arr[1] = 5
- Update leaf for position 1
- Propagate up, recomputing merges
- New tree reflects [1, 5, 3, -1, 2]
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n) | O(n) |
| Point Update | O(log n) | - |
| Prefix Max Query | O(log n) | - |
| **Total for q queries** | **O(n + q log n)** | **O(n)** |

## Common Mistakes

1. **Wrong merge formula:** prefix_max must be max(left.prefix_max, left.sum + right.prefix_max)
2. **Integer overflow:** Use `long long` for sums
3. **Identity element:** For out-of-range queries, return (0, -INF) not (0, 0)
4. **1-indexed vs 0-indexed:** Be consistent throughout
5. **Forgetting to propagate:** After update, must recompute all ancestors

## Variations

| Variation | Modification |
|-----------|--------------|
| Suffix max query | Store (sum, suffix_max), adjust merge |
| Maximum subarray | Store (sum, prefix_max, suffix_max, max_subarray) |
| Range update | Add lazy propagation |

## Key Takeaways

- Segment trees can store custom aggregate information
- The merge function must be associative
- Prefix max requires tracking both sum and prefix_max per segment
- Pattern: what info do I need to combine two segments?
- This technique generalizes to many "prefix/suffix queries with updates"
