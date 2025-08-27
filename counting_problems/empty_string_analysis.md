# CSES Empty String - Problem Analysis

## Problem Statement
Given a string s, you can perform the following operation: remove two adjacent equal characters. Count the number of different ways to reduce the string to an empty string.

### Input
The first input line has a string s.

### Output
Print one integer: the number of ways to reduce the string to empty.

### Constraints
- 1 ≤ |s| ≤ 100
- String contains only lowercase letters

### Example
```
Input:
aab

Output:
2
```

## Solution Progression

### Approach 1: Generate All Removal Sequences - O(n!)
**Description**: Generate all possible sequences of removing adjacent equal characters.

```python
def empty_string_naive(s):
    def can_remove(s, i):
        return i + 1 < len(s) and s[i] == s[i + 1]
    
    def remove_chars(s, i):
        return s[:i] + s[i + 2:]
    
    def count_ways(s):
        if len(s) == 0:
            return 1
        
        count = 0
        for i in range(len(s) - 1):
            if can_remove(s, i):
                new_s = remove_chars(s, i)
                count += count_ways(new_s)
        
        return count
    
    return count_ways(s)
```

**Why this is inefficient**: We need to try all possible removal sequences, leading to factorial time complexity.

### Improvement 1: Dynamic Programming with Memoization - O(n³)
**Description**: Use dynamic programming to avoid recalculating the same subproblems.

```python
def empty_string_dp(s):
    n = len(s)
    dp = {}
    
    def count_ways(left, right):
        if left > right:
            return 1
        
        if (left, right) in dp:
            return dp[(left, right)]
        
        count = 0
        
        # Try removing pairs of adjacent equal characters
        for i in range(left, right):
            if s[i] == s[i + 1]:
                # Remove characters at positions i and i+1
                count += count_ways(left, i - 1) * count_ways(i + 2, right)
        
        dp[(left, right)] = count
        return count
    
    return count_ways(0, n - 1)
```

**Why this improvement works**: Dynamic programming with memoization avoids recalculating the same subproblems.

## Final Optimal Solution

```python
s = input().strip()

def count_empty_string_ways(s):
    n = len(s)
    dp = {}
    
    def count_ways(left, right):
        if left > right:
            return 1
        
        if (left, right) in dp:
            return dp[(left, right)]
        
        count = 0
        
        # Try removing pairs of adjacent equal characters
        for i in range(left, right):
            if s[i] == s[i + 1]:
                # Remove characters at positions i and i+1
                count += count_ways(left, i - 1) * count_ways(i + 2, right)
        
        dp[(left, right)] = count
        return count
    
    return count_ways(0, n - 1)

result = count_empty_string_ways(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n!) | O(n) | Generate all removal sequences |
| Dynamic Programming | O(n³) | O(n²) | Use memoization to avoid recalculation |

## Key Insights for Other Problems

### 1. **String Reduction Problems**
**Principle**: Use dynamic programming to count different ways to reduce strings.
**Applicable to**: String problems, reduction problems, counting problems

### 2. **Dynamic Programming with Memoization**
**Principle**: Store results of subproblems to avoid recalculating.
**Applicable to**: Optimization problems, counting problems, recursive problems

### 3. **Adjacent Character Removal**
**Principle**: Focus on removing adjacent equal characters systematically.
**Applicable to**: String manipulation problems, pattern matching problems

## Notable Techniques

### 1. **Dynamic Programming Pattern**
```python
def dp_with_memoization(s):
    n = len(s)
    dp = {}
    
    def solve(left, right):
        if left > right:
            return 1
        
        if (left, right) in dp:
            return dp[(left, right)]
        
        # Solve subproblem
        result = solve_subproblem(left, right)
        dp[(left, right)] = result
        return result
    
    return solve(0, n - 1)
```

### 2. **Adjacent Pair Removal**
```python
def remove_adjacent_pairs(s, left, right):
    count = 0
    
    for i in range(left, right):
        if s[i] == s[i + 1]:
            # Remove characters at positions i and i+1
            count += solve(left, i - 1) * solve(i + 2, right)
    
    return count
```

### 3. **String Reduction Check**
```python
def can_reduce_to_empty(s):
    if len(s) == 0:
        return True
    
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            new_s = s[:i] + s[i + 2:]
            if can_reduce_to_empty(new_s):
                return True
    
    return False
```

## Problem-Solving Framework

1. **Identify problem type**: This is a string reduction counting problem
2. **Choose approach**: Use dynamic programming with memoization
3. **Define subproblems**: Count ways to reduce substring [left, right]
4. **Implement recursion**: Try removing adjacent equal pairs
5. **Count results**: Sum up all valid reduction sequences

---

*This analysis shows how to efficiently count ways to reduce a string to empty using dynamic programming with memoization.* 