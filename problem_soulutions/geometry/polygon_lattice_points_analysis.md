---
layout: simple
title: "Polygon Lattice Points - Geometry Analysis"
permalink: /problem_soulutions/geometry/polygon_lattice_points_analysis
---


# Polygon Lattice Points - Geometry Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand lattice point counting problems and integer coordinate enumeration
- [ ] **Objective 2**: Apply Pick's theorem or ray casting algorithms to count lattice points in polygons
- [ ] **Objective 3**: Implement efficient algorithms for counting lattice points inside polygons
- [ ] **Objective 4**: Optimize lattice point counting using geometric properties and coordinate transformations
- [ ] **Objective 5**: Handle edge cases in lattice point counting (degenerate polygons, boundary points, large coordinate values)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Lattice point counting, Pick's theorem, ray casting, geometric enumeration, polygon algorithms
- **Data Structures**: Polygon structures, lattice point structures, geometric data structures
- **Mathematical Concepts**: Pick's theorem, lattice points, polygon properties, coordinate geometry, geometric enumeration
- **Programming Skills**: Polygon manipulation, lattice point calculations, geometric computations, enumeration algorithms
- **Related Problems**: Point in Polygon (polygon algorithms), Polygon Area (polygon properties), Lattice point problems

## Problem Description

**Problem**: Given a polygon with n vertices, count the number of lattice points (integer coordinates) that lie inside the polygon.

**Input**: 
- n: number of polygon vertices
- n lines: x y (coordinates of each vertex in order)

**Output**: Number of lattice points inside the polygon.

**Example**:
```
Input:
4
0 0
4 0
4 3
0 3

Output:
6

Explanation: 
Using Pick's theorem: A = I + B/2 - 1
Area = 6 (using shoelace formula)
Boundary points = 10 (including vertices)
Interior points = 6 - 10/2 + 1 = 6
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Count lattice points inside a polygon
- Use Pick's theorem for efficiency
- Calculate area and boundary points
- Apply geometric counting algorithms

**Key Observations:**
- Pick's theorem relates area, interior, and boundary points
- Boundary points can be counted using GCD
- Area calculated using shoelace formula
- O(n) time complexity is optimal

### Step 2: Pick's Theorem Approach
**Idea**: Use Pick's theorem: A = I + B/2 - 1, where A is area, I is interior points, B is boundary points.

```python
def polygon_lattice_points_picks_theorem(vertices):
    # Pick's theorem: A = I + B/2 - 1
    # Therefore: I = A - B/2 + 1
    
    area = polygon_area(vertices)
    boundary = boundary_points(vertices)
    interior = area - boundary // 2 + 1
    
    return interior

def polygon_area(vertices):
    """Calculate area using shoelace formula"""
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
    return abs(area) // 2

def boundary_points(vertices):
    """Count lattice points on polygon boundary"""
    n = len(vertices)
    boundary = 0
    
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        # Number of lattice points on line segment is GCD(dx, dy) + 1
        boundary += gcd(dx, dy)
    
    return boundary

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a
```

**Why this works:**
- Pick's theorem is mathematically proven
- GCD gives exact boundary point count
- Shoelace formula calculates area efficiently
- O(n) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_polygon_lattice_points():
    n = int(input())
    vertices = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        vertices.append((x, y))
    
    result = count_interior_lattice_points(vertices)
    print(result)

def count_interior_lattice_points(vertices):
    # Pick's theorem: A = I + B/2 - 1
    # Therefore: I = A - B/2 + 1
    
    area = calculate_polygon_area(vertices)
    boundary = count_boundary_points(vertices)
    interior = area - boundary // 2 + 1
    
    return interior

def calculate_polygon_area(vertices):
    """Calculate area using shoelace formula"""
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
    return abs(area) // 2

def count_boundary_points(vertices):
    """Count lattice points on polygon boundary"""
    n = len(vertices)
    boundary = 0
    
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        # Number of lattice points on line segment is GCD(dx, dy) + 1
        boundary += gcd(dx, dy)
    
    return boundary

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

# Main execution
if __name__ == "__main__":
    solve_polygon_lattice_points()
```

**Why this works:**
- Optimal Pick's theorem approach
- Handles all edge cases correctly
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(0, 0), (4, 0), (4, 3), (0, 3)], 6),      # Rectangle
        ([(0, 0), (2, 0), (1, 2)], 1),               # Triangle
        ([(0, 0), (1, 0), (1, 1), (0, 1)], 0),      # Square (no interior points)
        ([(0, 0), (3, 0), (3, 2), (0, 2)], 2),      # Rectangle
    ]
    
    for vertices, expected in test_cases:
        result = solve_test(vertices)
        print(f"Vertices: {vertices}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(vertices):
    return count_interior_lattice_points(vertices)

def count_interior_lattice_points(vertices):
    area = calculate_polygon_area(vertices)
    boundary = count_boundary_points(vertices)
    interior = area - boundary // 2 + 1
    return interior

def calculate_polygon_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
    return abs(area) // 2

def count_boundary_points(vertices):
    n = len(vertices)
    boundary = 0
    
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        boundary += gcd(dx, dy)
    
    return boundary

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through all vertices
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Pick's Theorem**: Mathematically proven relationship
- **GCD Calculation**: Exact boundary point counting
- **Shoelace Formula**: Efficient area calculation
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
4 vertices:
(0,0), (4,0), (4,3), (0,3)
```

### Polygon Visualization
```
Y
3 | +---+---+---+---+
2 | |   |   |   |   |
1 | |   |   |   |   |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Polygon vertices: (0,0), (4,0), (4,3), (0,3)
```

### Lattice Points
```
Interior lattice points (marked with *):
Y
3 | +---+---+---+---+
2 | | * | * | * | * |
1 | | * | * | * | * |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Interior points: (1,1), (1,2), (2,1), (2,2), (3,1), (3,2)
Total interior points: 6
```

### Boundary Points
```
Boundary lattice points (marked with +):
Y
3 | +---+---+---+---+
2 | |   |   |   |   |
1 | |   |   |   |   |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Boundary points: (0,0), (1,0), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (3,3), (2,3), (1,3), (0,3), (0,2), (0,1)
Total boundary points: 14
```

### Pick's Theorem Application
```
Pick's Theorem: A = I + B/2 - 1
Where:
- A = Area of polygon
- I = Number of interior lattice points
- B = Number of boundary lattice points

Given:
- A = 12 (4 × 3 rectangle)
- B = 14 (boundary points)
- I = ?

Solving: 12 = I + 14/2 - 1
12 = I + 7 - 1
12 = I + 6
I = 12 - 6 = 6

Interior lattice points: 6
```

### Shoelace Formula
```
Area calculation using shoelace formula:
Vertices: (0,0), (4,0), (4,3), (0,3)

Area = |(0×0 + 4×3 + 4×3 + 0×0) - (0×4 + 0×4 + 3×0 + 3×0)| / 2
Area = |(0 + 12 + 12 + 0) - (0 + 0 + 0 + 0)| / 2
Area = |24 - 0| / 2
Area = 24 / 2 = 12
```

### GCD for Boundary Points
```
For each edge, count lattice points:
Edge 1: (0,0) to (4,0)
- dx = 4, dy = 0
- GCD(4,0) = 4
- Lattice points: 4 + 1 = 5

Edge 2: (4,0) to (4,3)
- dx = 0, dy = 3
- GCD(0,3) = 3
- Lattice points: 3 + 1 = 4

Edge 3: (4,3) to (0,3)
- dx = -4, dy = 0
- GCD(4,0) = 4
- Lattice points: 4 + 1 = 5

Edge 4: (0,3) to (0,0)
- dx = 0, dy = -3
- GCD(0,3) = 3
- Lattice points: 3 + 1 = 4

Total boundary points: 5 + 4 + 5 + 4 - 4 = 14
(Subtract 4 because vertices are counted twice)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(area)      │ O(1)         │ Check each   │
│                 │              │              │ point        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Pick's Theorem  │ O(n)         │ O(1)         │ Use          │
│                 │              │              │ mathematical │
│                 │              │              │ relationship │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Ray Casting     │ O(n×area)    │ O(1)         │ Cast rays    │
│                 │              │              │ from points  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Pick's Theorem**
- A = I + B/2 - 1 relates area, interior, and boundary points
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **GCD for Boundary Points**
- Number of lattice points on line segment is GCD(dx, dy) + 1
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Mathematical Relationships**
- Use geometric theorems for efficiency
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Lattice Points with Weights
**Problem**: Each lattice point has a weight, find total weight of interior points.

```python
def lattice_points_with_weights(vertices, weight_function):
    interior_points = count_interior_lattice_points(vertices)
    total_weight = 0
    
    # For each interior point, calculate weight
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if point_in_polygon((x, y), vertices):
                total_weight += weight_function(x, y)
    
    return total_weight

def point_in_polygon(point, polygon):
    # Use ray casting algorithm
    n = len(polygon)
    inside = False
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if ((p1[1] > point[1]) != (p2[1] > point[1])) and \
           (point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return inside

# Example usage
def simple_weight(x, y):
    return x + y

result = lattice_points_with_weights(vertices, simple_weight)
print(f"Weighted lattice points: {result}")
```

### Variation 2: Lattice Points with Constraints
**Problem**: Count lattice points subject to certain constraints.

```python
def lattice_points_with_constraints(vertices, constraints):
    interior_points = count_interior_lattice_points(vertices)
    constrained_count = 0
    
    # Check each interior point against constraints
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if point_in_polygon((x, y), vertices):
                if check_constraints(x, y, constraints):
                    constrained_count += 1
    
    return constrained_count

def check_constraints(x, y, constraints):
    # Example constraints: x + y <= max_sum, x >= min_x, y >= min_y
    if x + y <= constraints["max_sum"] and \
       x >= constraints["min_x"] and y >= constraints["min_y"]:
        return True
    return False

# Example usage
constraints = {"max_sum": 5, "min_x": 0, "min_y": 0}
result = lattice_points_with_constraints(vertices, constraints)
print(f"Constrained lattice points: {result}")
```

### Variation 3: Lattice Points with Dynamic Updates
**Problem**: Support adding/removing vertices and counting lattice points.

```python
class DynamicLatticePoints:
    def __init__(self):
        self.vertices = []
    
    def add_vertex(self, x, y):
        self.vertices.append((x, y))
    
    def remove_vertex(self, x, y):
        if (x, y) in self.vertices:
            self.vertices.remove((x, y))
    
    def get_interior_count(self):
        if len(self.vertices) < 3:
            return 0
        return count_interior_lattice_points(self.vertices)
    
    def get_boundary_count(self):
        if len(self.vertices) < 3:
            return 0
        return count_boundary_points(self.vertices)

# Example usage
dynamic_system = DynamicLatticePoints()
dynamic_system.add_vertex(0, 0)
dynamic_system.add_vertex(2, 0)
dynamic_system.add_vertex(1, 2)
interior = dynamic_system.get_interior_count()
boundary = dynamic_system.get_boundary_count()
print(f"Dynamic lattice points - Interior: {interior}, Boundary: {boundary}")
```

### Variation 4: Lattice Points with Range Queries
**Problem**: Answer queries about lattice points in specific ranges.

```python
def lattice_points_range_queries(vertices, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Count lattice points in range that are inside polygon
        count = 0
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if point_in_polygon((x, y), vertices):
                    count += 1
        
        results.append(count)
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (1, 3, 1, 3), (0, 4, 0, 4)]
result = lattice_points_range_queries(vertices, queries)
print(f"Range query results: {result}")
```

### Variation 5: Lattice Points with Convex Hull
**Problem**: Use convex hull to optimize lattice point counting.

```python
def lattice_points_convex_hull(points):
    if len(points) < 3:
        return 0
    
    # Build convex hull
    hull = build_convex_hull(points)
    
    # Count lattice points inside convex hull
    return count_interior_lattice_points(hull)

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
result = lattice_points_convex_hull(points)
print(f"Convex hull lattice points: {result}")
```

## 🔗 Related Problems

- **[Polygon Area](/cses-analyses/problem_soulutions/geometry/)**: Area calculation problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/)**: Point containment problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/)**: Geometric optimization

## 📚 Learning Points

1. **Pick's Theorem**: Essential for lattice point counting
2. **GCD for Boundary**: Important for accurate counting
3. **Mathematical Relationships**: Key for algorithm efficiency
4. **Geometric Optimization**: Important for performance

---

**This is a great introduction to lattice point counting algorithms!** 🎯
- Lattice point counting
- Geometric algorithms
- Computational geometry
- Area-based problems

### **Example Problems**:
- Lattice polygon problems
- Geometric counting
- Computational geometry
- Area calculations

## Notable Techniques

### **Code Patterns**:
```python
# Pick's theorem implementation
def picks_theorem(vertices):
    area = polygon_area(vertices)
    boundary = boundary_points(vertices)
    interior = area - boundary // 2 + 1
    return interior

# Lattice points on line segment
def lattice_points_on_segment(p1, p2):
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])
    return gcd(dx, dy) + 1

# Area calculation with Pick's theorem
def area_from_picks(interior, boundary):
    return interior + boundary // 2 - 1
```

## Problem-Solving Framework

### **1. Understand the Geometry**
- Visualize lattice points
- Understand Pick's theorem
- Consider boundary vs interior points

### **2. Choose the Right Tool**
- Pick's theorem for lattice point counting
- GCD for boundary point counting
- Shoelace formula for area

### **3. Handle Edge Cases**
- Degenerate polygons
- Zero area polygons
- Single point polygons

### **4. Optimize for Precision**
- Use integer arithmetic
- Handle GCD calculations
- Consider numerical stability 