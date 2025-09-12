---
layout: simple
title: "Message Route - Shortest Path Finding"
permalink: /problem_soulutions/graph_algorithms/message_route_analysis
---

# Message Route - Shortest Path Finding

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand shortest path problems and path reconstruction concepts
- Apply BFS to find shortest paths in unweighted graphs with path tracking
- Implement efficient shortest path algorithms with proper path reconstruction
- Optimize shortest path solutions using parent tracking and path enumeration
- Handle edge cases in shortest path problems (no path exists, single node, disconnected graphs)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: BFS, shortest path algorithms, path reconstruction, graph traversal, pathfinding
- **Data Structures**: Queues, parent arrays, path tracking, graph representations, BFS data structures
- **Mathematical Concepts**: Graph theory, shortest path properties, path reconstruction, graph traversal
- **Programming Skills**: BFS implementation, path tracking, graph traversal, algorithm implementation
- **Related Problems**: Labyrinth (grid pathfinding), Monsters (grid algorithms), Graph traversal

## Problem Description

**Problem**: There are n computers numbered 1,2,…,n. The computers are connected through m cables. Your task is to find a route from computer 1 to computer n.

This is a classic shortest path problem in an unweighted, undirected graph. The goal is to find the minimum number of computers to traverse to get from computer 1 to computer n, and output the actual path.

**Input**: 
- First line: Two integers n and m (number of computers and cables)
- Next m lines: Two integers a and b (cable between computers a and b)

**Output**: 
- First line: Number of computers on the route
- Second line: The route (sequence of computers)

**Constraints**:
- 2 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- Graph is undirected
- No self-loops or multiple edges between same pair of computers
- Cables are bidirectional
- Computers are numbered 1, 2, ..., n

**Example**:
```
Input:
5 5
1 2
1 3
1 4
2 3
5 4

Output:
3
1 4 5
```

**Explanation**: 
- Route: 1 → 4 → 5
- Number of computers: 3
- This is the shortest path from computer 1 to computer 5

## Visual Example

### Input Graph
```
Computers: 1, 2, 3, 4, 5
Cables: (1,2), (1,3), (1,4), (2,3), (5,4)

Graph representation:
    2 ──── 3
    │
    1 ──── 4 ──── 5
```

### BFS Traversal Process
```
Step 1: Initialize BFS from computer 1
Queue: [1]
Visited: {1}
Parent: {1: None}
Distance: {1: 0}

Step 2: Process computer 1
Queue: [2, 3, 4] (neighbors of 1)
Visited: {1, 2, 3, 4}
Parent: {1: None, 2: 1, 3: 1, 4: 1}
Distance: {1: 0, 2: 1, 3: 1, 4: 1}

Step 3: Process computer 2
Queue: [3, 4] (2's neighbor 3 already visited)
Visited: {1, 2, 3, 4}
Parent: {1: None, 2: 1, 3: 1, 4: 1}
Distance: {1: 0, 2: 1, 3: 1, 4: 1}

Step 4: Process computer 3
Queue: [4] (3's neighbors 1,2 already visited)
Visited: {1, 2, 3, 4}

Step 5: Process computer 4
Queue: [5] (4's neighbor 5)
Visited: {1, 2, 3, 4, 5}
Parent: {1: None, 2: 1, 3: 1, 4: 1, 5: 4}
Distance: {1: 0, 2: 1, 3: 1, 4: 1, 5: 2}

Step 6: Process computer 5
Queue: [] (5 is the target)
Target reached!
```

### Path Reconstruction
```
From computer 5, trace back using parent array:
- 5 → parent[5] = 4
- 4 → parent[4] = 1
- 1 → parent[1] = None (source)

Reversed path: 5 → 4 → 1
Final path: 1 → 4 → 5
Distance: 2 (number of edges)
Computers visited: 3 (including start and end)
```

### Alternative Paths
```
Other possible paths from 1 to 5:
- 1 → 2 → 3 → (no connection to 5) ✗
- 1 → 3 → 2 → (no connection to 5) ✗
- 1 → 4 → 5 ✓ (shortest path)

Shortest path: 1 → 4 → 5 (length = 2)
```

### Key Insight
BFS guarantees finding the shortest path in an unweighted graph because:
1. It explores nodes level by level
2. First time we reach a node, we've found the shortest path to it
3. Parent array allows us to reconstruct the actual path
4. Time complexity: O(V + E) where V = vertices, E = edges

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths from source to destination
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths from computer 1 to computer n
2. For each path, check if it's valid (all edges exist)
3. Return the shortest valid path found
4. Handle cases where no path exists

**Visual Example:**
```
Brute force: Try all possible paths
For graph: 1-2-3, 1-4-5
- Path 1: [1, 2, 3] - Check if 3 connects to 5 ✗
- Path 2: [1, 2, 3, 4, 5] - Check if 3 connects to 4 ✗
- Path 3: [1, 3, 2, 4, 5] - Check if 2 connects to 4 ✗
- Path 4: [1, 4, 5] ✓ (valid path)
- Path 5: [1, 3, 4, 5] - Check if 3 connects to 4 ✗

Shortest valid path: [1, 4, 5]
```

**Implementation:**
```python
def message_route_brute_force(n, m, cables):
    from itertools import permutations
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def is_valid_path(path):
        for i in range(len(path) - 1):
            if path[i + 1] not in graph[path[i]]:
                return False
        return True
    
    # Try all possible paths of increasing length
    for length in range(2, n + 1):
        for path in permutations(range(1, n + 1), length):
            if path[0] == 1 and path[-1] == n and is_valid_path(path):
                return f"{len(path)}\n{' '.join(map(str, path))}"
    
    return "IMPOSSIBLE"

def solve_message_route_brute_force():
    n, m = map(int, input().split())
    cables = []
    for _ in range(m):
        a, b = map(int, input().split())
        cables.append((a, b))
    
    result = message_route_brute_force(n, m, cables)
    print(result)
```

**Time Complexity:** O(n! × n) for n computers with exponential path enumeration
**Space Complexity:** O(n) for storing path

**Why it's inefficient:**
- O(n!) time complexity is too slow for large n values
- Not suitable for competitive programming with n up to 10^5
- Inefficient for large inputs
- Poor performance with many computers

### Approach 2: Basic BFS with Path Tracking (Better)

**Key Insights from Basic BFS Solution:**
- Use BFS to find shortest path with path tracking
- Much more efficient than brute force approach
- Standard method for unweighted shortest path
- Can handle larger graphs than brute force

**Algorithm:**
1. Use BFS to traverse the graph level by level
2. Track the path while exploring
3. Return the first path found to destination
4. Handle cases where no path exists

**Visual Example:**
```
Basic BFS for graph: 1-2-3, 1-4-5
- Queue: [(1, [1])]
- Process 1: Queue: [(2, [1,2]), (3, [1,3]), (4, [1,4])]
- Process 2: Queue: [(3, [1,3]), (4, [1,4])]
- Process 3: Queue: [(4, [1,4])]
- Process 4: Queue: [(5, [1,4,5])]
- Process 5: Found target! Path: [1,4,5]
```

**Implementation:**
```python
def message_route_basic_bfs(n, m, cables):
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def bfs():
        queue = deque([(1, [1])])  # (node, path)
        visited = [False] * (n + 1)
        visited[1] = True
        
        while queue:
            node, path = queue.popleft()
            
            if node == n:
                return path
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None  # No path found
    
    path = bfs()
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"

def solve_message_route_basic_bfs():
    n, m = map(int, input().split())
    cables = []
    for _ in range(m):
        a, b = map(int, input().split())
        cables.append((a, b))
    
    result = message_route_basic_bfs(n, m, cables)
    print(result)
```

**Time Complexity:** O(n + m) for n computers and m cables with BFS traversal
**Space Complexity:** O(n + m) for graph representation and queue

**Why it's better:**
- O(n + m) time complexity is much better than O(n! × n)
- Standard method for unweighted shortest path
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized BFS with Parent Tracking (Optimal)

**Key Insights from Optimized BFS Solution:**
- Use BFS with parent tracking for efficient path reconstruction
- Most efficient approach for shortest path problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use BFS with parent tracking to find shortest path
2. Reconstruct path efficiently using parent array
3. Use optimized data structures for better performance
4. Return the shortest path efficiently

**Visual Example:**
```
Optimized BFS for graph: 1-2-3, 1-4-5
- Initialize: parent = [None, None, None, None, None, None]
- BFS: parent = [None, None, 1, 1, 1, 4]
- Path reconstruction: 5 → 4 → 1
- Final path: [1, 4, 5]
```

**Implementation:**
```python
def message_route_optimized_bfs(n, m, cables):
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def bfs():
        queue = deque([1])
        visited = [False] * (n + 1)
        parent = [None] * (n + 1)
        visited[1] = True
        
        while queue:
            node = queue.popleft()
            
            if node == n:
                # Reconstruct path
                path = []
                current = n
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Reverse to get correct order
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = node
                    queue.append(neighbor)
        
        return None  # No path found
    
    path = bfs()
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"

def solve_message_route():
    n, m = map(int, input().split())
    cables = []
    for _ in range(m):
        a, b = map(int, input().split())
        cables.append((a, b))
    
    result = message_route_optimized_bfs(n, m, cables)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_message_route()
```

**Time Complexity:** O(n + m) for n computers and m cables with optimized BFS
**Space Complexity:** O(n + m) for graph representation and parent array

**Why it's optimal:**
- O(n + m) time complexity is optimal for unweighted shortest path
- Uses optimized BFS with efficient parent tracking
- Most efficient approach for competitive programming
- Standard method for shortest path problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Message Route with Weights
**Problem**: Find shortest path considering cable weights.

**Link**: [CSES Problem Set - Message Route Weights](https://cses.fi/problemset/task/message_route_weights)

```python
def message_route_weights(n, m, cables, weights):
    from collections import deque
    import heapq
    
    # Build adjacency list with weights
    graph = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(cables):
        weight = weights[i]
        graph[a].append((b, weight))
        graph[b].append((a, weight))
    
    def dijkstra():
        dist = [float('inf')] * (n + 1)
        parent = [None] * (n + 1)
        dist[1] = 0
        
        pq = [(0, 1)]
        
        while pq:
            d, node = heapq.heappop(pq)
            
            if node == n:
                # Reconstruct path
                path = []
                current = n
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            
            if d > dist[node]:
                continue
            
            for neighbor, weight in graph[node]:
                if dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
                    parent[neighbor] = node
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        
        return None
    
    path = dijkstra()
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"
```

### Variation 2: Message Route with Multiple Paths
**Problem**: Find all shortest paths from source to destination.

**Link**: [CSES Problem Set - Message Route Multiple Paths](https://cses.fi/problemset/task/message_route_multiple_paths)

```python
def message_route_multiple_paths(n, m, cables):
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def find_all_shortest_paths():
        # First, find shortest distance
        queue = deque([1])
        visited = [False] * (n + 1)
        dist = [float('inf')] * (n + 1)
        dist[1] = 0
        visited[1] = True
        
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        
        if dist[n] == float('inf'):
            return []
        
        # Find all paths with shortest distance
        def dfs(current, path, remaining_steps):
            if current == n and remaining_steps == 0:
                return [path[:]]
            
            if remaining_steps <= 0:
                return []
            
            paths = []
            for neighbor in graph[current]:
                if neighbor not in path:
                    path.append(neighbor)
                    paths.extend(dfs(neighbor, path, remaining_steps - 1))
                    path.pop()
            
            return paths
        
        return dfs(1, [1], dist[n])
    
    paths = find_all_shortest_paths()
    if not paths:
        return "IMPOSSIBLE"
    
    result = f"{len(paths)}\n"
    for path in paths:
        result += f"{len(path)}\n{' '.join(map(str, path))}\n"
    
    return result.strip()
```

### Variation 3: Message Route with Constraints
**Problem**: Find shortest path with additional constraints.

**Link**: [CSES Problem Set - Message Route Constraints](https://cses.fi/problemset/task/message_route_constraints)

```python
def message_route_constraints(n, m, cables, constraints):
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def bfs_with_constraints():
        queue = deque([(1, [1], set())])  # (node, path, used_constraints)
        visited = set()
        visited.add((1, frozenset()))
        
        while queue:
            node, path, used_constraints = queue.popleft()
            
            if node == n:
                return path
            
            for neighbor in graph[node]:
                # Check constraints
                constraint_key = (node, neighbor)
                if constraint_key in constraints:
                    constraint = constraints[constraint_key]
                    if constraint['type'] == 'max_uses' and used_constraints.count(constraint_key) >= constraint['limit']:
                        continue
                    if constraint['type'] == 'forbidden' and constraint_key in used_constraints:
                        continue
                
                new_used_constraints = used_constraints.copy()
                if constraint_key in constraints:
                    new_used_constraints.add(constraint_key)
                
                state = (neighbor, frozenset(new_used_constraints))
                if state not in visited:
                    visited.add(state)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path, new_used_constraints))
        
        return None
    
    path = bfs_with_constraints()
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"
```

### Related Problems

#### **CSES Problems**
- [Message Route](https://cses.fi/problemset/task/1667) - Basic shortest path problem
- [Labyrinth](https://cses.fi/problemset/task/1193) - Grid pathfinding problems
- [Monsters](https://cses.fi/problemset/task/1194) - Grid algorithms with obstacles

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - BFS traversal
- [Word Ladder](https://leetcode.com/problems/word-ladder/) - Shortest path in word graph
- [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) - Grid shortest path
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) - Shortest path with weights

#### **Problem Categories**
- **Graph Traversal**: BFS algorithms, shortest path, path reconstruction, parent tracking
- **Shortest Path**: Unweighted graphs, pathfinding, route optimization, network algorithms
- **Grid Algorithms**: 2D pathfinding, obstacle avoidance, grid traversal, spatial algorithms
- **Algorithm Design**: BFS algorithms, graph algorithms, pathfinding algorithms, network optimization

## 📚 Learning Points

1. **BFS Algorithm**: Essential for understanding unweighted shortest path
2. **Path Reconstruction**: Key technique for finding actual paths
3. **Parent Tracking**: Important for efficient path reconstruction
4. **Graph Traversal**: Critical for understanding graph algorithms
5. **Shortest Path Properties**: Foundation for many pathfinding problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Message Route problem demonstrates fundamental shortest path concepts for finding optimal routes in unweighted graphs. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n! × n) time complexity using exponential path generation, inefficient for large n values
2. **Basic BFS with Path Tracking**: O(n + m) time complexity using standard BFS algorithm, better approach for shortest path problems
3. **Optimized BFS with Parent Tracking**: O(n + m) time complexity with optimized BFS algorithm, optimal approach for unweighted shortest path

The key insights include understanding BFS properties for shortest path, using parent tracking for efficient path reconstruction, and applying graph traversal techniques for optimal performance. This problem serves as an excellent introduction to shortest path algorithms and BFS-based pathfinding techniques.

