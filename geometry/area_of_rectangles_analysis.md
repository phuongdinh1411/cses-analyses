# Area of Rectangles - CSES Geometry Analysis

## Problem Description
Calculate the total area covered by a set of rectangles.

## Solution Progression

### 1. **Brute Force Approach**
**Description**: Check each point to see if it's covered by any rectangle.

**Why this is inefficient**: 
- O(area) time complexity
- Too slow for large rectangles
- Inefficient for practical use

**Why this improvement works**:
- Use sweep line algorithm
- Process events in sorted order
- Much faster than brute force

### 2. **Optimal Solution**
**Description**: Implement sweep line algorithm with segment tree for area calculation.

**Key Insights**:
- Sort events by x-coordinate
- Maintain active intervals in segment tree
- Calculate area between events

## Complete Implementation

```python
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

def area_of_rectangles(rectangles):
    """Calculate total area covered by rectangles using sweep line"""
    events = []
    y_coords = set()
    
    # Create events and collect y-coordinates
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
            covered_length = st.tree[1]  # Total covered length
            total_area += (x - prev_x) * covered_length
        
        # Update active intervals
        idx1 = y_to_idx[y1]
        idx2 = y_to_idx[y2] - 1  # Convert to 0-based index
        
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
    
    for x, event_type, y1, y2 in events:
        if x > prev_x:
            covered_length = calculate_covered_length(active_intervals)
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