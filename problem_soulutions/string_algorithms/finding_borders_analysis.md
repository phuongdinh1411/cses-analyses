---
layout: simple
title: "Finding Borders - String Algorithm Problem"
permalink: /problem_soulutions/string_algorithms/finding_borders_analysis
difficulty: Medium
tags: [strings, kmp, failure-function, prefix-suffix]
prerequisites: []
---

# Finding Borders

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | KMP Failure Function |
| **CSES Link** | [Finding Borders](https://cses.fi/problemset/task/1732) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the concept of borders (proper prefix that is also a proper suffix)
- [ ] Implement the KMP failure function (LPS array)
- [ ] Extract all borders from the failure function efficiently
- [ ] Apply this technique to pattern matching problems

---

## Problem Statement

**Problem:** Given a string, find all border lengths. A border is a proper prefix that is also a proper suffix of the string.

**Input:**
- A single string s consisting of lowercase English letters

**Output:**
- Print all border lengths in increasing order, separated by spaces

**Constraints:**
- 1 <= |s| <= 10^6
- String contains only lowercase letters a-z

### Example

```
Input:
abcab

Output:
2

Explanation: "ab" is both a prefix and suffix of "abcab"
```

```
Input:
abacaba

Output:
1 3

Explanation:
- "a" (length 1) is both prefix and suffix
- "aba" (length 3) is both prefix and suffix
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently find all substrings that appear at both the beginning and end of the string?

The KMP algorithm's failure function (also called LPS array - Longest Proper Prefix which is also Suffix) stores exactly this information. For each position i, it tells us the length of the longest proper prefix of s[0..i] that is also a suffix.

### Breaking Down the Problem

1. **What are we looking for?** All lengths k where s[0..k-1] == s[n-k..n-1]
2. **What information do we have?** The complete string
3. **What's the relationship?** The failure function at position n-1 gives the longest border; following the chain gives all borders

### The Failure Function Insight

The failure function has a crucial property: if `fail[n-1] = k`, then:
- `s[0..k-1]` is a border of length k
- `fail[k-1]` gives the next shorter border
- Following this chain gives ALL borders

```
String:    a b a c a b a
Index:     0 1 2 3 4 5 6
fail[]:    0 0 1 0 1 2 3
                       ^
                       |
              fail[6] = 3 -> "aba" is a border
              fail[2] = 1 -> "a" is a border
              fail[0] = 0 -> stop
```

---

## Solution 1: Brute Force

### Idea

Check every possible prefix length to see if that prefix equals the corresponding suffix.

### Algorithm

1. For each length k from 1 to n-1
2. Compare s[0..k-1] with s[n-k..n-1]
3. If equal, k is a border length

### Code

```python
def find_borders_brute(s):
    """
    Brute force: check all possible prefix/suffix pairs.

    Time: O(n^2)
    Space: O(1)
    """
    n = len(s)
    borders = []

    for k in range(1, n):
        if s[:k] == s[n-k:]:
            borders.append(k)

    return borders
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | n prefix lengths, each comparison takes O(k) |
| Space | O(1) | Only store border lengths |

### Why This Works (But Is Slow)

Correctness is guaranteed by exhaustive checking, but comparing strings of length k takes O(k) time, making the total O(n^2) which is too slow for n = 10^6.

---

## Solution 2: Optimal Solution using KMP Failure Function

### Key Insight

> **The Trick:** Build the KMP failure function in O(n), then follow the chain from fail[n-1] to find all borders.

### State Definition

| State | Meaning |
|-------|---------|
| `fail[i]` | Length of longest proper prefix of s[0..i] that is also a suffix |

**In plain English:** fail[i] tells us the longest "border" of the substring ending at position i.

### Building the Failure Function

```
fail[i] = longest k such that s[0..k-1] == s[i-k+1..i]
```

**Why?** We use previously computed values to extend matches or fall back efficiently.

### Algorithm

1. Build the failure function array
2. Start from `fail[n-1]` (longest border of entire string)
3. Follow the chain: length -> fail[length-1] -> fail[...] until 0
4. Reverse the collected lengths to get increasing order

### Dry Run Example

Let's trace through with input `s = "abacaba"`:

```
Building failure function:

i=0: fail[0] = 0  (by definition, no proper prefix)

i=1: s[1]='b', compare with s[0]='a'
     'b' != 'a', fail[1] = 0

i=2: s[2]='a', compare with s[0]='a'
     'a' == 'a', fail[2] = 1

i=3: s[3]='c', compare with s[fail[2]]='b'
     'c' != 'b', fall back to fail[0]=0
     s[3]='c' != s[0]='a', fail[3] = 0

i=4: s[4]='a', compare with s[0]='a'
     'a' == 'a', fail[4] = 1

i=5: s[5]='b', compare with s[fail[4]]='b'
     'b' == 'b', fail[5] = 2

i=6: s[6]='a', compare with s[fail[5]]='a'
     'a' == 'a', fail[6] = 3

Final: fail = [0, 0, 1, 0, 1, 2, 3]

Extracting borders:
- fail[6] = 3 -> border of length 3
- fail[2] = 1 -> border of length 1
- fail[0] = 0 -> stop

Borders (reversed): [1, 3]
```

### Visual Diagram

```
String: a b a c a b a
Index:  0 1 2 3 4 5 6
fail:   0 0 1 0 1 2 3

Border "aba" (length 3):
  a b a c a b a
  [---]     [---]
  prefix    suffix

Border "a" (length 1):
  a b a c a b a
  [.]         [.]
  prefix      suffix

Chain: fail[6]=3 -> fail[2]=1 -> fail[0]=0 (stop)
```

### Code

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    if n == 1:
        return  # No proper borders possible

    # Build failure function
    fail = [0] * n
    j = 0  # Length of previous longest prefix-suffix

    for i in range(1, n):
        # Fall back until match or j becomes 0
        while j > 0 and s[i] != s[j]:
            j = fail[j - 1]

        if s[i] == s[j]:
            j += 1

        fail[i] = j

    # Extract all borders by following the chain
    borders = []
    length = fail[n - 1]

    while length > 0:
        borders.append(length)
        length = fail[length - 1]

    # Print in increasing order
    if borders:
        print(' '.join(map(str, reversed(borders))))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Building fail array is O(n) amortized; extraction is O(number of borders) |
| Space | O(n) | Failure function array |

---

## Common Mistakes

### Mistake 1: Forgetting the Proper Prefix Requirement

```python
# WRONG: Including the entire string as a border
for k in range(1, n + 1):  # Should be range(1, n)
    if s[:k] == s[n-k:]:
        borders.append(k)
```

**Problem:** A border must be a PROPER prefix/suffix (not the entire string)
**Fix:** Loop only up to n-1, not n

### Mistake 2: Wrong Chain Following

```python
# WRONG: Using wrong index
length = fail[n - 1]
while length > 0:
    borders.append(length)
    length = fail[length]  # Should be fail[length - 1]
```

**Problem:** fail[length] is wrong because we need the border of the border substring s[0..length-1]
**Fix:** Use `fail[length - 1]`

### Mistake 3: Not Reversing the Output

```python
# WRONG: Printing in decreasing order
while length > 0:
    print(length, end=' ')  # Gives "3 1" instead of "1 3"
    length = fail[length - 1]
```

**Problem:** The problem asks for increasing order
**Fix:** Collect all borders, then reverse before printing

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `a` | (empty) | No proper prefix possible |
| No borders | `abc` | (empty) | No prefix equals suffix |
| All same | `aaaa` | `1 2 3` | Every prefix is a border |
| Alternating | `abab` | `2` | Only "ab" is a border |
| Long border | `abaaba` | `1 3` | "a" and "aba" |

---

## When to Use This Pattern

### Use This Approach When:
- Finding repeating patterns at start/end of strings
- KMP pattern matching (failure function is the core)
- String period detection (closely related)
- Any problem involving prefix-suffix relationships

### Don't Use When:
- You need substrings from arbitrary positions (use suffix array/Z-algorithm)
- You need multiple string comparison (use hashing or Aho-Corasick)
- The string changes dynamically (rebuild is expensive)

### Pattern Recognition Checklist:
- [ ] Does the problem involve prefix-suffix relationships? -> **Consider KMP failure function**
- [ ] Need to find repetitive structure? -> **Consider failure function + period formula**
- [ ] Pattern matching with single pattern? -> **Consider full KMP algorithm**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Longest Happy Prefix (LC 1392)](https://leetcode.com/problems/longest-happy-prefix/) | Just return fail[n-1], the longest border |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Finding Periods (CSES 1733)](https://cses.fi/problemset/task/1733) | Uses failure function to find periods |
| [Pattern Positions (CSES 1753)](https://cses.fi/problemset/task/1753) | Full KMP pattern matching |
| [Shortest Palindrome (LC 214)](https://leetcode.com/problems/shortest-palindrome/) | Uses KMP on s + "#" + reverse(s) |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimal Rotations (CSES 1110)](https://cses.fi/problemset/task/1110) | Combines borders with rotation |
| [String Matching (CSES 1753)](https://cses.fi/problemset/task/1753) | Full pattern matching |

---

## Key Takeaways

1. **The Core Idea:** The KMP failure function encodes all border information - just follow the chain from fail[n-1]
2. **Time Optimization:** From O(n^2) brute force to O(n) using amortized analysis of the failure function
3. **Space Trade-off:** O(n) space for the failure array enables linear time
4. **Pattern:** This is the foundation for KMP pattern matching and period detection

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build the failure function from scratch without reference
- [ ] Explain why building the failure function is O(n) amortized
- [ ] Extract all borders by following the chain
- [ ] Identify when border/failure function is applicable to new problems

---

## Additional Resources

- [CP-Algorithms: KMP Algorithm](https://cp-algorithms.com/string/prefix-function.html)
- [CSES Finding Borders](https://cses.fi/problemset/task/1732) - KMP failure function
