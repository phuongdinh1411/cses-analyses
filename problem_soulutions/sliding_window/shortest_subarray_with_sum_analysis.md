---
layout: simple
title: "Shortest Subarray with Sum - Sliding Window"
permalink: /problem_soulutions/sliding_window/shortest_subarray_with_sum_analysis
difficulty: Medium
tags: [sliding-window, two-pointers, subarray]
---

# Shortest Subarray with Sum at Least Target

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window / Two Pointers |
| **Time Limit** | 1 second |
| **Key Technique** | Two Pointers with Variable Window |
| **Similar To** | [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Identify when to use the sliding window technique for minimum length problems
- [ ] Implement the two-pointer approach for variable-size windows
- [ ] Understand when to expand vs. contract a sliding window
- [ ] Recognize the key condition: all elements must be positive for this approach

---

## Problem Statement

**Problem:** Given an array of positive integers and a target sum, find the length of the shortest contiguous subarray whose sum is at least the target value. If no such subarray exists, return 0.

**Input:**
- Line 1: Two integers n (array size) and target (minimum required sum)
- Line 2: n positive integers separated by spaces

**Output:**
- Single integer: length of shortest valid subarray, or 0 if none exists

**Constraints:**
- 1 <= n <= 10^5
- 1 <= arr[i] <= 10^4
- 1 <= target <= 10^9

### Example

```
Input:
6 7
2 3 1 2 4 3

Output:
2
```

**Explanation:** The subarray [4, 3] has sum = 7 and length = 2. While other subarrays like [2,3,1,2] (sum=8) also satisfy the condition, [4,3] is the shortest.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When looking for a minimum-length subarray with a sum constraint, what approach works best?

When all elements are **positive**, adding more elements only increases the sum. This monotonic property allows us to use a **sliding window** that expands when we need more sum and contracts when we have enough.

### Breaking Down the Problem

1. **What are we looking for?** The shortest contiguous subarray with sum >= target
2. **What information do we have?** Array of positive integers and a target sum
3. **What's the key insight?** With positive numbers, if window sum is too small, we must expand; if sum is large enough, we can try contracting

### Analogy

Think of filling a bucket with water from a tap. You keep adding water (expanding right) until you have enough. Then you try draining some water (contracting left) to see if you can still meet your minimum requirement with a smaller bucket.

---

## Solution 1: Brute Force

### Idea

Check every possible subarray, calculate its sum, and track the minimum length among valid subarrays.

### Algorithm

1. For each starting index i from 0 to n-1
2. For each ending index j from i to n-1
3. Calculate sum of arr[i..j]
4. If sum >= target, update minimum length

### Code

```python
def solve_brute_force(arr, target):
  """
  Brute force: check all subarrays.

  Time: O(n^2) with running sum optimization
  Space: O(1)
  """
  n = len(arr)
  min_len = float('inf')

  for i in range(n):
    curr_sum = 0
    for j in range(i, n):
      curr_sum += arr[j]
      if curr_sum >= target:
        min_len = min(min_len, j - i + 1)
        break  # No need to extend further from this start

  return min_len if min_len != float('inf') else 0
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Worst case: nested loops when no valid subarray exists |
| Space | O(1) | Only tracking running sum and minimum length |

### Why This Works (But Is Slow)

The brute force correctly finds all valid subarrays by exhaustive search. The early break optimization helps when valid subarrays exist, but worst case remains O(n^2).

---

## Solution 2: Optimal - Two Pointers (Sliding Window)

### Key Insight

> **The Trick:** Since all elements are positive, we can maintain a window with two pointers. Expand when sum < target, contract when sum >= target to find the minimum length.

### Why Two Pointers Work Here

The critical observation is that with **positive integers only**:
- Moving right always increases the sum
- Moving left always decreases the sum
- This monotonic behavior means we never need to backtrack

### Algorithm

1. Initialize left = 0, current_sum = 0, min_length = infinity
2. For each right from 0 to n-1:
   - Add arr[right] to current_sum
   - While current_sum >= target:
     - Update min_length = min(min_length, right - left + 1)
     - Subtract arr[left] from current_sum
     - Move left pointer right
3. Return min_length (or 0 if still infinity)

### Dry Run Example

Let's trace through with `arr = [2, 3, 1, 2, 4, 3]`, `target = 7`:

```
Initial: left=0, sum=0, min_len=INF

right=0: sum=2
  sum(2) < 7, continue

right=1: sum=5
  sum(5) < 7, continue

right=2: sum=6
  sum(6) < 7, continue

right=3: sum=8
  sum(8) >= 7: min_len=4, subtract arr[0]=2, left=1, sum=6
  sum(6) < 7, continue

right=4: sum=10
  sum(10) >= 7: min_len=4, subtract arr[1]=3, left=2, sum=7
  sum(7) >= 7: min_len=3, subtract arr[2]=1, left=3, sum=6
  sum(6) < 7, continue

right=5: sum=9
  sum(9) >= 7: min_len=3, subtract arr[3]=2, left=4, sum=7
  sum(7) >= 7: min_len=2, subtract arr[4]=4, left=5, sum=3
  sum(3) < 7, continue

Final: min_len = 2
```

### Visual Diagram

```
Array: [2, 3, 1, 2, 4, 3]  Target: 7

Step 1: [2  3  1  2] 4  3    sum=8  len=4  (contract)
           L--------R

Step 2:  2 [3  1  2  4] 3    sum=10 len=4  (contract)
            L--------R

Step 3:  2  3 [1  2  4] 3    sum=7  len=3  (contract)
               L-----R

Step 4:  2  3  1 [2  4  3]   sum=9  len=3  (contract)
                  L-----R

Step 5:  2  3  1  2 [4  3]   sum=7  len=2  (BEST!)
                     L--R
```

### Code

```python
def solve_optimal(arr, target):
  """
  Two-pointer sliding window approach.

  Time: O(n) - each element visited at most twice
  Space: O(1) - only tracking pointers and sum
  """
  n = len(arr)
  left = 0
  curr_sum = 0
  min_len = float('inf')

  for right in range(n):
    curr_sum += arr[right]

    # Contract window while sum is sufficient
    while curr_sum >= target:
      min_len = min(min_len, right - left + 1)
      curr_sum -= arr[left]
      left += 1

  return min_len if min_len != float('inf') else 0


# Complete solution with I/O
def main():
  n, target = map(int, input().split())
  arr = list(map(int, input().split()))
  print(solve_optimal(arr, target))

if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element added once, removed at most once |
| Space | O(1) | Only tracking left pointer, sum, and min_len |

---

## Common Mistakes

### Mistake 1: Forgetting to Handle No Solution

```python
# WRONG - crashes or returns wrong answer
def solve(arr, target):
  min_len = float('inf')
  # ... algorithm ...
  return min_len  # Returns infinity if no solution!

# CORRECT
def solve(arr, target):
  min_len = float('inf')
  # ... algorithm ...
  return min_len if min_len != float('inf') else 0
```

**Problem:** No valid subarray means min_len stays at infinity.
**Fix:** Check for infinity and return 0.

### Mistake 2: Using This Approach with Negative Numbers

```python
# WRONG - two pointers fail with negative numbers
arr = [2, -1, 3, 4, -2]  # Has negatives!
# Cannot use sliding window - sum is not monotonic
```

**Problem:** With negative numbers, adding an element might decrease the sum, breaking the monotonic property.
**Fix:** Use monotonic deque with prefix sums for arrays with negatives.

### Mistake 3: Integer Overflow

**Problem:** Sum of 10^5 elements each up to 10^4 can exceed INT_MAX.
**Fix:** Use `long long` for cumulative sums.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element valid | `[10], target=5` | 1 | One element >= target |
| Single element invalid | `[3], target=5` | 0 | No valid subarray |
| Entire array needed | `[1,1,1], target=3` | 3 | Sum of all elements = target |
| No valid subarray | `[1,2,3], target=100` | 0 | Total sum < target |
| First element valid | `[7,1,2], target=7` | 1 | First element alone works |
| All same elements | `[3,3,3,3], target=9` | 3 | Any 3 consecutive elements |

---

## When to Use This Pattern

### Use Two-Pointer Sliding Window When:
- All array elements are **positive** (or all non-negative)
- Looking for minimum or maximum length subarray
- Sum/product constraint involves monotonic change with window size
- Need O(n) time complexity

### Do NOT Use When:
- Array contains **negative numbers** - use monotonic deque instead
- Looking for exact sum (may need hash map approach)
- Need to find all valid subarrays, not just min/max length

### Pattern Recognition Checklist:
- [ ] All elements positive? -> **Two-pointer works**
- [ ] Contains negatives? -> **Use monotonic deque + prefix sums**
- [ ] Need exact sum? -> **Consider prefix sums + hash map**
- [ ] Need count of subarrays? -> **Different approach needed**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subarray Sums I](https://cses.fi/problemset/task/1660) | Basic prefix sums and counting |
| [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) | Kadane's algorithm foundation |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Subarray Sums II](https://cses.fi/problemset/task/1661) | Handles negative numbers with prefix sums |
| [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/) | Same problem, different platform |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LeetCode 862](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) | Negative numbers, monotonic deque |
| [Subarray Distinct Values](https://cses.fi/problemset/task/2428) | Sliding window with different constraint |

---

## Key Takeaways

1. **The Core Idea:** With positive numbers, window sum is monotonic - expand to increase sum, contract to decrease.

2. **Time Optimization:** Brute force O(n^2) -> Optimal O(n) by avoiding redundant recalculation through the two-pointer technique.

3. **Space Trade-off:** No extra space needed (O(1)) since we only track pointers and running sum.

4. **Pattern:** This is the classic **variable-size sliding window** pattern for optimization problems.

5. **Key Limitation:** This approach only works when all elements are positive. For negative numbers, you need a monotonic deque approach.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement the two-pointer solution without looking at the code
- [ ] Explain why each pointer moves when it does
- [ ] Identify that this approach requires positive numbers
- [ ] Solve the problem in under 10 minutes
- [ ] Handle all edge cases correctly

---

## Additional Resources

- [CP-Algorithms: Two Pointers](https://cp-algorithms.com/others/two_pointers.html)
- [CSES Subarray Sums I](https://cses.fi/problemset/task/1660) - Related subarray sum problem
- [LeetCode Sliding Window Pattern](https://leetcode.com/tag/sliding-window/)
