---
layout: simple
title: "Sliding Window Maximum - Monotonic Deque"
permalink: /problem_soulutions/sliding_window/subarray_maximums_analysis
difficulty: Medium
tags: [sliding-window, monotonic-deque, deque, array]
prerequisites: [basic-arrays, deque-operations]
---

# Sliding Window Maximum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window |
| **Time Limit** | 1 second |
| **Key Technique** | Monotonic Deque |
| **CSES Link** | [Sliding Window Maximum](https://cses.fi/problemset/task/1076) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand why a monotonic deque achieves O(n) time complexity
- [ ] Implement a decreasing monotonic deque for maximum tracking
- [ ] Recognize sliding window problems that benefit from deque optimization
- [ ] Apply the same pattern to minimum queries by reversing the comparison

---

## Problem Statement

**Problem:** Given an array of n integers and a window size k, find the maximum element in each sliding window of size k as it moves from left to right.

**Input:**
- Line 1: Two integers n (array size) and k (window size)
- Line 2: n space-separated integers

**Output:**
- n-k+1 integers: the maximum of each window

**Constraints:**
- 1 <= k <= n <= 2 x 10^5
- 1 <= arr[i] <= 10^9

### Example

```
Input:
8 3
2 1 4 5 3 4 1 2

Output:
4 5 5 5 4 4
```

**Explanation:**
- Window [2,1,4] -> max = 4
- Window [1,4,5] -> max = 5
- Window [4,5,3] -> max = 5
- Window [5,3,4] -> max = 5
- Window [3,4,1] -> max = 4
- Window [4,1,2] -> max = 4

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When the window slides, how can we efficiently update the maximum without rechecking all k elements?

The core insight is that many elements in the window can never become the maximum. If we see a larger element, all smaller elements before it (still in the window) become irrelevant because the larger element will outlast them or we will find an even larger one.

### Breaking Down the Problem

1. **What are we looking for?** The maximum value in each window position
2. **What information do we have?** Array values and their indices (positions)
3. **What is the relationship?** We need to track "candidates" that could be maximum as the window slides

### The Monotonic Deque Idea

Think of it like a queue of "potential champions":
- New elements enter from the right
- Before entering, they "knock out" all weaker elements (smaller values)
- The strongest (largest) is always at the front
- Old elements that leave the window are removed from the front

This maintains a **decreasing sequence** from front to back.

---

## Solution 1: Brute Force

### Idea

For each window position, scan all k elements to find the maximum.

### Code

```python
def sliding_max_brute(arr, k):
 n = len(arr)
 result = []
 for i in range(n - k + 1):
  result.append(max(arr[i:i+k]))
 return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n*k) | k comparisons for each of n-k+1 windows |
| Space | O(1) | No extra space beyond output |

### Why This Works (But Is Slow)

Correctness is obvious - we check every element. But with n = 200,000 and k = 100,000, this is 10^10 operations, far too slow.

---

## Solution 2: Optimal - Monotonic Deque

### Key Insight

> **The Trick:** Maintain a deque of indices where values are in decreasing order. The front always holds the maximum for the current window.

### Why Store Indices?

We store indices (not values) because:
1. We can look up the value anytime via `arr[index]`
2. We need to know when an element leaves the window (when `index <= i - k`)

### Algorithm

1. **Process each element** at index i:
   - **Remove expired:** Pop from front if index is outside window
   - **Remove smaller:** Pop from back while back element <= current (they can never be max)
   - **Add current:** Push current index to back
   - **Record answer:** If window is complete (i >= k-1), front is the max

### Dry Run Example

Input: `arr = [2, 1, 4, 5, 3]`, `k = 3`

```
Deque stores INDICES. Values shown for clarity: deque -> [idx:val, ...]

i=0, arr[0]=2:
  Deque empty, add 0
  Deque: [0:2]
  Window incomplete (need k=3 elements)

i=1, arr[1]=1:
  arr[1]=1 < arr[0]=2, just add 1
  Deque: [0:2, 1:1]
  Window incomplete

i=2, arr[2]=4:
  arr[2]=4 > arr[1]=1, pop 1
  arr[2]=4 > arr[0]=2, pop 0
  Add 2
  Deque: [2:4]
  Window [0,1,2] complete -> max = arr[2] = 4

i=3, arr[3]=5:
  arr[3]=5 > arr[2]=4, pop 2
  Add 3
  Deque: [3:5]
  Front index 3 > 3-3=0, still valid
  Window [1,2,3] -> max = arr[3] = 5

i=4, arr[4]=3:
  arr[4]=3 < arr[3]=5, just add 4
  Deque: [3:5, 4:3]
  Front index 3 > 4-3=1, still valid
  Window [2,3,4] -> max = arr[3] = 5

Output: [4, 5, 5]
```

### Visual Diagram

```
Array: [2, 1, 4, 5, 3]  k=3

Window 1: [2, 1, 4]
  Deque maintains: [4] (index 2)
  Max = 4

Window 2: [1, 4, 5]
  5 removes 4, Deque: [5] (index 3)
  Max = 5

Window 3: [4, 5, 3]
  3 < 5, Deque: [5, 3] (indices 3, 4)
  Max = 5 (front)
```

### Code

**Python:**
```python
from collections import deque

def sliding_max(arr, k):
 """
 Find maximum in each sliding window of size k.

 Time: O(n) - each element pushed/popped at most once
 Space: O(k) - deque holds at most k indices
 """
 n = len(arr)
 dq = deque()  # stores indices
 result = []

 for i in range(n):
  # Remove indices outside current window
  while dq and dq[0] <= i - k:
   dq.popleft()

  # Remove indices of elements smaller than current
  # They can never be the maximum while current exists
  while dq and arr[dq[-1]] <= arr[i]:
   dq.pop()

  dq.append(i)

  # Window is complete when i >= k-1
  if i >= k - 1:
   result.append(arr[dq[0]])

 return result


# CSES I/O wrapper
def main():
 import sys
 input_data = sys.stdin.read().split()
 n, k = int(input_data[0]), int(input_data[1])
 arr = list(map(int, input_data[2:2+n]))

 result = sliding_max(arr, k)
 print(' '.join(map(str, result)))

if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each index is pushed and popped at most once |
| Space | O(k) | Deque stores at most k indices |

---

## Common Mistakes

### Mistake 1: Using Values Instead of Indices

```python
# WRONG - Cannot track when elements leave the window
dq.append(arr[i])  # Stores value
while dq and dq[0] < ???:  # How do we know if it's out of window?
 dq.popleft()
```

**Problem:** Without indices, you cannot determine when the front element has left the window.
**Fix:** Store indices and check `dq[0] <= i - k`.

### Mistake 2: Wrong Removal Order

```python
# WRONG - Removing from front before back
for i in range(n):
 while dq and dq[0] <= i - k:  # Front removal
  dq.popleft()
 dq.append(i)  # Adding without back removal!
```

**Problem:** Not removing smaller elements from back breaks the decreasing property.
**Fix:** Remove from back (smaller elements) before adding current element.

### Mistake 3: Strict vs Non-Strict Comparison

```python
# WRONG for some cases
while dq and arr[dq[-1]] < arr[i]:  # Strict less-than
 dq.pop()
```

**Problem:** With `<` instead of `<=`, duplicates can accumulate unnecessarily.
**Fix:** Use `<=` to remove equal elements too (the newer one is equally good and stays longer).

### Mistake 4: Off-by-One Window Start

```python
# WRONG
if i >= k:  # Should be k-1
 result.append(arr[dq[0]])
```

**Problem:** Misses the first window or outputs too late.
**Fix:** First complete window is at index k-1 (0-indexed), so check `i >= k - 1`.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| k equals n | `arr=[3,1,4], k=3` | `4` | Single window, just find max |
| k equals 1 | `arr=[3,1,4], k=1` | `3 1 4` | Output is the array itself |
| All same | `arr=[5,5,5], k=2` | `5 5` | Deque works correctly with duplicates |
| Decreasing | `arr=[5,4,3,2], k=2` | `5 4 3` | Deque keeps all elements |
| Increasing | `arr=[1,2,3,4], k=2` | `2 3 4` | Each new element clears deque |

---

## When to Use This Pattern

### Use Monotonic Deque When:
- Finding max/min in **fixed-size** sliding windows
- You need O(n) time and O(k) space
- Processing elements left-to-right (streaming)

### Do Not Use When:
- Window size varies dynamically (consider segment tree)
- You need random access to any window (consider sparse table)
- The "window" is defined by value range, not position (consider different structure)

### Pattern Recognition Checklist:
- [ ] Fixed window size k? -> **Consider monotonic deque**
- [ ] Need max OR min (not both)? -> **Monotonic deque is ideal**
- [ ] Need both max AND min? -> **Use two deques**
- [ ] Range updates involved? -> **Consider segment tree instead**

---

## Sliding Minimum Variant

To find the **minimum** instead of maximum, reverse the comparison:

```python
# For MINIMUM: maintain INCREASING deque
while dq and arr[dq[-1]] >= arr[i]:  # Remove larger elements
 dq.pop()
```

The front will hold the minimum instead of the maximum.

---

## Related Problems

### CSES Problems

| Problem | Technique |
|---------|-----------|
| [Sliding Window Median](https://cses.fi/problemset/task/1076) | Two multisets or segment tree |
| [Sliding Window Cost](https://cses.fi/problemset/task/1077) | Extension with cost calculation |

### LeetCode Problems

| Problem | Key Difference |
|---------|----------------|
| [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Same problem |
| [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) | Monotonic deque on prefix sums |
| [Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum/) | DP with monotonic deque optimization |

---

## Key Takeaways

1. **Core Idea:** A decreasing deque keeps the maximum at the front; smaller elements are discarded because they cannot become maximum while a larger element exists in the window.

2. **Time Optimization:** From O(n*k) to O(n) because each element enters and leaves the deque exactly once.

3. **Space Trade-off:** O(k) space for the deque enables O(1) time per query.

4. **Pattern:** Monotonic data structures are powerful for range min/max queries with sliding windows.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement monotonic deque without looking at code
- [ ] Explain why each element is pushed/popped at most once
- [ ] Modify for sliding minimum
- [ ] Identify this pattern in new problems within 2 minutes
