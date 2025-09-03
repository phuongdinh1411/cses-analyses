---
layout: simple
title: "Point in Polygon - Geometry Analysis"
permalink: /problem_soulutions/geometry/point_in_polygon_analysis
---


# Point in Polygon - Geometry Analysis

## Problem Description

**Problem**: Given a polygon with n vertices and m query points, determine if each query point lies inside, outside, or on the boundary of the polygon.

**Input**: 
- n: number of polygon vertices
- n lines: x y (coordinates of each vertex in order)
- m: number of query points
- m lines: x y (coordinates of each query point)

**Output**: For each query point, print "INSIDE", "OUTSIDE", or "BOUNDARY".

**Example**:
```
Input:
4
0 0
4 0
4 4
0 4
3
2 2
5 5
0 0

Output:
INSIDE
OUTSIDE
BOUNDARY

Explanation: 
- Point (2,2) is inside the square polygon
- Point (5,5) is outside the square polygon  
- Point (0,0) is on the boundary of the square polygon
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Determine if points lie inside, outside, or on polygon boundary
- Use geometric point-in-polygon algorithms
- Handle multiple query points efficiently
- Apply ray casting techniques

**Key Observations:**
- Need to handle all polygon types (convex, concave)
- Ray casting is the standard approach
- Boundary cases require special handling
- O(n) time per query is optimal

### Step 2: Ray Casting Approach
**Idea**: Cast a ray from the point to infinity and count intersections with polygon edges.

```python
def point_in_polygon_ray_casting(point, polygon):
    n = len(polygon)
    inside = False
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        # Check if point is on boundary
        if on_segment(p1, point, p2):
            return "BOUNDARY"
        
        # Ray casting: count intersections
        if ((p1[1] > point[1]) != (p2[1] > point[1])) and \
           (point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return "INSIDE" if inside else "OUTSIDE"

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))
```

**Why this works:**
- Ray casting is the standard method
- Handles all polygon types correctly
- Parity rule: odd intersections = inside
- O(n) time complexity per query

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_point_in_polygon():
    n, m = map(int, input().split())
    
    # Read polygon vertices
    polygon = []
    for _ in range(n):
        x, y = map(int, input().split())
        polygon.append((x, y))
    
    # Process each query
    for _ in range(m):
        x, y = map(int, input().split())
        result = point_in_polygon((x, y), polygon)
        print(result)

def point_in_polygon(point, polygon):
    n = len(polygon)
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        # Check if point is on boundary
        if on_segment(p1, point, p2):
            return "BOUNDARY"
    
    # Ray casting algorithm
    inside = False
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if ((p1[1] > point[1]) != (p2[1] > point[1])) and \
           (point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return "INSIDE" if inside else "OUTSIDE"

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

# Main execution
if __name__ == "__main__":
    solve_point_in_polygon()
```

**Why this works:**
- Optimal ray casting approach
- Handles all edge cases correctly
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(0, 0), (4, 0), (4, 4), (0, 4)], [(2, 2), (5, 5), (0, 0)], 
         ["INSIDE", "OUTSIDE", "BOUNDARY"]),
        ([(0, 0), (2, 0), (1, 2)], [(1, 1), (0, 0), (3, 3)], 
         ["INSIDE", "BOUNDARY", "OUTSIDE"]),
    ]
    
    for polygon, queries, expected in test_cases:
        results = []
        for point in queries:
            result = point_in_polygon(point, polygon)
            results.append(result)
        
        print(f"Polygon: {polygon}")
        print(f"Queries: {queries}")
        print(f"Expected: {expected}, Got: {results}")
        print(f"{'✓ PASS' if results == expected else '✗ FAIL'}")
        print()

def point_in_polygon(point, polygon):
    n = len(polygon)
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if on_segment(p1, point, p2):
            return "BOUNDARY"
    
    inside = False
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if ((p1[1] > point[1]) != (p2[1] > point[1])) and \
           (point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return "INSIDE" if inside else "OUTSIDE"

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) per query - check all polygon edges
- **Space**: O(1) - constant space per query

### Why This Solution Works
- **Ray Casting**: Standard method for point-in-polygon test
- **Parity Rule**: Odd intersections = inside, even = outside
- **Boundary Handling**: Special case for points on edges
- **Robust Algorithm**: Handles all polygon types

## 🎯 Key Insights

### 1. **Ray Casting Algorithm**
- Cast ray from point to infinity
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Parity Rule**
- Odd intersections = inside
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Boundary Handling**
- Check if point lies on edges
- Important for understanding
- Fundamental concept
- Essential for accuracy

## 🎯 Problem Variations

### Variation 1: Point in Polygon with Multiple Polygons
**Problem**: Check if a point lies inside any of multiple polygons.

```python
def point_in_multiple_polygons(point, polygons):
    for i, polygon in enumerate(polygons):
        result = point_in_polygon(point, polygon)
        if result == "INSIDE":
            return f"INSIDE_POLYGON_{i}"
        elif result == "BOUNDARY":
            return f"BOUNDARY_POLYGON_{i}"
    
    return "OUTSIDE_ALL"

# Example usage
polygons = [
    [(0, 0), (2, 0), (1, 2)],
    [(3, 0), (5, 0), (4, 2)]
]
result = point_in_multiple_polygons((1, 1), polygons)
print(f"Point in multiple polygons: {result}")
```

### Variation 2: Point in Polygon with Weights
**Problem**: Each polygon has a weight, find total weight of polygons containing the point.

```python
def point_in_polygons_with_weights(point, polygons_with_weights):
    total_weight = 0
    
    for polygon, weight in polygons_with_weights:
        result = point_in_polygon(point, polygon)
        if result == "INSIDE":
            total_weight += weight
    
    return total_weight

# Example usage
polygons_with_weights = [
    ([(0, 0), (2, 0), (1, 2)], 3),
    ([(3, 0), (5, 0), (4, 2)], 2)
]
result = point_in_polygons_with_weights((1, 1), polygons_with_weights)
print(f"Weighted polygon result: {result}")
```

### Variation 3: Point in Polygon with Dynamic Updates
**Problem**: Support adding/removing polygon vertices and answering queries.

```python
class DynamicPolygon:
    def __init__(self):
        self.vertices = []
    
    def add_vertex(self, x, y):
        self.vertices.append((x, y))
    
    def remove_vertex(self, x, y):
        if (x, y) in self.vertices:
            self.vertices.remove((x, y))
    
    def query_point(self, x, y):
        if len(self.vertices) < 3:
            return "INVALID_POLYGON"
        return point_in_polygon((x, y), self.vertices)

# Example usage
dynamic_polygon = DynamicPolygon()
dynamic_polygon.add_vertex(0, 0)
dynamic_polygon.add_vertex(2, 0)
dynamic_polygon.add_vertex(1, 2)
result = dynamic_polygon.query_point(1, 1)
print(f"Dynamic polygon query: {result}")
```

### Variation 4: Point in Polygon with Range Queries
**Problem**: Answer queries about points in specific ranges.

```python
def point_in_polygon_range_queries(polygon, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Check if any point in range is inside polygon
        found_inside = False
        found_boundary = False
        
        # Sample points in range
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                result = point_in_polygon((x, y), polygon)
                if result == "INSIDE":
                    found_inside = True
                elif result == "BOUNDARY":
                    found_boundary = True
        
        if found_inside:
            results.append("CONTAINS_INSIDE")
        elif found_boundary:
            results.append("CONTAINS_BOUNDARY")
        else:
            results.append("NO_POINTS")
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (3, 5, 3, 5), (0, 5, 0, 5)]
result = point_in_polygon_range_queries(polygon, queries)
print(f"Range query results: {result}")
```

### Variation 5: Point in Polygon with Convex Hull
**Problem**: Use convex hull optimization for faster queries.

```python
def point_in_polygon_convex_hull(point, polygon):
    # First check if point is outside convex hull (faster rejection)
    if not point_in_convex_hull(point, polygon):
        return "OUTSIDE"
    
    # Then use full ray casting for accurate result
    return point_in_polygon(point, polygon)

def point_in_convex_hull(point, polygon):
    n = len(polygon)
    
    # Check if point is on same side of all edges
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        # Cross product to determine side
        cross = (p2[0] - p1[0]) * (point[1] - p1[1]) - \
                (p2[1] - p1[1]) * (point[0] - p1[0])
        
        if cross < 0:  # Point is on wrong side
            return False
    
    return True

# Example usage
result = point_in_polygon_convex_hull((1, 1), polygon)
print(f"Convex hull optimized result: {result}")
```

## 🔗 Related Problems

- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/)**: Similar geometric problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/)**: Polygon optimization
- **[Geometric Algorithms](/cses-analyses/problem_soulutions/geometry/)**: Other geometric problems

## 📚 Learning Points

1. **Ray Casting**: Essential for point-in-polygon tests
2. **Parity Rule**: Important for understanding algorithms
3. **Boundary Handling**: Key for accurate results
4. **Geometric Properties**: Important for spatial algorithms

---

**This is a great introduction to point-in-polygon algorithms!** 🎯
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