---
layout: simple
title: "Fixed Length Subarray Sum - Sliding Window Technique"
permalink: /problem_soulutions/sliding_window/fixed_length_subarray_sum_analysis
difficulty: Easy
tags: [sliding-window, array, subarray-sum]
---

# Fixed Length Subarray Sum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Sliding Window |
| **Time Limit** | 1 second |
| **Key Technique** | Fixed-Size Sliding Window |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize fixed-size sliding window problems from problem statements
- [ ] Implement the sliding window technique with O(1) window updates
- [ ] Understand when to use sliding window vs. prefix sums vs. brute force
- [ ] Apply this pattern to similar subarray problems

---

## Problem Statement

**Problem:** Given an array of integers and a fixed length k, find the maximum sum of any contiguous subarray of length k.

**Input:**
- Line 1: Two integers n (array size) and k (window size)
- Line 2: n space-separated integers

**Output:**
- Single integer: maximum sum of any contiguous subarray of length k

**Constraints:**
- 1 <= k <= n <= 10^5
- -10^4 <= arr[i] <= 10^4

### Example

```
Input:
6 3
-2 1 -3 4 -1 2

Output:
5
```

**Explanation:** The subarrays of length 3 and their sums are:
- [-2, 1, -3] = -4
- [1, -3, 4] = 2
- [-3, 4, -1] = 0
- [4, -1, 2] = 5 (maximum)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** We need to examine every window of size k. How can we avoid recalculating each window's sum from scratch?

When you slide a window of fixed size by one position, only two elements change: one leaves, one enters. This means we can update the sum in O(1) instead of recalculating in O(k).

### Breaking Down the Problem

1. **What are we looking for?** Maximum sum among all k-length subarrays
2. **What information do we have?** Array values and fixed window size k
3. **What's the relationship?** Each window shares k-1 elements with adjacent windows

### Analogies

Think of this like a train with k cars. As the train moves forward on tracks:
- One car exits at the back
- One car enters at the front
- You update the passenger count by: `new_count = old_count - exiting + entering`

---

## Solution 1: Brute Force

### Idea

Check every possible window of size k by calculating each sum independently.

### Algorithm

1. For each starting position i from 0 to n-k
2. Calculate sum of elements from index i to i+k-1
3. Track the maximum sum found

### Code

**Python:**
```python
def max_sum_brute_force(arr, k):
 """
 Brute force: calculate each window sum independently.

 Time: O(n * k)
 Space: O(1)
 """
 n = len(arr)
 max_sum = float('-inf')

 for i in range(n - k + 1):
  window_sum = sum(arr[i:i+k])
  max_sum = max(max_sum, window_sum)

 return max_sum
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * k) | n windows, each taking O(k) to sum |
| Space | O(1) | Only storing current and max sum |

### Why This Works (But Is Slow)

Correctness is guaranteed because we examine every window. However, we wastefully recalculate sums for overlapping elements. Two adjacent windows share k-1 elements, but we sum all k elements for each window.

---

## Solution 2: Optimal Sliding Window

### Key Insight

> **The Trick:** When sliding the window by one position, update the sum by subtracting the element that left and adding the element that entered. This is O(1) per window instead of O(k).

### Algorithm

1. Calculate sum of first k elements (initial window)
2. For each subsequent position:
   - Subtract the element leaving the window (arr[i-k])
   - Add the element entering the window (arr[i])
   - Update maximum if current sum is larger
3. Return maximum sum

### Dry Run Example

Let's trace through with `arr = [-2, 1, -3, 4, -1, 2], k = 3`:

```
Initial window: arr[0..2]
  window = [-2, 1, -3]
  current_sum = -2 + 1 + (-3) = -4
  max_sum = -4

Step 1: Slide to arr[1..3]
  Remove arr[0] = -2
  Add arr[3] = 4
  current_sum = -4 - (-2) + 4 = 2
  max_sum = max(-4, 2) = 2

Step 2: Slide to arr[2..4]
  Remove arr[1] = 1
  Add arr[4] = -1
  current_sum = 2 - 1 + (-1) = 0
  max_sum = max(2, 0) = 2

Step 3: Slide to arr[3..5]
  Remove arr[2] = -3
  Add arr[5] = 2
  current_sum = 0 - (-3) + 2 = 5
  max_sum = max(2, 5) = 5

Final answer: 5
```

### Visual Diagram

```
Array: [-2, 1, -3, 4, -1, 2]   k = 3
        0   1   2   3   4   5

Window 1: [###]            sum = -4
Window 2:    [###]         sum = -4 - (-2) + 4 = 2
Window 3:       [###]      sum = 2 - 1 + (-1) = 0
Window 4:          [###]   sum = 0 - (-3) + 2 = 5  <-- MAX
           ^         ^
           |         |
        leaving   entering
```

### Code

**Python:**
```python
def max_sum_sliding_window(arr, k):
 """
 Optimal sliding window solution.

 Time: O(n) - single pass
 Space: O(1) - constant extra space
 """
 n = len(arr)

 # Calculate initial window sum
 current_sum = sum(arr[:k])
 max_sum = current_sum

 # Slide the window
 for i in range(k, n):
  current_sum = current_sum - arr[i - k] + arr[i]
  max_sum = max(max_sum, current_sum)

 return max_sum

# Main program for CSES-style input
def main():
 n, k = map(int, input().split())
 arr = list(map(int, input().split()))
 print(max_sum_sliding_window(arr, k))

if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through the array |
| Space | O(1) | Only storing current sum and max sum |

---

## Common Mistakes

### Mistake 1: Wrong Loop Bounds

```python
# WRONG - goes out of bounds
for i in range(k, n + 1):  # n + 1 causes index error
 current_sum = current_sum - arr[i - k] + arr[i]

# CORRECT
for i in range(k, n):  # stops at n - 1
 current_sum = current_sum - arr[i - k] + arr[i]
```

**Problem:** Accessing arr[n] when array indices go from 0 to n-1.
**Fix:** Loop should be `range(k, n)`.

### Mistake 2: Forgetting Initial Window

```python
# WRONG - starts max_sum at 0
max_sum = 0
for i in range(k, n):
 # ...misses comparing with initial window

# CORRECT
current_sum = sum(arr[:k])
max_sum = current_sum  # Initialize with first window
```

**Problem:** If all windows have negative sums, returning 0 is wrong.
**Fix:** Initialize max_sum with the first window's sum.

**Problem:** Sum of 10^5 elements each up to 10^4 can exceed int range.
**Fix:** Use `long long` for sum variables.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k equals n | `arr=[1,2,3], k=3` | 6 | Only one window exists |
| All negative | `arr=[-5,-3,-8], k=2` | -8 | Max of all negative sums |
| All same value | `arr=[4,4,4,4], k=2` | 8 | All windows have same sum |
| k equals 1 | `arr=[3,1,4,1,5], k=1` | 5 | Reduces to finding max element |
| Single element | `arr=[7], k=1` | 7 | Single window with one element |

---

## When to Use This Pattern

### Use Fixed-Size Sliding Window When:
- Window size k is given and constant
- You need to process ALL windows of size k
- Each window computation can be updated incrementally
- Problems ask for max/min/sum over fixed-size subarrays

### Don't Use When:
- Window size varies based on conditions (use variable sliding window)
- You need random access to arbitrary ranges (use prefix sums or segment tree)
- Elements are not contiguous (different technique needed)

### Pattern Recognition Checklist:
- [ ] Fixed subarray/substring length? --> **Fixed sliding window**
- [ ] Looking for max/min/sum of fixed-size segments? --> **Fixed sliding window**
- [ ] "Contiguous subarray of length k"? --> **Fixed sliding window**
- [ ] Variable window size with condition? --> **Variable sliding window (different pattern)**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Maximum Element](https://cses.fi/problemset/task/1643) | Basic array traversal, simpler version |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Sliding Window Maximum](https://cses.fi/problemset/task/1076) | Find max (not sum) in each window, needs deque |
| [Sliding Window Median](https://cses.fi/problemset/task/1076) | Find median in each window, needs two heaps |
| [LeetCode 643: Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Same problem, find average instead |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Subarray Sums I](https://cses.fi/problemset/task/1660) | Variable window with target sum |
| [Subarray Sums II](https://cses.fi/problemset/task/1661) | Variable window with negative numbers |
| [LeetCode 239: Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Monotonic deque for max in window |

---

## Key Takeaways

1. **The Core Idea:** Update window sum incrementally by subtracting exiting element and adding entering element
2. **Time Optimization:** Reduced from O(n*k) to O(n) by avoiding redundant calculations
3. **Space Trade-off:** Achieved O(1) space - no extra arrays needed
4. **Pattern:** Fixed-size sliding window - one of the most common array techniques

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why O(n) is optimal for this problem
- [ ] Identify fixed-size sliding window patterns in new problems
- [ ] Implement in your preferred language in under 5 minutes
- [ ] Handle edge cases (k=n, k=1, all negative values)

---

## Additional Resources

- [CP-Algorithms: Sliding Window](https://cp-algorithms.com/)
- [CSES Sum of Two Values](https://cses.fi/problemset/task/1640) - Related array problem
- [Sliding Window Technique Guide](https://www.geeksforgeeks.org/window-sliding-technique/)
