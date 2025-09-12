---
layout: simple
title: "Forest Queries - 2D Prefix Sums"
permalink: /problem_soulutions/range_queries/forest_queries_analysis
---

# Forest Queries - 2D Prefix Sums

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement 2D prefix sums for 2D range queries
- Apply 2D prefix sums to efficiently answer 2D range sum queries
- Optimize 2D range sum calculations using 2D prefix sums
- Handle edge cases in 2D prefix sum problems
- Recognize when to use 2D prefix sums vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D prefix sums, 2D range queries, 2D data structures
- **Data Structures**: 2D arrays, 2D prefix sum arrays
- **Mathematical Concepts**: 2D range sum optimization, 2D cumulative sums
- **Programming Skills**: 2D array manipulation, 2D prefix sum implementation
- **Related Problems**: Static range sum queries, hotel queries, 2D range query problems

## 📋 Problem Description

Given a 2D grid of integers and multiple queries, each query asks for the sum of elements in a 2D range [x1, y1] to [x2, y2]. The grid is static (no updates).

**Input**: 
- First line: n (grid size) and q (number of queries)
- Next n lines: n integers each (grid values)
- Next q lines: x1 y1 x2 y2 (2D range boundaries, 1-indexed)

**Output**: 
- q lines: sum of elements in 2D range [x1, y1] to [x2, y2] for each query

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ q ≤ 2×10⁵
- -10⁹ ≤ grid[i][j] ≤ 10⁹
- 1 ≤ x1 ≤ x2 ≤ n, 1 ≤ y1 ≤ y2 ≤ n

**Example**:
```
Input:
3 2
1 2 3
4 5 6
7 8 9
1 1 2 2
2 2 3 3

Output:
12
28

Explanation**: 
Query 1: sum of [1,2; 4,5] = 1+2+4+5 = 12
Query 2: sum of [5,6; 8,9] = 5+6+8+9 = 28
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n²)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the 2D range [x1, y1] to [x2, y2]
2. Sum all elements in the 2D range
3. Return the sum

**Implementation**:
```python
def brute_force_forest_queries(grid, queries):
    n = len(grid)
    results = []
    
    for x1, y1, x2, y2 in queries:
        # Convert to 0-indexed
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        
        # Calculate sum in 2D range [x1, y1] to [x2, y2]
        range_sum = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                range_sum += grid[i][j]
        
        results.append(range_sum)
    
    return results
```

### Approach 2: Optimized with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = sum of elements from (0,0) to (i,j)
2. For each query, calculate sum using 2D prefix sums
3. Return the sum

**Implementation**:
```python
def optimized_forest_queries(grid, queries):
    n = len(grid)
    
    # Precompute 2D prefix sums
    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            prefix[i + 1][j + 1] = (prefix[i][j + 1] + 
                                   prefix[i + 1][j] - 
                                   prefix[i][j] + 
                                   grid[i][j])
    
    results = []
    for x1, y1, x2, y2 in queries:
        # Calculate sum using 2D prefix sums
        range_sum = (prefix[x2][y2] - 
                    prefix[x1 - 1][y2] - 
                    prefix[x2][y1 - 1] + 
                    prefix[x1 - 1][y1 - 1])
        results.append(range_sum)
    
    return results
```

### Approach 3: Optimal with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = sum of elements from (0,0) to (i,j)
2. For each query, calculate sum using 2D prefix sums
3. Return the sum

**Implementation**:
```python
def optimal_forest_queries(grid, queries):
    n = len(grid)
    
    # Precompute 2D prefix sums
    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            prefix[i + 1][j + 1] = (prefix[i][j + 1] + 
                                   prefix[i + 1][j] - 
                                   prefix[i][j] + 
                                   grid[i][j])
    
    results = []
    for x1, y1, x2, y2 in queries:
        # Calculate sum using 2D prefix sums
        range_sum = (prefix[x2][y2] - 
                    prefix[x1 - 1][y2] - 
                    prefix[x2][y1 - 1] + 
                    prefix[x1 - 1][y1 - 1])
        results.append(range_sum)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n²) | O(1) | Calculate sum for each query |
| Optimized | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |
| Optimal | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |

### Time Complexity
- **Time**: O(n² + q) - O(n²) preprocessing + O(1) per query
- **Space**: O(n²) - 2D prefix sum array

### Why This Solution Works
- **2D Prefix Sum Property**: prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1] gives sum of 2D range
- **Efficient Preprocessing**: Calculate 2D prefix sums once in O(n²) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n² + q) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Forest Queries with Dynamic Updates
**Problem**: Handle dynamic updates to the forest grid and maintain 2D range sum queries.

**Link**: [CSES Problem Set - Forest Queries with Updates](https://cses.fi/problemset/task/forest_queries_updates)

```python
class ForestQueriesWithUpdates:
    def __init__(self, grid):
        self.n = len(grid)
        self.m = len(grid[0]) if grid else 0
        self.grid = [row[:] for row in grid]
        self.prefix = self._compute_2d_prefix()
    
    def _compute_2d_prefix(self):
        """Compute 2D prefix sums"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                prefix[i][j] = (self.grid[i-1][j-1] + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def update(self, row, col, value):
        """Update grid[row][col] to value"""
        self.grid[row][col] = value
        self.prefix = self._compute_2d_prefix()
    
    def range_query(self, x1, y1, x2, y2):
        """Query sum of rectangle from (x1,y1) to (x2,y2)"""
        return (self.prefix[x2+1][y2+1] - 
                self.prefix[x1][y2+1] - 
                self.prefix[x2+1][y1] + 
                self.prefix[x1][y1])
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for x1, y1, x2, y2 in queries:
            results.append(self.range_query(x1, y1, x2, y2))
        return results
```

### Variation 2: Forest Queries with Different Operations
**Problem**: Handle different types of operations (sum, count, max, min) on 2D ranges.

**Link**: [CSES Problem Set - Forest Queries Different Operations](https://cses.fi/problemset/task/forest_queries_operations)

```python
class ForestQueriesDifferentOps:
    def __init__(self, grid):
        self.n = len(grid)
        self.m = len(grid[0]) if grid else 0
        self.grid = [row[:] for row in grid]
        self.prefix_sum = self._compute_2d_prefix_sum()
        self.prefix_count = self._compute_2d_prefix_count()
        self.prefix_max = self._compute_2d_prefix_max()
        self.prefix_min = self._compute_2d_prefix_min()
    
    def _compute_2d_prefix_sum(self):
        """Compute 2D prefix sums"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                prefix[i][j] = (self.grid[i-1][j-1] + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def _compute_2d_prefix_count(self):
        """Compute 2D prefix counts (count of non-zero elements)"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                count = 1 if self.grid[i-1][j-1] != 0 else 0
                prefix[i][j] = (count + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def _compute_2d_prefix_max(self):
        """Compute 2D prefix maximums"""
        prefix = [[float('-inf')] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                prefix[i][j] = max(self.grid[i-1][j-1],
                                  prefix[i-1][j],
                                  prefix[i][j-1])
        
        return prefix
    
    def _compute_2d_prefix_min(self):
        """Compute 2D prefix minimums"""
        prefix = [[float('inf')] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                prefix[i][j] = min(self.grid[i-1][j-1],
                                  prefix[i-1][j],
                                  prefix[i][j-1])
        
        return prefix
    
    def range_sum(self, x1, y1, x2, y2):
        """Query sum of rectangle from (x1,y1) to (x2,y2)"""
        return (self.prefix_sum[x2+1][y2+1] - 
                self.prefix_sum[x1][y2+1] - 
                self.prefix_sum[x2+1][y1] + 
                self.prefix_sum[x1][y1])
    
    def range_count(self, x1, y1, x2, y2):
        """Query count of non-zero elements in rectangle"""
        return (self.prefix_count[x2+1][y2+1] - 
                self.prefix_count[x1][y2+1] - 
                self.prefix_count[x2+1][y1] + 
                self.prefix_count[x1][y1])
    
    def range_max(self, x1, y1, x2, y2):
        """Query maximum element in rectangle"""
        max_val = float('-inf')
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                max_val = max(max_val, self.grid[i][j])
        return max_val
    
    def range_min(self, x1, y1, x2, y2):
        """Query minimum element in rectangle"""
        min_val = float('inf')
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                min_val = min(min_val, self.grid[i][j])
        return min_val
```

### Variation 3: Forest Queries with Constraints
**Problem**: Handle 2D range queries with additional constraints (e.g., minimum area, maximum sum).

**Link**: [CSES Problem Set - Forest Queries with Constraints](https://cses.fi/problemset/task/forest_queries_constraints)

```python
class ForestQueriesWithConstraints:
    def __init__(self, grid, min_area, max_sum):
        self.n = len(grid)
        self.m = len(grid[0]) if grid else 0
        self.grid = [row[:] for row in grid]
        self.min_area = min_area
        self.max_sum = max_sum
        self.prefix = self._compute_2d_prefix()
    
    def _compute_2d_prefix(self):
        """Compute 2D prefix sums"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                prefix[i][j] = (self.grid[i-1][j-1] + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def constrained_range_query(self, x1, y1, x2, y2):
        """Query sum of rectangle with constraints"""
        # Check minimum area constraint
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        if area < self.min_area:
            return None  # Invalid area
        
        # Get sum
        sum_value = (self.prefix[x2+1][y2+1] - 
                    self.prefix[x1][y2+1] - 
                    self.prefix[x2+1][y1] + 
                    self.prefix[x1][y1])
        
        # Check maximum sum constraint
        if sum_value > self.max_sum:
            return None  # Exceeds maximum sum
        
        return sum_value
    
    def find_valid_rectangles(self):
        """Find all valid rectangles that satisfy constraints"""
        valid_rectangles = []
        
        for x1 in range(self.n):
            for y1 in range(self.m):
                for x2 in range(x1, self.n):
                    for y2 in range(y1, self.m):
                        result = self.constrained_range_query(x1, y1, x2, y2)
                        if result is not None:
                            valid_rectangles.append((x1, y1, x2, y2, result))
        
        return valid_rectangles
    
    def get_maximum_valid_sum(self):
        """Get maximum valid sum"""
        max_sum = float('-inf')
        
        for x1 in range(self.n):
            for y1 in range(self.m):
                for x2 in range(x1, self.n):
                    for y2 in range(y1, self.m):
                        result = self.constrained_range_query(x1, y1, x2, y2)
                        if result is not None:
                            max_sum = max(max_sum, result)
        
        return max_sum if max_sum != float('-inf') else None

# Example usage
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
min_area = 4
max_sum = 20

fq = ForestQueriesWithConstraints(grid, min_area, max_sum)
result = fq.constrained_range_query(0, 0, 1, 1)
print(f"Constrained range query result: {result}")  # Output: 12
```

### Related Problems

#### **CSES Problems**
- [Forest Queries](https://cses.fi/problemset/task/1652) - Basic 2D range sum queries problem
- [Static Range Sum Queries](https://cses.fi/problemset/task/1646) - 1D range sum queries
- [Range Sum Queries II](https://cses.fi/problemset/task/1649) - Range sum with updates

#### **LeetCode Problems**
- [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) - 2D range sum queries
- [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/) - 2D range sum with updates
- [Max Sum of Rectangle No Larger Than K](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/) - 2D range sum with constraints

#### **Problem Categories**
- **2D Prefix Sums**: 2D range queries, rectangle operations, efficient preprocessing
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Grid Processing**: 2D array operations, rectangle queries, spatial algorithms
- **Algorithm Design**: 2D prefix sum techniques, range optimization, spatial processing