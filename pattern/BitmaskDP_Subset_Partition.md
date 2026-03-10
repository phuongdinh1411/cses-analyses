---
layout: simple
title: "Bitmask DP — Subset Partition & TSP Patterns"
permalink: /pattern/bitmask-dp-subset-partition
---

# Bitmask DP — Subset Partition & TSP Patterns

A comprehensive walkthrough of 6 LeetCode problems that share the same bitmask DP engine, organized from the core pattern to its variants.

---

## Pattern Overview

All problems in this family share:
- **n ≤ 16** → use bitmask to represent subsets
- **dp[mask]** = optimal value for the subset of items represented by `mask`
- **Subset enumeration** via `sub = (sub - 1) & mask`

Three main flavors:

```
Subset Partition          TSP-Style              Dependency-Constrained
(order doesn't matter)    (order matters)        (topological order)

dp[mask]                  dp[mask][last]         dp[mask]
split: (sub-1) & mask     extend: mask|(1<<j)    extend: mask|sub (if prereqs met)
O(3^n)                    O(n² · 2^n)            O(3^n)

1986, 2305, 698,          943 Superstring        1494 Parallel Courses
1723, 3801
```

---

## Table of Contents

1. [Core Technique: Subset Enumeration](#1-core-technique-subset-enumeration)
2. [Precompute Pattern](#2-precompute-pattern)
3. [Problem 1986 — Minimum Number of Work Sessions](#3-problem-1986--minimum-number-of-work-sessions)
4. [Problem 2305 — Fair Distribution of Cookies](#4-problem-2305--fair-distribution-of-cookies)
5. [Problem 698 — Partition to K Equal Sum Subsets](#5-problem-698--partition-to-k-equal-sum-subsets)
6. [Problem 1723 — Find Minimum Time to Complete All Jobs](#6-problem-1723--find-minimum-time-to-complete-all-jobs)
7. [Problem 3801 — Minimum Cost to Merge Sorted Lists](#7-problem-3801--minimum-cost-to-merge-sorted-lists)
8. [Problem 943 — Find the Shortest Superstring (TSP)](#8-problem-943--find-the-shortest-superstring-tsp)
9. [Problem 1494 — Parallel Courses II (Dependencies)](#9-problem-1494--parallel-courses-ii-dependencies)
10. [Master Comparison Table](#10-master-comparison-table)
11. [How to Identify This Pattern](#11-how-to-identify-this-pattern)

---

## 1. Core Technique: Subset Enumeration

### Enumerate all submasks of a mask

```python
sub = mask
while sub > 0:
    # process sub
    sub = (sub - 1) & mask
```

**How `(sub - 1) & mask` works:**
- `sub - 1` flips the lowest set bit and sets all lower bits
- `& mask` keeps only bits that exist in the original mask
- This generates all submasks in descending order

**Total complexity across all masks**: O(3^n), because each element is either:
- In `sub` only
- In `complement` only
- Not in `mask` at all
→ 3 choices per element → 3^n total work

### Dedup trick: `sub < comp`

When splitting a mask into two halves, (sub, comp) and (comp, sub) are the same split:

```python
sub = (mask - 1) & mask
while sub > 0:
    comp = mask ^ sub
    if sub < comp:        # only process each pair once
        # process (sub, comp)
    sub = (sub - 1) & mask
```

---

## 2. Precompute Pattern

Almost every problem in this family precomputes a per-mask value (sum, length, feasibility):

```python
# Simple loop approach (O(n · 2^n), clear and readable)
total = [0] * (1 << n)
for mask in range(1, 1 << n):
    for i in range(n):
        if mask & (1 << i):
            total[mask] += items[i]
```

Alternative using lowest-bit trick (O(2^n) but less readable):

```python
total = [0] * (1 << n)
for i in range(n):
    total[1 << i] = items[i]
for mask in range(1, 1 << n):
    if not total[mask]:
        lb = mask & -mask
        total[mask] = total[lb] + total[mask ^ lb]
```

---

## 3. Problem 1986 — Minimum Number of Work Sessions

**Difficulty**: Medium | **Constraint**: n ≤ 14

> Given tasks array and sessionTime, find minimum number of work sessions.
> Each session can hold tasks with total time ≤ sessionTime.

### Key Idea

- Precompute `total[mask]` and `fits[mask] = (total[mask] <= sessionTime)`
- `dp[mask]` = minimum sessions to complete all tasks in mask
- Peel off one fitting subset per session

### Solution

```python
class Solution:
    def minSessions(self, tasks: list[int], sessionTime: int) -> int:
        n = len(tasks)
        full = (1 << n) - 1

        total = [0] * (1 << n)
        for mask in range(1, 1 << n):
            for i in range(n):
                if mask & (1 << i):
                    total[mask] += tasks[i]

        fits = [total[mask] <= sessionTime for mask in range(1 << n)]

        INF = float('inf')
        dp = [INF] * (1 << n)
        dp[0] = 0

        for mask in range(1, 1 << n):
            sub = mask
            while sub > 0:
                if fits[sub]:
                    val = dp[mask ^ sub] + 1
                    if val < dp[mask]:
                        dp[mask] = val
                sub = (sub - 1) & mask

        return dp[full]
```

**Complexity**: O(3^n) time, O(2^n) space

---

## 4. Problem 2305 — Fair Distribution of Cookies

**Difficulty**: Medium | **Constraint**: n ≤ 8

> Distribute cookie bags to k children. Minimize the maximum total cookies any child gets.

### Approach A: Binary Search + 1986

"Minimize the maximum" → binary search on the answer, then check feasibility using 1986.

```python
class Solution:
    def distributeCookies(self, cookies: list[int], k: int) -> int:
        n = len(cookies)
        full = (1 << n) - 1

        total = [0] * (1 << n)
        for mask in range(1, 1 << n):
            for i in range(n):
                if mask & (1 << i):
                    total[mask] += cookies[i]

        lo = max(cookies)
        hi = sum(cookies)

        while lo < hi:
            mid = lo + (hi - lo) // 2

            fits = [total[mask] <= mid for mask in range(1 << n)]
            INF = float('inf')
            dp = [INF] * (1 << n)
            dp[0] = 0

            for mask in range(1, 1 << n):
                sub = mask
                while sub > 0:
                    if fits[sub]:
                        val = dp[mask ^ sub] + 1
                        if val < dp[mask]:
                            dp[mask] = val
                    sub = (sub - 1) & mask

            if dp[full] <= k:
                hi = mid
            else:
                lo = mid + 1

        return lo
```

**Complexity**: O(3^n · log S) time

### Approach B: Direct DP with child dimension

`dp[j][mask]` = min max-sum distributing cookies in mask to j children.

```python
class Solution:
    def distributeCookies(self, cookies: list[int], k: int) -> int:
        n = len(cookies)
        full = (1 << n) - 1

        total = [0] * (1 << n)
        for mask in range(1, 1 << n):
            for i in range(n):
                if mask & (1 << i):
                    total[mask] += cookies[i]

        INF = float('inf')
        dp = [[INF] * (1 << n) for _ in range(k + 1)]
        dp[0][0] = 0

        for j in range(1, k + 1):
            for mask in range(1, 1 << n):
                sub = mask
                while sub > 0:
                    remaining = mask ^ sub
                    val = max(dp[j - 1][remaining], total[sub])
                    if val < dp[j][mask]:
                        dp[j][mask] = val
                    sub = (sub - 1) & mask

        return dp[k][full]
```

**Complexity**: O(k · 3^n) time, O(k · 2^n) space

---

## 5. Problem 698 — Partition to K Equal Sum Subsets

**Difficulty**: Medium | **Constraint**: n ≤ 16

> Can we divide array into k non-empty subsets with equal sums?

### Key Difference

The valid subset condition is **exact equality** (`total[sub] == target`), not `<=`.

```python
class Solution:
    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        total_sum = sum(nums)
        if total_sum % k != 0:
            return False

        target = total_sum // k
        if max(nums) > target:
            return False

        n = len(nums)
        total = [0] * (1 << n)
        for mask in range(1, 1 << n):
            for i in range(n):
                if mask & (1 << i):
                    total[mask] += nums[i]

        valid = [total[mask] == target for mask in range(1 << n)]

        INF = float('inf')
        dp = [INF] * (1 << n)
        dp[0] = 0

        for mask in range(1, 1 << n):
            sub = mask
            while sub > 0:
                if valid[sub]:
                    val = dp[mask ^ sub] + 1
                    if val < dp[mask]:
                        dp[mask] = val
                sub = (sub - 1) & mask

        return dp[(1 << n) - 1] == k
```

**Complexity**: O(3^n) time, O(2^n) space

---

## 6. Problem 1723 — Find Minimum Time to Complete All Jobs

**Difficulty**: Hard | **Constraint**: n ≤ 12

> Assign jobs to k workers. Minimize the maximum working time.

This is **identical to 2305** with larger n. Both approaches work:

| Approach | Time | n=12 operations |
|----------|------|-----------------|
| Direct DP: `dp[j][mask]` | O(k · 3^n) | ~6.4M |
| Binary Search + 1986 | O(3^n · log S) | ~12.7M |

Solution is the same code as 2305 — just swap `cookies` → `jobs`.

---

## 7. Problem 3801 — Minimum Cost to Merge Sorted Lists

**Difficulty**: Hard | **Constraint**: n ≤ 14

> Merge n sorted lists into one. Cost to merge two lists = total_length + |median_1 - median_2|.

### What's Different

- **Precompute is heavier**: need `total_len[mask]` AND `median[mask]`
- **Median via binary search**: find k-th element across multiple sorted lists
- **Split into two halves**: use `sub < comp` dedup trick

```python
from bisect import bisect_right

class Solution:
    def minCost(self, lists: list[list[int]]) -> int:
        n = len(lists)
        if n == 1:
            return 0
        full = (1 << n) - 1

        # Precompute total_len
        total_len = [0] * (1 << n)
        for mask in range(1, 1 << n):
            for i in range(n):
                if mask & (1 << i):
                    total_len[mask] += len(lists[i])

        # Precompute median via binary search
        gmin = min(lst[0] for lst in lists)
        gmax = max(lst[-1] for lst in lists)
        med = [0] * (1 << n)

        for mask in range(1, 1 << n):
            k = (total_len[mask] - 1) // 2
            lo, hi = gmin, gmax
            while lo < hi:
                mid = lo + (hi - lo) // 2
                count = 0
                for i in range(n):
                    if mask & (1 << i):
                        count += bisect_right(lists[i], mid)
                if count <= k:
                    lo = mid + 1
                else:
                    hi = mid
            med[mask] = lo

        # DP — split into two halves
        INF = float('inf')
        dp = [INF] * (1 << n)
        for i in range(n):
            dp[1 << i] = 0

        for mask in range(1, 1 << n):
            if bin(mask).count('1') < 2:
                continue
            tl = total_len[mask]
            sub = (mask - 1) & mask
            while sub > 0:
                comp = mask ^ sub
                if sub < comp:
                    val = dp[sub] + dp[comp] + tl + abs(med[sub] - med[comp])
                    if val < dp[mask]:
                        dp[mask] = val
                sub = (sub - 1) & mask

        return dp[full]
```

**Complexity**: O(3^n · n · log V) time, O(2^n) space

---

## 8. Problem 943 — Find the Shortest Superstring (TSP)

**Difficulty**: Hard | **Constraint**: n ≤ 12

> Find shortest string containing all given words as substrings.

### Key Difference: Order Matters → TSP-Style

This is NOT subset partition — it's the **Travelling Salesman Problem**.
The cost depends on which word comes **after** which (pairwise overlap).

**State**: `dp[mask][i]` = min length to form superstring of words in mask, ending with word `i`

### Step 1: Precompute Pairwise Overlaps

```python
overlap = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        max_ov = min(len(words[i]), len(words[j]))
        for k in range(max_ov, 0, -1):
            if words[i].endswith(words[j][:k]):
                overlap[i][j] = k
                break
```

### Step 2: TSP DP + Path Reconstruction

```python
class Solution:
    def shortestSuperstring(self, words: list[str]) -> str:
        n = len(words)

        # Precompute overlaps
        overlap = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                max_ov = min(len(words[i]), len(words[j]))
                for k in range(max_ov, 0, -1):
                    if words[i].endswith(words[j][:k]):
                        overlap[i][j] = k
                        break

        # DP
        INF = float('inf')
        dp = [[INF] * n for _ in range(1 << n)]
        parent = [[-1] * n for _ in range(1 << n)]

        for i in range(n):
            dp[1 << i][i] = len(words[i])

        for mask in range(1, 1 << n):
            for i in range(n):
                if not (mask & (1 << i)) or dp[mask][i] == INF:
                    continue
                for j in range(n):
                    if mask & (1 << j):
                        continue
                    new_mask = mask | (1 << j)
                    val = dp[mask][i] + len(words[j]) - overlap[i][j]
                    if val < dp[new_mask][j]:
                        dp[new_mask][j] = val
                        parent[new_mask][j] = i

        # Backtrack
        full = (1 << n) - 1
        last = min(range(n), key=lambda i: dp[full][i])

        order = []
        mask = full
        while last != -1:
            order.append(last)
            prev = parent[mask][last]
            mask ^= (1 << last)  # remove last from mask
            last = prev
        order.reverse()

        # Build string
        result = words[order[0]]
        for k in range(1, len(order)):
            i, j = order[k - 1], order[k]
            result += words[j][overlap[i][j]:]

        return result
```

**Complexity**: O(n² · 2^n) time, O(n · 2^n) space

### Why `mask ^= (1 << last)` in backtracking

XOR toggles the bit off. Since we know `last` is in the mask (we just visited it), the bit is guaranteed to be 1, so XOR turns it to 0 — removing it.

---

## 9. Problem 1494 — Parallel Courses II (Dependencies)

**Difficulty**: Hard | **Constraint**: n ≤ 15

> Take courses with prerequisites, at most k per semester. Minimize semesters.

### Key Difference: Dependency Constraints

Before taking a course, all its prerequisites must be completed. Encode prerequisites as bitmasks:

```python
prereq[i] |= (1 << j)  # course i requires course j
```

A course `i` is **available** given completed `mask` if:
```python
(prereq[i] & mask) == prereq[i]  # all prereqs are in mask
```

### Solution

```python
class Solution:
    def minNumberOfSemesters(self, n: int, relations: list[list[int]], k: int) -> int:
        prereq = [0] * n
        for prev, nxt in relations:
            prereq[nxt - 1] |= (1 << (prev - 1))

        full = (1 << n) - 1
        INF = float('inf')
        dp = [INF] * (1 << n)
        dp[0] = 0

        for mask in range(full):
            if dp[mask] == INF:
                continue

            # Find available courses
            available = 0
            for i in range(n):
                if mask & (1 << i):
                    continue
                if (prereq[i] & mask) == prereq[i]:
                    available |= (1 << i)

            # Enumerate subsets of available, take up to k
            sub = available
            while sub > 0:
                if bin(sub).count('1') <= k:
                    new_mask = mask | sub
                    val = dp[mask] + 1
                    if val < dp[new_mask]:
                        dp[new_mask] = val
                sub = (sub - 1) & available

        return dp[full]
```

**Complexity**: O(3^n · n) time, O(2^n) space

---

## 10. Master Comparison Table

| Problem | Difficulty | n | dp State | "Good" Subset | Transition | Return | Time |
|---------|-----------|---|----------|---------------|------------|--------|------|
| **1986** Sessions | Medium | ≤14 | `dp[mask]` | `sum ≤ sessionTime` | Peel off 1 fitting subset | `dp[full]` | O(3^n) |
| **2305** Cookies | Medium | ≤8 | `dp[j][mask]` | Any subset | Peel off 1 subset per child | `dp[k][full]` | O(k·3^n) |
| **2305** (alt) | Medium | ≤8 | `dp[mask]` | `sum ≤ threshold` | Binary search + 1986 check | Binary search answer | O(3^n·log S) |
| **698** Equal Partition | Medium | ≤16 | `dp[mask]` | `sum == target` | Peel off 1 exact subset | `dp[full] == k` | O(3^n) |
| **1723** Jobs | Hard | ≤12 | `dp[j][mask]` | Any subset | Same as 2305 | `dp[k][full]` | O(k·3^n) |
| **3801** Merge Lists | Hard | ≤14 | `dp[mask]` | Split into 2 halves | `sub < comp` dedup | `dp[full]` | O(3^n·n·log V) |
| **943** Superstring | Hard | ≤12 | `dp[mask][last]` | N/A (TSP) | Extend by 1 word | `min(dp[full][i])` | O(n²·2^n) |
| **1494** Par. Courses | Hard | ≤15 | `dp[mask]` | Available + `popcount ≤ k` | Extend by available subset | `dp[full]` | O(3^n·n) |

---

## 11. How to Identify This Pattern

### Trigger: `n ≤ 16` + "partition/assign/select all items"

```
See n ≤ 16?
  └── Yes → Bitmask DP likely
        │
        ├── "Partition into groups"?
        │     ├── Minimize group count      → 1986 pattern
        │     ├── Minimize max group sum    → 2305 pattern (or binary search + 1986)
        │     ├── Equal group sums?         → 698 pattern
        │     └── Custom merge cost?        → 3801 pattern (split into halves)
        │
        ├── "Order matters" / "pairwise cost"?
        │     └── TSP-style dp[mask][last]  → 943 pattern
        │
        └── "Dependencies / prerequisites"?
              └── Filter available by prereqs → 1494 pattern
```

### The Universal Skeleton

```python
# 1. Precompute per-mask values
for mask in range(1, 1 << n):
    # compute total[mask], fits[mask], valid[mask], etc.

# 2. Base case
dp[0] = 0  # (or dp[1<<i] for single items)

# 3. For each mask, enumerate subsets and transition
for mask in range(1, 1 << n):
    sub = mask  # (or sub = (mask-1) & mask for partition)
    while sub > 0:
        if is_good(sub):  # problem-specific filter
            dp[mask] = min(dp[mask], dp[mask ^ sub] + cost(sub))
        sub = (sub - 1) & mask

# 4. Answer
return dp[full]
```

The only thing that changes between problems is:
- **What you precompute** (sum, median, overlap, prerequisites)
- **What makes a subset "good"** (`≤ limit`, `== target`, `prereqs met`, `popcount ≤ k`)
- **How you score the transition** (+1, max(), custom cost)

Master this skeleton, and all 7 problems become the same problem with different pluggable parts.

---

## Practice Order

```
Start here
    │
    ▼
  1986 (Medium) ─── Core pattern: peel off fitting subsets
    │
    ▼
  2305 (Medium) ─── Add child dimension OR binary search reduction
    │
    ▼
   698 (Medium) ─── Change filter to exact equality
    │
    ▼
  1723 (Hard) ──── Same as 2305 with larger n
    │
    ▼
  3801 (Hard) ──── Custom cost, split into halves, median binary search
    │
    ▼
   943 (Hard) ──── TSP variant: dp[mask][last], pairwise overlaps
    │
    ▼
  1494 (Hard) ──── Add dependency graph constraints
```

---

## Key Bit Operations Reference

| Operation | Code | Purpose |
|-----------|------|---------|
| Check bit i | `mask & (1 << i)` | Is item i in the subset? |
| Set bit i | `mask \| (1 << i)` | Add item i to subset |
| Clear bit i | `mask ^ (1 << i)` | Remove item i (when known set) |
| Clear bit i (safe) | `mask & ~(1 << i)` | Remove item i (always works) |
| Next submask | `(sub - 1) & mask` | Enumerate submasks |
| Complement | `mask ^ sub` | Items in mask but not sub |
| Lowest set bit | `mask & -mask` | Isolate lowest bit |
| Count bits | `bin(mask).count('1')` | How many items in subset |
| All n bits | `(1 << n) - 1` | Full mask |

---

*Pattern mastered through 7 problems — same engine, different pluggable parts.*
