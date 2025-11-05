---
layout: simple
title: "Towers"
permalink: /problem_soulutions/sorting_and_searching/towers_analysis
---

# Towers

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the longest increasing subsequence (LIS) problem
- Apply greedy algorithms with binary search for LIS
- Implement efficient dynamic programming solutions
- Optimize LIS algorithms for large inputs
- Handle edge cases in sequence problems (empty sequences, single elements)

## 📋 Problem Description

Given n cubes with different sizes, you want to build towers by stacking cubes. Each cube can only be placed on top of a cube that is strictly larger than it. Find the minimum number of towers needed.

This is equivalent to finding the minimum number of decreasing subsequences that cover all elements, which is the same as finding the length of the longest increasing subsequence.

**Input**: 
- First line: integer n (number of cubes)
- Second line: n integers a₁, a₂, ..., aₙ (sizes of cubes)

**Output**: 
- Print one integer: the minimum number of towers needed

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ aᵢ ≤ 10⁹

**Example**:
```
Input:
5
3 8 2 1 5

Output:
3

Explanation**: 
We can build 3 towers:
- Tower 1: 8, 3, 2, 1 (decreasing order)
- Tower 2: 5
- Tower 3: (empty)

Or equivalently, the longest increasing subsequence is [2, 5, 8] with length 3.
Minimum towers needed: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Arrangements

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible ways to arrange cubes into towers
- **Greedy Placement**: For each arrangement, place cubes greedily on existing towers
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward greedy placement

**Key Insight**: For each possible order of cubes, try to place them greedily on existing towers or create new towers.

**Algorithm**:
- Generate all possible permutations of cubes
- For each permutation, place cubes greedily on towers
- Keep track of the minimum number of towers needed

**Visual Example**:
```
Cubes: [3, 8, 2, 1, 5]

Permutation 1: [3, 8, 2, 1, 5]
- Place 3: Tower 1 [3]
- Place 8: Tower 1 [8, 3] (8 > 3)
- Place 2: Tower 2 [2] (2 < 3)
- Place 1: Tower 2 [2, 1] (1 < 2)
- Place 5: Tower 3 [5] (5 > 1 but < 2)
Towers needed: 3

Permutation 2: [1, 2, 3, 5, 8]
- Place 1: Tower 1 [1]
- Place 2: Tower 1 [2, 1] (2 > 1)
- Place 3: Tower 1 [3, 2, 1] (3 > 2)
- Place 5: Tower 1 [5, 3, 2, 1] (5 > 3)
- Place 8: Tower 1 [8, 5, 3, 2, 1] (8 > 5)
Towers needed: 1

Minimum: 1 tower
```

**Implementation**:
```python
def brute_force_towers(cubes):
    """
    Find minimum towers using brute force approach
    
    Args:
        cubes: list of cube sizes
    
    Returns:
        int: minimum number of towers needed
    """
    from itertools import permutations
    
    min_towers = float('inf')
    
    # Try all possible arrangements
    for perm in permutations(cubes):
        towers = []
        
        for cube in perm:
            # Find the leftmost tower where cube can be placed
            placed = False
            for i, tower in enumerate(towers):
                if cube < tower[-1]:  # Can be placed on this tower
                    towers[i].append(cube)
                    placed = True
                    break
            
            # If can't be placed on any existing tower, create new one
            if not placed:
                towers.append([cube])
        
        min_towers = min(min_towers, len(towers))
    
    return min_towers

# Example usage
cubes = [3, 8, 2, 1, 5]
result = brute_force_towers(cubes)
print(f"Brute force result: {result}")  # Output: 1
```

**Time Complexity**: O(n! × n²) - All permutations with greedy placement
**Space Complexity**: O(n) - For storing towers

**Why it's inefficient**: Factorial time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Dynamic Programming

**Key Insights from Optimized Approach**:
- **LIS Problem**: This is equivalent to finding the longest increasing subsequence
- **DP State**: dp[i] = length of LIS ending at position i
- **Optimal Substructure**: LIS ending at i depends on LIS ending at previous positions
- **Efficient Calculation**: Use DP to avoid recalculating subproblems

**Key Insight**: The minimum number of towers equals the length of the longest increasing subsequence.

**Algorithm**:
- For each position i, find the longest increasing subsequence ending at i
- Use dynamic programming to calculate dp[i] efficiently
- Return the maximum value in dp array

**Visual Example**:
```
Cubes: [3, 8, 2, 1, 5]

DP calculation:
dp[0] = 1 (LIS ending at 3: [3])
dp[1] = 2 (LIS ending at 8: [3, 8])
dp[2] = 1 (LIS ending at 2: [2])
dp[3] = 1 (LIS ending at 1: [1])
dp[4] = 2 (LIS ending at 5: [2, 5] or [1, 5])

Maximum LIS length: 2
Minimum towers: 2
```

**Implementation**:
```python
def optimized_towers(cubes):
    """
    Find minimum towers using dynamic programming (LIS)
    
    Args:
        cubes: list of cube sizes
    
    Returns:
        int: minimum number of towers needed
    """
    n = len(cubes)
    dp = [1] * n  # dp[i] = length of LIS ending at position i
    
    for i in range(1, n):
        for j in range(i):
            if cubes[j] < cubes[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Example usage
cubes = [3, 8, 2, 1, 5]
result = optimized_towers(cubes)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - Nested loops for DP calculation
**Space Complexity**: O(n) - For DP array

**Why it's better**: Much more efficient than brute force, but still quadratic.

---

### Approach 3: Optimal - Binary Search with Greedy

**Key Insights from Optimal Approach**:
- **Binary Search on LIS**: Use binary search to find the optimal position
- **Greedy Maintenance**: Maintain the smallest tail element for each LIS length
- **Efficient Updates**: Update tails array in O(log n) time
- **Linear Processing**: Process each element in O(log n) time

**Key Insight**: Maintain an array where tails[i] is the smallest tail element of all increasing subsequences of length i+1.

**Algorithm**:
- Maintain a tails array where tails[i] = smallest tail of LIS of length i+1
- For each element, use binary search to find the correct position
- Update tails array efficiently

**Visual Example**:
```
Cubes: [3, 8, 2, 1, 5]

Processing:
1. 3: tails = [3]
2. 8: tails = [3, 8] (8 > 3, extend)
3. 2: tails = [2, 8] (2 < 3, replace)
4. 1: tails = [1, 8] (1 < 2, replace)
5. 5: tails = [1, 5] (5 < 8, replace)

Final tails: [1, 5]
LIS length: 2
Minimum towers: 2
```

**Implementation**:
```python
def optimal_towers(cubes):
    """
    Find minimum towers using binary search with greedy (optimal LIS)
    
    Args:
        cubes: list of cube sizes
    
    Returns:
        int: minimum number of towers needed
    """
    import bisect
    
    tails = []
    
    for cube in cubes:
        # Find the position where cube should be placed
        pos = bisect.bisect_left(tails, cube)
        
        if pos == len(tails):
            # Extend the sequence
            tails.append(cube)
        else:
            # Replace the element at position pos
            tails[pos] = cube
    
    return len(tails)

# Example usage
cubes = [3, 8, 2, 1, 5]
result = optimal_towers(cubes)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Binary search for each element
**Space Complexity**: O(n) - For tails array

**Why it's optimal**: Achieves the best possible time complexity for the LIS problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × n²) | O(n) | Try all permutations |
| Dynamic Programming | O(n²) | O(n) | LIS with DP |
| Binary Search + Greedy | O(n log n) | O(n) | Optimal LIS algorithm |

### Time Complexity
- **Time**: O(n log n) - Binary search for each element in optimal approach
- **Space**: O(n) - For tails array in optimal approach

### Why This Solution Works
- **Dilworth's Theorem**: The minimum number of chains equals the maximum antichain size
- **LIS Equivalence**: Minimum towers = length of longest increasing subsequence
- **Greedy Choice**: Always maintain the smallest possible tail for each LIS length
- **Optimal Approach**: Binary search with greedy maintenance provides the best theoretical performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Towers with Different Capacities
**Problem**: Each tower has a different capacity, and we want to minimize the number of towers used.

**Link**: [CSES Problem Set - Towers with Different Capacities](https://cses.fi/problemset/task/towers_different_capacities)

```python
def towers_different_capacities(blocks, tower_capacities):
    """
    Handle towers with different capacities
    """
    # Sort blocks in descending order
    blocks.sort(reverse=True)
    
    # Sort tower capacities in descending order
    tower_capacities.sort(reverse=True)
    
    # Use greedy approach: assign each block to the smallest tower that can hold it
    tower_heights = [0] * len(tower_capacities)
    used_towers = 0
    
    for block in blocks:
        # Find the smallest tower that can hold this block
        best_tower = -1
        for i in range(len(tower_capacities)):
            if tower_heights[i] + 1 <= tower_capacities[i]:
                if best_tower == -1 or tower_heights[i] < tower_heights[best_tower]:
                    best_tower = i
        
        if best_tower != -1:
            tower_heights[best_tower] += 1
            if tower_heights[best_tower] == 1:
                used_towers += 1
    
    return used_towers
```

### Variation 2: Towers with Weight Constraints
**Problem**: Each block has a weight, and towers have weight limits.

**Link**: [CSES Problem Set - Towers with Weight Constraints](https://cses.fi/problemset/task/towers_weight_constraints)

```python
def towers_weight_constraints(blocks, tower_weight_limits):
    """
    Handle towers with weight constraints
    """
    # Sort blocks by weight (descending)
    blocks.sort(key=lambda x: x['weight'], reverse=True)
    
    # Sort tower weight limits (descending)
    tower_weight_limits.sort(reverse=True)
    
    # Track current weight in each tower
    tower_weights = [0] * len(tower_weight_limits)
    used_towers = 0
    
    for block in blocks:
        # Find the smallest tower that can hold this block
        best_tower = -1
        for i in range(len(tower_weight_limits)):
            if tower_weights[i] + block['weight'] <= tower_weight_limits[i]:
                if best_tower == -1 or tower_weights[i] < tower_weights[best_tower]:
                    best_tower = i
        
        if best_tower != -1:
            tower_weights[best_tower] += block['weight']
            if tower_weights[best_tower] == block['weight']:
                used_towers += 1
    
    return used_towers
```

### Variation 3: Towers with Dynamic Updates
**Problem**: Blocks can be added or removed dynamically, and we need to maintain optimal tower arrangement.

**Link**: [CSES Problem Set - Towers with Dynamic Updates](https://cses.fi/problemset/task/towers_dynamic_updates)

```python
class TowersDynamic:
    def __init__(self):
        self.blocks = []
        self.towers = []
        self.min_towers = 0
    
    def add_block(self, block):
        """Add a new block"""
        self.blocks.append(block)
        self._update_towers()
    
    def remove_block(self, block):
        """Remove a block"""
        if block in self.blocks:
            self.blocks.remove(block)
            self._update_towers()
    
    def _update_towers(self):
        """Update the optimal tower arrangement"""
        # Sort blocks in descending order
        sorted_blocks = sorted(self.blocks, reverse=True)
        
        # Use greedy approach to find minimum towers
        self.towers = []
        
        for block in sorted_blocks:
            # Find the smallest tower that can hold this block
            best_tower = -1
            for i in range(len(self.towers)):
                if self.towers[i][-1] >= block:
                    if best_tower == -1 or len(self.towers[i]) < len(self.towers[best_tower]):
                        best_tower = i
            
            if best_tower != -1:
                self.towers[best_tower].append(block)
            else:
                # Create new tower
                self.towers.append([block])
        
        self.min_towers = len(self.towers)
    
    def get_min_towers(self):
        """Get current minimum number of towers"""
        return self.min_towers
    
    def get_towers(self):
        """Get current tower arrangement"""
        return self.towers
```

## Problem Variations

### **Variation 1: Towers with Dynamic Updates**
**Problem**: Handle dynamic block updates (add/remove/update blocks) while maintaining optimal tower arrangement.

**Approach**: Use efficient data structures and algorithms for dynamic tower management.

```python
from collections import defaultdict
import bisect

class DynamicTowers:
    def __init__(self, blocks):
        self.blocks = blocks[:]
        self.towers = []
        self.min_towers = 0
        self._update_towers()
    
    def _update_towers(self):
        """Update the optimal tower arrangement using greedy algorithm."""
        # Sort blocks in descending order
        sorted_blocks = sorted(self.blocks, reverse=True)
        
        # Use greedy approach to find minimum towers
        self.towers = []
        
        for block in sorted_blocks:
            # Find the smallest tower that can hold this block
            best_tower = -1
            for i in range(len(self.towers)):
                if self.towers[i][-1] >= block:
                    if best_tower == -1 or len(self.towers[i]) < len(self.towers[best_tower]):
                        best_tower = i
            
            if best_tower != -1:
                self.towers[best_tower].append(block)
            else:
                # Create new tower
                self.towers.append([block])
        
        self.min_towers = len(self.towers)
    
    def add_block(self, block):
        """Add a new block to the system."""
        self.blocks.append(block)
        self._update_towers()
    
    def remove_block(self, block):
        """Remove a block from the system."""
        if block in self.blocks:
            self.blocks.remove(block)
            self._update_towers()
    
    def update_block(self, old_block, new_block):
        """Update a block with new value."""
        if old_block in self.blocks:
            self.blocks.remove(old_block)
            self.blocks.append(new_block)
            self._update_towers()
    
    def get_min_towers(self):
        """Get current minimum number of towers."""
        return self.min_towers
    
    def get_towers(self):
        """Get current tower arrangement."""
        return self.towers
    
    def get_blocks(self):
        """Get current blocks."""
        return self.blocks
    
    def get_towers_with_constraints(self, constraint_func):
        """Get towers that satisfy custom constraints."""
        result = []
        for tower in self.towers:
            if constraint_func(tower):
                result.append(tower)
        return result
    
    def get_towers_in_range(self, min_height, max_height):
        """Get towers with height in specified range."""
        result = []
        for tower in self.towers:
            tower_height = len(tower)
            if min_height <= tower_height <= max_height:
                result.append(tower)
        return result
    
    def get_towers_with_capacity(self, capacity_func):
        """Get towers based on capacity function."""
        result = []
        for tower in self.towers:
            capacity = capacity_func(tower)
            result.append((tower, capacity))
        return result
    
    def get_tower_statistics(self):
        """Get statistics about towers."""
        if not self.towers:
            return {
                'total_towers': 0,
                'total_blocks': 0,
                'average_tower_height': 0,
                'max_tower_height': 0,
                'min_tower_height': 0
            }
        
        total_towers = len(self.towers)
        total_blocks = len(self.blocks)
        tower_heights = [len(tower) for tower in self.towers]
        average_tower_height = sum(tower_heights) / total_towers
        max_tower_height = max(tower_heights)
        min_tower_height = min(tower_heights)
        
        return {
            'total_towers': total_towers,
            'total_blocks': len(self.blocks),
            'average_tower_height': average_tower_height,
            'max_tower_height': max_tower_height,
            'min_tower_height': min_tower_height
        }
    
    def get_tower_patterns(self):
        """Get patterns in tower arrangement."""
        patterns = {
            'tall_towers': 0,
            'short_towers': 0,
            'balanced_towers': 0,
            'efficient_towers': 0
        }
        
        if not self.towers:
            return patterns
        
        tower_heights = [len(tower) for tower in self.towers]
        avg_height = sum(tower_heights) / len(tower_heights)
        
        for height in tower_heights:
            if height > avg_height * 1.2:
                patterns['tall_towers'] += 1
            elif height < avg_height * 0.8:
                patterns['short_towers'] += 1
            else:
                patterns['balanced_towers'] += 1
            
            if height >= 3:  # Efficient if height >= 3
                patterns['efficient_towers'] += 1
        
        return patterns
    
    def get_optimal_tower_strategy(self):
        """Get optimal tower arrangement strategy."""
        if not self.blocks:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'utilization_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible_towers = len(self.blocks)  # Worst case: one block per tower
        efficiency_rate = (total_possible_towers - self.min_towers) / total_possible_towers if total_possible_towers > 0 else 0
        
        # Calculate utilization rate
        total_blocks = len(self.blocks)
        total_tower_capacity = sum(len(tower) for tower in self.towers)
        utilization_rate = total_blocks / total_tower_capacity if total_tower_capacity > 0 else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.5:
            recommended_strategy = 'greedy_optimal'
        elif utilization_rate > 0.8:
            recommended_strategy = 'balanced_arrangement'
        else:
            recommended_strategy = 'minimal_towers'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'utilization_rate': utilization_rate
        }

# Example usage
blocks = [3, 2, 4, 1, 5]
dynamic_towers = DynamicTowers(blocks)
print(f"Initial min towers: {dynamic_towers.get_min_towers()}")

# Add a new block
dynamic_towers.add_block(6)
print(f"After adding block: {dynamic_towers.get_min_towers()}")

# Update a block
dynamic_towers.update_block(1, 7)
print(f"After updating block: {dynamic_towers.get_min_towers()}")

# Remove a block
dynamic_towers.remove_block(2)
print(f"After removing block: {dynamic_towers.get_min_towers()}")

# Get towers with constraints
def constraint_func(tower):
    return len(tower) >= 2

print(f"Towers with constraints: {dynamic_towers.get_towers_with_constraints(constraint_func)}")

# Get towers in range
print(f"Towers in range [1, 3]: {dynamic_towers.get_towers_in_range(1, 3)}")

# Get towers with capacity
def capacity_func(tower):
    return sum(tower)

print(f"Towers with capacity: {dynamic_towers.get_towers_with_capacity(capacity_func)}")

# Get statistics
print(f"Statistics: {dynamic_towers.get_tower_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_towers.get_tower_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_towers.get_optimal_tower_strategy()}")
```

### **Variation 2: Towers with Different Operations**
**Problem**: Handle different types of operations on tower arrangement (weighted blocks, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of tower arrangement queries.

```python
class AdvancedTowers:
    def __init__(self, blocks, weights=None, priorities=None):
        self.blocks = blocks[:]
        self.weights = weights or [1] * len(blocks)
        self.priorities = priorities or [1] * len(blocks)
        self.towers = []
        self.min_towers = 0
        self._update_towers()
    
    def _update_towers(self):
        """Update the optimal tower arrangement using advanced algorithms."""
        # Create indexed blocks with weights and priorities
        indexed_blocks = [(self.blocks[i], i, self.weights[i], self.priorities[i]) 
                         for i in range(len(self.blocks))]
        
        # Sort by weighted priority
        indexed_blocks.sort(key=lambda x: (x[0] * x[2] * x[3]), reverse=True)
        
        # Use greedy approach to find minimum towers
        self.towers = []
        
        for block, idx, weight, priority in indexed_blocks:
            # Find the best tower for this block
            best_tower = -1
            best_score = float('inf')
            
            for i in range(len(self.towers)):
                if self.towers[i][-1][0] >= block:  # Can hold this block
                    # Calculate score based on weight and priority
                    tower_score = len(self.towers[i]) * weight * priority
                    if tower_score < best_score:
                        best_score = tower_score
                        best_tower = i
            
            if best_tower != -1:
                self.towers[best_tower].append((block, idx, weight, priority))
            else:
                # Create new tower
                self.towers.append([(block, idx, weight, priority)])
        
        self.min_towers = len(self.towers)
    
    def get_towers(self):
        """Get current towers."""
        return self.towers
    
    def get_weighted_towers(self):
        """Get towers with weights applied."""
        result = []
        for tower in self.towers:
            weighted_tower = []
            for block, idx, weight, priority in tower:
                weighted_tower.append({
                    'block': block,
                    'index': idx,
                    'weight': weight,
                    'priority': priority,
                    'weighted_value': block * weight * priority
                })
            result.append(weighted_tower)
        return result
    
    def get_towers_with_priority(self, priority_func):
        """Get towers considering priority."""
        result = []
        for tower in self.towers:
            priority = priority_func(tower)
            result.append((tower, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_towers_with_optimization(self, optimization_func):
        """Get towers using custom optimization function."""
        result = []
        for tower in self.towers:
            score = optimization_func(tower)
            result.append((tower, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_towers_with_constraints(self, constraint_func):
        """Get towers that satisfy custom constraints."""
        result = []
        for tower in self.towers:
            if constraint_func(tower):
                result.append(tower)
        return result
    
    def get_towers_with_multiple_criteria(self, criteria_list):
        """Get towers that satisfy multiple criteria."""
        result = []
        for tower in self.towers:
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(tower):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(tower)
        return result
    
    def get_towers_with_alternatives(self, alternatives):
        """Get towers considering alternative block arrangements."""
        result = []
        
        # Check original towers
        for tower in self.towers:
            result.append((tower, 'original'))
        
        # Check alternative arrangements
        for alt_blocks in alternatives:
            # Create temporary towers with alternative blocks
            temp_towers = self._create_towers_with_blocks(alt_blocks)
            result.append((temp_towers, f'alternative_{alt_blocks}'))
        
        return result
    
    def _create_towers_with_blocks(self, blocks):
        """Create towers with given blocks."""
        sorted_blocks = sorted(blocks, reverse=True)
        towers = []
        
        for block in sorted_blocks:
            best_tower = -1
            for i in range(len(towers)):
                if towers[i][-1] >= block:
                    if best_tower == -1 or len(towers[i]) < len(towers[best_tower]):
                        best_tower = i
            
            if best_tower != -1:
                towers[best_tower].append(block)
            else:
                towers.append([block])
        
        return towers
    
    def get_towers_with_adaptive_criteria(self, adaptive_func):
        """Get towers using adaptive criteria."""
        result = []
        for tower in self.towers:
            if adaptive_func(tower, result):
                result.append(tower)
        return result
    
    def get_tower_optimization(self):
        """Get optimal tower configuration."""
        strategies = [
            ('towers', lambda: len(self.towers)),
            ('weighted_towers', lambda: len(self.get_weighted_towers())),
            ('min_towers', lambda: self.min_towers),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
blocks = [3, 2, 4, 1, 5]
weights = [2, 1, 3, 1, 2]
priorities = [1, 2, 1, 3, 1]
advanced_towers = AdvancedTowers(blocks, weights, priorities)

print(f"Towers: {len(advanced_towers.get_towers())}")
print(f"Weighted towers: {len(advanced_towers.get_weighted_towers())}")

# Get towers with priority
def priority_func(tower):
    return sum(block[0] * block[2] * block[3] for block in tower)

print(f"Towers with priority: {advanced_towers.get_towers_with_priority(priority_func)}")

# Get towers with optimization
def optimization_func(tower):
    return sum(block[0] for block in tower) / len(tower)

print(f"Towers with optimization: {advanced_towers.get_towers_with_optimization(optimization_func)}")

# Get towers with constraints
def constraint_func(tower):
    return len(tower) >= 2 and sum(block[0] for block in tower) > 5

print(f"Towers with constraints: {advanced_towers.get_towers_with_constraints(constraint_func)}")

# Get towers with multiple criteria
def criterion1(tower):
    return len(tower) >= 2

def criterion2(tower):
    return sum(block[0] for block in tower) > 5

criteria_list = [criterion1, criterion2]
print(f"Towers with multiple criteria: {advanced_towers.get_towers_with_multiple_criteria(criteria_list)}")

# Get towers with alternatives
alternatives = [[4, 3, 2, 1], [5, 4, 3, 2, 1]]
print(f"Towers with alternatives: {advanced_towers.get_towers_with_alternatives(alternatives)}")

# Get towers with adaptive criteria
def adaptive_func(tower, current_result):
    return len(tower) >= 2 and len(current_result) < 3

print(f"Towers with adaptive criteria: {advanced_towers.get_towers_with_adaptive_criteria(adaptive_func)}")

# Get tower optimization
print(f"Tower optimization: {advanced_towers.get_tower_optimization()}")
```

### **Variation 3: Towers with Constraints**
**Problem**: Handle tower arrangement with additional constraints (capacity limits, height constraints, weight constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTowers:
    def __init__(self, blocks, constraints=None):
        self.blocks = blocks[:]
        self.constraints = constraints or {}
        self.towers = []
        self.min_towers = 0
        self._update_towers()
    
    def _update_towers(self):
        """Update the optimal tower arrangement considering constraints."""
        # Sort blocks in descending order
        sorted_blocks = sorted(self.blocks, reverse=True)
        
        # Use greedy approach to find minimum towers
        self.towers = []
        
        for block in sorted_blocks:
            # Find the best tower for this block considering constraints
            best_tower = -1
            best_score = float('inf')
            
            for i in range(len(self.towers)):
                if self._can_add_to_tower(self.towers[i], block):
                    # Calculate score based on constraints
                    score = self._calculate_tower_score(self.towers[i], block)
                    if score < best_score:
                        best_score = score
                        best_tower = i
            
            if best_tower != -1:
                self.towers[best_tower].append(block)
            else:
                # Create new tower if constraints allow
                if self._can_create_tower(block):
                    self.towers.append([block])
        
        self.min_towers = len(self.towers)
    
    def _can_add_to_tower(self, tower, block):
        """Check if a block can be added to a tower considering constraints."""
        # Basic constraint: block must fit on top
        if tower[-1] < block:
            return False
        
        # Height constraint
        if 'max_height' in self.constraints:
            if len(tower) + 1 > self.constraints['max_height']:
                return False
        
        # Weight constraint
        if 'max_weight' in self.constraints:
            current_weight = sum(tower) + block
            if current_weight > self.constraints['max_weight']:
                return False
        
        # Capacity constraint
        if 'max_capacity' in self.constraints:
            if len(tower) + 1 > self.constraints['max_capacity']:
                return False
        
        return True
    
    def _can_create_tower(self, block):
        """Check if a new tower can be created with the given block."""
        # Check if we can create more towers
        if 'max_towers' in self.constraints:
            if len(self.towers) >= self.constraints['max_towers']:
                return False
        
        return True
    
    def _calculate_tower_score(self, tower, block):
        """Calculate score for adding block to tower."""
        score = len(tower)  # Prefer shorter towers
        
        # Add penalty for constraint violations
        if 'max_height' in self.constraints:
            if len(tower) + 1 > self.constraints['max_height']:
                score += 1000
        
        if 'max_weight' in self.constraints:
            current_weight = sum(tower) + block
            if current_weight > self.constraints['max_weight']:
                score += 1000
        
        return score
    
    def get_towers_with_capacity_constraints(self, capacity_limits):
        """Get towers considering capacity constraints."""
        result = []
        current_capacity = 0
        
        for tower in self.towers:
            # Check capacity constraints
            tower_capacity = len(tower)
            if current_capacity + tower_capacity <= capacity_limits:
                result.append(tower)
                current_capacity += tower_capacity
        
        return result
    
    def get_towers_with_height_constraints(self, height_limits):
        """Get towers considering height constraints."""
        result = []
        
        for tower in self.towers:
            # Check height constraints
            tower_height = len(tower)
            if height_limits[0] <= tower_height <= height_limits[1]:
                result.append(tower)
        
        return result
    
    def get_towers_with_weight_constraints(self, weight_limits):
        """Get towers considering weight constraints."""
        result = []
        
        for tower in self.towers:
            # Check weight constraints
            tower_weight = sum(tower)
            if weight_limits[0] <= tower_weight <= weight_limits[1]:
                result.append(tower)
        
        return result
    
    def get_towers_with_mathematical_constraints(self, constraint_func):
        """Get towers that satisfy custom mathematical constraints."""
        result = []
        
        for tower in self.towers:
            if constraint_func(tower):
                result.append(tower)
        
        return result
    
    def get_towers_with_range_constraints(self, range_constraints):
        """Get towers that satisfy range constraints."""
        result = []
        
        for tower in self.towers:
            # Check if tower satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(tower):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(tower)
        
        return result
    
    def get_towers_with_optimization_constraints(self, optimization_func):
        """Get towers using custom optimization constraints."""
        # Sort towers by optimization function
        all_towers = []
        for tower in self.towers:
            score = optimization_func(tower)
            all_towers.append((tower, score))
        
        # Sort by optimization score
        all_towers.sort(key=lambda x: x[1], reverse=True)
        
        return [tower for tower, _ in all_towers]
    
    def get_towers_with_multiple_constraints(self, constraints_list):
        """Get towers that satisfy multiple constraints."""
        result = []
        
        for tower in self.towers:
            # Check if tower satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(tower):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                result.append(tower)
        
        return result
    
    def get_towers_with_priority_constraints(self, priority_func):
        """Get towers with priority-based constraints."""
        # Sort towers by priority
        all_towers = []
        for tower in self.towers:
            priority = priority_func(tower)
            all_towers.append((tower, priority))
        
        # Sort by priority
        all_towers.sort(key=lambda x: x[1], reverse=True)
        
        return [tower for tower, _ in all_towers]
    
    def get_towers_with_adaptive_constraints(self, adaptive_func):
        """Get towers with adaptive constraints."""
        result = []
        
        for tower in self.towers:
            # Check adaptive constraints
            if adaptive_func(tower, result):
                result.append(tower)
        
        return result
    
    def get_optimal_tower_strategy(self):
        """Get optimal tower arrangement strategy considering all constraints."""
        strategies = [
            ('capacity_constraints', self.get_towers_with_capacity_constraints),
            ('height_constraints', self.get_towers_with_height_constraints),
            ('weight_constraints', self.get_towers_with_weight_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'capacity_constraints':
                    current_count = len(strategy_func(10))  # Capacity limit of 10
                elif strategy_name == 'height_constraints':
                    current_count = len(strategy_func((1, 5)))  # Height between 1 and 5
                elif strategy_name == 'weight_constraints':
                    current_count = len(strategy_func((5, 20)))  # Weight between 5 and 20
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_height': 4,
    'max_weight': 20,
    'max_towers': 5
}

blocks = [3, 2, 4, 1, 5, 2, 3, 1]
constrained_towers = ConstrainedTowers(blocks, constraints)

print("Capacity-constrained towers:", len(constrained_towers.get_towers_with_capacity_constraints(10)))

print("Height-constrained towers:", len(constrained_towers.get_towers_with_height_constraints((1, 5))))

print("Weight-constrained towers:", len(constrained_towers.get_towers_with_weight_constraints((5, 20))))

# Mathematical constraints
def custom_constraint(tower):
    return len(tower) >= 2 and sum(tower) > 5

print("Mathematical constraint towers:", len(constrained_towers.get_towers_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(tower):
    return 1 <= len(tower) <= 4 and 3 <= sum(tower) <= 15

range_constraints = [range_constraint]
print("Range-constrained towers:", len(constrained_towers.get_towers_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(tower):
    return len(tower) >= 2

def constraint2(tower):
    return sum(tower) > 5

constraints_list = [constraint1, constraint2]
print("Multiple constraints towers:", len(constrained_towers.get_towers_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(tower):
    return sum(tower) / len(tower)

print("Priority-constrained towers:", len(constrained_towers.get_towers_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(tower, current_result):
    return len(tower) >= 2 and len(current_result) < 3

print("Adaptive constraint towers:", len(constrained_towers.get_towers_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_towers.get_optimal_tower_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Towers](https://cses.fi/problemset/task/1073) - Basic towers problem
- [Longest Increasing Subsequence](https://cses.fi/problemset/task/1145) - Related LIS problem
- [Stick Lengths](https://cses.fi/problemset/task/1074) - Similar optimization problem

#### **LeetCode Problems**
- [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - Find longest increasing sequence
- [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) - Nested sequence problem
- [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) - Chain formation problem
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) - Interval scheduling

#### **Problem Categories**
- **Greedy Algorithms**: Optimal local choices, tower arrangement, sequence optimization
- **Longest Increasing Subsequence**: LIS algorithms, binary search, sequence analysis
- **Sorting**: Array sorting, sequence optimization, tower arrangement
- **Algorithm Design**: Greedy strategies, LIS algorithms, optimization techniques
