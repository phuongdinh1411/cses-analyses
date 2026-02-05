---
layout: simple
title: "Grouping - Subset DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/grouping_analysis
difficulty: Hard
tags: [bitmask-dp, subset-dp, partition, optimization]
---

# Grouping

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming (Bitmask/Subset DP) |
| **Time Limit** | 2 seconds |
| **Key Technique** | Subset DP with Bitmask Enumeration |
| **Problem Link** | [AtCoder DP Contest - Problem U](https://atcoder.jp/contests/dp/tasks/dp_u) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how to represent subsets using bitmasks
- [ ] Enumerate all submasks of a given mask efficiently in O(3^n) total
- [ ] Apply subset DP to partition optimization problems
- [ ] Precompute subset scores for efficient DP transitions

---

## Problem Statement

**Problem:** Given N people and a compatibility score matrix, partition all N people into groups (any number of groups). When people i and j are in the same group, you gain score a[i][j]. Find the maximum total score achievable.

**Input:**
- Line 1: N (number of people)
- Next N lines: N x N compatibility matrix a[i][j]

**Output:**
- Maximum total score when optimally partitioning people into groups

**Constraints:**
- 1 <= N <= 16
- |a[i][j]| <= 10^9
- a[i][j] = a[j][i] (symmetric)
- a[i][i] = 0

### Example

```
Input:
3
0 10 20
10 0 -100
20 -100 0

Output:
20
```

**Explanation:**
- Option 1: All in one group -> score = 10 + 20 + (-100) = -70
- Option 2: {0,1} and {2} -> score = 10
- Option 3: {0,2} and {1} -> score = 20 (optimal)
- Option 4: {1,2} and {0} -> score = -100
- Option 5: Each person alone -> score = 0

The optimal partition is {0,2} and {1}, giving score 20.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we try all possible partitions of N items?

Since N <= 16, we can represent any subset of people using a bitmask. The key insight is that we can use DP where `dp[mask]` represents the maximum score achievable when optimally partitioning the people in `mask` into groups.

### Breaking Down the Problem

1. **What are we looking for?** Maximum total compatibility score
2. **What information do we have?** Pairwise compatibility scores between all people
3. **What's the relationship?** For any subset, we either keep it as one group OR split it into two smaller subsets and solve recursively

### Analogies

Think of this like organizing a party where you need to split guests into conversation groups. Some pairs chat well together (positive score), others argue (negative score). You want to maximize the overall "vibe" by putting compatible people together.

---

## Solution 1: Brute Force (Recursive Enumeration)

### Idea

Try all possible ways to partition N items. For each partition, compute the total score.

### Algorithm

1. Generate all possible partitions of N items
2. For each partition, sum up pairwise scores within each group
3. Return the maximum score found

### Code

```python
def solve_brute_force(n, scores):
  """
  Brute force: enumerate all partitions.

  Time: O(B(n) * n^2) where B(n) is Bell number
  Space: O(n)
  """
  def partition_score(groups):
    total = 0
    for group in groups:
      for i in group:
        for j in group:
          if i < j:
            total += scores[i][j]
    return total

  def generate_partitions(items):
    if not items:
      yield []
      return
    first = items[0]
    rest = items[1:]
    for partition in generate_partitions(rest):
      # Add first to each existing group
      for i, group in enumerate(partition):
        new_partition = [g[:] for g in partition]
        new_partition[i].append(first)
        yield new_partition
      # Start new group with first
      yield [[first]] + partition

  max_score = float('-inf')
  for partition in generate_partitions(list(range(n))):
    max_score = max(max_score, partition_score(partition))
  return max_score
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(B(n) * n^2) | B(n) is the Bell number (~exponential) |
| Space | O(n) | Recursion depth |

### Why This Works (But Is Slow)

The Bell number B(16) is approximately 10 billion, making this approach infeasible for N=16.

---

## Solution 2: Subset DP (Optimal)

### Key Insight

> **The Trick:** For any subset represented by mask, either keep it as one group OR split into two non-empty submasks and combine their optimal solutions.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask]` | Maximum score when optimally partitioning people in `mask` into groups |
| `cost[mask]` | Score if all people in `mask` form exactly one group |

**In plain English:** `dp[mask]` answers "What's the best score if I only consider people whose bits are set in mask?"

### State Transition

```
dp[mask] = max(
    cost[mask],                           // Keep entire mask as one group
    max(dp[sub] + dp[mask ^ sub])         // Split into submask and complement
        for all non-empty submask of mask
)
```

**Why?** Any valid partition of `mask` either has all elements in one group, or can be divided into two non-empty parts. The DP tries all such divisions.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 0 | Empty set has score 0 |
| `cost[single bit]` | 0 | Single person group has no pairs |

### Algorithm

1. **Precompute** `cost[mask]` for all 2^N masks - sum of a[i][j] for all pairs in mask
2. **Process masks** in increasing order (smaller subsets first)
3. **For each mask**, enumerate all submasks and take maximum

### Dry Run Example

Let's trace with N=3, scores: a[0][1]=10, a[0][2]=20, a[1][2]=-100

```
Precompute cost[mask]:
  cost[001] = 0             (only person 0)
  cost[010] = 0             (only person 1)
  cost[011] = a[0][1] = 10  (persons 0,1)
  cost[100] = 0             (only person 2)
  cost[101] = a[0][2] = 20  (persons 0,2)
  cost[110] = a[1][2] = -100 (persons 1,2)
  cost[111] = 10 + 20 - 100 = -70  (all three)

DP computation:
  dp[000] = 0 (base case)
  dp[001] = cost[001] = 0
  dp[010] = cost[010] = 0
  dp[011] = max(cost[011], dp[001]+dp[010]) = max(10, 0+0) = 10
  dp[100] = cost[100] = 0
  dp[101] = max(cost[101], dp[001]+dp[100]) = max(20, 0+0) = 20
  dp[110] = max(cost[110], dp[010]+dp[100]) = max(-100, 0) = 0
  dp[111] = max(
      cost[111],           // -70 (all in one group)
      dp[001] + dp[110],   // 0 + 0 = 0
      dp[010] + dp[101],   // 0 + 20 = 20 <-- OPTIMAL
      dp[011] + dp[100],   // 10 + 0 = 10
      dp[100] + dp[011],   // (duplicate)
      dp[101] + dp[010],   // (duplicate)
      dp[110] + dp[001],   // (duplicate)
  ) = 20

Answer: dp[111] = 20
```

### Visual Diagram

```
All 8 subsets for N=3 (binary representation):

mask=111 (all people)
    |
    +-- cost[111] = -70 (keep as one group)
    |
    +-- split into submasks:
        |
        +-- 001 + 110: dp[001] + dp[110] = 0 + 0 = 0
        |
        +-- 010 + 101: dp[010] + dp[101] = 0 + 20 = 20  <-- Best!
        |
        +-- 011 + 100: dp[011] + dp[100] = 10 + 0 = 10

Optimal partition: {0,2} and {1} with score 20
```

### Code (Python)

```python
import sys
input = sys.stdin.readline

def solve():
  n = int(input())
  a = []
  for _ in range(n):
    a.append(list(map(int, input().split())))

  # Precompute cost for each subset (if all in one group)
  cost = [0] * (1 << n)
  for mask in range(1 << n):
    total = 0
    for i in range(n):
      if not (mask & (1 << i)):
        continue
      for j in range(i + 1, n):
        if mask & (1 << j):
          total += a[i][j]
    cost[mask] = total

  # dp[mask] = max score for optimal partition of mask
  dp = [0] * (1 << n)

  for mask in range(1 << n):
    # Option 1: entire mask as one group
    dp[mask] = cost[mask]

    # Option 2: split into submask and complement
    sub = mask
    while sub > 0:
      complement = mask ^ sub
      if complement > 0:  # both parts non-empty
        dp[mask] = max(dp[mask], dp[sub] + dp[complement])
      sub = (sub - 1) & mask

  print(dp[(1 << n) - 1])

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(3^N) | Each element is in submask, complement, or not in mask |
| Space | O(2^N) | Store dp and cost arrays |

**Why O(3^N)?** For each of N elements, it can be: (1) in submask, (2) in complement, or (3) not in current mask. Total combinations = 3^N.

---

## Common Mistakes

### Mistake 1: Not Handling Empty Submasks

```python
# WRONG: may count empty partitions
sub = mask
while sub >= 0:  # includes sub=0
  dp[mask] = max(dp[mask], dp[sub] + dp[mask ^ sub])
  if sub == 0:
    break
  sub = (sub - 1) & mask
```

**Problem:** When sub=0, mask^sub = mask, causing double counting.
**Fix:** Only consider non-empty submasks where complement is also non-empty.

### Mistake 2: Integer Overflow

**Problem:** With N=16 and values up to 10^9, sum can reach ~10^12.
**Fix:** Use 64-bit integers (long long in C++, int in Python is fine).

### Mistake 3: Wrong Submask Enumeration

```python
# WRONG: misses some submasks
for sub in range(1, mask):
  if (sub & mask) == sub:  # inefficient and may miss
    ...

# CORRECT: standard submask enumeration
sub = mask
while sub > 0:
  # process sub
  sub = (sub - 1) & mask
```

**Problem:** Linear iteration is O(2^N) per mask instead of O(submask count).
**Fix:** Use the standard `(sub - 1) & mask` trick.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| N=1 | Single person | 0 | No pairs possible |
| All negative | All a[i][j] < 0 | 0 | Keep everyone separate |
| All positive | All a[i][j] > 0 | Sum of all | Keep everyone together |
| Mixed scores | Example above | Optimal partition | Need DP to find best |
| Large values | a[i][j] = 10^9 | Use long long | Avoid overflow |

---

## When to Use This Pattern

### Use Subset DP When:
- N is small (typically N <= 20)
- Need to partition items into groups optimally
- Each subset can be evaluated independently
- Looking for optimal grouping/assignment

### Don't Use When:
- N is large (> 25) - exponential blowup
- Problem has simpler structure (greedy works)
- Need to enumerate actual partitions (not just optimal value)

### Pattern Recognition Checklist:
- [ ] Small N constraint (N <= 16-20)? -> **Consider bitmask DP**
- [ ] Partition optimization? -> **Consider subset DP**
- [ ] Pairwise interactions within groups? -> **Precompute subset costs**
- [ ] Need to try all subsets of subsets? -> **Use submask enumeration**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Matching](https://atcoder.jp/contests/dp/tasks/dp_o) | Basic bitmask DP |
| [Traveling Salesman](https://atcoder.jp/contests/dp/tasks/dp_o) | Bitmask DP with state |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [SOS DP Problems](https://codeforces.com/blog/entry/45223) | Sum over subsets technique |
| [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Simpler partition criteria |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Steiner Tree](https://judge.yosupo.jp/problem/steiner_tree) | Subset DP on graphs |
| [Chromatic Number](https://judge.yosupo.jp/problem/chromatic_number) | Graph coloring via subset DP |

---

## Key Takeaways

1. **The Core Idea:** Use bitmask to represent subsets; dp[mask] = optimal value for partitioning mask
2. **Time Optimization:** Submask enumeration gives O(3^N) instead of O(4^N)
3. **Space Trade-off:** O(2^N) space for precomputed costs enables efficient transitions
4. **Pattern:** Subset partition DP - fundamental technique for small N optimization

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Write the submask enumeration loop from memory: `sub = (sub - 1) & mask`
- [ ] Explain why total complexity is O(3^N)
- [ ] Precompute subset costs in O(N^2 * 2^N)
- [ ] Handle both maximization and minimization variants

---

## Additional Resources

- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp/editorial)
- [CP-Algorithms: Submask Enumeration](https://cp-algorithms.com/algebra/all-submasks.html)
- [USACO Guide: Bitmask DP](https://usaco.guide/gold/dp-bitmasks)
