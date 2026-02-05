---
layout: simple
title: "Collecting Numbers II - Dynamic Round Counting with Swap Queries"
permalink: /problem_soulutions/sorting_and_searching/collecting_numbers_ii_analysis
difficulty: Medium
tags: [position-tracking, delta-calculation, swap-queries, greedy]
prerequisites: [collecting_numbers]
---

# Collecting Numbers II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Position Tracking + Delta Calculation |
| **CSES Link** | [https://cses.fi/problemset/task/2217](https://cses.fi/problemset/task/2217) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how to maintain dynamic answers under swap operations
- [ ] Calculate delta changes efficiently instead of recomputing from scratch
- [ ] Identify when position(x) > position(x-1) creates a "break" requiring new rounds
- [ ] Handle adjacent vs non-adjacent element swaps correctly

---

## Problem Statement

**Problem:** This is an extension of Collecting Numbers. You have an array containing numbers 1 to n, and you need to collect them in increasing order. In each round, you go through the array left to right and collect as many numbers as possible.

Now, there are m swap operations. After each swap, report the minimum number of rounds needed.

**Input:**
- Line 1: Two integers n and m (array size and number of swaps)
- Line 2: n integers representing the permutation of 1 to n
- Lines 3 to m+2: Two integers a and b (positions to swap, 1-indexed)

**Output:**
- Print m lines: after each swap, the number of rounds needed

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= m <= 2 x 10^5
- 1 <= a, b <= n

### Example

```
Input:
5 3
4 2 1 5 3
2 3
1 5
2 3

Output:
2
3
4
```

**Explanation:**

Initial array [4, 2, 1, 5, 3] has positions: pos[1]=2, pos[2]=1, pos[3]=4, pos[4]=0, pos[5]=3.
Breaks occur at (1,2) and (3,4) where pos[x] > pos[x+1]. Initial rounds = 1 + 2 = 3.

After swap(2,3): Array becomes [4, 1, 2, 5, 3]. The break at (1,2) is removed. Rounds = 2.

After swap(1,5): Array becomes [3, 1, 2, 5, 4]. New break at (4,5) added. Rounds = 3.

After swap(2,3): Array becomes [3, 2, 1, 5, 4]. Breaks at (1,2), (2,3), (4,5). Rounds = 4.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How does swapping two elements affect the round count?

The round count equals 1 + (number of "breaks"). A break occurs when position(x) > position(x+1) for consecutive values. When we swap elements at positions a and b, we only need to check the breaks involving those two values and their neighbors.

### Breaking Down the Problem

1. **What are we looking for?** The number of rounds after each swap
2. **What information do we have?** Position of each value, which values are being swapped
3. **What's the relationship between input and output?** Rounds = 1 + count of breaks where pos[x] > pos[x+1]

### The Core Insight

Instead of recalculating rounds from scratch (O(n) per query), we can:
1. Before the swap: count breaks involving the swapped values
2. After the swap: count breaks involving the same values
3. Update: rounds += (new_breaks - old_breaks)

This gives us O(1) per query after O(n) preprocessing.

---

## Solution: Delta Calculation

### Key Insight

> **The Trick:** A swap at positions a and b only affects breaks involving values arr[a], arr[b], and their neighbors (arr[a]-1, arr[a]+1, arr[b]-1, arr[b]+1).

### What is a "Break"?

For consecutive values x and x+1:
- If pos[x] < pos[x+1]: NO break (can collect both in same round)
- If pos[x] > pos[x+1]: BREAK (need separate rounds)

### Algorithm

1. Initialize: Calculate initial round count
2. For each swap(a, b):
   - Let valA = arr[a], valB = arr[b]
   - Remove breaks involving valA-1, valA, valA+1, valB-1, valB, valB+1
   - Perform the swap (update arr and pos)
   - Add back breaks for the same values
   - Output current round count

### Dry Run Example

Input: `n=5, arr=[4,2,1,5,3]`, swap(2,3)

```
Initial: arr=[4,2,1,5,3], pos=[_,2,1,4,0,3]
         Breaks: (1,2) since pos[1]=2 > pos[2]=1
                 (3,4) since pos[3]=4 > pos[4]=0
         Initial rounds = 1 + 2 = 3

Swap positions 2,3 (indices 1,2): valA=2, valB=1
  Affected pairs: {1} (checking break between values 1 and 2)

  BEFORE: pos[1]=2 > pos[2]=1 -> 1 break
  SWAP:   arr=[4,1,2,5,3], pos[1]=1, pos[2]=2
  AFTER:  pos[1]=1 < pos[2]=2 -> 0 breaks

  Delta = 0 - 1 = -1
  rounds = 3 - 1 = 2  -> Output: 2
```

### Visual Diagram

```
Before swap:                      After swap:
Index:  0   1   2   3   4         Index:  0   1   2   3   4
Array: [4] [2] [1] [5] [3]        Array: [4] [1] [2] [5] [3]
            ^   ^                             ^   ^
Value:  1   2   3   4   5         Value:  1   2   3   4   5
Pos:    2   1   4   0   3         Pos:    1   2   4   0   3
       [2>1]   [4>0]                     [1<2]   [4>0]
       break   break                   no break  break
```

### Code

**Python Solution:**

```python
def solve():
  import sys
  input = sys.stdin.readline

  n, m = map(int, input().split())
  arr = list(map(int, input().split()))

  # pos[value] = index (0-indexed)
  pos = [0] * (n + 2)  # Extra space to avoid boundary checks
  for i in range(n):
    pos[arr[i]] = i

  def is_break(x):
    """Check if there's a break between value x and x+1."""
    if x < 1 or x >= n:
      return 0
    return 1 if pos[x] > pos[x + 1] else 0

  # Calculate initial rounds
  rounds = 1
  for x in range(1, n):
    rounds += is_break(x)

  results = []

  for _ in range(m):
    a, b = map(int, input().split())
    a -= 1  # Convert to 0-indexed
    b -= 1

    if a > b:
      a, b = b, a

    valA = arr[a]
    valB = arr[b]

    # Values whose break status might change
    affected = set()
    for v in [valA - 1, valA, valB - 1, valB]:
      if 1 <= v < n:
        affected.add(v)

    # Remove old breaks
    for v in affected:
      rounds -= is_break(v)

    # Perform swap
    arr[a], arr[b] = arr[b], arr[a]
    pos[valA] = b
    pos[valB] = a

    # Add new breaks
    for v in affected:
      rounds += is_break(v)

    results.append(rounds)

  print('\n'.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | O(n) init + O(1) per query |
| Space | O(n) | Position array |

---

## Common Mistakes

### Mistake 1: Checking Wrong Break Points

```python
# WRONG: Only checking the swapped values
affected = {valA, valB}

# CORRECT: Check pairs involving swapped values AND their neighbors
affected = {valA - 1, valA, valB - 1, valB}
```

**Problem:** A break is between consecutive VALUES (x, x+1). If we swap value 3, we need to check breaks (2,3) and (3,4).

**Fix:** Always check valA-1, valA, valB-1, valB as potential break points.

### Mistake 2: Not Handling Adjacent Swaps

```python
# WRONG: Treating adjacent and non-adjacent swaps the same way without deduplication
# If valA and valB are consecutive (e.g., valA=2, valB=3), we might double-count

# CORRECT: Use a set to deduplicate affected break points
affected = set()
for v in [valA - 1, valA, valB - 1, valB]:
  if 1 <= v < n:
    affected.add(v)
```

**Problem:** When swapped values are consecutive (like 2 and 3), valA and valB-1 might be the same.

**Fix:** Use a set to automatically handle deduplication.

### Mistake 3: Forgetting to Update Position Array

```python
# WRONG: Only swapping array, forgetting position array
arr[a], arr[b] = arr[b], arr[a]
# pos array is now stale!

# CORRECT: Update both
arr[a], arr[b] = arr[b], arr[a]
pos[valA] = b  # valA is now at position b
pos[valB] = a  # valB is now at position a
```

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Already sorted | `[1,2,3,4,5]` | 1 round initially | No breaks exist |
| Reverse sorted | `[5,4,3,2,1]` | n rounds initially | Maximum breaks |
| Swap same position | `swap(i, i)` | No change | Handle gracefully |
| Adjacent values swapped | Values 3,4 swapped | Check breaks (2,3), (3,4), (4,5) | 3 pairs affected |
| First/last value | Swap involving value 1 or n | Fewer boundary pairs | No pair (0,1) or (n,n+1) |
| Single element | n=1, no swaps | Always 1 round | Trivial case |

---

## When to Use This Pattern

Use delta calculation when:
- The answer is a sum of local contributions (consecutive pairs, neighbors)
- Updates affect only a constant number of terms
- There are many queries (m queries) requiring better than O(m*n)

Pattern indicators:
- [ ] Sum of local relationships? -> Consider delta updates
- [ ] Updates affect O(1) terms? -> O(1) per query possible

---

## Related Problems

### Prerequisite

| Problem | Why It Helps |
|---------|--------------|
| [Collecting Numbers](https://cses.fi/problemset/task/2216) | Base problem - understand round counting |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [List Removals](https://cses.fi/problemset/task/1749) | Dynamic array with queries |
| [Distinct Values Queries](https://cses.fi/problemset/task/1734) | Different query type on arrays |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Subarray Sum Queries](https://cses.fi/problemset/task/1190) | Segment tree for range queries |
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | More complex delta tracking |

### LeetCode Related

| Problem | Connection |
|---------|------------|
| [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | Position-based analysis |
| [Count Inversions](concept) | Similar break-counting idea |

---

## Key Takeaways

1. **The Core Idea:** Rounds = 1 + breaks, where a break occurs when pos[x] > pos[x+1]
2. **Time Optimization:** Track delta changes (O(1) per swap) instead of recalculating (O(n) per swap)
3. **Space Trade-off:** Maintain position array for O(1) lookup of any value's position
4. **Pattern:** Local update with constant affected terms -> Delta calculation

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve Collecting Numbers (the base problem) first
- [ ] Explain why rounds = 1 + number of breaks
- [ ] Identify which break points are affected by a swap
- [ ] Implement in your preferred language in under 15 minutes
