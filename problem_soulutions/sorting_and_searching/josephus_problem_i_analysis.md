---
layout: simple
title: "Josephus Problem I - Simulation Problem"
permalink: /problem_soulutions/sorting_and_searching/josephus_problem_i_analysis
difficulty: Medium
tags: [simulation, circular-array, modular-arithmetic, mathematical]
prerequisites: []
---

# Josephus Problem I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Simulation / Mathematical |
| **Time Limit** | 1 second |
| **Key Technique** | Circular Array Simulation |
| **CSES Link** | [Josephus Problem I](https://cses.fi/problemset/task/2162) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Simulate circular elimination processes efficiently
- [ ] Handle modular arithmetic for circular indexing
- [ ] Understand the classic Josephus problem with k=2
- [ ] Choose between simulation and mathematical approaches based on constraints

---

## Problem Statement

**Problem:** There are n children standing in a circle. We count every second child (k=2) starting from the first child, and eliminate them from the circle. Output the elimination order.

**Input:**
- Line 1: A single integer n (number of children)

**Output:**
- Print n integers: the elimination order

**Constraints:**
- 1 <= n <= 2 * 10^5

### Example

```
Input:
7

Output:
2 4 6 1 5 3 7
```

**Explanation:**
Starting with children [1, 2, 3, 4, 5, 6, 7] in a circle:
- Count 1, 2 -> eliminate 2: remaining [1, 3, 4, 5, 6, 7]
- Count 3, 4 -> eliminate 4: remaining [1, 3, 5, 6, 7]
- Count 5, 6 -> eliminate 6: remaining [1, 3, 5, 7]
- Count 7, 1 -> eliminate 1: remaining [3, 5, 7]
- Count 3, 5 -> eliminate 5: remaining [3, 7]
- Count 7, 3 -> eliminate 3: remaining [7]
- Only 7 remains: eliminate 7

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently track who is still in the circle and find the next person to eliminate?

The Josephus problem is a classic counting-out game. With k=2, we always skip one person and eliminate the next. The challenge is maintaining the circular structure as people are removed.

### Breaking Down the Problem

1. **What are we looking for?** The order in which children are eliminated.
2. **What information do we have?** The number of children n and the step size k=2.
3. **What's the relationship between input and output?** We simulate the elimination process, outputting each eliminated child in order.

### Analogies

Think of this like a game of "duck, duck, goose" where every second person is "it" and must leave the circle. The tricky part is that the circle keeps shrinking, so index positions change after each elimination.

---

## Solution 1: Brute Force (Array with Marking)

### Idea

Maintain an array of all children and mark eliminated ones. For each elimination, traverse the array counting only unmarked children.

### Algorithm

1. Create a boolean array to track who is eliminated
2. Start from position 0, count to k=2 (skipping eliminated)
3. Mark the k-th person as eliminated, output them
4. Repeat until all are eliminated

### Code

```python
def josephus_brute_force(n):
  """
  Brute force: mark eliminated children.

  Time: O(n^2) - for each of n eliminations, may traverse O(n)
  Space: O(n) - boolean array
  """
  eliminated = [False] * n
  result = []
  current = 0

  for _ in range(n):
    count = 0
    while count < 2:  # k = 2
      if not eliminated[current]:
        count += 1
        if count == 2:
          eliminated[current] = True
          result.append(current + 1)  # 1-indexed
      if count < 2:
        current = (current + 1) % n
    current = (current + 1) % n

  return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Each elimination may require O(n) traversal |
| Space | O(n) | Boolean array to track eliminated |

### Why This Works (But Is Slow)

This correctly simulates the process but wastes time skipping over already-eliminated children. As more children are eliminated, we spend more time traversing empty positions.

---

## Solution 2: Optimal Solution (List Removal)

### Key Insight

> **The Trick:** Use a dynamic list and remove elements directly. The next index is calculated using modular arithmetic on the current list size.

Instead of marking elements, we remove them from a list. This way, we always work with only the active children, and the index arithmetic stays simple.

### Index Calculation

After eliminating at index `i`, the next starting position is `i` (since the list shifted). We then move `k-1 = 1` position forward:

```
next_index = (current_index + 1) % remaining_size
```

**Why?** When we remove element at index `i`, the element that was at `i+1` is now at index `i`. So to count "1" from the current position, we stay at `i`. To count "2", we move to `(i+1) % size`.

### Dry Run Example

Let's trace through with input `n = 7`:

```
Initial: children = [1, 2, 3, 4, 5, 6, 7], index = 0

Step 1: Move to index (0 + 1) % 7 = 1
  Eliminate children[1] = 2
  children = [1, 3, 4, 5, 6, 7], index = 1
  Output: 2

Step 2: Move to index (1 + 1) % 6 = 2
  Eliminate children[2] = 4
  children = [1, 3, 5, 6, 7], index = 2
  Output: 4

Step 3: Move to index (2 + 1) % 5 = 3
  Eliminate children[3] = 6
  children = [1, 3, 5, 7], index = 3
  Output: 6

Step 4: Move to index (3 + 1) % 4 = 0
  Eliminate children[0] = 1
  children = [3, 5, 7], index = 0
  Output: 1

Step 5: Move to index (0 + 1) % 3 = 1
  Eliminate children[1] = 5
  children = [3, 7], index = 1
  Output: 5

Step 6: Move to index (1 + 1) % 2 = 0
  Eliminate children[0] = 3
  children = [7], index = 0
  Output: 3

Step 7: Only one left
  Eliminate children[0] = 7
  Output: 7

Final: 2 4 6 1 5 3 7
```

### Visual Diagram

```
Round 1: [1, 2, 3, 4, 5, 6, 7]    Count: 1->2  Eliminate: 2
             ^
Round 2: [1, 3, 4, 5, 6, 7]      Count: 3->4  Eliminate: 4
                ^
Round 3: [1, 3, 5, 6, 7]         Count: 5->6  Eliminate: 6
                   ^
Round 4: [1, 3, 5, 7]            Count: 7->1  Eliminate: 1
          ^
Round 5: [3, 5, 7]               Count: 3->5  Eliminate: 5
             ^
Round 6: [3, 7]                  Count: 7->3  Eliminate: 3
          ^
Round 7: [7]                     Last one     Eliminate: 7
          ^
```

### Code (Python)

```python
def solve():
  n = int(input())
  children = list(range(1, n + 1))
  result = []
  index = 0

  while children:
    # Move to next position to eliminate (k=2 means skip 1)
    index = (index + 1) % len(children)
    result.append(children.pop(index))

    # Adjust index if we removed the last element
    if index == len(children) and children:
      index = 0

  print(' '.join(map(str, result)))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Each removal from vector/list is O(n) |
| Space | O(n) | Store all children |

---

## Solution 3: Efficient Solution (Ordered Set / Indexed Set)

### Key Insight

> **The Trick:** Use a data structure that supports O(log n) removal and O(log n) access by index.

For larger inputs, we can use a balanced BST or indexed set (like GNU C++ `pb_ds` or a segment tree) to achieve O(n log n) time.

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Each operation on ordered set is O(log n) |
| Space | O(n) | Ordered set storage |

---

## Common Mistakes

### Mistake 1: Off-by-One in Index Calculation

```python
# WRONG - counts k positions including current
index = (index + k) % len(children)

# CORRECT - skip k-1, eliminate k-th (for k=2: skip 1, eliminate next)
index = (index + k - 1) % len(children)
# But since we already moved past the removed element, we need:
index = (index + 1) % len(children)  # for k=2 specifically
```

**Problem:** Misunderstanding whether we count the current position or start fresh.
**Fix:** Trace through a small example to verify your indexing logic.

### Mistake 2: Not Adjusting Index After Removal

```python
# WRONG
children.pop(index)
# index stays the same, but list shifted!

# CORRECT
children.pop(index)
if index >= len(children):
  index = 0
# Or: don't adjust since pop shifts elements left
```

**Problem:** After removing at index `i`, all elements after it shift left.
**Fix:** Understand that if you remove at index `i`, the element that was at `i+1` is now at `i`.

### Mistake 3: Confusing 0-indexed and 1-indexed

```python
# WRONG - children stored as 0-indexed
children = list(range(n))
result.append(children.pop(index))  # Outputs 0 to n-1

# CORRECT - children stored as 1-indexed
children = list(range(1, n + 1))
result.append(children.pop(index))  # Outputs 1 to n
```

**Problem:** The problem asks for child numbers 1 to n, not 0 to n-1.
**Fix:** Initialize list with 1-indexed values.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single child | `n = 1` | `1` | Only one child, immediately eliminated |
| Two children | `n = 2` | `2 1` | Skip 1, eliminate 2, then eliminate 1 |
| Small circle | `n = 3` | `2 1 3` | Quick to trace manually |
| Power of 2 | `n = 8` | `2 4 6 8 3 7 5 1` | Survivor is always 1 for n = 2^k |

---

## When to Use This Pattern

### Use This Approach When:
- Simulating elimination/selection processes in a circular arrangement
- The step size k is fixed and small
- You need the complete elimination sequence (not just the survivor)

### Don't Use When:
- You only need the final survivor (use mathematical formula)
- k varies during the process
- n is extremely large and you need O(n) or O(log n) time

### Pattern Recognition Checklist:
- [ ] Circular arrangement? -> **Consider modular arithmetic**
- [ ] Repeated elimination? -> **Simulation with index tracking**
- [ ] Need only final survivor? -> **Mathematical Josephus formula**
- [ ] Large n with need for efficiency? -> **Ordered set / Segment tree**

---

## Mathematical Alternative (For Survivor Only)

If you only need the last survivor (not the full sequence), use the Josephus recurrence:

```
J(1, k) = 0  (0-indexed)
J(n, k) = (J(n-1, k) + k) % n
```

For k=2 specifically:
```python
def josephus_survivor(n):
  """Returns the survivor position (1-indexed) for k=2."""
  survivor = 0
  for i in range(2, n + 1):
    survivor = (survivor + 2) % i
  return survivor + 1  # Convert to 1-indexed
```

This runs in O(n) time and O(1) space but only gives the final survivor.

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| Array rotation problems | Practice with circular indexing |
| Basic simulation problems | Build simulation skills |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Josephus Problem II](https://cses.fi/problemset/task/2163) | Variable step size k |
| [Find the Winner (LeetCode 1823)](https://leetcode.com/problems/find-the-winner-of-the-circular-game/) | Same problem, only return survivor |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Elimination Game (LeetCode 390)](https://leetcode.com/problems/elimination-game/) | Alternating direction elimination |
| Josephus with large k | Requires log-time jumping |

---

## Key Takeaways

1. **The Core Idea:** Simulate circular elimination by maintaining a list and using modular arithmetic for index wrapping.
2. **Time Optimization:** Use ordered set for O(n log n) instead of O(n^2) with plain list.
3. **Space Trade-off:** O(n) space is unavoidable if we need the full elimination sequence.
4. **Pattern:** This is a classic circular array simulation problem.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why `index = (index + 1) % len(children)` works for k=2
- [ ] Handle the edge case when the last element is removed
- [ ] Implement in your preferred language in under 10 minutes

---

## Additional Resources

- [Wikipedia: Josephus Problem](https://en.wikipedia.org/wiki/Josephus_problem)
- [CP-Algorithms: Josephus Problem](https://cp-algorithms.com/others/josephus_problem.html)
- [CSES Josephus Problem I](https://cses.fi/problemset/task/2162) - Every second person elimination
