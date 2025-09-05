---
layout: simple
title: "Lines and Queries II Analysis"
permalink: /problem_soulutions/geometry/lines_and_queries_ii_analysis
---


# Lines and Queries II Analysis

## Problem Description

**Problem**: Given a set of lines in 2D space and multiple queries, for each query determine how many lines intersect with a given line segment.

**Input**: 
- n: number of lines
- n lines: ax + by + c = 0 (coefficients a, b, c)
- q: number of queries
- q queries: x1 y1 x2 y2 (line segment endpoints)

**Output**: For each query, print the number of lines that intersect with the given line segment.

**Example**:
```
Input:
3
1 0 -2    # x = 2
0 1 -3    # y = 3
1 1 -5    # x + y = 5
2
0 0 4 4   # Line segment from (0,0) to (4,4)
1 1 3 3   # Line segment from (1,1) to (3,3)

Output:
2
1

Explanation: 
Query 1: Line segment (0,0) to (4,4) intersects with x=2 and x+y=5
Query 2: Line segment (1,1) to (3,3) intersects with x+y=5 only
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find intersections between line segments and lines
- Use geometric intersection algorithms
- Handle multiple queries efficiently
- Apply line-line intersection formulas

**Key Observations:**
- Need to check if line segment intersects with each line
- Line-line intersection can be computed algebraically
- Line segment intersection requires additional checks
- Can optimize with spatial data structures

### Step 2: Line-Line Intersection Approach
**Idea**: For each query, check intersection with each line using algebraic formulas.

```python
def lines_and_queries_ii_intersection(n, lines, queries):
    def line_segment_intersection(line, x1, y1, x2, y2):
        a, b, c = line
        
        # Check if line segment intersects with line ax + by + c = 0
        # Line segment: parametric form (x1 + t*(x2-x1), y1 + t*(y2-y1))
        # Substitute into line equation and solve for t
        
        dx = x2 - x1
        dy = y2 - y1
        
        # Denominator: a*dx + b*dy
        denom = a * dx + b * dy
        
        if abs(denom) < 1e-9:  # Lines are parallel
            # Check if line segment lies on the line
            return abs(a * x1 + b * y1 + c) < 1e-9
        
        # Parameter t where intersection occurs
        t = -(a * x1 + b * y1 + c) / denom
        
        # Check if intersection point lies on line segment
        return 0 <= t <= 1
    
    results = []
    for x1, y1, x2, y2 in queries:
        count = 0
        for line in lines:
            if line_segment_intersection(line, x1, y1, x2, y2):
                count += 1
        results.append(count)
    
    return results
```

**Why this works:**
- Uses parametric line representation
- Handles parallel lines correctly
- Checks intersection point bounds
- O(n*q) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_lines_and_queries_ii():
    n = int(input())
    lines = []
    
    for _ in range(n):
        a, b, c = map(int, input().split())
        lines.append((a, b, c))
    
    q = int(input())
    queries = []
    
    for _ in range(q):
        x1, y1, x2, y2 = map(int, input().split())
        queries.append((x1, y1, x2, y2))
    
    # Process each query
    for x1, y1, x2, y2 in queries:
        count = count_intersections(lines, x1, y1, x2, y2)
        print(count)

def count_intersections(lines, x1, y1, x2, y2):
    count = 0
    
    for a, b, c in lines:
        if line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
            count += 1
    
    return count

def line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    # Denominator: a*dx + b*dy
    denom = a * dx + b * dy
    
    if abs(denom) < 1e-9:  # Lines are parallel
        # Check if line segment lies on the line
        return abs(a * x1 + b * y1 + c) < 1e-9
    
    # Parameter t where intersection occurs
    t = -(a * x1 + b * y1 + c) / denom
    
    # Check if intersection point lies on line segment
    return 0 <= t <= 1

# Main execution
if __name__ == "__main__":
    solve_lines_and_queries_ii()
```

**Why this works:**
- Optimal geometric intersection approach
- Handles all edge cases correctly
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (3, [(1, 0, -2), (0, 1, -3), (1, 1, -5)], 
         [(0, 0, 4, 4), (1, 1, 3, 3)], [2, 1]),
        (2, [(1, 0, 0), (0, 1, 0)], 
         [(0, 0, 2, 2), (1, 0, 1, 2)], [2, 1]),
    ]
    
    for n, lines, queries, expected in test_cases:
        result = solve_test(n, lines, queries)
        print(f"n={n}, lines={lines}, queries={queries}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, lines, queries):
    results = []
    for x1, y1, x2, y2 in queries:
        count = count_intersections(lines, x1, y1, x2, y2)
        results.append(count)
    return results

def count_intersections(lines, x1, y1, x2, y2):
    count = 0
    
    for a, b, c in lines:
        if line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
            count += 1
    
    return count

def line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    denom = a * dx + b * dy
    
    if abs(denom) < 1e-9:
        return abs(a * x1 + b * y1 + c) < 1e-9
    
    t = -(a * x1 + b * y1 + c) / denom
    return 0 <= t <= 1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n*q) - check each line for each query
- **Space**: O(1) - constant space per query

### Why This Solution Works
- **Parametric Line Representation**: Efficient intersection calculation
- **Parallel Line Handling**: Special case for parallel lines
- **Boundary Checking**: Ensures intersection lies on segment
- **Numerical Stability**: Handles floating-point precision

## 🎨 Visual Example

### Input Example
```
3 lines:
1. x = 2 (1x + 0y - 2 = 0)
2. y = 3 (0x + 1y - 3 = 0)
3. x + y = 5 (1x + 1y - 5 = 0)

2 queries:
1. Line segment (0,0) to (4,4)
2. Line segment (1,1) to (3,3)
```

### Lines and Segments Visualization
```
Y
5 |     |   \
4 |     |     \   *
3 | ----+-------\----
2 |     |         \ *
1 |     |           \*
0 |     |             \
  +-----+-----+-----+-----+
    0   1   2   3   4   5  X

Line 1: x = 2 (vertical)
Line 2: y = 3 (horizontal)
Line 3: x + y = 5 (diagonal)
Segment 1: (0,0) to (4,4)
Segment 2: (1,1) to (3,3)
```

### Intersection Analysis
```
Query 1: Line segment (0,0) to (4,4)

Intersection with Line 1 (x = 2):
- Parametric form: (0,0) + t(4,4) = (4t, 4t)
- At x = 2: 4t = 2, so t = 0.5
- Intersection point: (2, 2)
- Check bounds: 0 ≤ 0.5 ≤ 1 ✓
- Intersection exists

Intersection with Line 2 (y = 3):
- At y = 3: 4t = 3, so t = 0.75
- Intersection point: (3, 3)
- Check bounds: 0 ≤ 0.75 ≤ 1 ✓
- Intersection exists

Intersection with Line 3 (x + y = 5):
- At x + y = 5: 4t + 4t = 8t = 5, so t = 0.625
- Intersection point: (2.5, 2.5)
- Check bounds: 0 ≤ 0.625 ≤ 1 ✓
- Intersection exists

Total intersections: 3
```

### Parametric Line Representation
```
Line segment from (x1, y1) to (x2, y2):
x = x1 + t(x2 - x1)
y = y1 + t(y2 - y1)
where 0 ≤ t ≤ 1

For segment (0,0) to (4,4):
x = 0 + t(4 - 0) = 4t
y = 0 + t(4 - 0) = 4t
```

### Intersection Calculation
```
For line ax + by + c = 0 and segment (x1,y1) to (x2,y2):

Substitute parametric form:
a(x1 + t(x2-x1)) + b(y1 + t(y2-y1)) + c = 0
a(x1 + t·dx) + b(y1 + t·dy) + c = 0
ax1 + a·t·dx + by1 + b·t·dy + c = 0
t(a·dx + b·dy) + (ax1 + by1 + c) = 0

Solve for t:
t = -(ax1 + by1 + c) / (a·dx + b·dy)

Check if 0 ≤ t ≤ 1 for intersection
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n×q)       │ O(1)         │ Check all    │
│                 │              │              │ lines        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Parametric      │ O(n×q)       │ O(1)         │ Use          │
│ Form            │              │              │ parametric   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Spatial Index   │ O(log n×q)   │ O(n)         │ Use spatial  │
│                 │              │              │ data structure│
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Line-Line Intersection**
- Use parametric form for efficiency
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Geometric Algorithms**
- Handle parallel lines correctly
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Numerical Precision**
- Use epsilon for floating-point comparisons
- Important for understanding
- Fundamental concept
- Essential for accuracy

## 🎯 Problem Variations

### Variation 1: Lines with Different Types
**Problem**: Handle different line types (vertical, horizontal, diagonal).

```python
def lines_and_queries_with_types(n, lines, queries):
    def classify_line(a, b):
        if abs(a) < 1e-9:
            return "horizontal"  # y = constant
        elif abs(b) < 1e-9:
            return "vertical"    # x = constant
        else:
            return "diagonal"
    
    def optimized_intersection(line_type, a, b, c, x1, y1, x2, y2):
        if line_type == "vertical":
            # x = -c/a, check if x1 <= -c/a <= x2
            x_intersect = -c / a
            return min(x1, x2) <= x_intersect <= max(x1, x2)
        elif line_type == "horizontal":
            # y = -c/b, check if y1 <= -c/b <= y2
            y_intersect = -c / b
            return min(y1, y2) <= y_intersect <= max(y1, y2)
        else:
            # Use general intersection method
            return line_segment_intersects_line(a, b, c, x1, y1, x2, y2)
    
    # Classify all lines
    line_types = [classify_line(a, b) for a, b, _ in lines]
    
    results = []
    for x1, y1, x2, y2 in queries:
        count = 0
        for i, (a, b, c) in enumerate(lines):
            if optimized_intersection(line_types[i], a, b, c, x1, y1, x2, y2):
                count += 1
        results.append(count)
    
    return results

# Example usage
lines = [(1, 0, -2), (0, 1, -3), (1, 1, -5)]
queries = [(0, 0, 4, 4), (1, 1, 3, 3)]
result = lines_and_queries_with_types(3, lines, queries)
print(f"Intersection counts: {result}")
```

### Variation 2: Lines with Weights
**Problem**: Each line has a weight, find total weight of intersecting lines.

```python
def lines_and_queries_with_weights(n, lines_with_weights, queries):
    results = []
    
    for x1, y1, x2, y2 in queries:
        total_weight = 0
        for (a, b, c), weight in lines_with_weights:
            if line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
                total_weight += weight
        results.append(total_weight)
    
    return results

# Example usage
lines_with_weights = [((1, 0, -2), 3), ((0, 1, -3), 2), ((1, 1, -5), 1)]
result = lines_and_queries_with_weights(3, lines_with_weights, queries)
print(f"Weighted intersections: {result}")
```

### Variation 3: Lines with Constraints
**Problem**: Only count intersections within certain constraints.

```python
def lines_and_queries_with_constraints(n, lines, queries, constraints):
    def check_constraints(x, y, constraint):
        if constraint["min_x"] <= x <= constraint["max_x"] and \
           constraint["min_y"] <= y <= constraint["max_y"]:
            return True
        return False
    
    results = []
    for x1, y1, x2, y2 in queries:
        count = 0
        for a, b, c in lines:
            if line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
                # Find intersection point
                dx = x2 - x1
                dy = y2 - y1
                denom = a * dx + b * dy
                t = -(a * x1 + b * y1 + c) / denom
                ix = x1 + t * dx
                iy = y1 + t * dy
                
                if check_constraints(ix, iy, constraints):
                    count += 1
        results.append(count)
    
    return results

# Example usage
constraints = {"min_x": 0, "max_x": 5, "min_y": 0, "max_y": 5}
result = lines_and_queries_with_constraints(3, lines, queries, constraints)
print(f"Constrained intersections: {result}")
```

### Variation 4: Lines with Dynamic Updates
**Problem**: Support adding/removing lines and answering queries.

```python
class DynamicLinesAndQueries:
    def __init__(self):
        self.lines = []
    
    def add_line(self, a, b, c):
        self.lines.append((a, b, c))
    
    def remove_line(self, a, b, c):
        if (a, b, c) in self.lines:
            self.lines.remove((a, b, c))
    
    def query(self, x1, y1, x2, y2):
        count = 0
        for a, b, c in self.lines:
            if line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
                count += 1
        return count

# Example usage
dynamic_system = DynamicLinesAndQueries()
dynamic_system.add_line(1, 0, -2)
dynamic_system.add_line(0, 1, -3)
result = dynamic_system.query(0, 0, 4, 4)
print(f"Dynamic query result: {result}")
```

### Variation 5: Lines with Spatial Indexing
**Problem**: Use spatial data structures for efficient queries.

```python
def lines_and_queries_with_spatial_index(n, lines, queries):
    # Simple spatial indexing: group lines by bounding box
    from collections import defaultdict
    
    def get_line_bounds(a, b, c):
        # Approximate bounds for line ax + by + c = 0
        if abs(a) < 1e-9:  # horizontal line
            return (float('-inf'), float('inf'), -c/b, -c/b)
        elif abs(b) < 1e-9:  # vertical line
            return (-c/a, -c/a, float('-inf'), float('inf'))
        else:  # diagonal line
            # Use some reasonable bounds
            return (-1000, 1000, -1000, 1000)
    
    # Group lines by spatial regions
    spatial_groups = defaultdict(list)
    for i, line in enumerate(lines):
        bounds = get_line_bounds(*line)
        # Simple hashing based on bounds
        key = (bounds[0] // 100, bounds[2] // 100)
        spatial_groups[key].append(i)
    
    results = []
    for x1, y1, x2, y2 in queries:
        count = 0
        # Check relevant spatial groups
        relevant_groups = set()
        for x in range(int(x1//100), int(x2//100) + 1):
            for y in range(int(y1//100), int(y2//100) + 1):
                relevant_groups.add((x, y))
        
        for group_key in relevant_groups:
            for line_idx in spatial_groups[group_key]:
                a, b, c = lines[line_idx]
                if line_segment_intersects_line(a, b, c, x1, y1, x2, y2):
                    count += 1
        
        results.append(count)
    
    return results

# Example usage
result = lines_and_queries_with_spatial_index(3, lines, queries)
print(f"Spatially indexed result: {result}")
```

## 🔗 Related Problems

- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/)**: Similar intersection problems
- **[Geometric Algorithms](/cses-analyses/problem_soulutions/geometry/)**: Other geometric problems
- **[Computational Geometry](/cses-analyses/problem_soulutions/geometry/)**: Advanced geometric algorithms

## 📚 Learning Points

1. **Line-Line Intersection**: Essential for geometric algorithms
2. **Parametric Line Representation**: Important for efficient calculations
3. **Numerical Stability**: Key for accurate geometric computations
4. **Spatial Data Structures**: Important for optimization

---

**This is a great introduction to geometric intersection algorithms!** 🎯
