---
layout: simple
title: "Minimal Rotation - String Algorithm Problem"
permalink: /problem_soulutions/string_algorithms/minimal_rotation_analysis
difficulty: Medium
tags: [strings, rotation, booth-algorithm, lexicographic]
prerequisites: [string-basics, two-pointers]
---

# Minimal Rotation

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Booth's Algorithm |
| **CSES Link** | [Minimal Rotation](https://cses.fi/problemset/task/1110) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand string rotation concepts and lexicographic comparison
- [ ] Implement Booth's algorithm for finding minimal rotation in O(n) time
- [ ] Apply the doubled-string technique for circular string problems
- [ ] Recognize when to use specialized string algorithms over brute force

---

## Problem Statement

**Problem:** Given a string, find its lexicographically smallest rotation.

A rotation of a string is obtained by moving some number of characters from the beginning to the end. For example, the rotations of "abc" are "abc", "bca", and "cab".

**Input:**
- Line 1: A string s consisting of lowercase English letters

**Output:**
- The lexicographically smallest rotation of the string

**Constraints:**
- 1 <= |s| <= 10^6
- s contains only lowercase English letters (a-z)

### Example

```
Input:
abacaba

Output:
aabacab
```

**Explanation:** All rotations of "abacaba":
- Position 0: "abacaba"
- Position 1: "bacabaa"
- Position 2: "acabaab"
- Position 3: "cabaaba"
- Position 4: "abaabac"
- Position 5: "baabaca"
- Position 6: "aabacab" (smallest)

The lexicographically smallest is "aabacab" (rotation starting at position 6).

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently compare all rotations without explicitly generating them?

The key insight is that every rotation of a string s can be found as a substring of s+s (the string concatenated with itself). Instead of generating all n rotations and comparing them, we can use Booth's algorithm to find the starting position of the minimal rotation in linear time.

### Breaking Down the Problem

1. **What are we looking for?** The starting index k such that s[k:] + s[:k] is lexicographically smallest.
2. **What information do we have?** The original string s.
3. **What's the relationship between input and output?** The output is a rotation of the input, specifically the one that would come first in dictionary order.

### Analogies

Think of this problem like finding the "canonical form" of a necklace. If you have beads on a circular string and want to describe the necklace uniquely, you'd start reading from the position that gives the smallest sequence - that's exactly what we're computing.

---

## Solution 1: Brute Force

### Idea

Generate all n rotations explicitly and find the minimum using string comparison.

### Algorithm

1. For each starting position i from 0 to n-1
2. Generate the rotation s[i:] + s[:i]
3. Keep track of the lexicographically smallest rotation seen

### Code

```python
def solve_brute_force(s: str) -> str:
  """
  Brute force: try all rotations.

  Time: O(n^2)
  Space: O(n)
  """
  n = len(s)
  min_rotation = s

  for i in range(n):
    rotation = s[i:] + s[:i]
    if rotation < min_rotation:
      min_rotation = rotation

  return min_rotation
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | n rotations, each comparison takes O(n) |
| Space | O(n) | Store current rotation string |

### Why This Works (But Is Slow)

Correctness is guaranteed because we examine every possible rotation. However, with n up to 10^6, O(n^2) is far too slow (10^12 operations).

---

## Solution 2: Optimal - Booth's Algorithm

### Key Insight

> **The Trick:** Use two pointers to compare rotations character-by-character, eliminating candidates efficiently without generating full rotation strings.

Booth's algorithm maintains two candidate starting positions (i and j) and determines which leads to a smaller rotation by comparing characters at corresponding positions. When a mismatch is found, one candidate can be eliminated entirely along with several subsequent positions.

### Algorithm

1. Create doubled string: `t = s + s`
2. Initialize two candidate positions: `i = 0`, `j = 1`
3. Use `k` to track how many characters match between rotations at i and j
4. Compare `t[i+k]` vs `t[j+k]`:
   - If equal: increment k (keep comparing)
   - If `t[i+k] < t[j+k]`: rotation at i is better, eliminate j and positions up to j+k
   - If `t[i+k] > t[j+k]`: rotation at j is better, eliminate i and positions up to i+k
5. The smaller of i, j at the end is the answer

### Why This Works

When we find that `t[i+k] < t[j+k]`, we know:
- Rotation starting at j is worse than rotation at i
- Rotations starting at j+1, j+2, ..., j+k are also worse (they share the same prefix up to the mismatch point)

This allows us to skip multiple positions at once, achieving linear time.

### Dry Run Example

Let's trace through with input `s = "baca"`:

```
Doubled string t = "bacabaca"
n = 4

Initial: i=0, j=1, k=0

Step 1: Compare t[0+0]='b' vs t[1+0]='a'
  'b' > 'a', so rotation at j=1 is better
  Move i to i+k+1 = 0+0+1 = 1
  But i == j, so i = 2
  Reset k = 0
  State: i=2, j=1, k=0

Step 2: Compare t[2+0]='c' vs t[1+0]='a'
  'c' > 'a', so rotation at j=1 is better
  Move i to i+k+1 = 2+0+1 = 3
  Reset k = 0
  State: i=3, j=1, k=0

Step 3: Compare t[3+0]='a' vs t[1+0]='a'
  Equal, increment k
  State: i=3, j=1, k=1

Step 4: Compare t[3+1]='b' vs t[1+1]='c'
  'b' < 'c', so rotation at i=3 is better
  Move j to j+k+1 = 1+1+1 = 3
  But j == i, so j = 4
  Reset k = 0
  State: i=3, j=4, k=0

j >= n, so stop.

Answer: min(i, j) = min(3, 4) = 3
Result: s[3:] + s[:3] = "a" + "bac" = "abac"
```

### Visual Diagram

```
String: b a c a
Index:  0 1 2 3

Doubled: b a c a | b a c a
Index:   0 1 2 3   4 5 6 7

Comparing rotations:
  i=0: "baca"  vs  j=1: "acab"  -> 'b' > 'a', j wins, move i
  i=2: "caba"  vs  j=1: "acab"  -> 'c' > 'a', j wins, move i
  i=3: "abac"  vs  j=1: "acab"  -> 'a'='a', continue...
                                   'b' < 'c', i wins, move j

Final: position 3 -> "abac" is minimal rotation
```

### Code

```python
def solve_optimal(s: str) -> str:
  """
  Booth's Algorithm for minimal rotation.

  Time: O(n)
  Space: O(n) for doubled string
  """
  n = len(s)
  if n == 0:
    return s

  t = s + s  # Doubled string

  i = 0  # First candidate position
  j = 1  # Second candidate position
  k = 0  # Number of matching characters

  while i < n and j < n and k < n:
    a = t[i + k]
    b = t[j + k]

    if a == b:
      k += 1
    elif a < b:
      # Rotation at i is better, eliminate j through j+k
      j = j + k + 1
      if j == i:
        j += 1
      k = 0
    else:
      # Rotation at j is better, eliminate i through i+k
      i = i + k + 1
      if i == j:
        i += 1
      k = 0

  # The smaller index is the answer
  start = min(i, j)
  return s[start:] + s[:start]


def main():
  s = input().strip()
  print(solve_optimal(s))


if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each character position is visited at most twice (once by i, once by j) |
| Space | O(n) | Doubled string requires 2n characters |

---

## Common Mistakes

### Mistake 1: Forgetting to Handle i == j

```python
# WRONG
if a < b:
  j = j + k + 1
  k = 0  # Missing: check if j == i

# CORRECT
if a < b:
  j = j + k + 1
  if j == i:
    j += 1  # Skip to avoid comparing same position
  k = 0
```

**Problem:** When we advance j and it lands on i (or vice versa), we'd be comparing a rotation with itself.
**Fix:** Always check if i == j after advancing and skip if needed.

### Mistake 2: Using Wrong Loop Condition

```python
# WRONG
while k < n:  # May access out of bounds

# CORRECT
while i < n and j < n and k < n:
```

**Problem:** If i or j exceeds n-1, we're no longer comparing valid rotation start positions.
**Fix:** Include bounds check for both i and j.

### Mistake 3: Returning Index Instead of String

```python
# WRONG
return min(i, j)  # Returns position, not string

# CORRECT
start = min(i, j)
return s[start:] + s[:start]  # Returns actual rotation
```

**Problem:** The problem asks for the rotated string, not the starting index.
**Fix:** Use the index to construct and return the actual rotation.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `"a"` | `"a"` | Only one rotation exists |
| All same characters | `"aaaa"` | `"aaaa"` | All rotations are identical |
| Already minimal | `"abcd"` | `"abcd"` | Original is lexicographically smallest |
| Two characters | `"ba"` | `"ab"` | Simple swap case |
| Repeated pattern | `"abab"` | `"abab"` | Position 0 and 2 give same result |
| Descending order | `"dcba"` | `"adcb"` | Start from 'a' |

---

## When to Use This Pattern

### Use Booth's Algorithm When:
- Finding the lexicographically smallest/largest rotation
- Computing canonical forms for cyclic sequences
- Comparing circular strings for equality
- String fingerprinting in competitive programming

### Don't Use When:
- You need all rotations (just iterate)
- The string is very short (brute force is fine for n < 100)
- You need rotation by a specific amount (direct slicing is simpler)

### Pattern Recognition Checklist:
- [ ] Is the problem about circular/rotational strings? -> Consider doubled string technique
- [ ] Need the "smallest" or "canonical" rotation? -> Use Booth's Algorithm
- [ ] Need to check if two strings are rotations of each other? -> Check if one is substring of the other doubled

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Rotate String (LC 796)](https://leetcode.com/problems/rotate-string/) | Basic rotation understanding |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Repeated String Match (LC 686)](https://leetcode.com/problems/repeated-string-match/) | String repetition + matching |
| [String Matching (CSES 1753)](https://cses.fi/problemset/task/1753) | KMP/Z-algorithm for pattern matching |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Finding Borders (CSES 1732)](https://cses.fi/problemset/task/1732) | Failure function / KMP preprocessing |
| [Finding Periods (CSES 1733)](https://cses.fi/problemset/task/1733) | String periodicity |
| [Longest Palindrome (CSES 1111)](https://cses.fi/problemset/task/1111) | Manacher's algorithm |

---

## Key Takeaways

1. **The Core Idea:** Use two-pointer comparison on a doubled string to find minimal rotation in O(n) time.
2. **Time Optimization:** From O(n^2) brute force to O(n) by eliminating multiple candidates at once.
3. **Space Trade-off:** O(n) extra space for doubled string enables O(1) access to any rotation position.
4. **Pattern:** This is a classic example of the "doubled string" technique for circular problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why doubling the string helps with rotations
- [ ] Trace through Booth's algorithm by hand on a small example
- [ ] Implement the algorithm without looking at the solution
- [ ] Explain why the time complexity is O(n), not O(n^2)

---

## Additional Resources

- [CP-Algorithms: Lyndon Factorization](https://cp-algorithms.com/string/lyndon_factorization.html)
- [Wikipedia: Lexicographically minimal string rotation](https://en.wikipedia.org/wiki/Lexicographically_minimal_string_rotation)
- [CSES Minimal Rotation](https://cses.fi/problemset/task/1110) - Smallest cyclic rotation
