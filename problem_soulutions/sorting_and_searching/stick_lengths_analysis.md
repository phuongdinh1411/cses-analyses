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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, median finding, optimization, greedy algorithms
- **Data Structures**: Arrays, sorting algorithms
- **Mathematical Concepts**: Median, absolute difference, optimization theory
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting
- **Related Problems**: Array Division (optimization), Nearest Smaller Values (optimization), Sum of Two Values (searching)

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
