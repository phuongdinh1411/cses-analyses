---
layout: simple
title: "Fixed-Length Path Queries I - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_trail_queries_analysis
difficulty: Hard
tags: [graph, matrix-exponentiation, binary-exponentiation, dynamic-programming]
---

# Fixed-Length Path Queries I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Fixed-Length Path Queries I](https://cses.fi/problemset/task/1723) |
| **Difficulty** | Hard |
| **Category** | Graph Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Matrix Exponentiation |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Count paths of exactly k edges in a directed graph using matrix exponentiation
- [ ] Implement binary exponentiation for matrix powers in O(n^3 log k) time
- [ ] Recognize when adjacency matrix powers solve path counting problems
- [ ] Handle large exponents (up to 10^9) efficiently

---

## Problem Statement

**Problem:** Given a directed graph with n nodes and m edges, answer q queries. Each query asks: how many paths of exactly k edges exist from node a to node b?

**Input:**
- Line 1: n m q (nodes, edges, queries)
- Next m lines: a b (directed edge from a to b)
- Next q lines: a b k (query: paths from a to b with exactly k edges)

**Output:**
- For each query, print the number of paths modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 100
- 1 <= m <= n^2
- 1 <= q <= 10^5
- 1 <= k <= 10^9
- 1 <= a, b <= n

### Example

```
Input:
4 5 3
1 2
2 3
3 1
3 4
1 4
1 3 2
1 4 2
1 1 3

Output:
1
2
1
```

**Explanation:**
- Query 1: Paths of length 2 from 1 to 3: `1->2->3` (1 path)
- Query 2: Paths of length 2 from 1 to 4: No 2-edge paths exist from 1 to 4
- Query 3: Paths of length 3 from 1 to 1: `1->2->3->1` (1 path)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count paths of exactly k edges efficiently?

The fundamental insight is that **adjacency matrix exponentiation counts paths**. If A is the adjacency matrix, then A^k[i][j] gives the number of paths of exactly k edges from i to j.

### Breaking Down the Problem

1. **What are we looking for?** Number of paths with exactly k edges
2. **What information do we have?** Graph structure (adjacency matrix) and queries
3. **What's the relationship?** A^k[i][j] = sum over all m of A^(k-1)[i][m] * A[m][j]

### Why Matrix Multiplication Works

Consider A^2[i][j]:
```
A^2[i][j] = sum(A[i][m] * A[m][j]) for all m
```

This counts: for each intermediate node m, if there's an edge i->m AND an edge m->j, we have one 2-edge path. Summing over all m gives total 2-edge paths from i to j.

---

## Solution 1: Brute Force DFS

### Idea

For each query, run DFS from node a, counting all paths that reach node b in exactly k steps.

### Algorithm

1. For each query (a, b, k):
2. Run DFS from a, tracking depth
3. When depth equals k and current node is b, increment count
4. Return count modulo 10^9 + 7

### Code

```python
def solve_brute_force(n, edges, queries):
  """
  Brute force: DFS for each query.

  Time: O(q * n^k) - exponential in k
  Space: O(k) - recursion depth
  """
  MOD = 10**9 + 7

  # Build adjacency list
  adj = [[] for _ in range(n + 1)]
  for a, b in edges:
    adj[a].append(b)

  def count_paths(start, end, steps):
    if steps == 0:
      return 1 if start == end else 0

    total = 0
    for neighbor in adj[start]:
      total += count_paths(neighbor, end, steps - 1)
    return total % MOD

  results = []
  for a, b, k in queries:
    results.append(count_paths(a, b, k))

  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n^k) | Each query explores up to n^k paths |
| Space | O(k) | Recursion depth |

### Why This Is Too Slow

With k up to 10^9, this approach is completely infeasible. We need logarithmic time in k.

---

## Solution 2: Matrix Exponentiation (Optimal)

### Key Insight

> **The Trick:** A^k[i][j] counts paths of exactly k edges from i to j. Use binary exponentiation to compute A^k in O(n^3 log k).

### Mathematical Foundation

For adjacency matrix A:
- A^1[i][j] = 1 if edge i->j exists (paths of length 1)
- A^2[i][j] = number of 2-edge paths from i to j
- A^k[i][j] = number of k-edge paths from i to j

**Proof by induction:** A^k[i][j] = sum over m of A^(k-1)[i][m] * A[m][j], which counts paths that go from i to some m in (k-1) steps, then from m to j in 1 step.

### Algorithm

1. Build n x n adjacency matrix A
2. For each unique k value, compute A^k using binary exponentiation
3. Answer queries using precomputed matrix powers

### Dry Run Example

```
Graph: 1->2, 2->3, 3->1, 3->4, 1->4

Adjacency Matrix A:
      1  2  3  4
   ┌─────────────┐
 1 │ 0  1  0  1 │
 2 │ 0  0  1  0 │
 3 │ 1  0  0  1 │
 4 │ 0  0  0  0 │
   └─────────────┘

Computing A^2[1][3] (paths of length 2 from 1 to 3):
= sum over m of A[1][m] * A[m][3]
= A[1][2]*A[2][3] = 1*1 = 1

Path found: 1->2->3
```

### Binary Exponentiation for Matrices

```
To compute A^k:
  If k = 0: return Identity matrix
  If k is even: compute A^(k/2), return (A^(k/2))^2
  If k is odd: return A * A^(k-1)

Example: A^13
  A^13 = A * A^12
  A^12 = (A^6)^2
  A^6 = (A^3)^2
  A^3 = A * A^2
  A^2 = (A^1)^2

Only log2(13) = 4 multiplications needed!
```

### Code

**Python Solution:**

```python
import sys
from collections import defaultdict

def solve():
  input_data = sys.stdin.read().split()
  idx = 0

  n, m, q = int(input_data[idx]), int(input_data[idx+1]), int(input_data[idx+2])
  idx += 3

  MOD = 10**9 + 7

  # Build adjacency matrix
  adj = [[0] * n for _ in range(n)]
  for _ in range(m):
    a, b = int(input_data[idx]) - 1, int(input_data[idx+1]) - 1
    idx += 2
    adj[a][b] += 1  # Handle multiple edges

  def matrix_mult(A, B):
    """Multiply two n x n matrices modulo MOD."""
    result = [[0] * n for _ in range(n)]
    for i in range(n):
      for k in range(n):
        if A[i][k] == 0:
          continue
        for j in range(n):
          result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % MOD
    return result

  def matrix_power(matrix, power):
    """Compute matrix^power using binary exponentiation."""
    # Identity matrix
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    base = [row[:] for row in matrix]  # Copy matrix

    while power > 0:
      if power & 1:
        result = matrix_mult(result, base)
      base = matrix_mult(base, base)
      power >>= 1

    return result

  # Collect unique k values and precompute
  queries = []
  k_values = set()
  for _ in range(q):
    a, b, k = int(input_data[idx]) - 1, int(input_data[idx+1]) - 1, int(input_data[idx+2])
    idx += 3
    queries.append((a, b, k))
    k_values.add(k)

  # Precompute matrix powers for unique k values
  powers = {}
  for k in k_values:
    powers[k] = matrix_power(adj, k)

  # Answer queries
  results = []
  for a, b, k in queries:
    results.append(powers[k][a][b])

  print('\n'.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 log k_max * unique_k + q) | Matrix power for each unique k, then O(1) per query |
| Space | O(n^2 * unique_k) | Store matrix power for each unique k |

---

## Common Mistakes

### Mistake 1: Forgetting to Handle Multiple Edges

**Problem:** Multiple edges between same pair of nodes should each count as a separate path option.

### Mistake 2: 0-indexed vs 1-indexed Confusion

```python
# WRONG - using 1-indexed input directly
adj[a][b] = 1  # a, b are 1-indexed from input

# CORRECT - convert to 0-indexed
adj[a-1][b-1] = 1
```

### Mistake 3: Integer Overflow in Matrix Multiplication

### Mistake 4: Not Using Long Long for k

---

## Edge Cases

| Case | Input | Expected Handling |
|------|-------|-------------------|
| k = 1 | Direct edge query | Just return adj[a][b] |
| Self-loops | Edge a->a | Counts as valid 1-edge path |
| No path exists | A^k[a][b] = 0 | Return 0 |
| Multiple edges | Two edges a->b | adj[a][b] = 2, affects all path counts |
| k = 0 | Zero-length path | Return 1 if a == b, else 0 (identity matrix) |
| Disconnected nodes | No path at any length | Return 0 |

---

## When to Use This Pattern

### Use Matrix Exponentiation When:
- Counting paths of exactly k steps/edges
- k is very large (up to 10^9)
- Graph is small-medium (n <= 100-200)
- Need multiple queries with same graph

### Pattern Recognition Checklist:
- [ ] Counting paths/walks of fixed length? -> **Matrix exponentiation**
- [ ] State transitions that can be expressed as matrix multiplication? -> **Matrix exponentiation**
- [ ] Need to compute f(n) where f(n) = sum of linear combinations of f(n-1), f(n-2), etc? -> **Matrix exponentiation**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Exponentiation](https://cses.fi/problemset/task/1095) | Learn binary exponentiation basics |
| [Fibonacci Numbers](https://cses.fi/problemset/task/1722) | Matrix exponentiation for recurrences |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Graph Paths I](https://cses.fi/problemset/task/1723) | This problem - path counting |
| [Graph Paths II](https://cses.fi/problemset/task/1724) | Find minimum length path of exactly k edges |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Knight's Tour](https://cses.fi/problemset/task/1689) | Apply matrix exponentiation to chessboard |
| [Dice Probability](https://cses.fi/problemset/task/1725) | Probability with matrix exponentiation |

---

## Key Takeaways

1. **The Core Idea:** Adjacency matrix power A^k[i][j] counts k-edge paths from i to j
2. **Time Optimization:** Binary exponentiation reduces O(k) to O(log k) multiplications
3. **Space Trade-off:** Store O(n^2) matrix instead of exploring O(n^k) paths
4. **Pattern:** Matrix exponentiation works for any linear state transition problem

---

## Additional Resources

- [CP-Algorithms: Matrix Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CSES Graph Paths I](https://cses.fi/problemset/task/1723) - Matrix exponentiation for paths
