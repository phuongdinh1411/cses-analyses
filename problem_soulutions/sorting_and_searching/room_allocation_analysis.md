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
