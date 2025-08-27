# CSES Coordinate Compression - Problem Analysis

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