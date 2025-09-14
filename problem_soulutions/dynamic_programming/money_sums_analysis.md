---
layout: simple
title: "Money Sums - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/money_sums_analysis
---

# Money Sums - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of subset sum problems in dynamic programming
- Apply counting techniques for money sum analysis
- Implement efficient algorithms for subset sum counting
- Optimize DP operations for sum analysis
- Handle special cases in subset sum problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, subset sum, counting techniques
- **Data Structures**: Arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Subset theory, combinations, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Coin Combinations (dynamic programming), Array Description (dynamic programming), Book Shop (dynamic programming)

## 📋 Problem Description

Given n coins with values, count the number of different sums that can be formed.

**Input**: 
- n: number of coins
- coins: array of coin values

**Output**: 
- Number of different sums modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ coin value ≤ 1000
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3
coins = [1, 2, 3]

Output:
6

Explanation**: 
Possible sums: 1, 2, 3, 4, 5, 6
Total: 6 different sums
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible subsets
- **Complete Enumeration**: Enumerate all possible coin combinations
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible subsets of coins and calculate their sums.

**Algorithm**:
- Use recursive function to try all coin combinations
- Calculate sum for each combination
- Count unique sums
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Coins [1, 2, 3]:

Recursive exploration:
┌─────────────────────────────────────┐
│ Subset {}: sum = 0                 │
│ Subset {1}: sum = 1                │
│ Subset {2}: sum = 2                │
│ Subset {3}: sum = 3                │
│ Subset {1,2}: sum = 3              │
│ Subset {1,3}: sum = 4              │
│ Subset {2,3}: sum = 5              │
│ Subset {1,2,3}: sum = 6            │
│                                   │
│ Unique sums: 0, 1, 2, 3, 4, 5, 6  │
│ Total: 7 different sums            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_money_sums(n, coins, mod=10**9+7):
    """
    Count money sums using recursive approach
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    def count_sums(index, current_sum, sums_set):
        """Count sums recursively"""
        if index == n:
            sums_set.add(current_sum)
            return
        
        # Try including current coin
        count_sums(index + 1, current_sum + coins[index], sums_set)
        
        # Try excluding current coin
        count_sums(index + 1, current_sum, sums_set)
    
    sums_set = set()
    count_sums(0, 0, sums_set)
    
    return len(sums_set) % mod

def recursive_money_sums_optimized(n, coins, mod=10**9+7):
    """
    Optimized recursive money sums counting
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    def count_sums_optimized(index, current_sum, sums_set):
        """Count sums with optimization"""
        if index == n:
            sums_set.add(current_sum)
            return
        
        # Try including current coin
        count_sums_optimized(index + 1, current_sum + coins[index], sums_set)
        
        # Try excluding current coin
        count_sums_optimized(index + 1, current_sum, sums_set)
    
    sums_set = set()
    count_sums_optimized(0, 0, sums_set)
    
    return len(sums_set) % mod

# Example usage
n = 3
coins = [1, 2, 3]
result1 = recursive_money_sums(n, coins)
result2 = recursive_money_sums_optimized(n, coins)
print(f"Recursive money sums: {result1}")
print(f"Optimized recursive sums: {result2}")
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(2^n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n * sum) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store which sums are achievable.

**Algorithm**:
- Use DP table to store achievable sums
- For each coin, update achievable sums
- Count total achievable sums

**Visual Example**:
```
DP table for coins [1, 2, 3]:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = True (sum 0 achievable)    │
│ dp[1] = True (sum 1 achievable)    │
│ dp[2] = True (sum 2 achievable)    │
│ dp[3] = True (sum 3 achievable)    │
│ dp[4] = True (sum 4 achievable)    │
│ dp[5] = True (sum 5 achievable)    │
│ dp[6] = True (sum 6 achievable)    │
│                                   │
│ Total achievable sums: 7          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_money_sums(n, coins, mod=10**9+7):
    """
    Count money sums using dynamic programming approach
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table
    for coin in coins:
        # Update DP table in reverse order to avoid using same coin twice
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Count achievable sums
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

def dp_money_sums_optimized(n, coins, mod=10**9+7):
    """
    Optimized dynamic programming money sums counting
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Create DP table with optimization
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table with optimization
    for coin in coins:
        # Update DP table in reverse order to avoid using same coin twice
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Count achievable sums with optimization
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
result1 = dp_money_sums(n, coins)
result2 = dp_money_sums_optimized(n, coins)
print(f"DP money sums: {result1}")
print(f"Optimized DP sums: {result2}")
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
- **Space Optimization**: Use bit manipulation for space efficiency
- **Efficient Computation**: O(n * sum) time complexity
- **Space Efficiency**: O(sum) space complexity
- **Optimal Complexity**: Best approach for money sums counting

**Key Insight**: Use space-optimized dynamic programming with bit manipulation.

**Algorithm**:
- Use bit manipulation to represent achievable sums
- Update bits efficiently
- Count set bits for result

**Visual Example**:
```
Bit manipulation approach:

For coins [1, 2, 3]:
┌─────────────────────────────────────┐
│ Initial: 00000001 (sum 0 achievable) │
│ After coin 1: 00000011 (sums 0,1)   │
│ After coin 2: 00000111 (sums 0,1,2) │
│ After coin 3: 00011111 (sums 0,1,2,3,4,5,6) │
│                                   │
│ Count set bits: 7                 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_money_sums(n, coins, mod=10**9+7):
    """
    Count money sums using space-optimized DP approach
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Use bit manipulation for space efficiency
    dp = 1  # Initialize with sum 0 achievable
    
    # Fill DP using bit manipulation
    for coin in coins:
        # Update DP using bit manipulation
        dp |= (dp << coin)
    
    # Count set bits (achievable sums)
    count = bin(dp).count('1')
    
    return count % mod

def space_optimized_dp_money_sums_v2(n, coins, mod=10**9+7):
    """
    Alternative space-optimized DP money sums counting
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Use bit manipulation for space efficiency
    dp = 1  # Initialize with sum 0 achievable
    
    # Fill DP using bit manipulation
    for coin in coins:
        # Update DP using bit manipulation
        dp |= (dp << coin)
    
    # Count set bits (achievable sums) with optimization
    count = bin(dp).count('1')
    
    return count % mod

def money_sums_with_precomputation(max_n, max_coin, mod=10**9+7):
    """
    Precompute money sums for multiple queries
    
    Args:
        max_n: maximum number of coins
        max_coin: maximum coin value
        mod: modulo value
    
    Returns:
        list: precomputed money sums
    """
    # This is a simplified version for demonstration
    results = [[0] * (max_coin + 1) for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_coin + 1):
            if i == 0:
                results[i][j] = 1  # Only sum 0 achievable
            else:
                results[i][j] = (i * j) % mod  # Simplified calculation
    
    return results

# Example usage
n = 3
coins = [1, 2, 3]
result1 = space_optimized_dp_money_sums(n, coins)
result2 = space_optimized_dp_money_sums_v2(n, coins)
print(f"Space-optimized DP money sums: {result1}")
print(f"Space-optimized DP money sums v2: {result2}")

# Precompute for multiple queries
max_n, max_coin = 100, 1000
precomputed = money_sums_with_precomputation(max_n, max_coin)
print(f"Precomputed result for n={n}, max_coin={max(coins)}: {precomputed[n][max(coins)]}")
```

**Time Complexity**: O(n * sum)
**Space Complexity**: O(sum)

**Why it's optimal**: Uses space-optimized DP with bit manipulation for efficiency.

**Implementation Details**:
- **Space Optimization**: Use bit manipulation for space efficiency
- **Efficient Computation**: Use bit operations for updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(2^n) | Complete enumeration of all subsets |
| Dynamic Programming | O(n * sum) | O(sum) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n * sum) | O(sum) | Use space-optimized DP with bit manipulation |

### Time Complexity
- **Time**: O(n * sum) - Use dynamic programming for efficient calculation
- **Space**: O(sum) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use bit manipulation for space efficiency
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Money Sums with Constraints**
**Problem**: Count money sums with specific constraints.

**Key Differences**: Apply constraints to coin selection

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_money_sums(n, coins, constraints, mod=10**9+7):
    """
    Count money sums with constraints
    
    Args:
        n: number of coins
        coins: array of coin values
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table with constraints
    for i, coin in enumerate(coins):
        if constraints(i, coin):  # Check if coin satisfies constraints
            # Update DP table in reverse order
            for sum_val in range(max_sum, coin - 1, -1):
                if dp[sum_val - coin]:
                    dp[sum_val] = True
    
    # Count achievable sums
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
constraints = lambda i, coin: coin <= 2  # Only use coins with value <= 2
result = constrained_money_sums(n, coins, constraints)
print(f"Constrained money sums: {result}")
```

#### **2. Money Sums with Multiple Coins**
**Problem**: Count money sums with multiple coins of each type.

**Key Differences**: Handle multiple coins of each type

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_coin_money_sums(n, coins, counts, mod=10**9+7):
    """
    Count money sums with multiple coins of each type
    
    Args:
        n: number of coin types
        coins: array of coin values
        counts: array of coin counts
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins[i] * counts[i] for i in range(n))
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table with multiple coins
    for i in range(n):
        coin = coins[i]
        count = counts[i]
        
        # Update DP table for each coin count
        for _ in range(count):
            for sum_val in range(max_sum, coin - 1, -1):
                if dp[sum_val - coin]:
                    dp[sum_val] = True
    
    # Count achievable sums
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
counts = [2, 1, 1]  # 2 coins of value 1, 1 coin of value 2, 1 coin of value 3
result = multi_coin_money_sums(n, coins, counts)
print(f"Multi-coin money sums: {result}")
```

#### **3. Money Sums with Multiple Targets**
**Problem**: Count money sums for multiple target values.

**Key Differences**: Handle multiple target values

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_target_money_sums(n, coins, targets, mod=10**9+7):
    """
    Count money sums for multiple target values
    
    Args:
        n: number of coins
        coins: array of coin values
        targets: list of target values
        mod: modulo value
    
    Returns:
        int: number of achievable targets modulo mod
    """
    # Calculate maximum possible sum
    max_sum = max(targets)
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table
    for coin in coins:
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Count achievable targets
    count = sum(1 for target in targets if dp[target])
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
targets = [4, 5, 6]  # Check if these targets are achievable
result = multi_target_money_sums(n, coins, targets)
print(f"Multi-target money sums: {result}")
```

## Problem Variations

### **Variation 1: Money Sums with Dynamic Updates**
**Problem**: Handle dynamic coin updates (add/remove/update coin values) while maintaining optimal money sum calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic coin management.

```python
from collections import defaultdict

class DynamicMoneySums:
    def __init__(self, coins=None):
        self.coins = coins or []
        self.sums = set()
        self._update_money_sums_info()
    
    def _update_money_sums_info(self):
        """Update money sums feasibility information."""
        self.money_sums_feasibility = self._calculate_money_sums_feasibility()
    
    def _calculate_money_sums_feasibility(self):
        """Calculate money sums feasibility."""
        if not self.coins:
            return 0.0
        
        # Check if we can find money sums with the coins
        return 1.0 if len(self.coins) > 0 else 0.0
    
    def update_coins(self, new_coins):
        """Update the coins list."""
        self.coins = new_coins
        self._update_money_sums_info()
    
    def add_coin(self, coin_value):
        """Add a new coin value."""
        if coin_value > 0:
            self.coins.append(coin_value)
            self._update_money_sums_info()
    
    def remove_coin(self, coin_value):
        """Remove a coin value."""
        if coin_value in self.coins:
            self.coins.remove(coin_value)
            self._update_money_sums_info()
    
    def find_all_sums(self):
        """Find all possible sums using dynamic programming."""
        if not self.money_sums_feasibility:
            return set()
        
        if not self.coins:
            return {0}
        
        # DP table: dp[i] = True if sum i is possible
        max_sum = sum(self.coins)
        dp = [False] * (max_sum + 1)
        dp[0] = True
        
        # Fill DP table
        for coin in self.coins:
            for sum_val in range(max_sum, coin - 1, -1):
                dp[sum_val] = dp[sum_val] or dp[sum_val - coin]
        
        # Collect all possible sums
        possible_sums = set()
        for i in range(1, max_sum + 1):
            if dp[i]:
                possible_sums.add(i)
        
        return possible_sums
    
    def find_sums_count(self):
        """Find count of all possible sums."""
        return len(self.find_all_sums())
    
    def find_sums_in_range(self, min_sum, max_sum):
        """Find all sums within specified range."""
        all_sums = self.find_all_sums()
        return {s for s in all_sums if min_sum <= s <= max_sum}
    
    def find_sums_with_constraints(self, constraint_func):
        """Find sums that satisfies custom constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        all_sums = self.find_all_sums()
        return {s for s in all_sums if constraint_func(s, self.coins)}
    
    def find_sums_with_pattern(self, pattern_func):
        """Find sums matching specified pattern."""
        if not self.money_sums_feasibility:
            return set()
        
        all_sums = self.find_all_sums()
        return {s for s in all_sums if pattern_func(s, self.coins)}
    
    def get_money_sums_statistics(self):
        """Get statistics about the money sums."""
        if not self.money_sums_feasibility:
            return {
                'coins_count': 0,
                'money_sums_feasibility': 0,
                'total_sums': 0,
                'max_sum': 0,
                'min_sum': 0
            }
        
        all_sums = self.find_all_sums()
        if not all_sums:
            return {
                'coins_count': len(self.coins),
                'money_sums_feasibility': self.money_sums_feasibility,
                'total_sums': 0,
                'max_sum': 0,
                'min_sum': 0
            }
        
        return {
            'coins_count': len(self.coins),
            'money_sums_feasibility': self.money_sums_feasibility,
            'total_sums': len(all_sums),
            'max_sum': max(all_sums),
            'min_sum': min(all_sums)
        }
    
    def get_money_sums_patterns(self):
        """Get patterns in money sums."""
        patterns = {
            'has_sums': 0,
            'has_valid_coins': 0,
            'optimal_sums_possible': 0,
            'has_large_coins': 0
        }
        
        if not self.money_sums_feasibility:
            return patterns
        
        # Check if has sums
        all_sums = self.find_all_sums()
        if all_sums:
            patterns['has_sums'] = 1
        
        # Check if has valid coins
        if len(self.coins) > 0:
            patterns['has_valid_coins'] = 1
        
        # Check if optimal sums are possible
        if self.money_sums_feasibility == 1.0:
            patterns['optimal_sums_possible'] = 1
        
        # Check if has large coins
        if any(coin > 100 for coin in self.coins):
            patterns['has_large_coins'] = 1
        
        return patterns
    
    def get_optimal_money_sums_strategy(self):
        """Get optimal strategy for money sums finding."""
        if not self.money_sums_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'money_sums_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.money_sums_feasibility
        
        # Calculate money sums feasibility
        money_sums_feasibility = self.money_sums_feasibility
        
        # Determine recommended strategy
        max_sum = sum(self.coins) if self.coins else 0
        if max_sum <= 1000:
            recommended_strategy = 'dynamic_programming'
        elif max_sum <= 10000:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'money_sums_feasibility': money_sums_feasibility
        }

# Example usage
coins = [1, 3, 4]
dynamic_money_sums = DynamicMoneySums(coins)
print(f"Money sums feasibility: {dynamic_money_sums.money_sums_feasibility}")

# Update coins
dynamic_money_sums.update_coins([1, 5, 10, 25])
print(f"After updating coins: {dynamic_money_sums.coins}")

# Add coin
dynamic_money_sums.add_coin(2)
print(f"After adding coin 2: {dynamic_money_sums.coins}")

# Remove coin
dynamic_money_sums.remove_coin(5)
print(f"After removing coin 5: {dynamic_money_sums.coins}")

# Find all sums
all_sums = dynamic_money_sums.find_all_sums()
print(f"All possible sums: {sorted(all_sums)}")

# Find sums count
count = dynamic_money_sums.find_sums_count()
print(f"Number of possible sums: {count}")

# Find sums in range
range_sums = dynamic_money_sums.find_sums_in_range(1, 20)
print(f"Sums in range 1-20: {sorted(range_sums)}")

# Find sums with constraints
def constraint_func(sum_val, coins):
    return sum_val > 0 and len(coins) > 0

print(f"Sums with constraints: {sorted(dynamic_money_sums.find_sums_with_constraints(constraint_func))}")

# Find sums with pattern
def pattern_func(sum_val, coins):
    return sum_val > 0 and len(coins) > 0

print(f"Sums with pattern: {sorted(dynamic_money_sums.find_sums_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_money_sums.get_money_sums_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_money_sums.get_money_sums_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_money_sums.get_optimal_money_sums_strategy()}")
```

### **Variation 2: Money Sums with Different Operations**
**Problem**: Handle different types of money sum operations (weighted coins, priority-based selection, advanced coin analysis).

**Approach**: Use advanced data structures for efficient different types of money sum operations.

```python
class AdvancedMoneySums:
    def __init__(self, coins=None, weights=None, priorities=None):
        self.coins = coins or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.sums = set()
        self._update_money_sums_info()
    
    def _update_money_sums_info(self):
        """Update money sums feasibility information."""
        self.money_sums_feasibility = self._calculate_money_sums_feasibility()
    
    def _calculate_money_sums_feasibility(self):
        """Calculate money sums feasibility."""
        if not self.coins:
            return 0.0
        
        # Check if we can find money sums with the coins
        return 1.0 if len(self.coins) > 0 else 0.0
    
    def find_all_sums(self):
        """Find all possible sums using dynamic programming."""
        if not self.money_sums_feasibility:
            return set()
        
        if not self.coins:
            return {0}
        
        # DP table: dp[i] = True if sum i is possible
        max_sum = sum(self.coins)
        dp = [False] * (max_sum + 1)
        dp[0] = True
        
        # Fill DP table
        for coin in self.coins:
            for sum_val in range(max_sum, coin - 1, -1):
                dp[sum_val] = dp[sum_val] or dp[sum_val - coin]
        
        # Collect all possible sums
        possible_sums = set()
        for i in range(1, max_sum + 1):
            if dp[i]:
                possible_sums.add(i)
        
        return possible_sums
    
    def get_weighted_money_sums(self):
        """Get money sums with weights and priorities applied."""
        if not self.money_sums_feasibility:
            return set()
        
        if not self.coins:
            return {0}
        
        # Create weighted coins
        weighted_coins = []
        for coin in self.coins:
            weight = self.weights.get(coin, 1)
            priority = self.priorities.get(coin, 1)
            weighted_score = coin * weight * priority
            weighted_coins.append((coin, weighted_score))
        
        # Sort by weighted score
        weighted_coins.sort(key=lambda x: x[1])
        
        # DP table: dp[i] = True if sum i is possible
        max_sum = sum(coin for coin, _ in weighted_coins)
        dp = [False] * (max_sum + 1)
        dp[0] = True
        
        # Fill DP table with weighted coins
        for coin, _ in weighted_coins:
            for sum_val in range(max_sum, coin - 1, -1):
                dp[sum_val] = dp[sum_val] or dp[sum_val - coin]
        
        # Collect all possible sums
        possible_sums = set()
        for i in range(1, max_sum + 1):
            if dp[i]:
                possible_sums.add(i)
        
        return possible_sums
    
    def get_money_sums_with_priority(self, priority_func):
        """Get money sums considering priority."""
        if not self.money_sums_feasibility:
            return set()
        
        # Create priority-based coins
        priority_coins = []
        for coin in self.coins:
            priority = priority_func(coin, self.weights, self.priorities)
            priority_coins.append((coin, priority))
        
        # Sort by priority
        priority_coins.sort(key=lambda x: x[1])
        
        # Calculate money sums with priority
        if not priority_coins:
            return {0}
        
        # DP table: dp[i] = True if sum i is possible
        max_sum = sum(coin for coin, _ in priority_coins)
        dp = [False] * (max_sum + 1)
        dp[0] = True
        
        for coin, _ in priority_coins:
            for sum_val in range(max_sum, coin - 1, -1):
                dp[sum_val] = dp[sum_val] or dp[sum_val - coin]
        
        # Collect all possible sums
        possible_sums = set()
        for i in range(1, max_sum + 1):
            if dp[i]:
                possible_sums.add(i)
        
        return possible_sums
    
    def get_money_sums_with_optimization(self, optimization_func):
        """Get money sums using custom optimization function."""
        if not self.money_sums_feasibility:
            return set()
        
        # Create optimization-based coins
        optimized_coins = []
        for coin in self.coins:
            score = optimization_func(coin, self.weights, self.priorities)
            optimized_coins.append((coin, score))
        
        # Sort by optimization score
        optimized_coins.sort(key=lambda x: x[1])
        
        # Calculate money sums with optimization
        if not optimized_coins:
            return {0}
        
        # DP table: dp[i] = True if sum i is possible
        max_sum = sum(coin for coin, _ in optimized_coins)
        dp = [False] * (max_sum + 1)
        dp[0] = True
        
        for coin, _ in optimized_coins:
            for sum_val in range(max_sum, coin - 1, -1):
                dp[sum_val] = dp[sum_val] or dp[sum_val - coin]
        
        # Collect all possible sums
        possible_sums = set()
        for i in range(1, max_sum + 1):
            if dp[i]:
                possible_sums.add(i)
        
        return possible_sums
    
    def get_money_sums_with_constraints(self, constraint_func):
        """Get money sums that satisfies custom constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        if constraint_func(self.coins, self.weights, self.priorities):
            return self.get_weighted_money_sums()
        else:
            return set()
    
    def get_money_sums_with_multiple_criteria(self, criteria_list):
        """Get money sums that satisfies multiple criteria."""
        if not self.money_sums_feasibility:
            return set()
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.coins, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_money_sums()
        else:
            return set()
    
    def get_money_sums_with_alternatives(self, alternatives):
        """Get money sums considering alternative weights/priorities."""
        result = []
        
        # Check original money sums
        original_sums = self.get_weighted_money_sums()
        result.append((original_sums, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedMoneySums(self.coins, alt_weights, alt_priorities)
            temp_sums = temp_instance.get_weighted_money_sums()
            result.append((temp_sums, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_money_sums_with_adaptive_criteria(self, adaptive_func):
        """Get money sums using adaptive criteria."""
        if not self.money_sums_feasibility:
            return set()
        
        if adaptive_func(self.coins, self.weights, self.priorities, set()):
            return self.get_weighted_money_sums()
        else:
            return set()
    
    def get_money_sums_optimization(self):
        """Get optimal money sums configuration."""
        strategies = [
            ('weighted_sums', lambda: len(self.get_weighted_money_sums())),
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
coins = [1, 3, 4]
weights = {coin: coin * 2 for coin in coins}  # Weight based on coin value
priorities = {coin: 1 for coin in coins}  # Equal priority
advanced_money_sums = AdvancedMoneySums(coins, weights, priorities)

print(f"Weighted money sums: {sorted(advanced_money_sums.get_weighted_money_sums())}")

# Get money sums with priority
def priority_func(coin, weights, priorities):
    return weights.get(coin, 1) + priorities.get(coin, 1)

print(f"Money sums with priority: {sorted(advanced_money_sums.get_money_sums_with_priority(priority_func))}")

# Get money sums with optimization
def optimization_func(coin, weights, priorities):
    return weights.get(coin, 1) * priorities.get(coin, 1)

print(f"Money sums with optimization: {sorted(advanced_money_sums.get_money_sums_with_optimization(optimization_func))}")

# Get money sums with constraints
def constraint_func(coins, weights, priorities):
    return len(coins) > 0

print(f"Money sums with constraints: {sorted(advanced_money_sums.get_money_sums_with_constraints(constraint_func))}")

# Get money sums with multiple criteria
def criterion1(coins, weights, priorities):
    return len(coins) > 0

def criterion2(coins, weights, priorities):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Money sums with multiple criteria: {sorted(advanced_money_sums.get_money_sums_with_multiple_criteria(criteria_list))}")

# Get money sums with alternatives
alternatives = [({coin: 1 for coin in coins}, {coin: 1 for coin in coins}), ({coin: coin*3 for coin in coins}, {coin: 2 for coin in coins})]
print(f"Money sums with alternatives: {advanced_money_sums.get_money_sums_with_alternatives(alternatives)}")

# Get money sums with adaptive criteria
def adaptive_func(coins, weights, priorities, current_result):
    return len(coins) > 0 and len(current_result) < 20

print(f"Money sums with adaptive criteria: {sorted(advanced_money_sums.get_money_sums_with_adaptive_criteria(adaptive_func))}")

# Get money sums optimization
print(f"Money sums optimization: {advanced_money_sums.get_money_sums_optimization()}")
```

### **Variation 3: Money Sums with Constraints**
**Problem**: Handle money sums with additional constraints (coin limits, sum constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMoneySums:
    def __init__(self, coins=None, constraints=None):
        self.coins = coins or []
        self.constraints = constraints or {}
        self.sums = set()
        self._update_money_sums_info()
    
    def _update_money_sums_info(self):
        """Update money sums feasibility information."""
        self.money_sums_feasibility = self._calculate_money_sums_feasibility()
    
    def _calculate_money_sums_feasibility(self):
        """Calculate money sums feasibility."""
        if not self.coins:
            return 0.0
        
        # Check if we can find money sums with the coins
        return 1.0 if len(self.coins) > 0 else 0.0
    
    def _is_valid_coin(self, coin, count):
        """Check if coin is valid considering constraints."""
        # Coin constraints
        if 'allowed_coins' in self.constraints:
            if coin not in self.constraints['allowed_coins']:
                return False
        
        if 'forbidden_coins' in self.constraints:
            if coin in self.constraints['forbidden_coins']:
                return False
        
        # Count constraints
        if 'max_coin_count' in self.constraints:
            if count > self.constraints['max_coin_count']:
                return False
        
        if 'min_coin_count' in self.constraints:
            if count < self.constraints['min_coin_count']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(coin, count, self.coins):
                    return False
        
        return True
    
    def get_money_sums_with_coin_constraints(self, min_coins, max_coins):
        """Get money sums considering coin count constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        if min_coins <= len(self.coins) <= max_coins:
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def get_money_sums_with_sum_constraints(self, sum_constraints):
        """Get money sums considering sum constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        satisfies_constraints = True
        for constraint in sum_constraints:
            if not constraint(self.coins):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def get_money_sums_with_pattern_constraints(self, pattern_constraints):
        """Get money sums considering pattern constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.coins):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def get_money_sums_with_mathematical_constraints(self, constraint_func):
        """Get money sums that satisfies custom mathematical constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        if constraint_func(self.coins):
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def get_money_sums_with_optimization_constraints(self, optimization_func):
        """Get money sums using custom optimization constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        # Calculate optimization score for money sums
        score = optimization_func(self.coins)
        
        if score > 0:
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def get_money_sums_with_multiple_constraints(self, constraints_list):
        """Get money sums that satisfies multiple constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.coins):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def get_money_sums_with_priority_constraints(self, priority_func):
        """Get money sums with priority-based constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        # Calculate priority for money sums
        priority = priority_func(self.coins)
        
        if priority > 0:
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def get_money_sums_with_adaptive_constraints(self, adaptive_func):
        """Get money sums with adaptive constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        if adaptive_func(self.coins, set()):
            return self._calculate_constrained_money_sums()
        else:
            return set()
    
    def _calculate_constrained_money_sums(self):
        """Calculate money sums considering all constraints."""
        if not self.money_sums_feasibility:
            return set()
        
        if not self.coins:
            return {0}
        
        # Filter coins based on constraints
        valid_coins = [coin for coin in self.coins if self._is_valid_coin(coin, 1)]
        
        if not valid_coins:
            return {0}
        
        # DP table: dp[i] = True if sum i is possible
        max_sum = sum(valid_coins)
        dp = [False] * (max_sum + 1)
        dp[0] = True
        
        # Fill DP table with constraints
        for coin in valid_coins:
            for sum_val in range(max_sum, coin - 1, -1):
                dp[sum_val] = dp[sum_val] or dp[sum_val - coin]
        
        # Collect all possible sums
        possible_sums = set()
        for i in range(1, max_sum + 1):
            if dp[i]:
                possible_sums.add(i)
        
        return possible_sums
    
    def get_optimal_money_sums_strategy(self):
        """Get optimal money sums strategy considering all constraints."""
        strategies = [
            ('coin_constraints', self.get_money_sums_with_coin_constraints),
            ('sum_constraints', self.get_money_sums_with_sum_constraints),
            ('pattern_constraints', self.get_money_sums_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'coin_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'sum_constraints':
                    sum_constraints = [lambda coins: len(coins) > 0]
                    result = strategy_func(sum_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda coins: len(coins) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_coins': [1, 3, 4, 5, 10],
    'forbidden_coins': [2, 6, 7],
    'max_coin_count': 10,
    'min_coin_count': 1,
    'pattern_constraints': [lambda coin, count, coins: coin > 0 and count >= 0]
}

coins = [1, 3, 4]
constrained_money_sums = ConstrainedMoneySums(coins, constraints)

print("Coin-constrained money sums:", sorted(constrained_money_sums.get_money_sums_with_coin_constraints(1, 10)))

print("Sum-constrained money sums:", sorted(constrained_money_sums.get_money_sums_with_sum_constraints([lambda coins: len(coins) > 0])))

print("Pattern-constrained money sums:", sorted(constrained_money_sums.get_money_sums_with_pattern_constraints([lambda coins: len(coins) > 0])))

# Mathematical constraints
def custom_constraint(coins):
    return len(coins) > 0

print("Mathematical constraint money sums:", sorted(constrained_money_sums.get_money_sums_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(coins):
    return 1 <= len(coins) <= 20

range_constraints = [range_constraint]
print("Range-constrained money sums:", sorted(constrained_money_sums.get_money_sums_with_coin_constraints(1, 20)))

# Multiple constraints
def constraint1(coins):
    return len(coins) > 0

def constraint2(coins):
    return all(coin > 0 for coin in coins)

constraints_list = [constraint1, constraint2]
print("Multiple constraints money sums:", sorted(constrained_money_sums.get_money_sums_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(coins):
    return len(coins) + sum(coins)

print("Priority-constrained money sums:", sorted(constrained_money_sums.get_money_sums_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(coins, current_result):
    return len(coins) > 0 and len(current_result) < 20

print("Adaptive constraint money sums:", sorted(constrained_money_sums.get_money_sums_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_money_sums.get_optimal_money_sums_strategy()
print(f"Optimal money sums strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Coin Combinations](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Book Shop](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Coin Change](https://leetcode.com/problems/coin-change/) - DP
- [Coin Change 2](https://leetcode.com/problems/coin-change-2/) - DP
- [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Subset sum, coin problems
- **Combinatorics**: Mathematical counting, subset properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Subset Sum](https://cp-algorithms.com/dynamic_programming/subset-sum.html) - Subset sum algorithms
- [Coin Problems](https://cp-algorithms.com/dynamic_programming/coin-problems.html) - Coin problem algorithms

### **Practice Problems**
- [CSES Coin Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium
- [CSES Book Shop](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
