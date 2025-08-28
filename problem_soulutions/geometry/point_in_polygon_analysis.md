---
layout: simple
title: Point in Polygon - CSES Geometry Analysis
permalink: /problem_soulutions/geometry/point_in_polygon_analysis/
---

# Point in Polygon - CSES Geometry Analysis

## Problem Description
Determine if a point lies inside, outside, or on the boundary of a polygon.

## Solution Progression

### 1. **Brute Force Approach**
**Description**: Use ray casting algorithm (point-in-polygon test).

**Why this is inefficient**: 
- Need to handle edge cases carefully
- Complex logic for boundary cases
- May have precision issues

**Why this improvement works**:
- Ray casting is the standard method
- Handles all polygon types
- Robust algorithm

### 2. **Optimal Solution**
**Description**: Implement ray casting with proper edge case handling.

**Key Insights**:
- Cast ray from point to infinity
- Count intersections with polygon edges
- Odd count = inside, even count = outside
- Handle boundary cases separately

## Complete Implementation

```python
def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def point_in_polygon(point, polygon):
    """Determine if point is inside, outside, or on boundary of polygon"""
    n = len(polygon)
    inside = False
    on_boundary = False
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        # Check if point is on boundary
        if on_segment(p1, point, p2):
            return "BOUNDARY"
        
        # Ray casting algorithm
        if ((p1[1] > point[1]) != (p2[1] > point[1])) and \
           (point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return "INSIDE" if inside else "OUTSIDE"

# Read input
n, m = map(int, input().split())
polygon = []
for _ in range(n):
    x, y = map(int, input().split())
    polygon.append((x, y))

for _ in range(m):
    x, y = map(int, input().split())
    result = point_in_polygon((x, y), polygon)
    print(result)
```

## Complexity Analysis
- **Time Complexity**: O(n) per query where n is number of polygon vertices
- **Space Complexity**: O(1) additional space per query

## Key Insights for Other Problems

### **Principles**:
1. **Ray Casting Algorithm**: Standard method for point-in-polygon test
2. **Parity Rule**: Odd intersections = inside, even = outside
3. **Boundary Handling**: Special case for points on polygon edges

### **Applicability**:
- Point location problems
- Geometric algorithms
- Spatial queries
- Computational geometry

### **Example Problems**:
- Polygon containment
- Spatial indexing
- Geometric algorithms
- Computational geometry

## Notable Techniques

### **Code Patterns**:
```python
# Ray casting implementation
def ray_casting(point, polygon):
    n = len(polygon)
    inside = False
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if ((p1[1] > point[1]) != (p2[1] > point[1])) and \
           (point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return inside

# Winding number algorithm (alternative)
def winding_number(point, polygon):
    n = len(polygon)
    wn = 0
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if p1[1] <= point[1]:
            if p2[1] > point[1] and cross_product(p1, p2, point) > 0:
                wn += 1
        else:
            if p2[1] <= point[1] and cross_product(p1, p2, point) < 0:
                wn -= 1
    
    return wn != 0
```

## Problem-Solving Framework

### **1. Understand the Geometry**
- Visualize the ray casting process
- Understand the parity rule
- Consider boundary cases

### **2. Choose the Right Tool**
- Ray casting for general polygons
- Winding number for complex cases
- Proper edge case handling

### **3. Handle Edge Cases**
- Points on polygon edges
- Points on polygon vertices
- Degenerate polygons

### **4. Optimize for Precision**
- Use integer arithmetic when possible
- Handle floating point precision
- Consider numerical stability 