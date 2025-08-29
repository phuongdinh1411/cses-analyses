---
layout: simple
title: "Permutations"
permalink: /problem_soulutions/introductory_problems/permutations_analysis
---

# Permutations

## Problem Description

**Problem**: Generate all permutations of numbers from 1 to n.

**Input**: An integer n (1 ≤ n ≤ 8)

**Output**: 
- First line: number of permutations
- Next lines: each permutation on a separate line (in lexicographic order)

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Generate all possible arrangements of numbers 1 to n
- Output in lexicographic (alphabetical) order
- Count the total number of permutations

**Key Observations:**
- For n numbers, there are n! permutations
- We need to generate them in lexicographic order
- We can use built-in functions or implement manually

### Step 2: Using Built-in Permutations
**Idea**: Use Python's itertools.permutations to generate all permutations.

```python
from itertools import permutations

def solve_with_itertools(n):
    # Generate all permutations of range(1, n+1)
    perms = list(permutations(range(1, n + 1)))
    
    # Convert to strings for output
    result = []
    for perm in perms:
        result.append(' '.join(map(str, perm)))
    
    return result
```

**Why this works:**
- `itertools.permutations()` generates all possible arrangements
- Automatically generates in lexicographic order
- Simple and efficient

### Step 3: Manual Permutation Generation
**Idea**: Implement permutation generation manually using backtracking.

```python
def solve_manual(n):
    def generate_permutations(arr, start, result):
        if start == len(arr):
            result.append(arr[:])
            return
        
        for i in range(start, len(arr)):
            # Swap elements
            arr[start], arr[i] = arr[i], arr[start]
            generate_permutations(arr, start + 1, result)
            # Swap back
            arr[start], arr[i] = arr[i], arr[start]
    
    arr = list(range(1, n + 1))
    result = []
    generate_permutations(arr, 0, result)
    
    # Convert to strings
    return [' '.join(map(str, perm)) for perm in result]
```

**Why this works:**
- Backtracking generates all possible arrangements
- We swap elements to generate different permutations
- We restore the array after each recursive call

### Step 4: Complete Solution
**Putting it all together:**

```python
from itertools import permutations

def solve_permutations():
    n = int(input())
    
    # Generate all permutations
    perms = list(permutations(range(1, n + 1)))
    
    # Print output
    print(len(perms))
    for perm in perms:
        print(' '.join(map(str, perm)))

# Main execution
if __name__ == "__main__":
    solve_permutations()
```

**Why this works:**
- Simple and efficient using built-in functions
- Automatically generates in correct order
- Produces correct output format

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (1, 1),      # 1! = 1 permutation
        (2, 2),      # 2! = 2 permutations
        (3, 6),      # 3! = 6 permutations
    ]
    
    for n, expected_count in test_cases:
        result = solve_test(n)
        print(f"n = {n}")
        print(f"Expected count: {expected_count}")
        print(f"Got count: {len(result)}")
        print(f"First few permutations: {result[:3]}")
        print(f"{'✓ PASS' if len(result) == expected_count else '✗ FAIL'}")
        print()

def solve_test(n):
    perms = list(permutations(range(1, n + 1)))
    return [' '.join(map(str, perm)) for perm in perms]

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Generation**: O(n!) - we generate all n! permutations
- **Output**: O(n! × n) - converting to strings
- **Overall**: O(n! × n)

### Space Complexity
- O(n! × n) - storing all permutations

### Why This Solution Works
- **Complete**: Generates all possible arrangements
- **Correct**: Produces permutations in lexicographic order
- **Efficient**: Uses optimized built-in functions

## 🎯 Key Insights

### 1. **Permutation Counting**
- For n elements: n! permutations
- This grows very quickly with n

### 2. **Lexicographic Order**
- Built-in functions generate in correct order
- Or implement next_permutation algorithm

### 3. **Backtracking Pattern**
- Swap elements to generate different arrangements
- Restore array after each recursive call

## 🔗 Related Problems

- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: String permutations
- **[String Reorder](/cses-analyses/problem_soulutions/introductory_problems/string_reorder_analysis)**: String manipulation
- **[Gray Code](/cses-analyses/problem_soulutions/introductory_problems/gray_code_analysis)**: Generate sequences

## 🎯 Problem Variations

### Variation 1: K-th Permutation
**Problem**: Find k-th lexicographical permutation.

```python
def kth_permutation(n, k):
    from math import factorial
    
    numbers = list(range(1, n + 1))
    result = []
    k -= 1  # Convert to 0-based indexing
    
    for i in range(n, 0, -1):
        fact = factorial(i - 1)
        index = k // fact
        result.append(numbers.pop(index))
        k %= fact
    
    return result
```

### Variation 2: Constrained Permutations
**Problem**: Some numbers must maintain relative order.

```python
def constrained_permutations(n, constraints):
    # constraints: list of (a, b) where a must come before b
    # This is a more complex problem requiring topological sorting
    pass
```

### Variation 3: Partial Permutations
**Problem**: Generate permutations of length k from numbers 1 to n.

```python
def partial_permutations(n, k):
    from itertools import permutations
    return list(permutations(range(1, n + 1), k))
```

### Variation 4: Circular Permutations
**Problem**: Consider rotations as equivalent.

```python
def circular_permutations(n):
    # For circular permutations, divide by n
    from math import factorial
    return factorial(n) // n
```

### Variation 5: Permutations with Repetition
**Problem**: Generate permutations where some elements can repeat.

```python
def permutations_with_repetition(elements):
    from itertools import permutations
    return list(permutations(elements))
```

## 📚 Learning Points

1. **Combinatorics**: Understanding permutation counting
2. **Backtracking**: Manual permutation generation
3. **Built-in Functions**: Using language features efficiently
4. **Output Formatting**: Converting to required format

---

**This is a great introduction to combinatorics and backtracking!** 🎯 