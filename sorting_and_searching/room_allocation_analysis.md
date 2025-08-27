# CSES Room Allocation - Problem Analysis

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