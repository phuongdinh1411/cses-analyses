---
layout: simple
title: "Distinct Values Subsequences - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/distinct_values_subsequences_analysis
difficulty: Easy
tags: [counting, hash-map, combinatorics, modular-arithmetic]
---

# Distinct Values Subsequences

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Sorting and Searching / Counting |
| **Time Limit** | 1.00 s |
| **CSES Link** | [Distinct Values Subsequences](https://cses.fi/problemset/task/3421) |
| **Key Technique** | Frequency count + product rule |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Turn "choose a subsequence" into independent per-value choices
- [ ] Apply the product rule and subtract the empty choice
- [ ] Keep products under a modulus

### In 60 seconds
- A subsequence with distinct values picks, for each distinct value `v`, either nothing or exactly one of its `cnt[v]` occurrences.
- Choices for different values are independent, so the count is `∏ (cnt[v] + 1)`, minus 1 for the empty subsequence.
- O(n) time with a hash map.

> **Say this in the interview:** "Each value contributes cnt + 1 options — skip it or pick one of its positions — and values are independent, so multiply and drop the empty pick."

---

## Problem Statement

**Problem:** Given an array of `n` integers, count the non-empty subsequences in which all values are distinct. Two subsequences are different if they use different positions. Print the answer modulo 10⁹ + 7.

**Input:**
- Line 1: `n`
- Line 2: `n` integers `x_1 … x_n`

**Output:**
- The number of distinct-valued subsequences modulo 10⁹ + 7

**Constraints:**
- 1 ≤ n ≤ 2 · 10⁵
- 1 ≤ x_i ≤ 10⁹

### Example

```
Input:
4
1 2 1 3

Output:
11
```

**Explanation:** counts are `1:2, 2:1, 3:1`. Value 1 has 3 options (skip, first 1, second 1); values 2 and 3 have 2 options each. `3 · 2 · 2 = 12` choices, minus the empty one = 11.

---

## Solution 1: Brute Force

Enumerate all `2ⁿ − 1` non-empty position subsets and keep those with distinct values. O(2ⁿ · n) — only useful for checking.

```python
def count_brute(arr: list[int]) -> int:
  n = len(arr)
  total = 0
  for mask in range(1, 1 << n):
    vals = [arr[i] for i in range(n) if mask >> i & 1]
    if len(vals) == len(set(vals)):
      total += 1
  return total
```

---

## Solution 2: Optimal — Product Rule

### Key Insight

> **The Trick:** A valid subsequence never uses the same value twice, so it is fully described by choosing, independently for each distinct value, "skip" or "which occurrence".

### Algorithm

1. Count occurrences of each value.
2. `answer = ∏ (cnt[v] + 1) mod p`.
3. Subtract 1 (the empty subsequence), keeping the result in `[0, p)`.

### Dry Run

```
arr = [1, 2, 1, 3]
cnt = {1: 2, 2: 1, 3: 1}
product = (2+1) · (1+1) · (1+1) = 12
answer  = 12 − 1 = 11
```

### Code

```python
import sys
from collections import Counter

MOD = 10**9 + 7


def solve() -> None:
  data = sys.stdin.buffer.read().split()
  n = int(data[0])
  cnt = Counter(data[1:n + 1])
  ans = 1
  for c in cnt.values():
    ans = ans * (c + 1) % MOD
  print((ans - 1) % MOD)


if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | One pass to count, one pass over distinct values |
| Space | O(d) | `d` distinct values in the counter |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting to subtract the empty subsequence | `ans − 1` at the end |
| Counting distinct *value sets* instead of position choices | Multiply by `cnt + 1`, not by 2 |
| Negative result after `ans − 1` in other languages | `(ans − 1 + MOD) % MOD`; Python's `%` already returns a non-negative value |

---

## Related Problems

| Problem | Link | Relation |
|---------|------|----------|
| Subarray Distinct Values | [Analysis](../sliding_window/subarray_distinct_values_analysis) | Contiguous version with at most k distinct values (sliding window) |
| Distinct Values Subarrays | [Analysis](distinct_values_subarrays_analysis) | Count subarrays with all-distinct values |
| LeetCode 940 — Distinct Subsequences II | [Link](https://leetcode.com/problems/distinct-subsequences-ii/) | Counts distinct *strings*, a harder DP |
