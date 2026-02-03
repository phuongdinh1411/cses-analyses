---
layout: simple
title: "Sliding Window Maximum - Monotonic Deque Pattern"
permalink: /problem_soulutions/sliding_window/sliding_window_advertisement_analysis
difficulty: Medium
tags: [sliding-window, monotonic-deque, multiset, array]
prerequisites: []
---

# Sliding Window Maximum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window |
| **Time Limit** | 1 second |
| **Key Technique** | Monotonic Deque / Multiset |
| **CSES Link** | [Sliding Window Maximum](https://cses.fi/problemset/task/1076) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand monotonic deque data structure and its applications
- [ ] Maintain sliding window maximum/minimum in O(n) time
- [ ] Use multiset (C++) or sorted containers for window operations
- [ ] Recognize when sliding window pattern applies to optimization problems

---

## Problem Statement

**Problem:** Given an array of n integers and a window size k, find the maximum value in each window as it slides from left to right.

**Input:**
- Line 1: Two integers n and k (array size and window size)
- Line 2: n integers representing the array elements

**Output:**
- n-k+1 integers: the maximum value in each sliding window

**Constraints:**
- 1 <= k <= n <= 2 * 10^5
- 1 <= x_i <= 10^9

### Example

```
Input:
8 3
2 4 3 5 8 1 2 1

Output:
4 5 8 8 8 2
```

**Explanation:**
- Window [2,4,3] -> max = 4
- Window [4,3,5] -> max = 5
- Window [3,5,8] -> max = 8
- Window [5,8,1] -> max = 8
- Window [8,1,2] -> max = 8
- Window [1,2,1] -> max = 2

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently track the maximum as elements enter and leave the window?

The brute force approach recalculates max for every window (O(nk)). The key insight is: we only need to track elements that could potentially become the maximum. If a newer element is larger than older elements, those older elements will never be the maximum.

### Breaking Down the Problem

1. **What are we looking for?** Maximum value in each window of size k
2. **What information do we have?** Array values and their positions
3. **What's the relationship?** Elements leaving the window can affect max; new elements might become the new max

### Analogies

Think of a waiting line where only the tallest person matters. When a taller person joins, everyone shorter in front becomes irrelevant - they will leave before the tall person, and can never be "the tallest".

---

## Solution 1: Brute Force

### Idea

For each window position, scan all k elements to find the maximum.

### Code

```python
def solve_brute_force(n, k, arr):
    """
    Brute force: check every element in each window.
    Time: O(n*k), Space: O(1)
    """
    result = []
    for i in range(n - k + 1):
        result.append(max(arr[i:i+k]))
    return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n*k) | For each of n-k+1 windows, scan k elements |
| Space | O(1) | Only store current max |

### Why This Works (But Is Slow)

Correctness is guaranteed - we check every element. However, with n,k up to 2*10^5, this gives 4*10^10 operations - far too slow.

---

## Solution 2: Optimal - Monotonic Deque

### Key Insight

> **The Trick:** Maintain a decreasing deque of indices. The front always holds the maximum for the current window.

### How Monotonic Deque Works

| Property | Description |
|----------|-------------|
| Store indices | Not values - allows checking if element is in window |
| Decreasing order | arr[dq[0]] >= arr[dq[1]] >= ... |
| Front is max | The front element is always the current window maximum |

**In plain English:** Keep only elements that could be the maximum. Remove smaller elements from back when adding a larger one.

### Algorithm

1. For each element at index i:
   - Remove indices from front that are outside window (index <= i-k)
   - Remove indices from back where arr[index] <= arr[i] (they can never be max)
   - Add current index i to back
   - If window is complete (i >= k-1), record arr[front] as the maximum

### Dry Run Example

Let's trace through with `arr = [2,4,3,5,8,1,2,1], k = 3`:

```
Initial: deque = []

i=0, arr[0]=2:
  deque = [0]                    (add index 0)
  Window incomplete

i=1, arr[1]=4:
  arr[0]=2 <= 4, pop back       deque = []
  deque = [1]                    (add index 1)
  Window incomplete

i=2, arr[2]=3:
  arr[1]=4 > 3, keep
  deque = [1, 2]                 (add index 2)
  Window complete: arr[1] = 4    OUTPUT: 4

i=3, arr[3]=5:
  arr[2]=3 <= 5, pop back       deque = [1]
  arr[1]=4 <= 5, pop back       deque = []
  deque = [3]                    (add index 3)
  Window [1,3]: arr[3] = 5       OUTPUT: 5

i=4, arr[4]=8:
  arr[3]=5 <= 8, pop back       deque = []
  deque = [4]                    (add index 4)
  Window [2,4]: arr[4] = 8       OUTPUT: 8

i=5, arr[5]=1:
  arr[4]=8 > 1, keep
  deque = [4, 5]                 (add index 5)
  Window [3,5]: arr[4] = 8       OUTPUT: 8

i=6, arr[6]=2:
  arr[5]=1 <= 2, pop back       deque = [4]
  deque = [4, 6]                 (add index 6)
  Window [4,6]: arr[4] = 8       OUTPUT: 8

i=7, arr[7]=1:
  Index 4 <= 7-3=4, pop front   deque = [6]
  arr[6]=2 > 1, keep
  deque = [6, 7]                 (add index 7)
  Window [5,7]: arr[6] = 2       OUTPUT: 2

Final: [4, 5, 8, 8, 8, 2]
```

### Visual Diagram

```
Array:    [2] [4] [3] [5] [8] [1] [2] [1]
Index:     0   1   2   3   4   5   6   7

Window at i=4:
          ─────────────────────────
                  [3] [5] [8]       <- Window covers indices 2,3,4
                           ^
          Deque: [4]       └── Only index 4 in deque (8 dominated all)
          Max = arr[4] = 8
```

### Code

**Python:**
```python
from collections import deque
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    dq = deque()  # stores indices
    result = []

    for i in range(n):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove indices of smaller elements (they can never be max)
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()

        dq.append(i)

        # Record maximum when window is complete
        if i >= k - 1:
            result.append(arr[dq[0]])

    print(' '.join(map(str, result)))

solve()
```

**C++ (Deque):**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    deque<int> dq;  // stores indices

    for (int i = 0; i < n; i++) {
        // Remove indices outside current window
        while (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }

        // Remove indices of smaller elements
        while (!dq.empty() && arr[dq.back()] <= arr[i]) {
            dq.pop_back();
        }

        dq.push_back(i);

        // Output maximum when window is complete
        if (i >= k - 1) {
            cout << arr[dq.front()];
            if (i < n - 1) cout << " ";
        }
    }
    cout << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element enters and leaves deque exactly once |
| Space | O(k) | Deque stores at most k indices |

---

## Solution 3: Alternative - Multiset (C++)

### Key Insight

> **The Trick:** Use a balanced BST (multiset) that supports O(log k) insertion, deletion, and max queries.

### Code

**C++ (Multiset):**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    multiset<int> window;

    for (int i = 0; i < n; i++) {
        window.insert(arr[i]);

        // Remove element leaving the window
        if (i >= k) {
            window.erase(window.find(arr[i - k]));
        }

        // Output maximum when window is complete
        if (i >= k - 1) {
            cout << *window.rbegin();
            if (i < n - 1) cout << " ";
        }
    }
    cout << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log k) | Each insert/erase is O(log k) |
| Space | O(k) | Multiset stores k elements |

---

## Common Mistakes

### Mistake 1: Using Value Instead of Index in Deque

```python
# WRONG - can't check if element is outside window
dq.append(arr[i])  # storing value

# CORRECT - store index to check window bounds
dq.append(i)  # storing index
```

**Problem:** Without indices, you cannot determine which elements are outside the window.
**Fix:** Always store indices; access values via arr[index].

### Mistake 2: Wrong Comparison Direction

```python
# WRONG - maintains increasing order (gives minimum!)
while dq and arr[dq[-1]] >= arr[i]:
    dq.pop()

# CORRECT - maintains decreasing order (gives maximum)
while dq and arr[dq[-1]] <= arr[i]:
    dq.pop()
```

**Problem:** Using >= instead of <= gives you minimum, not maximum.
**Fix:** For maximum, remove elements smaller than or equal to current.

### Mistake 3: Off-by-One in Window Check

```python
# WRONG - outputs too early
if i >= k:
    result.append(arr[dq[0]])

# CORRECT - window complete at index k-1
if i >= k - 1:
    result.append(arr[dq[0]])
```

**Problem:** First complete window is at index k-1 (0-indexed).
**Fix:** Check i >= k-1 for window completion.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Window equals array | n=3, k=3, [1,2,3] | 3 | Single window |
| Window size 1 | n=4, k=1, [3,1,4,2] | 3 1 4 2 | Each element is its own max |
| All same values | n=4, k=2, [5,5,5,5] | 5 5 5 | Deque may hold all indices |
| Decreasing array | n=4, k=2, [4,3,2,1] | 4 3 2 | Each new max at front |
| Increasing array | n=4, k=2, [1,2,3,4] | 2 3 4 | Deque always has single element |

---

## When to Use This Pattern

### Use Monotonic Deque When:
- Finding max/min in sliding window
- Need O(n) time complexity
- Window size is fixed
- Processing elements in order

### Use Multiset When:
- Need both max AND min in same window
- More flexible queries (kth element, etc.)
- O(n log k) is acceptable
- Simpler to implement correctly

### Pattern Recognition Checklist:
- [ ] Fixed window size? -> Consider monotonic deque
- [ ] Need max OR min (not both)? -> Monotonic deque is optimal
- [ ] Need both max AND min? -> Consider multiset or two deques
- [ ] Variable window size? -> Consider two-pointer + deque

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Sum of Two Values](https://cses.fi/problemset/task/1640) | Basic sliding window concept |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Sliding Window Minimum](https://cses.fi/problemset/task/1076) | Same technique, flip comparison |
| [Sliding Window Median](https://cses.fi/problemset/task/1076) | Two heaps or augmented BST |
| [Playlist](https://cses.fi/problemset/task/1141) | Variable window with distinct elements |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Subarray Sums II](https://cses.fi/problemset/task/1661) | Prefix sums with hash map |
| [Movie Festival II](https://cses.fi/problemset/task/1632) | Greedy + multiset |

---

## Key Takeaways

1. **Core Idea:** Monotonic deque maintains candidates for maximum by removing dominated elements
2. **Time Optimization:** From O(nk) brute force to O(n) by amortized analysis - each element enters/exits once
3. **Space Trade-off:** O(k) space for deque to achieve O(n) time
4. **Pattern:** This is the "Monotonic Deque" pattern - essential for sliding window max/min problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement monotonic deque from scratch without reference
- [ ] Explain why each element enters and exits deque at most once
- [ ] Adapt the solution for minimum instead of maximum
- [ ] Choose between deque (O(n)) and multiset (O(n log k)) based on requirements
