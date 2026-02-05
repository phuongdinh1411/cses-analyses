---
layout: simple
title: "Nested Ranges Check - Sorting Problem"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_check_analysis
difficulty: Medium
tags: [sorting, intervals, coordinate-compression, sweep-line]
---

# Nested Ranges Check

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **CSES Link** | [https://cses.fi/problemset/task/2168](https://cses.fi/problemset/task/2168) |
| **Key Technique** | Sorting + Min/Max Tracking |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand range containment relationships (contains vs contained by)
- [ ] Apply custom sorting strategies for interval problems
- [ ] Track running min/max to detect containment efficiently
- [ ] Handle coordinate compression for large value ranges
- [ ] Maintain original indices through sorting transformations

---

## Problem Statement

**Problem:** Given n ranges [a_i, b_i], for each range determine:
1. Does it **contain** any other range? (Output line 1)
2. Is it **contained by** any other range? (Output line 2)

**Containment Definition:**
- Range [a_i, b_i] **contains** [a_j, b_j] if: a_i <= a_j AND b_j <= b_i
- Range [a_i, b_i] **is contained by** [a_j, b_j] if: a_j <= a_i AND b_i <= b_j

**Input:**
- Line 1: Integer n (number of ranges)
- Lines 2 to n+1: Two integers a_i and b_i (range endpoints)

**Output:**
- Line 1: n integers (1 if range i contains another, 0 otherwise)
- Line 2: n integers (1 if range i is contained by another, 0 otherwise)

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= a_i <= b_i <= 10^9

### Example

```
Input:
4
1 6
2 4
4 8
3 6

Output:
1 0 0 0
0 1 0 1
```

**Explanation:**

```
Ranges visualization:
Range 1: [1,6]    |------|
Range 2: [2,4]      |--|
Range 3: [4,8]          |----|
Range 4: [3,6]        |---|

Analysis:
- Range 1 [1,6]: Contains range 2 [2,4] (1<=2 and 4<=6) -> contains=1
- Range 2 [2,4]: Contained by range 1 [1,6] -> contained=1
- Range 3 [4,8]: Neither contains nor is contained -> 0, 0
- Range 4 [3,6]: Contained by range 1 [1,6] (1<=3 and 6<=6) -> contained=1
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently check if a range contains or is contained by another without comparing all O(n^2) pairs?

The insight is that **sorting creates order**, and within that order, we can track running min/max values to detect containment in a single pass.

### Breaking Down the Problem

1. **What are we looking for?** For each range, binary answers to two questions: contains another? contained by another?
2. **What information do we have?** n ranges with start and end points.
3. **What's the relationship?** Containment depends on both endpoints - we need a[i] <= a[j] AND b[j] <= b[i].

### Key Insight

If we sort ranges by **start ascending, end descending**:
- Ranges that start earlier come first
- Among ranges with same start, longer ranges come first
- For "contains": a range contains another if a later range has smaller or equal end
- For "contained by": a range is contained if an earlier range has larger or equal end

### Analogies

Think of ranges as **time slots for meetings**. A meeting "contains" another if it starts before or at the same time AND ends after or at the same time. By sorting meetings by start time, we can track the "longest meeting seen so far" to quickly identify containment.

---

## Solution 1: Brute Force

### Idea

Compare every pair of ranges and check containment conditions directly.

### Algorithm

1. For each range i, check all other ranges j
2. If a[i] <= a[j] AND b[j] <= b[i], mark i as "contains"
3. If a[j] <= a[i] AND b[i] <= b[j], mark i as "contained"

### Code

```python
def solve_brute_force(n, ranges):
 """
 Brute force: check all pairs.

 Time: O(n^2)
 Space: O(n)
 """
 contains = [0] * n
 contained = [0] * n

 for i in range(n):
  a_i, b_i = ranges[i]
  for j in range(n):
   if i == j:
    continue
   a_j, b_j = ranges[j]

   # Does range i contain range j?
   if a_i <= a_j and b_j <= b_i:
    contains[i] = 1

   # Is range i contained by range j?
   if a_j <= a_i and b_i <= b_j:
    contained[i] = 1

 return contains, contained
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Compare every pair |
| Space | O(n) | Result arrays |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check all pairs. However, with n up to 2x10^5, O(n^2) = 4x10^10 operations is far too slow.

---

## Solution 2: Optimal Solution (Sorting + Min/Max Tracking)

### Key Insight

> **The Trick:** Sort by start ascending (tie-break by end descending). Then scan left-to-right tracking max_end for "contains", and right-to-left tracking min_end for "contained by".

After sorting:
- **Contains check:** If ranges are sorted by (start ASC, end DESC), a range at position i contains a later range j if end[j] <= end[i]. Track max_end seen so far - if current end equals or exceeds all previous, it might contain others.
- **Contained check:** Scan in reverse. If a range has end >= min_end seen so far (from the right), it's contained.

### Why Sorting Works

```
Sorted by (start ASC, end DESC):
[1,6], [2,4], [3,6], [4,8]

Left-to-right (checking "contains another"):
- Track max_end_so_far
- If current range has end >= max_end of all to the right, it contains nothing
- Actually: we track min_end seen after current position

Right-to-left (checking "contained by another"):
- Track max_end_so_far from the left
- If current end <= max_end seen from left, it's contained
```

### Algorithm

1. Create indexed list: [(start, end, original_index)]
2. Sort by (start ASC, end DESC)
3. **Pass 1 (Contains):** Left to right, track max_end. If current end >= max_end, it might contain later ranges.
4. **Pass 2 (Contained):** Right to left, track min_end. If current end >= min_end seen later, it's contained by an earlier range.

### Dry Run Example

Input: `n=4, ranges=[(1,6), (2,4), (4,8), (3,6)]`

```
Step 1: Create indexed ranges
[(1, 6, 0), (2, 4, 1), (4, 8, 2), (3, 6, 3)]

Step 2: Sort by (start ASC, end DESC)
[(1, 6, 0), (2, 4, 1), (3, 6, 3), (4, 8, 2)]

Step 3: Check "contains another" (left to right)
Track max_end seen so far, compare with ends later

Position 0: (1, 6, idx=0)
  - Look at remaining ends: [4, 6, 8]
  - min_end_after = 4, our end = 6 >= 4, so contains=1 for idx 0

Position 1: (2, 4, idx=1)
  - Look at remaining ends: [6, 8]
  - min_end_after = 6, our end = 4 < 6, so contains=0 for idx 1

Position 2: (3, 6, idx=3)
  - Look at remaining ends: [8]
  - min_end_after = 8, our end = 6 < 8, so contains=0 for idx 3

Position 3: (4, 8, idx=2)
  - No more ranges after, contains=0 for idx 2

contains = [1, 0, 0, 0]

Step 4: Check "contained by another" (scan with max tracking)
Process left to right, track max_end from earlier ranges

Position 0: (1, 6, idx=0)
  - No range before, max_end_before = -inf
  - 6 <= -inf? No -> contained=0 for idx 0
  - Update max_end = 6

Position 1: (2, 4, idx=1)
  - max_end_before = 6
  - 4 <= 6? Yes -> contained=1 for idx 1
  - max_end stays 6

Position 2: (3, 6, idx=3)
  - max_end_before = 6
  - 6 <= 6? Yes -> contained=1 for idx 3
  - max_end stays 6

Position 3: (4, 8, idx=2)
  - max_end_before = 6
  - 8 <= 6? No -> contained=0 for idx 2

contained = [0, 1, 0, 1]

Final Output:
Line 1: 1 0 0 0
Line 2: 0 1 0 1
```

### Visual Diagram

```
After sorting by (start ASC, end DESC):

Index:    0       1       2       3
Start:    1       2       3       4
End:      6       4       6       8
Orig:     0       1       3       2

Timeline:
1   2   3   4   5   6   7   8
|-------|-------|-------|-------|
[=======]         Range 0: [1,6]
    [===]         Range 1: [2,4]  <-- contained by Range 0
        [=======] Range 3: [3,6]  <-- contained by Range 0
            [===========] Range 2: [4,8]

Contains check (L->R): Track if any range to the right has smaller end
Contained check (L->R): Track max_end seen, current end <= max_end means contained
```

### Code

```python
import sys
from sys import stdin

def solve():
 input = stdin.readline
 n = int(input())

 # Read ranges with original indices
 ranges = []
 for i in range(n):
  a, b = map(int, input().split())
  ranges.append((a, b, i))

 # Sort by start ASC, then end DESC
 # This ensures: if range A comes before B, then A.start <= B.start
 # If same start, longer range comes first
 ranges.sort(key=lambda x: (x[0], -x[1]))

 contains = [0] * n
 contained = [0] * n

 # Check "contains another" using suffix minimum of end values
 # If my end >= min_end of all ranges after me, I contain at least one
 min_end_suffix = [float('inf')] * (n + 1)
 for i in range(n - 1, -1, -1):
  min_end_suffix[i] = min(ranges[i][1], min_end_suffix[i + 1])

 for i in range(n):
  a, b, orig_idx = ranges[i]
  # Check if any range after has end <= my end
  # (they have start >= my start due to sorting)
  if i + 1 < n and b >= min_end_suffix[i + 1]:
   contains[orig_idx] = 1

 # Check "contained by another" using prefix maximum of end values
 # If my end <= max_end of all ranges before me, I'm contained
 max_end = float('-inf')
 for i in range(n):
  a, b, orig_idx = ranges[i]
  # Check if any range before has end >= my end
  # (they have start <= my start due to sorting)
  if b <= max_end:
   contained[orig_idx] = 1
  max_end = max(max_end, b)

 print(' '.join(map(str, contains)))
 print(' '.join(map(str, contained)))

if __name__ == "__main__":
 solve()
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sorting dominates; two linear passes |
| Space | O(n) | Arrays for ranges, results, suffix minimum |

---

## Common Mistakes

### Mistake 1: Wrong Sort Order

```python
# WRONG: Sorting by end ascending
ranges.sort(key=lambda x: (x[0], x[1]))

# CORRECT: Sort by start ASC, end DESC
ranges.sort(key=lambda x: (x[0], -x[1]))
```

**Problem:** If two ranges have the same start, the longer one should come first. With end ascending, a range [1,6] would come after [1,4], but [1,6] contains [1,4].

**Fix:** Use `-x[1]` for descending end order.

### Mistake 2: Losing Original Indices

```python
# WRONG: Sorting without tracking indices
ranges.sort()
# Now we don't know which result belongs to which input

# CORRECT: Include original index
ranges = [(a, b, i) for i, (a, b) in enumerate(input_ranges)]
ranges.sort(key=lambda x: (x[0], -x[1]))
```

**Problem:** Output must be in original input order, not sorted order.

**Fix:** Store and track original indices through sorting.

### Mistake 3: Off-by-One in Suffix Array

```python
# WRONG: Suffix array too small
min_end_suffix = [float('inf')] * n  # Missing index n

# CORRECT: Size n+1 for boundary case
min_end_suffix = [float('inf')] * (n + 1)
```

**Problem:** When checking the last element, we access `min_end_suffix[n]`.

**Fix:** Allocate n+1 elements.

### Mistake 4: Confusing Contains vs Contained

```python
# WRONG: Using max_end for "contains" check
if b >= max_end:  # This is wrong logic
 contains[orig_idx] = 1

# CORRECT: Use suffix minimum for "contains"
if b >= min_end_suffix[i + 1]:  # If my end >= smallest end after me
 contains[orig_idx] = 1
```

**Problem:** "Contains" means my end is >= some later range's end. We need the minimum end after current position.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single range | `n=1, [(1,5)]` | `0` / `0` | Nothing to contain or be contained by |
| Identical ranges | `n=2, [(1,5), (1,5)]` | `1 1` / `1 1` | Each contains and is contained by the other |
| No nesting | `n=2, [(1,3), (4,6)]` | `0 0` / `0 0` | Disjoint ranges |
| Complete nesting | `n=2, [(1,10), (2,9)]` | `1 0` / `0 1` | Outer contains inner |
| Chain nesting | `n=3, [(1,6), (2,5), (3,4)]` | `1 1 0` / `0 1 1` | Nested like Russian dolls |
| Same start | `n=2, [(1,5), (1,3)]` | `1 0` / `0 1` | Same start, different ends |
| Same end | `n=2, [(1,5), (3,5)]` | `1 0` / `0 1` | Different starts, same end |

---

## When to Use This Pattern

### Use This Approach When:
- Checking pairwise relationships between intervals
- Containment/overlap detection in sorted order
- Problems where sorting reduces comparison scope
- Need to find if any interval satisfies a condition relative to others

### Don't Use When:
- Need to count exact number of contained/containing ranges (use different tracking)
- Intervals have weighted priorities requiring different ordering
- Need to find ALL containing pairs (may need segment tree or BIT)

### Pattern Recognition Checklist:
- [ ] Interval comparison problem? -> **Consider sorting**
- [ ] Need to check relationship with "all before" or "all after"? -> **Use prefix/suffix arrays**
- [ ] Containment involves two conditions (start and end)? -> **Sort by one, track the other**
- [ ] Need to preserve original order in output? -> **Store indices during sorting**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Basic interval sorting |
| [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) | Interval overlap detection |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Nested Ranges Count](https://cses.fi/problemset/task/2169) | Count instead of check |
| [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Minimum removals for no overlap |
| [Insert Interval](https://leetcode.com/problems/insert-interval/) | Modify sorted intervals |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Rectangle Area II](https://leetcode.com/problems/rectangle-area-ii/) | 2D coordinate compression |
| [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | Sweep line with events |
| [Range Module](https://leetcode.com/problems/range-module/) | Dynamic interval tracking |

---

## Key Takeaways

1. **The Core Idea:** Sort intervals strategically so containment can be detected by tracking a single value (min or max end).

2. **Time Optimization:** From O(n^2) brute force to O(n log n) by sorting and using prefix/suffix arrays.

3. **Space Trade-off:** O(n) extra space for suffix minimum array enables single-pass containment detection.

4. **Pattern:** Sort by (start ASC, end DESC), then:
   - "Contains" = my end >= suffix minimum of ends
   - "Contained" = my end <= prefix maximum of ends

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why sorting by (start ASC, end DESC) works
- [ ] Implement the suffix minimum array technique
- [ ] Handle index tracking through sorting transformations
- [ ] Identify the difference between "contains" and "contained" logic
- [ ] Solve this problem in under 15 minutes without reference

---

## Additional Resources

- [CP-Algorithms: Sweep Line](https://cp-algorithms.com/geometry/sweep_line.html)
- [CSES Nested Ranges Check](https://cses.fi/problemset/task/2168) - Check range containment
- [Interval Scheduling Algorithms](https://en.wikipedia.org/wiki/Interval_scheduling)
