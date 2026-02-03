---
layout: simple
title: "Fixed Length Tour Queries - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_tour_queries_analysis
difficulty: Hard
tags: [graph, matrix-exponentiation, binary-exponentiation, dynamic-programming]
---

# Fixed Length Tour Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph Theory / Matrix Exponentiation |
| **Time Limit** | 1 second |
| **Key Technique** | Matrix Exponentiation with Binary Exponentiation |
| **CSES Link** | [Graph Paths I](https://cses.fi/problemset/task/1723) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the relationship between adjacency matrices and path/tour counting
- [ ] Apply matrix exponentiation to solve graph path counting problems
- [ ] Implement binary exponentiation for efficient matrix power computation
- [ ] Recognize when matrix exponentiation is applicable to graph problems

---

## Problem Statement

**Problem:** Given a directed graph with n nodes, answer q queries. For each query, determine if there exists a tour (cycle) of exactly length k that starts and ends at node a.

**Input:**
- Line 1: n q (number of nodes, number of queries)
- Next n lines: adjacency matrix (n x n, 0 or 1)
- Next q lines: a k (start node, tour length)

**Output:**
- For each query: 1 if tour exists, 0 otherwise

**Constraints:**
- 1 <= n <= 100
- 1 <= q <= 10^5
- 1 <= k <= 10^9
- 1 <= a <= n

### Example

```
Input:
3 2
0 1 1
1 0 1
1 1 0

Output:
1
1
```

**Explanation:**
- Query 1 (a=1, k=3): Tour 1->2->3->1 has length 3. Answer: 1
- Query 2 (a=2, k=2): Tour 2->3->2 has length 2. Answer: 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count paths of length k in a graph?

The fundamental insight is that **A^k[i][j] gives the number of paths of length k from node i to node j**, where A is the adjacency matrix. For tours (cycles), we need paths from node a back to itself, so we check A^k[a][a].

### Breaking Down the Problem

1. **What are we looking for?** Whether a path of length k exists from node a back to node a
2. **What information do we have?** Adjacency matrix and query parameters
3. **What's the relationship?** Matrix power A^k encodes all path counts of length k

### Why Matrix Multiplication Works

Consider multiplying A x A = A^2:
- A^2[i][j] = sum of A[i][l] * A[l][j] for all l
- This counts paths i -> l -> j (length 2) for all intermediate nodes l

By induction, A^k counts all paths of length k.

---

## Solution 1: Brute Force (DFS)

### Idea

Use DFS to explore all possible tours of length k starting from node a.

### Algorithm

1. Start DFS from node a with remaining length k
2. At each step, try all outgoing edges
3. If we return to a with exactly 0 remaining length, tour exists

### Code

```python
def solve_brute_force(n, adj, queries):
    """
    Brute force DFS solution.

    Time: O(q * n^k) - exponential in k
    Space: O(k) - recursion depth
    """
    def has_tour(start, k):
        def dfs(node, remaining):
            if remaining == 0:
                return node == start
            for next_node in range(n):
                if adj[node][next_node] and dfs(next_node, remaining - 1):
                    return True
            return False
        return dfs(start, k)

    results = []
    for a, k in queries:
        results.append(1 if has_tour(a - 1, k) else 0)
    return results
```

```cpp
#include <vector>
using namespace std;

class BruteForceSolution {
    int n;
    vector<vector<int>>& adj;

    bool dfs(int node, int start, int remaining) {
        if (remaining == 0) return node == start;
        for (int next = 0; next < n; next++) {
            if (adj[node][next] && dfs(next, start, remaining - 1)) {
                return true;
            }
        }
        return false;
    }

public:
    BruteForceSolution(int n, vector<vector<int>>& adj) : n(n), adj(adj) {}

    bool hasTour(int start, int k) {
        return dfs(start, start, k);
    }
};
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k) per query | Up to n choices at each of k steps |
| Space | O(k) | Recursion stack depth |

### Why This Works (But Is Slow)

Correctness is guaranteed because we exhaustively check all possible paths. However, with k up to 10^9, this is completely impractical.

---

## Solution 2: Matrix Exponentiation (Optimal)

### Key Insight

> **The Trick:** A^k[i][j] counts paths of length exactly k from i to j. Use binary exponentiation to compute A^k in O(n^3 log k) time.

### Algorithm

1. Represent the graph as an adjacency matrix A
2. For each query (a, k), compute A^k using binary exponentiation
3. Check if A^k[a-1][a-1] > 0 (tour exists)

### Binary Exponentiation Concept

```
A^13 = A^(1101 in binary)
     = A^8 * A^4 * A^1

Compute: A^1, A^2, A^4, A^8 by successive squaring
Then multiply only powers where bit is set
```

### Dry Run Example

Let's trace through with the example graph and query (a=1, k=3):

```
Adjacency Matrix A:
    [0 1 1]
A = [1 0 1]
    [1 1 0]

Step 1: Compute A^2 = A * A
    [2 1 1]
A^2=[1 2 1]    (each entry counts 2-step paths)
    [1 1 2]

Step 2: Compute A^3 = A^2 * A
    [2 3 3]
A^3=[3 2 3]
    [3 3 2]

Check A^3[0][0] = 2 > 0, so tour exists!

The 2 tours of length 3 from node 1:
  - 1 -> 2 -> 3 -> 1
  - 1 -> 3 -> 2 -> 1
```

### Visual Diagram

```
Graph:
    1 -----> 2
    ^\ ___/^|
    | X    ||
    |/ ----v|
    3 <-----+

A^k[i][j] = number of k-length paths from i to j

k=1: A^1     k=2: A^2     k=3: A^3
[0 1 1]     [2 1 1]      [2 3 3]
[1 0 1]     [1 2 1]      [3 2 3]
[1 1 0]     [1 1 2]      [3 3 2]

Diagonal elements = tours (cycles back to same node)
```

### Code

```python
def solve_optimal(n, adj, queries):
    """
    Matrix exponentiation solution.

    Time: O(n^3 * log(max_k) + q)
    Space: O(n^2)
    """
    def matrix_mult(A, B):
        """Multiply two n x n matrices."""
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
                # Keep only existence info (prevent overflow)
                C[i][j] = min(C[i][j], 1)
        return C

    def matrix_power(M, p):
        """Compute M^p using binary exponentiation."""
        # Identity matrix
        result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        base = [row[:] for row in M]  # Copy

        while p > 0:
            if p & 1:
                result = matrix_mult(result, base)
            base = matrix_mult(base, base)
            p >>= 1

        return result

    # Group queries by k value to avoid recomputation
    from collections import defaultdict
    k_to_queries = defaultdict(list)
    for idx, (a, k) in enumerate(queries):
        k_to_queries[k].append((idx, a))

    results = [0] * len(queries)
    for k, query_list in k_to_queries.items():
        Ak = matrix_power(adj, k)
        for idx, a in query_list:
            results[idx] = 1 if Ak[a-1][a-1] > 0 else 0

    return results


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().split()
    ptr = 0
    n, q = int(data[ptr]), int(data[ptr+1]); ptr += 2
    adj = [[int(data[ptr + i*n + j]) for j in range(n)] for i in range(n)]; ptr += n*n
    queries = [(int(data[ptr+2*i]), int(data[ptr+2*i+1])) for i in range(q)]
    for r in solve_optimal(n, adj, queries): print(r)
```

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<vector<long long>> Matrix;

class MatrixExponentiation {
    int n;

    Matrix multiply(const Matrix& A, const Matrix& B) {
        Matrix C(n, vector<long long>(n, 0));
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
                // Keep as boolean to prevent overflow
                C[i][j] = min(C[i][j], 1LL);
            }
        }
        return C;
    }

public:
    MatrixExponentiation(int n) : n(n) {}

    Matrix power(Matrix& M, long long p) {
        // Identity matrix
        Matrix result(n, vector<long long>(n, 0));
        for (int i = 0; i < n; i++) result[i][i] = 1;

        Matrix base = M;
        while (p > 0) {
            if (p & 1) result = multiply(result, base);
            base = multiply(base, base);
            p >>= 1;
        }
        return result;
    }
};

int main() {
    ios_base::sync_with_stdio(false); cin.tie(nullptr);
    int n, q; cin >> n >> q;
    Matrix adj(n, vector<long long>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) cin >> adj[i][j];

    MatrixExponentiation solver(n);
    map<long long, vector<pair<int, int>>> queries_by_k;
    for (int i = 0; i < q; i++) {
        int a; long long k; cin >> a >> k;
        queries_by_k[k].push_back({i, a});
    }
    vector<int> results(q);
    for (auto& [k, qlist] : queries_by_k) {
        Matrix Ak = solver.power(adj, k);
        for (auto& [idx, a] : qlist)
            results[idx] = Ak[a-1][a-1] > 0 ? 1 : 0;
    }
    for (int r : results) cout << r << "\n";
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 log k) | Matrix multiplication is O(n^3), log k multiplications |
| Space | O(n^2) | Store matrices |

---

## Common Mistakes

### Mistake 1: Integer Overflow

```python
# WRONG - values can overflow
C[i][j] += A[i][k] * B[k][j]

# CORRECT - cap values for existence check
C[i][j] += A[i][k] * B[k][j]
C[i][j] = min(C[i][j], 1)  # Only need to know if > 0
```

**Problem:** Path counts grow exponentially; can overflow even 64-bit integers.
**Fix:** For existence queries, cap values at 1. For count queries, use modular arithmetic.

### Mistake 2: Wrong Base Case for k=0

```python
# WRONG - what's A^0?
if k == 0:
    return True  # Always a tour?

# CORRECT - A^0 = Identity matrix
# A^0[i][i] = 1 (path of length 0 from i to i exists)
```

**Problem:** Need to handle k=0 as identity matrix case.
**Fix:** Initialize result as identity matrix in binary exponentiation.

### Mistake 3: 1-indexed vs 0-indexed Confusion

```python
# WRONG
return Ak[a][a] > 0  # a is 1-indexed!

# CORRECT
return Ak[a-1][a-1] > 0
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Self-loop, k=1 | adj[0][0]=1, query(1,1) | 1 | Direct self-loop |
| No self-loop, k=1 | adj[0][0]=0, query(1,1) | 0 | No single-step tour |
| Disconnected node | No edges from node a | 0 | No outgoing paths |
| k=0 | query(a, 0) | 1 | Empty tour exists |
| Large k, small cycle | k=10^9, cycle length 2 | 1 | Use mod cycle length |

---

## When to Use This Pattern

### Use Matrix Exponentiation When:
- Counting paths of fixed length in a graph
- k is very large (up to 10^9 or more)
- Graph is relatively small (n <= 100-200)
- Need to answer many queries for same graph

### Don't Use When:
- k is small (direct DP is simpler)
- Graph is too large (n > 500, O(n^3) too slow)
- Looking for shortest path (use BFS/Dijkstra)
- Need actual path, not just count/existence

### Pattern Recognition Checklist:
- [ ] Fixed-length path counting? -> **Matrix exponentiation**
- [ ] Large exponent (k > 10^6)? -> **Binary exponentiation required**
- [ ] Small graph (n <= 100)? -> **Matrix approach feasible**
- [ ] Multiple queries, same graph? -> **Precompute matrix powers**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html) | Core technique for fast powers |
| [Round Trip](https://cses.fi/problemset/task/1669) | Basic cycle detection |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Graph Paths I](https://cses.fi/problemset/task/1723) | Count paths (not just existence) with modular arithmetic |
| [Graph Paths II](https://cses.fi/problemset/task/1724) | Shortest path of exactly k edges |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Hamiltonian Flights](https://cses.fi/problemset/task/1690) | Bitmask DP for Hamiltonian paths |
| [Knight's Tour](https://cses.fi/problemset/task/1689) | Tour with specific movement rules |

---

## Key Takeaways

1. **The Core Idea:** A^k[i][j] counts length-k paths from i to j
2. **Time Optimization:** Binary exponentiation reduces O(k) to O(log k) matrix multiplications
3. **Space Trade-off:** O(n^2) space for matrix enables O(n^3 log k) time
4. **Pattern:** Matrix exponentiation for path counting in small, dense graphs

**Practice Checklist:** Before moving on, make sure you can explain why A^k counts paths, implement binary exponentiation for matrices, handle overflow, and identify when this pattern applies.

**Resources:** [CP-Algorithms: Matrix Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html) | [CSES Graph Paths I](https://cses.fi/problemset/task/1723)
