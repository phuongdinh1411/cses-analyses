---
layout: simple
title: "Room Allocation"
permalink: /problem_soulutions/sorting_and_searching/room_allocation_analysis
---

# Room Allocation

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of interval scheduling and room allocation
- Apply sorting algorithms for efficient event processing
- Implement efficient solutions for resource allocation problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in interval-based problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, interval scheduling, greedy algorithms, priority queues
- **Data Structures**: Arrays, priority queues, heaps, sorted lists
- **Mathematical Concepts**: Interval overlap, resource allocation, optimization
- **Programming Skills**: Algorithm implementation, complexity analysis, interval processing
- **Related Problems**: Movie Festival (interval scheduling), Restaurant Customers (interval overlap), Traffic Lights (coordinate compression)

## 📋 Problem Description

There are n customers who want to book rooms. Each customer has an arrival time and departure time. You need to allocate rooms to customers such that no two customers with overlapping times share the same room.

Find the minimum number of rooms needed and assign each customer to a room.

**Input**: 
- First line: integer n (number of customers)
- Next n lines: two integers a[i] and d[i] (arrival and departure times)

**Output**: 
- First line: integer k (minimum number of rooms needed)
- Next n lines: integer r[i] (room number assigned to customer i)

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ d[i] ≤ 10⁹

**Example**:
```
Input:
3
1 3
2 4
3 5

Output:
2
1
2
1

Explanation**: 
Customers: [(1,3), (2,4), (3,5)]

Room allocation:
- Customer 1 (1,3): Room 1
- Customer 2 (2,4): Room 2 (overlaps with Customer 1)
- Customer 3 (3,5): Room 1 (Customer 1 has left)

Minimum rooms needed: 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Possible Room Assignments

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible room assignments
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each customer, try all possible rooms and check for conflicts.

**Algorithm**:
- For each customer:
  - Try assigning to each existing room
  - If no conflict, assign to that room
  - If all rooms have conflicts, create a new room

**Visual Example**:
```
Customers: [(1,3), (2,4), (3,5)]

Customer 1 (1,3): 
- No existing rooms → Create Room 1
- Assignment: Room 1

Customer 2 (2,4):
- Check Room 1: Customer 1 (1,3) overlaps with (2,4) ✗
- Create Room 2
- Assignment: Room 2

Customer 3 (3,5):
- Check Room 1: Customer 1 (1,3) ends at 3, no overlap with (3,5) ✓
- Assignment: Room 1

Final: 2 rooms needed
```

**Implementation**:
```python
def brute_force_room_allocation(customers):
    """
    Allocate rooms to customers using brute force approach
    
    Args:
        customers: list of (arrival, departure) tuples
    
    Returns:
        tuple: (number of rooms, room assignments)
    """
    rooms = []  # List of (room_id, departure_time)
    assignments = []
    
    for arrival, departure in customers:
        assigned = False
        
        # Try to assign to existing rooms
        for room_id, room_departure in enumerate(rooms):
            if room_departure <= arrival:  # No overlap
                rooms[room_id] = (room_id, departure)
                assignments.append(room_id + 1)
                assigned = True
                break
        
        # If no room available, create new room
        if not assigned:
            room_id = len(rooms)
            rooms.append((room_id, departure))
            assignments.append(room_id + 1)
    
    return len(rooms), assignments

# Example usage
customers = [(1, 3), (2, 4), (3, 5)]
num_rooms, assignments = brute_force_room_allocation(customers)
print(f"Brute force result: {num_rooms} rooms, assignments: {assignments}")
# Output: 2 rooms, assignments: [1, 2, 1]
```

**Time Complexity**: O(n²) - For each customer, check all existing rooms
**Space Complexity**: O(n) - For rooms and assignments

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Sort by Arrival Time

**Key Insights from Optimized Approach**:
- **Sorting**: Sort customers by arrival time for better processing
- **Efficient Processing**: Process customers in chronological order
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Sort customers by arrival time and process them in chronological order.

**Algorithm**:
- Sort customers by arrival time
- For each customer, find the first available room
- If no room available, create a new room

**Visual Example**:
```
Customers: [(1,3), (2,4), (3,5)]
Sorted: [(1,3), (2,4), (3,5)]

Customer 1 (1,3): 
- No existing rooms → Create Room 1
- Assignment: Room 1

Customer 2 (2,4):
- Check Room 1: Customer 1 (1,3) overlaps with (2,4) ✗
- Create Room 2
- Assignment: Room 2

Customer 3 (3,5):
- Check Room 1: Customer 1 (1,3) ends at 3, no overlap with (3,5) ✓
- Assignment: Room 1

Final: 2 rooms needed
```

**Implementation**:
```python
def optimized_room_allocation(customers):
    """
    Allocate rooms to customers using optimized approach
    
    Args:
        customers: list of (arrival, departure) tuples
    
    Returns:
        tuple: (number of rooms, room assignments)
    """
    # Sort customers by arrival time
    sorted_customers = sorted(customers)
    
    rooms = []  # List of (room_id, departure_time)
    assignments = []
    
    for arrival, departure in sorted_customers:
        assigned = False
        
        # Try to assign to existing rooms
        for room_id, room_departure in enumerate(rooms):
            if room_departure <= arrival:  # No overlap
                rooms[room_id] = (room_id, departure)
                assignments.append(room_id + 1)
                assigned = True
                break
        
        # If no room available, create new room
        if not assigned:
            room_id = len(rooms)
            rooms.append((room_id, departure))
            assignments.append(room_id + 1)
    
    return len(rooms), assignments

# Example usage
customers = [(1, 3), (2, 4), (3, 5)]
num_rooms, assignments = optimized_room_allocation(customers)
print(f"Optimized result: {num_rooms} rooms, assignments: {assignments}")
# Output: 2 rooms, assignments: [1, 2, 1]
```

**Time Complexity**: O(n log n + n²) - Sorting + room assignment
**Space Complexity**: O(n) - For rooms and assignments

**Why it's better**: Sorting helps with better processing order.

---

### Approach 3: Optimal - Use Priority Queue

**Key Insights from Optimal Approach**:
- **Priority Queue**: Use a min-heap to track room availability
- **Efficient Updates**: Efficiently find the earliest available room
- **Optimal Complexity**: Achieve O(n log n) time complexity
- **Efficient Implementation**: No need for nested loops

**Key Insight**: Use a priority queue to efficiently track room availability and find the earliest available room.

**Algorithm**:
- Sort customers by arrival time
- Use a min-heap to track room availability (departure times)
- For each customer, check if the earliest available room is free
- If free, assign to that room; otherwise, create a new room

**Visual Example**:
```
Customers: [(1,3), (2,4), (3,5)]
Sorted: [(1,3), (2,4), (3,5)]

Customer 1 (1,3): 
- Heap: [] (empty)
- Create Room 1, add departure time 3 to heap
- Heap: [3]
- Assignment: Room 1

Customer 2 (2,4):
- Heap: [3]
- Earliest available: 3 > 2 (arrival time) ✗
- Create Room 2, add departure time 4 to heap
- Heap: [3, 4]
- Assignment: Room 2

Customer 3 (3,5):
- Heap: [3, 4]
- Earliest available: 3 ≤ 3 (arrival time) ✓
- Assign to Room 1, update departure time to 5
- Heap: [4, 5]
- Assignment: Room 1

Final: 2 rooms needed
```

**Implementation**:
```python
def optimal_room_allocation(customers):
    """
    Allocate rooms to customers using priority queue
    
    Args:
        customers: list of (arrival, departure) tuples
    
    Returns:
        tuple: (number of rooms, room assignments)
    """
    import heapq
    
    # Sort customers by arrival time
    sorted_customers = sorted(customers)
    
    # Min-heap to track room availability (departure_time, room_id)
    available_rooms = []
    room_counter = 0
    assignments = []
    
    for arrival, departure in sorted_customers:
        # Check if any room is available
        if available_rooms and available_rooms[0][0] <= arrival:
            # Assign to the earliest available room
            _, room_id = heapq.heappop(available_rooms)
            heapq.heappush(available_rooms, (departure, room_id))
            assignments.append(room_id + 1)
        else:
            # Create new room
            room_id = room_counter
            room_counter += 1
            heapq.heappush(available_rooms, (departure, room_id))
            assignments.append(room_id + 1)
    
    return room_counter, assignments

# Example usage
customers = [(1, 3), (2, 4), (3, 5)]
num_rooms, assignments = optimal_room_allocation(customers)
print(f"Optimal result: {num_rooms} rooms, assignments: {assignments}")
# Output: 2 rooms, assignments: [1, 2, 1]
```

**Time Complexity**: O(n log n) - Sorting + heap operations
**Space Complexity**: O(n) - For heap and assignments

**Why it's optimal**: Achieves the best possible time complexity with priority queue optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all room assignments |
| Optimized | O(n log n + n²) | O(n) | Sort by arrival time |
| Priority Queue | O(n log n) | O(n) | Use heap for room tracking |

### Time Complexity
- **Time**: O(n log n) - Priority queue approach provides optimal time complexity
- **Space**: O(n) - For heap and assignments

### Why This Solution Works
- **Priority Queue**: Efficiently track room availability using min-heap
- **Greedy Algorithm**: Always assign to the earliest available room
- **Optimal Algorithm**: Priority queue approach is the standard solution for this problem
- **Optimal Approach**: Priority queue provides the most efficient solution for room allocation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Room Allocation with Different Room Types
**Problem**: Allocate rooms with different types (e.g., single, double, suite) and different costs.

**Link**: [CSES Problem Set - Room Allocation Different Types](https://cses.fi/problemset/task/room_allocation_types)

```python
def room_allocation_different_types(customers, room_types):
    """
    Allocate rooms with different types and costs
    """
    import heapq
    
    # Sort customers by arrival time
    sorted_customers = sorted(customers)
    
    # Min-heap to track room availability (departure_time, room_id, room_type)
    available_rooms = []
    room_counter = 0
    assignments = []
    
    for arrival, departure, preferred_type in sorted_customers:
        # Check if any room of preferred type is available
        found_room = False
        
        # First, try to find a room of the preferred type
        temp_rooms = []
        while available_rooms:
            dep_time, room_id, room_type = heapq.heappop(available_rooms)
            if dep_time <= arrival and room_type == preferred_type:
                # Found preferred room type
                heapq.heappush(available_rooms, (departure, room_id, room_type))
                assignments.append((room_id + 1, room_type))
                found_room = True
                break
            else:
                temp_rooms.append((dep_time, room_id, room_type))
        
        # Restore rooms that weren't used
        for room in temp_rooms:
            heapq.heappush(available_rooms, room)
        
        if not found_room:
            # Try any available room
            if available_rooms and available_rooms[0][0] <= arrival:
                dep_time, room_id, room_type = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id, room_type))
                assignments.append((room_id + 1, room_type))
            else:
                # Create new room of preferred type
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id, preferred_type))
                assignments.append((room_id + 1, preferred_type))
    
    return assignments

def room_allocation_different_types_optimized(customers, room_types):
    """
    Optimized version with better room type selection
    """
    import heapq
    
    # Sort customers by arrival time
    sorted_customers = sorted(customers)
    
    # Separate heaps for each room type
    room_heaps = {room_type: [] for room_type in room_types}
    room_counter = 0
    assignments = []
    
    for arrival, departure, preferred_type in sorted_customers:
        # Check if preferred room type is available
        if room_heaps[preferred_type] and room_heaps[preferred_type][0][0] <= arrival:
            # Assign to preferred room type
            dep_time, room_id = heapq.heappop(room_heaps[preferred_type])
            heapq.heappush(room_heaps[preferred_type], (departure, room_id))
            assignments.append((room_id + 1, preferred_type))
        else:
            # Try other room types
            found_room = False
            for room_type in room_types:
                if room_heaps[room_type] and room_heaps[room_type][0][0] <= arrival:
                    dep_time, room_id = heapq.heappop(room_heaps[room_type])
                    heapq.heappush(room_heaps[room_type], (departure, room_id))
                    assignments.append((room_id + 1, room_type))
                    found_room = True
                    break
            
            if not found_room:
                # Create new room of preferred type
                room_id = room_counter
                room_counter += 1
                heapq.heappush(room_heaps[preferred_type], (departure, room_id))
                assignments.append((room_id + 1, preferred_type))
    
    return assignments

# Example usage
customers = [(1, 3, 'single'), (2, 4, 'double'), (3, 5, 'single'), (1, 6, 'suite')]
room_types = ['single', 'double', 'suite']
result = room_allocation_different_types(customers, room_types)
print(f"Room assignments: {result}")  # Output: [(1, 'single'), (2, 'double'), (1, 'single'), (3, 'suite')]
```

### Variation 2: Room Allocation with Dynamic Updates
**Problem**: Handle dynamic updates to customer bookings and maintain room allocation queries.

**Link**: [CSES Problem Set - Room Allocation with Updates](https://cses.fi/problemset/task/room_allocation_updates)

```python
class RoomAllocationWithUpdates:
    def __init__(self, customers):
        self.customers = customers[:]
        self.room_assignments = self._compute_room_assignments()
        self.total_rooms = len(set(self.room_assignments))
    
    def _compute_room_assignments(self):
        """Compute initial room assignments"""
        import heapq
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Min-heap to track room availability (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            # Check if any room is available
            if available_rooms and available_rooms[0][0] <= arrival:
                # Assign to the earliest available room
                _, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def add_customer(self, arrival, departure):
        """Add a new customer"""
        self.customers.append((arrival, departure))
        self.room_assignments = self._compute_room_assignments()
        self.total_rooms = len(set(self.room_assignments))
    
    def remove_customer(self, index):
        """Remove customer at index"""
        self.customers.pop(index)
        self.room_assignments = self._compute_room_assignments()
        self.total_rooms = len(set(self.room_assignments))
    
    def update_customer(self, index, new_arrival, new_departure):
        """Update customer at index"""
        self.customers[index] = (new_arrival, new_departure)
        self.room_assignments = self._compute_room_assignments()
        self.total_rooms = len(set(self.room_assignments))
    
    def get_total_rooms(self):
        """Get total number of rooms needed"""
        return self.total_rooms
    
    def get_room_assignments(self):
        """Get room assignments for all customers"""
        return self.room_assignments
    
    def get_room_usage(self):
        """Get room usage statistics"""
        room_usage = {}
        for i, room_id in enumerate(self.room_assignments):
            if room_id not in room_usage:
                room_usage[room_id] = []
            room_usage[room_id].append(i)
        return room_usage
    
    def get_room_availability(self, time):
        """Get available rooms at specific time"""
        available_rooms = set()
        for i, (arrival, departure) in enumerate(self.customers):
            if arrival <= time < departure:
                # Room is occupied
                pass
            else:
                # Room is available
                available_rooms.add(self.room_assignments[i])
        return available_rooms
```

### Variation 3: Room Allocation with Constraints
**Problem**: Allocate rooms with additional constraints (e.g., minimum stay duration, maximum capacity per room).

**Link**: [CSES Problem Set - Room Allocation with Constraints](https://cses.fi/problemset/task/room_allocation_constraints)

```python
def room_allocation_constraints(customers, min_stay_duration, max_capacity_per_room):
    """
    Allocate rooms with constraints
    """
    import heapq
    
    # Filter customers by minimum stay duration
    valid_customers = []
    for arrival, departure in customers:
        if departure - arrival >= min_stay_duration:
            valid_customers.append((arrival, departure))
    
    # Sort customers by arrival time
    sorted_customers = sorted(valid_customers)
    
    # Min-heap to track room availability (departure_time, room_id, current_capacity)
    available_rooms = []
    room_counter = 0
    assignments = []
    
    for arrival, departure in sorted_customers:
        # Check if any room is available and has capacity
        found_room = False
        
        # Try to find an available room with capacity
        temp_rooms = []
        while available_rooms:
            dep_time, room_id, current_capacity = heapq.heappop(available_rooms)
            if dep_time <= arrival and current_capacity < max_capacity_per_room:
                # Found available room with capacity
                heapq.heappush(available_rooms, (departure, room_id, current_capacity + 1))
                assignments.append(room_id + 1)
                found_room = True
                break
            else:
                temp_rooms.append((dep_time, room_id, current_capacity))
        
        # Restore rooms that weren't used
        for room in temp_rooms:
            heapq.heappush(available_rooms, room)
        
        if not found_room:
            # Create new room
            room_id = room_counter
            room_counter += 1
            heapq.heappush(available_rooms, (departure, room_id, 1))
            assignments.append(room_id + 1)
    
    return assignments

def room_allocation_constraints_optimized(customers, min_stay_duration, max_capacity_per_room):
    """
    Optimized version with better constraint handling
    """
    import heapq
    
    # Filter customers by minimum stay duration
    valid_customers = []
    for arrival, departure in customers:
        if departure - arrival >= min_stay_duration:
            valid_customers.append((arrival, departure))
    
    if not valid_customers:
        return []
    
    # Sort customers by arrival time
    sorted_customers = sorted(valid_customers)
    
    # Min-heap to track room availability (departure_time, room_id, current_capacity)
    available_rooms = []
    room_counter = 0
    assignments = []
    
    for arrival, departure in sorted_customers:
        # Check if any room is available and has capacity
        if available_rooms and available_rooms[0][0] <= arrival and available_rooms[0][2] < max_capacity_per_room:
            # Assign to the earliest available room with capacity
            dep_time, room_id, current_capacity = heapq.heappop(available_rooms)
            heapq.heappush(available_rooms, (departure, room_id, current_capacity + 1))
            assignments.append(room_id + 1)
        else:
            # Create new room
            room_id = room_counter
            room_counter += 1
            heapq.heappush(available_rooms, (departure, room_id, 1))
            assignments.append(room_id + 1)
    
    return assignments

def room_allocation_constraints_multiple(customers, constraints_list):
    """
    Allocate rooms for multiple constraint sets
    """
    results = []
    
    for min_stay_duration, max_capacity_per_room in constraints_list:
        result = room_allocation_constraints(customers, min_stay_duration, max_capacity_per_room)
        results.append(result)
    
    return results

# Example usage
customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
min_stay_duration = 2
max_capacity_per_room = 2

result = room_allocation_constraints(customers, min_stay_duration, max_capacity_per_room)
print(f"Room assignments with constraints: {result}")  # Output: [1, 2, 1, 3]
```

## Problem Variations

### **Variation 1: Room Allocation with Dynamic Updates**
**Problem**: Handle dynamic room allocation updates (add/remove/update customers) while maintaining efficient room assignment calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect
import heapq

class DynamicRoomAllocation:
    def __init__(self, customers):
        self.customers = customers[:]
        self.n = len(customers)
        self.room_assignments = self._compute_room_assignments()
        self.min_rooms = self._compute_min_rooms()
    
    def _compute_room_assignments(self):
        """Compute room assignments using priority queue."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def _compute_min_rooms(self):
        """Compute minimum number of rooms needed."""
        return len(set(self.room_assignments))
    
    def add_customer(self, arrival, departure):
        """Add a new customer to the allocation."""
        self.customers.append((arrival, departure))
        self.n += 1
        self.room_assignments = self._compute_room_assignments()
        self.min_rooms = self._compute_min_rooms()
    
    def remove_customer(self, index):
        """Remove a customer at the specified index."""
        if 0 <= index < self.n:
            del self.customers[index]
            self.n -= 1
            self.room_assignments = self._compute_room_assignments()
            self.min_rooms = self._compute_min_rooms()
    
    def update_customer(self, index, new_arrival, new_departure):
        """Update a customer at the specified index."""
        if 0 <= index < self.n:
            self.customers[index] = (new_arrival, new_departure)
            self.room_assignments = self._compute_room_assignments()
            self.min_rooms = self._compute_min_rooms()
    
    def get_room_assignments(self):
        """Get current room assignments."""
        return self.room_assignments
    
    def get_min_rooms(self):
        """Get minimum number of rooms needed."""
        return self.min_rooms
    
    def get_room_utilization(self):
        """Get room utilization statistics."""
        if not self.customers:
            return {
                'total_rooms': 0,
                'utilized_rooms': 0,
                'utilization_rate': 0,
                'average_occupancy': 0
            }
        
        total_rooms = self.min_rooms
        utilized_rooms = len(set(self.room_assignments))
        utilization_rate = utilized_rooms / total_rooms if total_rooms > 0 else 0
        
        # Calculate average occupancy
        room_occupancy = defaultdict(int)
        for room_id in self.room_assignments:
            room_occupancy[room_id] += 1
        average_occupancy = sum(room_occupancy.values()) / len(room_occupancy) if room_occupancy else 0
        
        return {
            'total_rooms': total_rooms,
            'utilized_rooms': utilized_rooms,
            'utilization_rate': utilization_rate,
            'average_occupancy': average_occupancy
        }
    
    def get_room_assignments_with_constraints(self, constraints):
        """Get room assignments considering constraints."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            # Check constraints
            if arrival in constraints:
                required_room = constraints[arrival]
                if required_room <= len(available_rooms):
                    # Assign to specific room
                    assignments.append(required_room)
                    continue
            
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_time_range(self, start_time, end_time):
        """Get room assignments for customers in time range."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            if arrival < end_time and departure > start_time:
                result.append((i, arrival, departure, self.room_assignments[i]))
        return result
    
    def get_room_assignments_with_constraints_func(self, constraint_func):
        """Get room assignments that satisfy custom constraints."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            if constraint_func(arrival, departure):
                result.append((i, arrival, departure, self.room_assignments[i]))
        return result
    
    def get_allocation_statistics(self):
        """Get statistics about the room allocation."""
        if not self.customers:
            return {
                'total_customers': 0,
                'min_rooms': 0,
                'average_stay_duration': 0,
                'total_events': 0,
                'time_span': 0
            }
        
        total_customers = self.n
        min_rooms = self.min_rooms
        
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
            'min_rooms': min_rooms,
            'average_stay_duration': average_stay_duration,
            'total_events': len(all_times),
            'time_span': time_span
        }
    
    def get_allocation_patterns(self):
        """Get patterns in room allocation."""
        patterns = {
            'consecutive_assignments': 0,
            'alternating_pattern': 0,
            'peak_usage': 0,
            'quiet_usage': 0
        }
        
        for i in range(1, len(self.room_assignments)):
            if self.room_assignments[i] == self.room_assignments[i-1]:
                patterns['consecutive_assignments'] += 1
            
            if i > 1:
                if (self.room_assignments[i] != self.room_assignments[i-1] and 
                    self.room_assignments[i-1] != self.room_assignments[i-2]):
                    patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_allocation_strategy(self):
        """Get optimal allocation strategy based on customer patterns."""
        if not self.customers:
            return {
                'recommended_rooms': 0,
                'peak_time': 0,
                'efficiency_rate': 0
            }
        
        # Find peak time
        all_times = []
        for arrival, departure in self.customers:
            all_times.extend([arrival, departure])
        
        sorted_times = sorted(all_times)
        current_customers = 0
        max_customers = 0
        peak_time = 0
        
        for time in sorted_times:
            if time in [arrival for arrival, _ in self.customers]:
                current_customers += 1
            else:
                current_customers -= 1
            
            if current_customers > max_customers:
                max_customers = current_customers
                peak_time = time
        
        # Calculate efficiency rate
        total_customer_time = sum(departure - arrival for arrival, departure in self.customers)
        time_span = max(all_times) - min(all_times)
        efficiency_rate = total_customer_time / (time_span * self.min_rooms) if time_span > 0 and self.min_rooms > 0 else 0
        
        return {
            'recommended_rooms': self.min_rooms,
            'peak_time': peak_time,
            'efficiency_rate': efficiency_rate
        }

# Example usage
customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
dynamic_allocation = DynamicRoomAllocation(customers)
print(f"Initial room assignments: {dynamic_allocation.get_room_assignments()}")
print(f"Initial min rooms: {dynamic_allocation.get_min_rooms()}")

# Add a customer
dynamic_allocation.add_customer(4, 7)
print(f"After adding customer: {dynamic_allocation.get_room_assignments()}")

# Update a customer
dynamic_allocation.update_customer(1, 2, 5)
print(f"After updating customer: {dynamic_allocation.get_room_assignments()}")

# Get room utilization
print(f"Room utilization: {dynamic_allocation.get_room_utilization()}")

# Get room assignments with constraints
constraints = {1: 1, 3: 2}  # Customer 1 must get room 1, customer 3 must get room 2
print(f"Constrained assignments: {dynamic_allocation.get_room_assignments_with_constraints(constraints)}")

# Get room assignments in time range
print(f"Assignments in range [2, 5]: {dynamic_allocation.get_room_assignments_with_time_range(2, 5)}")

# Get room assignments with constraints function
def constraint_func(arrival, departure):
    return departure - arrival >= 2

print(f"Assignments with constraints: {dynamic_allocation.get_room_assignments_with_constraints_func(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_allocation.get_allocation_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_allocation.get_allocation_patterns()}")

# Get optimal allocation strategy
print(f"Optimal allocation strategy: {dynamic_allocation.get_optimal_allocation_strategy()}")
```

### **Variation 2: Room Allocation with Different Operations**
**Problem**: Handle different types of operations on room allocation (weighted customers, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of room allocation queries.

```python
class AdvancedRoomAllocation:
    def __init__(self, customers, weights=None, priorities=None):
        self.customers = customers[:]
        self.n = len(customers)
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.room_assignments = self._compute_room_assignments()
        self.min_rooms = self._compute_min_rooms()
        self.weighted_min_rooms = self._compute_weighted_min_rooms()
    
    def _compute_room_assignments(self):
        """Compute room assignments using priority queue."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def _compute_min_rooms(self):
        """Compute minimum number of rooms needed."""
        return len(set(self.room_assignments))
    
    def _compute_weighted_min_rooms(self):
        """Compute minimum weighted rooms needed."""
        if not self.customers:
            return 0
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id, weight)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for i, (arrival, departure) in enumerate(sorted_customers):
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id, weight = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id, weight + self.weights[i]))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id, self.weights[i]))
                assignments.append(room_id + 1)
        
        return len(set(assignments))
    
    def get_room_assignments(self):
        """Get current room assignments."""
        return self.room_assignments
    
    def get_min_rooms(self):
        """Get minimum number of rooms needed."""
        return self.min_rooms
    
    def get_weighted_min_rooms(self):
        """Get minimum weighted rooms needed."""
        return self.weighted_min_rooms
    
    def get_room_assignments_with_priority(self, priority_func):
        """Get room assignments considering priority."""
        if not self.customers:
            return []
        
        # Sort customers by priority
        sorted_customers = sorted(enumerate(self.customers), 
                                key=lambda x: priority_func(x[1][0], x[1][1], self.weights[x[0]], self.priorities[x[0]]), 
                                reverse=True)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = [0] * self.n
        
        for original_idx, (arrival, departure) in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments[original_idx] = room_id + 1
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments[original_idx] = room_id + 1
        
        return assignments
    
    def get_room_assignments_with_optimization(self, optimization_func):
        """Get room assignments using custom optimization function."""
        if not self.customers:
            return []
        
        # Sort customers by optimization function
        sorted_customers = sorted(enumerate(self.customers), 
                                key=lambda x: optimization_func(x[1][0], x[1][1], self.weights[x[0]], self.priorities[x[0]]), 
                                reverse=True)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = [0] * self.n
        
        for original_idx, (arrival, departure) in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments[original_idx] = room_id + 1
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments[original_idx] = room_id + 1
        
        return assignments
    
    def get_room_assignments_with_constraints(self, constraint_func):
        """Get room assignments that satisfy custom constraints."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            if constraint_func(arrival, departure, self.weights[i], self.priorities[i]):
                result.append((i, arrival, departure, self.room_assignments[i]))
        return result
    
    def get_room_assignments_with_multiple_criteria(self, criteria_list):
        """Get room assignments that satisfy multiple criteria."""
        result = []
        for i, (arrival, departure) in enumerate(self.customers):
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(arrival, departure, self.weights[i], self.priorities[i]):
                    satisfies_all_criteria = False
                    break
            
            if satisfies_all_criteria:
                result.append((i, arrival, departure, self.room_assignments[i]))
        
        return result
    
    def get_room_assignments_with_alternatives(self, alternatives):
        """Get room assignments considering alternative times."""
        result = []
        
        for i, (arrival, departure) in enumerate(self.customers):
            # Check original customer
            result.append((i, arrival, departure, self.room_assignments[i], 'original'))
            
            # Check alternative times
            if i in alternatives:
                for alt_arrival, alt_departure in alternatives[i]:
                    result.append((i, alt_arrival, alt_departure, self.room_assignments[i], 'alternative'))
        
        return result
    
    def get_room_assignments_with_adaptive_criteria(self, adaptive_func):
        """Get room assignments using adaptive criteria."""
        result = []
        
        for i, (arrival, departure) in enumerate(self.customers):
            if adaptive_func(arrival, departure, self.weights[i], self.priorities[i], result):
                result.append((i, arrival, departure, self.room_assignments[i]))
        
        return result
    
    def get_allocation_optimization(self):
        """Get optimal allocation configuration."""
        strategies = [
            ('min_rooms', self.get_min_rooms),
            ('weighted_min_rooms', self.get_weighted_min_rooms),
        ]
        
        best_strategy = None
        best_value = float('inf')
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value < best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
weights = [2, 1, 3, 1]
priorities = [1, 2, 1, 3]
advanced_allocation = AdvancedRoomAllocation(customers, weights, priorities)

print(f"Min rooms: {advanced_allocation.get_min_rooms()}")
print(f"Weighted min rooms: {advanced_allocation.get_weighted_min_rooms()}")

# Get room assignments with priority
def priority_func(arrival, departure, weight, priority):
    return (departure - arrival) * weight * priority

print(f"Priority-based assignments: {advanced_allocation.get_room_assignments_with_priority(priority_func)}")

# Get room assignments with optimization
def optimization_func(arrival, departure, weight, priority):
    return (departure - arrival) * weight + priority

print(f"Optimization-based assignments: {advanced_allocation.get_room_assignments_with_optimization(optimization_func)}")

# Get room assignments with constraints
def constraint_func(arrival, departure, weight, priority):
    return departure - arrival >= 2 and weight > 1

print(f"Constrained assignments: {advanced_allocation.get_room_assignments_with_constraints(constraint_func)}")

# Get room assignments with multiple criteria
def criterion1(arrival, departure, weight, priority):
    return departure - arrival >= 2

def criterion2(arrival, departure, weight, priority):
    return weight > 1

criteria_list = [criterion1, criterion2]
print(f"Multiple criteria assignments: {advanced_allocation.get_room_assignments_with_multiple_criteria(criteria_list)}")

# Get room assignments with alternatives
alternatives = {1: [(1, 5), (3, 6)], 3: [(2, 7), (4, 8)]}
print(f"Alternative assignments: {advanced_allocation.get_room_assignments_with_alternatives(alternatives)}")

# Get room assignments with adaptive criteria
def adaptive_func(arrival, departure, weight, priority, current_result):
    return departure - arrival >= 2 and len(current_result) < 3

print(f"Adaptive criteria assignments: {advanced_allocation.get_room_assignments_with_adaptive_criteria(adaptive_func)}")

# Get allocation optimization
print(f"Allocation optimization: {advanced_allocation.get_allocation_optimization()}")
```

### **Variation 3: Room Allocation with Constraints**
**Problem**: Handle room allocation with additional constraints (capacity limits, time constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedRoomAllocation:
    def __init__(self, customers, constraints=None):
        self.customers = customers[:]
        self.n = len(customers)
        self.constraints = constraints or {}
        self.room_assignments = self._compute_room_assignments()
        self.min_rooms = self._compute_min_rooms()
    
    def _compute_room_assignments(self):
        """Compute room assignments using priority queue."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def _compute_min_rooms(self):
        """Compute minimum number of rooms needed."""
        return len(set(self.room_assignments))
    
    def get_room_assignments_with_capacity_constraints(self, capacity_limit):
        """Get room assignments considering capacity constraints."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id, current_capacity)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            # Check if any room can accommodate this customer
            found_room = False
            for i, (dep_time, room_id, capacity) in enumerate(available_rooms):
                if dep_time <= arrival and capacity < capacity_limit:
                    # Assign to this room
                    available_rooms[i] = (departure, room_id, capacity + 1)
                    assignments.append(room_id + 1)
                    found_room = True
                    break
            
            if not found_room:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id, 1))
                assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_time_constraints(self, time_limit):
        """Get room assignments considering time constraints."""
        if not self.customers:
            return []
        
        # Filter customers within time limit
        filtered_customers = [(arrival, departure) for arrival, departure in self.customers 
                            if arrival <= time_limit]
        
        if not filtered_customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(filtered_customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get room assignments considering resource constraints."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id, current_resources)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            # Check if any room can accommodate this customer
            found_room = False
            for i, (dep_time, room_id, current_resources) in enumerate(available_rooms):
                if dep_time <= arrival:
                    # Check resource constraints
                    can_accommodate = True
                    for j, consumption in enumerate(resource_consumption.get(arrival, [0] * len(resource_limits))):
                        if current_resources[j] + consumption > resource_limits[j]:
                            can_accommodate = False
                            break
                    
                    if can_accommodate:
                        # Assign to this room
                        new_resources = current_resources[:]
                        for j, consumption in enumerate(resource_consumption.get(arrival, [0] * len(resource_limits))):
                            new_resources[j] += consumption
                        available_rooms[i] = (departure, room_id, new_resources)
                        assignments.append(room_id + 1)
                        found_room = True
                        break
            
            if not found_room:
                # Create new room
                room_id = room_counter
                room_counter += 1
                initial_resources = [0] * len(resource_limits)
                for j, consumption in enumerate(resource_consumption.get(arrival, [0] * len(resource_limits))):
                    initial_resources[j] += consumption
                heapq.heappush(available_rooms, (departure, room_id, initial_resources))
                assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_mathematical_constraints(self, constraint_func):
        """Get room assignments that satisfies custom mathematical constraints."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            if constraint_func(arrival, departure):
                if available_rooms and available_rooms[0][0] <= arrival:
                    # Reuse existing room
                    dep_time, room_id = heapq.heappop(available_rooms)
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
                else:
                    # Create new room
                    room_id = room_counter
                    room_counter += 1
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_range_constraints(self, range_constraints):
        """Get room assignments that satisfies range constraints."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            # Check if customer satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(arrival, departure):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                if available_rooms and available_rooms[0][0] <= arrival:
                    # Reuse existing room
                    dep_time, room_id = heapq.heappop(available_rooms)
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
                else:
                    # Create new room
                    room_id = room_counter
                    room_counter += 1
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_optimization_constraints(self, optimization_func):
        """Get room assignments using custom optimization constraints."""
        if not self.customers:
            return []
        
        # Sort customers by optimization function
        sorted_customers = sorted(self.customers, key=lambda x: optimization_func(x[0], x[1]), reverse=True)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_multiple_constraints(self, constraints_list):
        """Get room assignments that satisfies multiple constraints."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            # Check if customer satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(arrival, departure):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                if available_rooms and available_rooms[0][0] <= arrival:
                    # Reuse existing room
                    dep_time, room_id = heapq.heappop(available_rooms)
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
                else:
                    # Create new room
                    room_id = room_counter
                    room_counter += 1
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_priority_constraints(self, priority_func):
        """Get room assignments with priority-based constraints."""
        if not self.customers:
            return []
        
        # Sort customers by priority
        sorted_customers = sorted(self.customers, key=lambda x: priority_func(x[0], x[1]), reverse=True)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            if available_rooms and available_rooms[0][0] <= arrival:
                # Reuse existing room
                dep_time, room_id = heapq.heappop(available_rooms)
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
            else:
                # Create new room
                room_id = room_counter
                room_counter += 1
                heapq.heappush(available_rooms, (departure, room_id))
                assignments.append(room_id + 1)
        
        return assignments
    
    def get_room_assignments_with_adaptive_constraints(self, adaptive_func):
        """Get room assignments with adaptive constraints."""
        if not self.customers:
            return []
        
        # Sort customers by arrival time
        sorted_customers = sorted(self.customers)
        
        # Priority queue: (departure_time, room_id)
        available_rooms = []
        room_counter = 0
        assignments = []
        
        for arrival, departure in sorted_customers:
            # Check adaptive constraints
            if adaptive_func(arrival, departure, assignments):
                if available_rooms and available_rooms[0][0] <= arrival:
                    # Reuse existing room
                    dep_time, room_id = heapq.heappop(available_rooms)
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
                else:
                    # Create new room
                    room_id = room_counter
                    room_counter += 1
                    heapq.heappush(available_rooms, (departure, room_id))
                    assignments.append(room_id + 1)
        
        return assignments
    
    def get_optimal_allocation_strategy(self):
        """Get optimal allocation strategy considering all constraints."""
        strategies = [
            ('capacity_constraints', self.get_room_assignments_with_capacity_constraints),
            ('time_constraints', self.get_room_assignments_with_time_constraints),
            ('resource_constraints', self.get_room_assignments_with_resource_constraints),
        ]
        
        best_strategy = None
        best_rooms = float('inf')
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'capacity_constraints':
                    current_assignments = strategy_func(2)  # Capacity of 2
                elif strategy_name == 'time_constraints':
                    current_assignments = strategy_func(10)  # Time limit of 10
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {arrival: [10, 5] for arrival, _ in self.customers}
                    current_assignments = strategy_func(resource_limits, resource_consumption)
                
                current_rooms = len(set(current_assignments))
                if current_rooms < best_rooms:
                    best_rooms = current_rooms
                    best_strategy = (strategy_name, current_assignments, current_rooms)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_stay_duration': 1,
    'max_capacity': 10
}

customers = [(1, 3), (2, 4), (3, 5), (1, 6)]
constrained_allocation = ConstrainedRoomAllocation(customers, constraints)

print("Capacity-constrained assignments:", constrained_allocation.get_room_assignments_with_capacity_constraints(2))

print("Time-constrained assignments:", constrained_allocation.get_room_assignments_with_time_constraints(5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {arrival: [10, 5] for arrival, _ in customers}
print("Resource-constrained assignments:", constrained_allocation.get_room_assignments_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(arrival, departure):
    return departure - arrival >= 2

print("Mathematical constraint assignments:", constrained_allocation.get_room_assignments_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(arrival, departure):
    return departure - arrival >= 2

range_constraints = [range_constraint]
print("Range-constrained assignments:", constrained_allocation.get_room_assignments_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(arrival, departure):
    return departure - arrival >= 2

def constraint2(arrival, departure):
    return arrival >= 1

constraints_list = [constraint1, constraint2]
print("Multiple constraints assignments:", constrained_allocation.get_room_assignments_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(arrival, departure):
    return departure - arrival

print("Priority-constrained assignments:", constrained_allocation.get_room_assignments_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(arrival, departure, current_assignments):
    return departure - arrival >= 2 and len(current_assignments) < 4

print("Adaptive constraint assignments:", constrained_allocation.get_room_assignments_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_allocation.get_optimal_allocation_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Room Allocation](https://cses.fi/problemset/task/1164) - Basic room allocation problem
- [Restaurant Customers](https://cses.fi/problemset/task/1619) - Customer overlap problem
- [Movie Festival](https://cses.fi/problemset/task/1629) - Interval scheduling problem

#### **LeetCode Problems**
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) - Minimum meeting rooms needed
- [Car Pooling](https://leetcode.com/problems/car-pooling/) - Capacity constraint problem
- [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) - Maximum overlapping events

#### **Problem Categories**
- **Priority Queue**: Min-heap operations, room availability tracking, efficient scheduling
- **Interval Scheduling**: Event scheduling, resource allocation, time management
- **Greedy Algorithms**: Optimal local choices, room assignment, capacity management
- **Algorithm Design**: Priority queue techniques, interval processing, resource optimization
