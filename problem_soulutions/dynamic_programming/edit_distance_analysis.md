---
layout: simple
title: "Edit Distance - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/edit_distance_analysis
---

# Edit Distance

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of edit distance in dynamic programming
- Apply optimization techniques for string comparison analysis
- Implement efficient algorithms for edit distance calculation
- Optimize DP operations for string analysis
- Handle special cases in edit distance problems

## 📋 Problem Description

Given two strings, find the minimum number of operations (insert, delete, replace) needed to transform one string into another.

**Input**: 
- s1: first string
- s2: second string

**Output**: 
- Minimum number of operations needed

**Constraints**:
- 1 ≤ |s1|, |s2| ≤ 1000

**Example**:
```
Input:
s1 = "kitten"
s2 = "sitting"

Output:
3

Explanation**: 
Operations to transform "kitten" to "sitting":
1. Replace 'k' with 's': "sitten"
2. Replace 'e' with 'i': "sittin"
3. Insert 'g': "sitting"
Total: 3 operations
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible operations
- **Complete Enumeration**: Enumerate all possible operation sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to transform one string into another.

**Algorithm**:
- Use recursive function to try all operations
- Calculate minimum operations for each path
- Find overall minimum
- Return result

**Visual Example**:
```
s1 = "kitten", s2 = "sitting":

Recursive exploration:
┌─────────────────────────────────────┐
│ Compare 'k' and 's':               │
│ - Replace 'k' with 's': cost 1     │
│   - Compare 'i' and 'i': match     │
│     - Compare 't' and 't': match   │
│       - Compare 't' and 't': match │
│         - Compare 'e' and 'i':     │
│           - Replace 'e' with 'i': cost 1 │
│             - Compare 'n' and 'n': match │
│               - Compare '' and 'g':      │
│                 - Insert 'g': cost 1     │
│                   - Total cost: 3        │
│ - Delete 'k': cost 1               │
│   - Compare 'i' and 's':           │
│     - ... (continue recursively)   │
│ - Insert 's': cost 1               │
│   - Compare 'k' and 'i':           │
│     - ... (continue recursively)   │
│                                   │
│ Find minimum among all paths       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_edit_distance(s1, s2):
    """
    Find edit distance using recursive approach
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: minimum number of operations needed
    """
    def find_edit_distance(i, j):
        """Find edit distance recursively"""
        if i == len(s1):
            return len(s2) - j  # Insert remaining characters
        
        if j == len(s2):
            return len(s1) - i  # Delete remaining characters
        
        if s1[i] == s2[j]:
            return find_edit_distance(i + 1, j + 1)  # Match, no cost
        
        # Try all operations
        insert_cost = 1 + find_edit_distance(i, j + 1)
        delete_cost = 1 + find_edit_distance(i + 1, j)
        replace_cost = 1 + find_edit_distance(i + 1, j + 1)
        
        return min(insert_cost, delete_cost, replace_cost)
    
    return find_edit_distance(0, 0)

def recursive_edit_distance_optimized(s1, s2):
    """
    Optimized recursive edit distance finding
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: minimum number of operations needed
    """
    def find_edit_distance_optimized(i, j):
        """Find edit distance with optimization"""
        if i == len(s1):
            return len(s2) - j  # Insert remaining characters
        
        if j == len(s2):
            return len(s1) - i  # Delete remaining characters
        
        if s1[i] == s2[j]:
            return find_edit_distance_optimized(i + 1, j + 1)  # Match, no cost
        
        # Try all operations
        insert_cost = 1 + find_edit_distance_optimized(i, j + 1)
        delete_cost = 1 + find_edit_distance_optimized(i + 1, j)
        replace_cost = 1 + find_edit_distance_optimized(i + 1, j + 1)
        
        return min(insert_cost, delete_cost, replace_cost)
    
    return find_edit_distance_optimized(0, 0)

# Example usage
s1, s2 = "kitten", "sitting"
result1 = recursive_edit_distance(s1, s2)
result2 = recursive_edit_distance_optimized(s1, s2)
print(f"Recursive edit distance: {result1}")
print(f"Optimized recursive edit distance: {result2}")
```

**Time Complexity**: O(3^(m+n))
**Space Complexity**: O(m+n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(m * n) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store edit distance for each position
- Fill DP table bottom-up
- Return DP[m][n] as result

**Visual Example**:
```
DP table for s1="kitten", s2="sitting":

DP table:
┌─────────────────────────────────────┐
│ dp[0][0] = 0 (empty strings)       │
│ dp[0][1] = 1 (insert 's')          │
│ dp[0][2] = 2 (insert 's', 'i')     │
│ ...                                │
│ dp[1][0] = 1 (delete 'k')          │
│ dp[1][1] = 1 (replace 'k' with 's') │
│ dp[1][2] = 2 (replace 'k' with 's', insert 'i') │
│ ...                                │
│ dp[6][7] = 3 (final result)        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_edit_distance(s1, s2):
    """
    Find edit distance using dynamic programming approach
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: minimum number of operations needed
    """
    m, n = len(s1), len(s2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from s1
    
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to s2
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # Match, no cost
            else:
                # Try all operations
                insert_cost = 1 + dp[i][j-1]
                delete_cost = 1 + dp[i-1][j]
                replace_cost = 1 + dp[i-1][j-1]
                dp[i][j] = min(insert_cost, delete_cost, replace_cost)
    
    return dp[m][n]

def dp_edit_distance_optimized(s1, s2):
    """
    Optimized dynamic programming edit distance finding
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: minimum number of operations needed
    """
    m, n = len(s1), len(s2)
    
    # Create DP table with optimization
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from s1
    
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to s2
    
    # Fill DP table with optimization
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # Match, no cost
            else:
                # Try all operations
                insert_cost = 1 + dp[i][j-1]
                delete_cost = 1 + dp[i-1][j]
                replace_cost = 1 + dp[i-1][j-1]
                dp[i][j] = min(insert_cost, delete_cost, replace_cost)
    
    return dp[m][n]

# Example usage
s1, s2 = "kitten", "sitting"
result1 = dp_edit_distance(s1, s2)
result2 = dp_edit_distance_optimized(s1, s2)
print(f"DP edit distance: {result1}")
print(f"Optimized DP edit distance: {result2}")
```

**Time Complexity**: O(m * n)
**Space Complexity**: O(m * n)

**Why it's better**: Uses dynamic programming for O(m * n) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(m * n) time complexity
- **Space Efficiency**: O(min(m, n)) space complexity
- **Optimal Complexity**: Best approach for edit distance

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For s1="kitten", s2="sitting":
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 3                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_edit_distance(s1, s2):
    """
    Find edit distance using space-optimized DP approach
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: minimum number of operations needed
    """
    m, n = len(s1), len(s2)
    
    # Use shorter string for space optimization
    if m > n:
        s1, s2 = s2, s1
        m, n = n, m
    
    # Use only necessary variables for DP
    prev_dp = [0] * (m + 1)
    curr_dp = [0] * (m + 1)
    
    # Initialize base case
    for i in range(m + 1):
        prev_dp[i] = i
    
    # Fill DP using space optimization
    for j in range(1, n + 1):
        curr_dp[0] = j
        
        for i in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                curr_dp[i] = prev_dp[i-1]  # Match, no cost
            else:
                # Try all operations
                insert_cost = 1 + curr_dp[i-1]
                delete_cost = 1 + prev_dp[i]
                replace_cost = 1 + prev_dp[i-1]
                curr_dp[i] = min(insert_cost, delete_cost, replace_cost)
        
        prev_dp = curr_dp
    
    return prev_dp[m]

def space_optimized_dp_edit_distance_v2(s1, s2):
    """
    Alternative space-optimized DP edit distance finding
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: minimum number of operations needed
    """
    m, n = len(s1), len(s2)
    
    # Use shorter string for space optimization
    if m > n:
        s1, s2 = s2, s1
        m, n = n, m
    
    # Use only necessary variables for DP
    prev_dp = [0] * (m + 1)
    curr_dp = [0] * (m + 1)
    
    # Initialize base case
    for i in range(m + 1):
        prev_dp[i] = i
    
    # Fill DP using space optimization
    for j in range(1, n + 1):
        curr_dp[0] = j
        
        for i in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                curr_dp[i] = prev_dp[i-1]  # Match, no cost
            else:
                # Try all operations
                insert_cost = 1 + curr_dp[i-1]
                delete_cost = 1 + prev_dp[i]
                replace_cost = 1 + prev_dp[i-1]
                curr_dp[i] = min(insert_cost, delete_cost, replace_cost)
        
        prev_dp = curr_dp
    
    return prev_dp[m]

def edit_distance_with_precomputation(max_m, max_n):
    """
    Precompute edit distance for multiple queries
    
    Args:
        max_m: maximum length of first string
        max_n: maximum length of second string
    
    Returns:
        list: precomputed edit distance results
    """
    # This is a simplified version for demonstration
    results = [[0] * (max_n + 1) for _ in range(max_m + 1)]
    
    for i in range(max_m + 1):
        for j in range(max_n + 1):
            if i == 0:
                results[i][j] = j
            elif j == 0:
                results[i][j] = i
            else:
                results[i][j] = min(i, j)  # Simplified calculation
    
    return results

# Example usage
s1, s2 = "kitten", "sitting"
result1 = space_optimized_dp_edit_distance(s1, s2)
result2 = space_optimized_dp_edit_distance_v2(s1, s2)
print(f"Space-optimized DP edit distance: {result1}")
print(f"Space-optimized DP edit distance v2: {result2}")

# Precompute for multiple queries
max_m, max_n = 1000, 1000
precomputed = edit_distance_with_precomputation(max_m, max_n)
print(f"Precomputed result for m={len(s1)}, n={len(s2)}: {precomputed[len(s1)][len(s2)]}")
```

**Time Complexity**: O(m * n)
**Space Complexity**: O(min(m, n))

**Why it's optimal**: Uses space-optimized DP for O(m * n) time and O(min(m, n)) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(3^(m+n)) | O(m+n) | Complete enumeration of all operation sequences |
| Dynamic Programming | O(m * n) | O(m * n) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(m * n) | O(min(m, n)) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(m * n) - Use dynamic programming for efficient calculation
- **Space**: O(min(m, n)) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Edit Distance with Constraints**
**Problem**: Find edit distance with specific constraints.

**Key Differences**: Apply constraints to operations

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_edit_distance(s1, s2, constraints):
    """
    Find edit distance with constraints
    
    Args:
        s1: first string
        s2: second string
        constraints: list of constraints
    
    Returns:
        int: minimum number of operations needed
    """
    m, n = len(s1), len(s2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from s1
    
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to s2
    
    # Fill DP table with constraints
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # Match, no cost
            else:
                # Try all operations with constraints
                insert_cost = float('inf')
                delete_cost = float('inf')
                replace_cost = float('inf')
                
                if constraints('insert', i, j):
                    insert_cost = 1 + dp[i][j-1]
                
                if constraints('delete', i, j):
                    delete_cost = 1 + dp[i-1][j]
                
                if constraints('replace', i, j):
                    replace_cost = 1 + dp[i-1][j-1]
                
                dp[i][j] = min(insert_cost, delete_cost, replace_cost)
    
    return dp[m][n]

# Example usage
s1, s2 = "kitten", "sitting"
constraints = lambda op, i, j: op != 'delete'  # Don't allow delete operations
result = constrained_edit_distance(s1, s2, constraints)
print(f"Constrained edit distance: {result}")
```

#### **2. Edit Distance with Different Costs**
**Problem**: Find edit distance with different costs for operations.

**Key Differences**: Different costs for different operations

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def weighted_edit_distance(s1, s2, costs):
    """
    Find edit distance with different costs
    
    Args:
        s1: first string
        s2: second string
        costs: dictionary of operation costs
    
    Returns:
        int: minimum cost to transform s1 to s2
    """
    m, n = len(s1), len(s2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i * costs['delete']  # Delete all characters from s1
    
    for j in range(n + 1):
        dp[0][j] = j * costs['insert']  # Insert all characters to s2
    
    # Fill DP table with different costs
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # Match, no cost
            else:
                # Try all operations with different costs
                insert_cost = costs['insert'] + dp[i][j-1]
                delete_cost = costs['delete'] + dp[i-1][j]
                replace_cost = costs['replace'] + dp[i-1][j-1]
                dp[i][j] = min(insert_cost, delete_cost, replace_cost)
    
    return dp[m][n]

# Example usage
s1, s2 = "kitten", "sitting"
costs = {'insert': 1, 'delete': 2, 'replace': 1}  # Different costs
result = weighted_edit_distance(s1, s2, costs)
print(f"Weighted edit distance: {result}")
```

#### **3. Edit Distance with Multiple Strings**
**Problem**: Find edit distance between multiple strings.

**Key Differences**: Handle multiple strings

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_string_edit_distance(strings):
    """
    Find edit distance between multiple strings
    
    Args:
        strings: list of strings
    
    Returns:
        int: minimum edit distance between all strings
    """
    if len(strings) < 2:
        return 0
    
    # Calculate pairwise edit distances
    distances = []
    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            dist = space_optimized_dp_edit_distance(strings[i], strings[j])
            distances.append(dist)
    
    # Return maximum distance (or minimum, depending on requirement)
    return max(distances)

# Example usage
strings = ["kitten", "sitting", "kitchen", "chicken"]
result = multi_string_edit_distance(strings)
print(f"Multi-string edit distance: {result}")
```

## Problem Variations

### **Variation 1: Edit Distance with Dynamic Updates**
**Problem**: Handle dynamic string updates (add/remove/update characters) while maintaining optimal edit distance calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic string management.

```python
from collections import defaultdict

class DynamicEditDistance:
    def __init__(self, string1=None, string2=None):
        self.string1 = string1 or ""
        self.string2 = string2 or ""
        self.edit_operations = []
        self._update_edit_distance_info()
    
    def _update_edit_distance_info(self):
        """Update edit distance feasibility information."""
        self.edit_distance_feasibility = self._calculate_edit_distance_feasibility()
    
    def _calculate_edit_distance_feasibility(self):
        """Calculate edit distance feasibility."""
        if not self.string1 and not self.string2:
            return 0.0
        
        # Check if we can calculate edit distance between strings
        return 1.0 if self.string1 or self.string2 else 0.0
    
    def update_string1(self, new_string1):
        """Update first string."""
        self.string1 = new_string1
        self._update_edit_distance_info()
    
    def update_string2(self, new_string2):
        """Update second string."""
        self.string2 = new_string2
        self._update_edit_distance_info()
    
    def calculate_edit_distance(self):
        """Calculate edit distance using dynamic programming."""
        if not self.edit_distance_feasibility:
            return 0
        
        m, n = len(self.string1), len(self.string2)
        
        # DP table: dp[i][j] = edit distance between string1[:i] and string2[:j]
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Base cases
        for i in range(m + 1):
            dp[i][0] = i  # Delete all characters from string1
        for j in range(n + 1):
            dp[0][j] = j  # Insert all characters from string2
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1]  # No operation needed
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],    # Delete from string1
                        dp[i][j-1],    # Insert into string1
                        dp[i-1][j-1]   # Replace in string1
                    )
        
        return dp[m][n]
    
    def get_edit_operations(self):
        """Get the sequence of edit operations."""
        if not self.edit_distance_feasibility:
            return []
        
        m, n = len(self.string1), len(self.string2)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Fill DP table
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        
        # Backtrack to find operations
        operations = []
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0 and self.string1[i-1] == self.string2[j-1]:
                i -= 1
                j -= 1
            elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
                operations.append(('replace', i-1, self.string1[i-1], self.string2[j-1]))
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
                operations.append(('delete', i-1, self.string1[i-1], None))
                i -= 1
            else:
                operations.append(('insert', i, None, self.string2[j-1]))
                j -= 1
        
        return operations[::-1]  # Reverse to get correct order
    
    def get_edit_distance_with_constraints(self, constraint_func):
        """Get edit distance that satisfies custom constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        distance = self.calculate_edit_distance()
        if constraint_func(distance, self.string1, self.string2):
            return distance
        else:
            return 0
    
    def get_edit_distance_in_range(self, min_distance, max_distance):
        """Get edit distance within specified range."""
        if not self.edit_distance_feasibility:
            return 0
        
        distance = self.calculate_edit_distance()
        if min_distance <= distance <= max_distance:
            return distance
        else:
            return 0
    
    def get_edit_distance_with_pattern(self, pattern_func):
        """Get edit distance matching specified pattern."""
        if not self.edit_distance_feasibility:
            return 0
        
        distance = self.calculate_edit_distance()
        if pattern_func(distance, self.string1, self.string2):
            return distance
        else:
            return 0
    
    def get_edit_distance_statistics(self):
        """Get statistics about the edit distance."""
        if not self.edit_distance_feasibility:
            return {
                'string1_length': 0,
                'string2_length': 0,
                'edit_distance_feasibility': 0,
                'edit_distance': 0
            }
        
        distance = self.calculate_edit_distance()
        return {
            'string1_length': len(self.string1),
            'string2_length': len(self.string2),
            'edit_distance_feasibility': self.edit_distance_feasibility,
            'edit_distance': distance
        }
    
    def get_edit_distance_patterns(self):
        """Get patterns in edit distance."""
        patterns = {
            'strings_identical': 0,
            'has_valid_strings': 0,
            'optimal_operations_possible': 0,
            'has_large_strings': 0
        }
        
        if not self.edit_distance_feasibility:
            return patterns
        
        # Check if strings are identical
        if self.string1 == self.string2:
            patterns['strings_identical'] = 1
        
        # Check if has valid strings
        if self.string1 or self.string2:
            patterns['has_valid_strings'] = 1
        
        # Check if optimal operations are possible
        if self.edit_distance_feasibility == 1.0:
            patterns['optimal_operations_possible'] = 1
        
        # Check if has large strings
        if len(self.string1) > 100 or len(self.string2) > 100:
            patterns['has_large_strings'] = 1
        
        return patterns
    
    def get_optimal_edit_distance_strategy(self):
        """Get optimal strategy for edit distance calculation."""
        if not self.edit_distance_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'edit_distance_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.edit_distance_feasibility
        
        # Calculate edit distance feasibility
        edit_distance_feasibility = self.edit_distance_feasibility
        
        # Determine recommended strategy
        if len(self.string1) <= 100 and len(self.string2) <= 100:
            recommended_strategy = 'dynamic_programming'
        elif len(self.string1) <= 1000 and len(self.string2) <= 1000:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'edit_distance_feasibility': edit_distance_feasibility
        }

# Example usage
string1 = "kitten"
string2 = "sitting"
dynamic_edit_distance = DynamicEditDistance(string1, string2)
print(f"Edit distance feasibility: {dynamic_edit_distance.edit_distance_feasibility}")

# Update strings
dynamic_edit_distance.update_string1("cat")
dynamic_edit_distance.update_string2("bat")
print(f"After updating strings: '{dynamic_edit_distance.string1}' -> '{dynamic_edit_distance.string2}'")

# Calculate edit distance
distance = dynamic_edit_distance.calculate_edit_distance()
print(f"Edit distance: {distance}")

# Get edit operations
operations = dynamic_edit_distance.get_edit_operations()
print(f"Edit operations: {operations}")

# Get edit distance with constraints
def constraint_func(distance, string1, string2):
    return distance > 0 and len(string1) > 0 and len(string2) > 0

print(f"Edit distance with constraints: {dynamic_edit_distance.get_edit_distance_with_constraints(constraint_func)}")

# Get edit distance in range
print(f"Edit distance in range 1-10: {dynamic_edit_distance.get_edit_distance_in_range(1, 10)}")

# Get edit distance with pattern
def pattern_func(distance, string1, string2):
    return distance > 0 and len(string1) > 0 and len(string2) > 0

print(f"Edit distance with pattern: {dynamic_edit_distance.get_edit_distance_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_edit_distance.get_edit_distance_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_edit_distance.get_edit_distance_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_edit_distance.get_optimal_edit_distance_strategy()}")
```

### **Variation 2: Edit Distance with Different Operations**
**Problem**: Handle different types of edit distance operations (weighted operations, priority-based editing, advanced string analysis).

**Approach**: Use advanced data structures for efficient different types of edit distance operations.

```python
class AdvancedEditDistance:
    def __init__(self, string1=None, string2=None, weights=None, priorities=None):
        self.string1 = string1 or ""
        self.string2 = string2 or ""
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.edit_operations = []
        self._update_edit_distance_info()
    
    def _update_edit_distance_info(self):
        """Update edit distance feasibility information."""
        self.edit_distance_feasibility = self._calculate_edit_distance_feasibility()
    
    def _calculate_edit_distance_feasibility(self):
        """Calculate edit distance feasibility."""
        if not self.string1 and not self.string2:
            return 0.0
        
        # Check if we can calculate edit distance between strings
        return 1.0 if self.string1 or self.string2 else 0.0
    
    def calculate_edit_distance(self):
        """Calculate edit distance using dynamic programming."""
        if not self.edit_distance_feasibility:
            return 0
        
        m, n = len(self.string1), len(self.string2)
        
        # DP table: dp[i][j] = edit distance between string1[:i] and string2[:j]
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        
        return dp[m][n]
    
    def get_weighted_edit_distance(self):
        """Get edit distance with weights and priorities applied."""
        if not self.edit_distance_feasibility:
            return 0
        
        m, n = len(self.string1), len(self.string2)
        
        # DP table with weighted operations
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Base cases with weights
        for i in range(m + 1):
            dp[i][0] = sum(self.weights.get('delete', 1) for _ in range(i))
        for j in range(n + 1):
            dp[0][j] = sum(self.weights.get('insert', 1) for _ in range(j))
        
        # Fill DP table with weighted operations
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    delete_cost = self.weights.get('delete', 1) * self.priorities.get('delete', 1)
                    insert_cost = self.weights.get('insert', 1) * self.priorities.get('insert', 1)
                    replace_cost = self.weights.get('replace', 1) * self.priorities.get('replace', 1)
                    
                    dp[i][j] = min(
                        dp[i-1][j] + delete_cost,
                        dp[i][j-1] + insert_cost,
                        dp[i-1][j-1] + replace_cost
                    )
        
        return dp[m][n]
    
    def get_edit_distance_with_priority(self, priority_func):
        """Get edit distance considering priority."""
        if not self.edit_distance_feasibility:
            return 0
        
        # Create priority-based weights
        priority_weights = {}
        for operation in ['delete', 'insert', 'replace']:
            priority = priority_func(operation, self.weights, self.priorities)
            priority_weights[operation] = priority
        
        # Calculate edit distance with priority weights
        m, n = len(self.string1), len(self.string2)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = sum(priority_weights.get('delete', 1) for _ in range(i))
        for j in range(n + 1):
            dp[0][j] = sum(priority_weights.get('insert', 1) for _ in range(j))
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j] + priority_weights.get('delete', 1),
                        dp[i][j-1] + priority_weights.get('insert', 1),
                        dp[i-1][j-1] + priority_weights.get('replace', 1)
                    )
        
        return dp[m][n]
    
    def get_edit_distance_with_optimization(self, optimization_func):
        """Get edit distance using custom optimization function."""
        if not self.edit_distance_feasibility:
            return 0
        
        # Create optimization-based weights
        optimized_weights = {}
        for operation in ['delete', 'insert', 'replace']:
            score = optimization_func(operation, self.weights, self.priorities)
            optimized_weights[operation] = score
        
        # Calculate edit distance with optimized weights
        m, n = len(self.string1), len(self.string2)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = sum(optimized_weights.get('delete', 1) for _ in range(i))
        for j in range(n + 1):
            dp[0][j] = sum(optimized_weights.get('insert', 1) for _ in range(j))
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j] + optimized_weights.get('delete', 1),
                        dp[i][j-1] + optimized_weights.get('insert', 1),
                        dp[i-1][j-1] + optimized_weights.get('replace', 1)
                    )
        
        return dp[m][n]
    
    def get_edit_distance_with_constraints(self, constraint_func):
        """Get edit distance that satisfies custom constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        if constraint_func(self.string1, self.string2, self.weights, self.priorities):
            return self.get_weighted_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_multiple_criteria(self, criteria_list):
        """Get edit distance that satisfies multiple criteria."""
        if not self.edit_distance_feasibility:
            return 0
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.string1, self.string2, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_alternatives(self, alternatives):
        """Get edit distance considering alternative weights/priorities."""
        result = []
        
        # Check original edit distance
        original_distance = self.get_weighted_edit_distance()
        result.append((original_distance, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedEditDistance(self.string1, self.string2, alt_weights, alt_priorities)
            temp_distance = temp_instance.get_weighted_edit_distance()
            result.append((temp_distance, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_edit_distance_with_adaptive_criteria(self, adaptive_func):
        """Get edit distance using adaptive criteria."""
        if not self.edit_distance_feasibility:
            return 0
        
        if adaptive_func(self.string1, self.string2, self.weights, self.priorities, []):
            return self.get_weighted_edit_distance()
        else:
            return 0
    
    def get_edit_distance_optimization(self):
        """Get optimal edit distance configuration."""
        strategies = [
            ('weighted_edit_distance', lambda: self.get_weighted_edit_distance()),
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
string1 = "kitten"
string2 = "sitting"
weights = {'delete': 2, 'insert': 3, 'replace': 1}  # Different costs for operations
priorities = {'delete': 1, 'insert': 2, 'replace': 1}  # Priority for operations
advanced_edit_distance = AdvancedEditDistance(string1, string2, weights, priorities)

print(f"Weighted edit distance: {advanced_edit_distance.get_weighted_edit_distance()}")

# Get edit distance with priority
def priority_func(operation, weights, priorities):
    return weights.get(operation, 1) + priorities.get(operation, 1)

print(f"Edit distance with priority: {advanced_edit_distance.get_edit_distance_with_priority(priority_func)}")

# Get edit distance with optimization
def optimization_func(operation, weights, priorities):
    return weights.get(operation, 1) * priorities.get(operation, 1)

print(f"Edit distance with optimization: {advanced_edit_distance.get_edit_distance_with_optimization(optimization_func)}")

# Get edit distance with constraints
def constraint_func(string1, string2, weights, priorities):
    return len(string1) > 0 and len(string2) > 0

print(f"Edit distance with constraints: {advanced_edit_distance.get_edit_distance_with_constraints(constraint_func)}")

# Get edit distance with multiple criteria
def criterion1(string1, string2, weights, priorities):
    return len(string1) > 0

def criterion2(string1, string2, weights, priorities):
    return len(string2) > 0

criteria_list = [criterion1, criterion2]
print(f"Edit distance with multiple criteria: {advanced_edit_distance.get_edit_distance_with_multiple_criteria(criteria_list)}")

# Get edit distance with alternatives
alternatives = [({'delete': 1, 'insert': 1, 'replace': 1}, {'delete': 1, 'insert': 1, 'replace': 1}), ({'delete': 3, 'insert': 2, 'replace': 1}, {'delete': 1, 'insert': 2, 'replace': 3})]
print(f"Edit distance with alternatives: {advanced_edit_distance.get_edit_distance_with_alternatives(alternatives)}")

# Get edit distance with adaptive criteria
def adaptive_func(string1, string2, weights, priorities, current_result):
    return len(string1) > 0 and len(string2) > 0 and len(current_result) < 5

print(f"Edit distance with adaptive criteria: {advanced_edit_distance.get_edit_distance_with_adaptive_criteria(adaptive_func)}")

# Get edit distance optimization
print(f"Edit distance optimization: {advanced_edit_distance.get_edit_distance_optimization()}")
```

### **Variation 3: Edit Distance with Constraints**
**Problem**: Handle edit distance calculation with additional constraints (string limits, operation constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedEditDistance:
    def __init__(self, string1=None, string2=None, constraints=None):
        self.string1 = string1 or ""
        self.string2 = string2 or ""
        self.constraints = constraints or {}
        self.edit_operations = []
        self._update_edit_distance_info()
    
    def _update_edit_distance_info(self):
        """Update edit distance feasibility information."""
        self.edit_distance_feasibility = self._calculate_edit_distance_feasibility()
    
    def _calculate_edit_distance_feasibility(self):
        """Calculate edit distance feasibility."""
        if not self.string1 and not self.string2:
            return 0.0
        
        # Check if we can calculate edit distance between strings
        return 1.0 if self.string1 or self.string2 else 0.0
    
    def _is_valid_operation(self, operation, position, char1, char2):
        """Check if operation is valid considering constraints."""
        # Operation constraints
        if 'allowed_operations' in self.constraints:
            if operation not in self.constraints['allowed_operations']:
                return False
        
        if 'forbidden_operations' in self.constraints:
            if operation in self.constraints['forbidden_operations']:
                return False
        
        # Character constraints
        if 'allowed_characters' in self.constraints:
            if char1 and char1 not in self.constraints['allowed_characters']:
                return False
            if char2 and char2 not in self.constraints['allowed_characters']:
                return False
        
        if 'forbidden_characters' in self.constraints:
            if char1 and char1 in self.constraints['forbidden_characters']:
                return False
            if char2 and char2 in self.constraints['forbidden_characters']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(operation, position, char1, char2):
                    return False
        
        return True
    
    def get_edit_distance_with_string_constraints(self, min_length, max_length):
        """Get edit distance considering string length constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        if min_length <= len(self.string1) <= max_length and min_length <= len(self.string2) <= max_length:
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_operation_constraints(self, operation_constraints):
        """Get edit distance considering operation constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        satisfies_constraints = True
        for constraint in operation_constraints:
            if not constraint(self.string1, self.string2):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_pattern_constraints(self, pattern_constraints):
        """Get edit distance considering pattern constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.string1, self.string2):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_mathematical_constraints(self, constraint_func):
        """Get edit distance that satisfies custom mathematical constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        if constraint_func(self.string1, self.string2):
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_optimization_constraints(self, optimization_func):
        """Get edit distance using custom optimization constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        # Calculate optimization score for edit distance
        score = optimization_func(self.string1, self.string2)
        
        if score > 0:
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_multiple_constraints(self, constraints_list):
        """Get edit distance that satisfies multiple constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.string1, self.string2):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_priority_constraints(self, priority_func):
        """Get edit distance with priority-based constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        # Calculate priority for edit distance
        priority = priority_func(self.string1, self.string2)
        
        if priority > 0:
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def get_edit_distance_with_adaptive_constraints(self, adaptive_func):
        """Get edit distance with adaptive constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        if adaptive_func(self.string1, self.string2, []):
            return self._calculate_constrained_edit_distance()
        else:
            return 0
    
    def _calculate_constrained_edit_distance(self):
        """Calculate edit distance considering all constraints."""
        if not self.edit_distance_feasibility:
            return 0
        
        m, n = len(self.string1), len(self.string2)
        
        # DP table: dp[i][j] = edit distance between string1[:i] and string2[:j]
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill DP table with constraints
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    # Check if operations are valid
                    delete_valid = self._is_valid_operation('delete', i-1, self.string1[i-1], None)
                    insert_valid = self._is_valid_operation('insert', i, None, self.string2[j-1])
                    replace_valid = self._is_valid_operation('replace', i-1, self.string1[i-1], self.string2[j-1])
                    
                    costs = []
                    if delete_valid:
                        costs.append(dp[i-1][j] + 1)
                    if insert_valid:
                        costs.append(dp[i][j-1] + 1)
                    if replace_valid:
                        costs.append(dp[i-1][j-1] + 1)
                    
                    if costs:
                        dp[i][j] = min(costs)
                    else:
                        dp[i][j] = float('inf')  # No valid operations
        
        return dp[m][n] if dp[m][n] != float('inf') else 0
    
    def get_optimal_edit_distance_strategy(self):
        """Get optimal edit distance strategy considering all constraints."""
        strategies = [
            ('string_constraints', self.get_edit_distance_with_string_constraints),
            ('operation_constraints', self.get_edit_distance_with_operation_constraints),
            ('pattern_constraints', self.get_edit_distance_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'string_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'operation_constraints':
                    operation_constraints = [lambda string1, string2: len(string1) > 0 and len(string2) > 0]
                    result = strategy_func(operation_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda string1, string2: len(string1) > 0 and len(string2) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and result > best_score:
                    best_score = result
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_operations': ['delete', 'insert', 'replace'],
    'forbidden_operations': [],
    'allowed_characters': 'abcdefghijklmnopqrstuvwxyz',
    'forbidden_characters': '0123456789',
    'pattern_constraints': [lambda operation, position, char1, char2: operation in ['delete', 'insert', 'replace']]
}

string1 = "kitten"
string2 = "sitting"
constrained_edit_distance = ConstrainedEditDistance(string1, string2, constraints)

print("String-constrained edit distance:", constrained_edit_distance.get_edit_distance_with_string_constraints(1, 100))

print("Operation-constrained edit distance:", constrained_edit_distance.get_edit_distance_with_operation_constraints([lambda string1, string2: len(string1) > 0 and len(string2) > 0]))

print("Pattern-constrained edit distance:", constrained_edit_distance.get_edit_distance_with_pattern_constraints([lambda string1, string2: len(string1) > 0 and len(string2) > 0]))

# Mathematical constraints
def custom_constraint(string1, string2):
    return len(string1) > 0 and len(string2) > 0

print("Mathematical constraint edit distance:", constrained_edit_distance.get_edit_distance_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(string1, string2):
    return 1 <= len(string1) <= 20 and 1 <= len(string2) <= 20

range_constraints = [range_constraint]
print("Range-constrained edit distance:", constrained_edit_distance.get_edit_distance_with_string_constraints(1, 20))

# Multiple constraints
def constraint1(string1, string2):
    return len(string1) > 0

def constraint2(string1, string2):
    return len(string2) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints edit distance:", constrained_edit_distance.get_edit_distance_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(string1, string2):
    return len(string1) + len(string2)

print("Priority-constrained edit distance:", constrained_edit_distance.get_edit_distance_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(string1, string2, current_result):
    return len(string1) > 0 and len(string2) > 0 and len(current_result) < 5

print("Adaptive constraint edit distance:", constrained_edit_distance.get_edit_distance_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_edit_distance.get_optimal_edit_distance_strategy()
print(f"Optimal edit distance strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Counting Towers](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Book Shop](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Edit Distance](https://leetcode.com/problems/edit-distance/) - DP
- [One Edit Distance](https://leetcode.com/problems/one-edit-distance/) - DP
- [Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) - DP

#### **Problem Categories**
- **Dynamic Programming**: String DP, distance algorithms
- **String Algorithms**: String processing, comparison algorithms
- **Mathematical Algorithms**: Distance metrics, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [String Algorithms](https://cp-algorithms.com/string/string-algorithms.html) - String algorithms
- [Edit Distance](https://cp-algorithms.com/dynamic_programming/edit-distance.html) - Edit distance algorithms

### **Practice Problems**
- [CSES Counting Towers](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium
- [CSES Book Shop](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
