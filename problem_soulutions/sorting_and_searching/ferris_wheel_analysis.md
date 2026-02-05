---
layout: simple
title: "Ferris Wheel"
difficulty: Easy
tags: [sorting, two-pointers, greedy]
cses_link: https://cses.fi/problemset/task/1090
permalink: /problem_soulutions/sorting_and_searching/ferris_wheel_analysis
---

# Ferris Wheel

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem Type | Greedy Pairing |
| Core Technique | Two Pointers |
| Time Complexity | O(n log n) |
| Space Complexity | O(1) auxiliary |
| Key Insight | Pair heaviest with lightest when possible |

## Learning Goals

After solving this problem, you will understand:
- **Greedy pairing**: Why pairing extremes (heaviest + lightest) leads to optimal solutions
- **Two-pointer optimization**: How to efficiently process sorted arrays from both ends

## Problem Statement

There are `n` children who want to ride a Ferris wheel. Each gondola has maximum weight capacity `x` and can hold **at most 2 children**. Given the weight of each child, find the **minimum number of gondolas** needed.

**Input:**
- Line 1: `n` (number of children) and `x` (gondola capacity)
- Line 2: `n` integers representing weights `w[1], w[2], ..., w[n]`

**Output:** Minimum number of gondolas required

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= x <= 10^9
- 1 <= w[i] <= x (every child can fit alone)

**Example:**
```
Input:
4 10
7 2 3 9

Output:
3
```

## Key Insight

**Greedy Principle**: Always try to pair the heaviest remaining child with the lightest remaining child.

- If they fit together: Both ride, minimizing gondola usage
- If they don't fit: The heaviest must ride alone (no one else can help)

This greedy choice is always optimal because:
1. The heaviest child must eventually ride
2. If even the lightest child can't pair with them, no one can
3. Using the lightest child preserves heavier children for other potential pairings

## Algorithm

1. **Sort** the weights in ascending order
2. **Initialize** two pointers: `left = 0` (lightest), `right = n-1` (heaviest)
3. **While** `left <= right`:
   - If `weights[left] + weights[right] <= x`: pair them, move both pointers inward
   - Else: heaviest rides alone, move only right pointer
   - Increment gondola count
4. **Return** gondola count

## Visual Diagram

```
Weights: [7, 2, 3, 9], Capacity: 10

Step 1: Sort weights
[2, 3, 7, 9]
 ^        ^
 L        R

Step 2: Try pairing
[2, 3, 7, 9]    2 + 9 = 11 > 10  --> 9 rides ALONE
 ^        ^                          gondolas = 1
 L        R

[2, 3, 7, 9]    2 + 7 = 9 <= 10 --> (2,7) PAIRED
 ^     ^                            gondolas = 2
 L     R

[2, 3, 7, 9]    left > right? No, left == right
    ^                           3 rides ALONE
   L,R                          gondolas = 3

Result: 3 gondolas
```

## Dry Run

| Step | Left | Right | weights[L] | weights[R] | Sum | Action | Gondolas |
|------|------|-------|------------|------------|-----|--------|----------|
| 1 | 0 | 3 | 2 | 9 | 11 | 9 alone, R-- | 1 |
| 2 | 0 | 2 | 2 | 7 | 9 | Pair (2,7), L++, R-- | 2 |
| 3 | 1 | 1 | 3 | 3 | - | 3 alone, done | 3 |

## Implementation

### Python

```python
def min_gondolas(n: int, x: int, weights: list[int]) -> int:
    weights.sort()
    left, right = 0, n - 1
    gondolas = 0

    while left <= right:
        if weights[left] + weights[right] <= x:
            left += 1  # Lightest paired
        right -= 1     # Heaviest always assigned
        gondolas += 1

    return gondolas

# Read input
n, x = map(int, input().split())
weights = list(map(int, input().split()))

print(min_gondolas(n, x, weights))
```

## Why Greedy Works

**Claim**: Pairing the heaviest with the lightest (when possible) yields the minimum gondolas.

**Proof Sketch**:
1. Consider the heaviest child H. They must ride in some gondola.
2. If H can pair with the lightest child L, this is optimal:
   - If H could pair with anyone, L is the best choice (uses smallest weight)
   - Pairing H with a heavier child wastes pairing potential
3. If H cannot pair with L, H cannot pair with anyone (L is lightest)
4. By induction, this greedy choice at each step leads to the global optimum.

**Exchange Argument**: Any solution not using this pairing strategy can be transformed into one that does, without increasing gondola count.

## Complexity Analysis

| Operation | Complexity |
|-----------|------------|
| Sorting | O(n log n) |
| Two-pointer traversal | O(n) |
| **Total Time** | **O(n log n)** |
| **Space** | **O(1)** auxiliary |

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Forgetting single-person gondolas | When left == right, one child remains | The loop handles this: right-- always happens |
| Not sorting first | Two-pointer only works on sorted arrays | Always sort before applying two pointers |
| Moving both pointers when pairing fails | Heaviest goes alone, but lightest might pair later | Only move right when pairing fails |
| Using left < right instead of left <= right | Misses the last single child | Use `<=` to handle odd counts |

## Related Problems

- [CSES - Apartments](https://cses.fi/problemset/task/1084): Two-pointer matching
- [CSES - Concert Tickets](https://cses.fi/problemset/task/1091): Greedy assignment
- [LeetCode - Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/): Classic two-pointer
- [LeetCode - Boats to Save People](https://leetcode.com/problems/boats-to-save-people/): Nearly identical problem
