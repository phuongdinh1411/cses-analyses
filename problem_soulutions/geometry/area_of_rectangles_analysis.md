---
layout: simple
title: "Area of Rectangles - Geometry Analysis"
permalink: /problem_soulutions/geometry/area_of_rectangles_analysis
---


# Area of Rectangles - Geometry Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand rectangle union problems and area calculation with overlapping regions
- Apply sweep line algorithm or coordinate compression to compute union areas
- Implement efficient rectangle union algorithms with proper overlap handling
- Optimize area calculation using coordinate compression and event-driven processing
- Handle edge cases in rectangle union (no overlaps, complete overlaps, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sweep line algorithm, coordinate compression, rectangle union, area calculation
- **Data Structures**: Event queues, coordinate maps, interval trees, geometric data structures
- **Mathematical Concepts**: Rectangle geometry, area calculations, coordinate compression, interval arithmetic
- **Programming Skills**: Event processing, coordinate manipulation, area calculations, geometric computations
- **Related Problems**: Line Segment Intersection (sweep line), Polygon Area (area calculations), Rectangle geometry

## Problem Description

**Problem**: Given n rectangles, calculate the total area covered by all rectangles (union area).

**Input**: 
- n: number of rectangles
- n lines: x1 y1 x2 y2 (coordinates of rectangle corners)

**Output**: Total area covered by all rectangles.

**Constraints**:
- 1 ≤ n ≤ 1000
- -1000 ≤ x1, y1, x2, y2 ≤ 1000 for all coordinates
- All coordinates are integers
- x1 < x2 and y1 < y2 for each rectangle
- Rectangles may overlap

**Example**:
```
Input:
3
0 0 2 2
1 1 3 3
2 0 4 2

Output:
12

Explanation: 
Rectangle 1: (0,0) to (2,2) - area 4
Rectangle 2: (1,1) to (3,3) - area 4  
Rectangle 3: (2,0) to (4,2) - area 4
Total union area: 12 (no overlap)
```

## Visual Example

### Rectangle Visualization
```
Y
4 |     +---+---+
3 |     | 2 | 2 |
2 | +---+---+---+---+
1 | | 1 | 1+2| 2 | 3 |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Rectangle 1: (0,0) to (2,2) - area 4
Rectangle 2: (1,1) to (3,3) - area 4
Rectangle 3: (2,0) to (4,2) - area 4
```

### Sweep Line Process
```
Y
4 |     +---+---+
3 |     | 2 | 2 |
2 | +---+---+---+---+
1 | | 1 | 1+2| 2 | 3 |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Sweep line events:
x=0: Start Rectangle 1 → Active: [0,2]
x=1: Start Rectangle 2 → Active: [0,2], [1,3]
x=2: End Rectangle 1, Start Rectangle 3 → Active: [1,3], [0,2]
x=3: End Rectangle 2 → Active: [0,2]
x=4: End Rectangle 3 → Active: []
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Grid Check (Inefficient)

**Key Insights from Brute Force Solution:**
- Check every point in the coordinate space
- Mark covered points and count total area
- Simple but extremely inefficient for large rectangles
- Memory intensive for large coordinate ranges

**Algorithm:**
1. Create a grid covering all rectangle coordinates
2. For each rectangle, mark all covered grid points
3. Count total marked points to get area
4. Return total area

**Visual Example:**
```
Y
4 |     +---+---+
3 |     | 2 | 2 |
2 | +---+---+---+---+
1 | | 1 | 1+2| 2 | 3 |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Brute force: Check each grid point
Grid points: (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0), (3,1), (3,2), (4,0), (4,1), (4,2)
Total covered points: 12
```

**Implementation:**
```python
def area_of_rectangles_brute_force(rectangles):
    # Find coordinate bounds
    min_x = min(x1 for x1, y1, x2, y2 in rectangles)
    max_x = max(x2 for x1, y1, x2, y2 in rectangles)
    min_y = min(y1 for x1, y1, x2, y2 in rectangles)
    max_y = max(y2 for x1, y1, x2, y2 in rectangles)
    
    # Create grid
    grid = [[False for _ in range(max_y - min_y)] 
            for _ in range(max_x - min_x)]
    
    # Mark covered points
    for x1, y1, x2, y2 in rectangles:
        for x in range(x1, x2):
            for y in range(y1, y2):
                grid[x - min_x][y - min_y] = True
    
    # Count covered points
    total_area = 0
    for row in grid:
        total_area += sum(row)
    
    return total_area
```

**Time Complexity:** O(area) where area is the total coordinate space
**Space Complexity:** O(area) for the grid

**Why it's inefficient:**
- Time complexity depends on coordinate range, not number of rectangles
- Memory usage scales with coordinate space size
- Extremely slow for large rectangles or coordinate ranges
- Not scalable for competitive programming

### Approach 2: Rectangle Union with Interval Merging (Better)

**Key Insights from Interval Merging Solution:**
- Process rectangles by x-coordinate using sweep line
- Maintain active y-intervals and merge overlapping ones
- Calculate area contribution at each x-coordinate
- More efficient than brute force but still has limitations

**Algorithm:**
1. Sort rectangles by x-coordinate
2. For each x-coordinate, maintain active y-intervals
3. Merge overlapping intervals
4. Calculate area contribution: (x_diff) × (total_y_length)
5. Update active intervals for next x-coordinate

**Visual Example:**
```
Y
4 |     +---+---+
3 |     | 2 | 2 |
2 | +---+---+---+---+
1 | | 1 | 1+2| 2 | 3 |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Interval merging:
x=0: Active intervals: [0,2] → Area: 1×2 = 2
x=1: Active intervals: [0,2], [1,3] → Merged: [0,3] → Area: 1×3 = 3
x=2: Active intervals: [1,3], [0,2] → Merged: [0,3] → Area: 1×3 = 3
x=3: Active intervals: [0,2] → Area: 1×2 = 2
x=4: Active intervals: [] → Area: 1×0 = 0
Total: 2+3+3+2+0 = 10
```

**Implementation:**
```python
def area_of_rectangles_interval_merging(rectangles):
    events = []
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 'start', y1, y2))
        events.append((x2, 'end', y1, y2))
    
    events.sort()
    
    active_intervals = []
    total_area = 0
    prev_x = 0
    
    for x, event_type, y1, y2 in events:
        if x > prev_x:
            # Calculate total length of active intervals
            total_length = merge_intervals(active_intervals)
            total_area += (x - prev_x) * total_length
        
        if event_type == 'start':
            active_intervals.append((y1, y2))
        else:
            active_intervals.remove((y1, y2))
        
        prev_x = x
    
    return total_area

def merge_intervals(intervals):
    if not intervals:
        return 0
    
    intervals.sort()
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    return sum(end - start for start, end in merged)
```

**Time Complexity:** O(n² log n) due to interval merging
**Space Complexity:** O(n) for storing intervals

**Why it's better:**
- More efficient than brute force
- Time complexity independent of coordinate range
- Handles overlapping rectangles correctly
- Still has room for optimization

### Approach 3: Sweep Line with Segment Tree (Optimal)

**Key Insights from Sweep Line with Segment Tree Solution:**
- Use sweep line algorithm with coordinate compression
- Segment tree maintains active intervals efficiently
- O(n log n) time complexity is optimal for this problem
- Handles all edge cases and overlapping regions correctly

**Algorithm:**
1. Create events for rectangle start/end boundaries
2. Compress y-coordinates to reduce range
3. Sort events by x-coordinate
4. Use segment tree to maintain active intervals
5. Calculate area contribution at each event

**Visual Example:**
```
Y
4 |     +---+---+
3 |     | 2 | 2 |
2 | +---+---+---+---+
1 | | 1 | 1+2| 2 | 3 |
0 | +---+---+---+---+
  +---+---+---+---+---+
    0   1   2   3   4  X

Sweep line with segment tree:
x=0: Start Rectangle 1 → Segment tree: [0,2] active
x=1: Start Rectangle 2 → Segment tree: [0,2], [1,3] active
x=2: End Rectangle 1, Start Rectangle 3 → Segment tree: [1,3], [0,2] active
x=3: End Rectangle 2 → Segment tree: [0,2] active
x=4: End Rectangle 3 → Segment tree: [] active
```

**Implementation:**
```python
def area_of_rectangles_optimal(rectangles):
    events = []
    y_coords = set()
    
    # Create events for rectangle boundaries
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 'start', y1, y2))
        events.append((x2, 'end', y1, y2))
        y_coords.add(y1)
        y_coords.add(y2)
    
    # Sort y-coordinates for coordinate compression
    y_sorted = sorted(y_coords)
    y_to_idx = {y: i for i, y in enumerate(y_sorted)}
    
    # Sort events by x-coordinate
    events.sort()
    
    # Initialize segment tree
    n = len(y_sorted) - 1
    st = SegmentTree(n)
    
    total_area = 0
    prev_x = events[0][0] if events else 0
    
    for x, event_type, y1, y2 in events:
        # Calculate area covered so far
        if x > prev_x:
            covered_length = st.query(1, 0, n-1, 0, n-1)
            total_area += (x - prev_x) * covered_length
        
        # Update active intervals
        idx1 = y_to_idx[y1]
        idx2 = y_to_idx[y2] - 1
        if event_type == 'start':
            st.update_range(1, 0, n-1, idx1, idx2, 1)
        else:
            st.update_range(1, 0, n-1, idx1, idx2, -1)
        
        prev_x = x
    
    return total_area

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [0] * (4 * n)
    
    def update_range(self, node, start, end, left, right, val):
        if left > end or right < start:
            return
        
        if left <= start and right >= end:
            self.lazy[node] += val
            if self.lazy[node] > 0:
                self.tree[node] = end - start + 1
            else:
                self.tree[node] = 0
            return
        
        mid = (start + end) // 2
        self.update_range(2 * node, start, mid, left, right, val)
        self.update_range(2 * node + 1, mid + 1, end, left, right, val)
        
        if self.lazy[node] > 0:
            self.tree[node] = end - start + 1
        else:
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def query(self, node, start, end, left, right):
        if left > end or right < start:
            return 0
        
        if left <= start and right >= end:
            return self.tree[node]
        
        mid = (start + end) // 2
        return (self.query(2 * node, start, mid, left, right) + 
                self.query(2 * node + 1, mid + 1, end, left, right))
```

**Time Complexity:** O(n log n) where n is the number of rectangles
**Space Complexity:** O(n) for events and segment tree

**Why it's optimal:**
- Best known time complexity for rectangle union problems
- Uses coordinate compression to handle large coordinate ranges
- Segment tree efficiently maintains active intervals
- Handles all edge cases correctly
- Standard approach in competitive programming

## 🎯 Problem Variations

### Variation 1: Area of Rectangles with Weights
**Problem**: Each rectangle has a weight, calculate weighted area.

**Link**: [CSES Problem Set - Area of Rectangles with Weights](https://cses.fi/problemset/task/area_of_rectangles_weights)

```python
def area_of_rectangles_with_weights(rectangles_with_weights):
    events = []
    y_coords = set()
    
    # Create events with weights
    for (x1, y1, x2, y2), weight in rectangles_with_weights:
        events.append((x1, 'start', y1, y2, weight))
        events.append((x2, 'end', y1, y2, weight))
        y_coords.add(y1)
        y_coords.add(y2)
    
    y_sorted = sorted(y_coords)
    y_to_idx = {y: i for i, y in enumerate(y_sorted)}
    
    events.sort()
    
    n = len(y_sorted) - 1
    st = WeightedSegmentTree(n)
    
    total_area = 0
    prev_x = events[0][0] if events else 0
    
    for x, event_type, y1, y2, weight in events:
        if x > prev_x:
            covered_length = st.query(1, 0, n-1, 0, n-1)
            total_area += (x - prev_x) * covered_length
        
        idx1 = y_to_idx[y1]
        idx2 = y_to_idx[y2] - 1
        if event_type == 'start':
            st.update_range(1, 0, n-1, idx1, idx2, weight)
        else:
            st.update_range(1, 0, n-1, idx1, idx2, -weight)
        
        prev_x = x
    
    return total_area
```

### Variation 2: Area of Rectangles with Constraints
**Problem**: Calculate area subject to certain constraints.

**Link**: [CSES Problem Set - Area of Rectangles with Constraints](https://cses.fi/problemset/task/area_of_rectangles_constraints)

```python
def area_of_rectangles_with_constraints(rectangles, constraints):
    # Filter rectangles based on constraints
    filtered_rectangles = []
    for x1, y1, x2, y2 in rectangles:
        if check_constraints((x1, y1, x2, y2), constraints):
            filtered_rectangles.append((x1, y1, x2, y2))
    
    # Calculate area of filtered rectangles
    return area_of_rectangles_optimal(filtered_rectangles)

def check_constraints(rectangle, constraints):
    x1, y1, x2, y2 = rectangle
    if (x1 >= constraints["min_x"] and x2 <= constraints["max_x"] and
        y1 >= constraints["min_y"] and y2 <= constraints["max_y"]):
        return True
    return False
```

### Variation 3: Area of Rectangles with Dynamic Updates
**Problem**: Support adding/removing rectangles and calculating area.

**Link**: [CSES Problem Set - Area of Rectangles with Dynamic Updates](https://cses.fi/problemset/task/area_of_rectangles_dynamic)

```python
class DynamicRectangleArea:
    def __init__(self):
        self.rectangles = []
    
    def add_rectangle(self, x1, y1, x2, y2):
        self.rectangles.append((x1, y1, x2, y2))
    
    def remove_rectangle(self, x1, y1, x2, y2):
        if (x1, y1, x2, y2) in self.rectangles:
            self.rectangles.remove((x1, y1, x2, y2))
    
    def get_total_area(self):
        return area_of_rectangles_optimal(self.rectangles)
    
    def get_rectangle_count(self):
        return len(self.rectangles)
```

## 🔗 Related Problems

- **[Polygon Area](/cses-analyses/problem_soulutions/geometry/polygon_area_analysis/)**: Area calculation problems
- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/line_segment_intersection_analysis/)**: Intersection problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/convex_hull_analysis/)**: Geometric optimization
- **[Point in Polygon](/cses-analyses/problem_soulutions/geometry/point_in_polygon_analysis/)**: Point containment problems

## 📚 Learning Points

1. **Sweep Line Algorithm**: Essential for rectangle area problems
2. **Segment Tree**: Important for maintaining intervals
3. **Coordinate Compression**: Key for algorithm efficiency
4. **Geometric Optimization**: Important for performance
5. **Event Processing**: Critical for sweep line algorithms
6. **Interval Management**: Fundamental for area calculations

## 📝 Summary

The Area of Rectangles problem demonstrates advanced computational geometry concepts. We explored three approaches:

1. **Brute Force Grid Check**: O(area) time complexity, checks every grid point
2. **Rectangle Union with Interval Merging**: O(n² log n) time complexity, merges overlapping intervals
3. **Sweep Line with Segment Tree**: O(n log n) time complexity, optimal solution using coordinate compression

The key insights include using sweep line algorithms for efficiency, segment trees for interval management, and coordinate compression for handling large coordinate ranges. This problem serves as an excellent introduction to advanced geometric algorithms and spatial data structures.