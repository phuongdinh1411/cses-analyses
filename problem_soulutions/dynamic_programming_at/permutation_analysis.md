---
layout: simple
title: "Permutation - AtCoder DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/permutation_analysis
difficulty: Hard
tags: [dp, insertion-dp, permutation, prefix-sum, combinatorics]
prerequisites: [basic_dp, prefix_sums]
---

# Permutation

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | Insertion DP with Prefix Sum Optimization |
| **Problem Link** | [AtCoder DP Contest - T](https://atcoder.jp/contests/dp/tasks/dp_t) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and apply the insertion DP technique for permutation counting
- [ ] Use prefix sums to optimize range-sum DP transitions from O(N) to O(1)
- [ ] Handle relative ordering constraints in permutation problems
- [ ] Recognize when to track "relative rank" instead of absolute values

---

## Problem Statement

**Problem:** Given a string S of length N-1 consisting of `<` and `>` characters, count the number of permutations P of [1, 2, ..., N] that satisfy the constraints defined by S. For each position i (1-indexed), if S[i] = `<` then P[i] < P[i+1], and if S[i] = `>` then P[i] > P[i+1].

**Input:**
- Line 1: Integer N (2 <= N <= 3000)
- Line 2: String S of length N-1 containing only `<` and `>`

**Output:**
- The count of valid permutations modulo 10^9 + 7

**Constraints:**
- 2 <= N <= 3000
- |S| = N - 1
- S consists only of `<` and `>`

### Example

```
Input:
4
<><

Output:
5
```

**Explanation:** The valid permutations of [1, 2, 3, 4] satisfying `<><` are:
- 1 3 2 4 (1<3, 3>2, 2<4)
- 1 4 2 3 (1<4, 4>2, 2<3)
- 2 3 1 4 (2<3, 3>1, 1<4)
- 2 4 1 3 (2<4, 4>1, 1<3)
- 3 4 1 2 (3<4, 4>1, 1<2)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we build valid permutations incrementally while respecting the `<` and `>` constraints?

The critical insight is that we do not need to track which exact numbers we have used. Instead, we track the **relative rank** of the last element among all elements placed so far. When we insert a new number, the relative positions of existing elements shift accordingly.

### Breaking Down the Problem

1. **What are we looking for?** The count of permutations where adjacent elements satisfy the given comparison constraints.
2. **What information do we have?** A sequence of N-1 constraints (< or >) between consecutive positions.
3. **What is the relationship between input and output?** Each constraint restricts which relative positions are valid for the next element.

### Analogies

Think of this problem like inserting people into a line based on height rules. Each person you add has a relative "rank" among those already in line. If the rule says `<`, the new person must be taller than the previous one (higher rank). If `>`, they must be shorter (lower rank). We count how many ways we can build such a line.

---

## Solution: Insertion DP with Prefix Sum Optimization

### Key Insight

> **The Trick:** Build the permutation element by element. At step i, track how many valid arrangements exist where the i-th element has each possible relative rank (1st smallest, 2nd smallest, etc.) among the first i elements.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Number of valid permutations of the first i elements where the i-th element is the (j+1)-th smallest among those i elements |

**In plain English:** `dp[i][j]` counts arrangements of i elements where the last placed element ranks (j+1) out of i in ascending order.

### State Transition

For constraint S[i-1] (0-indexed):

```
If S[i-1] == '<':
    dp[i][j] = sum(dp[i-1][k]) for all k < j
    (Previous element must have smaller rank)

If S[i-1] == '>':
    dp[i][j] = sum(dp[i-1][k]) for all k >= j
    (Previous element must have larger or equal rank)
```

**Why the rank adjustment for `>`?** When we insert a new element at rank j, all existing elements with rank >= j get shifted up by 1. So if the previous element had rank k (where k >= j before insertion), it becomes rank k+1 after. For the `>` constraint, we need the previous rank to be higher than j after adjustment, meaning k >= j before insertion.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[1][0]` | 1 | One element, it is trivially the smallest (rank 1) |
| `dp[1][j]` for j > 0 | 0 | With one element, only rank 1 is possible |

### Algorithm

1. Initialize dp[1][0] = 1 (single element has rank 1)
2. For each position i from 2 to N:
   - Compute prefix sums of dp[i-1] for O(1) range queries
   - For each possible rank j from 0 to i-1:
     - If S[i-2] == '<': dp[i][j] = prefix_sum[0..j-1]
     - If S[i-2] == '>': dp[i][j] = prefix_sum[j..i-2]
3. Return sum of dp[N][0..N-1] modulo 10^9+7

### Dry Run Example

Let us trace through with input `N = 4, S = "<><"`:

```
Initial state:
  dp[1] = [1, 0, 0, 0]  (one element at rank 0)

Step 1: Process constraint S[0] = '<' (need increasing)
  i = 2, need previous rank < current rank
  prefix of dp[1] = [1, 1, 1, 1]  (cumulative sums)

  dp[2][0] = sum(dp[1][k] for k < 0) = 0
  dp[2][1] = sum(dp[1][k] for k < 1) = dp[1][0] = 1

  dp[2] = [0, 1]

Step 2: Process constraint S[1] = '>' (need decreasing)
  i = 3, need previous rank >= current rank
  prefix of dp[2] = [0, 1]

  dp[3][0] = sum(dp[2][k] for k >= 0) = 0 + 1 = 1
  dp[3][1] = sum(dp[2][k] for k >= 1) = 1
  dp[3][2] = sum(dp[2][k] for k >= 2) = 0

  dp[3] = [1, 1, 0]

Step 3: Process constraint S[2] = '<' (need increasing)
  i = 4, need previous rank < current rank
  prefix of dp[3] = [1, 2, 2]

  dp[4][0] = sum(dp[3][k] for k < 0) = 0
  dp[4][1] = sum(dp[3][k] for k < 1) = 1
  dp[4][2] = sum(dp[3][k] for k < 2) = 1 + 1 = 2
  dp[4][3] = sum(dp[3][k] for k < 3) = 1 + 1 + 0 = 2

  dp[4] = [0, 1, 2, 2]

Final answer: sum(dp[4]) = 0 + 1 + 2 + 2 = 5
```

### Visual Diagram

```
Building permutations for S = "<><" (N=4):

Position:    1     2     3     4
             |     |     |     |
Constraint:     <     >     <

dp[1]: [1]              (just element, rank 0)
            \
dp[2]: [0, 1]           (element 2 must have higher rank than element 1)
            |\
dp[3]: [1, 1, 0]        (element 3 must have lower rank than element 2)
            |\ \
dp[4]: [0, 1, 2, 2]     (element 4 must have higher rank than element 3)

Sum = 5 valid permutations
```

### Code

**Python Solution:**

```python
def solve(n: int, s: str) -> int:
    """
    Count permutations satisfying < and > constraints using insertion DP.

    Time: O(N^2)
    Space: O(N) with space optimization
    """
    MOD = 10**9 + 7

    # dp[j] = count of valid arrangements where last element has rank j
    dp = [0] * n
    dp[0] = 1  # Base case: single element at rank 0

    for i in range(2, n + 1):
        # Build prefix sums of previous dp
        prefix = [0] * i
        prefix[0] = dp[0]
        for j in range(1, i - 1):
            prefix[j] = (prefix[j - 1] + dp[j]) % MOD

        # Compute new dp values
        new_dp = [0] * n

        if s[i - 2] == '<':
            # Previous rank must be smaller than current rank
            for j in range(i):
                if j > 0:
                    new_dp[j] = prefix[j - 1]
        else:  # '>'
            # Previous rank must be >= current rank (before insertion)
            for j in range(i):
                if j == 0:
                    new_dp[j] = prefix[i - 2] if i >= 2 else 0
                else:
                    new_dp[j] = (prefix[i - 2] - prefix[j - 1] + MOD) % MOD

        dp = new_dp

    return sum(dp) % MOD


def main():
    n = int(input())
    s = input().strip()
    print(solve(n, s))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^2) | Two nested loops: outer over positions, inner over ranks |
| Space | O(N) | Only store current and previous DP row (space optimized) |

---

## Common Mistakes

### Mistake 1: Wrong Index in Prefix Sum

```python
# WRONG: Off-by-one error in prefix sum access
dp[i][j] = prefix[j]  # Should be prefix[j-1] for '<'
```

**Problem:** Accessing wrong prefix sum index leads to including the current rank in the sum.
**Fix:** For `<`, use `prefix[j-1]` to get sum of all ranks strictly less than j.

### Mistake 2: Not Handling Modular Arithmetic Properly

```python
# WRONG: Negative result from subtraction
new_dp[j] = (prefix[i-2] - prefix[j-1]) % MOD  # May be negative!

# CORRECT: Add MOD before taking modulo
new_dp[j] = (prefix[i-2] - prefix[j-1] + MOD) % MOD
```

**Problem:** Subtraction can produce negative values before modulo.
**Fix:** Add MOD before taking the final modulo to ensure non-negative result.

### Mistake 3: Confusing Rank Shift Logic for '>'

```python
# WRONG: Using k > j instead of k >= j for '>'
if s[i-1] == '>':
    dp[i][j] = sum(dp[i-1][k] for k > j)  # Off by one!
```

**Problem:** When inserting at rank j, elements at rank k >= j shift up. For `>` constraint, we need previous rank (after shift) > current rank j, which means original rank k >= j.
**Fix:** Use k >= j (not k > j) in the sum for `>` constraint.

### Mistake 4: Forgetting Base Case

```python
# WRONG: Not initializing base case
dp = [[0] * n for _ in range(n + 1)]
# Missing: dp[1][0] = 1
```

**Problem:** Without proper initialization, all DP values remain 0.
**Fix:** Set dp[1][0] = 1 to represent the single valid arrangement of one element.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum N | N=2, S="<" | 1 | Only [1,2] satisfies 1<2 |
| Minimum N | N=2, S=">" | 1 | Only [2,1] satisfies 2>1 |
| All increasing | N=4, S="<<<" | 1 | Only [1,2,3,4] works |
| All decreasing | N=4, S=">>>" | 1 | Only [4,3,2,1] works |
| Alternating | N=4, S="<><" | 5 | Multiple valid permutations |
| Large N | N=3000 | Varies | Must handle modular arithmetic correctly |

---

## When to Use This Pattern

### Use This Approach When:
- Counting permutations with relative ordering constraints
- Building sequences where only relative order matters, not absolute values
- Problems involving insertion of elements one by one
- Constraints involve comparisons between adjacent elements

### Do Not Use When:
- Absolute values of elements matter (not just relative order)
- Non-adjacent constraints are involved
- The problem asks for a specific permutation, not a count
- Constraints are on subsequences rather than adjacent pairs

### Pattern Recognition Checklist:
- [ ] Counting permutations? Consider insertion DP
- [ ] Constraints only on adjacent elements? Likely solvable with this approach
- [ ] Need to track "relative position" rather than exact values? Insertion DP fits well
- [ ] O(N^2) acceptable given constraints? This approach should work

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [LCS - AtCoder DP E](https://atcoder.jp/contests/dp/tasks/dp_e) | Basic string DP concepts |
| [Longest Increasing Subsequence](https://atcoder.jp/contests/dp/tasks/dp_q) | Understanding relative ordering |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Matching - AtCoder DP O](https://atcoder.jp/contests/dp/tasks/dp_o) | Bitmask DP for permutation counting |
| [Grouping - AtCoder DP U](https://atcoder.jp/contests/dp/tasks/dp_u) | Subset DP with constraints |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Tower - AtCoder DP X](https://atcoder.jp/contests/dp/tasks/dp_x) | Greedy + DP combination |
| [Intervals - AtCoder DP W](https://atcoder.jp/contests/dp/tasks/dp_w) | Segment tree optimization |

---

## Key Takeaways

1. **The Core Idea:** Track relative rank of the last element among all placed elements, not the actual values.
2. **Time Optimization:** Use prefix sums to convert O(N) range sum queries into O(1) operations.
3. **Space Trade-off:** Can optimize from O(N^2) to O(N) space by only keeping the previous row.
4. **Pattern:** Insertion DP is powerful for permutation counting with adjacent constraints.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why tracking relative rank is sufficient (not absolute values)
- [ ] Derive the recurrence relation for both `<` and `>` cases
- [ ] Implement the prefix sum optimization correctly
- [ ] Handle modular arithmetic including negative differences
- [ ] Solve this problem without looking at the solution in under 20 minutes

---

## Additional Resources

- [AtCoder DP Contest - Problem T](https://atcoder.jp/contests/dp/tasks/dp_t) - Original problem
- [CP-Algorithms: Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sums.html) - Prefix sum technique
- [AtCoder Editorial](https://atcoder.jp/contests/dp/editorial) - Official editorial for the DP contest
