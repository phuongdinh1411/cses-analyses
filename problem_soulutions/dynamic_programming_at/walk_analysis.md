---
layout: simple
title: "Walk"
permalink: /problem_soulutions/dynamic_programming_at/walk_analysis
---

# Walk

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand matrix exponentiation for DP
- Apply matrix exponentiation to count paths
- Recognize when to use matrix exponentiation
- Optimize DP with matrix operations

## 📋 Problem Description

Given a directed graph with N vertices, count the number of walks of length K from vertex 1 to vertex N.

**Input**: 
- First line: N, K (2 ≤ N ≤ 50, 1 ≤ K ≤ 10^18)
- Next N lines: adjacency matrix

**Output**: 
- Number of walks modulo 10^9+7

**Constraints**:
- 2 ≤ N ≤ 50
- 1 ≤ K ≤ 10^18

## 🔍 Solution Analysis

### Approach: Matrix Exponentiation

**Key Insight**: The number of walks of length k from i to j equals the (i,j)-th entry of the adjacency matrix raised to the k-th power.

**Algorithm**:
- Build adjacency matrix A
- Compute A^K using binary exponentiation
- Return A^K[0][N-1] (0-indexed: vertex 1 → vertex N)

**Implementation**:
```python
def matrix_multiply(A, B, MOD):
    """Multiply two matrices modulo MOD"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
    return C

def matrix_power(matrix, power, MOD):
    """Compute matrix^power using binary exponentiation"""
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = matrix
    
    while power:
        if power & 1:
            result = matrix_multiply(result, base, MOD)
        base = matrix_multiply(base, base, MOD)
        power //= 2
    
    return result

def walk_count(n, k, adjacency_matrix):
    """
    Matrix exponentiation solution for Walk problem
    
    Args:
        n: number of vertices
        k: walk length
        adjacency_matrix: 2D list representing graph
    
    Returns:
        int: number of walks modulo 10^9+7
    """
    MOD = 10**9 + 7
    
    # Compute adjacency matrix to the k-th power
    result_matrix = matrix_power(adjacency_matrix, k, MOD)
    
    # Return number of walks from vertex 0 (1) to vertex n-1 (N)
    return result_matrix[0][n - 1]

# Example usage
n, k = 4, 2
adjacency = [
    [0, 1, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [0, 1, 1, 0]
]
result = walk_count(n, k, adjacency)
print(f"Number of walks: {result}")
```

**Time Complexity**: O(N^3 * log K)
**Space Complexity**: O(N^2)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Matrix Exponentiation | O(N^3 * log K) | O(N^2) | Count paths with matrix powers |

### Why This Solution Works
- **Matrix Representation**: Adjacency matrix represents paths of length 1
- **Matrix Powers**: A^k represents paths of length k
- **Binary Exponentiation**: Efficient computation of large powers

## 🚀 Related Problems
- Path counting problems
- Matrix exponentiation problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem R](https://atcoder.jp/contests/dp/tasks/dp_r) - Original problem
- Matrix exponentiation techniques

