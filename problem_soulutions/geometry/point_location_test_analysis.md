---
layout: simple
title: "Point Location Test - Geometry Analysis"
permalink: /problem_soulutions/geometry/point_location_test_analysis
---


# Point Location Test - Geometry Analysis

## Problem Description

**Problem**: Given a point and a line segment, determine whether the point is on the line segment, to the left, or to the right.

**Input**: 
- n: number of test cases
- n lines: x1 y1 x2 y2 px py (line segment endpoints and query point)

**Output**: For each test case, print "LEFT", "RIGHT", "ON_SEGMENT", or "ON_LINE".

**Example**:
```
Input:
3
0 0 2 2 1 1
0 0 2 2 3 3
0 0 2 2 0 2

Output:
ON_SEGMENT
ON_LINE
LEFT

Explanation: 
- Point (1,1) lies on the line segment from (0,0) to (2,2)
- Point (3,3) lies on the line but outside the segment
- Point (0,2) lies to the left of the line segment
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Determine relative position of a point to a line segment
- Use geometric orientation tests
- Handle all possible cases correctly
- Apply cross product calculations

**Key Observations:**
- Cross product gives orientation information
- Need to handle collinear points separately
- Check if point lies within segment bounds
- Use integer arithmetic for precision

### Step 2: Cross Product Approach
**Idea**: Use cross product to determine orientation and check segment bounds.

```python
def point_location_test_cross_product(segment_start, segment_end, point):
    # Calculate cross product of vectors AB and AC
    # AB = segment_end - segment_start
    # AC = point - segment_start
    cross = cross_product(segment_start, segment_end, point)
    
    if cross > 0:
        return "LEFT"      # Point is to the left
    elif cross < 0:
        return "RIGHT"     # Point is to the right
    else:
        # Point is collinear, check if it's on segment
        if on_segment(segment_start, segment_end, point):
            return "ON_SEGMENT"
        else:
            return "ON_LINE"

def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(a, b, c):
    """Check if point c lies on segment ab"""
    return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))
```

**Why this works:**
- Cross product gives orientation directly
- Handles all cases correctly
- Integer arithmetic avoids precision issues
- O(1) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_point_location_test():
    n = int(input())
    
    for _ in range(n):
        x1, y1, x2, y2, px, py = map(int, input().split())
        segment_start = (x1, y1)
        segment_end = (x2, y2)
        point = (px, py)
        
        result = point_location_test(segment_start, segment_end, point)
        print(result)

def point_location_test(segment_start, segment_end, point):
    """
    Determine location of point relative to line segment.
    Returns: 'LEFT', 'RIGHT', 'ON_SEGMENT', 'ON_LINE'
    """
    cross = cross_product(segment_start, segment_end, point)
    
    if cross > 0:
        return "LEFT"
    elif cross < 0:
        return "RIGHT"
    else:
        # Point is collinear, check if it's on segment
        if on_segment(segment_start, segment_end, point):
            return "ON_SEGMENT"
        else:
            return "ON_LINE"

def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(a, b, c):
    """Check if point c lies on segment ab"""
    return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))

# Main execution
if __name__ == "__main__":
    solve_point_location_test()
```

**Why this works:**
- Optimal cross product approach
- Handles all edge cases correctly
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (((0, 0), (2, 2), (1, 1)), "ON_SEGMENT"),
        (((0, 0), (2, 2), (3, 3)), "ON_LINE"),
        (((0, 0), (2, 2), (0, 2)), "LEFT"),
        (((0, 0), (2, 2), (2, 0)), "RIGHT"),
    ]
    
    for (segment_start, segment_end, point), expected in test_cases:
        result = solve_test(segment_start, segment_end, point)
        print(f"Segment: {segment_start} to {segment_end}, Point: {point}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(segment_start, segment_end, point):
    return point_location_test(segment_start, segment_end, point)

def point_location_test(segment_start, segment_end, point):
    cross = cross_product(segment_start, segment_end, point)
    
    if cross > 0:
        return "LEFT"
    elif cross < 0:
        return "RIGHT"
    else:
        if on_segment(segment_start, segment_end, point):
            return "ON_SEGMENT"
        else:
            return "ON_LINE"

def cross_product(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(a, b, c):
    return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(1) per test case - constant time operations
- **Space**: O(1) - constant space usage

### Why This Solution Works
- **Cross Product**: Gives orientation information directly
- **Integer Arithmetic**: Avoids floating-point precision issues
- **Segment Bounds**: Checks if collinear point lies within segment
- **Efficient Algorithm**: Constant time per test case

## 🎯 Key Insights

### 1. **Cross Product for Orientation**
- Use cross product to determine relative position
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Integer Arithmetic**
- Avoid floating-point precision issues
- Important for understanding
- Simple but important concept
- Essential for accuracy

### 3. **Segment Bounds Checking**
- Check if collinear point lies within segment
- Important for understanding
- Fundamental concept
- Essential for algorithm

## 🎯 Problem Variations

### Variation 1: Point Location with Multiple Segments
**Problem**: Determine location relative to multiple line segments.

```python
def point_location_multiple_segments(point, segments):
    results = []
    
    for segment_start, segment_end in segments:
        result = point_location_test(segment_start, segment_end, point)
        results.append(result)
    
    return results

# Example usage
segments = [
    ((0, 0), (2, 2)),
    ((1, 0), (1, 2)),
    ((0, 1), (2, 1))
]
result = point_location_multiple_segments((1, 1), segments)
print(f"Multiple segment results: {result}")
```

### Variation 2: Point Location with Tolerance
**Problem**: Allow small tolerance for "on segment" classification.

```python
def point_location_with_tolerance(segment_start, segment_end, point, tolerance=1e-9):
    cross = cross_product(segment_start, segment_end, point)
    
    if abs(cross) <= tolerance:
        # Point is approximately collinear
        if on_segment_with_tolerance(segment_start, segment_end, point, tolerance):
            return "ON_SEGMENT"
        else:
            return "ON_LINE"
    elif cross > 0:
        return "LEFT"
    else:
        return "RIGHT"

def on_segment_with_tolerance(a, b, c, tolerance):
    # Check if point c is within tolerance of segment ab
    if abs(cross_product(a, b, c)) > tolerance:
        return False
    
    # Check bounds with tolerance
    return (min(a[0], b[0]) - tolerance <= c[0] <= max(a[0], b[0]) + tolerance and
            min(a[1], b[1]) - tolerance <= c[1] <= max(a[1], b[1]) + tolerance)

# Example usage
tolerance = 0.1
result = point_location_with_tolerance((0, 0), (2, 2), (1.05, 0.95), tolerance)
print(f"Tolerance-based result: {result}")
```

### Variation 3: Point Location with Dynamic Segments
**Problem**: Support adding/removing segments and answering queries.

```python
class DynamicPointLocation:
    def __init__(self):
        self.segments = []
    
    def add_segment(self, start, end):
        self.segments.append((start, end))
    
    def remove_segment(self, start, end):
        if (start, end) in self.segments:
            self.segments.remove((start, end))
    
    def query_point(self, point):
        results = []
        for segment_start, segment_end in self.segments:
            result = point_location_test(segment_start, segment_end, point)
            results.append(result)
        return results

# Example usage
dynamic_system = DynamicPointLocation()
dynamic_system.add_segment((0, 0), (2, 2))
dynamic_system.add_segment((1, 0), (1, 2))
result = dynamic_system.query_point((1, 1))
print(f"Dynamic query result: {result}")
```

### Variation 4: Point Location with Range Queries
**Problem**: Answer queries about points in specific ranges.

```python
def point_location_range_queries(segments, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Sample points in range and test against segments
        range_results = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                point = (x, y)
                for segment_start, segment_end in segments:
                    result = point_location_test(segment_start, segment_end, point)
                    range_results.append(result)
        
        results.append(range_results)
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (1, 3, 1, 3)]
result = point_location_range_queries(segments, queries)
print(f"Range query results: {result}")
```

### Variation 5: Point Location with Convex Hull
**Problem**: Use convex hull to optimize point location queries.

```python
def point_location_with_convex_hull(point, segments):
    # Build convex hull from segment endpoints
    all_points = set()
    for start, end in segments:
        all_points.add(start)
        all_points.add(end)
    
    # Use Graham scan or Jarvis march to build convex hull
    hull = build_convex_hull(list(all_points))
    
    # First check if point is outside convex hull
    if not point_in_convex_hull(point, hull):
        return ["OUTSIDE_HULL"] * len(segments)
    
    # Then perform detailed segment tests
    results = []
    for segment_start, segment_end in segments:
        result = point_location_test(segment_start, segment_end, point)
        results.append(result)
    
    return results

def build_convex_hull(points):
    # Simplified convex hull construction
    # In practice, use Graham scan or Jarvis march
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
result = point_location_with_convex_hull((1, 1), segments)
print(f"Convex hull optimized result: {result}")
```

## 🔗 Related Problems

- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/)**: Similar geometric problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/)**: Point containment problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/)**: Geometric optimization

## 📚 Learning Points

1. **Cross Product**: Essential for geometric orientation tests
2. **Integer Arithmetic**: Important for precision in geometry
3. **Segment Bounds**: Key for accurate point location
4. **Geometric Properties**: Important for spatial algorithms

---

**This is a great introduction to point location algorithms!** 🎯
def orientation(a, b, c):
    cross = cross_product(a, b, c)
    if cross > 0: return "COUNTERCLOCKWISE"
    elif cross < 0: return "CLOCKWISE"
    else: return "COLLINEAR"
```

## Problem-Solving Framework

### **1. Understand the Geometry**
- Visualize the problem
- Understand what cross product represents
- Consider edge cases (collinear points)

### **2. Choose the Right Tool**
- Cross product for orientation
- Integer arithmetic for precision
- Bounds checking for segment inclusion

### **3. Handle Edge Cases**
- Points exactly on the line
- Points outside segment bounds
- Degenerate cases (zero-length segments)

### **4. Optimize for Precision**
- Use integer coordinates when possible
- Avoid floating point comparisons
- Consider numerical stability 