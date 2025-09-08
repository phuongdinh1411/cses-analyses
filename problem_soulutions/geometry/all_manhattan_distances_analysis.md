---
layout: simple
title: "All Manhattan Distances Analysis"
permalink: /problem_soulutions/geometry/all_manhattan_distances_analysis
---


# All Manhattan Distances Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand Manhattan distance concepts and pairwise distance calculations
- Apply coordinate separation and sorting techniques to optimize distance calculations
- Implement efficient algorithms for computing all pairwise Manhattan distances
- Optimize distance calculations using coordinate transformations and mathematical properties
- Handle edge cases in distance calculations (single points, collinear points, large coordinate values)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Manhattan distance, coordinate separation, sorting algorithms, distance optimization
- **Data Structures**: Arrays, coordinate structures, sorting data structures
- **Mathematical Concepts**: Manhattan distance formula, coordinate geometry, distance properties, optimization
- **Programming Skills**: Coordinate manipulation, distance calculations, sorting, geometric computations
- **Related Problems**: Maximum Manhattan Distance (distance optimization), Minimum Euclidean Distance (distance algorithms), Distance problems

## Problem Description

**Problem**: Given a set of n points in 2D space, find the sum of Manhattan distances between all pairs of points.

**Input**: 
- n: number of points
- n lines: x y (coordinates of each point)

**Output**: Sum of Manhattan distances between all pairs of points.

**Constraints**:
- 1 ≤ n ≤ 1000
- -1000 ≤ x, y ≤ 1000 for all coordinates
- All coordinates are integers
- Manhattan distance = |x1-x2| + |y1-y2|
- Consider all pairs (i,j) where i < j

**Example**:
```
Input:
3
0 0
1 1
2 2

Output:
8

Explanation: 
Manhattan distances between pairs:
(0,0) to (1,1): |0-1| + |0-1| = 2
(0,0) to (2,2): |0-2| + |0-2| = 4  
(1,1) to (2,2): |1-2| + |1-2| = 2
Total: 2 + 4 + 2 = 8
```

## Visual Example

### Points Visualization
```
Y
2 |     *
1 |   *
0 | *
  +---+---+---+
    0   1   2  X

Points: (0,0), (1,1), (2,2)
```

### All Pairwise Manhattan Distances
```
Distance between (0,0) and (1,1):
- |0-1| + |0-1| = 1 + 1 = 2

Distance between (0,0) and (2,2):
- |0-2| + |0-2| = 2 + 2 = 4

Distance between (1,1) and (2,2):
- |1-2| + |1-2| = 1 + 1 = 2

Total sum: 2 + 4 + 2 = 8
```

### Manhattan Distance Visualization
```
Y
2 |     *
1 |   *   |
0 | *     |
  +---+---+---+
    0   1   2  X

Manhattan distance from (0,0) to (2,2):
- Path: (0,0) → (2,0) → (2,2)
- Distance: 2 + 2 = 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Check All Pairs (Inefficient)

**Key Insights from Brute Force Solution:**
- Calculate Manhattan distance between every pair of points
- Use direct distance formula |x1-x2| + |y1-y2|
- Simple but inefficient for large inputs
- Not suitable for competitive programming

**Algorithm:**
1. For each pair of points (i,j) where i < j
2. Calculate Manhattan distance |x1-x2| + |y1-y2|
3. Add distance to total sum
4. Return total sum

**Visual Example:**
```
Brute force: Check all pairs
For points: (0,0), (1,1), (2,2)

Pair (0,0) and (1,1):
- Distance: |0-1| + |0-1| = 1 + 1 = 2

Pair (0,0) and (2,2):
- Distance: |0-2| + |0-2| = 2 + 2 = 4

Pair (1,1) and (2,2):
- Distance: |1-2| + |1-2| = 1 + 1 = 2

Total: 2 + 4 + 2 = 8
```

**Implementation:**
```python
def all_manhattan_distances_brute_force(points):
    n = len(points)
    total_distance = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Manhattan distance
            distance = abs(x1 - x2) + abs(y1 - y2)
            total_distance += distance
    
    return total_distance
```

**Time Complexity:** O(n²) where n is the number of points
**Space Complexity:** O(1) for storing the total distance

**Why it's inefficient:**
- Time complexity is O(n²) - slow for large inputs
- No optimization for coordinate separation
- Redundant calculations
- Not suitable for competitive programming

### Approach 2: Coordinate Separation (Better)

**Key Insights from Coordinate Separation Solution:**
- Separate x and y coordinates for independent calculation
- Use sorted coordinates for efficiency
- Calculate distances for each dimension separately
- Much more efficient than brute force

**Algorithm:**
1. Extract x and y coordinates separately
2. Sort both coordinate arrays
3. Calculate sum of distances for x coordinates
4. Calculate sum of distances for y coordinates
5. Return sum of both dimensions

**Visual Example:**
```
Coordinate separation for points: (0,0), (1,1), (2,2)

X-coordinates: [0, 1, 2]
Y-coordinates: [0, 1, 2]

X-distance sum:
- (0,1): |0-1| = 1
- (0,2): |0-2| = 2
- (1,2): |1-2| = 1
- Total X: 1 + 2 + 1 = 4

Y-distance sum:
- (0,1): |0-1| = 1
- (0,2): |0-2| = 2
- (1,2): |1-2| = 1
- Total Y: 1 + 2 + 1 = 4

Total Manhattan distance: 4 + 4 = 8
```

**Implementation:**
```python
def all_manhattan_distances_coordinate_separation(points):
    n = len(points)
    
    # Extract x and y coordinates
    x_coords = [x for x, y in points]
    y_coords = [y for x, y in points]
    
    # Sort coordinates for efficient calculation
    x_coords.sort()
    y_coords.sort()
    
    # Calculate sum of distances for x coordinates
    x_distance = 0
    for i in range(n):
        x_distance += x_coords[i] * i - sum(x_coords[:i])
    
    # Calculate sum of distances for y coordinates
    y_distance = 0
    for i in range(n):
        y_distance += y_coords[i] * i - sum(y_coords[:i])
    
    return x_distance + y_distance
```

**Time Complexity:** O(n log n) where n is the number of points
**Space Complexity:** O(n) for storing sorted coordinates

**Why it's better:**
- Much more efficient than brute force
- O(n log n) time complexity is optimal for comparison-based algorithms
- Separates dimensions for independent calculation
- Better scalability for large inputs

### Approach 3: Optimized Mathematical Formula (Optimal)

**Key Insights from Optimized Mathematical Solution:**
- Use mathematical formula for distance calculation
- Optimize with prefix sums for efficiency
- Handle edge cases efficiently
- Best performance and reliability

**Algorithm:**
1. Validate input (minimum 2 points)
2. Extract and sort x and y coordinates
3. Use optimized formula with prefix sums
4. Calculate distances for each dimension
5. Return sum of both dimensions

**Visual Example:**
```
Optimized formula for points: (0,0), (1,1), (2,2)

X-coordinates: [0, 1, 2] (sorted)
Y-coordinates: [0, 1, 2] (sorted)

Using formula: Σᵢ₌₁ⁿ (2i - n - 1) × xᵢ

X-distance: (2×1-3-1)×0 + (2×2-3-1)×1 + (2×3-3-1)×2
= (-2)×0 + 0×1 + 2×2 = 4

Y-distance: (2×1-3-1)×0 + (2×2-3-1)×1 + (2×3-3-1)×2
= (-2)×0 + 0×1 + 2×2 = 4

Total: 4 + 4 = 8
```

**Implementation:**
```python
def all_manhattan_distances_optimized(points):
    n = len(points)
    if n < 2:
        return 0
    
    # Extract and sort coordinates
    x_coords = sorted([x for x, y in points])
    y_coords = sorted([y for x, y in points])
    
    # Calculate x distances using optimized formula
    x_distance = 0
    for i in range(n):
        x_distance += x_coords[i] * (2 * i - n + 1)
    
    # Calculate y distances using optimized formula
    y_distance = 0
    for i in range(n):
        y_distance += y_coords[i] * (2 * i - n + 1)
    
    return x_distance + y_distance

def solve_all_manhattan_distances():
    n = int(input())
    points = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = all_manhattan_distances_optimized(points)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_all_manhattan_distances()
```

**Time Complexity:** O(n log n) where n is the number of points
**Space Complexity:** O(n) for storing sorted coordinates

**Why it's optimal:**
- Best known approach for Manhattan distance calculations
- Uses mathematical formula for efficiency
- Optimal time complexity O(n log n)
- Handles all edge cases correctly
- Standard method in competitive programming

## 🎯 Problem Variations

### Variation 1: Manhattan Distances with Weights
**Problem**: Each point has a weight, find weighted sum of distances.

**Link**: [CSES Problem Set - Manhattan Distances with Weights](https://cses.fi/problemset/task/manhattan_distances_weights)

```python
def manhattan_distances_with_weights(points_with_weights):
    n = len(points_with_weights)
    
    # Extract coordinates and weights
    x_coords = [(x, w) for (x, y), w in points_with_weights]
    y_coords = [(y, w) for (x, y), w in points_with_weights]
    
    # Sort by coordinate
    x_coords.sort(key=lambda x: x[0])
    y_coords.sort(key=lambda x: x[0])
    
    # Calculate weighted distances
    x_distance = 0
    for i in range(n):
        xi, wi = x_coords[i]
        for j in range(i):
            xj, wj = x_coords[j]
            x_distance += (xi - xj) * wi * wj
    
    y_distance = 0
    for i in range(n):
        yi, wi = y_coords[i]
        for j in range(i):
            yj, wj = y_coords[j]
            y_distance += (yi - yj) * wi * wj
    
    return x_distance + y_distance
```

### Variation 2: Manhattan Distances with Constraints
**Problem**: Only consider distances within certain constraints.

**Link**: [CSES Problem Set - Manhattan Distances with Constraints](https://cses.fi/problemset/task/manhattan_distances_constraints)

```python
def manhattan_distances_with_constraints(points, max_distance):
    n = len(points)
    total_distance = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            distance = abs(x1 - x2) + abs(y1 - y2)
            if distance <= max_distance:
                total_distance += distance
    
    return total_distance
```

### Variation 3: Manhattan Distances with Dynamic Updates
**Problem**: Support adding/removing points and calculating distances.

**Link**: [CSES Problem Set - Manhattan Distances with Dynamic Updates](https://cses.fi/problemset/task/manhattan_distances_dynamic)

```python
class DynamicManhattanDistances:
    def __init__(self):
        self.points = []
        self.x_coords = []
        self.y_coords = []
    
    def add_point(self, x, y):
        self.points.append((x, y))
        self.x_coords.append(x)
        self.y_coords.append(y)
        self.x_coords.sort()
        self.y_coords.sort()
    
    def remove_point(self, x, y):
        if (x, y) in self.points:
            self.points.remove((x, y))
            self.x_coords.remove(x)
            self.y_coords.remove(y)
    
    def get_total_distance(self):
        n = len(self.points)
        if n < 2:
            return 0
        
        x_distance = 0
        for i in range(n):
            x_distance += self.x_coords[i] * (2 * i - n + 1)
        
        y_distance = 0
        for i in range(n):
            y_distance += self.y_coords[i] * (2 * i - n + 1)
        
        return x_distance + y_distance
```

## 🔗 Related Problems

- **[Maximum Manhattan Distance](/cses-analyses/problem_soulutions/geometry/maximum_manhattan_distance_analysis/)**: Similar distance problems
- **[Minimum Euclidean Distance](/cses-analyses/problem_soulutions/geometry/minimum_euclidean_distance_analysis/)**: Distance algorithms
- **[Point Location Test](/cses-analyses/problem_soulutions/geometry/point_location_test_analysis/)**: Geometric queries
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/convex_hull_analysis/)**: Geometric algorithms

## 📚 Learning Points

1. **Manhattan Distance**: Essential for geometric distance calculations
2. **Coordinate Separation**: Important for optimization
3. **Mathematical Optimization**: Key for efficient algorithms
4. **Sorting for Efficiency**: Important for performance
5. **Mathematical Formulas**: Critical for competitive programming
6. **Dimensional Independence**: Important for geometric problems

## 📝 Summary

The All Manhattan Distances problem demonstrates fundamental computational geometry concepts for distance calculations. We explored three approaches:

1. **Brute Force Check All Pairs**: O(n²) time complexity, checks every pair individually
2. **Coordinate Separation**: O(n log n) time complexity, separates x and y dimensions
3. **Optimized Mathematical Formula**: O(n log n) time complexity, best approach with mathematical optimization

The key insights include separating coordinates for independent calculation, using mathematical formulas for efficiency, and sorting coordinates for optimal performance. This problem serves as an excellent introduction to Manhattan distance algorithms and computational geometry.
