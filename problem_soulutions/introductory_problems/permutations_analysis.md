---
layout: simple
title: "Permutations"
permalink: /problem_soulutions/introductory_problems/permutations_analysis
---

# Permutations

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand permutation generation and lexicographic ordering concepts
- Apply backtracking or next_permutation to generate all permutations
- Implement efficient permutation generation algorithms with proper lexicographic ordering
- Optimize permutation generation using backtracking and lexicographic ordering techniques
- Handle edge cases in permutation problems (small n, lexicographic ordering, large output)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Permutation generation, backtracking, next_permutation, lexicographic ordering
- **Data Structures**: Arrays, permutation tracking, lexicographic ordering, backtracking stacks
- **Mathematical Concepts**: Permutations, combinatorics, lexicographic ordering, factorial calculations
- **Programming Skills**: Backtracking implementation, permutation generation, lexicographic ordering, algorithm implementation
- **Related Problems**: Permutation problems, Backtracking, Lexicographic ordering, Combinatorics

## Problem Description

**Problem**: Generate all permutations of numbers from 1 to n.

**Input**: An integer n (1 ≤ n ≤ 8)

**Output**: 
- First line: number of permutations
- Next lines: each permutation on a separate line (in lexicographic order)

**Constraints**:
- 1 ≤ n ≤ 8
- Generate all n! permutations
- Output must be in lexicographic order
- Each permutation on a separate line
- First line shows total count

**Example**:
```
Input: 3

Output:
6
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
```

## Visual Example

### Input and Permutation Generation
```
Input: n = 3

Numbers to permute: [1, 2, 3]
Total permutations: 3! = 6
```

### Lexicographic Order Generation
```
For n = 3, generating all permutations:

1. [1, 2, 3] ← Start with smallest
2. [1, 3, 2] ← Swap last two
3. [2, 1, 3] ← Move to next starting position
4. [2, 3, 1] ← Swap last two
5. [3, 1, 2] ← Move to next starting position
6. [3, 2, 1] ← Swap last two
```

### Backtracking Process
```
Backtracking tree for n = 3:

Level 0: []
├─ Level 1: [1]
│  ├─ Level 2: [1, 2]
│  │  └─ Level 3: [1, 2, 3] ✓
│  └─ Level 2: [1, 3]
│     └─ Level 3: [1, 3, 2] ✓
├─ Level 1: [2]
│  ├─ Level 2: [2, 1]
│  │  └─ Level 3: [2, 1, 3] ✓
│  └─ Level 2: [2, 3]
│     └─ Level 3: [2, 3, 1] ✓
└─ Level 1: [3]
   ├─ Level 2: [3, 1]
   │  └─ Level 3: [3, 1, 2] ✓
   └─ Level 2: [3, 2]
      └─ Level 3: [3, 2, 1] ✓
```

### Key Insight
The solution works by:
1. Using backtracking to generate all possible arrangements
2. Maintaining lexicographic order through systematic generation
3. Swapping elements to create different permutations
4. Time complexity: O(n! × n) for generating and outputting all permutations
5. Space complexity: O(n! × n) for storing all permutations

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Backtracking (Inefficient)

**Key Insights from Recursive Backtracking Solution:**
- Generate all permutations using recursive backtracking
- Simple but memory-intensive approach
- Not suitable for large n due to exponential growth
- Straightforward implementation but poor scalability

**Algorithm:**
1. Use recursive backtracking to generate all permutations
2. Build permutations by adding one element at a time
3. Use visited array to track used elements
4. Generate all possible arrangements systematically

**Visual Example:**
```
Recursive backtracking: Build permutations step by step
For n = 3, arr = [1, 2, 3]:

Step 1: Start with empty permutation []
Step 2: Add 1 → [1]
Step 3: Add 2 → [1, 2]
Step 4: Add 3 → [1, 2, 3] ✓ (complete permutation)

Backtrack and try other combinations:
Step 5: Remove 3, add 3 in different position
Step 6: Continue until all permutations generated
```

**Implementation:**
```python
def permutations_recursive(n):
    def backtrack(path, used):
        if len(path) == n:
            result.append(path[:])
            return
        
        for i in range(1, n + 1):
            if not used[i]:
                used[i] = True
                path.append(i)
                backtrack(path, used)
                path.pop()
                used[i] = False
    
    result = []
    used = [False] * (n + 1)
    backtrack([], used)
    return result

def solve_permutations_recursive():
    n = int(input())
    perms = permutations_recursive(n)
    
    print(len(perms))
    for perm in perms:
        print(' '.join(map(str, perm)))
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's inefficient:**
- O(n! × n) time complexity grows exponentially
- Not suitable for competitive programming with n up to 8
- Memory-intensive for large n
- Poor performance with factorial growth

### Approach 2: Iterative Next Permutation (Better)

**Key Insights from Iterative Solution:**
- Use iterative approach to generate permutations
- More memory-efficient than recursive backtracking
- Standard method for permutation generation
- Can handle larger n than recursive approach

**Algorithm:**
1. Start with the lexicographically smallest permutation
2. Generate next permutation using next_permutation algorithm
3. Continue until all permutations are generated
4. Output all permutations in lexicographic order

**Visual Example:**
```
Iterative approach: Generate next permutation
For n = 3, start with [1, 2, 3]:

1. [1, 2, 3] ← Initial permutation
2. [1, 3, 2] ← Next permutation
3. [2, 1, 3] ← Next permutation
4. [2, 3, 1] ← Next permutation
5. [3, 1, 2] ← Next permutation
6. [3, 2, 1] ← Final permutation
```

**Implementation:**
```python
def next_permutation(arr):
    n = len(arr)
    
    # Find the largest index i such that arr[i] < arr[i + 1]
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    
    if i == -1:
        return False  # No next permutation
    
    # Find the largest index j such that arr[i] < arr[j]
    j = n - 1
    while arr[j] <= arr[i]:
        j -= 1
    
    # Swap arr[i] and arr[j]
    arr[i], arr[j] = arr[j], arr[i]
    
    # Reverse the suffix starting at arr[i + 1]
    arr[i + 1:] = arr[i + 1:][::-1]
    
    return True

def permutations_iterative(n):
    arr = list(range(1, n + 1))
    result = [arr[:]]
    
    while next_permutation(arr):
        result.append(arr[:])
    
    return result

def solve_permutations_iterative():
    n = int(input())
    perms = permutations_iterative(n)
    
    print(len(perms))
    for perm in perms:
        print(' '.join(map(str, perm)))
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's better:**
- More memory-efficient than recursive approach
- Uses iterative next_permutation algorithm
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Built-in itertools.permutations (Optimal)

**Key Insights from Built-in Solution:**
- Use Python's optimized itertools.permutations
- Most efficient approach for permutation generation
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use itertools.permutations to generate all permutations
2. Convert permutations to required output format
3. Print count and all permutations
4. Leverage optimized built-in implementation

**Visual Example:**
```
Built-in approach: Use itertools.permutations
For n = 3:

import itertools
perms = list(itertools.permutations(range(1, 4)))
# Generates: [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

Output:
6
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
```

**Implementation:**
```python
from itertools import permutations

def solve_permutations():
    n = int(input())
    
    # Generate all permutations using built-in function
    perms = list(permutations(range(1, n + 1)))
    
    # Print output
    print(len(perms))
    for perm in perms:
        print(' '.join(map(str, perm)))

# Main execution
if __name__ == "__main__":
    solve_permutations()
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's optimal:**
- Uses optimized built-in implementation
- Most efficient approach for competitive programming
- Standard method for permutation generation
- Leverages Python's optimized algorithms

## 🎯 Problem Variations

### Variation 1: Permutations with Repetition
**Problem**: Generate all permutations when elements can be repeated.

**Link**: [CSES Problem Set - Permutations with Repetition](https://cses.fi/problemset/task/permutations_with_repetition)

```python
from itertools import product

def permutations_with_repetition(n, k):
    # Generate all k-length permutations with repetition
    return list(product(range(1, n + 1), repeat=k))
```

### Variation 2: Permutations of String
**Problem**: Generate all permutations of a given string.

**Link**: [CSES Problem Set - String Permutations](https://cses.fi/problemset/task/string_permutations)

```python
from itertools import permutations

def string_permutations(s):
    # Generate all permutations of string
    return [''.join(p) for p in permutations(s)]
```

### Variation 3: Next Permutation
**Problem**: Find the next lexicographically greater permutation.

**Link**: [CSES Problem Set - Next Permutation](https://cses.fi/problemset/task/next_permutation)

```python
def next_permutation(arr):
    n = len(arr)
    
    # Find the largest index i such that arr[i] < arr[i + 1]
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    
    if i == -1:
        return False  # No next permutation
    
    # Find the largest index j such that arr[i] < arr[j]
    j = n - 1
    while arr[j] <= arr[i]:
        j -= 1
    
    # Swap arr[i] and arr[j]
    arr[i], arr[j] = arr[j], arr[i]
    
    # Reverse the suffix starting at arr[i + 1]
    arr[i + 1:] = arr[i + 1:][::-1]
    
    return True
```

## 🔗 Related Problems

- **[Permutation Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Permutation problems
- **[Backtracking Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Backtracking problems
- **[Lexicographic Ordering Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Lexicographic ordering problems
- **[Combinatorics Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Combinatorics problems

## 📚 Learning Points

1. **Permutation Generation**: Essential for understanding combinatorial problems
2. **Backtracking**: Key technique for generating all possible arrangements
3. **Lexicographic Ordering**: Important for understanding systematic generation
4. **Combinatorics**: Critical for understanding factorial calculations
5. **Algorithm Optimization**: Foundation for many combinatorial algorithms
6. **Built-in Functions**: Critical for competitive programming efficiency

## 📝 Summary

The Permutations problem demonstrates permutation generation and lexicographic ordering concepts for systematic arrangement generation. We explored three approaches:

1. **Recursive Backtracking**: O(n! × n) time complexity using recursive backtracking, inefficient for large n
2. **Iterative Next Permutation**: O(n! × n) time complexity using iterative next_permutation algorithm, better approach for permutation generation
3. **Built-in itertools.permutations**: O(n! × n) time complexity with optimized built-in implementation, optimal approach for permutation generation

The key insights include understanding permutation generation principles, using backtracking for systematic arrangement generation, and applying built-in functions for optimal performance. This problem serves as an excellent introduction to combinatorial algorithms and permutation generation optimization.
