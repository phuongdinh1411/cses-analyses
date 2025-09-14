---
layout: simple
title: "Dice Combinations - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/dice_combinations_analysis
---

# Dice Combinations - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of dice combinations in dynamic programming
- Apply counting techniques for dice combination analysis
- Implement efficient algorithms for dice combination counting
- Optimize DP operations for combination analysis
- Handle special cases in dice combination problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, counting techniques, mathematical formulas
- **Data Structures**: Arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Combinations, permutations, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Coin Combinations (dynamic programming), Money Sums (dynamic programming), Array Description (dynamic programming)

## 📋 Problem Description

Given a target sum, count the number of ways to achieve it using dice rolls (1-6).

**Input**: 
- n: target sum

**Output**: 
- Number of ways to achieve sum modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3

Output:
4

Explanation**: 
Ways to achieve sum 3:
1. 1 + 1 + 1 = 3
2. 1 + 2 = 3
3. 2 + 1 = 3
4. 3 = 3
Total: 4 ways
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible dice combinations
- **Complete Enumeration**: Enumerate all possible dice roll sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to achieve the target sum using dice rolls.

**Algorithm**:
- Use recursive function to try all dice rolls
- Calculate sum for each combination
- Count valid combinations
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Target sum = 3:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try dice roll 1: remaining = 2     │
│ - Try dice roll 1: remaining = 1   │
│   - Try dice roll 1: remaining = 0 ✓ │
│ - Try dice roll 2: remaining = 0 ✓ │
│                                   │
│ Try dice roll 2: remaining = 1     │
│ - Try dice roll 1: remaining = 0 ✓ │
│                                   │
│ Try dice roll 3: remaining = 0 ✓   │
│                                   │
│ Total: 4 ways                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_dice_combinations(n, mod=10**9+7):
    """
    Count dice combinations using recursive approach
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    def count_combinations(target):
        """Count combinations recursively"""
        if target == 0:
            return 1  # Valid combination found
        
        if target < 0:
            return 0  # Invalid combination
        
        count = 0
        # Try each dice roll (1-6)
        for dice in range(1, 7):
            count = (count + count_combinations(target - dice)) % mod
        
        return count
    
    return count_combinations(n)

def recursive_dice_combinations_optimized(n, mod=10**9+7):
    """
    Optimized recursive dice combinations counting
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    def count_combinations_optimized(target):
        """Count combinations with optimization"""
        if target == 0:
            return 1  # Valid combination found
        
        if target < 0:
            return 0  # Invalid combination
        
        count = 0
        # Try each dice roll (1-6)
        for dice in range(1, 7):
            count = (count + count_combinations_optimized(target - dice)) % mod
        
        return count
    
    return count_combinations_optimized(n)

# Example usage
n = 3
result1 = recursive_dice_combinations(n)
result2 = recursive_dice_combinations_optimized(n)
print(f"Recursive dice combinations: {result1}")
print(f"Optimized recursive combinations: {result2}")
```

**Time Complexity**: O(6^n)
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
- Use DP table to store number of ways for each sum
- Fill DP table bottom-up
- Return DP[n] as result

**Visual Example**:
```
DP table for target sum = 3:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = 1 (one way: no dice)       │
│ dp[1] = 1 (one way: roll 1)        │
│ dp[2] = 2 (ways: 1+1, 2)           │
│ dp[3] = 4 (ways: 1+1+1, 1+2, 2+1, 3) │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_dice_combinations(n, mod=10**9+7):
    """
    Count dice combinations using dynamic programming approach
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Create DP table
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

def dp_dice_combinations_optimized(n, mod=10**9+7):
    """
    Optimized dynamic programming dice combinations counting
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Create DP table with optimization
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table with optimization
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

# Example usage
n = 3
result1 = dp_dice_combinations(n)
result2 = dp_dice_combinations_optimized(n)
print(f"DP dice combinations: {result1}")
print(f"Optimized DP combinations: {result2}")
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
- **Optimal Complexity**: Best approach for dice combinations counting

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For target sum = 3:
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 4                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_dice_combinations(n, mod=10**9+7):
    """
    Count dice combinations using space-optimized DP approach
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Use only necessary variables for DP
    prev = [0] * 7  # Store previous 6 values
    prev[0] = 1  # Base case
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        current = 0
        for dice in range(1, 7):
            if i >= dice:
                current = (current + prev[dice - 1]) % mod
        
        # Update previous values
        for j in range(6, 0, -1):
            prev[j] = prev[j - 1]
        prev[0] = current
    
    return prev[0]

def space_optimized_dp_dice_combinations_v2(n, mod=10**9+7):
    """
    Alternative space-optimized DP dice combinations counting
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Use only necessary variables for DP
    prev = [0] * 7  # Store previous 6 values
    prev[0] = 1  # Base case
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        current = 0
        for dice in range(1, 7):
            if i >= dice:
                current = (current + prev[dice - 1]) % mod
        
        # Update previous values
        for j in range(6, 0, -1):
            prev[j] = prev[j - 1]
        prev[0] = current
    
    return prev[0]

def dice_combinations_with_precomputation(max_n, mod=10**9+7):
    """
    Precompute dice combinations for multiple queries
    
    Args:
        max_n: maximum value of n
        mod: modulo value
    
    Returns:
        list: precomputed dice combinations
    """
    results = [0] * (max_n + 1)
    
    # Initialize base case
    results[0] = 1
    
    # Fill results using DP
    for i in range(1, max_n + 1):
        for dice in range(1, 7):
            if i >= dice:
                results[i] = (results[i] + results[i - dice]) % mod
    
    return results

# Example usage
n = 3
result1 = space_optimized_dp_dice_combinations(n)
result2 = space_optimized_dp_dice_combinations_v2(n)
print(f"Space-optimized DP dice combinations: {result1}")
print(f"Space-optimized DP dice combinations v2: {result2}")

# Precompute for multiple queries
max_n = 1000000
precomputed = dice_combinations_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses space-optimized DP for O(n) time and O(1) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity to O(1)
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(6^n) | O(n) | Complete enumeration of all dice combinations |
| Dynamic Programming | O(n) | O(n) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n) | O(1) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(n) - Use dynamic programming for efficient calculation
- **Space**: O(1) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Dice Combinations with Constraints**
**Problem**: Count dice combinations with specific constraints.

**Key Differences**: Apply constraints to dice rolls

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_dice_combinations(n, constraints, mod=10**9+7):
    """
    Count dice combinations with constraints
    
    Args:
        n: target sum
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained combinations modulo mod
    """
    # Create DP table
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table with constraints
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice and constraints(dice):  # Check if dice satisfies constraints
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

# Example usage
n = 3
constraints = lambda dice: dice <= 3  # Only use dice with value <= 3
result = constrained_dice_combinations(n, constraints)
print(f"Constrained dice combinations: {result}")
```

#### **2. Dice Combinations with Multiple Dice Types**
**Problem**: Count dice combinations with multiple types of dice.

**Key Differences**: Handle multiple types of dice

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_dice_combinations(n, dice_types, mod=10**9+7):
    """
    Count dice combinations with multiple types of dice
    
    Args:
        n: target sum
        dice_types: list of dice types
        mod: modulo value
    
    Returns:
        int: number of combinations modulo mod
    """
    # Create DP table
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table with multiple dice types
    for i in range(1, n + 1):
        for dice in dice_types:
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

# Example usage
n = 3
dice_types = [1, 2, 3, 4, 5, 6]  # Standard dice
result = multi_dice_combinations(n, dice_types)
print(f"Multi-dice combinations: {result}")
```

#### **3. Dice Combinations with Multiple Targets**
**Problem**: Count dice combinations for multiple target values.

**Key Differences**: Handle multiple target values

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_target_dice_combinations(targets, mod=10**9+7):
    """
    Count dice combinations for multiple target values
    
    Args:
        targets: list of target values
        mod: modulo value
    
    Returns:
        int: number of achievable targets modulo mod
    """
    max_target = max(targets)
    
    # Create DP table
    dp = [0] * (max_target + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table
    for i in range(1, max_target + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    # Count achievable targets
    count = sum(1 for target in targets if dp[target] > 0)
    
    return count % mod

# Example usage
targets = [3, 4, 5, 6]  # Check if these targets are achievable
result = multi_target_dice_combinations(targets)
print(f"Multi-target dice combinations: {result}")
```

## Problem Variations

### **Variation 1: Dice Combinations with Dynamic Updates**
**Problem**: Handle dynamic dice updates (add/remove/update dice faces) while maintaining optimal dice combination counting efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic dice management.

```python
from collections import defaultdict

class DynamicDiceCombinations:
    def __init__(self, target=None, dice_faces=None):
        self.target = target or 0
        self.dice_faces = dice_faces or 6  # Standard 6-sided die
        self.combinations = []
        self._update_dice_combinations_info()
    
    def _update_dice_combinations_info(self):
        """Update dice combinations feasibility information."""
        self.dice_combinations_feasibility = self._calculate_dice_combinations_feasibility()
    
    def _calculate_dice_combinations_feasibility(self):
        """Calculate dice combinations feasibility."""
        if self.target <= 0 or self.dice_faces <= 0:
            return 0.0
        
        # Check if we can make the target with available dice faces
        return 1.0 if self.dice_faces > 0 and self.target > 0 else 0.0
    
    def update_target(self, new_target):
        """Update target sum."""
        self.target = new_target
        self._update_dice_combinations_info()
    
    def update_dice_faces(self, new_faces):
        """Update number of dice faces."""
        self.dice_faces = new_faces
        self._update_dice_combinations_info()
    
    def count_combinations(self):
        """Count number of ways to make target using dynamic programming."""
        if self.target <= 0 or self.dice_faces <= 0:
            return 0
        
        # DP table: dp[i] = number of ways to make sum i
        dp = [0] * (self.target + 1)
        dp[0] = 1  # One way to make sum 0 (use no dice)
        
        # For each sum from 1 to target
        for sum_val in range(1, self.target + 1):
            # For each dice face
            for face in range(1, self.dice_faces + 1):
                if face <= sum_val:
                    dp[sum_val] += dp[sum_val - face]
        
        return dp[self.target]
    
    def get_combinations_with_constraints(self, constraint_func):
        """Get combinations that satisfies custom constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        count = self.count_combinations()
        if constraint_func(count, self.target, self.dice_faces):
            return self._generate_combinations()
        else:
            return []
    
    def get_combinations_in_range(self, min_count, max_count):
        """Get combinations within specified count range."""
        if not self.dice_combinations_feasibility:
            return []
        
        count = self.count_combinations()
        if min_count <= count <= max_count:
            return self._generate_combinations()
        else:
            return []
    
    def get_combinations_with_pattern(self, pattern_func):
        """Get combinations matching specified pattern."""
        if not self.dice_combinations_feasibility:
            return []
        
        count = self.count_combinations()
        if pattern_func(count, self.target, self.dice_faces):
            return self._generate_combinations()
        else:
            return []
    
    def _generate_combinations(self):
        """Generate all possible dice combinations."""
        if not self.dice_combinations_feasibility:
            return []
        
        combinations = []
        
        def backtrack(remaining, current_combination):
            if remaining == 0:
                combinations.append(current_combination[:])
                return
            
            if remaining < 0:
                return
            
            for face in range(1, self.dice_faces + 1):
                if face <= remaining:
                    current_combination.append(face)
                    backtrack(remaining - face, current_combination)
                    current_combination.pop()
        
        backtrack(self.target, [])
        return combinations
    
    def get_dice_combinations_statistics(self):
        """Get statistics about the dice combinations."""
        if not self.dice_combinations_feasibility:
            return {
                'target': 0,
                'dice_faces': 0,
                'dice_combinations_feasibility': 0,
                'combination_count': 0
            }
        
        count = self.count_combinations()
        return {
            'target': self.target,
            'dice_faces': self.dice_faces,
            'dice_combinations_feasibility': self.dice_combinations_feasibility,
            'combination_count': count
        }
    
    def get_dice_combinations_patterns(self):
        """Get patterns in dice combinations."""
        patterns = {
            'target_achievable': 0,
            'has_valid_dice': 0,
            'optimal_combinations_possible': 0,
            'has_large_target': 0
        }
        
        if not self.dice_combinations_feasibility:
            return patterns
        
        # Check if target is achievable
        if self.dice_combinations_feasibility == 1.0:
            patterns['target_achievable'] = 1
        
        # Check if has valid dice
        if self.dice_faces > 0:
            patterns['has_valid_dice'] = 1
        
        # Check if optimal combinations are possible
        if self.dice_combinations_feasibility == 1.0:
            patterns['optimal_combinations_possible'] = 1
        
        # Check if has large target
        if self.target > 20:
            patterns['has_large_target'] = 1
        
        return patterns
    
    def get_optimal_dice_combinations_strategy(self):
        """Get optimal strategy for dice combinations counting."""
        if not self.dice_combinations_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'dice_combinations_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.dice_combinations_feasibility
        
        # Calculate dice combinations feasibility
        dice_combinations_feasibility = self.dice_combinations_feasibility
        
        # Determine recommended strategy
        if self.target <= 20:
            recommended_strategy = 'dynamic_programming'
        elif self.target <= 100:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'dice_combinations_feasibility': dice_combinations_feasibility
        }

# Example usage
target = 8
dice_faces = 6
dynamic_dice_combinations = DynamicDiceCombinations(target, dice_faces)
print(f"Dice combinations feasibility: {dynamic_dice_combinations.dice_combinations_feasibility}")

# Update target
dynamic_dice_combinations.update_target(10)
print(f"After updating target to 10: {dynamic_dice_combinations.target}")

# Update dice faces
dynamic_dice_combinations.update_dice_faces(8)
print(f"After updating dice faces to 8: {dynamic_dice_combinations.dice_faces}")

# Count combinations
count = dynamic_dice_combinations.count_combinations()
print(f"Number of combinations: {count}")

# Get combinations with constraints
def constraint_func(count, target, dice_faces):
    return count > 0 and target > 0 and dice_faces > 0

print(f"Combinations with constraints: {len(dynamic_dice_combinations.get_combinations_with_constraints(constraint_func))}")

# Get combinations in range
print(f"Combinations in range 1-100: {len(dynamic_dice_combinations.get_combinations_in_range(1, 100))}")

# Get combinations with pattern
def pattern_func(count, target, dice_faces):
    return count > 0 and target > 0 and dice_faces > 0

print(f"Combinations with pattern: {len(dynamic_dice_combinations.get_combinations_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_dice_combinations.get_dice_combinations_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_dice_combinations.get_dice_combinations_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_dice_combinations.get_optimal_dice_combinations_strategy()}")
```

### **Variation 2: Dice Combinations with Different Operations**
**Problem**: Handle different types of dice combination operations (weighted dice, priority-based counting, advanced dice analysis).

**Approach**: Use advanced data structures for efficient different types of dice combination operations.

```python
class AdvancedDiceCombinations:
    def __init__(self, target=None, dice_faces=None, weights=None, priorities=None):
        self.target = target or 0
        self.dice_faces = dice_faces or 6
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.combinations = []
        self._update_dice_combinations_info()
    
    def _update_dice_combinations_info(self):
        """Update dice combinations feasibility information."""
        self.dice_combinations_feasibility = self._calculate_dice_combinations_feasibility()
    
    def _calculate_dice_combinations_feasibility(self):
        """Calculate dice combinations feasibility."""
        if self.target <= 0 or self.dice_faces <= 0:
            return 0.0
        
        # Check if we can make the target with available dice faces
        return 1.0 if self.dice_faces > 0 and self.target > 0 else 0.0
    
    def count_combinations(self):
        """Count number of ways to make target using dynamic programming."""
        if self.target <= 0 or self.dice_faces <= 0:
            return 0
        
        # DP table: dp[i] = number of ways to make sum i
        dp = [0] * (self.target + 1)
        dp[0] = 1  # One way to make sum 0 (use no dice)
        
        # For each sum from 1 to target
        for sum_val in range(1, self.target + 1):
            # For each dice face
            for face in range(1, self.dice_faces + 1):
                if face <= sum_val:
                    dp[sum_val] += dp[sum_val - face]
        
        return dp[self.target]
    
    def get_weighted_combinations(self):
        """Get combinations with weights and priorities applied."""
        if not self.dice_combinations_feasibility:
            return []
        
        # Create weighted dice faces
        weighted_faces = []
        for face in range(1, self.dice_faces + 1):
            weight = self.weights.get(face, 1)
            priority = self.priorities.get(face, 1)
            weighted_score = face * weight * priority
            weighted_faces.append((face, weighted_score))
        
        # Sort by weighted score
        weighted_faces.sort(key=lambda x: x[1], reverse=True)
        
        # Generate combinations with weighted faces
        combinations = []
        
        def backtrack(remaining, current_combination):
            if remaining == 0:
                combinations.append(current_combination[:])
                return
            
            if remaining < 0:
                return
            
            for face, score in weighted_faces:
                if face <= remaining:
                    current_combination.append(face)
                    backtrack(remaining - face, current_combination)
                    current_combination.pop()
        
        backtrack(self.target, [])
        return combinations
    
    def get_combinations_with_priority(self, priority_func):
        """Get combinations considering priority."""
        if not self.dice_combinations_feasibility:
            return []
        
        # Create priority-based faces
        priority_faces = []
        for face in range(1, self.dice_faces + 1):
            priority = priority_func(face, self.weights, self.priorities)
            priority_faces.append((face, priority))
        
        # Sort by priority
        priority_faces.sort(key=lambda x: x[1], reverse=True)
        
        # Generate combinations with priority faces
        combinations = []
        
        def backtrack(remaining, current_combination):
            if remaining == 0:
                combinations.append(current_combination[:])
                return
            
            if remaining < 0:
                return
            
            for face, priority in priority_faces:
                if face <= remaining:
                    current_combination.append(face)
                    backtrack(remaining - face, current_combination)
                    current_combination.pop()
        
        backtrack(self.target, [])
        return combinations
    
    def get_combinations_with_optimization(self, optimization_func):
        """Get combinations using custom optimization function."""
        if not self.dice_combinations_feasibility:
            return []
        
        # Create optimization-based faces
        optimized_faces = []
        for face in range(1, self.dice_faces + 1):
            score = optimization_func(face, self.weights, self.priorities)
            optimized_faces.append((face, score))
        
        # Sort by optimization score
        optimized_faces.sort(key=lambda x: x[1], reverse=True)
        
        # Generate combinations with optimized faces
        combinations = []
        
        def backtrack(remaining, current_combination):
            if remaining == 0:
                combinations.append(current_combination[:])
                return
            
            if remaining < 0:
                return
            
            for face, score in optimized_faces:
                if face <= remaining:
                    current_combination.append(face)
                    backtrack(remaining - face, current_combination)
                    current_combination.pop()
        
        backtrack(self.target, [])
        return combinations
    
    def get_combinations_with_constraints(self, constraint_func):
        """Get combinations that satisfies custom constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        if constraint_func(self.target, self.dice_faces, self.weights, self.priorities):
            return self.get_weighted_combinations()
        else:
            return []
    
    def get_combinations_with_multiple_criteria(self, criteria_list):
        """Get combinations that satisfies multiple criteria."""
        if not self.dice_combinations_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.target, self.dice_faces, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_combinations()
        else:
            return []
    
    def get_combinations_with_alternatives(self, alternatives):
        """Get combinations considering alternative weights/priorities."""
        result = []
        
        # Check original combinations
        original_combinations = self.get_weighted_combinations()
        result.append((original_combinations, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedDiceCombinations(self.target, self.dice_faces, alt_weights, alt_priorities)
            temp_combinations = temp_instance.get_weighted_combinations()
            result.append((temp_combinations, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_combinations_with_adaptive_criteria(self, adaptive_func):
        """Get combinations using adaptive criteria."""
        if not self.dice_combinations_feasibility:
            return []
        
        if adaptive_func(self.target, self.dice_faces, self.weights, self.priorities, []):
            return self.get_weighted_combinations()
        else:
            return []
    
    def get_dice_combinations_optimization(self):
        """Get optimal dice combinations configuration."""
        strategies = [
            ('weighted_combinations', lambda: len(self.get_weighted_combinations())),
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
target = 8
dice_faces = 6
weights = {face: face * 2 for face in range(1, dice_faces + 1)}  # Weight based on face value
priorities = {face: face // 2 for face in range(1, dice_faces + 1)}  # Priority based on face value
advanced_dice_combinations = AdvancedDiceCombinations(target, dice_faces, weights, priorities)

print(f"Weighted combinations: {len(advanced_dice_combinations.get_weighted_combinations())}")

# Get combinations with priority
def priority_func(face, weights, priorities):
    return weights.get(face, 1) + priorities.get(face, 1)

print(f"Combinations with priority: {len(advanced_dice_combinations.get_combinations_with_priority(priority_func))}")

# Get combinations with optimization
def optimization_func(face, weights, priorities):
    return weights.get(face, 1) * priorities.get(face, 1)

print(f"Combinations with optimization: {len(advanced_dice_combinations.get_combinations_with_optimization(optimization_func))}")

# Get combinations with constraints
def constraint_func(target, dice_faces, weights, priorities):
    return target > 0 and dice_faces > 0

print(f"Combinations with constraints: {len(advanced_dice_combinations.get_combinations_with_constraints(constraint_func))}")

# Get combinations with multiple criteria
def criterion1(target, dice_faces, weights, priorities):
    return target > 0

def criterion2(target, dice_faces, weights, priorities):
    return dice_faces > 0

criteria_list = [criterion1, criterion2]
print(f"Combinations with multiple criteria: {len(advanced_dice_combinations.get_combinations_with_multiple_criteria(criteria_list))}")

# Get combinations with alternatives
alternatives = [({face: 1 for face in range(1, dice_faces + 1)}, {face: 1 for face in range(1, dice_faces + 1)}), ({face: face*3 for face in range(1, dice_faces + 1)}, {face: face+1 for face in range(1, dice_faces + 1)})]
print(f"Combinations with alternatives: {advanced_dice_combinations.get_combinations_with_alternatives(alternatives)}")

# Get combinations with adaptive criteria
def adaptive_func(target, dice_faces, weights, priorities, current_result):
    return target > 0 and dice_faces > 0 and len(current_result) < 5

print(f"Combinations with adaptive criteria: {len(advanced_dice_combinations.get_combinations_with_adaptive_criteria(adaptive_func))}")

# Get dice combinations optimization
print(f"Dice combinations optimization: {advanced_dice_combinations.get_dice_combinations_optimization()}")
```

### **Variation 3: Dice Combinations with Constraints**
**Problem**: Handle dice combination counting with additional constraints (target limits, face constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedDiceCombinations:
    def __init__(self, target=None, dice_faces=None, constraints=None):
        self.target = target or 0
        self.dice_faces = dice_faces or 6
        self.constraints = constraints or {}
        self.combinations = []
        self._update_dice_combinations_info()
    
    def _update_dice_combinations_info(self):
        """Update dice combinations feasibility information."""
        self.dice_combinations_feasibility = self._calculate_dice_combinations_feasibility()
    
    def _calculate_dice_combinations_feasibility(self):
        """Calculate dice combinations feasibility."""
        if self.target <= 0 or self.dice_faces <= 0:
            return 0.0
        
        # Check if we can make the target with available dice faces
        return 1.0 if self.dice_faces > 0 and self.target > 0 else 0.0
    
    def _is_valid_combination(self, combination):
        """Check if combination is valid considering constraints."""
        # Target constraints
        if 'min_target' in self.constraints:
            if sum(combination) < self.constraints['min_target']:
                return False
        
        if 'max_target' in self.constraints:
            if sum(combination) > self.constraints['max_target']:
                return False
        
        # Face constraints
        if 'forbidden_faces' in self.constraints:
            if any(face in self.constraints['forbidden_faces'] for face in combination):
                return False
        
        if 'required_faces' in self.constraints:
            if not all(face in combination for face in self.constraints['required_faces']):
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(combination):
                    return False
        
        return True
    
    def get_combinations_with_target_constraints(self, min_target, max_target):
        """Get combinations considering target constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        combinations = self._generate_combinations()
        valid_combinations = []
        
        for combination in combinations:
            if min_target <= sum(combination) <= max_target and self._is_valid_combination(combination):
                valid_combinations.append(combination)
        
        return valid_combinations
    
    def get_combinations_with_face_constraints(self, face_constraints):
        """Get combinations considering face constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in face_constraints:
            if not constraint(self.target, self.dice_faces):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            combinations = self._generate_combinations()
            valid_combinations = []
            
            for combination in combinations:
                if self._is_valid_combination(combination):
                    valid_combinations.append(combination)
            
            return valid_combinations
        
        return []
    
    def get_combinations_with_pattern_constraints(self, pattern_constraints):
        """Get combinations considering pattern constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.target, self.dice_faces):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            combinations = self._generate_combinations()
            valid_combinations = []
            
            for combination in combinations:
                if self._is_valid_combination(combination):
                    valid_combinations.append(combination)
            
            return valid_combinations
        
        return []
    
    def get_combinations_with_mathematical_constraints(self, constraint_func):
        """Get combinations that satisfies custom mathematical constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        if constraint_func(self.target, self.dice_faces):
            combinations = self._generate_combinations()
            valid_combinations = []
            
            for combination in combinations:
                if self._is_valid_combination(combination):
                    valid_combinations.append(combination)
            
            return valid_combinations
        
        return []
    
    def get_combinations_with_optimization_constraints(self, optimization_func):
        """Get combinations using custom optimization constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        # Calculate optimization score for combinations
        score = optimization_func(self.target, self.dice_faces)
        
        if score > 0:
            combinations = self._generate_combinations()
            valid_combinations = []
            
            for combination in combinations:
                if self._is_valid_combination(combination):
                    valid_combinations.append(combination)
            
            return valid_combinations
        
        return []
    
    def get_combinations_with_multiple_constraints(self, constraints_list):
        """Get combinations that satisfies multiple constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.target, self.dice_faces):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            combinations = self._generate_combinations()
            valid_combinations = []
            
            for combination in combinations:
                if self._is_valid_combination(combination):
                    valid_combinations.append(combination)
            
            return valid_combinations
        
        return []
    
    def get_combinations_with_priority_constraints(self, priority_func):
        """Get combinations with priority-based constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        # Calculate priority for combinations
        priority = priority_func(self.target, self.dice_faces)
        
        if priority > 0:
            combinations = self._generate_combinations()
            valid_combinations = []
            
            for combination in combinations:
                if self._is_valid_combination(combination):
                    valid_combinations.append(combination)
            
            return valid_combinations
        
        return []
    
    def get_combinations_with_adaptive_constraints(self, adaptive_func):
        """Get combinations with adaptive constraints."""
        if not self.dice_combinations_feasibility:
            return []
        
        if adaptive_func(self.target, self.dice_faces, []):
            combinations = self._generate_combinations()
            valid_combinations = []
            
            for combination in combinations:
                if self._is_valid_combination(combination):
                    valid_combinations.append(combination)
            
            return valid_combinations
        
        return []
    
    def _generate_combinations(self):
        """Generate all possible dice combinations."""
        if not self.dice_combinations_feasibility:
            return []
        
        combinations = []
        
        def backtrack(remaining, current_combination):
            if remaining == 0:
                combinations.append(current_combination[:])
                return
            
            if remaining < 0:
                return
            
            for face in range(1, self.dice_faces + 1):
                if face <= remaining:
                    current_combination.append(face)
                    backtrack(remaining - face, current_combination)
                    current_combination.pop()
        
        backtrack(self.target, [])
        return combinations
    
    def get_optimal_dice_combinations_strategy(self):
        """Get optimal dice combinations strategy considering all constraints."""
        strategies = [
            ('target_constraints', self.get_combinations_with_target_constraints),
            ('face_constraints', self.get_combinations_with_face_constraints),
            ('pattern_constraints', self.get_combinations_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'target_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'face_constraints':
                    face_constraints = [lambda target, dice_faces: target > 0 and dice_faces > 0]
                    result = strategy_func(face_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda target, dice_faces: target > 0 and dice_faces > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_target': 5,
    'max_target': 15,
    'forbidden_faces': [1],
    'required_faces': [2],
    'pattern_constraints': [lambda combination: len(combination) > 0 and all(face > 0 for face in combination)]
}

target = 8
dice_faces = 6
constrained_dice_combinations = ConstrainedDiceCombinations(target, dice_faces, constraints)

print("Target-constrained combinations:", len(constrained_dice_combinations.get_combinations_with_target_constraints(5, 15)))

print("Face-constrained combinations:", len(constrained_dice_combinations.get_combinations_with_face_constraints([lambda target, dice_faces: target > 0 and dice_faces > 0])))

print("Pattern-constrained combinations:", len(constrained_dice_combinations.get_combinations_with_pattern_constraints([lambda target, dice_faces: target > 0 and dice_faces > 0])))

# Mathematical constraints
def custom_constraint(target, dice_faces):
    return target > 0 and dice_faces > 0

print("Mathematical constraint combinations:", len(constrained_dice_combinations.get_combinations_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(target, dice_faces):
    return 1 <= target <= 20 and 1 <= dice_faces <= 10

range_constraints = [range_constraint]
print("Range-constrained combinations:", len(constrained_dice_combinations.get_combinations_with_target_constraints(1, 20)))

# Multiple constraints
def constraint1(target, dice_faces):
    return target > 0

def constraint2(target, dice_faces):
    return dice_faces > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints combinations:", len(constrained_dice_combinations.get_combinations_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(target, dice_faces):
    return target + dice_faces

print("Priority-constrained combinations:", len(constrained_dice_combinations.get_combinations_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(target, dice_faces, current_result):
    return target > 0 and dice_faces > 0 and len(current_result) < 5

print("Adaptive constraint combinations:", len(constrained_dice_combinations.get_combinations_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_dice_combinations.get_optimal_dice_combinations_strategy()
print(f"Optimal dice combinations strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Coin Combinations](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Money Sums](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Coin Change](https://leetcode.com/problems/coin-change/) - DP
- [Coin Change 2](https://leetcode.com/problems/coin-change-2/) - DP
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Combination counting, path problems
- **Combinatorics**: Mathematical counting, combination properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Coin Problems](https://cp-algorithms.com/dynamic_programming/coin-problems.html) - Coin problem algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Coin Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Money Sums](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
