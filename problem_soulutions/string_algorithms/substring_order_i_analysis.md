---
layout: simple
title: "Substring Order I - String Algorithms Problem"
permalink: /problem_soulutions/string_algorithms/substring_order_i_analysis
difficulty: Hard
tags: [suffix-array, lcp-array, string-algorithms, binary-search]
---

# Substring Order I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/2108](https://cses.fi/problemset/task/2108) |
| **Difficulty** | Hard |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Suffix Array + LCP Array |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Build a suffix array and understand its lexicographical properties
- [ ] Construct an LCP (Longest Common Prefix) array efficiently
- [ ] Use LCP to count distinct substrings without duplication
- [ ] Apply binary search to find the k-th element in a cumulative sum array

---

## Problem Statement

**Problem:** Given a string and a value k, find the k-th lexicographically smallest **distinct** substring.

**Input:**
- Line 1: A string s of lowercase letters
- Line 2: An integer k

**Output:**
- The k-th lexicographically smallest distinct substring

**Constraints:**
- 1 <= |s| <= 10^5
- 1 <= k <= number of distinct substrings

### Example

```
Input:
ababab
3

Output:
aba
```

**Explanation:** The distinct substrings sorted lexicographically:
1. "a"
2. "ab"
3. "aba"    <-- k=3
4. "abab"
5. "ababab"
6. "b"
7. "ba"
8. "bab"
9. "baba"
10. "babab"

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently enumerate all distinct substrings in sorted order?

The suffix array gives us all suffixes sorted lexicographically. Each suffix contributes multiple substrings (its prefixes). The LCP array tells us how many of those prefixes are duplicates from the previous suffix.

### Breaking Down the Problem

1. **What are we looking for?** The k-th smallest distinct substring
2. **What information do we have?** A string and a position k
3. **What's the relationship?** Suffix array orders suffixes; each suffix's prefixes are substrings in sorted order

### Key Insight

```
For suffix at position i in suffix array:
- Total prefixes = n - SA[i]  (all substrings starting at SA[i])
- Duplicate prefixes = LCP[i]  (shared with previous suffix)
- New distinct substrings = (n - SA[i]) - LCP[i]
```

---

## Solution 1: Brute Force

### Idea

Generate all substrings, remove duplicates, sort them, and return the k-th one.

### Code

```python
def brute_force(s, k):
 """
 Time: O(n^2 log n) for generation and sorting
 Space: O(n^2) to store all substrings
 """
 substrings = set()
 n = len(s)
 for i in range(n):
  for j in range(i + 1, n + 1):
   substrings.add(s[i:j])

 sorted_subs = sorted(substrings)
 return sorted_subs[k - 1]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 log n) | Generate O(n^2) substrings, sort them |
| Space | O(n^2) | Store all distinct substrings |

**Why this is too slow:** For n = 10^5, we cannot store 10^10 substrings.

---

## Solution 2: Suffix Array + LCP (Optimal)

### Key Insight

> **The Trick:** Use suffix array for sorted order and LCP to skip duplicates. Binary search finds which suffix contains the k-th substring.

### Algorithm Overview

1. Build suffix array SA[] - gives suffixes in sorted order
2. Build LCP array - tells overlap with previous suffix
3. For each suffix i: new substrings = (n - SA[i]) - LCP[i]
4. Build cumulative count array
5. Binary search to find which suffix contains k-th substring
6. Extract the substring at the correct offset

### Dry Run Example

Let's trace through `s = "aba"`, `k = 3`:

```
Step 1: Build Suffix Array
Suffixes:     Sorted:
0: "aba"      1: "a"    (SA[0] = 2)
1: "ba"       0: "aba"  (SA[1] = 0)
2: "a"        1: "ba"   (SA[2] = 1)

SA = [2, 0, 1]

Step 2: Build LCP Array
LCP[0] = 0  (no previous suffix)
LCP[1] = 1  (lcp("a", "aba") = "a" -> length 1)
LCP[2] = 0  (lcp("aba", "ba") = "" -> length 0)

LCP = [0, 1, 0]

Step 3: Count New Substrings per Suffix
i=0: suffix "a",   new = (3-2) - 0 = 1  -> adds "a"
i=1: suffix "aba", new = (3-0) - 1 = 2  -> adds "ab", "aba"
i=2: suffix "ba",  new = (3-1) - 0 = 2  -> adds "b", "ba"

Cumulative: [1, 3, 5]

Step 4: Find k=3
Binary search: k=3 falls in suffix i=1 (cum[1]=3)
Offset within suffix = 3 - 1 = 2  (1 is cum[0])
Length = LCP[1] + offset = 1 + 2 = 3

Result: s[SA[1] : SA[1]+3] = s[0:3] = "aba"
```

### Visual Diagram

```
String: "aba" (n=3)

Suffix Array (sorted suffixes):
+-------+--------+------+-------+------------------+

| Index | SA[i]  | LCP  | Suffix| New Substrings   |
+-------+--------+------+-------+------------------+

|   0   |   2    |  0   | "a"   | 1: "a"           |
|   1   |   0    |  1   | "aba" | 2: "ab", "aba"   |
|   2   |   1    |  0   | "ba"  | 2: "b", "ba"     |
+-------+--------+------+-------+------------------+

Cumulative count: [1, 3, 5]
               k=1  k=2,3  k=4,5

For k=3: Find suffix 1, extract "aba"
```

### Code (Python)

```python
def build_suffix_array(s):
 """Build suffix array using O(n log n) algorithm."""
 n = len(s)
 sa = list(range(n))
 rank = [ord(c) for c in s]
 tmp = [0] * n
 k = 1

 while k < n:
  def key(i):
   return (rank[i], rank[i + k] if i + k < n else -1)
  sa.sort(key=key)

  tmp[sa[0]] = 0
  for i in range(1, n):
   tmp[sa[i]] = tmp[sa[i-1]]
   if key(sa[i]) != key(sa[i-1]):
    tmp[sa[i]] += 1
  rank = tmp[:]
  k *= 1

 return sa

def build_lcp(s, sa):
 """Build LCP array using Kasai's algorithm - O(n)."""
 n = len(s)
 rank = [0] * n
 for i in range(n):
  rank[sa[i]] = i

 lcp = [0] * n
 h = 0
 for i in range(n):
  if rank[i] > 0:
   j = sa[rank[i] - 1]
   while i + h < n and j + h < n and s[i + h] == s[j + h]:
    h += 1
   lcp[rank[i]] = h
   if h > 0:
    h -= 1
 return lcp

def solve(s, k):
 """
 Find k-th lexicographically smallest distinct substring.

 Time: O(n log n) for SA + O(n) for LCP + O(log n) for query
 Space: O(n)
 """
 n = len(s)
 sa = build_suffix_array(s)
 lcp = build_lcp(s, sa)

 # Build cumulative count of new substrings
 cum = []
 total = 0
 for i in range(n):
  new_count = (n - sa[i]) - lcp[i]
  total += new_count
  cum.append(total)

 # Binary search for the suffix containing k-th substring
 lo, hi = 0, n - 1
 while lo < hi:
  mid = (lo + hi) // 2
  if cum[mid] < k:
   lo = mid + 1
  else:
   hi = mid

 # Calculate substring length
 prev_cum = cum[lo - 1] if lo > 0 else 0
 offset = k - prev_cum  # Position within this suffix's new substrings
 length = lcp[lo] + offset

 return s[sa[lo]:sa[lo] + length]

# Main
s = input().strip()
k = int(input())
print(solve(s, k))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | SA construction dominates |
| Space | O(n) | SA, LCP, and cumulative arrays |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** With n = 10^5, total distinct substrings can reach ~5 * 10^9.
**Fix:** Use `long long` for cumulative counts.

### Mistake 2: Off-by-One in Length Calculation

```python
# WRONG
length = lcp[lo] + offset - 1

# CORRECT
length = lcp[lo] + offset
```

**Problem:** The offset represents "which new substring" (1-indexed within the suffix).
**Fix:** Add offset directly to LCP without subtracting 1.

### Mistake 3: Forgetting LCP[0] = 0

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single char | `"a", k=1` | `"a"` | Only one substring |
| All same chars | `"aaa", k=3` | `"aaa"` | Only 3 distinct: a, aa, aaa |
| k = 1 | `"cab", k=1` | `"a"` | Smallest is lexicographically first char |
| Max k | `"ab", k=3` | `"b"` | Substrings: a, ab, b |

---

## When to Use This Pattern

### Use This Approach When:
- Finding k-th lexicographically smallest substring
- Counting or enumerating distinct substrings
- Problems involving lexicographical ordering of substrings
- Need to avoid O(n^2) substring generation

### Don't Use When:
- Simple pattern matching (use KMP or Z-algorithm)
- Finding longest common substring between two strings (use different SA approach)
- String has special structure that allows simpler solution

### Pattern Recognition Checklist:
- [ ] Need substrings in sorted order? -> **Suffix Array**
- [ ] Need to count distinct substrings? -> **SA + LCP**
- [ ] Need k-th element in ordered set? -> **Binary search on cumulative counts**

---

## Related Problems

### Similar Difficulty (CSES)

| Problem | Key Difference |
|---------|----------------|
| [Substring Order II](https://cses.fi/problemset/task/2109) | Counts duplicates (non-distinct) |
| [Distinct Substrings](https://cses.fi/problemset/task/2105) | Count only, no need to find k-th |
| [Repeating Substring](https://cses.fi/problemset/task/2106) | Find longest repeating via LCP |

### Prerequisite Problems (CSES)

| Problem | Why It Helps |
|---------|--------------|
| [String Matching](https://cses.fi/problemset/task/1753) | Basic string algorithm foundation |
| [Finding Borders](https://cses.fi/problemset/task/1732) | Understanding string structure |

### Harder Extensions

| Problem | New Concept |
|---------|-------------|
| [Substring Distribution](https://cses.fi/problemset/task/2110) | Count substrings by length |
| [Finding Patterns](https://cses.fi/problemset/task/2102) | Multiple pattern matching |

---

## Key Takeaways

1. **Core Idea:** Suffix array gives sorted suffixes; each suffix's prefixes are substrings in sorted order
2. **LCP Optimization:** LCP[i] tells how many prefixes of suffix i are duplicates from suffix i-1
3. **Counting Formula:** New distinct substrings from suffix i = (n - SA[i]) - LCP[i]
4. **Binary Search:** Use cumulative counts to locate which suffix contains the k-th substring

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement suffix array construction from scratch
- [ ] Build LCP array using Kasai's algorithm
- [ ] Explain why LCP helps count distinct substrings
- [ ] Derive the substring extraction formula given suffix index and offset
- [ ] Handle edge cases with single characters and repeated patterns
