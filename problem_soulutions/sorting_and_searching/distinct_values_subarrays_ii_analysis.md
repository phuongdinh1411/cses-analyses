---
layout: simple
title: "Distinct Values Queries II - Range Queries Problem"
permalink: /problem_soulutions/sorting_and_searching/distinct_values_subarrays_ii_analysis
difficulty: Hard
tags: [segment-tree, range-queries, coordinate-compression, sqrt-decomposition]
---

# Distinct Values Queries II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Distinct Values Queries II](https://cses.fi/problemset/task/3356) |
| **Difficulty** | Hard |
| **Category** | Range Queries |
| **Time Limit** | 1.00 s |
| **Key Technique** | Segment Tree / Sqrt Decomposition |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply segment trees for range distinctness queries with updates
- [ ] Use coordinate compression to handle large value ranges
- [ ] Implement efficient data structures for "all distinct in range" queries
- [ ] Optimize between segment tree and sqrt decomposition based on constraints

---

## Problem Statement

**Problem:** Given an array of n integers, process q queries of two types:
1. **Update:** Change the value at position k to u
2. **Query:** Check if every value in range [a, b] is distinct (no duplicates)

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers x1, x2, ..., xn (array values)
- Next q lines: Either "1 k u" (update) or "2 a b" (query)

**Output:**
- For each type-2 query: Print "YES" if all values in range [a, b] are distinct, "NO" otherwise

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= xi, u <= 10^9
- 1 <= k <= n
- 1 <= a <= b <= n

### Example

```
Input:
5 4
3 2 7 2 8
2 3 5
2 2 5
1 2 9
2 2 5

Output:
YES
NO
YES
```

**Explanation:**
- Initial array: [3, 2, 7, 2, 8]
- Query 1: Range [3,5] = [7, 2, 8] - all distinct -> YES
- Query 2: Range [2,5] = [2, 7, 2, 8] - value 2 appears twice -> NO
- Update: Change position 2 to 9, array becomes [3, 9, 7, 2, 8]
- Query 3: Range [2,5] = [9, 7, 2, 8] - all distinct -> YES

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently check if a range contains duplicates, while supporting point updates?

The key insight is that instead of checking if all values are distinct (which requires O(range) time naively), we can track for each position i the **previous occurrence** of the same value. If prev[i] >= a (start of query range), then there is a duplicate.

### Breaking Down the Problem

1. **What are we looking for?** Whether any value appears more than once in range [a, b]
2. **What information do we have?** Array values, with point updates
3. **What's the relationship between input and output?** A range has all distinct values if and only if for every position i in [a, b], the previous occurrence of arr[i] is before position a.

### Core Insight

For each position i, define `prev[i]` = the largest index j < i where arr[j] = arr[i], or 0 if no such j exists.

A range [a, b] has all distinct values if and only if:
**max(prev[a], prev[a+1], ..., prev[b]) < a**

This transforms the problem into: **range maximum query with point updates**.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and use a set to check for duplicates.

### Algorithm

1. For update query: Simply update arr[k] = u
2. For distinctness query: Use a set to track seen values in range [a, b]

### Code

```python
def solve_brute_force():
 """
 Brute force solution - check each range with a set.

 Time: O(q * n) per query
 Space: O(n)
 """
 import sys
 input = sys.stdin.readline

 n, q = map(int, input().split())
 arr = [0] + list(map(int, input().split()))  # 1-indexed

 results = []
 for _ in range(q):
  query = list(map(int, input().split()))

  if query[0] == 1:  # Update
   k, u = query[1], query[2]
   arr[k] = u
  else:  # Query
   a, b = query[1], query[2]
   seen = set()
   is_distinct = True
   for i in range(a, b + 1):
    if arr[i] in seen:
     is_distinct = False
     break
    seen.add(arr[i])
   results.append("YES" if is_distinct else "NO")

 print('\n'.join(results))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query may scan entire range |
| Space | O(n) | Set for checking duplicates |

### Why This Works (But Is Slow)

Correctness is guaranteed since we explicitly check each value in the range. However, with n, q up to 2 x 10^5, worst case is 4 x 10^10 operations - far too slow.

---

## Solution 2: Optimal Solution - Segment Tree with prev[] Array

### Key Insight

> **The Trick:** Transform "all distinct" into "range max of prev[] < a" and use segment tree for efficient range max queries with point updates.

### Data Structure Design

| Component | Purpose |
|-----------|---------|
| `arr[i]` | Current value at position i |
| `prev[i]` | Previous occurrence index of arr[i], or 0 |
| `pos[v]` | Current positions where value v appears (sorted set) |
| Segment Tree | Range maximum query on prev[] array |

**In plain English:** We maintain for each position where the same value last appeared. A range has duplicates iff any position in that range has its previous occurrence within the range.

### Algorithm

1. **Preprocessing:**
   - Build `pos[v]` = sorted set of positions containing value v
   - Compute `prev[i]` = predecessor of i in pos[arr[i]]
   - Build segment tree on prev[] for range max

2. **Update (position k to value u):**
   - Remove k from pos[arr[k]], update prev[] for k's successor
   - Add k to pos[u], update prev[k] and prev[] for k's successor
   - Update segment tree at affected positions

3. **Query (range [a, b]):**
   - Return max(prev[a..b]) < a ? "YES" : "NO"

### Dry Run Example

Let's trace through with input `n=5, arr=[3,2,7,2,8]`:

```
Initial Setup:
  arr:  [_, 3, 2, 7, 2, 8]  (1-indexed)

  pos[3] = {1}
  pos[2] = {2, 4}
  pos[7] = {3}
  pos[8] = {5}

  prev[1] = 0  (no previous 3)
  prev[2] = 0  (no previous 2 before index 2)
  prev[3] = 0  (no previous 7)
  prev[4] = 2  (previous 2 is at index 2)
  prev[5] = 0  (no previous 8)

  prev array: [_, 0, 0, 0, 2, 0]

Query 1: Range [3, 5]
  max(prev[3], prev[4], prev[5]) = max(0, 2, 0) = 2
  Is 2 < 3? YES -> all distinct

Query 2: Range [2, 5]
  max(prev[2], prev[3], prev[4], prev[5]) = max(0, 0, 2, 0) = 2
  Is 2 < 2? NO -> has duplicates (value 2 at positions 2 and 4)

Update: arr[2] = 9
  Remove 2 from pos[2]: pos[2] = {4}
  Update prev[4] = 0 (no previous 2 now)
  Add 2 to pos[9]: pos[9] = {2}
  prev[2] = 0 (no previous 9)

  New prev array: [_, 0, 0, 0, 0, 0]

Query 3: Range [2, 5]
  max(prev[2], prev[3], prev[4], prev[5]) = max(0, 0, 0, 0) = 0
  Is 0 < 2? YES -> all distinct
```

### Visual Diagram

```
Array:    [3]  [2]  [7]  [2]  [8]
Index:     1    2    3    4    5

prev[]:    0    0    0    2    0
                         ^
                         |
              duplicate of index 2

Query [2,5]: max(prev[2..5]) = 2 >= 2 -> NO (has duplicates)
Query [3,5]: max(prev[3..5]) = 2 >= 3? No, 2 < 3 -> YES (all distinct)
```

### Code (Python)

```python
import sys
from collections import defaultdict
from sortedcontainers import SortedList

def solve():
 """
 Optimal solution using segment tree for range max queries.

 Time: O((n + q) * log n)
 Space: O(n)
 """
 input = sys.stdin.readline

 n, q = map(int, input().split())
 arr = [0] + list(map(int, input().split()))  # 1-indexed

 # Segment tree for range maximum
 tree = [0] * (4 * n)

 def build(node, start, end):
  if start == end:
   tree[node] = prev[start]
   return
  mid = (start + end) // 2
  build(2 * node, start, mid)
  build(2 * node + 1, mid + 1, end)
  tree[node] = max(tree[2 * node], tree[2 * node + 1])

 def update(node, start, end, idx, val):
  if start == end:
   tree[node] = val
   return
  mid = (start + end) // 2
  if idx <= mid:
   update(2 * node, start, mid, idx, val)
  else:
   update(2 * node + 1, mid + 1, end, idx, val)
  tree[node] = max(tree[2 * node], tree[2 * node + 1])

 def query(node, start, end, l, r):
  if r < start or end < l:
   return 0
  if l <= start and end <= r:
   return tree[node]
  mid = (start + end) // 2
  return max(query(2 * node, start, mid, l, r),
    query(2 * node + 1, mid + 1, end, l, r))

 # pos[v] = sorted list of positions where value v appears
 pos = defaultdict(SortedList)
 prev = [0] * (n + 2)  # prev[i] = previous occurrence of arr[i]

 # Initialize
 for i in range(1, n + 1):
  v = arr[i]
  # Find predecessor in pos[v]
  idx = pos[v].bisect_left(i)
  if idx > 0:
   prev[i] = pos[v][idx - 1]
  pos[v].add(i)

 build(1, 1, n)

 results = []
 for _ in range(q):
  line = list(map(int, input().split()))

  if line[0] == 1:  # Update arr[k] = u
   k, u = line[1], line[2]
   old_val = arr[k]

   if old_val == u:
    continue  # No change

   # Remove k from pos[old_val]
   pos[old_val].remove(k)
   idx = pos[old_val].bisect_left(k)
   # Update successor's prev if exists
   if idx < len(pos[old_val]):
    succ = pos[old_val][idx]
    if idx > 0:
     prev[succ] = pos[old_val][idx - 1]
    else:
     prev[succ] = 0
    update(1, 1, n, succ, prev[succ])

   # Add k to pos[u]
   arr[k] = u
   idx = pos[u].bisect_left(k)
   # Update prev[k]
   if idx > 0:
    prev[k] = pos[u][idx - 1]
   else:
    prev[k] = 0
   update(1, 1, n, k, prev[k])

   pos[u].add(k)
   idx = pos[u].bisect_left(k)
   # Update successor's prev if exists
   if idx + 1 < len(pos[u]):
    succ = pos[u][idx + 1]
    prev[succ] = k
    update(1, 1, n, succ, prev[succ])

  else:  # Query: check if range [a, b] has all distinct values
   a, b = line[1], line[2]
   max_prev = query(1, 1, n, a, b)
   results.append("YES" if max_prev < a else "NO")

 print('\n'.join(results))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | Each query/update is O(log n) |
| Space | O(n) | Segment tree and position sets |

---

## Common Mistakes

### Mistake 1: Not Handling Update Cascades

```python
# WRONG - Only updating the changed position
def update_wrong(k, u):
 arr[k] = u
 prev[k] = find_prev(k)
 update_tree(k, prev[k])  # Missing: update successor's prev!
```

**Problem:** When you change arr[k], both k's prev AND the successor's prev need updating.
**Fix:** After removing k from old value's set and adding to new value's set, update the successor in both sets.

### Mistake 2: Wrong Distinctness Condition

```python
# WRONG - Using <= instead of <
if max_prev <= a:  # Should be max_prev < a
 print("YES")
```

**Problem:** If max_prev == a, it means some element at position >= a has its duplicate exactly at position a, so there IS a duplicate in range.
**Fix:** The condition must be strictly less than: `max_prev < a`.

### Mistake 3: Off-by-One in 1-Indexing

```python
# WRONG - Using 0-indexed array with 1-indexed queries
arr = list(map(int, input().split()))  # 0-indexed
# Query asks for range [1, n], but arr[0] is first element
```

**Problem:** CSES uses 1-indexed positions in queries.
**Fix:** Pad array with dummy element at index 0: `arr = [0] + list(...)`.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `arr=[5], query [1,1]` | YES | Single element is always distinct |
| All same values | `arr=[3,3,3], query [1,3]` | NO | All duplicates |
| Update to same value | `update 2 to arr[2]` | (no change) | Optimization: skip if value unchanged |
| Adjacent duplicates | `arr=[1,1], query [1,2]` | NO | prev[2] = 1 >= 1 |
| Large values | `arr=[10^9, 10^9]` | NO | Handle values up to 10^9 |

---

## When to Use This Pattern

### Use This Approach When:
- You need to check range distinctness with point updates
- You can transform "all distinct" into "range max of prev[] < start"
- Updates are frequent and queries span varying ranges

### Don't Use When:
- No updates (offline Mo's algorithm may be simpler)
- Only need count of distinct values (different problem)
- Memory is extremely limited (sqrt decomposition uses less)

### Pattern Recognition Checklist:
- [ ] Need to check for duplicates in range? -> **Consider prev[] array**
- [ ] Range queries with point updates? -> **Consider segment tree**
- [ ] Transform "all X" into "range min/max satisfies condition"? -> **This pattern applies**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) | Basic segment tree range queries |
| [Dynamic Range Minimum Queries](https://cses.fi/problemset/task/1649) | Segment tree with point updates |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Distinct Values Queries](https://cses.fi/problemset/task/1734) | Count distinct (no updates), use Mo's algorithm |
| [Range Update Queries](https://cses.fi/problemset/task/1651) | Segment tree with lazy propagation |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | Complex segment tree operations |
| [Range Queries and Copies](https://cses.fi/problemset/task/1737) | Persistent segment tree |

---

## Key Takeaways

1. **The Core Idea:** Transform "all distinct in range" into "range max of prev[] < start"
2. **Time Optimization:** From O(n) per query to O(log n) using segment tree
3. **Space Trade-off:** O(n) extra space for prev[] array and position tracking
4. **Pattern:** Range property queries can often be reduced to range min/max queries

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why max(prev[a..b]) < a implies all values are distinct
- [ ] Implement segment tree for range max with point updates
- [ ] Handle the cascade updates when modifying a position
- [ ] Solve this problem without looking at the solution

---

## Additional Resources

- [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)
- [CSES Problem Set - Range Queries](https://cses.fi/problemset/list/)
- [Competitive Programmer's Handbook - Chapter 28: Segment Trees](https://cses.fi/book/book.pdf)
