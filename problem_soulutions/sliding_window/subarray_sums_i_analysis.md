---
layout: simple
title: "Subarray Sums I - Two Pointers / Sliding Window"
permalink: /problem_soulutions/sliding_window/subarray_sums_i_analysis
difficulty: Easy
tags: [two-pointers, sliding-window, prefix-sum, array]
---

# Subarray Sums I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Subarray Sums I](https://cses.fi/problemset/task/1660) |
| **Difficulty** | Easy |
| **Category** | Sliding Window / Two Pointers |
| **Time Limit** | 1 second |
| **Key Technique** | Two Pointers on Positive Array |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when two-pointer sliding window applies (positive numbers only)
- [ ] Implement the expand/shrink window pattern efficiently
- [ ] Understand why positive numbers guarantee monotonic window behavior
- [ ] Count subarrays with a target sum in O(n) time

---

## Problem Statement

**Problem:** Given an array of `n` positive integers and a target sum `x`, count the number of subarrays whose elements sum to exactly `x`.

**Input:**
- Line 1: Two integers `n` and `x` (array size and target sum)
- Line 2: `n` positive integers (the array elements)

**Output:**
- A single integer: the count of subarrays with sum equal to `x`

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= x <= 10^9
- 1 <= a[i] <= 10^9 (all elements are **positive**)

### Example

```
Input:
5 7
2 4 1 2 7

Output:
3
```

**Explanation:**
- Subarray [2, 4, 1] has sum 2 + 4 + 1 = 7
- Subarray [4, 1, 2] has sum 4 + 1 + 2 = 7
- Subarray [7] has sum 7
- Total: 3 subarrays

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** All elements are positive. What does this guarantee about subarray sums?

When all elements are positive:
- Adding an element to a window **always increases** the sum
- Removing an element from a window **always decreases** the sum
- This monotonic behavior means we never need to backtrack

### Breaking Down the Problem

1. **What are we looking for?** Count of contiguous subarrays summing to exactly `x`
2. **What information do we have?** Array of positive integers
3. **What's the key insight?** Since elements are positive, if current sum exceeds target, we must shrink the window (expanding cannot help)

### Analogy

Think of filling a bucket with water:
- Each element is a cup of water (always positive amount)
- If the bucket overflows (sum > target), you must pour some out (shrink left)
- If it's not full enough (sum < target), add more water (expand right)

---

## Solution 1: Brute Force

### Idea

Check every possible subarray and count those with sum equal to target.

### Algorithm

1. For each starting index `i`
2. For each ending index `j >= i`
3. Calculate sum of subarray [i, j]
4. If sum equals target, increment count

### Code

```python
def count_subarrays_brute(n, x, arr):
    """
    Brute force: check all subarrays.
    Time: O(n^2), Space: O(1)
    """
    count = 0
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                count += 1
            elif current_sum > x:
                break  # Optimization: sum can only increase
    return count
```

```cpp
// C++ Brute Force
long long countSubarraysBrute(int n, long long x, vector<long long>& arr) {
    long long count = 0;
    for (int i = 0; i < n; i++) {
        long long sum = 0;
        for (int j = i; j < n; j++) {
            sum += arr[j];
            if (sum == x) count++;
            else if (sum > x) break;
        }
    }
    return count;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Nested loops over array |
| Space | O(1) | Only tracking sum and count |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every subarray. However, O(n^2) is too slow for n = 2*10^5.

---

## Solution 2: Two Pointers (Optimal)

### Key Insight

> **The Trick:** Since all elements are positive, we can use a sliding window. Expand right to increase sum, shrink left to decrease sum. Each element is added and removed at most once.

### Algorithm

1. Initialize `left = 0`, `current_sum = 0`, `count = 0`
2. For each `right` from 0 to n-1:
   - Add `arr[right]` to `current_sum`
   - While `current_sum > x`: subtract `arr[left]` and increment `left`
   - If `current_sum == x`: increment `count`
3. Return `count`

### Why Two Pointers Works Here

| Property | Guaranteed By |
|----------|---------------|
| Sum increases when expanding | All elements positive |
| Sum decreases when shrinking | All elements positive |
| Never need to expand left | Monotonic sum behavior |
| Each element visited at most twice | Left pointer only moves right |

### Dry Run Example

Input: `n = 5, x = 7, arr = [2, 4, 1, 2, 7]`

```
Initial: left = 0, sum = 0, count = 0

Step 1: right = 0, add arr[0] = 2
  sum = 2
  2 < 7, no shrink
  2 != 7, no count
  Window: [2]

Step 2: right = 1, add arr[1] = 4
  sum = 6
  6 < 7, no shrink
  6 != 7, no count
  Window: [2, 4]

Step 3: right = 2, add arr[2] = 1
  sum = 7
  7 = 7, no shrink
  7 == 7, count = 1  <-- Found [2, 4, 1]
  Window: [2, 4, 1]

Step 4: right = 3, add arr[3] = 2
  sum = 9
  9 > 7, shrink: sum -= arr[0]=2, left = 1, sum = 7
  7 = 7, stop shrinking
  7 == 7, count = 2  <-- Found [4, 1, 2]
  Window: [4, 1, 2]

Step 5: right = 4, add arr[4] = 7
  sum = 14
  14 > 7, shrink: sum -= arr[1]=4, left = 2, sum = 10
  10 > 7, shrink: sum -= arr[2]=1, left = 3, sum = 9
  9 > 7, shrink: sum -= arr[3]=2, left = 4, sum = 7
  7 == 7, count = 3  <-- Found [7]
  Window: [7]

Result: count = 3
```

All three subarrays found: [2,4,1], [4,1,2], and [7], each summing to 7.

### Visual Diagram

```
arr:    [2,  4,  1,  2,  7]
index:   0   1   2   3   4

Window evolution (target = 7):

  [2]         sum=2  < 7, expand
  [2,4]       sum=6  < 7, expand
  [2,4,1]     sum=7  = 7, COUNT!
  [2,4,1,2]   sum=9  > 7, shrink
    [4,1,2]   sum=7  = 7, COUNT!
    [4,1,2,7] sum=14 > 7, shrink
      [1,2,7] sum=10 > 7, shrink
        [2,7] sum=9  > 7, shrink
          [7] sum=7  = 7, COUNT!
```

### Code

```python
def count_subarrays(n, x, arr):
    """
    Two-pointer sliding window for positive arrays.
    Time: O(n), Space: O(1)
    """
    count = 0
    current_sum = 0
    left = 0

    for right in range(n):
        current_sum += arr[right]

        # Shrink window while sum exceeds target
        while current_sum > x and left <= right:
            current_sum -= arr[left]
            left += 1

        # Check if current window matches target
        if current_sum == x:
            count += 1

    return count

# Main
if __name__ == "__main__":
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    print(count_subarrays(n, x, arr))
```

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long x;
    cin >> n >> x;

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    long long count = 0;
    long long current_sum = 0;
    int left = 0;

    for (int right = 0; right < n; right++) {
        current_sum += arr[right];

        // Shrink window while sum exceeds target
        while (current_sum > x && left <= right) {
            current_sum -= arr[left];
            left++;
        }

        // Check if current window matches target
        if (current_sum == x) {
            count++;
        }
    }

    cout << count << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element added once, removed at most once |
| Space | O(1) | Only pointers and sum variables |

---

## Common Mistakes

### Mistake 1: Forgetting the Positive Constraint

```python
# WRONG approach for arrays with negative numbers
# Two pointers does NOT work when elements can be negative!
# Use hash map approach for Subarray Sums II instead
```

**Problem:** If array has negatives, shrinking window might not decrease sum.
**Fix:** Verify constraint says "positive integers" before using two pointers.

### Mistake 2: Integer Overflow

```cpp
// WRONG
int current_sum = 0;  // Can overflow!

// CORRECT
long long current_sum = 0;  // Safe for sum up to 2*10^5 * 10^9
```

**Problem:** Sum can reach 2*10^14, exceeding `int` range.
**Fix:** Use `long long` for sum and count in C++.

### Mistake 3: Off-by-One in Window Shrinking

```python
# WRONG
while current_sum > x:
    current_sum -= arr[left]
    left += 1
# If left > right, we access invalid elements next iteration

# CORRECT
while current_sum > x and left <= right:
    current_sum -= arr[left]
    left += 1
```

**Problem:** Window can become empty, causing issues.
**Fix:** Add boundary check `left <= right`.

### Mistake 4: Not Handling Empty Result

```python
# The algorithm naturally handles no matches (returns 0)
# But ensure you don't print "IMPOSSIBLE" - just print 0
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element match | `1 5` / `5` | `1` | Subarray [5] |
| No matches | `3 100` / `1 2 3` | `0` | No subarray sums to 100 |
| All same elements | `4 6` / `2 2 2 2` | `2` | [2,2,2] appears twice |
| Entire array | `3 6` / `1 2 3` | `1` | Whole array sums to target |
| Large values | `2 2000000000` / `10^9 10^9` | `1` | Tests long long handling |
| Single element array | `1 1` / `1` | `1` | Simplest valid case |

---

## When to Use This Pattern

### Use Two Pointers / Sliding Window When:
- All array elements are **positive** (or non-negative with care)
- Looking for subarrays with exact/at-most/at-least sum
- Need O(n) time complexity
- Can tolerate O(1) extra space

### Don't Use When:
- Array contains **negative numbers** (use hash map - see Subarray Sums II)
- Need to find ALL subarrays, not just count
- Problem asks for non-contiguous subsequences

### Pattern Recognition Checklist:
- [ ] Contiguous subarray problem? --> Consider sliding window
- [ ] All positive elements? --> Two pointers works
- [ ] Target is exact sum? --> Track when sum equals target
- [ ] Elements can be negative? --> Use prefix sum + hash map instead

---

## Related Problems

### CSES Problems

| Problem | Link | Key Difference |
|---------|------|----------------|
| Subarray Sums II | [Task 1661](https://cses.fi/problemset/task/1661) | Allows negative numbers (use hash map) |
| Subarray Divisibility | [Task 1662](https://cses.fi/problemset/task/1662) | Sum divisible by n (prefix sum modulo) |
| Maximum Subarray Sum | [Task 1643](https://cses.fi/problemset/task/1643) | Find max sum (Kadane's algorithm) |

### Similar Patterns

| Problem | Platform | Technique |
|---------|----------|-----------|
| Minimum Size Subarray Sum | LeetCode 209 | Two pointers, find min length |
| Subarray Product Less Than K | LeetCode 713 | Two pointers with product |
| Longest Substring Without Repeating | LeetCode 3 | Sliding window with set |

---

## Key Takeaways

1. **The Core Idea:** Positive elements guarantee monotonic sum behavior, enabling O(n) two-pointer solution
2. **Time Optimization:** From O(n^2) brute force to O(n) sliding window
3. **Space Trade-off:** No extra space needed beyond pointers
4. **Critical Check:** This technique ONLY works for positive arrays - verify constraints!

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why two pointers works for positive arrays but not negative
- [ ] Trace through the algorithm on paper without code
- [ ] Implement the solution from scratch in under 10 minutes
- [ ] Identify this pattern when seeing similar problems
- [ ] Know when to use hash map approach instead (Subarray Sums II)
