# CSES Functional Graph Distribution - Problem Analysis

## Problem Statement
Given n nodes, count the number of different functional graphs (directed graphs where each node has exactly one outgoing edge).

### Input
The first input line has an integer n: the number of nodes.

### Output
Print the number of different functional graphs modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 10^5

### Example
```
Input:
3

Output:
27
```

## Solution Progression

### Approach 1: Generate All Functions - O(n^n)
**Description**: Generate all possible functions and count them.

```python
def functional_graph_distribution_naive(n):
    MOD = 10**9 + 7
    
    def count_functions(pos):
        if pos == n:
            return 1
        
        count = 0
        for target in range(n):
            count = (count + count_functions(pos + 1)) % MOD
        
        return count
    
    return count_functions(0)
```

**Why this is inefficient**: O(n^n) complexity is too slow for large n.

### Improvement 1: Mathematical Formula - O(n)
**Description**: Use mathematical formula for function counting.

```python
def functional_graph_distribution_improved(n):
    MOD = 10**9 + 7
    
    # Number of functions = n^n
    result = 1
    for _ in range(n):
        result = (result * n) % MOD
    
    return result
```

**Why this improvement works**: Uses mathematical formula for function counting.

### Approach 2: Fast Exponentiation - O(log n)
**Description**: Use fast exponentiation for large n.

```python
def functional_graph_distribution_optimal(n):
    MOD = 10**9 + 7
    
    # Number of functions = n^n
    return pow(n, n, MOD)
```

**Why this improvement works**: Fast exponentiation gives optimal solution.

## Final Optimal Solution

```python
n = int(input())

def count_functional_graphs(n):
    MOD = 10**9 + 7
    
    # Number of functional graphs = n^n
    return pow(n, n, MOD)

result = count_functional_graphs(n)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Generate All Functions | O(n^n) | O(n) | Simple but exponential |
| Mathematical Formula | O(n) | O(1) | Formula approach |
| Fast Exponentiation | O(log n) | O(1) | Optimal solution |

## Key Insights for Other Problems

### 1. **Functional Graph Properties**
**Principle**: Each node has exactly one outgoing edge in a functional graph.
**Applicable to**: Graph theory problems, function counting problems

### 2. **Function Counting**
**Principle**: The number of functions from n elements to n elements is n^n.
**Applicable to**: Combinatorics problems, function analysis problems

### 3. **Fast Exponentiation**
**Principle**: Use fast exponentiation for large power calculations.
**Applicable to**: Large number problems, exponentiation problems

## Notable Techniques

### 1. **Fast Exponentiation**
```python
def fast_pow(base, exp, MOD):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return result
```

### 2. **Function Counting**
```python
def count_functions(n, MOD):
    return pow(n, n, MOD)
```

### 3. **Functional Graph Analysis**
```python
def analyze_functional_graphs(n):
    # Each node can point to any of n nodes
    # Total combinations = n^n
    return pow(n, n, 10**9 + 7)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a functional graph counting problem
2. **Choose approach**: Use mathematical formula with fast exponentiation
3. **Apply formula**: Number of functional graphs = n^n
4. **Use fast exponentiation**: Handle large numbers efficiently
5. **Return result**: Output the count modulo 10^9 + 7

---

*This analysis shows how to efficiently count functional graphs using mathematical formulas and fast exponentiation.* 