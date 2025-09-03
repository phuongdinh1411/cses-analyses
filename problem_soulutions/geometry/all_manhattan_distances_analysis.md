---
layout: simple
title: "All Manhattan Distances Analysis"
permalink: /problem_soulutions/geometry/all_manhattan_distances_analysis
---


# All Manhattan Distances Analysis

## Problem Description

**Problem**: Given a set of n points in 2D space, find the sum of Manhattan distances between all pairs of points.

**Input**: 
- n: number of points
- n lines: x y (coordinates of each point)

**Output**: Sum of Manhattan distances between all pairs of points.

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Calculate Manhattan distance between all point pairs
- Manhattan distance = |x1-x2| + |y1-y2|
- Sum up all pairwise distances
- Use geometric distance formulas

**Key Observations:**
- Need to consider all pairs of points
- Manhattan distance is sum of absolute differences
- Can optimize by separating x and y coordinates
- O(n²) pairs to consider

### Step 2: Brute Force Approach
**Idea**: Calculate distance between every pair of points directly.

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

**Why this works:**
- Direct calculation of all pairs
- Simple and straightforward
- Handles all cases correctly
- O(n²) time complexity

### Step 3: Optimized Approach
**Idea**: Separate x and y coordinates and calculate distances for each dimension independently.

```python
def all_manhattan_distances_optimized(points):
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

**Why this works:**
- Separates x and y dimensions
- Uses sorted coordinates for efficiency
- Mathematical optimization
- O(n log n) time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_all_manhattan_distances():
    n = int(input())
    points = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = calculate_manhattan_distances(points)
    print(result)

def calculate_manhattan_distances(points):
    n = len(points)
    
    # Extract and sort coordinates
    x_coords = sorted([x for x, y in points])
    y_coords = sorted([y for x, y in points])
    
    # Calculate x distances
    x_distance = 0
    for i in range(n):
        x_distance += x_coords[i] * i - sum(x_coords[:i])
    
    # Calculate y distances
    y_distance = 0
    for i in range(n):
        y_distance += y_coords[i] * i - sum(y_coords[:i])
    
    return x_distance + y_distance

# Main execution
if __name__ == "__main__":
    solve_all_manhattan_distances()
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
        ([(0, 0), (1, 1), (2, 2)], 8),
        ([(0, 0), (1, 0), (0, 1)], 4),
        ([(1, 1), (2, 2), (3, 3)], 8),
        ([(0, 0), (2, 0), (0, 2)], 8),
    ]
    
    for points, expected in test_cases:
        result = solve_test(points)
        print(f"Points: {points}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(points):
    return calculate_manhattan_distances(points)

def calculate_manhattan_distances(points):
    n = len(points)
    
    x_coords = sorted([x for x, y in points])
    y_coords = sorted([y for x, y in points])
    
    x_distance = 0
    for i in range(n):
        x_distance += x_coords[i] * i - sum(x_coords[:i])
    
    y_distance = 0
    for i in range(n):
        y_distance += y_coords[i] * i - sum(y_coords[:i])
    
    return x_distance + y_distance

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting coordinates
- **Space**: O(n) - storing sorted coordinates

### Why This Solution Works
- **Coordinate Separation**: Handles x and y independently
- **Mathematical Optimization**: Uses sorted coordinates efficiently
- **Efficient Calculation**: Avoids recalculating distances
- **Optimal Approach**: Better than O(n²) brute force

## 🎯 Key Insights

### 1. **Manhattan Distance Properties**
- Separates into x and y components
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Coordinate Sorting**
- Sort coordinates for efficiency
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Mathematical Optimization**
- Use mathematical formulas
- Important for understanding
- Fundamental concept
- Essential for efficiency

## 🎯 Problem Variations

### Variation 1: Manhattan Distances with Weights
**Problem**: Each point has a weight, find weighted sum of distances.

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

# Example usage
points_with_weights = [((0, 0), 1), ((1, 1), 2), ((2, 2), 1)]
result = manhattan_distances_with_weights(points_with_weights)
print(f"Weighted Manhattan distances: {result}")
```

### Variation 2: Manhattan Distances with Constraints
**Problem**: Only consider distances within certain constraints.

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

# Example usage
max_dist = 2
result = manhattan_distances_with_constraints(points, max_dist)
print(f"Constrained Manhattan distances: {result}")
```

### Variation 3: Manhattan Distances with Dynamic Updates
**Problem**: Support adding/removing points and calculating distances.

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
            x_distance += self.x_coords[i] * i - sum(self.x_coords[:i])
        
        y_distance = 0
        for i in range(n):
            y_distance += self.y_coords[i] * i - sum(self.y_coords[:i])
        
        return x_distance + y_distance

# Example usage
dynamic_system = DynamicManhattanDistances()
dynamic_system.add_point(0, 0)
dynamic_system.add_point(1, 1)
result = dynamic_system.get_total_distance()
print(f"Dynamic Manhattan distances: {result}")
```

### Variation 4: Manhattan Distances with Range Queries
**Problem**: Answer queries about distances in specific ranges.

```python
def manhattan_distances_range_queries(points, queries):
    n = len(points)
    
    # Precompute all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            distance = abs(x1 - x2) + abs(y1 - y2)
            distances.append(distance)
    
    distances.sort()
    
    results = []
    for min_dist, max_dist in queries:
        # Count distances in range [min_dist, max_dist]
        count = 0
        for dist in distances:
            if min_dist <= dist <= max_dist:
                count += 1
        results.append(count)
    
    return results

# Example usage
queries = [(1, 3), (2, 4), (0, 5)]
result = manhattan_distances_range_queries(points, queries)
print(f"Range query results: {result}")
```

### Variation 5: Manhattan Distances with Clustering
**Problem**: Group points into clusters and find inter-cluster distances.

```python
def manhattan_distances_with_clustering(points, k):
    from sklearn.cluster import KMeans
    import numpy as np
    
    # Convert points to numpy array
    points_array = np.array(points)
    
    # Perform k-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(points_array)
    
    # Calculate distances between cluster centers
    centers = kmeans.cluster_centers_
    total_distance = 0
    
    for i in range(k):
        for j in range(i + 1, k):
            x1, y1 = centers[i]
            x2, y2 = centers[j]
            distance = abs(x1 - x2) + abs(y1 - y2)
            total_distance += distance
    
    return total_distance, clusters

# Example usage
k_clusters = 2
result, cluster_labels = manhattan_distances_with_clustering(points, k_clusters)
print(f"Clustered Manhattan distances: {result}")
print(f"Cluster labels: {cluster_labels}")
```

## 🔗 Related Problems

- **[Maximum Manhattan Distance](/cses-analyses/problem_soulutions/geometry/)**: Similar distance problems
- **[Geometric Algorithms](/cses-analyses/problem_soulutions/geometry/)**: Other geometric problems
- **[Distance Problems](/cses-analyses/problem_soulutions/geometry/)**: General distance algorithms

## 📚 Learning Points

1. **Manhattan Distance**: Essential for geometric distance calculations
2. **Coordinate Separation**: Important for optimization
3. **Mathematical Optimization**: Key for efficient algorithms
4. **Sorting for Efficiency**: Important for performance

---

**This is a great introduction to Manhattan distance algorithms!** 🎯
