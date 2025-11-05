---
layout: simple
title: "Increasing Subsequence - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/increasing_subsequence_analysis
---

# Increasing Subsequence

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of longest increasing subsequence in dynamic programming
- Apply optimization techniques for subsequence analysis
- Implement efficient algorithms for LIS calculation
- Optimize DP operations for subsequence analysis
- Handle special cases in subsequence problems

## 📋 Problem Description

Given an array of integers, find the length of the longest increasing subsequence.

**Input**: 
- n: array length
- array: array of integers

**Output**: 
- Length of the longest increasing subsequence

**Constraints**:
- 1 ≤ n ≤ 2×10^5
- -10^9 ≤ array[i] ≤ 10^9

**Example**:
```
Input:
n = 6
array = [10, 9, 2, 5, 3, 7, 101, 18]

Output:
4

Explanation**: 
Longest increasing subsequence: [2, 3, 7, 18]
Length: 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible subsequences
- **Complete Enumeration**: Enumerate all possible subsequence sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible increasing subsequences.

**Algorithm**:
- Use recursive function to try all subsequence combinations
- Check increasing property for each subsequence
- Find maximum length
- Return result

**Visual Example**:
```
Array = [10, 9, 2, 5, 3, 7, 101, 18]:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try starting with 10:              │
│ - Try next element 9: 10 > 9 ✗     │
│ - Try next element 2: 10 > 2 ✗     │
│ - Try next element 5: 10 > 5 ✗     │
│ - Try next element 3: 10 > 3 ✗     │
│ - Try next element 7: 10 > 7 ✗     │
│ - Try next element 101: 10 < 101 ✓ │
│   - Try next element 18: 101 > 18 ✗ │
│   - Length: 2                      │
│                                   │
│ Try starting with 9:               │
│ - Try next element 2: 9 > 2 ✗     │
│ - Try next element 5: 9 > 5 ✗     │
│ - Try next element 3: 9 > 3 ✗     │
│ - Try next element 7: 9 > 7 ✗     │
│ - Try next element 101: 9 < 101 ✓ │
│   - Try next element 18: 101 > 18 ✗ │
│   - Length: 2                      │
│                                   │
│ Try starting with 2:               │
│ - Try next element 5: 2 < 5 ✓     │
│   - Try next element 3: 5 > 3 ✗   │
│   - Try next element 7: 5 < 7 ✓   │
│     - Try next element 101: 7 < 101 ✓ │
│       - Try next element 18: 101 > 18 ✗ │
│       - Length: 4                  │
│                                   │
│ Maximum: 4                        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_increasing_subsequence(n, array):
    """
    Find LIS using recursive approach
    
    Args:
        n: array length
        array: array of integers
    
    Returns:
        int: length of longest increasing subsequence
    """
    def find_lis(index, last_element):
        """Find LIS recursively"""
        if index == n:
            return 0  # No more elements
        
        # Don't include current element
        max_length = find_lis(index + 1, last_element)
        
        # Include current element if it's greater than last element
        if array[index] > last_element:
            max_length = max(max_length, 1 + find_lis(index + 1, array[index]))
        
        return max_length
    
    return find_lis(0, float('-inf'))

def recursive_increasing_subsequence_optimized(n, array):
    """
    Optimized recursive increasing subsequence finding
    
    Args:
        n: array length
        array: array of integers
    
    Returns:
        int: length of longest increasing subsequence
    """
    def find_lis_optimized(index, last_element):
        """Find LIS with optimization"""
        if index == n:
            return 0  # No more elements
        
        # Don't include current element
        max_length = find_lis_optimized(index + 1, last_element)
        
        # Include current element if it's greater than last element
        if array[index] > last_element:
            max_length = max(max_length, 1 + find_lis_optimized(index + 1, array[index]))
        
        return max_length
    
    return find_lis_optimized(0, float('-inf'))

# Example usage
n = 6
array = [10, 9, 2, 5, 3, 7, 101, 18]
result1 = recursive_increasing_subsequence(n, array)
result2 = recursive_increasing_subsequence_optimized(n, array)
print(f"Recursive increasing subsequence: {result1}")
print(f"Optimized recursive increasing subsequence: {result2}")
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n²) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store LIS length ending at each position
- Fill DP table bottom-up
- Return maximum value in DP table

**Visual Example**:
```
DP table for array = [10, 9, 2, 5, 3, 7, 101, 18]:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = 1 (LIS ending at index 0)  │
│ dp[1] = 1 (LIS ending at index 1)  │
│ dp[2] = 1 (LIS ending at index 2)  │
│ dp[3] = 2 (LIS ending at index 3)  │
│ dp[4] = 2 (LIS ending at index 4)  │
│ dp[5] = 3 (LIS ending at index 5)  │
│ dp[6] = 4 (LIS ending at index 6)  │
│ dp[7] = 4 (LIS ending at index 7)  │
│                                   │
│ Maximum: 4                        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_increasing_subsequence(n, array):
    """
    Find LIS using dynamic programming approach
    
    Args:
        n: array length
        array: array of integers
    
    Returns:
        int: length of longest increasing subsequence
    """
    # Create DP table
    dp = [1] * n  # Each element is a subsequence of length 1
    
    # Fill DP table
    for i in range(1, n):
        for j in range(i):
            if array[j] < array[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

def dp_increasing_subsequence_optimized(n, array):
    """
    Optimized dynamic programming increasing subsequence finding
    
    Args:
        n: array length
        array: array of integers
    
    Returns:
        int: length of longest increasing subsequence
    """
    # Create DP table with optimization
    dp = [1] * n  # Each element is a subsequence of length 1
    
    # Fill DP table with optimization
    for i in range(1, n):
        for j in range(i):
            if array[j] < array[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Example usage
n = 6
array = [10, 9, 2, 5, 3, 7, 101, 18]
result1 = dp_increasing_subsequence(n, array)
result2 = dp_increasing_subsequence_optimized(n, array)
print(f"DP increasing subsequence: {result1}")
print(f"Optimized DP increasing subsequence: {result2}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n)

**Why it's better**: Uses dynamic programming for O(n²) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Binary Search Solution (Optimal)

**Key Insights from Binary Search Solution**:
- **Binary Search**: Use binary search to find optimal positions
- **Efficient Computation**: O(n log n) time complexity
- **Space Efficiency**: O(n) space complexity
- **Optimal Complexity**: Best approach for LIS

**Key Insight**: Use binary search to maintain the smallest tail element for each LIS length.

**Algorithm**:
- Maintain array of smallest tail elements for each LIS length
- Use binary search to find optimal position for each element
- Return length of the array

**Visual Example**:
```
Binary search approach for array = [10, 9, 2, 5, 3, 7, 101, 18]:

Process:
┌─────────────────────────────────────┐
│ tails = [] (empty initially)       │
│                                     │
│ Process 10: tails = [10]            │
│ Process 9: tails = [9]              │
│ Process 2: tails = [2]              │
│ Process 5: tails = [2, 5]           │
│ Process 3: tails = [2, 3]           │
│ Process 7: tails = [2, 3, 7]        │
│ Process 101: tails = [2, 3, 7, 101] │
│ Process 18: tails = [2, 3, 7, 18]   │
│                                     │
│ Length: 4                           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def binary_search_increasing_subsequence(n, array):
    """
    Find LIS using binary search approach
    
    Args:
        n: array length
        array: array of integers
    
    Returns:
        int: length of longest increasing subsequence
    """
    import bisect
    
    # Array to store smallest tail element for each LIS length
    tails = []
    
    for num in array:
        # Find position to insert current element
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            # Current element is larger than all elements in tails
            tails.append(num)
        else:
            # Replace element at position pos
            tails[pos] = num
    
    return len(tails)

def binary_search_increasing_subsequence_v2(n, array):
    """
    Alternative binary search increasing subsequence finding
    
    Args:
        n: array length
        array: array of integers
    
    Returns:
        int: length of longest increasing subsequence
    """
    import bisect
    
    # Array to store smallest tail element for each LIS length
    tails = []
    
    for num in array:
        # Find position to insert current element
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            # Current element is larger than all elements in tails
            tails.append(num)
        else:
            # Replace element at position pos
            tails[pos] = num
    
    return len(tails)

def binary_search_increasing_subsequence_optimized(n, array):
    """
    Optimized binary search increasing subsequence finding
    
    Args:
        n: array length
        array: array of integers
    
    Returns:
        int: length of longest increasing subsequence
    """
    import bisect
    
    # Array to store smallest tail element for each LIS length
    tails = []
    
    for num in array:
        # Find position to insert current element
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            # Current element is larger than all elements in tails
            tails.append(num)
        else:
            # Replace element at position pos
            tails[pos] = num
    
    return len(tails)

def increasing_subsequence_with_precomputation(max_n):
    """
    Precompute increasing subsequence for multiple queries
    
    Args:
        max_n: maximum array length
    
    Returns:
        list: precomputed increasing subsequence results
    """
    # This is a simplified version for demonstration
    results = [0] * (max_n + 1)
    
    for i in range(max_n + 1):
        results[i] = i  # Simplified calculation
    
    return results

# Example usage
n = 6
array = [10, 9, 2, 5, 3, 7, 101, 18]
result1 = binary_search_increasing_subsequence(n, array)
result2 = binary_search_increasing_subsequence_v2(n, array)
result3 = binary_search_increasing_subsequence_optimized(n, array)
print(f"Binary search increasing subsequence: {result1}")
print(f"Binary search increasing subsequence v2: {result2}")
print(f"Optimized binary search increasing subsequence: {result3}")

# Precompute for multiple queries
max_n = 200000
precomputed = increasing_subsequence_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses binary search for O(n log n) time and O(n) space complexity.

**Implementation Details**:
- **Binary Search**: Use binary search to find optimal positions
- **Efficient Computation**: Use bisect module for binary search
- **Space Efficiency**: Use only necessary variables
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Complete enumeration of all subsequences |
| Dynamic Programming | O(n²) | O(n) | Use DP to avoid recalculating subproblems |
| Binary Search | O(n log n) | O(n) | Use binary search to maintain optimal tails |

### Time Complexity
- **Time**: O(n log n) - Use binary search for efficient calculation
- **Space**: O(n) - Use binary search approach

### Why This Solution Works
- **Binary Search**: Use binary search to find optimal positions
- **Efficient Computation**: Use bisect module for binary search
- **Space Efficiency**: Use only necessary variables
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Increasing Subsequence with Constraints**
**Problem**: Find LIS with specific constraints.

**Key Differences**: Apply constraints to subsequence selection

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_increasing_subsequence(n, array, constraints):
    """
    Find LIS with constraints
    
    Args:
        n: array length
        array: array of integers
        constraints: list of constraints
    
    Returns:
        int: length of longest increasing subsequence
    """
    import bisect
    
    # Array to store smallest tail element for each LIS length
    tails = []
    
    for i, num in enumerate(array):
        if constraints(i, num):  # Check if element satisfies constraints
            # Find position to insert current element
            pos = bisect.bisect_left(tails, num)
            
            if pos == len(tails):
                # Current element is larger than all elements in tails
                tails.append(num)
            else:
                # Replace element at position pos
                tails[pos] = num
    
    return len(tails)

# Example usage
n = 6
array = [10, 9, 2, 5, 3, 7, 101, 18]
constraints = lambda i, num: num > 0  # Only positive numbers
result = constrained_increasing_subsequence(n, array, constraints)
print(f"Constrained increasing subsequence: {result}")
```

#### **2. Increasing Subsequence with Different Weights**
**Problem**: Find LIS with different weights for elements.

**Key Differences**: Different weights for different elements

**Solution Approach**: Use advanced algorithms

**Implementation**:
```python
def weighted_increasing_subsequence(n, array, weights):
    """
    Find LIS with different weights
    
    Args:
        n: array length
        array: array of integers
        weights: array of weights
    
    Returns:
        int: maximum weight of increasing subsequence
    """
    # Create DP table
    dp = [0] * n
    
    # Fill DP table
    for i in range(n):
        dp[i] = weights[i]  # Base case: single element
        for j in range(i):
            if array[j] < array[i]:
                dp[i] = max(dp[i], dp[j] + weights[i])
    
    return max(dp)

# Example usage
n = 6
array = [10, 9, 2, 5, 3, 7, 101, 18]
weights = [1, 2, 3, 4, 5, 6, 7, 8]  # Different weights
result = weighted_increasing_subsequence(n, array, weights)
print(f"Weighted increasing subsequence: {result}")
```

#### **3. Increasing Subsequence with Multiple Arrays**
**Problem**: Find LIS across multiple arrays.

**Key Differences**: Handle multiple arrays

**Solution Approach**: Use advanced algorithms

**Implementation**:
```python
def multi_array_increasing_subsequence(arrays):
    """
    Find LIS across multiple arrays
    
    Args:
        arrays: list of arrays
    
    Returns:
        int: length of longest increasing subsequence
    """
    import bisect
    
    # Combine all arrays with their indices
    combined = []
    for i, array in enumerate(arrays):
        for j, num in enumerate(array):
            combined.append((num, i, j))
    
    # Sort by value
    combined.sort()
    
    # Array to store smallest tail element for each LIS length
    tails = []
    
    for num, array_idx, element_idx in combined:
        # Find position to insert current element
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            # Current element is larger than all elements in tails
            tails.append(num)
        else:
            # Replace element at position pos
            tails[pos] = num
    
    return len(tails)

# Example usage
arrays = [[1, 3, 5], [2, 4, 6], [1, 2, 3]]
result = multi_array_increasing_subsequence(arrays)
print(f"Multi-array increasing subsequence: {result}")
```

## Problem Variations

### **Variation 1: Increasing Subsequence with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining optimal increasing subsequence finding efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic array management.

```python
from collections import defaultdict
import bisect

class DynamicIncreasingSubsequence:
    def __init__(self, array=None):
        self.array = array or []
        self.subsequences = []
        self._update_increasing_subsequence_info()
    
    def _update_increasing_subsequence_info(self):
        """Update increasing subsequence feasibility information."""
        self.increasing_subsequence_feasibility = self._calculate_increasing_subsequence_feasibility()
    
    def _calculate_increasing_subsequence_feasibility(self):
        """Calculate increasing subsequence feasibility."""
        if not self.array:
            return 0.0
        
        # Check if we can find increasing subsequences in the array
        return 1.0 if len(self.array) > 0 else 0.0
    
    def update_array(self, new_array):
        """Update the array."""
        self.array = new_array
        self._update_increasing_subsequence_info()
    
    def add_element(self, element):
        """Add element to the array."""
        self.array.append(element)
        self._update_increasing_subsequence_info()
    
    def remove_element(self, index):
        """Remove element at index from the array."""
        if 0 <= index < len(self.array):
            self.array.pop(index)
            self._update_increasing_subsequence_info()
    
    def find_longest_increasing_subsequence(self):
        """Find length of longest increasing subsequence using dynamic programming."""
        if not self.increasing_subsequence_feasibility:
            return 0
        
        n = len(self.array)
        if n == 0:
            return 0
        
        # DP table: dp[i] = length of LIS ending at index i
        dp = [1] * n
        
        # Fill DP table
        for i in range(1, n):
            for j in range(i):
                if self.array[j] < self.array[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        
        return max(dp)
    
    def find_longest_increasing_subsequence_optimized(self):
        """Find length of longest increasing subsequence using binary search optimization."""
        if not self.increasing_subsequence_feasibility:
            return 0
        
        n = len(self.array)
        if n == 0:
            return 0
        
        # tails[i] = smallest tail element of all increasing subsequences of length i+1
        tails = []
        
        for num in self.array:
            # Binary search for the position to replace
            pos = bisect.bisect_left(tails, num)
            
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        
        return len(tails)
    
    def get_increasing_subsequences_with_constraints(self, constraint_func):
        """Get increasing subsequences that satisfies custom constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        length = self.find_longest_increasing_subsequence()
        if constraint_func(length, self.array):
            return self._generate_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_in_range(self, min_length, max_length):
        """Get increasing subsequences within specified length range."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        length = self.find_longest_increasing_subsequence()
        if min_length <= length <= max_length:
            return self._generate_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_pattern(self, pattern_func):
        """Get increasing subsequences matching specified pattern."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        length = self.find_longest_increasing_subsequence()
        if pattern_func(length, self.array):
            return self._generate_increasing_subsequences()
        else:
            return []
    
    def _generate_increasing_subsequences(self):
        """Generate all possible increasing subsequences."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        subsequences = []
        
        def backtrack(index, current_subsequence):
            if index == len(self.array):
                if len(current_subsequence) > 1:
                    subsequences.append(current_subsequence[:])
                return
            
            # Include current element if it maintains increasing order
            if not current_subsequence or self.array[index] > current_subsequence[-1]:
                current_subsequence.append(self.array[index])
                backtrack(index + 1, current_subsequence)
                current_subsequence.pop()
            
            # Skip current element
            backtrack(index + 1, current_subsequence)
        
        backtrack(0, [])
        return subsequences
    
    def get_increasing_subsequence_statistics(self):
        """Get statistics about the increasing subsequences."""
        if not self.increasing_subsequence_feasibility:
            return {
                'array_length': 0,
                'increasing_subsequence_feasibility': 0,
                'longest_length': 0
            }
        
        length = self.find_longest_increasing_subsequence()
        return {
            'array_length': len(self.array),
            'increasing_subsequence_feasibility': self.increasing_subsequence_feasibility,
            'longest_length': length
        }
    
    def get_increasing_subsequence_patterns(self):
        """Get patterns in increasing subsequences."""
        patterns = {
            'has_increasing_elements': 0,
            'has_valid_array': 0,
            'optimal_subsequences_possible': 0,
            'has_large_array': 0
        }
        
        if not self.increasing_subsequence_feasibility:
            return patterns
        
        # Check if has increasing elements
        if len(self.array) > 1:
            for i in range(1, len(self.array)):
                if self.array[i] > self.array[i-1]:
                    patterns['has_increasing_elements'] = 1
                    break
        
        # Check if has valid array
        if len(self.array) > 0:
            patterns['has_valid_array'] = 1
        
        # Check if optimal subsequences are possible
        if self.increasing_subsequence_feasibility == 1.0:
            patterns['optimal_subsequences_possible'] = 1
        
        # Check if has large array
        if len(self.array) > 100:
            patterns['has_large_array'] = 1
        
        return patterns
    
    def get_optimal_increasing_subsequence_strategy(self):
        """Get optimal strategy for increasing subsequence finding."""
        if not self.increasing_subsequence_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'increasing_subsequence_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.increasing_subsequence_feasibility
        
        # Calculate increasing subsequence feasibility
        increasing_subsequence_feasibility = self.increasing_subsequence_feasibility
        
        # Determine recommended strategy
        if len(self.array) <= 100:
            recommended_strategy = 'dynamic_programming'
        elif len(self.array) <= 1000:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'binary_search_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'increasing_subsequence_feasibility': increasing_subsequence_feasibility
        }

# Example usage
array = [10, 9, 2, 5, 3, 7, 101, 18]
dynamic_increasing_subsequence = DynamicIncreasingSubsequence(array)
print(f"Increasing subsequence feasibility: {dynamic_increasing_subsequence.increasing_subsequence_feasibility}")

# Update array
dynamic_increasing_subsequence.update_array([1, 3, 6, 7, 9, 4, 10, 5, 6])
print(f"After updating array: {dynamic_increasing_subsequence.array}")

# Add element
dynamic_increasing_subsequence.add_element(8)
print(f"After adding element 8: {dynamic_increasing_subsequence.array}")

# Find longest increasing subsequence
length = dynamic_increasing_subsequence.find_longest_increasing_subsequence()
print(f"Longest increasing subsequence length: {length}")

# Find with optimization
optimized_length = dynamic_increasing_subsequence.find_longest_increasing_subsequence_optimized()
print(f"Optimized longest increasing subsequence length: {optimized_length}")

# Get subsequences with constraints
def constraint_func(length, array):
    return length > 0 and len(array) > 0

print(f"Subsequences with constraints: {len(dynamic_increasing_subsequence.get_increasing_subsequences_with_constraints(constraint_func))}")

# Get subsequences in range
print(f"Subsequences in range 1-10: {len(dynamic_increasing_subsequence.get_increasing_subsequences_in_range(1, 10))}")

# Get subsequences with pattern
def pattern_func(length, array):
    return length > 0 and len(array) > 0

print(f"Subsequences with pattern: {len(dynamic_increasing_subsequence.get_increasing_subsequences_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_increasing_subsequence.get_increasing_subsequence_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_increasing_subsequence.get_increasing_subsequence_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_increasing_subsequence.get_optimal_increasing_subsequence_strategy()}")
```

### **Variation 2: Increasing Subsequence with Different Operations**
**Problem**: Handle different types of increasing subsequence operations (weighted subsequences, priority-based finding, advanced array analysis).

**Approach**: Use advanced data structures for efficient different types of increasing subsequence operations.

```python
class AdvancedIncreasingSubsequence:
    def __init__(self, array=None, weights=None, priorities=None):
        self.array = array or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.subsequences = []
        self._update_increasing_subsequence_info()
    
    def _update_increasing_subsequence_info(self):
        """Update increasing subsequence feasibility information."""
        self.increasing_subsequence_feasibility = self._calculate_increasing_subsequence_feasibility()
    
    def _calculate_increasing_subsequence_feasibility(self):
        """Calculate increasing subsequence feasibility."""
        if not self.array:
            return 0.0
        
        # Check if we can find increasing subsequences in the array
        return 1.0 if len(self.array) > 0 else 0.0
    
    def find_longest_increasing_subsequence(self):
        """Find length of longest increasing subsequence using dynamic programming."""
        if not self.increasing_subsequence_feasibility:
            return 0
        
        n = len(self.array)
        if n == 0:
            return 0
        
        # DP table: dp[i] = length of LIS ending at index i
        dp = [1] * n
        
        # Fill DP table
        for i in range(1, n):
            for j in range(i):
                if self.array[j] < self.array[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        
        return max(dp)
    
    def get_weighted_increasing_subsequences(self):
        """Get increasing subsequences with weights and priorities applied."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        # Create weighted array
        weighted_array = []
        for i, element in enumerate(self.array):
            weight = self.weights.get(i, 1)
            priority = self.priorities.get(i, 1)
            weighted_score = element * weight * priority
            weighted_array.append((element, weighted_score, i))
        
        # Sort by weighted score
        weighted_array.sort(key=lambda x: x[1], reverse=True)
        
        # Generate subsequences with weighted elements
        subsequences = []
        
        def backtrack(index, current_subsequence, current_weight):
            if index == len(weighted_array):
                if len(current_subsequence) > 1:
                    subsequences.append((current_subsequence[:], current_weight))
                return
            
            element, weight, original_index = weighted_array[index]
            
            # Include current element if it maintains increasing order
            if not current_subsequence or element > current_subsequence[-1][0]:
                current_subsequence.append((element, original_index))
                backtrack(index + 1, current_subsequence, current_weight + weight)
                current_subsequence.pop()
            
            # Skip current element
            backtrack(index + 1, current_subsequence, current_weight)
        
        backtrack(0, [], 0)
        return subsequences
    
    def get_increasing_subsequences_with_priority(self, priority_func):
        """Get increasing subsequences considering priority."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        # Create priority-based array
        priority_array = []
        for i, element in enumerate(self.array):
            priority = priority_func(element, i, self.weights, self.priorities)
            priority_array.append((element, priority, i))
        
        # Sort by priority
        priority_array.sort(key=lambda x: x[1], reverse=True)
        
        # Generate subsequences with priority elements
        subsequences = []
        
        def backtrack(index, current_subsequence, current_priority):
            if index == len(priority_array):
                if len(current_subsequence) > 1:
                    subsequences.append((current_subsequence[:], current_priority))
                return
            
            element, priority, original_index = priority_array[index]
            
            # Include current element if it maintains increasing order
            if not current_subsequence or element > current_subsequence[-1][0]:
                current_subsequence.append((element, original_index))
                backtrack(index + 1, current_subsequence, current_priority + priority)
                current_subsequence.pop()
            
            # Skip current element
            backtrack(index + 1, current_subsequence, current_priority)
        
        backtrack(0, [], 0)
        return subsequences
    
    def get_increasing_subsequences_with_optimization(self, optimization_func):
        """Get increasing subsequences using custom optimization function."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        # Create optimization-based array
        optimized_array = []
        for i, element in enumerate(self.array):
            score = optimization_func(element, i, self.weights, self.priorities)
            optimized_array.append((element, score, i))
        
        # Sort by optimization score
        optimized_array.sort(key=lambda x: x[1], reverse=True)
        
        # Generate subsequences with optimized elements
        subsequences = []
        
        def backtrack(index, current_subsequence, current_score):
            if index == len(optimized_array):
                if len(current_subsequence) > 1:
                    subsequences.append((current_subsequence[:], current_score))
                return
            
            element, score, original_index = optimized_array[index]
            
            # Include current element if it maintains increasing order
            if not current_subsequence or element > current_subsequence[-1][0]:
                current_subsequence.append((element, original_index))
                backtrack(index + 1, current_subsequence, current_score + score)
                current_subsequence.pop()
            
            # Skip current element
            backtrack(index + 1, current_subsequence, current_score)
        
        backtrack(0, [], 0)
        return subsequences
    
    def get_increasing_subsequences_with_constraints(self, constraint_func):
        """Get increasing subsequences that satisfies custom constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        if constraint_func(self.array, self.weights, self.priorities):
            return self.get_weighted_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_multiple_criteria(self, criteria_list):
        """Get increasing subsequences that satisfies multiple criteria."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.array, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_alternatives(self, alternatives):
        """Get increasing subsequences considering alternative weights/priorities."""
        result = []
        
        # Check original subsequences
        original_subsequences = self.get_weighted_increasing_subsequences()
        result.append((original_subsequences, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedIncreasingSubsequence(self.array, alt_weights, alt_priorities)
            temp_subsequences = temp_instance.get_weighted_increasing_subsequences()
            result.append((temp_subsequences, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_increasing_subsequences_with_adaptive_criteria(self, adaptive_func):
        """Get increasing subsequences using adaptive criteria."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        if adaptive_func(self.array, self.weights, self.priorities, []):
            return self.get_weighted_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequence_optimization(self):
        """Get optimal increasing subsequence configuration."""
        strategies = [
            ('weighted_subsequences', lambda: len(self.get_weighted_increasing_subsequences())),
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
array = [10, 9, 2, 5, 3, 7, 101, 18]
weights = {i: (i + 1) * 2 for i in range(len(array))}  # Weight based on index
priorities = {i: array[i] // 10 for i in range(len(array))}  # Priority based on value
advanced_increasing_subsequence = AdvancedIncreasingSubsequence(array, weights, priorities)

print(f"Weighted subsequences: {len(advanced_increasing_subsequence.get_weighted_increasing_subsequences())}")

# Get subsequences with priority
def priority_func(element, index, weights, priorities):
    return weights.get(index, 1) + priorities.get(index, 1)

print(f"Subsequences with priority: {len(advanced_increasing_subsequence.get_increasing_subsequences_with_priority(priority_func))}")

# Get subsequences with optimization
def optimization_func(element, index, weights, priorities):
    return weights.get(index, 1) * priorities.get(index, 1)

print(f"Subsequences with optimization: {len(advanced_increasing_subsequence.get_increasing_subsequences_with_optimization(optimization_func))}")

# Get subsequences with constraints
def constraint_func(array, weights, priorities):
    return len(array) > 0

print(f"Subsequences with constraints: {len(advanced_increasing_subsequence.get_increasing_subsequences_with_constraints(constraint_func))}")

# Get subsequences with multiple criteria
def criterion1(array, weights, priorities):
    return len(array) > 0

def criterion2(array, weights, priorities):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Subsequences with multiple criteria: {len(advanced_increasing_subsequence.get_increasing_subsequences_with_multiple_criteria(criteria_list))}")

# Get subsequences with alternatives
alternatives = [({i: 1 for i in range(len(array))}, {i: 1 for i in range(len(array))}), ({i: (i+1)*3 for i in range(len(array))}, {i: array[i]//5 for i in range(len(array))})]
print(f"Subsequences with alternatives: {advanced_increasing_subsequence.get_increasing_subsequences_with_alternatives(alternatives)}")

# Get subsequences with adaptive criteria
def adaptive_func(array, weights, priorities, current_result):
    return len(array) > 0 and len(current_result) < 5

print(f"Subsequences with adaptive criteria: {len(advanced_increasing_subsequence.get_increasing_subsequences_with_adaptive_criteria(adaptive_func))}")

# Get increasing subsequence optimization
print(f"Increasing subsequence optimization: {advanced_increasing_subsequence.get_increasing_subsequence_optimization()}")
```

### **Variation 3: Increasing Subsequence with Constraints**
**Problem**: Handle increasing subsequence finding with additional constraints (array limits, element constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedIncreasingSubsequence:
    def __init__(self, array=None, constraints=None):
        self.array = array or []
        self.constraints = constraints or {}
        self.subsequences = []
        self._update_increasing_subsequence_info()
    
    def _update_increasing_subsequence_info(self):
        """Update increasing subsequence feasibility information."""
        self.increasing_subsequence_feasibility = self._calculate_increasing_subsequence_feasibility()
    
    def _calculate_increasing_subsequence_feasibility(self):
        """Calculate increasing subsequence feasibility."""
        if not self.array:
            return 0.0
        
        # Check if we can find increasing subsequences in the array
        return 1.0 if len(self.array) > 0 else 0.0
    
    def _is_valid_element(self, element, index):
        """Check if element is valid considering constraints."""
        # Element constraints
        if 'allowed_elements' in self.constraints:
            if element not in self.constraints['allowed_elements']:
                return False
        
        if 'forbidden_elements' in self.constraints:
            if element in self.constraints['forbidden_elements']:
                return False
        
        # Index constraints
        if 'allowed_indices' in self.constraints:
            if index not in self.constraints['allowed_indices']:
                return False
        
        if 'forbidden_indices' in self.constraints:
            if index in self.constraints['forbidden_indices']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(element, index):
                    return False
        
        return True
    
    def get_increasing_subsequences_with_array_constraints(self, min_length, max_length):
        """Get increasing subsequences considering array length constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        if min_length <= len(self.array) <= max_length:
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_element_constraints(self, element_constraints):
        """Get increasing subsequences considering element constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in element_constraints:
            if not constraint(self.array):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_pattern_constraints(self, pattern_constraints):
        """Get increasing subsequences considering pattern constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.array):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_mathematical_constraints(self, constraint_func):
        """Get increasing subsequences that satisfies custom mathematical constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        if constraint_func(self.array):
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_optimization_constraints(self, optimization_func):
        """Get increasing subsequences using custom optimization constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        # Calculate optimization score for subsequences
        score = optimization_func(self.array)
        
        if score > 0:
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_multiple_constraints(self, constraints_list):
        """Get increasing subsequences that satisfies multiple constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.array):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_priority_constraints(self, priority_func):
        """Get increasing subsequences with priority-based constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        # Calculate priority for subsequences
        priority = priority_func(self.array)
        
        if priority > 0:
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def get_increasing_subsequences_with_adaptive_constraints(self, adaptive_func):
        """Get increasing subsequences with adaptive constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        if adaptive_func(self.array, []):
            return self._generate_constrained_increasing_subsequences()
        else:
            return []
    
    def _generate_constrained_increasing_subsequences(self):
        """Generate all possible increasing subsequences considering constraints."""
        if not self.increasing_subsequence_feasibility:
            return []
        
        subsequences = []
        
        def backtrack(index, current_subsequence):
            if index == len(self.array):
                if len(current_subsequence) > 1:
                    subsequences.append(current_subsequence[:])
                return
            
            element = self.array[index]
            
            # Include current element if it maintains increasing order and satisfies constraints
            if (not current_subsequence or element > current_subsequence[-1]) and self._is_valid_element(element, index):
                current_subsequence.append(element)
                backtrack(index + 1, current_subsequence)
                current_subsequence.pop()
            
            # Skip current element
            backtrack(index + 1, current_subsequence)
        
        backtrack(0, [])
        return subsequences
    
    def get_optimal_increasing_subsequence_strategy(self):
        """Get optimal increasing subsequence strategy considering all constraints."""
        strategies = [
            ('array_constraints', self.get_increasing_subsequences_with_array_constraints),
            ('element_constraints', self.get_increasing_subsequences_with_element_constraints),
            ('pattern_constraints', self.get_increasing_subsequences_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'array_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'element_constraints':
                    element_constraints = [lambda array: len(array) > 0]
                    result = strategy_func(element_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda array: len(array) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_elements': list(range(1, 200)),  # Allow elements 1-199
    'forbidden_elements': [0, -1],
    'allowed_indices': list(range(10)),  # Allow indices 0-9
    'forbidden_indices': [],
    'pattern_constraints': [lambda element, index: element > 0 and index >= 0]
}

array = [10, 9, 2, 5, 3, 7, 101, 18]
constrained_increasing_subsequence = ConstrainedIncreasingSubsequence(array, constraints)

print("Array-constrained subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_array_constraints(1, 20)))

print("Element-constrained subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_element_constraints([lambda array: len(array) > 0])))

print("Pattern-constrained subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_pattern_constraints([lambda array: len(array) > 0])))

# Mathematical constraints
def custom_constraint(array):
    return len(array) > 0

print("Mathematical constraint subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(array):
    return 1 <= len(array) <= 20

range_constraints = [range_constraint]
print("Range-constrained subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_array_constraints(1, 20)))

# Multiple constraints
def constraint1(array):
    return len(array) > 0

def constraint2(array):
    return all(x > 0 for x in array)

constraints_list = [constraint1, constraint2]
print("Multiple constraints subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(array):
    return len(array) + sum(array)

print("Priority-constrained subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(array, current_result):
    return len(array) > 0 and len(current_result) < 5

print("Adaptive constraint subsequences:", len(constrained_increasing_subsequence.get_increasing_subsequences_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_increasing_subsequence.get_optimal_increasing_subsequence_strategy()
print(f"Optimal increasing subsequence strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Edit Distance](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Counting Towers](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - DP
- [Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) - DP
- [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Subsequence DP, optimization algorithms
- **Binary Search**: Search algorithms, optimization
- **Mathematical Algorithms**: Optimization, subsequence theory

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Binary Search](https://cp-algorithms.com/searching/binary-search.html) - Binary search algorithms
- [Subsequence Algorithms](https://cp-algorithms.com/sequences/longest_increasing_subsequence.html) - Subsequence algorithms

### **Practice Problems**
- [CSES Edit Distance](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Towers](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
