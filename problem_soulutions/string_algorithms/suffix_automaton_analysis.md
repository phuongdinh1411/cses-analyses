---
layout: simple
title: "Suffix Automaton - String Algorithm"
permalink: /problem_soulutions/string_algorithms/suffix_automaton_analysis
difficulty: Hard
tags: [string, automaton, suffix-automaton, substring, dp]
prerequisites: [basic_string_hashing, finite_automata_concepts]
---

# Suffix Automaton

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | String Algorithms |
| **Key Technique** | Suffix Automaton (SAM) |
| **Space Complexity** | O(n) states, O(n) transitions |

### Learning Goals

After studying this topic, you will be able to:
- [ ] Understand what a suffix automaton represents and why it uses linear space
- [ ] Build a suffix automaton incrementally by adding characters
- [ ] Handle clone states correctly during construction
- [ ] Count distinct substrings in O(n) time
- [ ] Apply SAM to pattern matching and LCS problems

---

## Concept Explanation

**What is a Suffix Automaton?**

A Suffix Automaton (SAM) is a minimal deterministic finite automaton (DFA) that accepts exactly all suffixes of a given string. The remarkable property is that it also accepts all substrings, since every substring is a prefix of some suffix.

**Key Properties:**
- Contains at most **2n - 1** states for a string of length n
- Contains at most **3n - 4** transitions
- Each state represents an equivalence class of substrings (ending at the same positions)

**Why Linear Space?**

Instead of storing each substring explicitly (O(n^2) space), SAM groups substrings that have the same set of ending positions into equivalence classes. Each class becomes one state.

---

## Intuition: States and Transitions

### State Representation

Each state in SAM represents a set of substrings that:
1. All end at the same positions in the original string
2. Form a contiguous chain by suffix relationship

| Component | Meaning |
|-----------|---------|
| `len` | Length of the longest substring in this equivalence class |
| `link` | Suffix link - points to state representing next shorter suffix class |
| `trans[c]` | Transition on character c to another state |

**Suffix Link Intuition:**

The suffix link of state `v` points to state `u` where `u` represents the longest proper suffix of substrings in `v` that belongs to a different equivalence class.

### Equivalence Classes

For string "abab":
- Substrings "ab" (at positions 2,4) and "abab" (at position 4) end at different position sets
- Substrings ending at the same positions are grouped together

```
State 0 (initial): represents empty string
State 1: represents "a" (ends at 1, 3)
State 2: represents "ab" (ends at 2, 4)
State 3: represents "aba", "ba" (ends at 3)
State 4: represents "abab", "bab" (ends at 4)
```

---

## Dry Run: Building SAM for "abab"

### Initial State

```
States: { 0 }
State 0: len=0, link=-1, trans={}
last = 0
```

### Step 1: Add 'a'

```
1. Create new state cur=1 with len=1
2. Walk from last=0:
   - State 0 has no 'a' transition, add trans[a]=1
   - Reached initial state's link (-1)
3. Set link[1] = 0 (no existing 'a' path)
4. Set last = 1

States after 'a':
  State 0: len=0, link=-1, trans={a:1}
  State 1: len=1, link=0,  trans={}
```

### Step 2: Add 'b'

```
1. Create new state cur=2 with len=2
2. Walk from last=1:
   - State 1 has no 'b' transition, add trans[b]=2
   - State 0 has no 'b' transition, add trans[b]=2
   - Reached initial state's link (-1)
3. Set link[2] = 0
4. Set last = 2

States after 'ab':
  State 0: len=0, link=-1, trans={a:1, b:2}
  State 1: len=1, link=0,  trans={b:2}
  State 2: len=2, link=0,  trans={}
```

### Step 3: Add 'a'

```
1. Create new state cur=3 with len=3
2. Walk from last=2:
   - State 2 has no 'a' transition, add trans[a]=3
   - State 0 already has trans[a]=1, stop here, q=1
3. Check: len[0] + 1 == len[1]? (0+1 == 1) YES
   - Set link[3] = 1 (no clone needed)
4. Set last = 3

States after 'aba':
  State 0: len=0, link=-1, trans={a:1, b:2}
  State 1: len=1, link=0,  trans={b:2}
  State 2: len=2, link=0,  trans={a:3}
  State 3: len=3, link=1,  trans={}
```

### Step 4: Add 'b' (Clone Required!)

```
1. Create new state cur=4 with len=4
2. Walk from last=3:
   - State 3 has no 'b' transition, add trans[b]=4
   - State 1 already has trans[b]=2, stop here, q=2
3. Check: len[1] + 1 == len[2]? (1+1 == 2) YES
   - Set link[4] = 2 (no clone needed)
4. Set last = 4

Final States for "abab":
  State 0: len=0, link=-1, trans={a:1, b:2}
  State 1: len=1, link=0,  trans={b:2}
  State 2: len=2, link=0,  trans={a:3}
  State 3: len=3, link=1,  trans={b:4}
  State 4: len=4, link=2,  trans={}
```

### Visual Representation

```
        a           b           a           b
  [0] -----> [1] -----> [2] -----> [3] -----> [4]
   |          ^          ^
   |          |          |
   +--- b ----+--- a ----+
   |                     |
   +-------- b ----------+

Suffix Links:
  4 -> 2 -> 0
  3 -> 1 -> 0
```

---

## Common Mistakes

### Mistake 1: Forgetting to Clone

```python
# WRONG: Assuming no clone is ever needed
if p != -1 and trans[p][c] exists:
    link[cur] = trans[p][c]  # WRONG! May need clone
```

**Problem:** When `len[p] + 1 != len[q]`, we must clone state q.

**Fix:** Always check the length condition:
```python
q = trans[p][c]
if len[p] + 1 == len[q]:
    link[cur] = q
else:
    # Clone q into new state clone
    clone = create_clone(q)
```

### Mistake 2: Not Updating All Transitions to Clone

```python
# WRONG: Only updating one transition
trans[p][c] = clone
```

**Problem:** All ancestors of p that transition to q must be updated.

**Fix:** Walk up suffix links and update all:
```python
while p != -1 and trans[p][c] == q:
    trans[p][c] = clone
    p = link[p]
```

### Mistake 3: Incorrect Suffix Link for Clone

```python
# WRONG
link[clone] = link[cur]
```

**Problem:** Clone's suffix link should be the original's suffix link, not cur's.

**Fix:**
```python
link[clone] = link[q]  # Clone inherits q's suffix link
link[q] = clone        # Original q now points to clone
link[cur] = clone      # New state also points to clone
```

---

## Edge Cases

| Case | Input | Behavior | Notes |
|------|-------|----------|-------|
| Empty string | "" | Single initial state | 0 distinct substrings |
| Single char | "a" | 2 states | 1 distinct substring |
| All same chars | "aaaa" | n+1 states, no clones | Linear chain structure |
| All distinct | "abcd" | 2n states possible | Maximum branching |
| Alternating | "abab" | May require clones | Test clone logic |
| Long repeats | "abcabc" | Multiple clones | Stress test |

---

## When to Use Suffix Automaton

### Use SAM When:
- Counting distinct substrings (optimal O(n) solution)
- Finding longest common substring of multiple strings
- Pattern matching with wildcards or complex conditions
- Computing substring statistics (count, positions)
- Online string processing (add characters incrementally)

### Don't Use When:
- Simple single pattern matching (use KMP or Z-algorithm)
- Only need suffix array properties (SA might be simpler)
- Memory is extremely constrained (consider suffix array)
- Problem only involves prefixes (simpler solutions exist)

### Comparison with Alternatives

| Structure | Space | Build Time | Distinct Substrings |
|-----------|-------|------------|---------------------|
| Suffix Automaton | O(n) | O(n) | O(n) |
| Suffix Tree | O(n) | O(n) | O(n) |
| Suffix Array | O(n) | O(n log n) | O(n) with LCP |
| Trie of Suffixes | O(n^2) | O(n^2) | O(n^2) |

---

## Applications

### 1. Counting Distinct Substrings

**Formula:** Sum of `(len[v] - len[link[v]])` for all states v except initial.

Each state contributes `len[v] - len[link[v]]` unique substrings.

```python
def count_distinct_substrings(sam):
    total = 0
    for state in range(1, sam.size):  # Skip initial state
        total += sam.len[state] - sam.len[sam.link[state]]
    return total
```

### 2. Longest Common Substring (LCS) of Two Strings

Build SAM on first string, then traverse with second string:

```python
def lcs_two_strings(s, t):
    sam = build_sam(s)
    v, l, best = 0, 0, 0
    for c in t:
        while v and c not in sam.trans[v]:
            v = sam.link[v]
            l = sam.len[v]
        if c in sam.trans[v]:
            v = sam.trans[v][c]
            l += 1
        best = max(best, l)
    return best
```

### 3. LCS of Multiple Strings

For each state, track minimum occurrence length across all strings.

---

## Solution: Python Implementation

```python
class SuffixAutomaton:
    """
    Suffix Automaton implementation.

    Time: O(n) construction
    Space: O(n) states and transitions
    """
    def __init__(self):
        self.size = 1
        self.last = 0
        self.len = [0]
        self.link = [-1]
        self.trans = [{}]

    def _add_state(self):
        self.len.append(0)
        self.link.append(-1)
        self.trans.append({})
        idx = self.size
        self.size += 1
        return idx

    def add_char(self, c):
        cur = self._add_state()
        self.len[cur] = self.len[self.last] + 1

        p = self.last
        while p != -1 and c not in self.trans[p]:
            self.trans[p][c] = cur
            p = self.link[p]

        if p == -1:
            self.link[cur] = 0
        else:
            q = self.trans[p][c]
            if self.len[p] + 1 == self.len[q]:
                self.link[cur] = q
            else:
                # Clone state q
                clone = self._add_state()
                self.len[clone] = self.len[p] + 1
                self.link[clone] = self.link[q]
                self.trans[clone] = self.trans[q].copy()

                # Update transitions to point to clone
                while p != -1 and self.trans[p].get(c) == q:
                    self.trans[p][c] = clone
                    p = self.link[p]

                self.link[q] = clone
                self.link[cur] = clone

        self.last = cur

    def build(self, s):
        for c in s:
            self.add_char(c)
        return self

    def count_distinct_substrings(self):
        """Count number of distinct substrings."""
        total = 0
        for i in range(1, self.size):
            total += self.len[i] - self.len[self.link[i]]
        return total


def solve_distinct_substrings():
    """CSES: Distinct Substrings"""
    s = input().strip()
    sam = SuffixAutomaton().build(s)
    print(sam.count_distinct_substrings())


def solve_lcs(s, t):
    """Longest Common Substring of two strings."""
    sam = SuffixAutomaton().build(s)

    v, length, best = 0, 0, 0
    for c in t:
        while v != 0 and c not in sam.trans[v]:
            v = sam.link[v]
            length = sam.len[v]
        if c in sam.trans[v]:
            v = sam.trans[v][c]
            length += 1
        best = max(best, length)
    return best
```

---

## Solution: C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SuffixAutomaton {
    struct State {
        int len, link;
        map<char, int> trans;
    };

    vector<State> st;
    int last;

    SuffixAutomaton() {
        st.push_back({0, -1, {}});
        last = 0;
    }

    void addChar(char c) {
        int cur = st.size();
        st.push_back({st[last].len + 1, -1, {}});

        int p = last;
        while (p != -1 && !st[p].trans.count(c)) {
            st[p].trans[c] = cur;
            p = st[p].link;
        }

        if (p == -1) {
            st[cur].link = 0;
        } else {
            int q = st[p].trans[c];
            if (st[p].len + 1 == st[q].len) {
                st[cur].link = q;
            } else {
                // Clone state q
                int clone = st.size();
                st.push_back({st[p].len + 1, st[q].link, st[q].trans});

                while (p != -1 && st[p].trans[c] == q) {
                    st[p].trans[c] = clone;
                    p = st[p].link;
                }

                st[q].link = clone;
                st[cur].link = clone;
            }
        }
        last = cur;
    }

    void build(const string& s) {
        for (char c : s) addChar(c);
    }

    long long countDistinct() {
        long long total = 0;
        for (int i = 1; i < (int)st.size(); i++) {
            total += st[i].len - st[st[i].link].len;
        }
        return total;
    }

    int lcs(const string& t) {
        int v = 0, len = 0, best = 0;
        for (char c : t) {
            while (v && !st[v].trans.count(c)) {
                v = st[v].link;
                len = st[v].len;
            }
            if (st[v].trans.count(c)) {
                v = st[v].trans[c];
                len++;
            }
            best = max(best, len);
        }
        return best;
    }
};

// CSES: Distinct Substrings
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;

    SuffixAutomaton sam;
    sam.build(s);

    cout << sam.countDistinct() << "\n";
    return 0;
}
```

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build SAM | O(n) | O(n) |
| Count distinct substrings | O(n) | O(1) |
| LCS of two strings | O(n + m) | O(n) |
| Pattern search | O(m) | O(1) |

**Why O(n) Space?**
- At most 2n-1 states (each char adds at most 2 states: cur and possibly clone)
- At most 3n-4 transitions (amortized across construction)

---

## Related CSES Problems

| Problem | Technique |
|---------|-----------|
| [Distinct Substrings](https://cses.fi/problemset/task/2105) | Direct SAM application |
| [Repeating Substring](https://cses.fi/problemset/task/2106) | SAM with occurrence counting |
| [Substring Order I](https://cses.fi/problemset/task/2108) | SAM with lexicographic traversal |
| [Substring Order II](https://cses.fi/problemset/task/2109) | SAM with DP on states |
| [Finding Patterns](https://cses.fi/problemset/task/2102) | Multi-pattern matching |

---

## Key Takeaways

1. **Core Idea:** SAM compresses all substrings into O(n) equivalence classes based on ending positions
2. **Clone Mechanism:** Essential for maintaining minimality when suffix link lengths mismatch
3. **Suffix Links:** Form a tree structure enabling efficient substring navigation
4. **Applications:** Distinct substrings, LCS, pattern matching - all in linear time

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain what each SAM state represents
- [ ] Trace through SAM construction on paper
- [ ] Identify when cloning is necessary
- [ ] Implement SAM from scratch in under 15 minutes
- [ ] Solve distinct substrings problem using SAM

---

## Additional Resources

- [CP-Algorithms: Suffix Automaton](https://cp-algorithms.com/string/suffix-automaton.html)
- [E-Maxx: Suffix Automaton (Russian)](https://e-maxx.ru/algo/suffix_automata)
- [CSES Problem Set](https://cses.fi/problemset/)
