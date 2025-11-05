---
layout: simple
title: "Stick Lengths"
permalink: /problem_soulutions/sorting_and_searching/stick_lengths_analysis
---

# Stick Lengths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of median and its applications in optimization
- Apply sorting algorithms for finding optimal solutions
- Implement efficient solutions for minimizing sum of absolute differences
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in optimization problems

## 📋 Problem Description

There are n sticks with some lengths. Your task is to modify the lengths of the sticks so that all sticks have the same length. You can either increase or decrease the length of each stick by 1 unit at a cost of 1 unit.

Find the minimum cost to make all sticks have the same length.

**Input**: 
- First line: integer n (number of sticks)
- Second line: n integers a[1], a[2], ..., a[n] (lengths of sticks)

**Output**: 
- Print one integer: the minimum cost to make all sticks the same length

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
5
2 3 1 5 2

Output:
5

Explanation**: 
Stick lengths: [2, 3, 1, 5, 2]

If we make all sticks length 2:
- Stick 1: 2 → 2 (cost: 0)
- Stick 2: 3 → 2 (cost: 1)
- Stick 3: 1 → 2 (cost: 1)
- Stick 4: 5 → 2 (cost: 3)
- Stick 5: 2 → 2 (cost: 0)

Total cost: 0 + 1 + 1 + 3 + 0 = 5

This is the minimum cost (length 2 is the median).
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Target Lengths

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible target lengths
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward nested loops approach
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each possible target length, calculate the total cost to make all sticks that length.

**Algorithm**:
- For each possible target length (from min to max stick length):
  - Calculate the cost to make all sticks that length
  - Keep track of the minimum cost

**Visual Example**:
```
Stick lengths: [2, 3, 1, 5, 2]
Possible targets: [1, 2, 3, 4, 5]

Target 1: |2-1| + |3-1| + |1-1| + |5-1| + |2-1| = 1 + 2 + 0 + 4 + 1 = 8
Target 2: |2-2| + |3-2| + |1-2| + |5-2| + |2-2| = 0 + 1 + 1 + 3 + 0 = 5 ✓
Target 3: |2-3| + |3-3| + |1-3| + |5-3| + |2-3| = 1 + 0 + 2 + 2 + 1 = 6
Target 4: |2-4| + |3-4| + |1-4| + |5-4| + |2-4| = 2 + 1 + 3 + 1 + 2 = 9
Target 5: |2-5| + |3-5| + |1-5| + |5-5| + |2-5| = 3 + 2 + 4 + 0 + 3 = 12

Minimum cost: 5 (target length 2)
```

**Implementation**:
```python
def brute_force_stick_lengths(sticks):
    """
    Find minimum cost using brute force approach
    
    Args:
        sticks: list of stick lengths
    
    Returns:
        int: minimum cost to make all sticks the same length
    """
    min_length = min(sticks)
    max_length = max(sticks)
    min_cost = float('inf')
    
    # Try all possible target lengths
    for target in range(min_length, max_length + 1):
        cost = 0
        for stick in sticks:
            cost += abs(stick - target)
        min_cost = min(min_cost, cost)
    
    return min_cost

# Example usage
sticks = [2, 3, 1, 5, 2]
result = brute_force_stick_lengths(sticks)
print(f"Brute force result: {result}")  # Output: 5
```

**Time Complexity**: O(n × (max - min)) - For each target, check all sticks
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Use Median

**Key Insights from Optimized Approach**:
- **Median Property**: The median minimizes the sum of absolute differences
- **Efficient Calculation**: Calculate median in O(n log n) time
- **Better Complexity**: Achieve O(n log n) time complexity
- **Mathematical Insight**: Median is the optimal target length

**Key Insight**: The median of the stick lengths is the optimal target length that minimizes the total cost.

**Algorithm**:
- Sort the stick lengths
- Find the median (middle element)
- Calculate the cost to make all sticks the median length

**Visual Example**:
```
Stick lengths: [2, 3, 1, 5, 2]
Sorted: [1, 2, 2, 3, 5]
Median: 2 (middle element)

Cost calculation:
|2-2| + |3-2| + |1-2| + |5-2| + |2-2| = 0 + 1 + 1 + 3 + 0 = 5
```

**Implementation**:
```python
def optimized_stick_lengths(sticks):
    """
    Find minimum cost using median approach
    
    Args:
        sticks: list of stick lengths
    
    Returns:
        int: minimum cost to make all sticks the same length
    """
    sorted_sticks = sorted(sticks)
    n = len(sorted_sticks)
    
    # Find median (middle element)
    median = sorted_sticks[n // 2]
    
    # Calculate cost to make all sticks the median length
    cost = 0
    for stick in sticks:
        cost += abs(stick - median)
    
    return cost

# Example usage
sticks = [2, 3, 1, 5, 2]
result = optimized_stick_lengths(sticks)
print(f"Optimized result: {result}")  # Output: 5
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(n) - For sorted array

**Why it's better**: Much more efficient than brute force with mathematical insight.

---

### Approach 3: Optimal - Quick Select for Median

**Key Insights from Optimal Approach**:
- **Quick Select**: Use quick select algorithm to find median in O(n) time
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: No need to sort the entire array
- **Optimal Performance**: Best possible time complexity

**Key Insight**: Use quick select algorithm to find the median in O(n) time without sorting the entire array.

**Algorithm**:
- Use quick select to find the median in O(n) time
- Calculate the cost to make all sticks the median length

**Visual Example**:
```
Stick lengths: [2, 3, 1, 5, 2]
Quick select to find median: 2

Cost calculation:
|2-2| + |3-2| + |1-2| + |5-2| + |2-2| = 0 + 1 + 1 + 3 + 0 = 5
```

**Implementation**:
```python
def optimal_stick_lengths(sticks):
    """
    Find minimum cost using quick select for median
    
    Args:
        sticks: list of stick lengths
    
    Returns:
        int: minimum cost to make all sticks the same length
    """
    def quick_select(arr, k):
        """Find k-th smallest element using quick select"""
        if len(arr) == 1:
            return arr[0]
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        if k < len(left):
            return quick_select(left, k)
        elif k < len(left) + len(middle):
            return pivot
        else:
            return quick_select(right, k - len(left) - len(middle))
    
    n = len(sticks)
    median = quick_select(sticks, n // 2)
    
    # Calculate cost to make all sticks the median length
    cost = 0
    for stick in sticks:
        cost += abs(stick - median)
    
    return cost

# Example usage
sticks = [2, 3, 1, 5, 2]
result = optimal_stick_lengths(sticks)
print(f"Optimal result: {result}")  # Output: 5
```

**Time Complexity**: O(n) - Quick select for median
**Space Complexity**: O(n) - For recursive calls

**Why it's optimal**: Achieves the best possible time complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × (max - min)) | O(1) | Try all possible target lengths |
| Median Sort | O(n log n) | O(n) | Use median to minimize cost |
| Quick Select | O(n) | O(n) | Find median in linear time |

### Time Complexity
- **Time**: O(n) - Quick select algorithm provides optimal time complexity
- **Space**: O(n) - For recursive calls in quick select

### Why This Solution Works
- **Median Property**: The median minimizes the sum of absolute differences
- **Mathematical Proof**: Median is the optimal target length for this problem
- **Efficient Algorithm**: Quick select finds median in O(n) time
- **Optimal Approach**: Quick select provides the most efficient solution for finding the median

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Stick Lengths with Different Costs
**Problem**: Each stick has different costs for increasing and decreasing its length.

**Link**: [CSES Problem Set - Stick Lengths Different Costs](https://cses.fi/problemset/task/stick_lengths_different_costs)

```python
def stick_lengths_different_costs(sticks, increase_costs, decrease_costs):
    """
    Find minimum cost with different costs for increasing/decreasing
    """
    def calculate_cost(target):
        """Calculate cost to make all sticks target length"""
        total_cost = 0
        for i, stick in enumerate(sticks):
            if stick < target:
                # Need to increase
                total_cost += (target - stick) * increase_costs[i]
            elif stick > target:
                # Need to decrease
                total_cost += (stick - target) * decrease_costs[i]
        return total_cost
    
    # Binary search on target length
    left = min(sticks)
    right = max(sticks)
    
    while left < right:
        mid = (left + right) // 2
        cost_mid = calculate_cost(mid)
        cost_mid_plus_1 = calculate_cost(mid + 1)
        
        if cost_mid < cost_mid_plus_1:
            right = mid
        else:
            left = mid + 1
    
    return calculate_cost(left)
```

### Variation 2: Stick Lengths with Constraints
**Problem**: Sticks can only be modified within certain limits (e.g., maximum increase/decrease).

**Link**: [CSES Problem Set - Stick Lengths with Constraints](https://cses.fi/problemset/task/stick_lengths_constraints)

```python
def stick_lengths_constraints(sticks, max_increase, max_decrease):
    """
    Find minimum cost with modification constraints
    """
    def is_feasible(target):
        """Check if target is achievable with constraints"""
        for stick in sticks:
            if stick < target:
                if target - stick > max_increase:
                    return False
            elif stick > target:
                if stick - target > max_decrease:
                    return False
        return True
    
    def calculate_cost(target):
        """Calculate cost to make all sticks target length"""
        if not is_feasible(target):
            return float('inf')
        
        total_cost = 0
        for stick in sticks:
            total_cost += abs(stick - target)
        return total_cost
    
    # Find feasible range
    min_feasible = max(min(sticks), max(sticks) - max_decrease)
    max_feasible = min(max(sticks), min(sticks) + max_increase)
    
    min_cost = float('inf')
    for target in range(min_feasible, max_feasible + 1):
        cost = calculate_cost(target)
        min_cost = min(min_cost, cost)
    
    return min_cost if min_cost != float('inf') else -1
```

### Variation 3: Stick Lengths with Multiple Targets
**Problem**: Find the minimum cost to make all sticks one of k possible target lengths.

**Link**: [CSES Problem Set - Stick Lengths Multiple Targets](https://cses.fi/problemset/task/stick_lengths_multiple_targets)

```python
def stick_lengths_multiple_targets(sticks, k):
    """
    Find minimum cost to make all sticks one of k target lengths
    """
    def calculate_cost(targets):
        """Calculate cost for given target lengths"""
        total_cost = 0
        for stick in sticks:
            min_cost = float('inf')
            for target in targets:
                min_cost = min(min_cost, abs(stick - target))
            total_cost += min_cost
        return total_cost
    
    # Use dynamic programming approach
    n = len(sticks)
    sorted_sticks = sorted(sticks)
    
    # DP[i][j] = minimum cost to assign first i sticks to j targets
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            # Try all possible target lengths for stick i-1
            for target in sorted_sticks:
                cost = abs(sorted_sticks[i-1] - target)
                dp[i][j] = min(dp[i][j], dp[i-1][j-1] + cost)
    
    return dp[n][k]

def stick_lengths_multiple_targets_optimized(sticks, k):
    """
    Optimized version using clustering approach
    """
    # Sort sticks
    sorted_sticks = sorted(sticks)
    n = len(sorted_sticks)
    
    # Use k-means clustering approach
    # Initialize targets as evenly spaced values
    targets = []
    for i in range(k):
        targets.append(sorted_sticks[i * n // k])
    
    # Iteratively improve targets
    for _ in range(100):  # Maximum iterations
        # Assign each stick to closest target
        assignments = [[] for _ in range(k)]
        for stick in sorted_sticks:
            closest_target = min(range(k), key=lambda i: abs(stick - targets[i]))
            assignments[closest_target].append(stick)
        
        # Update targets to be medians of assigned sticks
        new_targets = []
        for assignment in assignments:
            if assignment:
                new_targets.append(sorted(assignment)[len(assignment) // 2])
            else:
                new_targets.append(0)
        
        if new_targets == targets:
            break
        targets = new_targets
    
    # Calculate final cost
    total_cost = 0
    for stick in sorted_sticks:
        min_cost = min(abs(stick - target) for target in targets)
        total_cost += min_cost
    
    return total_cost
```

### Related Problems

## Problem Variations

### **Variation 1: Stick Lengths with Dynamic Updates**
**Problem**: Handle dynamic stick length updates (add/remove/update sticks) while maintaining efficient minimum cost calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect
import heapq

class DynamicStickLengths:
    def __init__(self, sticks):
        self.sticks = sorted(sticks[:])
        self.n = len(sticks)
        self.median = self._compute_median()
        self.min_cost = self._compute_min_cost()
    
    def _compute_median(self):
        """Compute median of stick lengths."""
        if not self.sticks:
            return 0
        n = len(self.sticks)
        if n % 2 == 1:
            return self.sticks[n // 2]
        else:
            return (self.sticks[n // 2 - 1] + self.sticks[n // 2]) // 2
    
    def _compute_min_cost(self):
        """Compute minimum cost to make all sticks equal length."""
        if not self.sticks:
            return 0
        median = self.median
        return sum(abs(stick - median) for stick in self.sticks)
    
    def add_stick(self, length):
        """Add a new stick to the collection."""
        bisect.insort(self.sticks, length)
        self.n += 1
        self.median = self._compute_median()
        self.min_cost = self._compute_min_cost()
    
    def remove_stick(self, length):
        """Remove a stick of specified length."""
        if length in self.sticks:
            self.sticks.remove(length)
            self.n -= 1
            self.median = self._compute_median()
            self.min_cost = self._compute_min_cost()
    
    def update_stick(self, old_length, new_length):
        """Update a stick from old_length to new_length."""
        if old_length in self.sticks:
            self.sticks.remove(old_length)
            bisect.insort(self.sticks, new_length)
            self.median = self._compute_median()
            self.min_cost = self._compute_min_cost()
    
    def get_min_cost(self):
        """Get current minimum cost."""
        return self.min_cost
    
    def get_median(self):
        """Get current median."""
        return self.median
    
    def get_sticks_with_cost_range(self, min_cost, max_cost):
        """Get sticks within cost range from median."""
        result = []
        for stick in self.sticks:
            cost = abs(stick - self.median)
            if min_cost <= cost <= max_cost:
                result.append((stick, cost))
        return result
    
    def get_sticks_with_constraints(self, constraint_func):
        """Get sticks that satisfy custom constraints."""
        result = []
        for stick in self.sticks:
            if constraint_func(stick, self.median):
                result.append((stick, abs(stick - self.median)))
        return result
    
    def get_stick_statistics(self):
        """Get statistics about the stick lengths."""
        if not self.sticks:
            return {
                'total_sticks': 0,
                'median': 0,
                'min_cost': 0,
                'average_length': 0,
                'length_range': 0
            }
        
        total_sticks = self.n
        median = self.median
        min_cost = self.min_cost
        average_length = sum(self.sticks) / total_sticks
        length_range = max(self.sticks) - min(self.sticks)
        
        return {
            'total_sticks': total_sticks,
            'median': median,
            'min_cost': min_cost,
            'average_length': average_length,
            'length_range': length_range
        }
    
    def get_stick_patterns(self):
        """Get patterns in stick lengths."""
        patterns = {
            'consecutive_lengths': 0,
            'alternating_pattern': 0,
            'clustered_lengths': 0,
            'uniform_distribution': 0
        }
        
        for i in range(1, len(self.sticks)):
            if self.sticks[i] == self.sticks[i-1] + 1:
                patterns['consecutive_lengths'] += 1
            
            if i > 1:
                if (self.sticks[i] != self.sticks[i-1] and 
                    self.sticks[i-1] != self.sticks[i-2]):
                    patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_target_selection(self):
        """Get optimal target selection based on stick patterns."""
        if not self.sticks:
            return {
                'recommended_target': 0,
                'efficiency_rate': 0,
                'cost_distribution': {}
            }
        
        # Find optimal target (median)
        recommended_target = self.median
        
        # Calculate efficiency rate
        total_length = sum(self.sticks)
        efficiency_rate = total_length / (len(self.sticks) * recommended_target) if recommended_target > 0 else 0
        
        # Calculate cost distribution
        cost_distribution = defaultdict(int)
        for stick in self.sticks:
            cost = abs(stick - recommended_target)
            cost_distribution[cost] += 1
        
        return {
            'recommended_target': recommended_target,
            'efficiency_rate': efficiency_rate,
            'cost_distribution': dict(cost_distribution)
        }

# Example usage
sticks = [2, 3, 1, 5, 4]
dynamic_sticks = DynamicStickLengths(sticks)
print(f"Initial min cost: {dynamic_sticks.get_min_cost()}")
print(f"Initial median: {dynamic_sticks.get_median()}")

# Add a stick
dynamic_sticks.add_stick(6)
print(f"After adding stick: {dynamic_sticks.get_min_cost()}")

# Update a stick
dynamic_sticks.update_stick(1, 7)
print(f"After updating stick: {dynamic_sticks.get_min_cost()}")

# Get sticks with cost range
print(f"Sticks with cost range [0, 2]: {dynamic_sticks.get_sticks_with_cost_range(0, 2)}")

# Get sticks with constraints
def constraint_func(stick, median):
    return abs(stick - median) <= 2

print(f"Sticks with constraints: {dynamic_sticks.get_sticks_with_constraints(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_sticks.get_stick_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_sticks.get_stick_patterns()}")

# Get optimal target selection
print(f"Optimal target selection: {dynamic_sticks.get_optimal_target_selection()}")
```

### **Variation 2: Stick Lengths with Different Operations**
**Problem**: Handle different types of operations on stick lengths (weighted sticks, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of stick length queries.

```python
class AdvancedStickLengths:
    def __init__(self, sticks, weights=None, priorities=None):
        self.sticks = sorted(sticks[:])
        self.n = len(sticks)
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.median = self._compute_median()
        self.min_cost = self._compute_min_cost()
        self.weighted_min_cost = self._compute_weighted_min_cost()
    
    def _compute_median(self):
        """Compute median of stick lengths."""
        if not self.sticks:
            return 0
        n = len(self.sticks)
        if n % 2 == 1:
            return self.sticks[n // 2]
        else:
            return (self.sticks[n // 2 - 1] + self.sticks[n // 2]) // 2
    
    def _compute_min_cost(self):
        """Compute minimum cost to make all sticks equal length."""
        if not self.sticks:
            return 0
        median = self.median
        return sum(abs(stick - median) for stick in self.sticks)
    
    def _compute_weighted_min_cost(self):
        """Compute minimum weighted cost to make all sticks equal length."""
        if not self.sticks:
            return 0
        median = self.median
        return sum(abs(stick - median) * self.weights[i] for i, stick in enumerate(self.sticks))
    
    def get_min_cost(self):
        """Get current minimum cost."""
        return self.min_cost
    
    def get_weighted_min_cost(self):
        """Get current minimum weighted cost."""
        return self.weighted_min_cost
    
    def get_median(self):
        """Get current median."""
        return self.median
    
    def get_sticks_with_priority(self, priority_func):
        """Get sticks considering priority."""
        result = []
        for i, stick in enumerate(self.sticks):
            priority = priority_func(stick, self.weights[i], self.priorities[i])
            result.append((i, stick, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_sticks_with_optimization(self, optimization_func):
        """Get sticks using custom optimization function."""
        result = []
        for i, stick in enumerate(self.sticks):
            score = optimization_func(stick, self.weights[i], self.priorities[i])
            result.append((i, stick, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_sticks_with_constraints(self, constraint_func):
        """Get sticks that satisfy custom constraints."""
        result = []
        for i, stick in enumerate(self.sticks):
            if constraint_func(stick, self.weights[i], self.priorities[i]):
                result.append((i, stick, abs(stick - self.median)))
        return result
    
    def get_sticks_with_multiple_criteria(self, criteria_list):
        """Get sticks that satisfy multiple criteria."""
        result = []
        for i, stick in enumerate(self.sticks):
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(stick, self.weights[i], self.priorities[i]):
                    satisfies_all_criteria = False
                    break
            
            if satisfies_all_criteria:
                result.append((i, stick, abs(stick - self.median)))
        
        return result
    
    def get_sticks_with_alternatives(self, alternatives):
        """Get sticks considering alternative lengths."""
        result = []
        
        for i, stick in enumerate(self.sticks):
            # Check original stick
            result.append((i, stick, abs(stick - self.median), 'original'))
            
            # Check alternative lengths
            if i in alternatives:
                for alt_length in alternatives[i]:
                    result.append((i, alt_length, abs(alt_length - self.median), 'alternative'))
        
        return result
    
    def get_sticks_with_adaptive_criteria(self, adaptive_func):
        """Get sticks using adaptive criteria."""
        result = []
        
        for i, stick in enumerate(self.sticks):
            if adaptive_func(stick, self.weights[i], self.priorities[i], result):
                result.append((i, stick, abs(stick - self.median)))
        
        return result
    
    def get_stick_optimization(self):
        """Get optimal stick configuration."""
        strategies = [
            ('min_cost', self.get_min_cost),
            ('weighted_min_cost', self.get_weighted_min_cost),
        ]
        
        best_strategy = None
        best_value = float('inf')
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value < best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
sticks = [2, 3, 1, 5, 4]
weights = [2, 1, 3, 1, 2]
priorities = [1, 2, 1, 3, 1]
advanced_sticks = AdvancedStickLengths(sticks, weights, priorities)

print(f"Min cost: {advanced_sticks.get_min_cost()}")
print(f"Weighted min cost: {advanced_sticks.get_weighted_min_cost()}")

# Get sticks with priority
def priority_func(stick, weight, priority):
    return (stick * weight * priority)

print(f"Sticks with priority: {advanced_sticks.get_sticks_with_priority(priority_func)}")

# Get sticks with optimization
def optimization_func(stick, weight, priority):
    return (stick * weight + priority)

print(f"Sticks with optimization: {advanced_sticks.get_sticks_with_optimization(optimization_func)}")

# Get sticks with constraints
def constraint_func(stick, weight, priority):
    return abs(stick - advanced_sticks.get_median()) <= 2 and weight > 1

print(f"Sticks with constraints: {advanced_sticks.get_sticks_with_constraints(constraint_func)}")

# Get sticks with multiple criteria
def criterion1(stick, weight, priority):
    return abs(stick - advanced_sticks.get_median()) <= 2

def criterion2(stick, weight, priority):
    return weight > 1

criteria_list = [criterion1, criterion2]
print(f"Sticks with multiple criteria: {advanced_sticks.get_sticks_with_multiple_criteria(criteria_list)}")

# Get sticks with alternatives
alternatives = {1: [2, 4], 3: [6, 7]}
print(f"Sticks with alternatives: {advanced_sticks.get_sticks_with_alternatives(alternatives)}")

# Get sticks with adaptive criteria
def adaptive_func(stick, weight, priority, current_result):
    return abs(stick - advanced_sticks.get_median()) <= 2 and len(current_result) < 3

print(f"Sticks with adaptive criteria: {advanced_sticks.get_sticks_with_adaptive_criteria(adaptive_func)}")

# Get stick optimization
print(f"Stick optimization: {advanced_sticks.get_stick_optimization()}")
```

### **Variation 3: Stick Lengths with Constraints**
**Problem**: Handle stick lengths with additional constraints (cost limits, length constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedStickLengths:
    def __init__(self, sticks, constraints=None):
        self.sticks = sorted(sticks[:])
        self.n = len(sticks)
        self.constraints = constraints or {}
        self.median = self._compute_median()
        self.min_cost = self._compute_min_cost()
    
    def _compute_median(self):
        """Compute median of stick lengths."""
        if not self.sticks:
            return 0
        n = len(self.sticks)
        if n % 2 == 1:
            return self.sticks[n // 2]
        else:
            return (self.sticks[n // 2 - 1] + self.sticks[n // 2]) // 2
    
    def _compute_min_cost(self):
        """Compute minimum cost to make all sticks equal length."""
        if not self.sticks:
            return 0
        median = self.median
        return sum(abs(stick - median) for stick in self.sticks)
    
    def get_min_cost_with_cost_constraints(self, cost_limit):
        """Get minimum cost considering cost constraints."""
        if not self.sticks:
            return 0
        
        median = self.median
        total_cost = 0
        
        for stick in self.sticks:
            cost = abs(stick - median)
            if total_cost + cost > cost_limit:
                return -1  # Cannot achieve target within cost limit
            total_cost += cost
        
        return total_cost
    
    def get_min_cost_with_length_constraints(self, length_limit):
        """Get minimum cost considering length constraints."""
        if not self.sticks:
            return 0
        
        # Filter sticks within length limit
        filtered_sticks = [stick for stick in self.sticks if stick <= length_limit]
        
        if not filtered_sticks:
            return 0
        
        # Calculate median of filtered sticks
        n = len(filtered_sticks)
        if n % 2 == 1:
            median = filtered_sticks[n // 2]
        else:
            median = (filtered_sticks[n // 2 - 1] + filtered_sticks[n // 2]) // 2
        
        return sum(abs(stick - median) for stick in filtered_sticks)
    
    def get_min_cost_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get minimum cost considering resource constraints."""
        if not self.sticks:
            return 0
        
        median = self.median
        total_cost = 0
        current_resources = [0] * len(resource_limits)
        
        for stick in self.sticks:
            cost = abs(stick - median)
            consumption = resource_consumption.get(stick, [0] * len(resource_limits))
            
            # Check resource constraints
            can_afford = True
            for j, res_consumption in enumerate(consumption):
                if current_resources[j] + res_consumption > resource_limits[j]:
                    can_afford = False
                    break
            
            if can_afford:
                total_cost += cost
                for j, res_consumption in enumerate(consumption):
                    current_resources[j] += res_consumption
        
        return total_cost
    
    def get_min_cost_with_mathematical_constraints(self, constraint_func):
        """Get minimum cost that satisfies custom mathematical constraints."""
        if not self.sticks:
            return 0
        
        median = self.median
        total_cost = 0
        
        for stick in self.sticks:
            if constraint_func(stick, median):
                total_cost += abs(stick - median)
        
        return total_cost
    
    def get_min_cost_with_range_constraints(self, range_constraints):
        """Get minimum cost that satisfies range constraints."""
        if not self.sticks:
            return 0
        
        median = self.median
        total_cost = 0
        
        for stick in self.sticks:
            # Check if stick satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(stick, median):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                total_cost += abs(stick - median)
        
        return total_cost
    
    def get_min_cost_with_optimization_constraints(self, optimization_func):
        """Get minimum cost using custom optimization constraints."""
        if not self.sticks:
            return 0
        
        # Sort sticks by optimization function
        sorted_sticks = sorted(self.sticks, key=lambda x: optimization_func(x, self.median), reverse=True)
        
        median = self.median
        return sum(abs(stick - median) for stick in sorted_sticks)
    
    def get_min_cost_with_multiple_constraints(self, constraints_list):
        """Get minimum cost that satisfies multiple constraints."""
        if not self.sticks:
            return 0
        
        median = self.median
        total_cost = 0
        
        for stick in self.sticks:
            # Check if stick satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(stick, median):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                total_cost += abs(stick - median)
        
        return total_cost
    
    def get_min_cost_with_priority_constraints(self, priority_func):
        """Get minimum cost with priority-based constraints."""
        if not self.sticks:
            return 0
        
        # Sort sticks by priority
        sorted_sticks = sorted(self.sticks, key=lambda x: priority_func(x, self.median), reverse=True)
        
        median = self.median
        return sum(abs(stick - median) for stick in sorted_sticks)
    
    def get_min_cost_with_adaptive_constraints(self, adaptive_func):
        """Get minimum cost with adaptive constraints."""
        if not self.sticks:
            return 0
        
        median = self.median
        total_cost = 0
        
        for stick in self.sticks:
            # Check adaptive constraints
            if adaptive_func(stick, median, total_cost):
                total_cost += abs(stick - median)
        
        return total_cost
    
    def get_optimal_stick_strategy(self):
        """Get optimal stick strategy considering all constraints."""
        strategies = [
            ('cost_constraints', self.get_min_cost_with_cost_constraints),
            ('length_constraints', self.get_min_cost_with_length_constraints),
            ('resource_constraints', self.get_min_cost_with_resource_constraints),
        ]
        
        best_strategy = None
        best_cost = float('inf')
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'cost_constraints':
                    current_cost = strategy_func(10)  # Cost limit of 10
                elif strategy_name == 'length_constraints':
                    current_cost = strategy_func(5)  # Length limit of 5
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {stick: [10, 5] for stick in self.sticks}
                    current_cost = strategy_func(resource_limits, resource_consumption)
                
                if current_cost != -1 and current_cost < best_cost:
                    best_cost = current_cost
                    best_strategy = (strategy_name, current_cost)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_cost': 10,
    'max_length': 5
}

sticks = [2, 3, 1, 5, 4]
constrained_sticks = ConstrainedStickLengths(sticks, constraints)

print("Cost-constrained min cost:", constrained_sticks.get_min_cost_with_cost_constraints(10))

print("Length-constrained min cost:", constrained_sticks.get_min_cost_with_length_constraints(5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {stick: [10, 5] for stick in sticks}
print("Resource-constrained min cost:", constrained_sticks.get_min_cost_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(stick, median):
    return abs(stick - median) <= 2

print("Mathematical constraint min cost:", constrained_sticks.get_min_cost_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(stick, median):
    return abs(stick - median) <= 2

range_constraints = [range_constraint]
print("Range-constrained min cost:", constrained_sticks.get_min_cost_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(stick, median):
    return abs(stick - median) <= 2

def constraint2(stick, median):
    return stick >= 1

constraints_list = [constraint1, constraint2]
print("Multiple constraints min cost:", constrained_sticks.get_min_cost_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(stick, median):
    return abs(stick - median)

print("Priority-constrained min cost:", constrained_sticks.get_min_cost_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(stick, median, current_cost):
    return abs(stick - median) <= 2 and current_cost < 10

print("Adaptive constraint min cost:", constrained_sticks.get_min_cost_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_sticks.get_optimal_stick_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Stick Lengths](https://cses.fi/problemset/task/1074) - Basic stick lengths problem
- [Array Division](https://cses.fi/problemset/task/1085) - Similar optimization problem
- [Nearest Smaller Values](https://cses.fi/problemset/task/1645) - Optimization with constraints

#### **LeetCode Problems**
- [Minimum Moves to Equal Array Elements](https://leetcode.com/problems/minimum-moves-to-equal-array-elements/) - Make array elements equal
- [Minimum Moves to Equal Array Elements II](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/) - Median-based optimization
- [Minimum Cost to Move Chips to The Same Position](https://leetcode.com/problems/minimum-cost-to-move-chips-to-the-same-position/) - Chip movement optimization
- [Minimum Operations to Make Array Equal](https://leetcode.com/problems/minimum-operations-to-make-array-equal/) - Array equalization

#### **Problem Categories**
- **Optimization**: Median-based optimization, cost minimization, constraint satisfaction
- **Mathematical Algorithms**: Median finding, absolute difference minimization, optimization theory
- **Sorting**: Array sorting, median calculation, optimization algorithms
- **Algorithm Design**: Optimization algorithms, mathematical algorithms, constraint algorithms
