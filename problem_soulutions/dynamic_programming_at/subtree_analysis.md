---
layout: simple
title: "Subtree - Tree DP with Rerooting"
permalink: /problem_soulutions/dynamic_programming_at/subtree_analysis
difficulty: Hard
tags: [tree-dp, rerooting, combinatorics, modular-arithmetic]
---

# Subtree (AtCoder DP V)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Tree DP / Rerooting |
| **Problem Link** | [AtCoder DP Contest - V](https://atcoder.jp/contests/dp/tasks/dp_v) |
| **Key Technique** | Rerooting DP |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply tree DP with rerooting to compute answers for all nodes as root
- [ ] Use prefix/suffix products to efficiently remove a child's contribution
- [ ] Handle modular arithmetic in tree DP problems
- [ ] Recognize when rerooting optimization transforms O(N^2) to O(N)

---

## Problem Statement

**Problem:** Given a tree with N vertices, for each vertex v, count the number of ways to paint some vertices black such that:
1. Vertex v is painted black
2. All black vertices form a connected subtree

**Input:**
- Line 1: N M (number of vertices and modulo)
- Next N-1 lines: edges (x_i, y_i)

**Output:**
- N lines: for each vertex 1 to N, print the count modulo M

**Constraints:**
- 1 <= N <= 10^5
- 2 <= M <= 10^9

### Example

```
Input:
3 1000000007
1 2
2 3

Output:
3
4
3
```

**Explanation:**
- Vertex 1 as root: {1}, {1,2}, {1,2,3} -> 3 ways
- Vertex 2 as root: {2}, {1,2}, {2,3}, {1,2,3} -> 4 ways
- Vertex 3 as root: {3}, {2,3}, {1,2,3} -> 3 ways

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently compute the answer for ALL nodes as root without re-running DFS N times?

The naive approach runs DFS from each vertex, giving O(N^2). The key insight is **rerooting**: compute answers for one root, then "shift" the root to adjacent nodes in O(1) per shift.

### Breaking Down the Problem

1. **What are we counting?** Connected subtrees containing a specific vertex
2. **For a fixed root:** If vertex v is black, each child subtree independently contributes `(ways_with_child_black + 1)` options (child black in some valid way, or child white)
3. **Rerooting insight:** When we move root from v to child u, u's subtree becomes "everything except the branch containing v"

### The Rerooting Technique

```
Original (root at v):          After rerooting to u:
       v                              u
      /|\                            /|\
     / | \                          / | \
    u  c  d                        v' c  d
   /|\                            /|\
  a b c                          w  x

u's contribution to v = dp[u]    v's contribution to u = dp_up[u]
```

When u becomes the new root:
- u keeps its original children (a, b, c)
- u gains v as a "new child" (with v's other children: c, d)

---

## Solution 1: Naive O(N^2) Approach

### Idea

Run a separate DFS from each vertex as root and compute the answer.

### Code

```python
def solve_naive(n, m, edges):
 """
 Naive solution: DFS from each vertex.
 Time: O(N^2), Space: O(N)
 """
 graph = [[] for _ in range(n + 1)]
 for u, v in edges:
  graph[u].append(v)
  graph[v].append(u)

 def dfs(v, parent):
  result = 1  # Just v itself painted black
  for u in graph[v]:
   if u != parent:
    child_ways = dfs(u, v)
    # For each child: either don't include it (1 way)
    # or include it in (child_ways) ways
    result = result * (child_ways + 1) % m
  return result

 return [dfs(root, -1) for root in range(1, n + 1)]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^2) | N roots, O(N) DFS each |
| Space | O(N) | Recursion stack + adjacency list |

---

## Solution 2: Optimal Rerooting DP - O(N)

### Key Insight

> **The Trick:** Compute dp_down[v] (ways when v is root of its subtree) and dp_up[v] (contribution from v's parent direction), then combine them.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[v]` | Number of valid colorings in subtree rooted at v (v must be black) |
| `dp_up[v]` | Contribution to v from its parent's direction (when v becomes root) |

**In plain English:**
- `dp[v]` counts ways to color v's subtree (in the initial rooting)
- `dp_up[v]` counts ways to color "everything outside v's subtree" when we reroot to v

### State Transition

**Phase 1 - Compute dp[v] (DFS down):**
```
dp[v] = product of (dp[child] + 1) for all children
```
The `+1` represents the option to not include that child at all.

**Phase 2 - Compute dp_up[v] (DFS down again):**
```
dp_up[child] = (dp_up[v] + 1) * product of (dp[sibling] + 1) for all siblings
```

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[leaf]` | 1 | Only the leaf itself can be black |
| `dp_up[root]` | 1 | No contribution from above for initial root |

### Algorithm

1. Build adjacency list from edges
2. **DFS 1 (Down):** Compute `dp[v]` for all vertices
3. **DFS 2 (Reroot):** Compute `dp_up[v]` using prefix/suffix products
4. **Final answer:** `ans[v] = dp[v] * (dp_up[v] + 1) % m` (but we need careful combination)

### Dry Run Example

Let's trace through with `N=3, edges: 1-2, 2-3`:

```
Tree structure (rooted at 1):
    1
    |
    2
    |
    3

Phase 1: DFS Down (compute dp[])
---------------------------------
Start DFS from node 1:

  Visit node 3 (leaf):
    dp[3] = 1  (just node 3)

  Visit node 2:
    children of 2: [3]
    dp[2] = (dp[3] + 1) = (1 + 1) = 2
    meaning: {2} or {2,3}

  Visit node 1:
    children of 1: [2]
    dp[1] = (dp[2] + 1) = (2 + 1) = 3
    meaning: {1}, {1,2}, {1,2,3}

After Phase 1:
  dp[1] = 3, dp[2] = 2, dp[3] = 1

Phase 2: Rerooting (compute final answers)
------------------------------------------
Node 1 is initial root:
  ans[1] = dp[1] = 3

Reroot to node 2:
  - Node 2 gains node 1 as "child" from above
  - Contribution from above = dp_up[2] = 1 (just node 1, no other branches)
  - ans[2] = dp[2] * (dp_up[2] + 1) = 2 * 2 = 4

  Actually using our formula:
  - Original dp[2] counts subtree below
  - dp_up[2] = 1 (contribution from node 1's direction)
  - Product of children + parent direction:
    ans[2] = (dp[3] + 1) * (dp_up[2] + 1) = 2 * 2 = 4

Reroot to node 3:
  - dp_up[3] from node 2's direction
  - Node 2's contribution to node 3 = (dp_up[2] + 1) = 2
  - ans[3] = (dp_up[3] + 1) = (2 + 1) = 3

Final: [3, 4, 3]
```

### Visual Diagram

```
Original tree (root=1):       Rerooted to 2:           Rerooted to 3:
      1                            2                        3
      |                           / \                       |
      2                          1   3                      2
      |                                                     |
      3                                                     1

dp[1]=3                     ans[2]=4                   ans[3]=3
{1},{1,2},{1,2,3}          {2},{1,2},{2,3},{1,2,3}    {3},{2,3},{1,2,3}
```

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200005)

def solve():
 input_data = sys.stdin.read().split()
 idx = 0
 n = int(input_data[idx]); idx += 1
 m = int(input_data[idx]); idx += 1

 graph = defaultdict(list)
 for _ in range(n - 1):
  x = int(input_data[idx]); idx += 1
  y = int(input_data[idx]); idx += 1
  graph[x].append(y)
  graph[y].append(x)

 # dp[v] = ways to color subtree rooted at v (v is black)
 dp = [0] * (n + 1)
 # ans[v] = final answer when v is the root
 ans = [0] * (n + 1)

 # Phase 1: DFS to compute dp[] (subtree answers)
 def dfs1(v, parent):
  dp[v] = 1
  for u in graph[v]:
   if u != parent:
    dfs1(u, v)
    dp[v] = dp[v] * (dp[u] + 1) % m

 # Phase 2: Rerooting DFS
 def dfs2(v, parent, from_parent):
  """
  from_parent = contribution from parent's direction
  (ways to extend upward from v)
  """
  children = [u for u in graph[v] if u != parent]
  k = len(children)

  # Compute prefix and suffix products for efficient child removal
  # prefix[i] = product of (dp[children[0..i-1]] + 1)
  # suffix[i] = product of (dp[children[i+1..k-1]] + 1)
  prefix = [1] * (k + 1)
  suffix = [1] * (k + 1)

  for i in range(k):
   prefix[i + 1] = prefix[i] * (dp[children[i]] + 1) % m
  for i in range(k - 1, -1, -1):
   suffix[i] = suffix[i + 1] * (dp[children[i]] + 1) % m

  # Final answer for v: all children + parent contribution
  ans[v] = prefix[k] * (from_parent + 1) % m

  # Propagate to each child
  for i, u in enumerate(children):
   # Contribution to child u from v's direction:
   # = (from_parent + 1) * product of all OTHER children
   siblings_product = prefix[i] * suffix[i + 1] % m
   contribution_to_child = (from_parent + 1) * siblings_product % m
   dfs2(u, v, contribution_to_child)

 dfs1(1, -1)
 dfs2(1, -1, 0)  # from_parent = 0 for root (no parent)

 result = []
 for v in range(1, n + 1):
  result.append(str(ans[v]))
 print('\n'.join(result))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N) | Two DFS traversals, O(degree) work per node |
| Space | O(N) | Adjacency list + DP arrays + recursion stack |

---

## Common Mistakes

### Mistake 1: Forgetting the +1 for "not including" a branch

```python
# WRONG
dp[v] = product of dp[child]

# CORRECT
dp[v] = product of (dp[child] + 1)
```

**Problem:** The `+1` accounts for the option to not paint any vertex in that subtree black.
**Fix:** Always add 1 to represent the "exclude this branch" option.

### Mistake 2: Incorrect from_parent initialization

```python
# WRONG
dfs2(1, -1, 1)  # Starting with from_parent = 1

# CORRECT
dfs2(1, -1, 0)  # Root has no parent contribution
```

**Problem:** The root has no parent, so its `from_parent` contribution should be 0.
**Fix:** Initialize `from_parent = 0` for the root.

### Mistake 3: Modular arithmetic overflow

**Problem:** Multiplying large numbers can overflow before taking mod.
**Fix:** Take mod after each multiplication.

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single node | N=1 | ans[1] = 1 | Only one way: paint node 1 |
| Linear chain | N nodes in a line | Middle nodes have more ways | More branching options |
| Star graph | One center, N-1 leaves | Center has 2^(N-1) ways | Each leaf independent |
| Large M | M > 10^9 | Handle without overflow | Use long long in C++ |

---

## When to Use This Pattern

### Use Rerooting DP When:
- You need to compute an answer for every node as if it were the root
- The answer for a node depends on its entire connected component
- The DP transition is "mergeable" (can combine/uncombine child contributions)

### Don't Use When:
- You only need the answer for one specific root
- The DP state cannot be efficiently "un-merged" (e.g., min/max without tracking)
- The tree has special structure that allows simpler solutions

### Pattern Recognition Checklist:
- [ ] Need answer for ALL nodes as root? -> **Consider rerooting**
- [ ] DP uses product/sum that can be inverted? -> **Rerooting works well**
- [ ] DP uses min/max? -> **Need extra bookkeeping (store top-2 values)**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Basic tree DFS |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Simpler rerooting |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum-based rerooting |
| [AtCoder DP P - Independent Set](https://atcoder.jp/contests/dp/tasks/dp_p) | Tree DP without rerooting |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Codeforces - Tree Painting](https://codeforces.com/contest/1187/problem/E) | More complex rerooting |
| [AtCoder ABC 220 F](https://atcoder.jp/contests/abc220/tasks/abc220_f) | Rerooting with XOR |

---

## Key Takeaways

1. **The Core Idea:** Rerooting DP computes answers for all roots in O(N) by reusing computation
2. **Time Optimization:** From O(N^2) naive to O(N) by propagating parent contributions
3. **Space Trade-off:** O(N) extra space for prefix/suffix products enables efficient child removal
4. **Pattern:** When DP values combine via product, use prefix/suffix arrays to "remove" one factor

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why prefix/suffix products enable O(1) contribution removal
- [ ] Identify when rerooting is applicable vs. when it's not
- [ ] Implement the two-DFS rerooting pattern from scratch

---

## Additional Resources

- [CP-Algorithms: Rerooting Technique](https://cp-algorithms.com/graph/reroot.html)
- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp/editorial)
- [USACO Guide: Tree DP](https://usaco.guide/gold/dp-trees)
