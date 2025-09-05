---
layout: simple
title: "Maximum Manhattan Distance Analysis"
permalink: /problem_soulutions/geometry/maximum_manhattan_distance_analysis
---


# Maximum Manhattan Distance Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand maximum distance problems and Manhattan distance optimization
- [ ] **Objective 2**: Apply coordinate transformation techniques to find maximum Manhattan distances
- [ ] **Objective 3**: Implement efficient algorithms for finding maximum Manhattan distances between points
- [ ] **Objective 4**: Optimize maximum distance calculations using geometric properties and coordinate transformations
- [ ] **Objective 5**: Handle edge cases in maximum distance problems (single points, collinear points, boundary conditions)

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find maximum Manhattan distance between any two points
- Manhattan distance = |x1-x2| + |y1-y2|
- Consider all pairs of points
- Use geometric distance optimization

**Key Observations:**
- Manhattan distance separates into x and y components
- Maximum distance occurs at extreme coordinates
- Can optimize by finding min/max x and y values
- O(n) solution possible instead of O(n²)

### Step 2: Brute Force Approach
**Idea**: Calculate distance between every pair of points and find maximum.

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

**Why this works:**
- Direct calculation of all pairs
- Simple and straightforward
- Guarantees correct result
- O(n²) time complexity

### Step 3: Optimized Approach
**Idea**: Manhattan distance separates into x and y components, so find extreme coordinates.

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
    
    # Maximum Manhattan distance is between extreme points
    # Can be achieved by (min_x, min_y) to (max_x, max_y)
    # or (min_x, max_y) to (max_x, min_y)
    distance1 = (max_x - min_x) + (max_y - min_y)
    distance2 = (max_x - min_x) + (max_y - min_y)  # Same as distance1
    
    return distance1
```

**Why this works:**
- Manhattan distance separates into x and y components
- Maximum occurs at extreme coordinates
- Mathematical optimization
- O(n) time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_maximum_manhattan_distance():
    n = int(input())
    points = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = find_maximum_manhattan_distance(points)
    print(result)

def find_maximum_manhattan_distance(points):
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

# Main execution
if __name__ == "__main__":
    solve_maximum_manhattan_distance()
```

**Why this works:**
- Optimal mathematical approach
- Handles all edge cases efficiently
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(0, 0), (1, 1), (2, 2), (5, 5)], 10),
        ([(0, 0), (1, 0), (0, 1)], 2),
        ([(1, 1), (2, 2), (3, 3)], 4),
        ([(0, 0), (2, 0), (0, 2)], 4),
        ([(1, 1)], 0),  # Single point
    ]
    
    for points, expected in test_cases:
        result = solve_test(points)
        print(f"Points: {points}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(points):
    return find_maximum_manhattan_distance(points)

def find_maximum_manhattan_distance(points):
    if len(points) < 2:
        return 0
    
    x_coords = [x for x, y in points]
    y_coords = [y for x, y in points]
    
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    return (max_x - min_x) + (max_y - min_y)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass to find min/max coordinates
- **Space**: O(1) - constant space for tracking min/max

### Why This Solution Works
- **Coordinate Separation**: Manhattan distance separates into x and y components
- **Extreme Points**: Maximum distance occurs at extreme coordinates
- **Mathematical Optimization**: Uses properties of Manhattan distance
- **Efficient Approach**: O(n) instead of O(n²)

## 🎨 Visual Example

### Input Example
```
4 points: (0,0), (1,1), (2,2), (5,5)
```

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

### Manhattan Distance Visualization
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

Manhattan distance from (0,0) to (5,5):
- Path: (0,0) → (5,0) → (5,5)
- Distance: 5 + 5 = 10
```

### Mathematical Insight
```
For Manhattan distance: |x₁ - x₂| + |y₁ - y₂|

Maximum occurs when:
- |x₁ - x₂| is maximized (at extreme x-coordinates)
- |y₁ - y₂| is maximized (at extreme y-coordinates)

Therefore:
Maximum distance = (max_x - min_x) + (max_y - min_y)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(1)         │ Check all    │
│                 │              │              │ pairs        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Extreme Points  │ O(n)         │ O(1)         │ Find min/max │
│                 │              │              │ coordinates  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Mathematical    │ O(n)         │ O(1)         │ Use          │
│ Optimization    │              │              │ properties   │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Manhattan Distance Properties**
- Separates into x and y components
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Extreme Coordinate Optimization**
- Maximum distance at extreme points
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Mathematical Insight**
- Use properties of distance function
- Important for understanding
- Fundamental concept
- Essential for efficiency

## 🎯 Problem Variations

### Variation 1: Maximum Manhattan Distance with Weights
**Problem**: Each point has a weight, find maximum weighted Manhattan distance.

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

# Example usage
points_with_weights = [((0, 0), 1), ((1, 1), 2), ((5, 5), 1)]
result = maximum_manhattan_distance_with_weights(points_with_weights)
print(f"Maximum weighted Manhattan distance: {result}")
```

### Variation 2: Maximum Manhattan Distance with Constraints
**Problem**: Find maximum distance subject to certain constraints.

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

# Example usage
constraints = {"min_x": 0, "max_x": 10, "min_y": 0, "max_y": 10}
result = maximum_manhattan_distance_with_constraints(points, constraints)
print(f"Constrained maximum Manhattan distance: {result}")
```

### Variation 3: Maximum Manhattan Distance with Dynamic Updates
**Problem**: Support adding/removing points and finding maximum distance.

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

# Example usage
dynamic_system = DynamicMaximumManhattanDistance()
dynamic_system.add_point(0, 0)
dynamic_system.add_point(5, 5)
result = dynamic_system.get_maximum_distance()
print(f"Dynamic maximum Manhattan distance: {result}")
```

### Variation 4: Maximum Manhattan Distance with Range Queries
**Problem**: Answer queries about maximum distance in specific ranges.

```python
def maximum_manhattan_distance_range_queries(points, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Filter points in range
        filtered_points = []
        for x, y in points:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                filtered_points.append((x, y))
        
        if len(filtered_points) < 2:
            results.append(0)
        else:
            # Find maximum distance in range
            x_coords = [x for x, y in filtered_points]
            y_coords = [y for x, y in filtered_points]
            
            range_min_x, range_max_x = min(x_coords), max(x_coords)
            range_min_y, range_max_y = min(y_coords), max(y_coords)
            
            max_distance = (range_max_x - range_min_x) + (range_max_y - range_min_y)
            results.append(max_distance)
    
    return results

# Example usage
queries = [(0, 3, 0, 3), (1, 5, 1, 5), (0, 10, 0, 10)]
result = maximum_manhattan_distance_range_queries(points, queries)
print(f"Range query results: {result}")
```

### Variation 5: Maximum Manhattan Distance with Clustering
**Problem**: Group points into clusters and find maximum inter-cluster distance.

```python
def maximum_manhattan_distance_with_clustering(points, k):
    from sklearn.cluster import KMeans
    import numpy as np
    
    if len(points) < 2:
        return 0
    
    # Convert points to numpy array
    points_array = np.array(points)
    
    # Perform k-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(points_array)
    
    # Calculate distances between cluster centers
    centers = kmeans.cluster_centers_
    max_distance = 0
    
    for i in range(k):
        for j in range(i + 1, k):
            x1, y1 = centers[i]
            x2, y2 = centers[j]
            distance = abs(x1 - x2) + abs(y1 - y2)
            max_distance = max(max_distance, distance)
    
    return max_distance, clusters

# Example usage
k_clusters = 2
result, cluster_labels = maximum_manhattan_distance_with_clustering(points, k_clusters)
print(f"Clustered maximum Manhattan distance: {result}")
print(f"Cluster labels: {cluster_labels}")
```

## 🔗 Related Problems

- **[All Manhattan Distances](/cses-analyses/problem_soulutions/geometry/)**: Similar distance problems
- **[Geometric Algorithms](/cses-analyses/problem_soulutions/geometry/)**: Other geometric problems
- **[Distance Problems](/cses-analyses/problem_soulutions/geometry/)**: General distance algorithms

## 📚 Learning Points

1. **Manhattan Distance**: Essential for geometric distance calculations
2. **Extreme Coordinate Optimization**: Important for efficiency
3. **Mathematical Properties**: Key for algorithm design
4. **Coordinate Separation**: Important for optimization

---

**This is a great introduction to maximum Manhattan distance algorithms!** 🎯
