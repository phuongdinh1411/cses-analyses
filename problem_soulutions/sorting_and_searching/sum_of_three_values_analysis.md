---
layout: simple
title: "Sum of Three Values - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/sum_of_three_values_analysis
difficulty: Medium
tags: [two-pointers, sorting, three-sum, hash-map]
prerequisites: [sum_of_two_values]
---

# Sum of Three Values

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Sorting + Two Pointers |
| **CSES Link** | [Sum of Three Values](https://cses.fi/problemset/task/1641) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the classic 3Sum pattern using sorting and two pointers
- [ ] Preserve original indices when sorting is required for the algorithm
- [ ] Reduce an O(n^3) brute force to O(n^2) using two-pointer technique
- [ ] Handle edge cases like duplicate values and no valid solution

---

## Problem Statement

**Problem:** Given an array of n integers and a target sum x, find three distinct elements whose values sum to exactly x. Return their 1-indexed positions.

**Input:**
- Line 1: Two integers n (array size) and x (target sum)
- Line 2: n integers representing array elements

**Output:**
- Three 1-indexed positions of elements that sum to x
- Print "IMPOSSIBLE" if no such triplet exists

**Constraints:**
- 1 <= n <= 5000
- 1 <= x <= 10^9
- 1 <= a[i] <= 10^9

### Example

```
Input:
4 8
2 7 5 1

Output:
1 3 4
```

**Explanation:** Elements at positions 1, 3, 4 are 2, 5, 1. Their sum is 2 + 5 + 1 = 8.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently find three numbers that sum to a target?

This is the classic **3Sum problem**. The key insight is to reduce it to multiple 2Sum problems: fix one element, then find two elements in the remaining array that sum to `target - fixed_element`.

### Breaking Down the Problem

1. **What are we looking for?** Three distinct indices i, j, k where arr[i] + arr[j] + arr[k] = target
2. **What information do we have?** Array values and target sum
3. **What's the relationship?** For each element as "first", we need a pair summing to `target - first`

### The Core Insight

After sorting, for any fixed first element, we can use **two pointers** (one at start, one at end of remaining array) to efficiently find pairs. If the sum is too small, move left pointer right. If too large, move right pointer left.

**Critical:** Since we sort the array but need original indices, we must store `(value, original_index)` pairs.

---

## Solution 1: Brute Force

### Idea

Check all possible triplets using three nested loops.

### Code

```python
def solve_brute_force(n, arr, target):
  """
  Check all triplets - O(n^3) time.
  """
  for i in range(n):
    for j in range(i + 1, n):
      for k in range(j + 1, n):
        if arr[i] + arr[j] + arr[k] == target:
          return (i + 1, j + 1, k + 1)  # 1-indexed
  return None
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | Three nested loops |
| Space | O(1) | No extra space |

**Why it's slow:** With n = 5000, this requires 5000^3 = 125 billion operations - way too slow.

---

## Solution 2: Optimal - Sorting + Two Pointers

### Key Insight

> **The Trick:** Sort the array, fix each element as the "first" of the triplet, then use two pointers to find the other two elements in O(n) time.

### Algorithm

1. Create pairs of `(value, original_index)` and sort by value
2. For each element at position i (first element of triplet):
   - Set `left = i + 1`, `right = n - 1`
   - While `left < right`:
     - Calculate `sum = arr[i] + arr[left] + arr[right]`
     - If sum equals target: return the three original indices
     - If sum < target: move left pointer right (need larger sum)
     - If sum > target: move right pointer left (need smaller sum)
3. If no triplet found, return "IMPOSSIBLE"

### Dry Run Example

Let's trace through with `arr = [2, 7, 5, 1]`, `target = 8`:

```
Step 1: Create indexed array and sort
  Original:     [(2,0), (7,1), (5,2), (1,3)]
  After sort:   [(1,3), (2,0), (5,2), (7,1)]
                  ^      ^      ^      ^
                 idx0   idx1   idx2   idx3

Step 2: Fix first element at index 0 (value=1, original_pos=3)
  Need remaining two to sum to: 8 - 1 = 7
  left = 1 (value=2), right = 3 (value=7)

  Iteration 1:
    sum = 1 + 2 + 7 = 10 > 8
    Move right pointer left: right = 2

  Iteration 2:
    sum = 1 + 2 + 5 = 8 = target!
    Found! Original indices: 3+1, 0+1, 2+1 = 4, 1, 3
    Output (sorted): 1 3 4
```

### Visual Diagram

```
Sorted array: [1, 2, 5, 7]
Original idx:  3  0  2  1

Fix first = 1 (original idx 3), need pair summing to 7:

    [1]  [2  5  7]
     ^    ^     ^
   fixed left  right
         sum = 2+7 = 9 > 7, move right

    [1]  [2  5]  7
     ^    ^  ^
   fixed L  R
         sum = 2+5 = 7 = target! Found!
```

### Code (Python)

```python
def solve(n, arr, target):
  """
  Optimal solution using sorting + two pointers.

  Time: O(n^2) - sort is O(n log n), two-pointer search is O(n^2)
  Space: O(n) - for storing indexed array
  """
  # Store (value, original_index) pairs
  indexed = [(arr[i], i) for i in range(n)]
  indexed.sort()  # Sort by value

  for i in range(n - 2):
    first_val = indexed[i][0]
    remaining = target - first_val

    left = i + 1
    right = n - 1

    while left < right:
      current_sum = indexed[left][0] + indexed[right][0]

      if current_sum == remaining:
        # Found triplet - get original 1-indexed positions
        positions = [
          indexed[i][1] + 1,
          indexed[left][1] + 1,
          indexed[right][1] + 1
        ]
        positions.sort()
        return positions
      elif current_sum < remaining:
        left += 1
      else:
        right -= 1

  return None


def main():
  n, target = map(int, input().split())
  arr = list(map(int, input().split()))

  result = solve(n, arr, target)

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
| Time | O(n^2) | O(n log n) sort + O(n^2) two-pointer search |
| Space | O(n) | Storing indexed array |

---

## Common Mistakes

### Mistake 1: Forgetting to Preserve Original Indices

```python
# WRONG - loses original positions after sorting
arr.sort()
# Now we can't report correct original indices!
```

**Problem:** The problem asks for original positions, but sorting destroys index information.
**Fix:** Store `(value, original_index)` pairs before sorting.

### Mistake 2: Using Same Element Twice

```python
# WRONG - may use same index twice
for i in range(n):
  left = 0  # Should start at i + 1
  right = n - 1
```

**Problem:** The left pointer might include index i, using the same element twice.
**Fix:** Start `left = i + 1` to ensure all three indices are distinct.

### Mistake 3: Integer Overflow

**Problem:** Three values each up to 10^9 can sum to 3*10^9, exceeding int range.
**Fix:** Use `long long` for sums in C++.

### Mistake 4: 0-indexed vs 1-indexed Output

```python
# WRONG
return (i, left, right)  # 0-indexed

# CORRECT
return (i + 1, left + 1, right + 1)  # 1-indexed as required
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No solution exists | `[1,2,3], target=100` | IMPOSSIBLE | No triplet sums to 100 |
| Minimum array size | `[1,2,5], target=8` | `1 2 3` | Exactly 3 elements |
| All same values | `[4,4,4], target=12` | `1 2 3` | Duplicate values allowed |
| Large values | `[10^9, 10^9, 1], target=2*10^9+1` | `1 2 3` | Handle overflow correctly |
| First triplet is answer | `[1,2,5,100], target=8` | `1 2 3` | Found immediately |

---

## When to Use This Pattern

### Use Sorting + Two Pointers When:
- Finding triplets/pairs with a target sum
- Array is unsorted but order of output indices doesn't need to match input order
- O(n^2) is acceptable (n <= 10^4 typically)

### Don't Use When:
- You need ALL triplets (need to handle duplicates carefully)
- Array is already sorted (skip the sort step)
- n is too large for O(n^2) - need more advanced techniques

### Pattern Recognition Checklist:
- [ ] Finding k numbers that sum to target? Start with sorting + two pointers
- [ ] Need original indices after sorting? Store (value, index) pairs
- [ ] Similar to 2Sum? Fix one element, reduce to 2Sum

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Sum of Two Values (CSES)](https://cses.fi/problemset/task/1640) | Same pattern, simpler case |
| [Two Sum (LeetCode)](https://leetcode.com/problems/two-sum/) | Classic hash map approach |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [3Sum (LeetCode)](https://leetcode.com/problems/3sum/) | Find ALL unique triplets summing to 0 |
| [3Sum Closest (LeetCode)](https://leetcode.com/problems/3sum-closest/) | Find triplet closest to target |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Sum of Four Values (CSES)](https://cses.fi/problemset/task/1642) | Extended to 4 elements |
| [4Sum (LeetCode)](https://leetcode.com/problems/4sum/) | Generalized k-sum |

---

## Key Takeaways

1. **The Core Idea:** Reduce 3Sum to multiple 2Sum problems by fixing one element
2. **Time Optimization:** From O(n^3) brute force to O(n^2) using sorting + two pointers
3. **Space Trade-off:** O(n) space to store original indices
4. **Pattern:** This is a foundational technique for k-sum problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement the solution without looking at code
- [ ] Explain why sorting enables the two-pointer technique
- [ ] Handle the index tracking correctly
- [ ] Identify when this pattern applies to new problems
