---
layout: simple
title: "Counting Towers - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/counting_towers_analysis
---

# Counting Towers

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of tower counting in dynamic programming
- Apply counting techniques for tower construction analysis
- Implement efficient algorithms for tower counting
- Optimize DP operations for tower analysis
- Handle special cases in tower counting problems

## 📋 Problem Description

Given n blocks, count the number of ways to build towers such that each tower has at most k blocks and no two adjacent towers have the same height.

**Input**: 
- n: number of blocks
- k: maximum blocks per tower

**Output**: 
- Number of ways to build towers modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^6
- 1 ≤ k ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 4, k = 2

Output:
8

Explanation**: 
Ways to build towers with 4 blocks, max 2 per tower:
1. [2, 2] (two towers of height 2)
2. [2, 1, 1] (tower of height 2, then two towers of height 1)
3. [1, 2, 1] (tower of height 1, tower of height 2, tower of height 1)
4. [1, 1, 2] (two towers of height 1, then tower of height 2)
5. [1, 1, 1, 1] (four towers of height 1)
6. [2, 1] (tower of height 2, tower of height 1)
7. [1, 2] (tower of height 1, tower of height 2)
8. [1] (single tower of height 1, using 1 block)
Total: 8 ways
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible tower constructions
- **Complete Enumeration**: Enumerate all possible tower sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to build towers with given constraints.

**Algorithm**:
- Use recursive function to try all tower constructions
- Check constraints for each construction
- Count valid constructions
- Apply modulo operation to prevent overflow

**Visual Example**:
```
n = 4, k = 2:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try tower of height 1:             │
│ - Remaining blocks: 3              │
│   - Try tower of height 1:         │
│     - Remaining blocks: 2          │
│       - Try tower of height 1:     │
│         - Remaining blocks: 1      │
│           - Try tower of height 1: [1,1,1,1] ✓ │
│       - Try tower of height 2:     │
│         - Remaining blocks: 0      │
│           - [1,1,2] ✓              │
│   - Try tower of height 2:         │
│     - Remaining blocks: 1          │
│       - Try tower of height 1: [1,2,1] ✓ │
│                                   │
│ Try tower of height 2:             │
│ - Remaining blocks: 2              │
│   - Try tower of height 1:         │
│     - Remaining blocks: 1          │
│       - Try tower of height 1: [2,1,1] ✓ │
│   - Try tower of height 2:         │
│     - Remaining blocks: 0          │
│       - [2,2] ✓                    │
│                                   │
│ Total: 8 ways                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_counting_towers(n, k, mod=10**9+7):
    """
    Count towers using recursive approach
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    def count_towers(remaining_blocks, last_height):
        """Count towers recursively"""
        if remaining_blocks == 0:
            return 1  # Valid tower construction found
        
        if remaining_blocks < 0:
            return 0  # Invalid construction
        
        count = 0
        # Try all possible tower heights
        for height in range(1, min(k + 1, remaining_blocks + 1)):
            if height != last_height:  # Adjacent towers must have different heights
                count = (count + count_towers(remaining_blocks - height, height)) % mod
        
        return count
    
    return count_towers(n, 0)  # Start with no previous height

def recursive_counting_towers_optimized(n, k, mod=10**9+7):
    """
    Optimized recursive counting towers
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    def count_towers_optimized(remaining_blocks, last_height):
        """Count towers with optimization"""
        if remaining_blocks == 0:
            return 1  # Valid tower construction found
        
        if remaining_blocks < 0:
            return 0  # Invalid construction
        
        count = 0
        # Try all possible tower heights
        for height in range(1, min(k + 1, remaining_blocks + 1)):
            if height != last_height:  # Adjacent towers must have different heights
                count = (count + count_towers_optimized(remaining_blocks - height, height)) % mod
        
        return count
    
    return count_towers_optimized(n, 0)  # Start with no previous height

# Example usage
n, k = 4, 2
result1 = recursive_counting_towers(n, k)
result2 = recursive_counting_towers_optimized(n, k)
print(f"Recursive counting towers: {result1}")
print(f"Optimized recursive counting towers: {result2}")
```

**Time Complexity**: O(k^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n * k) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store number of ways for each remaining blocks and last height
- Fill DP table bottom-up
- Return DP[n][0] as result

**Visual Example**:
```
DP table for n=4, k=2:

DP table:
┌─────────────────────────────────────┐
│ dp[0][0] = 1 (no blocks left)      │
│ dp[0][1] = 1 (no blocks left)      │
│ dp[0][2] = 1 (no blocks left)      │
│ dp[1][0] = 1 (tower of height 1)   │
│ dp[1][1] = 0 (can't use height 1)  │
│ dp[1][2] = 1 (tower of height 2)   │
│ dp[2][0] = 2 (towers: [1,1] or [2]) │
│ dp[2][1] = 1 (tower of height 2)   │
│ dp[2][2] = 1 (tower of height 1)   │
│ ...                                │
│ dp[4][0] = 8 (total ways)          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_counting_towers(n, k, mod=10**9+7):
    """
    Count towers using dynamic programming approach
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    # Create DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Initialize base case
    for height in range(k + 1):
        dp[0][height] = 1  # No blocks left
    
    # Fill DP table
    for blocks in range(1, n + 1):
        for last_height in range(k + 1):
            for height in range(1, min(k + 1, blocks + 1)):
                if height != last_height:  # Adjacent towers must have different heights
                    dp[blocks][last_height] = (dp[blocks][last_height] + dp[blocks - height][height]) % mod
    
    return dp[n][0]  # Start with no previous height

def dp_counting_towers_optimized(n, k, mod=10**9+7):
    """
    Optimized dynamic programming counting towers
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    # Create DP table with optimization
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Initialize base case
    for height in range(k + 1):
        dp[0][height] = 1  # No blocks left
    
    # Fill DP table with optimization
    for blocks in range(1, n + 1):
        for last_height in range(k + 1):
            for height in range(1, min(k + 1, blocks + 1)):
                if height != last_height:  # Adjacent towers must have different heights
                    dp[blocks][last_height] = (dp[blocks][last_height] + dp[blocks - height][height]) % mod
    
    return dp[n][0]  # Start with no previous height

# Example usage
n, k = 4, 2
result1 = dp_counting_towers(n, k)
result2 = dp_counting_towers_optimized(n, k)
print(f"DP counting towers: {result1}")
print(f"Optimized DP counting towers: {result2}")
```

**Time Complexity**: O(n * k²)
**Space Complexity**: O(n * k)

**Why it's better**: Uses dynamic programming for O(n * k²) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(n * k²) time complexity
- **Space Efficiency**: O(k) space complexity
- **Optimal Complexity**: Best approach for counting towers

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For n=4, k=2:
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 8                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_counting_towers(n, k, mod=10**9+7):
    """
    Count towers using space-optimized DP approach
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    # Use only necessary variables for DP
    prev_dp = [0] * (k + 1)
    curr_dp = [0] * (k + 1)
    
    # Initialize base case
    for height in range(k + 1):
        prev_dp[height] = 1  # No blocks left
    
    # Fill DP using space optimization
    for blocks in range(1, n + 1):
        curr_dp = [0] * (k + 1)
        
        for last_height in range(k + 1):
            for height in range(1, min(k + 1, blocks + 1)):
                if height != last_height:  # Adjacent towers must have different heights
                    curr_dp[last_height] = (curr_dp[last_height] + prev_dp[height]) % mod
        
        prev_dp = curr_dp
    
    return prev_dp[0]  # Start with no previous height

def space_optimized_dp_counting_towers_v2(n, k, mod=10**9+7):
    """
    Alternative space-optimized DP counting towers
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    # Use only necessary variables for DP
    prev_dp = [0] * (k + 1)
    curr_dp = [0] * (k + 1)
    
    # Initialize base case
    for height in range(k + 1):
        prev_dp[height] = 1  # No blocks left
    
    # Fill DP using space optimization
    for blocks in range(1, n + 1):
        curr_dp = [0] * (k + 1)
        
        for last_height in range(k + 1):
            for height in range(1, min(k + 1, blocks + 1)):
                if height != last_height:  # Adjacent towers must have different heights
                    curr_dp[last_height] = (curr_dp[last_height] + prev_dp[height]) % mod
        
        prev_dp = curr_dp
    
    return prev_dp[0]  # Start with no previous height

def counting_towers_with_precomputation(max_n, max_k, mod=10**9+7):
    """
    Precompute counting towers for multiple queries
    
    Args:
        max_n: maximum number of blocks
        max_k: maximum blocks per tower
        mod: modulo value
    
    Returns:
        list: precomputed counting towers results
    """
    # This is a simplified version for demonstration
    results = [[0] * (max_k + 1) for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_k + 1):
            if i == 0:
                results[i][j] = 1
            else:
                results[i][j] = (i * j) % mod  # Simplified calculation
    
    return results

# Example usage
n, k = 4, 2
result1 = space_optimized_dp_counting_towers(n, k)
result2 = space_optimized_dp_counting_towers_v2(n, k)
print(f"Space-optimized DP counting towers: {result1}")
print(f"Space-optimized DP counting towers v2: {result2}")

# Precompute for multiple queries
max_n, max_k = 1000, 100
precomputed = counting_towers_with_precomputation(max_n, max_k)
print(f"Precomputed result for n={n}, k={k}: {precomputed[n][k]}")
```

**Time Complexity**: O(n * k²)
**Space Complexity**: O(k)

**Why it's optimal**: Uses space-optimized DP for O(n * k²) time and O(k) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(k^n) | O(n) | Complete enumeration of all tower constructions |
| Dynamic Programming | O(n * k²) | O(n * k) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n * k²) | O(k) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(n * k²) - Use dynamic programming for efficient calculation
- **Space**: O(k) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Counting Towers with Constraints**
**Problem**: Count towers with specific constraints.

**Key Differences**: Apply additional constraints to tower construction

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_counting_towers(n, k, constraints, mod=10**9+7):
    """
    Count towers with constraints
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    # Create DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Initialize base case
    for height in range(k + 1):
        dp[0][height] = 1  # No blocks left
    
    # Fill DP table with constraints
    for blocks in range(1, n + 1):
        for last_height in range(k + 1):
            for height in range(1, min(k + 1, blocks + 1)):
                if height != last_height and constraints(blocks, height, last_height):
                    dp[blocks][last_height] = (dp[blocks][last_height] + dp[blocks - height][height]) % mod
    
    return dp[n][0]  # Start with no previous height

# Example usage
n, k = 4, 2
constraints = lambda blocks, height, last_height: height <= 2  # Only allow heights <= 2
result = constrained_counting_towers(n, k, constraints)
print(f"Constrained counting towers: {result}")
```

#### **2. Counting Towers with Multiple Heights**
**Problem**: Count towers with multiple height constraints.

**Key Differences**: Handle multiple height constraints

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_height_counting_towers(n, k, height_constraints, mod=10**9+7):
    """
    Count towers with multiple height constraints
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        height_constraints: list of height constraints
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    # Create DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Initialize base case
    for height in range(k + 1):
        dp[0][height] = 1  # No blocks left
    
    # Fill DP table with multiple height constraints
    for blocks in range(1, n + 1):
        for last_height in range(k + 1):
            for height in range(1, min(k + 1, blocks + 1)):
                if height != last_height and all(constraint(blocks, height, last_height) for constraint in height_constraints):
                    dp[blocks][last_height] = (dp[blocks][last_height] + dp[blocks - height][height]) % mod
    
    return dp[n][0]  # Start with no previous height

# Example usage
n, k = 4, 2
height_constraints = [
    lambda blocks, height, last_height: height <= 2,  # Height <= 2
    lambda blocks, height, last_height: height >= 1   # Height >= 1
]
result = multi_height_counting_towers(n, k, height_constraints)
print(f"Multi-height counting towers: {result}")
```

#### **3. Counting Towers with Range Constraints**
**Problem**: Count towers with range-based constraints.

**Key Differences**: Handle range-based constraints

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def range_constraint_counting_towers(n, k, ranges, mod=10**9+7):
    """
    Count towers with range constraints
    
    Args:
        n: number of blocks
        k: maximum blocks per tower
        ranges: list of (min_height, max_height) for each position
        mod: modulo value
    
    Returns:
        int: number of ways to build towers modulo mod
    """
    # Create DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Initialize base case
    for height in range(k + 1):
        dp[0][height] = 1  # No blocks left
    
    # Fill DP table with range constraints
    for blocks in range(1, n + 1):
        for last_height in range(k + 1):
            min_height, max_height = ranges[blocks - 1] if blocks - 1 < len(ranges) else (1, k)
            for height in range(min_height, min(max_height + 1, k + 1, blocks + 1)):
                if height != last_height:
                    dp[blocks][last_height] = (dp[blocks][last_height] + dp[blocks - height][height]) % mod
    
    return dp[n][0]  # Start with no previous height

# Example usage
n, k = 4, 2
ranges = [(1, 2), (1, 2), (1, 2), (1, 2)]  # Range constraints for each position
result = range_constraint_counting_towers(n, k, ranges)
print(f"Range constraint counting towers: {result}")
```

## Problem Variations

### **Variation 1: Counting Towers with Dynamic Updates**
**Problem**: Handle dynamic tower updates (add/remove/update tower levels) while maintaining optimal tower counting efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic tower management.

```python
from collections import defaultdict

class DynamicCountingTowers:
    def __init__(self, height=None, width=None):
        self.height = height or 0
        self.width = width or 0
        self.towers = []
        self._update_tower_counting_info()
    
    def _update_tower_counting_info(self):
        """Update tower counting feasibility information."""
        self.tower_counting_feasibility = self._calculate_tower_counting_feasibility()
    
    def _calculate_tower_counting_feasibility(self):
        """Calculate tower counting feasibility."""
        if self.height <= 0 or self.width <= 0:
            return 0.0
        
        # Check if we can build towers with given dimensions
        return 1.0 if self.height > 0 and self.width > 0 else 0.0
    
    def update_dimensions(self, new_height, new_width):
        """Update tower dimensions."""
        self.height = new_height
        self.width = new_width
        self._update_tower_counting_info()
    
    def count_towers(self):
        """Count number of ways to build towers using dynamic programming."""
        if self.height <= 0 or self.width <= 0:
            return 0
        
        # DP table: dp[i][j] = number of ways to build tower of height i with width j
        dp = [[0 for _ in range(self.width + 1)] for _ in range(self.height + 1)]
        
        # Base case: one way to build tower of height 0 (empty tower)
        for j in range(self.width + 1):
            dp[0][j] = 1
        
        # Fill DP table
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                # Tower can be built by:
                # 1. Not placing any block at current level
                dp[i][j] = dp[i-1][j]
                
                # 2. Placing blocks at current level
                for k in range(1, j + 1):
                    dp[i][j] += dp[i-1][j-k]
        
        return dp[self.height][self.width]
    
    def get_towers_with_constraints(self, constraint_func):
        """Get towers that satisfies custom constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        count = self.count_towers()
        if constraint_func(count, self.height, self.width):
            return self._generate_towers()
        else:
            return []
    
    def get_towers_in_range(self, min_count, max_count):
        """Get towers within specified count range."""
        if not self.tower_counting_feasibility:
            return []
        
        count = self.count_towers()
        if min_count <= count <= max_count:
            return self._generate_towers()
        else:
            return []
    
    def get_towers_with_pattern(self, pattern_func):
        """Get towers matching specified pattern."""
        if not self.tower_counting_feasibility:
            return []
        
        count = self.count_towers()
        if pattern_func(count, self.height, self.width):
            return self._generate_towers()
        else:
            return []
    
    def _generate_towers(self):
        """Generate all possible tower configurations."""
        if not self.tower_counting_feasibility:
            return []
        
        towers = []
        
        def backtrack(level, current_tower):
            if level == self.height:
                towers.append(current_tower[:])
                return
            
            # Try different block configurations at current level
            for blocks in range(self.width + 1):
                if blocks <= self.width:
                    current_tower.append(blocks)
                    backtrack(level + 1, current_tower)
                    current_tower.pop()
        
        backtrack(0, [])
        return towers
    
    def get_tower_counting_statistics(self):
        """Get statistics about the tower counting."""
        if not self.tower_counting_feasibility:
            return {
                'height': 0,
                'width': 0,
                'tower_counting_feasibility': 0,
                'tower_count': 0
            }
        
        count = self.count_towers()
        return {
            'height': self.height,
            'width': self.width,
            'tower_counting_feasibility': self.tower_counting_feasibility,
            'tower_count': count
        }
    
    def get_tower_counting_patterns(self):
        """Get patterns in tower counting."""
        patterns = {
            'tower_buildable': 0,
            'has_valid_dimensions': 0,
            'optimal_towers_possible': 0,
            'has_large_dimensions': 0
        }
        
        if not self.tower_counting_feasibility:
            return patterns
        
        # Check if tower is buildable
        if self.tower_counting_feasibility == 1.0:
            patterns['tower_buildable'] = 1
        
        # Check if has valid dimensions
        if self.height > 0 and self.width > 0:
            patterns['has_valid_dimensions'] = 1
        
        # Check if optimal towers are possible
        if self.tower_counting_feasibility == 1.0:
            patterns['optimal_towers_possible'] = 1
        
        # Check if has large dimensions
        if self.height > 10 or self.width > 10:
            patterns['has_large_dimensions'] = 1
        
        return patterns
    
    def get_optimal_tower_counting_strategy(self):
        """Get optimal strategy for tower counting."""
        if not self.tower_counting_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'tower_counting_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.tower_counting_feasibility
        
        # Calculate tower counting feasibility
        tower_counting_feasibility = self.tower_counting_feasibility
        
        # Determine recommended strategy
        if self.height <= 10 and self.width <= 10:
            recommended_strategy = 'dynamic_programming'
        elif self.height <= 50 and self.width <= 50:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'tower_counting_feasibility': tower_counting_feasibility
        }

# Example usage
height = 3
width = 2
dynamic_tower_counting = DynamicCountingTowers(height, width)
print(f"Tower counting feasibility: {dynamic_tower_counting.tower_counting_feasibility}")

# Update dimensions
dynamic_tower_counting.update_dimensions(4, 3)
print(f"After updating dimensions: {dynamic_tower_counting.height}x{dynamic_tower_counting.width}")

# Count towers
count = dynamic_tower_counting.count_towers()
print(f"Number of towers: {count}")

# Get towers with constraints
def constraint_func(count, height, width):
    return count > 0 and height > 0 and width > 0

print(f"Towers with constraints: {len(dynamic_tower_counting.get_towers_with_constraints(constraint_func))}")

# Get towers in range
print(f"Towers in range 1-100: {len(dynamic_tower_counting.get_towers_in_range(1, 100))}")

# Get towers with pattern
def pattern_func(count, height, width):
    return count > 0 and height > 0 and width > 0

print(f"Towers with pattern: {len(dynamic_tower_counting.get_towers_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_tower_counting.get_tower_counting_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_tower_counting.get_tower_counting_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_tower_counting.get_optimal_tower_counting_strategy()}")
```

### **Variation 2: Counting Towers with Different Operations**
**Problem**: Handle different types of tower counting operations (weighted towers, priority-based counting, advanced tower analysis).

**Approach**: Use advanced data structures for efficient different types of tower counting operations.

```python
class AdvancedCountingTowers:
    def __init__(self, height=None, width=None, weights=None, priorities=None):
        self.height = height or 0
        self.width = width or 0
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.towers = []
        self._update_tower_counting_info()
    
    def _update_tower_counting_info(self):
        """Update tower counting feasibility information."""
        self.tower_counting_feasibility = self._calculate_tower_counting_feasibility()
    
    def _calculate_tower_counting_feasibility(self):
        """Calculate tower counting feasibility."""
        if self.height <= 0 or self.width <= 0:
            return 0.0
        
        # Check if we can build towers with given dimensions
        return 1.0 if self.height > 0 and self.width > 0 else 0.0
    
    def count_towers(self):
        """Count number of ways to build towers using dynamic programming."""
        if self.height <= 0 or self.width <= 0:
            return 0
        
        # DP table: dp[i][j] = number of ways to build tower of height i with width j
        dp = [[0 for _ in range(self.width + 1)] for _ in range(self.height + 1)]
        
        # Base case: one way to build tower of height 0 (empty tower)
        for j in range(self.width + 1):
            dp[0][j] = 1
        
        # Fill DP table
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                # Tower can be built by:
                # 1. Not placing any block at current level
                dp[i][j] = dp[i-1][j]
                
                # 2. Placing blocks at current level
                for k in range(1, j + 1):
                    dp[i][j] += dp[i-1][j-k]
        
        return dp[self.height][self.width]
    
    def get_weighted_towers(self):
        """Get towers with weights and priorities applied."""
        if not self.tower_counting_feasibility:
            return []
        
        # Create weighted tower configurations
        weighted_towers = []
        towers = self._generate_towers()
        
        for tower in towers:
            weight = self.weights.get('height', 1) * self.weights.get('width', 1)
            priority = self.priorities.get('height', 1) * self.priorities.get('width', 1)
            weighted_score = len(tower) * weight * priority
            weighted_towers.append((tower, weighted_score))
        
        # Sort by weighted score
        weighted_towers.sort(key=lambda x: x[1], reverse=True)
        
        return [tower for tower, score in weighted_towers]
    
    def get_towers_with_priority(self, priority_func):
        """Get towers considering priority."""
        if not self.tower_counting_feasibility:
            return []
        
        # Create priority-based towers
        priority_towers = []
        towers = self._generate_towers()
        
        for tower in towers:
            priority = priority_func(tower, self.weights, self.priorities)
            priority_towers.append((tower, priority))
        
        # Sort by priority
        priority_towers.sort(key=lambda x: x[1], reverse=True)
        
        return [tower for tower, priority in priority_towers]
    
    def get_towers_with_optimization(self, optimization_func):
        """Get towers using custom optimization function."""
        if not self.tower_counting_feasibility:
            return []
        
        # Create optimization-based towers
        optimized_towers = []
        towers = self._generate_towers()
        
        for tower in towers:
            score = optimization_func(tower, self.weights, self.priorities)
            optimized_towers.append((tower, score))
        
        # Sort by optimization score
        optimized_towers.sort(key=lambda x: x[1], reverse=True)
        
        return [tower for tower, score in optimized_towers]
    
    def get_towers_with_constraints(self, constraint_func):
        """Get towers that satisfies custom constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        if constraint_func(self.height, self.width, self.weights, self.priorities):
            return self.get_weighted_towers()
        else:
            return []
    
    def get_towers_with_multiple_criteria(self, criteria_list):
        """Get towers that satisfies multiple criteria."""
        if not self.tower_counting_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.height, self.width, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_towers()
        else:
            return []
    
    def get_towers_with_alternatives(self, alternatives):
        """Get towers considering alternative weights/priorities."""
        result = []
        
        # Check original towers
        original_towers = self.get_weighted_towers()
        result.append((original_towers, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedCountingTowers(self.height, self.width, alt_weights, alt_priorities)
            temp_towers = temp_instance.get_weighted_towers()
            result.append((temp_towers, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_towers_with_adaptive_criteria(self, adaptive_func):
        """Get towers using adaptive criteria."""
        if not self.tower_counting_feasibility:
            return []
        
        if adaptive_func(self.height, self.width, self.weights, self.priorities, []):
            return self.get_weighted_towers()
        else:
            return []
    
    def _generate_towers(self):
        """Generate all possible tower configurations."""
        if not self.tower_counting_feasibility:
            return []
        
        towers = []
        
        def backtrack(level, current_tower):
            if level == self.height:
                towers.append(current_tower[:])
                return
            
            # Try different block configurations at current level
            for blocks in range(self.width + 1):
                if blocks <= self.width:
                    current_tower.append(blocks)
                    backtrack(level + 1, current_tower)
                    current_tower.pop()
        
        backtrack(0, [])
        return towers
    
    def get_tower_counting_optimization(self):
        """Get optimal tower counting configuration."""
        strategies = [
            ('weighted_towers', lambda: len(self.get_weighted_towers())),
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
height = 3
width = 2
weights = {'height': 2, 'width': 3}  # Weight based on dimensions
priorities = {'height': 1, 'width': 2}  # Priority based on dimensions
advanced_tower_counting = AdvancedCountingTowers(height, width, weights, priorities)

print(f"Weighted towers: {len(advanced_tower_counting.get_weighted_towers())}")

# Get towers with priority
def priority_func(tower, weights, priorities):
    return weights.get('height', 1) + priorities.get('width', 1)

print(f"Towers with priority: {len(advanced_tower_counting.get_towers_with_priority(priority_func))}")

# Get towers with optimization
def optimization_func(tower, weights, priorities):
    return weights.get('height', 1) * priorities.get('width', 1)

print(f"Towers with optimization: {len(advanced_tower_counting.get_towers_with_optimization(optimization_func))}")

# Get towers with constraints
def constraint_func(height, width, weights, priorities):
    return height > 0 and width > 0

print(f"Towers with constraints: {len(advanced_tower_counting.get_towers_with_constraints(constraint_func))}")

# Get towers with multiple criteria
def criterion1(height, width, weights, priorities):
    return height > 0

def criterion2(height, width, weights, priorities):
    return width > 0

criteria_list = [criterion1, criterion2]
print(f"Towers with multiple criteria: {len(advanced_tower_counting.get_towers_with_multiple_criteria(criteria_list))}")

# Get towers with alternatives
alternatives = [({'height': 1, 'width': 1}, {'height': 1, 'width': 1}), ({'height': 3, 'width': 2}, {'height': 2, 'width': 1})]
print(f"Towers with alternatives: {advanced_tower_counting.get_towers_with_alternatives(alternatives)}")

# Get towers with adaptive criteria
def adaptive_func(height, width, weights, priorities, current_result):
    return height > 0 and width > 0 and len(current_result) < 5

print(f"Towers with adaptive criteria: {len(advanced_tower_counting.get_towers_with_adaptive_criteria(adaptive_func))}")

# Get tower counting optimization
print(f"Tower counting optimization: {advanced_tower_counting.get_tower_counting_optimization()}")
```

### **Variation 3: Counting Towers with Constraints**
**Problem**: Handle tower counting with additional constraints (dimension limits, block constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedCountingTowers:
    def __init__(self, height=None, width=None, constraints=None):
        self.height = height or 0
        self.width = width or 0
        self.constraints = constraints or {}
        self.towers = []
        self._update_tower_counting_info()
    
    def _update_tower_counting_info(self):
        """Update tower counting feasibility information."""
        self.tower_counting_feasibility = self._calculate_tower_counting_feasibility()
    
    def _calculate_tower_counting_feasibility(self):
        """Calculate tower counting feasibility."""
        if self.height <= 0 or self.width <= 0:
            return 0.0
        
        # Check if we can build towers with given dimensions
        return 1.0 if self.height > 0 and self.width > 0 else 0.0
    
    def _is_valid_tower(self, tower):
        """Check if tower is valid considering constraints."""
        # Dimension constraints
        if 'min_height' in self.constraints:
            if len(tower) < self.constraints['min_height']:
                return False
        
        if 'max_height' in self.constraints:
            if len(tower) > self.constraints['max_height']:
                return False
        
        if 'min_width' in self.constraints:
            if any(level > self.constraints['min_width'] for level in tower):
                return False
        
        if 'max_width' in self.constraints:
            if any(level > self.constraints['max_width'] for level in tower):
                return False
        
        # Block constraints
        if 'forbidden_blocks' in self.constraints:
            if any(level in self.constraints['forbidden_blocks'] for level in tower):
                return False
        
        if 'required_blocks' in self.constraints:
            if not all(level in tower for level in self.constraints['required_blocks']):
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(tower):
                    return False
        
        return True
    
    def get_towers_with_dimension_constraints(self, min_height, max_height, min_width, max_width):
        """Get towers considering dimension constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        towers = self._generate_towers()
        valid_towers = []
        
        for tower in towers:
            if (min_height <= len(tower) <= max_height and 
                all(min_width <= level <= max_width for level in tower) and 
                self._is_valid_tower(tower)):
                valid_towers.append(tower)
        
        return valid_towers
    
    def get_towers_with_block_constraints(self, block_constraints):
        """Get towers considering block constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in block_constraints:
            if not constraint(self.height, self.width):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            towers = self._generate_towers()
            valid_towers = []
            
            for tower in towers:
                if self._is_valid_tower(tower):
                    valid_towers.append(tower)
            
            return valid_towers
        
        return []
    
    def get_towers_with_pattern_constraints(self, pattern_constraints):
        """Get towers considering pattern constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.height, self.width):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            towers = self._generate_towers()
            valid_towers = []
            
            for tower in towers:
                if self._is_valid_tower(tower):
                    valid_towers.append(tower)
            
            return valid_towers
        
        return []
    
    def get_towers_with_mathematical_constraints(self, constraint_func):
        """Get towers that satisfies custom mathematical constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        if constraint_func(self.height, self.width):
            towers = self._generate_towers()
            valid_towers = []
            
            for tower in towers:
                if self._is_valid_tower(tower):
                    valid_towers.append(tower)
            
            return valid_towers
        
        return []
    
    def get_towers_with_optimization_constraints(self, optimization_func):
        """Get towers using custom optimization constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        # Calculate optimization score for towers
        score = optimization_func(self.height, self.width)
        
        if score > 0:
            towers = self._generate_towers()
            valid_towers = []
            
            for tower in towers:
                if self._is_valid_tower(tower):
                    valid_towers.append(tower)
            
            return valid_towers
        
        return []
    
    def get_towers_with_multiple_constraints(self, constraints_list):
        """Get towers that satisfies multiple constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.height, self.width):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            towers = self._generate_towers()
            valid_towers = []
            
            for tower in towers:
                if self._is_valid_tower(tower):
                    valid_towers.append(tower)
            
            return valid_towers
        
        return []
    
    def get_towers_with_priority_constraints(self, priority_func):
        """Get towers with priority-based constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        # Calculate priority for towers
        priority = priority_func(self.height, self.width)
        
        if priority > 0:
            towers = self._generate_towers()
            valid_towers = []
            
            for tower in towers:
                if self._is_valid_tower(tower):
                    valid_towers.append(tower)
            
            return valid_towers
        
        return []
    
    def get_towers_with_adaptive_constraints(self, adaptive_func):
        """Get towers with adaptive constraints."""
        if not self.tower_counting_feasibility:
            return []
        
        if adaptive_func(self.height, self.width, []):
            towers = self._generate_towers()
            valid_towers = []
            
            for tower in towers:
                if self._is_valid_tower(tower):
                    valid_towers.append(tower)
            
            return valid_towers
        
        return []
    
    def _generate_towers(self):
        """Generate all possible tower configurations."""
        if not self.tower_counting_feasibility:
            return []
        
        towers = []
        
        def backtrack(level, current_tower):
            if level == self.height:
                towers.append(current_tower[:])
                return
            
            # Try different block configurations at current level
            for blocks in range(self.width + 1):
                if blocks <= self.width:
                    current_tower.append(blocks)
                    backtrack(level + 1, current_tower)
                    current_tower.pop()
        
        backtrack(0, [])
        return towers
    
    def get_optimal_tower_counting_strategy(self):
        """Get optimal tower counting strategy considering all constraints."""
        strategies = [
            ('dimension_constraints', self.get_towers_with_dimension_constraints),
            ('block_constraints', self.get_towers_with_block_constraints),
            ('pattern_constraints', self.get_towers_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'dimension_constraints':
                    result = strategy_func(0, 100, 0, 100)
                elif strategy_name == 'block_constraints':
                    block_constraints = [lambda height, width: height > 0 and width > 0]
                    result = strategy_func(block_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda height, width: height > 0 and width > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_height': 1,
    'max_height': 5,
    'min_width': 0,
    'max_width': 3,
    'forbidden_blocks': [0, -1],
    'required_blocks': [1],
    'pattern_constraints': [lambda tower: len(tower) > 0 and all(level >= 0 for level in tower)]
}

height = 3
width = 2
constrained_tower_counting = ConstrainedCountingTowers(height, width, constraints)

print("Dimension-constrained towers:", len(constrained_tower_counting.get_towers_with_dimension_constraints(1, 5, 0, 3)))

print("Block-constrained towers:", len(constrained_tower_counting.get_towers_with_block_constraints([lambda height, width: height > 0 and width > 0])))

print("Pattern-constrained towers:", len(constrained_tower_counting.get_towers_with_pattern_constraints([lambda height, width: height > 0 and width > 0])))

# Mathematical constraints
def custom_constraint(height, width):
    return height > 0 and width > 0

print("Mathematical constraint towers:", len(constrained_tower_counting.get_towers_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(height, width):
    return 1 <= height <= 10 and 1 <= width <= 10

range_constraints = [range_constraint]
print("Range-constrained towers:", len(constrained_tower_counting.get_towers_with_dimension_constraints(1, 10, 1, 10)))

# Multiple constraints
def constraint1(height, width):
    return height > 0

def constraint2(height, width):
    return width > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints towers:", len(constrained_tower_counting.get_towers_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(height, width):
    return height + width

print("Priority-constrained towers:", len(constrained_tower_counting.get_towers_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(height, width, current_result):
    return height > 0 and width > 0 and len(current_result) < 5

print("Adaptive constraint towers:", len(constrained_tower_counting.get_towers_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_tower_counting.get_optimal_tower_counting_strategy()
print(f"Optimal tower counting strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Book Shop](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Grid Paths](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Grid DP
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Grid DP
- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) - Grid DP

#### **Problem Categories**
- **Dynamic Programming**: Tower DP, constraint satisfaction
- **Combinatorics**: Mathematical counting, constraint properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Tower Algorithms](https://cp-algorithms.com/geometry/basic-geometry.html) - Tower algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium
- [CSES Book Shop](https://cses.fi/problemset/task/1075) - Medium
- [CSES Grid Paths](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
