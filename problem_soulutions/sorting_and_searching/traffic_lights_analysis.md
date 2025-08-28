---
layout: simple
title: CSES Traffic Lights - Problem Analysis
permalink: /problem_soulutions/sorting_and_searching/traffic_lights_analysis/
---

# CSES Traffic Lights - Problem Analysis

## Problem Statement
There are n traffic lights on a street. Initially, all lights are green. Then, q events happen: either a light turns red or a light turns green. After each event, find the length of the longest continuous segment of green lights.

### Input
The first input line has two integers n and q: the number of traffic lights and events.
Then there are q lines describing the events. Each line has an integer x: the position of the light that changes state.

### Output
Print q integers: the length of the longest continuous segment of green lights after each event.

### Constraints
- 1 ≤ n ≤ 10^9
- 1 ≤ q ≤ 2⋅10^5
- 1 ≤ x ≤ n

### Example
```
Input:
8 3
3
6
2

Output:
5
3
3
```

## Solution Progression

### Approach 1: Brute Force - O(q * n)
**Description**: After each event, scan the entire street to find the longest green segment.

```python
def traffic_lights_naive(n, q, events):
    lights = [True] * n  # True = green, False = red
    results = []
    
    for event in events:
        pos = event - 1  # Convert to 0-indexed
        lights[pos] = not lights[pos]  # Toggle light
        
        # Find longest continuous green segment
        max_length = 0
        current_length = 0
        
        for i in range(n):
            if lights[i]:
                current_length += 1
                max_length = max(max_length, current_length)
            else:
                current_length = 0
        
        results.append(max_length)
    
    return results
```

**Why this is inefficient**: For each event, we scan the entire street, leading to O(q * n) time complexity.

### Improvement 1: Set-based Approach - O(q log q)
**Description**: Track red light positions and find the longest gap between them.

```python
def traffic_lights_optimized(n, q, events):
    red_lights = set()
    results = []
    
    for event in events:
        pos = event
        
        if pos in red_lights:
            red_lights.remove(pos)
        else:
            red_lights.add(pos)
        
        # Find longest gap between red lights
        if not red_lights:
            max_length = n
        else:
            red_list = sorted(red_lights)
            max_length = max(red_list[0] - 1, n - red_list[-1])
            
            for i in range(1, len(red_list)):
                gap = red_list[i] - red_list[i-1] - 1
                max_length = max(max_length, gap)
        
        results.append(max_length)
    
    return results
```

**Why this improvement works**: We only track the positions of red lights and find the longest gap between them, which is much more efficient than scanning the entire street.

## Final Optimal Solution

```python
n, q = map(int, input().split())
events = [int(input()) for _ in range(q)]

def find_longest_green_segment(n, q, events):
    red_lights = set()
    results = []
    
    for event in events:
        pos = event
        
        if pos in red_lights:
            red_lights.remove(pos)
        else:
            red_lights.add(pos)
        
        # Find longest gap between red lights
        if not red_lights:
            max_length = n
        else:
            red_list = sorted(red_lights)
            max_length = max(red_list[0] - 1, n - red_list[-1])
            
            for i in range(1, len(red_list)):
                gap = red_list[i] - red_list[i-1] - 1
                max_length = max(max_length, gap)
        
        results.append(max_length)
    
    return results

results = find_longest_green_segment(n, q, events)
for result in results:
    print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q * n) | O(n) | Scan entire street after each event |
| Set-based | O(q log q) | O(q) | Track red lights and find gaps |

## Key Insights for Other Problems

### 1. **Interval Gap Problems**
**Principle**: Track boundary points and find longest gaps between them.
**Applicable to**: Interval problems, gap problems, segment problems

### 2. **State Tracking**
**Principle**: Track only the relevant state changes rather than the entire structure.
**Applicable to**: State problems, toggle problems, event-driven problems

### 3. **Gap Analysis**
**Principle**: Find the longest continuous segment by analyzing gaps between obstacles.
**Applicable to**: Segment problems, gap problems, optimization problems

## Notable Techniques

### 1. **Red Light Tracking**
```python
def track_red_lights(events, n):
    red_lights = set()
    
    for event in events:
        if event in red_lights:
            red_lights.remove(event)
        else:
            red_lights.add(event)
    
    return red_lights
```

### 2. **Gap Calculation**
```python
def calculate_gaps(red_lights, n):
    if not red_lights:
        return n
    
    red_list = sorted(red_lights)
    max_gap = max(red_list[0] - 1, n - red_list[-1])
    
    for i in range(1, len(red_list)):
        gap = red_list[i] - red_list[i-1] - 1
        max_gap = max(max_gap, gap)
    
    return max_gap
```

### 3. **State Toggle**
```python
def toggle_state(positions, pos):
    if pos in positions:
        positions.remove(pos)
    else:
        positions.add(pos)
    
    return positions
```

## Problem-Solving Framework

1. **Identify problem type**: This is an interval gap problem with state changes
2. **Choose approach**: Track red light positions and find gaps
3. **Initialize tracking**: Start with empty set of red lights
4. **Process events**: Toggle light states and update tracking
5. **Calculate gaps**: Find longest gap between red lights
6. **Handle boundaries**: Consider gaps at street boundaries
7. **Return result**: Output longest green segment after each event

---

*This analysis shows how to efficiently track traffic light states and find the longest continuous green segment using gap analysis.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Traffic Lights with Multiple Colors**
**Problem**: Traffic lights can be red, yellow, or green. Find longest green segment.
```python
def traffic_lights_multiple_colors(n, q, events):
    # events[i] = (position, color) where color is 'R', 'Y', or 'G'
    light_states = {}  # position -> color
    results = []
    
    for pos, color in events:
        light_states[pos] = color
        
        # Find longest continuous green segment
        max_length = 0
        current_length = 0
        
        for i in range(1, n + 1):
            if light_states.get(i) == 'G':
                current_length += 1
                max_length = max(max_length, current_length)
            else:
                current_length = 0
        
        results.append(max_length)
    
    return results
```

#### **Variation 2: Traffic Lights with Duration**
**Problem**: Each light has a duration. Find longest segment with total duration ≤ T.
```python
def traffic_lights_with_duration(n, q, events, durations):
    # events[i] = (position, state) where state is True (green) or False (red)
    # durations[i] = duration of light at position i
    light_states = {}
    results = []
    
    for pos, state in events:
        light_states[pos] = state
        
        # Find longest segment with total duration <= T
        max_length = 0
        current_length = 0
        current_duration = 0
        T = 100  # Example threshold
        
        for i in range(1, n + 1):
            if light_states.get(i, True):  # Default to green
                current_length += 1
                current_duration += durations.get(i, 1)
                
                if current_duration <= T:
                    max_length = max(max_length, current_length)
                else:
                    # Shrink from left until duration <= T
                    while current_duration > T and current_length > 0:
                        current_duration -= durations.get(i - current_length + 1, 1)
                        current_length -= 1
            else:
                current_length = 0
                current_duration = 0
        
        results.append(max_length)
    
    return results
```

#### **Variation 3: Traffic Lights with Priority**
**Problem**: Some lights have higher priority and must remain green longer.
```python
def traffic_lights_with_priority(n, q, events, priorities):
    # priorities[i] = priority of light at position i (higher = more priority)
    light_states = {}
    results = []
    
    for pos, state in events:
        light_states[pos] = state
        
        # Find longest green segment considering priorities
        max_length = 0
        current_length = 0
        current_priority_sum = 0
        
        for i in range(1, n + 1):
            if light_states.get(i, True):  # Default to green
                current_length += 1
                current_priority_sum += priorities.get(i, 1)
            else:
                current_length = 0
                current_priority_sum = 0
            
            # Weight length by priority
            weighted_length = current_length * (current_priority_sum / current_length if current_length > 0 else 0)
            max_length = max(max_length, weighted_length)
        
        results.append(int(max_length))
    
    return results
```

#### **Variation 4: Traffic Lights with Dynamic Updates**
**Problem**: Support adding and removing traffic lights dynamically.
```python
class DynamicTrafficLights:
    def __init__(self, n):
        self.n = n
        self.red_lights = set()
        self.max_length = n
    
    def toggle_light(self, pos):
        if pos in self.red_lights:
            self.red_lights.remove(pos)
        else:
            self.red_lights.add(pos)
        
        # Recalculate max length
        if not self.red_lights:
            self.max_length = self.n
        else:
            red_list = sorted(self.red_lights)
            self.max_length = max(red_list[0] - 1, self.n - red_list[-1])
            
            for i in range(1, len(red_list)):
                gap = red_list[i] - red_list[i-1] - 1
                self.max_length = max(self.max_length, gap)
        
        return self.max_length
    
    def add_light(self, pos):
        self.n += 1
        return self.get_max_length()
    
    def remove_light(self, pos):
        if pos in self.red_lights:
            self.red_lights.remove(pos)
        self.n -= 1
        return self.get_max_length()
    
    def get_max_length(self):
        return self.max_length
```

#### **Variation 5: Traffic Lights with Constraints**
**Problem**: Some lights cannot be green simultaneously due to safety constraints.
```python
def traffic_lights_with_constraints(n, q, events, constraints):
    # constraints[i] = list of positions that cannot be green with position i
    light_states = {}
    results = []
    
    for pos, state in events:
        light_states[pos] = state
        
        # Find longest valid green segment
        max_length = 0
        current_length = 0
        current_segment = []
        
        for i in range(1, n + 1):
            if light_states.get(i, True):  # Default to green
                # Check if adding this light violates constraints
                valid = True
                for light in current_segment:
                    if i in constraints.get(light, []):
                        valid = False
                        break
                
                if valid:
                    current_length += 1
                    current_segment.append(i)
                    max_length = max(max_length, current_length)
                else:
                    # Reset segment
                    current_length = 1
                    current_segment = [i]
            else:
                current_length = 0
                current_segment = []
        
        results.append(max_length)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Set Operations Problems**
- **Set Union**: Combine elements from multiple sets
- **Set Intersection**: Find common elements
- **Set Difference**: Find elements in one set but not another
- **Set Symmetric Difference**: Find elements in exactly one set

#### **2. Interval Management Problems**
- **Interval Scheduling**: Schedule non-overlapping intervals
- **Interval Merging**: Merge overlapping intervals
- **Interval Partitioning**: Partition intervals into groups
- **Interval Queries**: Query intervals efficiently

#### **3. Array Processing Problems**
- **Array Manipulation**: Efficient array operations
- **Array Partitioning**: Partition array based on conditions
- **Array Merging**: Merge sorted arrays
- **Array Sorting**: Sort array efficiently

#### **4. Dynamic Programming Problems**
- **Longest Increasing Subsequence**: Find LIS in array
- **Maximum Subarray Sum**: Find maximum subarray sum
- **Subarray Problems**: Various subarray problems
- **Sequence Problems**: Sequence-related problems

#### **5. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions
- **Greedy Algorithms**: Local optimal choices

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    events = [int(input()) for _ in range(q)]
    
    red_lights = set()
    results = []
    
    for event in events:
        if event in red_lights:
            red_lights.remove(event)
        else:
            red_lights.add(event)
        
        if not red_lights:
            max_length = n
        else:
            red_list = sorted(red_lights)
            max_length = max(red_list[0] - 1, n - red_list[-1])
            
            for i in range(1, len(red_list)):
                gap = red_list[i] - red_list[i-1] - 1
                max_length = max(max_length, gap)
        
        results.append(max_length)
    
    print(*results)
```

#### **2. Range Queries**
```python
# Precompute longest green segments for different ranges
def precompute_traffic_segments(n, events):
    segment_data = {}
    
    for start_pos in range(1, n + 1):
        for end_pos in range(start_pos, n + 1):
            # Simulate events in this range
            red_lights = set()
            for event in events:
                if start_pos <= event <= end_pos:
                    if event in red_lights:
                        red_lights.remove(event)
                    else:
                        red_lights.add(event)
            
            # Calculate max length for this range
            if not red_lights:
                max_length = end_pos - start_pos + 1
            else:
                red_list = sorted(red_lights)
                max_length = max(red_list[0] - start_pos, end_pos - red_list[-1])
                
                for i in range(1, len(red_list)):
                    gap = red_list[i] - red_list[i-1] - 1
                    max_length = max(max_length, gap)
            
            segment_data[(start_pos, end_pos)] = max_length
    
    return segment_data

# Answer queries about longest green segments in ranges
def segment_query(segment_data, start, end):
    return segment_data.get((start, end), 0)
```

#### **3. Interactive Problems**
```python
# Interactive traffic lights simulator
def interactive_traffic_lights():
    n = int(input("Enter number of traffic lights: "))
    q = int(input("Enter number of events: "))
    
    print(f"Street with {n} traffic lights")
    print("All lights start green")
    
    red_lights = set()
    
    for i in range(q):
        pos = int(input(f"Enter position for event {i+1}: "))
        
        if pos in red_lights:
            red_lights.remove(pos)
            print(f"Light at position {pos} turned GREEN")
        else:
            red_lights.add(pos)
            print(f"Light at position {pos} turned RED")
        
        # Calculate max length
        if not red_lights:
            max_length = n
            print(f"All lights are green! Max length: {max_length}")
        else:
            red_list = sorted(red_lights)
            max_length = max(red_list[0] - 1, n - red_list[-1])
            
            for j in range(1, len(red_list)):
                gap = red_list[j] - red_list[j-1] - 1
                max_length = max(max_length, gap)
            
            print(f"Red lights at positions: {red_list}")
            print(f"Longest green segment: {max_length}")
        
        print()
```

### 🧮 **Mathematical Extensions**

#### **1. Set Theory**
- **Set Operations**: Union, intersection, difference
- **Set Properties**: Properties of sets
- **Set Cardinality**: Size of sets
- **Set Partitions**: Partitioning sets

#### **2. Interval Theory**
- **Interval Properties**: Properties of intervals
- **Interval Operations**: Operations on intervals
- **Interval Graphs**: Graph representation of intervals
- **Interval Scheduling**: Scheduling with intervals

#### **3. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Amortized Analysis**: Average case analysis
- **Probabilistic Analysis**: Expected performance
- **Worst Case Analysis**: Upper bounds

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Set Operations**: Efficient set algorithms
- **Interval Management**: Efficient interval algorithms
- **Array Processing**: Efficient array operations
- **Dynamic Programming**: Optimal substructure

#### **2. Mathematical Concepts**
- **Set Theory**: Theory of sets
- **Interval Theory**: Theory of intervals
- **Algorithm Analysis**: Complexity and correctness
- **Discrete Mathematics**: Discrete structures

#### **3. Programming Concepts**
- **Set Implementation**: Efficient set operations
- **Interval Management**: Efficient interval handling
- **Algorithm Design**: Problem-solving strategies
- **Data Structure Design**: Efficient data structures

---

*This analysis demonstrates set operations and interval management techniques for traffic light problems.* 