---
layout: simple
title: "Line Segment Intersection - Geometry Analysis"
permalink: /problem_soulutions/geometry/line_segment_intersection_analysis
---


# Line Segment Intersection - Geometry Analysis

## Problem Description
Given two line segments, determine if they intersect.

## Solution Progression

### 1. **Brute Force Approach**
**Description**: Check all possible cases of line segment intersection manually.

**Why this is inefficient**: 
- Requires handling many edge cases
- Complex logic for different intersection scenarios
- Error-prone implementation

**Why this improvement works**:
- Use orientation tests to determine intersection
- Systematic approach using cross products
- Handles all edge cases properly

### 2. **Optimal Solution**
**Description**: Use orientation tests and bounding box checks to determine intersection.

**Key Insights**:
- Two segments intersect if they have different orientations
- Need to check bounding boxes for efficiency
- Handle collinear cases separately

## Complete Implementation

```python
def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def orientation(a, b, c):
    """Determine orientation of three points"""
    cross = cross_product(a, b, c)
    if cross > 0: return 1  # Counterclockwise
    elif cross < 0: return -1  # Clockwise
    else: return 0  # Collinear

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def segments_intersect(p1, p2, p3, p4):
    """Check if segments p1p2 and p3p4 intersect"""
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

# Read input
n = int(input())
for _ in range(n):
    x1, y1, x2, y2, x3, y3, x4, y4 = map(int, input().split())
    if segments_intersect((x1, y1), (x2, y2), (x3, y3), (x4, y4)):
        print("YES")
    else:
        print("NO")
```

## Complexity Analysis
- **Time Complexity**: O(1) per test case
- **Space Complexity**: O(1)

## Key Insights for Other Problems

### **Principles**:
1. **Orientation-Based Intersection**: Use cross products to determine relative orientations
2. **Bounding Box Optimization**: Check bounding boxes first for efficiency
3. **Collinear Handling**: Special handling for collinear segments

### **Applicability**:
- Polygon intersection problems
- Sweep line algorithms
- Computational geometry
- Path planning algorithms

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