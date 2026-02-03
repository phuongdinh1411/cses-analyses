---
layout: simple
title: "Fixed Length Cycle Queries - Matrix Exponentiation Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_cycle_queries_analysis
difficulty: Hard
tags: [matrix-exponentiation, graph, binary-exponentiation, modular-arithmetic]
---

# Fixed Length Cycle Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph / Matrix Exponentiation |
| **Time Limit** | 1 second |
| **Key Technique** | Matrix Exponentiation, Binary Exponentiation |
| **CSES Link** | [Graph Paths I](https://cses.fi/problemset/task/1723) (similar concept) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how adjacency matrix powers count paths of fixed length
- [ ] Apply matrix exponentiation with binary exponentiation for O(log k) efficiency
- [ ] Implement modular matrix multiplication to handle large numbers
- [ ] Recognize that diagonal elements of A^k give cycle counts

---

## Problem Statement

**Problem:** Given a directed graph with n nodes and q queries, for each query find the number of cycles of exactly length k starting and ending at node a.

**Input:**
- Line 1: n (number of nodes), q (number of queries)
- Next n lines: n x n adjacency matrix (1 if edge exists, 0 otherwise)
- Next q lines: a, k (find cycles from node a back to a of length k)

**Output:**
- For each query, output the count of cycles modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 100
- 1 <= q <= 10^5
- 1 <= k <= 10^9
- 1 <= a <= n

### Example

```
Input:
3 2
0 1 0
0 0 1
1 0 0
1 3
2 2

Output:
1
0
```

**Explanation:**
- Query 1: From node 1, path 1->2->3->1 is the only cycle of length 3. Answer: 1
- Query 2: From node 2, no cycle of length 2 exists. Answer: 0

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we count paths of a specific length in a graph efficiently?

The fundamental insight is that **matrix multiplication naturally counts paths**. If A is the adjacency matrix, then A^k[i][j] gives the number of paths of exactly k edges from node i to node j. For cycles, we need A^k[a][a] - the diagonal element!

### Breaking Down the Problem

1. **What are we looking for?** Number of walks of length k that return to the starting node
2. **What information do we have?** The adjacency matrix and query parameters (start node, path length)
3. **What's the relationship?** A^k[a][a] directly gives the answer

### The Matrix Power Insight

Think of matrix multiplication like this:
- A[i][j] = 1 means there's a direct path from i to j
- (A^2)[i][j] counts 2-step paths: sum over all k of A[i][k] * A[k][j]
- This naturally extends: A^k counts k-step paths

---

## Solution 1: Brute Force (DFS)

### Idea

Recursively explore all possible paths of length k from the start node, counting those that return to start.

### Code

```python
def brute_force(n, adj, a, k):
    """
    Count cycles using DFS. TLE for large k.
    Time: O(n^k), Space: O(k)
    """
    MOD = 10**9 + 7

    def dfs(node, remaining):
        if remaining == 0:
            return 1 if node == a else 0

        count = 0
        for next_node in range(n):
            if adj[node][next_node]:
                count = (count + dfs(next_node, remaining - 1)) % MOD
        return count

    return dfs(a, k)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k) | Exponential branching at each step |
| Space | O(k) | Recursion depth |

### Why This Is Too Slow

With k up to 10^9, this is completely impractical. We need logarithmic complexity in k.

---

## Solution 2: Optimal - Matrix Exponentiation

### Key Insight

> **The Trick:** Raise the adjacency matrix to power k using binary exponentiation in O(n^3 log k) time.

### Why Matrix Powers Work

```
A^1[i][j] = number of 1-step paths from i to j
A^2[i][j] = number of 2-step paths from i to j
...
A^k[i][j] = number of k-step paths from i to j

For cycles: A^k[a][a] = cycles of length k starting at node a
```

### Binary Exponentiation

To compute A^k efficiently:
```
A^k = A^(k/2) * A^(k/2)           if k is even
A^k = A^((k-1)/2) * A^((k-1)/2) * A   if k is odd
```

This gives O(log k) matrix multiplications.

### Dry Run Example

Input: 3 nodes with cycle 1->2->3->1, Query: cycles of length 3 from node 1

```
Adjacency Matrix A:
    [0, 1, 0]
    [0, 0, 1]
    [1, 0, 0]

Computing A^3:

Step 1: A^1 = A (base case)

Step 2: A^2 = A * A
    A^2[0][0] = A[0][0]*A[0][0] + A[0][1]*A[1][0] + A[0][2]*A[2][0]
              = 0*0 + 1*0 + 0*1 = 0
    A^2[0][1] = 0*1 + 1*0 + 0*0 = 0
    A^2[0][2] = 0*0 + 1*1 + 0*0 = 1  (path 1->2->3)

    A^2 = [0, 0, 1]
          [1, 0, 0]
          [0, 1, 0]

Step 3: A^3 = A^2 * A
    A^3[0][0] = 0*0 + 0*0 + 1*1 = 1  (cycle 1->2->3->1)

    A^3 = [1, 0, 0]
          [0, 1, 0]
          [0, 0, 1]

Answer: A^3[0][0] = 1 cycle
```

### Visual Diagram

```
Graph:        1 -----> 2
              ^        |
              |        v
              +------- 3

Matrix A:     To: 1  2  3
         From 1: [0, 1, 0]
              2: [0, 0, 1]
              3: [1, 0, 0]

A^3 diagonal: [1, 1, 1]
              ^
              |
              Cycles of length 3 from each node
```

### Code (Python)

```python
def solve(n, adj, queries):
    """
    Matrix exponentiation solution for cycle counting.

    Time: O(n^3 * log(k) * q) - can optimize with caching
    Space: O(n^2)
    """
    MOD = 10**9 + 7

    def matrix_mult(A, B):
        """Multiply two n x n matrices with modular arithmetic."""
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
        return C

    def matrix_power(M, p):
        """Compute M^p using binary exponentiation."""
        # Initialize result as identity matrix
        result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        base = [row[:] for row in M]  # Copy matrix

        while p > 0:
            if p & 1:  # If p is odd
                result = matrix_mult(result, base)
            base = matrix_mult(base, base)
            p >>= 1

        return result

    results = []
    for a, k in queries:
        powered = matrix_power(adj, k)
        results.append(powered[a - 1][a - 1])  # 1-indexed to 0-indexed

    return results


# Main
def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0

    n, q = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    adj = []
    for i in range(n):
        row = [int(input_data[idx + j]) for j in range(n)]
        adj.append(row)
        idx += n

    queries = []
    for _ in range(q):
        a, k = int(input_data[idx]), int(input_data[idx + 1])
        queries.append((a, k))
        idx += 2

    for ans in solve(n, adj, queries):
        print(ans)


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;
int n;

typedef vector<vector<long long>> Matrix;

Matrix multiply(const Matrix& A, const Matrix& B) {
    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
            }
        }
    }
    return C;
}

Matrix matpow(Matrix M, long long p) {
    // Identity matrix
    Matrix result(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++) result[i][i] = 1;

    while (p > 0) {
        if (p & 1) result = multiply(result, M);
        M = multiply(M, M);
        p >>= 1;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> n >> q;

    Matrix adj(n, vector<long long>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> adj[i][j];
        }
    }

    while (q--) {
        int a;
        long long k;
        cin >> a >> k;
        a--;  // Convert to 0-indexed

        Matrix powered = matpow(adj, k);
        cout << powered[a][a] << "\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 log k) per query | Matrix multiplication is O(n^3), done O(log k) times |
| Space | O(n^2) | Store matrices |

---

## Common Mistakes

### Mistake 1: Forgetting Modular Arithmetic

```python
# WRONG - will overflow
C[i][j] = C[i][j] + A[i][k] * B[k][j]

# CORRECT
C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
```

**Problem:** Numbers can exceed 10^18 quickly, causing overflow.
**Fix:** Apply modulo at every multiplication step.

### Mistake 2: Wrong Identity Matrix Initialization

```python
# WRONG - initializing with zeros
result = [[0] * n for _ in range(n)]

# CORRECT - identity matrix has 1s on diagonal
result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
```

**Problem:** A^0 should be the identity matrix, not zeros.
**Fix:** Identity matrix: I[i][j] = 1 if i == j, else 0.

### Mistake 3: Off-by-One Index Error

```python
# WRONG - forgetting 1-indexed to 0-indexed conversion
return powered[a][a]

# CORRECT
return powered[a - 1][a - 1]
```

**Problem:** Input is 1-indexed, matrix is 0-indexed.
**Fix:** Always convert indices when reading input.

### Mistake 4: Modifying Original Matrix

```python
# WRONG - modifying original matrix
base = M

# CORRECT - create a copy
base = [row[:] for row in M]
```

**Problem:** Binary exponentiation squares the base matrix repeatedly.
**Fix:** Create a deep copy of the matrix.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| k = 1 (self-loop) | Self-loop at node 1, query (1, 1) | 1 | Direct edge from 1 to 1 |
| No outgoing edges | Isolated node, any k | 0 | No paths possible |
| k = 0 | Any node | 1 | Empty path (stay in place) |
| Large k | k = 10^9 | Depends | Binary exp handles large powers |
| Complete graph | All edges exist | n^(k-1) | Many paths exist |

---

## When to Use This Pattern

### Use Matrix Exponentiation When:
- Counting paths/cycles of specific length in graphs
- Computing Fibonacci or linear recurrences for large n
- State transitions that can be expressed as matrix multiplication
- k is very large (up to 10^18) but n is small (< 100)

### Don't Use When:
- n is large (> 500) - O(n^3) per multiplication is slow
- Only single query - simpler DP might suffice
- Need actual paths, not just counts
- Graph is sparse - adjacency list methods may be better

### Pattern Recognition Checklist:
- [ ] Counting fixed-length paths/walks? --> **Matrix exponentiation**
- [ ] Linear recurrence with large n? --> **Matrix exponentiation**
- [ ] Small state space (< 100), large iterations? --> **Matrix exponentiation**

---

## Related Problems

### Prerequisite Problems
| Problem | Why It Helps |
|---------|--------------|
| [Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html) | Core technique for fast powers |
| Matrix Multiplication basics | Foundation for this problem |

### Similar CSES Problems
| Problem | Key Difference |
|---------|----------------|
| [Graph Paths I](https://cses.fi/problemset/task/1723) | Count paths from 1 to n of length k |
| [Graph Paths II](https://cses.fi/problemset/task/1724) | Shortest path of exactly k edges |
| [Dice Probability](https://cses.fi/problemset/task/1725) | Matrix exp for probability |

### Harder Extensions
| Problem | New Concept |
|---------|-------------|
| Shortest path of exactly k edges | Min-plus matrix multiplication |
| Count paths with specific sum | 3D state in matrix |

---

## Key Takeaways

1. **The Core Idea:** A^k[i][j] counts k-length paths from i to j; diagonal gives cycles
2. **Time Optimization:** Binary exponentiation reduces O(k) multiplications to O(log k)
3. **Space Trade-off:** O(n^2) for matrices, which is acceptable for n <= 100
4. **Pattern:** Matrix exponentiation is the go-to technique for counting fixed-length paths

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement matrix multiplication with modular arithmetic
- [ ] Implement binary exponentiation for matrices
- [ ] Explain why A^k gives path counts
- [ ] Identify matrix exponentiation problems in contests

---

## Additional Resources

- [CP-Algorithms: Matrix Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CSES Graph Paths I](https://cses.fi/problemset/task/1723) - Path counting with matrix exponentiation
- [TopCoder: Matrix Exponentiation Tutorial](https://www.topcoder.com/thrive/articles/matrix-exponentiation)
