---
layout: simple
title: "Substring Order II - String Algorithms Problem"
permalink: /problem_soulutions/string_algorithms/substring_order_ii_analysis
difficulty: Hard
tags: [suffix-automaton, counting, string-algorithms]
---

# Substring Order II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 2109 - Substring Order II](https://cses.fi/problemset/task/2109) |
| **Difficulty** | Hard |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Suffix Automaton + occurrence counts, greedy letter-by-letter walk |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Explain why "k-th substring with repetitions" is NOT "k-th prefix of the sorted suffixes"
- [ ] Build the answer letter by letter from prefix counts
- [ ] Use a suffix automaton to get occurrence counts and prefix counts in O(n)

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
ab
```

**Explanation:** the 21 substrings of `baabaa` in order, with repeats:

```
 1-4  a a a a        5-6  aa aa      7 aab    8 aaba    9 aabaa
 10   ab   <- answer 11   aba       12 abaa  13-14 b b  15-16 ba ba ...
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we find the k-th item of a sorted list of ~n²/2 strings without building the list?

Build the answer **one letter at a time**, the way you would find the k-th word in a dictionary. Let `cnt(p)` be the number of substrings (with repeats) that start with `p`. From the current answer `p`:

1. The `occ(p)` copies of `p` itself come first. If `k <= occ(p)`, the answer is `p`.
2. Otherwise skip them (`k -= occ(p)`) and try letters `c = a, b, ...`: if `k <= cnt(p + c)`, extend to `p + c`; else `k -= cnt(p + c)`.

### Why the "sorted suffixes" shortcut fails

It is tempting to list every prefix of every suffix in suffix-array order. That works for Substring Order I (distinct substrings), but not with repeats: in `baabaa` the suffix order lists `a, ab, aba, abaa` before the second `a`, yet `a < ab`. Every copy of `a` must come before `ab`.

### Key Insight

A suffix automaton groups substrings into states that share the same set of end positions, so every string in a state has the same occurrence count `occ`. Two DP passes over the states, longest first, give `occ` and `cnt` for every state in O(n), and the letter-by-letter walk follows the automaton's transitions.

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

## Solution 2: Optimal - Suffix Automaton + Counting

### Algorithm

1. Build the suffix automaton of `s`. New (non-clone) states start with `occ = 1`, clones with 0.
2. Process states by decreasing `length`: `occ[link[v]] += occ[v]`. Now `occ[v]` is how often each string of `v` occurs.
3. Again by decreasing `length`: `cnt[v] = occ[v] + Σ cnt[u]` over transitions `v -> u`. Set `cnt[root] = 0`, since the empty string is not a substring.
4. Walk from the root: try letters in order; enter `u` if `k <= cnt[u]`, then `k -= occ[u]`; otherwise `k -= cnt[u]`. Stop when `k <= 0`.

Decreasing `length` is a valid order for both passes: a suffix link points to a shorter state, and a transition `v -c-> u` always has `length[u] >= length[v] + 1`.

### Dry Run: `baabaa`, k = 10

```
At root (answer ""), k = 10
  'a': cnt = 12 (substrings starting with "a")  10 <= 12 -> take 'a'
       occ("a") = 4 copies of "a" come first     k = 10 - 4 = 6
At "a", k = 6
  'a': cnt("aa") = 5     6 > 5  -> skip,  k = 1
  'b': cnt("ab") = 3     1 <= 3 -> take 'b'
       occ("ab") = 1                         k = 1 - 1 = 0  -> stop
Answer: "ab"
```

### Code (Python)

```python
import sys


def kth_substring(s: str, k: int) -> str:
  # Suffix automaton: state 0 is the root (empty string).
  link, length, nxt, occ = [-1], [0], [{}], [0]
  last = 0
  for ch in s:
    cur = len(length)
    length.append(length[last] + 1); link.append(-1); nxt.append({}); occ.append(1)
    p = last
    while p != -1 and ch not in nxt[p]:
      nxt[p][ch] = cur
      p = link[p]
    if p == -1:
      link[cur] = 0
    else:
      q = nxt[p][ch]
      if length[p] + 1 == length[q]:
        link[cur] = q
      else:
        clone = len(length)
        length.append(length[p] + 1); link.append(link[q]); nxt.append(dict(nxt[q])); occ.append(0)
        while p != -1 and nxt[p].get(ch) == q:
          nxt[p][ch] = clone
          p = link[p]
        link[q] = link[cur] = clone
    last = cur

  # Longer states first: suffix links and transitions both respect this order.
  order = sorted(range(len(length)), key=length.__getitem__, reverse=True)
  for v in order:
    if link[v] > 0:
      occ[link[v]] += occ[v]          # occ[v] = occurrences of v's strings
  cnt = occ[:]                        # cnt[v] = substrings (with repeats) starting with v's string
  cnt[0] = 0
  for v in order:
    for u in nxt[v].values():
      cnt[v] += cnt[u]

  out, v = [], 0
  while k > 0:
    for ch in sorted(nxt[v]):
      u = nxt[v][ch]
      if k <= cnt[u]:
        out.append(ch)
        k -= occ[u]                   # the occ[u] copies of the current answer come first
        v = u
        break
      k -= cnt[u]
  return ''.join(out)


def main():
  data = sys.stdin.read().split()
  print(kth_substring(data[0], int(data[1])))


if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Automaton is O(n) states and transitions (alphabet of 26); the sort by length could be a counting sort for O(n) |
| Space | O(n) | At most 2n states |

---

## Common Mistakes

### Mistake 1: Using 32-bit integers for k

**Problem:** With n = 10^5 there are about 5 * 10^9 substrings, which overflows 32-bit ints.
**Fix:** In C++ use `long long` for `k`, `occ` and `cnt`. Python ints are unbounded.

### Mistake 2: Reusing the Substring Order I method

**Problem:** Walking the suffix array and taking prefixes in that order gives the right answer only for *distinct* substrings. With repeats, all copies of "a" must come before "ab", even copies that come from later suffixes.
**Fix:** Count by prefix (`cnt`) and build the answer letter by letter.

### Mistake 3: Forgetting to subtract the copies of the current answer

```python
# fragment
# WRONG - jumps straight to the children
if k <= cnt[u]:
  out.append(ch); v = u          # k still includes the occ[u] copies of out itself

# CORRECT
if k <= cnt[u]:
  out.append(ch); k -= occ[u]; v = u
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

### Use Suffix Automaton + Counting When:
- Finding k-th smallest/largest substring
- Problems involving lexicographical ordering of substrings
- Counting substrings with specific properties
- String comparison operations at scale

### Don't Use When:
- Simple string matching (use KMP or Z-algorithm)
- Only need to check substring existence (use hashing)
- Only distinct substrings matter: the suffix array + LCP method of Substring Order I is simpler

### Pattern Recognition Checklist:
- [ ] k-th distinct substring? -> **Suffix array + LCP** (Substring Order I)
- [ ] k-th substring with repetitions? -> **Suffix automaton occ + cnt, greedy walk** (Substring Order II)
- [ ] k-th of a huge implicit sorted set? -> **Count by prefix, choose letter by letter**

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
| [CSES - Repeating Substring](https://cses.fi/problemset/task/2106) | Finding repeated patterns |
| [CSES - Required Substring](https://cses.fi/problemset/task/1112) | DP + string matching |

---

## Key Takeaways

1. **The Core Idea:** Build the answer letter by letter; at each step skip whole groups of substrings by their prefix count `cnt(p + c)`
2. **Why a suffix automaton:** All strings in one state share an occurrence count, so `occ` and `cnt` take two linear passes
3. **Key Difference from Order I:** with repeats, sorted-suffix order is not substring order; every copy of "a" precedes "ab"
4. **Don't forget:** subtract `occ` of the current answer before moving on to longer strings

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Show with `baabaa` why prefixes of sorted suffixes are out of order when repeats count
- [ ] Build a suffix automaton and compute `occ` via suffix links
- [ ] Compute `cnt` over transitions and run the greedy walk
- [ ] Handle large k values with appropriate data types

---

## Additional Resources

- [CP-Algorithms: Suffix Automaton](https://cp-algorithms.com/string/suffix-automaton.html) (see "Number of occurrences" and "Lexicographically k-th substring")
- [CSES Substring Order II](https://cses.fi/problemset/task/2109) - K-th smallest substring
