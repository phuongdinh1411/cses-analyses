---
layout: simple
title: "Distinct Substrings - String Algorithms Problem"
permalink: /problem_soulutions/string_algorithms/distinct_strings_analysis
difficulty: Medium
tags: [suffix-array, lcp, string-hashing, trie]
---

# Distinct Substrings

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/2223](https://cses.fi/problemset/task/2223) |
| **Difficulty** | Medium |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Suffix Array + LCP Array |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Build a Suffix Array in O(n log n) time
- [ ] Compute the LCP (Longest Common Prefix) array from a Suffix Array
- [ ] Use the formula: `distinct_substrings = n*(n+1)/2 - sum(LCP)` to count distinct substrings
- [ ] Understand the relationship between suffix arrays and substring enumeration

---

## Problem Statement

**Problem:** Given a string of length n, count the number of distinct substrings.

**Input:**
- A single string s containing only lowercase letters a-z

**Output:**
- One integer: the number of distinct substrings

**Constraints:**
- 1 <= n <= 10^5
- s contains only lowercase English letters

### Example

```
Input:
abab

Output:
7
```

**Explanation:** The distinct substrings are: "a", "b", "ab", "ba", "aba", "bab", "abab". Note that "a", "b", and "ab" each appear twice but are counted only once.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently count unique substrings without storing them all?

The total number of substrings in a string of length n is n*(n+1)/2. If we can figure out how many of these are duplicates, we get our answer.

### Breaking Down the Problem

1. **What are we looking for?** Count of unique substrings
2. **What information do we have?** A string of lowercase letters
3. **What's the relationship between input and output?** Each suffix contains all substrings starting at that position. The LCP between adjacent sorted suffixes tells us the overlap (duplicates).

### Key Insight

> **The Trick:** Each suffix of length k contributes k substrings (all its prefixes). When suffixes are sorted, the LCP with the previous suffix tells us how many prefixes are duplicates.

---

## Solution 1: Brute Force (HashSet)

### Idea

Generate all substrings and store them in a set to count unique ones.

### Algorithm

1. For each starting position i from 0 to n-1
2. For each ending position j from i to n-1
3. Extract substring s[i:j+1] and add to set
4. Return set size

### Code

```python
def count_distinct_brute(s):
    """
    Brute force using a set to store all substrings.

    Time: O(n^3) for generation + hashing
    Space: O(n^2) to store all substrings
    """
    n = len(s)
    substrings = set()

    for i in range(n):
        for j in range(i + 1, n + 1):
            substrings.add(s[i:j])

    return len(substrings)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | O(n^2) substrings, each taking O(n) to hash |
| Space | O(n^2) | Storing up to n*(n+1)/2 substrings |

### Why This Works (But Is Slow)

Correct because sets eliminate duplicates automatically. However, O(n^3) is too slow for n = 10^5.

---

## Solution 2: Optimal - Suffix Array + LCP

### Key Insight

> **The Trick:** Total substrings = n*(n+1)/2. Duplicates = sum of LCP values between adjacent sorted suffixes.

When we sort all suffixes alphabetically, adjacent suffixes with a common prefix represent duplicate substrings. The LCP array tells us exactly how many duplicates each suffix introduces.

### Why This Formula Works

Consider string "abab" with sorted suffixes:
- "ab" (pos 2) - contributes 2 substrings: "a", "ab"
- "abab" (pos 0) - LCP with "ab" is 2, so 2 duplicates. New: 4-2 = 2 substrings
- "b" (pos 3) - LCP with "abab" is 0, so 0 duplicates. New: 1 substring
- "bab" (pos 1) - LCP with "b" is 1, so 1 duplicate. New: 3-1 = 2 substrings

Total = 2 + 2 + 1 + 2 = 7 distinct substrings.

### Algorithm

1. Build the suffix array (sorted indices of all suffixes)
2. Compute the LCP array using Kasai's algorithm
3. Result = n*(n+1)/2 - sum(LCP)

### Dry Run Example

Let's trace through with input `s = "abab"`:

```
Step 1: List all suffixes with their starting indices
  Index 0: "abab"
  Index 1: "bab"
  Index 2: "ab"
  Index 3: "b"

Step 2: Sort suffixes alphabetically
  Sorted order: "ab" < "abab" < "b" < "bab"
  Suffix Array: [2, 0, 3, 1]

Step 3: Compute LCP array (LCP between adjacent sorted suffixes)
  LCP[0] = 0 (no previous suffix)
  LCP[1] = LCP("ab", "abab") = 2
  LCP[2] = LCP("abab", "b") = 0
  LCP[3] = LCP("b", "bab") = 1

Step 4: Apply formula
  Total substrings = 4 * 5 / 2 = 10
  Sum of LCP = 0 + 2 + 0 + 1 = 3
  Distinct = 10 - 3 = 7
```

### Visual Diagram

```
String: "abab" (n=4)

Sorted Suffixes:      Length:   LCP with prev:   New substrings:
  "ab"   (idx 2)        2           -               2
  "abab" (idx 0)        4           2               2  (4-2)
  "b"    (idx 3)        1           0               1  (1-0)
  "bab"  (idx 1)        3           1               2  (3-1)
                                                   ---
                                    Total:          7
```

### Code (Python)

```python
def build_suffix_array(s):
    """Build suffix array using O(n log n) algorithm."""
    n = len(s)
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    return [idx for _, idx in suffixes]

def build_lcp_array(s, sa):
    """Kasai's algorithm for LCP array in O(n)."""
    n = len(s)
    rank = [0] * n
    lcp = [0] * n

    for i, suffix_idx in enumerate(sa):
        rank[suffix_idx] = i

    k = 0
    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue

        j = sa[rank[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1

        lcp[rank[i]] = k
        if k > 0:
            k -= 1

    return lcp

def count_distinct_substrings(s):
    """
    Count distinct substrings using Suffix Array + LCP.

    Time: O(n log n) for suffix array, O(n) for LCP
    Space: O(n) for arrays
    """
    n = len(s)
    if n == 0:
        return 0

    sa = build_suffix_array(s)
    lcp = build_lcp_array(s, sa)

    total = n * (n + 1) // 2
    duplicates = sum(lcp)

    return total - duplicates

# Read input and solve
s = input().strip()
print(count_distinct_substrings(s))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Dominated by suffix array construction |
| Space | O(n) | Suffix array and LCP array |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** n*(n+1) can exceed 2^31 for n = 10^5.
**Fix:** Cast to `long long` before multiplication.

### Mistake 2: Forgetting LCP[0] = 0

```python
# WRONG - trying to compute LCP for first suffix
lcp[0] = some_computation()

# CORRECT - first sorted suffix has no predecessor
lcp[0] = 0  # Always zero
```

**Problem:** The first suffix in sorted order has no previous suffix to compare.
**Fix:** Always set LCP[0] = 0.

### Mistake 3: Using Simple Sorting

```python
# WRONG - O(n^2 log n) time
suffixes = [s[i:] for i in range(n)]
suffixes.sort()  # Each comparison is O(n)

# CORRECT - Use rank-based sorting for O(n log n)
# (See the full implementation above)
```

**Problem:** Comparing strings directly takes O(n) per comparison.
**Fix:** Use the doubling algorithm with ranks.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | "a" | 1 | Only one substring |
| All same chars | "aaa" | 3 | "a", "aa", "aaa" |
| All unique chars | "abc" | 6 | No duplicates: n*(n+1)/2 |
| Two characters alternating | "abab" | 7 | Multiple repeated substrings |
| Empty string | "" | 0 | No substrings |

---

## When to Use This Pattern

### Use Suffix Array + LCP When:
- Counting distinct substrings
- Finding longest repeated substring
- Computing the number of occurrences of each substring
- Problems involving suffix comparisons

### Don't Use When:
- Simple pattern matching (use KMP or Z-algorithm)
- You only need to check if a specific substring exists (use hashing)
- The string is very short (brute force is simpler)

### Pattern Recognition Checklist:
- [ ] Need to enumerate or count substrings? -> **Consider Suffix Array**
- [ ] Need to find common prefixes between suffixes? -> **Use LCP Array**
- [ ] Need to handle multiple pattern queries? -> **Suffix Array with binary search**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [String Matching](https://cses.fi/problemset/task/1753) | Basic pattern matching, introduction to string algorithms |
| [Finding Borders](https://cses.fi/problemset/task/1732) | Understanding prefix-suffix relationships |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Repeating Substring](https://cses.fi/problemset/task/2106) | Find the longest substring that appears at least twice |
| [Minimal Rotation](https://cses.fi/problemset/task/1110) | Uses suffix array for lexicographic comparison |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Required Substring](https://cses.fi/problemset/task/1112) | Combines DP with string constraints |
| [Substring Distribution](https://cses.fi/problemset/task/2110) | Count substrings of each length |

---

## Key Takeaways

1. **The Core Idea:** Distinct substrings = Total substrings - Duplicates (from LCP sum)
2. **Time Optimization:** From O(n^3) brute force to O(n log n) using suffix array
3. **Space Trade-off:** O(n) extra space for suffix array and LCP array
4. **Pattern:** This is a classic application of suffix array + LCP for substring counting

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a suffix array from scratch
- [ ] Implement Kasai's algorithm for LCP array
- [ ] Explain why the formula `n*(n+1)/2 - sum(LCP)` works
- [ ] Solve this problem without looking at the solution
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Suffix Array](https://cp-algorithms.com/string/suffix-array.html)
- [CP-Algorithms: LCP Array (Kasai's Algorithm)](https://cp-algorithms.com/string/suffix-array.html#finding-the-longest-common-prefix-of-two-substrings-with-additional-memory)
- [CSES Distinct Substrings](https://cses.fi/problemset/task/2105) - Suffix array LCP
