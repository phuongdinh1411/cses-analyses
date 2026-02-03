---
title: "Road Construction II - Union-Find with Component Tracking"
cses_link: https://cses.fi/problemset/task/1676
category: Graph Algorithms
difficulty: Medium
---

# Road Construction II - Union-Find with Component Tracking

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Track connectivity after each road: number of components and largest component size |
| Input | n cities, m roads added one by one |
| Output | After each road: (component_count, max_component_size) |
| Constraints | 1 <= n, m <= 10^5 |
| Key Technique | Union-Find with size tracking |

## Problem Description

There are n cities and m roads to be built. After each road is constructed, report:
1. The number of connected components
2. The size of the largest component

**Example:**
```
Input:
5 3
1 2
1 3
4 5

Output:
4 2
3 3
2 3

Explanation:
After road 1-2: 4 components {1,2}, {3}, {4}, {5}, largest = 2
After road 1-3: 3 components {1,2,3}, {4}, {5}, largest = 3
After road 4-5: 2 components {1,2,3}, {4,5}, largest = 3
```

## Algorithm: Union-Find with Size Tracking

**Key Insight:** Standard Union-Find tracks connectivity, but we also need to track component sizes and maintain the maximum.

**Data Structure:**
- `parent[i]`: parent of node i (root points to itself)
- `size[i]`: size of component rooted at i
- `components`: current number of components
- `max_size`: size of largest component

**Operations:**
1. **Find(x):** Find root with path compression
2. **Union(x, y):** Merge components, update sizes, track max

```
Initial: n=5, components=5, max_size=1
         [1] [2] [3] [4] [5]

After union(1,2):
         [1,2] [3] [4] [5]
         components=4, max_size=2

After union(1,3):
         [1,2,3] [4] [5]
         components=3, max_size=3

After union(4,5):
         [1,2,3] [4,5]
         components=2, max_size=3
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
    size = [1] * (n + 1)
    components = n
    max_size = 1

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        nonlocal components, max_size
        ra, rb = find(a), find(b)
        if ra == rb:
            return  # Already connected

        # Union by size
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

        components -= 1
        max_size = max(max_size, size[ra])

    result = []
    for _ in range(m):
        a, b = map(int, input().split())
        union(a, b)
        result.append(f"{components} {max_size}")

    print('\n'.join(result))

solve()
```

### C++ Solution
```cpp
#include <bits/stdc++.h>
using namespace std;

int parent[100001], sz[100001];
int components, maxSize;

int find(int x) {
    if (parent[x] != x)
        parent[x] = find(parent[x]);
    return parent[x];
}

void unite(int a, int b) {
    int ra = find(a), rb = find(b);
    if (ra == rb) return;

    if (sz[ra] < sz[rb]) swap(ra, rb);
    parent[rb] = ra;
    sz[ra] += sz[rb];

    components--;
    maxSize = max(maxSize, sz[ra]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    components = n;
    maxSize = 1;
    for (int i = 1; i <= n; i++) {
        parent[i] = i;
        sz[i] = 1;
    }

    while (m--) {
        int a, b;
        cin >> a >> b;
        unite(a, b);
        cout << components << " " << maxSize << "\n";
    }

    return 0;
}
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Initialization | O(n) | O(n) |
| Each Query | O(alpha(n)) | - |
| Total | O(n + m * alpha(n)) | O(n) |

Where alpha(n) is the inverse Ackermann function, effectively O(1).

## Common Mistakes

1. **Forgetting path compression:** Without it, worst-case O(n) per find
2. **Not tracking max_size correctly:** Must update when merging, not when connecting same component
3. **Off-by-one in indexing:** Cities are 1-indexed
4. **Integer overflow:** Use `long long` for component sizes if they can exceed 2^31
5. **Printing inside loop:** Slow in Python; collect results and print once

## Key Takeaways

- Union-Find naturally tracks connected components
- Adding size tracking enables finding largest component
- Path compression + union by size gives near O(1) operations
- Maintain max incrementally rather than recomputing each query
