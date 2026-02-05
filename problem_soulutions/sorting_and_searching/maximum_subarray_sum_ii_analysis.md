---
layout: simple
title: "Maximum Subarray Sum II - Sorting and Searching"
permalink: /problem_soulutions/sorting_and_searching/maximum_subarray_sum_ii_analysis
difficulty: Medium
tags: [prefix-sum, multiset, deque, sliding-window, monotonic-deque]
prerequisites: [maximum_subarray_sum]
---

# Maximum Subarray Sum II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **CSES Link** | [https://cses.fi/problemset/task/1644](https://cses.fi/problemset/task/1644) |
| **Key Technique** | Prefix Sums + Multiset / Monotonic Deque |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Use prefix sums to transform subarray sum problems into range queries
- [ ] Apply multiset (or monotonic deque) to efficiently find minimum in a sliding window
- [ ] Handle length-constrained subarray problems with O(n log n) complexity
- [ ] Recognize when sliding window minimum/maximum is needed

---

## Problem Statement

**Problem:** Given an array of n integers, find the maximum sum of a contiguous subarray whose length is between a and b (inclusive).

**Input:**
- Line 1: Three integers n, a, b (array size and length constraints)
- Line 2: n integers x_1, x_2, ..., x_n (array elements)

**Output:**
- Print one integer: the maximum sum of a subarray with length between a and b

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= a <= b <= n
- -10^9 <= x_i <= 10^9

### Example

```
Input:
8 1 2
-1 3 -2 5 3 -5 2 2

Output:
8
```

**Explanation:** The subarray [5, 3] has length 2 (which is between 1 and 2) and sum 8. This is the maximum possible sum for any subarray with length in range [1, 2].

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently find the maximum subarray sum when the subarray length must be in range [a, b]?

The core insight is to use **prefix sums** to convert subarray sums into differences. For a subarray from index i to j, the sum is `prefix[j+1] - prefix[i]`. To maximize this for subarrays of length in [a, b], we need to find the **minimum prefix sum** in a sliding window.

### Breaking Down the Problem

1. **What are we looking for?** Maximum value of `prefix[j] - prefix[i]` where `a <= j - i <= b`
2. **What information do we have?** Array elements and length constraints [a, b]
3. **What's the relationship?** For each position j, we need the minimum `prefix[i]` where `j - b <= i <= j - a`

### Analogies

Think of this problem like finding the best buying and selling points for a stock, but with the constraint that you must hold the stock for between `a` and `b` days. The prefix sum represents cumulative value, and you want to maximize `sell_price - buy_price` within the holding period constraint.

---

## Solution 1: Brute Force

### Idea

Try all possible subarrays with length in range [a, b] and compute their sums.

### Algorithm

1. For each starting position i from 0 to n-1
2. For each ending position j from i+a-1 to min(i+b-1, n-1)
3. Calculate sum of subarray [i, j]
4. Track the maximum sum found

### Code

```python
def solve_brute_force(n, a, b, arr):
    """
    Brute force solution - check all valid subarrays.

    Time: O(n * b) or O(n^2) worst case
    Space: O(1)
    """
    max_sum = float('-inf')

    for i in range(n):
        current_sum = 0
        for j in range(i, min(i + b, n)):
            current_sum += arr[j]
            length = j - i + 1
            if a <= length <= b:
                max_sum = max(max_sum, current_sum)

    return max_sum
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * b) | For each of n positions, check up to b lengths |
| Space | O(1) | Only tracking current sum and max |

### Why This Works (But Is Slow)

The brute force correctly enumerates all valid subarrays, guaranteeing we find the maximum. However, when b is close to n, this becomes O(n^2), which is too slow for n = 2 * 10^5.

---

## Solution 2: Optimal Solution with Prefix Sums + Multiset

### Key Insight

> **The Trick:** Transform the problem from "find max subarray sum" to "find max difference of prefix sums" where `prefix[j] - prefix[i]` is maximized with `a <= j - i <= b`.

For each ending position j, we need the minimum `prefix[i]` where i is in the valid range [j-b, j-a]. A **multiset** (balanced BST) maintains these prefix values and supports O(log n) insertion, deletion, and minimum query.

### Prefix Sum Transformation

| Original Problem | Transformed Problem |
|-----------------|---------------------|
| Sum of arr[i..j] | prefix[j+1] - prefix[i] |
| Length in [a, b] | Index difference in [a, b] |
| Find max sum | Find max(prefix[j] - min_prefix_in_window) |

### Algorithm

1. Compute prefix sums: `prefix[i] = arr[0] + arr[1] + ... + arr[i-1]`
2. Use a multiset to maintain prefix values in the valid window
3. For each position j (from a to n):
   - Add `prefix[j-a]` to the multiset (it's now in valid range)
   - If `j > b`, remove `prefix[j-b-1]` from multiset (out of range)
   - Answer for position j = `prefix[j] - min(multiset)`
4. Return the maximum answer

### Dry Run Example

Let's trace through with input `n=8, a=1, b=2, arr=[-1, 3, -2, 5, 3, -5, 2, 2]`:

```
Prefix sums: [0, -1, 2, 0, 5, 8, 3, 5, 7]
             p0  p1  p2 p3 p4 p5 p6 p7 p8

j=1: Need min prefix from [j-b, j-a] = [1-2, 1-1] = [-1, 0]
     Valid range: [0, 0], so window = {p0} = {0}
     max_sum = prefix[1] - min{0} = -1 - 0 = -1

j=2: Valid range: [0, 1], window = {p0, p1} = {0, -1}
     max_sum = max(-1, prefix[2] - min{0, -1}) = max(-1, 2 - (-1)) = 3

j=3: Valid range: [1, 2], window = {p1, p2} = {-1, 2}
     max_sum = max(3, prefix[3] - (-1)) = max(3, 0 - (-1)) = 3

j=4: Valid range: [2, 3], window = {p2, p3} = {2, 0}
     max_sum = max(3, prefix[4] - 0) = max(3, 5 - 0) = 5

j=5: Valid range: [3, 4], window = {p3, p4} = {0, 5}
     max_sum = max(5, prefix[5] - 0) = max(5, 8 - 0) = 8

j=6: Valid range: [4, 5], window = {p4, p5} = {5, 8}
     max_sum = max(8, prefix[6] - 5) = max(8, 3 - 5) = 8

j=7: Valid range: [5, 6], window = {p5, p6} = {8, 3}
     max_sum = max(8, prefix[7] - 3) = max(8, 5 - 3) = 8

j=8: Valid range: [6, 7], window = {p6, p7} = {3, 5}
     max_sum = max(8, prefix[8] - 3) = max(8, 7 - 3) = 8

Result: 8 (subarray [5, 3] at indices 3-4)
```

### Visual Diagram

```
Array:  [-1,  3, -2,  5,  3, -5,  2,  2]
Index:    0   1   2   3   4   5   6   7

Prefix: [0, -1,  2,  0,  5,  8,  3,  5,  7]
Index:   0   1   2   3   4   5   6   7   8

For j=5 (considering subarrays ending at index 4):
  Valid starting indices: 3, 4 (lengths 2, 1)

  Window of prefix values: {prefix[3], prefix[4]} = {0, 5}
  Min = 0 (at index 3)

  Sum = prefix[5] - prefix[3] = 8 - 0 = 8
  This represents arr[3] + arr[4] = 5 + 3 = 8
```

### Code (Python with sortedcontainers)

```python
from sortedcontainers import SortedList

def solve_optimal(n, a, b, arr):
    """
    Optimal solution using prefix sums + sorted container (multiset).

    Time: O(n log n) - each element inserted/removed once
    Space: O(n) - prefix array and multiset
    """
    # Build prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]

    # Multiset to track minimum prefix in valid window
    window = SortedList()
    max_sum = float('-inf')

    for j in range(a, n + 1):
        # Add prefix[j-a] to window (now in valid range)
        window.add(prefix[j - a])

        # Remove prefix[j-b-1] if out of range
        if j > b:
            window.remove(prefix[j - b - 1])

        # Current best: prefix[j] - minimum in window
        max_sum = max(max_sum, prefix[j] - window[0])

    return max_sum


# CSES submission version (using list-based approach)
import sys
from bisect import insort, bisect_left

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n, a, b = int(input_data[idx]), int(input_data[idx+1]), int(input_data[idx+2])
    idx += 3
    arr = [int(input_data[idx + i]) for i in range(n)]

    # Build prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]

    # Sorted list as multiset
    window = []
    max_sum = float('-inf')

    for j in range(a, n + 1):
        insort(window, prefix[j - a])

        if j > b:
            pos = bisect_left(window, prefix[j - b - 1])
            window.pop(pos)

        max_sum = max(max_sum, prefix[j] - window[0])

    print(max_sum)

if __name__ == "__main__":
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Each prefix value inserted and removed once, each operation O(log n) |
| Space | O(n) | Prefix array and multiset each store O(n) elements |

---

## Alternative: Monotonic Deque (O(n) Time)

For this specific problem, we can use a **monotonic deque** to achieve O(n) time complexity.

### Key Insight

> **The Trick:** Maintain a deque of indices where prefix values are strictly increasing. The front always has the minimum.

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each index added and removed from deque at most once |
| Space | O(n) | Prefix array O(n), deque at most O(b-a+1) |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** With n = 2*10^5 elements each up to 10^9, prefix sums can reach 2*10^14.
**Fix:** Always use `long long` for prefix sums.

### Mistake 2: Wrong Window Bounds

**Problem:** The valid range is [j-b, j-a], so we remove j-b-1 when j > b.
**Fix:** Carefully derive the window boundaries on paper first.

### Mistake 3: Using erase() Instead of find() in Multiset

**Problem:** `multiset::erase(value)` removes all matching elements.
**Fix:** Use `erase(find(value))` to remove exactly one occurrence.

### Mistake 4: Initializing max_sum to 0

**Problem:** If all array elements are negative, the answer will be negative.
**Fix:** Initialize to the smallest possible value.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `1 1 1, [5]` | 5 | Only one subarray possible |
| All negative | `3 1 2, [-5, -3, -1]` | -1 | Best is single element -1 |
| All same length | `4 2 2, [1, -1, 2, 3]` | 5 | Only length-2 subarrays: max is [2,3] |
| Full array valid | `3 1 3, [1, 2, 3]` | 6 | Entire array is valid |
| Large values | `2 1 2, [10^9, 10^9]` | 2*10^9 | Test overflow handling |
| Negative prefix | `3 2 3, [5, -10, 6]` | 1 | Subarray [5, -10, 6] = 1 |

---

## When to Use This Pattern

### Use This Approach When:
- Finding max/min subarray sum with **length constraints**
- Problem can be transformed to finding min/max in a **sliding window**
- Need efficient (O(n log n) or O(n)) solution for range queries

### Don't Use When:
- No length constraint (use Kadane's algorithm instead)
- Need to find ALL subarrays with certain property
- Subarray constraint is on sum, not length

### Pattern Recognition Checklist:
- [ ] Subarray sum problem? --> **Consider prefix sums**
- [ ] Length constraint [a, b]? --> **Sliding window + min/max query**
- [ ] Need minimum in window? --> **Multiset or monotonic deque**
- [ ] Need both min and max? --> **Two deques or segment tree**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Maximum Subarray Sum (CSES)](https://cses.fi/problemset/task/1643) | Basic Kadane's algorithm without length constraint |
| [Sliding Window Maximum (LeetCode 239)](https://leetcode.com/problems/sliding-window-maximum/) | Practice monotonic deque technique |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Subarray Sums I (CSES)](https://cses.fi/problemset/task/1660) | Count subarrays with target sum |
| [Subarray Sums II (CSES)](https://cses.fi/problemset/task/1661) | Count with negative numbers allowed |
| [Shortest Subarray with Sum at Least K (LeetCode 862)](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) | Minimum length with sum constraint |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Maximum Sum Circular Subarray (LeetCode 918)](https://leetcode.com/problems/maximum-sum-circular-subarray/) | Handle circular array |
| [Max Sum of Rectangle No Larger Than K (LeetCode 363)](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/) | 2D extension with constraint |

---

## Key Takeaways

1. **The Core Idea:** Transform subarray sum into prefix difference, then find min prefix in a sliding window
2. **Time Optimization:** Multiset gives O(n log n), monotonic deque gives O(n)
3. **Space Trade-off:** O(n) space for prefix sums enables O(1) sum queries
4. **Pattern:** Length-constrained subarray problems often reduce to sliding window min/max

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why prefix[j] - prefix[i] gives sum of arr[i..j-1]
- [ ] Derive the valid window range [j-b, j-a] from length constraint [a, b]
- [ ] Implement multiset solution without looking at code
- [ ] Implement monotonic deque solution for O(n) time
- [ ] Handle edge cases (negative numbers, overflow)

---

## Additional Resources

- [CP-Algorithms: Minimum Stack/Queue](https://cp-algorithms.com/data_structures/stack_queue_modification.html)
- [CSES Maximum Subarray Sum II](https://cses.fi/problemset/task/1644) - Bounded length subarray sum
- [Monotonic Deque Tutorial](https://leetcode.com/problems/sliding-window-maximum/solutions/65884/java-o-n-solution-using-deque-with-explanation/)
