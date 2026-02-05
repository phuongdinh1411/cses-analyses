---
layout: simple
title: "Walk - Matrix Exponentiation Problem"
permalink: /problem_soulutions/dynamic_programming_at/walk_analysis
difficulty: Hard
tags: [matrix-exponentiation, dp, graph, binary-exponentiation]
---

# Walk

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Dynamic Programming / Matrix Exponentiation |
| **Time Limit** | 2 seconds |
| **Key Technique** | Matrix Exponentiation with Binary Exponentiation |
| **Problem Link** | [AtCoder DP Contest - Problem R](https://atcoder.jp/contests/dp/tasks/dp_r) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the connection between adjacency matrices and path counting
- [ ] Implement matrix multiplication with modular arithmetic
- [ ] Apply binary exponentiation to compute matrix powers efficiently
- [ ] Recognize problems where matrix exponentiation transforms O(K) DP into O(log K)

---

## Problem Statement

**Problem:** Given a directed graph with N vertices and its adjacency matrix, count the number of walks of length exactly K. A walk is a sequence of vertices where consecutive vertices are connected by an edge (can revisit vertices and edges).

**Input:**
- Line 1: Two integers N and K (number of vertices, walk length)
- Lines 2 to N+1: N x N adjacency matrix (1 = edge exists, 0 = no edge)

**Output:**
- Total number of walks of length K, modulo 10^9 + 7

**Constraints:**
- 1 <= N <= 50
- 1 <= K <= 10^18

### Example

```
Input:
4 2
0 1 0 0
0 0 1 1
0 0 0 1
1 0 0 0

Output:
6
```

**Explanation:** The walks of length 2 are:
- 1 -> 2 -> 3
- 1 -> 2 -> 4
- 2 -> 3 -> 4
- 2 -> 4 -> 1
- 3 -> 4 -> 1
- 4 -> 1 -> 2

Total: 6 walks

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently count paths of length K when K can be as large as 10^18?

The adjacency matrix A has a remarkable property: A[i][j] represents the number of walks of length 1 from vertex i to vertex j. When we multiply A by itself, (A^2)[i][j] gives the number of walks of length 2 from i to j. This pattern continues: A^K[i][j] gives walks of length K from i to j.

### Breaking Down the Problem

1. **What are we looking for?** Total count of all walks of length exactly K across all vertex pairs
2. **What information do we have?** The adjacency matrix showing direct connections
3. **What is the relationship between input and output?** Sum of all entries in A^K gives total walks

### The Matrix Multiplication Insight

Why does A^2[i][j] count paths of length 2?

```
(A^2)[i][j] = sum over all k of A[i][k] * A[k][j]
```

This sums over all intermediate vertices k: "paths from i to k" times "paths from k to j" = "paths from i to j via some k". This naturally counts all length-2 paths!

### Analogy

Think of matrix multiplication like a relay race. A[i][k] counts how many runners can go from station i to station k, and A[k][j] counts runners from k to j. The product counts all possible relay combinations through intermediate station k.

---

## Solution 1: Naive DP (TLE for large K)

### Idea

Use standard DP where dp[step][vertex] = number of ways to reach vertex in exactly step moves.

### Algorithm

1. Initialize dp[0][v] = 1 for all vertices (start anywhere)
2. For each step from 1 to K:
   - For each vertex v: dp[step][v] = sum of dp[step-1][u] for all u with edge u -> v
3. Sum all dp[K][v]

### Code

```python
def solve_naive(n, k, adj):
 """
 Naive DP solution - O(N^2 * K), times out for large K.

 Time: O(N^2 * K)
 Space: O(N)
 """
 MOD = 10**9 + 7

 # dp[v] = number of ways to be at vertex v
 dp = [1] * n  # Can start from any vertex

 for _ in range(k):
  new_dp = [0] * n
  for v in range(n):
   for u in range(n):
    if adj[u][v]:  # Edge from u to v
     new_dp[v] = (new_dp[v] + dp[u]) % MOD
  dp = new_dp

 return sum(dp) % MOD
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^2 * K) | K iterations, N^2 transitions each |
| Space | O(N) | Rolling array optimization |

### Why This Is Correct But Slow

The recurrence is correct: to reach v in step s, sum over all predecessors u. However, with K up to 10^18, this approach is computationally infeasible.

---

## Solution 2: Matrix Exponentiation (Optimal)

### Key Insight

> **The Trick:** Matrix multiplication directly encodes the DP transition. Computing A^K with binary exponentiation reduces O(K) to O(log K).

### DP to Matrix Transformation

| DP Concept | Matrix Equivalent |
|------------|-------------------|
| `dp[v]` | Vector of size N |
| Transition for one step | Multiply by adjacency matrix A |
| K steps of DP | Multiply by A^K |

**In plain English:** Each matrix multiplication applies one step of the DP transition. Instead of doing K separate multiplications (O(K)), we compute A^K directly using binary exponentiation (O(log K)).

### State Transition as Matrix Multiplication

```
new_dp[v] = sum(adj[u][v] * dp[u] for all u)
```

This is exactly matrix-vector multiplication: `new_dp = A * dp`

After K steps: `final_dp = A^K * initial_dp`

### Binary Exponentiation for Matrices

To compute A^K efficiently:
- A^K = A^(K/2) * A^(K/2) if K is even
- A^K = A * A^(K-1) if K is odd

This gives O(log K) matrix multiplications, each taking O(N^3).

### Algorithm

1. Read adjacency matrix A
2. Compute A^K using binary exponentiation
3. Sum all entries of A^K (total walks from any vertex to any vertex)

### Dry Run Example

Let us trace through with the example: N=4, K=2

```
Initial adjacency matrix A:
    0 1 2 3
  +--------
0 | 0 1 0 0
1 | 0 0 1 1
2 | 0 0 0 1
3 | 1 0 0 0

Computing A^2 = A * A:

A^2[0][0] = A[0][0]*A[0][0] + A[0][1]*A[1][0] + A[0][2]*A[2][0] + A[0][3]*A[3][0]
          = 0*0 + 1*0 + 0*0 + 0*1 = 0

A^2[0][1] = A[0][0]*A[0][1] + A[0][1]*A[1][1] + A[0][2]*A[2][1] + A[0][3]*A[3][1]
          = 0*1 + 1*0 + 0*0 + 0*0 = 0

A^2[0][2] = A[0][0]*A[0][2] + A[0][1]*A[1][2] + A[0][2]*A[2][2] + A[0][3]*A[3][2]
          = 0*0 + 1*1 + 0*0 + 0*0 = 1   (path: 0->1->2)

A^2[0][3] = 0*0 + 1*1 + 0*1 + 0*0 = 1   (path: 0->1->3)

Full A^2:
    0 1 2 3
  +--------
0 | 0 0 1 1    (paths starting from vertex 0)
1 | 1 0 0 1    (paths starting from vertex 1)
2 | 1 0 0 0    (paths starting from vertex 2)
3 | 0 1 0 0    (paths starting from vertex 3)

Sum of all entries = 0+0+1+1 + 1+0+0+1 + 1+0+0+0 + 0+1+0+0 = 6

Answer: 6 walks of length 2
```

### Visual Diagram

```
Graph visualization:

    +---+     +---+
    | 0 |---->| 1 |
    +---+     +---+
      ^         |
      |         v
    +---+     +---+
    | 3 |<----| 2 |
    +---+     +---+
      ^         |
      +---------+

Walks of length 2:
  0->1->2, 0->1->3
  1->2->3, 1->3->0
  2->3->0
  3->0->1

Total: 6 walks
```

### Code (Python)

```python
def matrix_multiply(A, B, mod):
 """Multiply two N x N matrices modulo mod."""
 n = len(A)
 C = [[0] * n for _ in range(n)]
 for i in range(n):
  for k in range(n):
   if A[i][k] == 0:
    continue
   for j in range(n):
    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
 return C


def matrix_power(M, p, mod):
 """Compute M^p using binary exponentiation."""
 n = len(M)
 # Initialize result as identity matrix
 result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
 base = [row[:] for row in M]  # Copy matrix

 while p > 0:
  if p & 1:
   result = matrix_multiply(result, base, mod)
  base = matrix_multiply(base, base, mod)
  p >>= 1

 return result


def solve():
 """
 Matrix exponentiation solution for Walk problem.

 Time: O(N^3 * log K)
 Space: O(N^2)
 """
 MOD = 10**9 + 7

 n, k = map(int, input().split())
 adj = []
 for _ in range(n):
  row = list(map(int, input().split()))
  adj.append(row)

 # Compute adjacency matrix to the K-th power
 result = matrix_power(adj, k, MOD)

 # Sum all entries to get total number of walks
 total = 0
 for i in range(n):
  for j in range(n):
   total = (total + result[i][j]) % MOD

 print(total)


if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N^3 log K) | log K matrix multiplications, each O(N^3) |
| Space | O(N^2) | Store matrices of size N x N |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** A[i][k] and B[k][j] can each be up to 10^9, their product exceeds 32-bit integer range.
**Fix:** Use 64-bit integers (long long in C++) and apply modulo during multiplication.

### Mistake 2: Forgetting Identity Matrix Initialization

```python
# WRONG - uninitialized result
result = [[0] * n for _ in range(n)]

# CORRECT - identity matrix
result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
```

**Problem:** Matrix exponentiation starts with identity matrix (A^0 = I), not zero matrix.
**Fix:** Initialize diagonal to 1, rest to 0.

### Mistake 3: Counting Only Specific Endpoints

```python
# WRONG - only counting walks from 0 to n-1
return result[0][n-1]

# CORRECT - sum all entries for total walks
total = sum(result[i][j] for i in range(n) for j in range(n))
```

**Problem:** The problem asks for ALL walks of length K, not just from a specific source to destination.
**Fix:** Sum all matrix entries.

### Mistake 4: Not Copying Matrix in Binary Exponentiation

```python
# WRONG - modifies original matrix
base = M

# CORRECT - create a copy
base = [row[:] for row in M]
```

**Problem:** Without copying, the original adjacency matrix gets modified during computation.
**Fix:** Deep copy the matrix before binary exponentiation.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| K = 1 | Any graph | Sum of adjacency matrix | A^1 = A |
| Self-loops | Diagonal = 1 | Count self-loop walks | A[i][i] contributes to paths |
| Disconnected graph | No edges from some vertices | May be 0 | Some vertices have no outgoing walks |
| Single vertex with self-loop | N=1, A=[[1]], K=5 | 1 | Only one walk: stay at vertex |
| Complete graph | All 1s | N^K mod M | Every path is valid |
| K = 10^18 | Large exponent | Use binary exp | Direct iteration would TLE |

---

## When to Use This Pattern

### Use Matrix Exponentiation When:
- The problem has a linear recurrence (like Fibonacci, path counting)
- The number of steps K is very large (10^9 or more)
- The state space is small (N <= 100 typically)
- Transitions can be expressed as matrix multiplication

### Do Not Use When:
- K is small enough for direct DP (K <= 10^6)
- State transitions are non-linear
- The state space is too large (matrix operations become expensive)
- The recurrence depends on more than the previous state

### Pattern Recognition Checklist:
- [ ] Is there a recurrence relation? Consider matrix exponentiation
- [ ] Is the step count K very large (10^9+)? Matrix exponentiation may help
- [ ] Can the transition be written as a matrix? This is key to applying the technique
- [ ] Is the state space small (N <= 100)? Matrix multiplication is O(N^3)

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Fibonacci (CSES)](https://cses.fi/problemset/task/1722) | Basic matrix exponentiation |
| [Power of Two](https://leetcode.com/problems/power-of-two/) | Understanding binary exponentiation |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Graph Paths I (CSES)](https://cses.fi/problemset/task/1723) | Paths from 1 to N specifically |
| [Graph Paths II (CSES)](https://cses.fi/problemset/task/1724) | Shortest path with exactly K edges |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Throwing Dice (CSES)](https://cses.fi/problemset/task/1096) | Matrix exponentiation for dice sequences |
| [Knight's Tour](https://atcoder.jp/contests/abc232/tasks/abc232_e) | Matrix exponentiation on grid |

---

## Key Takeaways

1. **The Core Idea:** Adjacency matrix powers count paths - A^K[i][j] gives walks of length K from i to j
2. **Time Optimization:** Binary exponentiation reduces O(K) iterations to O(log K) matrix multiplications
3. **Space Trade-off:** O(N^2) space for matrices enables handling astronomically large K values
4. **Pattern:** This is the "matrix exponentiation for linear recurrence" pattern

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why matrix multiplication counts paths
- [ ] Implement matrix multiplication with modular arithmetic
- [ ] Apply binary exponentiation to matrices
- [ ] Identify when a DP problem can be optimized with matrix exponentiation
- [ ] Solve this problem in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Matrix Exponentiation](https://cp-algorithms.com/algebra/matrix-exp.html)
- [AtCoder DP Contest](https://atcoder.jp/contests/dp)
- [CSES Graph Paths I](https://cses.fi/problemset/task/1723) - Count paths with matrix exponentiation
