# Point Location Test - CSES Geometry Analysis

## Problem Description
Given a point and a line segment, determine whether the point is on the line segment, to the left, or to the right.

## Solution Progression

### 1. **Brute Force Approach**
**Description**: Calculate the cross product to determine the orientation of three points.

**Why this is inefficient**: 
- Requires understanding of cross product geometry
- Need to handle edge cases carefully
- May have precision issues with floating point arithmetic

**Why this improvement works**:
- Cross product gives us the orientation directly
- Handles all cases: left, right, collinear, on segment

### 2. **Optimal Solution**
**Description**: Use cross product to determine orientation and then check if point lies on segment.

**Key Insights**:
- Cross product of vectors gives orientation
- Point is on segment if collinear and within bounds
- Use integer arithmetic to avoid precision issues

## Complete Implementation

```python
def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

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
        if (min(segment_start[0], segment_end[0]) <= point[0] <= max(segment_start[0], segment_end[0]) and
            min(segment_start[1], segment_end[1]) <= point[1] <= max(segment_start[1], segment_end[1])):
            return "ON_SEGMENT"
        else:
            return "ON_LINE"

# Read input
n = int(input())
for _ in range(n):
    x1, y1, x2, y2, px, py = map(int, input().split())
    result = point_location_test((x1, y1), (x2, y2), (px, py))
    print(result)
```

## Complexity Analysis
- **Time Complexity**: O(1) per test case
- **Space Complexity**: O(1)

## Key Insights for Other Problems

### **Principles**:
1. **Cross Product for Orientation**: Use cross product to determine relative position of points
2. **Integer Arithmetic**: Avoid floating point precision issues in geometry problems
3. **Collinearity Check**: Use cross product = 0 to detect collinear points

### **Applicability**:
- Point-in-polygon problems
- Line segment intersection
- Convex hull algorithms
- Geometric algorithms requiring orientation tests

### **Example Problems**:
- Line segment intersection
- Point in polygon
- Convex hull construction
- Triangulation problems

## Notable Techniques

### **Code Patterns**:
```python
# Cross product calculation
def cross_product(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

# Orientation test
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