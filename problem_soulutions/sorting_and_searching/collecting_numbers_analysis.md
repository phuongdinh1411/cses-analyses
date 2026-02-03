---
layout: simple
title: "Collecting Numbers - Position Inversion Counting"
permalink: /problem_soulutions/sorting_and_searching/collecting_numbers_analysis
difficulty: Easy
tags: [greedy, position-tracking, inversion-counting]
---

# Collecting Numbers

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Position Tracking / Inversion Counting |
| **CSES Link** | [Collecting Numbers](https://cses.fi/problemset/task/2216) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when to use position mapping for sequence problems
- [ ] Understand the relationship between position inversions and round counting
- [ ] Apply the "rounds = 1 + inversions" pattern efficiently
- [ ] Track positions of consecutive elements to determine collection order

---

## Problem Statement

**Problem:** You have an array containing n numbers 1, 2, ..., n in some order. Your task is to collect the numbers from 1 to n in increasing order. In each round, you go through the array from left to right and collect as many numbers as possible. What is the minimum number of rounds needed?

**Input:**
- Line 1: An integer n (the number of elements)
- Line 2: n integers describing the array (permutation of 1 to n)

**Output:**
- Print one integer: the minimum number of rounds

**Constraints:**
- 1 <= n <= 2 x 10^5

### Example

```
Input:
5
4 2 1 5 3

Output:
3
```

**Explanation:**
- Round 1: Collect 1 (at position 2)
- Round 2: Collect 2 (at position 1), then 3 (at position 4)
- Round 3: Collect 4 (at position 0), then 5 (at position 3)

We need a new round whenever the next number appears BEFORE the current number in the array.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When do we need to start a new round?

A new round is needed whenever we cannot continue collecting in the current round. This happens when the next number we need appears at a position that is to the LEFT of where we currently are in the array.

### The Core Insight: Rounds = 1 + Inversions

The key pattern is:

```
rounds = 1 + (number of times pos[i+1] < pos[i])
```

Where `pos[i]` is the position of value `i` in the array. Every time the next number appears before the current number, we must start a new round.

### Breaking Down the Problem

1. **What are we looking for?** The minimum number of left-to-right passes through the array.
2. **What information do we have?** The position of each number 1 to n in the array.
3. **What is the relationship between input and output?** Each "inversion" (next number before current) forces a new round.

### Analogies

Think of this like reading a book where chapters are scattered. You can only read forward, so every time the next chapter appears on an earlier page than your current position, you must start from the beginning again.

---

## Solution 1: Brute Force (Simulation)

### Idea

Simulate the actual collection process: repeatedly scan left-to-right, collecting numbers in order until no more can be collected in the current round.

### Algorithm

1. Start with target = 1 (first number to collect)
2. Scan array left to right, collect target when found, increment target
3. When scan completes, start new round if not all collected
4. Count total rounds

### Code

```python
def solve_brute_force(n, arr):
    """
    Brute force solution - simulate the collection process.

    Time: O(n^2)
    Space: O(1)
    """
    collected = 0
    rounds = 0
    target = 1

    while collected < n:
        rounds += 1
        for i in range(n):
            if arr[i] == target:
                collected += 1
                target += 1

    return rounds
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Worst case: n rounds, each scanning n elements |
| Space | O(1) | Only tracking counters |

### Why This Works (But Is Slow)

This correctly simulates the collection process, but repeating array scans is inefficient. In the worst case (reverse sorted array), we need n rounds, each scanning the full array.

---

## Solution 2: Optimal Solution (Position Tracking)

### Key Insight

> **The Trick:** Count position inversions instead of simulating. Each time pos[i+1] < pos[i], we need a new round.

We do not need to simulate the collection. We can simply:
1. Record where each value 1 to n appears in the array
2. Count how many times the next value appears BEFORE the current value

### Algorithm

1. Build position map: pos[value] = index in array
2. Start with rounds = 1
3. For each consecutive pair (i, i+1), if pos[i+1] < pos[i], increment rounds
4. Return rounds

### Dry Run Example

Let us trace through with input `n = 5, arr = [4, 2, 1, 5, 3]`:

```
Step 1: Build position map
  pos[1] = 2  (value 1 is at index 2)
  pos[2] = 1  (value 2 is at index 1)
  pos[3] = 4  (value 3 is at index 4)
  pos[4] = 0  (value 4 is at index 0)
  pos[5] = 3  (value 5 is at index 3)

Step 2: Count inversions (where next value appears before current)
  rounds = 1 (start with 1 round)

  Compare pos[1]=2 vs pos[2]=1: 1 < 2? YES -> rounds = 2
    (value 2 is at index 1, which is BEFORE index 2 where value 1 is)

  Compare pos[2]=1 vs pos[3]=4: 4 < 1? NO -> rounds stays 2
    (value 3 is at index 4, which is AFTER index 1, can collect in same round)

  Compare pos[3]=4 vs pos[4]=0: 0 < 4? YES -> rounds = 3
    (value 4 is at index 0, which is BEFORE index 4, need new round)

  Compare pos[4]=0 vs pos[5]=3: 3 < 0? NO -> rounds stays 3
    (value 5 is at index 3, which is AFTER index 0, can collect in same round)

Final answer: 3 rounds
```

### Visual Diagram

```
Array:    [4, 2, 1, 5, 3]
Index:     0  1  2  3  4

Position map:
  Value:    1  2  3  4  5
  Position: 2  1  4  0  3
            |__|  |__|
            inv   inv
          (1->2)(3->4)

Inversions (pos[i+1] < pos[i]):
  - pos[2]=1 < pos[1]=2  -> New round needed
  - pos[4]=0 < pos[3]=4  -> New round needed

Total inversions: 2
Rounds = 1 + 2 = 3
```

### Code

**Python Solution:**

```python
def solve_optimal(n, arr):
    """
    Optimal solution using position tracking.

    Key insight: Count how many times pos[i+1] < pos[i]
    Each such case requires a new round.

    Time: O(n) - single pass to build map, single pass to count
    Space: O(n) - position map storage
    """
    # Build position map: pos[value] = index
    pos = [0] * (n + 1)
    for i in range(n):
        pos[arr[i]] = i

    # Count inversions
    rounds = 1
    for i in range(1, n):
        if pos[i + 1] < pos[i]:
            rounds += 1

    return rounds


# Main code for CSES submission
def main():
    n = int(input())
    arr = list(map(int, input().split()))
    print(solve_optimal(n, arr))


if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    // pos[value] = index in array
    vector<int> pos(n + 1);

    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        pos[x] = i;
    }

    // Count inversions: when pos[i+1] < pos[i]
    int rounds = 1;
    for (int i = 1; i < n; i++) {
        if (pos[i + 1] < pos[i]) {
            rounds++;
        }
    }

    cout << rounds << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | One pass to build position map, one pass to count inversions |
| Space | O(n) | Position map stores n+1 integers |

---

## Common Mistakes

### Mistake 1: Counting Logic Error

```python
# WRONG - counting when current is before next (opposite condition)
if pos[i] < pos[i + 1]:
    rounds += 1
```

**Problem:** This counts when we CAN continue in the same round, not when we need a new round.
**Fix:** The condition should be `pos[i + 1] < pos[i]` (next value appears BEFORE current).

### Mistake 2: Off-by-One in Position Tracking

```python
# WRONG - using 0-indexed values
pos = [0] * n
for i in range(n):
    pos[arr[i]] = i  # Fails when arr[i] = n
```

**Problem:** Values are 1 to n, but array is 0 to n-1.
**Fix:** Use `pos = [0] * (n + 1)` to accommodate values 1 through n.

### Mistake 3: Starting Rounds at 0

```python
# WRONG
rounds = 0
for i in range(1, n):
    if pos[i + 1] < pos[i]:
        rounds += 1
return rounds  # Returns 0 for sorted array, should be 1
```

**Problem:** Even a perfectly sorted array needs 1 round to collect all numbers.
**Fix:** Initialize `rounds = 1` since we always need at least one round.

### Mistake 4: Using Wrong Index Range

```python
# WRONG - goes out of bounds
for i in range(1, n + 1):  # i+1 will be n+1, out of bounds
    if pos[i + 1] < pos[i]:
        rounds += 1
```

**Problem:** Accessing `pos[n + 1]` which does not exist.
**Fix:** Loop should be `for i in range(1, n)` to compare values 1..n-1 with values 2..n.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, arr=[1]` | 1 | Only need one round for one number |
| Already sorted | `n=5, arr=[1,2,3,4,5]` | 1 | No inversions, collect all in one pass |
| Reverse sorted | `n=5, arr=[5,4,3,2,1]` | 5 | Maximum inversions, need n rounds |
| Two elements swapped | `n=5, arr=[2,1,3,4,5]` | 2 | One inversion at the start |
| Last two swapped | `n=5, arr=[1,2,3,5,4]` | 2 | One inversion at the end |

---

## When to Use This Pattern

### Use This Approach When:
- You need to collect/process items in a specific order
- Items can only be accessed in one direction (left-to-right)
- You need to count passes/rounds through a sequence
- The problem involves position relationships between consecutive values

### Do Not Use When:
- Items can be accessed in any order (no round concept)
- The sequence has duplicates (this problem has unique values)
- You need to track actual collection order, not just count

### Pattern Recognition Checklist:
- [ ] Collecting in a fixed order? Consider position mapping
- [ ] Counting passes through array? Count inversions
- [ ] Values form a permutation of 1 to n? Direct position array possible

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Distinct Numbers](https://cses.fi/problemset/task/1621) | Basic sorting and counting |
| [Missing Number](https://cses.fi/problemset/task/1083) | Position/value relationship |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Collecting Numbers II](https://cses.fi/problemset/task/2217) | Dynamic updates after swaps |
| [Ferris Wheel](https://cses.fi/problemset/task/1090) | Greedy pairing with position |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Josephus Problem I](https://cses.fi/problemset/task/2162) | Circular collection order |
| [Inversion Count](https://www.geeksforgeeks.org/counting-inversions/) | Full inversion counting with merge sort |

---

## Key Takeaways

1. **The Core Idea:** Count position inversions where the next value appears before the current value
2. **Time Optimization:** From O(n^2) simulation to O(n) position tracking
3. **Space Trade-off:** O(n) space for position map enables single-pass counting
4. **Pattern:** Position inversion counting for sequential collection problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why rounds = 1 + inversions
- [ ] Build a position map from an array
- [ ] Identify the correct inversion condition (pos[i+1] < pos[i])
- [ ] Handle edge cases (sorted, reverse sorted, single element)
- [ ] Implement the solution in under 5 minutes

---

## Additional Resources

- [CSES Problem Set](https://cses.fi/problemset/)
- [Collecting Numbers II](https://cses.fi/problemset/task/2217) - Follow-up with updates
