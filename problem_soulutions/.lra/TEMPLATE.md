---
layout: simple
title: "[Problem Name] - [Category] Problem"
permalink: /problem_soulutions/[category]/[problem_name]_analysis
difficulty: Easy | Medium | Hard
tags: [tag1, tag2, tag3]
prerequisites: [prerequisite_problem_1, prerequisite_problem_2]
---

# [Problem Name]

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy / Medium / Hard |
| **Category** | DP / Graph / etc. |
| **Time Limit** | X seconds |
| **Key Technique** | Two Pointers / Binary Search / etc. |

### Learning Goals

After solving this problem, you will be able to:
- [ ] [Specific skill 1 - e.g., "Identify when to use the two-pointer technique"]
- [ ] [Specific skill 2 - e.g., "Implement Dijkstra's algorithm with a priority queue"]
- [ ] [Specific skill 3 - e.g., "Optimize space complexity using rolling arrays"]

---

## Problem Statement

**Problem:** [Clear, concise problem statement in your own words]

**Input:**
- Line 1: [description]
- Line 2: [description]

**Output:**
- [What to output]

**Constraints:**
- 1 ≤ n ≤ 10^5
- [Other constraints]

### Example

```
Input:
4 8
2 7 5 1

Output:
2 4
```

**Explanation:** [Step-by-step explanation of why this is the answer]

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What makes this problem special? What pattern does it follow?

[2-3 sentences explaining the core insight]

### Breaking Down the Problem

1. **What are we looking for?** [Answer]
2. **What information do we have?** [Answer]
3. **What's the relationship between input and output?** [Answer]

### Analogies

Think of this problem like [real-world analogy that helps understanding].

---

## Solution 1: Brute Force

### Idea

[1-2 sentences explaining the simplest approach]

### Algorithm

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Code

```python
def solve_brute_force(n, arr):
    """
    Brute force solution.

    Time: O(n^2)
    Space: O(1)
    """
    # Implementation
    pass
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n²) | [Why] |
| Space | O(1) | [Why] |

### Why This Works (But Is Slow)

[Explain why correctness is guaranteed but efficiency is poor]

---

## Solution 2: Optimal Solution

### Key Insight

> **The Trick:** [One sentence describing the key optimization insight]

### DP State Definition (if applicable)

| State | Meaning |
|-------|---------|
| `dp[i]` | [What dp[i] represents] |

**In plain English:** [Simple explanation]

### State Transition

```
dp[i] = [recurrence relation]
```

**Why?** [Explanation of why this transition is correct]

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 1 | [Why] |

### Algorithm

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Dry Run Example

Let's trace through with input `n = 4, arr = [2, 7, 5, 1], target = 8`:

```
Initial state:
  seen = {}

Step 1: Process arr[0] = 2
  complement = 8 - 2 = 6
  6 not in seen
  Add 2 to seen: {2: 0}

Step 2: Process arr[1] = 7
  complement = 8 - 7 = 1
  1 not in seen
  Add 7 to seen: {2: 0, 7: 1}

Step 3: Process arr[2] = 5
  complement = 8 - 5 = 3
  3 not in seen
  Add 5 to seen: {2: 0, 7: 1, 5: 2}

Step 4: Process arr[3] = 1
  complement = 8 - 1 = 7
  7 IS in seen at index 1!
  Found pair: (1, 3) -> output (2, 4) [1-indexed]
```

### Visual Diagram

```
Array: [2, 7, 5, 1]  Target: 8

Index:  0   1   2   3
        │   │   │   │
        2   7   5   1
            ↑       ↑
            └───────┘
            7 + 1 = 8 ✓
```

### Code

```python
def solve_optimal(n, arr, target):
    """
    Optimal solution using hash map.

    Time: O(n) - single pass
    Space: O(n) - hash map storage
    """
    seen = {}  # value -> index

    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return (seen[complement] + 1, i + 1)  # 1-indexed
        seen[num] = i

    return "IMPOSSIBLE"
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array |
| Space | O(n) | Hash map stores up to n elements |

---

## Common Mistakes

### Mistake 1: [Name]

```python
# WRONG
for i in range(n):
    for j in range(n):  # Should be range(i+1, n)
        if arr[i] + arr[j] == target:
            return (i, j)  # May return same index twice!
```

**Problem:** [Explanation]
**Fix:** [How to fix]

### Mistake 2: [Name]

```python
# WRONG
seen[num] = i  # Adding BEFORE checking
if complement in seen:
    return ...
```

**Problem:** This may match an element with itself.
**Fix:** Check complement BEFORE adding current element to the map.

### Mistake 3: Off-by-One in Output

```python
# WRONG
return (i, j)  # 0-indexed

# CORRECT
return (i + 1, j + 1)  # 1-indexed as required
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No solution | `[1,2,3], target=10` | IMPOSSIBLE | No pair sums to 10 |
| First two elements | `[4,4], target=8` | `1 2` | Immediate match |
| Duplicate values | `[3,3,3], target=6` | `1 2` | First valid pair |
| Large values | `[10^9, 1], target=10^9+1` | `1 2` | Handle large numbers |

---

## When to Use This Pattern

### Use This Approach When:
- You need to find pairs/triplets with a target sum
- You need O(1) lookup for complements
- Order of elements doesn't matter for the answer

### Don't Use When:
- You need to find ALL pairs (use different approach)
- Space is extremely constrained (use two-pointer on sorted array)
- Input is already sorted (two-pointer is simpler)

### Pattern Recognition Checklist:
- [ ] Looking for two numbers that satisfy a condition? → **Consider hash map**
- [ ] Input is sorted? → **Consider two pointers**
- [ ] Need to find multiple pairs? → **Consider sorting + two pointers**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Contains Duplicate](link) | Basic hash map usage |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Sorted input, use two pointers |
| [Sum of Three Values](https://cses.fi/problemset/task/1641) | Extended to three numbers |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [4Sum](https://leetcode.com/problems/4sum/) | Generalized k-sum |
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Prefix sums + hash map |

---

## Key Takeaways

1. **The Core Idea:** [One sentence summary]
2. **Time Optimization:** [How we improved from brute force]
3. **Space Trade-off:** [What space we used to gain time]
4. **Pattern:** [What pattern category this belongs to]

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain the time and space complexity
- [ ] Identify when to use this pattern in new problems
- [ ] Implement in your preferred language in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Hash Tables](https://cp-algorithms.com/data_structures/hash_table.html)
- [CSES Problem Set](https://cses.fi/problemset/)
