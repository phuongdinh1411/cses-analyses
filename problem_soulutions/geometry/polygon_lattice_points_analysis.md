# Polygon Lattice Points - CSES Geometry Analysis

## Problem Description
Count the number of lattice points (integer coordinates) inside a polygon.

## Solution Progression

### 1. **Brute Force Approach**
**Description**: Check each lattice point to see if it's inside the polygon.

**Why this is inefficient**: 
- O(area) time complexity
- Too slow for large polygons
- Inefficient for practical use

**Why this improvement works**:
- Use Pick's theorem for efficient calculation
- Relates area, boundary points, and interior points
- Much faster than brute force

### 2. **Optimal Solution**
**Description**: Use Pick's theorem: A = I + B/2 - 1, where A is area, I is interior points, B is boundary points.

**Key Insights**:
- Pick's theorem gives exact relationship
- Calculate area using shoelace formula
- Count boundary points using GCD
- Solve for interior points

## Complete Implementation

```python
import math

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

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
        boundary += gcd(dx, dy)
    
    return boundary

def interior_points(vertices):
    """Count interior lattice points using Pick's theorem"""
    area = polygon_area(vertices)
    boundary = boundary_points(vertices)
    interior = area - boundary // 2 + 1
    return interior

# Read input
n = int(input())
vertices = []
for _ in range(n):
    x, y = map(int, input().split())
    vertices.append((x, y))

result = interior_points(vertices)
print(result)
```

## Complexity Analysis
- **Time Complexity**: O(n) where n is number of vertices
- **Space Complexity**: O(1) additional space

## Key Insights for Other Problems

### **Principles**:
1. **Pick's Theorem**: A = I + B/2 - 1 relates area, interior, and boundary points
2. **GCD for Boundary**: Number of lattice points on line segment is GCD(dx, dy) + 1
3. **Shoelace Formula**: Calculate polygon area efficiently

### **Applicability**:
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