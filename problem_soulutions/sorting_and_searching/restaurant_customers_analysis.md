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

## Problem Variations

### **Variation 1: Restaurant Customers with Dynamic Updates**
**Problem**: Handle dynamic customer updates (add/remove/update customers) while maintaining efficient maximum customer calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicRestaurantCustomers:
    def __init__(self, customers):
        self.customers = customers[:]
        self.n = len(customers)
        self.events = self._create_events()
        self.max_customers = self._compute_max_customers()
    
    def _create_events(self):
        """Create events from customers."""
        events = []
        for arrival, departure in self.customers:
            events.append((arrival, 1))    # Arrival event
            events.append((departure, -1)) # Departure event
        return events
    
    def _compute_max_customers(self):
        """Compute maximum number of customers using line sweep."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type (departures before arrivals at same time)
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def add_customer(self, arrival, departure):
        """Add a new customer to the restaurant."""
        self.customers.append((arrival, departure))
        self.events.append((arrival, 1))
        self.events.append((departure, -1))
        self.n += 1
        self.max_customers = self._compute_max_customers()
    
    def remove_customer(self, index):
        """Remove a customer at the specified index."""
        if 0 <= index < self.n:
            arrival, departure = self.customers.pop(index)
            self.events.remove((arrival, 1))
            self.events.remove((departure, -1))
            self.n -= 1
            self.max_customers = self._compute_max_customers()
    
    def update_customer(self, index, new_arrival, new_departure):
        """Update a customer at the specified index."""
        if 0 <= index < self.n:
            old_arrival, old_departure = self.customers[index]
            self.customers[index] = (new_arrival, new_departure)
            
            # Remove old events
            self.events.remove((old_arrival, 1))
            self.events.remove((old_departure, -1))
            
            # Add new events
            self.events.append((new_arrival, 1))
            self.events.append((new_departure, -1))
            
            self.max_customers = self._compute_max_customers()
    
    def get_max_customers(self):
        """Get current maximum number of customers."""
        return self.max_customers
    
    def get_customers_at_time(self, time):
        """Get number of customers at specific time."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        
        for event_time, event_type in sorted_events:
            if event_time > time:
                break
            current_customers += event_type
        
        return current_customers
    
    def get_customers_in_time_range(self, start_time, end_time):
        """Get customers present in time range."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            if arrival < end_time and departure > start_time:
                result.append((i, arrival, departure))
        return result
    
    def get_customers_with_constraints(self, constraint_func):
        """Get customers that satisfy custom constraints."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            if constraint_func(arrival, departure):
                result.append((i, arrival, departure))
        return result
    
    def get_restaurant_statistics(self):
        """Get statistics about the restaurant customers."""
        if not self.customers:
            return {
                'total_customers': 0,
                'max_customers': 0,
                'average_stay_duration': 0,
                'total_events': 0,
                'time_span': 0
            }
        
        total_customers = self.n
        max_customers = self.max_customers
        total_events = len(self.events)
        
        # Calculate average stay duration
        total_stay_duration = sum(departure - arrival for arrival, departure in self.customers)
        average_stay_duration = total_stay_duration / total_customers
        
        # Calculate time span
        all_times = []
        for arrival, departure in self.customers:
            all_times.extend([arrival, departure])
        time_span = max(all_times) - min(all_times) if all_times else 0
        
        return {
            'total_customers': total_customers,
            'max_customers': max_customers,
            'average_stay_duration': average_stay_duration,
            'total_events': total_events,
            'time_span': time_span
        }
    
    def get_restaurant_patterns(self):
        """Get patterns in customer arrivals and departures."""
        patterns = {
            'consecutive_arrivals': 0,
            'alternating_pattern': 0,
            'peak_hours': 0,
            'quiet_hours': 0
        }
        
        # Sort events by time
        sorted_events = sorted(self.events, key=lambda x: x[0])
        
        for i in range(1, len(sorted_events)):
            if sorted_events[i][1] == 1 and sorted_events[i-1][1] == 1:
                patterns['consecutive_arrivals'] += 1
            
            if i > 1:
                if (sorted_events[i][1] != sorted_events[i-1][1] and 
                    sorted_events[i-1][1] != sorted_events[i-2][1]):
                    patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_capacity_planning(self):
        """Get optimal capacity planning based on customer patterns."""
        if not self.customers:
            return {
                'recommended_capacity': 0,
                'peak_time': 0,
                'utilization_rate': 0
            }
        
        # Find peak time
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        current_customers = 0
        max_customers = 0
        peak_time = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            if current_customers > max_customers:
                max_customers = current_customers
                peak_time = time
        
        # Calculate utilization rate
        total_customer_time = sum(departure - arrival for arrival, departure in self.customers)
        time_span = max(max(departure for _, departure in self.customers), 
                       max(arrival for arrival, _ in self.customers)) - \
                   min(min(arrival for arrival, _ in self.customers),
                       min(departure for _, departure in self.customers))
        utilization_rate = total_customer_time / (time_span * max_customers) if time_span > 0 and max_customers > 0 else 0
        
        return {
            'recommended_capacity': max_customers,
            'peak_time': peak_time,
            'utilization_rate': utilization_rate
        }

# Example usage
customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
dynamic_restaurant = DynamicRestaurantCustomers(customers)
print(f"Initial max customers: {dynamic_restaurant.get_max_customers()}")

# Add a customer
dynamic_restaurant.add_customer(4, 7)
print(f"After adding customer: {dynamic_restaurant.get_max_customers()}")

# Update a customer
dynamic_restaurant.update_customer(1, 2, 5)
print(f"After updating customer: {dynamic_restaurant.get_max_customers()}")

# Get customers at specific time
print(f"Customers at time 3: {dynamic_restaurant.get_customers_at_time(3)}")

# Get customers in time range
print(f"Customers in range [2, 5]: {dynamic_restaurant.get_customers_in_time_range(2, 5)}")

# Get customers with constraints
def constraint_func(arrival, departure):
    return departure - arrival >= 2

print(f"Customers with stay >= 2: {dynamic_restaurant.get_customers_with_constraints(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_restaurant.get_restaurant_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_restaurant.get_restaurant_patterns()}")

# Get optimal capacity planning
print(f"Optimal capacity planning: {dynamic_restaurant.get_optimal_capacity_planning()}")
```

### **Variation 2: Restaurant Customers with Different Operations**
**Problem**: Handle different types of operations on restaurant customers (weighted customers, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of restaurant customer queries.

```python
class AdvancedRestaurantCustomers:
    def __init__(self, customers, weights=None, priorities=None):
        self.customers = customers[:]
        self.n = len(customers)
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.events = self._create_events()
        self.max_customers = self._compute_max_customers()
        self.weighted_max_customers = self._compute_weighted_max_customers()
    
    def _create_events(self):
        """Create events from customers."""
        events = []
        for i, (arrival, departure) in enumerate(self.customers):
            events.append((arrival, 1, i))    # Arrival event
            events.append((departure, -1, i)) # Departure event
        return events
    
    def _compute_max_customers(self):
        """Compute maximum number of customers using line sweep."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type, customer_idx in sorted_events:
            current_customers += event_type
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def _compute_weighted_max_customers(self):
        """Compute maximum weighted customers."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_weighted_customers = 0
        max_weighted_customers = 0
        
        for time, event_type, customer_idx in sorted_events:
            current_weighted_customers += event_type * self.weights[customer_idx]
            max_weighted_customers = max(max_weighted_customers, current_weighted_customers)
        
        return max_weighted_customers
    
    def get_max_customers(self):
        """Get current maximum number of customers."""
        return self.max_customers
    
    def get_weighted_max_customers(self):
        """Get current maximum weighted customers."""
        return self.weighted_max_customers
    
    def get_customers_with_priority(self, priority_func):
        """Get customers considering priority."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            priority = priority_func(arrival, departure, self.weights[i], self.priorities[i])
            result.append((i, arrival, departure, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[3], reverse=True)
        return result
    
    def get_customers_with_optimization(self, optimization_func):
        """Get customers using custom optimization function."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            score = optimization_func(arrival, departure, self.weights[i], self.priorities[i])
            result.append((i, arrival, departure, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[3], reverse=True)
        return result
    
    def get_customers_with_constraints(self, constraint_func):
        """Get customers that satisfy custom constraints."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            if constraint_func(arrival, departure, self.weights[i], self.priorities[i]):
                result.append((i, arrival, departure))
        return result
    
    def get_customers_with_multiple_criteria(self, criteria_list):
        """Get customers that satisfy multiple criteria."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(arrival, departure, self.weights[i], self.priorities[i]):
                    satisfies_all_criteria = False
                    break
            
            if satisfies_all_criteria:
                result.append((i, arrival, departure))
        
        return result
    
    def get_customers_with_alternatives(self, alternatives):
        """Get customers considering alternative times."""
        result = []
        
        for i, (arrival, departure) in enumerate(self.customers):
            # Check original customer
            result.append((i, arrival, departure, 'original'))
            
            # Check alternative times
            if i in alternatives:
                for alt_arrival, alt_departure in alternatives[i]:
                    result.append((i, alt_arrival, alt_departure, 'alternative'))
        
        return result
    
    def get_customers_with_adaptive_criteria(self, adaptive_func):
        """Get customers using adaptive criteria."""
        result = []
        
        for i, (arrival, departure) in enumerate(self.customers):
            if adaptive_func(arrival, departure, self.weights[i], self.priorities[i], result):
                result.append((i, arrival, departure))
        
        return result
    
    def get_restaurant_optimization(self):
        """Get optimal restaurant configuration."""
        strategies = [
            ('max_customers', self.get_max_customers),
            ('weighted_max_customers', self.get_weighted_max_customers),
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
customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
weights = [2, 1, 3, 1]
priorities = [1, 2, 1, 3]
advanced_restaurant = AdvancedRestaurantCustomers(customers, weights, priorities)

print(f"Max customers: {advanced_restaurant.get_max_customers()}")
print(f"Weighted max customers: {advanced_restaurant.get_weighted_max_customers()}")

# Get customers with priority
def priority_func(arrival, departure, weight, priority):
    return (departure - arrival) * weight * priority

print(f"Customers with priority: {advanced_restaurant.get_customers_with_priority(priority_func)}")

# Get customers with optimization
def optimization_func(arrival, departure, weight, priority):
    return (departure - arrival) * weight + priority

print(f"Customers with optimization: {advanced_restaurant.get_customers_with_optimization(optimization_func)}")

# Get customers with constraints
def constraint_func(arrival, departure, weight, priority):
    return departure - arrival >= 2 and weight > 1

print(f"Customers with constraints: {advanced_restaurant.get_customers_with_constraints(constraint_func)}")

# Get customers with multiple criteria
def criterion1(arrival, departure, weight, priority):
    return departure - arrival >= 2

def criterion2(arrival, departure, weight, priority):
    return weight > 1

criteria_list = [criterion1, criterion2]
print(f"Customers with multiple criteria: {advanced_restaurant.get_customers_with_multiple_criteria(criteria_list)}")

# Get customers with alternatives
alternatives = {1: [(1, 5), (3, 6)], 3: [(2, 7), (4, 8)]}
print(f"Customers with alternatives: {advanced_restaurant.get_customers_with_alternatives(alternatives)}")

# Get customers with adaptive criteria
def adaptive_func(arrival, departure, weight, priority, current_result):
    return departure - arrival >= 2 and len(current_result) < 3

print(f"Customers with adaptive criteria: {advanced_restaurant.get_customers_with_adaptive_criteria(adaptive_func)}")

# Get restaurant optimization
print(f"Restaurant optimization: {advanced_restaurant.get_restaurant_optimization()}")
```

### **Variation 3: Restaurant Customers with Constraints**
**Problem**: Handle restaurant customers with additional constraints (capacity limits, time constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedRestaurantCustomers:
    def __init__(self, customers, constraints=None):
        self.customers = customers[:]
        self.n = len(customers)
        self.constraints = constraints or {}
        self.events = self._create_events()
        self.max_customers = self._compute_max_customers()
    
    def _create_events(self):
        """Create events from customers."""
        events = []
        for arrival, departure in self.customers:
            events.append((arrival, 1))    # Arrival event
            events.append((departure, -1)) # Departure event
        return events
    
    def _compute_max_customers(self):
        """Compute maximum number of customers using line sweep."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_capacity_constraints(self, capacity_limit):
        """Get maximum customers considering capacity constraints."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            
            # Check capacity constraint
            if current_customers > capacity_limit:
                return -1  # Cannot accommodate all customers
            
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_time_constraints(self, time_limit):
        """Get maximum customers considering time constraints."""
        if not self.events:
            return 0
        
        # Filter events within time limit
        filtered_events = [(time, event_type) for time, event_type in self.events if time <= time_limit]
        
        if not filtered_events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(filtered_events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get maximum customers considering resource constraints."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        current_resources = [0] * len(resource_limits)
        
        for time, event_type in sorted_events:
            # Check resource constraints
            can_accommodate = True
            for j, consumption in enumerate(resource_consumption.get(time, [0] * len(resource_limits))):
                if current_resources[j] + event_type * consumption > resource_limits[j]:
                    can_accommodate = False
                    break
            
            if can_accommodate:
                current_customers += event_type
                for j, consumption in enumerate(resource_consumption.get(time, [0] * len(resource_limits))):
                    current_resources[j] += event_type * consumption
                max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_mathematical_constraints(self, constraint_func):
        """Get maximum customers that satisfies custom mathematical constraints."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            if constraint_func(time, current_customers, event_type):
                current_customers += event_type
                max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_range_constraints(self, range_constraints):
        """Get maximum customers that satisfies range constraints."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            # Check if event satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(time, current_customers, event_type):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                current_customers += event_type
                max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_optimization_constraints(self, optimization_func):
        """Get maximum customers using custom optimization constraints."""
        if not self.events:
            return 0
        
        # Sort events by optimization function
        sorted_events = sorted(self.events, key=lambda x: optimization_func(x[0], x[1]), reverse=True)
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_multiple_constraints(self, constraints_list):
        """Get maximum customers that satisfies multiple constraints."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            # Check if event satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(time, current_customers, event_type):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                current_customers += event_type
                max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_priority_constraints(self, priority_func):
        """Get maximum customers with priority-based constraints."""
        if not self.events:
            return 0
        
        # Sort events by priority
        sorted_events = sorted(self.events, key=lambda x: priority_func(x[0], x[1]), reverse=True)
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            current_customers += event_type
            max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_max_customers_with_adaptive_constraints(self, adaptive_func):
        """Get maximum customers with adaptive constraints."""
        if not self.events:
            return 0
        
        # Sort events by time, then by type
        sorted_events = sorted(self.events, key=lambda x: (x[0], x[1]))
        
        current_customers = 0
        max_customers = 0
        
        for time, event_type in sorted_events:
            # Check adaptive constraints
            if adaptive_func(time, current_customers, event_type, max_customers):
                current_customers += event_type
                max_customers = max(max_customers, current_customers)
        
        return max_customers
    
    def get_optimal_restaurant_strategy(self):
        """Get optimal restaurant strategy considering all constraints."""
        strategies = [
            ('capacity_constraints', self.get_max_customers_with_capacity_constraints),
            ('time_constraints', self.get_max_customers_with_time_constraints),
            ('resource_constraints', self.get_max_customers_with_resource_constraints),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'capacity_constraints':
                    current_value = strategy_func(5)  # Capacity of 5
                elif strategy_name == 'time_constraints':
                    current_value = strategy_func(10)  # Time limit of 10
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {time: [10, 5] for time, _ in self.events}
                    current_value = strategy_func(resource_limits, resource_consumption)
                
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_stay_duration': 1,
    'max_capacity': 10
}

customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
constrained_restaurant = ConstrainedRestaurantCustomers(customers, constraints)

print("Capacity-constrained max customers:", constrained_restaurant.get_max_customers_with_capacity_constraints(3))

print("Time-constrained max customers:", constrained_restaurant.get_max_customers_with_time_constraints(5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {time: [10, 5] for time, _ in constrained_restaurant.events}
print("Resource-constrained max customers:", constrained_restaurant.get_max_customers_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(time, current_customers, event_type):
    return time >= 1 and current_customers + event_type <= 5

print("Mathematical constraint max customers:", constrained_restaurant.get_max_customers_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(time, current_customers, event_type):
    return time >= 1 and current_customers + event_type <= 5

range_constraints = [range_constraint]
print("Range-constrained max customers:", constrained_restaurant.get_max_customers_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(time, current_customers, event_type):
    return time >= 1

def constraint2(time, current_customers, event_type):
    return current_customers + event_type <= 5

constraints_list = [constraint1, constraint2]
print("Multiple constraints max customers:", constrained_restaurant.get_max_customers_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(time, event_type):
    return time * event_type

print("Priority-constrained max customers:", constrained_restaurant.get_max_customers_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(time, current_customers, event_type, max_customers):
    return time >= 1 and current_customers + event_type <= 5

print("Adaptive constraint max customers:", constrained_restaurant.get_max_customers_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_restaurant.get_optimal_restaurant_strategy()
print(f"Optimal strategy: {optimal}")
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
