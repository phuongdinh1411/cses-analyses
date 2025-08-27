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