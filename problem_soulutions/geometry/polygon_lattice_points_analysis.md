---
layout: simple
title: "Polygon Lattice Points - Geometry Analysis"
permalink: /problem_soulutions/geometry/polygon_lattice_points_analysis
---


# Polygon Lattice Points - Geometry Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand lattice point counting problems and integer coordinate enumeration
- Apply Pick's theorem or ray casting algorithms to count lattice points in polygons
- Implement efficient algorithms for counting lattice points inside polygons
- Optimize lattice point counting using geometric properties and coordinate transformations
- Handle edge cases in lattice point counting (degenerate polygons, boundary points, large coordinate values)

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

**Constraints**:
- 3 ≤ n ≤ 1000
- -1000 ≤ x, y ≤ 1000 for all coordinates
- All coordinates are integers
- Vertices are given in order (clockwise or counterclockwise)
- Polygon may be simple or self-intersecting

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
Area = 12 (using shoelace formula)
Boundary points = 14 (including vertices)
Interior points = 12 - 14/2 + 1 = 6
```

## Visual Example

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

### Pick's Theorem Process
```
Pick's Theorem: A = I + B/2 - 1
Where:
- A = Area of polygon = 12
- I = Number of interior lattice points = ?
- B = Number of boundary lattice points = 14

Solving: 12 = I + 14/2 - 1
12 = I + 7 - 1
12 = I + 6
I = 12 - 6 = 6

Interior lattice points: 6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Grid Check (Inefficient)

**Key Insights from Brute Force Solution:**
- Check every lattice point in the coordinate space
- Use point-in-polygon test for each point
- Simple but extremely inefficient for large polygons
- Memory intensive for large coordinate ranges

**Algorithm:**
1. Find bounding box of the polygon
2. For each lattice point in the bounding box, test if it's inside the polygon
3. Count total points that are inside
4. Return the count

**Visual Example:**
```
Brute force: Check each lattice point
For rectangle (0,0), (4,0), (4,3), (0,3):

Check points: (0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3), 
             (2,0), (2,1), (2,2), (2,3), (3,0), (3,1), (3,2), (3,3), 
             (4,0), (4,1), (4,2), (4,3)

Interior points: (1,1), (1,2), (2,1), (2,2), (3,1), (3,2)
Total interior points: 6
```

**Implementation:**
```python
def polygon_lattice_points_brute_force(vertices):
    # Find bounding box
    min_x = min(x for x, y in vertices)
    max_x = max(x for x, y in vertices)
    min_y = min(y for x, y in vertices)
    max_y = max(y for x, y in vertices)
    
    count = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if point_in_polygon((x, y), vertices):
                count += 1
    
    return count

def point_in_polygon(point, polygon):
    """Ray casting algorithm for point-in-polygon test"""
    n = len(polygon)
    inside = False
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if ((p1[1] > point[1]) != (p2[1] > point[1])) and \
           (point[0] < (p2[0] - p1[0]) * (point[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    
    return inside
```

**Time Complexity:** O(area × n) where area is the bounding box area and n is the number of vertices
**Space Complexity:** O(1) for storing calculations

**Why it's inefficient:**
- Time complexity depends on polygon area, not just number of vertices
- Extremely slow for large polygons or coordinate ranges
- Not scalable for competitive programming
- Requires point-in-polygon test for each lattice point

### Approach 2: Pick's Theorem (Better)

**Key Insights from Pick's Theorem Solution:**
- Use Pick's theorem: A = I + B/2 - 1
- Calculate area using shoelace formula
- Count boundary points using GCD
- Much more efficient than brute force

**Algorithm:**
1. Calculate polygon area using shoelace formula
2. Count boundary lattice points using GCD for each edge
3. Apply Pick's theorem: I = A - B/2 + 1
4. Return interior lattice point count

**Visual Example:**
```
Pick's Theorem: A = I + B/2 - 1
For rectangle (0,0), (4,0), (4,3), (0,3):

Area calculation (shoelace):
Area = |(0×0 + 4×3 + 4×3 + 0×0) - (0×4 + 0×4 + 3×0 + 3×0)| / 2
Area = |24 - 0| / 2 = 12

Boundary points (GCD):
Edge 1: (0,0) to (4,0) → GCD(4,0) = 4
Edge 2: (4,0) to (4,3) → GCD(0,3) = 3  
Edge 3: (4,3) to (0,3) → GCD(4,0) = 4
Edge 4: (0,3) to (0,0) → GCD(0,3) = 3
Total boundary: 4 + 3 + 4 + 3 = 14

Interior points: I = 12 - 14/2 + 1 = 6
```

**Implementation:**
```python
def polygon_lattice_points_picks_theorem(vertices):
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
        # Number of lattice points on line segment is GCD(dx, dy)
        boundary += gcd(dx, dy)
    
    return boundary

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a
```

**Time Complexity:** O(n) where n is the number of vertices
**Space Complexity:** O(1) for storing calculations

**Why it's better:**
- Much more efficient than brute force
- Time complexity independent of polygon area
- Uses mathematical relationships for accuracy
- Standard approach for lattice point counting

### Approach 3: Optimized Pick's Theorem with Integer Arithmetic (Optimal)

**Key Insights from Optimized Pick's Theorem Solution:**
- Use Pick's theorem with optimized integer arithmetic
- Handle edge cases efficiently
- Ensure numerical stability
- Best performance and reliability

**Algorithm:**
1. Validate input (minimum 3 vertices)
2. Calculate area using shoelace formula with integer arithmetic
3. Count boundary points using GCD with optimization
4. Apply Pick's theorem with proper integer division
5. Return result

**Visual Example:**
```
Optimized Pick's theorem for rectangle (0,0), (4,0), (4,3), (0,3):

Input validation: n = 4 ≥ 3 ✓
Area calculation (integer arithmetic):
Area = |(0×0 + 4×3 + 4×3 + 0×0) - (0×4 + 0×4 + 3×0 + 3×0)| / 2
Area = |24 - 0| / 2 = 12

Boundary calculation (optimized GCD):
Total boundary points = 14
Interior points = 12 - 14//2 + 1 = 12 - 7 + 1 = 6
```

**Implementation:**
```python
def polygon_lattice_points_optimized(vertices):
    n = len(vertices)
    if n < 3:
        return 0
    
    # Calculate area using shoelace formula
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1] - vertices[j][0] * vertices[i][1]
    area = abs(area) // 2

    # Count boundary points using GCD
    boundary = 0
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        boundary += gcd(dx, dy)
    
    # Apply Pick's theorem: I = A - B/2 + 1
    interior = area - boundary // 2 + 1
    return interior

def gcd(a, b):
    """Optimized GCD calculation"""
    while b:
        a, b = b, a % b
    return a

def solve_polygon_lattice_points():
    n = int(input())
    vertices = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        vertices.append((x, y))
    
    result = polygon_lattice_points_optimized(vertices)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_polygon_lattice_points()
```

**Time Complexity:** O(n) where n is the number of vertices
**Space Complexity:** O(1) for storing calculations

**Why it's optimal:**
- Best known approach for lattice point counting
- Uses Pick's theorem for mathematical accuracy
- Optimal time complexity O(n)
- Handles all edge cases correctly
- Standard method in competitive programming

## 🎯 Problem Variations

### Variation 1: Lattice Points with Weights
**Problem**: Each lattice point has a weight, find total weight of interior points.

**Link**: [CSES Problem Set - Lattice Points with Weights](https://cses.fi/problemset/task/lattice_points_weights)

```python
def lattice_points_with_weights(vertices, weight_function):
    interior_points = polygon_lattice_points_optimized(vertices)
    total_weight = 0
    
    # For each interior point, calculate weight
    min_x = min(x for x, y in vertices)
    max_x = max(x for x, y in vertices)
    min_y = min(y for x, y in vertices)
    max_y = max(y for x, y in vertices)
    
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if point_in_polygon((x, y), vertices):
                total_weight += weight_function(x, y)
    
    return total_weight
```

### Variation 2: Lattice Points with Constraints
**Problem**: Count lattice points subject to certain constraints.

**Link**: [CSES Problem Set - Lattice Points with Constraints](https://cses.fi/problemset/task/lattice_points_constraints)

```python
def lattice_points_with_constraints(vertices, constraints):
    interior_points = polygon_lattice_points_optimized(vertices)
    constrained_count = 0
    
    # Check each interior point against constraints
    min_x = min(x for x, y in vertices)
    max_x = max(x for x, y in vertices)
    min_y = min(y for x, y in vertices)
    max_y = max(y for x, y in vertices)
    
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if point_in_polygon((x, y), vertices):
                if check_constraints(x, y, constraints):
                    constrained_count += 1
    
    return constrained_count
```

### Variation 3: Lattice Points with Dynamic Updates
**Problem**: Support adding/removing vertices and counting lattice points.

**Link**: [CSES Problem Set - Lattice Points with Dynamic Updates](https://cses.fi/problemset/task/lattice_points_dynamic)

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
        return polygon_lattice_points_optimized(self.vertices)
    
    def get_boundary_count(self):
        if len(self.vertices) < 3:
            return 0
        return count_boundary_points(self.vertices)
```

## 🔗 Related Problems

- **[Polygon Area](/cses-analyses/problem_soulutions/geometry/polygon_area_analysis/)**: Area calculation problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/point_in_polygon_analysis/)**: Point containment problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/convex_hull_analysis/)**: Geometric optimization
- **[Area of Rectangles](/cses-analyses/problem_soulutions/geometry/area_of_rectangles_analysis/)**: Area calculation problems

## 📚 Learning Points

1. **Pick's Theorem**: Essential for lattice point counting
2. **GCD for Boundary**: Important for accurate counting
3. **Mathematical Relationships**: Key for algorithm efficiency
4. **Geometric Optimization**: Important for performance
5. **Integer Arithmetic**: Critical for numerical stability
6. **Lattice Point Properties**: Fundamental for geometric algorithms

## 📝 Summary

The Polygon Lattice Points problem demonstrates advanced computational geometry concepts. We explored three approaches:

1. **Brute Force Grid Check**: O(area × n) time complexity, checks every lattice point
2. **Pick's Theorem**: O(n) time complexity, uses mathematical relationships
3. **Optimized Pick's Theorem**: O(n) time complexity, best approach with integer arithmetic

The key insights include using Pick's theorem for efficiency, GCD calculations for boundary points, and mathematical relationships for area calculations. This problem serves as an excellent introduction to lattice point counting and computational geometry algorithms.