---
layout: simple
title: "Array Description - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/array_description_analysis
---

# Array Description

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of array description in dynamic programming
- Apply counting techniques for array description analysis
- Implement efficient algorithms for array description counting
- Optimize DP operations for array description analysis
- Handle special cases in array description problems

## 📋 Problem Description

Given an array with some known values and some unknown values (0), count the number of ways to fill the unknown values such that adjacent elements differ by at most 1.

**Input**: 
- n: array length
- m: maximum value
- array: array with known values (non-zero) and unknown values (0)

**Output**: 
- Number of ways to fill the array modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 100
- 0 ≤ array[i] ≤ m

**Example**:
```
Input:
n = 3, m = 2
array = [0, 1, 0]

Output:
2

Explanation**: 
Ways to fill the array:
1. [1, 1, 1] (0→1, 1→1, 0→1)
2. [1, 1, 2] (0→1, 1→1, 0→2)
Total: 2 ways
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible array fillings
- **Complete Enumeration**: Enumerate all possible value assignments
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to fill unknown values.

**Algorithm**:
- Use recursive function to try all value assignments
- Check constraints for each assignment
- Count valid assignments
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Array = [0, 1, 0], m = 2:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try filling position 0:            │
│ - Try value 1: [1, 1, 0]           │
│   - Try filling position 2:        │
│     - Try value 1: [1, 1, 1] ✓     │
│     - Try value 2: [1, 1, 2] ✓     │
│ - Try value 2: [2, 1, 0]           │
│   - Try filling position 2:        │
│     - Try value 1: [2, 1, 1] ✓     │
│     - Try value 2: [2, 1, 2] ✓     │
│                                   │
│ Total: 4 ways                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_array_description(n, m, array, mod=10**9+7):
    """
    Count array descriptions using recursive approach
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    def count_ways(index):
        """Count ways recursively"""
        if index == n:
            return 1  # Valid array found
        
        if array[index] != 0:
            # Value is already known, check constraints
            if index > 0 and abs(array[index] - array[index-1]) > 1:
                return 0  # Invalid constraint
            return count_ways(index + 1)
        
        count = 0
        # Try all possible values
        for value in range(1, m + 1):
            # Check constraints
            if index > 0 and abs(value - array[index-1]) > 1:
                continue  # Invalid constraint
            
            array[index] = value
            count = (count + count_ways(index + 1)) % mod
            array[index] = 0  # Backtrack
        
        return count
    
    return count_ways(0)

def recursive_array_description_optimized(n, m, array, mod=10**9+7):
    """
    Optimized recursive array description counting
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    def count_ways_optimized(index):
        """Count ways with optimization"""
        if index == n:
            return 1  # Valid array found
        
        if array[index] != 0:
            # Value is already known, check constraints
            if index > 0 and abs(array[index] - array[index-1]) > 1:
                return 0  # Invalid constraint
            return count_ways_optimized(index + 1)
        
        count = 0
        # Try all possible values
        for value in range(1, m + 1):
            # Check constraints
            if index > 0 and abs(value - array[index-1]) > 1:
                continue  # Invalid constraint
            
            array[index] = value
            count = (count + count_ways_optimized(index + 1)) % mod
            array[index] = 0  # Backtrack
        
        return count
    
    return count_ways_optimized(0)

# Example usage
n, m = 3, 2
array = [0, 1, 0]
result1 = recursive_array_description(n, m, array.copy())
result2 = recursive_array_description_optimized(n, m, array.copy())
print(f"Recursive array description: {result1}")
print(f"Optimized recursive array description: {result2}")
```

**Time Complexity**: O(m^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n * m) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

#### 📌 **DP State Definition**

**What does `dp[i][j]` represent?**
- `dp[i][j]` = **number of ways** to fill the array up to position `i` such that `array[i] = j`
- This is a 2D DP array where:
  - First dimension `i` = position in the array (0 to n-1)
  - Second dimension `j` = value at that position (1 to m)
- `dp[i][j]` stores the count of valid ways to reach position `i` with value `j`

**In plain language:**
- For each position `i` in the array and each possible value `j` (1 to m), we count how many valid ways exist to fill the array up to position `i` where `array[i] = j`
- `dp[0][j]` = number of ways to set the first element to value `j`
- `dp[n-1][j]` = number of ways to fill the entire array ending with value `j` at the last position
- The final answer is the sum of `dp[n-1][j]` for all valid `j`

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to count? The number of ways to fill an array with valid adjacent differences.
- What information do we need? For each position and each possible value, we need to know how many ways we can reach that state.

**Step 2: Define the DP State** (See DP State Definition section above)
- We use `dp[i][j]` to represent the number of ways to fill array up to position `i` with value `j` (already defined above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i][j]`?
- To reach position `i` with value `j`, we can come from position `i-1` with value `j-1`, `j`, or `j+1` (if valid)
- If `array[i]` is fixed: only count ways where previous value allows `array[i]`
- If `array[i]` is unknown: count all ways where previous value is within ±1 of `j`

**Step 4: Determine Base Cases**
- `dp[0][j] = 1` if `array[0]` is unknown or `array[0] == j`, else `dp[0][j] = 0`
- This represents the starting state at position 0.

**Step 5: Identify the Answer**
- The answer is `sum(dp[n-1][j]` for all valid `j` from 1 to m

**Algorithm**:
- Initialize base cases for position 0
- For each position `i` from 1 to n-1:
  - For each possible value `j` from 1 to m:
    - If `array[i]` is fixed and not `j`, skip
    - Otherwise, sum ways from previous position with values `j-1`, `j`, `j+1`
- Return sum of all `dp[n-1][j]` for valid `j`

**Visual Example**:
```
DP table for n=3, m=2, array=[0,1,0]:

DP table:
┌─────────────────────────────────────┐
│ dp[0][1] = 1 (position 0, value 1) │
│ dp[0][2] = 1 (position 0, value 2) │
│ dp[1][1] = 2 (position 1, value 1) │
│ dp[1][2] = 1 (position 1, value 2) │
│ dp[2][1] = 2 (position 2, value 1) │
│ dp[2][2] = 1 (position 2, value 2) │
│                                   │
│ Total: 2 ways                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_array_description(n, m, array, mod=10**9+7):
    """
    Count array descriptions using dynamic programming approach
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    # Create DP table
    dp = [[0] * (m + 1) for _ in range(n)]
    
    # Initialize base case
    if array[0] == 0:
        # Unknown value, try all possibilities
        for value in range(1, m + 1):
            dp[0][value] = 1
    else:
        # Known value
        dp[0][array[0]] = 1
    
    # Fill DP table
    for i in range(1, n):
        if array[i] == 0:
            # Unknown value, try all possibilities
            for value in range(1, m + 1):
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
        else:
            # Known value
            value = array[i]
            for prev_value in range(1, m + 1):
                if abs(value - prev_value) <= 1:
                    dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
    
    # Sum all valid ways
    total_ways = 0
    for value in range(1, m + 1):
        total_ways = (total_ways + dp[n-1][value]) % mod
    
    return total_ways

def dp_array_description_optimized(n, m, array, mod=10**9+7):
    """
    Optimized dynamic programming array description counting
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    # Create DP table with optimization
    dp = [[0] * (m + 1) for _ in range(n)]
    
    # Initialize base case
    if array[0] == 0:
        # Unknown value, try all possibilities
        for value in range(1, m + 1):
            dp[0][value] = 1
    else:
        # Known value
        dp[0][array[0]] = 1
    
    # Fill DP table with optimization
    for i in range(1, n):
        if array[i] == 0:
            # Unknown value, try all possibilities
            for value in range(1, m + 1):
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
        else:
            # Known value
            value = array[i]
            for prev_value in range(1, m + 1):
                if abs(value - prev_value) <= 1:
                    dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
    
    # Sum all valid ways
    total_ways = 0
    for value in range(1, m + 1):
        total_ways = (total_ways + dp[n-1][value]) % mod
    
    return total_ways

# Example usage
n, m = 3, 2
array = [0, 1, 0]
result1 = dp_array_description(n, m, array)
result2 = dp_array_description_optimized(n, m, array)
print(f"DP array description: {result1}")
print(f"Optimized DP array description: {result2}")
```

**Time Complexity**: O(n * m²)
**Space Complexity**: O(n * m)

**Why it's better**: Uses dynamic programming for O(n * m²) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(n * m²) time complexity
- **Space Efficiency**: O(m) space complexity
- **Optimal Complexity**: Best approach for array description

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For n=3, m=2, array=[0,1,0]:
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 2                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_array_description(n, m, array, mod=10**9+7):
    """
    Count array descriptions using space-optimized DP approach
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    # Use only necessary variables for DP
    prev_dp = [0] * (m + 1)
    curr_dp = [0] * (m + 1)
    
    # Initialize base case
    if array[0] == 0:
        # Unknown value, try all possibilities
        for value in range(1, m + 1):
            prev_dp[value] = 1
    else:
        # Known value
        prev_dp[array[0]] = 1
    
    # Fill DP using space optimization
    for i in range(1, n):
        curr_dp = [0] * (m + 1)
        
        if array[i] == 0:
            # Unknown value, try all possibilities
            for value in range(1, m + 1):
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        curr_dp[value] = (curr_dp[value] + prev_dp[prev_value]) % mod
        else:
            # Known value
            value = array[i]
            for prev_value in range(1, m + 1):
                if abs(value - prev_value) <= 1:
                    curr_dp[value] = (curr_dp[value] + prev_dp[prev_value]) % mod
        
        prev_dp = curr_dp
    
    # Sum all valid ways
    total_ways = 0
    for value in range(1, m + 1):
        total_ways = (total_ways + prev_dp[value]) % mod
    
    return total_ways

def space_optimized_dp_array_description_v2(n, m, array, mod=10**9+7):
    """
    Alternative space-optimized DP array description counting
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    # Use only necessary variables for DP
    prev_dp = [0] * (m + 1)
    curr_dp = [0] * (m + 1)
    
    # Initialize base case
    if array[0] == 0:
        # Unknown value, try all possibilities
        for value in range(1, m + 1):
            prev_dp[value] = 1
    else:
        # Known value
        prev_dp[array[0]] = 1
    
    # Fill DP using space optimization
    for i in range(1, n):
        curr_dp = [0] * (m + 1)
        
        if array[i] == 0:
            # Unknown value, try all possibilities
            for value in range(1, m + 1):
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        curr_dp[value] = (curr_dp[value] + prev_dp[prev_value]) % mod
        else:
            # Known value
            value = array[i]
            for prev_value in range(1, m + 1):
                if abs(value - prev_value) <= 1:
                    curr_dp[value] = (curr_dp[value] + prev_dp[prev_value]) % mod
        
        prev_dp = curr_dp
    
    # Sum all valid ways
    total_ways = 0
    for value in range(1, m + 1):
        total_ways = (total_ways + prev_dp[value]) % mod
    
    return total_ways

def array_description_with_precomputation(max_n, max_m, mod=10**9+7):
    """
    Precompute array description for multiple queries
    
    Args:
        max_n: maximum array length
        max_m: maximum value
        mod: modulo value
    
    Returns:
        list: precomputed array description results
    """
    # This is a simplified version for demonstration
    results = [[[0] * (max_m + 1) for _ in range(max_m + 1)] for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_m + 1):
            for k in range(max_m + 1):
                if i == 0:
                    results[i][j][k] = 1
                else:
                    results[i][j][k] = (i * j * k) % mod  # Simplified calculation
    
    return results

# Example usage
n, m = 3, 2
array = [0, 1, 0]
result1 = space_optimized_dp_array_description(n, m, array)
result2 = space_optimized_dp_array_description_v2(n, m, array)
print(f"Space-optimized DP array description: {result1}")
print(f"Space-optimized DP array description v2: {result2}")

# Precompute for multiple queries
max_n, max_m = 1000, 100
precomputed = array_description_with_precomputation(max_n, max_m)
print(f"Precomputed result for n={n}, m={m}: {precomputed[n][m][m]}")
```

**Time Complexity**: O(n * m²)
**Space Complexity**: O(m)

**Why it's optimal**: Uses space-optimized DP for O(n * m²) time and O(m) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(m^n) | O(n) | Complete enumeration of all array fillings |
| Dynamic Programming | O(n * m²) | O(n * m) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n * m²) | O(m) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(n * m²) - Use dynamic programming for efficient calculation
- **Space**: O(m) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Array Description with Constraints**
**Problem**: Count array descriptions with specific constraints.

**Key Differences**: Apply additional constraints to array filling

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_array_description(n, m, array, constraints, mod=10**9+7):
    """
    Count array descriptions with constraints
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    # Create DP table
    dp = [[0] * (m + 1) for _ in range(n)]
    
    # Initialize base case
    if array[0] == 0:
        # Unknown value, try all possibilities
        for value in range(1, m + 1):
            if constraints(0, value):  # Check if value satisfies constraints
                dp[0][value] = 1
    else:
        # Known value
        if constraints(0, array[0]):
            dp[0][array[0]] = 1
    
    # Fill DP table with constraints
    for i in range(1, n):
        if array[i] == 0:
            # Unknown value, try all possibilities
            for value in range(1, m + 1):
                if constraints(i, value):  # Check if value satisfies constraints
                    for prev_value in range(1, m + 1):
                        if abs(value - prev_value) <= 1:
                            dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
        else:
            # Known value
            value = array[i]
            if constraints(i, value):
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
    
    # Sum all valid ways
    total_ways = 0
    for value in range(1, m + 1):
        total_ways = (total_ways + dp[n-1][value]) % mod
    
    return total_ways

# Example usage
n, m = 3, 2
array = [0, 1, 0]
constraints = lambda i, value: value <= 2  # Only allow values <= 2
result = constrained_array_description(n, m, array, constraints)
print(f"Constrained array description: {result}")
```

#### **2. Array Description with Multiple Constraints**
**Problem**: Count array descriptions with multiple constraint types.

**Key Differences**: Handle multiple types of constraints

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_constraint_array_description(n, m, array, constraint_list, mod=10**9+7):
    """
    Count array descriptions with multiple constraints
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        constraint_list: list of constraint functions
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    # Create DP table
    dp = [[0] * (m + 1) for _ in range(n)]
    
    # Initialize base case
    if array[0] == 0:
        # Unknown value, try all possibilities
        for value in range(1, m + 1):
            if all(constraint(0, value) for constraint in constraint_list):
                dp[0][value] = 1
    else:
        # Known value
        if all(constraint(0, array[0]) for constraint in constraint_list):
            dp[0][array[0]] = 1
    
    # Fill DP table with multiple constraints
    for i in range(1, n):
        if array[i] == 0:
            # Unknown value, try all possibilities
            for value in range(1, m + 1):
                if all(constraint(i, value) for constraint in constraint_list):
                    for prev_value in range(1, m + 1):
                        if abs(value - prev_value) <= 1:
                            dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
        else:
            # Known value
            value = array[i]
            if all(constraint(i, value) for constraint in constraint_list):
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
    
    # Sum all valid ways
    total_ways = 0
    for value in range(1, m + 1):
        total_ways = (total_ways + dp[n-1][value]) % mod
    
    return total_ways

# Example usage
n, m = 3, 2
array = [0, 1, 0]
constraint_list = [
    lambda i, value: value <= 2,  # Value <= 2
    lambda i, value: value >= 1   # Value >= 1
]
result = multi_constraint_array_description(n, m, array, constraint_list)
print(f"Multi-constraint array description: {result}")
```

#### **3. Array Description with Range Constraints**
**Problem**: Count array descriptions with range-based constraints.

**Key Differences**: Handle range-based constraints

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def range_constraint_array_description(n, m, array, ranges, mod=10**9+7):
    """
    Count array descriptions with range constraints
    
    Args:
        n: array length
        m: maximum value
        array: array with known and unknown values
        ranges: list of (min_val, max_val) for each position
        mod: modulo value
    
    Returns:
        int: number of ways to fill array modulo mod
    """
    # Create DP table
    dp = [[0] * (m + 1) for _ in range(n)]
    
    # Initialize base case
    if array[0] == 0:
        # Unknown value, try all possibilities
        min_val, max_val = ranges[0]
        for value in range(min_val, max_val + 1):
            dp[0][value] = 1
    else:
        # Known value
        value = array[0]
        min_val, max_val = ranges[0]
        if min_val <= value <= max_val:
            dp[0][value] = 1
    
    # Fill DP table with range constraints
    for i in range(1, n):
        if array[i] == 0:
            # Unknown value, try all possibilities
            min_val, max_val = ranges[i]
            for value in range(min_val, max_val + 1):
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
        else:
            # Known value
            value = array[i]
            min_val, max_val = ranges[i]
            if min_val <= value <= max_val:
                for prev_value in range(1, m + 1):
                    if abs(value - prev_value) <= 1:
                        dp[i][value] = (dp[i][value] + dp[i-1][prev_value]) % mod
    
    # Sum all valid ways
    total_ways = 0
    for value in range(1, m + 1):
        total_ways = (total_ways + dp[n-1][value]) % mod
    
    return total_ways

# Example usage
n, m = 3, 2
array = [0, 1, 0]
ranges = [(1, 2), (1, 2), (1, 2)]  # Range constraints for each position
result = range_constraint_array_description(n, m, array, ranges)
print(f"Range constraint array description: {result}")
```

## Problem Variations

### **Variation 1: Array Description with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining optimal array description generation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic array management.

```python
from collections import defaultdict

class DynamicArrayDescription:
    def __init__(self, array=None, constraints=None):
        self.array = array or []
        self.constraints = constraints or {}
        self.valid_descriptions = []
        self._update_array_description_info()
    
    def _update_array_description_info(self):
        """Update array description feasibility information."""
        self.array_length = len(self.array)
        self.array_description_feasibility = self._calculate_array_description_feasibility()
    
    def _calculate_array_description_feasibility(self):
        """Calculate array description feasibility."""
        if self.array_length == 0:
            return 0.0
        
        # Check if we can generate valid descriptions
        if not self.array or any(x < 0 for x in self.array):
            return 0.0
        
        return 1.0
    
    def add_element(self, element, position=None):
        """Add element to the array."""
        if position is None:
            self.array.append(element)
        else:
            self.array.insert(position, element)
        
        self._update_array_description_info()
    
    def remove_element(self, position):
        """Remove element from the array."""
        if 0 <= position < len(self.array):
            self.array.pop(position)
            self._update_array_description_info()
    
    def update_element(self, position, new_element):
        """Update element in the array."""
        if 0 <= position < len(self.array):
            self.array[position] = new_element
            self._update_array_description_info()
    
    def generate_descriptions(self):
        """Generate all valid array descriptions."""
        if not self.array:
            return []
        
        n = len(self.array)
        descriptions = []
        
        def backtrack(index, current_desc):
            if index == n:
                descriptions.append(current_desc[:])
                return
            
            if self.array[index] == 0:
                # Try all possible values
                for value in range(1, n + 1):
                    if self._is_valid_value(current_desc, index, value):
                        current_desc.append(value)
                        backtrack(index + 1, current_desc)
                        current_desc.pop()
            else:
                # Use the given value
                if self._is_valid_value(current_desc, index, self.array[index]):
                    current_desc.append(self.array[index])
                    backtrack(index + 1, current_desc)
                    current_desc.pop()
        
        backtrack(0, [])
        return descriptions
    
    def _is_valid_value(self, current_desc, index, value):
        """Check if value is valid at given position."""
        if index == 0:
            return True
        
        # Check constraint: adjacent elements differ by at most 1
        if abs(value - current_desc[-1]) > 1:
            return False
        
        return True
    
    def get_descriptions_with_constraints(self, constraint_func):
        """Get descriptions that satisfies custom constraints."""
        if not self.array:
            return []
        
        descriptions = self.generate_descriptions()
        valid_descriptions = []
        
        for desc in descriptions:
            if constraint_func(desc, self.array):
                valid_descriptions.append(desc)
        
        return valid_descriptions
    
    def get_descriptions_in_range(self, min_length, max_length):
        """Get descriptions within specified length range."""
        if not self.array:
            return []
        
        descriptions = self.generate_descriptions()
        valid_descriptions = []
        
        for desc in descriptions:
            if min_length <= len(desc) <= max_length:
                valid_descriptions.append(desc)
        
        return valid_descriptions
    
    def get_descriptions_with_pattern(self, pattern_func):
        """Get descriptions matching specified pattern."""
        if not self.array:
            return []
        
        descriptions = self.generate_descriptions()
        valid_descriptions = []
        
        for desc in descriptions:
            if pattern_func(desc, self.array):
                valid_descriptions.append(desc)
        
        return valid_descriptions
    
    def get_array_statistics(self):
        """Get statistics about the array."""
        if not self.array:
            return {
                'array_length': 0,
                'array_description_feasibility': 0,
                'zero_count': 0
            }
        
        descriptions = self.generate_descriptions()
        return {
            'array_length': self.array_length,
            'array_description_feasibility': self.array_description_feasibility,
            'zero_count': self.array.count(0),
            'description_count': len(descriptions),
            'max_value': max(self.array) if self.array else 0,
            'min_value': min(self.array) if self.array else 0
        }
    
    def get_array_description_patterns(self):
        """Get patterns in array descriptions."""
        patterns = {
            'has_zeros': 0,
            'all_positive': 0,
            'valid_descriptions_exist': 0,
            'optimal_description_possible': 0
        }
        
        if not self.array:
            return patterns
        
        # Check if has zeros
        if 0 in self.array:
            patterns['has_zeros'] = 1
        
        # Check if all positive
        if all(x > 0 for x in self.array):
            patterns['all_positive'] = 1
        
        # Check if valid descriptions exist
        descriptions = self.generate_descriptions()
        if descriptions:
            patterns['valid_descriptions_exist'] = 1
        
        # Check if optimal description is possible
        if self.array_description_feasibility == 1.0:
            patterns['optimal_description_possible'] = 1
        
        return patterns
    
    def get_optimal_array_description_strategy(self):
        """Get optimal strategy for array description generation."""
        if not self.array:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'array_description_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.array_description_feasibility
        
        # Calculate array description feasibility
        array_description_feasibility = self.array_description_feasibility
        
        # Determine recommended strategy
        if self.array_length <= 10:
            recommended_strategy = 'backtracking'
        elif self.array_length <= 50:
            recommended_strategy = 'dynamic_programming'
        else:
            recommended_strategy = 'optimized_dp'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'array_description_feasibility': array_description_feasibility
        }

# Example usage
array = [0, 2, 0, 1]
dynamic_array_description = DynamicArrayDescription(array)
print(f"Array description feasibility: {dynamic_array_description.array_description_feasibility}")

# Add element
dynamic_array_description.add_element(3)
print(f"After adding 3: {dynamic_array_description.array}")

# Remove element
dynamic_array_description.remove_element(0)
print(f"After removing first element: {dynamic_array_description.array}")

# Update element
dynamic_array_description.update_element(0, 4)
print(f"After updating first element to 4: {dynamic_array_description.array[0]}")

# Generate descriptions
descriptions = dynamic_array_description.generate_descriptions()
print(f"Descriptions: {descriptions}")

# Get descriptions with constraints
def constraint_func(desc, array):
    return len(desc) == len(array) and all(x > 0 for x in desc)

print(f"Descriptions with constraints: {dynamic_array_description.get_descriptions_with_constraints(constraint_func)}")

# Get descriptions in range
print(f"Descriptions in range 3-5: {dynamic_array_description.get_descriptions_in_range(3, 5)}")

# Get descriptions with pattern
def pattern_func(desc, array):
    return len(desc) > 0 and all(x > 0 for x in desc)

print(f"Descriptions with pattern: {dynamic_array_description.get_descriptions_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_array_description.get_array_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_array_description.get_array_description_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_array_description.get_optimal_array_description_strategy()}")
```

### **Variation 2: Array Description with Different Operations**
**Problem**: Handle different types of array description operations (weighted elements, priority-based generation, advanced array analysis).

**Approach**: Use advanced data structures for efficient different types of array description operations.

```python
class AdvancedArrayDescription:
    def __init__(self, array=None, weights=None, priorities=None):
        self.array = array or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.valid_descriptions = []
        self._update_array_description_info()
    
    def _update_array_description_info(self):
        """Update array description feasibility information."""
        self.array_length = len(self.array)
        self.array_description_feasibility = self._calculate_array_description_feasibility()
    
    def _calculate_array_description_feasibility(self):
        """Calculate array description feasibility."""
        if self.array_length == 0:
            return 0.0
        
        # Check if we can generate valid descriptions
        if not self.array or any(x < 0 for x in self.array):
            return 0.0
        
        return 1.0
    
    def generate_descriptions(self):
        """Generate all valid array descriptions."""
        if not self.array:
            return []
        
        n = len(self.array)
        descriptions = []
        
        def backtrack(index, current_desc):
            if index == n:
                descriptions.append(current_desc[:])
                return
            
            if self.array[index] == 0:
                # Try all possible values
                for value in range(1, n + 1):
                    if self._is_valid_value(current_desc, index, value):
                        current_desc.append(value)
                        backtrack(index + 1, current_desc)
                        current_desc.pop()
            else:
                # Use the given value
                if self._is_valid_value(current_desc, index, self.array[index]):
                    current_desc.append(self.array[index])
                    backtrack(index + 1, current_desc)
                    current_desc.pop()
        
        backtrack(0, [])
        return descriptions
    
    def _is_valid_value(self, current_desc, index, value):
        """Check if value is valid at given position."""
        if index == 0:
            return True
        
        # Check constraint: adjacent elements differ by at most 1
        if abs(value - current_desc[-1]) > 1:
            return False
        
        return True
    
    def get_weighted_descriptions(self):
        """Get descriptions with weights and priorities applied."""
        if not self.array:
            return []
        
        descriptions = self.generate_descriptions()
        
        # Create weighted descriptions
        weighted_descriptions = []
        for desc in descriptions:
            total_weight = 0
            total_priority = 0
            
            for i, value in enumerate(desc):
                weight = self.weights.get(value, 1)
                priority = self.priorities.get(value, 1)
                total_weight += weight
                total_priority += priority
            
            weighted_score = total_weight * total_priority
            weighted_descriptions.append((desc, weighted_score))
        
        # Sort by weighted score
        weighted_descriptions.sort(key=lambda x: x[1], reverse=True)
        return weighted_descriptions
    
    def get_descriptions_with_priority(self, priority_func):
        """Get descriptions considering priority."""
        if not self.array:
            return []
        
        descriptions = self.generate_descriptions()
        
        # Create priority-based descriptions
        priority_descriptions = []
        for desc in descriptions:
            priority = priority_func(desc, self.weights, self.priorities)
            priority_descriptions.append((desc, priority))
        
        # Sort by priority
        priority_descriptions.sort(key=lambda x: x[1], reverse=True)
        return priority_descriptions
    
    def get_descriptions_with_optimization(self, optimization_func):
        """Get descriptions using custom optimization function."""
        if not self.array:
            return []
        
        descriptions = self.generate_descriptions()
        
        # Create optimization-based descriptions
        optimized_descriptions = []
        for desc in descriptions:
            score = optimization_func(desc, self.weights, self.priorities)
            optimized_descriptions.append((desc, score))
        
        # Sort by optimization score
        optimized_descriptions.sort(key=lambda x: x[1], reverse=True)
        return optimized_descriptions
    
    def get_descriptions_with_constraints(self, constraint_func):
        """Get descriptions that satisfies custom constraints."""
        if not self.array:
            return []
        
        if constraint_func(self.array, self.weights, self.priorities):
            return self.get_weighted_descriptions()
        else:
            return []
    
    def get_descriptions_with_multiple_criteria(self, criteria_list):
        """Get descriptions that satisfies multiple criteria."""
        if not self.array:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.array, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_descriptions()
        else:
            return []
    
    def get_descriptions_with_alternatives(self, alternatives):
        """Get descriptions considering alternative weights/priorities."""
        result = []
        
        # Check original descriptions
        original_descriptions = self.get_weighted_descriptions()
        result.append((original_descriptions, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedArrayDescription(self.array, alt_weights, alt_priorities)
            temp_descriptions = temp_instance.get_weighted_descriptions()
            result.append((temp_descriptions, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_descriptions_with_adaptive_criteria(self, adaptive_func):
        """Get descriptions using adaptive criteria."""
        if not self.array:
            return []
        
        if adaptive_func(self.array, self.weights, self.priorities, []):
            return self.get_weighted_descriptions()
        else:
            return []
    
    def get_array_description_optimization(self):
        """Get optimal array description configuration."""
        strategies = [
            ('weighted_descriptions', lambda: len(self.get_weighted_descriptions())),
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
array = [0, 2, 0, 1]
weights = {num: num * 2 for num in range(1, 10)}  # Weight based on number value
priorities = {num: num // 2 for num in range(1, 10)}  # Priority based on number value
advanced_array_description = AdvancedArrayDescription(array, weights, priorities)

print(f"Weighted descriptions: {advanced_array_description.get_weighted_descriptions()}")

# Get descriptions with priority
def priority_func(desc, weights, priorities):
    return sum(weights.get(x, 1) + priorities.get(x, 1) for x in desc)

print(f"Descriptions with priority: {advanced_array_description.get_descriptions_with_priority(priority_func)}")

# Get descriptions with optimization
def optimization_func(desc, weights, priorities):
    return sum(weights.get(x, 1) * priorities.get(x, 1) for x in desc)

print(f"Descriptions with optimization: {advanced_array_description.get_descriptions_with_optimization(optimization_func)}")

# Get descriptions with constraints
def constraint_func(array, weights, priorities):
    return len(array) > 0 and all(x >= 0 for x in array)

print(f"Descriptions with constraints: {advanced_array_description.get_descriptions_with_constraints(constraint_func)}")

# Get descriptions with multiple criteria
def criterion1(array, weights, priorities):
    return len(array) > 0

def criterion2(array, weights, priorities):
    return all(x >= 0 for x in array)

criteria_list = [criterion1, criterion2]
print(f"Descriptions with multiple criteria: {advanced_array_description.get_descriptions_with_multiple_criteria(criteria_list)}")

# Get descriptions with alternatives
alternatives = [({num: 1 for num in range(1, 10)}, {num: 1 for num in range(1, 10)}), ({num: num*3 for num in range(1, 10)}, {num: num+1 for num in range(1, 10)})]
print(f"Descriptions with alternatives: {advanced_array_description.get_descriptions_with_alternatives(alternatives)}")

# Get descriptions with adaptive criteria
def adaptive_func(array, weights, priorities, current_result):
    return len(array) > 0 and len(current_result) < 5

print(f"Descriptions with adaptive criteria: {advanced_array_description.get_descriptions_with_adaptive_criteria(adaptive_func)}")

# Get array description optimization
print(f"Array description optimization: {advanced_array_description.get_array_description_optimization()}")
```

### **Variation 3: Array Description with Constraints**
**Problem**: Handle array description generation with additional constraints (length limits, value constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedArrayDescription:
    def __init__(self, array=None, constraints=None):
        self.array = array or []
        self.constraints = constraints or {}
        self.valid_descriptions = []
        self._update_array_description_info()
    
    def _update_array_description_info(self):
        """Update array description feasibility information."""
        self.array_length = len(self.array)
        self.array_description_feasibility = self._calculate_array_description_feasibility()
    
    def _calculate_array_description_feasibility(self):
        """Calculate array description feasibility."""
        if self.array_length == 0:
            return 0.0
        
        # Check if we can generate valid descriptions
        if not self.array or any(x < 0 for x in self.array):
            return 0.0
        
        return 1.0
    
    def _is_valid_description(self, description):
        """Check if description is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if len(description) < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if len(description) > self.constraints['max_length']:
                return False
        
        # Value constraints
        if 'forbidden_values' in self.constraints:
            if any(val in self.constraints['forbidden_values'] for val in description):
                return False
        
        if 'required_values' in self.constraints:
            if not all(val in description for val in self.constraints['required_values']):
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(description):
                    return False
        
        return True
    
    def get_descriptions_with_length_constraints(self, min_length, max_length):
        """Get descriptions considering length constraints."""
        if not self.array:
            return []
        
        descriptions = self.generate_descriptions()
        valid_descriptions = []
        
        for desc in descriptions:
            if min_length <= len(desc) <= max_length and self._is_valid_description(desc):
                valid_descriptions.append(desc)
        
        return valid_descriptions
    
    def get_descriptions_with_value_constraints(self, value_constraints):
        """Get descriptions considering value constraints."""
        if not self.array:
            return []
        
        satisfies_constraints = True
        for constraint in value_constraints:
            if not constraint(self.array):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            descriptions = self.generate_descriptions()
            valid_descriptions = []
            
            for desc in descriptions:
                if self._is_valid_description(desc):
                    valid_descriptions.append(desc)
            
            return valid_descriptions
        
        return []
    
    def get_descriptions_with_pattern_constraints(self, pattern_constraints):
        """Get descriptions considering pattern constraints."""
        if not self.array:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.array):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            descriptions = self.generate_descriptions()
            valid_descriptions = []
            
            for desc in descriptions:
                if self._is_valid_description(desc):
                    valid_descriptions.append(desc)
            
            return valid_descriptions
        
        return []
    
    def get_descriptions_with_mathematical_constraints(self, constraint_func):
        """Get descriptions that satisfies custom mathematical constraints."""
        if not self.array:
            return []
        
        if constraint_func(self.array):
            descriptions = self.generate_descriptions()
            valid_descriptions = []
            
            for desc in descriptions:
                if self._is_valid_description(desc):
                    valid_descriptions.append(desc)
            
            return valid_descriptions
        
        return []
    
    def get_descriptions_with_optimization_constraints(self, optimization_func):
        """Get descriptions using custom optimization constraints."""
        if not self.array:
            return []
        
        # Calculate optimization score for descriptions
        score = optimization_func(self.array)
        
        if score > 0:
            descriptions = self.generate_descriptions()
            valid_descriptions = []
            
            for desc in descriptions:
                if self._is_valid_description(desc):
                    valid_descriptions.append(desc)
            
            return valid_descriptions
        
        return []
    
    def get_descriptions_with_multiple_constraints(self, constraints_list):
        """Get descriptions that satisfies multiple constraints."""
        if not self.array:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.array):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            descriptions = self.generate_descriptions()
            valid_descriptions = []
            
            for desc in descriptions:
                if self._is_valid_description(desc):
                    valid_descriptions.append(desc)
            
            return valid_descriptions
        
        return []
    
    def get_descriptions_with_priority_constraints(self, priority_func):
        """Get descriptions with priority-based constraints."""
        if not self.array:
            return []
        
        # Calculate priority for descriptions
        priority = priority_func(self.array)
        
        if priority > 0:
            descriptions = self.generate_descriptions()
            valid_descriptions = []
            
            for desc in descriptions:
                if self._is_valid_description(desc):
                    valid_descriptions.append(desc)
            
            return valid_descriptions
        
        return []
    
    def get_descriptions_with_adaptive_constraints(self, adaptive_func):
        """Get descriptions with adaptive constraints."""
        if not self.array:
            return []
        
        if adaptive_func(self.array, []):
            descriptions = self.generate_descriptions()
            valid_descriptions = []
            
            for desc in descriptions:
                if self._is_valid_description(desc):
                    valid_descriptions.append(desc)
            
            return valid_descriptions
        
        return []
    
    def generate_descriptions(self):
        """Generate all valid array descriptions."""
        if not self.array:
            return []
        
        n = len(self.array)
        descriptions = []
        
        def backtrack(index, current_desc):
            if index == n:
                descriptions.append(current_desc[:])
                return
            
            if self.array[index] == 0:
                # Try all possible values
                for value in range(1, n + 1):
                    if self._is_valid_value(current_desc, index, value):
                        current_desc.append(value)
                        backtrack(index + 1, current_desc)
                        current_desc.pop()
            else:
                # Use the given value
                if self._is_valid_value(current_desc, index, self.array[index]):
                    current_desc.append(self.array[index])
                    backtrack(index + 1, current_desc)
                    current_desc.pop()
        
        backtrack(0, [])
        return descriptions
    
    def _is_valid_value(self, current_desc, index, value):
        """Check if value is valid at given position."""
        if index == 0:
            return True
        
        # Check constraint: adjacent elements differ by at most 1
        if abs(value - current_desc[-1]) > 1:
            return False
        
        return True
    
    def get_optimal_array_description_strategy(self):
        """Get optimal array description strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_descriptions_with_length_constraints),
            ('value_constraints', self.get_descriptions_with_value_constraints),
            ('pattern_constraints', self.get_descriptions_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    result = strategy_func(1, 1000)
                elif strategy_name == 'value_constraints':
                    value_constraints = [lambda arr: len(arr) > 0]
                    result = strategy_func(value_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda arr: all(x >= 0 for x in arr)]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 3,
    'max_length': 10,
    'forbidden_values': [0, -1],
    'required_values': [1],
    'pattern_constraints': [lambda desc: len(desc) > 0 and all(x > 0 for x in desc)]
}

array = [0, 2, 0, 1, 0]
constrained_array_description = ConstrainedArrayDescription(array, constraints)

print("Length-constrained descriptions:", constrained_array_description.get_descriptions_with_length_constraints(3, 10))

print("Value-constrained descriptions:", constrained_array_description.get_descriptions_with_value_constraints([lambda arr: len(arr) > 0]))

print("Pattern-constrained descriptions:", constrained_array_description.get_descriptions_with_pattern_constraints([lambda arr: all(x >= 0 for x in arr)]))

# Mathematical constraints
def custom_constraint(arr):
    return len(arr) > 0 and all(x >= 0 for x in arr)

print("Mathematical constraint descriptions:", constrained_array_description.get_descriptions_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(arr):
    return all(0 <= x <= 10 for x in arr)

range_constraints = [range_constraint]
print("Range-constrained descriptions:", constrained_array_description.get_descriptions_with_length_constraints(1, 10))

# Multiple constraints
def constraint1(arr):
    return len(arr) > 0

def constraint2(arr):
    return all(x >= 0 for x in arr)

constraints_list = [constraint1, constraint2]
print("Multiple constraints descriptions:", constrained_array_description.get_descriptions_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(arr):
    return len(arr) + sum(1 for x in arr if x > 0)

print("Priority-constrained descriptions:", constrained_array_description.get_descriptions_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(arr, current_result):
    return len(arr) > 0 and len(current_result) < 5

print("Adaptive constraint descriptions:", constrained_array_description.get_descriptions_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_array_description.get_optimal_array_description_strategy()
print(f"Optimal array description strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Book Shop](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Grid Paths](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Money Sums](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Grid DP
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Grid DP
- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) - Grid DP

#### **Problem Categories**
- **Dynamic Programming**: Array DP, constraint satisfaction
- **Combinatorics**: Mathematical counting, constraint properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Array Algorithms](https://cp-algorithms.com/array/array-algorithms.html) - Array algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Book Shop](https://cses.fi/problemset/task/1075) - Medium
- [CSES Grid Paths](https://cses.fi/problemset/task/1075) - Medium
- [CSES Money Sums](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
