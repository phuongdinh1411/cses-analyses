---
layout: simple
title: "Permutations
permalink: /problem_soulutions/introductory_problems/permutations_analysis/"
---


# Permutations

## Problem Statement
A permutation of integers 1,2,…,n is called beautiful if there are no adjacent elements whose difference is 1."
Given n, construct a beautiful permutation of size n or determine that it's impossible.

### Input
The only input line contains an integer n.

### Output
Print a beautiful permutation of integers 1,2,…,n. If there are several solutions, you may print any of them. If it's impossible, print "NO SOLUTION".

### Constraints
- 1 ≤ n ≤ 10^6

### Example
```
Input:
5

Output:
4 2 5 3 1
```

## Solution Progression

### Approach 1: Brute Force - O(n!)
**Description**: Generate all permutations and check if any is beautiful.

```python
from itertools import permutations

def permutations_brute_force(n):
    numbers = list(range(1, n + 1))
    
    for perm in permutations(numbers):
        is_beautiful = True
        for i in range(len(perm) - 1):
            if abs(perm[i] - perm[i + 1]) == 1:
                is_beautiful = False
                break
        
        if is_beautiful:
            return list(perm)
    
    return None
```

**Why this is inefficient**: We're generating all n! permutations and checking each one. This is completely impractical for large n.

### Improvement 1: Pattern-Based Construction - O(n)
**Description**: Use a specific pattern to construct beautiful permutations.

```python
def permutations_pattern(n):
    if n == 1:
        return [1]
    elif n == 2 or n == 3:
        return None  # Impossible for n=2,3
    
    result = []
    
    # Add even numbers first
    for i in range(2, n + 1, 2):
        result.append(i)
    
    # Add odd numbers
    for i in range(1, n + 1, 2):
        result.append(i)
    
    return result
```

**Why this improvement works**: By separating even and odd numbers, we ensure that no adjacent elements have a difference of 1. Even numbers are at least 2 apart, and odd numbers are at least 2 apart.

### Improvement 2: Optimized Pattern - O(n)
**Description**: Use a more optimized pattern that works for all valid n.

```python
def permutations_optimized(n):
    if n == 1:
        return [1]
    elif n == 2 or n == 3:
        return None
    
    result = []
    
    # Start with even numbers in descending order
    for i in range(n, 0, -1):
        if i % 2 == 0:
            result.append(i)
    
    # Add odd numbers in descending order
    for i in range(n, 0, -1):
        if i % 2 == 1:
            result.append(i)
    
    return result
```

**Why this improvement works**: This pattern ensures that even numbers are placed first (in descending order), followed by odd numbers (in descending order). This guarantees that no adjacent elements have a difference of 1.

### Alternative: Simple Pattern - O(n)
**Description**: Use a simple alternating pattern.

```python
def permutations_simple(n):
    if n == 1:
        return [1]
    elif n == 2 or n == 3:
        return None
    
    result = []
    
    # Add numbers starting from n/2 + 1
    start = (n // 2) + 1
    for i in range(start, n + 1):
        result.append(i)
    
    # Add remaining numbers
    for i in range(1, start):
        result.append(i)
    
    return result
```

**Why this works**: This pattern creates a clear separation between the first half and second half of the numbers, ensuring no adjacent elements have a difference of 1.

## Final Optimal Solution

```python
n = int(input())

if n == 1:
    print(1)
elif n == 2 or n == 3:
    print("NO SOLUTION")
else:
    # Print even numbers first, then odd numbers
    for i in range(2, n + 1, 2):
        print(i, end=' ')
    for i in range(1, n + 1, 2):
        print(i, end=' ')
    print()
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Generate all permutations |
| Pattern-Based | O(n) | O(n) | Use specific pattern |
| Optimized Pattern | O(n) | O(n) | Separate even and odd |
| Simple Pattern | O(n) | O(n) | Use alternating pattern |

## Key Insights for Other Problems

### 1. **Pattern-Based Construction**
**Principle**: Use specific patterns to construct solutions instead of brute force.
**Applicable to**:
- Construction problems
- Pattern recognition
- Mathematical problems
- Algorithm design

**Example Problems**:
- Permutations
- Array construction
- Pattern generation
- Mathematical sequences

### 2. **Impossibility Detection**
**Principle**: Identify cases where no solution exists early in the process.
**Applicable to**:
- Decision problems
- Existence problems
- Mathematical problems
- Algorithm design

**Example Problems**:
- Permutation problems
- Graph problems
- Mathematical problems
- Decision problems

### 3. **Mathematical Patterns**
**Principle**: Use mathematical properties and patterns to solve problems efficiently.
**Applicable to**:
- Number theory
- Mathematical sequences
- Pattern recognition
- Algorithm design

**Example Problems**:
- Number theory problems
- Mathematical sequences
- Pattern recognition
- Algorithm design

### 4. **Construction vs Search**
**Principle**: Sometimes it's better to construct a solution than to search for one.
**Applicable to**:
- Construction problems
- Algorithm design
- Problem solving
- Mathematical problems

**Example Problems**:
- Construction problems
- Algorithm design
- Mathematical problems
- Pattern generation

## Notable Techniques

### 1. **Pattern Construction Pattern**
```python
# Use specific pattern to construct solution
def construct_pattern(n):
    if impossible_case(n):
        return None
    
    result = []
    # Apply pattern
    for i in range(start, end, step):
        result.append(i)
    return result
```

### 2. **Impossibility Check Pattern**
```python
# Check for impossible cases first
def solve_problem(n):
    if n == impossible_case:
        return "NO SOLUTION"
    # Continue with solution
```

### 3. **Alternating Pattern**
```python
# Use alternating pattern
for i in range(start1, end1, step1):
    result.append(i)
for i in range(start2, end2, step2):
    result.append(i)
```

## Edge Cases to Remember

1. **n = 1**: Only one element, always beautiful
2. **n = 2**: Impossible (1,2 or 2,1 both have adjacent difference 1)
3. **n = 3**: Impossible (any permutation has adjacent difference 1)
4. **n ≥ 4**: Always possible with proper pattern
5. **Large n**: Handle efficiently with pattern construction

## Problem-Solving Framework

1. **Identify construction nature**: This is about constructing a specific permutation
2. **Check impossibility**: Identify cases where no solution exists
3. **Find pattern**: Look for mathematical patterns that work
4. **Construct solution**: Use pattern to build solution efficiently
5. **Verify correctness**: Test with examples

---

*This analysis shows how to efficiently construct beautiful permutations using mathematical patterns.* 