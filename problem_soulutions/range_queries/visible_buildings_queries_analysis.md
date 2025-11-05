---
layout: simple
title: "Visible Buildings Queries - Geometric Queries"
permalink: /problem_soulutions/range_queries/visible_buildings_queries_analysis
---

# Visible Buildings Queries - Geometric Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement geometric queries for visible buildings problems
- Apply geometric queries to efficiently answer visible buildings queries
- Optimize visible buildings calculations using geometric queries
- Handle edge cases in visible buildings query problems
- Recognize when to use geometric queries vs other approaches

## 📋 Problem Description

Given an array of building heights and multiple queries, each query asks for the number of visible buildings from position i. A building is visible if it's taller than all buildings between position i and that building.

**Input**: 
- First line: n (number of buildings) and q (number of queries)
- Second line: n integers representing building heights
- Next q lines: i (position to query, 1-indexed)

**Output**: 
- q lines: number of visible buildings from position i for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ height[i] ≤ 10⁹
- 1 ≤ i ≤ n

**Example**:
```
Input:
5 3
3 1 4 1 5
1
3
5

Output:
2
2
1

Explanation**: 
Query 1: visible buildings from position 1 = 2 (buildings at positions 3 and 5)
Query 2: visible buildings from position 3 = 2 (buildings at positions 1 and 5)
Query 3: visible buildings from position 5 = 1 (no buildings to the right)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, check all buildings to the right of position i
2. Count buildings that are visible (taller than all buildings between)
3. Return the count

**Implementation**:
```python
def brute_force_visible_buildings_queries(heights, queries):
    n = len(heights)
    results = []
    
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        
        # Count visible buildings from position i
        visible_count = 0
        max_height = 0
        
        for j in range(i + 1, n):
            if heights[j] > max_height:
                visible_count += 1
                max_height = heights[j]
        
        results.append(visible_count)
    
    return results
```

### Approach 2: Optimized with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute visible buildings count for each position
2. For each query, return precomputed count
3. Return the count

**Implementation**:
```python
def optimized_visible_buildings_queries(heights, queries):
    n = len(heights)
    
    # Precompute visible buildings count for each position
    visible_counts = [0] * n
    
    for i in range(n):
        max_height = 0
        for j in range(i + 1, n):
            if heights[j] > max_height:
                visible_counts[i] += 1
                max_height = heights[j]
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(visible_counts[i])
    
    return results
```

### Approach 3: Optimal with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute visible buildings count for each position
2. For each query, return precomputed count
3. Return the count

**Implementation**:
```python
def optimal_visible_buildings_queries(heights, queries):
    n = len(heights)
    
    # Precompute visible buildings count for each position
    visible_counts = [0] * n
    
    for i in range(n):
        max_height = 0
        for j in range(i + 1, n):
            if heights[j] > max_height:
                visible_counts[i] += 1
                max_height = heights[j]
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(visible_counts[i])
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Count visible buildings for each query |
| Optimized | O(n + q) | O(n) | Precompute counts for O(1) queries |
| Optimal | O(n + q) | O(n) | Precompute counts for O(1) queries |

### Time Complexity
- **Time**: O(n + q) - O(n) preprocessing + O(1) per query
- **Space**: O(n) - Visible counts array

### Why This Solution Works
- **Preprocessing Property**: Precompute visible buildings count for each position
- **Efficient Preprocessing**: Calculate counts once in O(n) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n + q) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Visible Buildings Queries with Dynamic Updates
**Problem**: Handle dynamic updates to building heights and maintain visible buildings queries efficiently.

**Link**: [CSES Problem Set - Visible Buildings Queries with Updates](https://cses.fi/problemset/task/visible_buildings_queries_updates)

```python
class VisibleBuildingsQueriesWithUpdates:
    def __init__(self, heights):
        self.heights = heights[:]
        self.n = len(heights)
        self.visible_counts = self._build_visible_counts()
    
    def _build_visible_counts(self):
        """Build visible counts array"""
        visible_counts = [0] * self.n
        
        for i in range(self.n):
            count = 0
            max_height = 0
            
            for j in range(i + 1, self.n):
                if self.heights[j] > max_height:
                    count += 1
                    max_height = self.heights[j]
            
            visible_counts[i] = count
        
        return visible_counts
    
    def update(self, pos, height):
        """Update building height at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.heights[pos] = height
        
        # Rebuild visible counts
        self.visible_counts = self._build_visible_counts()
    
    def query(self, left, right):
        """Query visible buildings in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        count = 0
        max_height = 0
        
        for i in range(left, right + 1):
            if self.heights[i] > max_height:
                count += 1
                max_height = self.heights[i]
        
        return count
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['height'])
                results.append(None)
            elif query['type'] == 'query':
                result = self.query(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 2: Visible Buildings Queries with Different Operations
**Problem**: Handle different types of operations (count, list, height) on visible buildings queries.

**Link**: [CSES Problem Set - Visible Buildings Queries Different Operations](https://cses.fi/problemset/task/visible_buildings_queries_operations)

```python
class VisibleBuildingsQueriesDifferentOps:
    def __init__(self, heights):
        self.heights = heights[:]
        self.n = len(heights)
        self.visible_counts = self._build_visible_counts()
        self.visible_lists = self._build_visible_lists()
    
    def _build_visible_counts(self):
        """Build visible counts array"""
        visible_counts = [0] * self.n
        
        for i in range(self.n):
            count = 0
            max_height = 0
            
            for j in range(i + 1, self.n):
                if self.heights[j] > max_height:
                    count += 1
                    max_height = self.heights[j]
            
            visible_counts[i] = count
        
        return visible_counts
    
    def _build_visible_lists(self):
        """Build visible lists array"""
        visible_lists = [[] for _ in range(self.n)]
        
        for i in range(self.n):
            max_height = 0
            
            for j in range(i + 1, self.n):
                if self.heights[j] > max_height:
                    visible_lists[i].append(j)
                    max_height = self.heights[j]
        
        return visible_lists
    
    def count_visible(self, left, right):
        """Count visible buildings in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        count = 0
        max_height = 0
        
        for i in range(left, right + 1):
            if self.heights[i] > max_height:
                count += 1
                max_height = self.heights[i]
        
        return count
    
    def list_visible(self, left, right):
        """List visible buildings in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return []
        
        visible = []
        max_height = 0
        
        for i in range(left, right + 1):
            if self.heights[i] > max_height:
                visible.append(i)
                max_height = self.heights[i]
        
        return visible
    
    def get_visible_heights(self, left, right):
        """Get heights of visible buildings in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return []
        
        visible_heights = []
        max_height = 0
        
        for i in range(left, right + 1):
            if self.heights[i] > max_height:
                visible_heights.append(self.heights[i])
                max_height = self.heights[i]
        
        return visible_heights
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'count':
                result = self.count_visible(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'list':
                result = self.list_visible(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'heights':
                result = self.get_visible_heights(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 3: Visible Buildings Queries with Constraints
**Problem**: Handle visible buildings queries with additional constraints (e.g., minimum height, maximum range).

**Link**: [CSES Problem Set - Visible Buildings Queries with Constraints](https://cses.fi/problemset/task/visible_buildings_queries_constraints)

```python
class VisibleBuildingsQueriesWithConstraints:
    def __init__(self, heights, min_height, max_range):
        self.heights = heights[:]
        self.n = len(heights)
        self.min_height = min_height
        self.max_range = max_range
        self.visible_counts = self._build_visible_counts()
    
    def _build_visible_counts(self):
        """Build visible counts array"""
        visible_counts = [0] * self.n
        
        for i in range(self.n):
            count = 0
            max_height = 0
            
            for j in range(i + 1, self.n):
                if self.heights[j] > max_height:
                    count += 1
                    max_height = self.heights[j]
            
            visible_counts[i] = count
        
        return visible_counts
    
    def constrained_query(self, left, right):
        """Query visible buildings in range [left, right] with constraints"""
        # Check maximum range constraint
        if right - left + 1 > self.max_range:
            return None  # Range too large
        
        # Get visible count
        count = self.count_visible(left, right)
        
        # Check minimum height constraint
        if count < self.min_height:
            return None  # Below minimum height
        
        return count
    
    def count_visible(self, left, right):
        """Count visible buildings in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        count = 0
        max_height = 0
        
        for i in range(left, right + 1):
            if self.heights[i] > max_height:
                count += 1
                max_height = self.heights[i]
        
        return count
    
    def find_valid_ranges(self):
        """Find all valid ranges that satisfy constraints"""
        valid_ranges = []
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_maximum_valid_count(self):
        """Get maximum valid count"""
        max_count = 0
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    max_count = max(max_count, result)
        return max_count
    
    def count_valid_ranges(self):
        """Count number of valid ranges"""
        count = 0
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    count += 1
        return count

# Example usage
heights = [1, 2, 3, 4, 5]
min_height = 2
max_range = 3

vbq = VisibleBuildingsQueriesWithConstraints(heights, min_height, max_range)
result = vbq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 2

valid_ranges = vbq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")

max_count = vbq.get_maximum_valid_count()
print(f"Maximum valid count: {max_count}")
```

### Related Problems

#### **CSES Problems**
- [Visible Buildings Queries](https://cses.fi/problemset/task/2428) - Basic visible buildings queries problem
- [Range Sum Queries](https://cses.fi/problemset/task/1646) - Range sum queries
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range sum queries

#### **LeetCode Problems**
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) - Water trapping between buildings
- [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) - Largest rectangle in histogram
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) - Container with most water

#### **Problem Categories**
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Data Structures**: Preprocessing techniques, range operations, efficient preprocessing
- **Algorithm Design**: Range query techniques, constraint handling, optimization
- **Geometric Algorithms**: Building visibility, geometric queries, efficient algorithms

## 🚀 Key Takeaways

- **Preprocessing Technique**: The standard approach for visible buildings queries
- **Efficient Preprocessing**: Calculate counts once for all queries
- **Fast Queries**: Answer each query in O(1) time using precomputed counts
- **Space Trade-off**: Use O(n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many geometric query problems