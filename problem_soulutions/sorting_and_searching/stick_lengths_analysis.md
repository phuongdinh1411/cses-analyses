---
layout: simple
title: "Stick Lengths - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/stick_lengths_analysis
difficulty: Easy
tags: [sorting, median, optimization, greedy]
prerequisites: []
---

# Stick Lengths

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES Problem Set - Stick Lengths](https://cses.fi/problemset/task/1074) |
| **Difficulty** | Easy |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Median / Sorting |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand why the median minimizes the sum of absolute deviations
- [ ] Apply sorting to find the optimal target value in optimization problems
- [ ] Recognize problems where median is the optimal choice over mean
- [ ] Handle potential integer overflow when summing large values

---

## Problem Statement

**Problem:** Given n sticks with various lengths, modify all sticks to have the same length. You can increase or decrease each stick's length by 1 unit at a cost of 1 unit. Find the minimum total cost.

**Input:**
- Line 1: Integer n (number of sticks)
- Line 2: n integers representing stick lengths

**Output:**
- The minimum total cost to make all sticks equal length

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= a[i] <= 10^9

### Example

```
Input:
5
2 3 1 5 2

Output:
5
```

**Explanation:**
- Target length = 2 (the median)
- Stick 1: |2 - 2| = 0
- Stick 2: |3 - 2| = 1
- Stick 3: |1 - 2| = 1
- Stick 4: |5 - 2| = 3
- Stick 5: |2 - 2| = 0
- Total cost: 0 + 1 + 1 + 3 + 0 = 5

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Given a set of numbers, what single value minimizes the sum of absolute differences to all numbers?

The answer is the **median**. This is a fundamental property in statistics and optimization. The median is the "balance point" that minimizes total movement.

### Why Median, Not Mean?

Consider this simple example: `[1, 2, 100]`

| Target | Cost Calculation | Total |
|--------|------------------|-------|
| Mean (34.3) | \|1-34\| + \|2-34\| + \|100-34\| = 33 + 32 + 66 | 131 |
| Median (2) | \|1-2\| + \|2-2\| + \|100-2\| = 1 + 0 + 98 | 99 |

The median wins because it is **robust to outliers**. The mean gets "pulled" toward extreme values.

### Mathematical Proof (Intuitive)

Imagine moving the target point `t` along a number line:
- Moving `t` one unit **right**: Cost increases by (count of values <= t) and decreases by (count of values > t)
- At the median: roughly half the values are on each side, so moving in either direction increases total cost

```
Values: 1  2  2  3  5
        |  |  |  |  |
        ←-2-→ ←--2--→   (2 values left of median, 2 values right)
              ↑
           median (2)
```

### Analogies

Think of this problem like finding the optimal meeting point for a group of friends on a street. Each friend wants to minimize their travel distance. The median location ensures the total travel for everyone is minimized.

---

## Solution 1: Brute Force

### Idea

Try every possible target length (from minimum to maximum stick length) and calculate the total cost for each. Return the minimum.

### Algorithm

1. Find the range of stick lengths [min, max]
2. For each possible target in this range:
   - Calculate sum of |stick[i] - target| for all sticks
3. Return the minimum cost found

### Code

```python
def solve_brute_force(sticks):
    """
    Brute force: try all possible target lengths.

    Time: O(n * (max - min))
    Space: O(1)
    """
    min_len = min(sticks)
    max_len = max(sticks)
    min_cost = float('inf')

    for target in range(min_len, max_len + 1):
        cost = sum(abs(s - target) for s in sticks)
        min_cost = min(min_cost, cost)

    return min_cost
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * R) | R = max - min, can be up to 10^9 |
| Space | O(1) | Only tracking minimum cost |

### Why This Works (But Is Slow)

This guarantees finding the optimal solution by exhaustive search, but with stick lengths up to 10^9, iterating through all possible targets is far too slow.

---

## Solution 2: Optimal Solution (Median)

### Key Insight

> **The Trick:** The median minimizes the sum of absolute deviations. Sort the array and pick the middle element as the target.

### Why This Works

For any set of numbers, the median has this special property:
- Moving the target away from the median always increases total cost
- At the median, the number of values below roughly equals the number above
- Any movement benefits one side but hurts the other side more

### Algorithm

1. Sort the stick lengths
2. Find the median (middle element for odd n, either middle element for even n)
3. Calculate total cost: sum of |stick[i] - median|

### Dry Run Example

Let's trace through with input `sticks = [2, 3, 1, 5, 2]`:

```
Step 1: Sort the sticks
  Original: [2, 3, 1, 5, 2]
  Sorted:   [1, 2, 2, 3, 5]
            indices: 0  1  2  3  4

Step 2: Find median
  n = 5 (odd)
  median_index = n // 2 = 2
  median = sorted[2] = 2

Step 3: Calculate cost
  |1 - 2| = 1
  |2 - 2| = 0
  |2 - 2| = 0
  |3 - 2| = 1
  |5 - 2| = 3
  ─────────────
  Total = 5
```

### Visual Diagram

```
Sorted sticks: [1, 2, 2, 3, 5]

Number line:
    1     2     3     4     5
    |     |           |     |
    *    **           *     *
          ↑
       median = 2

Cost visualization:
    1 ←─1─→ 2 (median)
          2 ←─0─→ 2
          2 ←─0─→ 2
          2 ←──1──→ 3
          2 ←────3────→ 5
                        ─────
                        Total: 5
```

### Code

**Python Solution:**

```python
def solve(sticks):
    """
    Optimal solution using median.

    Time: O(n log n) - dominated by sorting
    Space: O(n) - for sorted array (or O(1) if sorting in-place)
    """
    sticks.sort()
    n = len(sticks)
    median = sticks[n // 2]

    return sum(abs(s - median) for s in sticks)


def main():
    n = int(input())
    sticks = list(map(int, input().split()))
    print(solve(sticks))


if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<long long> sticks(n);
    for (int i = 0; i < n; i++) {
        cin >> sticks[i];
    }

    sort(sticks.begin(), sticks.end());

    long long median = sticks[n / 2];
    long long cost = 0;

    for (int i = 0; i < n; i++) {
        cost += abs(sticks[i] - median);
    }

    cout << cost << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sorting dominates; sum calculation is O(n) |
| Space | O(n) | For sorted array; O(1) if sorting in-place |

### Note on Even-Length Arrays

For arrays with even length, both middle elements are valid medians. Any value between them (inclusive) gives the same minimum cost. We simply pick `sticks[n // 2]`.

---

## Common Mistakes

### Mistake 1: Using Mean Instead of Median

```python
# WRONG
target = sum(sticks) // len(sticks)  # This is the mean!
cost = sum(abs(s - target) for s in sticks)
```

**Problem:** The mean minimizes sum of SQUARED differences, not absolute differences.

**Fix:** Use the median (middle element of sorted array).

### Mistake 2: Integer Overflow

```cpp
// WRONG (in some languages)
int cost = 0;
for (int s : sticks) {
    cost += abs(s - median);  // Can overflow if cost > 2^31
}
```

**Problem:** With n = 2 x 10^5 sticks and values up to 10^9, the sum can reach ~2 x 10^14.

**Fix:** Use `long long` for the cost variable.

```cpp
// CORRECT
long long cost = 0;
for (int i = 0; i < n; i++) {
    cost += abs(sticks[i] - median);
}
```

### Mistake 3: Forgetting to Sort

```python
# WRONG
def solve(sticks):
    n = len(sticks)
    median = sticks[n // 2]  # This is NOT the median!
    return sum(abs(s - median) for s in sticks)
```

**Problem:** The middle element of an unsorted array is not the median.

**Fix:** Sort the array first.

### Mistake 4: Wrong Median Index for Even Length

```python
# Not wrong, but worth understanding
sticks = [1, 2, 3, 4]  # n = 4
# Both sticks[1] = 2 and sticks[2] = 3 are valid medians
# Any target in [2, 3] gives the same minimum cost
```

**Note:** For this problem, using `sticks[n // 2]` always works. You don't need to average two middle values.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single stick | `n=1, [5]` | `0` | Already equal to itself |
| Two sticks | `n=2, [1, 100]` | `99` | Either median works |
| All same | `n=4, [7,7,7,7]` | `0` | No modification needed |
| Large values | `n=2, [1, 10^9]` | `999999999` | Test overflow handling |
| Already sorted | `n=3, [1,2,3]` | `2` | Median is 2: \|1-2\|+\|2-2\|+\|3-2\|=2 |

---

## When to Use This Pattern

### Use Median When:
- Minimizing sum of **absolute** differences/deviations
- Finding optimal meeting point in 1D
- Robust estimation needed (resistant to outliers)
- Problem asks for minimum total "movement" or "cost"

### Use Mean When:
- Minimizing sum of **squared** differences
- Variance/standard deviation calculations

### Pattern Recognition Checklist:
- [ ] Need to find a target value that minimizes total distance? -> **Consider median**
- [ ] Problem involves making elements equal with unit cost? -> **Median is optimal**
- [ ] Seeing "minimum operations" or "minimum cost" language? -> **Think median vs mean**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Distinct Numbers](https://cses.fi/problemset/task/1621) | Basic sorting practice |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Minimum Moves to Equal Array Elements II](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/) | Same problem, different platform |
| [Apartments](https://cses.fi/problemset/task/1084) | Sorting + matching |
| [Ferris Wheel](https://cses.fi/problemset/task/1090) | Sorting + greedy pairing |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Best Position in 2D](https://leetcode.com/problems/best-meeting-point/) | Extend to 2D grid (x and y medians independently) |
| [Array Division](https://cses.fi/problemset/task/1085) | Binary search on answer |
| [Allocate Mailboxes](https://leetcode.com/problems/allocate-mailboxes/) | Multiple medians with DP |

---

## Key Takeaways

1. **The Core Idea:** The median minimizes the sum of absolute differences - this is a mathematical fact worth memorizing.

2. **Time Optimization:** We improved from O(n * R) brute force to O(n log n) by using the median property directly.

3. **Space Trade-off:** O(n) for sorting is acceptable; can be O(1) with in-place sort.

4. **Pattern:** This is a classic "minimization with absolute differences" problem - always think median!

5. **Watch for Overflow:** Sum of differences can be large; use appropriate data types.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why median minimizes sum of absolute deviations
- [ ] Implement the solution in under 5 minutes
- [ ] Handle the integer overflow edge case
- [ ] Recognize this pattern in disguised problems

---

## Additional Resources

- [Why Median Minimizes Absolute Deviations (Math Explanation)](https://math.stackexchange.com/questions/113270/the-median-minimizes-the-sum-of-absolute-deviations)
- [CSES Stick Lengths](https://cses.fi/problemset/task/1074) - Median optimization
- [Sorting Algorithms - CP-Algorithms](https://cp-algorithms.com/sorting/sorting.html)
