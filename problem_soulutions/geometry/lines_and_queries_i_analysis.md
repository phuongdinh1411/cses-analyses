---
layout: simple
title: "Lines and Queries I Analysis"
permalink: /problem_soulutions/geometry/lines_and_queries_i_analysis
---


# Lines and Queries I Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand line-point relationship queries and geometric containment testing
- Apply line equation evaluation and point-line distance calculations for query processing
- Implement efficient algorithms for processing multiple point-line relationship queries
- Optimize query processing using geometric properties and coordinate transformations
- Handle edge cases in line-point queries (precision issues, degenerate lines, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Line equations, point-line relationships, geometric queries, query processing
- **Data Structures**: Line structures, point structures, query data structures, geometric data structures
- **Mathematical Concepts**: Line equations, point-line distance, coordinate geometry, geometric relationships
- **Programming Skills**: Line equation evaluation, point manipulation, query processing, geometric computations
- **Related Problems**: Point in Polygon (geometric queries), Line Segment Intersection (line geometry), Point Location Test (point-line relationships)

## Problem Description

**Problem**: Given a set of lines in 2D space and multiple queries, for each query determine if a given point lies on any of the lines.

**Input**: 
- n: number of lines
- n lines: ax + by + c = 0 (coefficients a, b, c)
- q: number of queries
- q queries: x y (point coordinates)

**Output**: For each query, print "YES" if the point lies on any line, "NO" otherwise.

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ q ≤ 1000
- -1000 ≤ a, b, c, x, y ≤ 1000 for all coefficients and coordinates
- All values are integers
- Lines are given in general form: ax + by + c = 0
- At least one of a or b is non-zero for each line

**Example**:
```
Input:
3
1 0 -2    # x = 2
0 1 -3    # y = 3
1 1 -5    # x + y = 5
2
2 3       # Point (2,3)
4 1       # Point (4,1)

Output:
YES
NO

Explanation: 
Query 1: Point (2,3) lies on line x=2 (satisfies 1*2 + 0*3 - 2 = 0)
Query 2: Point (4,1) doesn't lie on any line
```

## Visual Example

### Lines Visualization
```
Y
5 |     |   \
4 |     |     \
3 | ----+-------\----
2 |     |         \
1 |     |           \
0 |     |             \
  +-----+-----+-----+-----+
    0   1   2   3   4   5  X

Line 1: x = 2 (vertical)
Line 2: y = 3 (horizontal)
Line 3: x + y = 5 (diagonal)
```

### Query Point Testing
```
Y
5 |     |   \
4 |     |     \
3 | ----+-------\----
2 |     |         \
1 |     |           \
0 |     |             \
  +-----+-----+-----+-----+
    0   1   2   3   4   5  X

Query 1: Point (2,3) - lies on line x=2 → YES
Query 2: Point (4,1) - doesn't lie on any line → NO
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Check (Inefficient)

**Key Insights from Brute Force Solution:**
- Check each point against every line
- Use line equation evaluation for each pair
- No early termination or optimization
- Simple but inefficient for large inputs

**Algorithm:**
1. For each query point (x, y):
   - For each line (a, b, c):
     - Check if ax + by + c = 0
     - If yes, return "YES"
2. If no line contains the point, return "NO"

**Visual Example:**
```
Y
5 |     |   \
4 |     |     \
3 | ----+-------\----
2 |     |         \
1 |     |           \
0 |     |             \
  +-----+-----+-----+-----+
    0   1   2   3   4   5  X

Brute force checks:
Point (2,3): Check all 3 lines → Line 1: 1*2 + 0*3 - 2 = 0 ✓
Point (4,1): Check all 3 lines → No match ✗
```

**Implementation:**
```python
def lines_and_queries_brute_force(n, lines, queries):
    results = []
    
    for x, y in queries:
        found = False
        
        # Check each line
        for a, b, c in lines:
            if a * x + b * y + c == 0:
                found = True
                break
        
        results.append("YES" if found else "NO")
    
    return results
```

**Time Complexity:** O(n*q) where n is lines, q is queries
**Space Complexity:** O(1) for storing results

**Why it's inefficient:**
- No early termination when point is found on a line
- Checks all lines even after finding a match
- No optimization for repeated queries
- Simple but not optimal for large inputs

### Approach 2: Early Termination (Better)

**Key Insights from Early Termination Solution:**
- Stop checking lines as soon as a match is found
- Use floating-point comparison with epsilon
- Handle numerical precision issues
- More efficient than brute force

**Algorithm:**
1. For each query point (x, y):
   - For each line (a, b, c):
     - Check if |ax + by + c| < epsilon
     - If yes, return "YES" immediately
2. If no line contains the point, return "NO"

**Visual Example:**
```
Y
5 |     |   \
4 |     |     \
3 | ----+-------\----
2 |     |         \
1 |     |           \
0 |     |             \
  +-----+-----+-----+-----+
    0   1   2   3   4   5  X

Early termination:
Point (2,3): Check Line 1 → Match found → Return "YES" immediately
Point (4,1): Check all 3 lines → No match → Return "NO"
```

**Implementation:**
```python
def lines_and_queries_early_termination(n, lines, queries):
    epsilon = 1e-9
    results = []
    
    for x, y in queries:
        found = False
        
        # Check each line with early termination
        for a, b, c in lines:
            if abs(a * x + b * y + c) < epsilon:
                found = True
                break  # Early termination
        
        results.append("YES" if found else "NO")
    
    return results
```

**Time Complexity:** O(n*q) worst case, O(k*q) average case where k is average lines checked
**Space Complexity:** O(1) for storing results

**Why it's better:**
- Early termination reduces average case complexity
- Handles floating-point precision with epsilon
- More efficient than brute force
- Still simple to implement

### Approach 3: Optimized with Integer Arithmetic (Optimal)

**Key Insights from Optimized Solution:**
- Use integer arithmetic when possible to avoid precision issues
- Optimize line equation evaluation
- Handle edge cases efficiently
- Best performance for this problem type

**Algorithm:**
1. For each query point (x, y):
   - For each line (a, b, c):
     - Evaluate ax + by + c using integer arithmetic
     - If result equals 0, return "YES" immediately
2. If no line contains the point, return "NO"

**Visual Example:**
```
Y
5 |     |   \
4 |     |     \
3 | ----+-------\----
2 |     |         \
1 |     |           \
0 |     |             \
  +-----+-----+-----+-----+
    0   1   2   3   4   5  X

Optimized approach:
Point (2,3): Line 1: 1*2 + 0*3 - 2 = 0 (integer arithmetic)
Point (4,1): All lines checked with integer precision
```

**Implementation:**
```python
def lines_and_queries_optimized(n, lines, queries):
    results = []
    
    for x, y in queries:
        found = False
        
        # Check each line with optimized evaluation
        for a, b, c in lines:
            # Use integer arithmetic when possible
            result = a * x + b * y + c
            if result == 0:
                found = True
                break
        
        results.append("YES" if found else "NO")
    
    return results

def solve_lines_and_queries_i():
    n = int(input())
    lines = []
    
    for _ in range(n):
        a, b, c = map(int, input().split())
        lines.append((a, b, c))
    
    q = int(input())
    
    for _ in range(q):
        x, y = map(int, input().split())
        result = check_point_on_lines(lines, x, y)
        print(result)

def check_point_on_lines(lines, x, y):
    for a, b, c in lines:
        if a * x + b * y + c == 0:
            return "YES"
    return "NO"
```

**Time Complexity:** O(n*q) worst case, O(k*q) average case where k is average lines checked
**Space Complexity:** O(1) for storing results

**Why it's optimal:**
- Uses integer arithmetic for exact precision
- Early termination for efficiency
- Handles all edge cases correctly
- Best known approach for this problem type
- Simple and robust implementation

## 🎯 Problem Variations

### Variation 1: Lines with Tolerance
**Problem**: Check if points lie within a certain distance of any line.

**Link**: [CSES Problem Set - Lines and Queries with Tolerance](https://cses.fi/problemset/task/lines_and_queries_tolerance)

```python
def lines_and_queries_with_tolerance(n, lines, queries, tolerance):
    def point_near_line(point, line, tol):
        x, y = point
        a, b, c = line
        
        # Calculate distance from point to line
        distance = abs(a * x + b * y + c) / (a**2 + b**2)**0.5
        return distance <= tol
    
    results = []
    for x, y in queries:
        point = (x, y)
        found = False
        
        for line in lines:
            if point_near_line(point, line, tolerance):
                found = True
                break
        
        results.append("YES" if found else "NO")
    
    return results
```

### Variation 2: Lines with Weights
**Problem**: Each line has a weight, find total weight of lines containing the point.

**Link**: [CSES Problem Set - Lines and Queries with Weights](https://cses.fi/problemset/task/lines_and_queries_weights)

```python
def lines_and_queries_with_weights(n, lines_with_weights, queries):
    results = []
    
    for x, y in queries:
        total_weight = 0
        for (a, b, c), weight in lines_with_weights:
            if a * x + b * y + c == 0:
                total_weight += weight
        results.append(total_weight)
    
    return results
```

### Variation 3: Lines with Dynamic Updates
**Problem**: Support adding/removing lines and answering queries.

**Link**: [CSES Problem Set - Lines and Queries with Dynamic Updates](https://cses.fi/problemset/task/lines_and_queries_dynamic)

```python
class DynamicLinesAndQueries:
    def __init__(self):
        self.lines = []
    
    def add_line(self, a, b, c):
        self.lines.append((a, b, c))
    
    def remove_line(self, a, b, c):
        if (a, b, c) in self.lines:
            self.lines.remove((a, b, c))
    
    def query(self, x, y):
        for a, b, c in self.lines:
            if a * x + b * y + c == 0:
                return "YES"
        return "NO"
```

## 🔗 Related Problems

- **[Lines and Queries II](/cses-analyses/problem_soulutions/geometry/lines_and_queries_ii_analysis/)**: Advanced line query problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/point_in_polygon_analysis/)**: Point containment problems
- **[Point Location Test](/cses-analyses/problem_soulutions/geometry/point_location_test_analysis/)**: Point-line relationships
- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/line_segment_intersection_analysis/)**: Line geometry problems

## 📚 Learning Points

1. **Point-Line Equations**: Essential for geometric algorithms
2. **Numerical Stability**: Important for accurate computations
3. **Early Termination**: Key for efficient algorithms
4. **Integer Arithmetic**: Useful for avoiding precision issues
5. **Query Processing**: Important for handling multiple queries
6. **Geometric Relationships**: Fundamental for spatial algorithms

## 📝 Summary

The Lines and Queries I problem demonstrates fundamental computational geometry concepts. We explored three approaches:

1. **Brute Force Check**: O(n*q) time complexity, checks all lines for each query
2. **Early Termination**: O(n*q) worst case, O(k*q) average case, stops when match is found
3. **Optimized with Integer Arithmetic**: O(n*q) worst case, O(k*q) average case, uses exact precision

The key insights include using line equations for point-line relationships, early termination for efficiency, and integer arithmetic for precision. This problem serves as an excellent introduction to geometric query processing and spatial algorithms.

