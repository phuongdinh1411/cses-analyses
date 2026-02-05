---
layout: simple
title: "String Matching - Pattern Search in Text"
permalink: /problem_soulutions/string_algorithms/string_matching_analysis
difficulty: Easy
tags: [strings, kmp, z-algorithm, pattern-matching]
prerequisites: []
---

# String Matching

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | KMP Algorithm / Z-Algorithm |
| **CSES Link** | [String Matching](https://cses.fi/problemset/task/1753) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the string matching problem and its linear-time solutions
- [ ] Build and utilize the LPS (Longest Proper Prefix Suffix) array in KMP
- [ ] Implement the Z-algorithm as an alternative approach
- [ ] Recognize when to apply pattern matching algorithms

---

## Problem Statement

**Problem:** Given a text string and a pattern string, count the number of positions where the pattern occurs in the text.

**Input:**
- Line 1: Text string
- Line 2: Pattern string

**Output:**
- Print the number of occurrences of the pattern in the text

**Constraints:**
- 1 <= |text|, |pattern| <= 10^6
- Both strings contain only lowercase English letters (a-z)

### Example

```
Input:
saippuakauppias
pp

Output:
2
```

**Explanation:** The pattern "pp" occurs at positions 3 and 10 (0-indexed) in "saippuakauppias":
- Position 3: sai**pp**uakauppias
- Position 10: saippuakau**pp**ias

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we avoid re-comparing characters we have already seen?

The naive approach compares the pattern at every position, leading to O(n * m) time. The key insight is that when a mismatch occurs, the characters we have already matched contain information about where the next potential match could start.

### Breaking Down the Problem

1. **What are we looking for?** All positions where the pattern matches the text
2. **What information do we have?** The text and pattern strings
3. **What's the relationship between input and output?** Count overlapping occurrences

### Analogies

Think of this problem like searching for a word in a book. Instead of starting fresh after each failed attempt, you remember what you have already read to skip ahead intelligently.

---

## Solution 1: Brute Force

### Idea

Try to match the pattern at every possible starting position in the text.

### Algorithm

1. For each position i from 0 to n-m
2. Compare pattern with text[i:i+m] character by character
3. If all characters match, increment the count

### Code

```python
def solve_brute_force(text, pattern):
    """
    Brute force solution - check every position.

    Time: O(n * m)
    Space: O(1)
    """
    n, m = len(text), len(pattern)
    count = 0

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            count += 1

    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * m) | For each of n-m+1 positions, compare up to m characters |
| Space | O(1) | Only counters and loop variables |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every possible position. However, when pattern has repeated characters (like "aaa"), we waste time re-comparing characters we have already seen.

---

## Solution 2: KMP Algorithm (Optimal)

### Key Insight

> **The Trick:** Preprocess the pattern to build an LPS (Longest Proper Prefix which is also Suffix) array. When a mismatch occurs, use this array to skip characters that we know will match.

### LPS Array Definition

| State | Meaning |
|-------|---------|
| `lps[i]` | Length of the longest proper prefix of pattern[0..i] that is also a suffix |

**In plain English:** lps[i] tells us how many characters from the start of the pattern match the characters just before position i+1.

### Why LPS Works

When we have matched j characters and get a mismatch at position j:
- Characters pattern[0..j-1] matched text[i-j..i-1]
- lps[j-1] tells us the longest prefix of pattern that is also a suffix of what we matched
- We can safely skip to comparing pattern[lps[j-1]] next

### Algorithm

1. Build the LPS array for the pattern
2. Use two pointers: i for text, j for pattern
3. On match: increment both pointers
4. On mismatch: use LPS to skip characters in pattern
5. When j reaches m, we found a match

### Dry Run Example

Let's trace through with text = "ababcabab", pattern = "abab":

```
Step 1: Build LPS array for "abab"

  Index:  0   1   2   3
  Char:   a   b   a   b
  LPS:    0   0   1   2

  - lps[0] = 0 (no proper prefix for single char)
  - lps[1] = 0 ("ab" has no matching prefix/suffix)
  - lps[2] = 1 ("aba": prefix "a" = suffix "a")
  - lps[3] = 2 ("abab": prefix "ab" = suffix "ab")

Step 2: KMP Matching

  text:    a b a b c a b a b
  index:   0 1 2 3 4 5 6 7 8

  i=0, j=0: text[0]='a' == pattern[0]='a' -> i=1, j=1
  i=1, j=1: text[1]='b' == pattern[1]='b' -> i=2, j=2
  i=2, j=2: text[2]='a' == pattern[2]='a' -> i=3, j=3
  i=3, j=3: text[3]='b' == pattern[3]='b' -> i=4, j=4

  j=4 equals m=4: MATCH FOUND at position 0!
  j = lps[3] = 2 (continue searching)

  i=4, j=2: text[4]='c' != pattern[2]='a'
  j != 0, so j = lps[1] = 0

  i=4, j=0: text[4]='c' != pattern[0]='a'
  j == 0, so i=5

  i=5, j=0: text[5]='a' == pattern[0]='a' -> i=6, j=1
  i=6, j=1: text[6]='b' == pattern[1]='b' -> i=7, j=2
  i=7, j=2: text[7]='a' == pattern[2]='a' -> i=8, j=3
  i=8, j=3: text[8]='b' == pattern[3]='b' -> i=9, j=4

  j=4 equals m=4: MATCH FOUND at position 5!

Result: 2 matches found
```

### Visual Diagram

```
Text:    a b a b c a b a b
         -----             Match 1 at index 0
               -----       Match 2 at index 5

Pattern: a b a b
LPS:     0 0 1 2

When mismatch at 'c' (i=4, j=2):
  - We know "ab" just matched (positions 2-3 in text)
  - lps[1]=0 tells us no prefix of "ab" is also a suffix
  - Reset j to 0, but don't move i backwards
```

### Code

**Python Solution:**

```python
def build_lps(pattern):
    """
    Build Longest Proper Prefix Suffix array.

    Time: O(m)
    Space: O(m)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Use previously computed LPS value
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_count(text, pattern):
    """
    Count pattern occurrences using KMP algorithm.

    Time: O(n + m)
    Space: O(m)
    """
    n, m = len(text), len(pattern)

    if m == 0:
        return 0
    if m > n:
        return 0

    lps = build_lps(pattern)
    count = 0
    i = 0  # Index for text
    j = 0  # Index for pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            # Found a match
            count += 1
            j = lps[j - 1]  # Continue searching for overlapping matches
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return count


def solve():
    text = input().strip()
    pattern = input().strip()
    print(kmp_count(text, pattern))


if __name__ == "__main__":
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | O(m) for LPS construction, O(n) for matching |
| Space | O(m) | LPS array storage |

---

## Solution 3: Z-Algorithm (Alternative)

### Key Insight

> **The Trick:** Concatenate pattern + "$" + text, then compute Z-values. Positions where Z[i] equals pattern length are matches.

### Z-Array Definition

| State | Meaning |
|-------|---------|
| `z[i]` | Length of the longest substring starting at i that matches a prefix of the string |

### Code

**Python Solution:**

```python
def z_algorithm(s):
    """
    Compute Z-array for string s.

    Time: O(n)
    Space: O(n)
    """
    n = len(s)
    z = [0] * n
    z[0] = n
    l, r = 0, 0

    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])

        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] > r:
            l, r = i, i + z[i]

    return z


def z_count(text, pattern):
    """
    Count pattern occurrences using Z-algorithm.

    Time: O(n + m)
    Space: O(n + m)
    """
    m = len(pattern)
    if m == 0:
        return 0

    # Concatenate with separator
    combined = pattern + "$" + text
    z = z_algorithm(combined)

    count = 0
    for i in range(m + 1, len(combined)):
        if z[i] == m:
            count += 1

    return count


def solve():
    text = input().strip()
    pattern = input().strip()
    print(z_count(text, pattern))


if __name__ == "__main__":
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Linear Z-array construction |
| Space | O(n + m) | Combined string and Z-array |

---

## Common Mistakes

### Mistake 1: Incorrect LPS Construction

```python
# WRONG - Not handling the case when length != 0
while i < m:
    if pattern[i] == pattern[length]:
        length += 1
        lps[i] = length
        i += 1
    else:
        lps[i] = 0  # Should use lps[length-1] first!
        i += 1
```

**Problem:** Missing the fallback to previous LPS value.
**Fix:** When mismatch and length != 0, set length = lps[length - 1] and retry.

### Mistake 2: Forgetting Overlapping Matches

```python
# WRONG - Resets j to 0 after finding match
if j == m:
    count += 1
    j = 0  # Misses overlapping matches!
```

**Problem:** Pattern "aa" in text "aaa" should find 2 matches, not 1.
**Fix:** Set j = lps[j - 1] to allow overlapping matches.

### Mistake 3: Index Out of Bounds in Z-Algorithm

```python
# WRONG - Not checking bounds before comparison
while s[z[i]] == s[i + z[i]]:  # May go out of bounds!
    z[i] += 1
```

**Problem:** No bounds check leads to index error.
**Fix:** Add condition i + z[i] < n before comparison.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No matches | text="abc", pattern="xyz" | 0 | Pattern not in text |
| Pattern equals text | text="abc", pattern="abc" | 1 | Exact match |
| Pattern longer than text | text="ab", pattern="abc" | 0 | Cannot match |
| Single character repeated | text="aaaa", pattern="aa" | 3 | Overlapping matches |
| Empty pattern | text="abc", pattern="" | 0 | Edge case handling |
| Pattern at start | text="abcdef", pattern="abc" | 1 | Match at position 0 |
| Pattern at end | text="defabc", pattern="abc" | 1 | Match at last position |

---

## When to Use This Pattern

### Use KMP When:
- Finding all occurrences of a pattern in text
- Pattern may have repeated prefixes
- You need to find positions of matches (not just count)
- Working with streaming data

### Use Z-Algorithm When:
- You need additional prefix matching information
- Computing multiple pattern-related queries
- The problem involves prefix/suffix relationships

### Don't Use When:
- Pattern has wildcards (use regex or DP)
- Approximate matching needed (use edit distance)
- Multiple patterns to search (use Aho-Corasick)

### Pattern Recognition Checklist:
- [ ] Exact pattern matching? -> **KMP or Z-algorithm**
- [ ] Multiple patterns? -> **Aho-Corasick**
- [ ] Suffix queries? -> **Suffix Array/Tree**
- [ ] Approximate match? -> **Edit Distance DP**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Longest Palindrome](https://leetcode.com/problems/longest-palindrome/) | Basic string manipulation |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Finding Borders](https://cses.fi/problemset/task/1732) | Uses LPS array directly |
| [Finding Periods](https://cses.fi/problemset/task/1733) | Extension of border concept |
| [Implement strStr()](https://leetcode.com/problems/find-the-index-of-the-first-substring-in-a-string/) | Find first occurrence only |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimal Rotation](https://cses.fi/problemset/task/1110) | String rotation with comparison |
| [Longest Repeating Substring](https://leetcode.com/problems/longest-repeating-substring/) | Binary search + hashing |
| [Word Break](https://leetcode.com/problems/word-break/) | DP + string matching |

---

## Key Takeaways

1. **The Core Idea:** Use preprocessing to avoid re-comparing characters that we know will match.
2. **Time Optimization:** From O(n * m) brute force to O(n + m) with KMP/Z-algorithm.
3. **Space Trade-off:** O(m) extra space for LPS array enables linear time.
4. **Pattern:** Failure function / prefix function is fundamental to many string algorithms.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build the LPS array from scratch without reference
- [ ] Explain why KMP never backtracks in the text
- [ ] Implement Z-algorithm as an alternative
- [ ] Handle overlapping matches correctly
- [ ] Identify edge cases and handle them

---

## Additional Resources

- [CP-Algorithms: KMP](https://cp-algorithms.com/string/prefix-function.html)
- [CP-Algorithms: Z-function](https://cp-algorithms.com/string/z-function.html)
- [CSES String Matching](https://cses.fi/problemset/task/1753) - Pattern occurrence counting
