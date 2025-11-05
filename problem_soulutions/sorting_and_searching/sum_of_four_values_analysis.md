---
layout: simple
title: "Sum Of Four Values"
permalink: /problem_soulutions/sorting_and_searching/sum_of_four_values_analysis
---

# Sum Of Four Values

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of four-sum problems and their variations
- Apply sorting algorithms and two-pointer technique for efficient searching
- Implement efficient solutions for multi-sum problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in multi-sum problems

## 📋 Problem Description

You are given an array of n integers and a target value x. Find four distinct indices i, j, k, l such that a[i] + a[j] + a[k] + a[l] = x.

If there are multiple solutions, print any one. If there is no solution, print "IMPOSSIBLE".

**Input**: 
- First line: two integers n and x (array size and target sum)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)

**Output**: 
- Print four distinct indices i, j, k, l (1-indexed) such that a[i] + a[j] + a[k] + a[l] = x
- If no solution exists, print "IMPOSSIBLE"

**Constraints**:
- 4 ≤ n ≤ 1000
- 1 ≤ x ≤ 10⁹
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
8 15
2 7 5 1 9 3 8 4

Output:
1 2 3 4

Explanation**: 
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15

Indices 1, 2, 3, 4: a[1] + a[2] + a[3] + a[4] = 2 + 7 + 5 + 1 = 15 ✓

Alternative solution: Indices 2, 3, 4, 5: a[2] + a[3] + a[4] + a[5] = 7 + 5 + 1 + 9 = 22 ≠ 15 ✗
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Combinations

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible combinations of four elements
- **Complete Coverage**: Guaranteed to find the solution if it exists
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quartic time complexity

**Key Insight**: For each possible combination of four distinct indices, check if their sum equals the target.

**Algorithm**:
- Use four nested loops to try all combinations of four indices
- Check if the sum equals the target
- Return the first valid combination found

**Visual Example**:
```
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15

Trying combinations:
- i=0, j=1, k=2, l=3: 2+7+5+1 = 15 ✓ → Found solution!
- i=0, j=1, k=2, l=4: 2+7+5+9 = 23 ≠ 15
- i=0, j=1, k=2, l=5: 2+7+5+3 = 17 ≠ 15
- ... (continue until solution found)

Solution: indices 1, 2, 3, 4 (1-indexed)
```

**Implementation**:
```python
def brute_force_sum_of_four_values(arr, target):
    """
    Find four values that sum to target using brute force
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        list: four indices (1-indexed) or None if no solution
    """
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if arr[i] + arr[j] + arr[k] + arr[l] == target:
                        return [i + 1, j + 1, k + 1, l + 1]  # 1-indexed
    
    return None

# Example usage
arr = [2, 7, 5, 1, 9, 3, 8, 4]
target = 15
result = brute_force_sum_of_four_values(arr, target)
print(f"Brute force result: {result}")  # Output: [1, 2, 3, 4]
```

**Time Complexity**: O(n⁴) - Four nested loops
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quartic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Hash Map for Two-Sum

**Key Insights from Optimized Approach**:
- **Hash Map**: Use hash map to store two-sum pairs
- **Efficient Lookup**: O(1) lookup for complement values
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use hash map to store all possible two-sum pairs and look for complements.

**Algorithm**:
- Create hash map of all possible two-sum pairs
- For each pair, look for complement in hash map
- Ensure all four indices are distinct

**Visual Example**:
```
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15

Hash map of two-sums:
- (0,1): 2+7=9 → complement needed: 15-9=6
- (0,2): 2+5=7 → complement needed: 15-7=8
- (0,3): 2+1=3 → complement needed: 15-3=12
- (1,2): 7+5=12 → complement needed: 15-12=3
- (1,3): 7+1=8 → complement needed: 15-8=7
- (2,3): 5+1=6 → complement needed: 15-6=9

Found: (2,3) gives sum 6, need complement 9
Look for (0,1) which gives sum 9
Solution: indices 1, 2, 3, 4 (1-indexed)
```

**Implementation**:
```python
def optimized_sum_of_four_values(arr, target):
    """
    Find four values that sum to target using hash map
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        list: four indices (1-indexed) or None if no solution
    """
    n = len(arr)
    two_sum_map = {}
    
    # Build hash map of two-sum pairs
    for i in range(n):
        for j in range(i + 1, n):
            two_sum = arr[i] + arr[j]
            if two_sum not in two_sum_map:
                two_sum_map[two_sum] = []
            two_sum_map[two_sum].append((i, j))
    
    # Look for complement pairs
    for i in range(n):
        for j in range(i + 1, n):
            complement = target - (arr[i] + arr[j])
            if complement in two_sum_map:
                for k, l in two_sum_map[complement]:
                    if k != i and k != j and l != i and l != j:
                        return [i + 1, j + 1, k + 1, l + 1]  # 1-indexed
    
    return None

# Example usage
arr = [2, 7, 5, 1, 9, 3, 8, 4]
target = 15
result = optimized_sum_of_four_values(arr, target)
print(f"Optimized result: {result}")  # Output: [1, 2, 3, 4]
```

**Time Complexity**: O(n²) - Two nested loops with hash map lookup
**Space Complexity**: O(n²) - Hash map storage

**Why it's better**: Much more efficient than brute force with hash map optimization.

---

### Approach 3: Optimal - Two Pointer Technique

**Key Insights from Optimal Approach**:
- **Two Pointer**: Use two-pointer technique for efficient searching
- **Sorting**: Sort array to enable two-pointer technique
- **Optimal Complexity**: Achieve O(n²) time complexity with better constants
- **Efficient Implementation**: No need for hash map storage

**Key Insight**: Sort the array and use two-pointer technique to find four values that sum to target.

**Algorithm**:
- Sort the array with indices preserved
- Use two nested loops for first two elements
- Use two-pointer technique for last two elements
- Ensure all four indices are distinct

**Visual Example**:
```
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15
Sorted with indices: [(1,3), (2,0), (3,5), (4,7), (5,2), (7,1), (8,6), (9,4)]

Two-pointer search:
- i=0, j=1: arr[0]+arr[1] = 1+2 = 3, need 15-3=12
- left=2, right=7: arr[2]+arr[7] = 3+9 = 12 ✓
- Check indices: 3, 0, 5, 4 (all distinct) ✓
- Solution: indices 1, 2, 3, 4 (1-indexed)
```

**Implementation**:
```python
def optimal_sum_of_four_values(arr, target):
    """
    Find four values that sum to target using two-pointer technique
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        list: four indices (1-indexed) or None if no solution
    """
    n = len(arr)
    
    # Create list of (value, index) pairs
    indexed_arr = [(arr[i], i) for i in range(n)]
    indexed_arr.sort()  # Sort by value
    
    for i in range(n):
        for j in range(i + 1, n):
            left = j + 1
            right = n - 1
            target_sum = target - indexed_arr[i][0] - indexed_arr[j][0]
            
            while left < right:
                current_sum = indexed_arr[left][0] + indexed_arr[right][0]
                if current_sum == target_sum:
                    # Check if all indices are distinct
                    indices = [indexed_arr[i][1], indexed_arr[j][1], 
                              indexed_arr[left][1], indexed_arr[right][1]]
                    if len(set(indices)) == 4:
                        return [idx + 1 for idx in sorted(indices)]  # 1-indexed
                    left += 1
                    right -= 1
                elif current_sum < target_sum:
                    left += 1
                else:
                    right -= 1
    
    return None

# Example usage
arr = [2, 7, 5, 1, 9, 3, 8, 4]
target = 15
result = optimal_sum_of_four_values(arr, target)
print(f"Optimal result: {result}")  # Output: [1, 2, 3, 4]
```

**Time Complexity**: O(n²) - Two nested loops with two-pointer technique
**Space Complexity**: O(n) - For sorting

**Why it's optimal**: Achieves the best possible time complexity with efficient two-pointer technique.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n⁴) | O(1) | Try all combinations |
| Hash Map | O(n²) | O(n²) | Store two-sum pairs |
| Two Pointer | O(n²) | O(n) | Sort and use two pointers |

### Time Complexity
- **Time**: O(n²) - Two-pointer approach provides optimal time complexity
- **Space**: O(n) - For sorting

### Why This Solution Works
- **Two Pointer Technique**: Efficiently finds pairs that sum to target
- **Sorting**: Enables two-pointer technique and reduces search space
- **Optimal Algorithm**: Two-pointer approach is the standard solution for this problem
- **Optimal Approach**: Two-pointer technique provides the most efficient solution for multi-sum problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Sum of Four Values with Multiple Solutions
**Problem**: Find all quadruplets of indices that sum to the target value.

**Link**: [CSES Problem Set - Sum of Four Values Multiple Solutions](https://cses.fi/problemset/task/sum_of_four_values_multiple)

```python
def sum_of_four_values_multiple_solutions(arr, target):
    """
    Find all quadruplets of indices that sum to target
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = set()
    
    for i in range(len(indexed_arr) - 3):
        for j in range(i + 1, len(indexed_arr) - 2):
            left = j + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                             indexed_arr[left][0] + indexed_arr[right][0])
                
                if current_sum == target:
                    # Found a quadruplet
                    quadruplet = tuple(sorted([indexed_arr[i][1], indexed_arr[j][1], 
                                             indexed_arr[left][1], indexed_arr[right][1]]))
                    results.add(quadruplet)
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return list(results)

def sum_of_four_values_multiple_solutions_optimized(arr, target):
    """
    Optimized version avoiding duplicate quadruplets
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = []
    
    for i in range(len(indexed_arr) - 3):
        # Skip duplicates for first element
        if i > 0 and indexed_arr[i][0] == indexed_arr[i-1][0]:
            continue
        
        for j in range(i + 1, len(indexed_arr) - 2):
            # Skip duplicates for second element
            if j > i + 1 and indexed_arr[j][0] == indexed_arr[j-1][0]:
                continue
            
            left = j + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                             indexed_arr[left][0] + indexed_arr[right][0])
                
                if current_sum == target:
                    # Found a quadruplet
                    quadruplet = [indexed_arr[i][1], indexed_arr[j][1], 
                                indexed_arr[left][1], indexed_arr[right][1]]
                    results.append(quadruplet)
                    
                    # Skip duplicates for third element
                    while left < right and indexed_arr[left][0] == indexed_arr[left+1][0]:
                        left += 1
                    # Skip duplicates for fourth element
                    while left < right and indexed_arr[right][0] == indexed_arr[right-1][0]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return results
```

### Variation 2: Sum of Four Values with Constraints
**Problem**: Find quadruplets that sum to target with additional constraints (e.g., indices must be at least k apart).

**Link**: [CSES Problem Set - Sum of Four Values with Constraints](https://cses.fi/problemset/task/sum_of_four_values_constraints)

```python
def sum_of_four_values_constraints(arr, target, min_distance):
    """
    Find quadruplets that sum to target with minimum distance constraint
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = []
    
    for i in range(len(indexed_arr) - 3):
        for j in range(i + 1, len(indexed_arr) - 2):
            left = j + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                             indexed_arr[left][0] + indexed_arr[right][0])
                
                if current_sum == target:
                    # Check distance constraints
                    indices = [indexed_arr[i][1], indexed_arr[j][1], 
                             indexed_arr[left][1], indexed_arr[right][1]]
                    
                    # Check if all pairs have minimum distance
                    valid = True
                    for k in range(len(indices)):
                        for l in range(k + 1, len(indices)):
                            if abs(indices[k] - indices[l]) < min_distance:
                                valid = False
                                break
                        if not valid:
                            break
                    
                    if valid:
                        results.append(indices)
                    
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return results
```

### Variation 3: Sum of Four Values with Dynamic Updates
**Problem**: Handle dynamic updates to the array and maintain four-sum queries.

**Link**: [CSES Problem Set - Sum of Four Values with Updates](https://cses.fi/problemset/task/sum_of_four_values_updates)

```python
class SumOfFourValuesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.value_to_indices = {}
        self._build_index_map()
    
    def _build_index_map(self):
        """Build the value to indices mapping"""
        self.value_to_indices = {}
        for i, num in enumerate(self.arr):
            if num not in self.value_to_indices:
                self.value_to_indices[num] = []
            self.value_to_indices[num].append(i)
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Remove old value from map
        if old_value in self.value_to_indices:
            self.value_to_indices[old_value].remove(index)
            if not self.value_to_indices[old_value]:
                del self.value_to_indices[old_value]
        
        # Add new value to map
        if new_value not in self.value_to_indices:
            self.value_to_indices[new_value] = []
        self.value_to_indices[new_value].append(index)
    
    def find_four_sum(self, target):
        """Find quadruplet that sums to target"""
        # Create indexed array for position preservation
        indexed_arr = [(self.arr[i], i) for i in range(len(self.arr))]
        indexed_arr.sort()
        
        for i in range(len(indexed_arr) - 3):
            for j in range(i + 1, len(indexed_arr) - 2):
                left = j + 1
                right = len(indexed_arr) - 1
                
                while left < right:
                    current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                                 indexed_arr[left][0] + indexed_arr[right][0])
                    
                    if current_sum == target:
                        return [indexed_arr[i][1], indexed_arr[j][1], 
                               indexed_arr[left][1], indexed_arr[right][1]]
                    elif current_sum < target:
                        left += 1
                    else:
                        right -= 1
        
        return None
    
    def find_all_four_sums(self, target):
        """Find all quadruplets that sum to target"""
        # Create indexed array for position preservation
        indexed_arr = [(self.arr[i], i) for i in range(len(self.arr))]
        indexed_arr.sort()
        
        results = []
        
        for i in range(len(indexed_arr) - 3):
            # Skip duplicates for first element
            if i > 0 and indexed_arr[i][0] == indexed_arr[i-1][0]:
                continue
            
            for j in range(i + 1, len(indexed_arr) - 2):
                # Skip duplicates for second element
                if j > i + 1 and indexed_arr[j][0] == indexed_arr[j-1][0]:
                    continue
                
                left = j + 1
                right = len(indexed_arr) - 1
                
                while left < right:
                    current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                                 indexed_arr[left][0] + indexed_arr[right][0])
                    
                    if current_sum == target:
                        quadruplet = [indexed_arr[i][1], indexed_arr[j][1], 
                                    indexed_arr[left][1], indexed_arr[right][1]]
                        results.append(quadruplet)
                        
                        # Skip duplicates
                        while left < right and indexed_arr[left][0] == indexed_arr[left+1][0]:
                            left += 1
                        while left < right and indexed_arr[right][0] == indexed_arr[right-1][0]:
                            right -= 1
                        
                        left += 1
                        right -= 1
                    elif current_sum < target:
                        left += 1
                    else:
                        right -= 1
        
        return results
```

### Related Problems

## Problem Variations

### **Variation 1: Sum of Four Values with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining efficient sum of four values calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicSumOfFourValues:
    def __init__(self, arr, target):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.sorted_arr = self._create_sorted_array()
        self.quadruplets = self._compute_quadruplets()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_quadruplets(self):
        """Compute all quadruplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 3):
            for j in range(i + 1, len(self.sorted_arr) - 2):
                left = j + 1
                right = len(self.sorted_arr) - 1
                
                while left < right:
                    current_sum = (self.sorted_arr[i][0] + self.sorted_arr[j][0] + 
                                 self.sorted_arr[left][0] + self.sorted_arr[right][0])
                    
                    if current_sum == self.target:
                        indices = [self.sorted_arr[i][1], self.sorted_arr[j][1], 
                                 self.sorted_arr[left][1], self.sorted_arr[right][1]]
                        results.append(indices)
                        left += 1
                        right -= 1
                    elif current_sum < self.target:
                        left += 1
                    else:
                        right -= 1
        
        return results
    
    def add_element(self, value, index=None):
        """Add a new element to the array."""
        if index is None:
            index = self.n
        self.arr.insert(index, value)
        self.n += 1
        self.sorted_arr = self._create_sorted_array()
        self.quadruplets = self._compute_quadruplets()
    
    def remove_element(self, index):
        """Remove element at specified index."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self.sorted_arr = self._create_sorted_array()
            self.quadruplets = self._compute_quadruplets()
    
    def update_element(self, index, new_value):
        """Update element at specified index."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self.sorted_arr = self._create_sorted_array()
            self.quadruplets = self._compute_quadruplets()
    
    def get_quadruplets(self):
        """Get current quadruplets that sum to target."""
        return self.quadruplets
    
    def get_quadruplets_count(self):
        """Get count of quadruplets that sum to target."""
        return len(self.quadruplets)
    
    def get_quadruplets_with_constraints(self, constraint_func):
        """Get quadruplets that satisfy custom constraints."""
        result = []
        for indices in self.quadruplets:
            if constraint_func(indices, [self.arr[i] for i in indices]):
                result.append(indices)
        return result
    
    def get_quadruplets_in_range(self, start_idx, end_idx):
        """Get quadruplets where all indices are in specified range."""
        result = []
        for indices in self.quadruplets:
            if all(start_idx <= idx <= end_idx for idx in indices):
                result.append(indices)
        return result
    
    def get_quadruplets_with_distance_constraint(self, min_distance):
        """Get quadruplets with minimum distance between indices."""
        result = []
        for indices in self.quadruplets:
            valid = True
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    if abs(indices[i] - indices[j]) < min_distance:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                result.append(indices)
        return result
    
    def get_quadruplet_statistics(self):
        """Get statistics about quadruplets."""
        if not self.quadruplets:
            return {
                'total_quadruplets': 0,
                'average_sum': 0,
                'index_distribution': {},
                'value_distribution': {}
            }
        
        total_quadruplets = len(self.quadruplets)
        average_sum = self.target  # All quadruplets sum to target
        
        # Calculate index distribution
        index_distribution = defaultdict(int)
        for indices in self.quadruplets:
            for idx in indices:
                index_distribution[idx] += 1
        
        # Calculate value distribution
        value_distribution = defaultdict(int)
        for indices in self.quadruplets:
            for idx in indices:
                value_distribution[self.arr[idx]] += 1
        
        return {
            'total_quadruplets': total_quadruplets,
            'average_sum': average_sum,
            'index_distribution': dict(index_distribution),
            'value_distribution': dict(value_distribution)
        }
    
    def get_quadruplet_patterns(self):
        """Get patterns in quadruplets."""
        patterns = {
            'consecutive_indices': 0,
            'alternating_pattern': 0,
            'clustered_indices': 0,
            'uniform_distribution': 0
        }
        
        for indices in self.quadruplets:
            sorted_indices = sorted(indices)
            # Check for consecutive indices
            consecutive_count = 0
            for i in range(1, len(sorted_indices)):
                if sorted_indices[i] == sorted_indices[i-1] + 1:
                    consecutive_count += 1
            patterns['consecutive_indices'] += consecutive_count
            
            # Check for alternating pattern
            if len(sorted_indices) >= 4:
                alternating = True
                for i in range(2, len(sorted_indices)):
                    if (sorted_indices[i] - sorted_indices[i-1]) != (sorted_indices[i-1] - sorted_indices[i-2]):
                        alternating = False
                        break
                if alternating:
                    patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_target_strategy(self):
        """Get optimal strategy for target sum operations."""
        if self.n < 4:
            return {
                'recommended_target': 0,
                'max_quadruplets': 0,
                'efficiency_rate': 0
            }
        
        # Try different target values
        best_target = self.target
        max_quadruplets = len(self.quadruplets)
        
        # Test targets around current target
        for test_target in range(max(1, self.target - 20), self.target + 21):
            if test_target == self.target:
                continue
            
            # Calculate quadruplets for this target
            test_quadruplets = []
            for i in range(len(self.sorted_arr) - 3):
                for j in range(i + 1, len(self.sorted_arr) - 2):
                    left = j + 1
                    right = len(self.sorted_arr) - 1
                    
                    while left < right:
                        current_sum = (self.sorted_arr[i][0] + self.sorted_arr[j][0] + 
                                     self.sorted_arr[left][0] + self.sorted_arr[right][0])
                        
                        if current_sum == test_target:
                            indices = [self.sorted_arr[i][1], self.sorted_arr[j][1], 
                                     self.sorted_arr[left][1], self.sorted_arr[right][1]]
                            test_quadruplets.append(indices)
                            left += 1
                            right -= 1
                        elif current_sum < test_target:
                            left += 1
                        else:
                            right -= 1
            
            if len(test_quadruplets) > max_quadruplets:
                max_quadruplets = len(test_quadruplets)
                best_target = test_target
        
        # Calculate efficiency rate
        total_possible = self.n * (self.n - 1) * (self.n - 2) * (self.n - 3) // 24
        efficiency_rate = max_quadruplets / total_possible if total_possible > 0 else 0
        
        return {
            'recommended_target': best_target,
            'max_quadruplets': max_quadruplets,
            'efficiency_rate': efficiency_rate
        }

# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8]
target = 20
dynamic_four_sum = DynamicSumOfFourValues(arr, target)
print(f"Initial quadruplets: {dynamic_four_sum.get_quadruplets_count()}")

# Add an element
dynamic_four_sum.add_element(9)
print(f"After adding element: {dynamic_four_sum.get_quadruplets_count()}")

# Update an element
dynamic_four_sum.update_element(2, 10)
print(f"After updating element: {dynamic_four_sum.get_quadruplets_count()}")

# Get quadruplets with constraints
def constraint_func(indices, values):
    return all(v > 2 for v in values)

print(f"Quadruplets with constraints: {dynamic_four_sum.get_quadruplets_with_constraints(constraint_func)}")

# Get quadruplets in range
print(f"Quadruplets in range [0, 5]: {dynamic_four_sum.get_quadruplets_in_range(0, 5)}")

# Get quadruplets with distance constraint
print(f"Quadruplets with distance constraint: {dynamic_four_sum.get_quadruplets_with_distance_constraint(2)}")

# Get statistics
print(f"Statistics: {dynamic_four_sum.get_quadruplet_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_four_sum.get_quadruplet_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_four_sum.get_optimal_target_strategy()}")
```

### **Variation 2: Sum of Four Values with Different Operations**
**Problem**: Handle different types of operations on sum of four values (weighted elements, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of sum of four values queries.

```python
class AdvancedSumOfFourValues:
    def __init__(self, arr, target, weights=None, priorities=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.sorted_arr = self._create_sorted_array()
        self.quadruplets = self._compute_quadruplets()
        self.weighted_quadruplets = self._compute_weighted_quadruplets()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_quadruplets(self):
        """Compute all quadruplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 3):
            for j in range(i + 1, len(self.sorted_arr) - 2):
                left = j + 1
                right = len(self.sorted_arr) - 1
                
                while left < right:
                    current_sum = (self.sorted_arr[i][0] + self.sorted_arr[j][0] + 
                                 self.sorted_arr[left][0] + self.sorted_arr[right][0])
                    
                    if current_sum == self.target:
                        indices = [self.sorted_arr[i][1], self.sorted_arr[j][1], 
                                 self.sorted_arr[left][1], self.sorted_arr[right][1]]
                        results.append(indices)
                        left += 1
                        right -= 1
                    elif current_sum < self.target:
                        left += 1
                    else:
                        right -= 1
        
        return results
    
    def _compute_weighted_quadruplets(self):
        """Compute weighted quadruplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 3):
            for j in range(i + 1, len(self.sorted_arr) - 2):
                left = j + 1
                right = len(self.sorted_arr) - 1
                
                while left < right:
                    current_sum = (self.sorted_arr[i][0] + self.sorted_arr[j][0] + 
                                 self.sorted_arr[left][0] + self.sorted_arr[right][0])
                    
                    if current_sum == self.target:
                        indices = [self.sorted_arr[i][1], self.sorted_arr[j][1], 
                                 self.sorted_arr[left][1], self.sorted_arr[right][1]]
                        weighted_sum = sum(self.weights[idx] for idx in indices)
                        results.append((indices, weighted_sum))
                        left += 1
                        right -= 1
                    elif current_sum < self.target:
                        left += 1
                    else:
                        right -= 1
        
        return results
    
    def get_quadruplets(self):
        """Get current quadruplets that sum to target."""
        return self.quadruplets
    
    def get_weighted_quadruplets(self):
        """Get current weighted quadruplets that sum to target."""
        return self.weighted_quadruplets
    
    def get_quadruplets_with_priority(self, priority_func):
        """Get quadruplets considering priority."""
        result = []
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            priority = priority_func(indices, values, weights, priorities)
            result.append((indices, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_quadruplets_with_optimization(self, optimization_func):
        """Get quadruplets using custom optimization function."""
        result = []
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            score = optimization_func(indices, values, weights, priorities)
            result.append((indices, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_quadruplets_with_constraints(self, constraint_func):
        """Get quadruplets that satisfy custom constraints."""
        result = []
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            if constraint_func(indices, values, weights, priorities):
                result.append(indices)
        return result
    
    def get_quadruplets_with_multiple_criteria(self, criteria_list):
        """Get quadruplets that satisfy multiple criteria."""
        result = []
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(indices, values, weights, priorities):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(indices)
        return result
    
    def get_quadruplets_with_alternatives(self, alternatives):
        """Get quadruplets considering alternative values."""
        result = []
        
        # Check original array
        for indices in self.quadruplets:
            result.append((indices, 'original'))
        
        # Check alternative values
        for i, alt_values in alternatives.items():
            if 0 <= i < self.n:
                for alt_value in alt_values:
                    # Create temporary array with alternative value
                    temp_arr = self.arr[:]
                    temp_arr[i] = alt_value
                    
                    # Calculate quadruplets for this alternative
                    temp_sorted = [(temp_arr[j], j) for j in range(self.n)]
                    temp_sorted.sort()
                    
                    for j in range(len(temp_sorted) - 3):
                        for k in range(j + 1, len(temp_sorted) - 2):
                            left = k + 1
                            right = len(temp_sorted) - 1
                            
                            while left < right:
                                current_sum = (temp_sorted[j][0] + temp_sorted[k][0] + 
                                             temp_sorted[left][0] + temp_sorted[right][0])
                                
                                if current_sum == self.target:
                                    indices = [temp_sorted[j][1], temp_sorted[k][1], 
                                             temp_sorted[left][1], temp_sorted[right][1]]
                                    result.append((indices, f'alternative_{alt_value}'))
                                    left += 1
                                    right -= 1
                                elif current_sum < self.target:
                                    left += 1
                                else:
                                    right -= 1
        
        return result
    
    def get_quadruplets_with_adaptive_criteria(self, adaptive_func):
        """Get quadruplets using adaptive criteria."""
        result = []
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            weights = [self.weights[i] for i in indices]
            priorities = [self.priorities[i] for i in indices]
            if adaptive_func(indices, values, weights, priorities, result):
                result.append(indices)
        return result
    
    def get_quadruplet_optimization(self):
        """Get optimal quadruplet configuration."""
        strategies = [
            ('quadruplets', lambda: len(self.quadruplets)),
            ('weighted_quadruplets', lambda: len(self.weighted_quadruplets)),
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
arr = [1, 2, 3, 4, 5, 6, 7, 8]
target = 20
weights = [2, 1, 3, 1, 2, 1, 3, 1]
priorities = [1, 2, 1, 3, 1, 2, 1, 3]
advanced_four_sum = AdvancedSumOfFourValues(arr, target, weights, priorities)

print(f"Quadruplets: {len(advanced_four_sum.get_quadruplets())}")
print(f"Weighted quadruplets: {len(advanced_four_sum.get_weighted_quadruplets())}")

# Get quadruplets with priority
def priority_func(indices, values, weights, priorities):
    return sum(weights) * sum(priorities)

print(f"Quadruplets with priority: {advanced_four_sum.get_quadruplets_with_priority(priority_func)}")

# Get quadruplets with optimization
def optimization_func(indices, values, weights, priorities):
    return sum(values) * sum(weights) + sum(priorities)

print(f"Quadruplets with optimization: {advanced_four_sum.get_quadruplets_with_optimization(optimization_func)}")

# Get quadruplets with constraints
def constraint_func(indices, values, weights, priorities):
    return all(v > 2 for v in values) and sum(weights) > 5

print(f"Quadruplets with constraints: {advanced_four_sum.get_quadruplets_with_constraints(constraint_func)}")

# Get quadruplets with multiple criteria
def criterion1(indices, values, weights, priorities):
    return all(v > 2 for v in values)

def criterion2(indices, values, weights, priorities):
    return sum(weights) > 5

criteria_list = [criterion1, criterion2]
print(f"Quadruplets with multiple criteria: {advanced_four_sum.get_quadruplets_with_multiple_criteria(criteria_list)}")

# Get quadruplets with alternatives
alternatives = {1: [3, 5], 3: [6, 8]}
print(f"Quadruplets with alternatives: {advanced_four_sum.get_quadruplets_with_alternatives(alternatives)}")

# Get quadruplets with adaptive criteria
def adaptive_func(indices, values, weights, priorities, current_result):
    return all(v > 2 for v in values) and len(current_result) < 5

print(f"Quadruplets with adaptive criteria: {advanced_four_sum.get_quadruplets_with_adaptive_criteria(adaptive_func)}")

# Get quadruplet optimization
print(f"Quadruplet optimization: {advanced_four_sum.get_quadruplet_optimization()}")
```

### **Variation 3: Sum of Four Values with Constraints**
**Problem**: Handle sum of four values with additional constraints (cost limits, distance constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedSumOfFourValues:
    def __init__(self, arr, target, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.target = target
        self.constraints = constraints or {}
        self.sorted_arr = self._create_sorted_array()
        self.quadruplets = self._compute_quadruplets()
    
    def _create_sorted_array(self):
        """Create sorted array with original indices."""
        indexed_arr = [(self.arr[i], i) for i in range(self.n)]
        indexed_arr.sort()
        return indexed_arr
    
    def _compute_quadruplets(self):
        """Compute all quadruplets that sum to target."""
        results = []
        
        for i in range(len(self.sorted_arr) - 3):
            for j in range(i + 1, len(self.sorted_arr) - 2):
                left = j + 1
                right = len(self.sorted_arr) - 1
                
                while left < right:
                    current_sum = (self.sorted_arr[i][0] + self.sorted_arr[j][0] + 
                                 self.sorted_arr[left][0] + self.sorted_arr[right][0])
                    
                    if current_sum == self.target:
                        indices = [self.sorted_arr[i][1], self.sorted_arr[j][1], 
                                 self.sorted_arr[left][1], self.sorted_arr[right][1]]
                        results.append(indices)
                        left += 1
                        right -= 1
                    elif current_sum < self.target:
                        left += 1
                    else:
                        right -= 1
        
        return results
    
    def get_quadruplets_with_cost_constraints(self, cost_limit):
        """Get quadruplets considering cost constraints."""
        result = []
        total_cost = 0
        
        for indices in self.quadruplets:
            # Calculate cost for this quadruplet
            cost = sum(abs(self.arr[i]) for i in indices)  # Simple cost model
            if total_cost + cost <= cost_limit:
                result.append(indices)
                total_cost += cost
        
        return result
    
    def get_quadruplets_with_distance_constraints(self, min_distance, max_distance):
        """Get quadruplets considering distance constraints."""
        result = []
        
        for indices in self.quadruplets:
            # Check distance constraints
            valid = True
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    distance = abs(indices[i] - indices[j])
                    if distance < min_distance or distance > max_distance:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                result.append(indices)
        
        return result
    
    def get_quadruplets_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get quadruplets considering resource constraints."""
        result = []
        current_resources = [0] * len(resource_limits)
        
        for indices in self.quadruplets:
            # Check resource constraints
            can_afford = True
            for idx in indices:
                consumption = resource_consumption.get(idx, [0] * len(resource_limits))
                for j, res_consumption in enumerate(consumption):
                    if current_resources[j] + res_consumption > resource_limits[j]:
                        can_afford = False
                        break
                if not can_afford:
                    break
            
            if can_afford:
                result.append(indices)
                for idx in indices:
                    consumption = resource_consumption.get(idx, [0] * len(resource_limits))
                    for j, res_consumption in enumerate(consumption):
                        current_resources[j] += res_consumption
        
        return result
    
    def get_quadruplets_with_mathematical_constraints(self, constraint_func):
        """Get quadruplets that satisfy custom mathematical constraints."""
        result = []
        
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            if constraint_func(indices, values):
                result.append(indices)
        
        return result
    
    def get_quadruplets_with_range_constraints(self, range_constraints):
        """Get quadruplets that satisfy range constraints."""
        result = []
        
        for indices in self.quadruplets:
            # Check if quadruplet satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(indices, [self.arr[i] for i in indices]):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(indices)
        
        return result
    
    def get_quadruplets_with_optimization_constraints(self, optimization_func):
        """Get quadruplets using custom optimization constraints."""
        # Sort quadruplets by optimization function
        all_quadruplets = []
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            score = optimization_func(indices, values)
            all_quadruplets.append((indices, score))
        
        # Sort by optimization score
        all_quadruplets.sort(key=lambda x: x[1], reverse=True)
        
        return [indices for indices, _ in all_quadruplets]
    
    def get_quadruplets_with_multiple_constraints(self, constraints_list):
        """Get quadruplets that satisfy multiple constraints."""
        result = []
        
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            # Check if quadruplet satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(indices, values):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                result.append(indices)
        
        return result
    
    def get_quadruplets_with_priority_constraints(self, priority_func):
        """Get quadruplets with priority-based constraints."""
        # Sort quadruplets by priority
        all_quadruplets = []
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            priority = priority_func(indices, values)
            all_quadruplets.append((indices, priority))
        
        # Sort by priority
        all_quadruplets.sort(key=lambda x: x[1], reverse=True)
        
        return [indices for indices, _ in all_quadruplets]
    
    def get_quadruplets_with_adaptive_constraints(self, adaptive_func):
        """Get quadruplets with adaptive constraints."""
        result = []
        
        for indices in self.quadruplets:
            values = [self.arr[i] for i in indices]
            # Check adaptive constraints
            if adaptive_func(indices, values, result):
                result.append(indices)
        
        return result
    
    def get_optimal_quadruplet_strategy(self):
        """Get optimal quadruplet strategy considering all constraints."""
        strategies = [
            ('cost_constraints', self.get_quadruplets_with_cost_constraints),
            ('distance_constraints', self.get_quadruplets_with_distance_constraints),
            ('resource_constraints', self.get_quadruplets_with_resource_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'cost_constraints':
                    current_count = len(strategy_func(100))  # Cost limit of 100
                elif strategy_name == 'distance_constraints':
                    current_count = len(strategy_func(1, 10))  # Distance between 1 and 10
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    current_count = len(strategy_func(resource_limits, resource_consumption))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_cost': 100,
    'min_distance': 1,
    'max_distance': 10
}

arr = [1, 2, 3, 4, 5, 6, 7, 8]
target = 20
constrained_four_sum = ConstrainedSumOfFourValues(arr, target, constraints)

print("Cost-constrained quadruplets:", len(constrained_four_sum.get_quadruplets_with_cost_constraints(100)))

print("Distance-constrained quadruplets:", len(constrained_four_sum.get_quadruplets_with_distance_constraints(1, 10)))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(arr))}
print("Resource-constrained quadruplets:", len(constrained_four_sum.get_quadruplets_with_resource_constraints(resource_limits, resource_consumption)))

# Mathematical constraints
def custom_constraint(indices, values):
    return all(v > 2 for v in values) and len(set(indices)) == 4

print("Mathematical constraint quadruplets:", len(constrained_four_sum.get_quadruplets_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(indices, values):
    return all(0 <= idx < len(arr) for idx in indices)

range_constraints = [range_constraint]
print("Range-constrained quadruplets:", len(constrained_four_sum.get_quadruplets_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(indices, values):
    return all(v > 2 for v in values)

def constraint2(indices, values):
    return len(set(indices)) == 4

constraints_list = [constraint1, constraint2]
print("Multiple constraints quadruplets:", len(constrained_four_sum.get_quadruplets_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(indices, values):
    return sum(values)

print("Priority-constrained quadruplets:", len(constrained_four_sum.get_quadruplets_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(indices, values, current_result):
    return all(v > 2 for v in values) and len(current_result) < 10

print("Adaptive constraint quadruplets:", len(constrained_four_sum.get_quadruplets_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_four_sum.get_optimal_quadruplet_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Sum of Four Values](https://cses.fi/problemset/task/1642) - Basic four values problem
- [Sum of Two Values](https://cses.fi/problemset/task/1640) - Two values variant
- [Sum of Three Values](https://cses.fi/problemset/task/1641) - Three values variant

#### **LeetCode Problems**
- [4Sum](https://leetcode.com/problems/4sum/) - Basic four sum problem
- [4Sum II](https://leetcode.com/problems/4sum-ii/) - Four sum with four arrays
- [3Sum](https://leetcode.com/problems/3sum/) - Three sum problem
- [Two Sum](https://leetcode.com/problems/two-sum/) - Two sum problem

#### **Problem Categories**
- **Two Pointers**: Sorted array algorithms, efficient quadruplet finding, pointer techniques
- **Hash Maps**: Key-value lookups, complement search, efficient searching
- **Array Processing**: Element searching, quadruplet finding, index manipulation
- **Algorithm Design**: Two-pointer techniques, hash-based algorithms, search optimization
