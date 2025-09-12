---
layout: simple
title: "Hotel Queries - 2D Range Queries"
permalink: /problem_soulutions/range_queries/hotel_queries_analysis
---

# Hotel Queries - 2D Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement 2D range queries for hotel problems
- Apply 2D range queries to efficiently answer hotel queries
- Optimize hotel query calculations using 2D range queries
- Handle edge cases in hotel query problems
- Recognize when to use 2D range queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D range queries, hotel problems, 2D data structures
- **Data Structures**: 2D arrays, 2D range query structures
- **Mathematical Concepts**: 2D range query optimization, hotel optimization
- **Programming Skills**: 2D array manipulation, 2D range query implementation
- **Related Problems**: Forest queries, 2D range query problems, hotel problems

## 📋 Problem Description

Given a 2D grid representing hotel rooms and multiple queries, each query asks for the number of available rooms in a 2D range [x1, y1] to [x2, y2]. The grid is static (no updates).

**Input**: 
- First line: n (grid size) and q (number of queries)
- Next n lines: n integers each (room availability: 1 = available, 0 = occupied)
- Next q lines: x1 y1 x2 y2 (2D range boundaries, 1-indexed)

**Output**: 
- q lines: number of available rooms in 2D range [x1, y1] to [x2, y2] for each query

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ q ≤ 2×10⁵
- 0 ≤ grid[i][j] ≤ 1
- 1 ≤ x1 ≤ x2 ≤ n, 1 ≤ y1 ≤ y2 ≤ n

**Example**:
```
Input:
3 2
1 0 1
0 1 0
1 1 1
1 1 2 2
2 2 3 3

Output:
2
3

Explanation**: 
Query 1: available rooms in [1,0; 0,1] = 1+0+0+1 = 2
Query 2: available rooms in [1,0; 1,1] = 1+0+1+1 = 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n²)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the 2D range [x1, y1] to [x2, y2]
2. Count available rooms in the 2D range
3. Return the count

**Implementation**:
```python
def brute_force_hotel_queries(grid, queries):
    n = len(grid)
    results = []
    
    for x1, y1, x2, y2 in queries:
        # Convert to 0-indexed
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        
        # Count available rooms in 2D range [x1, y1] to [x2, y2]
        count = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                if grid[i][j] == 1:
                    count += 1
        
        results.append(count)
    
    return results
```

### Approach 2: Optimized with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = count of available rooms from (0,0) to (i,j)
2. For each query, calculate count using 2D prefix sums
3. Return the count

**Implementation**:
```python
def optimized_hotel_queries(grid, queries):
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
        # Calculate count using 2D prefix sums
        count = (prefix[x2][y2] - 
                prefix[x1 - 1][y2] - 
                prefix[x2][y1 - 1] + 
                prefix[x1 - 1][y1 - 1])
        results.append(count)
    
    return results
```

### Approach 3: Optimal with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = count of available rooms from (0,0) to (i,j)
2. For each query, calculate count using 2D prefix sums
3. Return the count

**Implementation**:
```python
def optimal_hotel_queries(grid, queries):
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
        # Calculate count using 2D prefix sums
        count = (prefix[x2][y2] - 
                prefix[x1 - 1][y2] - 
                prefix[x2][y1 - 1] + 
                prefix[x1 - 1][y1 - 1])
        results.append(count)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n²) | O(1) | Count available rooms for each query |
| Optimized | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |
| Optimal | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |

### Time Complexity
- **Time**: O(n² + q) - O(n²) preprocessing + O(1) per query
- **Space**: O(n²) - 2D prefix sum array

### Why This Solution Works
- **2D Prefix Sum Property**: prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1] gives count of available rooms in 2D range
- **Efficient Preprocessing**: Calculate 2D prefix sums once in O(n²) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n² + q) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Hotel Queries with Dynamic Updates
**Problem**: Handle dynamic updates to the hotel grid and maintain 2D range count queries.

**Link**: [CSES Problem Set - Hotel Queries with Updates](https://cses.fi/problemset/task/hotel_queries_updates)

```python
class HotelQueriesWithUpdates:
    def __init__(self, grid):
        self.n = len(grid)
        self.m = len(grid[0]) if grid else 0
        self.grid = [row[:] for row in grid]
        self.prefix = self._compute_2d_prefix()
    
    def _compute_2d_prefix(self):
        """Compute 2D prefix sums for count queries"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                count = 1 if self.grid[i-1][j-1] == 'H' else 0
                prefix[i][j] = (count + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def update(self, row, col, value):
        """Update grid[row][col] to value"""
        self.grid[row][col] = value
        self.prefix = self._compute_2d_prefix()
    
    def range_count(self, x1, y1, x2, y2):
        """Query count of hotels in rectangle from (x1,y1) to (x2,y2)"""
        return (self.prefix[x2+1][y2+1] - 
                self.prefix[x1][y2+1] - 
                self.prefix[x2+1][y1] + 
                self.prefix[x1][y1])
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for x1, y1, x2, y2 in queries:
            results.append(self.range_count(x1, y1, x2, y2))
        return results
```

### Variation 2: Hotel Queries with Different Operations
**Problem**: Handle different types of operations (count, sum, max, min) on 2D ranges.

**Link**: [CSES Problem Set - Hotel Queries Different Operations](https://cses.fi/problemset/task/hotel_queries_operations)

```python
class HotelQueriesDifferentOps:
    def __init__(self, grid):
        self.n = len(grid)
        self.m = len(grid[0]) if grid else 0
        self.grid = [row[:] for row in grid]
        self.prefix_count = self._compute_2d_prefix_count()
        self.prefix_sum = self._compute_2d_prefix_sum()
        self.prefix_max = self._compute_2d_prefix_max()
        self.prefix_min = self._compute_2d_prefix_min()
    
    def _compute_2d_prefix_count(self):
        """Compute 2D prefix counts (count of hotels)"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                count = 1 if self.grid[i-1][j-1] == 'H' else 0
                prefix[i][j] = (count + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def _compute_2d_prefix_sum(self):
        """Compute 2D prefix sums (sum of hotel values)"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                value = 1 if self.grid[i-1][j-1] == 'H' else 0
                prefix[i][j] = (value + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def _compute_2d_prefix_max(self):
        """Compute 2D prefix maximums"""
        prefix = [[float('-inf')] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                value = 1 if self.grid[i-1][j-1] == 'H' else 0
                prefix[i][j] = max(value,
                                  prefix[i-1][j],
                                  prefix[i][j-1])
        
        return prefix
    
    def _compute_2d_prefix_min(self):
        """Compute 2D prefix minimums"""
        prefix = [[float('inf')] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                value = 1 if self.grid[i-1][j-1] == 'H' else 0
                prefix[i][j] = min(value,
                                  prefix[i-1][j],
                                  prefix[i][j-1])
        
        return prefix
    
    def range_count(self, x1, y1, x2, y2):
        """Query count of hotels in rectangle"""
        return (self.prefix_count[x2+1][y2+1] - 
                self.prefix_count[x1][y2+1] - 
                self.prefix_count[x2+1][y1] + 
                self.prefix_count[x1][y1])
    
    def range_sum(self, x1, y1, x2, y2):
        """Query sum of hotel values in rectangle"""
        return (self.prefix_sum[x2+1][y2+1] - 
                self.prefix_sum[x1][y2+1] - 
                self.prefix_sum[x2+1][y1] + 
                self.prefix_sum[x1][y1])
    
    def range_max(self, x1, y1, x2, y2):
        """Query maximum hotel value in rectangle"""
        max_val = float('-inf')
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                value = 1 if self.grid[i][j] == 'H' else 0
                max_val = max(max_val, value)
        return max_val
    
    def range_min(self, x1, y1, x2, y2):
        """Query minimum hotel value in rectangle"""
        min_val = float('inf')
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                value = 1 if self.grid[i][j] == 'H' else 0
                min_val = min(min_val, value)
        return min_val
```

### Variation 3: Hotel Queries with Constraints
**Problem**: Handle 2D range queries with additional constraints (e.g., minimum count, maximum area).

**Link**: [CSES Problem Set - Hotel Queries with Constraints](https://cses.fi/problemset/task/hotel_queries_constraints)

```python
class HotelQueriesWithConstraints:
    def __init__(self, grid, min_count, max_area):
        self.n = len(grid)
        self.m = len(grid[0]) if grid else 0
        self.grid = [row[:] for row in grid]
        self.min_count = min_count
        self.max_area = max_area
        self.prefix = self._compute_2d_prefix()
    
    def _compute_2d_prefix(self):
        """Compute 2D prefix sums for count queries"""
        prefix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                count = 1 if self.grid[i-1][j-1] == 'H' else 0
                prefix[i][j] = (count + 
                               prefix[i-1][j] + 
                               prefix[i][j-1] - 
                               prefix[i-1][j-1])
        
        return prefix
    
    def constrained_range_query(self, x1, y1, x2, y2):
        """Query count of hotels in rectangle with constraints"""
        # Check maximum area constraint
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        if area > self.max_area:
            return None  # Exceeds maximum area
        
        # Get count
        count = (self.prefix[x2+1][y2+1] - 
                self.prefix[x1][y2+1] - 
                self.prefix[x2+1][y1] + 
                self.prefix[x1][y1])
        
        # Check minimum count constraint
        if count < self.min_count:
            return None  # Below minimum count
        
        return count
    
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
    
    def get_maximum_valid_count(self):
        """Get maximum valid count"""
        max_count = float('-inf')
        
        for x1 in range(self.n):
            for y1 in range(self.m):
                for x2 in range(x1, self.n):
                    for y2 in range(y1, self.m):
                        result = self.constrained_range_query(x1, y1, x2, y2)
                        if result is not None:
                            max_count = max(max_count, result)
        
        return max_count if max_count != float('-inf') else None

# Example usage
grid = [['H', '.', 'H'], ['.', 'H', '.'], ['H', 'H', '.']]
min_count = 2
max_area = 6

hq = HotelQueriesWithConstraints(grid, min_count, max_area)
result = hq.constrained_range_query(0, 0, 1, 1)
print(f"Constrained range query result: {result}")  # Output: 2
```

### Related Problems

#### **CSES Problems**
- [Hotel Queries](https://cses.fi/problemset/task/1143) - Basic 2D range count queries problem
- [Forest Queries](https://cses.fi/problemset/task/1652) - 2D range sum queries
- [Static Range Sum Queries](https://cses.fi/problemset/task/1646) - 1D range sum queries

#### **LeetCode Problems**
- [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) - 2D range sum queries
- [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/) - 2D range sum with updates
- [Max Sum of Rectangle No Larger Than K](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/) - 2D range sum with constraints

#### **Problem Categories**
- **2D Prefix Sums**: 2D range queries, rectangle operations, efficient preprocessing
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Grid Processing**: 2D array operations, rectangle queries, spatial algorithms
- **Algorithm Design**: 2D prefix sum techniques, range optimization, spatial processing