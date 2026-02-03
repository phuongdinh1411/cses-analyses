---
layout: simple
title: "Collecting Numbers - Counting Inversions"
permalink: /problem_soulutions/counting_problems/collecting_numbers_distribution_analysis
difficulty: Easy
tags: [arrays, inversions, position-tracking, sorting]
prerequisites: []
---

# Collecting Numbers

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Collecting Numbers](https://cses.fi/problemset/task/2216) |
| **Difficulty** | Easy |
| **Category** | Sorting / Inversions |
| **Time Limit** | 1 second |
| **Key Technique** | Position Tracking |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Track element positions efficiently using arrays or hash maps
- [ ] Identify "rounds" based on relative ordering of consecutive values
- [ ] Count inversions between specific element pairs
- [ ] Apply the pattern of checking predecessor positions

---

## Problem Statement

**Problem:** You are given an array containing a permutation of numbers 1 to n. You want to collect the numbers from 1 to n in increasing order. In each round, you go through the array from left to right and collect as many numbers as possible (each number you collect must be the next one you need).

Count the minimum number of rounds needed.

**Input:**
- Line 1: Integer n (size of permutation)
- Line 2: n integers forming a permutation of 1 to n

**Output:**
- Single integer: minimum number of rounds

**Constraints:**
- 1 <= n <= 2 * 10^5

### Example

```
Input:
5
4 2 1 5 3

Output:
3
```

**Explanation:**
- Round 1: Go left to right, collect 1 (at position 3)
- Round 2: Go left to right, collect 2 (at position 2), then 3 (at position 5)
- Round 3: Go left to right, collect 4 (at position 1), then 5 (at position 4)

Total: 3 rounds

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When do we need a new round?

A new round is needed when the next number we want to collect appears **before** the current number in the array. If number `k+1` is to the left of number `k`, we cannot collect `k+1` in the same round as `k`.

### Breaking Down the Problem

1. **What are we looking for?** The number of times we need to restart from the beginning.
2. **What causes a restart?** When the next consecutive number is positioned earlier than the current one.
3. **Core insight:** Count how many times `position[k+1] < position[k]` for k from 1 to n-1.

### Analogies

Imagine walking through a hallway picking up numbered items. You must pick them in order (1, 2, 3...). Each time you find a number and the next one is behind you, you must walk back to the start - that is a new round.

---

## Solution 1: Simulation (Brute Force)

### Idea

Simulate the actual process: repeatedly scan left to right, collecting the next needed number each time.

### Algorithm

1. Keep track of the next number to collect (starts at 1)
2. Scan array from left to right
3. Collect numbers when found, increment next target
4. When reaching array end, if not done, start new round
5. Count total rounds

### Code

```python
def solve_simulation(n, arr):
    """
    Brute force: simulate the collection process.

    Time: O(n^2) worst case
    Space: O(1)
    """
    rounds = 0
    next_to_collect = 1

    while next_to_collect <= n:
        rounds += 1
        for num in arr:
            if num == next_to_collect:
                next_to_collect += 1

    return rounds
```

```cpp
int solveSimulation(int n, vector<int>& arr) {
    int rounds = 0;
    int nextToCollect = 1;

    while (nextToCollect <= n) {
        rounds++;
        for (int num : arr) {
            if (num == nextToCollect) {
                nextToCollect++;
            }
        }
    }
    return rounds;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Worst case: need n rounds, each scans n elements |
| Space | O(1) | Only tracking round count and next target |

### Why This Works (But Is Slow)

Correctness is guaranteed because we faithfully simulate the process. However, we redundantly scan the entire array for each round.

---

## Solution 2: Position Tracking (Optimal)

### Key Insight

> **The Trick:** Instead of simulating, directly count how many times `position[k+1] < position[k]`.

If the position of number `k+1` is less than the position of number `k`, we need a new round to collect `k+1` (since we already passed it when collecting `k`).

### Algorithm

1. Build position array: `pos[x]` = index where value x appears
2. Start with 1 round (we always need at least one)
3. For each consecutive pair (k, k+1), if `pos[k+1] < pos[k]`, increment rounds
4. Return total rounds

### Dry Run Example

Let's trace through with input `n = 5, arr = [4, 2, 1, 5, 3]`:

```
Step 1: Build position array
  arr:    [4, 2, 1, 5, 3]
  index:   0  1  2  3  4

  pos[1] = 2  (value 1 is at index 2)
  pos[2] = 1  (value 2 is at index 1)
  pos[3] = 4  (value 3 is at index 4)
  pos[4] = 0  (value 4 is at index 0)
  pos[5] = 3  (value 5 is at index 3)

Step 2: Count position inversions
  rounds = 1 (start with 1)

  Check 1->2: pos[2]=1 < pos[1]=2? YES -> rounds=2
  Check 2->3: pos[3]=4 < pos[2]=1? NO  -> rounds=2
  Check 3->4: pos[4]=0 < pos[3]=4? YES -> rounds=3
  Check 4->5: pos[5]=3 < pos[4]=0? NO  -> rounds=3

Final answer: 3
```

### Visual Diagram

```
Array:  [4, 2, 1, 5, 3]
Index:   0  1  2  3  4

Position tracking:
  Value: 1  2  3  4  5
  Pos:   2  1  4  0  3

Checking consecutive pairs:
  1->2: pos[2]=1 < pos[1]=2  =>  NEW ROUND
  2->3: pos[3]=4 > pos[2]=1  =>  same round
  3->4: pos[4]=0 < pos[3]=4  =>  NEW ROUND
  4->5: pos[5]=3 > pos[4]=0  =>  same round

Total rounds: 1 + 2 inversions = 3
```

### Code

```python
def solve_optimal(n, arr):
    """
    Optimal solution using position tracking.

    Time: O(n) - single pass to build positions, single pass to count
    Space: O(n) - position array
    """
    # Build position array (1-indexed values)
    pos = [0] * (n + 1)
    for i, val in enumerate(arr):
        pos[val] = i

    # Count rounds: start with 1, add 1 for each inversion
    rounds = 1
    for k in range(1, n):
        if pos[k + 1] < pos[k]:
            rounds += 1

    return rounds


# Main I/O
if __name__ == "__main__":
    n = int(input())
    arr = list(map(int, input().split()))
    print(solve_optimal(n, arr))
```

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> pos(n + 1);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        pos[x] = i;
    }

    int rounds = 1;
    for (int k = 1; k < n; k++) {
        if (pos[k + 1] < pos[k]) {
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
| Time | O(n) | One pass to build positions, one pass to count inversions |
| Space | O(n) | Position array of size n+1 |

---

## Common Mistakes

### Mistake 1: Off-by-One in Position Array

```python
# WRONG - using 0-indexed for values
pos = [0] * n
for i, val in enumerate(arr):
    pos[val] = i  # Error when val = n

# CORRECT - size n+1 for 1-indexed values
pos = [0] * (n + 1)
for i, val in enumerate(arr):
    pos[val] = i
```

**Problem:** Array index out of bounds when value equals n.
**Fix:** Allocate size n+1 to accommodate values 1 through n.

### Mistake 2: Forgetting Initial Round

```python
# WRONG
rounds = 0
for k in range(1, n):
    if pos[k + 1] < pos[k]:
        rounds += 1

# CORRECT
rounds = 1  # Always need at least one round
for k in range(1, n):
    if pos[k + 1] < pos[k]:
        rounds += 1
```

**Problem:** Even a sorted array needs 1 round to collect all numbers.
**Fix:** Initialize rounds to 1.

### Mistake 3: Wrong Loop Bounds

```python
# WRONG - goes out of bounds
for k in range(1, n + 1):
    if pos[k + 1] < pos[k]:  # pos[n+1] doesn't exist!

# CORRECT
for k in range(1, n):  # k goes from 1 to n-1
    if pos[k + 1] < pos[k]:
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Already sorted | `[1,2,3,4,5]` | 1 | All positions increasing, no inversions |
| Reverse sorted | `[5,4,3,2,1]` | 5 | Every pair is inverted, n rounds needed |
| Single element | `[1]` | 1 | Trivially one round |
| Two elements swapped | `[2,1]` | 2 | One inversion, need 2 rounds |
| Alternating | `[2,1,4,3]` | 2 | Two inversions but both same type |

---

## When to Use This Pattern

### Use This Approach When:
- Tracking relative positions of consecutive/related elements
- Counting "restarts" or "passes" based on ordering
- Problems involving permutations and position comparisons

### Don't Use When:
- Need to count all inversions (use merge sort or BIT)
- Elements are not a permutation (may have duplicates or gaps)
- Need the actual collection order, not just the count

### Pattern Recognition Checklist:
- [ ] Is input a permutation of 1 to n? -> **Position tracking works well**
- [ ] Counting passes/rounds based on ordering? -> **Check consecutive positions**
- [ ] "When must we restart?" -> **Find position inversions**

---

## Related Problems

### Similar Difficulty (CSES)
| Problem | Key Difference |
|---------|----------------|
| [Collecting Numbers II](https://cses.fi/problemset/task/2217) | Dynamic updates with swaps |
| [Distinct Numbers](https://cses.fi/problemset/task/1621) | Basic set counting |
| [Ferris Wheel](https://cses.fi/problemset/task/1090) | Greedy pairing |

### Related Concepts (LeetCode)
| Problem | Connection |
|---------|------------|
| [Count Inversions](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | General inversion counting |
| [Minimum Swaps to Sort](https://leetcode.com/problems/minimum-swaps-to-sort/) | Position-based analysis |

### Harder Extensions
| Problem | New Concept |
|---------|-------------|
| [Collecting Numbers II](https://cses.fi/problemset/task/2217) | Segment trees or efficient updates |
| [Inversion Count](https://cses.fi/problemset/task/1643) | Merge sort technique |

---

## Key Takeaways

1. **The Core Idea:** Count position inversions between consecutive values to determine rounds needed.
2. **Time Optimization:** From O(n^2) simulation to O(n) position analysis.
3. **Space Trade-off:** O(n) space for position array enables O(n) time.
4. **Pattern:** Position tracking for permutation problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why position inversions equal extra rounds needed
- [ ] Implement the O(n) solution in under 5 minutes
- [ ] Extend to Collecting Numbers II (with updates)
