---
layout: simple
title: "Contribution Counting — Subarray & Subset Aggregation Patterns"
permalink: /pattern/contribution-counting
---

# Contribution Counting — Subarray & Subset Aggregation Patterns

Instead of iterating over all subarrays and checking a property, **flip the perspective**: for each element (or pair, or bit), ask *"how many subarrays does this contribute to?"* This is often the difference between O(n^2) and O(n).

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| **Sum of all subarray sums** | Element contribution | [1](#1-core-idea-the-mental-flip) |
| **Sum of subarray minimums/maximums** | Monotonic stack + contribution | [3](#3-monotonic-stack--contribution-sum-of-subarray-minimums) |
| **Sum of subarray ranges (max - min)** | Dual monotonic stack | [4](#4-sum-of-subarray-ranges-dual-contribution) |
| **Count unique chars across subarrays** | Per-character contribution with prev/next occurrence | [5](#5-per-character-contribution-unique-characters) |
| **Total hamming distance / XOR sums** | Bit-level contribution | [6](#6-bit-level-contribution) |
| **Pair contribution across subarrays** | Pair containment formula | [7](#7-pair-contribution) |
| **Sum of subsequence widths** | Sorted contribution with powers of 2 | [8](#8-subsequence-contribution) |
| Understand **when NOT to use** this technique | Limitations | [9](#9-when-contribution-counting-does-not-work) |

---

## Table of Contents

1. [Core Idea: The Mental Flip](#1-core-idea-the-mental-flip)
2. [Foundation: Element Containment Formula](#2-foundation-element-containment-formula)
3. [Monotonic Stack + Contribution: Sum of Subarray Minimums](#3-monotonic-stack--contribution-sum-of-subarray-minimums)
4. [Sum of Subarray Ranges: Dual Contribution](#4-sum-of-subarray-ranges-dual-contribution)
5. [Per-Character Contribution: Unique Characters](#5-per-character-contribution-unique-characters)
6. [Bit-Level Contribution](#6-bit-level-contribution)
7. [Pair Contribution](#7-pair-contribution)
8. [Subsequence Contribution](#8-subsequence-contribution)
9. [When Contribution Counting Does NOT Work](#9-when-contribution-counting-does-not-work)
10. [Pattern Recognition Cheat Sheet](#10-pattern-recognition-cheat-sheet)
11. [Problem Roadmap](#11-problem-roadmap)

---

## 1. Core Idea: The Mental Flip

**Traditional approach:**
```
for each subarray [l..r]:
    compute property → accumulate
```
This is O(n^2) subarrays × O(cost per subarray).

**Contribution counting:**
```
for each element/pair/bit:
    count how many subarrays it participates in → accumulate
```
This is O(n) elements × O(1) per element = **O(n)**.

### The Analogy

Imagine counting total tips at a restaurant:

- **Subarray approach:** Go table by table, sum each table's tips, then total everything --- slow with many tables.
- **Contribution approach:** Ask each waiter "how many tables did you serve?" and multiply by their tip rate --- one pass over waiters.

### Key Insight

Every aggregate over all subarrays can be decomposed as:

```
Total = Σ (contribution of each unit × number of subarrays containing that unit)
```

The "unit" can be an element, a pair, a bit position, a character occurrence --- whatever the problem decomposes into.

---

## 2. Foundation: Element Containment Formula

**Question:** For an array of length `n`, how many subarrays contain element at index `i`?

A subarray `[l..r]` contains index `i` when `l <= i` and `r >= i`.

```
Choices for l: 0, 1, ..., i       → (i + 1) choices
Choices for r: i, i+1, ..., n-1   → (n - i) choices

Subarrays containing nums[i] = (i + 1) × (n - i)
```

Visual:

```
Array:  [a, b, c, d, e]    n = 5
              ^
              i = 2

l can be: 0, 1, 2     → 3 choices  (i + 1)
r can be: 2, 3, 4     → 3 choices  (n - i)
Total subarrays containing c: 3 × 3 = 9

The 9 subarrays: [c], [b,c], [a,b,c], [c,d], [b,c,d], [a,b,c,d],
                 [c,d,e], [b,c,d,e], [a,b,c,d,e]
```

This is the **building block** for everything below.

### Application: Sum of All Subarray Sums

**Problem:** Find the sum of sums of all subarrays.

**Brute force:** O(n^2) --- enumerate all subarrays.

**Contribution:** Each `nums[i]` appears in `(i+1) × (n-i)` subarrays:

```python
def sum_of_subarray_sums(nums):
    n = len(nums)
    total = 0
    for i in range(n):
        total += nums[i] * (i + 1) * (n - i)
    return total
```

**O(n).** That's it.

### Verification

```
nums = [1, 2, 3]

Subarrays: [1]=1, [2]=2, [3]=3, [1,2]=3, [2,3]=5, [1,2,3]=6
Total = 1 + 2 + 3 + 3 + 5 + 6 = 20

Contribution:
  nums[0]=1: appears in (0+1)×(3-0) = 3 subarrays → 1 × 3 = 3
  nums[1]=2: appears in (1+1)×(3-1) = 4 subarrays → 2 × 4 = 8
  nums[2]=3: appears in (2+1)×(3-2) = 3 subarrays → 3 × 3 = 9
  Total = 3 + 8 + 9 = 20 ✓
```

---

## 3. Monotonic Stack + Contribution: Sum of Subarray Minimums

### Problem: LC 907 --- Sum of Subarray Minimums

For each `nums[i]`, find: **in how many subarrays is it the minimum?**

You need the **span** where `nums[i]` dominates as the minimum:

- `left[i]`: number of consecutive elements to the left where `nums[i]` is still the min (distance to previous smaller element)
- `right[i]`: number of consecutive elements to the right where `nums[i]` is still the min (distance to next smaller-or-equal element)

```
nums:    [3, 1, 2, 4]
          0  1  2  3

For nums[2] = 2:
  left boundary:  index 1 (value 1 < 2)
  left[2] = 2 - 1 = 1   (only index 2 itself)
  right boundary: index 4 (end of array)
  right[2] = 4 - 2 = 2  (indices 2, 3)

  Subarrays where 2 is minimum: 1 × 2 = 2
    → [2], [2, 4]
```

### Why Strict < on One Side, <= on the Other?

To avoid **double counting** with duplicates:

```
nums = [2, 2]

If both use strict <:
  nums[0]: left=1, right=2 → 2 subarrays
  nums[1]: left=2, right=1 → 2 subarrays
  Total = 4, but there are only 3 subarrays!

  Subarray [2,2] is counted TWICE (once by each 2).

Fix: Use strict < for previous, and <= for next.
  nums[0]: left=1, right=1 → 1   (only [2] at index 0)
  nums[1]: left=2, right=1 → 2   ([2] at index 1, and [2,2])
  Total = 3 ✓
```

### Implementation

```python
def sumSubarrayMins(nums):
    n = len(nums)
    MOD = 10**9 + 7

    # Previous Less Element (strictly less)
    left = [0] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    # Next Less-or-Equal Element
    right = [0] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] > nums[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    return sum(nums[i] * left[i] * right[i] for i in range(n)) % MOD
```

**Time:** O(n), **Space:** O(n)

### Walkthrough

```
nums = [3, 1, 2, 4]

Previous Less (strict <):
  i=0: stack=[], left[0]=0+1=1.     stack=[0]
  i=1: pop 0 (3>=1), stack=[], left[1]=1+1=2.  stack=[1]
  i=2: 1<2, stop. left[2]=2-1=1.    stack=[1,2]
  i=3: 2<4, stop. left[3]=3-2=1.    stack=[1,2,3]

  left = [1, 2, 1, 1]

Next Less-or-Equal (strict > in pop condition):
  i=3: stack=[], right[3]=4-3=1.     stack=[3]
  i=2: 4>2, pop 3. stack=[], right[2]=4-2=2.  stack=[2]
  i=1: 2>1, pop 2. stack=[], right[1]=4-1=3.  stack=[1]
  i=0: 1 not > 3, stop. right[0]=1-0=1. stack=[0,1]

  right = [1, 3, 2, 1]

Contributions:
  3 × 1 × 1 = 3
  1 × 2 × 3 = 6
  2 × 1 × 2 = 4
  4 × 1 × 1 = 4
  Total = 17

Verify: subarrays and their mins:
  [3]=3, [1]=1, [2]=2, [4]=4, [3,1]=1, [1,2]=1, [2,4]=2, [3,1,2]=1, [1,2,4]=1, [3,1,2,4]=1
  Sum = 3+1+2+4+1+1+2+1+1+1 = 17 ✓
```

---

## 4. Sum of Subarray Ranges: Dual Contribution

### Problem: LC 2104 --- Sum of Subarray Ranges

**Sum of (max - min) over all subarrays** = **Σ(max) - Σ(min)** over all subarrays.

Apply contribution counting **twice**: once for minimums (same as LC 907), once for maximums (flip the comparisons).

```python
def subArrayRanges(nums):
    n = len(nums)

    def contribution(compare_pop, compare_pop_right):
        """
        compare_pop: condition to pop for left pass
        compare_pop_right: condition to pop for right pass
        """
        left = [0] * n
        right = [0] * n

        stack = []
        for i in range(n):
            while stack and compare_pop(nums[stack[-1]], nums[i]):
                stack.pop()
            left[i] = i - stack[-1] if stack else i + 1
            stack.append(i)

        stack = []
        for i in range(n - 1, -1, -1):
            while stack and compare_pop_right(nums[stack[-1]], nums[i]):
                stack.pop()
            right[i] = stack[-1] - i if stack else n - i
            stack.append(i)

        return sum(nums[i] * left[i] * right[i] for i in range(n))

    # Sum of maximums: pop when stack top <= current (finding previous greater)
    sum_max = contribution(lambda a, b: a <= b, lambda a, b: a < b)
    # Sum of minimums: pop when stack top >= current (finding previous smaller)
    sum_min = contribution(lambda a, b: a >= b, lambda a, b: a > b)

    return sum_max - sum_min
```

**Time:** O(n), **Space:** O(n)

---

## 5. Per-Character Contribution: Unique Characters

### Problem: LC 828 --- Count Unique Characters of All Substrings

For each character occurrence, count subarrays where it is **unique** (appears exactly once).

A character at index `j` is unique in `[l..r]` if the **previous** same character is before `l` and the **next** same character is after `r`.

```
s = "ABA"
     0 1 2

For A at index 0:
  prev same char: -1 (none)
  next same char: 2
  l choices: l in [0, 0] → (-1, 0) exclusive → 0 - (-1) = 1
  r choices: r in [0, 1] → (0, 2) exclusive → 2 - 0 = 2
  Contribution: 1 × 2 = 2   → subarrays [A], [AB]

For B at index 1:
  prev same char: -1 (none)
  next same char: 3 (none)
  l choices: 1 - (-1) = 2
  r choices: 3 - 1 = 2
  Contribution: 2 × 2 = 4   → [B], [AB], [BA], [ABA]

For A at index 2:
  prev same char: 0
  next same char: 3 (none)
  l choices: 2 - 0 = 2
  r choices: 3 - 2 = 1
  Contribution: 2 × 1 = 2   → [BA], [A]

Total = 2 + 4 + 2 = 8
```

```python
def uniqueLetterString(s):
    n = len(s)
    # For each char, track indices where it appears
    last = {}   # char → list of indices
    for i, c in enumerate(s):
        last.setdefault(c, [-1]).append(i)
    for c in last:
        last[c].append(n)  # sentinel

    total = 0
    for c in last:
        indices = last[c]
        for k in range(1, len(indices) - 1):
            prev_idx = indices[k - 1]
            curr_idx = indices[k]
            next_idx = indices[k + 1]
            total += (curr_idx - prev_idx) * (next_idx - curr_idx)
    return total
```

**Time:** O(n), **Space:** O(n)

### Variant: LC 2262 --- Total Appeal of a String

Appeal = number of **distinct** characters in a substring. Each character contributes 1 to appeal for every subarray where it appears **at least once**.

For character at index `i` with previous occurrence at `prev`:

```
Subarrays where this occurrence is the FIRST of its character:
  l choices: prev+1, prev+2, ..., i  → (i - prev)
  r choices: i, i+1, ..., n-1        → (n - i)
  Contribution: (i - prev) × (n - i)
```

```python
def appealSum(s):
    n = len(s)
    prev = {}  # char → last seen index
    total = 0
    for i, c in enumerate(s):
        p = prev.get(c, -1)
        total += (i - p) * (n - i)
        prev[c] = i
    return total
```

**O(n) time, O(26) space.** Elegantly simple.

---

## 6. Bit-Level Contribution

### Problem: LC 477 --- Total Hamming Distance

For each bit position, count elements with that bit set vs unset. Each (set, unset) pair contributes 1 to Hamming distance.

```python
def totalHammingDistance(nums):
    total = 0
    n = len(nums)
    for bit in range(30):
        ones = sum(1 for x in nums if x & (1 << bit))
        zeros = n - ones
        total += ones * zeros
    return total
```

**Time:** O(30n), **Space:** O(1)

### Problem: Sum of XOR of All Subarrays

For each bit position `b` and index `i`, `nums[i]`'s bit `b` contributes to the XOR of subarray `[l..r]` only if the count of set bits at position `b` in `[l..r]` is **odd**.

Use prefix XOR to count:

```python
def sum_xor_all_subarrays(nums):
    total = 0
    n = len(nums)
    for bit in range(30):
        # prefix[i] = XOR of bit b for nums[0..i-1]
        # Count prefix values where bit b is 0 vs 1
        count = [1, 0]  # count[0]=1 for empty prefix
        prefix_bit = 0
        for num in nums:
            prefix_bit ^= (num >> bit) & 1
            count[prefix_bit] += 1
        # Subarrays with odd count = pairs (prefix=0, prefix=1)
        total += count[0] * count[1] * (1 << bit)
    return total
```

---

## 7. Pair Contribution

For a pair of indices `(i, j)` with `i < j`, a subarray `[l..r]` contains both when `l <= i` and `r >= j`:

```
Count of subarrays containing pair (i, j) = (i + 1) × (n - j)
```

### Application: Total Equal Pairs Across All Subarrays

```python
def total_equal_pairs(nums):
    n = len(nums)
    # Group indices by value
    from collections import defaultdict
    positions = defaultdict(list)
    for i, v in enumerate(nums):
        positions[v].append(i)

    total = 0
    for indices in positions.values():
        for k in range(len(indices)):
            j = indices[k]
            # For each pair (i, j) where i < j and nums[i] == nums[j]
            # Contribution: (i+1) × (n-j)
            # Optimize: for fixed j, sum over all i < j with same value
            #   = (n - j) × Σ(i + 1) for all previous i
            # Track running sum of (i+1)
            pass

    # Cleaner O(n) approach:
    total = 0
    prefix_sum = defaultdict(int)  # value → running sum of (i+1)
    for j in range(n):
        total += prefix_sum[nums[j]] * (n - j)
        prefix_sum[nums[j]] += j + 1
    return total
```

**Time:** O(n), **Space:** O(n)

---

## 8. Subsequence Contribution

### Problem: LC 891 --- Sum of Subsequence Widths

Width = max - min of a subsequence. For each element, count subsequences where it's the max minus where it's the min.

**After sorting:** For `nums[i]` in sorted order:
- Subsequences where `nums[i]` is the max: any subset of `nums[0..i-1]` plus `nums[i]` → `2^i` subsequences
- Subsequences where `nums[i]` is the min: any subset of `nums[i+1..n-1]` plus `nums[i]` → `2^(n-1-i)` subsequences

```python
def sumSubseqWidths(nums):
    MOD = 10**9 + 7
    nums.sort()
    n = len(nums)
    total = 0
    for i in range(n):
        # As max: contributes +nums[i] × 2^i
        # As min: contributes -nums[i] × 2^(n-1-i)
        total += nums[i] * (pow(2, i, MOD) - pow(2, n - 1 - i, MOD))
        total %= MOD
    return total % MOD
```

**Time:** O(n log n) for sort, **Space:** O(1)

---

## 9. When Contribution Counting Does NOT Work

Contribution counting works when contributions are **independent and additive**. It fails when the problem requires a **threshold or interaction** between contributions within the same subarray.

| Works (independent, additive) | Does NOT Work (threshold / interaction) |
|-------------------------------|----------------------------------------|
| "Sum of minimums of all subarrays" | "Count subarrays with at least k equal pairs" |
| "Total equal pairs across all subarrays" | "Count subarrays where min > X" |
| "Sum of XOR of all subarrays" | "Count subarrays with at most k distinct elements" |
| "Total appeal of all substrings" | "Longest subarray where max - min <= k" |
| "Sum of subsequence widths" | "Count subarrays with XOR > target" |

### The Dividing Line

Ask: **"Can I compute each unit's contribution independently of other units?"**

- **YES** → Contribution counting. Each element/pair/bit contributes some value × (number of subarrays containing it).
- **NO** → The answer depends on the *combination* of elements within a subarray. Use **sliding window**, **DP**, or **segment tree** instead.

### The "At Least k" Trap

For LC 2537 (Count Good Subarrays, at least k equal pairs):

You CAN count total equal pairs across ALL subarrays using contribution: each pair `(i,j)` appears in `(i+1) × (n-j)` subarrays.

But you CANNOT count subarrays with **at least k** pairs, because that requires knowing how many pairs are **simultaneously** inside each specific subarray. The contributions interact --- you need **sliding window** for that.

---

## 10. Pattern Recognition Cheat Sheet

| Signal in Problem | Technique | Example |
|--------------------|-----------|---------|
| "Sum of [property] over ALL subarrays" | Element contribution `(i+1)×(n-i)` | Sum of subarray sums |
| "Sum of min/max over all subarrays" | Monotonic stack + contribution | LC 907, LC 2104 |
| "Unique/distinct characters in all substrings" | Per-char with prev/next occurrence | LC 828, LC 2262 |
| "Total hamming distance" / bit aggregates | Bit-level contribution | LC 477 |
| "Sum of pairs across all subarrays" | Pair formula `(i+1)×(n-j)` | Total equal pairs |
| "Subsequence widths / ranges" | Sort + power-of-2 counting | LC 891 |
| "How many subarrays contain element X?" | Direct formula `(i+1)×(n-i)` | Sum of odd-length sums |
| "Appeal / distinctness across substrings" | Last-occurrence contribution | LC 2262 |

### Decision Flowchart

```
Problem asks for aggregate over ALL subarrays?
├── YES → Can each element/pair contribute independently?
│   ├── YES → CONTRIBUTION COUNTING
│   │   ├── Involves min/max? → + Monotonic Stack
│   │   ├── Involves distinct chars? → + Last occurrence tracking
│   │   └── Involves bits? → + Bit decomposition
│   └── NO (threshold / k constraint) → Sliding Window or DP
└── NO (single subarray: longest, count satisfying X) → Sliding Window / DP / Binary Search
```

---

## 11. Problem Roadmap

### Tier 1 --- Direct Element Contribution

| # | Problem | Key Technique |
|---|---------|---------------|
| 1 | **LC 1588** --- Sum of All Odd Length Subarrays | `nums[i] × count_of_odd_length_subarrays_containing_i` |
| 2 | **LC 1748** --- Sum of Unique Elements | Basic contribution warm-up |

### Tier 2 --- Monotonic Stack + Contribution

| # | Problem | Key Technique |
|---|---------|---------------|
| 3 | **LC 907** --- Sum of Subarray Minimums | PLE/NLE + contribution (the canonical problem) |
| 4 | **LC 2104** --- Sum of Subarray Ranges | Dual contribution: sum_max - sum_min |
| 5 | **LC 1856** --- Maximum Subarray Min-Product | Monotonic stack span × prefix sum |

### Tier 3 --- Per-Character / Occurrence Contribution

| # | Problem | Key Technique |
|---|---------|---------------|
| 6 | **LC 828** --- Count Unique Characters of All Substrings | prev/next same char → span product |
| 7 | **LC 2262** --- Total Appeal of a String | Last occurrence tracking, O(n) one-pass |

### Tier 4 --- Bit-Level & Pair Contribution

| # | Problem | Key Technique |
|---|---------|---------------|
| 8 | **LC 477** --- Total Hamming Distance | Per-bit: ones × zeros |
| 9 | **LC 1863** --- Sum of All Subset XOR Totals | Each bit set in `2^(n-1)` subsets |
| 10 | **LC 2425** --- Bitwise XOR of All Pairings | Contribution counting on bits |

### Tier 5 --- Advanced Contribution

| # | Problem | Key Technique |
|---|---------|---------------|
| 11 | **LC 891** --- Sum of Subsequence Widths | Sort + contribution via powers of 2 |
| 12 | **LC 2681** --- Power of Heroes | Sorted contribution with prefix sums |
| 13 | **LC 2262** --- Total Appeal of a String | One-pass elegance |
| 14 | **LC 1498** --- Number of Subsequences That Satisfy the Given Sum | Sort + two pointers + power contribution |

---

## Summary

The core skill is always the same: **stop thinking about subarrays, start thinking about what each element (or pair, or bit) contributes to the final answer.**

```
Total = Σ (value of unit) × (number of subarrays/subsets containing that unit)
```

Master the containment formula `(i+1) × (n-i)`, learn to combine it with monotonic stacks for min/max problems and with last-occurrence tracking for character problems, and you'll solve an entire class of "aggregate over all subarrays" problems in O(n).
