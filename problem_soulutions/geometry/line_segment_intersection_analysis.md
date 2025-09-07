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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Determine if two line segments intersect
- Handle different types of intersections
- Use efficient geometric algorithms
- Apply orientation-based approach

**Key Observations:**
- Need to handle general intersection and collinear cases
- Cross product determines relative orientation
- Bounding box check can optimize performance
- O(1) time complexity per test case

### Step 2: Orientation-Based Approach
**Idea**: Use cross products to determine the relative orientation of three points and check for intersection.

```python
def line_segment_intersection_orientation(p1, p2, p3, p4):
    # Check if segments p1p2 and p3p4 intersect
    
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

**Why this works:**
- Cross product determines relative orientation efficiently
- Handles all intersection cases systematically
- O(1) time complexity per test case
- Mathematically proven approach

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_line_segment_intersection():
    n = int(input())
    
    for _ in range(n):
        x1, y1, x2, y2, x3, y3, x4, y4 = map(int, input().split())
        
        p1 = (x1, y1)
        p2 = (x2, y2)
        p3 = (x3, y3)
        p4 = (x4, y4)
        
        if segments_intersect(p1, p2, p3, p4):
            print("YES")
        else:
            print("NO")

def segments_intersect(p1, p2, p3, p4):
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

# Main execution
if __name__ == "__main__":
    solve_line_segment_intersection()
```

**Why this works:**
- Optimal orientation-based approach
- Handles all edge cases correctly
- Efficient intersection detection
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (((0, 0), (2, 2)), ((1, 0), (1, 2)), True),   # Intersecting segments
        (((0, 0), (2, 0)), ((1, 0), (3, 0)), True),   # Overlapping collinear
        (((0, 0), (2, 2)), ((2, 0), (4, 2)), False),  # Non-intersecting
        (((0, 0), (1, 1)), ((1, 0), (2, 1)), False),  # Parallel segments
        (((0, 0), (2, 2)), ((0, 0), (1, 1)), True),   # Shared endpoint
    ]
    
    for (p1, p2), (p3, p4), expected in test_cases:
        result = solve_test(p1, p2, p3, p4)
        print(f"Segments: {p1}-{p2} and {p3}-{p4}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(p1, p2, p3, p4):
    return segments_intersect(p1, p2, p3, p4)

def segments_intersect(p1, p2, p3, p4):
    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)
    
    if o1 != o2 and o3 != o4:
        return True
    
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True
    
    return False

def orientation(a, b, c):
    cross = cross_product(a, b, c)
    if cross > 0: return 1
    elif cross < 0: return -1
    else: return 0

def cross_product(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(1) per test case - constant time intersection check
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Orientation-Based Approach**: Uses cross products for efficient orientation determination
- **Systematic Case Handling**: Covers all intersection scenarios
- **Mathematical Foundation**: Based on proven geometric principles
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
Test Cases:
3
0 0 2 2 1 0 1 2  (Case 1)
0 0 2 0 1 0 3 0  (Case 2)
0 0 2 2 2 0 4 2  (Case 3)
```

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

### Cross Product for Orientation
```
Cross Product Formula: (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

Example: Points A(0,0), B(2,2), C(1,0)
Cross product: (2-0) * (0-0) - (2-0) * (1-0) = 2 * 0 - 2 * 1 = -2

- Negative: Clockwise (right turn)
- Positive: Counterclockwise (left turn)
- Zero: Collinear

Visualization:
    y
    ↑
    │
2.0 │     •B (2,2)
    │    /
    │   /
    │  /
    │ /
    │/
0.0 │•────•C
    │A(0,0) (1,0)
    │
    └────────────→ x

Vector AB: (2,2)
Vector AC: (1,0)
Cross product AB × AC = -2 (negative = clockwise)
```

### Orientation-Based Intersection Algorithm
```
For segments AB and CD to intersect:

Step 1: Check orientations
- Orientation of A, B, C: O1 = cross_product(A, B, C)
- Orientation of A, B, D: O2 = cross_product(A, B, D)
- Orientation of C, D, A: O3 = cross_product(C, D, A)
- Orientation of C, D, B: O4 = cross_product(C, D, B)

Step 2: General case
If O1 ≠ O2 and O3 ≠ O4: segments intersect

Step 3: Collinear case
If O1 = O2 = O3 = O4 = 0: check if segments overlap

Case 1 Example:
A(0,0), B(2,2), C(1,0), D(1,2)
O1 = cross_product((0,0), (2,2), (1,0)) = -2
O2 = cross_product((0,0), (2,2), (1,2)) = 2
O3 = cross_product((1,0), (1,2), (0,0)) = 2
O4 = cross_product((1,0), (1,2), (2,2)) = -2

O1 ≠ O2 (-2 ≠ 2) and O3 ≠ O4 (2 ≠ -2) → YES
```

### Collinear Overlap Detection
```
For collinear segments, check if they overlap:

Case 2 Example:
A(0,0), B(2,0), C(1,0), D(3,0)

All orientations are 0 (collinear):
O1 = O2 = O3 = O4 = 0

Check overlap:
- Project onto x-axis: [0,2] and [1,3]
- Overlap exists if: max(0,1) ≤ min(2,3)
- max(0,1) = 1, min(2,3) = 2
- 1 ≤ 2 → YES (overlap from 1 to 2)
```

### Step-by-Step Intersection Detection
```
Case 1: (0,0)-(2,2) and (1,0)-(1,2)

Step 1: Calculate orientations
O1 = (2-0)*(0-0) - (2-0)*(1-0) = 0 - 2 = -2
O2 = (2-0)*(2-0) - (2-0)*(1-0) = 4 - 2 = 2
O3 = (1-1)*(0-1) - (2-0)*(0-1) = 0 - (-2) = 2
O4 = (1-1)*(2-1) - (2-0)*(2-1) = 0 - 2 = -2

Step 2: Check general case
O1 ≠ O2 (-2 ≠ 2) ✓
O3 ≠ O4 (2 ≠ -2) ✓
→ Segments intersect

Step 3: Find intersection point
Using parametric equations:
Line 1: x = t, y = t (0 ≤ t ≤ 2)
Line 2: x = 1, y = s (0 ≤ s ≤ 2)
Intersection: t = 1, s = 1 → (1,1)
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Orientation     │ O(1)         │ O(1)         │ Cross        │
│ Based           │              │              │ product      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Parametric      │ O(1)         │ O(1)         │ Line         │
│ Equations       │              │              │ equations    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sweep Line      │ O(n log n)   │ O(n)         │ For multiple │
│ Algorithm       │              │              │ segments     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(1)         │ Check all    │
│                 │              │              │ pairs        │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Line Segment Intersection Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: Two      │
              │ Line Segments   │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Calculate       │
              │ Orientations    │
              │ (Cross Products)│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Check General   │
              │ Case: O1 ≠ O2   │
              │ and O3 ≠ O4?    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Check Collinear │
              │ Case: All O = 0?│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Check Overlap   │
              │ for Collinear   │
              │ Segments        │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return YES/NO   │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Cross Product for Orientation**
- Determines if three points are clockwise, counterclockwise, or collinear
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Orientation-Based Intersection**
- Two segments intersect if they have different orientations
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Collinear Case Handling**
- Special handling for segments that lie on the same line
- Important for understanding
- Fundamental concept
- Essential for correctness

## 🎯 Problem Variations

### Variation 1: Line Segment Intersection with Weights
**Problem**: Each line segment has a weight, find total weight of intersecting pairs.

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

# Example usage
segments_with_weights = [
    (((0, 0), (2, 2)), 3),
    (((1, 0), (1, 2)), 2),
    (((0, 0), (2, 0)), 1)
]
result = line_segment_intersection_with_weights(segments_with_weights)
print(f"Weighted intersections: {result}")
```

### Variation 2: Line Segment Intersection with Constraints
**Problem**: Find intersections subject to certain constraints.

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

# Example usage
constraints = {"min_length": 1.0}
result = line_segment_intersection_with_constraints(segments, constraints)
print(f"Constrained intersections: {result}")
```

### Variation 3: Line Segment Intersection with Dynamic Updates
**Problem**: Support adding/removing segments and checking intersections.

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

# Example usage
dynamic_system = DynamicLineSegments()
dynamic_system.add_segment((0, 0), (2, 2))
dynamic_system.add_segment((1, 0), (1, 2))
intersections = dynamic_system.get_all_intersections()
print(f"Dynamic intersections: {intersections}")
```

### Variation 4: Line Segment Intersection with Range Queries
**Problem**: Answer queries about intersections in specific ranges.

```python
def line_segment_intersection_range_queries(segments, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Filter segments in range
        filtered_segments = []
        for p1, p2 in segments:
            if (min_x <= p1[0] <= max_x and min_y <= p1[1] <= max_y) or \
               (min_x <= p2[0] <= max_x and min_y <= p2[1] <= max_y):
                filtered_segments.append((p1, p2))
        
        # Check intersections in filtered segments
        intersecting_pairs = []
        for i in range(len(filtered_segments)):
            for j in range(i + 1, len(filtered_segments)):
                seg1 = filtered_segments[i]
                seg2 = filtered_segments[j]
                
                if segments_intersect(seg1[0], seg1[1], seg2[0], seg2[1]):
                    intersecting_pairs.append((seg1, seg2))
        
        results.append(len(intersecting_pairs))
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (1, 3, 1, 3), (0, 4, 0, 4)]
result = line_segment_intersection_range_queries(segments, queries)
print(f"Range query results: {result}")
```

### Variation 5: Line Segment Intersection with Convex Hull
**Problem**: Use convex hull to optimize intersection checking.

```python
def line_segment_intersection_convex_hull(points):
    if len(points) < 3:
        return []
    
    # Build convex hull
    hull = build_convex_hull(points)
    
    # Convert hull to segments
    segments = []
    for i in range(len(hull)):
        p1 = hull[i]
        p2 = hull[(i + 1) % len(hull)]
        segments.append((p1, p2))
    
    # Check intersections
    intersecting_pairs = []
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            seg1 = segments[i]
            seg2 = segments[j]
            
            if segments_intersect(seg1[0], seg1[1], seg2[0], seg2[1]):
                intersecting_pairs.append((seg1, seg2))
    
    return intersecting_pairs

def build_convex_hull(points):
    if len(points) < 3:
        return points
    
    # Find leftmost point
    leftmost = min(points, key=lambda p: p[0])
    
    # Sort by polar angle
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

# Example usage
points = [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.5)]
result = line_segment_intersection_convex_hull(points)
print(f"Convex hull intersections: {result}")
```

## 🔗 Related Problems

- **[Intersection Points](/cses-analyses/problem_soulutions/geometry/)**: Multiple segment intersection problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/)**: Point containment problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/)**: Geometric optimization

## 📚 Learning Points

1. **Cross Product**: Essential for determining orientation
2. **Orientation-Based Approach**: Key for intersection detection
3. **Collinear Case Handling**: Important for algorithm correctness
4. **Geometric Optimization**: Important for performance

---

**This is a great introduction to line segment intersection algorithms!** 🎯

### **Example Problems**:
- Polygon intersection
- Sweep line problems
- Path finding with obstacles
- Geometric algorithms

## Notable Techniques

### **Code Patterns**:
```python
# Orientation test for intersection
def segments_intersect(a, b, c, d):
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)
    
    # Different orientations
    if o1 != o2 and o3 != o4:
        return True
    
    # Collinear cases
    if o1 == 0 and on_segment(a, c, b): return True
    # ... handle other collinear cases
    return False
```

## Problem-Solving Framework

### **1. Understand the Geometry**
- Visualize the intersection scenarios
- Understand orientation concepts
- Consider edge cases

### **2. Choose the Right Tool**
- Cross product for orientation
- Bounding box checks for efficiency
- Systematic case handling

### **3. Handle Edge Cases**
- Collinear segments
- Overlapping segments
- Degenerate cases

### **4. Optimize for Precision**
- Use integer arithmetic
- Avoid floating point comparisons
- Consider numerical stability 