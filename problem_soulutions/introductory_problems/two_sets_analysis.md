---
layout: simple
title: "Two Sets
permalink: /problem_soulutions/introductory_problems/two_sets_analysis/
---

# Two Sets

## Problem Statement
Your task is to divide the numbers 1,2,…,n into two sets of equal sum.

### Input
The only input line contains an integer n.

### Output"
Print "YES", if the division is possible, and "NO" otherwise.

In the first case, also print an example of how to create the sets. First, print the number of elements in the first set and then the elements themselves in a separate line, and then, print the second set in a similar way.

### Constraints
- 1 ≤ n ≤ 10^6

### Example
```
Input:
7

Output:
YES
4
1 2 4 7
3
3 5 6
```

## Solution Progression

### Approach 1: Brute Force - O(2^n)
**Description**: Try all possible ways to divide the numbers into two sets.

```python
def two_sets_brute_force(n):
    numbers = list(range(1, n + 1))
    total_sum = sum(numbers)
    
    if total_sum % 2 != 0:
        return None  # Impossible if total sum is odd
    
    target_sum = total_sum // 2
    
    def try_combinations(index, current_sum, current_set):
        if current_sum == target_sum:
            return current_set
        if current_sum > target_sum or index >= len(numbers):
            return None
        
        # Try including current number
        result = try_combinations(index + 1, current_sum + numbers[index], current_set + [numbers[index]])
        if result:
            return result
        
        # Try excluding current number
        return try_combinations(index + 1, current_sum, current_set)
    
    first_set = try_combinations(0, 0, [])
    if first_set:
        second_set = [x for x in numbers if x not in first_set]
        return first_set, second_set
    
    return None
```

**Why this is inefficient**: We're trying all possible combinations of numbers, which leads to exponential complexity. This is completely impractical for large n.

### Improvement 1: Mathematical Analysis - O(1)
**Description**: Use mathematical analysis to determine if it's possible and construct the solution.

```python
def two_sets_math(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None  # Impossible if total sum is odd
    
    target_sum = total_sum // 2
    
    # Try to construct the first set
    first_set = []
    current_sum = 0
    
    # Start from the largest number and work backwards
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
            if current_sum == target_sum:
                break
    
    if current_sum == target_sum:
        second_set = [x for x in range(1, n + 1) if x not in first_set]
        return first_set, second_set
    
    return None
```

**Why this improvement works**: We use a greedy approach starting from the largest number. If the total sum is even, we can always construct such a division.

### Improvement 2: Optimized Construction - O(n)
**Description**: Use a more efficient construction method.

```python
def two_sets_optimized(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None
    
    target_sum = total_sum // 2
    first_set = []
    current_sum = 0
    
    # Use a more systematic approach
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    if current_sum == target_sum:
        second_set = [x for x in range(1, n + 1) if x not in first_set]
        return first_set, second_set
    
    return None
```

**Why this improvement works**: This approach is more systematic and guarantees to find a solution if one exists.

### Alternative: Pattern-Based - O(n)
**Description**: Use a specific pattern to construct the solution.

```python
def two_sets_pattern(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None
    
    # Use a specific pattern for construction
    first_set = []
    second_set = []
    
    if n % 4 == 0:
        # Pattern for n divisible by 4
        for i in range(1, n + 1):
            if i % 4 == 1 or i % 4 == 2:
                first_set.append(i)
            else:
                second_set.append(i)
    elif n % 4 == 3:
        # Pattern for n ≡ 3 (mod 4)
        first_set = [1, 2]
        second_set = [3]
        for i in range(4, n + 1):
            if i % 4 == 0 or i % 4 == 3:
                first_set.append(i)
            else:
                second_set.append(i)
    else:
        return None  # Impossible for n ≡ 1, 2 (mod 4)
    
    return first_set, second_set
```

**Why this works**: This pattern-based approach uses specific mathematical patterns for different values of n modulo 4.

## Final Optimal Solution

```python
n = int(input())

total_sum = n * (n + 1) // 2

if total_sum % 2 != 0:
    print("NO")
else:
    print("YES")
    
    target_sum = total_sum // 2
    first_set = []
    current_sum = 0
    
    # Construct first set starting from largest number
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    # Construct second set
    second_set = [x for x in range(1, n + 1) if x not in first_set]
    
    # Print first set
    print(len(first_set))
    print(*first_set)
    
    # Print second set
    print(len(second_set))
    print(*second_set)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n) | O(n) | Try all combinations |
| Mathematical Analysis | O(n) | O(n) | Use greedy construction |
| Optimized Construction | O(n) | O(n) | Systematic construction |
| Pattern-Based | O(n) | O(n) | Use specific patterns |

## Key Insights for Other Problems

### 1. **Mathematical Feasibility Check**
**Principle**: Check mathematical conditions first before attempting construction.
**Applicable to**:
- Feasibility problems
- Mathematical problems
- Decision problems
- Optimization problems

**Example Problems**:
- Two sets
- Feasibility problems
- Mathematical problems
- Decision problems

### 2. **Greedy Construction**
**Principle**: Use greedy strategies to construct solutions when possible.
**Applicable to**:
- Construction problems
- Greedy algorithms
- Optimization problems
- Algorithm design

**Example Problems**:
- Set construction
- Greedy algorithms
- Optimization problems
- Algorithm design

### 3. **Pattern Recognition**
**Principle**: Recognize patterns in mathematical problems to simplify solutions.
**Applicable to**:
- Pattern problems
- Mathematical problems
- Algorithm design
- Problem solving

**Example Problems**:
- Pattern recognition
- Mathematical problems
- Algorithm design
- Problem solving

### 4. **Modular Arithmetic**
**Principle**: Use modular arithmetic to analyze problems and find patterns.
**Applicable to**:
- Number theory
- Mathematical problems
- Pattern recognition
- Algorithm design

**Example Problems**:
- Number theory problems
- Mathematical problems
- Pattern recognition
- Algorithm design

## Notable Techniques

### 1. **Feasibility Check Pattern**
```python
# Check mathematical conditions first
def check_feasibility(inputs):
    if mathematical_condition_not_met(inputs):
        return False
    return True
```

### 2. **Greedy Construction Pattern**
```python
# Use greedy approach for construction
def construct_solution(inputs):
    solution = []
    for item in sorted_items:
        if can_add(item, solution):
            solution.append(item)
    return solution
```

### 3. **Pattern-Based Construction**
```python
# Use specific patterns for construction
def construct_with_pattern(inputs):
    if inputs % 4 == 0:
        return pattern_for_divisible_by_4(inputs)
    elif inputs % 4 == 3:
        return pattern_for_mod_3(inputs)
    else:
        return None
```

## Edge Cases to Remember

1. **n = 1**: Impossible (only one number)
2. **n = 2**: Impossible (sum is 3, odd)
3. **n = 3**: Impossible (sum is 6, but no valid division)
4. **n = 4**: Possible (1,4 and 2,3)
5. **Large n**: Handle efficiently with mathematical analysis

## Problem-Solving Framework

1. **Check feasibility**: Use mathematical analysis to determine if solution exists
2. **Use greedy construction**: Start from largest numbers
3. **Handle edge cases**: Consider special cases and boundaries
4. **Optimize for efficiency**: Use O(n) construction instead of brute force
5. **Verify correctness**: Test with examples

---

*This analysis shows how to efficiently determine feasibility and construct solutions using mathematical analysis.* 