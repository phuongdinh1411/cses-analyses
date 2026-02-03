---
layout: simple
title: "SOS DP (Sum over Subsets) - Dynamic Programming Technique"
permalink: /problem_soulutions/dynamic_programming/sos_dp_analysis
difficulty: Hard
tags: [bitmask, dp, subset-sum, combinatorics]
---

# SOS DP (Sum over Subsets)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming / Bitmask |
| **Key Technique** | Sum over Subsets DP |
| **Time Complexity** | O(n * 2^n) |

### Concept Explanation

SOS DP is a technique to efficiently compute, for each bitmask `mask`, the sum (or count, min, max, etc.) over all subsets of that mask. Given an array `A` of size `2^n`, we want to compute:

```
F[mask] = sum of A[submask] for all submask where (submask & mask) == submask
```

The naive approach takes O(3^n), but SOS DP reduces this to O(n * 2^n).

### Learning Goals

After studying this technique, you will be able to:
- [ ] Understand bitmask subset relationships and iteration
- [ ] Implement SOS DP to compute subset sums in O(n * 2^n)
- [ ] Apply SOS DP to AND convolution and subset counting problems
- [ ] Recognize problems that can be optimized using SOS DP
- [ ] Differentiate between subset DP and superset DP formulations

---

## Problem Statement

**Problem:** Given an array `A` of `2^n` elements indexed by bitmasks from `0` to `2^n - 1`, compute array `F` where:

```
F[mask] = sum of A[i] for all i such that i is a subset of mask (i.e., i & mask == i)
```

**Input:**
- `n`: Number of bits
- `A[0..2^n-1]`: Array of values

**Output:**
- `F[0..2^n-1]`: Array where F[mask] = sum over all subsets of mask

**Constraints:**
- 1 <= n <= 20 (practical limit due to 2^n space)

### Example

```
Input: n = 2, A = [1, 2, 3, 4]  (indices: 00, 01, 10, 11)

Output: F = [1, 3, 4, 10]

Explanation:
F[00] = A[00] = 1                    (only subset is 00)
F[01] = A[00] + A[01] = 1 + 2 = 3    (subsets: 00, 01)
F[10] = A[00] + A[10] = 1 + 3 = 4    (subsets: 00, 10)
F[11] = A[00] + A[01] + A[10] + A[11] = 1 + 2 + 3 + 4 = 10
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we avoid recomputing overlapping subsets?

The key insight is to build up the answer dimension by dimension (bit by bit). Instead of iterating over all subsets directly, we process one bit position at a time, combining results from having that bit "on" or "off".

### Bitmask Visualization (n=3)

```
Bitmasks for n=3:
  Index (binary)   Index (decimal)   Subsets
  ─────────────────────────────────────────────
       000              0            {000}
       001              1            {000, 001}
       010              2            {000, 010}
       011              3            {000, 001, 010, 011}
       100              4            {000, 100}
       101              5            {000, 001, 100, 101}
       110              6            {000, 010, 100, 110}
       111              7            {all 8 masks}
```

### Breaking Down the Problem

1. **What are we looking for?** Sum over all subsets for each mask
2. **What information do we have?** Original array A indexed by bitmasks
3. **Key Relationship:** If `dp[mask][i]` = sum over subsets that differ only in bits 0..i-1, then we can build this incrementally

---

## Solution 1: Brute Force (O(3^n))

### Idea

For each mask, enumerate all its subsets using the standard subset enumeration technique.

### Algorithm

1. For each mask from 0 to 2^n - 1
2. Enumerate all subsets of mask
3. Sum up A[submask] for each subset

### Code

```python
def sos_brute_force(n: int, A: list[int]) -> list[int]:
    """
    Brute force: enumerate all subsets of each mask.

    Time: O(3^n) - each element belongs to 2^k supersets
    Space: O(2^n) for result array
    """
    size = 1 << n
    F = [0] * size

    for mask in range(size):
        submask = mask
        while True:
            F[mask] += A[submask]
            if submask == 0:
                break
            submask = (submask - 1) & mask

    return F
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(3^n) | Sum of 2^(popcount(mask)) over all masks = 3^n |
| Space | O(2^n) | Result array |

### Why This Is Slow

Each subset is counted multiple times across different masks. For n=20, 3^20 is about 3.5 billion operations.

---

## Solution 2: SOS DP (O(n * 2^n))

### Key Insight

> **The Trick:** Process one bit at a time. Build dp[mask][i] = sum over subsets that match mask in bits >= i.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask][i]` | Sum of A[s] for all s that are subsets of mask AND s agrees with mask on bits i to n-1 |

**In plain English:** After processing i bits, dp[mask][i] holds the partial sum considering only choices in the first i bit positions.

### State Transition

```
dp[mask][i+1] = dp[mask][i]                           (if bit i of mask is 0)
dp[mask][i+1] = dp[mask][i] + dp[mask ^ (1<<i)][i]   (if bit i of mask is 1)
```

**Why?** When bit i is 1 in mask, subsets can either have bit i as 0 or 1. We combine both cases.

### Space-Optimized Transition

Since we only need the previous iteration, we can use 1D array:

```
for i in 0 to n-1:
    for mask in 0 to 2^n - 1:
        if mask & (1 << i):
            dp[mask] += dp[mask ^ (1 << i)]
```

### Dry Run Example (n=3)

Let's trace through with `A = [1, 2, 3, 4, 5, 6, 7, 8]` (indices 000 to 111):

```
Initial: dp = A = [1, 2, 3, 4, 5, 6, 7, 8]

═══════════════════════════════════════════════════════
ITERATION i=0 (process bit 0):
───────────────────────────────────────────────────────
For each mask with bit 0 set, add dp[mask with bit 0 cleared]:

mask=001: dp[001] += dp[000]  =>  2 + 1 = 3
mask=011: dp[011] += dp[010]  =>  4 + 3 = 7
mask=101: dp[101] += dp[100]  =>  6 + 5 = 11
mask=111: dp[111] += dp[110]  =>  8 + 7 = 15

After i=0: dp = [1, 3, 3, 7, 5, 11, 7, 15]

═══════════════════════════════════════════════════════
ITERATION i=1 (process bit 1):
───────────────────────────────────────────────────────
For each mask with bit 1 set, add dp[mask with bit 1 cleared]:

mask=010: dp[010] += dp[000]  =>  3 + 1 = 4
mask=011: dp[011] += dp[001]  =>  7 + 3 = 10
mask=110: dp[110] += dp[100]  =>  7 + 5 = 12
mask=111: dp[111] += dp[101]  => 15 + 11 = 26

After i=1: dp = [1, 3, 4, 10, 5, 11, 12, 26]

═══════════════════════════════════════════════════════
ITERATION i=2 (process bit 2):
───────────────────────────────────────────────────────
For each mask with bit 2 set, add dp[mask with bit 2 cleared]:

mask=100: dp[100] += dp[000]  =>  5 + 1 = 6
mask=101: dp[101] += dp[001]  => 11 + 3 = 14
mask=110: dp[110] += dp[010]  => 12 + 4 = 16
mask=111: dp[111] += dp[011]  => 26 + 10 = 36

FINAL: dp = [1, 3, 4, 10, 6, 14, 16, 36]

═══════════════════════════════════════════════════════
VERIFICATION:
───────────────────────────────────────────────────────
F[111] = A[000]+A[001]+A[010]+A[011]+A[100]+A[101]+A[110]+A[111]
       = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 = 36  [Correct!]

F[101] = A[000] + A[001] + A[100] + A[101]
       = 1 + 2 + 5 + 6 = 14  [Correct!]
```

### Visual Diagram

```
Processing bit-by-bit for mask = 111 (binary):

             Original values
             ┌─────────────┐
             │    A[s]     │
             └─────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   Bit 0 = 0              Bit 0 = 1
   (000,010,100,110)      (001,011,101,111)
        │                     │
        └──────────┬──────────┘
                   ▼
             After i=0:
         dp[111] = sum of all
         masks ending in 1
        ┌──────────┴──────────┐
        ▼                     ▼
   Bit 1 = 0              Bit 1 = 1
        │                     │
        └──────────┬──────────┘
                   ▼
             After i=1:
         dp[111] includes
         all bit-1 variations
                   │
                   ▼
             After i=2:
         dp[111] = sum over
         ALL 8 subsets = 36
```

### Code (Python)

```python
def sos_dp(n: int, A: list[int]) -> list[int]:
    """
    SOS DP: Sum over Subsets in O(n * 2^n).

    Time: O(n * 2^n)
    Space: O(2^n)
    """
    size = 1 << n
    dp = A[:]  # Copy input array

    for i in range(n):  # Process each bit
        for mask in range(size):
            if mask & (1 << i):  # If bit i is set
                dp[mask] += dp[mask ^ (1 << i)]

    return dp
```

### Code (C++)

```cpp
#include <vector>
using namespace std;

vector<long long> sos_dp(int n, vector<long long>& A) {
    /*
     * SOS DP: Sum over Subsets in O(n * 2^n).
     *
     * Time: O(n * 2^n)
     * Space: O(2^n)
     */
    int size = 1 << n;
    vector<long long> dp(A);  // Copy input array

    for (int i = 0; i < n; i++) {          // Process each bit
        for (int mask = 0; mask < size; mask++) {
            if (mask & (1 << i)) {          // If bit i is set
                dp[mask] += dp[mask ^ (1 << i)];
            }
        }
    }

    return dp;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * 2^n) | n iterations, each processing 2^n masks |
| Space | O(2^n) | Single DP array |

### Why O(n * 2^n) Works

The magic comes from the **inclusion principle done incrementally**:
- Outer loop: n iterations (one per bit position)
- Inner loop: 2^n masks
- Total: n * 2^n operations

Compare to O(3^n): For n=20:
- O(3^n) = 3,486,784,401 operations
- O(n * 2^n) = 20 * 1,048,576 = 20,971,520 operations
- **167x faster!**

---

## Common Mistakes

### Mistake 1: Wrong Iteration Order

```python
# WRONG: Processing masks before bits
for mask in range(size):
    for i in range(n):  # Bits inside!
        if mask & (1 << i):
            dp[mask] += dp[mask ^ (1 << i)]
```

**Problem:** The dp values for smaller masks haven't been computed correctly yet when needed.
**Fix:** Always iterate bits in the outer loop, masks in the inner loop.

### Mistake 2: Confusing Subset vs Superset DP

```python
# SUBSET DP (sum over subsets of mask):
if mask & (1 << i):
    dp[mask] += dp[mask ^ (1 << i)]

# SUPERSET DP (sum over supersets of mask):
if not (mask & (1 << i)):
    dp[mask] += dp[mask | (1 << i)]
```

**Problem:** Using subset logic when superset is needed (or vice versa).
**Fix:** Understand which direction you need:
- Subset: smaller masks contribute to larger masks
- Superset: larger masks contribute to smaller masks

### Mistake 3: Not Copying Input Array

```python
# WRONG: Modifying input directly
dp = A  # Reference, not copy!

# CORRECT:
dp = A[:]  # Python
dp = A.copy()  # Also Python
vector<ll> dp(A);  // C++
```

### Mistake 4: Integer Overflow (C++)

```cpp
// WRONG: Using int for large sums
vector<int> dp(A);

// CORRECT: Use long long
vector<long long> dp(A.begin(), A.end());
```

---

## Edge Cases

| Case | Input | Expected Behavior | Notes |
|------|-------|-------------------|-------|
| n=0 | Single element | F[0] = A[0] | Trivial case |
| All zeros | A = [0,0,0,...] | F = [0,0,0,...] | Sum of zeros |
| Single set bit | A[k]=1, rest 0 | Only supersets of k are non-zero | Tests mask relationships |
| Max values | A[i] = 10^9 | Use long long | Sum can exceed 2^31 |
| n=1 | Two elements | F = [A[0], A[0]+A[1]] | Minimal non-trivial case |
| Negative values | Mixed signs | Works correctly | SOS DP handles negatives |

---

## When to Use This Pattern

### Use SOS DP When:
- Computing sum/count over all subsets of each bitmask
- AND convolution of two arrays: `C[k] = sum of A[i]*B[j] where i&j=k`
- Counting subsets with specific properties
- Problems involving "for each mask, consider all subsets"
- The constraint involves n <= 20 (since 2^n must fit in memory)

### Don't Use When:
- n > 20-22 (memory/time constraints)
- You only need subset sum for a single mask (use simple iteration)
- The problem involves OR convolution (different technique)
- Subset XOR problems (use linear algebra / Gaussian elimination)

### Pattern Recognition Checklist:
- [ ] Array indexed by bitmasks? -> **Consider SOS DP**
- [ ] "Sum over all subsets" phrase in problem? -> **Strong indicator**
- [ ] AND operation combining results? -> **AND convolution via SOS**
- [ ] Need inverse (Mobius transform)? -> **SOS with subtraction**
- [ ] Superset sum instead? -> **Reverse the bit condition**

---

## Variant: Superset Sum

To compute sum over all **supersets** instead of subsets:

```python
def superset_dp(n: int, A: list[int]) -> list[int]:
    """Sum over all supersets of each mask."""
    size = 1 << n
    dp = A[:]

    for i in range(n):
        for mask in range(size):
            if not (mask & (1 << i)):  # If bit i is NOT set
                dp[mask] += dp[mask | (1 << i)]

    return dp
```

---

## Related Problems

### Foundation Problems (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| Subset enumeration basics | Understand `submask = (submask-1) & mask` |
| Bitmask DP introduction | Familiarize with bitmask indexing |

### Direct Applications
| Problem | Key Concept |
|---------|-------------|
| [CSES - Counting Subsets](https://cses.fi/problemset/) | Direct SOS DP application |
| [Codeforces - Compatible Numbers](https://codeforces.com/contest/165/problem/E) | Find subset with AND = 0 |
| [Atcoder - AND Grid](https://atcoder.jp/contests/) | AND convolution |

### Advanced Problems
| Problem | New Concept |
|---------|-------------|
| Maximum AND subset | Combine with greedy/binary search |
| Mobius Transform | Inverse of SOS DP |
| Subset Sum Convolution | Combine with popcount dimension |

---

## Key Takeaways

1. **The Core Idea:** Process one bit at a time, accumulating contributions from having each bit on or off
2. **Time Optimization:** From O(3^n) to O(n * 2^n) by avoiding redundant subset enumeration
3. **Space Trade-off:** O(2^n) space is required and unavoidable
4. **Pattern:** This is a "dimension-by-dimension" DP technique, similar to Floyd-Warshall
5. **Variants:** Superset DP uses reversed bit condition; Mobius transform uses subtraction

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement SOS DP from scratch without reference
- [ ] Explain why the bit-by-bit approach is correct
- [ ] Convert between subset and superset formulations
- [ ] Identify SOS DP problems in contest settings
- [ ] Handle edge cases (n=0, negative values, overflow)
- [ ] Derive time complexity O(n * 2^n) mathematically

---

## Additional Resources

- [CP-Algorithms: Sum over Subsets](https://cp-algorithms.com/algebra/all-submasks.html)
- [Codeforces Blog: SOS DP](https://codeforces.com/blog/entry/45223)
- [CSES Problem Set](https://cses.fi/problemset/)
