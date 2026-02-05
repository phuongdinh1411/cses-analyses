---
layout: simple
title: "Josephus Problem II - Sorting and Searching"
permalink: /problem_soulutions/sorting_and_searching/josephus_problem_ii_analysis
difficulty: Medium
tags: [order-statistics-tree, indexed-set, simulation, modular-arithmetic]
prerequisites: [josephus_problem_i]
---

# Josephus Problem II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Data Structures / Simulation |
| **Time Limit** | 1 second |
| **Key Technique** | Indexed Set (Order Statistics Tree) |
| **CSES Link** | [Josephus Problem II](https://cses.fi/problemset/task/2163) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when simulation requires O(n log n) data structures
- [ ] Implement and use an indexed set (order statistics tree) in C++
- [ ] Handle circular indexing with modulo arithmetic correctly
- [ ] Recognize problems that need efficient k-th element removal

---

## Problem Statement

**Problem:** There are n children in a circle. Starting from child 1, count k children clockwise and remove the k-th child. Repeat until all children are removed. Print the removal order.

**Input:**
- Line 1: Two integers n and k (number of children and skip count)

**Output:**
- Print n integers: the removal order of children

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= k <= 10^9

### Example

```
Input:
7 3

Output:
3 6 2 7 5 1 4
```

**Explanation:** Starting from position 1, count 3 positions: 1->2->3, remove child 3. Next, count 3 from position 4: 4->5->6, remove child 6. Continue this process until all children are removed.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why is this different from Josephus Problem I (k=2)?

With k=2, we can use the mathematical formula J(n) = 2*L + 1 where n = 2^m + L. But this problem:
1. Has **arbitrary k** (up to 10^9)
2. Requires the **full elimination order**, not just the survivor

The mathematical recurrence J(n,k) = (J(n-1,k) + k) mod n only gives the FINAL survivor, not the elimination sequence.

### Breaking Down the Problem

1. **What are we looking for?** The complete sequence of eliminated children
2. **What information do we have?** Circle size n, skip count k
3. **What operation do we need repeatedly?** Find and remove the k-th element from current position

### The Core Challenge

Each step requires:
- Finding the k-th element from current position in a shrinking circle
- Removing that element efficiently
- Continuing from the next position

With a simple list, removal is O(n), giving O(n^2) total - too slow for n = 2*10^5.

**We need a data structure supporting O(log n) operations for:**
1. Find k-th element (order statistics)
2. Delete an element
3. Determine position/rank of an element

---

## Solution 1: Brute Force (List Simulation)

### Idea

Maintain a list of remaining children. For each elimination, compute the target index using modulo and remove from the list.

### Algorithm

1. Initialize list with children 1 to n
2. Start at index 0
3. While list is not empty:
   - Compute target = (current + k - 1) % size
   - Remove and output element at target
   - Update current = target % new_size (if non-empty)

### Code

```python
def josephus_brute_force(n: int, k: int) -> list[int]:
    """
    Brute force simulation using list.

    Time: O(n^2) - each removal is O(n)
    Space: O(n)
    """
    children = list(range(1, n + 1))
    result = []
    current = 0

    while children:
        current = (current + k - 1) % len(children)
        result.append(children.pop(current))
        if children:
            current = current % len(children)

    return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | n removals, each O(n) for list.pop |
| Space | O(n) | Storing the list |

### Why This Is Too Slow

For n = 2*10^5, we need ~4*10^10 operations, which exceeds the time limit.

---

## Solution 2: Optimal - Indexed Set (Order Statistics Tree)

### Key Insight

> **The Trick:** Use a balanced BST that supports O(log n) rank queries and deletions - the "indexed set" or "order statistics tree."

This data structure provides:
- `find_by_order(k)`: Find k-th smallest element in O(log n)
- `order_of_key(x)`: Find rank of element x in O(log n)
- `erase(x)`: Delete element in O(log n)

### Why Indexed Set Works

In a circle of size m, to find the k-th element from current position:
1. Current position has rank `pos` (0-indexed)
2. Target rank = (pos + k - 1) % m
3. Get element at that rank, remove it
4. New position = target_rank % (m - 1)

All operations are O(log n) with an indexed set.

### Algorithm

1. Insert all children 1..n into indexed set
2. Start at position 0
3. While set is not empty:
   - target_pos = (current_pos + k - 1) % size
   - Get element at target_pos using find_by_order
   - Output and erase that element
   - Update current_pos = target_pos % new_size (if non-empty)

### Dry Run Example

Let's trace through with n=7, k=3:

```
Initial: {1, 2, 3, 4, 5, 6, 7}, pos = 0

Step 1:
  size = 7, target = (0 + 3 - 1) % 7 = 2
  Element at rank 2 is: 3
  Remove 3, output: [3]
  New pos = 2 % 6 = 2
  Set: {1, 2, 4, 5, 6, 7}

Step 2:
  size = 6, target = (2 + 3 - 1) % 6 = 4
  Element at rank 4 is: 6
  Remove 6, output: [3, 6]
  New pos = 4 % 5 = 4
  Set: {1, 2, 4, 5, 7}

Step 3:
  size = 5, target = (4 + 3 - 1) % 5 = 1
  Element at rank 1 is: 2
  Remove 2, output: [3, 6, 2]
  New pos = 1 % 4 = 1
  Set: {1, 4, 5, 7}

Step 4:
  size = 4, target = (1 + 3 - 1) % 4 = 3
  Element at rank 3 is: 7
  Remove 7, output: [3, 6, 2, 7]
  New pos = 3 % 3 = 0
  Set: {1, 4, 5}

Step 5:
  size = 3, target = (0 + 3 - 1) % 3 = 2
  Element at rank 2 is: 5
  Remove 5, output: [3, 6, 2, 7, 5]
  New pos = 2 % 2 = 0
  Set: {1, 4}

Step 6:
  size = 2, target = (0 + 3 - 1) % 2 = 0
  Element at rank 0 is: 1
  Remove 1, output: [3, 6, 2, 7, 5, 1]
  New pos = 0 % 1 = 0
  Set: {4}

Step 7:
  size = 1, target = (0 + 3 - 1) % 1 = 0
  Element at rank 0 is: 4
  Remove 4, output: [3, 6, 2, 7, 5, 1, 4]
  Set: {}

Final output: 3 6 2 7 5 1 4
```

### Visual Diagram

```
Circle (n=7, k=3):

Initial:        After removing 3:    After removing 6:
    1                 1                   1
  7   2             7   2               7   2
 6     3 <-X       6     4 <-         5     4 <-
  5   4             5   4
                        ^                   ^
                    count from 4        count from 4
```

### Code (Python with SortedList)

Python's standard library lacks an indexed set, but we can use `sortedcontainers.SortedList`:

```python
from sortedcontainers import SortedList

def josephus_optimal(n: int, k: int) -> list[int]:
    """
    Optimal solution using SortedList (balanced BST).

    Time: O(n log n)
    Space: O(n)
    """
    children = SortedList(range(1, n + 1))
    result = []
    pos = 0

    while children:
        pos = (pos + k - 1) % len(children)
        removed = children.pop(pos)
        result.append(removed)
        if children:
            pos = pos % len(children)

    return result

# Main
if __name__ == "__main__":
    n, k = map(int, input().split())
    result = josephus_optimal(n, k)
    print(" ".join(map(str, result)))
```

**Note:** For CSES submissions, use the C++ version as `sortedcontainers` is not available.

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | n iterations, each O(log n) for tree operations |
| Space | O(n) | Storing n elements in the tree |

---

## Common Mistakes

### Mistake 1: Wrong Modulo Calculation

```python
# WRONG: Using k directly without adjusting for 0-indexing
pos = (pos + k) % len(children)  # Off by one!

# CORRECT: Account for 0-indexed positions
pos = (pos + k - 1) % len(children)
```

**Problem:** The k-th element from current means moving k-1 positions forward.
**Fix:** Use `k - 1` in the calculation.

### Mistake 2: Forgetting to Update Position After Removal

```python
# WRONG: Not adjusting position after removal
children.pop(pos)
# pos might now be out of bounds!

# CORRECT: Adjust position for next iteration
children.pop(pos)
if children:
    pos = pos % len(children)
```

**Problem:** After removing element at position `pos`, the new size is smaller.
**Fix:** Take modulo with new size if non-empty.

### Mistake 3: Confusing 0-indexed vs 1-indexed

**Problem:** The problem uses 1-indexed children.
**Fix:** Insert values 1 to n, not 0 to n-1.

### Mistake 4: Using Mathematical Formula for Elimination Order

```python
# WRONG: This only gives the FINAL survivor
def josephus_math(n, k):
    result = 0
    for i in range(2, n + 1):
        result = (result + k) % i
    return result + 1  # Only the survivor!

# CORRECT: Need simulation for full elimination order
# Use indexed set as shown above
```

**Problem:** The recurrence J(n,k) = (J(n-1,k) + k) % n gives only the survivor.
**Fix:** For elimination ORDER, simulation is required.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single child | n=1, k=5 | 1 | Only one child to remove |
| k=1 | n=5, k=1 | 1 2 3 4 5 | Remove in order |
| k=n | n=4, k=4 | 4 3 2 1 | Remove last, then last of remaining |
| Large k | n=3, k=10^9 | Depends on k%n pattern | Modulo handles large k |
| k > n | n=5, k=7 | Same as k=2 (mod pattern) | Modulo wraps around |

---

## When to Use This Pattern

### Use This Approach When:
- You need to repeatedly find and remove the k-th element
- Operations must be faster than O(n) per step
- Order of removal matters (not just final survivor)
- k is arbitrary (not just k=2 which has a formula)

### Don't Use When:
- Only the final survivor is needed (use mathematical formula)
- k=2 specifically (Josephus I has O(n) formula)
- n is very small (brute force is simpler)

### Pattern Recognition Checklist:
- [ ] Need to find k-th element repeatedly? -> **Order Statistics Tree**
- [ ] Need efficient removal from middle? -> **Balanced BST / Indexed Set**
- [ ] Circular elimination with arbitrary k? -> **This exact pattern**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Josephus Problem I (CSES 2162)](https://cses.fi/problemset/task/2162) | k=2 case with mathematical solution |
| [Find the Winner (LeetCode 1823)](https://leetcode.com/problems/find-the-winner-of-the-circular-game/) | Same problem, only asks for survivor |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Traffic Lights (CSES 1163)](https://cses.fi/problemset/task/1163) | Ordered set for tracking segments |
| [Room Allocation (CSES 1164)](https://cses.fi/problemset/task/1164) | Set operations for interval scheduling |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Sliding Window Median (LeetCode 480)](https://leetcode.com/problems/sliding-window-median/) | Two balanced BSTs for median tracking |
| [Range Sum BST variants](https://cses.fi/problemset/task/1749) | Order statistics in more complex scenarios |

---

## Key Takeaways

1. **The Core Idea:** Use an indexed set (order statistics tree) for O(log n) k-th element queries and deletions
2. **Time Optimization:** From O(n^2) brute force to O(n log n) with balanced BST
3. **Space Trade-off:** O(n) space for the tree structure is acceptable
4. **Pattern:** This is the "repeated k-th element removal" pattern requiring order statistics

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why mathematical formula doesn't work for elimination order
- [ ] Implement indexed set solution in C++ using pb_ds
- [ ] Handle the modulo arithmetic correctly (k-1 and position adjustment)
- [ ] Identify similar problems requiring order statistics

---

## Additional Resources

- [CP-Algorithms: Order Statistics Tree](https://cp-algorithms.com/data_structures/order_statistic_tree.html)
- [GNU Policy-Based Data Structures](https://gcc.gnu.org/onlinedocs/libstdc++/manual/policy_data_structures.html)
- [CSES Josephus Problem II](https://cses.fi/problemset/task/2163) - Order statistic variant
