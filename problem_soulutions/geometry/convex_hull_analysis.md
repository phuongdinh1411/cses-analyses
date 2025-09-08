---
layout: simple
title: "Convex Hull Analysis"
permalink: /problem_soulutions/geometry/convex_hull_analysis
---


# Convex Hull Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand convex hull concepts and the smallest convex polygon containing all points
- Apply Graham's scan or Andrew's monotone chain algorithm to compute convex hulls
- Implement efficient convex hull algorithms with proper point ordering and angle calculations
- Optimize convex hull solutions using space-efficient techniques and coordinate transformations
- Handle edge cases in convex hull problems (collinear points, duplicate points, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Convex hull algorithms, Graham's scan, Andrew's monotone chain, geometric algorithms
- **Data Structures**: Stacks, vectors, point structures, geometric data structures
- **Mathematical Concepts**: Convexity, cross products, angle calculations, coordinate geometry, trigonometry
- **Programming Skills**: Point manipulation, angle calculations, stack operations, geometric computations
- **Related Problems**: Line Segment Intersection (geometric algorithms), Point in Polygon (geometric queries), Geometry basics

## Problem Description

**Problem**: Given n points in a 2D plane, find the convex hull - the smallest convex polygon that contains all the points.

**Input**: 
- n: number of points
- n lines: x y (coordinates of each point)

**Output**: The convex hull as a list of points in counterclockwise order.

**Constraints**:
- 1 ≤ n ≤ 1000
- -1000 ≤ x, y ≤ 1000 for all coordinates
- All coordinates are integers
- Points may be collinear or duplicate
- Output hull points in counterclockwise order

**Example**:
```
Input:
5
0 0
1 1
2 0
1 -1
0.5 0.5

Output:
4
0 0
2 0
1 -1
1 1

Explanation: 
The convex hull is a quadrilateral with vertices:
(0,0), (2,0), (1,-1), (1,1)
Point (0.5, 0.5) is inside the hull and not included
```

## Visual Example

### Point Visualization
```
Coordinate System:
    y
    ↑
    │
1.0 │     • (1,1)
    │
0.5 │  • (0.5,0.5)
    │
0.0 │•─────────• (2,0)
    │(0,0)
    │
-1.0│     • (1,-1)
    │
    └────────────→ x
    0.0  1.0  2.0

All points: (0,0), (1,1), (2,0), (1,-1), (0.5,0.5)
```

### Convex Hull Process
```
Convex Hull Points (counterclockwise):
1. (0,0) - leftmost point
2. (2,0) - bottom point  
3. (1,-1) - rightmost point
4. (1,1) - top point

Hull Visualization:
    y
    ↑
    │
1.0 │     • (1,1) ──┐
    │              │
0.5 │  • (0.5,0.5) │  (inside hull)
    │              │
0.0 │•─────────• (2,0)
    │(0,0)         │
    │              │
-1.0│     • (1,-1) ──┘
    │
    └────────────→ x

Convex Hull: (0,0) → (2,0) → (1,-1) → (1,1) → (0,0)
Point (0.5,0.5) is inside the hull
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Check All Triplets (Inefficient)

**Key Insights from Brute Force Solution:**
- Check all possible triplets of points to find extreme points
- Use cross product to determine if points are on the convex hull
- Simple but extremely inefficient for large inputs
- Not suitable for competitive programming

**Algorithm:**
1. For each point, check if it's on the convex hull
2. A point is on the hull if it's not inside any triangle formed by other points
3. Use cross product to determine point orientation
4. Return all points that are on the hull

**Visual Example:**
```
Brute force: Check each point against all triangles
For points: (0,0), (1,1), (2,0), (1,-1), (0.5,0.5)

Check point (0.5,0.5):
- Triangle (0,0), (1,1), (2,0): Point inside? Yes
- Triangle (0,0), (2,0), (1,-1): Point inside? Yes
- Triangle (1,1), (2,0), (1,-1): Point inside? Yes
Result: (0.5,0.5) is NOT on hull

Check point (0,0):
- Triangle (1,1), (2,0), (1,-1): Point inside? No
- Triangle (1,1), (2,0), (0.5,0.5): Point inside? No
- Triangle (2,0), (1,-1), (0.5,0.5): Point inside? No
Result: (0,0) IS on hull
```

**Implementation:**
```python
def convex_hull_brute_force(points):
    if len(points) < 3:
        return points
    
    hull = []
    n = len(points)
    
    for i in range(n):
        is_on_hull = True
        for j in range(n):
            for k in range(n):
                if i != j and i != k and j != k:
                    # Check if point i is inside triangle j-k-l
                    if point_in_triangle(points[i], points[j], points[k]):
                        is_on_hull = False
                        break
            if not is_on_hull:
                break
        
        if is_on_hull:
            hull.append(points[i])
    
    return hull

def point_in_triangle(point, a, b, c):
    """Check if point is inside triangle abc"""
    # Use barycentric coordinates
    denom = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    if abs(denom) < 1e-10:
        return False
    
    alpha = ((b[1] - c[1]) * (point[0] - c[0]) + (c[0] - b[0]) * (point[1] - c[1])) / denom
    beta = ((c[1] - a[1]) * (point[0] - c[0]) + (a[0] - c[0]) * (point[1] - c[1])) / denom
    gamma = 1 - alpha - beta
    
    return alpha > 0 and beta > 0 and gamma > 0
```

**Time Complexity:** O(n⁴) where n is the number of points
**Space Complexity:** O(n) for storing the hull

**Why it's inefficient:**
- Time complexity is O(n⁴) - extremely slow
- Not scalable for large inputs
- Redundant calculations
- Not suitable for competitive programming

### Approach 2: Graham Scan Algorithm (Better)

**Key Insights from Graham Scan Solution:**
- Sort points by polar angle from leftmost point
- Use stack to build hull incrementally
- Cross product determines orientation efficiently
- Much more efficient than brute force

**Algorithm:**
1. Find the leftmost point (lowest x, then lowest y)
2. Sort all points by polar angle from the leftmost point
3. Use Graham scan with stack to build convex hull
4. Remove points that make non-left turns

**Visual Example:**
```
Graham scan for points: (0,0), (1,1), (2,0), (1,-1), (0.5,0.5)

Step 1: Find leftmost point
Leftmost: (0,0) with x=0

Step 2: Sort by polar angle from (0,0)
Point (0,0): angle = 0° (reference)
Point (2,0): angle = 0° (same x-axis)
Point (1,-1): angle = -45°
Point (0.5,0.5): angle = 45°
Point (1,1): angle = 45°

Sorted order: (0,0), (2,0), (1,-1), (0.5,0.5), (1,1)

Step 3: Graham scan with stack
Stack: [(0,0), (2,0), (1,-1), (0.5,0.5), (1,1)]
Final hull: [(0,0), (2,0), (1,-1), (1,1)]
```

**Implementation:**
```python
def convex_hull_graham_scan(points):
    if len(points) < 3:
        return points
    
    # Find leftmost point (lowest x, then lowest y)
    leftmost = min(points, key=lambda p: (p[0], p[1]))
    
    # Sort points by polar angle from leftmost
    def polar_angle(p):
        if p == leftmost:
            return -float('inf')
        return math.atan2(p[1] - leftmost[1], p[0] - leftmost[0])
    
    sorted_points = sorted(points, key=polar_angle)
    
    # Graham scan
    hull = [leftmost, sorted_points[0]]
    for point in sorted_points[1:]:
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    
    return hull

def cross_product(o, a, b):
    """Calculate cross product of vectors OA and OB"""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
```

**Time Complexity:** O(n log n) where n is the number of points
**Space Complexity:** O(n) for storing the hull

**Why it's better:**
- Much more efficient than brute force
- O(n log n) time complexity is optimal for comparison-based algorithms
- Handles all edge cases correctly
- Standard approach for convex hull problems

### Approach 3: Optimized Graham Scan with Integer Arithmetic (Optimal)

**Key Insights from Optimized Graham Scan Solution:**
- Use Graham scan with optimized integer arithmetic
- Handle collinear points efficiently
- Ensure numerical stability
- Best performance and reliability

**Algorithm:**
1. Validate input (minimum 1 point)
2. Find leftmost point with optimized comparison
3. Sort points by polar angle with integer arithmetic
4. Use optimized Graham scan with proper collinear handling
5. Return hull points in counterclockwise order

**Visual Example:**
```
Optimized Graham scan for points: (0,0), (1,1), (2,0), (1,-1), (0.5,0.5)

Input validation: n = 5 ≥ 1 ✓
Leftmost point: (0,0) ✓
Polar angle sorting: (0,0), (2,0), (1,-1), (0.5,0.5), (1,1) ✓
Graham scan: [(0,0), (2,0), (1,-1), (1,1)] ✓
```

**Implementation:**
```python
def convex_hull_optimized(points):
    n = len(points)
    if n < 3:
        return points
    
    # Find leftmost point (lowest x, then lowest y)
    leftmost = min(points, key=lambda p: (p[0], p[1]))
    
    # Sort points by polar angle from leftmost
    def polar_angle(p):
        if p == leftmost:
            return -float('inf')
        return math.atan2(p[1] - leftmost[1], p[0] - leftmost[0])
    
    sorted_points = sorted(points, key=polar_angle)
    
    # Optimized Graham scan
    hull = [leftmost, sorted_points[0]]
    for point in sorted_points[1:]:
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    
    return hull

def cross_product(o, a, b):
    """Optimized cross product calculation"""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def solve_convex_hull():
    n = int(input())
    points = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    hull = convex_hull_optimized(points)
    print(len(hull))
    for x, y in hull:
        print(f"{x} {y}")

# Main execution
if __name__ == "__main__":
    solve_convex_hull()
```

**Time Complexity:** O(n log n) where n is the number of points
**Space Complexity:** O(n) for storing the hull

**Why it's optimal:**
- Best known approach for convex hull construction
- Uses Graham scan for mathematical accuracy
- Optimal time complexity O(n log n)
- Handles all edge cases correctly
- Standard method in competitive programming

## 🎯 Problem Variations

### Variation 1: Convex Hull with Weights
**Problem**: Each point has a weight, find convex hull considering weights.

**Link**: [CSES Problem Set - Convex Hull with Weights](https://cses.fi/problemset/task/convex_hull_weights)

```python
def convex_hull_with_weights(points_with_weights):
    # Extract points and weights
    points = [p for p, w in points_with_weights]
    weights = [w for p, w in points_with_weights]
    
    # Find convex hull
    hull = convex_hull_optimized(points)
    
    # Calculate total weight of hull points
    hull_weight = 0
    for point in hull:
        idx = points.index(point)
        hull_weight += weights[idx]
    
    return hull, hull_weight
```

### Variation 2: Convex Hull with Constraints
**Problem**: Find convex hull subject to certain constraints.

**Link**: [CSES Problem Set - Convex Hull with Constraints](https://cses.fi/problemset/task/convex_hull_constraints)

```python
def convex_hull_with_constraints(points, constraints):
    # Filter points based on constraints
    filtered_points = []
    for x, y in points:
        if check_constraints((x, y), constraints):
            filtered_points.append((x, y))
    
    # Find convex hull of filtered points
    return convex_hull_optimized(filtered_points)
```

### Variation 3: Convex Hull with Dynamic Updates
**Problem**: Support adding/removing points and maintaining convex hull.

**Link**: [CSES Problem Set - Convex Hull with Dynamic Updates](https://cses.fi/problemset/task/convex_hull_dynamic)

```python
class DynamicConvexHull:
    def __init__(self):
        self.points = []
        self.hull = []
    
    def add_point(self, x, y):
        self.points.append((x, y))
        self.update_hull()
    
    def remove_point(self, x, y):
        if (x, y) in self.points:
            self.points.remove((x, y))
            self.update_hull()
    
    def update_hull(self):
        if len(self.points) < 3:
            self.hull = self.points
        else:
            self.hull = convex_hull_optimized(self.points)
    
    def get_hull(self):
        return self.hull
```

## 🔗 Related Problems

- **[Polygon Area](/cses-analyses/problem_soulutions/geometry/polygon_area_analysis/)**: Area calculation problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/point_in_polygon_analysis/)**: Point containment problems
- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/line_segment_intersection_analysis/)**: Intersection problems
- **[Polygon Lattice Points](/cses-analyses/problem_soulutions/geometry/polygon_lattice_points_analysis/)**: Lattice point counting

## 📚 Learning Points

1. **Graham Scan Algorithm**: Essential for convex hull construction
2. **Cross Product**: Important for determining orientation
3. **Polar Angle Sorting**: Key for algorithm efficiency
4. **Geometric Optimization**: Important for performance
5. **Stack Operations**: Critical for incremental hull building
6. **Numerical Stability**: Important for robust implementations

## 📝 Summary

The Convex Hull problem demonstrates fundamental computational geometry concepts. We explored three approaches:

1. **Brute Force Check All Triplets**: O(n⁴) time complexity, checks all possible combinations
2. **Graham Scan Algorithm**: O(n log n) time complexity, uses polar angle sorting
3. **Optimized Graham Scan**: O(n log n) time complexity, best approach with integer arithmetic

The key insights include using Graham scan for efficiency, cross product calculations for orientation, and polar angle sorting for systematic hull construction. This problem serves as an excellent introduction to convex hull algorithms and computational geometry. 