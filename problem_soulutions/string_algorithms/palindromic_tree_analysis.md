---
layout: simple
title: "Palindromic Tree (Eertree) - String Algorithm"
permalink: /problem_soulutions/string_algorithms/palindromic_tree_analysis
difficulty: Hard
tags: [strings, palindrome, data-structure, suffix-link, tree]
---

# Palindromic Tree (Eertree)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | String Algorithms / Data Structures |
| **Key Technique** | Suffix Links, Tree Construction |
| **Invented By** | Mikhail Rubinchik (2014) |

### Concept Explanation

The **Palindromic Tree** (also called **Eertree**) is a data structure that efficiently represents all distinct palindromic substrings of a string. Unlike tries or suffix trees, it has exactly **two root nodes**:
- **Odd Root (-1)**: Represents palindromes of odd length (conceptual length -1)
- **Even Root (0)**: Represents palindromes of even length (conceptual length 0)

Each node in the tree represents a unique palindromic substring, and edges are labeled with characters.

### Learning Goals

After studying this topic, you will be able to:
- [ ] Understand the two-root structure of palindromic trees
- [ ] Build a palindromic tree in O(n) time
- [ ] Count all distinct palindromic substrings efficiently
- [ ] Find the longest palindromic substring
- [ ] Use suffix links to navigate between palindromes

---

## Intuition: How to Think About This Structure

### Why Two Roots?

> **Key Insight:** Palindromes can have odd or even length, requiring different "base cases."

- **Odd-length palindromes** like "aba" have a center character
- **Even-length palindromes** like "abba" have no center character

The odd root (length -1) allows us to build single characters: adding 'a' to both sides of length -1 gives length 1 ("a").
The even root (length 0) allows us to build pairs: adding 'a' to both sides of length 0 gives length 2 ("aa").

### Core Components

| Component | Purpose |
|-----------|---------|
| **Node** | Represents a distinct palindrome |
| **Edge (child)** | Adding character c to both ends |
| **Suffix Link** | Points to longest proper palindromic suffix |
| **Length** | Length of palindrome this node represents |

### Suffix Link Intuition

The suffix link of a palindrome P points to the longest palindromic suffix of P (excluding P itself).

```
Example: "abaaba"
  Node for "abaaba" -> suffix link -> Node for "aba"
  Node for "aba"    -> suffix link -> Node for "a"
  Node for "a"      -> suffix link -> Odd root
```

---

## Structure Definition

### Node Structure

```
Node:
  - length: int          # Length of this palindrome
  - children: map[char -> node]  # Transitions by adding char to both ends
  - suffix_link: node    # Longest proper palindromic suffix
  - count: int           # (optional) Occurrences in string
```

### Tree Properties

| Property | Value |
|----------|-------|
| Max Nodes | n + 2 (at most n distinct palindromes + 2 roots) |
| Time Complexity | O(n) amortized for construction |
| Space Complexity | O(n * alphabet_size) |

---

## Dry Run: Building Tree for "abaaba"

Let's trace the construction step by step.

### Initial State

```
Nodes:
  Node 0 (Even Root): length=0, suffix_link -> Node 1
  Node 1 (Odd Root):  length=-1, suffix_link -> Node 1

Current suffix node: Node 1 (odd root)
String processed: ""
```

### The one rule used at every step

To add `s[i]`, start at `last` (the longest palindrome ending at `i-1`) and follow suffix links until you reach a node `X` of length `L` with `s[i-L-1] == s[i]`. Then `s[i] + X + s[i]` is the longest palindrome ending at `i`. The odd root (length -1) always matches, because the check becomes `s[i] == s[i]`.

### Trace

Node numbers match the code below: 0 = even root (length 0), 1 = odd root (length -1).

| i | char | Suffix-link chain tried (✗ fails, ✓ extends) | Result | Suffix link of new node |
|---|------|----------------------------------------------|--------|-------------------------|
| 0 | a | odd root ✓ | **new** node 2 `a` | even root (single chars always do) |
| 1 | b | `a` ✗ (s[-1] is out of range) → even root ✗ (s[0]=a) → odd root ✓ | **new** node 3 `b` | even root |
| 2 | a | `b` ✓ (s[0]=a) | **new** node 4 `aba` | `a` |
| 3 | a | `aba` ✗ (out of range) → `a` ✗ (s[1]=b) → even root ✓ (s[2]=a) | **new** node 5 `aa` | `a` |
| 4 | b | `aa` ✓ (s[1]=b) | **new** node 6 `baab` | `b` |
| 5 | a | `baab` ✓ (s[0]=a) | **new** node 7 `abaaba` | `aba` |

A new node's suffix link is found the same way: start from the suffix link of `X` (not from `X`), find the next node that extends with `s[i]`, and take its child.

### Final Tree Structure for "abaaba"

```
     Odd Root (len -1)              Even Root (len 0)
       /        \                         |
     'a'        'b'                       'a'
      |          |                         |
  node 2 "a"  node 3 "b"              node 5 "aa"
                 |                         |
                'a'                       'b'
                 |                         |
            node 4 "aba"             node 6 "baab"
                                           |
                                          'a'
                                           |
                                    node 7 "abaaba"

Edges add the same letter on both sides: "aa" --b--> "baab".
Distinct palindromes: a, b, aba, aa, baab, abaaba
Total: 6 (number of nodes minus the two roots)
```

---

## Common Mistakes

### Mistake 1: Incorrect Suffix Link Updates

```python
# WRONG: Not following suffix links properly
def get_suffix_link(node, pos, s):
  return node.suffix_link  # Too simple!

# CORRECT: Must verify the palindrome condition
def get_suffix_link(node, pos, s):
  cur = node.suffix_link
  while pos - cur.length - 1 < 0 or s[pos - cur.length - 1] != s[pos]:
    cur = cur.suffix_link
  return cur
```

**Problem:** Suffix links must point to valid palindromic suffixes.
**Fix:** Always verify boundary and character match conditions.

### Mistake 2: Boundary Check Errors

```python
# fragment
# WRONG: Missing boundary check
if s[pos - cur.length - 1] == s[pos]:  # May access negative index!

# CORRECT: Check boundary first
if pos - cur.length - 1 >= 0 and s[pos - cur.length - 1] == s[pos]:
```

### Mistake 3: Forgetting Even Root's Suffix Link

```python
# WRONG: Even root suffix link to itself
even_root.suffix_link = even_root

# CORRECT: Even root points to odd root
even_root.suffix_link = odd_root  # Allows falling back to single chars
```

---

## Edge Cases

| Case | Input | Behavior | Notes |
|------|-------|----------|-------|
| Empty string | "" | Only roots exist | 0 palindromes |
| Single char | "a" | 1 palindrome | Just "a" |
| All same chars | "aaaa" | n palindromes | "a", "aa", "aaa", "aaaa" |
| No repeats | "abcd" | n palindromes | Only single characters |
| All pairs | "aabb" | 4 palindromes | "a", "b", "aa", "bb" |

---

## When to Use Palindromic Tree

### Use This Approach When:
- Counting distinct palindromic substrings
- Finding all palindromes in O(n) time
- Need occurrence count of each palindrome
- Building incrementally (online algorithm)

### Don't Use When:
- Only need longest palindrome (Manacher's is simpler)
- Memory is extremely constrained
- String is very short (brute force is fine)

### Comparison with Alternatives

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| Palindromic Tree | O(n) | O(n) | All distinct palindromes |
| Manacher's | O(n) | O(n) | Longest palindrome only |
| Brute Force | O(n^3) | O(1) | Very short strings |
| Hashing | O(n^2) | O(n) | Counting with collision risk |

---

## Solutions

### Python Implementation

```python
class PalindromicTree:
  def __init__(self):
    self.nodes = []
    # Node 0: even root (length 0)
    # Node 1: odd root (length -1)
    self.nodes.append({'len': 0, 'suffix': 1, 'children': {}})
    self.nodes.append({'len': -1, 'suffix': 1, 'children': {}})
    self.last = 1  # Start from odd root
    self.s = ""

  def _get_link(self, v, pos):
    """Find node where we can extend with s[pos]."""
    while True:
      cur_len = self.nodes[v]['len']
      if pos - cur_len - 1 >= 0 and self.s[pos - cur_len - 1] == self.s[pos]:
        return v
      v = self.nodes[v]['suffix']

  def add(self, c):
    """Add character c to the tree. Returns True if new palindrome created."""
    pos = len(self.s)
    self.s += c

    # Find longest palindrome that can be extended
    cur = self._get_link(self.last, pos)

    if c in self.nodes[cur]['children']:
      self.last = self.nodes[cur]['children'][c]
      return False  # Palindrome already exists

    # Create new node
    new_node = len(self.nodes)
    new_len = self.nodes[cur]['len'] + 2
    self.nodes.append({
      'len': new_len,
      'suffix': 1,  # Will update below
      'children': {}
    })
    self.nodes[cur]['children'][c] = new_node

    # Find suffix link for new node
    if new_len == 1:
      self.nodes[new_node]['suffix'] = 0  # Single char -> even root
    else:
      suffix_parent = self._get_link(self.nodes[cur]['suffix'], pos)
      self.nodes[new_node]['suffix'] = self.nodes[suffix_parent]['children'][c]

    self.last = new_node
    return True  # New palindrome created

  def count_distinct(self):
    """Return count of distinct palindromic substrings."""
    return len(self.nodes) - 2  # Exclude two roots

  def build(self, s):
    """Build tree for entire string."""
    for c in s:
      self.add(c)
    return self.count_distinct()


# Example usage
def count_palindromic_substrings(s):
  """Count distinct palindromic substrings in s."""
  tree = PalindromicTree()
  return tree.build(s)


def get_longest_palindrome(s):
  """Find the longest palindromic substring."""
  tree = PalindromicTree()
  tree.build(s)

  max_len = 0
  max_node = -1
  for i in range(2, len(tree.nodes)):
    if tree.nodes[i]['len'] > max_len:
      max_len = tree.nodes[i]['len']
      max_node = i

  # Reconstruct palindrome (simplified - returns length)
  return max_len


# Test
if __name__ == "__main__":
  s = "abaaba"
  print(f"Distinct palindromes in '{s}': {count_palindromic_substrings(s)}")
  print(f"Longest palindrome length: {get_longest_palindrome(s)}")
```

---

## Applications

### 1. Count Distinct Palindromic Substrings

The number of nodes (excluding roots) equals distinct palindromes.

```python
def count_distinct(s):
  tree = PalindromicTree()
  tree.build(s)
  return tree.count_distinct()  # nodes - 2
```

### 2. Longest Palindromic Substring

Track maximum length node during construction.

```python
def longest_palindrome(s):
  tree = PalindromicTree()
  tree.build(s)
  return max(node['len'] for node in tree.nodes[2:])
```

### 3. Count Total Palindrome Occurrences

Use suffix links to propagate counts.

```python
def count_occurrences(s):
  tree = PalindromicTree()
  tree.build(s)
  # Each node is visited once per occurrence
  # Propagate via suffix links in reverse order
```

---

## Related CSES Problems

| Problem | Connection |
|---------|------------|
| [Longest Palindrome](https://cses.fi/problemset/task/1111) | Find longest palindromic substring |
| [Required Substring](https://cses.fi/problemset/task/1112) | String pattern matching |

---

## Key Takeaways

1. **Two Roots:** Odd root (length -1) and even root (length 0) handle different palindrome parities
2. **Linear Time:** O(n) construction despite complex structure
3. **Suffix Links:** Enable efficient navigation to longest palindromic suffix
4. **Node Count:** At most n distinct palindromic substrings in any string of length n

---

## Practice Checklist

- [ ] Implement palindromic tree from scratch
- [ ] Trace construction on paper for a small string
- [ ] Solve "count distinct palindromes" problem
- [ ] Compare with Manacher's algorithm for longest palindrome
- [ ] Understand suffix link computation

---

## Additional Resources

- [CP-Algorithms: Palindromic Tree](https://cp-algorithms.com/string/eertree.html)
- [Original Paper by Rubinchik](https://arxiv.org/abs/1506.04862)
- [Codeforces Tutorial](https://codeforces.com/blog/entry/12143)
