---
layout: simple
title: "Coordinate Compression"
permalink: /cses-analyses/problem_soulutions/graph_algorithms/coordinate_compression_analysis
---


# Coordinate Compression

## Problem Statement
Given n points in a 2D plane, compress the coordinates so that the relative order is preserved but the coordinates are mapped to consecutive integers starting from 0.

### Input
The first input line has an integer n: the number of points.
Then there are n lines. Each line has two integers x and y: the coordinates of a point.

### Output
Print n lines. Each line should have two integers: the compressed coordinates of the corresponding point.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- -10^9 ≤ x,y ≤ 10^9

### Example
```
Input:
5
2 1
1 4
2 1
3 5
1 4

Output:
1 0
0 1
1 0
2 2
0 1
```

## Solution Progression

### Approach 1: Naive Sorting - O(n log n)
**Description**: Sort coordinates and assign compressed values.

```python
def coordinate_compression_naive(n, points):
    # Extract x and y coordinates
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    
    # Create sorted unique lists
    unique_x = sorted(set(x_coords))
    unique_y = sorted(set(y_coords))
    
    # Create mapping dictionaries
    x_map = {val: idx for idx, val in enumerate(unique_x)}
    y_map = {val: idx for idx, val in enumerate(unique_y)}
    
    # Compress coordinates
    compressed = []
    for x, y in points:
        compressed.append((x_map[x], y_map[y]))
    
    return compressed
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Compression - O(n log n)
**Description**: Use optimized coordinate compression with better structure.

```python
def coordinate_compression_optimized(n, points):
    # Extract and sort unique coordinates
    x_coords = sorted(set(point[0] for point in points))
    y_coords = sorted(set(point[1] for point in points))
    
    # Create mapping dictionaries
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates
    result = []
    for x, y in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        result.append((compressed_x, compressed_y))
    
    return result
```

**Why this improvement works**: We extract unique coordinates, sort them, and create mapping dictionaries to compress the coordinates while preserving relative order.

## Final Optimal Solution

```python
n = int(input())
points = []
for _ in range(n):
    x, y = map(int, input().split())
    points.append((x, y))

def compress_coordinates(n, points):
    # Extract and sort unique coordinates
    x_coords = sorted(set(point[0] for point in points))
    y_coords = sorted(set(point[1] for point in points))
    
    # Create mapping dictionaries
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates
    result = []
    for x, y in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        result.append((compressed_x, compressed_y))
    
    return result

result = compress_coordinates(n, points)
for x, y in result:
    print(x, y)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Sorting | O(n log n) | O(n) | Sort unique coordinates |
| Optimized Compression | O(n log n) | O(n) | Use mapping dictionaries |

## Key Insights for Other Problems

### 1. **Coordinate Compression**
**Principle**: Map large coordinate values to consecutive integers while preserving relative order.
**Applicable to**: Geometry problems, range problems, coordinate problems

### 2. **Mapping Dictionaries**
**Principle**: Use dictionaries to map original values to compressed indices.
**Applicable to**: Compression problems, mapping problems, indexing problems

### 3. **Relative Order Preservation**
**Principle**: Maintain the relative ordering of values while compressing to smaller ranges.
**Applicable to**: Ordering problems, compression problems, range problems

## Notable Techniques

### 1. **Coordinate Extraction**
```python
def extract_coordinates(points):
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    return x_coords, y_coords
```

### 2. **Unique Sorting**
```python
def sort_unique_coordinates(coords):
    return sorted(set(coords))
```

### 3. **Mapping Creation**
```python
def create_mapping(unique_coords):
    return {val: idx for idx, val in enumerate(unique_coords)}
```

### 4. **Coordinate Compression**
```python
def compress_single_coordinate(coord, mapping):
    return mapping[coord]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a coordinate compression problem
2. **Extract coordinates**: Separate x and y coordinates from points
3. **Find unique values**: Get unique x and y coordinates
4. **Sort coordinates**: Sort unique coordinates to maintain order
5. **Create mappings**: Build dictionaries mapping original to compressed values
6. **Compress points**: Apply mappings to each point
7. **Return result**: Output compressed coordinates

---

*This analysis shows how to efficiently compress coordinates while preserving relative order using sorting and mapping.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Coordinate Compression with Costs**
**Variation**: Each coordinate has a cost associated with compression.
**Approach**: Use weighted compression based on costs.
```python
def cost_based_coordinate_compression(n, points, costs):
    # costs[(x, y)] = cost of compressing point (x, y)
    
    # Extract coordinates with costs
    x_coords = []
    y_coords = []
    point_costs = []
    
    for x, y in points:
        cost = costs.get((x, y), 1)
        x_coords.append(x)
        y_coords.append(y)
        point_costs.append(cost)
    
    # Sort by cost for priority compression
    sorted_indices = sorted(range(n), key=lambda i: point_costs[i])
    
    # Create mappings with cost consideration
    unique_x = sorted(set(x_coords))
    unique_y = sorted(set(y_coords))
    
    x_map = {x: i for i, x in enumerate(unique_x)}
    y_map = {y: i for i, y in enumerate(unique_y)}
    
    # Compress coordinates
    result = []
    total_cost = 0
    for i in sorted_indices:
        x, y = points[i]
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        total_cost += point_costs[i]
        result.append((compressed_x, compressed_y))
    
    return result, total_cost
```

#### 2. **Coordinate Compression with Constraints**
**Variation**: Certain coordinates must be compressed to specific values.
**Approach**: Use constraint satisfaction with coordinate mapping.
```python
def constrained_coordinate_compression(n, points, constraints):
    # constraints = {(x, y): target_compressed_value}
    
    # Extract coordinates
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    
    # Handle constraints first
    used_compressed_values = set()
    result = []
    
    for i, (x, y) in enumerate(points):
        if (x, y) in constraints:
            target = constraints[(x, y)]
            used_compressed_values.add(target)
            result.append((target, target))  # Simplified for 2D
        else:
            result.append(None)  # Placeholder
    
    # Compress remaining coordinates
    remaining_x = sorted(set(x for i, (x, y) in enumerate(points) if result[i] is None))
    remaining_y = sorted(set(y for i, (x, y) in enumerate(points) if result[i] is None))
    
    x_map = {}
    y_map = {}
    next_x = 0
    next_y = 0
    
    for x in remaining_x: while next_x in 
used_compressed_values: next_x += 1
        x_map[x] = next_x
        next_x += 1
    
    for y in remaining_y: while next_y in 
used_compressed_values: next_y += 1
        y_map[y] = next_y
        next_y += 1
    
    # Fill in remaining results
    for i, (x, y) in enumerate(points):
        if result[i] is None:
            result[i] = (x_map[x], y_map[y])
    
    return result
```

#### 3. **Coordinate Compression with Probabilities**
**Variation**: Each coordinate has a probability of being compressed.
**Approach**: Use probabilistic compression with Monte Carlo simulation.
```python
def probabilistic_coordinate_compression(n, points, probabilities):
    # probabilities[(x, y)] = probability of compressing point (x, y)
    
    def monte_carlo_compression(trials=1000):
        successful_compressions = 0
        
        for _ in range(trials):
            if can_compress_with_probabilities(n, points, probabilities):
                successful_compressions += 1
        
        return successful_compressions / trials
    
    def can_compress_with_probabilities(n, points, probs):
        # Simplified simulation
        compressed_points = []
        for x, y in points:
            if random.random() < probs.get((x, y), 1.0):
                compressed_points.append((x, y))
        
        # Check if compression is valid
        if len(compressed_points) == 0:
            return False
        
        # Perform actual compression
        x_coords = sorted(set(point[0] for point in compressed_points))
        y_coords = sorted(set(point[1] for point in compressed_points))
        
        x_map = {x: i for i, x in enumerate(x_coords)}
        y_map = {y: i for i, y in enumerate(y_coords)}
        
        return len(x_map) > 0 and len(y_map) > 0
    
    return monte_carlo_compression()
```

#### 4. **Coordinate Compression with Multiple Dimensions**
**Variation**: Compress coordinates in higher dimensions (3D, 4D, etc.).
**Approach**: Extend the algorithm to handle multiple dimensions.
```python
def multi_dimensional_coordinate_compression(n, points, dimensions):
    # points = [(x1, x2, ..., xd), ...] for d dimensions
    
    # Extract coordinates for each dimension
    coord_lists = [[] for _ in range(dimensions)]
    for point in points:
        for i in range(dimensions):
            coord_lists[i].append(point[i])
    
    # Create mappings for each dimension
    mappings = []
    for i in range(dimensions):
        unique_coords = sorted(set(coord_lists[i]))
        mapping = {coord: idx for idx, coord in enumerate(unique_coords)}
        mappings.append(mapping)
    
    # Compress coordinates
    result = []
    for point in points:
        compressed_point = tuple(mappings[i][point[i]] for i in range(dimensions))
        result.append(compressed_point)
    
    return result
```

#### 5. **Coordinate Compression with Dynamic Updates**
**Variation**: Points can be added or removed dynamically.
**Approach**: Use dynamic data structures for efficient updates.
```python
class DynamicCoordinateCompressor:
    def __init__(self):
        self.x_coords = set()
        self.y_coords = set()
        self.x_map = {}
        self.y_map = {}
        self.reverse_x_map = {}
        self.reverse_y_map = {}
    
    def add_point(self, x, y):
        # Add new coordinates
        if x not in self.x_coords:
            self.x_coords.add(x)
            new_x_idx = len(self.x_map)
            self.x_map[x] = new_x_idx
            self.reverse_x_map[new_x_idx] = x
        
        if y not in self.y_coords:
            self.y_coords.add(y)
            new_y_idx = len(self.y_map)
            self.y_map[y] = new_y_idx
            self.reverse_y_map[new_y_idx] = y
        
        return (self.x_map[x], self.y_map[y])
    
    def remove_point(self, x, y):
        # Remove coordinates if no other points use them
        # This is a simplified version - in practice would need reference counting
        pass
    
    def compress_point(self, x, y):
        if x in self.x_map and y in self.y_map:
            return (self.x_map[x], self.y_map[y])
        else:
            return self.add_point(x, y)
```

### Related Problems & Concepts

#### 1. **Compression Problems**
- **Data Compression**: Huffman coding, LZ77, LZ78
- **Image Compression**: JPEG, PNG, GIF
- **Text Compression**: Run-length encoding
- **Coordinate Compression**: Spatial indexing

#### 2. **Mapping Problems**
- **Hash Tables**: Key-value mapping
- **Bijective Functions**: One-to-one mappings
- **Index Mapping**: Array reindexing
- **Coordinate Systems**: Cartesian, polar, spherical

#### 3. **Sorting Problems**
- **Comparison Sorting**: Merge sort, quick sort
- **Counting Sort**: Integer sorting
- **Radix Sort**: Digit-based sorting
- **Topological Sort**: DAG ordering

#### 4. **Geometry Problems**
- **Point Location**: Finding points in regions
- **Convex Hull**: Boundary computation
- **Voronoi Diagrams**: Region partitioning
- **Delaunay Triangulation**: Triangle mesh

#### 5. **Range Problems**
- **Range Queries**: Segment trees, BIT
- **Range Updates**: Lazy propagation
- **Range Compression**: Coordinate mapping
- **Range Counting**: Frequency queries

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large datasets
- **Edge Cases**: Robust compression

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On coordinate space
- **Two Pointers**: Efficient coordinate processing
- **Sliding Window**: Optimal coordinate ranges
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Combinatorics**
- **Permutations**: Coordinate ordering
- **Combinations**: Point selection
- **Partitions**: Coordinate grouping
- **Catalan Numbers**: Valid coordinate sequences

#### 2. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special coordinate cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime coordinates

#### 3. **Linear Algebra**
- **Vector Spaces**: Coordinate transformations
- **Matrix Operations**: Linear mappings
- **Eigenvalues**: Coordinate scaling
- **Orthogonal Transformations**: Rotation, reflection

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Geometry and coordinate problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Geometry Problems**: Point location, convex hull
- **Compression Problems**: Data compression, coordinate mapping
- **Sorting Problems**: Various sorting algorithms
- **Range Problems**: Segment trees, coordinate compression 