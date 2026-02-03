---
layout: simple
title: "Matching - Bitmask DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/matching_analysis
difficulty: Hard
tags: [bitmask-dp, combinatorics, bipartite-matching, counting]
prerequisites: [subset_sum, traveling_salesman]
---

# Matching

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming (Bitmask DP) |
| **Time Limit** | 2 seconds |
| **Key Technique** | Bitmask DP, State Compression |
| **Problem Link** | [AtCoder DP Contest - Problem O](https://atcoder.jp/contests/dp/tasks/dp_o) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Represent subset states using bitmasks
- [ ] Design DP states where the "index" is implicitly encoded in the popcount
- [ ] Count perfect matchings in bipartite graphs using DP
- [ ] Apply bitmask DP to assignment/pairing problems

---

## Problem Statement

**Problem:** Given N men and N women, with a compatibility matrix indicating which pairs can be matched, count the number of ways to create a perfect matching where each man is paired with exactly one compatible woman.

**Input:**
- Line 1: N (number of men and women)
- Next N lines: N integers a[i][j] where a[i][j] = 1 if man i is compatible with woman j

**Output:**
- Number of perfect matchings modulo 10^9 + 7

**Constraints:**
- 1 <= N <= 21
- a[i][j] is 0 or 1

### Example

```
Input:
3
0 1 1
1 0 1
1 1 1

Output:
3
```

**Explanation:** The three valid matchings are:
1. Man 0 -> Woman 1, Man 1 -> Woman 0, Man 2 -> Woman 2
2. Man 0 -> Woman 1, Man 1 -> Woman 2, Man 2 -> Woman 0
3. Man 0 -> Woman 2, Man 1 -> Woman 0, Man 2 -> Woman 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count all possible ways to pair N men with N women without repetition?

This is a counting problem on bipartite matching. The key insight is that we can process men sequentially (man 0, then man 1, etc.) and track which women have already been used. A bitmask perfectly encodes this "used women" state.

### Breaking Down the Problem

1. **What are we looking for?** The count of all valid one-to-one matchings.
2. **What information do we have?** A compatibility matrix telling us valid pairs.
3. **What's the relationship between input and output?** Each 1 in the matrix represents a possible edge; we count all ways to select N edges forming a perfect matching.

### Analogies

Think of this like assigning tasks to workers. Each worker (man) must be assigned exactly one task (woman), workers can only do tasks they are qualified for (compatibility = 1), and no two workers can share the same task. We want to count all valid assignment schemes.

---

## Solution 1: Brute Force (Permutation)

### Idea

Generate all N! permutations of women and check which ones form valid matchings.

### Algorithm

1. Generate all permutations of [0, 1, ..., N-1]
2. For each permutation p, check if a[i][p[i]] = 1 for all i
3. Count valid permutations

### Code

```python
from itertools import permutations

def solve_brute_force(n, compatibility):
    """
    Brute force: check all N! permutations.

    Time: O(N! * N)
    Space: O(N)
    """
    MOD = 10**9 + 7
    count = 0

    for perm in permutations(range(n)):
        valid = True
        for man, woman in enumerate(perm):
            if compatibility[man][woman] == 0:
                valid = False
                break
        if valid:
            count = (count + 1) % MOD

    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N! * N) | N! permutations, O(N) to validate each |
| Space | O(N) | Store one permutation at a time |

### Why This Works (But Is Slow)

This correctly enumerates all possible matchings but 21! is astronomically large (about 5 * 10^19), making it infeasible for N = 21.

---

## Solution 2: Bitmask DP (Optimal)

### Key Insight

> **The Trick:** Process men in order (0, 1, 2, ...). Use a bitmask to track which women are already matched. The current man's index equals the popcount of the mask.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask]` | Number of ways to match the first `popcount(mask)` men with the women indicated by set bits in `mask` |

**In plain English:** If mask = 0b1010 (bits 1 and 3 set), then dp[mask] = number of ways to match men 0 and 1 with women 1 and 3.

### State Transition

```
For each unmatched woman j where bit j is 0 in mask:
    if compatibility[popcount(mask)][j] == 1:
        dp[mask | (1 << j)] += dp[mask]
```

**Why?** We extend a partial matching (of k men) by adding one more man (man k) matched to an available compatible woman j.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 1 | Empty matching (0 men matched to 0 women) is valid |

### Algorithm

1. Initialize dp[0] = 1, all others = 0
2. Iterate through all masks from 0 to 2^N - 1
3. For each mask, compute man index = popcount(mask)
4. Try matching this man to each unmatched compatible woman
5. Answer is dp[(1 << N) - 1]

### Dry Run Example

Let's trace through with N = 3 and compatibility:
```
     W0 W1 W2
M0: [ 0, 1, 1 ]
M1: [ 1, 0, 1 ]
M2: [ 1, 1, 1 ]
```

```
Initial: dp[000] = 1

Processing mask = 000 (binary), man_idx = 0:
  Man 0 compatible with: W1, W2
  dp[010] += dp[000] = 1  (match M0->W1)
  dp[100] += dp[000] = 1  (match M0->W2)

Processing mask = 010, man_idx = 1:
  Man 1 compatible with: W0, W2 (W1 used)
  dp[011] += dp[010] = 1  (match M1->W0)
  dp[110] += dp[010] = 1  (match M1->W2)

Processing mask = 011, man_idx = 2:
  Man 2 compatible with: W2 (W0,W1 used)
  dp[111] += dp[011] = 1  (match M2->W2)

Processing mask = 100, man_idx = 1:
  Man 1 compatible with: W0 (W2 used, W1 not compatible)
  dp[101] += dp[100] = 1  (match M1->W0)

Processing mask = 101, man_idx = 2:
  Man 2 compatible with: W1 (W0,W2 used)
  dp[111] += dp[101] = 1  (match M2->W1)

Processing mask = 110, man_idx = 2:
  Man 2 compatible with: W0 (W1,W2 used)
  dp[111] += dp[110] = 1  (match M2->W0)

Final: dp[111] = 3
```

### Visual Diagram

```
Men:    M0 -----> M1 -----> M2
        |         |         |
        v         v         v
State: 000 ----> 0X0 ----> 0XX ----> 111
       (empty)   (1 woman) (2 women) (all matched)

Three paths to dp[111]:
Path 1: 000 -> 010 -> 011 -> 111  (M0->W1, M1->W0, M2->W2)
Path 2: 000 -> 010 -> 110 -> 111  (M0->W1, M1->W2, M2->W0)
Path 3: 000 -> 100 -> 101 -> 111  (M0->W2, M1->W0, M2->W1)
```

### Code

**Python Solution:**

```python
import sys
input = sys.stdin.readline

def solve():
    """
    Bitmask DP solution for counting perfect matchings.

    Time: O(N * 2^N)
    Space: O(2^N)
    """
    MOD = 10**9 + 7

    n = int(input())
    compatibility = []
    for _ in range(n):
        row = list(map(int, input().split()))
        compatibility.append(row)

    # dp[mask] = ways to match first popcount(mask) men with women in mask
    dp = [0] * (1 << n)
    dp[0] = 1

    for mask in range(1 << n):
        man_idx = bin(mask).count('1')

        if man_idx >= n:
            continue

        for woman in range(n):
            # Skip if woman already matched
            if (mask >> woman) & 1:
                continue

            # Check compatibility
            if compatibility[man_idx][woman] == 1:
                new_mask = mask | (1 << woman)
                dp[new_mask] = (dp[new_mask] + dp[mask]) % MOD

    print(dp[(1 << n) - 1])

if __name__ == "__main__":
    solve()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    const int MOD = 1e9 + 7;

    int n;
    cin >> n;

    vector<vector<int>> compat(n, vector<int>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> compat[i][j];
        }
    }

    // dp[mask] = ways to match first popcount(mask) men with women in mask
    vector<long long> dp(1 << n, 0);
    dp[0] = 1;

    for (int mask = 0; mask < (1 << n); mask++) {
        int man_idx = __builtin_popcount(mask);

        if (man_idx >= n) continue;

        for (int woman = 0; woman < n; woman++) {
            // Skip if woman already matched
            if ((mask >> woman) & 1) continue;

            // Check compatibility
            if (compat[man_idx][woman] == 1) {
                int new_mask = mask | (1 << woman);
                dp[new_mask] = (dp[new_mask] + dp[mask]) % MOD;
            }
        }
    }

    cout << dp[(1 << n) - 1] << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N * 2^N) | Iterate 2^N masks, O(N) work per mask |
| Space | O(2^N) | DP array of size 2^N |

For N = 21: 21 * 2^21 = ~44 million operations, which is feasible.

---

## Common Mistakes

### Mistake 1: Wrong Man Index Calculation

```python
# WRONG - using loop variable as man index
for mask in range(1 << n):
    for man in range(n):  # Wrong! Man is determined by popcount
        ...

# CORRECT - man index equals popcount of mask
for mask in range(1 << n):
    man_idx = bin(mask).count('1')
    ...
```

**Problem:** The man to be matched is always the next one in sequence (determined by how many are already matched).
**Fix:** Use popcount(mask) to determine which man we are currently matching.

### Mistake 2: Forgetting the Modulo

```python
# WRONG - overflow without modulo
dp[new_mask] = dp[new_mask] + dp[mask]

# CORRECT
dp[new_mask] = (dp[new_mask] + dp[mask]) % MOD
```

**Problem:** Numbers can exceed integer limits quickly.
**Fix:** Apply modulo at every addition.

### Mistake 3: Off-by-One in Full Mask

```python
# WRONG
return dp[1 << n]  # Index out of bounds!

# CORRECT
return dp[(1 << n) - 1]  # All N bits set
```

**Problem:** `1 << n` has bit n set (one beyond valid range), while `(1 << n) - 1` has bits 0 to n-1 set.
**Fix:** Use `(1 << n) - 1` for the "all matched" state.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| N = 1, compatible | `[[1]]` | 1 | Single valid matching |
| N = 1, incompatible | `[[0]]` | 0 | No valid matching possible |
| All compatible | N x N matrix of 1s | N! % MOD | Every permutation is valid |
| No valid matching | Incompatible pairs | 0 | dp remains 0 at final state |
| Identity only | Diagonal matrix | 1 | Only M_i -> W_i allowed |

---

## When to Use This Pattern

### Use Bitmask DP When:
- Problem involves selecting/matching from a set of up to ~20-25 elements
- You need to track which items have been "used" or "visited"
- The order of processing can be fixed (e.g., by index)
- State depends on a subset, not the order of selection

### Don't Use When:
- N > 25 (2^N becomes too large)
- Order of selection matters (need different state)
- A greedy or simpler DP structure exists
- Problem has polynomial-time algorithm (e.g., Hungarian algorithm for weighted matching)

### Pattern Recognition Checklist:
- [ ] Subset selection with constraints? Consider bitmask DP
- [ ] N <= 20 and need to track used items? Consider bitmask DP
- [ ] Counting assignments/matchings? Consider bitmask DP
- [ ] Can fix processing order to eliminate one dimension? Classic bitmask optimization

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Traveling Salesman](https://atcoder.jp/contests/dp/tasks/dp_u) | Basic bitmask DP with state transitions |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Elevator Rides (CSES)](https://cses.fi/problemset/task/1653) | Bitmask DP with weight constraints |
| [SOS DP](https://codeforces.com/blog/entry/45223) | Subset sum over bitmasks |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Hamiltonian Flights (CSES)](https://cses.fi/problemset/task/1690) | Bitmask DP on graphs |
| [Counting Tilings (CSES)](https://cses.fi/problemset/task/2181) | Profile DP (bitmask on grid) |

---

## Key Takeaways

1. **The Core Idea:** Use bitmask to represent which items (women) are used; the popcount implicitly encodes progress (which man).
2. **Time Optimization:** From O(N! * N) brute force to O(N * 2^N) by reusing subproblem solutions.
3. **Space Trade-off:** O(2^N) space to store all subset states enables polynomial-time per state.
4. **Pattern:** This is the "assignment counting" pattern - useful whenever you count ways to assign N items to N slots with constraints.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why popcount(mask) gives the current man index
- [ ] Trace through a small example by hand
- [ ] Implement in your preferred language in under 15 minutes
- [ ] Identify similar bitmask DP problems in contests

---

## Additional Resources

- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp/editorial)
- [CP-Algorithms: Bitmask DP](https://cp-algorithms.com/algebra/all-submasks.html)
- [Bitmask DP Tutorial (Codeforces)](https://codeforces.com/blog/entry/337)
