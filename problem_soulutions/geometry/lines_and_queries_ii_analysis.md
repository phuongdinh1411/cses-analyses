---
layout: simple
title: "Line Segment Intersection Queries II - Li Chao Tree"
permalink: /problem_soulutions/geometry/lines_and_queries_ii_analysis
difficulty: Hard
tags: [li-chao-tree, convex-hull-trick, geometry, segment-tree, optimization]
---

# Line Segment Intersection Queries II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Geometry / Data Structures |
| **Time Limit** | 1 second |
| **Key Technique** | Li Chao Tree (Dynamic CHT) |
| **CSES Link** | [Line Segment Intersection Queries](https://cses.fi/problemset/task/2190) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when Li Chao Tree is needed over standard CHT
- [ ] Implement a Li Chao segment tree for arbitrary query order
- [ ] Handle dynamic line insertions with O(log n) query time
- [ ] Apply Li Chao Tree to optimize DP problems with non-monotonic transitions

---

## Problem Statement

**Problem:** Given n lines of the form y = mx + b, answer q queries. Each query gives an x-coordinate, and you must find the minimum y-value among all lines at that x. Unlike the simpler version, queries can come in any order (not sorted by x).

**Input:**
- Line 1: Two integers n and q (number of lines and queries)
- Next n lines: Two integers m and b (slope and y-intercept)
- Next q lines: One integer x (query x-coordinate)

**Output:**
- For each query, print the minimum y-value at x

**Constraints:**
- 1 <= n, q <= 2 * 10^5
- -10^9 <= m, b, x <= 10^9

### Example

```
Input:
3 4
1 3
2 1
-1 4
0
1
-2
5

Output:
1
3
-3
-1
```

**Explanation:** Lines: y = x+3, y = 2x+1, y = -x+4
- x=0: min(3, 1, 4) = 1
- x=1: min(4, 3, 3) = 3
- x=-2: min(1, -3, 6) = -3
- x=5: min(8, 11, -1) = -1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** The standard Convex Hull Trick requires sorted queries. What if queries come in arbitrary order?

The Li Chao Tree is a segment tree where each node stores the "best" line for its interval. When inserting a new line, we compare it with the existing line and keep the one that wins more often.

### Why Standard CHT Fails

Standard CHT maintains a deque of lines and uses a pointer that only moves in one direction. This requires:
1. Lines inserted in sorted slope order, OR
2. Queries in sorted x order

When neither condition holds, we need Li Chao Tree.

### The Li Chao Insight

Instead of maintaining a hull explicitly, we use divide-and-conquer:
- Each segment tree node covers an x-range
- Store the line that is "dominant" at the midpoint
- Recursively push the dominated line to the half where it might still win

---

## Solution 1: Brute Force

### Idea

For each query, evaluate all n lines and find the minimum.

### Code

```python
def solve_brute_force(lines, queries):
  """
  Time: O(n * q)
  Space: O(1)
  """
  results = []
  for x in queries:
    min_y = float('inf')
    for m, b in lines:
      min_y = min(min_y, m * x + b)
    results.append(min_y)
  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * q) | Check all lines for each query |
| Space | O(1) | No extra storage |

**Why This Is Slow:** With n, q up to 2*10^5, we get 4*10^10 operations - far too slow.

---

## Solution 2: Li Chao Tree (Optimal)

### Key Insight

> **The Trick:** Use a segment tree over x-coordinates. Each node stores one line. When querying, traverse from root to leaf, taking the best value seen.

### How Li Chao Tree Works

1. **Structure:** Segment tree over x-coordinate range [MIN_X, MAX_X]
2. **Node storage:** Each node stores at most one line
3. **Insert:** Compare new line with stored line at midpoint; winner stays, loser recurses
4. **Query:** Traverse root to leaf, evaluating stored lines at query point

### Visual Diagram

```
Insert lines: y=2x+1, y=-x+4, y=x+3
Query x-range: [-4, 4]

        [-4, 4] stores: y=2x+1 (best at mid=0? -> eval: 1)
         /            \
    [-4, 0]          [0, 4]
  stores: y=-x+4   stores: y=x+3
  (wins left)      (wins right)

Query x=3:
  Root [-4,4]: line y=2x+1, eval(3)=7
  Go right [0,4]: line y=x+3, eval(3)=6
  Result: min(7, 6) = 6
```

### Algorithm

1. Build segment tree covering x-coordinate range
2. For each line, insert into tree using divide-and-conquer
3. For each query, traverse tree and find minimum

### Dry Run Example

```
Lines: (m=2, b=1), (m=-1, b=4), (m=1, b=3)
Tree range: [-10, 10]

Insert y = 2x+1: Node [-10,10] empty -> store (2,1)

Insert y = -x+4:
  At mid=0: cur(2,1)=1 vs new(-1,4)=4 -> cur wins
  At x=10: cur=21 vs new=-6 -> new wins right half
  Push (-1,4) to right child [1,10]

Insert y = x+3:
  At mid=0: cur(2,1)=1 vs new(1,3)=3 -> cur wins
  At x=10: cur=21 vs new=13 -> new wins right
  Node [1,10] has (-1,4), at mid=5: (-1,4)=-1 vs (1,3)=8
  Current wins, push (1,3) to left child

Query x=2:
  Root [-10,10]: (2,1) -> 5
  Right [1,10]: (-1,4) -> 2
  Result: min(5, 2) = 2
```

### Code (Python)

```python
import sys

class LiChaoTree:
  def __init__(self, lo, hi):
    self.lo, self.hi = lo, hi
    self.line = None
    self.left = self.right = None

  def eval(self, line, x):
    return line[0] * x + line[1]

  def insert(self, new_line):
    if self.line is None:
      self.line = new_line
      return
    lo, hi = self.lo, self.hi
    mid = (lo + hi) // 2
    if self.eval(new_line, mid) < self.eval(self.line, mid):
      self.line, new_line = new_line, self.line
    if lo == hi:
      return
    if self.eval(new_line, lo) < self.eval(self.line, lo):
      if not self.left:
        self.left = LiChaoTree(lo, mid)
      self.left.insert(new_line)
    else:
      if not self.right:
        self.right = LiChaoTree(mid + 1, hi)
      self.right.insert(new_line)

  def query(self, x):
    result = self.eval(self.line, x) if self.line else float('inf')
    if self.lo == self.hi:
      return result
    mid = (self.lo + self.hi) // 2
    if x <= mid and self.left:
      result = min(result, self.left.query(x))
    elif x > mid and self.right:
      result = min(result, self.right.query(x))
    return result

def solve():
  data = sys.stdin.read().split()
  idx = 0
  n, q = int(data[idx]), int(data[idx+1])
  idx += 2
  tree = LiChaoTree(-10**9, 10**9)
  for _ in range(n):
    m, b = int(data[idx]), int(data[idx+1])
    tree.insert((m, b))
    idx += 2
  for _ in range(q):
    print(tree.query(int(data[idx])))
    idx += 1

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log C) | Each insert/query traverses O(log C) depth |
| Space | O(n log C) | At most n*log(C) nodes created |

Where C = MAX_X - MIN_X (coordinate range).

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** m * x can exceed 10^18, causing overflow.
**Fix:** Use `long long` for all calculations.

### Mistake 2: Wrong Recursion Direction

```python
# WRONG - always goes left
if new_lo < cur_lo:
  self.left.insert(new_line)
else:
  self.left.insert(new_line)  # Bug: should be right!

# CORRECT
if new_lo < cur_lo:
  self.left.insert(new_line)
else:
  self.right.insert(new_line)
```

### Mistake 3: Not Handling Empty Nodes

```python
# WRONG - crashes on empty node
def query(self, x):
  result = self.eval(self.line, x)  # self.line might be None!

# CORRECT
def query(self, x):
  result = float('inf')
  if self.line is not None:
    result = self.eval(self.line, x)
```

---

## Edge Cases

| Case | Input | Handling |
|------|-------|----------|
| Single line | n=1 | Tree has one node, query returns that line's value |
| Parallel lines | Same slope | Both stored, one dominates based on intercept |
| Large coordinates | x = 10^9 | Use long long, handle overflow |
| Negative coordinates | x < 0, m < 0 | Works correctly with signed arithmetic |
| All same line | Duplicate lines | Redundant but handled correctly |

---

## When to Use This Pattern

### Use Li Chao Tree When:
- Need minimum/maximum over set of linear functions
- Queries come in **arbitrary order** (not sorted)
- Lines can be inserted **online** (one at a time)
- Coordinate range is bounded

### Use Standard CHT Instead When:
- Queries are sorted by x (use monotonic deque)
- Lines have sorted slopes (allows amortized O(1) insertion)
- Tighter memory constraints (Li Chao uses more space)

### Pattern Recognition Checklist:
- [ ] DP recurrence like `dp[i] = min(dp[j] + a[i]*b[j])` -> **Consider CHT/Li Chao**
- [ ] Need min/max of y = mx + b at point x -> **Line container problem**
- [ ] Unsorted queries, online insertions -> **Li Chao Tree**
- [ ] Sorted queries or slopes -> **Standard CHT deque**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Line Segment Intersection Queries I](https://cses.fi/problemset/task/2189) | Simpler CHT with sorted queries |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Frog 3 (AtCoder DP)](https://atcoder.jp/contests/dp/tasks/dp_z) | CHT application in DP |
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | Different segment tree application |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Covered Points Count](https://cses.fi/problemset/task/2168) | Coordinate compression with sweepline |
| [Aliens (IOI)](https://oj.uz/problem/view/IOI16_aliens) | Li Chao + Lagrangian relaxation |

---

## Key Takeaways

1. **Core Idea:** Li Chao Tree uses segment tree structure to answer arbitrary-order line queries
2. **Time Trade-off:** O(log C) per operation vs O(1) amortized for sorted CHT
3. **Space Cost:** O(n log C) nodes, more than standard CHT's O(n)
4. **Versatility:** Handles online insertions and arbitrary query order

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why standard CHT fails with unsorted queries
- [ ] Implement Li Chao Tree insertion and query from scratch
- [ ] Identify problems where Li Chao Tree applies
- [ ] Handle edge cases (overflow, empty nodes, single line)

---

## Additional Resources

- [CP-Algorithms: Li Chao Tree](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- [CF Blog: Li Chao Tree Tutorial](https://codeforces.com/blog/entry/86731)
- [CSES Line Segment Intersection](https://cses.fi/problemset/task/2190) - Related geometry problem
