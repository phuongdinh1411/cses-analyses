---
layout: simple
title: "Sorting Patterns"
permalink: /pattern/sorting
---

# Sorting Patterns — Comprehensive Guide

Sorting is almost never the end goal — it's the preprocessing step that *unlocks* a faster second algorithm. The core insight:

> **Sorting removes the need to consider all O(n²) pairs. Once elements are ordered, you can answer "which element is relevant here?" in O(log n) or O(1) instead of O(n).**

The skill in hard problems is recognising *what* to sort by and *which* second algorithm becomes efficient after that.

---

## Quick Navigation: "I need to..."

| I need to... | Sort by | Second algorithm | Section |
|---|---|---|---|
| Assign tasks/workers optimally | ratio / exchange key | Greedy + heap | [1](#1-sort--greedy-exchange-argument) |
| Schedule jobs, maximize profit | end time / weight | DP + binary search | [2](#2-sort--dp) |
| Find kth smallest pair value | values | Binary search on answer | [3](#3-sort--binary-search-on-answer) |
| Dynamic median / top-K | insert order | Two heaps | [4](#4-sort--heap) |
| Process events left-to-right | coordinate / time | Sweep line | [5](#5-sweep-line--sort) |
| Connect nodes cheaply (MST) | edge weight | Union-Find (Kruskal) | [6](#6-sort--union-find-kruskal-pattern) |
| Answer offline range queries | query + data together | BIT / segment tree | [7](#7-sort--bitfenwick-tree-or-segment-tree) |
| Next-greater-element in sorted order | value | Monotonic stack | [8](#8-sort--monotonic-stack) |
| Sort itself IS the insight | problem-specific key | Identity / rotation / median | [9](#9-sorting-as-the-algorithm) |
| LIS in 2D envelope problem | width asc, height desc | Patience sort / BIS | [10](#10-lis-variants-after-sorting) |

---

## The Sorting Diagnostic

Before reaching for a sort, ask:

```
1. Does the answer depend on relative ORDER of elements (not their values)?
   → Probably sort by the key that defines that order.

2. After sorting, do I need the CLOSEST / CHEAPEST / LARGEST available element?
   → Sort + heap or sorted set.

3. After sorting, does the problem decompose into non-overlapping subproblems?
   → Sort + DP (sorting removes back-edges, creating a valid DP ordering).

4. After sorting, does a two-pointer or binary-search scan suffice?
   → Sort + binary search on answer or sliding window.

5. Is the sort order defined by a RATIO or DIFFERENCE of two fields?
   → Exchange argument. Prove swapping adjacent wrong-order elements hurts.
```

---

## 1. Sort + Greedy (Exchange Argument)

**Pattern:** Sort by a key derived from an exchange argument. Then make locally greedy decisions left-to-right.

**Exchange argument recipe:**
1. Assume an optimal solution that differs from your greedy order.
2. Find two adjacent elements in wrong greedy order: `A, B` where greedy says `B, A`.
3. Show that swapping them does not improve (or worsens) the objective.
4. Conclude the greedy order is optimal.

### Common sort keys

| Problem type | Sort key | Intuition |
|---|---|---|
| Hire workers (857) | `wage / quality` ratio ascending | Workers at same wage-per-quality can all join at the max ratio's wage |
| Finish tasks with min energy (1665) | `min_needed - actual_cost` descending | Tasks with large "slack" should be done last |
| Minimize damage taken (3273) | `damage / health` ratio descending | Kill high DPS enemies first (rate-of-damage argument) |
| Bloom flowers earliest (2136) | `grow_time` descending | Plant slow-growers first; bloom time is `plant_day + grow_time + 1` |
| Hire/fire workers, min money needed (2412) | `(cost + cashback)` descending | Worst-case cost transaction should come last |

### Template

```python
# Exchange argument sort → greedy sweep
items.sort(key=lambda x: exchange_key(x))   # proven order
result = 0
state = initial_state()
for item in items:
    state = update(state, item)              # greedy decision
    result = optimise(result, state)
return result
```

### Example: 857. Minimum Cost to Hire K Workers

```python
import heapq

def mincostToHireWorkers(quality, wage, k):
    # Sort by wage/quality ratio. At any chosen ratio r,
    # worker i's fair wage = quality[i] * r.
    workers = sorted(zip(quality, wage), key=lambda x: x[1] / x[0])
    max_heap = []   # store -quality (max-heap)
    q_sum = 0
    result = float('inf')

    for q, w in workers:
        ratio = w / q
        heapq.heappush(max_heap, -q)
        q_sum += q
        if len(max_heap) > k:
            q_sum += heapq.heappop(max_heap)   # remove largest quality
        if len(max_heap) == k:
            result = min(result, ratio * q_sum)
    return result
# Time: O(n log n), Space: O(k)
```

---

## 2. Sort + DP

**Pattern:** Sorting removes back-edges so that `dp[i]` only needs `dp[j]` for `j < i` in sorted order.

### Sub-patterns

**2a. Interval / job scheduling DP** — sort by end time, binary search for last non-overlapping job.

```python
# 1235. Maximum Profit in Job Scheduling
from bisect import bisect_right

def jobScheduling(startTime, endTime, profit):
    jobs = sorted(zip(endTime, startTime, profit))
    ends = [j[0] for j in jobs]
    # dp[i] = max profit using first i jobs
    dp = [0] * (len(jobs) + 1)
    for i, (end, start, p) in enumerate(jobs):
        # last job that ends <= start of this job
        j = bisect_right(ends, start)
        dp[i + 1] = max(dp[i], dp[j] + p)
    return dp[-1]
# Time: O(n log n), Space: O(n)
```

**2b. LIS-style DP after sorting** — sort makes the constraint one-dimensional.

```python
# 1691. Maximum Height by Stacking Cuboids
# Sort all 3 sides of each cuboid, then sort cuboids.
# dp[i] = max stack height with cuboid i on top.
def maxHeight(cuboids):
    cuboids = [sorted(c) for c in cuboids]
    cuboids.sort()
    n = len(cuboids)
    dp = [c[2] for c in cuboids]
    for i in range(n):
        for j in range(i):
            if all(cuboids[j][k] <= cuboids[i][k] for k in range(3)):
                dp[i] = max(dp[i], dp[j] + cuboids[i][2])
    return max(dp)
```

**2c. Sort + contribution DP** — sort so each element's contribution (as min or max) can be computed via prefix products.

```python
# 891. Sum of Subsequence Widths
# After sorting, a[i] is max in 2^i subsequences and min in 2^(n-1-i) subsequences.
def sumSubseqWidths(nums):
    MOD = 10**9 + 7
    nums.sort()
    n = len(nums)
    result = 0
    pw = 1
    for i, x in enumerate(nums):
        result = (result + pw * x - pw * nums[n - 1 - i]) % MOD
        pw = pw * 2 % MOD
    return result
```

### Complexity guide

| DP type | Sort cost | DP cost | Total |
|---|---|---|---|
| Job scheduling (binary search) | O(n log n) | O(n log n) | O(n log n) |
| LIS after sort | O(n log n) | O(n²) naive / O(n log n) patience | O(n log n) |
| Contribution (sorted order) | O(n log n) | O(n) | O(n log n) |

---

## 3. Sort + Binary Search on Answer

**Pattern:** Sort the data. Binary search on the *answer value* `x`. For a given `x`, use a scan/two-pointer over the sorted array to count how many pairs/windows satisfy the constraint.

```
Identify when to use:
- "Find the k-th smallest [pair/distance/sum]"
- "Minimize the maximum [something]"
- "Maximize the minimum [something]"
- Answer is monotone: if x works, x+1 also works (or vice versa)
```

### Template

```python
def solve(nums, k):
    nums.sort()

    def count(mid):
        # How many [things] have value <= mid?
        # Two-pointer scan in O(n) because nums is sorted
        ...

    lo, hi = min_possible, max_possible
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Example: 719. Find K-th Smallest Pair Distance

```python
from bisect import bisect_right

def smallestDistancePair(nums, k):
    nums.sort()
    n = len(nums)

    def count_pairs(mid):
        # Count pairs with distance <= mid using sliding window
        left = res = 0
        for right in range(n):
            while nums[right] - nums[left] > mid:
                left += 1
            res += right - left
        return res

    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_pairs(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
# Time: O(n log n + n log W) where W = max - min
```

---

## 4. Sort + Heap

**Pattern:** Sort establishes initial order or offline query order; heap maintains a dynamic top-K / min / max invariant as elements are added or removed.

### Sub-patterns

**4a. Two-heap for dynamic median (295)**

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (negate values): lower half
        self.hi = []   # min-heap: upper half

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

**4b. Offline sort + heap sweep**

Sort data and queries together by a shared key; as you process left-to-right, push items into the heap when they become "active."

```python
# 1851. Minimum Interval to Include Each Query
def minInterval(intervals, queries):
    intervals.sort()
    indexed_queries = sorted(enumerate(queries), key=lambda x: x[1])
    result = [-1] * len(queries)
    heap = []   # (size, right_end)
    i = 0

    for qi, q in indexed_queries:
        # Activate all intervals whose left <= q
        while i < len(intervals) and intervals[i][0] <= q:
            l, r = intervals[i]
            heapq.heappush(heap, (r - l + 1, r))
            i += 1
        # Remove expired intervals
        while heap and heap[0][1] < q:
            heapq.heappop(heap)
        if heap:
            result[qi] = heap[0][0]
    return result
```

**4c. Greedy with heap for "always pick best available"**

```python
# 630. Course Schedule III
def scheduleCourse(courses):
    courses.sort(key=lambda x: x[1])   # sort by deadline
    heap = []   # max-heap of durations (negate)
    time = 0
    for duration, last_day in courses:
        time += duration
        heapq.heappush(heap, -duration)
        if time > last_day:
            time += heapq.heappop(heap)   # drop the longest course
    return len(heap)
```

---

## 5. Sweep Line + Sort

**Pattern:** Model the problem as events on a line. Sort events by coordinate/time. Process left-to-right, maintaining active state.

### Event types

```
Interval problems:    (start, +1), (end+1, -1)  → count active intervals
Building heights:     (x, +height), (x+width, -height)  → track max height (skyline)
Point queries:        (query, type), (event, type) → interleave queries with data
```

### Example: 218. The Skyline Problem

```python
import heapq

def getSkyline(buildings):
    events = []
    for l, r, h in buildings:
        events.append((l, -h, r))   # start: negative height = active
        events.append((r, 0, 0))    # end
    events.sort()

    result = [[0, 0]]
    heap = [(0, float('inf'))]   # (neg_height, end)

    for x, neg_h, r in events:
        if neg_h:   # start event
            heapq.heappush(heap, (neg_h, r))
        # Remove expired buildings
        while heap[0][1] <= x:
            heapq.heappop(heap)
        cur_max = -heap[0][0]
        if result[-1][1] != cur_max:
            result.append([x, cur_max])
    return result[1:]
```

### Sweep line decision table

| Problem shape | Event type | Active structure |
|---|---|---|
| Max active intervals | +1/-1 events | Running sum |
| Max height (skyline) | start/end of rectangles | Max-heap |
| Offline point queries | queries + data sorted together | BIT / sorted set |
| Segment intersections | left/right endpoints | Sorted set (order by y) |

---

## 6. Sort + Union-Find (Kruskal Pattern)

**Pattern:** Sort edges (or constraints) by weight. Process in order, merging components. This is Kruskal's MST but generalises to any "connect greedily in weight order" problem.

```python
# Generic Kruskal template
parent = list(range(n))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    a, b = find(a), find(b)
    if a == b: return False
    parent[a] = b
    return True

edges.sort(key=lambda e: e[2])   # sort by weight
mst_cost = 0
for u, v, w in edges:
    if union(u, v):
        mst_cost += w
```

### Generalizations

| Problem | Sort by | Union-Find action |
|---|---|---|
| MST (1489) | edge weight | merge components, track MST edges |
| Offline path queries (1697) | query limit ascending | add edges ≤ limit, check connectivity |
| Good paths (2421) | node value ascending | merge nodes of equal value, count same-value pairs |
| GCD sort (1998) | share prime factors | merge numbers with common prime factors |

### Example: 1697. Checking Existence of Edge Length Limited Paths

```python
def distanceLimitedPathsExist(n, edgeList, queries):
    edgeList.sort(key=lambda e: e[2])
    # Attach original index to queries before sorting
    queries = sorted(enumerate(queries), key=lambda x: x[1][2])
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    result = [False] * len(queries)
    ei = 0
    for qi, (u, v, limit) in queries:
        while ei < len(edgeList) and edgeList[ei][2] < limit:
            a, b, _ = edgeList[ei]
            ra, rb = find(a), find(b)
            if ra != rb: parent[ra] = rb
            ei += 1
        result[qi] = find(u) == find(v)
    return result
```

---

## 7. Sort + BIT/Fenwick Tree or Segment Tree

**Pattern:** Sort by one dimension to reduce a 2D problem to 1D, then answer 1D range queries with a BIT or segment tree.

### When to use

- You need to count/sum elements satisfying `value ≤ x` dynamically as you insert.
- Problem has two constraints (e.g., index and value); fix one by sorting, handle the other with a BIT.

### Example: 2713. Maximum Strictly Increasing Cells in a Matrix

```python
# Sort all cells by value. For each cell (r,c,v), dp[r][c] = 
# 1 + max dp over cells in same row/col with smaller value.
# Use two segment trees (one per row, one per col) for range max queries.
from sortedcontainers import SortedList

def maxIncreasingCells(mat):
    m, n = len(mat), len(mat[0])
    from collections import defaultdict
    val_to_cells = defaultdict(list)
    for r in range(m):
        for c in range(n):
            val_to_cells[mat[r][c]].append((r, c))

    row_max = [0] * m
    col_max = [0] * n
    result = 0

    for val in sorted(val_to_cells):
        cells = val_to_cells[val]
        # Compute new dp values before updating (same value can't extend itself)
        new_dp = []
        for r, c in cells:
            dp_rc = 1 + max(row_max[r], col_max[c])
            new_dp.append(dp_rc)
            result = max(result, dp_rc)
        for (r, c), dp_rc in zip(cells, new_dp):
            row_max[r] = max(row_max[r], dp_rc)
            col_max[c] = max(col_max[c], dp_rc)
    return result
# Time: O(mn log(mn)), Space: O(mn)
```

---

## 8. Sort + Monotonic Stack

**Pattern:** Sort elements so that when you process them left-to-right, each new element is "greater" in some sense — enabling the monotonic stack invariant.

### Example: 975. Odd Even Jump

```python
# Sort indices by value (breaking ties by index) for "odd jumps."
# Monotonic stack finds, for each index, the next index in sorted order.
def oddEvenJumps(arr):
    n = len(arr)
    # next_higher[i] = smallest index j > i where arr[j] >= arr[i]
    # next_lower[i]  = smallest index j > i where arr[j] <= arr[i]

    def make_next(sorted_indices):
        result = [None] * n
        stack = []
        for i in sorted_indices:
            while stack and stack[-1] < i:
                result[stack.pop()] = i
            stack.append(i)
        return result

    sorted_by_val = sorted(range(n), key=lambda i: (arr[i], i))
    sorted_by_val_desc = sorted(range(n), key=lambda i: (-arr[i], i))

    next_higher = make_next(sorted_by_val)
    next_lower  = make_next(sorted_by_val_desc)

    # DP: odd[i] = can reach end starting with odd jump from i
    odd  = [False] * n
    even = [False] * n
    odd[-1] = even[-1] = True

    for i in range(n - 2, -1, -1):
        if next_higher[i] is not None:
            odd[i]  = even[next_higher[i]]
        if next_lower[i] is not None:
            even[i] = odd[next_lower[i]]

    return sum(odd)
# Time: O(n log n), Space: O(n)
```

---

## 9. Sorting as the Algorithm

Problems where the sort key or sort itself is the core insight.

### 9a. Median minimizes L1 distance

> Sum of `|x - p|` over all points is minimized when `p` is the **median**.

```python
# 296. Best Meeting Point
# Sort row coords and col coords independently, then take medians.
def minTotalDistance(grid):
    rows, cols = [], []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c]:
                rows.append(r)
                cols.append(c)
    cols.sort()
    mid_r = rows[len(rows) // 2]
    mid_c = cols[len(cols) // 2]
    return sum(abs(r - mid_r) for r in rows) + sum(abs(c - mid_c) for c in cols)
```

### 9b. Orderly Queue — sort string when K ≥ 2

```python
# 899. Orderly Queue
# K=1: only cyclic rotations possible → return minimum rotation.
# K≥2: any permutation reachable (bubble-sort argument) → return sorted string.
def orderlyQueue(s, k):
    if k == 1:
        return min(s[i:] + s[:i] for i in range(len(s)))
    return ''.join(sorted(s))
```

### 9c. Chebyshev transform (rotate 45°) to minimize Manhattan distance

```python
# 3102. Minimize Manhattan Distances
# Manhattan distance |x1-x2| + |y1-y2| = Chebyshev max(|u1-u2|, |v1-v2|)
# where u = x+y, v = x-y.
# After transform, minimize max(|u1-u2|, |v1-v2|) → just sort u and v separately.
def minimumDistance(points):
    from sortedcontainers import SortedList
    us = SortedList(x + y for x, y in points)
    vs = SortedList(x - y for x, y in points)
    result = float('inf')
    for x, y in points:
        u, v = x + y, x - y
        us.remove(u); vs.remove(v)
        result = min(result, max(us[-1]-us[0], vs[-1]-vs[0]))
        us.add(u); vs.add(v)
    return result
```

### 9d. Cycle sort / permutation cycles

```python
# 2459. Sort Array by Moving Items to Empty Space
# Count cycles in the permutation. Minimum swaps = n - num_cycles.
# (Special case if 0 is in a cycle.)
def sortArray(nums):
    def count_swaps(arr, target):
        visited = [False] * len(arr)
        pos = {v: i for i, v in enumerate(arr)}
        swaps = 0
        for i in range(len(arr)):
            if not visited[i] and arr[i] != target[i]:
                cycle = 0
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = pos[target[j]]
                    cycle += 1
                swaps += cycle + 1   # extra swap to move 0 in
        return swaps
    n = len(nums)
    return min(count_swaps(nums, list(range(n))),
               count_swaps(nums, list(range(1, n)) + [0]))
```

---

## 10. LIS Variants After Sorting

**Pattern:** Reduce 2D constraint to 1D LIS by careful sort key choice.

### 354. Russian Doll Envelopes — the canonical example

Sort by width ascending, **height descending** (for same width). Then find LIS on heights only.

**Why height descending for same width?** — same-width envelopes can never nest. If heights were ascending, two envelopes with width 5 would form a length-2 LIS. Height descending prevents this: among same-width envelopes, LIS can pick at most one.

```python
from bisect import bisect_left

def maxEnvelopes(envelopes):
    envelopes.sort(key=lambda x: (x[0], -x[1]))   # width asc, height desc
    # LIS on heights using patience sorting (O(n log n))
    tails = []
    for _, h in envelopes:
        pos = bisect_left(tails, h)
        if pos == len(tails):
            tails.append(h)
        else:
            tails[pos] = h
    return len(tails)
# Time: O(n log n), Space: O(n)
```

### Patience sort (LIS in O(n log n))

```python
from bisect import bisect_left

def lengthOfLIS(nums):
    tails = []   # tails[i] = smallest tail of all IS of length i+1
    for x in nums:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)
```

---

## Complexity Summary

| Pattern | Sort cost | Second algo | Total |
|---|---|---|---|
| Greedy (exchange) | O(n log n) | O(n) or O(n log n) heap | O(n log n) |
| Sort + DP (job scheduling) | O(n log n) | O(n log n) | O(n log n) |
| Sort + binary search on answer | O(n log n) | O(n log W) | O(n log n + n log W) |
| Sort + heap sweep | O(n log n) | O(n log n) | O(n log n) |
| Sweep line | O(n log n) | O(n log n) | O(n log n) |
| Sort + Union-Find (Kruskal) | O(E log E) | O(E α(V)) | O(E log E) |
| Sort + BIT/seg tree | O(n log n) | O(n log n) | O(n log n) |
| Sort + monotonic stack | O(n log n) | O(n) | O(n log n) |
| LIS after sort (patience) | O(n log n) | O(n log n) | O(n log n) |

---

## Problem Index by Technique

### Sort + Greedy
502 · 630 · 757 · 857 · 1383 · 1402 · 1665 · 2071 · 2136 · 2141 · 2412 · 2449 · 2551 · 2813 · 3219 · 3273

### Sort + DP
354 · 1187 · 1235 · 1340 · 1363 · 1478 · 1547 · 1691 · 1751 · 2463 · 2681 · 2809 · 3041 · 3098 · 3414

### Sort + Binary Search on Answer
719 · 1889 · 2071 · 2234 · 2604 · 2790 · 2819 · 2968 · 3288 · 3347

### Sort + Heap
218 · 295 · 358 · 502 · 632 · 759 · 857 · 1383 · 1851 · 2386 · 2402 · 2454 · 2503

### Sweep Line + Sort
218 · 759 · 1610 · 1840 · 2251 · 3009 · 3382

### Sort + Union-Find
1489 · 1632 · 1697 · 1724 · 1998 · 2092 · 2371 · 2421 · 3695

### Sort + BIT / Segment Tree
2659 · 2713 · 2736 · 3762

### Sort + Monotonic Stack
768 · 975 · 2818

### Sorting as the Algorithm
296 · 891 · 899 · 1585 · 2459 · 2613 · 3027 · 3102

### LIS after Sort
354 · 1187 · 1691 · 3288
