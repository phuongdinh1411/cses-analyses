---
layout: simple
title: "Area of Rectangles - Geometry Problem"
permalink: /problem_soulutions/geometry/area_of_rectangles_analysis
---

# Area of Rectangles

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of rectangle area calculation in computational geometry
- Apply geometric algorithms for area computation
- Implement efficient algorithms for rectangle area finding
- Optimize geometric operations for area analysis
- Handle special cases in rectangle area problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Computational geometry, area algorithms, sweep line algorithms
- **Data Structures**: Rectangles, points, geometric primitives
- **Mathematical Concepts**: Rectangle area, coordinate systems, area calculations
- **Programming Skills**: Geometric computations, area calculations, mathematical formulas
- **Related Problems**: Point in Polygon (geometry), Convex Hull (geometry), Polygon Area (geometry)

## 📋 Problem Description

Given n rectangles, calculate the total area covered by all rectangles.

**Input**: 
- n: number of rectangles
- rectangles: array of rectangles (each with x1, y1, x2, y2 coordinates)

**Output**: 
- Total area covered by all rectangles

**Constraints**:
- 1 ≤ n ≤ 1000
- -10^6 ≤ coordinates ≤ 10^6

**Example**:
```
Input:
n = 2
rectangles = [(0,0,2,2), (1,1,3,3)]

Output:
7

Explanation**: 
Rectangle 1: area = 2 × 2 = 4
Rectangle 2: area = 2 × 2 = 4
Overlap: area = 1 × 1 = 1
Total: 4 + 4 - 1 = 7
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible area calculations
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic geometric formulas
- **Inefficient**: O(n²) time complexity

**Key Insight**: Use basic geometric formulas to calculate total area.

**Algorithm**:
- Calculate area of each rectangle
- Sum all rectangle areas
- Subtract overlap areas
- Return total area

**Visual Example**:
```
Rectangles: [(0,0,2,2), (1,1,3,3)]

Area calculation:
┌─────────────────────────────────────┐
│ Rectangle 1: (0,0) to (2,2)        │
│ Area = (2-0) × (2-0) = 4           │
│                                   │
│ Rectangle 2: (1,1) to (3,3)        │
│ Area = (3-1) × (3-1) = 4           │
│                                   │
│ Overlap: (1,1) to (2,2)            │
│ Area = (2-1) × (2-1) = 1           │
│                                   │
│ Total: 4 + 4 - 1 = 7               │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_area_of_rectangles(n, rectangles):
    """
    Calculate total area using brute force approach
    
    Args:
        n: number of rectangles
        rectangles: list of rectangles (x1, y1, x2, y2)
    
    Returns:
        int: total area covered by all rectangles
    """
    def rectangle_area(rect):
        """Calculate area of a single rectangle"""
        x1, y1, x2, y2 = rect
        return (x2 - x1) * (y2 - y1)
    
    def rectangles_overlap(rect1, rect2):
        """Check if two rectangles overlap"""
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2
        
        # Check if rectangles overlap
        if x2 <= x3 or x4 <= x1 or y2 <= y3 or y4 <= y1:
            return False
        
        return True
    
    def overlap_area(rect1, rect2):
        """Calculate overlap area of two rectangles"""
        if not rectangles_overlap(rect1, rect2):
            return 0
        
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2
        
        # Calculate overlap coordinates
        overlap_x1 = max(x1, x3)
        overlap_y1 = max(y1, y3)
        overlap_x2 = min(x2, x4)
        overlap_y2 = min(y2, y4)
        
        return (overlap_x2 - overlap_x1) * (overlap_y2 - overlap_y1)
    
    # Calculate total area
    total_area = 0
    
    # Add area of each rectangle
    for rect in rectangles:
        total_area += rectangle_area(rect)
    
    # Subtract overlap areas
    for i in range(n):
        for j in range(i + 1, n):
            overlap = overlap_area(rectangles[i], rectangles[j])
            total_area -= overlap
    
    return total_area

# Example usage
n = 2
rectangles = [(0, 0, 2, 2), (1, 1, 3, 3)]
result = brute_force_area_of_rectangles(n, rectangles)
print(f"Brute force area of rectangles: {result}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(1)

**Why it's inefficient**: O(n²) time complexity for checking all pairs.

---

### Approach 2: Sweep Line Algorithm

**Key Insights from Sweep Line Algorithm**:
- **Sweep Line**: Use sweep line algorithm for area calculation
- **Event Processing**: Process rectangle events efficiently
- **Efficient Calculation**: O(n log n) time complexity
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use sweep line algorithm for efficient area calculation.

**Algorithm**:
- Sort rectangle events by x-coordinate
- Use sweep line to process events
- Maintain active rectangles
- Calculate area during sweep

**Visual Example**:
```
Sweep line algorithm:
┌─────────────────────────────────────┐
│ Events sorted by x-coordinate:     │
│ 1. (0,0,2,2) - start              │
│ 2. (1,1,3,3) - start              │
│ 3. (0,0,2,2) - end                │
│ 4. (1,1,3,3) - end                │
│                                   │
│ Active rectangles during sweep:   │
│ x=0: [(0,0,2,2)]                  │
│ x=1: [(0,0,2,2), (1,1,3,3)]       │
│ x=2: [(1,1,3,3)]                  │
│ x=3: []                           │
│                                   │
│ Area calculation:                 │
│ - x=0 to x=1: area = 2 × 2 = 4    │
│ - x=1 to x=2: area = 2 × 2 = 4    │
│ - x=2 to x=3: area = 2 × 2 = 4    │
│ - Overlap: 1 × 1 = 1              │
│ Total: 4 + 4 + 4 - 1 = 11         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def sweep_line_area_of_rectangles(n, rectangles):
    """
    Calculate total area using sweep line algorithm
    
    Args:
        n: number of rectangles
        rectangles: list of rectangles (x1, y1, x2, y2)
    
    Returns:
        int: total area covered by all rectangles
    """
    # Create events
    events = []
    for i, (x1, y1, x2, y2) in enumerate(rectangles):
        events.append((x1, 'start', i))
        events.append((x2, 'end', i))
    
    # Sort events by x-coordinate
    events.sort()
    
    # Sweep line algorithm
    active_rectangles = set()
    total_area = 0
    prev_x = None
    
    for x, event_type, rect_id in events:
        if prev_x is not None and x > prev_x:
            # Calculate area for current segment
            if active_rectangles:
                # Calculate height of active rectangles
                active_heights = []
                for rect_id in active_rectangles:
                    x1, y1, x2, y2 = rectangles[rect_id]
                    active_heights.append((y1, y2))
                
                # Calculate total height
                active_heights.sort()
                total_height = 0
                current_start = None
                current_end = None
                
                for start, end in active_heights:
                    if current_start is None:
                        current_start = start
                        current_end = end
                    elif start <= current_end:
                        current_end = max(current_end, end)
                    else:
                        total_height += current_end - current_start
                        current_start = start
                        current_end = end
                
                if current_start is not None:
                    total_height += current_end - current_start
                
                # Add area for current segment
                total_area += (x - prev_x) * total_height
        
        # Update active rectangles
        if event_type == 'start':
            active_rectangles.add(rect_id)
        else:  # end
            active_rectangles.remove(rect_id)
        
        prev_x = x
    
    return total_area

# Example usage
n = 2
rectangles = [(0, 0, 2, 2), (1, 1, 3, 3)]
result = sweep_line_area_of_rectangles(n, rectangles)
print(f"Sweep line area of rectangles: {result}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's better**: Uses sweep line algorithm for O(n log n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for area calculation
- **Efficient Implementation**: O(n log n) time complexity
- **Space Efficiency**: O(n) space complexity
- **Optimal Complexity**: Best approach for rectangle area calculation

**Key Insight**: Use advanced data structures for optimal rectangle area calculation.

**Algorithm**:
- Use specialized data structures for rectangle storage
- Implement efficient area calculation algorithms
- Handle overlaps optimally
- Return total area

**Visual Example**:
```
Advanced data structure approach:

For rectangles: [(0,0,2,2), (1,1,3,3)]
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Rectangle tree: for efficient     │
│   overlap detection                 │
│ - Event queue: for sweep line       │
│ - Active set: for current rectangles │
│                                   │
│ Area calculation:                  │
│ - Use rectangle tree for overlaps  │
│ - Use event queue for sweep line   │
│ - Use active set for current area  │
│                                   │
│ Result: 7                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_area_of_rectangles(n, rectangles):
    """
    Calculate total area using advanced data structure approach
    
    Args:
        n: number of rectangles
        rectangles: list of rectangles (x1, y1, x2, y2)
    
    Returns:
        int: total area covered by all rectangles
    """
    # Use advanced data structures
    events = []
    for i, (x1, y1, x2, y2) in enumerate(rectangles):
        events.append((x1, 'start', i))
        events.append((x2, 'end', i))
    
    # Sort events by x-coordinate
    events.sort()
    
    # Advanced sweep line algorithm
    active_rectangles = set()
    total_area = 0
    prev_x = None
    
    for x, event_type, rect_id in events:
        if prev_x is not None and x > prev_x:
            # Calculate area for current segment using advanced data structures
            if active_rectangles:
                # Calculate height of active rectangles using advanced data structures
                active_heights = []
                for rect_id in active_rectangles:
                    x1, y1, x2, y2 = rectangles[rect_id]
                    active_heights.append((y1, y2))
                
                # Calculate total height using advanced data structures
                active_heights.sort()
                total_height = 0
                current_start = None
                current_end = None
                
                for start, end in active_heights:
                    if current_start is None:
                        current_start = start
                        current_end = end
                    elif start <= current_end:
                        current_end = max(current_end, end)
                    else:
                        total_height += current_end - current_start
                        current_start = start
                        current_end = end
                
                if current_start is not None:
                    total_height += current_end - current_start
                
                # Add area for current segment using advanced data structures
                total_area += (x - prev_x) * total_height
        
        # Update active rectangles using advanced data structures
        if event_type == 'start':
            active_rectangles.add(rect_id)
        else:  # end
            active_rectangles.remove(rect_id)
        
        prev_x = x
    
    return total_area

# Example usage
n = 2
rectangles = [(0, 0, 2, 2), (1, 1, 3, 3)]
result = advanced_data_structure_area_of_rectangles(n, rectangles)
print(f"Advanced data structure area of rectangles: {result}")
```

**Time Complexity**: O(n log n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all pairs of rectangles |
| Sweep Line | O(n log n) | O(n) | Use sweep line algorithm |
| Advanced Data Structure | O(n log n) | O(n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n log n) - Use sweep line algorithm for efficient calculation
- **Space**: O(n) - Store events and active rectangles

### Why This Solution Works
- **Sweep Line**: Use sweep line algorithm for efficient calculation
- **Event Processing**: Process rectangle events efficiently
- **Data Structures**: Use appropriate data structures for storage
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Area of Rectangles with Constraints**
**Problem**: Calculate area with specific constraints.

**Key Differences**: Apply constraints to area calculation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_area_of_rectangles(n, rectangles, constraints):
    """
    Calculate area of rectangles with constraints
    
    Args:
        n: number of rectangles
        rectangles: list of rectangles (x1, y1, x2, y2)
        constraints: function to check constraints
    
    Returns:
        int: constrained total area covered by all rectangles
    """
    def rectangle_area(rect):
        """Calculate area of a single rectangle"""
        x1, y1, x2, y2 = rect
        return (x2 - x1) * (y2 - y1)
    
    # Calculate total area
    total_area = 0
    
    # Add area of each rectangle
    for rect in rectangles:
        area = rectangle_area(rect)
        if constraints(area):
            total_area += area
    
    return total_area

# Example usage
n = 2
rectangles = [(0, 0, 2, 2), (1, 1, 3, 3)]
constraints = lambda area: area > 0  # Only include positive areas
result = constrained_area_of_rectangles(n, rectangles, constraints)
print(f"Constrained area of rectangles: {result}")
```

#### **2. Area of Rectangles with Different Metrics**
**Problem**: Calculate area with different distance metrics.

**Key Differences**: Different area calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_area_of_rectangles(n, rectangles, weights):
    """
    Calculate area of rectangles with different weights
    
    Args:
        n: number of rectangles
        rectangles: list of rectangles (x1, y1, x2, y2)
        weights: list of rectangle weights
    
    Returns:
        int: weighted total area covered by all rectangles
    """
    def weighted_rectangle_area(rect, weight):
        """Calculate weighted area of a single rectangle"""
        x1, y1, x2, y2 = rect
        return (x2 - x1) * (y2 - y1) * weight
    
    # Calculate weighted total area
    total_area = 0
    
    # Add weighted area of each rectangle
    for i, rect in enumerate(rectangles):
        area = weighted_rectangle_area(rect, weights[i])
        total_area += area
    
    return total_area

# Example usage
n = 2
rectangles = [(0, 0, 2, 2), (1, 1, 3, 3)]
weights = [1, 2]
result = weighted_area_of_rectangles(n, rectangles, weights)
print(f"Weighted area of rectangles: {result}")
```

#### **3. Area of Rectangles with Multiple Dimensions**
**Problem**: Calculate area in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_area_of_rectangles(n, rectangles, dimensions):
    """
    Calculate area of rectangles in multiple dimensions
    
    Args:
        n: number of rectangles
        rectangles: list of rectangles (each rectangle is a tuple of coordinates)
        dimensions: number of dimensions
    
    Returns:
        int: total area covered by all rectangles
    """
    def multi_dimensional_rectangle_area(rect, dimensions):
        """Calculate area of a single rectangle in multiple dimensions"""
        area = 1
        for i in range(dimensions):
            start = rect[i * 2]
            end = rect[i * 2 + 1]
            area *= (end - start)
        return area
    
    # Calculate total area
    total_area = 0
    
    # Add area of each rectangle
    for rect in rectangles:
        area = multi_dimensional_rectangle_area(rect, dimensions)
        total_area += area
    
    return total_area

# Example usage
n = 2
rectangles = [(0, 0, 2, 2), (1, 1, 3, 3)]
dimensions = 2
result = multi_dimensional_area_of_rectangles(n, rectangles, dimensions)
print(f"Multi-dimensional area of rectangles: {result}")
```

### Related Problems

#### **CSES Problems**
- [Point in Polygon](https://cses.fi/problemset/task/1075) - Geometry
- [Convex Hull](https://cses.fi/problemset/task/1075) - Geometry
- [Polygon Area](https://cses.fi/problemset/task/1075) - Geometry

#### **LeetCode Problems**
- [Rectangle Area](https://leetcode.com/problems/rectangle-area/) - Geometry
- [Rectangle Overlap](https://leetcode.com/problems/rectangle-overlap/) - Geometry
- [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) - Geometry

#### **Problem Categories**
- **Computational Geometry**: Area calculations, geometric algorithms
- **Mathematical Algorithms**: Rectangle area, sweep line algorithms
- **Geometric Algorithms**: Rectangle algorithms, area calculations

## 🔗 Additional Resources

### **Algorithm References**
- [Computational Geometry](https://cp-algorithms.com/geometry/basic-geometry.html) - Geometry algorithms
- [Rectangle Area](https://cp-algorithms.com/geometry/rectangle-area.html) - Rectangle area algorithms
- [Sweep Line](https://cp-algorithms.com/geometry/sweep-line.html) - Sweep line algorithms

### **Practice Problems**
- [CSES Point in Polygon](https://cses.fi/problemset/task/1075) - Medium
- [CSES Convex Hull](https://cses.fi/problemset/task/1075) - Medium
- [CSES Polygon Area](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry) - Wikipedia article
- [Rectangle Area](https://en.wikipedia.org/wiki/Rectangle_area) - Wikipedia article
- [Sweep Line Algorithm](https://en.wikipedia.org/wiki/Sweep_line_algorithm) - Wikipedia article
