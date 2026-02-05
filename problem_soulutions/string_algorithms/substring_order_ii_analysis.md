---
layout: simple
title: "Substring Order II - String Algorithms Problem"
permalink: /problem_soulutions/string_algorithms/substring_order_ii_analysis
difficulty: Hard
tags: [suffix-array, lcp-array, binary-search, string-algorithms]
---

# Substring Order II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 2109 - Substring Order II](https://cses.fi/problemset/task/2109) |
| **Difficulty** | Hard |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Suffix Array + LCP Array + Binary Search |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Build suffix arrays efficiently using the doubling algorithm
- [ ] Compute LCP arrays using Kasai's algorithm
- [ ] Count substrings (with repetitions) using suffix array and LCP
- [ ] Apply binary search on cumulative substring counts
- [ ] Extract the k-th lexicographically smallest substring

---

## Problem Statement

**Problem:** Given a string, find the k-th lexicographically smallest substring. Substrings are **counted with repetitions** - if a substring appears multiple times, it is counted multiple times.

**Input:**
- Line 1: String s (lowercase letters only)
- Line 2: Integer k

**Output:**
- The k-th smallest substring

**Constraints:**
- 1 <= |s| <= 10^5
- 1 <= k <= n(n+1)/2 (guaranteed valid)

### Example

```
Input:
baabaa
10

Output:
baa
```

**Explanation:**
Substrings in lexicographical order (with repetitions):
1. "a" (position 2)
2. "a" (position 3)
3. "a" (position 5)
4. "aa" (position 2)
5. "aa" (position 4 - note: only one 'a' follows, so this might vary)
6. "aab" (position 2)
7. "aabaa" (position 2)
8. "abaa" (position 3)
9. "b" (position 0)
10. "baa" (position 0) <-- Answer

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we enumerate all substrings in sorted order without generating them explicitly?

The suffix array gives us all suffixes in sorted order. Each suffix starting at position `i` contributes `(n - i)` substrings (all prefixes of that suffix). These prefixes are automatically sorted because the suffixes are sorted.

### Breaking Down the Problem

1. **What are we looking for?** The k-th substring in lexicographical order (counting duplicates)
2. **What information do we have?** The sorted order of suffixes (via suffix array) and shared prefixes between adjacent suffixes (via LCP array)
3. **What's the relationship?** Each suffix contributes substrings; LCP tells us how many are duplicates with the previous suffix

### Key Insight

For suffix at position `sa[i]` with length `len = n - sa[i]`:
- It contributes `len` total substrings (all prefixes)
- But `lcp[i]` of them are duplicates of the previous suffix's prefixes
- **New substrings contributed = len - lcp[i]**

However, for Substring Order II we count WITH repetitions, so each suffix contributes ALL its `(n - sa[i])` substrings.

---

## Solution 1: Brute Force

### Idea

Generate all substrings, sort them, and return the k-th one.

### Code

```python
def solve_brute_force(s, k):
 """
 Generate all substrings, sort, return k-th.

 Time: O(n^3 log n) - generating and sorting all substrings
 Space: O(n^2) - storing all substrings
 """
 n = len(s)
 substrings = []

 for i in range(n):
  for j in range(i + 1, n + 1):
   substrings.append(s[i:j])

 substrings.sort()
 return substrings[k - 1]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 log n) | O(n^2) substrings, O(n log n) to sort strings |
| Space | O(n^2) | Store all substrings |

### Why This Works (But Is Slow)

Correctness is guaranteed since we enumerate everything. But with n = 10^5, we'd have ~10^10 substrings - far too many.

---

## Solution 2: Optimal - Suffix Array + Binary Search

### Key Insight

> **The Trick:** Use suffix array to get sorted suffix order. Each suffix contributes substrings in sorted order. Binary search to find which suffix contains the k-th substring.

### Algorithm Overview

1. Build suffix array (sorted positions of all suffixes)
2. For each suffix at `sa[i]`, it contributes `(n - sa[i])` substrings
3. Compute prefix sums of substring counts
4. Binary search to find which suffix contains substring k
5. Extract the appropriate prefix of that suffix

### Dry Run Example

Let's trace through with `s = "baa"`:

```
String: "baa" (n = 3)

Step 1: Build Suffix Array
  Suffixes:
    Position 0: "baa"
    Position 1: "aa"
    Position 2: "a"

  Sorted order: "a" < "aa" < "baa"
  Suffix Array: sa = [2, 1, 0]

Step 2: Count substrings per suffix
  sa[0] = 2: suffix "a"   -> contributes 1 substring:  "a"
  sa[1] = 1: suffix "aa"  -> contributes 2 substrings: "a", "aa"
  sa[2] = 0: suffix "baa" -> contributes 3 substrings: "b", "ba", "baa"

Step 3: Prefix sums
  cumulative = [1, 3, 6]

  Substring mapping:
    k=1: "a"    (from sa[0])
    k=2: "a"    (from sa[1], length 1)
    k=3: "aa"   (from sa[1], length 2)
    k=4: "b"    (from sa[2], length 1)
    k=5: "ba"   (from sa[2], length 2)
    k=6: "baa"  (from sa[2], length 3)

Step 4: Query k=4
  Binary search: cumulative[2] = 6 >= 4, cumulative[1] = 3 < 4
  So k=4 falls in suffix sa[2] = 0 ("baa")
  Offset within this suffix: 4 - 3 = 1
  Length = 1
  Answer: s[0:1] = "b"
```

### Visual Diagram

```
Suffix Array for "baabaa":

Position:  0    1    2    3    4    5
String:    b    a    a    b    a    a

Sorted Suffixes:
Rank | SA[i] | Suffix        | Substrings (count = n - SA[i])
-----|-------|---------------|--------------------------------
  0  |   5   | "a"           | 1: "a"
  1  |   2   | "abaa"        | 4: "a", "ab", "aba", "abaa"
  2  |   4   | "aa"          | 2: "a", "aa"
  3  |   1   | "aabaa"       | 5: "a", "aa", "aab", "aaba", "aabaa"
  4  |   3   | "baa"         | 3: "b", "ba", "baa"
  5  |   0   | "baabaa"      | 6: "b", "ba", "baa", "baab", "baaba", "baabaa"

Cumulative: [1, 5, 7, 12, 15, 21]

To find k=10:
- Binary search finds index 4 (cumulative[3]=12 < 10... wait, 12 >= 10)
- Actually: cumulative = [1, 5, 7, 12, 15, 21]
- k=10: cumulative[2]=7 < 10 <= cumulative[3]=12
- Falls in suffix sa[3]=1 ("aabaa")
- Offset = 10 - 7 = 3, so length = 3
- Answer = s[1:1+3] = "aab"
```

### Code (Python)

```python
def build_suffix_array(s):
 """
 Build suffix array using doubling algorithm.
 Time: O(n log n)
 """
 n = len(s)
 sa = list(range(n))
 rank = [ord(c) for c in s]
 tmp = [0] * n
 k = 1

 while k < n:
  def key(i):
   r1 = rank[i]
   r2 = rank[i + k] if i + k < n else -1
   return (r1, r2)

  sa.sort(key=key)

  tmp[sa[0]] = 0
  for i in range(1, n):
   tmp[sa[i]] = tmp[sa[i-1]]
   if key(sa[i]) != key(sa[i-1]):
    tmp[sa[i]] += 1

  rank = tmp[:]
  if rank[sa[n-1]] == n - 1:
   break
  k *= 2

 return sa

def solve(s, k):
 """
 Find k-th lexicographically smallest substring (with repetitions).

 Time: O(n log n)
 Space: O(n)
 """
 n = len(s)
 sa = build_suffix_array(s)

 # Compute prefix sums of substring counts
 # Each suffix sa[i] contributes (n - sa[i]) substrings
 cumulative = []
 total = 0
 for i in range(n):
  total += n - sa[i]
  cumulative.append(total)

 # Binary search for which suffix contains k-th substring
 left, right = 0, n - 1
 while left < right:
  mid = (left + right) // 2
  if cumulative[mid] < k:
   left = mid + 1
  else:
   right = mid

 # Suffix at sa[left] contains our answer
 idx = left
 prev_count = cumulative[idx - 1] if idx > 0 else 0
 offset = k - prev_count  # Which prefix of this suffix (1-indexed)

 start = sa[idx]
 length = offset

 return s[start:start + length]

# Read input and solve
import sys
input = sys.stdin.readline

s = input().strip()
k = int(input())
print(solve(s, k))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Suffix array construction dominates |
| Space | O(n) | Store suffix array and cumulative counts |

---

## Common Mistakes

### Mistake 1: Using 32-bit integers for k

**Problem:** With n = 10^5, total substrings = ~5 * 10^9, exceeding int range.
**Fix:** Use `long long` for k and cumulative counts.

### Mistake 2: Confusing with Substring Order I (distinct)

```python
# WRONG - This counts DISTINCT substrings (Substring Order I)
new_substrings = n - sa[i] - lcp[i]

# CORRECT for Substring Order II - count ALL substrings (with repetitions)
all_substrings = n - sa[i]
```

**Problem:** Substring Order I counts distinct substrings (subtract LCP), Order II counts with repetitions.
**Fix:** For Order II, each suffix contributes `(n - sa[i])` substrings without LCP subtraction.

### Mistake 3: Off-by-one in binary search

```python
# WRONG - Wrong boundary condition
while left <= right:
 mid = (left + right) // 2
 if cumulative[mid] < k:
  left = mid + 1
 else:
  right = mid - 1  # May skip the correct answer

# CORRECT
while left < right:
 mid = (left + right) // 2
 if cumulative[mid] < k:
  left = mid + 1
 else:
  right = mid  # Keep mid as potential answer
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `s="a", k=1` | `"a"` | Only one substring |
| k=1 | Any string | Smallest character | First in lex order |
| k=max | `s="ab", k=3` | `"b"` | Substrings: "a", "ab", "b" |
| Repeated characters | `s="aaa", k=6` | `"aaa"` | All substrings exist |
| Large k | `s="ab", k=3` | `"b"` | Must handle cumulative sums |

---

## When to Use This Pattern

### Use Suffix Array + Counting When:
- Finding k-th smallest/largest substring
- Problems involving lexicographical ordering of substrings
- Counting substrings with specific properties
- String comparison operations at scale

### Don't Use When:
- Simple string matching (use KMP or Z-algorithm)
- Only need to check substring existence (use hashing)
- Working with multiple separate strings (consider suffix automaton)

### Pattern Recognition Checklist:
- [ ] Need to order ALL substrings? -> **Suffix Array**
- [ ] Need to count distinct substrings? -> **Suffix Array + LCP** (Substring Order I)
- [ ] Need to count with repetitions? -> **Suffix Array only** (Substring Order II)
- [ ] Need k-th element? -> **Binary search on prefix sums**

---

## Related Problems

### Prerequisites (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [CSES - Distinct Substrings](https://cses.fi/problemset/task/2105) | Learn suffix array basics |
| [CSES - Substring Order I](https://cses.fi/problemset/task/2108) | Similar but counts distinct |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Longest Repeating Substring](https://cses.fi/problemset/task/2106) | Use max LCP value |
| [CSES - String Matching](https://cses.fi/problemset/task/1753) | Pattern matching with suffix array |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES - Repeating Substring](https://cses.fi/problemset/task/2107) | Finding repeated patterns |
| [CSES - Required Substring](https://cses.fi/problemset/task/1112) | DP + string matching |

---

## Key Takeaways

1. **The Core Idea:** Suffix array gives sorted order of all suffixes; each suffix's prefixes are substrings in sorted order
2. **Time Optimization:** From O(n^3) brute force to O(n log n) via suffix array
3. **Key Difference from Order I:** Order II counts with repetitions (no LCP subtraction)
4. **Pattern:** Binary search on cumulative counts to find k-th element

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a suffix array in O(n log n) time
- [ ] Explain why suffix array gives lexicographically sorted substrings
- [ ] Distinguish between Substring Order I (distinct) and II (with repetitions)
- [ ] Implement binary search on cumulative substring counts
- [ ] Handle large k values with appropriate data types

---

## Additional Resources

- [CP-Algorithms: Suffix Array](https://cp-algorithms.com/string/suffix-array.html)
- [CP-Algorithms: Kasai's LCP Algorithm](https://cp-algorithms.com/string/suffix-array.html#finding-the-longest-common-prefix-of-two-substrings-without-additional-memory)
- [CSES Substring Order II](https://cses.fi/problemset/task/2109) - K-th smallest substring
