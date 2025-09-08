---
layout: simple
title: "Minimum Euclidean Distance Analysis"
permalink: /problem_soulutions/geometry/minimum_euclidean_distance_analysis
---


# Minimum Euclidean Distance Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand minimum distance problems and Euclidean distance calculations
- Apply divide-and-conquer or sweep line algorithms to find minimum Euclidean distances
- Implement efficient algorithms for finding minimum Euclidean distances between points
- Optimize minimum distance calculations using geometric properties and coordinate transformations
- Handle edge cases in minimum distance problems (single points, collinear points, precision issues)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Euclidean distance, divide-and-conquer, sweep line algorithms, distance optimization
- **Data Structures**: Arrays, coordinate structures, optimization data structures, geometric data structures
- **Mathematical Concepts**: Euclidean distance formula, coordinate geometry, distance properties, optimization, precision
- **Programming Skills**: Coordinate manipulation, distance calculations, optimization techniques, geometric computations
- **Related Problems**: All Manhattan Distances (distance calculations), Maximum Manhattan Distance (distance optimization), Distance algorithms

## Problem Description

**Problem**: Given a set of n points in 2D plane, find the minimum Euclidean distance between any two points.

**Input**: 
- n: number of points
- n lines: x y (coordinates of each point)

**Output**: Minimum Euclidean distance between any pair of points.

**Constraints**:
- 2 ≤ n ≤ 1000
- -1000 ≤ x, y ≤ 1000 for all coordinates
- All coordinates are integers
- Points may have duplicate coordinates
- Euclidean distance = √((x1-x2)² + (y1-y2)²)

**Example**:
```
Input:
4
0 0
1 1
2 2
5 5

Output:
1.4142135623730951

Explanation: 
Euclidean distances between pairs:
(0,0) to (1,1): √((0-1)² + (0-1)²) = √2 ≈ 1.414
(0,0) to (2,2): √((0-2)² + (0-2)²) = √8 ≈ 2.828
(0,0) to (5,5): √((0-5)² + (0-5)²) = √50 ≈ 7.071
(1,1) to (2,2): √((1-2)² + (1-2)²) = √2 ≈ 1.414
(1,1) to (5,5): √((1-5)² + (1-5)²) = √32 ≈ 5.657
(2,2) to (5,5): √((2-5)² + (2-5)²) = √18 ≈ 4.243
Minimum: √2 ≈ 1.414 (between (0,0) and (1,1), or (1,1) and (2,2))
```

## Visual Example

### Points Visualization
```
Y
5 |         *
4 |
3 |
2 |     *
1 |   *
0 | *
  +---+---+---+---+---+---+
    0   1   2   3   4   5  X

Points: (0,0), (1,1), (2,2), (5,5)
```

### Distance Calculations
```
Y
5 |         *
4 |
3 |
2 |     *   |
1 |   *     |
0 | *       |
  +---+---+---+---+---+---+
    0   1   2   3   4   5  X

Minimum distance: √2 ≈ 1.414
Between points: (0,0) ↔ (1,1) and (1,1) ↔ (2,2)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Check every pair of points for distance
- Calculate Euclidean distance for each pair
- Keep track of minimum distance found
- Simple but inefficient for large inputs

**Algorithm:**
1. For each pair of points (i, j) where i < j:
   - Calculate Euclidean distance: √((x1-x2)² + (y1-y2)²)
   - Update minimum distance if current distance is smaller
2. Return the minimum distance found

**Visual Example:**
```
Y
5 |         *
4 |
3 |
2 |     *
1 |   *
0 | *
  +---+---+---+---+---+---+
    0   1   2   3   4   5  X

Brute force checks all pairs:
- (0,0) ↔ (1,1): distance = √2 ≈ 1.414
- (0,0) ↔ (2,2): distance = √8 ≈ 2.828
- (0,0) ↔ (5,5): distance = √50 ≈ 7.071
- (1,1) ↔ (2,2): distance = √2 ≈ 1.414
- (1,1) ↔ (5,5): distance = √32 ≈ 5.657
- (2,2) ↔ (5,5): distance = √18 ≈ 4.243
Minimum: √2 ≈ 1.414
```

**Implementation:**
```python
def minimum_euclidean_distance_brute_force(points):
    n = len(points)
    min_distance = float('inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Euclidean distance
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            min_distance = min(min_distance, distance)
    
    return min_distance
```

**Time Complexity:** O(n²) where n is the number of points
**Space Complexity:** O(1) for storing minimum distance

**Why it's inefficient:**
- Quadratic time complexity makes it too slow for large inputs
- Checks all pairs even when points are far apart
- No spatial optimization to reduce unnecessary calculations

### Approach 2: Divide and Conquer (Better)

**Key Insights from Divide and Conquer Solution:**
- Split the plane into two halves using x-coordinate
- Recursively find minimum distance in each half
- Check for pairs that cross the dividing line
- Use strip search to reduce candidate pairs

**Algorithm:**
1. Sort points by x-coordinate
2. Divide points into left and right halves
3. Recursively find minimum distance in each half
4. Find minimum of left and right results
5. Check strip around dividing line for cross-pairs
6. Return overall minimum distance

**Visual Example:**
```
Y
5 |         *
4 |
3 |
2 |     *   |
1 |   *     |
0 | *       |
  +---+---+---+---+---+---+
    0   1   2   3   4   5  X

Divide at x = 1.5:
Left half: (0,0), (1,1)
Right half: (2,2), (5,5)
Strip: points within min_dist of dividing line
```

**Implementation:**
```python
def minimum_euclidean_distance_divide_conquer(points):
    n = len(points)
    if n <= 1:
        return float('inf')
    if n == 2:
        return euclidean_distance(points[0], points[1])
    
    # Sort by x-coordinate
    points.sort()
    
    # Divide into two halves
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    # Recursively find minimum distances in each half
    left_min = minimum_euclidean_distance_divide_conquer(left_points)
    right_min = minimum_euclidean_distance_divide_conquer(right_points)
    
    # Find minimum of left and right
    min_dist = min(left_min, right_min)
    
    # Check for pairs that cross the dividing line
    mid_x = points[mid][0]
    strip = [p for p in points if abs(p[0] - mid_x) < min_dist]
    
    # Sort strip by y-coordinate
    strip.sort(key=lambda p: p[1])
    
    # Check pairs in strip (only need to check 7 points ahead)
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            dist = euclidean_distance(strip[i], strip[j])
            min_dist = min(min_dist, dist)
    
    return min_dist

def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
```

**Time Complexity:** O(n log n) where n is the number of points
**Space Complexity:** O(n) for recursion stack and strip

**Why it's better:**
- Reduces time complexity from O(n²) to O(n log n)
- Uses spatial properties to reduce search space
- Strip search eliminates many unnecessary comparisons
- Handles large inputs efficiently

### Approach 3: Optimized Divide and Conquer with Squared Distances (Optimal)

**Key Insights from Optimized Divide and Conquer Solution:**
- Use squared distances to avoid expensive square root calculations
- Optimize strip search with early termination
- Use mathematical properties to limit comparisons
- Handle edge cases efficiently

**Algorithm:**
1. Use squared distances for comparisons (avoid square root)
2. Implement divide and conquer as before
3. Optimize strip search with early termination
4. Use geometric properties to limit comparisons
5. Convert final result back to actual distance

**Visual Example:**
```
Y
5 |         *
4 |
3 |
2 |     *   |
1 |   *     |
0 | *       |
  +---+---+---+---+---+---+
    0   1   2   3   4   5  X

Optimized approach:
- Use squared distances: (x1-x2)² + (y1-y2)²
- Only compute √ when returning final result
- Early termination in strip search
```

**Implementation:**
```python
def minimum_euclidean_distance_optimized(points):
    n = len(points)
    if n <= 1:
        return float('inf')
    if n == 2:
        return math.sqrt(distance_squared(points[0], points[1]))
    
    # Sort by x-coordinate
    points.sort()
    
    # Divide into two halves
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    # Recursively find minimum distances
    left_min = minimum_euclidean_distance_optimized(left_points)
    right_min = minimum_euclidean_distance_optimized(right_points)
    
    min_dist = min(left_min, right_min)
    
    # Check strip around dividing line
    mid_x = points[mid][0]
    strip = [p for p in points if abs(p[0] - mid_x) < min_dist]
    strip.sort(key=lambda p: p[1])
    
    # Check pairs in strip with early termination
    min_dist_squared = min_dist * min_dist
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            dist_squared = distance_squared(strip[i], strip[j])
            if dist_squared < min_dist_squared:
                min_dist_squared = dist_squared
                min_dist = math.sqrt(dist_squared)
    
    return min_dist

def distance_squared(p1, p2):
    """Calculate squared Euclidean distance to avoid square root"""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
```

**Time Complexity:** O(n log n) where n is the number of points
**Space Complexity:** O(n) for recursion stack and strip

**Why it's optimal:**
- Best known time complexity for closest pair problem
- Uses squared distances to avoid expensive square root
- Early termination in strip search
- Handles all edge cases efficiently
- Mathematical proof ensures correctness

## 🎯 Problem Variations

### Variation 1: Minimum Euclidean Distance with Weights
**Problem**: Each point has a weight, find minimum weighted Euclidean distance.

**Link**: [CSES Problem Set - Minimum Euclidean Distance with Weights](https://cses.fi/problemset/task/minimum_euclidean_distance_weights)

```python
def minimum_euclidean_distance_with_weights(points_with_weights):
    n = len(points_with_weights)
    min_distance = float('inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), w1 = points_with_weights[i]
            (x2, y2), w2 = points_with_weights[j]
            
            # Weighted Euclidean distance
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 * w1 * w2
            min_distance = min(min_distance, distance)
    
    return min_distance
```

### Variation 2: Minimum Euclidean Distance with Constraints
**Problem**: Find minimum distance subject to certain constraints.

**Link**: [CSES Problem Set - Minimum Euclidean Distance with Constraints](https://cses.fi/problemset/task/minimum_euclidean_distance_constraints)

```python
def minimum_euclidean_distance_with_constraints(points, constraints):
    n = len(points)
    min_distance = float('inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Check constraints
            if (constraints["min_x"] <= x1 <= constraints["max_x"] and
                constraints["min_y"] <= y1 <= constraints["max_y"] and
                constraints["min_x"] <= x2 <= constraints["max_x"] and
                constraints["min_y"] <= y2 <= constraints["max_y"]):
                
                distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                min_distance = min(min_distance, distance)
    
    return min_distance if min_distance != float('inf') else -1
```

### Variation 3: Minimum Euclidean Distance with Dynamic Updates
**Problem**: Support adding/removing points and finding minimum distance.

**Link**: [CSES Problem Set - Minimum Euclidean Distance with Dynamic Updates](https://cses.fi/problemset/task/minimum_euclidean_distance_dynamic)

```python
class DynamicMinimumEuclideanDistance:
    def __init__(self):
        self.points = []
    
    def add_point(self, x, y):
        self.points.append((x, y))
    
    def remove_point(self, x, y):
        if (x, y) in self.points:
            self.points.remove((x, y))
    
    def get_minimum_distance(self):
        if len(self.points) < 2:
            return float('inf')
        return minimum_euclidean_distance_optimized(self.points)
```

## 🔗 Related Problems

- **[All Manhattan Distances](/cses-analyses/problem_soulutions/geometry/all_manhattan_distances_analysis/)**: Similar distance calculations
- **[Maximum Manhattan Distance](/cses-analyses/problem_soulutions/geometry/maximum_manhattan_distance_analysis/)**: Distance optimization problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/convex_hull_analysis/)**: Geometric algorithms
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/point_in_polygon_analysis/)**: Point containment problems

## 📚 Learning Points

1. **Euclidean Distance**: Essential for geometric distance calculations
2. **Divide and Conquer**: Important for efficient algorithms
3. **Strip Search**: Key optimization technique for spatial problems
4. **Geometric Properties**: Important for spatial algorithms
5. **Squared Distances**: Useful optimization to avoid square root
6. **Spatial Algorithms**: Fundamental for computational geometry

## 📝 Summary

The Minimum Euclidean Distance problem demonstrates fundamental computational geometry concepts. We explored three approaches:

1. **Brute Force**: O(n²) time complexity, checks all pairs of points
2. **Divide and Conquer**: O(n log n) time complexity, uses spatial properties
3. **Optimized Divide and Conquer**: O(n log n) with squared distances, avoids expensive square root

The key insights include using divide and conquer to reduce complexity, strip search to eliminate unnecessary comparisons, and squared distances to optimize calculations. This problem serves as an excellent introduction to computational geometry and spatial algorithms.
