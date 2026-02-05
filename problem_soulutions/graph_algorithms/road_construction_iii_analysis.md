---
title: "Road Construction III - When All Cities Become Connected"
cses_link: https://cses.fi/problemset/task/1677
category: Graph Algorithms
difficulty: Medium
---

# Road Construction III - When All Cities Become Connected

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find after which road all cities become connected |
| Input | n cities, m roads added sequentially |
| Output | Index of road that connects all cities, or "IMPOSSIBLE" |
| Constraints | 1 <= n <= 10^5, 1 <= m <= 2*10^5 |
| Key Technique | Union-Find with component counting |

## Problem Description

Given n cities and m roads added one by one, determine which road (by 1-indexed position) causes all cities to become connected. If not all cities are connected after all roads, output "IMPOSSIBLE".

**Example:**
```
Input:
4 3
1 2
3 4
2 3

Output:
3

Explanation:
After road 1 (1-2): Components = {1,2}, {3}, {4} - not connected
After road 2 (3-4): Components = {1,2}, {3,4} - not connected
After road 3 (2-3): Components = {1,2,3,4} - ALL CONNECTED!
Answer: Road 3
```

```
Input:
4 2
1 2
3 4

Output:
IMPOSSIBLE

Explanation: After all roads, still 2 components: {1,2} and {3,4}
```

## Algorithm: Union-Find with Early Termination

**Key Insight:** Track the number of connected components. When it reaches 1, all cities are connected.

**Strategy:**
1. Start with n components (each city is its own component)
2. For each road, try to union the two cities
3. If union succeeds (different components), decrement component count
4. When component count = 1, return current road index
5. If we process all roads and count > 1, return "IMPOSSIBLE"

```
n=4, Initial components = 4

Road 1 (1-2): union succeeds, components = 3
Road 2 (3-4): union succeeds, components = 2
Road 3 (2-3): union succeeds, components = 1 -> ANSWER!
```

## Implementation

### Python Solution
```python
import sys
from sys import stdin

def solve():
    input = stdin.readline
    n, m = map(int, input().split())

    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    components = n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        nonlocal components
        ra, rb = find(a), find(b)
        if ra == rb:
            return False  # Already connected

        # Union by rank
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

        components -= 1
        return True

    for i in range(1, m + 1):
        a, b = map(int, input().split())
        union(a, b)

        if components == 1:
            print(i)
            return

    print("IMPOSSIBLE")

solve()
```

### Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Initialization | O(n) | O(n) |
| Per Road | O(alpha(n)) | - |
| Total | O(n + m * alpha(n)) | O(n) |

Note: Early termination when components = 1 can improve average case.

## Visual Walkthrough

```
Example: n=5, roads: [(1,2), (3,4), (2,3), (4,5)]

Initial State:
[1]  [2]  [3]  [4]  [5]    components = 5

After Road 1 (1-2):
[1-2]  [3]  [4]  [5]       components = 4

After Road 2 (3-4):
[1-2]  [3-4]  [5]          components = 3

After Road 3 (2-3):
[1-2-3-4]  [5]             components = 2

After Road 4 (4-5):
[1-2-3-4-5]                components = 1  --> Answer: 4
```

## Common Mistakes

1. **Not checking if already connected:** If union returns false (same component), don't decrement count
2. **Off-by-one errors:** Roads are 1-indexed in output
3. **Forgetting IMPOSSIBLE case:** Must handle when m roads aren't enough
4. **Not reading remaining input:** After finding answer, must consume remaining input in some judges
5. **Minimum roads needed:** At least n-1 roads needed to connect n cities

## Edge Cases

| Case | Expected Output |
|------|-----------------|
| n=1, m=0 | 0 (or 1 city is always connected) |
| n=2, m=1, road(1,2) | 1 |
| n=3, m=2, roads don't connect all | IMPOSSIBLE |
| Duplicate roads | Still works (union returns false) |

## Key Takeaways

- Union-Find efficiently tracks connected components
- Component count starts at n and decreases with each successful union
- Early termination when components = 1 improves efficiency
- At minimum, n-1 edges are needed to connect n vertices
- The problem is essentially finding when the graph becomes a spanning tree
