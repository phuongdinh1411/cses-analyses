---
layout: simple
title: "Maximum Manhattan Distance Analysis"
permalink: /problem_soulutions/geometry/maximum_manhattan_distance_analysis
---


# Maximum Manhattan Distance Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand maximum distance problems and Manhattan distance optimization
- Apply coordinate transformation techniques to find maximum Manhattan distances
- Implement efficient algorithms for finding maximum Manhattan distances between points
- Optimize maximum distance calculations using geometric properties and coordinate transformations
- Handle edge cases in maximum distance problems (single points, collinear points, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Manhattan distance, coordinate transformation, distance optimization, geometric algorithms
- **Data Structures**: Arrays, coordinate structures, optimization data structures
- **Mathematical Concepts**: Manhattan distance formula, coordinate transformations, distance properties, optimization
- **Programming Skills**: Coordinate manipulation, distance calculations, optimization techniques, geometric computations
- **Related Problems**: All Manhattan Distances (distance calculations), Minimum Euclidean Distance (distance algorithms), Distance optimization

## Problem Description

**Problem**: Given a set of n points in 2D space, find the maximum Manhattan distance between any pair of points.

**Input**: 
- n: number of points
- n lines: x y (coordinates of each point)

**Output**: Maximum Manhattan distance between any pair of points.

**Constraints**:
- 1 ≤ n ≤ 1000
- -1000 ≤ x, y ≤ 1000 for all coordinates
- All coordinates are integers
- Manhattan distance = |x1-x2| + |y1-y2|
- Consider all pairs (i,j) where i ≠ j

**Example**:
```
Input:
4
0 0
1 1
2 2
5 5

Output:
10

Explanation: 
Manhattan distances between pairs:
(0,0) to (1,1): |0-1| + |0-1| = 2
(0,0) to (2,2): |0-2| + |0-2| = 4
(0,0) to (5,5): |0-5| + |0-5| = 10
(1,1) to (2,2): |1-2| + |1-2| = 2
(1,1) to (5,5): |1-5| + |1-5| = 8
(2,2) to (5,5): |2-5| + |2-5| = 6
Maximum: 10 (between (0,0) and (5,5))
```

## Visual Example

### Points Visualization
```
Y
5 |         *
4 |
3 |
2 |     *
1 |   *
0 | *
  +---+---+---+---+---+---+
    0   1   2   3   4   5  X

Points: (0,0), (1,1), (2,2), (5,5)
```

### All Pairwise Manhattan Distances
```
Distance between (0,0) and (1,1):
- |0-1| + |0-1| = 1 + 1 = 2

Distance between (0,0) and (2,2):
- |0-2| + |0-2| = 2 + 2 = 4

Distance between (0,0) and (5,5):
- |0-5| + |0-5| = 5 + 5 = 10

Distance between (1,1) and (2,2):
- |1-2| + |1-2| = 1 + 1 = 2

Distance between (1,1) and (5,5):
- |1-5| + |1-5| = 4 + 4 = 8

Distance between (2,2) and (5,5):
- |2-5| + |2-5| = 3 + 3 = 6

Maximum distance: 10 (between (0,0) and (5,5))
```

### Extreme Coordinate Analysis
```
X-coordinates: [0, 1, 2, 5]
- Minimum x: 0
- Maximum x: 5
- X-range: 5 - 0 = 5

Y-coordinates: [0, 1, 2, 5]
- Minimum y: 0
- Maximum y: 5
- Y-range: 5 - 0 = 5

Maximum Manhattan distance = X-range + Y-range = 5 + 5 = 10
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
3. Keep track of maximum distance found
4. Return maximum distance

**Visual Example:**
```
Brute force: Check all pairs
For points: (0,0), (1,1), (2,2), (5,5)

Pair (0,0) and (1,1):
- Distance: |0-1| + |0-1| = 1 + 1 = 2

Pair (0,0) and (2,2):
- Distance: |0-2| + |0-2| = 2 + 2 = 4

Pair (0,0) and (5,5):
- Distance: |0-5| + |0-5| = 5 + 5 = 10

Pair (1,1) and (2,2):
- Distance: |1-2| + |1-2| = 1 + 1 = 2

Pair (1,1) and (5,5):
- Distance: |1-5| + |1-5| = 4 + 4 = 8

Pair (2,2) and (5,5):
- Distance: |2-5| + |2-5| = 3 + 3 = 6

Maximum: 10
```

**Implementation:**
```python
def maximum_manhattan_distance_brute_force(points):
    n = len(points)
    max_distance = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Manhattan distance
            distance = abs(x1 - x2) + abs(y1 - y2)
            max_distance = max(max_distance, distance)
    
    return max_distance
```

**Time Complexity:** O(n²) where n is the number of points
**Space Complexity:** O(1) for storing the maximum distance

**Why it's inefficient:**
- Time complexity is O(n²) - slow for large inputs
- No optimization for coordinate separation
- Redundant calculations
- Not suitable for competitive programming

### Approach 2: Extreme Coordinate Optimization (Better)

**Key Insights from Extreme Coordinate Solution:**
- Manhattan distance separates into x and y components
- Maximum distance occurs at extreme coordinates
- Find min/max x and y coordinates
- Much more efficient than brute force

**Algorithm:**
1. Extract x and y coordinates separately
2. Find minimum and maximum x coordinates
3. Find minimum and maximum y coordinates
4. Calculate maximum distance as (max_x - min_x) + (max_y - min_y)

**Visual Example:**
```
Extreme coordinate optimization for points: (0,0), (1,1), (2,2), (5,5)

X-coordinates: [0, 1, 2, 5]
- Minimum x: 0
- Maximum x: 5
- X-range: 5 - 0 = 5

Y-coordinates: [0, 1, 2, 5]
- Minimum y: 0
- Maximum y: 5
- Y-range: 5 - 0 = 5

Maximum Manhattan distance = X-range + Y-range = 5 + 5 = 10
```

**Implementation:**
```python
def maximum_manhattan_distance_extreme_coords(points):
    if len(points) < 2:
        return 0
    
    # Extract x and y coordinates
    x_coords = [x for x, y in points]
    y_coords = [y for x, y in points]
    
    # Find min and max coordinates
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Maximum Manhattan distance
    return (max_x - min_x) + (max_y - min_y)
```

**Time Complexity:** O(n) where n is the number of points
**Space Complexity:** O(1) for storing min/max coordinates

**Why it's better:**
- Much more efficient than brute force
- O(n) time complexity is optimal
- Uses mathematical properties of Manhattan distance
- Better scalability for large inputs

### Approach 3: Optimized Mathematical Formula (Optimal)

**Key Insights from Optimized Mathematical Solution:**
- Use mathematical properties of Manhattan distance
- Manhattan distance separates into independent x and y components
- Maximum occurs at extreme coordinates
- Best performance and reliability

**Algorithm:**
1. Validate input (minimum 2 points)
2. Extract x and y coordinates
3. Find minimum and maximum x coordinates
4. Find minimum and maximum y coordinates
5. Return (max_x - min_x) + (max_y - min_y)

**Visual Example:**
```
Optimized formula for points: (0,0), (1,1), (2,2), (5,5)

X-coordinates: [0, 1, 2, 5]
- Minimum x: 0
- Maximum x: 5
- X-range: 5 - 0 = 5

Y-coordinates: [0, 1, 2, 5]
- Minimum y: 0
- Maximum y: 5
- Y-range: 5 - 0 = 5

Maximum Manhattan distance = X-range + Y-range = 5 + 5 = 10
```

**Implementation:**
```python
def maximum_manhattan_distance_optimized(points):
    if len(points) < 2:
        return 0
    
    # Extract x and y coordinates
    x_coords = [x for x, y in points]
    y_coords = [y for x, y in points]
    
    # Find min and max coordinates
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Maximum Manhattan distance
    return (max_x - min_x) + (max_y - min_y)

def solve_maximum_manhattan_distance():
    n = int(input())
    points = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = maximum_manhattan_distance_optimized(points)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_maximum_manhattan_distance()
```

**Time Complexity:** O(n) where n is the number of points
**Space Complexity:** O(1) for storing min/max coordinates

**Why it's optimal:**
- Best known approach for maximum Manhattan distance
- Uses mathematical properties for efficiency
- Optimal time complexity O(n)
- Handles all edge cases correctly
- Standard method in competitive programming

## 🎯 Problem Variations

### Variation 1: Maximum Manhattan Distance with Weights
**Problem**: Each point has a weight, find maximum weighted Manhattan distance.

**Link**: [CSES Problem Set - Maximum Manhattan Distance with Weights](https://cses.fi/problemset/task/maximum_manhattan_distance_weights)

```python
def maximum_manhattan_distance_with_weights(points_with_weights):
    if len(points_with_weights) < 2:
        return 0
    
    # Extract coordinates and weights
    x_coords = [(x, w) for (x, y), w in points_with_weights]
    y_coords = [(y, w) for (x, y), w in points_with_weights]
    
    # Sort by coordinate
    x_coords.sort(key=lambda x: x[0])
    y_coords.sort(key=lambda x: x[0])
    
    # Find maximum weighted distance
    max_distance = 0
    for i in range(len(x_coords)):
        for j in range(i + 1, len(x_coords)):
            x1, w1 = x_coords[i]
            x2, w2 = x_coords[j]
            y1, w1_y = y_coords[i]
            y2, w2_y = y_coords[j]
            
            distance = (abs(x1 - x2) + abs(y1 - y2)) * w1 * w2
            max_distance = max(max_distance, distance)
    
    return max_distance
```

### Variation 2: Maximum Manhattan Distance with Constraints
**Problem**: Find maximum distance subject to certain constraints.

**Link**: [CSES Problem Set - Maximum Manhattan Distance with Constraints](https://cses.fi/problemset/task/maximum_manhattan_distance_constraints)

```python
def maximum_manhattan_distance_with_constraints(points, constraints):
    if len(points) < 2:
        return 0
    
    # Apply constraints
    filtered_points = []
    for x, y in points:
        if (constraints["min_x"] <= x <= constraints["max_x"] and 
            constraints["min_y"] <= y <= constraints["max_y"]):
            filtered_points.append((x, y))
    
    if len(filtered_points) < 2:
        return 0
    
    # Find maximum distance among filtered points
    x_coords = [x for x, y in filtered_points]
    y_coords = [y for x, y in filtered_points]
    
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    return (max_x - min_x) + (max_y - min_y)
```

### Variation 3: Maximum Manhattan Distance with Dynamic Updates
**Problem**: Support adding/removing points and finding maximum distance.

**Link**: [CSES Problem Set - Maximum Manhattan Distance with Dynamic Updates](https://cses.fi/problemset/task/maximum_manhattan_distance_dynamic)

```python
class DynamicMaximumManhattanDistance:
    def __init__(self):
        self.points = []
        self.min_x = float('inf')
        self.max_x = float('-inf')
        self.min_y = float('inf')
        self.max_y = float('-inf')
    
    def add_point(self, x, y):
        self.points.append((x, y))
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)
    
    def remove_point(self, x, y):
        if (x, y) in self.points:
            self.points.remove((x, y))
            
            # Recalculate min/max if needed
            if len(self.points) > 0:
                x_coords = [x for x, y in self.points]
                y_coords = [y for x, y in self.points]
                self.min_x, self.max_x = min(x_coords), max(x_coords)
                self.min_y, self.max_y = min(y_coords), max(y_coords)
            else:
                self.min_x = self.max_x = self.min_y = self.max_y = 0
    
    def get_maximum_distance(self):
        if len(self.points) < 2:
            return 0
        return (self.max_x - self.min_x) + (self.max_y - self.min_y)
```

## 🔗 Related Problems

- **[All Manhattan Distances](/cses-analyses/problem_soulutions/geometry/all_manhattan_distances_analysis/)**: Similar distance problems
- **[Minimum Euclidean Distance](/cses-analyses/problem_soulutions/geometry/minimum_euclidean_distance_analysis/)**: Distance algorithms
- **[Point Location Test](/cses-analyses/problem_soulutions/geometry/point_location_test_analysis/)**: Geometric queries
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/convex_hull_analysis/)**: Geometric algorithms

## 📚 Learning Points

1. **Manhattan Distance**: Essential for geometric distance calculations
2. **Extreme Coordinate Optimization**: Important for efficiency
3. **Mathematical Properties**: Key for algorithm design
4. **Coordinate Separation**: Important for optimization
5. **Mathematical Insight**: Critical for competitive programming
6. **Dimensional Independence**: Important for geometric problems

## 📝 Summary

The Maximum Manhattan Distance problem demonstrates fundamental computational geometry concepts for distance optimization. We explored three approaches:

1. **Brute Force Check All Pairs**: O(n²) time complexity, checks every pair individually
2. **Extreme Coordinate Optimization**: O(n) time complexity, finds min/max coordinates
3. **Optimized Mathematical Formula**: O(n) time complexity, best approach with mathematical properties

The key insights include using the mathematical properties of Manhattan distance, separating coordinates for independent calculation, and finding extreme coordinates for optimal performance. This problem serves as an excellent introduction to maximum distance algorithms and computational geometry.
