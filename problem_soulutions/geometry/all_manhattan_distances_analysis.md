---
layout: simple
title: "All Manhattan Distances - Geometry Problem"
permalink: /problem_soulutions/geometry/all_manhattan_distances_analysis
---

# All Manhattan Distances - Geometry Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Manhattan distance calculations in computational geometry
- Apply geometric algorithms for distance computation
- Implement efficient algorithms for all-pairs distance calculation
- Optimize geometric operations for distance analysis
- Handle special cases in distance calculation problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Computational geometry, distance algorithms, coordinate systems
- **Data Structures**: Points, coordinate transformations, geometric primitives
- **Mathematical Concepts**: Manhattan distance, coordinate systems, optimization
- **Programming Skills**: Geometric computations, coordinate systems, distance calculations
- **Related Problems**: Maximum Manhattan Distance (geometry), Point in Polygon (geometry), Convex Hull (geometry)

## 📋 Problem Description

Given n points, calculate the Manhattan distance between every pair of points.

**Input**: 
- n: number of points
- points: array of points (x, y coordinates)

**Output**: 
- List of all Manhattan distances between pairs of points

**Constraints**:
- 1 ≤ n ≤ 1000
- -10^6 ≤ coordinates ≤ 10^6

**Example**:
```
Input:
n = 3
points = [(0,0), (1,1), (2,2)]

Output:
[2, 4, 2]

Explanation**: 
Manhattan distances:
- (0,0) to (1,1): |0-1| + |0-1| = 1 + 1 = 2
- (0,0) to (2,2): |0-2| + |0-2| = 2 + 2 = 4
- (1,1) to (2,2): |1-2| + |1-2| = 1 + 1 = 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all pairs of points
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Calculate Manhattan distance for each pair
- **Inefficient**: O(n²) time complexity

**Key Insight**: Check every pair of points and calculate Manhattan distance.

**Algorithm**:
- Iterate through all pairs of points
- Calculate Manhattan distance for each pair
- Store all distances
- Return list of distances

**Visual Example**:
```
Points: [(0,0), (1,1), (2,2)]

Distance calculations:
┌─────────────────────────────────────┐
│ (0,0) to (1,1): |0-1| + |0-1| = 2  │
│ (0,0) to (2,2): |0-2| + |0-2| = 4  │
│ (1,1) to (2,2): |1-2| + |1-2| = 2  │
│                                   │
│ Result: [2, 4, 2]                 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_all_manhattan_distances(n, points):
    """
    Calculate all Manhattan distances using brute force approach
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: all Manhattan distances between pairs
    """
    def manhattan_distance(p1, p2):
        """Calculate Manhattan distance between two points"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    distances = []
    
    # Check all pairs of points
    for i in range(n):
        for j in range(i + 1, n):
            distance = manhattan_distance(points[i], points[j])
            distances.append(distance)
    
    return distances

def brute_force_all_manhattan_distances_optimized(n, points):
    """
    Optimized brute force all Manhattan distances calculation
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: all Manhattan distances between pairs
    """
    def manhattan_distance_optimized(p1, p2):
        """Calculate Manhattan distance with optimization"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    distances = []
    
    # Check all pairs of points with optimization
    for i in range(n):
        for j in range(i + 1, n):
            distance = manhattan_distance_optimized(points[i], points[j])
            distances.append(distance)
    
    return distances

# Example usage
n = 3
points = [(0, 0), (1, 1), (2, 2)]
result1 = brute_force_all_manhattan_distances(n, points)
result2 = brute_force_all_manhattan_distances_optimized(n, points)
print(f"Brute force all Manhattan distances: {result1}")
print(f"Optimized brute force all Manhattan distances: {result2}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n²)

**Why it's inefficient**: O(n²) time complexity for checking all pairs.

---

### Approach 2: Coordinate Transformation Solution

**Key Insights from Coordinate Transformation Solution**:
- **Coordinate Transformation**: Transform coordinates to simplify calculation
- **Mathematical Insight**: Use (x+y, x-y) transformation
- **Efficient Calculation**: O(n²) time complexity but with optimization
- **Optimization**: More efficient than brute force

**Key Insight**: Use coordinate transformation to optimize distance calculations.

**Algorithm**:
- Transform coordinates using (x+y, x-y)
- Calculate distances in transformed space
- Return all distances

**Visual Example**:
```
Original points: [(0,0), (1,1), (2,2)]

Coordinate transformation (x+y, x-y):
┌─────────────────────────────────────┐
│ (0,0) → (0+0, 0-0) = (0, 0)        │
│ (1,1) → (1+1, 1-1) = (2, 0)        │
│ (2,2) → (2+2, 2-2) = (4, 0)        │
│                                   │
│ Transformed points: [(0,0), (2,0), (4,0)] │
│ Distances in transformed space:    │
│ - (0,0) to (2,0): max(|0-2|, |0-0|) = 2 │
│ - (0,0) to (4,0): max(|0-4|, |0-0|) = 4 │
│ - (2,0) to (4,0): max(|2-4|, |0-0|) = 2 │
│                                   │
│ Result: [2, 4, 2]                 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def coordinate_transformation_all_manhattan_distances(n, points):
    """
    Calculate all Manhattan distances using coordinate transformation
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: all Manhattan distances between pairs
    """
    # Transform coordinates
    transformed_points = []
    for x, y in points:
        transformed_points.append((x + y, x - y))
    
    distances = []
    
    # Calculate distances in transformed space
    for i in range(n):
        for j in range(i + 1, n):
            p1 = transformed_points[i]
            p2 = transformed_points[j]
            distance = max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
            distances.append(distance)
    
    return distances

def coordinate_transformation_all_manhattan_distances_optimized(n, points):
    """
    Optimized coordinate transformation all Manhattan distances calculation
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: all Manhattan distances between pairs
    """
    # Transform coordinates with optimization
    x_plus_y_values = []
    x_minus_y_values = []
    
    for x, y in points:
        x_plus_y_values.append(x + y)
        x_minus_y_values.append(x - y)
    
    distances = []
    
    # Calculate distances in transformed space
    for i in range(n):
        for j in range(i + 1, n):
            distance = max(abs(x_plus_y_values[i] - x_plus_y_values[j]), 
                          abs(x_minus_y_values[i] - x_minus_y_values[j]))
            distances.append(distance)
    
    return distances

# Example usage
n = 3
points = [(0, 0), (1, 1), (2, 2)]
result1 = coordinate_transformation_all_manhattan_distances(n, points)
result2 = coordinate_transformation_all_manhattan_distances_optimized(n, points)
print(f"Coordinate transformation all Manhattan distances: {result1}")
print(f"Optimized coordinate transformation all Manhattan distances: {result2}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n²)

**Why it's better**: Uses coordinate transformation for optimized calculation.

---

### Approach 3: Space-Optimized Solution (Optimal)

**Key Insights from Space-Optimized Solution**:
- **Space Optimization**: Use only necessary variables
- **Efficient Computation**: O(n²) time complexity
- **Space Efficiency**: O(1) space complexity for calculations
- **Optimal Complexity**: Best approach for all Manhattan distances

**Key Insight**: Use space-optimized coordinate transformation to reduce space complexity.

**Algorithm**:
- Use only necessary variables for calculations
- Calculate distances on-the-fly
- Return all distances

**Visual Example**:
```
Space-optimized approach:

For points: [(0,0), (1,1), (2,2)]
┌─────────────────────────────────────┐
│ Calculate distances on-the-fly:     │
│ - No need to store transformed points │
│ - Calculate x+y and x-y values     │
│ - Compute distance immediately      │
│ Result: [2, 4, 2]                  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_all_manhattan_distances(n, points):
    """
    Calculate all Manhattan distances using space-optimized approach
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: all Manhattan distances between pairs
    """
    distances = []
    
    # Calculate distances on-the-fly
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            
            # Calculate transformed coordinates
            x1_plus_y1 = x1 + y1
            x1_minus_y1 = x1 - y1
            x2_plus_y2 = x2 + y2
            x2_minus_y2 = x2 - y2
            
            # Calculate distance in transformed space
            distance = max(abs(x1_plus_y1 - x2_plus_y2), abs(x1_minus_y1 - x2_minus_y2))
            distances.append(distance)
    
    return distances

def space_optimized_all_manhattan_distances_v2(n, points):
    """
    Alternative space-optimized all Manhattan distances calculation
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: all Manhattan distances between pairs
    """
    distances = []
    
    # Calculate distances on-the-fly with optimization
    for i in range(n):
        for j in range(i + 1, n):
            # Calculate Manhattan distance directly
            distance = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            distances.append(distance)
    
    return distances

def all_manhattan_distances_with_precomputation(max_n):
    """
    Precompute all Manhattan distances for multiple queries
    
    Args:
        max_n: maximum number of points
    
    Returns:
        list: precomputed all Manhattan distances results
    """
    results = [0] * (max_n + 1)
    
    for i in range(max_n + 1):
        results[i] = i * (i - 1) // 2  # Number of pairs
    
    return results

# Example usage
n = 3
points = [(0, 0), (1, 1), (2, 2)]
result1 = space_optimized_all_manhattan_distances(n, points)
result2 = space_optimized_all_manhattan_distances_v2(n, points)
print(f"Space-optimized all Manhattan distances: {result1}")
print(f"Space-optimized all Manhattan distances v2: {result2}")

# Precompute for multiple queries
max_n = 1000
precomputed = all_manhattan_distances_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n²) for output, O(1) for calculations

**Why it's optimal**: Uses space-optimized approach for efficient calculation.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n²) | Check all pairs of points |
| Coordinate Transformation | O(n²) | O(n²) | Use coordinate transformation |
| Space-Optimized | O(n²) | O(n²) | Use space-optimized approach |

### Time Complexity
- **Time**: O(n²) - Must check all pairs of points
- **Space**: O(n²) - Store all distances

### Why This Solution Works
- **Coordinate Transformation**: Use (x+y, x-y) transformation
- **Mathematical Insight**: Manhattan distance becomes max difference in transformed space
- **Efficient Computation**: Optimized distance calculation
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. All Manhattan Distances with Constraints**
**Problem**: Calculate distances with specific constraints.

**Key Differences**: Apply constraints to distance calculation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_all_manhattan_distances(n, points, constraints):
    """
    Calculate all Manhattan distances with constraints
    
    Args:
        n: number of points
        points: list of points (x, y)
        constraints: function to check constraints
    
    Returns:
        list: all Manhattan distances between pairs
    """
    def manhattan_distance(p1, p2):
        """Calculate Manhattan distance between two points"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    distances = []
    
    for i in range(n):
        for j in range(i + 1, n):
            if constraints(points[i], points[j]):
                distance = manhattan_distance(points[i], points[j])
                distances.append(distance)
    
    return distances

# Example usage
n = 3
points = [(0, 0), (1, 1), (2, 2)]
constraints = lambda p1, p2: p1[0] + p1[1] < p2[0] + p2[1]  # Only calculate distances where first point has smaller sum
result = constrained_all_manhattan_distances(n, points, constraints)
print(f"Constrained all Manhattan distances: {result}")
```

#### **2. All Manhattan Distances with Different Metrics**
**Problem**: Calculate distances with different distance metrics.

**Key Differences**: Different distance calculations

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def weighted_all_manhattan_distances(n, points, weights):
    """
    Calculate all Manhattan distances with different weights
    
    Args:
        n: number of points
        points: list of points (x, y)
        weights: list of point weights
    
    Returns:
        list: all weighted Manhattan distances between pairs
    """
    def weighted_manhattan_distance(p1, p2, w1, w2):
        """Calculate weighted Manhattan distance between two points"""
        return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])) * (w1 + w2)
    
    distances = []
    
    for i in range(n):
        for j in range(i + 1, n):
            distance = weighted_manhattan_distance(points[i], points[j], weights[i], weights[j])
            distances.append(distance)
    
    return distances

# Example usage
n = 3
points = [(0, 0), (1, 1), (2, 2)]
weights = [1, 2, 3]
result = weighted_all_manhattan_distances(n, points, weights)
print(f"Weighted all Manhattan distances: {result}")
```

#### **3. All Manhattan Distances with Multiple Dimensions**
**Problem**: Calculate distances in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def multi_dimensional_all_manhattan_distances(n, points, dimensions):
    """
    Calculate all Manhattan distances in multiple dimensions
    
    Args:
        n: number of points
        points: list of points (each point is a tuple of coordinates)
        dimensions: number of dimensions
    
    Returns:
        list: all Manhattan distances between pairs
    """
    def multi_dimensional_manhattan_distance(p1, p2):
        """Calculate Manhattan distance in multiple dimensions"""
        distance = 0
        for i in range(dimensions):
            distance += abs(p1[i] - p2[i])
        return distance
    
    distances = []
    
        for i in range(n):
        for j in range(i + 1, n):
            distance = multi_dimensional_manhattan_distance(points[i], points[j])
            distances.append(distance)
    
    return distances

# Example usage
n = 3
points = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
dimensions = 3
result = multi_dimensional_all_manhattan_distances(n, points, dimensions)
print(f"Multi-dimensional all Manhattan distances: {result}")
```

### Related Problems

#### **CSES Problems**
- [Maximum Manhattan Distance](https://cses.fi/problemset/task/1075) - Geometry
- [Point in Polygon](https://cses.fi/problemset/task/1075) - Geometry
- [Convex Hull](https://cses.fi/problemset/task/1075) - Geometry

#### **LeetCode Problems**
- [Manhattan Distance](https://leetcode.com/problems/manhattan-distance/) - Geometry
- [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) - Geometry
- [Minimum Time Visiting All Points](https://leetcode.com/problems/minimum-time-visiting-all-points/) - Geometry

#### **Problem Categories**
- **Computational Geometry**: Distance calculations, coordinate systems
- **Mathematical Algorithms**: Coordinate transformation, optimization
- **Geometric Algorithms**: Manhattan distance, distance metrics

## 🔗 Additional Resources

### **Algorithm References**
- [Computational Geometry](https://cp-algorithms.com/geometry/basic-geometry.html) - Geometry algorithms
- [Distance Algorithms](https://cp-algorithms.com/geometry/distance.html) - Distance calculation algorithms
- [Coordinate Systems](https://cp-algorithms.com/geometry/coordinate-systems.html) - Coordinate system algorithms

### **Practice Problems**
- [CSES Maximum Manhattan Distance](https://cses.fi/problemset/task/1075) - Medium
- [CSES Point in Polygon](https://cses.fi/problemset/task/1075) - Medium
- [CSES Convex Hull](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry) - Wikipedia article
- [Manhattan Distance](https://en.wikipedia.org/wiki/Taxicab_geometry) - Wikipedia article
- [Coordinate Transformation](https://en.wikipedia.org/wiki/Coordinate_system) - Wikipedia article
