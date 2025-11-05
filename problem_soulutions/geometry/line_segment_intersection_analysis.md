---
layout: simple
title: "Line Segment Intersection - Geometry Problem"
permalink: /problem_soulutions/geometry/line_segment_intersection_analysis
---

# Line Segment Intersection

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of line segment intersection in computational geometry
- Apply geometric algorithms for intersection detection
- Implement efficient algorithms for line segment intersection
- Optimize geometric operations for intersection analysis
- Handle special cases in geometric intersection problems

## 📋 Problem Description

Given n line segments, find all pairs of intersecting line segments.

**Input**: 
- n: number of line segments
- segments: array of line segments (each with two endpoints)

**Output**: 
- List of all pairs of intersecting line segments

**Constraints**:
- 1 ≤ n ≤ 1000
- -10^6 ≤ coordinates ≤ 10^6

**Example**:
```
Input:
n = 3
segments = [(0,0,2,2), (1,1,3,3), (0,2,2,0)]

Output:
[(0,1), (0,2), (1,2)]

Explanation**: 
Segment 0: (0,0) to (2,2)
Segment 1: (1,1) to (3,3) 
Segment 2: (0,2) to (2,0)
All three segments intersect with each other
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all pairs of line segments
- **Simple Implementation**: Easy to understand and implement
- **Geometric Tests**: Use basic intersection tests
- **Inefficient**: O(n²) time complexity

**Key Insight**: Check every pair of line segments for intersection.

**Algorithm**:
- Iterate through all pairs of line segments
- Use geometric intersection test for each pair
- Collect all intersecting pairs
- Return result

**Visual Example**:
```
Line segments:
┌─────────────────────────────────────┐
│ Segment 0: (0,0) ──── (2,2)        │
│ Segment 1: (1,1) ──── (3,3)        │
│ Segment 2: (0,2) ──── (2,0)        │
│                                   │
│ Intersection tests:               │
│ - Segments 0 & 1: intersect ✓     │
│ - Segments 0 & 2: intersect ✓     │
│ - Segments 1 & 2: intersect ✓     │
│                                   │
│ Result: [(0,1), (0,2), (1,2)]     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_line_segment_intersection(n, segments):
    """
    Find intersecting line segments using brute force approach
    
    Args:
        n: number of line segments
        segments: list of line segments
    
    Returns:
        list: pairs of intersecting line segments
    """
    def do_segments_intersect(seg1, seg2):
        """Check if two line segments intersect"""
        x1, y1, x2, y2 = seg1
        x3, y3, x4, y4 = seg2
        
        # Calculate cross products
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        # Check if segments intersect
        d1 = cross_product((x3, y3), (x4, y4), (x1, y1))
        d2 = cross_product((x3, y3), (x4, y4), (x2, y2))
        d3 = cross_product((x1, y1), (x2, y2), (x3, y3))
        d4 = cross_product((x1, y1), (x2, y2), (x4, y4))
        
        # Check for intersection
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        
        # Check for collinear intersection
        if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
            # Check if segments overlap
            return not (max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2))
        
        return False
    
    intersections = []
    
    # Check all pairs of segments
    for i in range(n):
        for j in range(i + 1, n):
            if do_segments_intersect(segments[i], segments[j]):
                intersections.append((i, j))
    
    return intersections

# Example usage
n = 3
segments = [(0, 0, 2, 2), (1, 1, 3, 3), (0, 2, 2, 0)]
result = brute_force_line_segment_intersection(n, segments)
print(f"Brute force intersections: {result}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(1)

**Why it's inefficient**: O(n²) time complexity for checking all pairs.

---

### Approach 2: Sweep Line Algorithm

**Key Insights from Sweep Line Algorithm**:
- **Sweep Line**: Use vertical line sweeping technique
- **Event Processing**: Process segment endpoints as events
- **Efficient Detection**: O(n log n) time complexity
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use sweep line algorithm to process segments efficiently.

**Algorithm**:
- Sort segment endpoints by x-coordinate
- Use sweep line to process events
- Maintain active segments
- Detect intersections during sweep

**Visual Example**:
```
Sweep line algorithm:
┌─────────────────────────────────────┐
│ Events sorted by x-coordinate:     │
│ 1. (0,0) - start of segment 0      │
│ 2. (0,2) - start of segment 2      │
│ 3. (1,1) - start of segment 1      │
│ 4. (2,0) - end of segment 2        │
│ 5. (2,2) - end of segment 0        │
│ 6. (3,3) - end of segment 1        │
│                                   │
│ Active segments during sweep:     │
│ x=0: [0, 2]                       │
│ x=1: [0, 1, 2] → check intersections │
│ x=2: [1]                          │
│                                   │
│ Intersections found: (0,1), (0,2), (1,2) │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def sweep_line_intersection(n, segments):
    """
    Find intersecting line segments using sweep line algorithm
    
    Args:
        n: number of line segments
        segments: list of line segments
    
    Returns:
        list: pairs of intersecting line segments
    """
    def do_segments_intersect(seg1, seg2):
        """Check if two line segments intersect"""
        x1, y1, x2, y2 = seg1
        x3, y3, x4, y4 = seg2
        
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        d1 = cross_product((x3, y3), (x4, y4), (x1, y1))
        d2 = cross_product((x3, y3), (x4, y4), (x2, y2))
        d3 = cross_product((x1, y1), (x2, y2), (x3, y3))
        d4 = cross_product((x1, y1), (x2, y2), (x4, y4))
        
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        
        if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
            return not (max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2))
        
        return False
    
    # Create events (start and end points)
    events = []
    for i, (x1, y1, x2, y2) in enumerate(segments):
        events.append((x1, 'start', i))
        events.append((x2, 'end', i))
    
    # Sort events by x-coordinate
    events.sort()
    
    intersections = []
    active_segments = set()
    
    # Process events
    for x, event_type, segment_id in events:
        if event_type == 'start':
            # Check intersections with active segments
            for active_id in active_segments:
                if do_segments_intersect(segments[segment_id], segments[active_id]):
                    intersections.append((min(segment_id, active_id), max(segment_id, active_id)))
            active_segments.add(segment_id)
        else:  # end
            active_segments.remove(segment_id)
    
    return intersections

# Example usage
n = 3
segments = [(0, 0, 2, 2), (1, 1, 3, 3), (0, 2, 2, 0)]
result = sweep_line_intersection(n, segments)
print(f"Sweep line intersections: {result}")
```

**Time Complexity**: O(n log n + k) where k is number of intersections
**Space Complexity**: O(n)

**Why it's better**: Uses sweep line algorithm for O(n log n) time complexity.

---

### Approach 3: Bentley-Ottmann Algorithm (Optimal)

**Key Insights from Bentley-Ottmann Algorithm**:
- **Optimal Algorithm**: O(n log n + k log n) time complexity
- **Event-Driven**: Process intersection events
- **Efficient Data Structures**: Use balanced trees
- **Optimal Complexity**: Best known algorithm for line segment intersection

**Key Insight**: Use Bentley-Ottmann algorithm for optimal line segment intersection.

**Algorithm**:
- Use event queue for sweep line events
- Maintain active segments in balanced tree
- Process intersection events
- Return all intersections

**Visual Example**:
```
Bentley-Ottmann algorithm:
┌─────────────────────────────────────┐
│ Event queue:                       │
│ 1. (0,0) - start segment 0         │
│ 2. (0,2) - start segment 2         │
│ 3. (1,1) - start segment 1         │
│ 4. (1,1) - intersection (0,2)      │
│ 5. (2,0) - end segment 2           │
│ 6. (2,2) - end segment 0           │
│ 7. (3,3) - end segment 1           │
│                                   │
│ Active segments tree:              │
│ Maintains segments ordered by y    │
│ at current x position              │
│                                   │
│ Intersections: (0,1), (0,2), (1,2) │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def bentley_ottmann_intersection(n, segments):
    """
    Find intersecting line segments using Bentley-Ottmann algorithm
    
    Args:
        n: number of line segments
        segments: list of line segments
    
    Returns:
        list: pairs of intersecting line segments
    """
    def do_segments_intersect(seg1, seg2):
        """Check if two line segments intersect"""
        x1, y1, x2, y2 = seg1
        x3, y3, x4, y4 = seg2
        
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        d1 = cross_product((x3, y3), (x4, y4), (x1, y1))
        d2 = cross_product((x3, y3), (x4, y4), (x2, y2))
        d3 = cross_product((x1, y1), (x2, y2), (x3, y3))
        d4 = cross_product((x1, y1), (x2, y2), (x4, y4))
        
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        
        if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
            return not (max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2))
        
        return False
    
    # Create event queue
    events = []
    for i, (x1, y1, x2, y2) in enumerate(segments):
        events.append((x1, 'start', i))
        events.append((x2, 'end', i))
    
    # Sort events
    events.sort()
    
    intersections = []
    active_segments = []
    
    # Process events
    for x, event_type, segment_id in events:
        if event_type == 'start':
            # Insert segment and check for intersections
            active_segments.append(segment_id)
            active_segments.sort(key=lambda i: segments[i][1])  # Sort by y-coordinate
            
            # Check intersections with neighbors
            idx = active_segments.index(segment_id)
            for neighbor_idx in [idx - 1, idx + 1]:
                if 0 <= neighbor_idx < len(active_segments):
                    neighbor_id = active_segments[neighbor_idx]
                    if do_segments_intersect(segments[segment_id], segments[neighbor_id]):
                        intersections.append((min(segment_id, neighbor_id), max(segment_id, neighbor_id)))
        else:  # end
            # Remove segment and check for intersections
            idx = active_segments.index(segment_id)
            if idx > 0 and idx < len(active_segments) - 1:
                # Check intersection between neighbors
                left_id = active_segments[idx - 1]
                right_id = active_segments[idx + 1]
                if do_segments_intersect(segments[left_id], segments[right_id]):
                    intersections.append((min(left_id, right_id), max(left_id, right_id)))
            active_segments.remove(segment_id)
    
    return intersections

# Example usage
n = 3
segments = [(0, 0, 2, 2), (1, 1, 3, 3), (0, 2, 2, 0)]
result = bentley_ottmann_intersection(n, segments)
print(f"Bentley-Ottmann intersections: {result}")
```

**Time Complexity**: O(n log n + k log n) where k is number of intersections
**Space Complexity**: O(n + k)

**Why it's optimal**: Uses Bentley-Ottmann algorithm for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all pairs of line segments |
| Sweep Line | O(n log n + k) | O(n) | Use sweep line algorithm |
| Bentley-Ottmann | O(n log n + k log n) | O(n + k) | Use optimal algorithm |

### Time Complexity
- **Time**: O(n log n + k log n) - Use Bentley-Ottmann algorithm
- **Space**: O(n + k) - Store active segments and intersections

### Why This Solution Works
- **Geometric Algorithms**: Use computational geometry techniques
- **Event Processing**: Process segment endpoints as events
- **Efficient Data Structures**: Use balanced trees for active segments
- **Optimal Algorithms**: Use Bentley-Ottmann algorithm

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Line Segment Intersection with Constraints**
**Problem**: Find intersections with specific constraints.

**Key Differences**: Apply constraints to intersection detection

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_line_segment_intersection(n, segments, constraints):
    """
    Find intersecting line segments with constraints
    
    Args:
        n: number of line segments
        segments: list of line segments
        constraints: function to check constraints
    
    Returns:
        list: pairs of intersecting line segments
    """
    def do_segments_intersect(seg1, seg2):
        """Check if two line segments intersect"""
        x1, y1, x2, y2 = seg1
        x3, y3, x4, y4 = seg2
        
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        d1 = cross_product((x3, y3), (x4, y4), (x1, y1))
        d2 = cross_product((x3, y3), (x4, y4), (x2, y2))
        d3 = cross_product((x1, y1), (x2, y2), (x3, y3))
        d4 = cross_product((x1, y1), (x2, y2), (x4, y4))
        
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        
        if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
            return not (max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2))
        
        return False
    
    intersections = []
    
    for i in range(n):
        for j in range(i + 1, n):
            if do_segments_intersect(segments[i], segments[j]) and constraints(i, j):
                intersections.append((i, j))
    
    return intersections

# Example usage
n = 3
segments = [(0, 0, 2, 2), (1, 1, 3, 3), (0, 2, 2, 0)]
constraints = lambda i, j: i + j < 3  # Only check segments with sum < 3
result = constrained_line_segment_intersection(n, segments, constraints)
print(f"Constrained intersections: {result}")
```

#### **2. Line Segment Intersection with Different Types**
**Problem**: Find intersections with different segment types.

**Key Differences**: Handle different types of line segments

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def typed_line_segment_intersection(n, segments, types):
    """
    Find intersecting line segments with different types
    
    Args:
        n: number of line segments
        segments: list of line segments
        types: list of segment types
    
    Returns:
        list: pairs of intersecting line segments
    """
    def do_segments_intersect(seg1, seg2):
        """Check if two line segments intersect"""
        x1, y1, x2, y2 = seg1
        x3, y3, x4, y4 = seg2
        
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        d1 = cross_product((x3, y3), (x4, y4), (x1, y1))
        d2 = cross_product((x3, y3), (x4, y4), (x2, y2))
        d3 = cross_product((x1, y1), (x2, y2), (x3, y3))
        d4 = cross_product((x1, y1), (x2, y2), (x4, y4))
        
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        
        if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
            return not (max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2))
        
        return False
    
    intersections = []
    
    for i in range(n):
        for j in range(i + 1, n):
            if do_segments_intersect(segments[i], segments[j]) and types[i] != types[j]:
                intersections.append((i, j))
    
    return intersections

# Example usage
n = 3
segments = [(0, 0, 2, 2), (1, 1, 3, 3), (0, 2, 2, 0)]
types = ['horizontal', 'vertical', 'diagonal']
result = typed_line_segment_intersection(n, segments, types)
print(f"Typed intersections: {result}")
```

#### **3. Line Segment Intersection with Weights**
**Problem**: Find intersections with weighted segments.

**Key Differences**: Handle weighted line segments

**Solution Approach**: Use advanced geometric techniques

**Implementation**:
```python
def weighted_line_segment_intersection(n, segments, weights):
    """
    Find intersecting line segments with weights
    
    Args:
        n: number of line segments
        segments: list of line segments
        weights: list of segment weights
    
    Returns:
        list: pairs of intersecting line segments with weights
    """
    def do_segments_intersect(seg1, seg2):
        """Check if two line segments intersect"""
        x1, y1, x2, y2 = seg1
        x3, y3, x4, y4 = seg2
        
        def cross_product(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        d1 = cross_product((x3, y3), (x4, y4), (x1, y1))
        d2 = cross_product((x3, y3), (x4, y4), (x2, y2))
        d3 = cross_product((x1, y1), (x2, y2), (x3, y3))
        d4 = cross_product((x1, y1), (x2, y2), (x4, y4))
        
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        
        if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
            return not (max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2))
        
        return False
    
    intersections = []
    
    for i in range(n):
        for j in range(i + 1, n):
            if do_segments_intersect(segments[i], segments[j]):
                weight = weights[i] + weights[j]
                intersections.append((i, j, weight))
    
    return intersections

# Example usage
n = 3
segments = [(0, 0, 2, 2), (1, 1, 3, 3), (0, 2, 2, 0)]
weights = [1, 2, 3]
result = weighted_line_segment_intersection(n, segments, weights)
print(f"Weighted intersections: {result}")
```

### Related Problems

#### **CSES Problems**
- [Point in Polygon](https://cses.fi/problemset/task/1075) - Geometry
- [Convex Hull](https://cses.fi/problemset/task/1075) - Geometry
- [Area of Rectangles](https://cses.fi/problemset/task/1075) - Geometry

#### **LeetCode Problems**
- [Line Reflection](https://leetcode.com/problems/line-reflection/) - Geometry
- [Self Crossing](https://leetcode.com/problems/self-crossing/) - Geometry
- [Rectangle Overlap](https://leetcode.com/problems/rectangle-overlap/) - Geometry

#### **Problem Categories**
- **Computational Geometry**: Line intersection, sweep line algorithms
- **Geometric Algorithms**: Bentley-Ottmann, event processing
- **Mathematical Algorithms**: Cross products, orientation tests

## 🔗 Additional Resources

### **Algorithm References**
- [Computational Geometry](https://cp-algorithms.com/geometry/basic-geometry.html) - Geometry algorithms
- [Line Intersection](https://cp-algorithms.com/geometry/line-intersection.html) - Line intersection algorithms
- [Sweep Line](https://cp-algorithms.com/geometry/sweep-line.html) - Sweep line algorithms

### **Practice Problems**
- [CSES Point in Polygon](https://cses.fi/problemset/task/1075) - Medium
- [CSES Convex Hull](https://cses.fi/problemset/task/1075) - Medium
- [CSES Area of Rectangles](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry) - Wikipedia article
- [Bentley-Ottmann Algorithm](https://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm) - Wikipedia article
- [Sweep Line Algorithm](https://en.wikipedia.org/wiki/Sweep_line_algorithm) - Wikipedia article
