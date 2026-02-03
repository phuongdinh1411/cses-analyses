---
layout: simple
title: "Tree Matching - Tree DP Problem"
permalink: /problem_soulutions/tree_algorithms/tree_matching_analysis
difficulty: Medium
tags: [tree-dp, matching, greedy, dfs]
prerequisites: [tree_traversal, basic_dp]
---

# Tree Matching

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree DP |
| **Time Limit** | 1 second |
| **Key Technique** | Tree DP with matched/unmatched states |
| **CSES Link** | [Tree Matching](https://cses.fi/problemset/task/1130) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand maximum matching in trees and why greedy works bottom-up
- [ ] Define DP states for "matched" vs "unmatched" nodes in tree problems
- [ ] Implement post-order DFS for tree DP computations
- [ ] Recognize when a node's state depends on children's states
- [ ] Apply this pattern to other tree DP problems involving edge selection

---

## Problem Statement

**Problem:** Given a tree with n nodes, find the maximum number of edges that can be selected such that no two selected edges share a common vertex (maximum matching).

**Input:**
- Line 1: integer n (number of nodes)
- Next n-1 lines: two integers a and b representing an edge between nodes a and b

**Output:**
- Print one integer: the maximum number of edges in a matching

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= a, b <= n

### Example

```
Input:
5
1 2
1 3
3 4
3 5

Output:
2
```

**Explanation:**
The tree structure:
```
    1
   / \
  2   3
     / \
    4   5
```

Maximum matching: 2 edges. Possible matchings:
- (1-2) and (3-4)
- (1-2) and (3-5)
- (1-3) and (4-5) -- Note: this is also 2 edges

No matching can have 3 edges because node 3 has 3 edges but can only be in one matched pair.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we decide whether to match a node with one of its children?

This is a classic tree DP problem where each node has two states: **matched** (already part of an edge in our matching) or **unmatched** (available to be matched with parent). The key insight is that we process bottom-up: when we visit a node, we already know the optimal solutions for all its subtrees.

### Breaking Down the Problem

1. **What are we looking for?** Maximum number of non-adjacent edges
2. **What information do we have?** Tree structure (edges between nodes)
3. **What's the relationship between input and output?** We must select edges such that each node appears in at most one selected edge

### Analogies

Think of this problem like **pairing up dance partners** at a party arranged in a tree. Each person (node) can dance with at most one partner (matched to one edge). We process from the leaves up: first pair up people at the edges of the party, then work our way to the center, always making locally optimal choices.

---

## Solution 1: Brute Force

### Idea

Try all possible subsets of edges and find the largest valid matching (no shared vertices).

### Algorithm

1. Generate all 2^(n-1) subsets of edges
2. For each subset, check if it forms a valid matching
3. Track the maximum size valid matching found

### Code

```python
def solve_brute_force(n, edges):
    """
    Brute force: try all edge subsets.

    Time: O(2^m * m) where m = n-1 edges
    Space: O(m)
    """
    from itertools import combinations

    def is_valid_matching(edge_subset):
        used = set()
        for a, b in edge_subset:
            if a in used or b in used:
                return False
            used.add(a)
            used.add(b)
        return True

    max_matching = 0
    for k in range(len(edges) + 1):
        for subset in combinations(edges, k):
            if is_valid_matching(subset):
                max_matching = max(max_matching, len(subset))

    return max_matching
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n) | 2^(n-1) subsets, O(n) validation each |
| Space | O(n) | Storing current subset and used set |

### Why This Works (But Is Slow)

This exhaustively checks every possible selection, guaranteeing we find the maximum. However, with n up to 2 x 10^5, this is completely infeasible.

---

## Solution 2: Optimal Solution (Tree DP)

### Key Insight

> **The Trick:** Process the tree bottom-up. For each node, decide greedily: if any child is unmatched, match with that child (gaining +1 to our answer). This greedy choice is always optimal in trees!

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[node][0]` | Max matching in subtree when node is **unmatched** (available for parent) |
| `dp[node][1]` | Max matching in subtree when node is **matched** (not available for parent) |

**In plain English:**
- `dp[v][0]`: Best we can do in v's subtree if we promise NOT to use v
- `dp[v][1]`: Best we can do in v's subtree if we ARE using v (matched with a child)

### State Transition

For a node v with children c1, c2, ..., ck:

```
dp[v][0] = sum of max(dp[ci][0], dp[ci][1]) for all children
dp[v][1] = dp[v][0] + 1 - max(dp[cj][0], dp[cj][1]) + dp[cj][0]
         = dp[v][0] + 1 + min(dp[ci][0] - max(dp[ci][0], dp[ci][1])) for some child ci
```

**Simplified logic:**
- If node is unmatched: take the best from each child subtree
- If node is matched: match with one child (that child must be unmatched), take best from others

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| Leaf node | dp[leaf][0] = 0, dp[leaf][1] = 0 | No edges in subtree, cannot match alone |

### Algorithm

1. Build adjacency list from edges
2. Run DFS from any root (e.g., node 1)
3. For each node in post-order:
   - Calculate dp[node][0] by summing best of children
   - Calculate dp[node][1] by trying to match with each child
4. Answer is max(dp[root][0], dp[root][1])

### Dry Run Example

Let's trace through with the example tree:

```
Tree:     1
         / \
        2   3
           / \
          4   5

Processing in post-order: 2, 4, 5, 3, 1
```

```
Step 1: Process node 2 (leaf)
  dp[2][0] = 0  (no children)
  dp[2][1] = 0  (cannot match, no children)

Step 2: Process node 4 (leaf)
  dp[4][0] = 0
  dp[4][1] = 0

Step 3: Process node 5 (leaf)
  dp[5][0] = 0
  dp[5][1] = 0

Step 4: Process node 3 (children: 4, 5)
  dp[3][0] = max(dp[4][0], dp[4][1]) + max(dp[5][0], dp[5][1])
           = max(0,0) + max(0,0) = 0

  For dp[3][1], try matching with child 4:
    = dp[3][0] - max(dp[4][0], dp[4][1]) + dp[4][0] + 1
    = 0 - 0 + 0 + 1 = 1
  Try matching with child 5:
    = dp[3][0] - max(dp[5][0], dp[5][1]) + dp[5][0] + 1
    = 0 - 0 + 0 + 1 = 1

  dp[3][1] = 1

Step 5: Process node 1 (children: 2, 3)
  dp[1][0] = max(dp[2][0], dp[2][1]) + max(dp[3][0], dp[3][1])
           = max(0,0) + max(0,1) = 0 + 1 = 1

  For dp[1][1], try matching with child 2:
    = dp[1][0] - max(dp[2][0], dp[2][1]) + dp[2][0] + 1
    = 1 - 0 + 0 + 1 = 2
  Try matching with child 3:
    = dp[1][0] - max(dp[3][0], dp[3][1]) + dp[3][0] + 1
    = 1 - 1 + 0 + 1 = 1

  dp[1][1] = 2

Answer: max(dp[1][0], dp[1][1]) = max(1, 2) = 2
```

### Visual Diagram

```
        1 (dp: [1, 2])
       / \
      /   \
     2     3 (dp: [0, 1])
 (dp:[0,0]) / \
           4   5
    (dp:[0,0]) (dp:[0,0])

Matching selected: (1-2) and (3-4) or (3-5)
```

### Code

**Python Solution:**

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve(n, edges):
    """
    Tree DP for maximum matching.

    Time: O(n) - single DFS traversal
    Space: O(n) - adjacency list and DP array
    """
    if n == 1:
        return 0

    # Build adjacency list
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    # dp[node] = [unmatched_value, matched_value]
    dp = [[0, 0] for _ in range(n + 1)]

    def dfs(node, parent):
        sum_children = 0
        best_gain = float('-inf')

        for child in adj[node]:
            if child != parent:
                dfs(child, node)

                # When unmatched, take best from each child
                best_child = max(dp[child][0], dp[child][1])
                sum_children += best_child

                # Gain if we match with this child instead
                # We lose best_child but gain dp[child][0] + 1
                gain = dp[child][0] + 1 - best_child
                best_gain = max(best_gain, gain)

        dp[node][0] = sum_children

        # Can only match if we have children
        if best_gain != float('-inf'):
            dp[node][1] = sum_children + best_gain
        else:
            dp[node][1] = 0

    dfs(1, -1)
    return max(dp[1][0], dp[1][1])


def main():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1

    edges = []
    for _ in range(n - 1):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        edges.append((a, b))

    print(solve(n, edges))


if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
vector<int> adj[MAXN];
int dp[MAXN][2];  // dp[node][0] = unmatched, dp[node][1] = matched

void dfs(int node, int parent) {
    int sum_children = 0;
    int best_gain = INT_MIN;

    for (int child : adj[node]) {
        if (child != parent) {
            dfs(child, node);

            int best_child = max(dp[child][0], dp[child][1]);
            sum_children += best_child;

            // Gain if we match with this child
            int gain = dp[child][0] + 1 - best_child;
            best_gain = max(best_gain, gain);
        }
    }

    dp[node][0] = sum_children;
    dp[node][1] = (best_gain != INT_MIN) ? sum_children + best_gain : 0;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    dfs(1, -1);

    cout << max(dp[1][0], dp[1][1]) << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single DFS visiting each node once |
| Space | O(n) | Adjacency list + DP array + recursion stack |

---

## Common Mistakes

### Mistake 1: Forgetting to Handle Single Node

```python
# WRONG - crashes on n=1
def solve(n, edges):
    adj = build_adj(edges)
    dfs(1, -1)
    return max(dp[1])

# CORRECT
def solve(n, edges):
    if n == 1:
        return 0  # No edges, no matching possible
    # ... rest of solution
```

**Problem:** A single node has no edges to match.
**Fix:** Return 0 immediately for n=1.

### Mistake 2: Wrong State Transition

```python
# WRONG - always matching with first child
dp[node][1] = dp[children[0]][0] + 1 + sum(max(dp[c]) for c in children[1:])

# CORRECT - try all children, pick best
for child in children:
    option = dp[node][0] - max(dp[child]) + dp[child][0] + 1
    dp[node][1] = max(dp[node][1], option)
```

**Problem:** Not considering all children for matching.
**Fix:** Try matching with each child and take the best option.

### Mistake 3: Stack Overflow on Deep Trees

```python
# WRONG - may stack overflow for n=200000
def dfs(node, parent):
    for child in adj[node]:
        if child != parent:
            dfs(child, node)  # Deep recursion
```

**Problem:** Default Python recursion limit is ~1000.
**Fix:** Use `sys.setrecursionlimit(300000)` or implement iterative DFS.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1 | 0 | No edges exist |
| Two nodes | n=2, edge (1,2) | 1 | Only one edge, must be in matching |
| Linear tree (path) | 1-2-3-4-5 | 2 | Every other edge: (1-2), (3-4) |
| Star graph | 1 connected to 2,3,4,5 | 1 | Center can only match with one leaf |
| Complete binary tree | 7 nodes, height 2 | 3 | Match all leaves with their parents |

---

## When to Use This Pattern

### Use This Approach When:
- Finding maximum/minimum edge selections in trees
- Each node can be in at most one selected edge
- Problem has optimal substructure (subtree solutions combine)
- Need to track binary state per node (used/unused, matched/unmatched)

### Don't Use When:
- Graph has cycles (not a tree) - use general matching algorithms
- Need to find ALL matchings, not just maximum
- Edges have weights and you need weighted matching (modify DP states)

### Pattern Recognition Checklist:
- [ ] Is it a tree structure? --> **Consider tree DP**
- [ ] Does each node have two possible states? --> **Use dp[node][0/1]**
- [ ] Can you solve subtrees independently? --> **Use post-order DFS**
- [ ] Is greedy locally optimal? --> **Bottom-up matching works**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Subordinates (CSES)](https://cses.fi/problemset/task/1674) | Basic tree DP - counting subtree sizes |
| [Tree Diameter (CSES)](https://cses.fi/problemset/task/1131) | Tree traversal and path computation |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Tree Distances I (CSES)](https://cses.fi/problemset/task/1132) | Different DP state (distance instead of matching) |
| [Tree Distances II (CSES)](https://cses.fi/problemset/task/1133) | Sum of distances, requires rerooting technique |
| [Binary Tree Cameras (LC)](https://leetcode.com/problems/binary-tree-cameras/) | Three states: covered, has camera, not covered |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Finding a Centroid (CSES)](https://cses.fi/problemset/task/1674) | Centroid decomposition |
| [Binary Tree Maximum Path Sum (LC)](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Path DP with negative values |
| [Maximum Matching in General Graphs](https://cp-algorithms.com/graph/matching.html) | Blossom algorithm for non-trees |

---

## Key Takeaways

1. **The Core Idea:** Process bottom-up; greedily match unmatched children with their parent
2. **Time Optimization:** From O(2^n) brute force to O(n) tree DP
3. **Space Trade-off:** O(n) space for DP array enables linear time
4. **Pattern:** Classic tree DP with binary states per node (matched/unmatched)

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why greedy bottom-up matching is optimal for trees
- [ ] Draw the DP state transitions for a small example
- [ ] Implement in your preferred language in under 15 minutes
- [ ] Handle edge cases (n=1, linear tree, star graph)

---

## Additional Resources

- [CP-Algorithms: Maximum Matching](https://cp-algorithms.com/graph/matching.html)
- [CSES Problem Set - Tree Algorithms](https://cses.fi/problemset/list/)
- [Tree DP Tutorial](https://codeforces.com/blog/entry/20935)
