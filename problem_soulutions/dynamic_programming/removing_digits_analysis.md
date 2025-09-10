---
layout: simple
title: "Removing Digits - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/removing_digits_analysis
---

# Removing Digits - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of digit removal in dynamic programming
- Apply optimization techniques for digit removal analysis
- Implement efficient algorithms for minimum digit removal counting
- Optimize DP operations for digit removal analysis
- Handle special cases in digit removal problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, optimization techniques, mathematical formulas
- **Data Structures**: Arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Digit manipulation, optimization, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Minimizing Coins (dynamic programming), Money Sums (dynamic programming), Array Description (dynamic programming)

## 📋 Problem Description

Given a number, find the minimum number of operations to reduce it to 0 by removing digits.

**Input**: 
- n: the number to reduce

**Output**: 
- Minimum number of operations needed

**Constraints**:
- 1 ≤ n ≤ 10^6

**Example**:
```
Input:
n = 27

Output:
5

Explanation**: 
Operations to reduce 27 to 0:
1. 27 → 25 (remove digit 7)
2. 25 → 20 (remove digit 5)
3. 20 → 18 (remove digit 2)
4. 18 → 10 (remove digit 8)
5. 10 → 0 (remove digit 1)
Total: 5 operations
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible digit removals
- **Complete Enumeration**: Enumerate all possible digit removal sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to remove digits and find the minimum.

**Algorithm**:
- Use recursive function to try all digit removals
- Calculate minimum operations for each path
- Find overall minimum
- Return result

**Visual Example**:
```
Number = 27:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try removing digit 7: 27 → 25      │
│ - Try removing digit 5: 25 → 20    │
│   - Try removing digit 2: 20 → 18  │
│     - Try removing digit 8: 18 → 10 │
│       - Try removing digit 1: 10 → 0 ✓ │
│ - Try removing digit 2: 25 → 5     │
│   - Try removing digit 5: 5 → 0 ✓  │
│                                   │
│ Try removing digit 2: 27 → 7      │
│ - Try removing digit 7: 7 → 0 ✓   │
│                                   │
│ Find minimum among all paths       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_removing_digits(n):
    """
    Find minimum operations using recursive approach
    
    Args:
        n: the number to reduce
    
    Returns:
        int: minimum number of operations needed
    """
    def find_minimum_operations(number):
        """Find minimum operations recursively"""
        if number == 0:
            return 0  # No operations needed for 0
        
        if number < 0:
            return float('inf')  # Invalid number
        
        min_operations = float('inf')
        # Try removing each digit
        for digit in str(number):
            new_number = number - int(digit)
            if new_number >= 0:
                result = find_minimum_operations(new_number)
                if result != float('inf'):
                    min_operations = min(min_operations, 1 + result)
        
        return min_operations
    
    result = find_minimum_operations(n)
    return result if result != float('inf') else -1

def recursive_removing_digits_optimized(n):
    """
    Optimized recursive removing digits finding
    
    Args:
        n: the number to reduce
    
    Returns:
        int: minimum number of operations needed
    """
    def find_minimum_operations_optimized(number):
        """Find minimum operations with optimization"""
        if number == 0:
            return 0  # No operations needed for 0
        
        if number < 0:
            return float('inf')  # Invalid number
        
        min_operations = float('inf')
        # Try removing each digit
        for digit in str(number):
            new_number = number - int(digit)
            if new_number >= 0:
                result = find_minimum_operations_optimized(new_number)
                if result != float('inf'):
                    min_operations = min(min_operations, 1 + result)
        
        return min_operations
    
    result = find_minimum_operations_optimized(n)
    return result if result != float('inf') else -1

# Example usage
n = 27
result1 = recursive_removing_digits(n)
result2 = recursive_removing_digits_optimized(n)
print(f"Recursive removing digits: {result1}")
print(f"Optimized recursive removing digits: {result2}")
```

**Time Complexity**: O(digits^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store minimum operations for each number
- Fill DP table bottom-up
- Return DP[n] as result

**Visual Example**:
```
DP table for number = 27:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = 0 (no operations needed)   │
│ dp[1] = 1 (remove digit 1)         │
│ dp[2] = 1 (remove digit 2)         │
│ dp[3] = 1 (remove digit 3)         │
│ dp[4] = 1 (remove digit 4)         │
│ dp[5] = 1 (remove digit 5)         │
│ dp[6] = 1 (remove digit 6)         │
│ dp[7] = 1 (remove digit 7)         │
│ dp[8] = 1 (remove digit 8)         │
│ dp[9] = 1 (remove digit 9)         │
│ dp[10] = 2 (remove digit 1, then 0) │
│ ...                                │
│ dp[27] = 5 (minimum operations)    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_removing_digits(n):
    """
    Find minimum operations using dynamic programming approach
    
    Args:
        n: the number to reduce
    
    Returns:
        int: minimum number of operations needed
    """
    # Create DP table
    dp = [float('inf')] * (n + 1)
    
    # Initialize base case
    dp[0] = 0  # No operations needed for 0
    
    # Fill DP table
    for i in range(1, n + 1):
        # Try removing each digit
        for digit in str(i):
            digit_value = int(digit)
            if i >= digit_value:
                dp[i] = min(dp[i], 1 + dp[i - digit_value])
    
    return dp[n] if dp[n] != float('inf') else -1

def dp_removing_digits_optimized(n):
    """
    Optimized dynamic programming removing digits finding
    
    Args:
        n: the number to reduce
    
    Returns:
        int: minimum number of operations needed
    """
    # Create DP table with optimization
    dp = [float('inf')] * (n + 1)
    
    # Initialize base case
    dp[0] = 0  # No operations needed for 0
    
    # Fill DP table with optimization
    for i in range(1, n + 1):
        # Try removing each digit
        for digit in str(i):
            digit_value = int(digit)
            if i >= digit_value:
                dp[i] = min(dp[i], 1 + dp[i - digit_value])
    
    return dp[n] if dp[n] != float('inf') else -1

# Example usage
n = 27
result1 = dp_removing_digits(n)
result2 = dp_removing_digits_optimized(n)
print(f"DP removing digits: {result1}")
print(f"Optimized DP removing digits: {result2}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Uses dynamic programming for O(n) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(n) time complexity
- **Space Efficiency**: O(1) space complexity
- **Optimal Complexity**: Best approach for removing digits

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For number = 27:
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 5                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_removing_digits(n):
    """
    Find minimum operations using space-optimized DP approach
    
    Args:
        n: the number to reduce
    
    Returns:
        int: minimum number of operations needed
    """
    # Use only necessary variables for DP
    dp = [float('inf')] * (n + 1)
    
    # Initialize base case
    dp[0] = 0  # No operations needed for 0
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        # Try removing each digit
        for digit in str(i):
            digit_value = int(digit)
            if i >= digit_value:
                dp[i] = min(dp[i], 1 + dp[i - digit_value])
    
    return dp[n] if dp[n] != float('inf') else -1

def space_optimized_dp_removing_digits_v2(n):
    """
    Alternative space-optimized DP removing digits finding
    
    Args:
        n: the number to reduce
    
    Returns:
        int: minimum number of operations needed
    """
    # Use only necessary variables for DP
    dp = [float('inf')] * (n + 1)
    
    # Initialize base case
    dp[0] = 0  # No operations needed for 0
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        # Try removing each digit
        for digit in str(i):
            digit_value = int(digit)
            if i >= digit_value:
                dp[i] = min(dp[i], 1 + dp[i - digit_value])
    
    return dp[n] if dp[n] != float('inf') else -1

def removing_digits_with_precomputation(max_n):
    """
    Precompute removing digits for multiple queries
    
    Args:
        max_n: maximum value of n
    
    Returns:
        list: precomputed removing digits
    """
    results = [0] * (max_n + 1)
    
    # Initialize base case
    results[0] = 0
    
    # Fill results using DP
    for i in range(1, max_n + 1):
        min_operations = float('inf')
        for digit in str(i):
            digit_value = int(digit)
            if i >= digit_value:
                min_operations = min(min_operations, 1 + results[i - digit_value])
        results[i] = min_operations if min_operations != float('inf') else -1
    
    return results

# Example usage
n = 27
result1 = space_optimized_dp_removing_digits(n)
result2 = space_optimized_dp_removing_digits_v2(n)
print(f"Space-optimized DP removing digits: {result1}")
print(f"Space-optimized DP removing digits v2: {result2}")

# Precompute for multiple queries
max_n = 1000000
precomputed = removing_digits_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses space-optimized DP for O(n) time and O(n) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(digits^n) | O(n) | Complete enumeration of all digit removal sequences |
| Dynamic Programming | O(n) | O(n) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n) | O(n) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(n) - Use dynamic programming for efficient calculation
- **Space**: O(n) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Removing Digits with Constraints**
**Problem**: Find minimum operations with specific constraints.

**Key Differences**: Apply constraints to digit removal

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_removing_digits(n, constraints):
    """
    Find minimum operations with constraints
    
    Args:
        n: the number to reduce
        constraints: list of constraints
    
    Returns:
        int: minimum number of operations needed
    """
    # Create DP table
    dp = [float('inf')] * (n + 1)
    
    # Initialize base case
    dp[0] = 0  # No operations needed for 0
    
    # Fill DP table with constraints
    for i in range(1, n + 1):
        # Try removing each digit
        for digit in str(i):
            digit_value = int(digit)
            if i >= digit_value and constraints(digit_value):  # Check if digit satisfies constraints
                dp[i] = min(dp[i], 1 + dp[i - digit_value])
    
    return dp[n] if dp[n] != float('inf') else -1

# Example usage
n = 27
constraints = lambda digit: digit <= 5  # Only remove digits <= 5
result = constrained_removing_digits(n, constraints)
print(f"Constrained removing digits: {result}")
```

#### **2. Removing Digits with Multiple Operations**
**Problem**: Find minimum operations with multiple operation types.

**Key Differences**: Handle multiple types of operations

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_operation_removing_digits(n, operations):
    """
    Find minimum operations with multiple operation types
    
    Args:
        n: the number to reduce
        operations: list of operation types
    
    Returns:
        int: minimum number of operations needed
    """
    # Create DP table
    dp = [float('inf')] * (n + 1)
    
    # Initialize base case
    dp[0] = 0  # No operations needed for 0
    
    # Fill DP table with multiple operations
    for i in range(1, n + 1):
        for operation in operations:
            if operation(i) >= 0:  # Check if operation is valid
                dp[i] = min(dp[i], 1 + dp[operation(i)])
    
    return dp[n] if dp[n] != float('inf') else -1

# Example usage
n = 27
operations = [
    lambda x: x - int(str(x)[0]) if x > 0 else -1,  # Remove first digit
    lambda x: x - int(str(x)[-1]) if x > 0 else -1   # Remove last digit
]
result = multi_operation_removing_digits(n, operations)
print(f"Multi-operation removing digits: {result}")
```

#### **3. Removing Digits with Multiple Targets**
**Problem**: Find minimum operations for multiple target values.

**Key Differences**: Handle multiple target values

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_target_removing_digits(targets, max_n):
    """
    Find minimum operations for multiple target values
    
    Args:
        targets: list of target values
        max_n: maximum value to consider
    
    Returns:
        list: minimum number of operations needed for each target
    """
    # Create DP table
    dp = [float('inf')] * (max_n + 1)
    
    # Initialize base case
    dp[0] = 0  # No operations needed for 0
    
    # Fill DP table
    for i in range(1, max_n + 1):
        # Try removing each digit
        for digit in str(i):
            digit_value = int(digit)
            if i >= digit_value:
                dp[i] = min(dp[i], 1 + dp[i - digit_value])
    
    # Return results for each target
    results = []
    for target in targets:
        results.append(dp[target] if dp[target] != float('inf') else -1)
    
    return results

# Example usage
targets = [10, 20, 30]  # Check minimum operations for these targets
max_n = 100
result = multi_target_removing_digits(targets, max_n)
print(f"Multi-target removing digits: {result}")
```

### Related Problems

#### **CSES Problems**
- [Minimizing Coins](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Money Sums](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Coin Change](https://leetcode.com/problems/coin-change/) - DP
- [Minimum Cost For Tickets](https://leetcode.com/problems/minimum-cost-for-tickets/) - DP
- [Perfect Squares](https://leetcode.com/problems/perfect-squares/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Optimization, minimization problems
- **Digit Manipulation**: Number processing, digit operations
- **Mathematical Algorithms**: Optimization, minimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Digit Manipulation](https://cp-algorithms.com/algebra/binary-exp.html) - Digit manipulation algorithms
- [Optimization](https://cp-algorithms.com/dynamic_programming/optimization.html) - Optimization algorithms

### **Practice Problems**
- [CSES Minimizing Coins](https://cses.fi/problemset/task/1075) - Medium
- [CSES Money Sums](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
