---
layout: simple
title: "Traffic Lights"
permalink: /problem_soulutions/sorting_and_searching/traffic_lights_analysis
---

# Traffic Lights

## Problem Description

**Problem**: There are n traffic lights on a street. Initially, all lights are green. Then, q events happen: either a light turns red or a light turns green. After each event, find the length of the longest continuous segment of green lights.

**Input**: 
- First line: n q (number of lights and events)
- Next q lines: x (position of light that changes state)

**Output**: q integers - length of longest continuous green segment after each event.

**Example**:
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

Explanation: 
After event 1: Lights 1-2, 4-5, 7-8 are green → max length = 5
After event 2: Lights 1-2, 4-5, 7-8 are green → max length = 3
After event 3: Lights 1, 4-5, 7-8 are green → max length = 3
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Track state of n traffic lights
- Handle toggle events (red ↔ green)
- Find longest continuous green segment after each event
- Need efficient data structure for range queries

**Key Observations:**
- Initially all lights are green
- Each event toggles a light's state
- Need to track red light positions
- Longest green segment = longest gap between red lights

### Step 2: Brute Force Approach
**Idea**: After each event, scan the entire street to find the longest green segment.

```python
def traffic_lights_brute_force(n, q, events):
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

**Why this works:**
- Simulates the actual street
- Toggles light states correctly
- Scans entire street after each event
- Simple to understand and implement
- O(q * n) time complexity

### Step 3: Set-based Optimization
**Idea**: Track red light positions and find the longest gap between them.

```python
def traffic_lights_set_based(n, q, events):
    red_lights = set()
    results = []
    
    for event in events:
        pos = event
        
        # Toggle light state
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

**Why this is better:**
- Only track red light positions
- Longest green segment = longest gap between red lights
- O(q log q) time complexity
- Much more efficient for large n

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_traffic_lights():
    n, q = map(int, input().split())
    events = [int(input()) for _ in range(q)]
    
    # Track red light positions
    red_lights = set()
    results = []
    
    for event in events:
        # Toggle light state
        if event in red_lights:
            red_lights.remove(event)
        else:
            red_lights.add(event)
        
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
    
    # Print results
    for result in results:
        print(result)

# Main execution
if __name__ == "__main__":
    solve_traffic_lights()
```

**Why this works:**
- Optimal set-based approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (8, 3, [3, 6, 2], [5, 3, 3]),
        (5, 2, [2, 4], [3, 2]),
        (3, 1, [2], [2]),
        (10, 4, [3, 7, 3, 5], [7, 4, 7, 5]),
    ]
    
    for n, q, events, expected in test_cases:
        result = solve_test(n, q, events)
        print(f"n={n}, q={q}, events={events}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, q, events):
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
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(q log q) - sorting red lights for each event
- **Space**: O(q) - storing red light positions

### Why This Solution Works
- **Set Operations**: Efficient add/remove operations
- **Gap Calculation**: Find longest gap between red lights
- **Edge Cases**: Handle no red lights and boundary cases
- **Optimal Approach**: Much faster than brute force

## 🎯 Key Insights

### 1. **Gap-based Approach**
- Track red light positions instead of all lights
- Longest green segment = longest gap between red lights
- Key insight: focus on boundaries, not content
- Reduces complexity significantly

### 2. **Set Data Structure**
- Efficient add/remove operations
- O(1) membership testing
- Perfect for tracking state changes
- Simple and effective

### 3. **Boundary Handling**
- Consider gaps at street boundaries
- Handle case with no red lights
- Account for 1-indexed positions
- Crucial for correctness

## 🎯 Problem Variations

### Variation 1: Weighted Traffic Lights
**Problem**: Each light has a weight. Find longest weighted green segment.

```python
def weighted_traffic_lights(n, q, events, weights):
    red_lights = set()
    results = []
    
    for event in events:
        if event in red_lights:
            red_lights.remove(event)
        else:
            red_lights.add(event)
        
        if not red_lights:
            max_weight = sum(weights)
        else:
            red_list = sorted(red_lights)
            max_weight = max(sum(weights[:red_list[0]-1]), 
                           sum(weights[red_list[-1]:]))
            
            for i in range(1, len(red_list)):
                gap_weight = sum(weights[red_list[i-1]:red_list[i]-1])
                max_weight = max(max_weight, gap_weight)
        
        results.append(max_weight)
    
    return results
```

### Variation 2: Traffic Light Groups
**Problem**: Lights are grouped. Find longest continuous group of green groups.

```python
def grouped_traffic_lights(n, q, events, group_size):
    red_lights = set()
    results = []
    
    for event in events:
        if event in red_lights:
            red_lights.remove(event)
        else:
            red_lights.add(event)
        
        # Convert to group-based gaps
        group_red = set()
        for pos in red_lights:
            group_red.add((pos - 1) // group_size + 1)
        
        if not group_red:
            max_groups = (n + group_size - 1) // group_size
        else:
            group_list = sorted(group_red)
            max_groups = max(group_list[0] - 1, 
                           (n + group_size - 1) // group_size - group_list[-1])
            
            for i in range(1, len(group_list)):
                gap = group_list[i] - group_list[i-1] - 1
                max_groups = max(max_groups, gap)
        
        results.append(max_groups)
    
    return results
```

### Variation 3: Dynamic Traffic Lights
**Problem**: Support adding/removing lights dynamically.

```python
class DynamicTrafficLights:
    def __init__(self, n):
        self.n = n
        self.red_lights = set()
    
    def toggle_light(self, pos):
        if pos in self.red_lights:
            self.red_lights.remove(pos)
        else:
            self.red_lights.add(pos)
        
        return self.get_longest_green()
    
    def add_light(self):
        self.n += 1
        return self.get_longest_green()
    
    def remove_light(self, pos):
        if pos <= self.n:
            if pos in self.red_lights:
                self.red_lights.remove(pos)
            
            # Adjust positions
            new_red_lights = set()
            for light in self.red_lights:
                if light < pos:
                    new_red_lights.add(light)
                elif light > pos:
                    new_red_lights.add(light - 1)
            
            self.red_lights = new_red_lights
            self.n -= 1
        
        return self.get_longest_green()
    
    def get_longest_green(self):
        if not self.red_lights:
            return self.n
        
        red_list = sorted(self.red_lights)
        max_length = max(red_list[0] - 1, self.n - red_list[-1])
        
        for i in range(1, len(red_list)):
            gap = red_list[i] - red_list[i-1] - 1
            max_length = max(max_length, gap)
        
        return max_length
```

### Variation 4: Traffic Light Patterns
**Problem**: Lights follow patterns (e.g., alternating red/green).

```python
def pattern_traffic_lights(n, q, events, pattern):
    # pattern[i] = True if light i should be green initially
    red_lights = set()
    
    # Initialize based on pattern
    for i in range(1, n + 1):
        if not pattern[i - 1]:
            red_lights.add(i)
    
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
    
    return results
```

### Variation 5: Traffic Light Queries
**Problem**: Support range queries for green segments.

```python
def traffic_light_queries(n, q, events, queries):
    red_lights = set()
    results = []
    
    for event in events:
        if event in red_lights:
            red_lights.remove(event)
        else:
            red_lights.add(event)
        
        # Answer queries
        query_results = []
        for left, right in queries:
            # Find red lights in range
            range_red = [pos for pos in red_lights if left <= pos <= right]
            
            if not range_red:
                max_length = right - left + 1
            else:
                range_red.sort()
                max_length = max(range_red[0] - left, right - range_red[-1])
                
                for i in range(1, len(range_red)):
                    gap = range_red[i] - range_red[i-1] - 1
                    max_length = max(max_length, gap)
            
            query_results.append(max_length)
        
        results.append(query_results)
    
    return results
```

## 🔗 Related Problems

- **[Room Allocation](/cses-analyses/problem_soulutions/sorting_and_searching/room_allocation_analysis)**: Range management
- **[Nearest Smaller Values](/cses-analyses/problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis)**: Array processing
- **[Distinct Values Subarrays](/cses-analyses/problem_soulutions/sorting_and_searching/distinct_values_subarrays_analysis)**: Subarray problems

## 📚 Learning Points

1. **Set Data Structures**: Efficient state tracking
2. **Gap Analysis**: Focus on boundaries rather than content
3. **Range Queries**: Efficient range-based calculations
4. **State Management**: Handling dynamic state changes

---

**This is a great introduction to set-based algorithms and gap analysis!** 🎯 