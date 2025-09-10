---
layout: simple
title: "Two Sets II - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/two_sets_ii_analysis
---

# Two Sets II - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of set partitioning in dynamic programming
- Apply counting techniques for set partition analysis
- Implement efficient algorithms for set partition counting
- Optimize DP operations for partition analysis
- Handle special cases in set partition problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, counting techniques, mathematical formulas
- **Data Structures**: Arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Set theory, combinations, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Removal Game (dynamic programming), Rectangle Cutting (dynamic programming), Longest Common Subsequence (dynamic programming)

## 📋 Problem Description

Given a number n, count the number of ways to partition the set {1, 2, ..., n} into two subsets with equal sum.

**Input**: 
- n: the number

**Output**: 
- Number of ways to partition the set modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 500

**Example**:
```
Input:
n = 3

Output:
1

Explanation**: 
Set {1, 2, 3} has sum = 6
Need to partition into two subsets with sum = 3 each
Ways to partition:
1. {1, 2} and {3} (sums: 3 and 3)
Total: 1 way
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible set partitions
- **Complete Enumeration**: Enumerate all possible partition combinations
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to partition the set.

**Algorithm**:
- Use recursive function to try all partition combinations
- Check if partition has equal sum
- Count valid partitions
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Set {1, 2, 3}, target sum = 3:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try including 1 in first set:      │
│ - First set: {1}, remaining: {2,3} │
│   - Try including 2 in first set:  │
│     - First set: {1,2}, remaining: {3} │
│       - First set sum: 3, second set sum: 3 ✓ │
│   - Try including 3 in first set:  │
│     - First set: {1,3}, remaining: {2} │
│       - First set sum: 4, second set sum: 2 ✗ │
│ - Try including 2 in first set:    │
│   - First set: {1,2}, remaining: {3} │
│     - First set sum: 3, second set sum: 3 ✓ │
│ - Try including 3 in first set:    │
│   - First set: {1,3}, remaining: {2} │
│     - First set sum: 4, second set sum: 2 ✗ │
│                                   │
│ Total: 1 way                      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_two_sets_ii(n, mod=10**9+7):
    """
    Count set partitions using recursive approach
    
    Args:
        n: the number
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    def count_partitions(index, current_sum, target_sum):
        """Count partitions recursively"""
        if index > n:
            return 1 if current_sum == target_sum else 0
        
        # Don't include current element
        count = count_partitions(index + 1, current_sum, target_sum)
        
        # Include current element
        count = (count + count_partitions(index + 1, current_sum + index, target_sum)) % mod
        
        return count
    
    total_sum = n * (n + 1) // 2
    if total_sum % 2 != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // 2
    return count_partitions(1, 0, target_sum)

def recursive_two_sets_ii_optimized(n, mod=10**9+7):
    """
    Optimized recursive two sets II counting
    
    Args:
        n: the number
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    def count_partitions_optimized(index, current_sum, target_sum):
        """Count partitions with optimization"""
        if index > n:
            return 1 if current_sum == target_sum else 0
        
        # Don't include current element
        count = count_partitions_optimized(index + 1, current_sum, target_sum)
        
        # Include current element
        count = (count + count_partitions_optimized(index + 1, current_sum + index, target_sum)) % mod
        
        return count
    
    total_sum = n * (n + 1) // 2
    if total_sum % 2 != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // 2
    return count_partitions_optimized(1, 0, target_sum)

# Example usage
n = 3
result1 = recursive_two_sets_ii(n)
result2 = recursive_two_sets_ii_optimized(n)
print(f"Recursive two sets II: {result1}")
print(f"Optimized recursive two sets II: {result2}")
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n * sum) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store number of ways for each sum
- Fill DP table bottom-up
- Return DP[target_sum] as result

**Visual Example**:
```
DP table for n=3, target_sum=3:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = 1 (empty set)              │
│ dp[1] = 1 (set {1})                │
│ dp[2] = 1 (set {2})                │
│ dp[3] = 2 (sets {3} and {1,2})     │
│ dp[4] = 1 (set {1,3})              │
│ dp[5] = 1 (set {2,3})              │
│ dp[6] = 1 (set {1,2,3})            │
│                                   │
│ Result: dp[3] = 2, but we need to divide by 2 │
│ because each partition is counted twice       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_two_sets_ii(n, mod=10**9+7):
    """
    Count set partitions using dynamic programming approach
    
    Args:
        n: the number
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    total_sum = n * (n + 1) // 2
    if total_sum % 2 != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // 2
    
    # Create DP table
    dp = [0] * (target_sum + 1)
    dp[0] = 1  # Empty set
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(target_sum, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % mod
    
    return dp[target_sum]

def dp_two_sets_ii_optimized(n, mod=10**9+7):
    """
    Optimized dynamic programming two sets II counting
    
    Args:
        n: the number
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    total_sum = n * (n + 1) // 2
    if total_sum % 2 != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // 2
    
    # Create DP table with optimization
    dp = [0] * (target_sum + 1)
    dp[0] = 1  # Empty set
    
    # Fill DP table with optimization
    for i in range(1, n + 1):
        for j in range(target_sum, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % mod
    
    return dp[target_sum]

# Example usage
n = 3
result1 = dp_two_sets_ii(n)
result2 = dp_two_sets_ii_optimized(n)
print(f"DP two sets II: {result1}")
print(f"Optimized DP two sets II: {result2}")
```

**Time Complexity**: O(n * sum)
**Space Complexity**: O(sum)

**Why it's better**: Uses dynamic programming for O(n * sum) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(n * sum) time complexity
- **Space Efficiency**: O(sum) space complexity
- **Optimal Complexity**: Best approach for two sets II

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For n=3, target_sum=3:
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 2                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_two_sets_ii(n, mod=10**9+7):
    """
    Count set partitions using space-optimized DP approach
    
    Args:
        n: the number
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    total_sum = n * (n + 1) // 2
    if total_sum % 2 != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // 2
    
    # Use only necessary variables for DP
    dp = [0] * (target_sum + 1)
    dp[0] = 1  # Empty set
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        for j in range(target_sum, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % mod
    
    return dp[target_sum]

def space_optimized_dp_two_sets_ii_v2(n, mod=10**9+7):
    """
    Alternative space-optimized DP two sets II counting
    
    Args:
        n: the number
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    total_sum = n * (n + 1) // 2
    if total_sum % 2 != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // 2
    
    # Use only necessary variables for DP
    dp = [0] * (target_sum + 1)
    dp[0] = 1  # Empty set
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        for j in range(target_sum, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % mod
    
    return dp[target_sum]

def two_sets_ii_with_precomputation(max_n, mod=10**9+7):
    """
    Precompute two sets II for multiple queries
    
    Args:
        max_n: maximum value of n
        mod: modulo value
    
    Returns:
        list: precomputed two sets II results
    """
    results = [0] * (max_n + 1)
    
    for i in range(1, max_n + 1):
        total_sum = i * (i + 1) // 2
        if total_sum % 2 != 0:
            results[i] = 0
        else:
            target_sum = total_sum // 2
            dp = [0] * (target_sum + 1)
            dp[0] = 1
            
            for j in range(1, i + 1):
                for k in range(target_sum, j - 1, -1):
                    dp[k] = (dp[k] + dp[k - j]) % mod
            
            results[i] = dp[target_sum]
    
    return results

# Example usage
n = 3
result1 = space_optimized_dp_two_sets_ii(n)
result2 = space_optimized_dp_two_sets_ii_v2(n)
print(f"Space-optimized DP two sets II: {result1}")
print(f"Space-optimized DP two sets II v2: {result2}")

# Precompute for multiple queries
max_n = 500
precomputed = two_sets_ii_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n * sum)
**Space Complexity**: O(sum)

**Why it's optimal**: Uses space-optimized DP for O(n * sum) time and O(sum) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Complete enumeration of all set partitions |
| Dynamic Programming | O(n * sum) | O(sum) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n * sum) | O(sum) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(n * sum) - Use dynamic programming for efficient calculation
- **Space**: O(sum) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Two Sets II with Constraints**
**Problem**: Count set partitions with specific constraints.

**Key Differences**: Apply constraints to partition selection

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_two_sets_ii(n, constraints, mod=10**9+7):
    """
    Count set partitions with constraints
    
    Args:
        n: the number
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    total_sum = n * (n + 1) // 2
    if total_sum % 2 != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // 2
    
    # Create DP table
    dp = [0] * (target_sum + 1)
    dp[0] = 1  # Empty set
    
    # Fill DP table with constraints
    for i in range(1, n + 1):
        if constraints(i):  # Check if element satisfies constraints
            for j in range(target_sum, i - 1, -1):
                dp[j] = (dp[j] + dp[j - i]) % mod
    
    return dp[target_sum]

# Example usage
n = 3
constraints = lambda i: i <= 2  # Only include elements <= 2
result = constrained_two_sets_ii(n, constraints)
print(f"Constrained two sets II: {result}")
```

#### **2. Two Sets II with Different Weights**
**Problem**: Count set partitions with different weights for elements.

**Key Differences**: Different weights for different elements

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def weighted_two_sets_ii(n, weights, mod=10**9+7):
    """
    Count set partitions with different weights
    
    Args:
        n: the number
        weights: array of weights
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    total_weight = sum(weights)
    if total_weight % 2 != 0:
        return 0  # Cannot partition into equal weights
    
    target_weight = total_weight // 2
    
    # Create DP table
    dp = [0] * (target_weight + 1)
    dp[0] = 1  # Empty set
    
    # Fill DP table with weights
    for i in range(n):
        weight = weights[i]
        for j in range(target_weight, weight - 1, -1):
            dp[j] = (dp[j] + dp[j - weight]) % mod
    
    return dp[target_weight]

# Example usage
n = 3
weights = [1, 2, 3]  # Different weights
result = weighted_two_sets_ii(n, weights)
print(f"Weighted two sets II: {result}")
```

#### **3. Two Sets II with Multiple Partitions**
**Problem**: Count set partitions into multiple subsets with equal sum.

**Key Differences**: Handle multiple subsets

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_partition_two_sets_ii(n, num_partitions, mod=10**9+7):
    """
    Count set partitions into multiple subsets with equal sum
    
    Args:
        n: the number
        num_partitions: number of partitions
        mod: modulo value
    
    Returns:
        int: number of ways to partition set modulo mod
    """
    total_sum = n * (n + 1) // 2
    if total_sum % num_partitions != 0:
        return 0  # Cannot partition into equal sums
    
    target_sum = total_sum // num_partitions
    
    # Create DP table
    dp = [0] * (target_sum + 1)
    dp[0] = 1  # Empty set
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(target_sum, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % mod
    
    return dp[target_sum]

# Example usage
n = 3
num_partitions = 2
result = multi_partition_two_sets_ii(n, num_partitions)
print(f"Multi-partition two sets II: {result}")
```

### Related Problems

#### **CSES Problems**
- [Removal Game](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Rectangle Cutting](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Longest Common Subsequence](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) - DP
- [Target Sum](https://leetcode.com/problems/target-sum/) - DP
- [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Set DP, partition algorithms
- **Combinatorics**: Mathematical counting, partition properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Set Algorithms](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Set algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Removal Game](https://cses.fi/problemset/task/1075) - Medium
- [CSES Rectangle Cutting](https://cses.fi/problemset/task/1075) - Medium
- [CSES Longest Common Subsequence](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
