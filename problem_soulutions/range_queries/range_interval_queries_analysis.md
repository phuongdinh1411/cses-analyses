# CSES Range Interval Queries - Problem Analysis

## Problem Statement
Given n intervals, process q queries. Each query asks for the number of intervals that contain a given point x.

### Input
The first input line has two integers n and q: the number of intervals and the number of queries.
Then there are n lines describing the intervals. Each line has two integers a and b: the interval [a,b].
Then there are q lines describing the queries. Each line has one integer x: find the number of intervals containing x.

### Output
Print the answer to each query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ a,b,x ≤ 10^9

### Example
```
Input:
3 2
1 5
2 8
3 6
4
7

Output:
2
1
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct interval checking.

```python
def range_interval_queries_naive(n, q, intervals, queries):
    result = []
    
    for x in queries:
        count = 0
        for a, b in intervals:
            if a <= x <= b:
                count += 1
        result.append(count)
    
    return result
```

**Why this is inefficient**: Each query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Coordinate Compression with Binary Indexed Tree - O(n log n + q log n)
**Description**: Use coordinate compression and BIT for efficient range counting.

```python
def range_interval_queries_bit(n, q, intervals, queries):
    from collections import defaultdict
    from bisect import bisect_left
    
    # Coordinate compression
    coordinates = set()
    for a, b in intervals:
        coordinates.add(a)
        coordinates.add(b)
    for x in queries:
        coordinates.add(x)
    
    # Sort and assign compressed coordinates
    sorted_coords = sorted(coordinates)
    coord_to_idx = {coord: idx for idx, coord in enumerate(sorted_coords)}
    
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        
        def update(self, index, val):
            while index <= self.n:
                self.tree[index] += val
                index += index & -index
        
        def query(self, index):
            total = 0
            while index > 0:
                total += self.tree[index]
                index -= index & -index
            return total
    
    # Initialize BIT
    bit = BIT(len(sorted_coords))
    
    # Add intervals to BIT
    for a, b in intervals:
        start_idx = coord_to_idx[a] + 1
        end_idx = coord_to_idx[b] + 1
        bit.update(start_idx, 1)
        bit.update(end_idx + 1, -1)
    
    # Process queries
    result = []
    for x in queries:
        idx = coord_to_idx[x] + 1
        count = bit.query(idx)
        result.append(count)
    
    return result
```

**Why this improvement works**: We use coordinate compression and BIT to efficiently count intervals containing a point.

### Improvement 2: Line Sweep with Events - O(n log n + q log n)
**Description**: Use line sweep algorithm with events for efficient processing.

```python
def range_interval_queries_line_sweep(n, q, intervals, queries):
    # Create events: (position, type, query_index)
    events = []
    
    # Add interval events
    for a, b in intervals:
        events.append((a, 1, -1))  # Start of interval
        events.append((b + 1, -1, -1))  # End of interval (exclusive)
    
    # Add query events
    for i, x in enumerate(queries):
        events.append((x, 0, i))  # Query point
    
    # Sort events by position
    events.sort()
    
    # Process events
    active_intervals = 0
    result = [0] * q
    
    for pos, event_type, query_idx in events:
        if event_type == 1:  # Start of interval
            active_intervals += 1
        elif event_type == -1:  # End of interval
            active_intervals -= 1
        else:  # Query point
            result[query_idx] = active_intervals
    
    return result
```

**Why this improvement works**: Line sweep algorithm efficiently processes all events in sorted order.

## Final Optimal Solution

```python
n, q = map(int, input().split())
intervals = []
for _ in range(n):
    a, b = map(int, input().split())
    intervals.append((a, b))
queries = []
for _ in range(q):
    x = int(input())
    queries.append(x)

def process_range_interval_queries(n, q, intervals, queries):
    # Create events: (position, type, query_index)
    events = []
    
    # Add interval events
    for a, b in intervals:
        events.append((a, 1, -1))  # Start of interval
        events.append((b + 1, -1, -1))  # End of interval (exclusive)
    
    # Add query events
    for i, x in enumerate(queries):
        events.append((x, 0, i))  # Query point
    
    # Sort events by position
    events.sort()
    
    # Process events
    active_intervals = 0
    result = [0] * q
    
    for pos, event_type, query_idx in events:
        if event_type == 1:  # Start of interval
            active_intervals += 1
        elif event_type == -1:  # End of interval
            active_intervals -= 1
        else:  # Query point
            result[query_idx] = active_intervals
    
    return result

result = process_range_interval_queries(n, q, intervals, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(1) | Direct interval checking |
| BIT with Compression | O(n log n + q log n) | O(n) | Coordinate compression and BIT |
| Line Sweep | O(n log n + q log n) | O(n + q) | Event-based processing |

## Key Insights for Other Problems

### 1. **Line Sweep Algorithm**
**Principle**: Process events in sorted order to efficiently handle range problems.
**Applicable to**: Range problems, interval problems, event processing

### 2. **Coordinate Compression**
**Principle**: Compress large coordinate values to smaller indices for efficient processing.
**Applicable to**: Large coordinate problems, range problems, optimization

### 3. **Event-Based Processing**
**Principle**: Convert range problems into events that can be processed in sorted order.
**Applicable to**: Range problems, interval problems, sweep line problems

## Notable Techniques

### 1. **Line Sweep Implementation**
```python
def line_sweep_intervals(intervals, queries):
    events = []
    
    # Add interval events
    for a, b in intervals:
        events.append((a, 1))  # Start
        events.append((b + 1, -1))  # End
    
    # Add query events
    for i, x in enumerate(queries):
        events.append((x, 0, i))
    
    events.sort()
    
    active = 0
    result = [0] * len(queries)
    
    for pos, event_type, *args in events:
        if event_type == 1:
            active += 1
        elif event_type == -1:
            active -= 1
        else:
            query_idx = args[0]
            result[query_idx] = active
    
    return result
```

### 2. **Coordinate Compression**
```python
def compress_coordinates(values):
    sorted_values = sorted(set(values))
    coord_to_idx = {val: idx for idx, val in enumerate(sorted_values)}
    return coord_to_idx, sorted_values
```

### 3. **Event Processing**
```python
def process_events(events):
    events.sort()
    active_count = 0
    result = []
    
    for pos, event_type in events:
        if event_type == 1:  # Start
            active_count += 1
        elif event_type == -1:  # End
            active_count -= 1
        result.append(active_count)
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is an interval containment problem
2. **Choose approach**: Use line sweep algorithm with events
3. **Create events**: Convert intervals and queries into events
4. **Sort events**: Sort by position for line sweep
5. **Process events**: Track active intervals and answer queries
6. **Return result**: Output count for each query

---

*This analysis shows how to efficiently count intervals containing a point using line sweep algorithm.* 