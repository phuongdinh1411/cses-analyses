---
layout: simple
title: "Polygon Area Analysis"
permalink: /problem_soulutions/geometry/polygon_area_analysis
---


# Polygon Area Analysis

## Problem Description

**Problem**: Given a polygon with n vertices, calculate its area using the shoelace formula.

**Input**: 
- n: number of polygon vertices
- n lines: x y (coordinates of each vertex in order)

**Output**: Area of the polygon.

**Example**:
```
Input:
4
0 0
4 0
4 3
0 3

Output:
12.0

Explanation: 
Using shoelace formula:
Area = |(0×0 + 4×3 + 4×3 + 0×0) - (0×4 + 0×4 + 3×0 + 3×0)| / 2
     = |(0 + 12 + 12 + 0) - (0 + 0 + 0 + 0)| / 2
     = |24 - 0| / 2
     = 24 / 2
     = 12.0
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Calculate area of a polygon from its vertices
- Use geometric area formulas
- Handle different polygon types
- Apply shoelace formula efficiently

**Key Observations:**
- Shoelace formula works for any polygon
- Vertices must be in order (clockwise or counterclockwise)
- Formula handles self-intersecting polygons
- O(n) time complexity is optimal

### Step 2: Shoelace Formula Approach
**Idea**: Use the shoelace formula to calculate area directly from vertex coordinates.

```python
def polygon_area_shoelace(vertices):
    n = len(vertices)
    if n < 3:
        return 0
    
    area = 0
    for i in range(n):
        j = (i + 1) % n  # Next vertex (wraps around)
        
        # Shoelace formula: area += xi * yi+1 - xi+1 * yi
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    
    return abs(area) / 2
```

**Why this works:**
- Shoelace formula is mathematically proven
- Handles all polygon types correctly
- Simple and efficient implementation
- O(n) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_polygon_area():
    n = int(input())
    vertices = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        vertices.append((x, y))
    
    area = calculate_polygon_area(vertices)
    print(f"{area:.1f}")

def calculate_polygon_area(vertices):
    n = len(vertices)
    if n < 3:
        return 0
    
    area = 0
    for i in range(n):
        j = (i + 1) % n
        
        # Shoelace formula
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    
    return abs(area) / 2

# Main execution
if __name__ == "__main__":
    solve_polygon_area()
```

**Why this works:**
- Optimal shoelace formula approach
- Handles all edge cases correctly
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(0, 0), (4, 0), (4, 3), (0, 3)], 12.0),  # Rectangle
        ([(0, 0), (2, 0), (1, 2)], 2.0),            # Triangle
        ([(0, 0), (1, 0), (1, 1), (0, 1)], 1.0),   # Square
        ([(0, 0), (3, 0), (3, 4), (0, 4)], 12.0),  # Rectangle
    ]
    
    for vertices, expected in test_cases:
        result = solve_test(vertices)
        print(f"Vertices: {vertices}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if abs(result - expected) < 1e-9 else '✗ FAIL'}")
        print()

def solve_test(vertices):
    return calculate_polygon_area(vertices)

def calculate_polygon_area(vertices):
    n = len(vertices)
    if n < 3:
        return 0
    
    area = 0
    for i in range(n):
        j = (i + 1) % n
        
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    
    return abs(area) / 2

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through all vertices
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Shoelace Formula**: Mathematically proven area calculation
- **Vertex Order**: Works with any vertex ordering
- **Polygon Types**: Handles simple and complex polygons
- **Efficient Algorithm**: Optimal time complexity

## 🎨 Visual Example

### Input Example
```
Polygon:
4
0 0
4 0
4 3
0 3
```

### Polygon Visualization
```
Coordinate System:
    y
    ↑
    │
3.0 │•─────────•
    │(0,3)     │(4,3)
    │          │
    │          │
    │          │
    │          │
0.0 │•─────────•
    │(0,0)     │(4,0)
    │          │
    └──────────┼────→ x
               4.0

Polygon vertices (counterclockwise):
1. (0,0) - bottom-left
2. (4,0) - bottom-right
3. (4,3) - top-right
4. (0,3) - top-left

This is a rectangle with width=4 and height=3
```

### Shoelace Formula Application
```
Shoelace Formula: Area = |Σ(xi * yi+1 - xi+1 * yi)| / 2

For vertices: (0,0), (4,0), (4,3), (0,3)

Step 1: Calculate cross products
i=0: x0 * y1 - x1 * y0 = 0 * 0 - 4 * 0 = 0
i=1: x1 * y2 - x2 * y1 = 4 * 3 - 4 * 0 = 12
i=2: x2 * y3 - x3 * y2 = 4 * 3 - 0 * 3 = 12
i=3: x3 * y0 - x0 * y3 = 0 * 0 - 0 * 3 = 0

Step 2: Sum the cross products
Sum = 0 + 12 + 12 + 0 = 24

Step 3: Calculate area
Area = |24| / 2 = 12.0
```

### Shoelace Formula Visualization
```
The "shoelace" pattern:

For vertices: (0,0), (4,0), (4,3), (0,3)

Forward products (like lacing a shoe):
x0 * y1 = 0 * 0 = 0
x1 * y2 = 4 * 3 = 12
x2 * y3 = 4 * 3 = 12
x3 * y0 = 0 * 0 = 0
Forward sum = 24

Backward products (reverse lacing):
x1 * y0 = 4 * 0 = 0
x2 * y1 = 4 * 0 = 0
x3 * y2 = 0 * 3 = 0
x0 * y3 = 0 * 3 = 0
Backward sum = 0

Area = |Forward sum - Backward sum| / 2
     = |24 - 0| / 2
     = 12.0
```

### Different Vertex Orderings
```
Case 1: Counterclockwise (original)
(0,0) → (4,0) → (4,3) → (0,3) → (0,0)
Area = 12.0

Case 2: Clockwise
(0,0) → (0,3) → (4,3) → (4,0) → (0,0)
Area = |0 + 12 + 12 + 0 - (0 + 0 + 0 + 0)| / 2 = 12.0

Case 3: Different starting point
(4,0) → (4,3) → (0,3) → (0,0) → (4,0)
Area = |0 + 12 + 0 + 0 - (12 + 0 + 0 + 0)| / 2 = 12.0

The shoelace formula works regardless of starting point or direction!
```

### Complex Polygon Example
```
Triangle with vertices: (0,0), (3,0), (1,2)

Coordinate System:
    y
    ↑
    │
2.0 │     • (1,2)
    │    / \
    │   /   \
    │  /     \
    │ /       \
0.0 │•─────────•
    │(0,0)     │(3,0)
    │          │
    └──────────┼────→ x
               3.0

Shoelace calculation:
Forward: 0*0 + 3*2 + 1*0 = 6
Backward: 3*0 + 1*0 + 0*2 = 0
Area = |6 - 0| / 2 = 3.0

Verification: Triangle area = (base * height) / 2 = (3 * 2) / 2 = 3.0 ✓
```

### Step-by-Step Calculation
```
For rectangle: (0,0), (4,0), (4,3), (0,3)

Step 1: List vertices in order
V0 = (0,0), V1 = (4,0), V2 = (4,3), V3 = (0,3)

Step 2: Calculate each term
Term 0: x0 * y1 - x1 * y0 = 0 * 0 - 4 * 0 = 0
Term 1: x1 * y2 - x2 * y1 = 4 * 3 - 4 * 0 = 12
Term 2: x2 * y3 - x3 * y2 = 4 * 3 - 0 * 3 = 12
Term 3: x3 * y0 - x0 * y3 = 0 * 0 - 0 * 3 = 0

Step 3: Sum all terms
Sum = 0 + 12 + 12 + 0 = 24

Step 4: Calculate final area
Area = |Sum| / 2 = |24| / 2 = 12.0
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Method      │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Shoelace        │ O(n)         │ O(1)         │ Cross        │
│ Formula         │              │              │ products     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Triangulation   │ O(n log n)   │ O(n)         │ Divide into  │
│                 │              │              │ triangles    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Green's         │ O(n)         │ O(1)         │ Line         │
│ Theorem         │              │              │ integrals    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Monte Carlo     │ O(k)         │ O(1)         │ Random       │
│                 │              │              │ sampling     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Polygon Area Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: n vertices│
              │ (x1,y1), ...,   │
              │ (xn,yn)         │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize      │
              │ area = 0        │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For i = 0 to n-1│
              │ j = (i+1) mod n │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ area += xi * yj │
              │ area -= xj * yi │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ area = |area|/2 │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return area     │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Shoelace Formula**
- Area = |Σ(xi * yi+1 - xi+1 * yi)| / 2
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Vertex Ordering**
- Works with clockwise or counterclockwise order
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Mathematical Properties**
- Formula works for all polygon types
- Important for understanding
- Fundamental concept
- Essential for correctness

## 🎯 Problem Variations

### Variation 1: Polygon Area with Weights
**Problem**: Each vertex has a weight, calculate weighted area.

```python
def polygon_area_with_weights(vertices_with_weights):
    n = len(vertices_with_weights)
    if n < 3:
        return 0
    
    area = 0
    for i in range(n):
        j = (i + 1) % n
        
        (x1, y1), w1 = vertices_with_weights[i]
        (x2, y2), w2 = vertices_with_weights[j]
        
        # Weighted shoelace formula
        area += x1 * y2 * w1 * w2
        area -= x2 * y1 * w1 * w2
    
    return abs(area) / 2

# Example usage
vertices_with_weights = [((0, 0), 1), ((4, 0), 2), ((4, 3), 1), ((0, 3), 2)]
result = polygon_area_with_weights(vertices_with_weights)
print(f"Weighted polygon area: {result}")
```

### Variation 2: Polygon Area with Holes
**Problem**: Calculate area of polygon with holes.

```python
def polygon_area_with_holes(outer_vertices, hole_vertices_list):
    # Calculate outer polygon area
    outer_area = calculate_polygon_area(outer_vertices)
    
    # Subtract areas of holes
    for hole_vertices in hole_vertices_list:
        hole_area = calculate_polygon_area(hole_vertices)
        outer_area -= hole_area
    
    return max(0, outer_area)

# Example usage
outer = [(0, 0), (4, 0), (4, 4), (0, 4)]
holes = [[(1, 1), (3, 1), (3, 3), (1, 3)]]
result = polygon_area_with_holes(outer, holes)
print(f"Polygon with holes area: {result}")
```

### Variation 3: Polygon Area with Dynamic Updates
**Problem**: Support adding/removing vertices and calculating area.

```python
class DynamicPolygon:
    def __init__(self):
        self.vertices = []
    
    def add_vertex(self, x, y):
        self.vertices.append((x, y))
    
    def remove_vertex(self, x, y):
        if (x, y) in self.vertices:
            self.vertices.remove((x, y))
    
    def get_area(self):
        return calculate_polygon_area(self.vertices)
    
    def get_perimeter(self):
        n = len(self.vertices)
        if n < 2:
            return 0
        
        perimeter = 0
        for i in range(n):
            j = (i + 1) % n
            dx = self.vertices[i][0] - self.vertices[j][0]
            dy = self.vertices[i][1] - self.vertices[j][1]
            perimeter += (dx**2 + dy**2)**0.5
        
        return perimeter

# Example usage
dynamic_polygon = DynamicPolygon()
dynamic_polygon.add_vertex(0, 0)
dynamic_polygon.add_vertex(2, 0)
dynamic_polygon.add_vertex(1, 2)
area = dynamic_polygon.get_area()
perimeter = dynamic_polygon.get_perimeter()
print(f"Dynamic polygon area: {area}, perimeter: {perimeter}")
```

### Variation 4: Polygon Area with Range Queries
**Problem**: Answer queries about area in specific ranges.

```python
def polygon_area_range_queries(vertices, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Filter vertices in range
        filtered_vertices = []
        for x, y in vertices:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                filtered_vertices.append((x, y))
        
        if len(filtered_vertices) < 3:
            results.append(0)
        else:
            # Calculate area of filtered polygon
            area = calculate_polygon_area(filtered_vertices)
            results.append(area)
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (1, 3, 1, 3), (0, 4, 0, 4)]
result = polygon_area_range_queries(vertices, queries)
print(f"Range query results: {result}")
```

### Variation 5: Polygon Area with Convex Hull
**Problem**: Calculate area of convex hull of given points.

```python
def convex_hull_area(points):
    if len(points) < 3:
        return 0
    
    # Build convex hull using Graham scan
    hull = build_convex_hull(points)
    
    # Calculate area of convex hull
    return calculate_polygon_area(hull)

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

def cross_product(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

# Example usage
points = [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.5)]
result = convex_hull_area(points)
print(f"Convex hull area: {result}")
```

## 🔗 Related Problems

- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/)**: Polygon containment problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/)**: Geometric optimization
- **[Geometric Algorithms](/cses-analyses/problem_soulutions/geometry/)**: Other geometric problems

## 📚 Learning Points

1. **Shoelace Formula**: Essential for polygon area calculations
2. **Vertex Ordering**: Important for algorithm correctness
3. **Mathematical Properties**: Key for understanding algorithms
4. **Geometric Optimization**: Important for efficiency

---

**This is a great introduction to polygon area algorithms!** 🎯 