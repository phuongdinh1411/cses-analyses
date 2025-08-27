# CSES Prüfer Code - Problem Analysis

## Problem Statement
Given a tree with n nodes labeled from 1 to n, find its Prüfer code. The Prüfer code is a sequence of n-2 integers that uniquely represents a labeled tree.

### Input
The first input line has one integer n: the number of nodes.
Then there are n-1 lines describing the tree edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print the Prüfer code of the tree.

### Constraints
- 2 ≤ n ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4
1 2
2 3
3 4

Output:
2 3
```

## Solution Progression

### Approach 1: Naive Prüfer Code Construction - O(n²)
**Description**: Use the standard algorithm to construct Prüfer code by repeatedly removing leaves.

```python
def prufer_code_naive(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Find degree of each node
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Construct Prüfer code
    prufer = []
    remaining_nodes = set(range(1, n + 1))
    
    for _ in range(n - 2):
        # Find the leaf with smallest label
        leaf = min(node for node in remaining_nodes if degree[node] == 1)
        
        # Find its neighbor
        neighbor = None
        for neighbor_node in adj[leaf]:
            if neighbor_node in remaining_nodes:
                neighbor = neighbor_node
                break
        
        # Add neighbor to Prüfer code
        prufer.append(neighbor)
        
        # Remove leaf and update degrees
        remaining_nodes.remove(leaf)
        degree[leaf] -= 1
        degree[neighbor] -= 1
    
    return prufer
```

**Why this is inefficient**: Finding the minimum leaf takes O(n) time in each iteration, leading to O(n²) total complexity.

### Improvement 1: Efficient Prüfer Code Construction - O(n log n)
**Description**: Use a priority queue to efficiently find the minimum leaf.

```python
def prufer_code_efficient(n, edges):
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Find degree of each node
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Use priority queue for leaves
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heapq.heappush(leaves, i)
    
    # Construct Prüfer code
    prufer = []
    remaining_nodes = set(range(1, n + 1))
    
    for _ in range(n - 2):
        # Get the leaf with smallest label
        leaf = heapq.heappop(leaves)
        
        # Find its neighbor
        neighbor = None
        for neighbor_node in adj[leaf]:
            if neighbor_node in remaining_nodes:
                neighbor = neighbor_node
                break
        
        # Add neighbor to Prüfer code
        prufer.append(neighbor)
        
        # Remove leaf and update degrees
        remaining_nodes.remove(leaf)
        degree[leaf] -= 1
        degree[neighbor] -= 1
        
        # If neighbor becomes a leaf, add it to queue
        if degree[neighbor] == 1:
            heapq.heappush(leaves, neighbor)
    
    return prufer
```

**Why this improvement works**: Using a priority queue reduces the time to find the minimum leaf from O(n) to O(log n) per iteration.

## Final Optimal Solution

```python
import heapq

n = int(input())
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))

def construct_prufer_code(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Find degree of each node
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = len(adj[i])
    
    # Use priority queue for leaves
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heapq.heappush(leaves, i)
    
    # Construct Prüfer code
    prufer = []
    remaining_nodes = set(range(1, n + 1))
    
    for _ in range(n - 2):
        # Get the leaf with smallest label
        leaf = heapq.heappop(leaves)
        
        # Find its neighbor
        neighbor = None
        for neighbor_node in adj[leaf]:
            if neighbor_node in remaining_nodes:
                neighbor = neighbor_node
                break
        
        # Add neighbor to Prüfer code
        prufer.append(neighbor)
        
        # Remove leaf and update degrees
        remaining_nodes.remove(leaf)
        degree[leaf] -= 1
        degree[neighbor] -= 1
        
        # If neighbor becomes a leaf, add it to queue
        if degree[neighbor] == 1:
            heapq.heappush(leaves, neighbor)
    
    return prufer

result = construct_prufer_code(n, edges)
print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Construction | O(n²) | O(n) | Simple but inefficient |
| Priority Queue | O(n log n) | O(n) | Efficient leaf selection |

## Key Insights for Other Problems

### 1. **Prüfer Code Properties**
**Principle**: Prüfer code is a bijection between labeled trees and sequences of n-2 integers.
**Applicable to**: Tree encoding problems, tree isomorphism problems, tree counting problems

### 2. **Priority Queue for Minimum Selection**
**Principle**: Use priority queue to efficiently find and remove minimum elements.
**Applicable to**: Minimum selection problems, greedy algorithms, tree problems

### 3. **Tree Leaf Removal**
**Principle**: Trees can be constructed by iteratively removing leaves and tracking neighbors.
**Applicable to**: Tree construction problems, tree traversal problems, graph problems

## Notable Techniques

### 1. **Prüfer Code Construction**
```python
def prufer_code_construction(n, edges):
    import heapq
    
    # Build adjacency list and degrees
    adj = [[] for _ in range(n + 1)]
    degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        degree[a] += 1
        degree[b] += 1
    
    # Initialize leaves
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heapq.heappush(leaves, i)
    
    # Construct Prüfer code
    prufer = []
    remaining = set(range(1, n + 1))
    
    for _ in range(n - 2):
        leaf = heapq.heappop(leaves)
        neighbor = next(n for n in adj[leaf] if n in remaining)
        
        prufer.append(neighbor)
        remaining.remove(leaf)
        degree[leaf] -= 1
        degree[neighbor] -= 1
        
        if degree[neighbor] == 1:
            heapq.heappush(leaves, neighbor)
    
    return prufer
```

### 2. **Tree from Prüfer Code**
```python
def tree_from_prufer(prufer):
    n = len(prufer) + 2
    degree = [1] * (n + 1)
    
    # Count occurrences in Prüfer code
    for x in prufer:
        degree[x] += 1
    
    # Find leaves
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            leaves.append(i)
    
    # Construct tree
    edges = []
    for x in prufer:
        leaf = min(leaves)
        edges.append((leaf, x))
        leaves.remove(leaf)
        degree[x] -= 1
        if degree[x] == 1:
            leaves.append(x)
    
    # Add last edge
    edges.append((leaves[0], leaves[1]))
    return edges
```

### 3. **Efficient Leaf Management**
```python
def manage_leaves(degree, leaves, node):
    degree[node] -= 1
    if degree[node] == 1:
        heapq.heappush(leaves, node)
    elif degree[node] == 0:
        # Node becomes isolated, remove from leaves if present
        if node in leaves:
            leaves.remove(node)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a tree encoding problem using Prüfer code
2. **Choose approach**: Use priority queue for efficient leaf selection
3. **Initialize data structure**: Build adjacency list and degree array
4. **Find initial leaves**: Add all degree-1 nodes to priority queue
5. **Iterative construction**: Remove minimum leaf and add its neighbor to code
6. **Update degrees**: Decrease degrees and add new leaves to queue
7. **Return result**: Output the Prüfer code sequence

---

*This analysis shows how to efficiently construct Prüfer code using priority queue optimization.* 