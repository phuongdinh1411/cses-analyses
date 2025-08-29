---
layout: simple
title: "Room Allocation"
permalink: /problem_soulutions/sorting_and_searching/room_allocation_analysis
---

# Room Allocation

## Problem Description

**Problem**: Given n customers, each with arrival and departure times, assign rooms to customers so that no two customers share a room at the same time. Find the minimum number of rooms needed and assign rooms to each customer.

**Input**: 
- First line: n (number of customers)
- Next n lines: a b (arrival and departure time of each customer)

**Output**: Minimum number of rooms needed and room assignment for each customer.

**Example**:
```
Input:
3
1 3
2 4
3 5

Output:
2
1 2 1

Explanation: 
Customer 1: arrives at 1, departs at 3 → gets room 1
Customer 2: arrives at 2, departs at 4 → gets room 2 (room 1 still occupied)
Customer 3: arrives at 3, departs at 5 → gets room 1 (room 1 is now free)
Minimum rooms needed: 2
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Assign rooms to customers based on their stay times
- No two customers can share a room at the same time
- Find minimum number of rooms needed
- Assign specific room numbers to each customer

**Key Observations:**
- Sort customers by arrival time
- Use priority queue to track room availability
- Greedy approach: assign earliest available room
- Track room end times efficiently

### Step 2: Brute Force Approach
**Idea**: Sort customers by arrival time and assign rooms greedily.

```python
def room_allocation_brute_force(n, customers):
    # Sort customers by arrival time
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    rooms = []  # List of (end_time, room_id) for occupied rooms
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        # Find an available room
        assigned = False
        for i, (end_time, room_id) in enumerate(rooms):
            if end_time < arrival:
                rooms[i] = (departure, room_id)
                assignments[customer_id] = room_id
                assigned = True
                break
        
        if not assigned:
            # Need a new room
            new_room_id = len(rooms) + 1
            rooms.append((departure, new_room_id))
            assignments[customer_id] = new_room_id
    
    return len(rooms), assignments
```

**Why this works:**
- Checks all rooms for availability
- Simple to understand and implement
- Guarantees correct answer
- O(n²) time complexity

### Step 3: Priority Queue Optimization
**Idea**: Use a priority queue to efficiently find available rooms.

```python
import heapq

def room_allocation_priority_queue(n, customers):
    # Sort customers by arrival time
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    # Priority queue of (end_time, room_id) for occupied rooms
    occupied_rooms = []
    available_rooms = []  # Stack of available room IDs
    next_room_id = 1
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        # Free up rooms that are no longer occupied
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_id = heapq.heappop(occupied_rooms)
            available_rooms.append(room_id)
        
        # Assign a room
        if available_rooms:
            room_id = available_rooms.pop()
        else:
            room_id = next_room_id
            next_room_id += 1
        
        # Add room to occupied rooms
        heapq.heappush(occupied_rooms, (departure, room_id))
        assignments[customer_id] = room_id
    
    return next_room_id - 1, assignments
```

**Why this is better:**
- O(n log n) time complexity
- Uses priority queue for efficiency
- Maintains room availability
- Much more efficient

### Step 4: Complete Solution
**Putting it all together:**

```python
import heapq

def solve_room_allocation():
    n = int(input())
    customers = []
    
    for i in range(n):
        a, b = map(int, input().split())
        customers.append((a, b, i))
    
    # Sort customers by arrival time
    customers.sort()
    
    # Priority queue of (end_time, room_id) for occupied rooms
    occupied_rooms = []
    available_rooms = []  # Stack of available room IDs
    next_room_id = 1
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        # Free up rooms that are no longer occupied
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_id = heapq.heappop(occupied_rooms)
            available_rooms.append(room_id)
        
        # Assign a room
        if available_rooms:
            room_id = available_rooms.pop()
        else:
            room_id = next_room_id
            next_room_id += 1
        
        # Add room to occupied rooms
        heapq.heappush(occupied_rooms, (departure, room_id))
        assignments[customer_id] = room_id
    
    # Print results
    print(next_room_id - 1)
    print(*assignments)

# Main execution
if __name__ == "__main__":
    solve_room_allocation()
```

**Why this works:**
- Optimal priority queue approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
import heapq

def test_solution():
    test_cases = [
        (3, [(1, 3), (2, 4), (3, 5)], (2, [1, 2, 1])),
        (2, [(1, 2), (2, 3)], (1, [1, 1])),
        (4, [(1, 3), (2, 4), (3, 5), (1, 2)], (2, [1, 2, 1, 1])),
        (1, [(1, 1)], (1, [1])),
    ]
    
    for n, customers, expected in test_cases:
        result = solve_test(n, customers)
        print(f"n={n}, customers={customers}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, customers):
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    occupied_rooms = []
    available_rooms = []
    next_room_id = 1
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_id = heapq.heappop(occupied_rooms)
            available_rooms.append(room_id)
        
        if available_rooms:
            room_id = available_rooms.pop()
        else:
            room_id = next_room_id
            next_room_id += 1
        
        heapq.heappush(occupied_rooms, (departure, room_id))
        assignments[customer_id] = room_id
    
    return next_room_id - 1, assignments

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting + priority queue operations
- **Space**: O(n) - storing customers and room assignments

### Why This Solution Works
- **Sorting**: Process customers in arrival order
- **Priority Queue**: Efficiently track room availability
- **Greedy Assignment**: Always assign earliest available room
- **Optimal Approach**: Minimum rooms needed

## 🎯 Key Insights

### 1. **Greedy Strategy**
- Process customers in arrival order
- Always assign earliest available room
- Ensures minimum number of rooms
- Key insight for optimization

### 2. **Priority Queue Usage**
- Track room end times efficiently
- Find earliest available room in O(log n)
- Maintain room availability
- Crucial for efficiency

### 3. **Room Reuse**
- Reuse rooms when customers depart
- Track available room IDs
- Minimize total rooms needed
- Important for optimal solution

## 🎯 Problem Variations

### Variation 1: Weighted Room Allocation
**Problem**: Each customer has a priority/weight. Assign rooms to maximize total priority.

```python
import heapq

def weighted_room_allocation(n, customers):
    # customers[i] = (arrival, departure, priority, customer_id)
    customers = [(customers[i][0], customers[i][1], customers[i][2], i) for i in range(n)]
    customers.sort()  # Sort by arrival time
    
    occupied_rooms = []
    available_rooms = []
    next_room_id = 1
    assignments = [0] * n
    total_priority = 0
    
    for arrival, departure, priority, customer_id in customers:
        # Free up rooms
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_id = heapq.heappop(occupied_rooms)
            available_rooms.append(room_id)
        
        # Assign room
        if available_rooms:
            room_id = available_rooms.pop()
        else:
            room_id = next_room_id
            next_room_id += 1
        
        heapq.heappush(occupied_rooms, (departure, room_id))
        assignments[customer_id] = room_id
        total_priority += priority
    
    return next_room_id - 1, assignments, total_priority
```

### Variation 2: Room Capacity Constraints
**Problem**: Each room has a capacity limit. Assign customers to rooms respecting capacity.

```python
import heapq

def capacity_constrained_allocation(n, customers, room_capacities):
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    # Track room occupancy: (end_time, room_id, current_capacity)
    occupied_rooms = []
    available_rooms = []  # (room_id, max_capacity, current_capacity)
    next_room_id = 1
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        # Free up rooms
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            end_time, room_id, capacity = heapq.heappop(occupied_rooms)
            # Find room capacity
            max_capacity = room_capacities[room_id - 1]
            available_rooms.append((room_id, max_capacity, 0))
        
        # Find available room with capacity
        assigned = False
        for i, (room_id, max_cap, curr_cap) in enumerate(available_rooms):
            if curr_cap < max_cap:
                available_rooms[i] = (room_id, max_cap, curr_cap + 1)
                assignments[customer_id] = room_id
                heapq.heappush(occupied_rooms, (departure, room_id, curr_cap + 1))
                assigned = True
                break
        
        if not assigned:
            # Need new room
            room_id = next_room_id
            next_room_id += 1
            assignments[customer_id] = room_id
            heapq.heappush(occupied_rooms, (departure, room_id, 1))
    
    return next_room_id - 1, assignments
```

### Variation 3: Dynamic Room Allocation
**Problem**: Support adding/removing customers dynamically.

```python
import heapq

class DynamicRoomAllocator:
    def __init__(self):
        self.customers = []
        self.occupied_rooms = []
        self.available_rooms = []
        self.next_room_id = 1
        self.assignments = {}
    
    def add_customer(self, customer_id, arrival, departure):
        # Add customer and sort
        self.customers.append((arrival, departure, customer_id))
        self.customers.sort()
        
        # Reallocate all customers
        return self._allocate_rooms()
    
    def remove_customer(self, customer_id):
        # Remove customer
        self.customers = [(a, d, cid) for a, d, cid in self.customers if cid != customer_id]
        
        # Reallocate remaining customers
        return self._allocate_rooms()
    
    def _allocate_rooms(self):
        self.occupied_rooms = []
        self.available_rooms = []
        self.next_room_id = 1
        self.assignments = {}
        
        for arrival, departure, customer_id in self.customers:
            # Free up rooms
            while self.occupied_rooms and self.occupied_rooms[0][0] < arrival:
                _, room_id = heapq.heappop(self.occupied_rooms)
                self.available_rooms.append(room_id)
            
            # Assign room
            if self.available_rooms:
                room_id = self.available_rooms.pop()
            else:
                room_id = self.next_room_id
                self.next_room_id += 1
            
            heapq.heappush(self.occupied_rooms, (departure, room_id))
            self.assignments[customer_id] = room_id
        
        return self.next_room_id - 1, self.assignments
```

### Variation 4: Room Preference Allocation
**Problem**: Each customer has room preferences. Assign rooms respecting preferences when possible.

```python
import heapq

def preference_room_allocation(n, customers, preferences):
    # customers[i] = (arrival, departure, customer_id)
    # preferences[i] = list of preferred room IDs for customer i
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    occupied_rooms = []
    available_rooms = []
    next_room_id = 1
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        # Free up rooms
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_id = heapq.heappop(occupied_rooms)
            available_rooms.append(room_id)
        
        # Try to assign preferred room
        assigned = False
        for pref_room in preferences[customer_id]:
            if pref_room in available_rooms:
                available_rooms.remove(pref_room)
                assignments[customer_id] = pref_room
                heapq.heappush(occupied_rooms, (departure, pref_room))
                assigned = True
                break
        
        if not assigned:
            # Assign any available room or new room
            if available_rooms:
                room_id = available_rooms.pop()
            else:
                room_id = next_room_id
                next_room_id += 1
            
            assignments[customer_id] = room_id
            heapq.heappush(occupied_rooms, (departure, room_id))
    
    return next_room_id - 1, assignments
```

### Variation 5: Multi-Resource Allocation
**Problem**: Each customer needs multiple resources (room, equipment, etc.). Allocate all resources efficiently.

```python
import heapq

def multi_resource_allocation(n, customers, resources_needed):
    # customers[i] = (arrival, departure, customer_id)
    # resources_needed[i] = list of required resource types
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    # Track each resource type separately
    resource_allocators = {}
    for resource_type in set().union(*resources_needed):
        resource_allocators[resource_type] = {
            'occupied': [],
            'available': [],
            'next_id': 1
        }
    
    assignments = {resource_type: [0] * n for resource_type in set().union(*resources_needed)}
    
    for arrival, departure, customer_id in customers:
        # Free up resources
        for resource_type in resource_allocators:
            allocator = resource_allocators[resource_type]
            while allocator['occupied'] and allocator['occupied'][0][0] < arrival:
                _, resource_id = heapq.heappop(allocator['occupied'])
                allocator['available'].append(resource_id)
        
        # Assign required resources
        for resource_type in resources_needed[customer_id]:
            allocator = resource_allocators[resource_type]
            
            if allocator['available']:
                resource_id = allocator['available'].pop()
            else:
                resource_id = allocator['next_id']
                allocator['next_id'] += 1
            
            heapq.heappush(allocator['occupied'], (departure, resource_id))
            assignments[resource_type][customer_id] = resource_id
    
    return assignments
```

## 🔗 Related Problems

- **[Movie Festival](/cses-analyses/problem_soulutions/sorting_and_searching/cses_movie_festival_analysis)**: Interval scheduling
- **[Nested Ranges](/cses-analyses/problem_soulutions/sorting_and_searching/nested_ranges_count_analysis)**: Range problems
- **[Tasks and Deadlines](/cses-analyses/problem_soulutions/sorting_and_searching/tasks_and_deadlines_analysis)**: Scheduling problems

## 📚 Learning Points

1. **Greedy Strategy**: Process in arrival order for optimal allocation
2. **Priority Queue**: Efficiently track resource availability
3. **Resource Reuse**: Minimize total resources needed
4. **Scheduling Problems**: Common pattern in competitive programming

---

**This is a great introduction to resource allocation and scheduling problems!** 🎯 