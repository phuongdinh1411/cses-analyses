---
layout: simple
title: "Fixed Length Walk Queries - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_walk_queries_analysis
difficulty: Hard
tags: [matrix-exponentiation, graph-theory, binary-exponentiation]
prerequisites: [graph_basics, matrix_multiplication]
---

# Fixed Length Walk Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Graph Theory / Linear Algebra |
| **Time Limit** | 1 second |
| **Key Technique** | Matrix Exponentiation |
| **CSES Link** | [Graph Paths I](https://cses.fi/problemset/task/1723) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how adjacency matrix powers count walks
- [ ] Implement matrix exponentiation with binary exponentiation
- [ ] Apply this technique to path counting problems
- [ ] Recognize when matrix exponentiation is the right approach

---

## Problem Statement

**Problem:** Given a directed graph with n nodes, determine if there exists a walk of exactly k steps from node a to node b.

**Input:**
- Line 1: `n q` - number of nodes and queries
- Next n lines: adjacency matrix (1 if edge exists, 0 otherwise)
- Next q lines: `a b k` - query for walk from a to b of length k

**Output:**
- For each query: 1 if walk exists, 0 otherwise

**Constraints:**
- 1 <= n <= 100
- 1 <= q <= 10^5
- 1 <= k <= 10^9
- 1 <= a, b <= n

### Example

```
Input:
3 2
0 1 1
1 0 1
1 1 0
1 3 2
2 1 1

Output:
1
1
```

**Explanation:**
- Query 1: Walk 1 -> 2 -> 3 has length 2. Answer: 1
- Query 2: Direct edge 2 -> 1 has length 1. Answer: 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we count walks of exactly k steps efficiently?

The adjacency matrix A has a remarkable property: A^k[i][j] gives the number of walks of exactly k steps from node i to node j. This transforms a graph problem into a linear algebra problem.

### Breaking Down the Problem

1. **What are we looking for?** Whether a walk of exactly k steps exists
2. **What information do we have?** Graph structure (adjacency matrix) and k
3. **What's the relationship?** A^k[a][b] > 0 means a walk exists

### Why Does A^k Work?

Consider A^2[i][j]:
```
A^2[i][j] = sum(A[i][m] * A[m][j]) for all m
```

This counts all intermediate nodes m where:
- There's an edge from i to m (A[i][m] = 1)
- There's an edge from m to j (A[m][j] = 1)

Each valid m contributes one 2-step walk. By induction, A^k counts k-step walks.

---

## Solution 1: Brute Force (DFS)

### Idea

Try all possible walks of length k using depth-first search.

### Algorithm

1. Start DFS from source node
2. Explore all neighbors at each step
3. Check if we reach target at exactly step k

### Code

```python
def solve_brute_force(n, adj, a, b, k):
  """
  Brute force using DFS.

  Time: O(n^k) - exponential
  Space: O(k) - recursion depth
  """
  def dfs(node, steps):
    if steps == k:
      return node == b
    for next_node in range(n):
      if adj[node][next_node] == 1:
        if dfs(next_node, steps + 1):
          return True
    return False

  return 1 if dfs(a, 0) else 0
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k) | Each step branches up to n ways |
| Space | O(k) | Recursion stack depth |

### Why This Works (But Is Slow)

Correctness is guaranteed because we try all possible walks. However, with k up to 10^9, this is completely infeasible.

---

## Solution 2: Matrix Exponentiation (Optimal)

### Key Insight

> **The Trick:** Use binary exponentiation to compute A^k in O(n^3 log k) time.

### Algorithm

1. Read adjacency matrix A
2. Compute A^k using binary exponentiation
3. For each query (a, b, k), check if A^k[a][b] > 0

### Binary Exponentiation for Matrices

```
A^k = | A^(k/2) * A^(k/2)           if k is even
      | A^(k/2) * A^(k/2) * A       if k is odd
      | I (identity matrix)         if k is 0
```

### Dry Run Example

Let's trace through with n=3, k=2:

```
Adjacency Matrix A:
    [0 1 1]
A = [1 0 1]
    [1 1 0]

Computing A^2:
Since k=2 is even: A^2 = A^1 * A^1 = A * A

A * A calculation:
Row 0, Col 0: 0*0 + 1*1 + 1*1 = 2
Row 0, Col 1: 0*1 + 1*0 + 1*1 = 1
Row 0, Col 2: 0*1 + 1*1 + 1*0 = 1
...

      [2 1 1]
A^2 = [1 2 1]
      [1 1 2]

Query: Is there a walk from 1 to 3 (0-indexed: 0 to 2) of length 2?
A^2[0][2] = 1 > 0, so YES!

The walks: 0->1->2, validating our answer.
```

### Visual Diagram

```
Graph:           Matrix Powers:

  1 <---> 2      A^1 = adjacency (1-step reachability)
  |\     /|      A^2 = 2-step reachability counts
  | \   / |      A^k = k-step reachability counts
  |  \ /  |
  |   X   |
  |  / \  |      A^k[i][j] > 0 means: walk exists!
  | /   \ |
  v/     \v
  3 <---> (implied)
```

### Code

```python
def solve_optimal(n, adj, queries):
  """
  Optimal solution using matrix exponentiation.

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
          # For existence check, cap at 1 to avoid overflow
          if C[i][j] > 0:
            C[i][j] = 1
    return C

  def matrix_power(M, k):
    """Compute M^k using binary exponentiation."""
    # Identity matrix
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    base = [row[:] for row in M]  # Copy matrix

    while k > 0:
      if k % 2 == 1:
        result = matrix_mult(result, base)
      base = matrix_mult(base, base)
      k //= 2

    return result

  # Group queries by k value
  from collections import defaultdict
  k_to_queries = defaultdict(list)
  for idx, (a, b, k) in enumerate(queries):
    k_to_queries[k].append((idx, a - 1, b - 1))  # Convert to 0-indexed

  # Answer queries
  answers = [0] * len(queries)
  for k, query_list in k_to_queries.items():
    Ak = matrix_power(adj, k)
    for idx, a, b in query_list:
      answers[idx] = 1 if Ak[a][b] > 0 else 0

  return answers


# Main execution
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
    a, b, k = int(input_data[idx]), int(input_data[idx + 1]), int(input_data[idx + 2])
    queries.append((a, b, k))
    idx += 3

  results = solve_optimal(n, adj, queries)
  print('\n'.join(map(str, results)))


if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 log k + q) | Matrix mult is O(n^3), done O(log k) times |
| Space | O(n^2) | Store matrices |

---

## Common Mistakes

### Mistake 1: Integer Overflow

```python
# WRONG - can overflow for counting paths
C[i][j] += A[i][k] * B[k][j]

# CORRECT - for existence check only
if A[i][k] and B[k][j]:
  C[i][j] = 1
```

**Problem:** With large k, path counts can overflow even 64-bit integers.
**Fix:** For existence queries, just track whether value is > 0.

### Mistake 2: Forgetting Identity Matrix Base Case

```python
# WRONG
def matrix_power(M, k):
  if k == 1:
    return M
  # What if k == 0?

# CORRECT
def matrix_power(M, k):
  result = identity_matrix()  # Start with I
  while k > 0:
    # ... binary exponentiation
```

**Problem:** k=0 should return identity matrix (walk of length 0 from i to i).

### Mistake 3: Off-by-One Indexing

```python
# WRONG - using 1-indexed directly
answers[idx] = Ak[a][b]  # If a,b are 1-indexed

# CORRECT
answers[idx] = Ak[a-1][b-1]  # Convert to 0-indexed
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k = 0 | a = b | 1 | Stay in place (0-length walk) |
| k = 0 | a != b | 0 | Can't reach different node in 0 steps |
| No edges | Any k > 0 | 0 | No walks possible |
| Self-loop | k = 1, self-loop exists | 1 | Can walk to self |
| Large k | k = 10^9 | Varies | Binary exp handles this |

---

## When to Use This Pattern

### Use Matrix Exponentiation When:
- Counting paths/walks of exact length k
- k is very large (up to 10^9 or more)
- Graph is small (n <= 100-200)
- Need to answer many queries for same k

### Don't Use When:
- k is small (simple BFS/DFS suffices)
- Graph is large (n > 500, matrix ops too slow)
- Looking for shortest path (use BFS/Dijkstra)
- Graph is sparse (adjacency list + DP might be better)

### Pattern Recognition Checklist:
- [ ] Need exact length k paths? -> **Matrix Exponentiation**
- [ ] Large k (> 10^6)? -> **Must use Matrix Exponentiation**
- [ ] Small n (< 200)? -> **Matrix Exponentiation is efficient**
- [ ] Counting paths modulo M? -> **Matrix Exponentiation with mod**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Binary Exponentiation](https://cses.fi/problemset/task/1095) | Core technique for fast power |
| [BFS Shortest Path](https://cses.fi/problemset/task/1667) | Basic graph traversal |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Graph Paths I](https://cses.fi/problemset/task/1723) | Count paths (mod 10^9+7) |
| [Graph Paths II](https://cses.fi/problemset/task/1724) | Shortest path of exactly k edges |
| [Dice Combinations](https://cses.fi/problemset/task/1633) | Linear recurrence via matrix exp |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Fibonacci Numbers](https://cses.fi/problemset/task/1722) | Matrix exp for recurrences |
| [Knight's Tour](https://cses.fi/problemset/task/1689) | Hamiltonian path |

---

## Key Takeaways

1. **The Core Idea:** A^k[i][j] counts walks of length k from i to j
2. **Time Optimization:** Binary exponentiation reduces O(k) to O(log k)
3. **Space Trade-off:** O(n^2) space for matrices
4. **Pattern:** Graph counting problems with large k often need matrix exponentiation

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why A^k counts k-length walks
- [ ] Implement matrix multiplication correctly
- [ ] Apply binary exponentiation to matrices
- [ ] Recognize when this technique applies

## Additional Resources

- [CP-Algorithms: Matrix Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CSES Graph Paths I](https://cses.fi/problemset/task/1723) - Matrix exponentiation for path counting
