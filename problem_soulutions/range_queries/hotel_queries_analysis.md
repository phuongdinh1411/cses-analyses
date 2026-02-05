---
layout: simple
title: "Hotel Queries - Segment Tree with Max"
permalink: /problem_soulutions/range_queries/hotel_queries_analysis
difficulty: Medium
tags: [segment-tree, range-queries, binary-search, point-update]
---

# Hotel Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES 1143 - Hotel Queries](https://cses.fi/problemset/task/1143) |
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Segment Tree with Maximum + Descend Search |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Implement a segment tree that tracks maximum values
- [ ] Use segment tree structure to find the first position satisfying a condition
- [ ] Combine point updates with efficient search operations
- [ ] Apply "descend" technique to search within a segment tree

---

## Problem Statement

**Problem:** There are n hotels with specified room capacities. For each of m groups of tourists, find the first hotel (leftmost) that has enough rooms to accommodate the entire group, book those rooms, and report the hotel number (or 0 if no hotel can accommodate them).

**Input:**
- Line 1: Two integers n and m (number of hotels, number of groups)
- Line 2: n integers h_1, h_2, ..., h_n (room count in each hotel)
- Next m lines: One integer r_i (size of each group)

**Output:**
- For each group, print the hotel number (1-indexed) where they are assigned, or 0 if impossible

**Constraints:**
- 1 <= n, m <= 2 * 10^5
- 1 <= h_i <= 10^9
- 1 <= r_i <= 10^9

### Example

```
Input:
8 5
3 2 4 1 5 5 2 6
4 4 7 1 1

Output:
3 5 0 1 1
```

**Explanation:**
- Group 1 (size 4): Hotels have [3,2,4,1,5,5,2,6]. First hotel with >= 4 rooms is hotel 3 (4 rooms). Book it: [3,2,0,1,5,5,2,6]. Output: 3
- Group 2 (size 4): First hotel with >= 4 rooms is hotel 5 (5 rooms). Book it: [3,2,0,1,1,5,2,6]. Output: 5
- Group 3 (size 7): No hotel has >= 7 rooms. Output: 0
- Group 4 (size 1): First hotel with >= 1 room is hotel 1 (3 rooms). Book it: [2,2,0,1,1,5,2,6]. Output: 1
- Group 5 (size 1): First hotel with >= 1 room is hotel 1 (2 rooms). Book it: [1,2,0,1,1,5,2,6]. Output: 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** We need to repeatedly find the "first position with value >= X" and then update that position. What data structure supports both operations efficiently?

This is a classic application of segment trees. A segment tree with maximum allows us to:
1. Check if any hotel in a range has enough rooms (compare range max with required rooms)
2. Navigate down the tree to find the leftmost such hotel
3. Update a single hotel's room count after booking

### Breaking Down the Problem

1. **What are we looking for?** The leftmost hotel with rooms >= group size
2. **What information do we have?** Current room counts for all hotels
3. **What's the relationship between input and output?** For each query, find first valid position, update it, return the position

### Why a Segment Tree?

Think of the segment tree as a tournament bracket where each node stores the maximum of its children. To find the leftmost hotel with enough rooms:
- If the root's max is less than needed, no hotel works (return 0)
- Otherwise, always try the left subtree first (to get leftmost)
- Only go right if left subtree's max is insufficient

---

## Solution 1: Brute Force

### Idea

For each group, linearly scan hotels from left to right to find the first one with enough rooms.

### Algorithm

1. For each group of size r:
2. Iterate through hotels 1 to n
3. If hotel i has >= r rooms, book it (subtract r), output i, move to next group
4. If no hotel found, output 0

### Code

```python
def solve_brute_force(n, m, hotels, groups):
  """
  Brute force: linear scan for each query.

  Time: O(m * n)
  Space: O(1) extra
  """
  results = []

  for group_size in groups:
    found = 0
    for i in range(n):
      if hotels[i] >= group_size:
        hotels[i] -= group_size
        found = i + 1  # 1-indexed
        break
    results.append(found)

  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(m * n) | Each of m queries scans up to n hotels |
| Space | O(1) | Only using input array |

### Why This Works (But Is Slow)

The correctness is obvious: we check every hotel in order. However, with n, m up to 2*10^5, this gives 4*10^10 operations - far too slow.

---

## Solution 2: Optimal Solution with Segment Tree

### Key Insight

> **The Trick:** Build a segment tree storing maximum room count in each range. To find the leftmost hotel with enough rooms, descend from root, always preferring the left child.

### Segment Tree Node Meaning

| Node | Meaning |
|------|---------|
| `tree[v]` | Maximum room count among all hotels in the range covered by node v |

**In plain English:** Each node tells us "the best hotel in my range has this many rooms available."

### Operations Needed

1. **Query + Update Combined:** Find leftmost position with value >= X, then subtract X from that position
2. This is done in a single tree descent - no separate query and update phases

### Algorithm

1. Build segment tree where each node stores max of its range
2. For each group of size r:
   - If root's max < r: output 0 (no hotel works)
   - Otherwise, descend the tree:
     - At each internal node, go left if left child's max >= r, else go right
     - At leaf, update value (subtract r) and propagate max changes up
   - Output the found position

### Dry Run Example

Let's trace with `hotels = [3, 2, 4, 1, 5, 5, 2, 6]` and first query `r = 4`:

```
Initial segment tree (showing max values):
                    [6]                    <- root: max of all = 6
                /         \
             [4]           [6]             <- max of [0-3] = 4, max of [4-7] = 6
            /   \         /    \
          [3]   [4]     [5]    [6]         <- max of pairs
         /  \   /  \   /  \   /  \
        3    2  4   1  5   5  2   6        <- leaf values (hotels)
        ^    ^  ^   ^  ^   ^  ^   ^
       h1   h2 h3  h4 h5  h6 h7  h8

Query: Find leftmost hotel with >= 4 rooms

Step 1: At root [6], max=6 >= 4, so solution exists
Step 2: Check left child [4], max=4 >= 4, go LEFT
Step 3: Check left child of [4], which is [3], max=3 < 4, go RIGHT
Step 4: At node [4] (covering h3-h4), left child is leaf h3=4 >= 4, go LEFT
Step 5: Reached leaf h3 (index 2, 1-indexed = 3)

Update: h3 = 4 - 4 = 0

After update, tree becomes:
                    [6]
                /         \
             [3]           [6]             <- updated from 4 to 3
            /   \         /    \
          [3]   [1]     [5]    [6]         <- updated from 4 to 1
         /  \   /  \
        3    2  0   1                      <- h3 updated to 0

Output: 3
```

### Visual Diagram

```
Segment Tree Structure (array-based, 1-indexed internal):

For n=8 hotels, tree size = 2*8 = 16

         Index:    1
                /     \
              2         3
            /   \     /   \
           4     5   6     7
          /\    /\   /\    /\
         8  9 10 11 12 13 14 15   <- leaves store hotel rooms

Leaf index i corresponds to hotel (i - n + 1) in 1-indexed terms
Or: leaf at tree[n + i] stores hotel[i] (0-indexed)
```

### Code

**Python Solution:**

```python
import sys
from typing import List

def solve():
  input_data = sys.stdin.read().split()
  idx = 0

  n = int(input_data[idx]); idx += 1
  m = int(input_data[idx]); idx += 1

  hotels = [int(input_data[idx + i]) for i in range(n)]
  idx += n

  groups = [int(input_data[idx + i]) for i in range(m)]

  # Build segment tree (1-indexed, size 2*n)
  # tree[i] for i >= n are leaves (hotels)
  # tree[i] for i < n are internal nodes (max of children)
  tree = [0] * (2 * n)

  # Initialize leaves
  for i in range(n):
    tree[n + i] = hotels[i]

  # Build internal nodes (bottom-up)
  for i in range(n - 1, 0, -1):
    tree[i] = max(tree[2 * i], tree[2 * i + 1])

  results = []

  for group_size in groups:
    # Check if any hotel can accommodate
    if tree[1] < group_size:
      results.append(0)
      continue

    # Descend to find leftmost hotel with enough rooms
    v = 1
    while v < n:
      if tree[2 * v] >= group_size:
        v = 2 * v      # go left
      else:
        v = 2 * v + 1  # go right

    # v is now a leaf, hotel index = v - n (0-indexed), output v - n + 1 (1-indexed)
    hotel_idx = v - n
    results.append(hotel_idx + 1)

    # Update: subtract group_size from this hotel
    tree[v] -= group_size

    # Propagate update upward
    v //= 2
    while v >= 1:
      tree[v] = max(tree[2 * v], tree[2 * v + 1])
      v //= 2

  print(' '.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + m) * log n) | Build tree O(n), each query O(log n) |
| Space | O(n) | Segment tree of size 2n |

---

## Common Mistakes

### Mistake 1: Using Binary Search Instead of Tree Descent

```python
# WRONG APPROACH
def find_hotel_binary_search(tree, n, required):
  lo, hi = 0, n - 1
  while lo < hi:
    mid = (lo + hi) // 2
    # This doesn't work! Can't query "max in [0, mid]" efficiently
    # without understanding segment tree structure
```

**Problem:** Standard binary search doesn't leverage segment tree structure efficiently.
**Fix:** Use the descent approach - check left child first, go right only if necessary.

### Mistake 2: Forgetting to Propagate Updates

```python
# WRONG
tree[v] -= group_size  # Update leaf
# Missing: propagate change to ancestors!

# CORRECT
tree[v] -= group_size
v //= 2
while v >= 1:
  tree[v] = max(tree[2 * v], tree[2 * v + 1])
  v //= 2
```

**Problem:** Parent nodes still have stale max values.
**Fix:** Always update ancestors after modifying a leaf.

### Mistake 3: Off-by-One Indexing

```python
# WRONG - mixing 0-indexed and 1-indexed
hotel_number = v - n  # This is 0-indexed!

# CORRECT
hotel_number = v - n + 1  # Convert to 1-indexed for output
```

### Mistake 4: Wrong Tree Size for Non-Power-of-2

```python
# Potential issue: if n is not power of 2
# The simple 2*n approach works, but be careful with indexing

# Safe approach: pad to next power of 2, or use this exact method
# which works for any n
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No room available | `n=2, hotels=[1,1], group=5` | 0 | Max room count < required |
| All groups same hotel | `n=3, hotels=[10,1,1], groups=[1,1,1]` | 1 1 1 | First hotel keeps having enough |
| Single hotel | `n=1, hotels=[5], groups=[3,3]` | 1 0 | Second group can't fit |
| Large values | `hotels=[10^9], group=10^9` | 1 | Handle large numbers |
| Exact fit | `hotels=[4,3], group=4` | 1 | Exact match works |

---

## When to Use This Pattern

### Use This Approach When:
- You need to find the **first/leftmost position** satisfying a condition
- The condition can be checked using **range aggregates** (max, min, sum, etc.)
- You need **point updates** after finding the position
- Multiple queries require efficient repeated searches

### Don't Use When:
- Simple linear scan is fast enough (small n, m)
- You need range updates (consider lazy propagation)
- The "first position" logic doesn't fit segment tree descent

### Pattern Recognition Checklist:
- [ ] Need to find first position with value >= X? **Segment tree with max + descent**
- [ ] Need to find first position with prefix sum >= X? **Segment tree with sum + descent**
- [ ] Need range max/min queries without position finding? **Standard segment tree query**
- [ ] Need to support range updates too? **Segment tree with lazy propagation**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Minimum Queries (CSES 1647)](https://cses.fi/problemset/task/1647) | Basic segment tree / sparse table for range min |
| [Dynamic Range Sum Queries (CSES 1648)](https://cses.fi/problemset/task/1648) | Segment tree with point updates |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Dynamic Range Minimum Queries (CSES 1649)](https://cses.fi/problemset/task/1649) | Range min instead of max, no descent needed |
| [Range Update Queries (CSES 1651)](https://cses.fi/problemset/task/1651) | Range updates instead of point updates |
| [List Removals (CSES 1749)](https://cses.fi/problemset/task/1749) | Similar descent technique to find k-th element |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Polynomial Queries (CSES 1736)](https://cses.fi/problemset/task/1736) | Lazy propagation with arithmetic sequences |
| [Range Queries and Copies (CSES 1737)](https://cses.fi/problemset/task/1737) | Persistent segment tree |

---

## Key Takeaways

1. **The Core Idea:** Use segment tree maximum to quickly check if a valid position exists, then descend preferring left to find the leftmost one.
2. **Time Optimization:** From O(n) per query to O(log n) by using tree structure for both searching and updating.
3. **Space Trade-off:** O(n) extra space for the segment tree enables logarithmic operations.
4. **Pattern:** "Find first position with condition" problems often use segment tree descent.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a segment tree with max in O(n) time
- [ ] Implement the descent to find leftmost position with value >= X
- [ ] Correctly update a leaf and propagate changes upward
- [ ] Handle the "no valid position" case
- [ ] Implement in under 15 minutes without reference

---

## Additional Resources

- [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)
- [CSES Problem Set - Range Queries](https://cses.fi/problemset/list/)
- [Codeforces EDU: Segment Tree (Part 2)](https://codeforces.com/edu/course/2/lesson/4)
