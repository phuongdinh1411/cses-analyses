---
layout: simple
title: "Fixed Length Circuit Queries - Matrix Exponentiation Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_circuit_queries_analysis
difficulty: Hard
tags: [matrix-exponentiation, graph, binary-exponentiation, modular-arithmetic]
prerequisites: [binary-exponentiation, matrix-multiplication]
---

# Fixed Length Circuit Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph / Matrix Exponentiation |
| **Time Limit** | 1 second |
| **Key Technique** | Matrix Exponentiation with Binary Exponentiation |
| **CSES Link** | [Graph Paths II](https://cses.fi/problemset/task/1724) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand that adjacency matrix powers count paths of specific lengths
- [ ] Implement matrix multiplication with modular arithmetic
- [ ] Apply binary exponentiation to compute matrix powers in O(log k) time
- [ ] Recognize when matrix exponentiation applies to counting problems

---

## Problem Statement

**Problem:** Given a directed graph with n nodes, answer q queries. For each query, find the number of circuits (closed walks) of exactly length k starting and ending at node a.

**Input:**
- Line 1: n (number of nodes), q (number of queries)
- Next n lines: n x n adjacency matrix (1 if edge exists, 0 otherwise)
- Next q lines: a k (find circuits from node a of length k)

**Output:**
- For each query, output the count modulo 10^9 + 7

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
- Query 1: From node 1 with length 3, the path 1->2->3->1 is the only circuit. Answer: 1
- Query 2: From node 2 with length 2, no circuit exists (2->3->1 ends at 1, not 2). Answer: 0

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we count paths of length k efficiently without enumerating all paths?

The fundamental insight is from linear algebra: if A is the adjacency matrix of a graph, then A^k[i][j] gives the number of paths of length k from node i to node j. For circuits starting and ending at node a, we need A^k[a][a].

### Breaking Down the Problem

1. **What are we looking for?** Number of walks of exactly length k that start and end at the same node
2. **What information do we have?** The graph structure (adjacency matrix) and query parameters
3. **What's the relationship?** A^k[a][a] = count of circuits of length k from node a

### Why Does Matrix Power Work?

Consider a path of length 2 from i to j. It goes through some intermediate node m:
- Number of paths: sum over all m of (paths from i to m) * (paths from m to j)
- This is exactly how matrix multiplication works: (A*A)[i][j] = sum(A[i][m] * A[m][j])

By induction, A^k[i][j] counts all paths of length k from i to j.

---

## Solution 1: Brute Force DFS

### Idea

Enumerate all possible paths of length k starting from node a using DFS, counting those that return to a.

### Code

```python
def brute_force(n, adj, queries):
    """
    DFS enumeration of all paths.

    Time: O(n^k * q) - exponential in k
    Space: O(k) - recursion depth
    """
    MOD = 10**9 + 7

    def count_circuits(start, length):
        def dfs(node, remaining):
            if remaining == 0:
                return 1 if node == start else 0
            total = 0
            for neighbor in range(n):
                if adj[node][neighbor]:
                    total = (total + dfs(neighbor, remaining - 1)) % MOD
            return total
        return dfs(start, length)

    return [count_circuits(a - 1, k) for a, k in queries]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k * q) | Up to n choices at each of k steps |
| Space | O(k) | Recursion stack depth |

### Why This Is Too Slow

With k up to 10^9, this approach is completely infeasible. We need a way to "skip" the enumeration.

---

## Solution 2: Matrix Exponentiation (Optimal)

### Key Insight

> **The Trick:** Use binary exponentiation to compute A^k in O(n^3 * log k) time instead of O(n^3 * k).

Binary exponentiation exploits: A^k = (A^(k/2))^2 if k is even, or A * A^(k-1) if k is odd.

### Algorithm

1. Convert adjacency matrix to working matrix
2. Use binary exponentiation to compute A^k
3. Return the diagonal entry A^k[a-1][a-1] for each query

### Dry Run Example

Let's trace through with the example: n=3, query (1, 3)

```
Adjacency matrix A:
    0  1  2
0 [ 0  1  0 ]    Node 0 -> Node 1
1 [ 0  0  1 ]    Node 1 -> Node 2
2 [ 1  0  0 ]    Node 2 -> Node 0

Computing A^3 using binary exponentiation:

k = 3 (binary: 11)

Step 1: k=3 is odd, result = result * base
  result = I * A = A
  k = 2, base = A * A = A^2

  A^2 calculation:
  A^2[0][0] = A[0][0]*A[0][0] + A[0][1]*A[1][0] + A[0][2]*A[2][0] = 0
  A^2[0][1] = A[0][0]*A[0][1] + A[0][1]*A[1][1] + A[0][2]*A[2][1] = 0
  A^2[0][2] = A[0][0]*A[0][2] + A[0][1]*A[1][2] + A[0][2]*A[2][2] = 1
  ...

  A^2 = [ 0  0  1 ]
        [ 1  0  0 ]
        [ 0  1  0 ]

Step 2: k=2 is even
  k = 1, base = A^2 * A^2 = A^4

Step 3: k=1 is odd, result = result * base
  result = A * A^4 = A^5? No wait...

Let me redo more carefully:

Initial: result = I (identity), base = A, k = 3

Iteration 1: k=3 (odd)
  result = I * A = A
  base = A * A = A^2
  k = 3 // 2 = 1

Iteration 2: k=1 (odd)
  result = A * A^2 = A^3
  base = A^2 * A^2 = A^4
  k = 1 // 2 = 0

Final: result = A^3

A^3 = [ 1  0  0 ]
      [ 0  1  0 ]
      [ 0  0  1 ]

A^3[0][0] = 1 (circuits of length 3 from node 1)
```

### Visual Diagram

```
Graph structure:        Path enumeration for k=3 from node 1:

    1 -----> 2              1 -> 2 -> 3 -> 1  (returns to 1)
    ^        |
    |        v         Only 1 circuit exists
    +------- 3

Matrix Power Intuition:
A^1[i][j] = direct edges from i to j
A^2[i][j] = paths of length 2 (through any intermediate)
A^3[i][j] = paths of length 3
...
A^k[i][j] = paths of length k
```

### Code

```python
def matrix_exponentiation(n, adj, queries):
    """
    Optimal solution using matrix exponentiation.

    Time: O(n^3 * log(max_k) + q)
    Space: O(n^2)
    """
    MOD = 10**9 + 7

    def mat_mult(A, B):
        """Multiply two n x n matrices."""
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                if A[i][k] == 0:
                    continue
                for j in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
        return C

    def mat_pow(M, p):
        """Compute M^p using binary exponentiation."""
        # Initialize result as identity matrix
        result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        base = [row[:] for row in M]

        while p > 0:
            if p & 1:
                result = mat_mult(result, base)
            base = mat_mult(base, base)
            p >>= 1

        return result

    results = []
    for a, k in queries:
        powered = mat_pow(adj, k)
        results.append(powered[a - 1][a - 1])

    return results
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 log k * q) | Matrix multiply is O(n^3), log k iterations per query |
| Space | O(n^2) | Store matrices |

---

## Common Mistakes

### Mistake 1: Not Using Modular Arithmetic

```python
# WRONG - integer overflow for large k
C[i][j] = C[i][j] + A[i][k] * B[k][j]

# CORRECT
C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
```

**Problem:** Numbers grow exponentially; 64-bit integers overflow.
**Fix:** Apply modulo at every multiplication step.

### Mistake 2: Wrong Identity Matrix Initialization

```python
# WRONG - all zeros
result = [[0] * n for _ in range(n)]

# CORRECT - identity matrix
result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
```

**Problem:** Starting with zeros gives zero result.
**Fix:** Initialize result as identity matrix (1s on diagonal).

### Mistake 3: Modifying Input Matrix

```python
# WRONG - modifies original
base = M
base = mat_mult(base, base)  # Corrupts M

# CORRECT - make a copy
base = [row[:] for row in M]
```

**Problem:** Modifying the input affects subsequent queries.
**Fix:** Create a deep copy of the matrix before modifying.

### Mistake 4: 1-indexed vs 0-indexed Confusion

```python
# WRONG
return powered[a][a]  # a is 1-indexed!

# CORRECT
return powered[a - 1][a - 1]  # Convert to 0-indexed
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k = 1, self-loop exists | adj[0][0] = 1, query (1, 1) | 1 | Direct self-loop is a circuit |
| k = 1, no self-loop | adj[0][0] = 0, query (1, 1) | 0 | No path of length 1 back to self |
| Disconnected node | No edges to/from node a | 0 | No circuits possible |
| k = 10^9 | Large k | Computed via log k steps | Binary exponentiation handles this |
| Complete graph | All edges present | n^(k-1) mod MOD | Many paths possible |

---

## When to Use This Pattern

### Use Matrix Exponentiation When:
- Counting paths/walks of a specific length in a graph
- Linear recurrences with large iteration counts (e.g., Fibonacci for large n)
- State transitions that can be expressed as matrix multiplication
- Multiple queries on the same graph with different path lengths

### Don't Use When:
- k is small (k < n^2) - direct DP might be faster
- Finding actual paths, not counting them
- Graph changes between queries
- Need shortest/longest path (use Dijkstra/Bellman-Ford)

### Pattern Recognition Checklist:
- [ ] Need to count paths of length k? -> **Matrix exponentiation**
- [ ] Linear recurrence like dp[i] = a*dp[i-1] + b*dp[i-2]? -> **Matrix exponentiation**
- [ ] k is very large (> 10^6)? -> **Must use O(log k) approach**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html) | Core technique for matrix power |
| [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | Simple matrix exponentiation application |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Graph Paths I](https://cses.fi/problemset/task/1723) | Count paths between different nodes (not circuits) |
| [Graph Paths II](https://cses.fi/problemset/task/1724) | Same technique, paths instead of circuits |
| [Counting Paths](https://cses.fi/problemset/task/1136) | Different approach (LCA-based) |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Knight's Tour](https://cses.fi/problemset/task/1635) | Matrix exponentiation on grid |
| [Shortest Routes II](https://cses.fi/problemset/task/1672) | Floyd-Warshall for all-pairs shortest paths |

---

## Key Takeaways

1. **The Core Idea:** Adjacency matrix raised to power k counts paths of length k
2. **Time Optimization:** Binary exponentiation reduces O(k) to O(log k) matrix multiplications
3. **Space Trade-off:** O(n^2) space for matrices, but handles arbitrarily large k
4. **Pattern:** Matrix exponentiation for counting problems with large iteration counts

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement matrix multiplication with modular arithmetic
- [ ] Implement binary exponentiation for matrices
- [ ] Explain why A^k[i][j] counts paths from i to j
- [ ] Recognize problems solvable with matrix exponentiation
- [ ] Handle edge cases (self-loops, disconnected nodes)

---

## Additional Resources

- [CP-Algorithms: Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CP-Algorithms: Matrix Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html#toc-tgt-5)
- [CSES Graph Paths II](https://cses.fi/problemset/task/1724) - Matrix exponentiation for shortest paths
