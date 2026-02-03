---
layout: simple
title: "Hamiltonian Flights"
difficulty: Hard
tags: [graph, bitmask-dp, hamiltonian-path, tsp]
cses_link: https://cses.fi/problemset/task/1690
permalink: /problem_soulutions/graph_algorithms/hamiltonian_flights_analysis
---

# Hamiltonian Flights

## Problem Overview

| Attribute       | Details                                           |
|-----------------|---------------------------------------------------|
| Problem         | Count Hamiltonian paths from city 1 to city n     |
| Difficulty      | Hard                                              |
| Key Technique   | Bitmask Dynamic Programming                       |
| Time Complexity | O(2^n * n * m) or O(2^n * n^2)                   |
| Constraint      | n <= 20 (exponential in n)                       |

## Learning Goals

After completing this problem, you will understand:

1. **Bitmask DP** - Using integers as sets to represent visited states
2. **Hamiltonian Path Counting** - Counting paths that visit every vertex exactly once
3. **Subset Representation** - Encoding subsets as binary numbers for efficient operations
4. **State Space Design** - Designing DP states for graph traversal problems

## Problem Statement

You are given n cities and m one-way flights between them. Your task is to count the number of routes from city 1 to city n that visit **every city exactly once**.

**Input:**
- First line: n (cities) and m (flights)
- Next m lines: each contains a b, meaning a flight from city a to city b

**Output:**
- Number of valid routes modulo 10^9 + 7

**Constraints:**
- 2 <= n <= 20
- 1 <= m <= n^2
- 1 <= a, b <= n

**Example:**
```
Input:
4 6
1 2
1 3
2 3
2 4
3 2
3 4

Output:
2

Explanation:
Valid routes visiting all cities exactly once:
1 -> 2 -> 3 -> 4
1 -> 3 -> 2 -> 4
```

## Key Insight

The crucial observation is that to count Hamiltonian paths, we need to track:
1. **Which cities have been visited** - to ensure each city is visited exactly once
2. **Current position** - to know where we can go next

This leads to the state design: **(current city, set of visited cities)**

Since n <= 20, we can represent the visited set as a **bitmask** - an integer where bit i is 1 if city i has been visited.

```
Example: n = 4
mask = 0101 (binary) = 5 (decimal)
Means: cities 0 and 2 are visited, cities 1 and 3 are not
```

## DP State Definition

```
dp[mask][v] = number of paths ending at city v having visited exactly
              the cities represented by the bits set in mask
```

**State interpretation:**
- `mask`: bitmask representing which cities have been visited
- `v`: current city (0-indexed, so city 1 becomes index 0)
- `dp[mask][v]`: count of valid partial paths

**Important:** City v must be included in mask (bit v must be set).

## State Transition

For each state `dp[mask][v]` with a positive count, we extend the path by considering all outgoing edges from v:

```
For each edge v -> u where u is NOT in mask:
    dp[mask | (1 << u)][u] += dp[mask][v]
```

**Breakdown:**
- `v -> u`: there exists a flight from city v to city u
- `u not in mask`: city u has not been visited yet, checked by `(mask & (1 << u)) == 0`
- `mask | (1 << u)`: new mask with city u also marked as visited
- We add the count because we are counting paths

## Base Case and Answer

**Base Case:**
```
dp[1][0] = 1
```
- Start at city 1 (index 0)
- Only city 1 is visited (mask = 1 = binary 0001)
- There is exactly 1 way to be at start

**Answer:**
```
dp[(1 << n) - 1][n - 1]
```
- `(1 << n) - 1`: all n cities visited (all bits set)
- `n - 1`: at city n (index n-1)

## Visual Diagram: State Transitions

```
Example: n = 4, edges: 1->2, 1->3, 2->3, 2->4, 3->2, 3->4

Cities: 1, 2, 3, 4 (1-indexed) = 0, 1, 2, 3 (0-indexed in code)

State transitions (showing mask in binary):

Level 0 (Start):
    dp[0001][0] = 1    (at city 1, visited {1})
         |
         v
Level 1:
    dp[0011][1] = 1    (at city 2, visited {1,2})  via edge 1->2
    dp[0101][2] = 1    (at city 3, visited {1,3})  via edge 1->3
         |                   |
         v                   v
Level 2:
    dp[0111][2] = 1    (at city 3, visited {1,2,3})  via 1->2->3
    dp[1011][3] = 1    (at city 4, visited {1,2,4})  via 1->2->4 (dead end!)
    dp[0111][1] = 1    (at city 2, visited {1,2,3})  via 1->3->2
    dp[1101][3] = 1    (at city 4, visited {1,3,4})  via 1->3->4 (dead end!)
         |                   |
         v                   v
Level 3:
    dp[1111][3] = 1    (at city 4, visited all)  via 1->2->3->4
    dp[1111][3] += 1   (at city 4, visited all)  via 1->3->2->4

Final: dp[1111][3] = 2

Answer: 2 routes
```

## Dry Run with Small Example

**Input:** n=3, edges: 1->2, 2->3, 1->3, 3->2

```
Step 1: Initialize
  dp[001][0] = 1  (at city 1, visited {1})

Step 2: Process mask=001 (only city 1 visited)
  From dp[001][0]=1:
    Edge 1->2: dp[011][1] += 1  -> dp[011][1] = 1
    Edge 1->3: dp[101][2] += 1  -> dp[101][2] = 1

Step 3: Process mask=011 (cities 1,2 visited)
  From dp[011][1]=1:
    Edge 2->3: dp[111][2] += 1  -> dp[111][2] = 1

Step 4: Process mask=101 (cities 1,3 visited)
  From dp[101][2]=1:
    Edge 3->2: dp[111][1] += 1  -> dp[111][1] = 1
    (Note: this ends at city 2, not city 3, so it won't contribute)

Step 5: Check answer
  dp[111][2] = 1 (all visited, at city 3)

Answer: 1
```

## Python Implementation

```python
def count_hamiltonian_paths(n: int, edges: list[tuple[int, int]]) -> int:
    """
    Count Hamiltonian paths from city 1 to city n.

    Args:
        n: number of cities (1-indexed in problem, 0-indexed internally)
        edges: list of (a, b) representing flight from city a to city b (1-indexed)

    Returns:
        Number of valid routes modulo 10^9 + 7
    """
    MOD = 10**9 + 7

    # Build adjacency list (convert to 0-indexed)
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a - 1].append(b - 1)

    # dp[mask][v] = number of paths ending at v with visited set = mask
    dp = [[0] * n for _ in range(1 << n)]

    # Base case: start at city 0 (city 1 in problem), only city 0 visited
    dp[1][0] = 1

    # Iterate over all masks in increasing order
    for mask in range(1, 1 << n):
        for v in range(n):
            # Skip if city v is not in current mask
            if not (mask & (1 << v)):
                continue

            # Skip if no paths reach this state
            if dp[mask][v] == 0:
                continue

            # Try extending path to unvisited neighbors
            for u in adj[v]:
                # Check if city u is not visited
                if not (mask & (1 << u)):
                    new_mask = mask | (1 << u)
                    dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD

    # Answer: all cities visited, at city n-1 (city n in problem)
    full_mask = (1 << n) - 1
    return dp[full_mask][n - 1]


# Example usage
if __name__ == "__main__":
    n, m = 4, 6
    edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 2), (3, 4)]
    print(count_hamiltonian_paths(n, edges))  # Output: 2
```

## C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    // Build adjacency list (0-indexed)
    vector<vector<int>> adj(n);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a - 1].push_back(b - 1);
    }

    // dp[mask][v] = number of paths ending at v with visited set = mask
    vector<vector<long long>> dp(1 << n, vector<long long>(n, 0));

    // Base case: at city 0, only city 0 visited
    dp[1][0] = 1;

    // Iterate over all masks
    for (int mask = 1; mask < (1 << n); mask++) {
        for (int v = 0; v < n; v++) {
            // Skip if city v is not in current mask
            if (!(mask & (1 << v))) continue;

            // Skip if no paths reach this state
            if (dp[mask][v] == 0) continue;

            // Try extending to unvisited neighbors
            for (int u : adj[v]) {
                // Check if city u is not visited
                if (!(mask & (1 << u))) {
                    int new_mask = mask | (1 << u);
                    dp[new_mask][u] = (dp[new_mask][u] + dp[mask][v]) % MOD;
                }
            }
        }
    }

    // Answer: all cities visited, at city n-1
    int full_mask = (1 << n) - 1;
    cout << dp[full_mask][n - 1] << "\n";

    return 0;
}
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Wrong bit check | Using `mask & (1 << u) == 0` | Use `!(mask & (1 << u))` or `(mask & (1 << u)) == 0` with parentheses |
| Forgetting modulo | Integer overflow | Apply `% MOD` after each addition |
| 1-indexed vs 0-indexed | Off-by-one errors | Convert input to 0-indexed consistently |
| Wrong base case | Missing starting state | `dp[1][0] = 1` (not `dp[0][0]`) |
| Wrong final state | Checking wrong mask/city | `dp[(1<<n)-1][n-1]` not `dp[(1<<n)-1][0]` |
| Iterating invalid states | Processing when v not in mask | Always check `if (mask & (1 << v))` |

**Bit Operation Pitfalls:**

```python
# WRONG: Operator precedence issue
if mask & (1 << u) == 0:    # Evaluates as: mask & ((1 << u) == 0)

# CORRECT: Use parentheses or negation
if (mask & (1 << u)) == 0:  # Explicit parentheses
if not (mask & (1 << u)):   # Pythonic way
```

## Time and Space Complexity

**Time Complexity: O(2^n * n * m)** or equivalently **O(2^n * n^2)**
- 2^n possible masks (subsets of cities)
- For each mask, we iterate over n cities
- For each city, we check up to m edges (or n neighbors)

**Space Complexity: O(2^n * n)**
- DP table has 2^n * n entries
- Each entry is a single integer

**Why n <= 20?**
- 2^20 = 1,048,576 (about 1 million)
- 2^20 * 20 = ~20 million states
- This is manageable within typical time/memory limits
- For n = 25: 2^25 = 33 million - too slow
- For n = 30: 2^30 = 1 billion - way too slow

## Space Optimization (Optional)

Since we process masks in increasing order, we only need the current row:

```python
# Memory-optimized version (harder to implement correctly)
# Process masks by number of bits set (popcount)
for num_bits in range(1, n + 1):
    for mask in range(1 << n):
        if bin(mask).count('1') == num_bits:
            # Process this mask
            pass
```

However, the standard O(2^n * n) space is usually acceptable for n <= 20.

## Related Problems

| Problem | Similarity |
|---------|------------|
| Traveling Salesman Problem (TSP) | Same DP structure, but minimize cost instead of count |
| CSES - Elevator Rides | Bitmask DP with different state meaning |
| CSES - Counting Tilings | Different application of bitmask DP |
| LeetCode 847 - Shortest Path Visiting All Nodes | BFS version, minimize steps |

## Summary

1. **State**: `dp[mask][v]` = paths ending at v having visited cities in mask
2. **Transition**: `dp[mask | (1<<u)][u] += dp[mask][v]` for edge v->u, u not in mask
3. **Base**: `dp[1][0] = 1`
4. **Answer**: `dp[(1<<n)-1][n-1]`
5. **Complexity**: O(2^n * n^2) time, O(2^n * n) space
6. **Constraint**: Only works for n <= 20 due to exponential complexity
