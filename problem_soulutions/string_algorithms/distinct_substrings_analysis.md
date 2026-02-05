---
layout: simple
title: "Distinct Substrings - String Algorithms Problem"
permalink: /problem_soulutions/string_algorithms/distinct_substrings_analysis
difficulty: Medium
tags: [suffix-array, lcp-array, string-processing]
prerequisites: []
---

# Distinct Substrings

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Suffix Array + LCP Array |
| **CSES Link** | [https://cses.fi/problemset/task/2105](https://cses.fi/problemset/task/2105) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Build a suffix array efficiently using sorting or radix sort
- [ ] Construct the LCP (Longest Common Prefix) array from a suffix array
- [ ] Apply the formula: distinct substrings = total substrings - sum(LCP)
- [ ] Recognize when suffix array + LCP is the optimal approach for substring problems

---

## Problem Statement

**Problem:** Given a string s, count the number of distinct substrings.

**Input:**
- Line 1: A string s consisting of lowercase English letters

**Output:**
- A single integer: the number of distinct substrings

**Constraints:**
- 1 <= |s| <= 10^5
- s contains only lowercase English letters (a-z)

### Example

```
Input:
abab

Output:
7
```

**Explanation:** The distinct substrings are: "a", "b", "ab", "ba", "aba", "bab", "abab". Note that "a" and "b" each appear twice in the string, but we count them only once.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently count unique substrings without generating all of them?

The insight is that every suffix of a string contains all substrings starting at that position. If we sort all suffixes lexicographically, consecutive suffixes share common prefixes - and these shared prefixes represent duplicate substrings. The LCP array captures exactly this redundancy.

### Breaking Down the Problem

1. **What are we looking for?** Count of unique substrings
2. **What information do we have?** A string of length n has n*(n+1)/2 total substrings (with duplicates)
3. **What's the relationship between input and output?** Distinct count = Total count - Duplicates

### Analogies

Think of this like counting unique words in a sorted dictionary. If consecutive words share a common prefix (like "pre-" in "predict" and "prefer"), we don't want to double-count that shared part. The LCP tells us exactly how many characters are shared.

---

## Solution 1: Brute Force

### Idea

Generate all possible substrings and store them in a set to eliminate duplicates.

### Algorithm

1. Iterate over all starting positions i from 0 to n-1
2. For each starting position, iterate over all ending positions j from i to n-1
3. Add substring s[i:j+1] to a hash set
4. Return the size of the set

### Code

```python
def count_distinct_brute(s: str) -> int:
    """
    Brute force: generate all substrings and use a set.

    Time: O(n^2) substrings, each taking O(n) to hash
    Space: O(n^2) for storing substrings
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
| Time | O(n^3) | O(n^2) substrings, each O(n) to create/hash |
| Space | O(n^2) | Up to n*(n+1)/2 unique substrings stored |

### Why This Works (But Is Slow)

Correctness is guaranteed because we enumerate all substrings. However, for n=10^5, this generates up to 5 billion substrings - far too slow.

---

## Solution 2: Optimal Solution (Suffix Array + LCP)

### Key Insight

> **The Trick:** Each suffix contributes (length - LCP with previous suffix) new distinct substrings.

A suffix of length L represents L unique substrings (its prefixes). When suffixes are sorted, the LCP with the previous suffix tells us how many of those substrings are duplicates.

### Core Formula

```
Distinct Substrings = n*(n+1)/2 - sum(LCP[i])
```

Or equivalently, sum over all suffixes: (suffix_length - LCP_with_previous).

### Algorithm

1. Build the suffix array (sort all suffix starting positions by lexicographic order)
2. Build the LCP array (longest common prefix between adjacent suffixes)
3. Total substrings = n*(n+1)/2
4. Subtract sum of all LCP values
5. Return the result

### Dry Run Example

Let's trace through with input `s = "abab"`:

```
Step 1: Generate all suffixes with their starting indices
  Index 0: "abab"
  Index 1: "bab"
  Index 2: "ab"
  Index 3: "b"

Step 2: Sort suffixes lexicographically
  Sorted order: "ab" (2), "abab" (0), "b" (3), "bab" (1)
  Suffix Array: [2, 0, 3, 1]

Step 3: Compute LCP array (LCP between adjacent sorted suffixes)
  LCP[0] = 0  (no previous suffix)
  LCP[1] = 2  ("ab" and "abab" share "ab")
  LCP[2] = 0  ("abab" and "b" share nothing)
  LCP[3] = 1  ("b" and "bab" share "b")

  LCP Array: [0, 2, 0, 1]

Step 4: Calculate distinct substrings
  Total possible = 4 * 5 / 2 = 10
  Sum of LCP = 0 + 2 + 0 + 1 = 3
  Distinct = 10 - 3 = 7

Answer: 7
```

### Visual Diagram

```
String: "abab" (n=4)

Sorted Suffixes:        Suffix  |  Length  |  LCP  |  New Substrings
                        --------|----------|-------|------------------
                        "ab"    |    2     |   0   |  2 ("a", "ab")
                        "abab"  |    4     |   2   |  2 ("aba", "abab")
                        "b"     |    1     |   0   |  1 ("b")
                        "bab"   |    3     |   1   |  2 ("ba", "bab")
                        --------|----------|-------|------------------
                        Total   |   10     |   3   |  7 distinct
```

### Code (Python)

```python
def count_distinct_substrings(s: str) -> int:
    """
    Count distinct substrings using Suffix Array + LCP.

    Time: O(n log n) for suffix array construction
    Space: O(n) for arrays
    """
    n = len(s)
    if n == 0:
        return 0

    # Build suffix array (indices sorted by suffix)
    suffix_array = sorted(range(n), key=lambda i: s[i:])

    # Build rank array (position of each suffix in sorted order)
    rank = [0] * n
    for i, sa in enumerate(suffix_array):
        rank[sa] = i

    # Build LCP array using Kasai's algorithm
    lcp = [0] * n
    k = 0
    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue
        j = suffix_array[rank[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k > 0:
            k -= 1

    # Distinct = total - duplicates
    total = n * (n + 1) // 2
    duplicates = sum(lcp)
    return total - duplicates


# Read input and solve
if __name__ == "__main__":
    s = input().strip()
    print(count_distinct_substrings(s))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Suffix array sorting dominates |
| Space | O(n) | Suffix array + rank + LCP arrays |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** n*(n+1) can exceed 2^31 for n = 10^5.
**Fix:** Cast to long long before multiplication.

### Mistake 2: Forgetting Empty LCP at Position 0

```python
# WRONG - Starting LCP sum from index 0 with undefined value
lcp = compute_lcp()
# Assuming lcp[0] has a meaningful value

# CORRECT - LCP[0] is always 0 (no previous suffix)
lcp[0] = 0  # First suffix has no predecessor
```

**Problem:** The first suffix in sorted order has no previous suffix to compare with.
**Fix:** Always set LCP[0] = 0.

### Mistake 3: Incorrect Kasai's Algorithm Implementation

```python
# WRONG - Not decrementing k properly
k = 0
for i in range(n):
    # ... compute lcp
    k = lcp[rank[i]]  # Wrong: should preserve k and decrement

# CORRECT
k = 0
for i in range(n):
    # ... compute lcp
    if k > 0:
        k -= 1  # Key optimization in Kasai's algorithm
```

**Problem:** Kasai's algorithm relies on the property that LCP can decrease by at most 1.
**Fix:** Decrement k by 1 (not reset to 0) after each iteration.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `"a"` | 1 | Only substring is "a" |
| All same characters | `"aaaa"` | 4 | "a", "aa", "aaa", "aaaa" |
| All distinct characters | `"abcd"` | 10 | n*(n+1)/2 = 10, no duplicates |
| Two characters alternating | `"abab"` | 7 | Some prefixes repeat |
| Empty string | `""` | 0 | No substrings possible |

---

## When to Use This Pattern

### Use Suffix Array + LCP When:
- Counting distinct substrings
- Finding longest repeated substring
- Comparing all pairs of suffixes efficiently
- Problems involving lexicographic ordering of substrings

### Don't Use When:
- Simple pattern matching (use KMP or Z-algorithm)
- String length is very small (brute force may be simpler)
- You only need to check existence of a specific substring

### Pattern Recognition Checklist:
- [ ] Need to count/enumerate all substrings? -> **Consider Suffix Array**
- [ ] Looking for repeated patterns in string? -> **Consider Suffix Array + LCP**
- [ ] Need lexicographically k-th substring? -> **Consider Suffix Array**
- [ ] Simple string matching? -> **Use KMP or hashing instead**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [String Matching (CSES 1753)](https://cses.fi/problemset/task/1753) | Basic string matching with KMP/Z-algorithm |
| [Finding Borders (CSES 1732)](https://cses.fi/problemset/task/1732) | Understanding string prefixes/suffixes |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Repeating Substring (CSES 2106)](https://cses.fi/problemset/task/2106) | Find longest substring that appears >= k times |
| [Longest Repeating Substring (LC 1062)](https://leetcode.com/problems/longest-repeating-substring/) | Find max LCP in array |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Substring Distribution (CSES 2110)](https://cses.fi/problemset/task/2110) | Count substrings of each length |
| [Distinct Substrings II (LC 940)](https://leetcode.com/problems/distinct-subsequences-ii/) | Subsequences instead of substrings |

---

## Key Takeaways

1. **The Core Idea:** Suffix Array + LCP lets us count duplicates among all substrings efficiently
2. **Time Optimization:** From O(n^3) brute force to O(n log n) with suffix array
3. **Space Trade-off:** O(n) space for suffix array and LCP array
4. **Pattern:** This is the standard approach for substring counting problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a suffix array from scratch (sorting-based approach)
- [ ] Implement Kasai's algorithm for LCP construction
- [ ] Explain why distinct = total - sum(LCP)
- [ ] Implement the full solution in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Suffix Array](https://cp-algorithms.com/string/suffix-array.html)
- [CP-Algorithms: LCP Array (Kasai's Algorithm)](https://cp-algorithms.com/string/suffix-array.html#lcp-array)
- [CSES Distinct Substrings](https://cses.fi/problemset/task/2105) - Count unique substrings
