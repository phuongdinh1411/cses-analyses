---
layout: simple
title: "Three-Way Equal-Value Partition of a Binary String"
permalink: /worldquant/three_way_equal_value_partition
difficulty: Hard
tags: [string, greedy, math, binary, worldquant]
---

# Three-Way Equal-Value Partition of a Binary String

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | String / Math / Greedy |
| **Key Technique** | Count total 1s, find cut points |
| **LeetCode** | [927 — Three Equal Parts](https://leetcode.com/problems/three-equal-parts/) |

### Learning Goals
- [ ] Partition a binary string into 3 parts with equal binary value
- [ ] Handle leading zeros correctly (the value, not the representation, must be equal)
- [ ] Use total 1-count to determine if a valid partition exists

### In 60 seconds
- **Pattern:** Count 1s, then pattern match
- **Key insight:** Equal values need equal counts of 1s; part 3 fixes the bit pattern (including trailing zeros), and parts 1 and 2 must copy it from their first 1.
- **Complexity:** O(n) time, O(n) space (O(1) possible)
- **Trap:** All-zero input (return `[0, n-1]`) and the LeetCode 927 return convention.

> **Say this in the interview:** "The last part has no freedom, so it defines the pattern the other two must match."

---

## Problem Statement

Given a binary string `s` of length `n`, split it into **three non-empty parts** with the **same binary value** (leading zeros allowed, so `"011"` equals `"11"`).

Return `[i, j]` using the LeetCode 927 convention:
- part 1 = `s[0..i]`
- part 2 = `s[i+1..j-1]`
- part 3 = `s[j..n-1]`

and `i + 1 < j`. If no split exists, return `[-1, -1]`.

**Constraints:**
- `3 <= n <= 3 * 10^4`
- `s[i]` is `'0'` or `'1'`

---

## Examples

### Example 1
```
Input:  s = "10101"
Output: [0, 3]

Part 1: s[0..0] = "1"  → 1
Part 2: s[1..2] = "01" → 1
Part 3: s[3..4] = "01" → 1
```

### Example 2
```
Input:  s = "11011"
Output: [-1, -1]      # 4 ones cannot be split into 3 equal groups
```

### Example 3
```
Input:  s = "1001001"
Output: [0, 4]

Part 1: s[0..0] = "1"   → 1
Part 2: s[1..3] = "001" → 1   (leading zeros are free)
Part 3: s[4..6] = "001" → 1
```

---

## Brute Force → Optimal Reasoning

**Brute force O(n²):** Try every pair of split indices `(i, j)` with `1 ≤ i < j ≤ n-1`. Compute the sum of `s[0..i-1]`, `s[i..j-1]`, and `s[j..n-1]` and check if they’re equal.

```python
# sketch: O(n²) brute force
def can_partition_brute(s):
    n = len(s)
    total = s.count('1')
    if total % 3 != 0: return False
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if s[:i].count('1') == s[i:j].count('1') == s[j:].count('1'):
                return True
    return False
```

**Why counting is O(n):** Total 1s must be divisible by 3; call that `t3`. The first boundary must fall after the `t3`-th one, the second after the `2×t3`-th one — two fixed positions computable in a single scan. No loop over pairs needed.

**Key insight:** The *positions* of boundaries are uniquely determined by where the cumulative 1-count crosses `t3` and `2×t3`. Everything between the fixed 1s can be zeros — the split is valid as long as the trailing zeros can be distributed correctly. This reduces a 2D search to two pointer positions found in O(n).

---

## Approach: Count 1s, then match the last part’s pattern

### Key observations

1. Equal values ⇒ equal numbers of 1s. If `ones % 3 != 0` → impossible.
2. If `ones == 0` → every part is 0; return `[0, n - 1]`.
3. **Part 3 is fixed**: it runs from the first 1 of the last group to the end of the string, so its trailing zeros are known. Parts 1 and 2 must reproduce that exact pattern (starting at their own first 1); any zeros before their first 1 are free leading zeros.

### Algorithm

```
k = ones // 3
p1, p2, p3 = index of the 1st, (k+1)-th, (2k+1)-th '1'
while p3 < n:
    if s[p1] != s[p2] or s[p2] != s[p3]: return [-1, -1]
    p1, p2, p3 += 1
return [p1 - 1, p2]       # p1-1 = end of part 1; p2 = start of part 3
```

If the walk succeeds, part 1's pattern ends at `p1 - 1`. Part 2 starts at `p1` (leading zeros allowed) and its pattern ends at `p2 - 1`, so part 3 starts at `p2`.

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) |
| **Space** | O(n) for the list of 1-positions (O(1) if you scan for the three starts) |

---

## Implementation

```python
def three_equal_parts(s: str) -> list[int]:
    n = len(s)
    ones_pos = [i for i, c in enumerate(s) if c == '1']
    total = len(ones_pos)

    if total % 3 != 0:
        return [-1, -1]
    if total == 0:
        return [0, n - 1]

    k = total // 3
    p1, p2, p3 = ones_pos[0], ones_pos[k], ones_pos[2 * k]
    while p3 < n:
        if s[p1] != s[p2] or s[p2] != s[p3]:
            return [-1, -1]
        p1 += 1; p2 += 1; p3 += 1
    return [p1 - 1, p2]
```

---

## Dry Run — `s = "1001001"`

- ones = 3, k = 1 → `p1 = 0`, `p2 = 3`, `p3 = 6`
- Compare `s[0], s[3], s[6]` = `1, 1, 1` → advance to `p1 = 1`, `p2 = 4`, `p3 = 7 = n` → stop
- Return `[p1 - 1, p2] = [0, 4]`
- Parts: `"1"`, `"001"`, `"001"` → 1, 1, 1 ✅

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Ignoring part 3's trailing zeros | Part 3 fixes them; the walk forces parts 1 and 2 to copy them |
| Treating leading zeros as significant | Start each walk at the part's first `1` |
| All-zero string | Return `[0, n - 1]`; `[0, 1]` would leave part 2 empty |
| Off-by-one in the return value | `p1 - 1` is the inclusive end of part 1; `p2` is the start of part 3 |

---

## Related Problems

| Problem | Note |
|---|---|
| LeetCode 927 — Three Equal Parts | This exact problem on 0/1 arrays |
| LeetCode 678 — Valid Parenthesis String | Partition/greedy on strings |
| Counting Pairs | Counting valid split positions |
