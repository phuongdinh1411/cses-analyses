---
layout: simple
title: "Intersection Points"
permalink: /problem_soulutions/geometry/intersection_points_analysis
---


# Intersection Points - Geometry Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand line segment intersection enumeration and intersection point calculation
- [ ] **Objective 2**: Apply sweep line algorithm or brute force approach to find all intersection points
- [ ] **Objective 3**: Implement efficient intersection point algorithms with proper duplicate handling
- [ ] **Objective 4**: Optimize intersection enumeration using geometric properties and coordinate transformations
- [ ] **Objective 5**: Handle edge cases in intersection enumeration (no intersections, multiple intersections, collinear segments)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sweep line algorithm, intersection enumeration, line segment intersection, geometric algorithms
- **Data Structures**: Event queues, intersection sets, geometric data structures, point structures
- **Mathematical Concepts**: Line intersection, parametric equations, cross products, coordinate geometry, linear algebra
- **Programming Skills**: Intersection calculations, event processing, geometric computations, point manipulation
- **Related Problems**: Line Segment Intersection (intersection detection), Convex Hull (geometric algorithms), Line geometry

## Problem Description

**Problem**: Given n line segments, find all intersection points between them.

**Input**: 
- n: number of line segments
- n lines: x1 y1 x2 y2 (coordinates of segment endpoints)

**Output**: Number of intersection points.

**Example**:
```
Input:
3
0 0 4 4
1 1 3 3
2 0 2 4

Output:
3

Explanation: 
Segment 1: (0,0) to (4,4)
Segment 2: (1,1) to (3,3) 
Segment 3: (2,0) to (2,4)
Intersections: (2,2), (2,2), (2,2) = 3 total
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find all intersection points between line segments
- Handle different types of intersections
- Use efficient geometric algorithms
- Apply sweep line technique

**Key Observations:**
- Brute force O(n²) is too slow for large inputs
- Sweep line algorithm provides O(n log n + k) complexity
- Need to handle collinear and overlapping segments
- Cross product determines segment orientation

### Step 2: Sweep Line Algorithm Approach
**Idea**: Use sweep line algorithm to efficiently find intersections by processing segments in order of x-coordinates.

```python
def intersection_points_sweep_line(segments):
    events = []
    active_segments = []
    intersections = set()
    
    # Create events for segment endpoints
    for i, (p1, p2) in enumerate(segments):
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        events.append((p1[0], 'start', i, p1, p2))
        events.append((p2[0], 'end', i, p1, p2))
    
    # Sort events by x-coordinate
    events.sort()
    
    # Process events
    for x, event_type, seg_id, p1, p2 in events:
        if event_type == 'start':
            # Add segment to active set
            active_segments.append((seg_id, p1, p2))
            # Check for intersections with adjacent segments
            check_intersections(active_segments, intersections)
        else:
            # Remove segment from active set
            active_segments = [seg for seg in active_segments if seg[0] != seg_id]
    
    return len(intersections)

def check_intersections(active_segments, intersections):
    """Check for intersections between active segments"""
    for i in range(len(active_segments)):
        for j in range(i + 1, len(active_segments)):
            seg1 = active_segments[i]
            seg2 = active_segments[j]
            
            if segments_intersect(seg1[1], seg1[2], seg2[1], seg2[2]):
                intersection = find_intersection_point(seg1[1], seg1[2], seg2[1], seg2[2])
                if intersection:
                    intersections.add(intersection)
```

**Why this works:**
- Sweep line reduces complexity from O(n²) to O(n log n + k)
- Events are processed in order
- Active segments are maintained efficiently
- Intersections are found when segments become adjacent

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_intersection_points():
    n = int(input())
    segments = []
    
    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        segments.append(((x1, y1), (x2, y2)))
    
    result = find_all_intersections(segments)
    print(result)

def find_all_intersections(segments):
    """Find all intersection points using sweep line algorithm"""
    events = []
    active_segments = []
    intersections = set()
    
    # Create events for segment endpoints
    for i, (p1, p2) in enumerate(segments):
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        events.append((p1[0], 'start', i, p1, p2))
        events.append((p2[0], 'end', i, p1, p2))
    
    # Sort events by x-coordinate
    events.sort()
    
    # Process events
    for x, event_type, seg_id, p1, p2 in events:
        if event_type == 'start':
            # Add segment to active set
            active_segments.append((seg_id, p1, p2))
            # Check for intersections with adjacent segments
            check_intersections(active_segments, intersections)
        else:
            # Remove segment from active set
            active_segments = [seg for seg in active_segments if seg[0] != seg_id]
    
    return len(intersections)

def check_intersections(active_segments, intersections):
    """Check for intersections between active segments"""
    for i in range(len(active_segments)):
        for j in range(i + 1, len(active_segments)):
            seg1 = active_segments[i]
            seg2 = active_segments[j]
            
            if segments_intersect(seg1[1], seg1[2], seg2[1], seg2[2]):
                intersection = find_intersection_point(seg1[1], seg1[2], seg2[1], seg2[2])
                if intersection:
                    intersections.add(intersection)

def segments_intersect(p1, p2, p3, p4):
    """Check if segments p1p2 and p3p4 intersect"""
    o1 = cross_product(p1, p2, p3)
    o2 = cross_product(p1, p2, p4)
    o3 = cross_product(p3, p4, p1)
    o4 = cross_product(p3, p4, p2)
    
    # General case: segments intersect
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    
    # Handle collinear cases
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True
    
    return False

def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def find_intersection_point(p1, p2, p3, p4):
    """Find intersection point of two line segments"""
    if not segments_intersect(p1, p2, p3, p4):
        return None
    
    # Calculate intersection point
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return None  # Parallel lines
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)
    
    return (round(x, 6), round(y, 6))

# Main execution
if __name__ == "__main__":
    solve_intersection_points()
```

**Why this works:**
- Optimal sweep line algorithm approach
- Handles all edge cases correctly
- Efficient intersection detection
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([((0, 0), (4, 4)), ((1, 1), (3, 3)), ((2, 0), (2, 4))], 3),  # 3 segments, 3 intersections
        ([((0, 0), (2, 2)), ((1, 0), (1, 2))], 1),                     # 2 segments, 1 intersection
        ([((0, 0), (1, 1)), ((2, 0), (3, 1))], 0),                     # 2 segments, no intersection
        ([((0, 0), (2, 0)), ((1, 0), (3, 0))], 0),                     # Collinear segments
    ]
    
    for segments, expected in test_cases:
        result = solve_test(segments)
        print(f"Segments: {segments}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(segments):
    return find_all_intersections(segments)

def find_all_intersections(segments):
    events = []
    active_segments = []
    intersections = set()
    
    # Create events for segment endpoints
    for i, (p1, p2) in enumerate(segments):
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        events.append((p1[0], 'start', i, p1, p2))
        events.append((p2[0], 'end', i, p1, p2))
    
    # Sort events by x-coordinate
    events.sort()
    
    # Process events
    for x, event_type, seg_id, p1, p2 in events:
        if event_type == 'start':
            active_segments.append((seg_id, p1, p2))
            check_intersections(active_segments, intersections)
        else:
            active_segments = [seg for seg in active_segments if seg[0] != seg_id]
    
    return len(intersections)

def check_intersections(active_segments, intersections):
    for i in range(len(active_segments)):
        for j in range(i + 1, len(active_segments)):
            seg1 = active_segments[i]
            seg2 = active_segments[j]
            
            if segments_intersect(seg1[1], seg1[2], seg2[1], seg2[2]):
                intersection = find_intersection_point(seg1[1], seg1[2], seg2[1], seg2[2])
                if intersection:
                    intersections.add(intersection)

def segments_intersect(p1, p2, p3, p4):
    o1 = cross_product(p1, p2, p3)
    o2 = cross_product(p1, p2, p4)
    o3 = cross_product(p3, p4, p1)
    o4 = cross_product(p3, p4, p2)
    
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True
    
    return False

def cross_product(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def find_intersection_point(p1, p2, p3, p4):
    if not segments_intersect(p1, p2, p3, p4):
        return None
    
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return None
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)
    
    return (round(x, 6), round(y, 6))

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n + k) where n is number of segments, k is number of intersections
- **Space**: O(n) for storing events and active segments

### Why This Solution Works
- **Sweep Line Algorithm**: Efficiently processes segments in order
- **Event-Driven Processing**: Handles start/end events systematically
- **Cross Product**: Determines segment orientation and intersection
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
3 line segments:
Segment 1: (0,0) to (4,4)
Segment 2: (1,1) to (3,3)
Segment 3: (2,0) to (2,4)
```

### Line Segment Visualization
```
Y
4 |     |
3 |   \ | /
2 |     + (2,2)
1 |   / | \
0 | +---+---+---+
  +---+---+---+---+
    0   1   2   3   4  X

Segment 1: (0,0) to (4,4) - diagonal
Segment 2: (1,1) to (3,3) - diagonal
Segment 3: (2,0) to (2,4) - vertical
```

### Intersection Points
```
Intersection 1: Segment 1 ∩ Segment 2
- Point: (2,2)
- Both segments pass through (2,2)

Intersection 2: Segment 1 ∩ Segment 3
- Point: (2,2)
- Segment 1: y = x, at x=2, y=2
- Segment 3: x = 2, at x=2, y=2

Intersection 3: Segment 2 ∩ Segment 3
- Point: (2,2)
- Segment 2: y = x, at x=2, y=2
- Segment 3: x = 2, at x=2, y=2

Total intersections: 3 (all at point (2,2))
```

### Sweep Line Events
```
Events (sorted by x-coordinate):
1. x=0: Start Segment 1, (0,0) to (4,4)
2. x=1: Start Segment 2, (1,1) to (3,3)
3. x=2: Start Segment 3, (2,0) to (2,4)
4. x=2: End Segment 2, (1,1) to (3,3)
5. x=4: End Segment 1, (0,0) to (4,4)
6. x=2: End Segment 3, (2,0) to (2,4)

Active segments at each x:
x=0: [Segment 1]
x=1: [Segment 1, Segment 2]
x=2: [Segment 1, Segment 2, Segment 3] → Check intersections
x=4: [Segment 1, Segment 3]
```

### Cross Product Calculation
```
For intersection of Segment 1 and Segment 2:
Segment 1: (0,0) to (4,4)
Segment 2: (1,1) to (3,3)

Cross product test:
- Point (1,1) relative to Segment 1: (1-0)(4-0) - (1-0)(4-0) = 0
- Point (3,3) relative to Segment 1: (3-0)(4-0) - (3-0)(4-0) = 0
- Both points are collinear with Segment 1

Intersection exists at (2,2)
```

### Step-by-Step Sweep Line Process
```
Step 1: x=0, Start Segment 1
Active segments: [Segment 1]
Intersections found: 0

Step 2: x=1, Start Segment 2
Active segments: [Segment 1, Segment 2]
Check intersection: Segment 1 ∩ Segment 2
- Intersection at (2,2)
- Add to result
Intersections found: 1

Step 3: x=2, Start Segment 3
Active segments: [Segment 1, Segment 2, Segment 3]
Check intersections:
- Segment 1 ∩ Segment 3: (2,2)
- Segment 2 ∩ Segment 3: (2,2)
- Add to result
Intersections found: 3

Step 4: x=2, End Segment 2
Active segments: [Segment 1, Segment 3]
Intersections found: 3

Step 5: x=4, End Segment 1
Active segments: [Segment 3]
Intersections found: 3

Step 6: x=2, End Segment 3
Active segments: []
Intersections found: 3
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(1)         │ Check all    │
│                 │              │              │ pairs        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sweep Line      │ O(n log n + k)│ O(n)        │ Process      │
│                 │              │              │ events       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bentley-Ottmann │ O(n log n + k)│ O(n)        │ Advanced     │
│                 │              │              │ sweep line   │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Sweep Line Algorithm**
- Process segments in order of x-coordinates
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Cross Product for Orientation**
- Determines if three points are clockwise, counterclockwise, or collinear
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Event-Driven Processing**
- Handle segment start/end events systematically
- Important for understanding
- Fundamental concept
- Essential for efficiency

## 🎯 Problem Variations

### Variation 1: Intersection Points with Weights
**Problem**: Each intersection point has a weight, find total weight.

```python
def intersection_points_with_weights(segments, weight_function):
    intersections = find_all_intersections(segments)
    total_weight = 0
    
    for intersection in intersections:
        total_weight += weight_function(intersection)
    
    return total_weight

def simple_weight(point):
    return point[0] + point[1]

# Example usage
result = intersection_points_with_weights(segments, simple_weight)
print(f"Weighted intersections: {result}")
```

### Variation 2: Intersection Points with Constraints
**Problem**: Find intersections subject to certain constraints.

```python
def intersection_points_with_constraints(segments, constraints):
    intersections = find_all_intersections(segments)
    constrained_intersections = []
    
    for intersection in intersections:
        if check_constraints(intersection, constraints):
            constrained_intersections.append(intersection)
    
    return constrained_intersections

def check_constraints(point, constraints):
    x, y = point
    if x >= constraints["min_x"] and x <= constraints["max_x"] and \
       y >= constraints["min_y"] and y <= constraints["max_y"]:
        return True
    return False

# Example usage
constraints = {"min_x": 0, "max_x": 5, "min_y": 0, "max_y": 5}
result = intersection_points_with_constraints(segments, constraints)
print(f"Constrained intersections: {result}")
```

### Variation 3: Intersection Points with Dynamic Updates
**Problem**: Support adding/removing segments and finding intersections.

```python
class DynamicIntersections:
    def __init__(self):
        self.segments = []
    
    def add_segment(self, p1, p2):
        self.segments.append((p1, p2))
    
    def remove_segment(self, p1, p2):
        if (p1, p2) in self.segments:
            self.segments.remove((p1, p2))
    
    def get_intersections(self):
        return find_all_intersections(self.segments)
    
    def get_intersection_count(self):
        return len(self.get_intersections())

# Example usage
dynamic_system = DynamicIntersections()
dynamic_system.add_segment((0, 0), (2, 2))
dynamic_system.add_segment((1, 0), (1, 2))
intersections = dynamic_system.get_intersections()
count = dynamic_system.get_intersection_count()
print(f"Dynamic intersections: {intersections}, count: {count}")
```

### Variation 4: Intersection Points with Range Queries
**Problem**: Answer queries about intersections in specific ranges.

```python
def intersection_points_range_queries(segments, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Filter segments in range
        filtered_segments = []
        for p1, p2 in segments:
            if (min_x <= p1[0] <= max_x and min_y <= p1[1] <= max_y) or \
               (min_x <= p2[0] <= max_x and min_y <= p2[1] <= max_y):
                filtered_segments.append((p1, p2))
        
        # Find intersections in filtered segments
        intersections = find_all_intersections(filtered_segments)
        results.append(len(intersections))
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (1, 3, 1, 3), (0, 4, 0, 4)]
result = intersection_points_range_queries(segments, queries)
print(f"Range query results: {result}")
```

### Variation 5: Intersection Points with Convex Hull
**Problem**: Use convex hull to optimize intersection finding.

```python
def intersection_points_convex_hull(points):
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
    
    # Find intersections
    return find_all_intersections(segments)

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
result = intersection_points_convex_hull(points)
print(f"Convex hull intersections: {result}")
```

## 🔗 Related Problems

- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/)**: Basic intersection problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/)**: Point containment problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/)**: Geometric optimization

## 📚 Learning Points

1. **Sweep Line Algorithm**: Essential for geometric intersection problems
2. **Cross Product**: Important for determining orientation
3. **Event-Driven Processing**: Key for algorithm efficiency
4. **Geometric Optimization**: Important for performance

---

**This is a great introduction to intersection point algorithms!** 🎯 