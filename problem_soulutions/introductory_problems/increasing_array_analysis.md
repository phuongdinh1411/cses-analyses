---
layout: simple
title: "Increasing Array - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/increasing_array_analysis
difficulty: Easy
tags: [greedy, array, introductory]
prerequisites: []
---

# Increasing Array

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Greedy / Array |
| **Time Limit** | 1 second |
| **Key Technique** | Greedy, Single Pass |
| **CSES Link** | [Increasing Array](https://cses.fi/problemset/task/1094) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when a greedy approach yields optimal results
- [ ] Track running maximum while iterating through an array
- [ ] Handle potential integer overflow in accumulation problems
- [ ] Apply single-pass array transformation techniques

---

## Problem Statement

**Problem:** Given an array of n integers, find the minimum number of moves required to make the array non-decreasing. In one move, you can increase any element by 1.

**Input:**
- Line 1: An integer n (size of array)
- Line 2: n space-separated integers (array elements)

**Output:**
- A single integer: the minimum number of moves required

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= arr[i] <= 10^9

### Example

```
Input:
5
3 2 5 1 7

Output:
5
```

**Explanation:** We need to increase arr[1] from 2 to 3 (1 move) and arr[3] from 1 to 5 (4 moves). Total: 5 moves. Final array: [3, 3, 5, 5, 7].

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Since we can only increase elements (not decrease), what determines the minimum operations?

Each element must be at least as large as the previous one. When we encounter an element smaller than its predecessor, we must increase it to match. The key insight is that the optimal target for each element is exactly the maximum value seen so far - no more, no less.

### Breaking Down the Problem

1. **What are we looking for?** The total number of +1 operations needed.
2. **What information do we have?** The original array values.
3. **What's the relationship between input and output?** For each element smaller than the running maximum, we need (max - element) operations.

### Why Greedy Works

Since we can only increase elements, once we've processed an element, its value becomes a constraint for all future elements. The minimum operations required for position i depends only on positions 0 to i-1. This optimal substructure makes greedy the right approach.

---

## Solution 1: Brute Force (Simulation)

### Idea

Iterate through the array. When an element is smaller than the previous, "simulate" increasing it one at a time until it matches.

### Algorithm

1. Start from index 1
2. Compare each element with the previous
3. If smaller, calculate the difference and add to total moves
4. Update the current element to match the previous

### Code

```python
def solve_brute_force(n, arr):
    """
    Brute force: simulate the process.

    Time: O(n)
    Space: O(n) - copies the array
    """
    arr = arr.copy()  # Don't modify original
    moves = 0

    for i in range(1, n):
        if arr[i] < arr[i-1]:
            diff = arr[i-1] - arr[i]
            moves += diff
            arr[i] = arr[i-1]

    return moves
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array |
| Space | O(n) | Creates a copy of the array |

### Why This Works (But Uses Extra Space)

This approach correctly computes the answer but wastes space by copying the array. We can optimize by tracking only what we need.

---

## Solution 2: Optimal Solution (Greedy with Running Maximum)

### Key Insight

> **The Trick:** Instead of modifying the array, track the running maximum. Each element must be raised to at least this maximum.

### Algorithm

1. Initialize `max_so_far` with the first element
2. Initialize `moves` counter to 0
3. For each subsequent element:
   - If element < max_so_far: add (max_so_far - element) to moves
   - Otherwise: update max_so_far = element
4. Return total moves

### Dry Run Example

Let's trace through with input `n = 5, arr = [3, 2, 5, 1, 7]`:

```
Initial state:
  max_so_far = 3
  moves = 0

Step 1: Process arr[1] = 2
  2 < 3 (max_so_far)
  moves += 3 - 2 = 1
  moves = 1, max_so_far = 3

Step 2: Process arr[2] = 5
  5 >= 3 (max_so_far)
  Update max_so_far = 5
  moves = 1, max_so_far = 5

Step 3: Process arr[3] = 1
  1 < 5 (max_so_far)
  moves += 5 - 1 = 4
  moves = 5, max_so_far = 5

Step 4: Process arr[4] = 7
  7 >= 5 (max_so_far)
  Update max_so_far = 7
  moves = 5, max_so_far = 7

Final answer: 5
```

### Visual Diagram

```
Array: [3, 2, 5, 1, 7]
Index:  0  1  2  3  4

Processing left to right:

Position 0: max = 3
            [3] - baseline established

Position 1: 2 < 3, need +1
            [3, 3] - arr[1] raised to 3
            moves = 1

Position 2: 5 > 3, update max = 5
            [3, 3, 5] - no change needed
            moves = 1

Position 3: 1 < 5, need +4
            [3, 3, 5, 5] - arr[3] raised to 5
            moves = 5

Position 4: 7 > 5, update max = 7
            [3, 3, 5, 5, 7] - no change needed
            moves = 5 (final)
```

### Code (Python)

```python
def solve_optimal(n, arr):
    """
    Optimal solution using running maximum.

    Time: O(n) - single pass
    Space: O(1) - only tracking max and moves
    """
    moves = 0
    max_so_far = arr[0]

    for i in range(1, n):
        if arr[i] < max_so_far:
            moves += max_so_far - arr[i]
        else:
            max_so_far = arr[i]

    return moves


# CSES Input/Output format
def main():
    n = int(input())
    arr = list(map(int, input().split()))
    print(solve_optimal(n, arr))


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    long long moves = 0;
    long long max_so_far = arr[0];

    for (int i = 1; i < n; i++) {
        if (arr[i] < max_so_far) {
            moves += max_so_far - arr[i];
        } else {
            max_so_far = arr[i];
        }
    }

    cout << moves << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array |
| Space | O(1) | Only two variables needed |

---

## Common Mistakes

### Mistake 1: Integer Overflow

```cpp
// WRONG - int overflow when summing large differences
int moves = 0;  // May overflow!

// CORRECT - use long long
long long moves = 0;
```

**Problem:** With n up to 2x10^5 and values up to 10^9, the total moves can exceed 2^31-1.
**Fix:** Use `long long` in C++ or Python's arbitrary precision integers.

### Mistake 2: Processing Wrong Direction

```python
# WRONG - processing right to left
for i in range(n-1, 0, -1):
    if arr[i] > arr[i-1]:  # Wrong comparison
        moves += arr[i] - arr[i-1]
```

**Problem:** We can only increase elements, so we must process left to right, raising elements to meet the running maximum.
**Fix:** Always iterate left to right and compare with the maximum seen so far.

### Mistake 3: Forgetting to Update Maximum

```python
# WRONG - not updating max when current is larger
for i in range(1, n):
    if arr[i] < max_so_far:
        moves += max_so_far - arr[i]
    # Missing: max_so_far = arr[i] when arr[i] >= max_so_far
```

**Problem:** If we don't update the maximum, we undercount required operations.
**Fix:** Always update `max_so_far` when encountering a larger element.

### Mistake 4: Modifying Array Unnecessarily

```python
# INEFFICIENT - modifying array
arr[i] = max_so_far  # Unnecessary

# BETTER - just track the max
max_so_far = max(max_so_far, arr[i])
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Already sorted | `[1, 2, 3, 4, 5]` | `0` | No changes needed |
| Single element | `[42]` | `0` | Trivially non-decreasing |
| All same values | `[5, 5, 5, 5]` | `0` | Already non-decreasing |
| Strictly decreasing | `[5, 4, 3, 2, 1]` | `10` | 1+2+3+4 = 10 moves |
| Large values | `[10^9, 1]` | `999999999` | Test overflow handling |
| Two elements | `[5, 3]` | `2` | Simple case: 5-3 = 2 |

---

## When to Use This Pattern

### Use This Approach When:
- You need to make an array non-decreasing
- You can only increase elements (one-directional changes)
- You want minimum total operations
- A single left-to-right pass can determine the answer

### Don't Use When:
- You can both increase and decrease elements (different problem)
- You need to make the array strictly increasing (may need different handling)
- The problem asks for the final array, not just the count

### Pattern Recognition Checklist:
- [ ] Array transformation problem? -> **Consider greedy**
- [ ] Can only modify in one direction? -> **Running max/min approach**
- [ ] Optimal substructure (current depends on past only)? -> **Single pass greedy**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Weird Algorithm](https://cses.fi/problemset/task/1068) | Basic iteration and simulation |
| [Missing Number](https://cses.fi/problemset/task/1083) | Simple array processing |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Permutations](https://cses.fi/problemset/task/1070) | Greedy construction |
| [Non-decreasing Array (LeetCode 665)](https://leetcode.com/problems/non-decreasing-array/) | At most one modification allowed |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Minimum Moves to Equal Array Elements (LC 453)](https://leetcode.com/problems/minimum-moves-to-equal-array-elements/) | Different operation model |
| [Candy (LC 135)](https://leetcode.com/problems/candy/) | Two-pass greedy |
| [Minimum Operations to Make Array Equal (LC 1551)](https://leetcode.com/problems/minimum-operations-to-make-array-equal/) | Mathematical insight |

---

## Key Takeaways

1. **The Core Idea:** Track the running maximum; each element must be raised to at least this value.
2. **Time Optimization:** Single pass O(n) by avoiding array modification.
3. **Space Trade-off:** O(1) space by only tracking the maximum, not the whole modified array.
4. **Pattern:** Greedy with running aggregate - common in array transformation problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why greedy gives the optimal answer
- [ ] Handle integer overflow correctly
- [ ] Implement in both Python and C++ in under 5 minutes
- [ ] Identify similar problems where this pattern applies

---

## Additional Resources

- [CSES Problem Set - Introductory Problems](https://cses.fi/problemset/list/)
- [CP-Algorithms: Greedy Algorithms](https://cp-algorithms.com/)
- [USACO Guide - Greedy Algorithms](https://usaco.guide/bronze/intro-greedy)
