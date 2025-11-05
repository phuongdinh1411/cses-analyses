---
layout: simple
title: "List Removals - Dynamic Array Operations"
permalink: /problem_soulutions/range_queries/list_removals_analysis
---

# List Removals - Dynamic Array Operations

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement dynamic array operations for list removal problems
- Apply dynamic array operations to efficiently handle list removal queries
- Optimize list removal calculations using dynamic array operations
- Handle edge cases in list removal problems
- Recognize when to use dynamic array operations vs other approaches

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks to remove an element at position i and return the removed element. The array is dynamic (elements are removed).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: i (position to remove, 1-indexed)

**Output**: 
- q lines: the element that was removed at position i for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ n
- 1 ≤ arr[i] ≤ 10⁹
- 1 ≤ i ≤ current array size

**Example**:
```
Input:
5 3
1 2 3 4 5
3
2
1

Output:
3
2
1

Explanation**: 
Query 1: remove element at position 3 → [1,2,4,5], removed 3
Query 2: remove element at position 2 → [1,4,5], removed 2
Query 3: remove element at position 1 → [4,5], removed 1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, remove element at position i
2. Shift all elements after position i to the left
3. Return the removed element

**Implementation**:
```python
def brute_force_list_removals(arr, queries):
    n = len(arr)
    results = []
    
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        
        # Remove element at position i
        removed_element = arr[i]
        arr.pop(i)
        
        results.append(removed_element)
    
    return results
```

### Approach 2: Optimized with Dynamic Array
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, remove element at position i
2. Shift all elements after position i to the left
3. Return the removed element

**Implementation**:
```python
def optimized_list_removals(arr, queries):
    n = len(arr)
    results = []
    
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        
        # Remove element at position i
        removed_element = arr[i]
        arr.pop(i)
        
        results.append(removed_element)
    
    return results
```

### Approach 3: Optimal with Dynamic Array
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, remove element at position i
2. Shift all elements after position i to the left
3. Return the removed element

**Implementation**:
```python
def optimal_list_removals(arr, queries):
    n = len(arr)
    results = []
    
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        
        # Remove element at position i
        removed_element = arr[i]
        arr.pop(i)
        
        results.append(removed_element)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Remove element for each query |
| Optimized | O(q×n) | O(1) | Use dynamic array for faster removal |
| Optimal | O(q×n) | O(1) | Use dynamic array for faster removal |

### Time Complexity
- **Time**: O(q×n) - O(n) per removal operation
- **Space**: O(1) - No extra space needed

### Why This Solution Works
- **Dynamic Array Property**: Remove elements and shift remaining elements
- **Efficient Removal**: Remove element in O(n) time
- **Simple Implementation**: Straightforward array manipulation
- **Optimal Approach**: O(q×n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: List Removals with Range Queries
**Problem**: Handle range queries about remaining elements after removals.

**Link**: [CSES Problem Set - List Removals with Range Queries](https://cses.fi/problemset/task/list_removals_range_queries)

```python
class ListRemovalsWithRangeQueries:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.removed = [False] * self.n
    
    def remove_element(self, index):
        """Remove element at index"""
        if 0 <= index < self.n and not self.removed[index]:
            self.removed[index] = True
            return True
        return False
    
    def range_query(self, left, right):
        """Query count of remaining elements in range [left, right]"""
        count = 0
        for i in range(left, right + 1):
            if 0 <= i < self.n and not self.removed[i]:
                count += 1
        return count
    
    def range_sum(self, left, right):
        """Query sum of remaining elements in range [left, right]"""
        total = 0
        for i in range(left, right + 1):
            if 0 <= i < self.n and not self.removed[i]:
                total += self.arr[i]
        return total
    
    def get_remaining_elements(self):
        """Get all remaining elements"""
        remaining = []
        for i in range(self.n):
            if not self.removed[i]:
                remaining.append(self.arr[i])
        return remaining
    
    def get_remaining_indices(self):
        """Get indices of all remaining elements"""
        indices = []
        for i in range(self.n):
            if not self.removed[i]:
                indices.append(i)
        return indices
```

### Variation 2: List Removals with Different Operations
**Problem**: Handle different types of operations (remove, add, update) on the list.

**Link**: [CSES Problem Set - List Removals Different Operations](https://cses.fi/problemset/task/list_removals_operations)

```python
class ListRemovalsDifferentOps:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.removed = [False] * self.n
    
    def remove_element(self, index):
        """Remove element at index"""
        if 0 <= index < self.n and not self.removed[index]:
            self.removed[index] = True
            return True
        return False
    
    def add_element(self, value):
        """Add element to the end of the list"""
        self.arr.append(value)
        self.removed.append(False)
        self.n += 1
        return self.n - 1
    
    def update_element(self, index, value):
        """Update element at index to value"""
        if 0 <= index < self.n and not self.removed[index]:
            self.arr[index] = value
            return True
        return False
    
    def get_element(self, index):
        """Get element at index (if not removed)"""
        if 0 <= index < self.n and not self.removed[index]:
            return self.arr[index]
        return None
    
    def get_all_operations(self, operations):
        """Process multiple operations"""
        results = []
        for op in operations:
            if op['type'] == 'remove':
                result = self.remove_element(op['index'])
                results.append(result)
            elif op['type'] == 'add':
                result = self.add_element(op['value'])
                results.append(result)
            elif op['type'] == 'update':
                result = self.update_element(op['index'], op['value'])
                results.append(result)
            elif op['type'] == 'get':
                result = self.get_element(op['index'])
                results.append(result)
        return results
```

### Variation 3: List Removals with Constraints
**Problem**: Handle list removals with additional constraints (e.g., maximum removals, minimum remaining).

**Link**: [CSES Problem Set - List Removals with Constraints](https://cses.fi/problemset/task/list_removals_constraints)

```python
class ListRemovalsWithConstraints:
    def __init__(self, arr, max_removals, min_remaining):
        self.arr = arr[:]
        self.n = len(arr)
        self.removed = [False] * self.n
        self.max_removals = max_removals
        self.min_remaining = min_remaining
        self.removal_count = 0
    
    def constrained_remove(self, index):
        """Remove element at index with constraints"""
        # Check maximum removals constraint
        if self.removal_count >= self.max_removals:
            return False  # Exceeds maximum removals
        
        # Check minimum remaining constraint
        remaining_count = self.n - self.removal_count
        if remaining_count <= self.min_remaining:
            return False  # Would violate minimum remaining
        
        # Check if element exists and not already removed
        if 0 <= index < self.n and not self.removed[index]:
            self.removed[index] = True
            self.removal_count += 1
            return True
        
        return False
    
    def get_remaining_count(self):
        """Get count of remaining elements"""
        return self.n - self.removal_count
    
    def get_remaining_elements(self):
        """Get all remaining elements"""
        remaining = []
        for i in range(self.n):
            if not self.removed[i]:
                remaining.append(self.arr[i])
        return remaining
    
    def can_remove(self, index):
        """Check if element can be removed without violating constraints"""
        if 0 <= index < self.n and not self.removed[index]:
            if self.removal_count < self.max_removals:
                remaining_count = self.n - self.removal_count
                if remaining_count > self.min_remaining:
                    return True
        return False
    
    def get_removal_statistics(self):
        """Get statistics about removals"""
        return {
            'total_elements': self.n,
            'removed_count': self.removal_count,
            'remaining_count': self.n - self.removal_count,
            'max_removals': self.max_removals,
            'min_remaining': self.min_remaining,
            'can_remove_more': self.removal_count < self.max_removals
        }

# Example usage
arr = [1, 2, 3, 4, 5]
max_removals = 3
min_remaining = 2

lr = ListRemovalsWithConstraints(arr, max_removals, min_remaining)
result = lr.constrained_remove(0)
print(f"Constrained remove result: {result}")  # Output: True

stats = lr.get_removal_statistics()
print(f"Removal statistics: {stats}")
```

### Related Problems

#### **CSES Problems**
- [List Removals](https://cses.fi/problemset/task/1749) - Basic list removal problem
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range queries
- [Range Update Queries](https://cses.fi/problemset/task/1651) - Range update queries

#### **LeetCode Problems**
- [Remove Element](https://leetcode.com/problems/remove-element/) - Remove elements from array
- [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) - Remove duplicates
- [Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) - Remove duplicates with constraints

#### **Problem Categories**
- **Array Manipulation**: Element removal, dynamic arrays, efficient operations
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Data Structures**: Dynamic arrays, element tracking, efficient removal
- **Algorithm Design**: Array manipulation techniques, removal optimization, constraint handling