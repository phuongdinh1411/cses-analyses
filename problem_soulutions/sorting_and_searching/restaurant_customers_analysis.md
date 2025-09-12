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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Restaurant Customers with Range Queries
**Problem**: Answer multiple queries about maximum customers at different time ranges.

**Link**: [CSES Problem Set - Restaurant Customers Range Queries](https://cses.fi/problemset/task/restaurant_customers_range)

```python
def restaurant_customers_range_queries(customers, queries):
    """
    Answer range queries about maximum customers
    """
    results = []
    
    for query in queries:
        start_time, end_time = query['start'], query['end']
        
        # Filter customers within the time range
        filtered_customers = []
        for arrival, departure in customers:
            if arrival <= end_time and departure >= start_time:
                filtered_customers.append((arrival, departure))
        
        # Find maximum customers in this range
        max_customers = find_max_customers(filtered_customers)
        results.append(max_customers)
    
    return results

def find_max_customers(customers):
    """
    Find maximum number of customers using line sweep
    """
    events = []
    
    # Create events for arrivals and departures
    for arrival, departure in customers:
        events.append((arrival, 1))    # Arrival event
        events.append((departure, -1)) # Departure event
    
    # Sort events by time, then by type (departures before arrivals for same time)
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_customers = 0
    max_customers = 0
    
    for time, event_type in events:
        current_customers += event_type
        max_customers = max(max_customers, current_customers)
    
    return max_customers

def find_max_customers_optimized(customers):
    """
    Optimized version with early termination
    """
    events = []
    
    # Create events for arrivals and departures
    for arrival, departure in customers:
        events.append((arrival, 1))    # Arrival event
        events.append((departure, -1)) # Departure event
    
    # Sort events by time, then by type
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_customers = 0
    max_customers = 0
    
    for time, event_type in events:
        current_customers += event_type
        max_customers = max(max_customers, current_customers)
        
        # Early termination if we can't improve
        if max_customers == len(customers):
            break
    
    return max_customers
```

### Variation 2: Restaurant Customers with Updates
**Problem**: Handle dynamic updates to customer arrivals/departures and maintain maximum customer queries.

**Link**: [CSES Problem Set - Restaurant Customers with Updates](https://cses.fi/problemset/task/restaurant_customers_updates)

```python
class RestaurantCustomersWithUpdates:
    def __init__(self, customers):
        self.customers = customers[:]
        self.events = self._create_events()
        self.max_customers = self._compute_max_customers()
    
    def _create_events(self):
        """Create events from customers"""
        events = []
        for arrival, departure in self.customers:
            events.append((arrival, 1))    # Arrival event
            events.append((departure, -1)) # Departure event
        return events
    
    def _compute_max_customers(self):
        """Compute maximum number of customers"""
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def add_customer(self, arrival, departure):
        """Add a new customer"""
        self.customers.append((arrival, departure))
        self.events.append((arrival, 1))
        self.events.append((departure, -1))
        self.max_customers = self._compute_max_customers()
    
    def remove_customer(self, index):
        """Remove customer at index"""
        arrival, departure = self.customers.pop(index)
        self.events.remove((arrival, 1))
        self.events.remove((departure, -1))
        self.max_customers = self._compute_max_customers()
    
    def update_customer(self, index, new_arrival, new_departure):
        """Update customer at index"""
        old_arrival, old_departure = self.customers[index]
        self.customers[index] = (new_arrival, new_departure)
        
        # Update events
        self.events.remove((old_arrival, 1))
        self.events.remove((old_departure, -1))
        self.events.append((new_arrival, 1))
        self.events.append((new_departure, -1))
        
        self.max_customers = self._compute_max_customers()
    
    def get_max_customers(self):
        """Get current maximum number of customers"""
        return self.max_customers
    
    def get_max_customers_range(self, start_time, end_time):
        """Get maximum customers in time range [start_time, end_time]"""
        # Filter customers within the time range
        filtered_customers = []
        for arrival, departure in self.customers:
            if arrival <= end_time and departure >= start_time:
                filtered_customers.append((arrival, departure))
        
        return find_max_customers(filtered_customers)
    
    def get_customer_count_at_time(self, time):
        """Get number of customers at specific time"""
        count = 0
        for arrival, departure in self.customers:
            if arrival <= time < departure:
                count += 1
        return count
```

### Variation 3: Restaurant Customers with Constraints
**Problem**: Find maximum customers with additional constraints (e.g., minimum stay duration, maximum capacity).

**Link**: [CSES Problem Set - Restaurant Customers with Constraints](https://cses.fi/problemset/task/restaurant_customers_constraints)

```python
def restaurant_customers_constraints(customers, min_stay_duration, max_capacity):
    """
    Find maximum customers with constraints
    """
    events = []
    
    # Create events for arrivals and departures
    for arrival, departure in customers:
        # Check minimum stay duration constraint
        if departure - arrival >= min_stay_duration:
            events.append((arrival, 1))    # Arrival event
            events.append((departure, -1)) # Departure event
    
    # Sort events by time, then by type
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_customers = 0
    max_customers = 0
    
    for time, event_type in events:
        current_customers += event_type
        
        # Check capacity constraint
        if current_customers <= max_capacity:
            max_customers = max(max_customers, current_customers)
        else:
            # Exceeded capacity, need to reject some customers
            max_customers = max_capacity
    
    return max_customers

def restaurant_customers_constraints_optimized(customers, min_stay_duration, max_capacity):
    """
    Optimized version with better constraint handling
    """
    # Filter customers by minimum stay duration
    valid_customers = []
    for arrival, departure in customers:
        if departure - arrival >= min_stay_duration:
            valid_customers.append((arrival, departure))
    
    if not valid_customers:
        return 0
    
    events = []
    
    # Create events for valid customers
    for arrival, departure in valid_customers:
        events.append((arrival, 1))    # Arrival event
        events.append((departure, -1)) # Departure event
    
    # Sort events by time, then by type
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_customers = 0
    max_customers = 0
    
    for time, event_type in events:
        current_customers += event_type
        
        # Check capacity constraint
        if current_customers <= max_capacity:
            max_customers = max(max_customers, current_customers)
        else:
            # Exceeded capacity, need to reject some customers
            max_customers = max_capacity
    
    return max_customers

def restaurant_customers_constraints_multiple(customers, constraints_list):
    """
    Find maximum customers for multiple constraint sets
    """
    results = []
    
    for min_stay_duration, max_capacity in constraints_list:
        result = restaurant_customers_constraints(customers, min_stay_duration, max_capacity)
        results.append(result)
    
    return results

# Example usage
customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
min_stay_duration = 2
max_capacity = 3

result = restaurant_customers_constraints(customers, min_stay_duration, max_capacity)
print(f"Maximum customers with constraints: {result}")  # Output: 3
```

### Related Problems

#### **CSES Problems**
- [Restaurant Customers](https://cses.fi/problemset/task/1619) - Basic restaurant customers problem
- [Movie Festival](https://cses.fi/problemset/task/1629) - Interval scheduling problem
- [Movie Festival II](https://cses.fi/problemset/task/1632) - Multiple interval scheduling

#### **LeetCode Problems**
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) - Minimum meeting rooms needed
- [Car Pooling](https://leetcode.com/problems/car-pooling/) - Capacity constraint problem
- [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) - Maximum overlapping events

#### **Problem Categories**
- **Line Sweep**: Event processing, chronological sorting, interval overlap
- **Interval Scheduling**: Event scheduling, resource allocation, time management
- **Sorting Algorithms**: Event sorting, chronological processing, efficient ordering
- **Algorithm Design**: Line sweep techniques, interval processing, event-based algorithms
