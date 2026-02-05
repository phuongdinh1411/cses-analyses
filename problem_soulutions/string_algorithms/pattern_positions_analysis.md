---
layout: simple
title: "Pattern Positions - Multi-Pattern String Matching"
permalink: /problem_soulutions/string_algorithms/pattern_positions_analysis
difficulty: Hard
tags: [strings, aho-corasick, automaton, multi-pattern-matching, trie]
prerequisites: [string_matching_analysis, finding_borders_analysis]
---

# Pattern Positions

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Aho-Corasick Automaton |
| **CSES Link** | [Pattern Positions](https://cses.fi/problemset/task/2102) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when to use Aho-Corasick vs KMP algorithm
- [ ] Build a trie structure for multiple patterns
- [ ] Construct failure links (similar to KMP's LPS array)
- [ ] Implement efficient multi-pattern matching in O(n + m + z) time

---

## Problem Statement

**Problem:** Given a text string and k pattern strings, find the first occurrence position of each pattern in the text.

**Input:**
- Line 1: Text string
- Line 2: Number of patterns k
- Lines 3 to k+2: Pattern strings (one per line)

**Output:**
- For each pattern, print the 1-indexed position of its first occurrence, or -1 if not found

**Constraints:**
- 1 <= |text| <= 10^5
- 1 <= k <= 500
- 1 <= |pattern_i| <= 10^5
- Total length of all patterns <= 10^6
- All strings contain only lowercase English letters (a-z)

### Example

```
Input:
aybabtu
3
bab
abc
tu

Output:
3
-1
6
```

**Explanation:**
- "bab" first occurs at position 3 (1-indexed): ay**bab**tu
- "abc" does not occur in the text: -1
- "tu" first occurs at position 6 (1-indexed): aybab**tu**

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why can't we just use KMP k times?

If we use KMP for each pattern separately, the time complexity becomes O(n * k + total_pattern_length). When k is large, this becomes inefficient. The key insight is that we can search for ALL patterns simultaneously in a single pass through the text.

### Why Aho-Corasick?

Think of it like searching for 500 words in a book. Instead of scanning 500 times (once per word), scan ONCE while tracking all words simultaneously using a state machine.

| Approach | Time Complexity | When to Use |
|----------|-----------------|-------------|
| KMP per pattern | O(n * k + m) | Few patterns (k < 10) |
| Rabin-Karp | O(n * k + m) avg | When patterns same length |
| **Aho-Corasick** | O(n + m + z) | Many patterns, different lengths |

Where n = text length, m = total pattern length, k = number of patterns, z = total matches.

---

## Solution 1: Brute Force (KMP per Pattern)

### Idea

Apply KMP algorithm for each pattern independently. Simple but inefficient for many patterns.

### Algorithm

1. For each pattern, build its LPS array
2. Run KMP matching against the text
3. Record the first match position (or -1)

### Code

```python
def solve_brute_force(text, patterns):
  """Apply KMP for each pattern separately. Time: O(n * k + m)"""
  def kmp_first_match(text, pattern):
    # Build LPS array
    m, lps = len(pattern), [0] * len(pattern)
    length, i = 0, 1
    while i < m:
      if pattern[i] == pattern[length]:
        length += 1
        lps[i] = length
        i += 1
      elif length:
        length = lps[length - 1]
      else:
        i += 1
    # KMP search
    i = j = 0
    while i < len(text):
      if text[i] == pattern[j]:
        i, j = i + 1, j + 1
      if j == m:
        return i - j
      elif i < len(text) and text[i] != pattern[j]:
        j = lps[j - 1] if j else 0
        if not j:
          i += 1
    return -1

  return [kmp_first_match(text, p) + 1 if kmp_first_match(text, p) != -1 else -1
      for p in patterns]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * k + m) | KMP is O(n + pattern_len) per pattern |
| Space | O(max_pattern_len) | LPS array for each pattern |

### Why This Works (But Is Slow)

Correctness is guaranteed since KMP correctly finds all occurrences. However, scanning the text k times is wasteful when patterns share common prefixes or when k is large.

---

## Solution 2: Aho-Corasick Algorithm (Optimal)

### Key Insight

> **The Trick:** Build a trie of all patterns, add failure links (like KMP's LPS), then scan text ONCE while tracking all pattern matches simultaneously.

| Component | Purpose |
|-----------|---------|
| **Trie** | Store all patterns as a tree |
| **Failure Links** | Point to longest suffix that is also a prefix of some pattern |
| **Output** | Track which patterns end at each node |

**Algorithm:** (1) Build trie, (2) Compute failure links via BFS, (3) Process text char-by-char

### Dry Run Example

Let's trace through with text = "ushers", patterns = ["he", "she", "hers"]:

```
Trie with Failure Links:
       root(0)
      /      \
    h(1)     s(2)         Failure links:
    |          \           - node 4 (sh) --fail--> node 1 (h)
   e(3)        h(4)        - node 5 (she) --fail--> node 3 (he)
  [he]          \
    |          e(5)
   r(6)       [she]
    |
   s(7)
  [hers]

Processing "ushers":
  i=0 'u': stay at root (no child 'u')
  i=1 's': root -> node 2
  i=2 'h': node 2 -> node 4
  i=3 'e': node 4 -> node 5 [she] -> also fail to node 3 [he]
           MATCH "she" at pos 3, "he" at pos 4 (1-indexed)
  i=4 'r': node 5 has no 'r' -> fail to node 3 -> node 6
  i=5 's': node 6 -> node 7 [hers]
           MATCH "hers" at pos 4 (1-indexed)

Output: he=4, she=3, hers=4
```

### Code

**Python Solution:**

```python
from collections import deque, defaultdict

class AhoCorasick:
  def __init__(self):
    self.goto = [{}]          # Trie transitions
    self.fail = [0]           # Failure links
    self.output = [[]]        # Pattern indices ending at each node
    self.node_count = 1

  def add_pattern(self, pattern, index):
    """Add a pattern to the trie with its index."""
    node = 0
    for char in pattern:
      if char not in self.goto[node]:
        self.goto[node][char] = self.node_count
        self.goto.append({})
        self.fail.append(0)
        self.output.append([])
        self.node_count += 1
      node = self.goto[node][char]
    self.output[node].append(index)

  def build(self):
    """Build failure links using BFS."""
    queue = deque()

    # Initialize: depth-1 nodes fail to root
    for char, node in self.goto[0].items():
      queue.append(node)
      # fail[node] = 0 already set

    # BFS to compute failure links
    while queue:
      curr = queue.popleft()

      for char, next_node in self.goto[curr].items():
        queue.append(next_node)

        # Find failure link for next_node
        fail_state = self.fail[curr]
        while fail_state and char not in self.goto[fail_state]:
          fail_state = self.fail[fail_state]

        self.fail[next_node] = self.goto[fail_state].get(char, 0)

        # Merge output from failure link
        if self.fail[next_node] != next_node:
          self.output[next_node] += self.output[self.fail[next_node]]

  def search(self, text, pattern_lengths):
    """Find first occurrence of each pattern (1-indexed, -1 if not found)."""
    result = [-1] * len(pattern_lengths)
    node = 0

    for i, char in enumerate(text):
      while node and char not in self.goto[node]:
        node = self.fail[node]
      node = self.goto[node].get(char, 0)

      # Check outputs via failure chain
      temp = node
      while temp:
        for idx in self.output[temp]:
          if result[idx] == -1:
            result[idx] = i - pattern_lengths[idx] + 2  # 1-indexed start
        temp = self.fail[temp]

    return result


def solve(text, patterns):
  """Find first occurrence of each pattern using Aho-Corasick."""
  ac = AhoCorasick()
  lengths = [len(p) for p in patterns]
  for i, p in enumerate(patterns):
    ac.add_pattern(p, i)
  ac.build()
  return ac.search(text, lengths)


def main():
  text = input().strip()
  k = int(input().strip())
  patterns = [input().strip() for _ in range(k)]

  result = solve(text, patterns)
  for pos in result:
    print(pos)


if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m + z) | n = text length, m = total pattern length, z = matches |
| Space | O(m * SIGMA) | Trie storage, SIGMA = alphabet size (26) |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Only check current node outputs | Shorter patterns via failure link are missed | Traverse entire failure chain for outputs |
| Use end position as start | Pattern "abc" at i=5 starts at 3, not 5 | `start = i - len(pattern) + 1` |
| Direct child access without check | KeyError when character not in trie | Follow failure links until found or root |

```python
# WRONG: Only current node    |  # CORRECT: Follow failure chain
for idx in out[node]: ...     |  temp = node
              |  while temp:
              |      for idx in out[temp]: ...
              |      temp = fail[temp]
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| No patterns match | text="xyz", patterns=["abc"] | -1 | Pattern not in text |
| Pattern equals text | text="abc", patterns=["abc"] | 1 | Exact match at position 1 |
| Overlapping patterns | text="abab", patterns=["ab","bab"] | 1, 2 | Both found at different positions |
| Pattern is prefix of another | text="abcd", patterns=["ab","abc"] | 1, 1 | Both start at same position |
| Single character patterns | text="aaa", patterns=["a"] | 1 | First occurrence |
| Duplicate patterns | text="abc", patterns=["ab","ab"] | 1, 1 | Same result for duplicates |
| Pattern longer than text | text="ab", patterns=["abc"] | -1 | Cannot match |

---

## When to Use This Pattern

| Scenario | Best Algorithm |
|----------|---------------|
| Multiple patterns (k > 10) | **Aho-Corasick** |
| Single pattern | KMP or Z-algorithm |
| All patterns same length | Rabin-Karp with rolling hash |
| Approximate matching | Edit distance DP |
| Streaming text + multiple patterns | **Aho-Corasick** (stateful) |

---

## Related Problems

| Level | Problem | Key Concept |
|-------|---------|-------------|
| Easier | [String Matching](https://cses.fi/problemset/task/1753) | Single pattern KMP |
| Easier | [Finding Borders](https://cses.fi/problemset/task/1732) | LPS/failure function |
| Similar | [Counting Patterns](https://cses.fi/problemset/task/2103) | Count instead of position |
| Similar | [Word Combinations](https://cses.fi/problemset/task/1731) | DP + Aho-Corasick |
| Harder | [Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | Reverse Aho-Corasick |
| Harder | [Word Search II](https://leetcode.com/problems/word-search-ii/) | Trie + backtracking |

---

## Key Takeaways

1. **The Core Idea:** Build a trie with failure links to search for all patterns in a single text scan.
2. **Time Optimization:** From O(n * k) with separate KMP to O(n + m + z) with Aho-Corasick.
3. **Space Trade-off:** O(m) space for trie enables linear-time multi-pattern matching.
4. **Pattern:** Failure links generalize KMP's LPS array to multiple patterns.

---

## Practice Checklist

- [ ] Explain why Aho-Corasick beats running KMP k times
- [ ] Build trie and compute failure links using BFS
- [ ] Trace the automaton on a sample input
- [ ] Handle edge cases (overlapping patterns, no matches)

## Additional Resources

- [CP-Algorithms: Aho-Corasick](https://cp-algorithms.com/string/aho_corasick.html)
- [CSES Pattern Positions](https://cses.fi/problemset/task/2107) - Multi-pattern string matching
