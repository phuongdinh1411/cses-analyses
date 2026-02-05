---
layout: simple
title: "Sum of Four Values - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/sum_of_four_values_analysis
difficulty: Medium
tags: [two-pointers, sorting, k-sum, hash-map]
prerequisites: [sum_of_two_values, sum_of_three_values]
---

# Sum of Four Values

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Sum of Four Values](https://cses.fi/problemset/task/1642) |
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Sorting + Two Pointers (Reduce 4Sum to 3Sum to 2Sum) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the k-Sum problem reduction pattern (4Sum -> 3Sum -> 2Sum)
- [ ] Apply sorting with index preservation for problems requiring original indices
- [ ] Implement the two-pointer technique for finding pairs with a target sum
- [ ] Handle duplicate values while maintaining distinct index requirements

---

## Problem Statement

**Problem:** Given an array of n integers and a target sum x, find four distinct indices i, j, k, l such that arr[i] + arr[j] + arr[k] + arr[l] = x.

**Input:**
- Line 1: Two integers n (array size) and x (target sum)
- Line 2: n integers representing the array elements

**Output:**
- Four distinct indices (1-indexed) whose values sum to x
- Print "IMPOSSIBLE" if no such quadruplet exists

**Constraints:**
- 4 <= n <= 1000
- 1 <= x <= 10^9
- 1 <= arr[i] <= 10^9

### Example

```
Input:
8 15
2 7 5 1 9 3 8 4

Output:
1 2 3 4
```

**Explanation:** arr[1] + arr[2] + arr[3] + arr[4] = 2 + 7 + 5 + 1 = 15 (using 1-indexed values)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently find 4 numbers that sum to a target?

The classic k-Sum pattern: **Reduce the problem dimension by fixing elements one at a time.**
- 4Sum becomes 3Sum by fixing one element
- 3Sum becomes 2Sum by fixing another element
- 2Sum is solved efficiently with two pointers on a sorted array

### Breaking Down the Problem

1. **What are we looking for?** Four distinct indices whose values sum to the target.
2. **What information do we have?** An unsorted array and a target sum.
3. **What's the key insight?** After sorting, we can use two pointers to find pairs that sum to a specific value in O(n) time.

### Analogies

Think of this like finding four people whose ages add up to a specific number. Instead of checking every possible group of 4 (expensive), you:
1. Pick person A
2. Pick person B
3. For the remaining people (sorted by age), use two pointers from both ends to find a pair that completes the sum

---

## Solution 1: Brute Force

### Idea

Try all possible combinations of 4 distinct indices and check if their sum equals the target.

### Algorithm

1. Use four nested loops for indices i < j < k < l
2. Check if arr[i] + arr[j] + arr[k] + arr[l] == target
3. Return the first valid quadruplet found

### Code

```python
def solve_brute_force(n, arr, target):
  """
  Brute force: Try all combinations of 4 elements.

  Time: O(n^4)
  Space: O(1)
  """
  for i in range(n):
    for j in range(i + 1, n):
      for k in range(j + 1, n):
        for l in range(k + 1, n):
          if arr[i] + arr[j] + arr[k] + arr[l] == target:
            return [i + 1, j + 1, k + 1, l + 1]  # 1-indexed
  return None
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^4) | Four nested loops over n elements |
| Space | O(1) | No extra data structures |

### Why This Works (But Is Slow)

This guarantees finding a solution if one exists by checking every possibility. However, with n = 1000, we have roughly 10^12 operations - far too slow for the 1-second time limit.

---

## Solution 2: Optimal - Sorting + Two Pointers

### Key Insight

> **The Trick:** Fix the first two elements with nested loops O(n^2), then use two pointers to find the remaining pair in O(n). Total: O(n^3).

**Critical Detail:** We must preserve original indices since the problem asks for positions, not values.

### Algorithm

1. Create pairs of (value, original_index) and sort by value
2. Fix element i (first loop)
3. Fix element j > i (second loop)
4. Use two pointers (left, right) for the remaining portion
5. When a valid sum is found, verify all 4 indices are distinct

### Dry Run Example

Let's trace through with `arr = [2, 7, 5, 1, 9, 3, 8, 4], target = 15`:

```
Step 1: Create indexed array and sort by value
  Original: [(2,0), (7,1), (5,2), (1,3), (9,4), (3,5), (8,6), (4,7)]
  Sorted:   [(1,3), (2,0), (3,5), (4,7), (5,2), (7,1), (8,6), (9,4)]
            val: 1    2    3    4    5    7    8    9
            idx: 3    0    5    7    2    1    6    4

Step 2: Fix i=0, j=1 (values 1, 2)
  Need: 15 - 1 - 2 = 12
  left=2 (val=3), right=7 (val=9)

  3 + 9 = 12  --> Found!
  Indices: [3, 0, 5, 4] -> All distinct
  Sort and convert to 1-indexed: [1, 4, 5, 6]

Output: 1 4 5 6 (or any valid quadruplet)
```

### Visual Diagram

```
Sorted array (by value):
  Index:  0    1    2    3    4    5    6    7
  Value:  1    2    3    4    5    7    8    9
  Orig:   3    0    5    7    2    1    6    4

For i=0, j=1 (values 1+2=3), need remaining sum = 12:

         i    j    left                    right
         v    v    v                         v
  Value: 1    2    3    4    5    7    8    9
                   |__________________________|
                        Two pointer search

  left + right = 3 + 9 = 12  --> Match!
```

### Code

**Python Solution:**

```python
import sys
from typing import List, Optional

def solve(n: int, arr: List[int], target: int) -> Optional[List[int]]:
  """
  Find four distinct indices whose values sum to target.

  Time: O(n^3) - Two nested loops + two-pointer search
  Space: O(n) - For the indexed array
  """
  # Create (value, original_index) pairs and sort by value
  indexed = [(arr[i], i) for i in range(n)]
  indexed.sort()

  # Fix first two elements
  for i in range(n - 3):
    for j in range(i + 1, n - 2):
      remaining = target - indexed[i][0] - indexed[j][0]

      # Two pointers for the remaining sum
      left = j + 1
      right = n - 1

      while left < right:
        current_sum = indexed[left][0] + indexed[right][0]

        if current_sum == remaining:
          # Collect original indices
          indices = [
            indexed[i][1],
            indexed[j][1],
            indexed[left][1],
            indexed[right][1]
          ]
          # Convert to 1-indexed and sort for consistent output
          return sorted([idx + 1 for idx in indices])
        elif current_sum < remaining:
          left += 1
        else:
          right -= 1

  return None

def main():
  input_data = sys.stdin.read().split()
  n = int(input_data[0])
  x = int(input_data[1])
  arr = list(map(int, input_data[2:2+n]))

  result = solve(n, arr, x)
  if result:
    print(*result)
  else:
    print("IMPOSSIBLE")

if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | O(n^2) for fixing i,j + O(n) two-pointer search |
| Space | O(n) | Storing indexed pairs for sorting |

---

## Common Mistakes

### Mistake 1: Losing Original Indices After Sorting

```python
# WRONG - Sorts values but loses original positions
arr.sort()
# Now we cannot report the original indices!
```

**Problem:** The problem requires original indices, but sorting destroys position information.
**Fix:** Store (value, index) pairs before sorting.

```python
# CORRECT
indexed = [(arr[i], i) for i in range(n)]
indexed.sort()  # Preserves original index in tuple
```

### Mistake 2: Duplicate Index in Result

```python
# WRONG - May return same index twice for duplicates
if indexed[i][0] + indexed[j][0] + indexed[left][0] + indexed[right][0] == target:
  return [i, j, left, right]  # These are sorted positions, not original!
```

**Problem:** Using sorted positions instead of original indices.
**Fix:** Always extract the original index from the tuple.

```python
# CORRECT
indices = [indexed[i][1], indexed[j][1], indexed[left][1], indexed[right][1]]
```

### Mistake 3: Starting Two Pointers from Wrong Position

```python
# WRONG - May reuse elements i or j
left = 0
right = n - 1
```

**Problem:** Two pointers might select the same element already used by i or j.
**Fix:** Start left pointer after j.

```python
# CORRECT - Start after the fixed elements
left = j + 1
right = n - 1
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No solution exists | `4 100`, `[1,2,3,4]` | IMPOSSIBLE | Max sum = 10, target = 100 |
| Exact four elements | `4 10`, `[1,2,3,4]` | `1 2 3 4` | Only one possible combination |
| All same values | `5 20`, `[5,5,5,5,5]` | `1 2 3 4` | Any four indices work |
| Large values | `4 4000000000`, `[10^9,10^9,10^9,10^9]` | `1 2 3 4` | Handle large sums (use long long) |
| Multiple solutions | `6 10`, `[1,2,3,4,5,6]` | Any valid quad | Output any one solution |

---

## When to Use This Pattern

### Use This Approach When:
- Finding k numbers (k >= 3) that sum to a target
- Array is unsorted and you need O(n^(k-1)) complexity
- You need to report indices, not just values

### Don't Use When:
- k = 2 (simple hash map is O(n))
- You need ALL quadruplets (requires more complex handling)
- Array has special structure (e.g., already sorted)

### Pattern Recognition Checklist:
- [ ] Looking for k numbers summing to target? --> **k-Sum pattern**
- [ ] k >= 3? --> **Sort + fix (k-2) elements + two pointers**
- [ ] Need original indices? --> **Store (value, index) pairs**
- [ ] Large values? --> **Use long long in C++**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Two Sum (LeetCode)](https://leetcode.com/problems/two-sum/) | Basic complement search with hash map |
| [Sum of Two Values (CSES)](https://cses.fi/problemset/task/1640) | Two-pointer technique on sorted array |
| [Sum of Three Values (CSES)](https://cses.fi/problemset/task/1641) | Direct prerequisite - 3Sum pattern |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [3Sum (LeetCode)](https://leetcode.com/problems/3sum/) | Return values, handle duplicates |
| [3Sum Closest (LeetCode)](https://leetcode.com/problems/3sum-closest/) | Find closest sum, not exact |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [4Sum (LeetCode)](https://leetcode.com/problems/4sum/) | Return all unique quadruplets |
| [4Sum II (LeetCode)](https://leetcode.com/problems/4sum-ii/) | Four separate arrays, count pairs |
| [kSum (Generalized)](https://leetcode.com/problems/4sum/) | Recursive k-Sum reduction |

---

## Key Takeaways

1. **The Core Idea:** Reduce 4Sum to 2Sum by fixing two elements, then use two pointers.
2. **Time Optimization:** From O(n^4) brute force to O(n^3) with two pointers.
3. **Space Trade-off:** O(n) space to preserve original indices during sorting.
4. **Pattern:** This is the classic k-Sum pattern - extendable to any k.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why we need to preserve indices when sorting
- [ ] Implement the two-pointer technique correctly
- [ ] Identify k-Sum problems in new contexts
- [ ] Handle edge cases (no solution, overflow, duplicates)

---

## Additional Resources

- [LeetCode - 4Sum Editorial](https://leetcode.com/problems/4sum/editorial/)
- [CP-Algorithms: Two Pointers](https://cp-algorithms.com/others/two_pointers.html)
- [CSES Sum of Four Values](https://cses.fi/problemset/task/1642) - Find 4 elements summing to target
