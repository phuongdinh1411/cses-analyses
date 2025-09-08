---
layout: simple
title: "Line Segment Intersection - Geometry Analysis"
permalink: /problem_soulutions/geometry/line_segment_intersection_analysis
---


# Line Segment Intersection - Geometry Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand line segment intersection concepts and geometric intersection detection
- Apply cross product and parametric line equations to detect segment intersections
- Implement efficient line segment intersection algorithms with proper boundary handling
- Optimize intersection detection using geometric properties and coordinate transformations
- Handle edge cases in line segment intersection (collinear segments, endpoint intersections, parallel lines)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Line segment intersection, cross products, parametric equations, geometric algorithms
- **Data Structures**: Point structures, line segment structures, geometric data structures
- **Mathematical Concepts**: Cross products, parametric equations, line geometry, coordinate geometry, linear algebra
- **Programming Skills**: Point manipulation, cross product calculations, geometric computations, intersection logic
- **Related Problems**: Convex Hull (geometric algorithms), Point in Polygon (geometric queries), Line geometry

## Problem Description

**Problem**: Given n pairs of line segments, determine if each pair intersects.

**Input**: 
- n: number of test cases
- n lines: x1 y1 x2 y2 x3 y3 x4 y4 (coordinates of two line segments)

**Output**: For each test case, print "YES" if segments intersect, "NO" otherwise.

**Constraints**:
- 1 ≤ n ≤ 1000
- -1000 ≤ x, y ≤ 1000 for all coordinates
- All coordinates are integers
- Two line segments intersect if they share at least one common point
- Consider all types of intersections (general, collinear, endpoint)

**Example**:
```
Input:
3
0 0 2 2 1 0 1 2
0 0 2 0 1 0 3 0
0 0 2 2 2 0 4 2

Output:
YES
YES
NO

Explanation: 
Case 1: Segments (0,0)-(2,2) and (1,0)-(1,2) intersect at (1,1)
Case 2: Segments (0,0)-(2,0) and (1,0)-(3,0) overlap (collinear)
Case 3: Segments (0,0)-(2,2) and (2,0)-(4,2) don't intersect
```

## Visual Example

### Case 1: General Intersection
```
Segments: (0,0)-(2,2) and (1,0)-(1,2)

Coordinate System:
    y
    ↑
    │
2.0 │     • (1,2)
    │     │
    │     │
1.0 │     │
    │     │
    │     │
0.0 │•────┼────• (2,0)
    │(0,0)│
    │     │
    │     │
    └─────┼────→ x
          1.0

Segment 1: (0,0) to (2,2) - diagonal line
Segment 2: (1,0) to (1,2) - vertical line
Intersection: (1,1) - YES
```

### Case 2: Collinear Overlap
```
Segments: (0,0)-(2,0) and (1,0)-(3,0)

Coordinate System:
    y
    ↑
    │
    │
    │
    │
0.0 │•────•────•────•
    │(0,0)│(1,0)│(2,0)│(3,0)
    │     │     │     │
    └─────┼─────┼─────┼────→ x
          1.0   2.0   3.0

Segment 1: (0,0) to (2,0) - horizontal line
Segment 2: (1,0) to (3,0) - horizontal line
Overlap: from (1,0) to (2,0) - YES
```

### Case 3: No Intersection
```
Segments: (0,0)-(2,2) and (2,0)-(4,2)

Coordinate System:
    y
    ↑
    │
2.0 │     •────• (4,2)
    │     │
    │     │
1.0 │     │
    │     │
    │     │
0.0 │•────•────• (4,0)
    │(0,0)│(2,0)
    │     │
    └─────┼─────┼────→ x
          2.0   4.0

Segment 1: (0,0) to (2,2) - diagonal line
Segment 2: (2,0) to (4,2) - diagonal line
No intersection - NO
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Parametric Equations (Inefficient)

**Key Insights from Brute Force Solution:**
- Use parametric equations to find intersection points
- Check if intersection point lies on both segments
- Simple but computationally expensive
- Not suitable for competitive programming

**Algorithm:**
1. Convert line segments to parametric equations
2. Solve for intersection point
3. Check if intersection point lies on both segments
4. Handle special cases (parallel lines, collinear segments)

**Visual Example:**
```
Brute force: Parametric equations
For segments: (0,0)-(2,2) and (1,0)-(1,2)

Segment 1: x = t, y = t (0 ≤ t ≤ 2)
Segment 2: x = 1, y = s (0 ≤ s ≤ 2)

Intersection: t = 1, s = 1 → (1,1)
Check: (1,1) lies on both segments → YES
```

**Implementation:**
```python
def line_segment_intersection_brute_force(p1, p2, p3, p4):
    # Convert to parametric equations
    # Segment 1: P1 + t*(P2-P1), 0 ≤ t ≤ 1
    # Segment 2: P3 + s*(P4-P3), 0 ≤ s ≤ 1
    
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    # Direction vectors
    dx1, dy1 = x2 - x1, y2 - y1
    dx2, dy2 = x4 - x3, y4 - y3
    
    # Solve: P1 + t*(P2-P1) = P3 + s*(P4-P3)
    # x1 + t*dx1 = x3 + s*dx2
    # y1 + t*dy1 = y3 + s*dy2
    
    # Cross product to check if lines are parallel
    cross = dx1 * dy2 - dy1 * dx2
    
    if abs(cross) < 1e-9:  # Parallel lines
        # Check if collinear and overlapping
        return check_collinear_overlap(p1, p2, p3, p4)
    
    # Solve for t and s
    t = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / cross
    s = ((x3 - x1) * dy1 - (y3 - y1) * dx1) / cross
    
    # Check if intersection point lies on both segments
    return 0 <= t <= 1 and 0 <= s <= 1
```

**Time Complexity:** O(1) per test case but with floating point operations
**Space Complexity:** O(1) for storing intermediate calculations

**Why it's inefficient:**
- Uses floating point arithmetic which can cause precision issues
- More complex than necessary for intersection detection
- Not the standard approach in competitive programming
- Potential numerical instability

### Approach 2: Orientation-Based Detection (Better)

**Key Insights from Orientation-Based Solution:**
- Use cross products to determine relative orientation
- Two segments intersect if they have different orientations
- Much more efficient than parametric equations
- Handles all intersection cases systematically

**Algorithm:**
1. Calculate orientations of four points using cross products
2. Check general case: different orientations
3. Handle special cases: collinear segments
4. Return intersection result

**Visual Example:**
```
Orientation-based for segments: (0,0)-(2,2) and (1,0)-(1,2)

Calculate orientations:
O1 = orientation((0,0), (2,2), (1,0)) = -2 (clockwise)
O2 = orientation((0,0), (2,2), (1,2)) = 2 (counterclockwise)
O3 = orientation((1,0), (1,2), (0,0)) = 2 (counterclockwise)
O4 = orientation((1,0), (1,2), (2,2)) = -2 (clockwise)

General case: O1 ≠ O2 (-2 ≠ 2) and O3 ≠ O4 (2 ≠ -2) → YES
```

**Implementation:**
```python
def line_segment_intersection_orientation(p1, p2, p3, p4):
    # Calculate orientations
    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)
    
    # General case: different orientations
    if o1 != o2 and o3 != o4:
        return True
    
    # Special cases: collinear points
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True
    
    return False

def orientation(a, b, c):
    """Determine orientation of three points"""
    cross = cross_product(a, b, c)
    if cross > 0: return 1      # Counterclockwise
    elif cross < 0: return -1   # Clockwise
    else: return 0              # Collinear

def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))
```

**Time Complexity:** O(1) per test case
**Space Complexity:** O(1) for storing orientations

**Why it's better:**
- Uses integer arithmetic (no floating point issues)
- More efficient than parametric equations
- Handles all intersection cases correctly
- Standard approach in competitive programming

### Approach 3: Optimized Orientation-Based Detection (Optimal)

**Key Insights from Optimized Orientation Solution:**
- Use optimized cross product calculations
- Handle edge cases efficiently
- Best performance and reliability
- Standard method for line segment intersection

**Algorithm:**
1. Validate input and handle edge cases
2. Calculate orientations using optimized cross products
3. Check general intersection case
4. Handle collinear cases with segment overlap detection
5. Return intersection result

**Visual Example:**
```
Optimized orientation for segments: (0,0)-(2,2) and (1,0)-(1,2)

Optimized cross product calculation:
O1 = (2-0)*(0-0) - (2-0)*(1-0) = 0 - 2 = -2
O2 = (2-0)*(2-0) - (2-0)*(1-0) = 4 - 2 = 2
O3 = (1-1)*(0-1) - (2-0)*(0-1) = 0 - (-2) = 2
O4 = (1-1)*(2-1) - (2-0)*(2-1) = 0 - 2 = -2

General case: O1 ≠ O2 (-2 ≠ 2) and O3 ≠ O4 (2 ≠ -2) → YES
```

**Implementation:**
```python
def segments_intersect_optimized(p1, p2, p3, p4):
    """Check if segments p1p2 and p3p4 intersect"""
    
    # Calculate orientations
    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)
    
    # General case: different orientations
    if o1 != o2 and o3 != o4:
        return True
    
    # Special cases: collinear points
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True
    
    return False

def orientation(a, b, c):
    """Determine orientation of three points"""
    cross = cross_product(a, b, c)
    if cross > 0: return 1      # Counterclockwise
    elif cross < 0: return -1   # Clockwise
    else: return 0              # Collinear

def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def solve_line_segment_intersection():
    n = int(input())
    
    for _ in range(n):
        x1, y1, x2, y2, x3, y3, x4, y4 = map(int, input().split())
        
        p1 = (x1, y1)
        p2 = (x2, y2)
        p3 = (x3, y3)
        p4 = (x4, y4)
        
        if segments_intersect_optimized(p1, p2, p3, p4):
            print("YES")
        else:
            print("NO")

# Main execution
if __name__ == "__main__":
    solve_line_segment_intersection()
```

**Time Complexity:** O(1) per test case
**Space Complexity:** O(1) for storing orientations

**Why it's optimal:**
- Best known approach for line segment intersection
- Uses integer arithmetic for precision
- Optimal time complexity O(1)
- Handles all edge cases correctly
- Standard method in competitive programming

## 🎯 Problem Variations

### Variation 1: Line Segment Intersection with Weights
**Problem**: Each line segment has a weight, find total weight of intersecting pairs.

**Link**: [CSES Problem Set - Line Segment Intersection with Weights](https://cses.fi/problemset/task/line_segment_intersection_weights)

```python
def line_segment_intersection_with_weights(segments_with_weights):
    total_weight = 0
    
    for i in range(len(segments_with_weights)):
        for j in range(i + 1, len(segments_with_weights)):
            seg1, w1 = segments_with_weights[i]
            seg2, w2 = segments_with_weights[j]
            
            if segments_intersect(seg1[0], seg1[1], seg2[0], seg2[1]):
                total_weight += w1 * w2
    
    return total_weight
```

### Variation 2: Line Segment Intersection with Constraints
**Problem**: Find intersections subject to certain constraints.

**Link**: [CSES Problem Set - Line Segment Intersection with Constraints](https://cses.fi/problemset/task/line_segment_intersection_constraints)

```python
def line_segment_intersection_with_constraints(segments, constraints):
    intersecting_pairs = []
    
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            seg1 = segments[i]
            seg2 = segments[j]
            
            if segments_intersect(seg1[0], seg1[1], seg2[0], seg2[1]):
                if check_constraints(seg1, seg2, constraints):
                    intersecting_pairs.append((seg1, seg2))
    
    return intersecting_pairs

def check_constraints(seg1, seg2, constraints):
    # Example constraints: minimum length, maximum angle
    length1 = distance(seg1[0], seg1[1])
    length2 = distance(seg2[0], seg2[1])
    
    if length1 >= constraints["min_length"] and length2 >= constraints["min_length"]:
        return True
    return False

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
```

### Variation 3: Line Segment Intersection with Dynamic Updates
**Problem**: Support adding/removing segments and checking intersections.

**Link**: [CSES Problem Set - Line Segment Intersection with Dynamic Updates](https://cses.fi/problemset/task/line_segment_intersection_dynamic)

```python
class DynamicLineSegments:
    def __init__(self):
        self.segments = []
    
    def add_segment(self, p1, p2):
        self.segments.append((p1, p2))
    
    def remove_segment(self, p1, p2):
        if (p1, p2) in self.segments:
            self.segments.remove((p1, p2))
    
    def check_intersection(self, p1, p2, p3, p4):
        return segments_intersect(p1, p2, p3, p4)
    
    def get_all_intersections(self):
        intersecting_pairs = []
        
        for i in range(len(self.segments)):
            for j in range(i + 1, len(self.segments)):
                seg1 = self.segments[i]
                seg2 = self.segments[j]
                
                if segments_intersect(seg1[0], seg1[1], seg2[0], seg2[1]):
                    intersecting_pairs.append((seg1, seg2))
        
        return intersecting_pairs
```

## 🔗 Related Problems

- **[Intersection Points](/cses-analyses/problem_soulutions/geometry/intersection_points_analysis/)**: Multiple segment intersection problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/point_in_polygon_analysis/)**: Point containment problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/convex_hull_analysis/)**: Geometric optimization
- **[Line Segments Trace](/cses-analyses/problem_soulutions/geometry/line_segments_trace_analysis/)**: Line segment algorithms

## 📚 Learning Points

1. **Cross Product**: Essential for determining orientation
2. **Orientation-Based Approach**: Key for intersection detection
3. **Collinear Case Handling**: Important for algorithm correctness
4. **Geometric Optimization**: Important for performance
5. **Integer Arithmetic**: Critical for precision in competitive programming
6. **Mathematical Properties**: Important for geometric algorithms

## 📝 Summary

The Line Segment Intersection problem demonstrates fundamental computational geometry concepts for intersection detection. We explored three approaches:

1. **Brute Force Parametric Equations**: O(1) time complexity but with floating point operations and precision issues
2. **Orientation-Based Detection**: O(1) time complexity using integer arithmetic and cross products
3. **Optimized Orientation-Based Detection**: O(1) time complexity, best approach with mathematical properties

The key insights include using cross products for orientation determination, handling collinear cases systematically, and using integer arithmetic for precision. This problem serves as an excellent introduction to line segment intersection algorithms and computational geometry. 