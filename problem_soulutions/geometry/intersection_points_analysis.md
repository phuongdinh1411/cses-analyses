---
layout: simple
title: "Intersection Points"
permalink: /problem_soulutions/geometry/intersection_points_analysis
---


# Intersection Points - Geometry Analysis

## Problem Description
Find all intersection points between a set of line segments.

## Solution Progression

### 1. **Brute Force Approach**
**Description**: Check all pairs of line segments for intersection.

**Why this is inefficient**: 
- O(n²) time complexity
- Too slow for large numbers of segments
- Inefficient for practical use

**Why this improvement works**:
- Use sweep line algorithm
- Much faster for large inputs
- Efficient handling of events

### 2. **Optimal Solution**
**Description**: Implement sweep line algorithm to find all intersections.

**Key Insights**:
- Sort events by x-coordinate
- Maintain active segments in balanced tree
- Check for intersections when segments become adjacent

## Complete Implementation

```python
import heapq
from sortedcontainers import SortedList

def cross_product(a, b, c):
    """Calculate cross product of vectors AB and AC"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def segments_intersect(p1, p2, p3, p4):
    """Check if segments p1p2 and p3p4 intersect"""
    o1 = cross_product(p1, p2, p3)
    o2 = cross_product(p1, p2, p4)
    o3 = cross_product(p3, p4, p1)
    o4 = cross_product(p3, p4, p2)
    
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    
    # Handle collinear cases
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True
    
    return False

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def find_intersection(p1, p2, p3, p4):
    """Find intersection point of two line segments"""
    if not segments_intersect(p1, p2, p3, p4):
        return None
    
    # Calculate intersection point
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Parallel lines
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)
    
    return (x, y)

def sweep_line_intersections(segments):
    """Find all intersection points using sweep line algorithm"""
    events = []
    active_segments = SortedList()
    intersections = set()
    
    # Create events
    for i, (p1, p2) in enumerate(segments):
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        events.append((p1[0], 'start', i, p1, p2))
        events.append((p2[0], 'end', i, p1, p2))
    
    events.sort()
    
    for x, event_type, seg_id, p1, p2 in events:
        if event_type == 'start':
            # Insert segment into active set
            active_segments.add((p1, p2, seg_id))
            
            # Check for intersections with adjacent segments
            idx = active_segments.index((p1, p2, seg_id))
            if idx > 0:
                prev_seg = active_segments[idx - 1]
                intersection = find_intersection(p1, p2, prev_seg[0], prev_seg[1])
                if intersection:
                    intersections.add(intersection)
            
            if idx < len(active_segments) - 1:
                next_seg = active_segments[idx + 1]
                intersection = find_intersection(p1, p2, next_seg[0], next_seg[1])
                if intersection:
                    intersections.add(intersection)
        
        else:  # end event
            # Remove segment from active set
            idx = active_segments.index((p1, p2, seg_id))
            active_segments.pop(idx)
            
            # Check for intersections between adjacent segments
            if idx > 0 and idx < len(active_segments):
                prev_seg = active_segments[idx - 1]
                next_seg = active_segments[idx]
                intersection = find_intersection(prev_seg[0], prev_seg[1], next_seg[0], next_seg[1])
                if intersection:
                    intersections.add(intersection)
    
    return sorted(intersections)

# Read input
n = int(input())
segments = []
for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    segments.append(((x1, y1), (x2, y2)))

intersections = sweep_line_intersections(segments)
print(len(intersections))
for x, y in intersections:
    print(f"{x:.6f} {y:.6f}")
```

## Complexity Analysis
- **Time Complexity**: O((n + k) log n) where k is number of intersections
- **Space Complexity**: O(n + k)

## Key Insights for Other Problems

### **Principles**:
1. **Sweep Line Algorithm**: Efficient for geometric intersection problems
2. **Event-Driven Processing**: Process events in sorted order
3. **Balanced Data Structure**: Use balanced tree for active segments

### **Applicability**:
- Line segment intersection
- Geometric algorithms
- Computational geometry
- Sweep line problems

### **Example Problems**:
- Polygon intersection
- Geometric algorithms
- Computational geometry
- Sweep line problems

## Notable Techniques

### **Code Patterns**:
```python
# Sweep line framework
def sweep_line_algorithm(events):
    active_set = SortedList()
    
    for event in sorted(events):
        if event.type == 'start':
            active_set.add(event.segment)
            check_intersections(event.segment, active_set)
        else:
            active_set.remove(event.segment)
            check_adjacent_intersections(active_set)
    
    return intersections

# Event creation
def create_events(segments):
    events = []
    for i, (p1, p2) in enumerate(segments):
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        events.append((p1[0], 'start', i))
        events.append((p2[0], 'end', i))
    return events
```

## Problem-Solving Framework

### **1. Understand the Geometry**
- Visualize sweep line process
- Understand intersection detection
- Consider event ordering

### **2. Choose the Right Tool**
- Sweep line for efficiency
- Balanced data structure for active segments
- Proper intersection calculation

### **3. Handle Edge Cases**
- Parallel segments
- Collinear segments
- Degenerate cases

### **4. Optimize for Performance**
- Use efficient data structures
- Minimize intersection checks
- Handle precision issues 