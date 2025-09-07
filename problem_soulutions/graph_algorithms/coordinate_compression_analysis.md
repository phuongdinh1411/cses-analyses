---
layout: simple
title: "Coordinate Compression - Efficient Coordinate Mapping"
permalink: /problem_soulutions/graph_algorithms/coordinate_compression_analysis
---

# Coordinate Compression - Efficient Coordinate Mapping

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand coordinate compression and efficient coordinate mapping concepts
- Apply sorting and mapping techniques to compress coordinates while preserving relative order
- Implement efficient coordinate compression algorithms with proper sorting and mapping
- Optimize coordinate compression using sorting algorithms and efficient data structures
- Handle edge cases in coordinate compression (duplicate coordinates, large coordinate ranges, empty sets)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Coordinate compression, sorting algorithms, mapping techniques, data structure optimization
- **Data Structures**: Arrays, sorting data structures, mapping structures, coordinate tracking
- **Mathematical Concepts**: Coordinate geometry, sorting theory, mapping theory, optimization
- **Programming Skills**: Sorting implementation, coordinate manipulation, mapping techniques, algorithm implementation
- **Related Problems**: Sorting problems, Coordinate problems, Data structure optimization

## 📋 Problem Description

Given n points in a 2D plane, compress the coordinates so that the relative order is preserved but the coordinates are mapped to consecutive integers starting from 0.

**Input**: 
- First line: Integer n (number of points)
- Next n lines: Two integers x and y (coordinates of each point)

**Output**: 
- n lines with two integers each (compressed coordinates)

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- -10⁹ ≤ x, y ≤ 10⁹

**Example**:
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

**Explanation**: 
- x-coordinates: 1 → 0, 2 → 1, 3 → 2
- y-coordinates: 1 → 0, 4 → 1, 5 → 2
- Relative ordering is preserved in both dimensions

## 🎯 Visual Example

### Input Points
```
Points: (2,1), (1,4), (2,1), (3,5), (1,4)

Original coordinates:
Point 1: (2, 1)
Point 2: (1, 4)
Point 3: (2, 1)
Point 4: (3, 5)
Point 5: (1, 4)
```

### Coordinate Compression Process
```
Step 1: Extract unique coordinates
x-coordinates: [1, 2, 3]
y-coordinates: [1, 4, 5]

Step 2: Sort coordinates
x-coordinates: [1, 2, 3] → [0, 1, 2]
y-coordinates: [1, 4, 5] → [0, 1, 2]

Step 3: Create mapping
x-mapping: {1: 0, 2: 1, 3: 2}
y-mapping: {1: 0, 4: 1, 5: 2}

Step 4: Apply compression
Point 1: (2,1) → (1,0)
Point 2: (1,4) → (0,1)
Point 3: (2,1) → (1,0)
Point 4: (3,5) → (2,2)
Point 5: (1,4) → (0,1)
```

### Compression Visualization
```
Original coordinates:
(2,1) (1,4) (2,1) (3,5) (1,4)

Compressed coordinates:
(1,0) (0,1) (1,0) (2,2) (0,1)

Relative ordering preserved:
- x: 1 < 2 < 3 → 0 < 1 < 2
- y: 1 < 4 < 5 → 0 < 1 < 2
```

### Key Insight
Coordinate compression works by:
1. Extracting unique coordinate values
2. Sorting coordinates to determine relative order
3. Mapping to consecutive integers starting from 0
4. Preserving relative ordering between points
5. Time complexity: O(n log n) for sorting
6. Space complexity: O(n) for mapping

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Map large coordinate values to small consecutive integers
- **Key Insight**: Sort unique coordinates and create mapping dictionaries
- **Challenge**: Handle duplicate coordinates and preserve relative ordering

### Step 2: Brute Force Approach
**Try to map each coordinate individually:**

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

**Complexity**: O(n log n) - actually optimal for this problem

### Step 3: Optimization
**Use more efficient data structures and avoid redundant operations:**

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

**Key Insight**: Use set() to remove duplicates efficiently

### Step 4: Complete Solution

```python
def solve_coordinate_compression():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    result = coordinate_compression(n, points)
    for x, y in result:
        print(x, y)

def coordinate_compression(n, points):
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

if __name__ == "__main__":
    solve_coordinate_compression()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, [(2, 1), (1, 4), (2, 1), (3, 5), (1, 4)]), [(1, 0), (0, 1), (1, 0), (2, 2), (0, 1)]),
        ((3, [(1, 1), (2, 2), (3, 3)]), [(0, 0), (1, 1), (2, 2)]),
        ((4, [(0, 0), (0, 1), (1, 0), (1, 1)]), [(0, 0), (0, 1), (1, 0), (1, 1)]),
        ((2, [(1000000000, -1000000000), (-1000000000, 1000000000)]), [(1, 0), (0, 1)]),
        ((1, [(5, 5)]), [(0, 0)]),
    ]
    
    for (n, points), expected in test_cases:
        result = coordinate_compression(n, points)
        print(f"n={n}, points={points}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def coordinate_compression(n, points):
    x_coords = sorted(set(point[0] for point in points))
    y_coords = sorted(set(point[1] for point in points))
    
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    result = []
    for x, y in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        result.append((compressed_x, compressed_y))
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting unique coordinates
- **Space**: O(n) - storing unique coordinates and mappings

### Why This Solution Works
- **Sorting**: Ensures relative order is preserved
- **Set Operations**: Efficiently removes duplicates
- **Dictionary Mapping**: O(1) lookup for compression
- **Optimal Algorithm**: Best possible complexity for this problem

## 🎨 Visual Example

### Input Example
```
5 points:
Point 1: (2, 1)
Point 2: (1, 4)
Point 3: (2, 1)
Point 4: (3, 5)
Point 5: (1, 4)
```

### Coordinate Extraction
```
X-coordinates: [2, 1, 2, 3, 1]
Y-coordinates: [1, 4, 1, 5, 4]

Unique X-coordinates: {1, 2, 3}
Unique Y-coordinates: {1, 4, 5}
```

### Compression Process
```
Step 1: Sort unique X-coordinates
- Sorted X: [1, 2, 3]
- Mapping: 1 → 0, 2 → 1, 3 → 2

Step 2: Sort unique Y-coordinates
- Sorted Y: [1, 4, 5]
- Mapping: 1 → 0, 4 → 1, 5 → 2

Step 3: Apply compression
- Point 1: (2, 1) → (1, 0)
- Point 2: (1, 4) → (0, 1)
- Point 3: (2, 1) → (1, 0)
- Point 4: (3, 5) → (2, 2)
- Point 5: (1, 4) → (0, 1)
```

### Compression Visualization
```
Original coordinates:
(2,1) (1,4) (2,1) (3,5) (1,4)

Compressed coordinates:
(1,0) (0,1) (1,0) (2,2) (0,1)

Order preservation:
- X: 1 < 2 < 3 → 0 < 1 < 2 ✓
- Y: 1 < 4 < 5 → 0 < 1 < 2 ✓
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Set + Sort      │ O(n log n)   │ O(n)         │ Remove       │
│                 │              │              │ duplicates   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Hash Map        │ O(n log n)   │ O(n)         │ Direct       │
│                 │              │              │ mapping      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Binary Search   │ O(n log n)   │ O(n)         │ Find         │
│                 │              │              │ position     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## Key Insights

### 1. **Coordinate Compression Principle**
- **Value Mapping**: Map large coordinate values to small consecutive integers
- **Order Preservation**: Maintain relative ordering between coordinates
- **Efficiency**: Reduce coordinate space from potentially huge values to manageable integers
- **Memory Optimization**: Enable efficient storage and processing of large coordinate datasets

### 2. **Duplicate Handling Strategy**
- **Set Operations**: Use `set()` to efficiently remove duplicate coordinates in O(1) time
- **Unique Processing**: Only process unique coordinate values, reducing unnecessary work
- **Mapping Consistency**: Ensure consistent compression for identical coordinates
- **Space Efficiency**: Avoid storing redundant coordinate information

### 3. **Sorting for Ordering**
- **Relative Order**: Sort unique coordinates to maintain their relative ordering
- **Index Assignment**: Assign consecutive indices based on sorted order
- **Consistent Mapping**: Ensure deterministic compression results
- **Algorithm Correctness**: Critical for preserving spatial relationships

## 🎯 Problem Variations

### **Variation 1: Coordinate Compression with Custom Ordering**
**Problem**: Compress coordinates while preserving custom ordering (e.g., reverse order, specific priority).
```python
def coordinate_compression_custom_order(n, points, x_order='asc', y_order='asc'):
    # Extract coordinates
    x_coords = list(set(point[0] for point in points))
    y_coords = list(set(point[1] for point in points))
    
    # Sort with custom ordering
    if x_order == 'desc':
        x_coords.sort(reverse=True)
    else:
        x_coords.sort()
    
    if y_order == 'desc':
        y_coords.sort(reverse=True)
    else:
        y_coords.sort()
    
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

### **Variation 2: Multi-Dimensional Coordinate Compression**
**Problem**: Compress coordinates in 3D or higher dimensions.
```python
def multi_dimensional_compression(points, dimensions):
    # points = [(x1, x2, ..., xd), ...] for d dimensions
    # dimensions = number of dimensions
    
    # Extract coordinates for each dimension
    coord_lists = [[] for _ in range(dimensions)]
    for point in points:
        for i in range(dimensions):
            coord_lists[i].append(point[i])
    
    # Create mappings for each dimension
    mappings = []
    for coord_list in coord_lists:
        unique_coords = sorted(set(coord_list))
        coord_map = {coord: i for i, coord in enumerate(unique_coords)}
        mappings.append(coord_map)
    
    # Compress coordinates
    result = []
    for point in points:
        compressed_point = tuple(mappings[i][point[i]] for i in range(dimensions))
        result.append(compressed_point)
    
    return result
```

### **Variation 3: Dynamic Coordinate Compression**
**Problem**: Handle dynamic updates to the coordinate set while maintaining compression.
```python
class DynamicCoordinateCompressor:
    def __init__(self):
        self.x_coords = set()
        self.y_coords = set()
        self.x_mapping = {}
        self.y_mapping = {}
        self.points = []
        self.compressed = []
    
    def add_point(self, x, y):
        """Add a new point and update compression"""
        self.points.append((x, y))
        
        # Update coordinate sets
        if x not in self.x_coords:
            self.x_coords.add(x)
            self._rebuild_x_mapping()
        
        if y not in self.y_coords:
            self.y_coords.add(y)
            self._rebuild_y_mapping()
        
        # Update compressed coordinates
        compressed_x = self.x_mapping[x]
        compressed_y = self.y_mapping[y]
        self.compressed.append((compressed_x, compressed_y))
    
    def _rebuild_x_mapping(self):
        """Rebuild x-coordinate mapping after adding new coordinate"""
        sorted_x = sorted(self.x_coords)
        self.x_mapping = {x: i for i, x in enumerate(sorted_x)}
        # Recompress all points
        self._recompress_all()
    
    def _rebuild_y_mapping(self):
        """Rebuild y-coordinate mapping after adding new coordinate"""
        sorted_y = sorted(self.y_coords)
        self.y_mapping = {y: i for i, y in enumerate(sorted_y)}
        # Recompress all points
        self._recompress_all()
    
    def _recompress_all(self):
        """Recompress all points with updated mappings"""
        self.compressed = []
        for x, y in self.points:
            compressed_x = self.x_mapping[x]
            compressed_y = self.y_mapping[y]
            self.compressed.append((compressed_x, compressed_y))
    
    def get_compressed(self):
        return self.compressed
```

### **Variation 4: Coordinate Compression with Weights**
**Problem**: Compress coordinates while considering point weights or priorities.
```python
def weighted_coordinate_compression(points, weights):
    # weights = [w1, w2, ..., wn] - weight of each point
    
    # Extract coordinates
    x_coords = list(set(point[0] for point in points))
    y_coords = list(set(point[1] for point in points))
    
    # Sort coordinates (can be customized based on weights)
    x_coords.sort()
    y_coords.sort()
    
    # Create mappings
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates
    compressed = []
    for i, (x, y) in enumerate(points):
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        compressed.append((compressed_x, compressed_y, weights[i]))
    
    return compressed
```

### **Variation 5: Range-Based Coordinate Compression**
**Problem**: Compress coordinates within specific ranges or bounds.
```python
def range_based_compression(points, x_range, y_range):
    # x_range = (x_min, x_max), y_range = (y_min, y_max)
    
    # Filter points within range
    filtered_points = []
    for x, y in points:
        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            filtered_points.append((x, y))
    
    # Extract coordinates from filtered points
    x_coords = sorted(set(point[0] for point in filtered_points))
    y_coords = sorted(set(point[1] for point in filtered_points))
    
    # Create mappings
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates
    result = []
    for x, y in filtered_points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        result.append((compressed_x, compressed_y))
    
    return result
```
        y_coords.sort(reverse=True)
    else:
        y_coords.sort()
    
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

# Example usage
points = [(2, 1), (1, 4), (3, 5)]
result = coordinate_compression_custom_order(3, points, x_order='asc', y_order='desc')
print(f"Custom order compression: {result}")
```

### Variation 2: Multi-Dimensional Coordinate Compression
**Problem**: Compress coordinates in 3D or higher dimensions.

```python
def multi_dimensional_compression(n, points, dimensions):
    """
    Compress coordinates in arbitrary dimensions
    dimensions: list of dimension indices to compress
    """
    # Extract coordinates for each dimension
    coord_lists = {}
    for dim in dimensions:
        coord_lists[dim] = sorted(set(point[dim] for point in points))
    
    # Create mapping dictionaries
    maps = {}
    for dim in dimensions:
        maps[dim] = {coord: i for i, coord in enumerate(coord_lists[dim])}
    
    # Compress coordinates
    result = []
    for point in points:
        compressed_point = list(point)
        for dim in dimensions:
            compressed_point[dim] = maps[dim][point[dim]]
        result.append(tuple(compressed_point))
    
    return result

# Example usage
points_3d = [(1, 2, 3), (4, 5, 6), (1, 2, 9)]
result = multi_dimensional_compression(3, points_3d, [0, 1, 2])
print(f"3D compression: {result}")

# Compress only x and z dimensions
result_2d = multi_dimensional_compression(3, points_3d, [0, 2])
print(f"Partial compression: {result_2d}")
```

### Variation 3: Coordinate Compression with Weighted Mapping
**Problem**: Compress coordinates considering weights or frequencies of coordinates.

```python
def weighted_coordinate_compression(n, points, weights):
    """
    Compress coordinates considering weights
    weights: dictionary mapping (x, y) to weight
    """
    from collections import defaultdict
    
    # Group points by coordinates and sum weights
    coord_weights = defaultdict(int)
    for point in points:
        coord_weights[point] += weights.get(point, 1)
    
    # Sort coordinates by weight (descending)
    sorted_coords = sorted(coord_weights.items(), key=lambda x: x[1], reverse=True)
    
    # Create mapping dictionaries
    x_coords = sorted(set(point[0] for point, _ in sorted_coords))
    y_coords = sorted(set(point[1] for point, _ in sorted_coords))
    
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates
    result = []
    for x, y in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        result.append((compressed_x, compressed_y))
    
    return result

# Example usage
points = [(1, 1), (2, 2), (1, 1), (3, 3)]
weights = {(1, 1): 5, (2, 2): 3, (3, 3): 1}
result = weighted_coordinate_compression(4, points, weights)
print(f"Weighted compression: {result}")
```

### Variation 4: Dynamic Coordinate Compression
**Problem**: Maintain compressed coordinates as points are added/removed dynamically.

```python
class DynamicCoordinateCompressor:
    def __init__(self):
        self.x_coords = set()
        self.y_coords = set()
        self.x_map = {}
        self.y_map = {}
        self.points = []
    
    def add_point(self, x, y):
        """Add a new point and update compression"""
        self.points.append((x, y))
        self.x_coords.add(x)
        self.y_coords.add(y)
        self.update_compression()
    
    def remove_point(self, x, y):
        """Remove a point and update compression"""
        if (x, y) in self.points:
            self.points.remove((x, y))
            
            # Check if coordinates are still used
            if not any(px == x for px, _ in self.points):
                self.x_coords.discard(x)
            if not any(py == y for _, py in self.points):
                self.y_coords.discard(y)
            
            self.update_compression()
            return True
        return False
    
    def update_compression(self):
        """Update compression mappings"""
        sorted_x = sorted(self.x_coords)
        sorted_y = sorted(self.y_coords)
        
        self.x_map = {x: i for i, x in enumerate(sorted_x)}
        self.y_map = {y: i for i, y in enumerate(sorted_y)}
    
    def get_compressed_coordinates(self):
        """Get current compressed coordinates"""
        result = []
        for x, y in self.points:
            compressed_x = self.x_map[x]
            compressed_y = self.y_map[y]
            result.append((compressed_x, compressed_y))
        return result
    
    def get_compression_maps(self):
        """Get current compression mappings"""
        return self.x_map, self.y_map

# Example usage
compressor = DynamicCoordinateCompressor()
print(f"Initial state: {compressor.get_compressed_coordinates()}")

compressor.add_point(100, 200)
print(f"After adding (100, 200): {compressor.get_compressed_coordinates()}")

compressor.add_point(50, 150)
print(f"After adding (50, 150): {compressor.get_compressed_coordinates()}")

compressor.remove_point(100, 200)
print(f"After removing (100, 200): {compressor.get_compressed_coordinates()}")
```

### Variation 5: Coordinate Compression with Range Queries
**Problem**: Compress coordinates and support range queries on compressed space.

```python
class CompressedRangeQueries:
    def __init__(self, points):
        self.points = points
        self.compressed = self.compress_coordinates()
        self.x_coords = sorted(set(point[0] for point in points))
        self.y_coords = sorted(set(point[1] for point in points))
    
    def compress_coordinates(self):
        """Compress coordinates"""
        x_coords = sorted(set(point[0] for point in self.points))
        y_coords = sorted(set(point[1] for point in self.points))
        
        x_map = {x: i for i, x in enumerate(x_coords)}
        y_map = {y: i for i, y in enumerate(y_coords)}
        
        result = []
        for x, y in self.points:
            compressed_x = x_map[x]
            compressed_y = y_map[y]
            result.append((compressed_x, compressed_y))
        
        return result
    
    def query_range(self, x_min, x_max, y_min, y_max):
        """Query points in compressed range"""
        # Find compressed range bounds
        x_start = 0
        x_end = len(self.x_coords) - 1
        y_start = 0
        y_end = len(self.y_coords) - 1
        
        # Binary search for bounds
        for i, x in enumerate(self.x_coords):
            if x >= x_min:
                x_start = i
                break
        
        for i in range(len(self.x_coords) - 1, -1, -1):
            if self.x_coords[i] <= x_max:
                x_end = i
                break
        
        for i, y in enumerate(self.y_coords):
            if y >= y_min:
                y_start = i
                break
        
        for i in range(len(self.y_coords) - 1, -1, -1):
            if self.y_coords[i] <= y_max:
                y_end = i
                break
        
        # Find points in compressed range
        result = []
        for i, (cx, cy) in enumerate(self.compressed):
            if x_start <= cx <= x_end and y_start <= cy <= y_end:
                result.append(self.points[i])
        
        return result
    
    def get_compressed_bounds(self):
        """Get bounds of compressed space"""
        return {
            'x_range': (0, len(self.x_coords) - 1),
            'y_range': (0, len(self.y_coords) - 1),
            'x_coords': self.x_coords,
            'y_coords': self.y_coords
        }

# Example usage
points = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
compressor = CompressedRangeQueries(points)
print(f"Compressed coordinates: {compressor.compressed}")

# Query range in original coordinates
result = compressor.query_range(2, 4, 2, 4)
print(f"Points in range [2,4] x [2,4]: {result}")

bounds = compressor.get_compressed_bounds()
print(f"Compressed bounds: {bounds}")
```

## Related Problems

### **1. Grid and Coordinate Problems**
- **Labyrinth**: Grid-based pathfinding with coordinate compression
- **Counting Rooms**: Connected components in grid with large coordinates
- **Building Roads**: Graph connectivity in coordinate space

### **2. Range and Query Problems**
- **Range Sum Queries**: Efficient range queries on compressed coordinates
- **2D Range Queries**: Handling large coordinate spaces efficiently
- **Spatial Data Structures**: Building efficient spatial indexes

### **3. Graph Problems with Coordinates**
- **Shortest Path**: Finding paths in coordinate space
- **Minimum Spanning Tree**: Connecting points in coordinate space
- **Closest Pair**: Finding nearest neighbors efficiently

## 🎯 Key Insights

### Important Concepts and Patterns
- **Coordinate Compression**: Map large coordinate values to small consecutive integers
- **Set Operations**: Remove duplicates efficiently using set data structure
- **Dictionary Mapping**: Create O(1) lookup for coordinate compression
- **Relative Ordering**: Preserve spatial relationships during compression

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. 3D Coordinate Compression**
```python
def coordinate_compression_3d(n, points):
    # Handle 3D coordinate compression
    
    # Extract x, y, z coordinates
    x_coords = sorted(set(point[0] for point in points))
    y_coords = sorted(set(point[1] for point in points))
    z_coords = sorted(set(point[2] for point in points))
    
    # Create mapping dictionaries
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    z_map = {z: i for i, z in enumerate(z_coords)}
    
    # Compress coordinates
    result = []
    for x, y, z in points:
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        compressed_z = z_map[z]
        result.append((compressed_x, compressed_y, compressed_z))
    
    return result
```

#### **2. Coordinate Compression with Weights**
```python
def coordinate_compression_weighted(n, points, weights):
    # Handle coordinate compression with point weights
    
    # Extract coordinates
    x_coords = sorted(set(point[0] for point in points))
    y_coords = sorted(set(point[1] for point in points))
    
    # Create mapping dictionaries
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}
    
    # Compress coordinates with weights
    result = []
    for i, (x, y) in enumerate(points):
        compressed_x = x_map[x]
        compressed_y = y_map[y]
        weight = weights[i]
        result.append((compressed_x, compressed_y, weight))
    
    return result
```

#### **3. Dynamic Coordinate Compression**
```python
class DynamicCoordinateCompression:
    def __init__(self):
        self.x_coords = []
        self.y_coords = []
        self.x_map = {}
        self.y_map = {}
        self.next_x = 0
        self.next_y = 0
    
    def add_point(self, x, y):
        # Add x coordinate if new
        if x not in self.x_map:
            self.x_coords.append(x)
            self.x_map[x] = self.next_x
            self.next_x += 1
        
        # Add y coordinate if new
        if y not in self.y_map:
            self.y_coords.append(y)
            self.y_map[y] = self.next_y
            self.next_y += 1
        
        return (self.x_map[x], self.y_map[y])
    
    def compress_point(self, x, y):
        if x in self.x_map and y in self.y_map:
            return (self.x_map[x], self.y_map[y])
        return None
```

## 🔗 Related Problems

### Links to Similar Problems
- **Grid Problems**: Labyrinth, Counting Rooms, Building Roads
- **Range Queries**: Range Sum Queries, 2D Range Queries
- **Spatial Data**: Closest Pair, Minimum Spanning Tree
- **Graph Algorithms**: Shortest Path in coordinate space

## 📚 Learning Points

### Key Takeaways
- **Coordinate compression** efficiently handles large coordinate values
- **Set operations** remove duplicates in O(1) time
- **Dictionary mapping** provides O(1) coordinate lookup
- **Relative ordering** is preserved during compression

---

**This is a great introduction to coordinate compression and efficient coordinate mapping!** 🎯 