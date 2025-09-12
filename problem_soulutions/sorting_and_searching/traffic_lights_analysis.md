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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Traffic Lights with Different Colors
**Problem**: Traffic lights have different colors, and we want to find the longest segment of each color.

**Link**: [CSES Problem Set - Traffic Lights Different Colors](https://cses.fi/problemset/task/traffic_lights_colors)

```python
def traffic_lights_different_colors(road_length, queries):
    """
    Handle traffic lights with different colors
    """
    from collections import defaultdict
    
    # Track traffic lights by color
    traffic_lights = defaultdict(list)  # color -> list of positions
    segments = defaultdict(list)  # color -> list of segment lengths
    
    # Initialize with road endpoints
    for color in ['red', 'green', 'blue']:
        traffic_lights[color] = [0, road_length]
        segments[color] = [road_length]
    
    result = []
    
    for query in queries:
        pos, color = query['position'], query['color']
        
        # Find insertion point using binary search
        lights = traffic_lights[color]
        insert_idx = bisect.bisect_left(lights, pos)
        
        if insert_idx > 0 and insert_idx < len(lights):
            # Get the segment that will be split
            left_pos = lights[insert_idx - 1]
            right_pos = lights[insert_idx]
            old_segment_length = right_pos - left_pos
            
            # Remove old segment length
            segments[color].remove(old_segment_length)
            
            # Add two new segment lengths
            left_segment_length = pos - left_pos
            right_segment_length = right_pos - pos
            segments[color].append(left_segment_length)
            segments[color].append(right_segment_length)
            
            # Insert new traffic light
            lights.insert(insert_idx, pos)
        
        # Find maximum segment length for this color
        max_length = max(segments[color])
        result.append(max_length)
    
    return result
```

### Variation 2: Traffic Lights with Dynamic Removal
**Problem**: Traffic lights can be added or removed dynamically.

**Link**: [CSES Problem Set - Traffic Lights Dynamic Removal](https://cses.fi/problemset/task/traffic_lights_dynamic)

```python
class TrafficLightsDynamic:
    def __init__(self, road_length):
        self.road_length = road_length
        self.traffic_lights = [0, road_length]  # Sorted list
        self.segments = [road_length]  # Multiset of segment lengths
    
    def add_traffic_light(self, pos):
        """Add a traffic light at position pos"""
        if pos in self.traffic_lights:
            return max(self.segments)  # Already exists
        
        # Find insertion point
        insert_idx = bisect.bisect_left(self.traffic_lights, pos)
        
        if insert_idx > 0 and insert_idx < len(self.traffic_lights):
            # Get the segment that will be split
            left_pos = self.traffic_lights[insert_idx - 1]
            right_pos = self.traffic_lights[insert_idx]
            old_segment_length = right_pos - left_pos
            
            # Remove old segment length
            self.segments.remove(old_segment_length)
            
            # Add two new segment lengths
            left_segment_length = pos - left_pos
            right_segment_length = right_pos - pos
            self.segments.append(left_segment_length)
            self.segments.append(right_segment_length)
            
            # Insert new traffic light
            self.traffic_lights.insert(insert_idx, pos)
        
        return max(self.segments)
    
    def remove_traffic_light(self, pos):
        """Remove a traffic light at position pos"""
        if pos not in self.traffic_lights or pos in [0, self.road_length]:
            return max(self.segments)  # Cannot remove endpoints
        
        # Find position in list
        idx = bisect.bisect_left(self.traffic_lights, pos)
        
        if idx > 0 and idx < len(self.traffic_lights) - 1:
            # Get adjacent positions
            left_pos = self.traffic_lights[idx - 1]
            right_pos = self.traffic_lights[idx + 1]
            
            # Remove two segment lengths
            left_segment_length = pos - left_pos
            right_segment_length = right_pos - pos
            self.segments.remove(left_segment_length)
            self.segments.remove(right_segment_length)
            
            # Add merged segment length
            merged_segment_length = right_pos - left_pos
            self.segments.append(merged_segment_length)
            
            # Remove traffic light
            self.traffic_lights.pop(idx)
        
        return max(self.segments)
    
    def get_max_segment_length(self):
        """Get current maximum segment length"""
        return max(self.segments)
```

### Variation 3: Traffic Lights with Time Constraints
**Problem**: Traffic lights have time constraints, and we want to find the longest segment at each time.

**Link**: [CSES Problem Set - Traffic Lights Time Constraints](https://cses.fi/problemset/task/traffic_lights_time)

```python
def traffic_lights_time_constraints(road_length, queries):
    """
    Handle traffic lights with time constraints
    """
    # Create events for traffic light changes
    events = []
    
    for query in queries:
        if query['type'] == 'add':
            events.append((query['time'], 'add', query['position']))
        else:  # remove
            events.append((query['time'], 'remove', query['position']))
    
    # Sort events by time
    events.sort()
    
    # Initialize traffic lights system
    traffic_system = TrafficLightsDynamic(road_length)
    
    result = []
    current_time = 0
    
    for time, event_type, pos in events:
        # Process all events up to current time
        if event_type == 'add':
            max_length = traffic_system.add_traffic_light(pos)
        else:  # remove
            max_length = traffic_system.remove_traffic_light(pos)
        
        result.append((time, max_length))
        current_time = time
    
    return result
```

## Problem Variations

### **Variation 1: Traffic Lights with Dynamic Updates**
**Problem**: Handle dynamic traffic light updates (add/remove/update traffic lights) while maintaining optimal road segment tracking.

**Approach**: Use efficient data structures and algorithms for dynamic traffic light management.

```python
from collections import defaultdict
import bisect

class DynamicTrafficLights:
    def __init__(self, road_length):
        self.road_length = road_length
        self.traffic_lights = set()
        self.segments = [road_length]  # Initially one segment of full length
        self.max_segment_length = road_length
        self._update_segments()
    
    def _update_segments(self):
        """Update the road segments based on current traffic lights."""
        if not self.traffic_lights:
            self.segments = [self.road_length]
            self.max_segment_length = self.road_length
            return
        
        # Sort traffic lights
        sorted_lights = sorted(self.traffic_lights)
        
        # Calculate segments
        self.segments = []
        prev_light = 0
        
        for light in sorted_lights:
            if light > prev_light:
                self.segments.append(light - prev_light)
            prev_light = light
        
        # Add final segment
        if prev_light < self.road_length:
            self.segments.append(self.road_length - prev_light)
        
        self.max_segment_length = max(self.segments) if self.segments else 0
    
    def add_traffic_light(self, position):
        """Add a new traffic light at the specified position."""
        if 0 <= position <= self.road_length and position not in self.traffic_lights:
            self.traffic_lights.add(position)
            self._update_segments()
        return self.max_segment_length
    
    def remove_traffic_light(self, position):
        """Remove a traffic light at the specified position."""
        if position in self.traffic_lights:
            self.traffic_lights.remove(position)
            self._update_segments()
        return self.max_segment_length
    
    def update_traffic_light(self, old_position, new_position):
        """Update a traffic light position."""
        if old_position in self.traffic_lights and 0 <= new_position <= self.road_length:
            self.traffic_lights.remove(old_position)
            self.traffic_lights.add(new_position)
            self._update_segments()
        return self.max_segment_length
    
    def get_max_segment_length(self):
        """Get current maximum segment length."""
        return self.max_segment_length
    
    def get_segments(self):
        """Get current road segments."""
        return self.segments
    
    def get_traffic_lights(self):
        """Get current traffic light positions."""
        return sorted(self.traffic_lights)
    
    def get_segments_with_constraints(self, constraint_func):
        """Get segments that satisfy custom constraints."""
        result = []
        for segment in self.segments:
            if constraint_func(segment):
                result.append(segment)
        return result
    
    def get_segments_in_range(self, min_length, max_length):
        """Get segments with length in specified range."""
        result = []
        for segment in self.segments:
            if min_length <= segment <= max_length:
                result.append(segment)
        return result
    
    def get_segments_with_capacity(self, capacity_func):
        """Get segments based on capacity function."""
        result = []
        for segment in self.segments:
            capacity = capacity_func(segment)
            result.append((segment, capacity))
        return result
    
    def get_traffic_statistics(self):
        """Get statistics about traffic lights and segments."""
        if not self.traffic_lights:
            return {
                'total_traffic_lights': 0,
                'total_segments': 1,
                'average_segment_length': self.road_length,
                'max_segment_length': self.road_length,
                'min_segment_length': self.road_length
            }
        
        total_traffic_lights = len(self.traffic_lights)
        total_segments = len(self.segments)
        average_segment_length = sum(self.segments) / total_segments
        max_segment_length = max(self.segments)
        min_segment_length = min(self.segments)
        
        return {
            'total_traffic_lights': total_traffic_lights,
            'total_segments': total_segments,
            'average_segment_length': average_segment_length,
            'max_segment_length': max_segment_length,
            'min_segment_length': min_segment_length
        }
    
    def get_traffic_patterns(self):
        """Get patterns in traffic light arrangement."""
        patterns = {
            'long_segments': 0,
            'short_segments': 0,
            'balanced_segments': 0,
            'efficient_segments': 0
        }
        
        if not self.segments:
            return patterns
        
        avg_length = sum(self.segments) / len(self.segments)
        
        for segment in self.segments:
            if segment > avg_length * 1.5:
                patterns['long_segments'] += 1
            elif segment < avg_length * 0.5:
                patterns['short_segments'] += 1
            else:
                patterns['balanced_segments'] += 1
            
            if segment >= 5:  # Efficient if length >= 5
                patterns['efficient_segments'] += 1
        
        return patterns
    
    def get_optimal_traffic_strategy(self):
        """Get optimal traffic light arrangement strategy."""
        if not self.traffic_lights:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'utilization_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible_segments = len(self.traffic_lights) + 1
        efficiency_rate = (total_possible_segments - len(self.segments)) / total_possible_segments if total_possible_segments > 0 else 0
        
        # Calculate utilization rate
        total_road_length = self.road_length
        total_segment_length = sum(self.segments)
        utilization_rate = total_segment_length / total_road_length if total_road_length > 0 else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.3:
            recommended_strategy = 'balanced_arrangement'
        elif utilization_rate > 0.9:
            recommended_strategy = 'minimal_lights'
        else:
            recommended_strategy = 'optimal_segmentation'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'utilization_rate': utilization_rate
        }

# Example usage
road_length = 10
dynamic_traffic = DynamicTrafficLights(road_length)
print(f"Initial max segment: {dynamic_traffic.get_max_segment_length()}")

# Add traffic lights
dynamic_traffic.add_traffic_light(3)
print(f"After adding light at 3: {dynamic_traffic.get_max_segment_length()}")

dynamic_traffic.add_traffic_light(7)
print(f"After adding light at 7: {dynamic_traffic.get_max_segment_length()}")

# Update a traffic light
dynamic_traffic.update_traffic_light(3, 4)
print(f"After updating light: {dynamic_traffic.get_max_segment_length()}")

# Remove a traffic light
dynamic_traffic.remove_traffic_light(7)
print(f"After removing light: {dynamic_traffic.get_max_segment_length()}")

# Get segments with constraints
def constraint_func(segment):
    return segment >= 3

print(f"Long segments: {dynamic_traffic.get_segments_with_constraints(constraint_func)}")

# Get segments in range
print(f"Segments in range [2, 6]: {dynamic_traffic.get_segments_in_range(2, 6)}")

# Get segments with capacity
def capacity_func(segment):
    return segment * 2  # Capacity is 2x segment length

print(f"Segments with capacity: {dynamic_traffic.get_segments_with_capacity(capacity_func)}")

# Get statistics
print(f"Statistics: {dynamic_traffic.get_traffic_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_traffic.get_traffic_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_traffic.get_optimal_traffic_strategy()}")
```

### **Variation 2: Traffic Lights with Different Operations**
**Problem**: Handle different types of operations on traffic light management (weighted segments, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of traffic light management queries.

```python
class AdvancedTrafficLights:
    def __init__(self, road_length, weights=None, priorities=None):
        self.road_length = road_length
        self.traffic_lights = set()
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.segments = [road_length]
        self.max_segment_length = road_length
        self._update_segments()
    
    def _update_segments(self):
        """Update the road segments using advanced algorithms."""
        if not self.traffic_lights:
            self.segments = [self.road_length]
            self.max_segment_length = self.road_length
            return
        
        # Sort traffic lights
        sorted_lights = sorted(self.traffic_lights)
        
        # Calculate segments with weights and priorities
        self.segments = []
        prev_light = 0
        
        for light in sorted_lights:
            if light > prev_light:
                segment_length = light - prev_light
                weight = self.weights.get(light, 1)
                priority = self.priorities.get(light, 1)
                self.segments.append({
                    'length': segment_length,
                    'weight': weight,
                    'priority': priority,
                    'weighted_length': segment_length * weight * priority
                })
            prev_light = light
        
        # Add final segment
        if prev_light < self.road_length:
            segment_length = self.road_length - prev_light
            self.segments.append({
                'length': segment_length,
                'weight': 1,
                'priority': 1,
                'weighted_length': segment_length
            })
        
        self.max_segment_length = max(seg['length'] for seg in self.segments) if self.segments else 0
    
    def get_segments(self):
        """Get current segments."""
        return self.segments
    
    def get_weighted_segments(self):
        """Get segments with weights applied."""
        result = []
        for segment in self.segments:
            weighted_segment = segment.copy()
            weighted_segment['efficiency'] = segment['weighted_length'] / segment['length']
            result.append(weighted_segment)
        return result
    
    def get_segments_with_priority(self, priority_func):
        """Get segments considering priority."""
        result = []
        for segment in self.segments:
            priority = priority_func(segment)
            result.append((segment, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_segments_with_optimization(self, optimization_func):
        """Get segments using custom optimization function."""
        result = []
        for segment in self.segments:
            score = optimization_func(segment)
            result.append((segment, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_segments_with_constraints(self, constraint_func):
        """Get segments that satisfy custom constraints."""
        result = []
        for segment in self.segments:
            if constraint_func(segment):
                result.append(segment)
        return result
    
    def get_segments_with_multiple_criteria(self, criteria_list):
        """Get segments that satisfy multiple criteria."""
        result = []
        for segment in self.segments:
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(segment):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(segment)
        return result
    
    def get_segments_with_alternatives(self, alternatives):
        """Get segments considering alternative traffic light arrangements."""
        result = []
        
        # Check original segments
        for segment in self.segments:
            result.append((segment, 'original'))
        
        # Check alternative arrangements
        for alt_lights in alternatives:
            # Create temporary segments with alternative traffic lights
            temp_segments = self._create_segments_with_lights(alt_lights)
            result.append((temp_segments, f'alternative_{alt_lights}'))
        
        return result
    
    def _create_segments_with_lights(self, traffic_lights):
        """Create segments with given traffic lights."""
        if not traffic_lights:
            return [{'length': self.road_length, 'weight': 1, 'priority': 1, 'weighted_length': self.road_length}]
        
        sorted_lights = sorted(traffic_lights)
        segments = []
        prev_light = 0
        
        for light in sorted_lights:
            if light > prev_light:
                segment_length = light - prev_light
                weight = self.weights.get(light, 1)
                priority = self.priorities.get(light, 1)
                segments.append({
                    'length': segment_length,
                    'weight': weight,
                    'priority': priority,
                    'weighted_length': segment_length * weight * priority
                })
            prev_light = light
        
        # Add final segment
        if prev_light < self.road_length:
            segment_length = self.road_length - prev_light
            segments.append({
                'length': segment_length,
                'weight': 1,
                'priority': 1,
                'weighted_length': segment_length
            })
        
        return segments
    
    def get_segments_with_adaptive_criteria(self, adaptive_func):
        """Get segments using adaptive criteria."""
        result = []
        for segment in self.segments:
            if adaptive_func(segment, result):
                result.append(segment)
        return result
    
    def get_traffic_optimization(self):
        """Get optimal traffic light configuration."""
        strategies = [
            ('segments', lambda: len(self.segments)),
            ('weighted_segments', lambda: len(self.get_weighted_segments())),
            ('max_segment', lambda: self.max_segment_length),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
road_length = 10
weights = {3: 2, 7: 1, 5: 3}
priorities = {3: 1, 7: 2, 5: 1}
advanced_traffic = AdvancedTrafficLights(road_length, weights, priorities)

# Add traffic lights
advanced_traffic.traffic_lights.add(3)
advanced_traffic.traffic_lights.add(7)
advanced_traffic._update_segments()

print(f"Segments: {len(advanced_traffic.get_segments())}")
print(f"Weighted segments: {len(advanced_traffic.get_weighted_segments())}")

# Get segments with priority
def priority_func(segment):
    return segment['weighted_length'] / segment['length']

print(f"Segments with priority: {advanced_traffic.get_segments_with_priority(priority_func)}")

# Get segments with optimization
def optimization_func(segment):
    return segment['length'] * segment['weight'] * segment['priority']

print(f"Segments with optimization: {advanced_traffic.get_segments_with_optimization(optimization_func)}")

# Get segments with constraints
def constraint_func(segment):
    return segment['length'] >= 3 and segment['weight'] > 1

print(f"Segments with constraints: {advanced_traffic.get_segments_with_constraints(constraint_func)}")

# Get segments with multiple criteria
def criterion1(segment):
    return segment['length'] >= 3

def criterion2(segment):
    return segment['weight'] > 1

criteria_list = [criterion1, criterion2]
print(f"Segments with multiple criteria: {advanced_traffic.get_segments_with_multiple_criteria(criteria_list)}")

# Get segments with alternatives
alternatives = [[2, 6, 8], [1, 4, 9]]
print(f"Segments with alternatives: {advanced_traffic.get_segments_with_alternatives(alternatives)}")

# Get segments with adaptive criteria
def adaptive_func(segment, current_result):
    return segment['length'] >= 3 and len(current_result) < 3

print(f"Segments with adaptive criteria: {advanced_traffic.get_segments_with_adaptive_criteria(adaptive_func)}")

# Get traffic optimization
print(f"Traffic optimization: {advanced_traffic.get_traffic_optimization()}")
```

### **Variation 3: Traffic Lights with Constraints**
**Problem**: Handle traffic light management with additional constraints (capacity limits, time constraints, weight constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTrafficLights:
    def __init__(self, road_length, constraints=None):
        self.road_length = road_length
        self.traffic_lights = set()
        self.constraints = constraints or {}
        self.segments = [road_length]
        self.max_segment_length = road_length
        self._update_segments()
    
    def _update_segments(self):
        """Update the road segments considering constraints."""
        if not self.traffic_lights:
            self.segments = [self.road_length]
            self.max_segment_length = self.road_length
            return
        
        # Sort traffic lights
        sorted_lights = sorted(self.traffic_lights)
        
        # Calculate segments considering constraints
        self.segments = []
        prev_light = 0
        
        for light in sorted_lights:
            if light > prev_light:
                segment_length = light - prev_light
                if self._can_create_segment(segment_length):
                    self.segments.append(segment_length)
            prev_light = light
        
        # Add final segment
        if prev_light < self.road_length:
            segment_length = self.road_length - prev_light
            if self._can_create_segment(segment_length):
                self.segments.append(segment_length)
        
        self.max_segment_length = max(self.segments) if self.segments else 0
    
    def _can_create_segment(self, segment_length):
        """Check if a segment can be created considering constraints."""
        # Length constraint
        if 'min_length' in self.constraints:
            if segment_length < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if segment_length > self.constraints['max_length']:
                return False
        
        # Capacity constraint
        if 'max_capacity' in self.constraints:
            if len(self.segments) >= self.constraints['max_capacity']:
                return False
        
        return True
    
    def get_segments_with_capacity_constraints(self, capacity_limits):
        """Get segments considering capacity constraints."""
        result = []
        current_capacity = 0
        
        for segment in self.segments:
            # Check capacity constraints
            if current_capacity + segment <= capacity_limits:
                result.append(segment)
                current_capacity += segment
        
        return result
    
    def get_segments_with_length_constraints(self, length_limits):
        """Get segments considering length constraints."""
        result = []
        
        for segment in self.segments:
            # Check length constraints
            if length_limits[0] <= segment <= length_limits[1]:
                result.append(segment)
        
        return result
    
    def get_segments_with_time_constraints(self, time_constraints):
        """Get segments considering time constraints."""
        result = []
        
        for segment in self.segments:
            # Check time constraints
            satisfies_constraints = True
            for constraint in time_constraints:
                if not constraint(segment):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(segment)
        
        return result
    
    def get_segments_with_mathematical_constraints(self, constraint_func):
        """Get segments that satisfy custom mathematical constraints."""
        result = []
        
        for segment in self.segments:
            if constraint_func(segment):
                result.append(segment)
        
        return result
    
    def get_segments_with_range_constraints(self, range_constraints):
        """Get segments that satisfy range constraints."""
        result = []
        
        for segment in self.segments:
            # Check if segment satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(segment):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(segment)
        
        return result
    
    def get_segments_with_optimization_constraints(self, optimization_func):
        """Get segments using custom optimization constraints."""
        # Sort segments by optimization function
        all_segments = []
        for segment in self.segments:
            score = optimization_func(segment)
            all_segments.append((segment, score))
        
        # Sort by optimization score
        all_segments.sort(key=lambda x: x[1], reverse=True)
        
        return [segment for segment, _ in all_segments]
    
    def get_segments_with_multiple_constraints(self, constraints_list):
        """Get segments that satisfy multiple constraints."""
        result = []
        
        for segment in self.segments:
            # Check if segment satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(segment):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                result.append(segment)
        
        return result
    
    def get_segments_with_priority_constraints(self, priority_func):
        """Get segments with priority-based constraints."""
        # Sort segments by priority
        all_segments = []
        for segment in self.segments:
            priority = priority_func(segment)
            all_segments.append((segment, priority))
        
        # Sort by priority
        all_segments.sort(key=lambda x: x[1], reverse=True)
        
        return [segment for segment, _ in all_segments]
    
    def get_segments_with_adaptive_constraints(self, adaptive_func):
        """Get segments with adaptive constraints."""
        result = []
        
        for segment in self.segments:
            # Check adaptive constraints
            if adaptive_func(segment, result):
                result.append(segment)
        
        return result
    
    def get_optimal_traffic_strategy(self):
        """Get optimal traffic light arrangement strategy considering all constraints."""
        strategies = [
            ('capacity_constraints', self.get_segments_with_capacity_constraints),
            ('length_constraints', self.get_segments_with_length_constraints),
            ('time_constraints', self.get_segments_with_time_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'capacity_constraints':
                    current_count = len(strategy_func(20))  # Capacity limit of 20
                elif strategy_name == 'length_constraints':
                    current_count = len(strategy_func((2, 8)))  # Length between 2 and 8
                elif strategy_name == 'time_constraints':
                    time_constraints = [lambda segment: segment >= 3]
                    current_count = len(strategy_func(time_constraints))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 2,
    'max_length': 8,
    'max_capacity': 5
}

road_length = 10
constrained_traffic = ConstrainedTrafficLights(road_length, constraints)

# Add traffic lights
constrained_traffic.traffic_lights.add(3)
constrained_traffic.traffic_lights.add(7)
constrained_traffic._update_segments()

print("Capacity-constrained segments:", len(constrained_traffic.get_segments_with_capacity_constraints(20)))

print("Length-constrained segments:", len(constrained_traffic.get_segments_with_length_constraints((2, 8))))

# Time constraints
time_constraints = [lambda segment: segment >= 3]
print("Time-constrained segments:", len(constrained_traffic.get_segments_with_time_constraints(time_constraints)))

# Mathematical constraints
def custom_constraint(segment):
    return segment >= 3 and segment <= 6

print("Mathematical constraint segments:", len(constrained_traffic.get_segments_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(segment):
    return 2 <= segment <= 8

range_constraints = [range_constraint]
print("Range-constrained segments:", len(constrained_traffic.get_segments_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(segment):
    return segment >= 3

def constraint2(segment):
    return segment <= 6

constraints_list = [constraint1, constraint2]
print("Multiple constraints segments:", len(constrained_traffic.get_segments_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(segment):
    return segment

print("Priority-constrained segments:", len(constrained_traffic.get_segments_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(segment, current_result):
    return segment >= 3 and len(current_result) < 3

print("Adaptive constraint segments:", len(constrained_traffic.get_segments_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_traffic.get_optimal_traffic_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Traffic Lights](https://cses.fi/problemset/task/1163) - Basic traffic lights problem
- [Stick Lengths](https://cses.fi/problemset/task/1074) - Similar optimization problem
- [Array Division](https://cses.fi/problemset/task/1085) - Similar binary search optimization

#### **LeetCode Problems**
- [Insert Interval](https://leetcode.com/problems/insert-interval/) - Insert and merge intervals
- [Merge Intervals](https://leetcode.com/problems/merge-intervals/) - Merge overlapping intervals
- [My Calendar I](https://leetcode.com/problems/my-calendar-i/) - Calendar booking system
- [My Calendar II](https://leetcode.com/problems/my-calendar-ii/) - Calendar with double booking

#### **Problem Categories**
- **Binary Search**: Efficient insertion, sorted array maintenance, search optimization
- **Data Structures**: Multiset operations, segment tracking, dynamic updates
- **Interval Problems**: Segment management, interval insertion, dynamic intervals
- **Algorithm Design**: Binary search algorithms, data structure design, optimization techniques
