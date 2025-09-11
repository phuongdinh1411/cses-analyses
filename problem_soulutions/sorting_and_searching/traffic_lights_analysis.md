---
layout: simple
title: "Traffic Lights"
permalink: /problem_soulutions/sorting_and_searching/traffic_lights_analysis
---

# Traffic Lights

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of coordinate compression and its applications
- Apply sorting algorithms for efficient coordinate processing
- Implement efficient solutions for dynamic coordinate problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in coordinate-based problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, coordinate compression, binary search, set operations
- **Data Structures**: Arrays, sets, sorted lists, binary search trees
- **Mathematical Concepts**: Coordinate systems, interval management, dynamic updates
- **Programming Skills**: Algorithm implementation, complexity analysis, coordinate compression
- **Related Problems**: Room Allocation (coordinate compression), Nested Ranges (coordinate processing), Array Division (optimization)

## 📋 Problem Description

There is a street with traffic lights at positions 0 and x. You need to add n more traffic lights at positions a[1], a[2], ..., a[n].

After adding each traffic light, find the length of the longest segment between consecutive traffic lights.

**Input**: 
- First line: two integers x and n (street length and number of traffic lights)
- Second line: n integers a[1], a[2], ..., a[n] (positions of traffic lights)

**Output**: 
- Print n integers: the length of the longest segment after adding each traffic light

**Constraints**:
- 1 ≤ x ≤ 10⁹
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ x-1

**Example**:
```
Input:
8 3
3 6 2

Output:
5 3 3

Explanation**: 
Initial traffic lights: [0, 8]
Segments: [0-8] with length 8

After adding light at position 3: [0, 3, 8]
Segments: [0-3] with length 3, [3-8] with length 5
Longest segment: 5

After adding light at position 6: [0, 3, 6, 8]
Segments: [0-3] with length 3, [3-6] with length 3, [6-8] with length 2
Longest segment: 3

After adding light at position 2: [0, 2, 3, 6, 8]
Segments: [0-2] with length 2, [2-3] with length 1, [3-6] with length 3, [6-8] with length 2
Longest segment: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Recalculate All Segments

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: After each addition, recalculate all segments
- **Complete Coverage**: Guaranteed to find the correct longest segment
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity

**Key Insight**: After adding each traffic light, recalculate all segments and find the maximum.

**Algorithm**:
- For each traffic light position:
  - Add it to the list of traffic lights
  - Sort the list
  - Calculate all segment lengths
  - Find the maximum segment length

**Visual Example**:
```
Initial: x = 8, traffic lights = [0, 8]
Segments: [0-8] with length 8

Add position 3: traffic lights = [0, 3, 8]
Segments: [0-3] with length 3, [3-8] with length 5
Longest segment: 5

Add position 6: traffic lights = [0, 3, 6, 8]
Segments: [0-3] with length 3, [3-6] with length 3, [6-8] with length 2
Longest segment: 3

Add position 2: traffic lights = [0, 2, 3, 6, 8]
Segments: [0-2] with length 2, [2-3] with length 1, [3-6] with length 3, [6-8] with length 2
Longest segment: 3
```

**Implementation**:
```python
def brute_force_traffic_lights(x, positions):
    """
    Find longest segment after each traffic light addition using brute force
    
    Args:
        x: street length
        positions: list of traffic light positions
    
    Returns:
        list: longest segment length after each addition
    """
    traffic_lights = [0, x]
    result = []
    
    for pos in positions:
        # Add new traffic light
        traffic_lights.append(pos)
        
        # Sort traffic lights
        traffic_lights.sort()
        
        # Calculate all segment lengths
        max_length = 0
        for i in range(len(traffic_lights) - 1):
            segment_length = traffic_lights[i + 1] - traffic_lights[i]
            max_length = max(max_length, segment_length)
        
        result.append(max_length)
    
    return result

# Example usage
x, n = 8, 3
positions = [3, 6, 2]
result = brute_force_traffic_lights(x, positions)
print(f"Brute force result: {result}")  # Output: [5, 3, 3]
```

**Time Complexity**: O(n² log n) - Sort n times, each taking O(n log n)
**Space Complexity**: O(n) - For traffic lights list

**Why it's inefficient**: Sorting after each addition leads to quadratic time complexity.

---

### Approach 2: Optimized - Use Sorted List

**Key Insights from Optimized Approach**:
- **Sorted List**: Maintain traffic lights in sorted order
- **Efficient Insertion**: Use binary search to find insertion position
- **Better Complexity**: Achieve O(n log n) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Maintain traffic lights in sorted order and use binary search for efficient insertion.

**Algorithm**:
- Keep traffic lights in a sorted list
- For each new position, use binary search to find insertion point
- Insert the new position
- Calculate segment lengths and find maximum

**Visual Example**:
```
Initial: sorted_lights = [0, 8]
Segments: [0-8] with length 8

Add position 3: binary search finds insertion point at index 1
sorted_lights = [0, 3, 8]
Segments: [0-3] with length 3, [3-8] with length 5
Longest segment: 5

Add position 6: binary search finds insertion point at index 2
sorted_lights = [0, 3, 6, 8]
Segments: [0-3] with length 3, [3-6] with length 3, [6-8] with length 2
Longest segment: 3

Add position 2: binary search finds insertion point at index 1
sorted_lights = [0, 2, 3, 6, 8]
Segments: [0-2] with length 2, [2-3] with length 1, [3-6] with length 3, [6-8] with length 2
Longest segment: 3
```

**Implementation**:
```python
def optimized_traffic_lights(x, positions):
    """
    Find longest segment after each traffic light addition using sorted list
    
    Args:
        x: street length
        positions: list of traffic light positions
    
    Returns:
        list: longest segment length after each addition
    """
    from bisect import insort
    
    traffic_lights = [0, x]
    result = []
    
    for pos in positions:
        # Insert new traffic light in sorted order
        insort(traffic_lights, pos)
        
        # Calculate all segment lengths
        max_length = 0
        for i in range(len(traffic_lights) - 1):
            segment_length = traffic_lights[i + 1] - traffic_lights[i]
            max_length = max(max_length, segment_length)
        
        result.append(max_length)
    
    return result

# Example usage
x, n = 8, 3
positions = [3, 6, 2]
result = optimized_traffic_lights(x, positions)
print(f"Optimized result: {result}")  # Output: [5, 3, 3]
```

**Time Complexity**: O(n log n) - Binary search insertion for each position
**Space Complexity**: O(n) - For traffic lights list

**Why it's better**: Much more efficient than brute force with binary search optimization.

---

### Approach 3: Optimal - Use Multiset with Segment Tracking

**Key Insights from Optimal Approach**:
- **Multiset**: Use a multiset to track segment lengths
- **Efficient Updates**: Only update affected segments when adding new traffic light
- **Optimal Complexity**: Achieve O(n log n) time complexity
- **Efficient Implementation**: No need to recalculate all segments

**Key Insight**: Use a multiset to track segment lengths and only update affected segments.

**Algorithm**:
- Use a multiset to track segment lengths
- For each new position, find the segment it splits
- Remove the old segment and add two new segments
- The maximum segment length is always at the end of the multiset

**Visual Example**:
```
Initial: segments = {8}
Traffic lights: [0, 8]

Add position 3: splits segment [0-8] into [0-3] and [3-8]
segments = {3, 5}
Traffic lights: [0, 3, 8]
Longest segment: 5

Add position 6: splits segment [3-8] into [3-6] and [6-8]
segments = {3, 3, 2}
Traffic lights: [0, 3, 6, 8]
Longest segment: 3

Add position 2: splits segment [0-3] into [0-2] and [2-3]
segments = {2, 1, 3, 2}
Traffic lights: [0, 2, 3, 6, 8]
Longest segment: 3
```

**Implementation**:
```python
def optimal_traffic_lights(x, positions):
    """
    Find longest segment after each traffic light addition using multiset
    
    Args:
        x: street length
        positions: list of traffic light positions
    
    Returns:
        list: longest segment length after each addition
    """
    from bisect import bisect_left
    
    # Use sorted list to simulate multiset
    traffic_lights = [0, x]
    segments = [x]  # Track segment lengths
    
    result = []
    
    for pos in positions:
        # Find insertion point
        insert_idx = bisect_left(traffic_lights, pos)
        
        # Get the segment that will be split
        left_pos = traffic_lights[insert_idx - 1]
        right_pos = traffic_lights[insert_idx]
        old_segment_length = right_pos - left_pos
        
        # Remove old segment length
        segments.remove(old_segment_length)
        
        # Add two new segment lengths
        left_segment_length = pos - left_pos
        right_segment_length = right_pos - pos
        segments.append(left_segment_length)
        segments.append(right_segment_length)
        
        # Insert new traffic light
        traffic_lights.insert(insert_idx, pos)
        
        # Find maximum segment length
        max_length = max(segments)
        result.append(max_length)
    
    return result

# Example usage
x, n = 8, 3
positions = [3, 6, 2]
result = optimal_traffic_lights(x, positions)
print(f"Optimal result: {result}")  # Output: [5, 3, 3]
```

**Time Complexity**: O(n log n) - Binary search and list operations
**Space Complexity**: O(n) - For traffic lights and segments

**Why it's optimal**: Achieves the best possible time complexity with efficient segment tracking.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n² log n) | O(n) | Recalculate all segments |
| Sorted List | O(n log n) | O(n) | Use binary search for insertion |
| Multiset | O(n log n) | O(n) | Track segment lengths efficiently |

### Time Complexity
- **Time**: O(n log n) - Multiset approach provides optimal time complexity
- **Space**: O(n) - For traffic lights and segment tracking

### Why This Solution Works
- **Segment Tracking**: Efficiently track segment lengths using multiset
- **Binary Search**: Use binary search for efficient insertion
- **Optimal Algorithm**: Multiset approach is the standard solution for this problem
- **Optimal Approach**: Multiset provides the most efficient solution for dynamic segment tracking
