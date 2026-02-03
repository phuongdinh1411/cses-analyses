---
layout: simple
title: "Hamiltonian Flights - Bitmask DP Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_hamiltonian_cycle_queries_analysis
difficulty: Hard
tags: [bitmask-dp, graph, hamiltonian-path, np-hard]
prerequisites: [graph_basics, dynamic_programming, bit_manipulation]
---

# Hamiltonian Flights

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Bitmask DP / Graph Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Bitmask DP with State Compression |
| **CSES Link** | [Hamiltonian Flights](https://cses.fi/problemset/task/1690) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the Hamiltonian path/cycle problem and its NP-hard nature
- [ ] Apply bitmask DP to represent visited vertex sets efficiently
- [ ] Design state transitions for path-counting problems
- [ ] Recognize when O(2^n * n^2) is acceptable given small n constraints

---

## Problem Statement

**Problem:** Count the number of distinct routes from city 1 to city n that visit every city exactly once.

**Input:**
- Line 1: n (cities) and m (flights)
- Next m lines: a b (flight from city a to city b)

**Output:**
- Number of routes modulo 10^9 + 7

**Constraints:**
- 2 <= n <= 20
- 1 <= m <= n^2
- 1 <= a, b <= n

### Example

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
```

**Explanation:** The two valid Hamiltonian paths from 1 to 4 are:
- Path 1: 1 -> 2 -> 3 -> 4
- Path 2: 1 -> 3 -> 2 -> 4

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently track which cities have been visited?

The constraint n <= 20 is a strong hint for bitmask DP. With 20 cities, we have 2^20 = ~1M possible subsets, which is manageable. Each subset can be represented as a binary number where bit i indicates whether city i has been visited.

### Breaking Down the Problem

1. **What are we looking for?** Number of paths visiting all n cities exactly once, starting at 1 and ending at n.
2. **What information do we have?** Directed edges between cities.
3. **What's the relationship?** We need to track both "which cities visited" AND "where we currently are."

### Analogy

Think of this like a delivery truck that must visit every house in a neighborhood exactly once. The bitmask is like a checklist of houses visited, and the current position tells us where the truck is now.

---

## Solution 1: Brute Force (DFS)

### Idea

Try all possible orderings using DFS and count valid Hamiltonian paths.

### Algorithm

1. Start DFS from city 1 with only city 1 visited
2. At each step, try all unvisited neighbors
3. If we reach city n with all cities visited, count it

### Code

```python
def solve_brute_force(n, edges):
    """
    Brute force DFS solution.

    Time: O(n! * n)
    Space: O(n)
    """
    MOD = 10**9 + 7
    graph = [[] for _ in range(n + 1)]
    for a, b in edges:
        graph[a].append(b)

    def dfs(node, visited, count):
        if count == n:
            return 1 if node == n else 0

        total = 0
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                total = (total + dfs(neighbor, visited, count + 1)) % MOD
                visited.remove(neighbor)
        return total

    visited = {1}
    return dfs(1, visited, 1)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * n) | Up to n! paths, each taking O(n) to verify |
| Space | O(n) | Recursion depth and visited set |

### Why This Works (But Is Slow)

Correct because it explores all possibilities. Too slow for n = 20 since 20! is astronomically large.

---

## Solution 2: Bitmask DP (Optimal)

### Key Insight

> **The Trick:** Represent the set of visited cities as a bitmask, and track counts for each (mask, current_city) pair.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[mask][i]` | Number of paths that have visited exactly the cities in `mask` and currently end at city `i` |

**In plain English:** "How many ways can we reach city i, having visited the exact set of cities represented by mask?"

### State Transition

```
dp[new_mask][j] += dp[mask][i]  for each edge (i -> j) where j not in mask
where new_mask = mask | (1 << j)
```

**Why?** If we're at city i with visited set mask, and there's an edge to unvisited city j, we can extend our path to j.

### Base Case

| Case | Value | Reason |
|------|-------|--------|
| `dp[1][0]` | 1 | Start at city 1 (bit 0 set), one way to be there initially |

### Algorithm

1. Initialize dp[1][0] = 1 (at city 1, only city 1 visited)
2. Iterate through all masks in increasing order
3. For each (mask, i) with dp[mask][i] > 0, extend to neighbors
4. Answer is dp[(1 << n) - 1][n - 1] (all visited, at city n)

### Dry Run Example

Input: n = 4, edges = [(1,2), (1,3), (2,3), (2,4), (3,2), (3,4)]

Using 0-indexed cities internally:

```
Initial: dp[0001][0] = 1  (at city 0, visited {0})

Process mask = 0001 (binary), city 0:
  Edge 0->1: dp[0011][1] += 1  (visited {0,1}, at city 1)
  Edge 0->2: dp[0101][2] += 1  (visited {0,2}, at city 2)

Process mask = 0011, city 1:
  Edge 1->2: dp[0111][2] += 1  (visited {0,1,2}, at city 2)
  Edge 1->3: dp[1011][3] += 1  (visited {0,1,3}, at city 3) -- INVALID END

Process mask = 0101, city 2:
  Edge 2->1: dp[0111][1] += 1  (visited {0,1,2}, at city 1)

Process mask = 0111, city 1:
  Edge 1->3: dp[1111][3] += 1  (visited {0,1,2,3}, at city 3)

Process mask = 0111, city 2:
  Edge 2->3: dp[1111][3] += 1  (visited {0,1,2,3}, at city 3)

Final: dp[1111][3] = 2  (two paths reaching city 3 with all visited)
```

### Visual Diagram

```
Cities: 0 -- 1 -- 2 -- 3  (0-indexed)

Path 1: 0 -> 1 -> 2 -> 3
        mask progression: 0001 -> 0011 -> 0111 -> 1111

Path 2: 0 -> 2 -> 1 -> 3
        mask progression: 0001 -> 0101 -> 0111 -> 1111
```

### Code

```python
def solve_hamiltonian(n, m, edges):
    """
    Bitmask DP solution for counting Hamiltonian paths.

    Time: O(2^n * n^2)
    Space: O(2^n * n)
    """
    MOD = 10**9 + 7

    # Build adjacency list (0-indexed)
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a - 1].append(b - 1)

    # dp[mask][i] = number of ways to reach city i with visited set = mask
    dp = [[0] * n for _ in range(1 << n)]
    dp[1][0] = 1  # Start at city 0, only city 0 visited

    # Process all masks in order
    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] == 0:
                continue
            if not (mask & (1 << i)):  # City i must be in mask
                continue

            # Try extending to each neighbor
            for j in graph[i]:
                if mask & (1 << j):  # Skip if already visited
                    continue
                new_mask = mask | (1 << j)
                dp[new_mask][j] = (dp[new_mask][j] + dp[mask][i]) % MOD

    # Answer: all cities visited, ending at city n-1
    full_mask = (1 << n) - 1
    return dp[full_mask][n - 1]


# Read input and solve
def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    n, m = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2
    edges = []
    for _ in range(m):
        a, b = int(input_data[idx]), int(input_data[idx + 1])
        edges.append((a, b))
        idx += 2
    print(solve_hamiltonian(n, m, edges))

if __name__ == "__main__":
    main()
```

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> graph(n);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        graph[a - 1].push_back(b - 1);
    }

    // dp[mask][i] = ways to reach city i with visited set = mask
    vector<vector<long long>> dp(1 << n, vector<long long>(n, 0));
    dp[1][0] = 1;

    for (int mask = 1; mask < (1 << n); mask++) {
        for (int i = 0; i < n; i++) {
            if (dp[mask][i] == 0) continue;
            if (!(mask & (1 << i))) continue;

            for (int j : graph[i]) {
                if (mask & (1 << j)) continue;
                int new_mask = mask | (1 << j);
                dp[new_mask][j] = (dp[new_mask][j] + dp[mask][i]) % MOD;
            }
        }
    }

    int full_mask = (1 << n) - 1;
    cout << dp[full_mask][n - 1] << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n^2) | 2^n masks, n cities per mask, up to n neighbors |
| Space | O(2^n * n) | DP table storing all states |

---

## Common Mistakes

### Mistake 1: Wrong Base Case

```python
# WRONG: Starting from all cities
for i in range(n):
    dp[1 << i][i] = 1

# CORRECT: Must start from city 0 (city 1 in 1-indexed)
dp[1][0] = 1
```

**Problem:** The path must start at city 1, not any city.
**Fix:** Only initialize the starting city.

### Mistake 2: Checking Visited Incorrectly

```python
# WRONG: Using subtraction
if mask - (1 << j) >= 0:  # Doesn't check if j is actually in mask

# CORRECT: Using bitwise AND
if mask & (1 << j):  # True only if j is in mask
```

**Problem:** Subtraction doesn't properly check set membership.
**Fix:** Use bitwise AND for membership testing.

### Mistake 3: Forgetting Modulo

```python
# WRONG: No modulo, causes overflow
dp[new_mask][j] += dp[mask][i]

# CORRECT: Apply modulo
dp[new_mask][j] = (dp[new_mask][j] + dp[mask][i]) % MOD
```

**Problem:** Answer can be huge, will overflow without modulo.
**Fix:** Apply MOD at each addition.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum n | n=2, 1->2 exists | 1 | Single direct edge |
| No path | n=2, no 1->2 edge | 0 | Cannot reach destination |
| Single path | Linear graph 1->2->3->4 | 1 | Only one valid ordering |
| Complete graph | All n*(n-1) edges | (n-2)! | Any middle ordering works |
| Disconnected | No path to n | 0 | Cannot complete tour |

---

## When to Use This Pattern

### Use Bitmask DP When:
- n is small (typically n <= 20-22)
- You need to track "which items have been selected/visited"
- Subsets of items matter, not just their count
- Problem involves Hamiltonian paths/cycles, TSP variants

### Don't Use When:
- n is large (bitmask won't fit in memory)
- Only count matters, not specific items (use combinatorics)
- Problem has polynomial-time solution

### Pattern Recognition Checklist:
- [ ] Small n constraint (n <= 20)? -> **Consider bitmask DP**
- [ ] Need to visit all nodes exactly once? -> **Hamiltonian path pattern**
- [ ] Need to track subset of items? -> **Bitmask state**
- [ ] Order within subset matters? -> **Add position to state**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [CSES Counting Paths](https://cses.fi/problemset/task/1638) | Basic path counting DP |
| [CSES Grid Paths](https://cses.fi/problemset/task/1639) | 2D grid path counting |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES Round Trip II](https://cses.fi/problemset/task/1678) | Directed cycle finding |
| [CSES Shortest Routes I](https://cses.fi/problemset/task/1671) | Dijkstra, different goal |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES Hamiltonian Cycle](https://cses.fi/problemset/task/XXXX) | Must return to start |
| [Traveling Salesman (TSP)](https://en.wikipedia.org/wiki/Travelling_salesman_problem) | Minimum weight Hamiltonian cycle |
| [LeetCode Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | BFS + bitmask |

---

## Key Takeaways

1. **The Core Idea:** Use bitmask to represent visited set, track (mask, current_position) pairs
2. **Time Optimization:** O(n!) brute force -> O(2^n * n^2) bitmask DP
3. **Space Trade-off:** O(2^n * n) space for exponential time savings
4. **Pattern:** Classic bitmask DP for small-n subset problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why bitmask DP is O(2^n * n^2) and when it's applicable
- [ ] Write the state transition without looking at notes
- [ ] Identify the base case and final answer location
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Bitmask DP](https://cp-algorithms.com/algebra/all-submasks.html)
- [CSES Problem Set](https://cses.fi/problemset/)
- [Hamiltonian Path - Wikipedia](https://en.wikipedia.org/wiki/Hamiltonian_path)
