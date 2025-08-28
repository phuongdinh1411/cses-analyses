---
layout: simple
title: "Room Allocation
permalink: /problem_soulutions/sorting_and_searching/room_allocation_analysis/"
---


# Room Allocation

## Problem Statement
Given n customers, each with arrival and departure times, assign rooms to customers so that no two customers share a room at the same time. Find the minimum number of rooms needed and assign rooms to each customer.

### Input
The first input line has an integer n: the number of customers.
Then there are n lines. Each line has two integers a and b: the arrival and departure time of a customer.

### Output
Print the minimum number of rooms needed and the room assignment for each customer.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ bi ≤ 10^9

### Example
```
Input:
3
1 3
2 4
3 5

Output:
2
1 2 1
```

## Solution Progression

### Approach 1: Greedy with Sorting - O(n²)
**Description**: Sort customers by arrival time and assign rooms greedily.

```python
def room_allocation_naive(n, customers):
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

**Why this is inefficient**: For each customer, we check all rooms, leading to O(n²) time complexity.

### Improvement 1: Priority Queue - O(n log n)
**Description**: Use a priority queue to efficiently find available rooms.

```python
import heapq

def room_allocation_optimized(n, customers):
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
        
        assignments[customer_id] = room_id
        heapq.heappush(occupied_rooms, (departure, room_id))
    
    return next_room_id - 1, assignments
```

**Why this improvement works**: We use a priority queue to efficiently track occupied rooms and a stack to reuse room IDs, reducing the time complexity to O(n log n).

## Final Optimal Solution

```python
import heapq

n = int(input())
customers = []
for _ in range(n):
    a, b = map(int, input().split())
    customers.append((a, b))

def allocate_rooms(n, customers):
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
        
        assignments[customer_id] = room_id
        heapq.heappush(occupied_rooms, (departure, room_id))
    
    return next_room_id - 1, assignments

num_rooms, assignments = allocate_rooms(n, customers)
print(num_rooms)
print(*assignments)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Greedy with Sorting | O(n²) | O(n) | Check all rooms for each customer |
| Priority Queue | O(n log n) | O(n) | Use priority queue for efficient room management |

## Key Insights for Other Problems

### 1. **Room Allocation Problems**
**Principle**: Use priority queue to efficiently manage room availability.
**Applicable to**: Allocation problems, scheduling problems, resource management

### 2. **Interval Scheduling**
**Principle**: Sort by start time and use greedy approach with priority queue.
**Applicable to**: Scheduling problems, interval problems, resource allocation

### 3. **Resource Reuse**
**Principle**: Reuse available resources (room IDs) to minimize total resources needed.
**Applicable to**: Resource management, optimization problems, allocation problems

## Notable Techniques

### 1. **Priority Queue Management**
```python
def manage_occupied_rooms(occupied_rooms, current_time):
    # Free up rooms that are no longer occupied
    while occupied_rooms and occupied_rooms[0][0] < current_time:
        _, room_id = heapq.heappop(occupied_rooms)
        yield room_id
```

### 2. **Room Assignment**
```python
def assign_room(available_rooms, next_room_id):
    if available_rooms:
        return available_rooms.pop()
    else:
        room_id = next_room_id
        next_room_id += 1
        return room_id
```

### 3. **Customer Processing**
```python
def process_customers(customers):
    customers.sort()  # Sort by arrival time
    occupied_rooms = []
    available_rooms = []
    next_room_id = 1
    assignments = []
    
    for arrival, departure, customer_id in customers:
        # Free up rooms
        for room_id in manage_occupied_rooms(occupied_rooms, arrival):
            available_rooms.append(room_id)
        
        # Assign room
        room_id = assign_room(available_rooms, next_room_id)
        assignments.append(room_id)
        heapq.heappush(occupied_rooms, (departure, room_id))
    
    return assignments
```

## Problem-Solving Framework

1. **Identify problem type**: This is a room allocation problem with interval scheduling
2. **Choose approach**: Use priority queue for efficient room management
3. **Sort customers**: Sort by arrival time for greedy processing
4. **Initialize data structures**: Priority queue for occupied rooms, stack for available rooms
5. **Process customers**: For each customer, free up rooms and assign available room
6. **Track assignments**: Maintain room assignments for each customer
7. **Return result**: Output minimum rooms needed and room assignments

---

*This analysis shows how to efficiently allocate rooms to customers using priority queue and greedy approach.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Room Allocation with Room Types**
**Problem**: Different room types with different costs. Minimize total cost.
```python
def room_allocation_with_types(n, customers, room_types):
    # room_types: [(capacity, cost), ...]
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    occupied_rooms = []  # (end_time, room_type_id, room_id)
    available_rooms = {i: [] for i in range(len(room_types))}  # Available rooms by type
    next_room_ids = {i: 1 for i in range(len(room_types))}
    assignments = [0] * n
    total_cost = 0
    
    for arrival, departure, customer_id in customers:
        # Free up rooms
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_type, room_id = heapq.heappop(occupied_rooms)
            available_rooms[room_type].append(room_id)
        
        # Find cheapest available room
        best_room_type = None"
        best_cost = float('inf')
        
        for room_type, (capacity, cost) in enumerate(room_types):
            if available_rooms[room_type] and cost < best_cost:
                best_room_type = room_type
                best_cost = cost
        
        if best_room_type is not None:
            room_id = available_rooms[best_room_type].pop()
        else:
            # Create new room of cheapest type
            best_room_type = min(range(len(room_types)), key=lambda i: room_types[i][1])
            room_id = next_room_ids[best_room_type]
            next_room_ids[best_room_type] += 1
        
        assignments[customer_id] = (best_room_type, room_id)
        total_cost += room_types[best_room_type][1]
        heapq.heappush(occupied_rooms, (departure, best_room_type, room_id))
    
    return total_cost, assignments
```

#### **Variation 2: Room Allocation with Capacity Constraints**
**Problem**: Each room has a capacity. Assign customers to rooms optimally.
```python
def room_allocation_with_capacity(n, customers, room_capacity):
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    occupied_rooms = []  # (end_time, room_id, current_capacity)
    available_rooms = []  # Stack of available room IDs
    next_room_id = 1
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        # Free up rooms
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_id, _ = heapq.heappop(occupied_rooms)
            available_rooms.append(room_id)
        
        # Find room with available capacity
        assigned = False
        for i, (end_time, room_id, capacity) in enumerate(occupied_rooms):
            if capacity < room_capacity:
                occupied_rooms[i] = (departure, room_id, capacity + 1)
                assignments[customer_id] = room_id
                assigned = True
                break
        
        if not assigned:
            if available_rooms:
                room_id = available_rooms.pop()
            else:
                room_id = next_room_id
                next_room_id += 1
            
            assignments[customer_id] = room_id
            heapq.heappush(occupied_rooms, (departure, room_id, 1))
    
    return next_room_id - 1, assignments
```

#### **Variation 3: Room Allocation with Priority**
**Problem**: Some customers have higher priority and must be assigned first.
```python
def room_allocation_with_priority(n, customers, priorities):
    # Sort by priority (higher first), then by arrival time
    customers = [(customers[i][0], customers[i][1], priorities[i], i) for i in range(n)]
    customers.sort(key=lambda x: (-x[2], x[0]))  # Sort by priority desc, then arrival
    
    occupied_rooms = []
    available_rooms = []
    next_room_id = 1
    assignments = [0] * n
    
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
        
        assignments[customer_id] = room_id
        heapq.heappush(occupied_rooms, (departure, room_id))
    
    return next_room_id - 1, assignments
```

#### **Variation 4: Room Allocation with Dynamic Updates**
**Problem**: Support adding and removing customers dynamically.
```python
class DynamicRoomAllocation:
    def __init__(self):
        self.customers = []
        self.occupied_rooms = []
        self.available_rooms = []
        self.next_room_id = 1
        self.assignments = {}
    
    def add_customer(self, arrival, departure, customer_id):
        self.customers.append((arrival, departure, customer_id))
        
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
        
        self.assignments[customer_id] = room_id
        heapq.heappush(self.occupied_rooms, (departure, room_id))
        
        return room_id
    
    def remove_customer(self, customer_id):
        if customer_id in self.assignments:
            room_id = self.assignments[customer_id]
            # Mark room as available
            self.available_rooms.append(room_id)
            del self.assignments[customer_id]
            
            # Remove from customers list
            self.customers = [(a, d, cid) for a, d, cid in self.customers if cid != customer_id]
        
        return self.get_room_count()
    
    def get_room_count(self):
        return self.next_room_id - 1
```

#### **Variation 5: Room Allocation with Constraints**
**Problem**: Some customers have specific room requirements or constraints.
```python
def room_allocation_with_constraints(n, customers, constraints):
    # constraints[i] = list of allowed room types for customer i
    customers = [(customers[i][0], customers[i][1], constraints[i], i) for i in range(n)]
    customers.sort()
    
    occupied_rooms = []  # (end_time, room_type, room_id)
    available_rooms = {0: []}  # Available rooms by type
    next_room_ids = {0: 1}
    assignments = [0] * n
    
    for arrival, departure, allowed_types, customer_id in customers:
        # Free up rooms
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            _, room_type, room_id = heapq.heappop(occupied_rooms)
            if room_type not in available_rooms:
                available_rooms[room_type] = []
            available_rooms[room_type].append(room_id)
        
        # Find available room of allowed type
        assigned = False
        for room_type in allowed_types:
            if room_type in available_rooms and available_rooms[room_type]:
                room_id = available_rooms[room_type].pop()
                assignments[customer_id] = (room_type, room_id)
                heapq.heappush(occupied_rooms, (departure, room_type, room_id))
                assigned = True
                break
        
        if not assigned:
            # Create new room of first allowed type
            room_type = allowed_types[0]
            if room_type not in next_room_ids:
                next_room_ids[room_type] = 1
            room_id = next_room_ids[room_type]
            next_room_ids[room_type] += 1
            
            assignments[customer_id] = (room_type, room_id)
            heapq.heappush(occupied_rooms, (departure, room_type, room_id))
    
    return assignments
```

### 🔗 **Related Problems & Concepts**

#### **1. Interval Scheduling Problems**
- **Activity Selection**: Select maximum activities
- **Interval Partitioning**: Partition intervals into minimum groups
- **Weighted Interval Scheduling**: Maximize weight of non-overlapping intervals
- **Interval Merging**: Merge overlapping intervals

#### **2. Priority Queue Problems**
- **Priority Queue Implementation**: Custom priority queue design
- **Heap Operations**: Efficient heap operations
- **Top K Elements**: Find top k elements efficiently
- **Median Finding**: Find median using heaps

#### **3. Resource Allocation Problems**
- **Job Scheduling**: Schedule jobs on machines
- **Resource Management**: Allocate limited resources
- **Load Balancing**: Distribute load evenly
- **Capacity Planning**: Plan resource capacity

#### **4. Greedy Algorithm Problems**
- **Fractional Knapsack**: Fill knapsack optimally
- **Huffman Coding**: Build optimal prefix codes
- **Dijkstra's Algorithm**: Find shortest paths
- **Prim's Algorithm**: Find minimum spanning tree

#### **5. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Network Flow**: Maximum flow applications
- **Combinatorial Optimization**: Discrete optimization
- **Approximation Algorithms**: Find approximate solutions

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    customers = []
    for _ in range(n):
        a, b = map(int, input().split())
        customers.append((a, b))
    
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
        
        assignments[customer_id] = room_id
        heapq.heappush(occupied_rooms, (departure, room_id))
    
    print(next_room_id - 1)
    print(*assignments)
```

#### **2. Range Queries**
```python
# Precompute room allocation for different time ranges
def precompute_room_allocation(customers, max_time):
    allocation_data = {}
    
    for start_time in range(max_time + 1):
        for end_time in range(start_time, max_time + 1):
            # Filter customers in time range
            filtered_customers = [(a, b, i) for i, (a, b) in enumerate(customers) 
                                if a >= start_time and b <= end_time]
            
            if filtered_customers:
                allocation_data[(start_time, end_time)] = room_allocation_optimized(
                    len(filtered_customers), filtered_customers)
    
    return allocation_data

# Answer queries about room allocation in time ranges
def allocation_query(allocation_data, start_time, end_time):
    return allocation_data.get((start_time, end_time), (0, []))
```

#### **3. Interactive Problems**
```python
# Interactive room allocation system
def interactive_room_allocation():
    n = int(input("Enter number of customers: "))
    customers = []
    
    for i in range(n):
        arrival = int(input(f"Enter arrival time for customer {i+1}: "))
        departure = int(input(f"Enter departure time for customer {i+1}: "))
        customers.append((arrival, departure))
    
    print(f"Customers: {customers}")
    
    customers = [(customers[i][0], customers[i][1], i) for i in range(n)]
    customers.sort()
    
    occupied_rooms = []
    available_rooms = []
    next_room_id = 1
    assignments = [0] * n
    
    for arrival, departure, customer_id in customers:
        print(f"\nProcessing customer {customer_id + 1}: arrival={arrival}, departure={departure}")
        
        # Free up rooms
        while occupied_rooms and occupied_rooms[0][0] < arrival:
            end_time, room_id = heapq.heappop(occupied_rooms)
            available_rooms.append(room_id)
            print(f"Room {room_id} freed at time {end_time}")
        
        print(f"Available rooms: {available_rooms}")
        
        # Assign room
        if available_rooms:
            room_id = available_rooms.pop()
            print(f"Assigned existing room {room_id}")
        else:
            room_id = next_room_id
            next_room_id += 1
            print(f"Created new room {room_id}")
        
        assignments[customer_id] = room_id
        heapq.heappush(occupied_rooms, (departure, room_id))
        print(f"Room {room_id} occupied until {departure}")
    
    print(f"\nMinimum rooms needed: {next_room_id - 1}")
    print(f"Assignments: {assignments}")
```

### 🧮 **Mathematical Extensions**

#### **1. Scheduling Theory**
- **Interval Scheduling**: Theory of interval scheduling
- **Resource Allocation**: Mathematical resource allocation
- **Queueing Theory**: Mathematical queueing theory
- **Optimization Theory**: Mathematical optimization

#### **2. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Amortized Analysis**: Average case analysis
- **Probabilistic Analysis**: Expected performance
- **Worst Case Analysis**: Upper bounds

#### **3. Graph Theory**
- **Interval Graphs**: Graph representation of intervals
- **Matching Theory**: Theory of matching in graphs
- **Coloring Problems**: Graph coloring applications
- **Network Flow**: Maximum flow theory

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Priority Queue**: Efficient priority queue algorithms
- **Greedy Algorithms**: Local optimal choices
- **Interval Scheduling**: Efficient scheduling algorithms
- **Resource Allocation**: Efficient allocation algorithms

#### **2. Mathematical Concepts**
- **Scheduling Theory**: Mathematical scheduling
- **Optimization**: Mathematical optimization theory
- **Graph Theory**: Graph algorithms and theory
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Priority Queue Implementation**: Efficient data structures
- **Greedy Algorithm Design**: Problem-solving strategies
- **Resource Management**: Efficient resource handling
- **Algorithm Design**: Problem-solving strategies

---

*This analysis demonstrates interval scheduling techniques and shows various extensions for resource allocation problems.* 