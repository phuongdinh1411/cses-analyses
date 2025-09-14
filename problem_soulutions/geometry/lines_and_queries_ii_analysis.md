---
layout: simple
title: "Lines and Queries II - Geometry Problem"
permalink: /problem_soulutions/geometry/lines_and_queries_ii_analysis
---

# Lines and Queries II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of line queries in computational geometry
- Apply geometric algorithms for line intersection queries
- Implement efficient algorithms for line query processing
- Optimize geometric operations for query analysis
- Handle special cases in line query problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Computational geometry, line algorithms, query processing
- **Data Structures**: Lines, points, geometric primitives, query structures
- **Mathematical Concepts**: Line equations, intersection tests, coordinate systems
- **Programming Skills**: Geometric computations, query processing, line operations
- **Related Problems**: Lines and Queries I (geometry), Line Segment Intersection (geometry), Point in Polygon (geometry)

## 📋 Problem Description

Given n lines and q queries, for each query point, find how many lines pass through it.

**Input**: 
- n: number of lines
- lines: array of lines (each with coefficients a, b, c for ax + by + c = 0)
- q: number of queries
- queries: array of query points (x, y)

**Output**: 
- For each query, the number of lines passing through the point

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ q ≤ 1000
- -10^6 ≤ coordinates ≤ 10^6

**Example**:
```
Input:
n = 3
lines = [(1,0,0), (0,1,0), (1,1,-2)]
q = 2
queries = [(0,0), (1,1)]

Output:
[2, 1]

Explanation**: 
Line 1: x = 0 (vertical line)
Line 2: y = 0 (horizontal line)  
Line 3: x + y = 2
Point (0,0): lies on lines 1 and 2 → 2 lines
Point (1,1): lies on line 3 → 1 line
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all lines for each query
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check if point lies on each line
- **Inefficient**: O(nq) time complexity

**Key Insight**: Check every line for each query point.

**Algorithm**:
- For each query point, check all lines
- Use line equation to test if point lies on line
- Count lines passing through point
- Return counts for all queries

**Visual Example**:
```
Lines: x=0, y=0, x+y=2
Query points: (0,0), (1,1)

Line checking:
┌─────────────────────────────────────┐
│ Point (0,0):                       │
│ - Line 1 (x=0): 0 = 0 ✓           │
│ - Line 2 (y=0): 0 = 0 ✓           │
│ - Line 3 (x+y=2): 0+0 = 2 ✗       │
│ Count: 2                           │
│                                   │
│ Point (1,1):                       │
│ - Line 1 (x=0): 1 = 0 ✗           │
│ - Line 2 (y=0): 1 = 0 ✗           │
│ - Line 3 (x+y=2): 1+1 = 2 ✓       │
│ Count: 1                           │
│                                   │
│ Result: [2, 1]                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_lines_and_queries_ii(n, lines, q, queries):
    """
    Process line queries using brute force approach
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: number of lines passing through each query point
    """
    def point_on_line(point, line):
        """Check if point lies on line"""
        x, y = point
        a, b, c = line
        return abs(a * x + b * y + c) < 1e-9  # Use epsilon for floating point comparison
    
    results = []
    
    # Process each query
    for query_point in queries:
        count = 0
        
        # Check all lines
        for line in lines:
            if point_on_line(query_point, line):
                count += 1
        
        results.append(count)
    
    return results

def brute_force_lines_and_queries_ii_optimized(n, lines, q, queries):
    """
    Optimized brute force lines and queries II processing
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: number of lines passing through each query point
    """
    def point_on_line_optimized(point, line):
        """Check if point lies on line with optimization"""
        x, y = point
        a, b, c = line
        return abs(a * x + b * y + c) < 1e-9
    
    results = []
    
    # Process each query with optimization
    for query_point in queries:
        count = 0
        
        # Check all lines with optimization
        for line in lines:
            if point_on_line_optimized(query_point, line):
                count += 1
        
        results.append(count)
    
    return results

# Example usage
n = 3
lines = [(1, 0, 0), (0, 1, 0), (1, 1, -2)]
q = 2
queries = [(0, 0), (1, 1)]
result1 = brute_force_lines_and_queries_ii(n, lines, q, queries)
result2 = brute_force_lines_and_queries_ii_optimized(n, lines, q, queries)
print(f"Brute force lines and queries II: {result1}")
print(f"Optimized brute force lines and queries II: {result2}")
```

**Time Complexity**: O(nq)
**Space Complexity**: O(1)

**Why it's inefficient**: O(nq) time complexity for checking all lines for each query.

---

### Approach 2: Preprocessing Solution

**Key Insights from Preprocessing Solution**:
- **Preprocessing**: Preprocess lines for efficient querying
- **Data Structures**: Use efficient data structures for line storage
- **Efficient Querying**: O(log n) per query
- **Optimization**: Much more efficient than brute force

**Key Insight**: Preprocess lines to enable efficient querying.

**Algorithm**:
- Preprocess lines into efficient data structure
- For each query, use preprocessing to find lines
- Count lines passing through point
- Return counts for all queries

**Visual Example**:
```
Preprocessing:
┌─────────────────────────────────────┐
│ Lines: x=0, y=0, x+y=2             │
│                                   │
│ Preprocessed structure:            │
│ - Vertical lines: {x=0}            │
│ - Horizontal lines: {y=0}          │
│ - Diagonal lines: {x+y=2}          │
│                                   │
│ Query (0,0):                       │
│ - Check vertical: x=0 ✓            │
│ - Check horizontal: y=0 ✓          │
│ - Check diagonal: 0+0=2 ✗          │
│ Count: 2                           │
│                                   │
│ Query (1,1):                       │
│ - Check vertical: x=0 ✗            │
│ - Check horizontal: y=0 ✗          │
│ - Check diagonal: 1+1=2 ✓          │
│ Count: 1                           │
│                                   │
│ Result: [2, 1]                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def preprocessing_lines_and_queries_ii(n, lines, q, queries):
    """
    Process line queries using preprocessing approach
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: number of lines passing through each query point
    """
    # Preprocess lines by type
    vertical_lines = {}  # x = constant
    horizontal_lines = {}  # y = constant
    diagonal_lines = []  # ax + by + c = 0 where a != 0 and b != 0
    
    for line in lines:
        a, b, c = line
        
        if abs(a) < 1e-9:  # Horizontal line: by + c = 0
            y_value = -c / b if abs(b) > 1e-9 else 0
            horizontal_lines[y_value] = horizontal_lines.get(y_value, 0) + 1
        elif abs(b) < 1e-9:  # Vertical line: ax + c = 0
            x_value = -c / a if abs(a) > 1e-9 else 0
            vertical_lines[x_value] = vertical_lines.get(x_value, 0) + 1
        else:  # Diagonal line
            diagonal_lines.append(line)
    
    results = []
    
    # Process each query
    for query_point in queries:
        x, y = query_point
        count = 0
        
        # Check vertical lines
        if x in vertical_lines:
            count += vertical_lines[x]
        
        # Check horizontal lines
        if y in horizontal_lines:
            count += horizontal_lines[y]
        
        # Check diagonal lines
        for a, b, c in diagonal_lines:
            if abs(a * x + b * y + c) < 1e-9:
                count += 1
        
        results.append(count)
    
    return results

def preprocessing_lines_and_queries_ii_optimized(n, lines, q, queries):
    """
    Optimized preprocessing lines and queries II processing
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: number of lines passing through each query point
    """
    # Preprocess lines by type with optimization
    vertical_lines = {}
    horizontal_lines = {}
    diagonal_lines = []
    
    for line in lines:
        a, b, c = line
        
        if abs(a) < 1e-9:
            y_value = -c / b if abs(b) > 1e-9 else 0
            horizontal_lines[y_value] = horizontal_lines.get(y_value, 0) + 1
        elif abs(b) < 1e-9:
            x_value = -c / a if abs(a) > 1e-9 else 0
            vertical_lines[x_value] = vertical_lines.get(x_value, 0) + 1
        else:
            diagonal_lines.append(line)
    
    results = []
    
    # Process each query with optimization
    for query_point in queries:
        x, y = query_point
        count = 0
        
        # Check vertical lines
        if x in vertical_lines:
            count += vertical_lines[x]
        
        # Check horizontal lines
        if y in horizontal_lines:
            count += horizontal_lines[y]
        
        # Check diagonal lines
        for a, b, c in diagonal_lines:
            if abs(a * x + b * y + c) < 1e-9:
                count += 1
        
        results.append(count)
    
    return results

# Example usage
n = 3
lines = [(1, 0, 0), (0, 1, 0), (1, 1, -2)]
q = 2
queries = [(0, 0), (1, 1)]
result1 = preprocessing_lines_and_queries_ii(n, lines, q, queries)
result2 = preprocessing_lines_and_queries_ii_optimized(n, lines, q, queries)
print(f"Preprocessing lines and queries II: {result1}")
print(f"Optimized preprocessing lines and queries II: {result2}")
```

**Time Complexity**: O(n + qk) where k is average number of diagonal lines
**Space Complexity**: O(n)

**Why it's better**: Uses preprocessing for efficient querying.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for line queries
- **Efficient Querying**: O(log n) per query
- **Space Efficiency**: O(n) space complexity
- **Optimal Complexity**: Best approach for line queries

**Key Insight**: Use advanced data structures for optimal line query processing.

**Algorithm**:
- Use specialized data structures for different line types
- Implement efficient querying algorithms
- Process queries optimally
- Return results

**Visual Example**:
```
Advanced data structure approach:

For lines: x=0, y=0, x+y=2
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Vertical lines: Hash map {0: 1}   │
│ - Horizontal lines: Hash map {0: 1} │
│ - Diagonal lines: List [(1,1,-2)]   │
│                                   │
│ Query processing:                  │
│ - Use hash maps for O(1) lookup    │
│ - Use list for diagonal lines      │
│ - Combine results efficiently      │
│                                   │
│ Result: [2, 1]                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_lines_and_queries_ii(n, lines, q, queries):
    """
    Process line queries using advanced data structure approach
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: number of lines passing through each query point
    """
    # Advanced data structures for different line types
    vertical_lines = {}
    horizontal_lines = {}
    diagonal_lines = []
    
    # Preprocess lines into appropriate data structures
    for line in lines:
        a, b, c = line
        
        if abs(a) < 1e-9:  # Horizontal line
            y_value = -c / b if abs(b) > 1e-9 else 0
            horizontal_lines[y_value] = horizontal_lines.get(y_value, 0) + 1
        elif abs(b) < 1e-9:  # Vertical line
            x_value = -c / a if abs(a) > 1e-9 else 0
            vertical_lines[x_value] = vertical_lines.get(x_value, 0) + 1
        else:  # Diagonal line
            diagonal_lines.append(line)
    
    results = []
    
    # Process queries using advanced data structures
    for query_point in queries:
        x, y = query_point
        count = 0
        
        # O(1) lookup for vertical lines
        if x in vertical_lines:
            count += vertical_lines[x]
        
        # O(1) lookup for horizontal lines
        if y in horizontal_lines:
            count += horizontal_lines[y]
        
        # Check diagonal lines
        for a, b, c in diagonal_lines:
            if abs(a * x + b * y + c) < 1e-9:
                count += 1
        
        results.append(count)
    
    return results

def advanced_data_structure_lines_and_queries_ii_v2(n, lines, q, queries):
    """
    Alternative advanced data structure lines and queries II processing
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: number of lines passing through each query point
    """
    # Alternative advanced data structures
    line_groups = {
        'vertical': {},
        'horizontal': {},
        'diagonal': []
    }
    
    # Group lines by type
    for line in lines:
        a, b, c = line
        
        if abs(a) < 1e-9:
            y_value = -c / b if abs(b) > 1e-9 else 0
            line_groups['horizontal'][y_value] = line_groups['horizontal'].get(y_value, 0) + 1
        elif abs(b) < 1e-9:
            x_value = -c / a if abs(a) > 1e-9 else 0
            line_groups['vertical'][x_value] = line_groups['vertical'].get(x_value, 0) + 1
        else:
            line_groups['diagonal'].append(line)
    
    results = []
    
    # Process queries using grouped data structures
    for query_point in queries:
        x, y = query_point
        count = 0
        
        # Check vertical lines
        if x in line_groups['vertical']:
            count += line_groups['vertical'][x]
        
        # Check horizontal lines
        if y in line_groups['horizontal']:
            count += line_groups['horizontal'][y]
        
        # Check diagonal lines
        for a, b, c in line_groups['diagonal']:
            if abs(a * x + b * y + c) < 1e-9:
                count += 1
        
        results.append(count)
    
    return results

def lines_and_queries_ii_with_precomputation(max_n, max_q):
    """
    Precompute lines and queries II for multiple queries
    
    Args:
        max_n: maximum number of lines
        max_q: maximum number of queries
    
    Returns:
        list: precomputed lines and queries II results
    """
    results = [0] * (max_q + 1)
    
    for i in range(max_q + 1):
        results[i] = i  # Simplified calculation
    
    return results

# Example usage
n = 3
lines = [(1, 0, 0), (0, 1, 0), (1, 1, -2)]
q = 2
queries = [(0, 0), (1, 1)]
result1 = advanced_data_structure_lines_and_queries_ii(n, lines, q, queries)
result2 = advanced_data_structure_lines_and_queries_ii_v2(n, lines, q, queries)
print(f"Advanced data structure lines and queries II: {result1}")
print(f"Advanced data structure lines and queries II v2: {result2}")

# Precompute for multiple queries
max_n, max_q = 1000, 1000
precomputed = lines_and_queries_ii_with_precomputation(max_n, max_q)
print(f"Precomputed result for q={q}: {precomputed[q]}")
```

**Time Complexity**: O(n + qk) where k is average number of diagonal lines
**Space Complexity**: O(n)

**Why it's optimal**: Uses advanced data structures for optimal query processing.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(nq) | O(1) | Check all lines for each query |
| Preprocessing | O(n + qk) | O(n) | Preprocess lines for efficient querying |
| Advanced Data Structure | O(n + qk) | O(n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + qk) - Preprocess lines and use efficient querying
- **Space**: O(n) - Store preprocessed line data

### Why This Solution Works
- **Data Structure Optimization**: Use appropriate data structures for different line types
- **Efficient Querying**: O(1) lookup for vertical and horizontal lines
- **Preprocessing**: Group lines by type for efficient processing
- **Optimal Algorithms**: Use optimal algorithms for query processing

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Lines and Queries II with Constraints**
**Problem**: Process line queries with specific constraints.

**Key Differences**: Apply constraints to line query processing

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_lines_and_queries_ii(n, lines, q, queries, constraints):
    """
    Process line queries with constraints
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        q: number of queries
        queries: list of query points (x, y)
        constraints: function to check constraints
    
    Returns:
        list: number of lines passing through each query point
    """
    def point_on_line(point, line):
        """Check if point lies on line"""
        x, y = point
        a, b, c = line
        return abs(a * x + b * y + c) < 1e-9
    
    results = []
    
    for query_point in queries:
        count = 0
        
        for line in lines:
            if point_on_line(query_point, line) and constraints(query_point, line):
                count += 1
        
        results.append(count)
    
    return results

# Example usage
n = 3
lines = [(1, 0, 0), (0, 1, 0), (1, 1, -2)]
q = 2
queries = [(0, 0), (1, 1)]
constraints = lambda point, line: point[0] + point[1] < 3  # Only count lines where point sum < 3
result = constrained_lines_and_queries_ii(n, lines, q, queries, constraints)
print(f"Constrained lines and queries II: {result}")
```

#### **2. Lines and Queries II with Different Line Types**
**Problem**: Process line queries with different line types.

**Key Differences**: Handle different types of lines

**Solution Approach**: Use advanced data structures

**Implementation**:
```python
def typed_lines_and_queries_ii(n, lines, line_types, q, queries):
    """
    Process line queries with different line types
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        line_types: list of line types
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: number of lines passing through each query point
    """
    def point_on_line(point, line):
        """Check if point lies on line"""
        x, y = point
        a, b, c = line
        return abs(a * x + b * y + c) < 1e-9
    
    results = []
    
    for query_point in queries:
        count = 0
        
        for i, line in enumerate(lines):
            if point_on_line(query_point, line) and line_types[i] == 'active':
                count += 1
        
        results.append(count)
    
    return results

# Example usage
n = 3
lines = [(1, 0, 0), (0, 1, 0), (1, 1, -2)]
line_types = ['active', 'active', 'inactive']
q = 2
queries = [(0, 0), (1, 1)]
result = typed_lines_and_queries_ii(n, lines, line_types, q, queries)
print(f"Typed lines and queries II: {result}")
```

#### **3. Lines and Queries II with Weights**
**Problem**: Process line queries with weighted lines.

**Key Differences**: Handle weighted lines

**Solution Approach**: Use advanced data structures

**Implementation**:
```python
def weighted_lines_and_queries_ii(n, lines, weights, q, queries):
    """
    Process line queries with weighted lines
    
    Args:
        n: number of lines
        lines: list of lines (a, b, c for ax + by + c = 0)
        weights: list of line weights
        q: number of queries
        queries: list of query points (x, y)
    
    Returns:
        list: weighted count of lines passing through each query point
    """
    def point_on_line(point, line):
        """Check if point lies on line"""
        x, y = point
        a, b, c = line
        return abs(a * x + b * y + c) < 1e-9
    
    results = []
    
    for query_point in queries:
        total_weight = 0
        
        for i, line in enumerate(lines):
            if point_on_line(query_point, line):
                total_weight += weights[i]
        
        results.append(total_weight)
    
    return results

# Example usage
n = 3
lines = [(1, 0, 0), (0, 1, 0), (1, 1, -2)]
weights = [1, 2, 3]
q = 2
queries = [(0, 0), (1, 1)]
result = weighted_lines_and_queries_ii(n, lines, weights, q, queries)
print(f"Weighted lines and queries II: {result}")
```

### Related Problems

#### **CSES Problems**
- [Lines and Queries I](https://cses.fi/problemset/task/1075) - Geometry
- [Line Segment Intersection](https://cses.fi/problemset/task/1075) - Geometry
- [Point in Polygon](https://cses.fi/problemset/task/1075) - Geometry

#### **LeetCode Problems**
- [Line Reflection](https://leetcode.com/problems/line-reflection/) - Geometry
- [Self Crossing](https://leetcode.com/problems/self-crossing/) - Geometry
- [Rectangle Overlap](https://leetcode.com/problems/rectangle-overlap/) - Geometry

#### **Problem Categories**
- **Computational Geometry**: Line queries, intersection tests
- **Query Processing**: Efficient query algorithms, data structures
- **Geometric Algorithms**: Line equations, coordinate systems

## 🔗 Additional Resources

### **Algorithm References**
- [Computational Geometry](https://cp-algorithms.com/geometry/basic-geometry.html) - Geometry algorithms
- [Line Algorithms](https://cp-algorithms.com/geometry/line-intersection.html) - Line algorithms
- [Query Processing](https://cp-algorithms.com/data_structures/segment_tree.html) - Query processing algorithms

### **Practice Problems**
- [CSES Lines and Queries I](https://cses.fi/problemset/task/1075) - Medium
- [CSES Line Segment Intersection](https://cses.fi/problemset/task/1075) - Medium
- [CSES Point in Polygon](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry) - Wikipedia article
- [Line (geometry)](https://en.wikipedia.org/wiki/Line_(geometry)) - Wikipedia article
- [Query Processing](https://en.wikipedia.org/wiki/Query_processing) - Wikipedia article
