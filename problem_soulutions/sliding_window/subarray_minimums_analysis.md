---
layout: simple
title: "Sliding Window Minimum - Monotonic Deque"
permalink: /problem_soulutions/sliding_window/subarray_minimums_analysis
difficulty: Medium
tags: [sliding-window, monotonic-deque, array]
---

# Sliding Window Minimum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window |
| **Time Limit** | 1 second |
| **Key Technique** | Monotonic Deque |
| **CSES Link** | [Sliding Median](https://cses.fi/problemset/task/1076) (related) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement a monotonic deque data structure
- [ ] Recognize when sliding window problems need O(1) min/max queries
- [ ] Apply the monotonic deque pattern to similar problems
- [ ] Explain why each element enters and leaves the deque at most once

---

## Problem Statement

**Problem:** Given an array of n integers and a window size k, find the minimum element in each sliding window of size k as the window moves from left to right.

**Input:**
- Line 1: Two integers n (array size) and k (window size)
- Line 2: n space-separated integers

**Output:**
- n - k + 1 integers: the minimum of each window

**Constraints:**
- 1 <= k <= n <= 10^5
- -10^9 <= arr[i] <= 10^9

### Example

```
Input:
8 3
2 1 4 5 3 4 1 2

Output:
1 1 3 3 1 1
```

**Explanation:**
- Window [2,1,4] -> min = 1
- Window [1,4,5] -> min = 1
- Window [4,5,3] -> min = 3
- Window [5,3,4] -> min = 3
- Window [3,4,1] -> min = 1
- Window [4,1,2] -> min = 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we track the minimum efficiently as the window slides?

The naive approach recalculates the minimum for each window in O(k), giving O(nk) total. We need a data structure that:
1. Gives us the current minimum in O(1)
2. Allows efficient updates when the window slides

### Breaking Down the Problem

1. **What are we looking for?** The minimum value in each window position
2. **What changes between windows?** One element leaves (left), one enters (right)
3. **Key insight:** If we see a smaller element, all larger elements before it in the window can never be the minimum

### The Monotonic Deque Idea

Think of it like a queue of "candidates" for minimum:
- New elements enter from the right
- Before adding, remove all larger elements (they can never win)
- The front always holds the current minimum
- Remove the front if it exits the window

```
Window: [5, 3, 4]  ->  Deque holds indices of: [3, 4]
                       (5 was removed because 3 < 5)
                       Front value 3 is the minimum
```

---

## Solution 1: Brute Force

### Idea

For each window position, scan all k elements to find the minimum.

### Code

```python
def sliding_minimum_brute(arr, k):
  """
  Brute force: check all elements in each window.
  Time: O(n*k), Space: O(1)
  """
  n = len(arr)
  result = []
  for i in range(n - k + 1):
    result.append(min(arr[i:i+k]))
  return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n*k) | Each window scans k elements |
| Space | O(1) | No extra data structures |

### Why This Is Too Slow

For n = k = 10^5, this gives 10^10 operations - way too slow.

---

## Solution 2: Optimal - Monotonic Deque

### Key Insight

> **The Trick:** Maintain a deque of indices where values are in increasing order. The front is always the minimum.

### How the Deque Works

| Operation | When | Effect |
|-----------|------|--------|
| Pop from back | New element is smaller than back | Remove elements that can never be minimum |
| Push to back | Always | Add new candidate |
| Pop from front | Front index is outside window | Remove expired minimum |
| Read front | Output time | Get current window minimum |

### Algorithm

1. Initialize empty deque (stores indices)
2. For each index i:
   - Remove indices from back while arr[back] >= arr[i]
   - Add index i to back
   - Remove front if it's outside window (front <= i - k)
   - If window is complete (i >= k-1), output arr[front]

### Dry Run Example

Input: `arr = [2, 1, 4, 5, 3]`, `k = 3`

```
i=0: arr[0]=2
     Deque: []
     Pop back? No elements
     Add 0: [0]
     Pop front? 0 > 0-3, no
     Window incomplete (i < k-1)
     Deque: [0]          (values: [2])

i=1: arr[1]=1
     Deque: [0]
     Pop back? arr[0]=2 >= arr[1]=1, yes -> pop 0
     Deque: []
     Add 1: [1]
     Pop front? 1 > 1-3, no
     Window incomplete
     Deque: [1]          (values: [1])

i=2: arr[2]=4
     Deque: [1]
     Pop back? arr[1]=1 >= arr[2]=4? No
     Add 2: [1, 2]
     Pop front? 1 > 2-3, no
     Window complete! Output arr[1] = 1
     Deque: [1, 2]       (values: [1, 4])

i=3: arr[3]=5
     Deque: [1, 2]
     Pop back? arr[2]=4 >= arr[3]=5? No
     Add 3: [1, 2, 3]
     Pop front? 1 > 3-3=0? No (1 > 0 is true... wait)
     Actually: 1 <= 3-3=0? No, 1 > 0
     Pop front? 1 <= 0? No
     Window complete! Output arr[1] = 1
     Deque: [1, 2, 3]    (values: [1, 4, 5])

i=4: arr[4]=3
     Deque: [1, 2, 3]
     Pop back? arr[3]=5 >= arr[4]=3? Yes -> pop 3
     Deque: [1, 2]
     Pop back? arr[2]=4 >= arr[4]=3? Yes -> pop 2
     Deque: [1]
     Pop back? arr[1]=1 >= arr[4]=3? No
     Add 4: [1, 4]
     Pop front? 1 <= 4-3=1? Yes! -> pop 1
     Deque: [4]
     Window complete! Output arr[4] = 3
     Deque: [4]          (values: [3])

Output: [1, 1, 3]
```

### Visual Diagram

```
Array:  [2,  1,  4,  5,  3]
Index:   0   1   2   3   4

Window 1: [2, 1, 4]     Deque indices: [1, 2]  -> min = arr[1] = 1
              ^front

Window 2: [1, 4, 5]     Deque indices: [1, 2, 3] -> min = arr[1] = 1
              ^front    (index 1 still in window)

Window 3: [4, 5, 3]     Deque indices: [4] -> min = arr[4] = 3
              ^front    (index 1 expired, 2&3 popped)
```

### Code

```python
from collections import deque

def sliding_minimum(arr, k):
  """
  Optimal solution using monotonic deque.
  Time: O(n), Space: O(k)
  """
  n = len(arr)
  dq = deque()  # stores indices
  result = []

  for i in range(n):
    # Remove indices of larger elements from back
    while dq and arr[dq[-1]] >= arr[i]:
      dq.pop()

    # Add current index
    dq.append(i)

    # Remove index if outside window
    if dq[0] <= i - k:
      dq.popleft()

    # Record minimum once window is complete
    if i >= k - 1:
      result.append(arr[dq[0]])

  return result


# CSES-style I/O
def main():
  import sys
  input_data = sys.stdin.read().split()
  idx = 0
  n, k = int(input_data[idx]), int(input_data[idx+1])
  idx += 2
  arr = [int(input_data[idx+i]) for i in range(n)]

  result = sliding_minimum(arr, k)
  print(' '.join(map(str, result)))

if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element enters and leaves deque at most once |
| Space | O(k) | Deque holds at most k indices |

### Why O(n) Time?

Each index is:
- Added to deque exactly once
- Removed from deque at most once

Total operations: at most 2n = O(n)

---

## Common Mistakes

### Mistake 1: Using Values Instead of Indices

```python
# WRONG - Cannot track window boundaries
dq.append(arr[i])

# CORRECT - Store indices to check window bounds
dq.append(i)
```

**Problem:** Without indices, you cannot determine when an element leaves the window.

### Mistake 2: Wrong Comparison Direction

```python
# WRONG - Creates decreasing deque (for maximum, not minimum)
while dq and arr[dq[-1]] <= arr[i]:
  dq.pop()

# CORRECT - Increasing deque for minimum
while dq and arr[dq[-1]] >= arr[i]:
  dq.pop()
```

**Problem:** Using `<=` gives you a decreasing deque, which tracks maximum, not minimum.

### Mistake 3: Forgetting Window Boundary Check

```python
# WRONG - Never removes expired elements
for i in range(n):
  while dq and arr[dq[-1]] >= arr[i]:
    dq.pop()
  dq.append(i)
  result.append(arr[dq[0]])  # May use element outside window!

# CORRECT - Check and remove expired front
if dq[0] <= i - k:
  dq.popleft()
```

### Mistake 4: Off-by-One in Window Completion

```python
# WRONG - Starts output too early
if i >= k:
  result.append(arr[dq[0]])

# CORRECT - First complete window at index k-1
if i >= k - 1:
  result.append(arr[dq[0]])
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element window | `k=1, arr=[3,1,4]` | `3 1 4` | Each element is its own minimum |
| Window equals array | `k=n, arr=[3,1,4]` | `1` | Single window, global minimum |
| All same elements | `arr=[5,5,5,5], k=2` | `5 5 5` | Deque behavior still correct |
| Strictly decreasing | `arr=[5,4,3,2,1], k=3` | `3 2 1` | Minimum always at right |
| Strictly increasing | `arr=[1,2,3,4,5], k=3` | `1 2 3` | Minimum always at left (front stays) |
| Negative numbers | `arr=[-3,1,-5,2], k=2` | `-3 -5 -5` | Works with any integers |

---

## When to Use This Pattern

### Use Monotonic Deque When:
- Finding min/max in a sliding window of fixed size
- Need O(1) per window (O(n) total)
- Window moves one element at a time
- Examples: stock prices, temperature ranges, buffer analysis

### Don't Use When:
- Window size varies -> consider segment tree
- Need min in arbitrary ranges -> consider sparse table or segment tree
- Updates to array values -> consider segment tree with lazy propagation

### Pattern Recognition Checklist:
- [ ] Fixed window size sliding across array? -> **Consider monotonic deque**
- [ ] Need min OR max (not both)? -> **Monotonic deque works well**
- [ ] Need both min AND max? -> **Use two deques (one increasing, one decreasing)**

---

## Related Problems

### CSES Problems

| Problem | Link | Relevance |
|---------|------|-----------|
| Sliding Median | [cses.fi/problemset/task/1076](https://cses.fi/problemset/task/1076) | Sliding window statistics |
| Sliding Cost | [cses.fi/problemset/task/1077](https://cses.fi/problemset/task/1077) | Window optimization |
| Range Minimum Queries | [cses.fi/problemset/task/1647](https://cses.fi/problemset/task/1647) | Static RMQ (different technique) |

### LeetCode Problems

| Problem | Link | Connection |
|---------|------|------------|
| Sliding Window Maximum | [leetcode.com/problems/sliding-window-maximum](https://leetcode.com/problems/sliding-window-maximum/) | Same pattern, track max instead |
| Shortest Subarray with Sum >= K | [leetcode.com/problems/shortest-subarray-with-sum-at-least-k](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) | Monotonic deque on prefix sums |
| Constrained Subsequence Sum | [leetcode.com/problems/constrained-subsequence-sum](https://leetcode.com/problems/constrained-subsequence-sum/) | DP + monotonic deque |

---

## Key Takeaways

1. **The Core Idea:** Maintain candidates in sorted order; discard elements that can never be the answer
2. **Time Optimization:** From O(nk) to O(n) by avoiding redundant comparisons
3. **Space Trade-off:** O(k) extra space for the deque
4. **Pattern:** Monotonic data structures eliminate dominated elements

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement monotonic deque for sliding window min without references
- [ ] Modify the solution for sliding window maximum
- [ ] Explain why time complexity is O(n), not O(nk)
- [ ] Handle edge cases: k=1, k=n, all equal elements
- [ ] Solve in under 15 minutes
