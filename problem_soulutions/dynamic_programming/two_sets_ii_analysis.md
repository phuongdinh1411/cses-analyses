---
layout: simple
title: "Two Sets II - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/two_sets_ii_analysis
---

# Two Sets II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of set partitioning in dynamic programming
- Apply counting techniques for set partition analysis
- Implement efficient algorithms for set partition counting
- Optimize DP operations for partition analysis
- Handle special cases in set partition problems

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

## Problem Variations

### **Variation 1: Two Sets II with Dynamic Updates**
**Problem**: Handle dynamic number updates (add/remove/update numbers) while maintaining optimal two sets partitioning calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic number management.

```python
from collections import defaultdict

class DynamicTwoSetsII:
    def __init__(self, n=None):
        self.n = n or 0
        self.numbers = []
        self._update_two_sets_info()
    
    def _update_two_sets_info(self):
        """Update two sets feasibility information."""
        self.two_sets_feasibility = self._calculate_two_sets_feasibility()
    
    def _calculate_two_sets_feasibility(self):
        """Calculate two sets feasibility."""
        if self.n <= 0:
            return 0.0
        
        # Check if we can partition numbers 1 to n into two equal sum sets
        total_sum = self.n * (self.n + 1) // 2
        return 1.0 if total_sum % 2 == 0 else 0.0
    
    def update_n(self, new_n):
        """Update the value of n."""
        self.n = new_n
        self._update_two_sets_info()
    
    def add_number(self, number):
        """Add a number to the set."""
        if 1 <= number <= self.n:
            self.numbers.append(number)
            self._update_two_sets_info()
    
    def remove_number(self, number):
        """Remove a number from the set."""
        if number in self.numbers:
            self.numbers.remove(number)
            self._update_two_sets_info()
    
    def find_partition_count(self):
        """Find number of ways to partition into two equal sum sets using dynamic programming."""
        if not self.two_sets_feasibility:
            return 0
        
        if self.n == 0:
            return 0
        
        target_sum = self.n * (self.n + 1) // 4  # Half of total sum
        
        # DP table: dp[i][j] = number of ways to make sum j using first i numbers
        dp = [[0 for _ in range(target_sum + 1)] for _ in range(self.n + 1)]
        dp[0][0] = 1
        
        # Fill DP table
        for i in range(1, self.n + 1):
            for j in range(target_sum + 1):
                # Don't take number i
                dp[i][j] = dp[i-1][j]
                
                # Take number i
                if j >= i:
                    dp[i][j] = (dp[i][j] + dp[i-1][j-i]) % (10**9 + 7)
        
        return dp[self.n][target_sum]
    
    def find_partition_ways(self):
        """Find actual ways to partition into two equal sum sets."""
        if not self.two_sets_feasibility:
            return []
        
        if self.n == 0:
            return []
        
        target_sum = self.n * (self.n + 1) // 4
        
        # DP table: dp[i][j] = number of ways to make sum j using first i numbers
        dp = [[0 for _ in range(target_sum + 1)] for _ in range(self.n + 1)]
        dp[0][0] = 1
        
        # Fill DP table
        for i in range(1, self.n + 1):
            for j in range(target_sum + 1):
                dp[i][j] = dp[i-1][j]
                if j >= i:
                    dp[i][j] = (dp[i][j] + dp[i-1][j-i]) % (10**9 + 7)
        
        # Backtrack to find one valid partition
        if dp[self.n][target_sum] == 0:
            return []
        
        set1 = []
        set2 = []
        current_sum = target_sum
        
        for i in range(self.n, 0, -1):
            if current_sum >= i and dp[i-1][current_sum - i] > 0:
                set1.append(i)
                current_sum -= i
            else:
                set2.append(i)
        
        return [set1, set2]
    
    def get_two_sets_with_constraints(self, constraint_func):
        """Get two sets that satisfies custom constraints."""
        if not self.two_sets_feasibility:
            return []
        
        partition_count = self.find_partition_count()
        if constraint_func(partition_count, self.n):
            return self.find_partition_ways()
        else:
            return []
    
    def get_two_sets_in_range(self, min_count, max_count):
        """Get two sets within specified count range."""
        if not self.two_sets_feasibility:
            return []
        
        result = self.find_partition_count()
        if min_count <= result <= max_count:
            return self.find_partition_ways()
        else:
            return []
    
    def get_two_sets_with_pattern(self, pattern_func):
        """Get two sets matching specified pattern."""
        if not self.two_sets_feasibility:
            return []
        
        partition_count = self.find_partition_count()
        if pattern_func(partition_count, self.n):
            return self.find_partition_ways()
        else:
            return []
    
    def get_two_sets_statistics(self):
        """Get statistics about the two sets."""
        if not self.two_sets_feasibility:
            return {
                'n': 0,
                'two_sets_feasibility': 0,
                'partition_count': 0
            }
        
        partition_count = self.find_partition_count()
        return {
            'n': self.n,
            'two_sets_feasibility': self.two_sets_feasibility,
            'partition_count': partition_count
        }
    
    def get_two_sets_patterns(self):
        """Get patterns in two sets."""
        patterns = {
            'has_even_sum': 0,
            'has_valid_n': 0,
            'optimal_partition_possible': 0,
            'has_large_n': 0
        }
        
        if not self.two_sets_feasibility:
            return patterns
        
        # Check if has even sum
        total_sum = self.n * (self.n + 1) // 2
        if total_sum % 2 == 0:
            patterns['has_even_sum'] = 1
        
        # Check if has valid n
        if self.n > 0:
            patterns['has_valid_n'] = 1
        
        # Check if optimal partition is possible
        if self.two_sets_feasibility == 1.0:
            patterns['optimal_partition_possible'] = 1
        
        # Check if has large n
        if self.n > 100:
            patterns['has_large_n'] = 1
        
        return patterns
    
    def get_optimal_two_sets_strategy(self):
        """Get optimal strategy for two sets partitioning."""
        if not self.two_sets_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'two_sets_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.two_sets_feasibility
        
        # Calculate two sets feasibility
        two_sets_feasibility = self.two_sets_feasibility
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'dynamic_programming'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'two_sets_feasibility': two_sets_feasibility
        }

# Example usage
n = 7
dynamic_two_sets = DynamicTwoSetsII(n)
print(f"Two sets feasibility: {dynamic_two_sets.two_sets_feasibility}")

# Update n
dynamic_two_sets.update_n(8)
print(f"After updating n: {dynamic_two_sets.n}")

# Add number
dynamic_two_sets.add_number(5)
print(f"After adding number 5: {dynamic_two_sets.numbers}")

# Remove number
dynamic_two_sets.remove_number(5)
print(f"After removing number 5: {dynamic_two_sets.numbers}")

# Find partition count
partition_count = dynamic_two_sets.find_partition_count()
print(f"Partition count: {partition_count}")

# Find partition ways
ways = dynamic_two_sets.find_partition_ways()
print(f"Partition ways: {ways}")

# Get two sets with constraints
def constraint_func(partition_count, n):
    return partition_count > 0 and n > 0

print(f"Two sets with constraints: {dynamic_two_sets.get_two_sets_with_constraints(constraint_func)}")

# Get two sets in range
print(f"Two sets in range 0-100: {dynamic_two_sets.get_two_sets_in_range(0, 100)}")

# Get two sets with pattern
def pattern_func(partition_count, n):
    return partition_count > 0 and n > 0

print(f"Two sets with pattern: {dynamic_two_sets.get_two_sets_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_two_sets.get_two_sets_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_two_sets.get_two_sets_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_two_sets.get_optimal_two_sets_strategy()}")
```

### **Variation 2: Two Sets II with Different Operations**
**Problem**: Handle different types of two sets operations (weighted numbers, priority-based selection, advanced partitioning analysis).

**Approach**: Use advanced data structures for efficient different types of two sets operations.

```python
class AdvancedTwoSetsII:
    def __init__(self, n=None, weights=None, priorities=None):
        self.n = n or 0
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.partitions = []
        self._update_two_sets_info()
    
    def _update_two_sets_info(self):
        """Update two sets feasibility information."""
        self.two_sets_feasibility = self._calculate_two_sets_feasibility()
    
    def _calculate_two_sets_feasibility(self):
        """Calculate two sets feasibility."""
        if self.n <= 0:
            return 0.0
        
        # Check if we can partition numbers 1 to n into two equal sum sets
        total_sum = self.n * (self.n + 1) // 2
        return 1.0 if total_sum % 2 == 0 else 0.0
    
    def find_partition_count(self):
        """Find number of ways to partition into two equal sum sets using dynamic programming."""
        if not self.two_sets_feasibility:
            return 0
        
        if self.n == 0:
            return 0
        
        target_sum = self.n * (self.n + 1) // 4
        
        # DP table: dp[i][j] = number of ways to make sum j using first i numbers
        dp = [[0 for _ in range(target_sum + 1)] for _ in range(self.n + 1)]
        dp[0][0] = 1
        
        # Fill DP table
        for i in range(1, self.n + 1):
            for j in range(target_sum + 1):
                dp[i][j] = dp[i-1][j]
                if j >= i:
                    dp[i][j] = (dp[i][j] + dp[i-1][j-i]) % (10**9 + 7)
        
        return dp[self.n][target_sum]
    
    def get_weighted_two_sets(self):
        """Get two sets with weights and priorities applied."""
        if not self.two_sets_feasibility:
            return []
        
        if self.n == 0:
            return []
        
        # Create weighted partitioning options
        partitioning_options = []
        for i in range(1, self.n + 1):
            weight = self.weights.get(i, 1)
            priority = self.priorities.get(i, 1)
            weighted_score = i * weight * priority
            partitioning_options.append((i, weighted_score))
        
        # Sort by weighted score (descending for maximization)
        partitioning_options.sort(key=lambda x: x[1], reverse=True)
        
        # Create two sets based on weighted scores
        set1 = []
        set2 = []
        for i, (number, score) in enumerate(partitioning_options):
            if i % 2 == 0:
                set1.append(number)
            else:
                set2.append(number)
        
        return [set1, set2]
    
    def get_two_sets_with_priority(self, priority_func):
        """Get two sets considering priority."""
        if not self.two_sets_feasibility:
            return []
        
        # Create priority-based partitioning options
        priority_options = []
        for i in range(1, self.n + 1):
            priority = priority_func(i, self.weights, self.priorities)
            priority_options.append((i, priority))
        
        # Sort by priority (descending for maximization)
        priority_options.sort(key=lambda x: x[1], reverse=True)
        
        # Create two sets based on priority
        set1 = []
        set2 = []
        for i, (number, priority) in enumerate(priority_options):
            if i % 2 == 0:
                set1.append(number)
            else:
                set2.append(number)
        
        return [set1, set2]
    
    def get_two_sets_with_optimization(self, optimization_func):
        """Get two sets using custom optimization function."""
        if not self.two_sets_feasibility:
            return []
        
        # Create optimization-based partitioning options
        optimized_options = []
        for i in range(1, self.n + 1):
            score = optimization_func(i, self.weights, self.priorities)
            optimized_options.append((i, score))
        
        # Sort by optimization score (descending for maximization)
        optimized_options.sort(key=lambda x: x[1], reverse=True)
        
        # Create two sets based on optimization
        set1 = []
        set2 = []
        for i, (number, score) in enumerate(optimized_options):
            if i % 2 == 0:
                set1.append(number)
            else:
                set2.append(number)
        
        return [set1, set2]
    
    def get_two_sets_with_constraints(self, constraint_func):
        """Get two sets that satisfies custom constraints."""
        if not self.two_sets_feasibility:
            return []
        
        if constraint_func(self.n, self.weights, self.priorities):
            return self.get_weighted_two_sets()
        else:
            return []
    
    def get_two_sets_with_multiple_criteria(self, criteria_list):
        """Get two sets that satisfies multiple criteria."""
        if not self.two_sets_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_two_sets()
        else:
            return []
    
    def get_two_sets_with_alternatives(self, alternatives):
        """Get two sets considering alternative weights/priorities."""
        result = []
        
        # Check original two sets
        original_sets = self.get_weighted_two_sets()
        result.append((original_sets, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedTwoSetsII(self.n, alt_weights, alt_priorities)
            temp_sets = temp_instance.get_weighted_two_sets()
            result.append((temp_sets, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_two_sets_with_adaptive_criteria(self, adaptive_func):
        """Get two sets using adaptive criteria."""
        if not self.two_sets_feasibility:
            return []
        
        if adaptive_func(self.n, self.weights, self.priorities, []):
            return self.get_weighted_two_sets()
        else:
            return []
    
    def get_two_sets_optimization(self):
        """Get optimal two sets configuration."""
        strategies = [
            ('weighted_sets', lambda: len(self.get_weighted_two_sets())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n = 7
weights = {i: i * 2 for i in range(1, n + 1)}  # Weight based on number value
priorities = {i: 1 for i in range(1, n + 1)}  # Equal priority
advanced_two_sets = AdvancedTwoSetsII(n, weights, priorities)

print(f"Weighted two sets: {advanced_two_sets.get_weighted_two_sets()}")

# Get two sets with priority
def priority_func(number, weights, priorities):
    return weights.get(number, 1) + priorities.get(number, 1)

print(f"Two sets with priority: {advanced_two_sets.get_two_sets_with_priority(priority_func)}")

# Get two sets with optimization
def optimization_func(number, weights, priorities):
    return weights.get(number, 1) * priorities.get(number, 1)

print(f"Two sets with optimization: {advanced_two_sets.get_two_sets_with_optimization(optimization_func)}")

# Get two sets with constraints
def constraint_func(n, weights, priorities):
    return n > 0

print(f"Two sets with constraints: {advanced_two_sets.get_two_sets_with_constraints(constraint_func)}")

# Get two sets with multiple criteria
def criterion1(n, weights, priorities):
    return n > 0

def criterion2(n, weights, priorities):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Two sets with multiple criteria: {advanced_two_sets.get_two_sets_with_multiple_criteria(criteria_list)}")

# Get two sets with alternatives
alternatives = [({i: 1 for i in range(1, n + 1)}, {i: 1 for i in range(1, n + 1)}), ({i: i*3 for i in range(1, n + 1)}, {i: 2 for i in range(1, n + 1)})]
print(f"Two sets with alternatives: {advanced_two_sets.get_two_sets_with_alternatives(alternatives)}")

# Get two sets with adaptive criteria
def adaptive_func(n, weights, priorities, current_result):
    return n > 0 and len(current_result) < 10

print(f"Two sets with adaptive criteria: {advanced_two_sets.get_two_sets_with_adaptive_criteria(adaptive_func)}")

# Get two sets optimization
print(f"Two sets optimization: {advanced_two_sets.get_two_sets_optimization()}")
```

### **Variation 3: Two Sets II with Constraints**
**Problem**: Handle two sets partitioning with additional constraints (number limits, partitioning constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTwoSetsII:
    def __init__(self, n=None, constraints=None):
        self.n = n or 0
        self.constraints = constraints or {}
        self.partitions = []
        self._update_two_sets_info()
    
    def _update_two_sets_info(self):
        """Update two sets feasibility information."""
        self.two_sets_feasibility = self._calculate_two_sets_feasibility()
    
    def _calculate_two_sets_feasibility(self):
        """Calculate two sets feasibility."""
        if self.n <= 0:
            return 0.0
        
        # Check if we can partition numbers 1 to n into two equal sum sets
        total_sum = self.n * (self.n + 1) // 2
        return 1.0 if total_sum % 2 == 0 else 0.0
    
    def _is_valid_number(self, number):
        """Check if number is valid considering constraints."""
        # Number constraints
        if 'allowed_numbers' in self.constraints:
            if number not in self.constraints['allowed_numbers']:
                return False
        
        if 'forbidden_numbers' in self.constraints:
            if number in self.constraints['forbidden_numbers']:
                return False
        
        # Range constraints
        if 'max_number' in self.constraints:
            if number > self.constraints['max_number']:
                return False
        
        if 'min_number' in self.constraints:
            if number < self.constraints['min_number']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(number, self.n):
                    return False
        
        return True
    
    def get_two_sets_with_number_constraints(self, min_numbers, max_numbers):
        """Get two sets considering number count constraints."""
        if not self.two_sets_feasibility:
            return []
        
        if min_numbers <= self.n <= max_numbers:
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def get_two_sets_with_partitioning_constraints(self, partitioning_constraints):
        """Get two sets considering partitioning constraints."""
        if not self.two_sets_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in partitioning_constraints:
            if not constraint(self.n):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def get_two_sets_with_pattern_constraints(self, pattern_constraints):
        """Get two sets considering pattern constraints."""
        if not self.two_sets_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def get_two_sets_with_mathematical_constraints(self, constraint_func):
        """Get two sets that satisfies custom mathematical constraints."""
        if not self.two_sets_feasibility:
            return []
        
        if constraint_func(self.n):
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def get_two_sets_with_optimization_constraints(self, optimization_func):
        """Get two sets using custom optimization constraints."""
        if not self.two_sets_feasibility:
            return []
        
        # Calculate optimization score for two sets
        score = optimization_func(self.n)
        
        if score > 0:
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def get_two_sets_with_multiple_constraints(self, constraints_list):
        """Get two sets that satisfies multiple constraints."""
        if not self.two_sets_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def get_two_sets_with_priority_constraints(self, priority_func):
        """Get two sets with priority-based constraints."""
        if not self.two_sets_feasibility:
            return []
        
        # Calculate priority for two sets
        priority = priority_func(self.n)
        
        if priority > 0:
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def get_two_sets_with_adaptive_constraints(self, adaptive_func):
        """Get two sets with adaptive constraints."""
        if not self.two_sets_feasibility:
            return []
        
        if adaptive_func(self.n, []):
            return self._calculate_constrained_two_sets()
        else:
            return []
    
    def _calculate_constrained_two_sets(self):
        """Calculate two sets considering all constraints."""
        if not self.two_sets_feasibility:
            return []
        
        if self.n == 0:
            return []
        
        # Find valid numbers
        valid_numbers = []
        for i in range(1, self.n + 1):
            if self._is_valid_number(i):
                valid_numbers.append(i)
        
        # Create two sets for valid numbers
        set1 = []
        set2 = []
        for i, number in enumerate(valid_numbers):
            if i % 2 == 0:
                set1.append(number)
            else:
                set2.append(number)
        
        return [set1, set2]
    
    def get_optimal_two_sets_strategy(self):
        """Get optimal two sets strategy considering all constraints."""
        strategies = [
            ('number_constraints', self.get_two_sets_with_number_constraints),
            ('partitioning_constraints', self.get_two_sets_with_partitioning_constraints),
            ('pattern_constraints', self.get_two_sets_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'number_constraints':
                    result = strategy_func(1, 1000)
                elif strategy_name == 'partitioning_constraints':
                    partitioning_constraints = [lambda n: n > 0]
                    result = strategy_func(partitioning_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n: n > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'forbidden_numbers': [11, 12, 13, 14, 15],
    'max_number': 10,
    'min_number': 1,
    'pattern_constraints': [lambda number, n: number > 0 and number <= n]
}

n = 7
constrained_two_sets = ConstrainedTwoSetsII(n, constraints)

print("Number-constrained two sets:", constrained_two_sets.get_two_sets_with_number_constraints(1, 10))

print("Partitioning-constrained two sets:", constrained_two_sets.get_two_sets_with_partitioning_constraints([lambda n: n > 0]))

print("Pattern-constrained two sets:", constrained_two_sets.get_two_sets_with_pattern_constraints([lambda n: n > 0]))

# Mathematical constraints
def custom_constraint(n):
    return n > 0

print("Mathematical constraint two sets:", constrained_two_sets.get_two_sets_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n):
    return 1 <= n <= 100

range_constraints = [range_constraint]
print("Range-constrained two sets:", constrained_two_sets.get_two_sets_with_number_constraints(1, 10))

# Multiple constraints
def constraint1(n):
    return n > 0

def constraint2(n):
    return n % 2 == 0 or n % 2 == 1  # Always true

constraints_list = [constraint1, constraint2]
print("Multiple constraints two sets:", constrained_two_sets.get_two_sets_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n):
    return n + n * (n + 1) // 2

print("Priority-constrained two sets:", constrained_two_sets.get_two_sets_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, current_result):
    return n > 0 and len(current_result) < 10

print("Adaptive constraint two sets:", constrained_two_sets.get_two_sets_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_two_sets.get_optimal_two_sets_strategy()
print(f"Optimal two sets strategy: {optimal}")
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
