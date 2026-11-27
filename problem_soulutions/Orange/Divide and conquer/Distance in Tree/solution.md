# Distance in Tree

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a tree with n vertices and a positive number k, find the number of distinct pairs of vertices which have a distance of exactly k between them. Note that pairs (u, v) and (v, u) are the same.

## Input Format
- First line: n and k (1 ≤ n ≤ 50000, 1 ≤ k ≤ 500)
- Next n-1 lines: edges aᵢ bᵢ (1 ≤ aᵢ, bᵢ ≤ n)

## Output Format
Print the number of distinct pairs with distance exactly k.

## Example
```
Input:
5 2
1 2
2 3
3 4
4 5

Output:
3
```
Tree is a path: 1-2-3-4-5. Pairs at distance exactly 2: (1,3), (2,4), (3,5). Total = 3.

## Solution

### Approach
Because k ≤ 500, a tree DP over distances is enough (no centroid decomposition needed):
1. `cnt[d]` = number of nodes at depth d below u, for d ≤ k.
2. Before merging each child v, pair it with what is already in `cnt`: a node at depth d2 in v's subtree is d2 + 1 from u, so it pairs with `cnt[k - d2 - 1]`.
3. Merge the child's counts shifted by one.

Each pair is counted exactly once, at its highest node.

### Python Solution (Tree DP)

```python
import sys
from collections import defaultdict

sys.setrecursionlimit(100000)

def solve():
    n, k = map(int, input().split())

    adj = defaultdict(list)
    for _ in range(n - 1):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    total_pairs = 0

    def dfs(u, parent):
        nonlocal total_pairs

        # cnt[d] = count of nodes at distance d from u in u's subtree
        cnt = [0] * (k + 1)
        cnt[0] = 1  # u itself at distance 0

        for v in adj[u]:
            if v == parent:
                continue

            # Get counts from child subtree
            child_cnt = dfs(v, u)

            # Count pairs using zip-like iteration
            for d1 in range(k + 1):
                d2 = k - d1 - 1  # -1 because edge u-v adds 1
                if 0 <= d2 < len(child_cnt):
                    total_pairs += cnt[d1] * child_cnt[d2]

            # Merge child counts (shifted by 1 for edge u-v)
            for d in range(min(k, len(child_cnt))):
                cnt[d + 1] += child_cnt[d]

        return cnt

    dfs(1, -1)
    print(total_pairs)

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × K) with tree DP
- **Space Complexity:** O(N × K) for DP arrays

### Key Insight
For each node u, count paths of length k passing through u by combining distances from different subtrees. If one subtree has nodes at distance d from u, and another has nodes at distance k-d, they form pairs at distance k.
