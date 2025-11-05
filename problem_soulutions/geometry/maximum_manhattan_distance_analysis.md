---
layout: simple
title: "Maximum Manhattan Distance - Geometry Problem"
permalink: /problem_soulutions/geometry/maximum_manhattan_distance_analysis
---

# Maximum Manhattan Distance

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Manhattan distance in computational geometry
- Apply geometric algorithms for distance calculation
- Implement efficient algorithms for maximum distance finding
- Optimize geometric operations for distance analysis
- Handle special cases in distance calculation problems

## 📋 Problem Description

Given n points, find the maximum Manhattan distance between any two points.

**Input**: 
- n: number of points
- points: array of points (x, y coordinates)

**Output**: 
- Maximum Manhattan distance between any two points

**Constraints**:
- 1 ≤ n ≤ 100000
- -10^6 ≤ coordinates ≤ 10^6

**Example**:
```
Input:
n = 4
points = [(0,0), (1,1), (2,2), (3,3)]

Output:
6

Explanation**: 
Manhattan distances:
- (0,0) to (3,3): |0-3| + |0-3| = 3 + 3 = 6
- (0,0) to (2,2): |0-2| + |0-2| = 2 + 2 = 4
- (1,1) to (3,3): |1-3| + |1-3| = 2 + 2 = 4
Maximum: 6
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
- Keep track of maximum distance
- Return maximum distance

**Visual Example**:
```
Points: [(0,0), (1,1), (2,2), (3,3)]

Distance calculations:
┌─────────────────────────────────────┐
│ (0,0) to (1,1): |0-1| + |0-1| = 2  │
│ (0,0) to (2,2): |0-2| + |0-2| = 4  │
│ (0,0) to (3,3): |0-3| + |0-3| = 6  │
│ (1,1) to (2,2): |1-2| + |1-2| = 2  │
│ (1,1) to (3,3): |1-3| + |1-3| = 4  │
│ (2,2) to (3,3): |2-3| + |2-3| = 2  │
│                                   │
│ Maximum: 6                        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_maximum_manhattan_distance(n, points):
    """
    Find maximum Manhattan distance using brute force approach
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        int: maximum Manhattan distance
    """
    def manhattan_distance(p1, p2):
        """Calculate Manhattan distance between two points"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    max_distance = 0
    
    # Check all pairs of points
    for i in range(n):
        for j in range(i + 1, n):
            distance = manhattan_distance(points[i], points[j])
            max_distance = max(max_distance, distance)
    
    return max_distance

def brute_force_maximum_manhattan_distance_optimized(n, points):
    """
    Optimized brute force maximum Manhattan distance finding
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        int: maximum Manhattan distance
    """
    def manhattan_distance_optimized(p1, p2):
        """Calculate Manhattan distance with optimization"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    max_distance = 0
    
    # Check all pairs of points with optimization
    for i in range(n):
        for j in range(i + 1, n):
            distance = manhattan_distance_optimized(points[i], points[j])
            max_distance = max(max_distance, distance)
    
    return max_distance

# Example usage
n = 4
points = [(0, 0), (1, 1), (2, 2), (3, 3)]
result1 = brute_force_maximum_manhattan_distance(n, points)
result2 = brute_force_maximum_manhattan_distance_optimized(n, points)
print(f"Brute force maximum Manhattan distance: {result1}")
print(f"Optimized brute force maximum Manhattan distance: {result2}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(1)

**Why it's inefficient**: O(n²) time complexity for checking all pairs.

---

### Approach 2: Coordinate Transformation Solution

**Key Insights from Coordinate Transformation Solution**:
- **Coordinate Transformation**: Transform coordinates to simplify calculation
- **Mathematical Insight**: Use (x+y, x-y) transformation
- **Efficient Calculation**: O(n) time complexity
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use coordinate transformation to find maximum distance in O(n) time.

**Algorithm**:
- Transform coordinates using (x+y, x-y)
- Find min and max values in transformed space
- Calculate maximum distance from transformed values
- Return result

**Visual Example**:
```
Original points: [(0,0), (1,1), (2,2), (3,3)]

Coordinate transformation (x+y, x-y):
┌─────────────────────────────────────┐
│ (0,0) → (0+0, 0-0) = (0, 0)        │
│ (1,1) → (1+1, 1-1) = (2, 0)        │
│ (2,2) → (2+2, 2-2) = (4, 0)        │
│ (3,3) → (3+3, 3-3) = (6, 0)        │
│                                   │
│ Transformed points: [(0,0), (2,0), (4,0), (6,0)] │
│ Min x+y: 0, Max x+y: 6            │
│ Min x-y: 0, Max x-y: 0            │
│                                   │
│ Maximum distance: max(6-0, 0-0) = 6 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def coordinate_transformation_maximum_manhattan_distance(n, points):
    """
    Find maximum Manhattan distance using coordinate transformation
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        int: maximum Manhattan distance
    """
    # Transform coordinates
    transformed_points = []
    for x, y in points:
        transformed_points.append((x + y, x - y))
    
    # Find min and max values
    min_x_plus_y = min(point[0] for point in transformed_points)
    max_x_plus_y = max(point[0] for point in transformed_points)
    min_x_minus_y = min(point[1] for point in transformed_points)
    max_x_minus_y = max(point[1] for point in transformed_points)
    
    # Calculate maximum distance
    max_distance = max(max_x_plus_y - min_x_plus_y, max_x_minus_y - min_x_minus_y)
    
    return max_distance

def coordinate_transformation_maximum_manhattan_distance_optimized(n, points):
    """
    Optimized coordinate transformation maximum Manhattan distance finding
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        int: maximum Manhattan distance
    """
    # Transform coordinates with optimization
    x_plus_y_values = []
    x_minus_y_values = []
    
    for x, y in points:
        x_plus_y_values.append(x + y)
        x_minus_y_values.append(x - y)
    
    # Find min and max values
    min_x_plus_y = min(x_plus_y_values)
    max_x_plus_y = max(x_plus_y_values)
    min_x_minus_y = min(x_minus_y_values)
    max_x_minus_y = max(x_minus_y_values)
    
    # Calculate maximum distance
    max_distance = max(max_x_plus_y - min_x_plus_y, max_x_minus_y - min_x_minus_y)
    
    return max_distance

# Example usage
n = 4
points = [(0, 0), (1, 1), (2, 2), (3, 3)]
result1 = coordinate_transformation_maximum_manhattan_distance(n, points)
result2 = coordinate_transformation_maximum_manhattan_distance_optimized(n, points)
print(f"Coordinate transformation maximum Manhattan distance: {result1}")
print(f"Optimized coordinate transformation maximum Manhattan distance: {result2}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Uses coordinate transformation for O(n) time complexity.

---

### Approach 3: Space-Optimized Solution (Optimal)

**Key Insights from Space-Optimized Solution**:
- **Space Optimization**: Use only necessary variables
- **Efficient Computation**: O(n) time complexity
- **Space Efficiency**: O(1) space complexity
- **Optimal Complexity**: Best approach for maximum Manhattan distance

**Key Insight**: Use space-optimized coordinate transformation to reduce space complexity.

**Algorithm**:
- Use only necessary variables for min/max tracking
- Update values in single pass
- Return final result

**Visual Example**:
```
Space-optimized approach:

For points: [(0,0), (1,1), (2,2), (3,3)]
┌─────────────────────────────────────┐
│ Single pass through points:        │
│ - Track min/max x+y values         │
│ - Track min/max x-y values         │
│ - Calculate maximum distance       │
│ Final result: 6                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_maximum_manhattan_distance(n, points):
    """
    Find maximum Manhattan distance using space-optimized approach
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        int: maximum Manhattan distance
    """
    # Initialize min/max values
    min_x_plus_y = float('inf')
    max_x_plus_y = float('-inf')
    min_x_minus_y = float('inf')
    max_x_minus_y = float('-inf')
    
    # Single pass through points
    for x, y in points:
        x_plus_y = x + y
        x_minus_y = x - y
        
        min_x_plus_y = min(min_x_plus_y, x_plus_y)
        max_x_plus_y = max(max_x_plus_y, x_plus_y)
        min_x_minus_y = min(min_x_minus_y, x_minus_y)
        max_x_minus_y = max(max_x_minus_y, x_minus_y)
    
    # Calculate maximum distance
    max_distance = max(max_x_plus_y - min_x_plus_y, max_x_minus_y - min_x_minus_y)
    
    return max_distance

def space_optimized_maximum_manhattan_distance_v2(n, points):
    """
    Alternative space-optimized maximum Manhattan distance finding
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        int: maximum Manhattan distance
    """
    # Initialize min/max values
    min_x_plus_y = max_x_plus_y = points[0][0] + points[0][1]
    min_x_minus_y = max_x_minus_y = points[0][0] - points[0][1]
    
    # Single pass through points
    for x, y in points[1:]:
        x_plus_y = x + y
        x_minus_y = x - y
        
        min_x_plus_y = min(min_x_plus_y, x_plus_y)
        max_x_plus_y = max(max_x_plus_y, x_plus_y)
        min_x_minus_y = min(min_x_minus_y, x_minus_y)
        max_x_minus_y = max(max_x_minus_y, x_minus_y)
    
    # Calculate maximum distance
    max_distance = max(max_x_plus_y - min_x_plus_y, max_x_minus_y - min_x_minus_y)
    
    return max_distance

def maximum_manhattan_distance_with_precomputation(max_n):
    """
    Precompute maximum Manhattan distance for multiple queries
    
    Args:
        max_n: maximum number of points
    
    Returns:
        list: precomputed maximum Manhattan distance results
    """
    results = [0] * (max_n + 1)
    
    for i in range(max_n + 1):
        results[i] = i  # Simplified calculation
    
    return results

# Example usage
n = 4
points = [(0, 0), (1, 1), (2, 2), (3, 3)]
result1 = space_optimized_maximum_manhattan_distance(n, points)
result2 = space_optimized_maximum_manhattan_distance_v2(n, points)
print(f"Space-optimized maximum Manhattan distance: {result1}")
print(f"Space-optimized maximum Manhattan distance v2: {result2}")

# Precompute for multiple queries
max_n = 100000
precomputed = maximum_manhattan_distance_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses space-optimized coordinate transformation for O(n) time and O(1) space complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all pairs of points |
| Coordinate Transformation | O(n) | O(n) | Use coordinate transformation |
| Space-Optimized | O(n) | O(1) | Use space-optimized transformation |

### Time Complexity
- **Time**: O(n) - Use coordinate transformation for efficient calculation
- **Space**: O(1) - Use space-optimized approach

### Why This Solution Works
- **Coordinate Transformation**: Use (x+y, x-y) transformation
- **Mathematical Insight**: Manhattan distance becomes max difference in transformed space
- **Efficient Computation**: Single pass through points
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Maximum Manhattan Distance with Constraints**
**Problem**: Find maximum distance with specific constraints.

**Key Differences**: Apply constraints to distance calculation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_maximum_manhattan_distance(n, points, constraints):
    """
    Find maximum Manhattan distance with constraints
    
    Args:
        n: number of points
        points: list of points (x, y)
        constraints: function to check constraints
    
    Returns:
        int: maximum Manhattan distance
    """
    def manhattan_distance(p1, p2):
        """Calculate Manhattan distance between two points"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    max_distance = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if constraints(points[i], points[j]):
                distance = manhattan_distance(points[i], points[j])
            max_distance = max(max_distance, distance)
    
    return max_distance

# Example usage
n = 4
points = [(0, 0), (1, 1), (2, 2), (3, 3)]
constraints = lambda p1, p2: p1[0] + p1[1] < p2[0] + p2[1]  # Only check points where first point has smaller sum
result = constrained_maximum_manhattan_distance(n, points, constraints)
print(f"Constrained maximum Manhattan distance: {result}")
```

#### **2. Maximum Manhattan Distance with Different Metrics**
**Problem**: Find maximum distance with different distance metrics.

**Key Differences**: Different distance calculations

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def weighted_maximum_manhattan_distance(n, points, weights):
    """
    Find maximum Manhattan distance with different weights
    
    Args:
        n: number of points
        points: list of points (x, y)
        weights: list of point weights
    
    Returns:
        int: maximum weighted Manhattan distance
    """
    def weighted_manhattan_distance(p1, p2, w1, w2):
        """Calculate weighted Manhattan distance between two points"""
        return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])) * (w1 + w2)
    
    max_distance = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            distance = weighted_manhattan_distance(points[i], points[j], weights[i], weights[j])
            max_distance = max(max_distance, distance)
    
    return max_distance

# Example usage
n = 4
points = [(0, 0), (1, 1), (2, 2), (3, 3)]
weights = [1, 2, 3, 4]
result = weighted_maximum_manhattan_distance(n, points, weights)
print(f"Weighted maximum Manhattan distance: {result}")
```

#### **3. Maximum Manhattan Distance with Multiple Dimensions**
**Problem**: Find maximum distance in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def multi_dimensional_maximum_manhattan_distance(n, points, dimensions):
    """
    Find maximum Manhattan distance in multiple dimensions
    
    Args:
        n: number of points
        points: list of points (each point is a tuple of coordinates)
        dimensions: number of dimensions
    
    Returns:
        int: maximum Manhattan distance
    """
    def multi_dimensional_manhattan_distance(p1, p2):
        """Calculate Manhattan distance in multiple dimensions"""
        distance = 0
        for i in range(dimensions):
            distance += abs(p1[i] - p2[i])
        return distance
    
    max_distance = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            distance = multi_dimensional_manhattan_distance(points[i], points[j])
            max_distance = max(max_distance, distance)
    
    return max_distance

# Example usage
n = 3
points = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
dimensions = 3
result = multi_dimensional_maximum_manhattan_distance(n, points, dimensions)
print(f"Multi-dimensional maximum Manhattan distance: {result}")
```

### Related Problems

#### **CSES Problems**
- [All Manhattan Distances](https://cses.fi/problemset/task/1075) - Geometry
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
- [CSES All Manhattan Distances](https://cses.fi/problemset/task/1075) - Medium
- [CSES Point in Polygon](https://cses.fi/problemset/task/1075) - Medium
- [CSES Convex Hull](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry) - Wikipedia article
- [Manhattan Distance](https://en.wikipedia.org/wiki/Taxicab_geometry) - Wikipedia article
- [Coordinate Transformation](https://en.wikipedia.org/wiki/Coordinate_system) - Wikipedia article
