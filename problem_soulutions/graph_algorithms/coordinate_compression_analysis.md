---
layout: simple
title: "Coordinate Compression - Efficient Coordinate Mapping"
permalink: /problem_soulutions/graph_algorithms/coordinate_compression_analysis
---

# Coordinate Compression - Efficient Coordinate Mapping

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand coordinate compression and efficient coordinate mapping concepts
- Apply sorting and mapping techniques to compress coordinates while preserving relative order
- Implement efficient coordinate compression algorithms with proper sorting and mapping
- Optimize coordinate compression using sorting algorithms and efficient data structures
- Handle edge cases in coordinate compression (duplicate coordinates, large coordinate ranges, empty sets)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Coordinate compression, sorting algorithms, mapping techniques, data structure optimization
- **Data Structures**: Arrays, sorting data structures, mapping structures, coordinate tracking
- **Mathematical Concepts**: Coordinate geometry, sorting theory, mapping theory, optimization
- **Programming Skills**: Sorting implementation, coordinate manipulation, mapping techniques, algorithm implementation
- **Related Problems**: Sorting problems, Coordinate problems, Data structure optimization

## Problem Description

Given n points in a 2D plane, compress the coordinates so that the relative order is preserved but the coordinates are mapped to consecutive integers starting from 0.

**Input**: 
- First line: Integer n (number of points)
- Next n lines: Two integers x and y (coordinates of each point)

**Output**: 
- n lines with two integers each (compressed coordinates)

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- -10⁹ ≤ x, y ≤ 10⁹
- Points can have duplicate coordinates
- Coordinates can be negative
- No self-loops or multiple edges between same pair of points
- Points are numbered 1, 2, ..., n
- Compress coordinates while preserving relative order
- Map coordinates to consecutive integers starting from 0
- Handle duplicate coordinates efficiently
- Preserve ordering relationships between points

**Example**:
```
Input:
5
2 1
1 4
2 1
3 5
1 4

Output:
1 0
0 1
1 0
2 2
0 1
```

**Explanation**: 
- x-coordinates: 1 → 0, 2 → 1, 3 → 2
- y-coordinates: 1 → 0, 4 → 1, 5 → 2
- Relative ordering is preserved in both dimensions

## Visual Example

### Input Points
```
Points: (2,1), (1,4), (2,1), (3,5), (1,4)

Original coordinates:
Point 1: (2, 1)
Point 2: (1, 4)
Point 3: (2, 1)
Point 4: (3, 5)
Point 5: (1, 4)
```

### Coordinate Compression Process
```
Step 1: Extract unique coordinates
x-coordinates: [1, 2, 3]
y-coordinates: [1, 4, 5]

Step 2: Sort coordinates
x-coordinates: [1, 2, 3] → [0, 1, 2]
y-coordinates: [1, 4, 5] → [0, 1, 2]

Step 3: Create mapping
x-mapping: {1: 0, 2: 1, 3: 2}
y-mapping: {1: 0, 4: 1, 5: 2}

Step 4: Apply compression
Point 1: (2,1) → (1,0)
Point 2: (1,4) → (0,1)
Point 3: (2,1) → (1,0)
Point 4: (3,5) → (2,2)
Point 5: (1,4) → (0,1)
```

### Compression Visualization
```
Original coordinates:
(2,1) (1,4) (2,1) (3,5) (1,4)

Compressed coordinates:
(1,0) (0,1) (1,0) (2,2) (0,1)

Relative ordering preserved:
- x: 1 < 2 < 3 → 0 < 1 < 2
- y: 1 < 4 < 5 → 0 < 1 < 2
```

### Key Insight
Coordinate compression works by:
1. Extracting unique coordinate values
2. Sorting coordinates to determine relative order
3. Mapping to consecutive integers starting from 0
4. Preserving relative ordering between points
5. Time complexity: O(n log n) for sorting
6. Space complexity: O(n) for mapping

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Coordinate Mapping (Inefficient)

**Key Insights from Brute Force Solution:**
- Try to map each coordinate individually without optimization
- Simple but computationally expensive approach
- Not suitable for large coordinate ranges
- Straightforward implementation but poor performance

**Algorithm:**
1. For each coordinate, find its position in the sorted list
2. Use linear search to find the mapping for each coordinate
3. Create mapping for each coordinate individually
4. Return compressed coordinates

**Visual Example:**
```
Brute force: Linear search for each coordinate
For coordinates: [2,1,3,2,1]
- For coordinate 2: search in [1,2,3] → position 1
- For coordinate 1: search in [1,2,3] → position 0
- For coordinate 3: search in [1,2,3] → position 2
- Linear search for each coordinate
```

**Implementation:**
```python
def coordinate_compression_brute_force(n, points):
    # Extract x and y coordinates
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    
    # Create sorted unique lists
    unique_x = sorted(set(x_coords))
    unique_y = sorted(set(y_coords))
    
    # Brute force mapping using linear search
    def find_position(coord, sorted_list):
        for i, val in enumerate(sorted_list):
            if val == coord:
                return i
        return -1
    
    # Compress coordinates using linear search
    compressed = []
    for x, y in points:
        compressed_x = find_position(x, unique_x)
        compressed_y = find_position(y, unique_y)
        compressed.append((compressed_x, compressed_y))
    
    return compressed

def solve_coordinate_compression_brute_force():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = coordinate_compression_brute_force(n, points)
    for x, y in result:
        print(x, y)
```

**Time Complexity:** O(n²) for n points with linear search for each coordinate
**Space Complexity:** O(n) for storing coordinates and mapping

**Why it's inefficient:**
- O(n²) time complexity is too slow for large inputs
- Not suitable for competitive programming with n up to 2×10^5
- Inefficient for large coordinate ranges
- Poor performance with many points

### Approach 2: Basic Coordinate Compression with Sorting (Better)

**Key Insights from Basic Compression Solution:**
- Use sorting to determine relative order efficiently
- Much more efficient than brute force approach
- Standard method for coordinate compression
- Can handle larger inputs than brute force

**Algorithm:**
1. Extract unique coordinate values
2. Sort coordinates to determine relative order
3. Create mapping dictionaries using sorted order
4. Apply compression using mapping dictionaries

**Visual Example:**
```
Basic compression for coordinates: [2,1,3,2,1]
- Extract unique: [1,2,3]
- Sort: [1,2,3] → [0,1,2]
- Mapping: {1:0, 2:1, 3:2}
- Compress: [2,1,3,2,1] → [1,0,2,1,0]
```

**Implementation:**
```python
def coordinate_compression_basic(n, points):
    # Extract x and y coordinates
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    
    # Create sorted unique lists
    unique_x = sorted(set(x_coords))
    unique_y = sorted(set(y_coords))
    
    # Create mapping dictionaries
    x_map = {val: idx for idx, val in enumerate(unique_x)}
    y_map = {val: idx for idx, val in enumerate(unique_y)}
    
    # Compress coordinates
    compressed = []
    for x, y in points:
        compressed.append((x_map[x], y_map[y]))
    
    return compressed

def solve_coordinate_compression_basic():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = coordinate_compression_basic(n, points)
    for x, y in result:
        print(x, y)
```

**Time Complexity:** O(n log n) for n points with sorting and mapping
**Space Complexity:** O(n) for storing coordinates and mapping

**Why it's better:**
- O(n log n) time complexity is much better than O(n²)
- Standard method for coordinate compression
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Coordinate Compression with Efficient Data Structures (Optimal)

**Key Insights from Optimized Compression Solution:**
- Use optimized sorting and mapping techniques
- Most efficient approach for coordinate compression
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized data structures for coordinate extraction
2. Perform efficient sorting with built-in algorithms
3. Create optimized mapping dictionaries
4. Apply compression with efficient data access

**Visual Example:**
```
Optimized compression for coordinates: [2,1,3,2,1]
- Optimized extraction: [1,2,3]
- Efficient sorting: [1,2,3] → [0,1,2]
- Optimized mapping: {1:0, 2:1, 3:2}
- Efficient compression: [2,1,3,2,1] → [1,0,2,1,0]
```

**Implementation:**
```python
def coordinate_compression_optimized(n, points):
    # Extract and sort unique coordinates efficiently
    x_coords = sorted(set(point[0] for point in points))
    y_coords = sorted(set(point[1] for point in points))
    
    # Create mapping dictionaries efficiently
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates efficiently
    result = []
    for x, y in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        result.append((compressed_x, compressed_y))
    
    return result

def solve_coordinate_compression():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = coordinate_compression_optimized(n, points)
    for x, y in result:
        print(x, y)

# Main execution
if __name__ == "__main__":
    solve_coordinate_compression()
```

**Time Complexity:** O(n log n) for n points with optimized sorting and mapping
**Space Complexity:** O(n) for storing coordinates and mapping

**Why it's optimal:**
- O(n log n) time complexity is optimal for coordinate compression
- Uses optimized sorting and mapping techniques
- Most efficient approach for competitive programming
- Standard method for coordinate compression

## 🎯 Problem Variations

### Variation 1: Coordinate Compression with Custom Ordering
**Problem**: Compress coordinates with custom ordering function.

**Link**: [CSES Problem Set - Coordinate Compression Custom Order](https://cses.fi/problemset/task/coordinate_compression_custom_order)

```python
def coordinate_compression_custom_order(n, points, order_func):
    # Extract and sort unique coordinates with custom ordering
    x_coords = sorted(set(point[0] for point in points), key=order_func)
    y_coords = sorted(set(point[1] for point in points), key=order_func)
    
    # Create mapping dictionaries
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates
    result = []
    for x, y in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        result.append((compressed_x, compressed_y))
    
    return result
```

### Variation 2: Coordinate Compression with Multiple Dimensions
**Problem**: Compress coordinates in multiple dimensions.

**Link**: [CSES Problem Set - Coordinate Compression Multi-Dimensional](https://cses.fi/problemset/task/coordinate_compression_multi_dimensional)

```python
def coordinate_compression_multi_dimensional(n, points, dimensions):
    # Extract and sort unique coordinates for each dimension
    coord_maps = []
    
    for dim in range(dimensions):
        coords = sorted(set(point[dim] for point in points))
        coord_map = {coord: i for i, coord in enumerate(coords)}
        coord_maps.append(coord_map)
    
    # Compress coordinates for all dimensions
    result = []
    for point in points:
        compressed_point = []
        for dim in range(dimensions):
            compressed_point.append(coord_maps[dim][point[dim]])
        result.append(tuple(compressed_point))
    
    return result
```

### Variation 3: Coordinate Compression with Range Queries
**Problem**: Compress coordinates and support range queries.

**Link**: [CSES Problem Set - Coordinate Compression Range Queries](https://cses.fi/problemset/task/coordinate_compression_range_queries)

```python
def coordinate_compression_range_queries(n, points, queries):
    # Extract and sort unique coordinates
    x_coords = sorted(set(point[0] for point in points))
    y_coords = sorted(set(point[1] for point in points))
    
    # Create mapping dictionaries
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates
    compressed_points = []
    for x, y in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        compressed_points.append((compressed_x, compressed_y))
    
    # Process range queries on compressed coordinates
    results = []
    for query in queries:
        # Process query on compressed coordinates
        result = process_range_query(compressed_points, query)
        results.append(result)
    
    return compressed_points, results
```

## 🔗 Related Problems

- **[Sorting Problems](/cses-analyses/problem_soulutions/sorting_and_searching/)**: Sorting algorithms
- **[Coordinate Problems](/cses-analyses/problem_soulutions/geometry/)**: Coordinate geometry
- **[Data Structure Optimization](/cses-analyses/problem_soulutions/)**: Data structure problems
- **[Mapping Techniques](/cses-analyses/problem_soulutions/)**: Mapping problems

## 📚 Learning Points

1. **Coordinate Compression**: Essential for understanding efficient coordinate mapping
2. **Sorting Algorithms**: Key technique for determining relative order
3. **Mapping Techniques**: Important for understanding coordinate transformation
4. **Data Structure Optimization**: Critical for understanding efficient algorithms
5. **Relative Ordering**: Foundation for many geometric algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Coordinate Compression problem demonstrates fundamental sorting and mapping concepts for efficient coordinate transformation. We explored three approaches:

1. **Brute Force Coordinate Mapping**: O(n²) time complexity using linear search for each coordinate, inefficient for large inputs
2. **Basic Coordinate Compression with Sorting**: O(n log n) time complexity using standard sorting and mapping, better approach for coordinate compression
3. **Optimized Coordinate Compression with Efficient Data Structures**: O(n log n) time complexity with optimized sorting and mapping, optimal approach for coordinate compression

The key insights include understanding sorting principles, using mapping techniques for efficient coordinate transformation, and applying data structure optimization for optimal performance. This problem serves as an excellent introduction to coordinate compression algorithms and efficient data structure techniques.

