---
layout: simple
title: "Repeating Substring - String Algorithm Problem"
permalink: /problem_soulutions/string_algorithms/repeating_substring_analysis
difficulty: Medium
tags: [string, hashing, binary-search, suffix-array]
---

# Repeating Substring

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/2106](https://cses.fi/problemset/task/2106) |
| **Difficulty** | Medium |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Binary Search + Hashing / Suffix Array |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply binary search on answer to find optimal string length
- [ ] Implement rolling hash (Rabin-Karp) for O(1) substring comparison
- [ ] Understand suffix arrays and LCP arrays for string problems
- [ ] Choose between hashing and suffix array approaches based on constraints

---

## Problem Statement

**Problem:** Find the longest substring that appears at least twice in a given string.

**Input:**
- A single string `s` of lowercase English letters

**Output:**
- The length of the longest repeating substring
- If such a substring exists, print the length; otherwise print `-1`

**Constraints:**
- 1 <= |s| <= 10^5
- s contains only lowercase English letters (a-z)

### Example

```
Input:
ababab

Output:
4
```

**Explanation:** The substring "abab" appears twice:
- At position 0: **abab**ab
- At position 2: ab**abab**

These occurrences overlap, which is allowed.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently check if a repeating substring of length `k` exists?

If a repeating substring of length `k` exists, then a repeating substring of length `k-1` also exists (just take a prefix). This **monotonic property** means we can binary search on the answer!

### Breaking Down the Problem

1. **What are we looking for?** The maximum length `L` such that some substring of length `L` appears at least twice.
2. **What information do we have?** A string where we can extract and compare substrings.
3. **What's the relationship?** If length `L` works, all lengths < `L` also work. If `L` doesn't work, no length > `L` works.

### Analogies

Think of this like finding the longest common prefix among duplicate entries in a sorted phone book. If we sort all suffixes of the string, duplicates (repeating substrings) will be adjacent!

---

## Solution 1: Brute Force

### Idea

Check all possible substrings and count their occurrences using a hash set.

### Algorithm

1. For each length `L` from `n-1` down to `1`
2. Extract all substrings of length `L`
3. If any substring appears twice, return `L`

### Code

```python
def solve_brute_force(s):
 """
 Brute force: check all substrings.
 Time: O(n^3)  Space: O(n^2)
 """
 n = len(s)
 for length in range(n - 1, 0, -1):
  seen = set()
  for i in range(n - length + 1):
   sub = s[i:i + length]
   if sub in seen:
    return length
   seen.add(sub)
 return -1
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | O(n) lengths x O(n) substrings x O(n) string comparison |
| Space | O(n^2) | Storing substrings in hash set |

### Why This Is Slow

String comparison and hashing each substring takes O(n) time, making this approach too slow for n = 10^5.

---

## Solution 2: Binary Search + Rolling Hash (Optimal)

### Key Insight

> **The Trick:** Binary search on the answer length, and use rolling hash to check if any substring of that length repeats in O(n) time.

### Algorithm

1. Binary search on length `L` in range `[1, n-1]`
2. For each `L`, compute rolling hashes of all substrings of length `L`
3. If any hash appears twice (and strings match), length `L` is achievable
4. Maximize `L` using binary search

### Dry Run Example

Let's trace through with input `s = "ababab"`:

```
Binary Search: lo=1, hi=5

Mid = 3: Check if repeating substring of length 3 exists
  Substrings: "aba", "bab", "aba", "bab"
  Hashes:     h1,    h2,    h1,    h2
  "aba" appears twice -> YES, length 3 works
  Update: lo = 4

Mid = 4: Check if repeating substring of length 4 exists
  Substrings: "abab", "baba", "abab"
  Hashes:     h1,     h2,     h1
  "abab" appears twice -> YES, length 4 works
  Update: lo = 5

Mid = 5: Check if repeating substring of length 5 exists
  Substrings: "ababa", "babab"
  Hashes:     h1,      h2
  No repeats -> NO
  Update: hi = 4

Answer: 4
```

### Visual Diagram

```
String: a b a b a b
Index:  0 1 2 3 4 5

Length 4 substrings:
[a b a b] . .    hash = H1, position 0
. [b a b a] .    hash = H2, position 1
. . [a b a b]    hash = H1, position 2  <- MATCH with position 0!

Binary Search Progress:
[1----3----5]
      ^mid=3: works, go right
[----4----5]
     ^mid=4: works, go right
[--------5]
         ^mid=5: fails, go left
Answer: 4
```

### Code

**Python:**
```python
def solve(s):
 """
 Binary Search + Rolling Hash.
 Time: O(n log n)  Space: O(n)
 """
 n = len(s)
 if n == 1:
  return -1

 BASE = 31
 MOD = 10**18 + 9

 # Precompute powers
 pw = [1] * (n + 1)
 for i in range(1, n + 1):
  pw[i] = (pw[i-1] * BASE) % MOD

 # Precompute prefix hashes
 h = [0] * (n + 1)
 for i in range(n):
  h[i + 1] = (h[i] * BASE + ord(s[i]) - ord('a') + 1) % MOD

 def get_hash(l, r):
  """Get hash of s[l:r] in O(1)"""
  return (h[r] - h[l] * pw[r - l] % MOD + MOD) % MOD

 def has_repeat(length):
  """Check if any substring of given length repeats"""
  seen = {}
  for i in range(n - length + 1):
   hval = get_hash(i, i + length)
   if hval in seen:
    # Verify to handle hash collisions
    if s[seen[hval]:seen[hval] + length] == s[i:i + length]:
     return True
   else:
    seen[hval] = i
  return False

 # Binary search on answer
 lo, hi, ans = 1, n - 1, -1
 while lo <= hi:
  mid = (lo + hi) // 2
  if has_repeat(mid):
   ans = mid
   lo = mid + 1
  else:
   hi = mid - 1

 return ans

# Input/Output
s = input().strip()
print(solve(s))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Binary search (log n) x hash check (O(n)) |
| Space | O(n) | Hash arrays and hash map |

---

## Solution 3: Suffix Array + LCP (Alternative Optimal)

### Key Insight

> **The Trick:** The longest repeating substring equals the maximum value in the LCP (Longest Common Prefix) array of the suffix array.

### Why It Works

- Suffix array sorts all suffixes lexicographically
- Adjacent suffixes in sorted order share the longest common prefix
- A repeating substring is a common prefix of two different suffixes

### Code

**Python:**
```python
def solve_suffix_array(s):
 """
 Suffix Array + LCP approach.
 Time: O(n log n)  Space: O(n)
 """
 n = len(s)
 if n == 1:
  return -1

 # Build suffix array (simplified O(n log^2 n) version)
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
  k *= 2

 # Build LCP array using Kasai's algorithm
 lcp = [0] * n
 rank_inv = [0] * n
 for i in range(n):
  rank_inv[sa[i]] = i

 k = 0
 for i in range(n):
  if rank_inv[i] == 0:
   k = 0
   continue
  j = sa[rank_inv[i] - 1]
  while i + k < n and j + k < n and s[i + k] == s[j + k]:
   k += 1
  lcp[rank_inv[i]] = k
  if k > 0:
   k -= 1

 return max(lcp) if max(lcp) > 0 else -1

s = input().strip()
print(solve_suffix_array(s))
```

---

## Common Mistakes

### Mistake 1: Ignoring Hash Collisions

```python
# WRONG - no collision check
if hval in seen:
 return True  # May be false positive!
```

**Problem:** Two different strings can have the same hash value.
**Fix:** Always verify actual string equality when hashes match.

### Mistake 2: Wrong Hash Formula

```python
# WRONG - subtracting hashes directly
def get_hash(l, r):
 return h[r] - h[l]  # Doesn't account for positional weights!
```

**Problem:** Must scale by power of base when subtracting prefix hashes.
**Fix:** Use `(h[r] - h[l] * pw[r-l]) % MOD`

**Problem:** `h[l] * pw[r-l]` can overflow before taking mod.
**Fix:** Use `((h[r] - h[l] * pw[r-l] % MOD) % MOD + MOD) % MOD`

### Mistake 4: Off-by-One in Binary Search

```python
# WRONG
hi = n  # Should be n-1, substring of length n can't repeat
```

**Problem:** A substring of length n is the entire string; it can appear at most once.
**Fix:** Set `hi = n - 1`

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `"a"` | -1 | Cannot repeat |
| All same chars | `"aaaa"` | 3 | "aaa" repeats twice |
| No repeats | `"abcde"` | -1 | All unique chars |
| Two chars | `"aa"` | 1 | "a" repeats |
| Entire string repeats | `"abab"` | 2 | "ab" appears twice |

---

## When to Use This Pattern

### Use Binary Search + Hashing When:
- You need to find the longest/shortest X satisfying a condition
- The condition has monotonic property (if length k works, k-1 works too)
- String comparison is the bottleneck

### Use Suffix Array When:
- Multiple queries on the same string
- Need to find all repeating substrings
- Problem involves suffix/prefix relationships

### Pattern Recognition Checklist:
- [ ] Looking for longest repeating pattern? -> **Binary search + hash** or **Suffix Array**
- [ ] Need to compare many substrings? -> **Rolling hash**
- [ ] Monotonic property on answer? -> **Binary search on answer**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [String Matching](https://cses.fi/problemset/task/1753) | Basic hashing for pattern matching |
| [Finding Borders](https://cses.fi/problemset/task/1732) | Prefix function, related to repeating patterns |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Finding Periods](https://cses.fi/problemset/task/1733) | Find all periods, not just longest repeat |
| [Minimal Rotation](https://cses.fi/problemset/task/1110) | Uses similar suffix array techniques |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Distinct Substrings](https://cses.fi/problemset/task/2105) | Count unique substrings using suffix array |
| [Longest Palindrome](https://cses.fi/problemset/task/1111) | Combines hashing with palindrome properties |

---

## Key Takeaways

1. **Binary Search on Answer:** When the answer has monotonic property, binary search!
2. **Rolling Hash:** Enables O(1) substring hash computation after O(n) preprocessing.
3. **Suffix Array + LCP:** Max LCP value = longest repeating substring length.
4. **Always Verify:** Hash collisions happen; verify string equality on hash match.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement rolling hash with prefix sums from scratch
- [ ] Explain why binary search works (monotonic property)
- [ ] Build a suffix array and LCP array
- [ ] Handle hash collisions properly
- [ ] Solve in under 15 minutes without looking at solution

---

## Additional Resources

- [CP-Algorithms: String Hashing](https://cp-algorithms.com/string/string-hashing.html)
- [CP-Algorithms: Suffix Array](https://cp-algorithms.com/string/suffix-array.html)
- [CSES Repeating Substring](https://cses.fi/problemset/task/2106) - Longest repeated substring
