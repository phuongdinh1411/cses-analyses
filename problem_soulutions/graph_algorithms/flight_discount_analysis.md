# CSES Flight Discount - Problem Analysis

## Problem Statement
Given a directed graph with n cities and m flights, find the minimum cost to travel from city 1 to city n. You can use at most one discount coupon that halves the cost of any flight.

### Input
The first input line has two integers n and m: the number of cities and flights.
Then there are m lines describing the flights. Each line has three integers a, b, and c: there is a flight from city a to city b with cost c.

### Output
Print one integer: the minimum cost to travel from city 1 to city n.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n
- 1 ≤ c ≤ 10^9

### Example
```
Input:
3 4
1 2 3
2 3 1
1 3 7
2 1 5

Output:
2
```

## Solution Progression

### Approach 1: Dijkstra with Discount State - O(m log n)
**Description**: Use Dijkstra's algorithm with a state to track discount usage.

```python
import heapq

def flight_discount_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state
    pq = [(0, 1, False)]  # (cost, node, discount_used)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[1][0] = 0
    
    while pq:
        cost, node, used = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Without discount
            if not used and cost + weight < dist[neighbor][0]:
                dist[neighbor][0] = cost + weight
                heapq.heappush(pq, (dist[neighbor][0], neighbor, False))
            
            # With discount (if not used yet)
            if not used and cost + weight // 2 < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight // 2
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
            
            # Already used discount
            if used and cost + weight < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
    
    return min(dist[n][0], dist[n][1])
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Dijkstra with State - O(m log n)
**Description**: Use optimized Dijkstra with cleaner state management.

```python
import heapq

def flight_discount_optimized(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state
    pq = [(0, 1, False)]  # (cost, node, discount_used)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[1][0] = 0
    
    while pq:
        cost, node, used = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Try without discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][used]:
                dist[neighbor][used] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, used))
            
            # Try with discount (if not used yet)
            if not used:
                new_cost = cost + weight // 2
                if new_cost < dist[neighbor][1]:
                    dist[neighbor][1] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, True))
    
    return min(dist[n][0], dist[n][1])
```

**Why this improvement works**: We use Dijkstra's algorithm with a state to track whether the discount has been used. We maintain two distances for each node: one without discount and one with discount.

## Final Optimal Solution

```python
import heapq

n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

def find_minimum_cost_with_discount(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state
    pq = [(0, 1, False)]  # (cost, node, discount_used)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[1][0] = 0
    
    while pq:
        cost, node, used = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Try without discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][used]:
                dist[neighbor][used] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, used))
            
            # Try with discount (if not used yet)
            if not used:
                new_cost = cost + weight // 2
                if new_cost < dist[neighbor][1]:
                    dist[neighbor][1] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, True))
    
    return min(dist[n][0], dist[n][1])

result = find_minimum_cost_with_discount(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Dijkstra with State | O(m log n) | O(n) | Use state to track discount usage |
| Optimized Dijkstra | O(m log n) | O(n) | Cleaner state management |

## Key Insights for Other Problems

### 1. **Dijkstra with State**
**Principle**: Use Dijkstra's algorithm with additional state to handle constraints like discount usage.
**Applicable to**: Shortest path problems, constraint problems, graph problems

### 2. **State Management**
**Principle**: Maintain multiple distances for each node based on different states.
**Applicable to**: State-dependent problems, constraint problems, optimization problems

### 3. **Discount Optimization**
**Principle**: Find optimal use of limited resources (like discounts) in path problems.
**Applicable to**: Resource optimization problems, path problems, constraint problems

## Notable Techniques

### 1. **Dijkstra with State**
```python
def dijkstra_with_state(n, adj, start, end):
    pq = [(0, start, False)]  # (cost, node, state)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[start][0] = 0
    
    while pq:
        cost, node, state = heapq.heappop(pq)
        
        if node == end:
            return cost
        
        if cost > dist[node][state]:
            continue
        
        for neighbor, weight in adj[node]:
            # Process with current state
            new_cost = cost + weight
            if new_cost < dist[neighbor][state]:
                dist[neighbor][state] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, state))
            
            # Process with state change (if applicable)
            if not state:
                new_cost = cost + weight // 2
                if new_cost < dist[neighbor][1]:
                    dist[neighbor][1] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, True))
    
    return min(dist[end][0], dist[end][1])
```

### 2. **State Tracking**
```python
def track_state(cost, node, used, dist, pq):
    if cost < dist[node][used]:
        dist[node][used] = cost
        heapq.heappush(pq, (cost, node, used))
```

### 3. **Discount Application**
```python
def apply_discount(weight, discount_used):
    if not discount_used:
        return weight // 2
    return weight
```

## Problem-Solving Framework

1. **Identify problem type**: This is a shortest path problem with a discount constraint
2. **Choose approach**: Use Dijkstra's algorithm with state tracking
3. **Define state**: Track whether discount has been used
4. **Initialize**: Set up priority queue and distance arrays
5. **Process nodes**: Handle both with and without discount cases
6. **Update distances**: Maintain separate distances for each state
7. **Return result**: Output minimum of both final states

---

*This analysis shows how to efficiently find the minimum cost path with discount using Dijkstra's algorithm with state tracking.* 