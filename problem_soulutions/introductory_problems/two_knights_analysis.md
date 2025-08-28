---
layout: simple
title: "Two Knights
permalink: /problem_soulutions/introductory_problems/two_knights_analysis/"
---


# Two Knights

## Problem Statement
Your task is to count for k=1,2,…,n the number of ways two knights can be placed on a k×k chessboard so that they do not attack each other.

### Input
The only input line contains an integer n.

### Output
Print n lines: the kth line contains the number of ways two knights can be placed on a k×k chessboard.

### Constraints
- 1 ≤ n ≤ 10000

### Example
```
Input:
8

Output:
0
6
28
96
252
550
1056
1848
```

## Solution Progression

### Approach 1: Brute Force - O(n⁴)
**Description**: For each board size, try all possible positions for two knights and check if they attack each other.

```python
def two_knights_brute_force(n):
    def can_attack(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
    
    def count_ways(k):
        total_positions = k * k
        ways = 0
        
        for i in range(total_positions):
            for j in range(i + 1, total_positions):
                pos1 = (i // k, i % k)
                pos2 = (j // k, j % k)
                if not can_attack(pos1, pos2):
                    ways += 1
        
        return ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```"
**Why this is inefficient**: For each board size k, we're trying all possible pairs of positions, which leads to O(k⁴) complexity. For n board sizes, this becomes O(n⁵).

### Improvement 1: Mathematical Formula - O(n)
**Description**: Use mathematical formulas to calculate the number of ways directly.

```python
def two_knights_math(n):
    def count_ways(k):
        if k < 2:
            return 0
        
        # Total ways to place two knights
        total_ways = (k * k) * (k * k - 1) // 2
        
        # Ways where knights attack each other
        attacking_ways = 0
        
        # Count attacking positions
        for i in range(k):
            for j in range(k):
                # Check all 8 possible knight moves
                moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                for ni, nj in moves:
                    if 0 <= ni < k and 0 <= nj < k:
                        attacking_ways += 1
        
        # Each attacking pair is counted twice, so divide by 2
        attacking_ways //= 2
        
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

**Why this improvement works**: Instead of checking all pairs, we calculate the total number of ways to place two knights and subtract the number of attacking positions.

### Improvement 2: Optimized Formula - O(n)
**Description**: Use a more efficient formula that directly calculates the result.

```python
def two_knights_optimized(n):
    def count_ways(k):
        if k < 2:
            return 0
        
        # Total ways to place two knights
        total_ways = (k * k) * (k * k - 1) // 2
        
        # For each position, count valid knight moves
        attacking_ways = 0
        for i in range(k):
            for j in range(k):
                # Count valid knight moves from this position
                valid_moves = 0
                moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                for ni, nj in moves:
                    if 0 <= ni < k and 0 <= nj < k:
                        valid_moves += 1
                
                attacking_ways += valid_moves
        
        # Each attacking pair is counted twice
        attacking_ways //= 2
        
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

**Why this improvement works**: This approach is more efficient as it directly calculates the attacking positions without redundant checks.

### Alternative: Closed Formula - O(n)
**Description**: Use a closed mathematical formula for the result.

```python
def two_knights_closed_formula(n):
    def count_ways(k):
        if k < 2:
            return 0
        
        # Closed formula: (k²(k²-1))/2 - 4(k-1)(k-2)
        total_ways = (k * k) * (k * k - 1) // 2
        attacking_ways = 4 * (k - 1) * (k - 2)
        
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

**Why this works**: This closed formula directly gives the result without any loops, making it the most efficient approach.

## Final Optimal Solution

```python
n = int(input())

for k in range(1, n + 1):
    if k < 2:
        print(0)
    else:
        # Closed formula: (k²(k²-1))/2 - 4(k-1)(k-2)
        total_ways = (k * k) * (k * k - 1) // 2
        attacking_ways = 4 * (k - 1) * (k - 2)
        result = total_ways - attacking_ways
        print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n⁵) | O(1) | Check all possible pairs |
| Mathematical Formula | O(n³) | O(1) | Calculate total and subtract attacking |
| Optimized Formula | O(n³) | O(1) | More efficient calculation |
| Closed Formula | O(n) | O(1) | Direct mathematical formula |

## Key Insights for Other Problems

### 1. **Combinatorial Counting**
**Principle**: Use combinatorial formulas to count possibilities efficiently.
**Applicable to**:
- Counting problems
- Combinatorial problems
- Probability problems
- Mathematical problems

**Example Problems**:
- Two knights
- Counting combinations
- Probability problems
- Mathematical counting

### 2. **Mathematical Formula Derivation**
**Principle**: Derive mathematical formulas to solve problems efficiently.
**Applicable to**:
- Mathematical problems
- Formula derivation
- Algorithm optimization
- Pattern recognition

**Example Problems**:
- Mathematical sequences
- Formula problems
- Algorithm optimization
- Pattern recognition

### 3. **Geometric Pattern Recognition**
**Principle**: Recognize geometric patterns and use them to simplify problems.
**Applicable to**:
- Geometric problems
- Pattern recognition
- Mathematical problems
- Algorithm design

**Example Problems**:
- Geometric algorithms
- Pattern recognition
- Mathematical problems
- Algorithm design

### 4. **Inclusion-Exclusion Principle**
**Principle**: Use inclusion-exclusion to count valid configurations.
**Applicable to**:
- Counting problems
- Set theory
- Combinatorial problems
- Mathematical problems

**Example Problems**:
- Set counting
- Combinatorial problems
- Mathematical counting
- Probability problems

## Notable Techniques

### 1. **Combinatorial Counting Pattern**
```python
# Count total possibilities and subtract invalid ones
def count_valid_configurations(total, invalid):
    return total - invalid
```

### 2. **Mathematical Formula Pattern**
```python
# Use closed formula for efficiency
def solve_with_formula(inputs):
    return closed_formula(inputs)
```

### 3. **Geometric Pattern Recognition**
```python
# Recognize geometric patterns
def count_geometric_patterns(size):
    # Apply geometric formula
    return geometric_formula(size)
```

## Edge Cases to Remember

1. **k = 1**: No valid configurations (0 ways)
2. **k = 2**: Only 6 valid configurations
3. **Large k**: Handle efficiently with formulas
4. **Integer overflow**: Handle large numbers properly
5. **Multiple test cases**: Process each case independently

## Problem-Solving Framework

1. **Identify counting nature**: This is about counting valid configurations
2. **Use combinatorial approach**: Calculate total and subtract invalid
3. **Derive formulas**: Use mathematical analysis to find closed formulas
4. **Handle edge cases**: Consider special cases and boundaries
5. **Optimize for efficiency**: Use O(1) formulas instead of brute force

---

*This analysis shows how to efficiently count valid configurations using mathematical formulas.* 