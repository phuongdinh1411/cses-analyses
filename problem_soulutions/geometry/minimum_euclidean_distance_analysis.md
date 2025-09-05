---
layout: simple
title: "Minimum Euclidean Distance Analysis"
permalink: /problem_soulutions/geometry/minimum_euclidean_distance_analysis
---


# Minimum Euclidean Distance Analysis

## Problem Description

**Problem**: Given a set of n points in 2D plane, find the minimum Euclidean distance between any two points.

**Input**: 
- n: number of points
- n lines: x y (coordinates of each point)

**Output**: Minimum Euclidean distance between any pair of points.

**Example**:
```
Input:
4
0 0
1 1
2 2
5 5

Output:
1.4142135623730951

Explanation: 
Euclidean distances between pairs:
(0,0) to (1,1): √((0-1)² + (0-1)²) = √2 ≈ 1.414
(0,0) to (2,2): √((0-2)² + (0-2)²) = √8 ≈ 2.828
(0,0) to (5,5): √((0-5)² + (0-5)²) = √50 ≈ 7.071
(1,1) to (2,2): √((1-2)² + (1-2)²) = √2 ≈ 1.414
(1,1) to (5,5): √((1-5)² + (1-5)²) = √32 ≈ 5.657
(2,2) to (5,5): √((2-5)² + (2-5)²) = √18 ≈ 4.243
Minimum: √2 ≈ 1.414 (between (0,0) and (1,1), or (1,1) and (2,2))
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find minimum Euclidean distance between any two points
- Euclidean distance = √((x1-x2)² + (y1-y2)²)
- Consider all pairs of points
- Use geometric divide-and-conquer algorithms

**Key Observations:**
- Need to check all pairs for brute force
- Can optimize using spatial properties
- Divide-and-conquer approach is optimal
- Strip search reduces candidate pairs

### Step 2: Brute Force Approach
**Idea**: Calculate distance between every pair of points and find minimum.

```python
def minimum_euclidean_distance_brute_force(points):
    n = len(points)
    min_distance = float('inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Euclidean distance
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            min_distance = min(min_distance, distance)
    
    return min_distance
```

**Why this works:**
- Direct calculation of all pairs
- Simple and straightforward
- Guarantees correct result
- O(n²) time complexity

### Step 3: Divide and Conquer Approach
**Idea**: Divide the plane into two halves, solve recursively, and combine results.

```python
def minimum_euclidean_distance_divide_conquer(points):
    n = len(points)
    if n <= 1:
        return float('inf')
    if n == 2:
        return euclidean_distance(points[0], points[1])
    
    # Sort by x-coordinate
    points.sort()
    
    # Divide into two halves
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    # Recursively find minimum distances in each half
    left_min = minimum_euclidean_distance_divide_conquer(left_points)
    right_min = minimum_euclidean_distance_divide_conquer(right_points)
    
    # Find minimum of left and right
    min_dist = min(left_min, right_min)
    
    # Check for pairs that cross the dividing line
    mid_x = points[mid][0]
    strip = [p for p in points if abs(p[0] - mid_x) < min_dist]
    
    # Sort strip by y-coordinate
    strip.sort(key=lambda p: p[1])
    
    # Check pairs in strip (only need to check 7 points ahead)
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            dist = euclidean_distance(strip[i], strip[j])
            min_dist = min(min_dist, dist)
    
    return min_dist

def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
```

**Why this works:**
- Uses divide-and-conquer strategy
- Strip search reduces candidate pairs
- Mathematical proof shows only 7 points need checking
- O(n log n) time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_minimum_euclidean_distance():
    n = int(input())
    points = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = find_minimum_euclidean_distance(points)
    print(f"{result:.9f}")

def find_minimum_euclidean_distance(points):
    n = len(points)
    if n <= 1:
        return float('inf')
    if n == 2:
        return euclidean_distance(points[0], points[1])
    
    # Sort by x-coordinate
    points.sort()
    
    # Divide into two halves
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    # Recursively find minimum distances
    left_min = find_minimum_euclidean_distance(left_points)
    right_min = find_minimum_euclidean_distance(right_points)
    
    min_dist = min(left_min, right_min)
    
    # Check strip around dividing line
    mid_x = points[mid][0]
    strip = [p for p in points if abs(p[0] - mid_x) < min_dist]
    strip.sort(key=lambda p: p[1])
    
    # Check pairs in strip
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            dist = euclidean_distance(strip[i], strip[j])
            min_dist = min(min_dist, dist)
    
    return min_dist

def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# Main execution
if __name__ == "__main__":
    solve_minimum_euclidean_distance()
```

**Why this works:**
- Optimal divide-and-conquer approach
- Handles all edge cases efficiently
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(0, 0), (1, 1), (2, 2), (5, 5)], 1.4142135623730951),
        ([(0, 0), (1, 0), (0, 1)], 1.0),
        ([(1, 1), (2, 2), (3, 3)], 1.4142135623730951),
        ([(0, 0), (2, 0), (0, 2)], 2.0),
    ]
    
    for points, expected in test_cases:
        result = solve_test(points)
        print(f"Points: {points}")
        print(f"Expected: {expected:.9f}, Got: {result:.9f}")
        print(f"{'✓ PASS' if abs(result - expected) < 1e-9 else '✗ FAIL'}")
        print()

def solve_test(points):
    return find_minimum_euclidean_distance(points)

def find_minimum_euclidean_distance(points):
    n = len(points)
    if n <= 1:
        return float('inf')
    if n == 2:
        return euclidean_distance(points[0], points[1])
    
    points.sort()
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    left_min = find_minimum_euclidean_distance(left_points)
    right_min = find_minimum_euclidean_distance(right_points)
    
    min_dist = min(left_min, right_min)
    
    mid_x = points[mid][0]
    strip = [p for p in points if abs(p[0] - mid_x) < min_dist]
    strip.sort(key=lambda p: p[1])
    
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            dist = euclidean_distance(strip[i], strip[j])
            min_dist = min(min_dist, dist)
    
    return min_dist

def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - divide and conquer with sorting
- **Space**: O(n) - for storing points and strip

### Why This Solution Works
- **Divide and Conquer**: Splits problem into smaller subproblems
- **Strip Search**: Only checks points within minimum distance of dividing line
- **Mathematical Optimization**: Proves only 7 points need checking in strip
- **Optimal Approach**: Best known algorithm for closest pair problem

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

### All Pairwise Euclidean Distances
```
Distance between (0,0) and (1,1):
- √((0-1)² + (0-1)²) = √(1 + 1) = √2 ≈ 1.414

Distance between (0,0) and (2,2):
- √((0-2)² + (0-2)²) = √(4 + 4) = √8 ≈ 2.828

Distance between (0,0) and (5,5):
- √((0-5)² + (0-5)²) = √(25 + 25) = √50 ≈ 7.071

Distance between (1,1) and (2,2):
- √((1-2)² + (1-2)²) = √(1 + 1) = √2 ≈ 1.414

Distance between (1,1) and (5,5):
- √((1-5)² + (1-5)²) = √(16 + 16) = √32 ≈ 5.657

Distance between (2,2) and (5,5):
- √((2-5)² + (2-5)²) = √(9 + 9) = √18 ≈ 4.243

Minimum distance: √2 ≈ 1.414
```

### Divide and Conquer Process
```
Step 1: Sort points by x-coordinate
Points: (0,0), (1,1), (2,2), (5,5)

Step 2: Divide at x = 1.5
Left half: (0,0), (1,1)
Right half: (2,2), (5,5)

Step 3: Recursively find minimum in each half
Left minimum: distance between (0,0) and (1,1) = √2
Right minimum: distance between (2,2) and (5,5) = √18

Step 4: Find minimum across dividing line
Current minimum: min(√2, √18) = √2
Strip width: √2
Points in strip: (1,1), (2,2)
Check distance: (1,1) to (2,2) = √2

Final minimum: √2
```

### Strip Search Visualization
```
Y
5 |         *
4 |
3 |
2 |     *   |
1 |   *     |
0 | *       |
  +---+---+---+---+---+---+
    0   1   2   3   4   5  X

Dividing line at x = 1.5
Strip: x ∈ [1.5 - √2, 1.5 + √2] ≈ [0.086, 2.914]
Points in strip: (1,1), (2,2)
```

### Geometric Properties
```
For points in strip, only need to check 7 points ahead:
- Sort points in strip by y-coordinate
- For each point, check next 7 points
- This is proven to be sufficient

Example:
Strip points: (1,1), (2,2)
- Point (1,1): check (2,2) → distance = √2
- Point (2,2): no more points to check
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(1)         │ Check all    │
│                 │              │              │ pairs        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Divide & Conquer│ O(n log n)   │ O(n)         │ Split        │
│                 │              │              │ recursively  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Strip Search    │ O(n log n)   │ O(n)         │ Only check   │
│                 │              │              │ nearby points│
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Divide and Conquer Strategy**
- Split problem into smaller subproblems
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Strip Search Optimization**
- Only check points near dividing line
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Geometric Properties**
- Use spatial properties to reduce search
- Important for understanding
- Fundamental concept
- Essential for efficiency

## 🎯 Problem Variations

### Variation 1: Minimum Euclidean Distance with Weights
**Problem**: Each point has a weight, find minimum weighted Euclidean distance.

```python
def minimum_euclidean_distance_with_weights(points_with_weights):
    n = len(points_with_weights)
    min_distance = float('inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), w1 = points_with_weights[i]
            (x2, y2), w2 = points_with_weights[j]
            
            # Weighted Euclidean distance
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 * w1 * w2
            min_distance = min(min_distance, distance)
    
    return min_distance

# Example usage
points_with_weights = [((0, 0), 1), ((1, 1), 2), ((2, 2), 1)]
result = minimum_euclidean_distance_with_weights(points_with_weights)
print(f"Minimum weighted Euclidean distance: {result}")
```

### Variation 2: Minimum Euclidean Distance with Constraints
**Problem**: Find minimum distance subject to certain constraints.

```python
def minimum_euclidean_distance_with_constraints(points, constraints):
    n = len(points)
    min_distance = float('inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Check constraints
            if (constraints["min_x"] <= x1 <= constraints["max_x"] and
                constraints["min_y"] <= y1 <= constraints["max_y"] and
                constraints["min_x"] <= x2 <= constraints["max_x"] and
                constraints["min_y"] <= y2 <= constraints["max_y"]):
                
                distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                min_distance = min(min_distance, distance)
    
    return min_distance if min_distance != float('inf') else -1

# Example usage
constraints = {"min_x": 0, "max_x": 10, "min_y": 0, "max_y": 10}
result = minimum_euclidean_distance_with_constraints(points, constraints)
print(f"Constrained minimum Euclidean distance: {result}")
```

### Variation 3: Minimum Euclidean Distance with Dynamic Updates
**Problem**: Support adding/removing points and finding minimum distance.

```python
class DynamicMinimumEuclideanDistance:
    def __init__(self):
        self.points = []
    
    def add_point(self, x, y):
        self.points.append((x, y))
    
    def remove_point(self, x, y):
        if (x, y) in self.points:
            self.points.remove((x, y))
    
    def get_minimum_distance(self):
        if len(self.points) < 2:
            return float('inf')
        return find_minimum_euclidean_distance(self.points)

# Example usage
dynamic_system = DynamicMinimumEuclideanDistance()
dynamic_system.add_point(0, 0)
dynamic_system.add_point(1, 1)
result = dynamic_system.get_minimum_distance()
print(f"Dynamic minimum Euclidean distance: {result}")
```

### Variation 4: Minimum Euclidean Distance with Range Queries
**Problem**: Answer queries about minimum distance in specific ranges.

```python
def minimum_euclidean_distance_range_queries(points, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Filter points in range
        filtered_points = []
        for x, y in points:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                filtered_points.append((x, y))
        
        if len(filtered_points) < 2:
            results.append(float('inf'))
        else:
            # Find minimum distance in range
            min_distance = float('inf')
            for i in range(len(filtered_points)):
                for j in range(i + 1, len(filtered_points)):
                    x1, y1 = filtered_points[i]
                    x2, y2 = filtered_points[j]
                    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                    min_distance = min(min_distance, distance)
            results.append(min_distance)
    
    return results

# Example usage
queries = [(0, 3, 0, 3), (1, 5, 1, 5), (0, 10, 0, 10)]
result = minimum_euclidean_distance_range_queries(points, queries)
print(f"Range query results: {result}")
```

### Variation 5: Minimum Euclidean Distance with Clustering
**Problem**: Group points into clusters and find minimum inter-cluster distance.

```python
def minimum_euclidean_distance_with_clustering(points, k):
    from sklearn.cluster import KMeans
    import numpy as np
    
    if len(points) < 2:
        return float('inf')
    
    # Convert points to numpy array
    points_array = np.array(points)
    
    # Perform k-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(points_array)
    
    # Calculate minimum distance between cluster centers
    centers = kmeans.cluster_centers_
    min_distance = float('inf')
    
    for i in range(k):
        for j in range(i + 1, k):
            x1, y1 = centers[i]
            x2, y2 = centers[j]
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            min_distance = min(min_distance, distance)
    
    return min_distance, clusters

# Example usage
k_clusters = 2
result, cluster_labels = minimum_euclidean_distance_with_clustering(points, k_clusters)
print(f"Clustered minimum Euclidean distance: {result}")
print(f"Cluster labels: {cluster_labels}")
```

## 🔗 Related Problems

- **[All Manhattan Distances](/cses-analyses/problem_soulutions/geometry/)**: Similar distance problems
- **[Geometric Algorithms](/cses-analyses/problem_soulutions/geometry/)**: Other geometric problems
- **[Divide and Conquer](/cses-analyses/problem_soulutions/geometry/)**: Algorithmic techniques

## 📚 Learning Points

1. **Euclidean Distance**: Essential for geometric distance calculations
2. **Divide and Conquer**: Important for efficient algorithms
3. **Strip Search**: Key optimization technique
4. **Geometric Properties**: Important for spatial algorithms

---

**This is a great introduction to minimum Euclidean distance algorithms!** 🎯
- Point Clustering
- Voronoi Diagrams

## Notable Techniques

### Code Patterns
```python
# Calculate Euclidean distance
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Check if points are within distance
def within_distance(p1, p2, max_dist):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 <= max_dist**2
```

### Geometric Concepts
- **Euclidean Distance**: Straight-line distance between two points
- **Divide and Conquer**: Split problem into smaller parts
- **Strip Search**: Check only points near dividing line
- **Spatial Properties**: Use geometric intuition to optimize

## Problem-Solving Framework

### 1. Problem Analysis
- Identify that we need to find minimum distance between any two points
- Recognize that brute force is too slow
- Consider divide and conquer approach

### 2. Algorithm Selection
- Choose divide and conquer for optimal time complexity
- Consider spatial properties for optimization
- Handle edge cases properly

### 3. Implementation Strategy
- Sort points by x-coordinate for division
- Implement recursive solution
- Handle strip search efficiently

### 4. Optimization
- Use squared distances to avoid square root
- Optimize strip search with early termination
- Handle edge cases efficiently

## Complete Implementation

```python
import math

def distance_squared(p1, p2):
    """Calculate squared Euclidean distance to avoid square root"""
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def closest_pair(points):
    """Find closest pair of points using divide and conquer"""
    n = len(points)
    if n <= 1:
        return float('inf')
    if n == 2:
        return math.sqrt(distance_squared(points[0], points[1]))
    
    # Sort by x-coordinate
    points.sort()
    
    # Divide into two halves
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    # Recursively find closest pairs in each half
    left_min = closest_pair(left_points)
    right_min = closest_pair(right_points)
    
    # Find minimum of left and right
    min_dist = min(left_min, right_min)
    
    # Check for pairs that cross the dividing line
    mid_x = points[mid][0]
    strip = [p for p in points if abs(p[0] - mid_x) < min_dist]
    
    # Sort strip by y-coordinate
    strip.sort(key=lambda p: p[1])
    
    # Check pairs in strip (only need to check next 6 points)
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            dist = math.sqrt(distance_squared(strip[i], strip[j]))
            min_dist = min(min_dist, dist)
    
    return min_dist

# Example usage
points = [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)]
min_dist = closest_pair(points)
print(f"Minimum distance: {min_dist}")
```

## Edge Cases and Considerations

### Edge Cases
1. **Single point**: Return infinity
2. **Two points**: Return distance between them
3. **Collinear points**: Handle properly
4. **Duplicate points**: Return 0

### Precision Issues
- Use squared distances when possible
- Handle floating point comparisons carefully
- Consider using epsilon for comparisons

### Optimization Tips
- Avoid square root in comparisons
- Use early termination in strip search
- Optimize memory usage
- Consider using specialized data structures 