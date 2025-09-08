---
layout: simple
title: "Nearest Shops - Multi-Source Shortest Path Problem"
permalink: /problem_soulutions/advanced_graph_problems/nearest_shops_analysis
---

# Nearest Shops - Multi-Source Shortest Path Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of multi-source shortest path problems
- Apply Dijkstra's algorithm with multiple source vertices
- Implement efficient multi-source BFS for unweighted graphs
- Optimize shortest path algorithms for multiple destinations
- Handle edge cases in multi-source problems (no reachable shops, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dijkstra's algorithm, BFS, shortest path algorithms
- **Data Structures**: Priority queues, adjacency lists, distance arrays
- **Mathematical Concepts**: Graph theory, shortest path properties, greedy algorithms
- **Programming Skills**: Priority queue implementation, graph representation, distance tracking
- **Related Problems**: Shortest Routes I (single-source shortest path), Message Route (BFS), Monsters (multi-source BFS)

## 📋 Problem Description

Given a graph with shops and customers, find the nearest shop for each customer.

**Input**: 
- n: number of nodes (shops and customers)
- m: number of edges
- k: number of shops
- m lines: a b w (edge from a to b with weight w)
- k lines: shop locations

**Output**: 
- For each customer, find the nearest shop and distance

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5
- 1 ≤ k ≤ n
- 1 ≤ w ≤ 10^9

**Example**:
```
Input:
4 4 2
1 2 3
2 3 2
3 4 1
1 4 5
1
3

Output:
Customer 2: Nearest shop is 1, distance = 3
Customer 4: Nearest shop is 3, distance = 1

Explanation**: 
Shop at node 1, shop at node 3
Customer 2 is closest to shop 1 (distance 3)
Customer 4 is closest to shop 3 (distance 1)
```

### 📊 Visual Example

**Input Graph with Shops and Customers:**
```
Shops: 🏪 (nodes 1, 3)
Customers: 👤 (nodes 2, 4)

    1🏪 ──3── 2👤
    │           │
    │5          │2
    │           │
    4👤 ──1── 3🏪
```

**Multi-Source Dijkstra Process:**
```
Step 1: Initialize with shops as sources
Queue: [(0,1), (0,3)]  ← (distance, node)
Distances: [∞, 0, ∞, 0]  ← shops at distance 0

Step 2: Process node 1 (distance 0)
Neighbors: 2 (weight 3), 4 (weight 5)
Queue: [(0,3), (3,2), (5,4)]
Distances: [∞, 0, 3, 0]

Step 3: Process node 3 (distance 0)
Neighbors: 2 (weight 2), 4 (weight 1)
Queue: [(1,4), (2,2), (3,2), (5,4)]
Distances: [∞, 0, 2, 1]  ← Update 2 and 4

Step 4: Process node 4 (distance 1)
Neighbors: 1 (weight 5), 3 (weight 1)
Queue: [(2,2), (3,2), (5,4)]
Distances: [∞, 0, 2, 1]  ← No improvement

Step 5: Process node 2 (distance 2)
Neighbors: 1 (weight 3), 3 (weight 2)
Queue: [(3,2), (5,4)]
Distances: [∞, 0, 2, 1]  ← No improvement
```

**Final Results:**
```
Customer 2: Nearest shop is 3, distance = 2
Customer 4: Nearest shop is 3, distance = 1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Single-Source Dijkstra (Brute Force)

**Key Insights from Brute Force Approach**:
- **Single-Source Dijkstra**: Run Dijkstra's algorithm from each shop
- **Distance Comparison**: Compare distances from all shops to find nearest
- **Exhaustive Search**: Try all possible shop-customer combinations
- **Multiple Dijkstra Runs**: Run Dijkstra k times (once per shop)

**Key Insight**: Use brute force by running Dijkstra's algorithm from each shop and comparing distances.

**Algorithm**:
- For each shop, run Dijkstra's algorithm
- Calculate shortest distances to all customers
- For each customer, find the shop with minimum distance
- Return nearest shop and distance for each customer

**Visual Example**:
```
Graph: 1🏪-3-2👤, 2👤-2-3🏪, 3🏪-1-4👤, 1🏪-5-4👤

Brute Force Approach:
┌─────────────────────────────────────┐
│ Dijkstra from shop 1:              │
│ Distances: [0, 3, 5, 5]            │
│ Nearest to 2: shop 1 (dist 3)      │
│ Nearest to 4: shop 1 (dist 5)      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Dijkstra from shop 3:              │
│ Distances: [5, 2, 0, 1]            │
│ Nearest to 2: shop 3 (dist 2) ✓    │
│ Nearest to 4: shop 3 (dist 1) ✓    │
└─────────────────────────────────────┘

Result: Customer 2 → shop 3 (dist 2), Customer 4 → shop 3 (dist 1)
```

### Step 2: Initial Approach
**Brute force approach (inefficient but correct):**

**Key Observations:**
- This is a multi-source shortest path problem
- Can use Dijkstra's from all shops
- Need to find minimum distance to any shop
- Efficient algorithm is crucial

### Step 3: Optimization/Alternative
**Multi-source Dijkstra's approach:**

```python
def nearest_shops_dijkstra(n, edges, shops):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    import heapq
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    
    # Priority queue: (distance, node, shop)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        nearest_shop[shop] = shop
        heappush(pq, (0, shop, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node, shop = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                nearest_shop[neighbor] = shop
                heappush(pq, (new_dist, neighbor, shop))
    
    return distances, nearest_shop
```

**Why this works:**
- Uses multi-source Dijkstra's algorithm
- Finds shortest path from any shop
- Efficient priority queue implementation
- O((n + m) log n) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_nearest_shops():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b, w = map(int, input().split())
        edges.append((a, b, w))
    
    k = int(input())
    shops = list(map(int, input().split()))
    
    l = int(input())
    customers = list(map(int, input().split()))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    
    # Priority queue: (distance, node)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    # Print results for customers
    result = []
    for customer in customers:
        result.append(distances[customer])
    
    print(*result)

# Main execution
if __name__ == "__main__":
    solve_nearest_shops()
```

**Why this works:**
- Optimal multi-source shortest path approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, 4, [(1, 2, 1), (2, 3, 2), (3, 4, 1), (1, 4, 3)], [1, 4], [2, 3]),
        (3, 2, [(1, 2, 1), (2, 3, 1)], [1], [2, 3]),
    ]
    
    for n, m, edges, shops, customers in test_cases:
        result = solve_test(n, m, edges, shops, customers)
        print(f"n={n}, m={m}, edges={edges}, shops={shops}, customers={customers}")
        print(f"Result: {result}")
        print()

def solve_test(n, m, edges, shops, customers):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    
    # Priority queue: (distance, node)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    # Return results for customers
    result = []
    for customer in customers:
        result.append(distances[customer])
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O((n + m) log n) - multi-source Dijkstra's algorithm
- **Space**: O(n + m) - adjacency list and priority queue

### Why This Solution Works
- **Multi-Source Shortest Path**: Finds shortest path from any shop
- **Dijkstra's Algorithm**: Efficient shortest path algorithm
- **Priority Queue**: Maintains minimum distance nodes
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### Important Concepts and Patterns
- **Multi-Source Shortest Path**: Find shortest path from multiple sources efficiently
- **Dijkstra's Algorithm**: Efficient shortest path algorithm for weighted graphs
- **Priority Queue**: Maintains minimum distance nodes for optimal performance
- **Graph Algorithms**: Use BFS for unweighted graphs, Dijkstra's for weighted graphs

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Nearest Shops with Constraints**
```python
def nearest_shops_constrained(n, edges, shops, customers, constraints):
    # Handle nearest shops with additional constraints
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Apply constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    allowed_shops = constraints.get('allowed_shops', set(shops))
    
    # Remove forbidden edges
    filtered_adj = [[] for _ in range(n + 1)]
    for a in range(n + 1):
        for b, w in adj[a]:
            if (a, b) not in forbidden_edges and (b, a) not in forbidden_edges:
                filtered_adj[a].append((b, w))
    
    # Multi-source Dijkstra's with constraints
    from heapq import heappush, heappop
    
    distances = [float('inf')] * (n + 1)
    pq = []
    
    # Add only allowed shops to priority queue
    for shop in shops:
        if shop in allowed_shops:
            distances[shop] = 0
            heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in filtered_adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    # Return results for customers
    result = []
    for customer in customers:
        result.append(distances[customer])
    
    return result
```

#### **2. Nearest Shops with Dynamic Updates**
```python
def nearest_shops_dynamic(n, initial_edges, initial_shops, operations):
    # Handle nearest shops with dynamic shop updates
    
    current_edges = initial_edges.copy()
    current_shops = initial_shops.copy()
    results = []
    
    for op in operations:
        if op[0] == 'add_shop':
            # Add new shop
            shop = op[1]
            current_shops.append(shop)
        elif op[0] == 'remove_shop':
            # Remove shop
            shop = op[1]
            current_shops.remove(shop)
        elif op[0] == 'add_edge':
            # Add new edge
            a, b, w = op[1], op[2], op[3]
            current_edges.append((a, b, w))
        elif op[0] == 'query':
            # Query nearest shops
            customers = op[1]
            result = solve_nearest_shops(n, current_edges, current_shops, customers)
            results.append(result)
    
    return results
```

#### **3. Nearest Shops with Multiple Criteria**
```python
def nearest_shops_multiple_criteria(n, edges, shops, customers, criteria):
    # Handle nearest shops with multiple criteria (distance, price, rating)
    
    # Build adjacency list with multiple weights
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's with multiple criteria
    from heapq import heappush, heappop
    
    distances = [float('inf')] * (n + 1)
    prices = [float('inf')] * (n + 1)
    ratings = [0] * (n + 1)
    
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        prices[shop] = criteria['shop_prices'].get(shop, 0)
        ratings[shop] = criteria['shop_ratings'].get(shop, 0)
        heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prices[neighbor] = prices[node]
                ratings[neighbor] = ratings[node]
                heappush(pq, (new_dist, neighbor))
    
    # Return results for customers with multiple criteria
    result = []
    for customer in customers:
        result.append({
            'distance': distances[customer],
            'price': prices[customer],
            'rating': ratings[customer]
        })
    
    return result
```

## 🔗 Related Problems

### Links to Similar Problems
- **Graph Theory**: Multi-source shortest path, Dijkstra's algorithm
- **Graph Algorithms**: BFS, shortest path algorithms
- **Location Optimization**: Facility location, nearest neighbor
- **Optimization**: Multi-source problems, distance optimization

## 📚 Learning Points

### Key Takeaways
- **Multi-source shortest path** efficiently handles multiple starting points
- **Dijkstra's algorithm** is optimal for weighted graphs
- **Priority queue** maintains optimal performance
- **Graph algorithms** solve complex location optimization problems

## 🎯 Problem Variations

### Variation 1: Nearest Shops with Constraints
**Problem**: Find nearest shop with certain constraints.

```python
def constrained_nearest_shops(n, edges, shops, customers, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Apply constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    allowed_shops = constraints.get('allowed_shops', set(shops))
    
    # Remove forbidden edges
    for a, b, w in forbidden_edges:
        if (a, b, w) in edges:
            edges.remove((a, b, w))
        if (b, a, w) in edges:
            edges.remove((b, a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    
    # Priority queue: (distance, node)
    pq = []
    
    # Add allowed shops to priority queue
    for shop in allowed_shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    # Return results for customers
    result = []
    for customer in customers:
        result.append(distances[customer])
    
    return result
```

### Variation 2: Nearest Shops with Time Windows
**Problem**: Shops have opening hours, find nearest open shop.

```python
def time_window_nearest_shops(n, edges, shops, customers, time_windows):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's with time consideration
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    
    # Priority queue: (distance, node, time)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop, 0))
    
    # Dijkstra's algorithm
    while pq:
        dist, node, time = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            new_time = time + weight
            
            # Check if shop is open at new time
            if neighbor in time_windows:
                open_start, open_end = time_windows[neighbor]
                if not (open_start <= new_time <= open_end):
                    continue
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor, new_time))
    
    # Return results for customers
    result = []
    for customer in customers:
        result.append(distances[customer])
    
    return result
```

### Variation 3: Dynamic Nearest Shops
**Problem**: Support adding/removing shops and customers dynamically.

```python
class DynamicNearestShops:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.edges = set()
        self.shops = set()
    
    def add_edge(self, a, b, w):
        if (a, b, w) not in self.edges and (b, a, w) not in self.edges:
            self.edges.add((a, b, w))
            self.adj[a].append((b, w))
            self.adj[b].append((a, w))
    
    def remove_edge(self, a, b, w):
        if (a, b, w) in self.edges:
            self.edges.remove((a, b, w))
            self.adj[a].remove((b, w))
            self.adj[b].remove((a, w))
            return True
        elif (b, a, w) in self.edges:
            self.edges.remove((b, a, w))
            self.adj[a].remove((b, w))
            self.adj[b].remove((a, w))
            return True
        return False
    
    def add_shop(self, shop):
        self.shops.add(shop)
    
    def remove_shop(self, shop):
        if shop in self.shops:
            self.shops.remove(shop)
            return True
        return False
    
    def get_nearest_shop(self, customer):
        # Multi-source Dijkstra's
        from heapq import heappush, heappop
        
        # Initialize distances
        distances = [float('inf')] * (self.n + 1)
        
        # Priority queue: (distance, node)
        pq = []
        
        # Add all shops to priority queue
        for shop in self.shops:
            distances[shop] = 0
            heappush(pq, (0, shop))
        
        # Dijkstra's algorithm
        while pq:
            dist, node = heappop(pq)
            
            if dist > distances[node]:
                continue
            
            for neighbor, weight in self.adj[node]:
                new_dist = dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor))
        
        return distances[customer]
```

### Variation 4: Nearest Shops with Multiple Constraints
**Problem**: Find nearest shop satisfying multiple constraints.

```python
def multi_constrained_nearest_shops(n, edges, shops, customers, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Apply multiple constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    allowed_shops = constraints.get('allowed_shops', set(shops))
    max_distance = constraints.get('max_distance', float('inf'))
    
    # Remove forbidden edges
    for a, b, w in forbidden_edges:
        if (a, b, w) in edges:
            edges.remove((a, b, w))
        if (b, a, w) in edges:
            edges.remove((b, a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    
    # Priority queue: (distance, node)
    pq = []
    
    # Add allowed shops to priority queue
    for shop in allowed_shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node] or dist > max_distance:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor] and new_dist <= max_distance:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    # Return results for customers
    result = []
    for customer in customers:
        result.append(distances[customer])
    
    return result
```

### Variation 5: Nearest Shops with Capacity
**Problem**: Shops have capacity limits, find nearest available shop.

```python
def capacity_nearest_shops(n, edges, shops, customers, capacities):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's with capacity consideration
    from heapq import heappush, heappop
    
    # Initialize distances and capacities
    distances = [float('inf')] * (n + 1)
    remaining_capacity = capacities.copy()
    
    # Priority queue: (distance, node)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    # Assign customers to shops with capacity
    result = []
    for customer in customers:
        # Find nearest shop with available capacity
        nearest_shop = None
        min_distance = float('inf')
        
        for shop in shops:
            if remaining_capacity[shop] > 0 and distances[customer] < min_distance:
                min_distance = distances[customer]
                nearest_shop = shop
        
        if nearest_shop:
            remaining_capacity[nearest_shop] -= 1
            result.append(min_distance)
        else:
            result.append(-1)  # No available shop
    
    return result
```

## 🔗 Related Problems

- **[Shortest Path](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Shortest path algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Dijkstra's Algorithm](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Dijkstra's algorithm

## 📚 Learning Points

1. **Multi-Source Shortest Path**: Essential for multiple sources
2. **Dijkstra's Algorithm**: Efficient shortest path algorithm
3. **Priority Queue**: Important data structure
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to nearest shops and multi-source shortest paths!** 🎯
    
    # Return results
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

**Why this works:**
- Uses multi-source Dijkstra's algorithm
- Finds shortest paths from all shops
- Handles weighted edges efficiently
- O((n + m) log n) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_nearest_shops():
    n, m, k = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b, w = map(int, input().split())
        edges.append((a, b, w))
    
    shops = []
    for _ in range(k):
        shop = int(input())
        shops.append(shop)
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    
    # Priority queue: (distance, node)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    # Print results
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            print(-1)
        else:
            print(distances[i])

# Main execution
if __name__ == "__main__":
    solve_nearest_shops()
```

**Why this works:**
- Optimal multi-source Dijkstra's approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2, 3), (2, 3, 2), (3, 4, 1), (1, 4, 5)], [1, 3]),
        (3, [(1, 2, 1), (2, 3, 1)], [1]),
    ]
    
    for n, edges, shops in test_cases:
        result = solve_test(n, edges, shops)
        print(f"n={n}, edges={edges}, shops={shops}")
        print(f"Distances: {result}")
        print()

def solve_test(n, edges, shops):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    distances = [float('inf')] * (n + 1)
    pq = []
    
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O((n + m) log n) - multi-source Dijkstra's
- **Space**: O(n + m) - adjacency list and priority queue

### Why This Solution Works
- **Multi-Source Dijkstra's**: Finds shortest paths from all shops
- **Priority Queue**: Efficiently processes vertices
- **Distance Tracking**: Maintains minimum distances
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Multi-Source Shortest Paths**
- Dijkstra's from multiple sources
- Essential for nearest neighbor problems
- Key optimization technique
- Enables efficient solution

### 2. **Priority Queue**
- Efficient vertex processing
- Important for performance
- Fundamental data structure
- Essential for algorithm

### 3. **Distance Tracking**
- Maintain minimum distances
- Important for optimization
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Unweighted Graph
**Problem**: Find nearest shops in an unweighted graph.

```python
def nearest_shops_bfs(n, edges, shops):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Multi-source BFS
    from collections import deque
    
    distances = [float('inf')] * (n + 1)
    queue = deque()
    
    # Add all shops to queue
    for shop in shops:
        distances[shop] = 0
        queue.append((shop, 0))
    
    # BFS
    while queue:
        node, dist = queue.popleft()
        
        for neighbor in adj[node]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))
    
    # Return results
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

### Variation 2: Directed Graph
**Problem**: Find nearest shops in a directed graph.

```python
def nearest_shops_directed(n, edges, shops):
    # Build directed adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))  # Directed edge
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    distances = [float('inf')] * (n + 1)
    pq = []
    
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

### Variation 3: K-Nearest Shops
**Problem**: Find k nearest shops for each vertex.

```python
def k_nearest_shops(n, edges, shops, k):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's with k nearest
    from heapq import heappush, heappop
    
    # distances[i][j] = distance from vertex i to j-th nearest shop
    distances = [[float('inf')] * k for _ in range(n + 1)]
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop][0] = 0
        heappush(pq, (0, shop, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node, shop = heappop(pq)
        
        # Find position in k nearest for this shop
        pos = 0
        while pos < k and distances[node][pos] != float('inf'):
            if distances[node][pos] == dist:
                break
            pos += 1
        
        if pos >= k:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            # Check if this is a better distance
            for i in range(k):
                if new_dist < distances[neighbor][i]:
                    # Shift distances
                    for j in range(k-1, i, -1):
                        distances[neighbor][j] = distances[neighbor][j-1]
                    distances[neighbor][i] = new_dist
                    heappush(pq, (new_dist, neighbor, shop))
                    break
    
    return distances
```

### Variation 4: Dynamic Shops
**Problem**: Support adding/removing shops and answering nearest shop queries.

```python
class DynamicNearestShops:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.shops = set()
    
    def add_edge(self, a, b, w):
        self.adj[a].append((b, w))
        self.adj[b].append((a, w))
    
    def add_shop(self, shop):
        self.shops.add(shop)
    
    def remove_shop(self, shop):
        self.shops.discard(shop)
    
    def get_nearest_shop(self, vertex):
        if not self.shops:
            return -1
        
        # Single-source Dijkstra's from vertex
        from heapq import heappush, heappop
        
        distances = [float('inf')] * (self.n + 1)
        distances[vertex] = 0
        pq = [(0, vertex)]
        
        while pq:
            dist, node = heappop(pq)
            
            if dist > distances[node]:
                continue
            
            if node in self.shops:
                return dist
            
            for neighbor, weight in self.adj[node]:
                new_dist = dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor))
        
        return -1
```

### Variation 5: Shop with Constraints
**Problem**: Find nearest shop with certain constraints.

```python
def constrained_nearest_shops(n, edges, shops, constraints):
    # constraints: set of forbidden vertex pairs
    # Build adjacency list avoiding constraints
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        if (a, b) not in constraints and (b, a) not in constraints:
            adj[a].append((b, w))
            adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    distances = [float('inf')] * (n + 1)
    pq = []
    
    for shop in shops:
        distances[shop] = 0
        heappush(pq, (0, shop))
    
    while pq:
        dist, node = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))
    
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

## 🔗 Related Problems

- **[Shortest Paths](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[Dijkstra's Algorithm](/cses-analyses/problem_soulutions/graph_algorithms/)**: Shortest path algorithms
- **[Multi-Source BFS](/cses-analyses/problem_soulutions/graph_algorithms/)**: BFS algorithms

## 📚 Learning Points

1. **Multi-Source Dijkstra's**: Essential for nearest neighbor problems
2. **Priority Queue**: Efficient vertex processing
3. **Shortest Paths**: Fundamental graph algorithm
4. **Distance Tracking**: Important optimization technique

---

**This is a great introduction to nearest shop problems and multi-source shortest paths!** 🎯
    
    return distances, nearest_shop
```

**Why this works:**
- Uses multi-source Dijkstra's
- Finds shortest path from any shop
- Efficient priority queue implementation
- O((n + m) log n) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_nearest_shops():
    n, m, k = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b, w = map(int, input().split())
        edges.append((a, b, w))
    
    shops = []
    for _ in range(k):
        shop = int(input())
        shops.append(shop)
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    
    # Priority queue: (distance, node, shop)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        nearest_shop[shop] = shop
        heappush(pq, (0, shop, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node, shop = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                nearest_shop[neighbor] = shop
                heappush(pq, (new_dist, neighbor, shop))
    
    # Print results for customers
    for i in range(1, n + 1):
        if i not in shops:
            print(f"Customer {i}: Nearest shop is {nearest_shop[i]}, distance = {distances[i]}")

# Main execution
if __name__ == "__main__":
    solve_nearest_shops()
```

**Why this works:**
- Optimal multi-source shortest path approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 2, 3), (2, 3, 2), (3, 4, 1), (1, 4, 5)], [1, 3]),
        (3, [(1, 2, 1), (2, 3, 2)], [1]),
        (5, [(1, 2, 1), (2, 3, 2), (3, 4, 1), (4, 5, 3)], [1, 5]),
    ]
    
    for n, edges, shops in test_cases:
        result = solve_test(n, edges, shops)
        print(f"n={n}, edges={edges}, shops={shops}")
        print(f"Result: {result}")
        print()

def solve_test(n, edges, shops):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # Initialize distances
    distances = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    
    # Priority queue: (distance, node, shop)
    pq = []
    
    # Add all shops to priority queue
    for shop in shops:
        distances[shop] = 0
        nearest_shop[shop] = shop
        heappush(pq, (0, shop, shop))
    
    # Dijkstra's algorithm
    while pq:
        dist, node, shop = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                nearest_shop[neighbor] = shop
                heappush(pq, (new_dist, neighbor, shop))
    
    # Return results for customers
    result = {}
    for i in range(1, n + 1):
        if i not in shops:
            result[i] = (nearest_shop[i], distances[i])
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O((n + m) log n) - multi-source Dijkstra's
- **Space**: O(n + m) - adjacency list and priority queue

### Why This Solution Works
- **Multi-Source Dijkstra's**: Finds shortest paths from all shops
- **Priority Queue**: Efficient distance updates
- **Nearest Shop Tracking**: Maintains which shop is closest
- **Optimal Approach**: Guarantees shortest distances

## 🎯 Key Insights

### 1. **Multi-Source Shortest Path**
- Dijkstra's from multiple sources
- Key insight for optimization
- Essential for understanding
- Enables efficient solution

### 2. **Priority Queue Usage**
- Efficient distance updates
- Maintains minimum distances
- Important for performance
- Fundamental data structure

### 3. **Nearest Shop Tracking**
- Track which shop is closest
- Update when better path found
- Simple but important observation
- Essential for solution

## 🎯 Problem Variations

### Variation 1: Weighted Customer Preferences
**Problem**: Each customer has preferences for shops. Find nearest preferred shop.

```python
def nearest_preferred_shops(n, edges, shops, customer_preferences):
    # customer_preferences[customer] = list of preferred shops
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's for each customer
    from heapq import heappush, heappop
    
    result = {}
    
    for customer in range(1, n + 1):
        if customer in shops:
            continue
        
        # Find shortest path to preferred shops
        distances = [float('inf')] * (n + 1)
        pq = []
        
        # Add preferred shops to priority queue
        for shop in customer_preferences.get(customer, shops):
            if shop in shops:
                distances[shop] = 0
                heappush(pq, (0, shop))
        
        # Dijkstra's algorithm
        while pq:
            dist, node = heappop(pq)
            
            if dist > distances[node]:
                continue
            
            for neighbor, weight in adj[node]:
                new_dist = dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heappush(pq, (new_dist, neighbor))
        
        # Find nearest preferred shop
        min_dist = float('inf')
        nearest_shop = -1
        
        for shop in customer_preferences.get(customer, shops):
            if shop in shops and distances[shop] < min_dist:
                min_dist = distances[shop]
                nearest_shop = shop
        
        result[customer] = (nearest_shop, min_dist)
    
    return result
```

### Variation 2: Dynamic Shop Locations
**Problem**: Support adding/removing shops dynamically.

```python
class DynamicNearestShops:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        for a, b, w in edges:
            self.adj[a].append((b, w))
            self.adj[b].append((a, w))
        self.shops = set()
    
    def add_shop(self, shop):
        self.shops.add(shop)
        self.update_distances()
    
    def remove_shop(self, shop):
        self.shops.discard(shop)
        self.update_distances()
    
    def update_distances(self):
        # Recompute distances when shops change
        from heapq import heappush, heappop
        
        self.distances = [float('inf')] * (self.n + 1)
        self.nearest_shop = [-1] * (self.n + 1)
        
        pq = []
        for shop in self.shops:
            self.distances[shop] = 0
            self.nearest_shop[shop] = shop
            heappush(pq, (0, shop, shop))
        
        while pq:
            dist, node, shop = heappop(pq)
            
            if dist > self.distances[node]:
                continue
            
            for neighbor, weight in self.adj[node]:
                new_dist = dist + weight
                
                if new_dist < self.distances[neighbor]:
                    self.distances[neighbor] = new_dist
                    self.nearest_shop[neighbor] = shop
                    heappush(pq, (new_dist, neighbor, shop))
    
    def get_nearest_shop(self, customer):
        if customer in self.shops:
            return (customer, 0)
        return (self.nearest_shop[customer], self.distances[customer])
```

### Variation 3: Shop Capacity Constraints
**Problem**: Each shop has a capacity limit. Find nearest available shop.

```python
def nearest_available_shops(n, edges, shops, capacities, customer_demands):
    # capacities[shop] = maximum customers
    # customer_demands[customer] = demand amount
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    distances = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    
    pq = []
    for shop in shops:
        distances[shop] = 0
        nearest_shop[shop] = shop
        heappush(pq, (0, shop, shop))
    
    while pq:
        dist, node, shop = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                nearest_shop[neighbor] = shop
                heappush(pq, (new_dist, neighbor, shop))
    
    # Assign customers to available shops
    shop_usage = {shop: 0 for shop in shops}
    assignments = {}
    
    # Sort customers by distance to nearest shop
    customers = [(i, distances[i], nearest_shop[i]) for i in range(1, n + 1) if i not in shops]
    customers.sort(key=lambda x: x[1])
    
    for customer, dist, shop in customers:
        if shop_usage[shop] + customer_demands[customer] <= capacities[shop]:
            assignments[customer] = (shop, dist)
            shop_usage[shop] += customer_demands[customer]
        else:
            # Find next nearest available shop
            assignments[customer] = (-1, float('inf'))  # No available shop
    
    return assignments
```

### Variation 4: Time-Dependent Distances
**Problem**: Edge weights change over time. Find nearest shop considering time.

```python
def time_dependent_nearest_shops(n, edges, shops, time):
    # edges: (a, b, base_weight, time_factor)
    # weight = base_weight + time_factor * time
    
    # Build adjacency list with time-dependent weights
    adj = [[] for _ in range(n + 1)]
    for a, b, base_w, time_factor in edges:
        weight = base_w + time_factor * time
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    distances = [float('inf')] * (n + 1)
    nearest_shop = [-1] * (n + 1)
    
    pq = []
    for shop in shops:
        distances[shop] = 0
        nearest_shop[shop] = shop
        heappush(pq, (0, shop, shop))
    
    while pq:
        dist, node, shop = heappop(pq)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                nearest_shop[neighbor] = shop
                heappush(pq, (new_dist, neighbor, shop))
    
    return distances, nearest_shop
```

### Variation 5: Multiple Nearest Shops
**Problem**: Find k nearest shops for each customer.

```python
def k_nearest_shops(n, edges, shops, k):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    
    # Multi-source Dijkstra's
    from heapq import heappush, heappop
    
    # For each node, maintain k nearest shops
    k_nearest = [[] for _ in range(n + 1)]
    
    pq = []
    for shop in shops:
        heappush(pq, (0, shop, shop))
    
    while pq:
        dist, node, shop = heappop(pq)
        
        # Add to k nearest if not already present
        if len(k_nearest[node]) < k:
            k_nearest[node].append((shop, dist))
        
        # Continue if we haven't found k shops yet
        if len(k_nearest[node]) < k:
            for neighbor, weight in adj[node]:
                new_dist = dist + weight
                heappush(pq, (new_dist, neighbor, shop))
    
    return k_nearest
```

## 🔗 Related Problems

- **[Shortest Path](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_i_analysis)**: Path algorithms
- **[Dijkstra's Algorithm](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[Graph Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms

## 📚 Learning Points

1. **Multi-Source Shortest Path**: Essential for location problems
2. **Dijkstra's Algorithm**: Efficient shortest path finding
3. **Priority Queue**: Key data structure for graph algorithms
4. **Location Optimization**: Common pattern in real-world problems

---

**This is a great introduction to multi-source shortest path and location optimization!** 🎯 