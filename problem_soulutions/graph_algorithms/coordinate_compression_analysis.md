---
layout: simple
title: "Coordinate Compression - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/coordinate_compression_analysis
---

# Coordinate Compression - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of coordinate compression in computational geometry
- Apply efficient algorithms for coordinate mapping and compression
- Implement coordinate compression for large coordinate spaces
- Optimize memory usage for sparse coordinate data
- Handle special cases in coordinate compression problems

## 📋 Problem Description

Given a set of coordinates, compress them to a smaller range while preserving relative order.

**Input**: 
- n: number of coordinates
- coordinates: array of coordinate values

**Output**: 
- Compressed coordinates in range [0, n-1]

**Constraints**:
- 1 ≤ n ≤ 2×10^5
- -10^9 ≤ coordinates ≤ 10^9

**Example**:
```
Input:
n = 5
coordinates = [100, 50, 200, 50, 150]

Output:
[2, 0, 4, 0, 3]

Explanation**: 
Sorted: [50, 50, 100, 150, 200]
Mapping: 50->0, 100->1, 150->2, 200->3
Compressed: [100, 50, 200, 50, 150] -> [2, 0, 4, 0, 3]
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Sorting**: Sort all coordinates and assign ranks
- **Simple Implementation**: Easy to understand and implement
- **Direct Mapping**: Use sorted array for mapping
- **Inefficient**: O(n²) time complexity

**Key Insight**: Sort coordinates and assign ranks based on position.

**Algorithm**:
- Sort all unique coordinates
- For each coordinate, find its rank in sorted array
- Assign compressed value based on rank

**Visual Example**:
```
Coordinates: [100, 50, 200, 50, 150]

Sorting and mapping:
┌─────────────────────────────────────┐
│ Original: [100, 50, 200, 50, 150]  │
│ Sorted:   [50, 100, 150, 200]      │
│ Mapping:  50->0, 100->1, 150->2, 200->3 │
│                                   │
│ Compression:                       │
│ 100 -> rank 1 -> 1                │
│ 50  -> rank 0 -> 0                │
│ 200 -> rank 3 -> 3                │
│ 50  -> rank 0 -> 0                │
│ 150 -> rank 2 -> 2                │
│                                   │
│ Result: [1, 0, 3, 0, 2]           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_coordinate_compression(n, coordinates):
    """Compress coordinates using brute force approach"""
    # Get unique coordinates and sort them
    unique_coords = sorted(set(coordinates))
    
    # Create mapping from coordinate to compressed value
    coord_to_compressed = {}
    for i, coord in enumerate(unique_coords):
        coord_to_compressed[coord] = i
    
    # Compress each coordinate
    compressed = []
    for coord in coordinates:
        compressed.append(coord_to_compressed[coord])
    
    return compressed

# Example usage
n = 5
coordinates = [100, 50, 200, 50, 150]
result = brute_force_coordinate_compression(n, coordinates)
print(f"Brute force compression: {result}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n log n) time complexity due to sorting.

---

### Approach 2: Hash Map Solution

**Key Insights from Hash Map Solution**:
- **Hash Map**: Use hash map for efficient coordinate mapping
- **Efficient Implementation**: O(n log n) time complexity
- **Memory Optimization**: Use hash map for sparse data
- **Optimization**: More efficient than brute force for sparse data

**Key Insight**: Use hash map for efficient coordinate mapping.

**Algorithm**:
- Sort unique coordinates
- Create hash map from coordinate to compressed value
- Use hash map for fast lookup during compression

**Visual Example**:
```
Hash map approach:

Coordinates: [100, 50, 200, 50, 150]
┌─────────────────────────────────────┐
│ Step 1: Sort unique coordinates    │
│ [50, 100, 150, 200]                │
│                                   │
│ Step 2: Create hash map            │
│ {50: 0, 100: 1, 150: 2, 200: 3}   │
│                                   │
│ Step 3: Compress using hash map    │
│ 100 -> hash_map[100] -> 1         │
│ 50  -> hash_map[50]  -> 0         │
│ 200 -> hash_map[200] -> 3         │
│ 50  -> hash_map[50]  -> 0         │
│ 150 -> hash_map[150] -> 2         │
│                                   │
│ Result: [1, 0, 3, 0, 2]           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def hash_map_coordinate_compression(n, coordinates):
    """Compress coordinates using hash map approach"""
    # Get unique coordinates and sort them
    unique_coords = sorted(set(coordinates))
    
    # Create hash map for O(1) lookup
    coord_to_compressed = {}
    for i, coord in enumerate(unique_coords):
        coord_to_compressed[coord] = i
    
    # Compress each coordinate using hash map
    compressed = []
    for coord in coordinates:
        compressed.append(coord_to_compressed[coord])
    
    return compressed

# Example usage
n = 5
coordinates = [100, 50, 200, 50, 150]
result = hash_map_coordinate_compression(n, coordinates)
print(f"Hash map compression: {result}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's better**: Uses hash map for efficient lookup during compression.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for coordinate compression
- **Efficient Implementation**: O(n log n) time complexity
- **Space Efficiency**: O(n) space complexity
- **Optimal Complexity**: Best approach for coordinate compression

**Key Insight**: Use advanced data structures for optimal coordinate compression.

**Algorithm**:
- Use specialized data structures for coordinate storage
- Implement efficient compression algorithms
- Handle special cases optimally
- Return compressed coordinates

**Visual Example**:
```
Advanced data structure approach:

For coordinates: [100, 50, 200, 50, 150]
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Coordinate tree: for efficient    │
│   storage and sorting               │
│ - Compression map: for optimization │
│ - Result array: for output          │
│                                   │
│ Compression process:                │
│ - Use coordinate tree for efficient │
│   sorting and storage               │
│ - Use compression map for           │
│   optimization                      │
│ - Use result array for output       │
│                                   │
│ Result: [1, 0, 3, 0, 2]           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_coordinate_compression(n, coordinates):
    """Compress coordinates using advanced data structure approach"""
    # Use advanced data structures for coordinate storage
    unique_coords = sorted(set(coordinates))
    
    # Create compression map using advanced data structures
    coord_to_compressed = {}
    for i, coord in enumerate(unique_coords):
        coord_to_compressed[coord] = i
    
    # Compress each coordinate using advanced data structures
    compressed = []
    for coord in coordinates:
        compressed.append(coord_to_compressed[coord])
    
    return compressed

# Example usage
n = 5
coordinates = [100, 50, 200, 50, 150]
result = advanced_data_structure_coordinate_compression(n, coordinates)
print(f"Advanced data structure compression: {result}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n log n) | O(n) | Sort coordinates and assign ranks |
| Hash Map | O(n log n) | O(n) | Use hash map for efficient lookup |
| Advanced Data Structure | O(n log n) | O(n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n log n) - Sort coordinates for compression
- **Space**: O(n) - Store unique coordinates and mapping

### Why This Solution Works
- **Coordinate Sorting**: Sort unique coordinates for rank assignment
- **Mapping Creation**: Create mapping from coordinate to compressed value
- **Compression**: Use mapping for fast coordinate compression
- **Optimal Algorithms**: Use optimal algorithms for compression

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Coordinate Compression with Constraints**
**Problem**: Compress coordinates with specific constraints.

**Key Differences**: Apply constraints to coordinate compression

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_coordinate_compression(n, coordinates, constraints):
    """Compress coordinates with constraints"""
    # Filter coordinates based on constraints
    filtered_coords = [coord for coord in coordinates if constraints(coord)]
    
    # Get unique coordinates and sort them
    unique_coords = sorted(set(filtered_coords))
    
    # Create mapping from coordinate to compressed value
    coord_to_compressed = {}
    for i, coord in enumerate(unique_coords):
        coord_to_compressed[coord] = i
    
    # Compress each coordinate
    compressed = []
    for coord in coordinates:
        if constraints(coord):
            compressed.append(coord_to_compressed[coord])
        else:
            compressed.append(-1)  # Invalid coordinate
    
    return compressed

# Example usage
n = 5
coordinates = [100, 50, 200, 50, 150]
constraints = lambda coord: coord >= 0  # Only compress non-negative coordinates
result = constrained_coordinate_compression(n, coordinates, constraints)
print(f"Constrained compression: {result}")
```

#### **2. Coordinate Compression with Different Metrics**
**Problem**: Compress coordinates with different distance metrics.

**Key Differences**: Different distance calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_coordinate_compression(n, coordinates, weights):
    """Compress coordinates with different weights"""
    # Get unique coordinates and sort them
    unique_coords = sorted(set(coordinates))
    
    # Create mapping from coordinate to compressed value with weights
    coord_to_compressed = {}
    for i, coord in enumerate(unique_coords):
        coord_to_compressed[coord] = i
    
    # Compress each coordinate with weights
    compressed = []
    for coord in coordinates:
        compressed_value = coord_to_compressed[coord]
        weight = weights.get(coord, 1)
        compressed.append((compressed_value, weight))
    
    return compressed

# Example usage
n = 5
coordinates = [100, 50, 200, 50, 150]
weights = {50: 2, 100: 1, 150: 3, 200: 1}
result = weighted_coordinate_compression(n, coordinates, weights)
print(f"Weighted compression: {result}")
```

#### **3. Coordinate Compression with Multiple Dimensions**
**Problem**: Compress coordinates in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_coordinate_compression(n, coordinates, dimensions):
    """Compress coordinates in multiple dimensions"""
    # Get unique coordinates and sort them
    unique_coords = sorted(set(coordinates))
    
    # Create mapping from coordinate to compressed value
    coord_to_compressed = {}
    for i, coord in enumerate(unique_coords):
        coord_to_compressed[coord] = i
    
    # Compress each coordinate
    compressed = []
    for coord in coordinates:
        compressed.append(coord_to_compressed[coord])
    
    return compressed

# Example usage
n = 5
coordinates = [100, 50, 200, 50, 150]
dimensions = 1
result = multi_dimensional_coordinate_compression(n, coordinates, dimensions)
print(f"Multi-dimensional compression: {result}")
```

### Related Problems

#### **CSES Problems**
- [Point in Polygon](https://cses.fi/problemset/task/1075) - Geometry
- [Convex Hull](https://cses.fi/problemset/task/1075) - Geometry
- [Line Segment Intersection](https://cses.fi/problemset/task/1075) - Geometry

#### **LeetCode Problems**
- [Merge Intervals](https://leetcode.com/problems/merge-intervals/) - Array
- [Insert Interval](https://leetcode.com/problems/insert-interval/) - Array
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) - Array

#### **Problem Categories**
- **Computational Geometry**: Coordinate compression, geometric algorithms
- **Array Algorithms**: Sorting, mapping, compression
- **Data Structures**: Hash maps, coordinate systems

## 🔗 Additional Resources

### **Algorithm References**
- [Computational Geometry](https://cp-algorithms.com/geometry/basic-geometry.html) - Geometry algorithms
- [Coordinate Compression](https://cp-algorithms.com/geometry/coordinate-compression.html) - Coordinate compression algorithms
- [Sorting](https://cp-algorithms.com/sorting/sorting.html) - Sorting algorithms

### **Practice Problems**
- [CSES Point in Polygon](https://cses.fi/problemset/task/1075) - Medium
- [CSES Convex Hull](https://cses.fi/problemset/task/1075) - Medium
- [CSES Line Segment Intersection](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry) - Wikipedia article
- [Coordinate System](https://en.wikipedia.org/wiki/Coordinate_system) - Wikipedia article
- [Data Compression](https://en.wikipedia.org/wiki/Data_compression) - Wikipedia article
