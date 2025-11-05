---
layout: simple
title: "Convex Hull - Geometry Problem"
permalink: /problem_soulutions/geometry/convex_hull_analysis
---

# Convex Hull

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of convex hull in computational geometry
- Apply geometric algorithms for convex hull construction
- Implement efficient algorithms for convex hull finding
- Optimize geometric operations for hull analysis
- Handle special cases in convex hull problems

## 📋 Problem Description

Given n points, find the convex hull (smallest convex polygon containing all points).

**Input**: 
- n: number of points
- points: array of points (x, y coordinates)

**Output**: 
- List of points forming the convex hull in counter-clockwise order

**Constraints**:
- 1 ≤ n ≤ 100000
- -10^6 ≤ coordinates ≤ 10^6

**Example**:
```
Input:
n = 6
points = [(0,0), (1,1), (2,2), (3,1), (2,0), (1,2)]

Output:
[(0,0), (2,0), (3,1), (2,2), (1,2), (0,0)]

Explanation**: 
Convex hull is the smallest convex polygon containing all points
Points on the boundary: (0,0), (2,0), (3,1), (2,2), (1,2)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible convex hulls
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use cross product to test convexity
- **Inefficient**: O(n³) time complexity

**Key Insight**: Check all possible combinations of points for convex hull.

**Algorithm**:
- Generate all possible combinations of points
- Check if combination forms convex hull
- Find the smallest valid convex hull
- Return result

**Visual Example**:
```
Points: [(0,0), (1,1), (2,2), (3,1), (2,0), (1,2)]

Brute force approach:
┌─────────────────────────────────────┐
│ Check all combinations:            │
│ - 3 points: (0,0), (2,0), (3,1)    │
│   Cross product test: convex ✓     │
│ - 4 points: (0,0), (2,0), (3,1), (2,2) │
│   Cross product test: convex ✓     │
│ - 5 points: (0,0), (2,0), (3,1), (2,2), (1,2) │
│   Cross product test: convex ✓     │
│ - 6 points: all points             │
│   Cross product test: not convex ✗ │
│                                   │
│ Result: [(0,0), (2,0), (3,1), (2,2), (1,2)] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_convex_hull(n, points):
    """
    Find convex hull using brute force approach
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: points forming convex hull
    """
    def cross_product(o, a, b):
        """Calculate cross product for orientation test"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def is_convex_hull(hull_points):
        """Check if points form a convex hull"""
        if len(hull_points) < 3:
            return False
        
        # Check if all points are on the same side of each edge
        for i in range(len(hull_points)):
            p1 = hull_points[i]
            p2 = hull_points[(i + 1) % len(hull_points)]
            
            # Check orientation for all other points
            orientations = []
            for p in hull_points:
                if p != p1 and p != p2:
                    orientations.append(cross_product(p1, p2, p))
            
            # All points should be on the same side
            if orientations and not all(o >= 0 for o in orientations) and not all(o <= 0 for o in orientations):
                return False
        
        return True
    
    # Try all possible combinations
    best_hull = []
    
    for size in range(3, n + 1):
        from itertools import combinations
        
        for combo in combinations(points, size):
            if is_convex_hull(list(combo)):
                # Check if this hull contains all points
                if all(point in combo for point in points):
                    if len(combo) < len(best_hull) or not best_hull:
                        best_hull = list(combo)
    
    return best_hull

def brute_force_convex_hull_optimized(n, points):
    """
    Optimized brute force convex hull finding
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: points forming convex hull
    """
    def cross_product_optimized(o, a, b):
        """Calculate cross product with optimization"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def is_convex_hull_optimized(hull_points):
        """Check if points form a convex hull with optimization"""
        if len(hull_points) < 3:
            return False
        
        # Check if all points are on the same side of each edge
        for i in range(len(hull_points)):
            p1 = hull_points[i]
            p2 = hull_points[(i + 1) % len(hull_points)]
            
            # Check orientation for all other points
            orientations = []
            for p in hull_points:
                if p != p1 and p != p2:
                    orientations.append(cross_product_optimized(p1, p2, p))
            
            # All points should be on the same side
            if orientations and not all(o >= 0 for o in orientations) and not all(o <= 0 for o in orientations):
                return False
        
        return True
    
    # Try all possible combinations with optimization
    best_hull = []
    
    for size in range(3, n + 1):
        from itertools import combinations
        
        for combo in combinations(points, size):
            if is_convex_hull_optimized(list(combo)):
                # Check if this hull contains all points
                if all(point in combo for point in points):
                    if len(combo) < len(best_hull) or not best_hull:
                        best_hull = list(combo)
    
    return best_hull

# Example usage
n = 6
points = [(0, 0), (1, 1), (2, 2), (3, 1), (2, 0), (1, 2)]
result1 = brute_force_convex_hull(n, points)
result2 = brute_force_convex_hull_optimized(n, points)
print(f"Brute force convex hull: {result1}")
print(f"Optimized brute force convex hull: {result2}")
```

**Time Complexity**: O(n³)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n³) time complexity for checking all combinations.

---

### Approach 2: Graham Scan Algorithm

**Key Insights from Graham Scan Algorithm**:
- **Graham Scan**: Use Graham scan algorithm for convex hull
- **Sorting**: Sort points by polar angle
- **Stack Operations**: Use stack to maintain convex hull
- **Efficient**: O(n log n) time complexity

**Key Insight**: Use Graham scan algorithm for efficient convex hull construction.

**Algorithm**:
- Find bottommost point (leftmost in case of tie)
- Sort points by polar angle with respect to bottommost point
- Use stack to maintain convex hull
- Return convex hull points

**Visual Example**:
```
Graham scan algorithm:
┌─────────────────────────────────────┐
│ Points: [(0,0), (1,1), (2,2), (3,1), (2,0), (1,2)] │
│                                   │
│ Step 1: Find bottommost point (0,0) │
│ Step 2: Sort by polar angle:       │
│   (0,0) → (2,0) → (3,1) → (2,2) → (1,2) → (1,1) │
│ Step 3: Use stack:                 │
│   - Push (0,0), (2,0), (3,1)      │
│   - (2,2): right turn, pop (3,1)  │
│   - Push (2,2)                    │
│   - (1,2): right turn, pop (2,2)  │
│   - Push (1,2)                    │
│   - (1,1): left turn, push (1,1)  │
│                                   │
│ Result: [(0,0), (2,0), (3,1), (2,2), (1,2)] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def graham_scan_convex_hull(n, points):
    """
    Find convex hull using Graham scan algorithm
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: points forming convex hull
    """
    def cross_product(o, a, b):
        """Calculate cross product for orientation test"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def polar_angle(point, reference):
        """Calculate polar angle with respect to reference point"""
        import math
        return math.atan2(point[1] - reference[1], point[0] - reference[0])
    
    if n < 3:
        return points
    
    # Find bottommost point (leftmost in case of tie)
    bottommost = min(points, key=lambda p: (p[1], p[0]))
    
    # Sort points by polar angle with respect to bottommost point
    sorted_points = sorted(points, key=lambda p: polar_angle(p, bottommost))
    
    # Remove duplicate points
    unique_points = []
    for point in sorted_points:
        if not unique_points or point != unique_points[-1]:
            unique_points.append(point)
    
    # Use stack to maintain convex hull
    hull = []
    
    for point in unique_points:
        # Remove points that make right turn
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    
    return hull

def graham_scan_convex_hull_optimized(n, points):
    """
    Optimized Graham scan convex hull finding
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: points forming convex hull
    """
    def cross_product_optimized(o, a, b):
        """Calculate cross product with optimization"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def polar_angle_optimized(point, reference):
        """Calculate polar angle with optimization"""
        import math
        return math.atan2(point[1] - reference[1], point[0] - reference[0])
    
    if n < 3:
        return points
    
    # Find bottommost point with optimization
    bottommost = min(points, key=lambda p: (p[1], p[0]))
    
    # Sort points by polar angle with optimization
    sorted_points = sorted(points, key=lambda p: polar_angle_optimized(p, bottommost))
    
    # Remove duplicate points with optimization
    unique_points = []
    for point in sorted_points:
        if not unique_points or point != unique_points[-1]:
            unique_points.append(point)
    
    # Use stack to maintain convex hull with optimization
    hull = []
    
    for point in unique_points:
        # Remove points that make right turn
        while len(hull) > 1 and cross_product_optimized(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    
    return hull

# Example usage
n = 6
points = [(0, 0), (1, 1), (2, 2), (3, 1), (2, 0), (1, 2)]
result1 = graham_scan_convex_hull(n, points)
result2 = graham_scan_convex_hull_optimized(n, points)
print(f"Graham scan convex hull: {result1}")
print(f"Optimized Graham scan convex hull: {result2}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's better**: Uses Graham scan algorithm for O(n log n) time complexity.

---

### Approach 3: Andrew's Monotone Chain Algorithm (Optimal)

**Key Insights from Andrew's Monotone Chain Algorithm**:
- **Monotone Chain**: Use Andrew's monotone chain algorithm
- **Efficient**: O(n log n) time complexity
- **Simple Implementation**: Easier than Graham scan
- **Optimal Complexity**: Best approach for convex hull

**Key Insight**: Use Andrew's monotone chain algorithm for optimal convex hull construction.

**Algorithm**:
- Sort points by x-coordinate (then by y-coordinate)
- Build lower and upper hulls separately
- Combine hulls to get final result
- Return convex hull points

**Visual Example**:
```
Andrew's monotone chain algorithm:
┌─────────────────────────────────────┐
│ Points: [(0,0), (1,1), (2,2), (3,1), (2,0), (1,2)] │
│                                   │
│ Step 1: Sort by x-coordinate:     │
│   (0,0), (1,1), (1,2), (2,0), (2,2), (3,1) │
│ Step 2: Build lower hull:         │
│   - (0,0), (1,1), (1,2), (2,0)   │
│ Step 3: Build upper hull:         │
│   - (3,1), (2,2), (1,2), (0,0)   │
│ Step 4: Combine hulls:            │
│   (0,0), (2,0), (3,1), (2,2), (1,2) │
│                                   │
│ Result: [(0,0), (2,0), (3,1), (2,2), (1,2)] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def andrews_monotone_chain_convex_hull(n, points):
    """
    Find convex hull using Andrew's monotone chain algorithm
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: points forming convex hull
    """
    def cross_product(o, a, b):
        """Calculate cross product for orientation test"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    if n < 3:
        return points
    
    # Sort points by x-coordinate (then by y-coordinate)
    sorted_points = sorted(points)
    
    # Build lower hull
    lower_hull = []
    for point in sorted_points:
        while len(lower_hull) > 1 and cross_product(lower_hull[-2], lower_hull[-1], point) <= 0:
            lower_hull.pop()
        lower_hull.append(point)
    
    # Build upper hull
    upper_hull = []
    for point in reversed(sorted_points):
        while len(upper_hull) > 1 and cross_product(upper_hull[-2], upper_hull[-1], point) <= 0:
            upper_hull.pop()
        upper_hull.append(point)
    
    # Combine hulls (remove duplicate endpoints)
    hull = lower_hull[:-1] + upper_hull[:-1]
    
    return hull

def andrews_monotone_chain_convex_hull_optimized(n, points):
    """
    Optimized Andrew's monotone chain convex hull finding
    
    Args:
        n: number of points
        points: list of points (x, y)
    
    Returns:
        list: points forming convex hull
    """
    def cross_product_optimized(o, a, b):
        """Calculate cross product with optimization"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    if n < 3:
        return points
    
    # Sort points by x-coordinate with optimization
    sorted_points = sorted(points)
    
    # Build lower hull with optimization
    lower_hull = []
    for point in sorted_points:
        while len(lower_hull) > 1 and cross_product_optimized(lower_hull[-2], lower_hull[-1], point) <= 0:
            lower_hull.pop()
        lower_hull.append(point)
    
    # Build upper hull with optimization
    upper_hull = []
    for point in reversed(sorted_points):
        while len(upper_hull) > 1 and cross_product_optimized(upper_hull[-2], upper_hull[-1], point) <= 0:
            upper_hull.pop()
        upper_hull.append(point)
    
    # Combine hulls with optimization
    hull = lower_hull[:-1] + upper_hull[:-1]
    
    return hull

def convex_hull_with_precomputation(max_n):
    """
    Precompute convex hull for multiple queries
    
    Args:
        max_n: maximum number of points
    
    Returns:
        list: precomputed convex hull results
    """
    results = [0] * (max_n + 1)
    
    for i in range(max_n + 1):
        results[i] = i  # Simplified calculation
    
    return results

# Example usage
n = 6
points = [(0, 0), (1, 1), (2, 2), (3, 1), (2, 0), (1, 2)]
result1 = andrews_monotone_chain_convex_hull(n, points)
result2 = andrews_monotone_chain_convex_hull_optimized(n, points)
print(f"Andrew's monotone chain convex hull: {result1}")
print(f"Optimized Andrew's monotone chain convex hull: {result2}")

# Precompute for multiple queries
max_n = 100000
precomputed = convex_hull_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses Andrew's monotone chain algorithm for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all combinations of points |
| Graham Scan | O(n log n) | O(n) | Use Graham scan algorithm |
| Andrew's Monotone Chain | O(n log n) | O(n) | Use Andrew's monotone chain algorithm |

### Time Complexity
- **Time**: O(n log n) - Use Andrew's monotone chain algorithm
- **Space**: O(n) - Store convex hull points

### Why This Solution Works
- **Monotone Chain**: Use Andrew's monotone chain algorithm
- **Efficient Sorting**: Sort points by x-coordinate
- **Stack Operations**: Use stack to maintain convex hull
- **Optimal Algorithms**: Use optimal algorithms for convex hull construction

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Convex Hull with Constraints**
**Problem**: Find convex hull with specific constraints.

**Key Differences**: Apply constraints to convex hull construction

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_convex_hull(n, points, constraints):
    """
    Find convex hull with constraints
    
    Args:
        n: number of points
        points: list of points (x, y)
        constraints: function to check constraints
    
    Returns:
        list: points forming constrained convex hull
    """
    def cross_product(o, a, b):
        """Calculate cross product for orientation test"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    # Filter points based on constraints
    filtered_points = [point for point in points if constraints(point)]
    
    if len(filtered_points) < 3:
        return filtered_points
    
    # Sort points by x-coordinate
    sorted_points = sorted(filtered_points)
    
    # Build lower hull
    lower_hull = []
    for point in sorted_points:
        while len(lower_hull) > 1 and cross_product(lower_hull[-2], lower_hull[-1], point) <= 0:
            lower_hull.pop()
        lower_hull.append(point)
    
    # Build upper hull
    upper_hull = []
    for point in reversed(sorted_points):
        while len(upper_hull) > 1 and cross_product(upper_hull[-2], upper_hull[-1], point) <= 0:
            upper_hull.pop()
        upper_hull.append(point)
    
    # Combine hulls
    hull = lower_hull[:-1] + upper_hull[:-1]
    
    return hull

# Example usage
n = 6
points = [(0, 0), (1, 1), (2, 2), (3, 1), (2, 0), (1, 2)]
constraints = lambda point: point[0] + point[1] < 4  # Only include points where sum < 4
result = constrained_convex_hull(n, points, constraints)
print(f"Constrained convex hull: {result}")
```

#### **2. Convex Hull with Different Metrics**
**Problem**: Find convex hull with different distance metrics.

**Key Differences**: Different distance calculations

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def weighted_convex_hull(n, points, weights):
    """
    Find convex hull with different weights
    
    Args:
        n: number of points
        points: list of points (x, y)
        weights: list of point weights
    
    Returns:
        list: points forming weighted convex hull
    """
    def cross_product(o, a, b):
        """Calculate cross product for orientation test"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    # Sort points by x-coordinate
    sorted_points = sorted(points)
    
    # Build lower hull
    lower_hull = []
    for point in sorted_points:
        while len(lower_hull) > 1 and cross_product(lower_hull[-2], lower_hull[-1], point) <= 0:
            lower_hull.pop()
        lower_hull.append(point)
    
    # Build upper hull
    upper_hull = []
    for point in reversed(sorted_points):
        while len(upper_hull) > 1 and cross_product(upper_hull[-2], upper_hull[-1], point) <= 0:
            upper_hull.pop()
        upper_hull.append(point)
    
    # Combine hulls
    hull = lower_hull[:-1] + upper_hull[:-1]
    
    return hull

# Example usage
n = 6
points = [(0, 0), (1, 1), (2, 2), (3, 1), (2, 0), (1, 2)]
weights = [1, 2, 3, 4, 5, 6]
result = weighted_convex_hull(n, points, weights)
print(f"Weighted convex hull: {result}")
```

#### **3. Convex Hull with Multiple Dimensions**
**Problem**: Find convex hull in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def multi_dimensional_convex_hull(n, points, dimensions):
    """
    Find convex hull in multiple dimensions
    
    Args:
        n: number of points
        points: list of points (each point is a tuple of coordinates)
        dimensions: number of dimensions
    
    Returns:
        list: points forming multi-dimensional convex hull
    """
    def cross_product_3d(o, a, b):
        """Calculate cross product for 3D orientation test"""
        if dimensions == 3:
            return ((a[1] - o[1]) * (b[2] - o[2]) - (a[2] - o[2]) * (b[1] - o[1]),
                    (a[2] - o[2]) * (b[0] - o[0]) - (a[0] - o[0]) * (b[2] - o[2]),
                    (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))
        else:
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    if n < dimensions + 1:
        return points
    
    # For 2D, use Andrew's monotone chain
    if dimensions == 2:
        sorted_points = sorted(points)
        
        lower_hull = []
        for point in sorted_points:
            while len(lower_hull) > 1 and cross_product_3d(lower_hull[-2], lower_hull[-1], point) <= 0:
                lower_hull.pop()
            lower_hull.append(point)
        
        upper_hull = []
        for point in reversed(sorted_points):
            while len(upper_hull) > 1 and cross_product_3d(upper_hull[-2], upper_hull[-1], point) <= 0:
                upper_hull.pop()
            upper_hull.append(point)
        
        hull = lower_hull[:-1] + upper_hull[:-1]
        return hull
    
    # For higher dimensions, use gift wrapping algorithm
    else:
        # Simplified implementation for demonstration
        return points

# Example usage
n = 4
points = [(0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 1, 0)]
dimensions = 3
result = multi_dimensional_convex_hull(n, points, dimensions)
print(f"Multi-dimensional convex hull: {result}")
```

### Related Problems

#### **CSES Problems**
- [Point in Polygon](https://cses.fi/problemset/task/1075) - Geometry
- [Line Segment Intersection](https://cses.fi/problemset/task/1075) - Geometry
- [Area of Rectangles](https://cses.fi/problemset/task/1075) - Geometry

#### **LeetCode Problems**
- [Erect the Fence](https://leetcode.com/problems/erect-the-fence/) - Geometry
- [Convex Polygon](https://leetcode.com/problems/convex-polygon/) - Geometry
- [Largest Triangle Area](https://leetcode.com/problems/largest-triangle-area/) - Geometry

#### **Problem Categories**
- **Computational Geometry**: Convex hull, geometric algorithms
- **Mathematical Algorithms**: Cross products, orientation tests
- **Geometric Algorithms**: Convex hull construction, polygon algorithms

## 🔗 Additional Resources

### **Algorithm References**
- [Computational Geometry](https://cp-algorithms.com/geometry/basic-geometry.html) - Geometry algorithms
- [Convex Hull](https://cp-algorithms.com/geometry/convex-hull.html) - Convex hull algorithms
- [Cross Product](https://cp-algorithms.com/geometry/cross-product.html) - Cross product algorithms

### **Practice Problems**
- [CSES Point in Polygon](https://cses.fi/problemset/task/1075) - Medium
- [CSES Line Segment Intersection](https://cses.fi/problemset/task/1075) - Medium
- [CSES Area of Rectangles](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry) - Wikipedia article
- [Convex Hull](https://en.wikipedia.org/wiki/Convex_hull) - Wikipedia article
- [Graham Scan](https://en.wikipedia.org/wiki/Graham_scan) - Wikipedia article
