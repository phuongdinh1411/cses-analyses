---
layout: simple
title: "Area of Rectangles - Geometry Analysis"
permalink: /problem_soulutions/geometry/area_of_rectangles_analysis
---


# Area of Rectangles - Geometry Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand rectangle union problems and area calculation with overlapping regions
- [ ] **Objective 2**: Apply sweep line algorithm or coordinate compression to compute union areas
- [ ] **Objective 3**: Implement efficient rectangle union algorithms with proper overlap handling
- [ ] **Objective 4**: Optimize area calculation using coordinate compression and event-driven processing
- [ ] **Objective 5**: Handle edge cases in rectangle union (no overlaps, complete overlaps, boundary conditions)

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Calculate total area covered by multiple rectangles
- Handle overlapping rectangles correctly
- Use efficient geometric algorithms
- Apply sweep line technique

**Key Observations:**
- Brute force O(area) is too slow for large rectangles
- Sweep line algorithm provides O(n log n) complexity
- Need to handle overlapping regions properly
- Segment tree maintains active intervals

### Step 2: Sweep Line Algorithm Approach
**Idea**: Use sweep line algorithm with segment tree to efficiently calculate union area by processing events in order.

```python
def area_of_rectangles_sweep_line(rectangles):
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
```

**Why this works:**
- Sweep line processes events in order
- Segment tree maintains active intervals efficiently
- O(n log n) time complexity is optimal
- Handles overlapping regions correctly

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_area_of_rectangles():
    n = int(input())
    rectangles = []
    
    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        rectangles.append((x1, y1, x2, y2))
    
    result = calculate_total_area(rectangles)
    print(result)

def calculate_total_area(rectangles):
    """Calculate total area covered by rectangles using sweep line"""
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

# Main execution
if __name__ == "__main__":
    solve_area_of_rectangles()
```

**Why this works:**
- Optimal sweep line algorithm approach
- Handles all edge cases correctly
- Efficient area calculation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(0, 0, 2, 2), (1, 1, 3, 3), (2, 0, 4, 2)], 12),  # 3 rectangles, no overlap
        ([(0, 0, 2, 2), (1, 1, 3, 3)], 7),                   # 2 rectangles with overlap
        ([(0, 0, 1, 1), (1, 1, 2, 2)], 2),                   # 2 rectangles, touching
        ([(0, 0, 2, 2)], 4),                                   # 1 rectangle
    ]
    
    for rectangles, expected in test_cases:
        result = solve_test(rectangles)
        print(f"Rectangles: {rectangles}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(rectangles):
    return calculate_total_area(rectangles)

def calculate_total_area(rectangles):
    events = []
    y_coords = set()
    
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 'start', y1, y2))
        events.append((x2, 'end', y1, y2))
        y_coords.add(y1)
        y_coords.add(y2)
    
    y_sorted = sorted(y_coords)
    y_to_idx = {y: i for i, y in enumerate(y_sorted)}
    
    events.sort()
    
    n = len(y_sorted) - 1
    st = SegmentTree(n)
    
    total_area = 0
    prev_x = events[0][0] if events else 0
    
    for x, event_type, y1, y2 in events:
        if x > prev_x:
            covered_length = st.query(1, 0, n-1, 0, n-1)
            total_area += (x - prev_x) * covered_length
        
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - dominated by sorting events and segment tree operations
- **Space**: O(n) - for storing events and segment tree

### Why This Solution Works
- **Sweep Line Algorithm**: Efficiently processes rectangle boundaries
- **Segment Tree**: Maintains active intervals efficiently
- **Coordinate Compression**: Reduces y-coordinate range
- **Optimal Algorithm**: Best known approach for this problem

## 🎨 Visual Example

### Input Example
```
3 rectangles:
Rectangle 1: (0,0) to (2,2)
Rectangle 2: (1,1) to (3,3)
Rectangle 3: (2,0) to (4,2)
```

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

### Sweep Line Events
```
Events (sorted by x-coordinate):
1. x=0: Start Rectangle 1, y=[0,2]
2. x=1: Start Rectangle 2, y=[1,3]
3. x=2: End Rectangle 1, y=[0,2]
4. x=2: Start Rectangle 3, y=[0,2]
5. x=3: End Rectangle 2, y=[1,3]
6. x=4: End Rectangle 3, y=[0,2]

Active intervals at each x:
x=0: [0,2] → area = 2
x=1: [0,2], [1,3] → area = 3
x=2: [1,3], [0,2] → area = 3
x=3: [0,2] → area = 2
x=4: [] → area = 0
```

### Step-by-Step Sweep Line Process
```
Step 1: x=0, Start Rectangle 1
Active intervals: [0,2]
Area contribution: 2 × 1 = 2
Total area: 2

Step 2: x=1, Start Rectangle 2
Active intervals: [0,2], [1,3]
Merged intervals: [0,3]
Area contribution: 3 × 1 = 3
Total area: 2 + 3 = 5

Step 3: x=2, End Rectangle 1, Start Rectangle 3
Active intervals: [1,3], [0,2]
Merged intervals: [0,3]
Area contribution: 3 × 1 = 3
Total area: 5 + 3 = 8

Step 4: x=3, End Rectangle 2
Active intervals: [0,2]
Area contribution: 2 × 1 = 2
Total area: 8 + 2 = 10

Step 5: x=4, End Rectangle 3
Active intervals: []
Area contribution: 0 × 1 = 0
Total area: 10 + 0 = 10
```

### Coordinate Compression
```
Original y-coordinates: [0, 1, 2, 3]
Compressed mapping:
0 → 0
1 → 1
2 → 2
3 → 3

Compressed range: [0, 3] (4 values)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(area)      │ O(1)         │ Check each   │
│                 │              │              │ point        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sweep Line      │ O(n log n)   │ O(n)         │ Process      │
│                 │              │              │ events       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Segment Tree    │ O(n log n)   │ O(n)         │ Maintain     │
│                 │              │              │ intervals    │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Sweep Line Algorithm**
- Process events in order of x-coordinates
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Segment Tree for Intervals**
- Maintains active y-intervals efficiently
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Coordinate Compression**
- Reduce y-coordinate range for efficiency
- Important for understanding
- Fundamental concept
- Essential for performance

## 🎯 Problem Variations

### Variation 1: Area of Rectangles with Weights
**Problem**: Each rectangle has a weight, calculate weighted area.

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

# Example usage
rectangles_with_weights = [
    ((0, 0, 2, 2), 3),
    ((1, 1, 3, 3), 2),
    ((2, 0, 4, 2), 1)
]
result = area_of_rectangles_with_weights(rectangles_with_weights)
print(f"Weighted area: {result}")
```

### Variation 2: Area of Rectangles with Constraints
**Problem**: Calculate area subject to certain constraints.

```python
def area_of_rectangles_with_constraints(rectangles, constraints):
    # Filter rectangles based on constraints
    filtered_rectangles = []
    for x1, y1, x2, y2 in rectangles:
        if check_constraints((x1, y1, x2, y2), constraints):
            filtered_rectangles.append((x1, y1, x2, y2))
    
    # Calculate area of filtered rectangles
    return calculate_total_area(filtered_rectangles)

def check_constraints(rectangle, constraints):
    x1, y1, x2, y2 = rectangle
    if (x1 >= constraints["min_x"] and x2 <= constraints["max_x"] and
        y1 >= constraints["min_y"] and y2 <= constraints["max_y"]):
        return True
    return False

# Example usage
constraints = {"min_x": 0, "max_x": 5, "min_y": 0, "max_y": 5}
result = area_of_rectangles_with_constraints(rectangles, constraints)
print(f"Constrained area: {result}")
```

### Variation 3: Area of Rectangles with Dynamic Updates
**Problem**: Support adding/removing rectangles and calculating area.

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
        return calculate_total_area(self.rectangles)
    
    def get_rectangle_count(self):
        return len(self.rectangles)

# Example usage
dynamic_system = DynamicRectangleArea()
dynamic_system.add_rectangle(0, 0, 2, 2)
dynamic_system.add_rectangle(1, 1, 3, 3)
area = dynamic_system.get_total_area()
count = dynamic_system.get_rectangle_count()
print(f"Dynamic area: {area}, Rectangle count: {count}")
```

### Variation 4: Area of Rectangles with Range Queries
**Problem**: Answer queries about area in specific ranges.

```python
def area_of_rectangles_range_queries(rectangles, queries):
    results = []
    
    for min_x, max_x, min_y, max_y in queries:
        # Filter rectangles in range
        filtered_rectangles = []
        for x1, y1, x2, y2 in rectangles:
            if (min_x <= x1 <= max_x or min_x <= x2 <= max_x or
                x1 <= min_x <= x2 or x1 <= max_x <= x2) and \
               (min_y <= y1 <= max_y or min_y <= y2 <= max_y or
                y1 <= min_y <= y2 or y1 <= max_y <= y2):
                # Clip rectangle to range
                clip_x1 = max(x1, min_x)
                clip_y1 = max(y1, min_y)
                clip_x2 = min(x2, max_x)
                clip_y2 = min(y2, max_y)
                if clip_x1 < clip_x2 and clip_y1 < clip_y2:
                    filtered_rectangles.append((clip_x1, clip_y1, clip_x2, clip_y2))
        
        # Calculate area of filtered rectangles
        area = calculate_total_area(filtered_rectangles)
        results.append(area)
    
    return results

# Example usage
queries = [(0, 2, 0, 2), (1, 3, 1, 3), (0, 4, 0, 4)]
result = area_of_rectangles_range_queries(rectangles, queries)
print(f"Range query results: {result}")
```

### Variation 5: Area of Rectangles with Convex Hull
**Problem**: Use convex hull to optimize area calculation.

```python
def area_of_rectangles_convex_hull(points):
    if len(points) < 3:
        return 0
    
    # Build convex hull
    hull = build_convex_hull(points)
    
    # Convert hull to rectangles (simplified approach)
    rectangles = []
    for i in range(len(hull)):
        p1 = hull[i]
        p2 = hull[(i + 1) % len(hull)]
        # Create rectangle from hull edge
        x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
        x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
        rectangles.append((x1, y1, x2, y2))
    
    # Calculate area
    return calculate_total_area(rectangles)

def build_convex_hull(points):
    if len(points) < 3:
        return points
    
    leftmost = min(points, key=lambda p: p[0])
    
    def polar_angle(p):
        if p == leftmost:
            return -float('inf')
        return math.atan2(p[1] - leftmost[1], p[0] - leftmost[0])
    
    sorted_points = sorted(points, key=polar_angle)
    
    hull = [leftmost, sorted_points[0]]
    for point in sorted_points[1:]:
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    
    return hull

def cross_product(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

# Example usage
points = [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.5)]
result = area_of_rectangles_convex_hull(points)
print(f"Convex hull area: {result}")
```

## 🔗 Related Problems

- **[Polygon Area](/cses-analyses/problem_soulutions/geometry/)**: Area calculation problems
- **[Line Segment Intersection](/cses-analyses/problem_soulutions/geometry/)**: Intersection problems
- **[Convex Hull](/cses-analyses/problem_soulutions/geometry/)**: Geometric optimization

## 📚 Learning Points

1. **Sweep Line Algorithm**: Essential for rectangle area problems
2. **Segment Tree**: Important for maintaining intervals
3. **Coordinate Compression**: Key for algorithm efficiency
4. **Geometric Optimization**: Important for performance

---

**This is a great introduction to rectangle area algorithms!** 🎯
        
        if event_type == 'start':
            st.update_range(1, 0, n - 1, idx1, idx2, 1)
        else:
            st.update_range(1, 0, n - 1, idx1, idx2, -1)
        
        prev_x = x
    
    return total_area

# Read input
n = int(input())
rectangles = []
for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    rectangles.append((x1, y1, x2, y2))

result = area_of_rectangles(rectangles)
print(result)
```

## Complexity Analysis
- **Time Complexity**: O(n log n) where n is number of rectangles
- **Space Complexity**: O(n)

## Key Insights for Other Problems

### **Principles**:
1. **Sweep Line Algorithm**: Efficient for area calculation problems
2. **Coordinate Compression**: Map coordinates to indices for efficiency
3. **Segment Tree**: Maintain active intervals efficiently

### **Applicability**:
- Area calculation problems
- Geometric algorithms
- Computational geometry
- Sweep line problems

### **Example Problems**:
- Union of rectangles
- Geometric algorithms
- Computational geometry
- Area-based problems

## Notable Techniques

### **Code Patterns**:
```python
# Sweep line for area calculation
def sweep_line_area(rectangles):
    events = []
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 'start', y1, y2))
        events.append((x2, 'end', y1, y2))
    
    events.sort()
    active_intervals = []
    total_area = 0
    prev_x = 0
    
    for x, event_type, y1, y2 in events: if x > 
prev_x: covered_length = calculate_covered_length(active_intervals)
            total_area += (x - prev_x) * covered_length
        
        if event_type == 'start':
            active_intervals.append((y1, y2))
        else:
            active_intervals.remove((y1, y2))
        
        prev_x = x
    
    return total_area

# Coordinate compression
def compress_coordinates(coords):
    sorted_coords = sorted(set(coords))
    return {coord: i for i, coord in enumerate(sorted_coords)}
```

## Problem-Solving Framework

### **1. Understand the Geometry**
- Visualize sweep line process
- Understand area calculation
- Consider coordinate compression

### **2. Choose the Right Tool**
- Sweep line for efficiency
- Segment tree for interval management
- Coordinate compression for large coordinates

### **3. Handle Edge Cases**
- Overlapping rectangles
- Degenerate rectangles
- Large coordinate values

### **4. Optimize for Performance**
- Use efficient data structures
- Compress coordinates
- Minimize memory usage 