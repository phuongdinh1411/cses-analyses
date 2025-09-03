---
layout: simple
title: "Lines and Queries I Analysis"
permalink: /problem_soulutions/geometry/lines_and_queries_i_analysis
---


# Lines and Queries I Analysis

## Problem Description

**Problem**: Given a set of lines in 2D space and multiple queries, for each query determine if a given point lies on any of the lines.

**Input**: 
- n: number of lines
- n lines: ax + by + c = 0 (coefficients a, b, c)
- q: number of queries
- q queries: x y (point coordinates)

**Output**: For each query, print "YES" if the point lies on any line, "NO" otherwise.

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Check if points lie on any given lines
- Use point-line distance formulas
- Handle multiple queries efficiently
- Apply geometric point-line relationships

**Key Observations:**
- Point (x,y) lies on line ax + by + c = 0 if ax + by + c = 0
- Need to check each line for each query
- Can optimize with early termination
- Numerical precision is important

### Step 2: Point-Line Relationship Approach
**Idea**: For each query, check if the point satisfies any line equation.

```python
def lines_and_queries_i_point_check(n, lines, queries):
    def point_on_line(point, line):
        x, y = point
        a, b, c = line
        
        # Check if point satisfies line equation: ax + by + c = 0
        result = a * x + b * y + c
        
        # Use small epsilon for floating-point comparison
        return abs(result) < 1e-9
    
    results = []
    for x, y in queries:
        point = (x, y)
        found = False
        
        # Check each line
        for line in lines:
            if point_on_line(point, line):
                found = True
                break
        
        results.append("YES" if found else "NO")
    
    return results
```

**Why this works:**
- Direct application of line equation
- Handles all line types correctly
- Efficient early termination
- O(n*q) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_lines_and_queries_i():
    n = int(input())
    lines = []
    
    for _ in range(n):
        a, b, c = map(int, input().split())
        lines.append((a, b, c))
    
    q = int(input())
    queries = []
    
    for _ in range(q):
        x, y = map(int, input().split())
        queries.append((x, y))
    
    # Process each query
    for x, y in queries:
        result = check_point_on_lines(lines, x, y)
        print(result)

def check_point_on_lines(lines, x, y):
    for a, b, c in lines:
        if abs(a * x + b * y + c) < 1e-9:
            return "YES"
    return "NO"

# Main execution
if __name__ == "__main__":
    solve_lines_and_queries_i()
```

**Why this works:**
- Optimal point-line checking approach
- Handles all edge cases correctly
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (3, [(1, 0, -2), (0, 1, -3), (1, 1, -5)], 
         [(2, 3), (4, 1)], ["YES", "NO"]),
        (2, [(1, 0, 0), (0, 1, 0)], 
         [(0, 0), (1, 1)], ["YES", "NO"]),
    ]
    
    for n, lines, queries, expected in test_cases:
        result = solve_test(n, lines, queries)
        print(f"n={n}, lines={lines}, queries={queries}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, lines, queries):
    results = []
    for x, y in queries:
        result = check_point_on_lines(lines, x, y)
        results.append(result)
    return results

def check_point_on_lines(lines, x, y):
    for a, b, c in lines:
        if abs(a * x + b * y + c) < 1e-9:
            return "YES"
    return "NO"

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n*q) - check each line for each query
- **Space**: O(1) - constant space per query

### Why This Solution Works
- **Point-Line Equation**: Direct application of line formula
- **Early Termination**: Stop when first match is found
- **Numerical Stability**: Use epsilon for floating-point comparison
- **Simple Logic**: Clear and straightforward implementation

## 🎯 Key Insights

### 1. **Point-Line Relationship**
- Use line equation ax + by + c = 0
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Numerical Precision**
- Use epsilon for floating-point comparisons
- Important for understanding
- Simple but important concept
- Essential for accuracy

### 3. **Early Termination**
- Stop checking when first match is found
- Important for understanding
- Fundamental concept
- Essential for efficiency

## 🎯 Problem Variations

### Variation 1: Points with Tolerance
**Problem**: Check if points lie within a certain distance of any line.

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

# Example usage
tolerance = 0.1
result = lines_and_queries_with_tolerance(3, lines, queries, tolerance)
print(f"Tolerance-based result: {result}")
```

### Variation 2: Lines with Weights
**Problem**: Each line has a weight, find total weight of lines containing the point.

```python
def lines_and_queries_with_weights(n, lines_with_weights, queries):
    results = []
    
    for x, y in queries:
        total_weight = 0
        for (a, b, c), weight in lines_with_weights:
            if abs(a * x + b * y + c) < 1e-9:
                total_weight += weight
        results.append(total_weight)
    
    return results

# Example usage
lines_with_weights = [((1, 0, -2), 3), ((0, 1, -3), 2), ((1, 1, -5), 1)]
result = lines_and_queries_with_weights(3, lines_with_weights, queries)
print(f"Weighted result: {result}")
```

### Variation 3: Lines with Constraints
**Problem**: Only check lines within certain constraints.

```python
def lines_and_queries_with_constraints(n, lines, queries, constraints):
    def check_constraints(line, constraint):
        a, b, c = line
        # Example constraint: only check lines with |a| + |b| <= constraint
        return abs(a) + abs(b) <= constraint
    
    results = []
    for x, y in queries:
        found = False
        
        for line in lines:
            if check_constraints(line, constraints):
                if abs(line[0] * x + line[1] * y + line[2]) < 1e-9:
                    found = True
                    break
        
        results.append("YES" if found else "NO")
    
    return results

# Example usage
constraint = 2  # Only check lines with |a| + |b| <= 2
result = lines_and_queries_with_constraints(3, lines, queries, constraint)
print(f"Constrained result: {result}")
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
    
    def query(self, x, y):
        for a, b, c in self.lines:
            if abs(a * x + b * y + c) < 1e-9:
                return "YES"
        return "NO"

# Example usage
dynamic_system = DynamicLinesAndQueries()
dynamic_system.add_line(1, 0, -2)
dynamic_system.add_line(0, 1, -3)
result = dynamic_system.query(2, 3)
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
    for x, y in queries:
        found = False
        
        # Check relevant spatial groups
        relevant_groups = set()
        for x_region in range(int(x//100) - 1, int(x//100) + 2):
            for y_region in range(int(y//100) - 1, int(y//100) + 2):
                relevant_groups.add((x_region, y_region))
        
        for group_key in relevant_groups:
            for line_idx in spatial_groups[group_key]:
                a, b, c = lines[line_idx]
                if abs(a * x + b * y + c) < 1e-9:
                    found = True
                    break
            if found:
                break
        
        results.append("YES" if found else "NO")
    
    return results

# Example usage
result = lines_and_queries_with_spatial_index(3, lines, queries)
print(f"Spatially indexed result: {result}")
```

## 🔗 Related Problems

- **[Lines and Queries II](/cses-analyses/problem_soulutions/geometry/)**: Similar line query problems
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/)**: Point containment problems
- **[Geometric Algorithms](/cses-analyses/problem_soulutions/geometry/)**: Other geometric problems

## 📚 Learning Points

1. **Point-Line Equations**: Essential for geometric algorithms
2. **Numerical Stability**: Important for accurate computations
3. **Early Termination**: Key for efficient algorithms
4. **Spatial Indexing**: Important for optimization

---

**This is a great introduction to point-line geometric algorithms!** 🎯
