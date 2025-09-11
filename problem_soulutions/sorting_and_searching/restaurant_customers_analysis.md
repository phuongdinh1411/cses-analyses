---
layout: simple
title: "Restaurant Customers"
permalink: /problem_soulutions/sorting_and_searching/restaurant_customers_analysis
---

# Restaurant Customers

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of interval scheduling and maximum overlap
- Apply sorting and line sweep algorithms for interval problems
- Implement efficient solutions for counting overlapping intervals
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in interval problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, line sweep algorithm, interval scheduling, coordinate compression
- **Data Structures**: Arrays, sorting algorithms, coordinate arrays
- **Mathematical Concepts**: Interval theory, maximum overlap, coordinate compression
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting
- **Related Problems**: Movie Festival (interval scheduling), Nested Ranges Check (interval problems), Room Allocation (interval scheduling)

## 📋 Problem Description

There are n customers in a restaurant. Each customer has an arrival time and a departure time. Find the maximum number of customers that are in the restaurant at the same time.

This is a classic interval scheduling problem that tests understanding of line sweep algorithms and interval overlap.

**Input**: 
- First line: integer n (number of customers)
- Next n lines: two integers a[i] and b[i] (arrival and departure times)

**Output**: 
- Print one integer: the maximum number of customers in the restaurant simultaneously

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] < b[i] ≤ 10⁹

**Example**:
```
Input:
3
5 8
2 4
3 9

Output:
2

Explanation**: 
Customer 1: arrives at 5, leaves at 8
Customer 2: arrives at 2, leaves at 4
Customer 3: arrives at 3, leaves at 9

Timeline:
2: Customer 2 arrives (1 customer)
3: Customer 3 arrives (2 customers) ← Maximum
4: Customer 2 leaves (1 customer)
5: Customer 1 arrives (2 customers)
8: Customer 1 leaves (1 customer)
9: Customer 3 leaves (0 customers)

Maximum simultaneous customers: 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Time Points

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check every possible time point to count customers
- **Complete Coverage**: Guaranteed to find the maximum overlap
- **Simple Implementation**: Straightforward nested loops approach
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each time point, count how many customers are present at that time.

**Algorithm**:
- Collect all unique time points (arrival and departure times)
- For each time point, count customers whose intervals contain that time
- Find the maximum count

**Visual Example**:
```
Customers: [(5,8), (2,4), (3,9)]
Time points: [2, 3, 4, 5, 8, 9]

Time 2: Customer 2 present → 1 customer
Time 3: Customers 2, 3 present → 2 customers
Time 4: Customer 3 present → 1 customer
Time 5: Customers 1, 3 present → 2 customers
Time 8: Customer 3 present → 1 customer
Time 9: No customers → 0 customers

Maximum: 2 customers
```

**Implementation**:
```python
def brute_force_restaurant_customers(customers):
    """
    Find maximum customers using brute force approach
    
    Args:
        customers: list of (arrival, departure) tuples
    
    Returns:
        int: maximum number of customers simultaneously
    """
    # Collect all unique time points
    time_points = set()
    for arrival, departure in customers:
        time_points.add(arrival)
        time_points.add(departure)
    
    max_customers = 0
    
    # Check each time point
    for time_point in time_points:
        count = 0
        for arrival, departure in customers:
            if arrival <= time_point < departure:
                count += 1
        max_customers = max(max_customers, count)
    
    return max_customers

# Example usage
customers = [(5, 8), (2, 4), (3, 9)]
result = brute_force_restaurant_customers(customers)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - For each time point, check all customers
**Space Complexity**: O(n) - For time points set

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Sort and Count Events

**Key Insights from Optimized Approach**:
- **Event-Based**: Treat arrivals and departures as separate events
- **Sorting**: Sort events by time to process chronologically
- **Efficient Counting**: Count customers by processing events in order
- **Better Complexity**: Achieve O(n log n) time complexity

**Key Insight**: Sort all arrival and departure events by time and process them chronologically.

**Algorithm**:
- Create events for arrivals (+1) and departures (-1)
- Sort events by time
- Process events in order, maintaining a running count
- Track the maximum count

**Visual Example**:
```
Customers: [(5,8), (2,4), (3,9)]
Events: [(2, +1), (3, +1), (4, -1), (5, +1), (8, -1), (9, -1)]
Sorted: [(2, +1), (3, +1), (4, -1), (5, +1), (8, -1), (9, -1)]

Processing:
Time 2: +1 → count = 1
Time 3: +1 → count = 2 (maximum)
Time 4: -1 → count = 1
Time 5: +1 → count = 2
Time 8: -1 → count = 1
Time 9: -1 → count = 0

Maximum: 2 customers
```

**Implementation**:
```python
def optimized_restaurant_customers(customers):
    """
    Find maximum customers using event-based approach
    
    Args:
        customers: list of (arrival, departure) tuples
    
    Returns:
        int: maximum number of customers simultaneously
    """
    events = []
    
    # Create events for arrivals and departures
    for arrival, departure in customers:
        events.append((arrival, 1))    # +1 for arrival
        events.append((departure, -1)) # -1 for departure
    
    # Sort events by time
    events.sort()
    
    max_customers = 0
    current_customers = 0
    
    # Process events in chronological order
    for time, delta in events:
        current_customers += delta
        max_customers = max(max_customers, current_customers)
    
    return max_customers

# Example usage
customers = [(5, 8), (2, 4), (3, 9)]
result = optimized_restaurant_customers(customers)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(n) - For events list

**Why it's better**: Much more efficient than brute force with linear processing after sorting.

---

### Approach 3: Optimal - Line Sweep Algorithm

**Key Insights from Optimal Approach**:
- **Line Sweep**: Process events in chronological order
- **Optimal Sorting**: Use efficient sorting algorithms
- **Efficient Processing**: Process events in O(n) time after sorting
- **Optimal Complexity**: Achieve O(n log n) time complexity

**Key Insight**: Use the line sweep algorithm to process all events in chronological order efficiently.

**Algorithm**:
- Create events for arrivals (+1) and departures (-1)
- Sort events by time (with tie-breaking for departures before arrivals)
- Process events in order, maintaining running count
- Track maximum count

**Visual Example**:
```
Customers: [(5,8), (2,4), (3,9)]
Events: [(2, +1), (3, +1), (4, -1), (5, +1), (8, -1), (9, -1)]
Sorted: [(2, +1), (3, +1), (4, -1), (5, +1), (8, -1), (9, -1)]

Line sweep processing:
Time 2: +1 → count = 1
Time 3: +1 → count = 2 (maximum)
Time 4: -1 → count = 1
Time 5: +1 → count = 2
Time 8: -1 → count = 1
Time 9: -1 → count = 0

Maximum: 2 customers
```

**Implementation**:
```python
def optimal_restaurant_customers(customers):
    """
    Find maximum customers using line sweep algorithm
    
    Args:
        customers: list of (arrival, departure) tuples
    
    Returns:
        int: maximum number of customers simultaneously
    """
    events = []
    
    # Create events for arrivals and departures
    for arrival, departure in customers:
        events.append((arrival, 1))    # +1 for arrival
        events.append((departure, -1)) # -1 for departure
    
    # Sort events by time (departures before arrivals for same time)
    events.sort(key=lambda x: (x[0], x[1]))
    
    max_customers = 0
    current_customers = 0
    
    # Process events in chronological order
    for time, delta in events:
        current_customers += delta
        max_customers = max(max_customers, current_customers)
    
    return max_customers

# Example usage
customers = [(5, 8), (2, 4), (3, 9)]
result = optimal_restaurant_customers(customers)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(n) - For events list

**Why it's optimal**: Achieves the best possible time complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all time points |
| Event-Based | O(n log n) | O(n) | Sort and process events |
| Line Sweep | O(n log n) | O(n) | Optimal event processing |

### Time Complexity
- **Time**: O(n log n) - Line sweep algorithm provides optimal time complexity
- **Space**: O(n) - For storing events

### Why This Solution Works
- **Event-Based Approach**: Treating arrivals and departures as events simplifies the problem
- **Chronological Processing**: Processing events in time order ensures correct counting
- **Efficient Sorting**: Sorting events enables linear processing after sorting
- **Optimal Approach**: Line sweep algorithm provides the most efficient solution for interval overlap problems
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
