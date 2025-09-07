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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the smallest convex polygon containing all points
- Use efficient geometric algorithms
- Apply incremental construction techniques
- Handle edge cases properly

**Key Observations:**
- Brute force O(n³) is too slow for large inputs
- Graham scan provides O(n log n) complexity
- Andrew's monotone chain is also O(n log n)
- Cross product determines point orientation

### Step 2: Graham Scan Algorithm Approach
**Idea**: Sort points by polar angle from the leftmost point and use a stack to build the convex hull incrementally.

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

**Why this works:**
- Graham scan builds hull incrementally
- Cross product determines orientation efficiently
- O(n log n) time complexity is optimal
- Handles all edge cases correctly

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_convex_hull():
    n = int(input())
    points = []
    
    for _ in range(n):
        x, y = map(float, input().split())
        points.append((x, y))
    
    hull = find_convex_hull(points)
    print(len(hull))
    for x, y in hull:
        print(f"{x:.0f} {y:.0f}")

def find_convex_hull(points):
    """Find convex hull using Graham scan algorithm"""
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

# Main execution
if __name__ == "__main__":
    solve_convex_hull()
```

**Why this works:**
- Optimal Graham scan algorithm approach
- Handles all edge cases correctly
- Efficient convex hull construction
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.5)], 4),  # 5 points, 4 hull vertices
        ([(0, 0), (1, 0), (1, 1), (0, 1)], 4),                # Square, 4 hull vertices
        ([(0, 0), (1, 1), (2, 2)], 3),                         # Line, 3 hull vertices
        ([(0, 0), (1, 1)], 2),                                 # 2 points, 2 hull vertices
    ]
    
    for points, expected_vertices in test_cases:
        result = solve_test(points)
        print(f"Points: {points}")
        print(f"Expected hull vertices: {expected_vertices}, Got: {len(result)}")
        print(f"Hull: {result}")
        print(f"{'✓ PASS' if len(result) == expected_vertices else '✗ FAIL'}")
        print()

def solve_test(points):
    return find_convex_hull(points)

def find_convex_hull(points):
    if len(points) < 3:
        return points
    
    leftmost = min(points, key=lambda p: (p[0], p[1]))
    
    def polar_angle(p):
        if p == leftmost:
            return -float('inf')
        return math.atan2(p[1] - leftmost[1], p[0] - leftmost[0])
    
    sorted_points = sorted(points, key=polar_angle)
    
    hull = [leftmost, sorted_points[0]]
    for point in sorted_points[1:]:
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    
    return hull

def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - dominated by sorting points by polar angle
- **Space**: O(n) - for storing the hull points

### Why This Solution Works
- **Graham Scan Algorithm**: Efficiently builds convex hull incrementally
- **Cross Product**: Determines point orientation efficiently
- **Polar Angle Sorting**: Enables systematic hull construction
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
Points:
5
0 0
1 1
2 0
1 -1
0.5 0.5
```

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

### Convex Hull Identification
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

### Graham Scan Algorithm Process
```
Step 1: Find leftmost point
Points: (0,0), (1,1), (2,0), (1,-1), (0.5,0.5)
Leftmost: (0,0) with x=0

Step 2: Sort by polar angle from (0,0)
Point (0,0): angle = 0° (reference)
Point (2,0): angle = 0° (same x-axis)
Point (1,-1): angle = -45°
Point (0.5,0.5): angle = 45°
Point (1,1): angle = 45°

Sorted order: (0,0), (2,0), (1,-1), (0.5,0.5), (1,1)

Step 3: Graham Scan with stack
Stack: []

Process (0,0): Stack = [(0,0)]
Process (2,0): Stack = [(0,0), (2,0)]
Process (1,-1): 
- Cross product: (2,0) to (1,-1) vs (0,0) to (2,0)
- Turn right, remove (2,0)
- Stack = [(0,0), (1,-1)]
Process (0.5,0.5):
- Cross product: (1,-1) to (0.5,0.5) vs (0,0) to (1,-1)
- Turn left, keep (1,-1)
- Stack = [(0,0), (1,-1), (0.5,0.5)]
Process (1,1):
- Cross product: (0.5,0.5) to (1,1) vs (1,-1) to (0.5,0.5)
- Turn left, keep (0.5,0.5)
- Stack = [(0,0), (1,-1), (0.5,0.5), (1,1)]

Final hull: [(0,0), (1,-1), (0.5,0.5), (1,1)]
```

### Cross Product for Orientation
```
Cross Product Formula: (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

Example: Points A(0,0), B(2,0), C(1,-1)
Cross product: (2-0) * (-1-0) - (0-0) * (1-0) = 2 * (-1) - 0 = -2

- Negative: Turn right (clockwise)
- Positive: Turn left (counterclockwise)
- Zero: Collinear

Visualization:
    y
    ↑
    │
0.0 │A•─────────•B
    │(0,0)     (2,0)
    │
-1.0│     •C (1,-1)
    │
    └────────────→ x

Vector AB: (2,0)
Vector AC: (1,-1)
Cross product AB × AC = -2 (negative = right turn)
```

### Jarvis March (Gift Wrapping) Algorithm
```
Step 1: Start with leftmost point
Start: (0,0)

Step 2: Find next point with smallest polar angle
From (0,0):
- (2,0): angle = 0°
- (1,-1): angle = -45°
- (0.5,0.5): angle = 45°
- (1,1): angle = 45°

Next: (2,0)

Step 3: Continue from (2,0)
From (2,0):
- (1,-1): angle = -90°
- (0.5,0.5): angle = -45°
- (1,1): angle = -45°
- (0,0): angle = 180°

Next: (1,-1)

Step 4: Continue from (1,-1)
From (1,-1):
- (1,1): angle = 90°
- (0.5,0.5): angle = 45°
- (0,0): angle = 45°
- (2,0): angle = 0°

Next: (1,1)

Step 5: Continue from (1,1)
From (1,1):
- (0,0): angle = -135°
- (0.5,0.5): angle = -90°
- (2,0): angle = -45°
- (1,-1): angle = 0°

Next: (0,0) (back to start)

Hull: (0,0) → (2,0) → (1,-1) → (1,1) → (0,0)
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Algorithm   │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Graham Scan     │ O(n log n)   │ O(n)         │ Sort by      │
│                 │              │              │ polar angle  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Jarvis March    │ O(nh)        │ O(n)         │ Gift         │
│                 │              │              │ wrapping     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Quick Hull      │ O(n log n)   │ O(n)         │ Divide and   │
│                 │              │              │ conquer      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Chan's          │ O(n log h)   │ O(n)         │ Optimal      │
│ Algorithm       │              │              │ for small h  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Convex Hull Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: n points │
              │ in 2D plane     │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Choose Algorithm│
              │ (Graham/Jarvis) │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Find Leftmost   │
              │ Point           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Sort Points by  │
              │ Polar Angle     │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Build Hull      │
              │ Using Stack     │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return Hull     │
              │ Points          │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Graham Scan Algorithm**
- Build hull incrementally using a stack
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Cross Product for Orientation**
- Determines if three points turn left, right, or are collinear
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Polar Angle Sorting**
- Sort points by angle from leftmost point
- Important for understanding
- Fundamental concept
- Essential for efficiency

## 🎯 Problem Variations

### Variation 1: Convex Hull with Weights
**Problem**: Each point has a weight, find convex hull considering weights.

```python
def convex_hull_with_weights(points_with_weights):
    # Extract points and weights
    points = [p for p, w in points_with_weights]
    weights = [w for p, w in points_with_weights]
    
    # Find convex hull
    hull = find_convex_hull(points)
    
    # Calculate total weight of hull points
    hull_weight = 0
    for point in hull:
        idx = points.index(point)
        hull_weight += weights[idx]
    
    return hull, hull_weight

# Example usage
points_with_weights = [((0, 0), 1), ((1, 1), 2), ((2, 0), 1), ((1, -1), 3)]
hull, weight = convex_hull_with_weights(points_with_weights)
print(f"Convex hull: {hull}, Total weight: {weight}")
```

### Variation 2: Convex Hull with Constraints
**Problem**: Find convex hull subject to certain constraints.

```python
def convex_hull_with_constraints(points, constraints):
    # Filter points based on constraints
    filtered_points = []
    for x, y in points:
        if check_constraints((x, y), constraints):
            filtered_points.append((x, y))
    
    # Find convex hull of filtered points
    return find_convex_hull(filtered_points)

def check_constraints(point, constraints):
    x, y = point
    if x >= constraints["min_x"] and x <= constraints["max_x"] and \
       y >= constraints["min_y"] and y <= constraints["max_y"]:
        return True
    return False

# Example usage
constraints = {"min_x": 0, "max_x": 5, "min_y": 0, "max_y": 5}
result = convex_hull_with_constraints(points, constraints)
print(f"Constrained convex hull: {result}")
```

### Variation 3: Convex Hull with Dynamic Updates
**Problem**: Support adding/removing points and maintaining convex hull.

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
            self.hull = find_convex_hull(self.points)
    
    def get_hull(self):
        return self.hull
    
    def get_hull_area(self):
        if len(self.hull) < 3:
            return 0
        return calculate_polygon_area(self.hull)

def calculate_polygon_area(vertices):
    """Calculate area using shoelace formula"""
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
    return abs(area) / 2

# Example usage
dynamic_hull = DynamicConvexHull()
dynamic_hull.add_point(0, 0)
dynamic_hull.add_point(1, 1)
dynamic_hull.add_point(2, 0)
hull = dynamic_hull.get_hull()
area = dynamic_hull.get_hull_area()
print(f"Dynamic convex hull: {hull}, Area: {area}")
```

### Variation 4: Convex Hull with Range Queries
**Problem**: Answer queries about convex hull in specific ranges.

```python
def convex_hull_range_queries(points, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Filter points in range
        filtered_points = []
        for x, y in points:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                filtered_points.append((x, y))
        
        # Find convex hull of filtered points
        if len(filtered_points) < 3:
            results.append([])
        else:
            hull = find_convex_hull(filtered_points)
            results.append(hull)
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (1, 3, 1, 3), (0, 4, 0, 4)]
result = convex_hull_range_queries(points, queries)
print(f"Range query results: {result}")
```

### Variation 5: Convex Hull with Multiple Hulls
**Problem**: Find multiple convex hulls for different point sets.

```python
def multiple_convex_hulls(point_sets):
    hulls = []
    
    for point_set in point_sets:
        if len(point_set) < 3:
            hulls.append(point_set)
        else:
            hull = find_convex_hull(point_set)
            hulls.append(hull)
    
    return hulls

def find_common_hull_vertices(hulls):
    """Find vertices that appear in multiple hulls"""
    vertex_count = {}
    
    for hull in hulls:
        for vertex in hull:
            vertex_count[vertex] = vertex_count.get(vertex, 0) + 1
    
    # Return vertices that appear in multiple hulls
    common_vertices = [v for v, count in vertex_count.items() if count > 1]
    return common_vertices

# Example usage
point_sets = [
    [(0, 0), (1, 1), (2, 0)],
    [(1, 0), (2, 1), (3, 0)],
    [(0, 0), (2, 0), (1, 1)]
]
hulls = multiple_convex_hulls(point_sets)
common = find_common_hull_vertices(hulls)
print(f"Multiple hulls: {hulls}")
print(f"Common vertices: {common}")
```

## 🔗 Related Problems

- **[Polygon Area](/cses-analyses/problem_soulutions/geometry/)**: Area calculation problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/)**: Point containment problems
- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/)**: Intersection problems

## 📚 Learning Points

1. **Graham Scan Algorithm**: Essential for convex hull construction
2. **Cross Product**: Important for determining orientation
3. **Polar Angle Sorting**: Key for algorithm efficiency
4. **Geometric Optimization**: Important for performance

---

**This is a great introduction to convex hull algorithms!** 🎯 