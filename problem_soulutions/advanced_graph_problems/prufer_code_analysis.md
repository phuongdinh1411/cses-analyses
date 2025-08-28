---
layout: simple
title: "Prüfer Code
permalink: /problem_soulutions/advanced_graph_problems/prufer_code_analysis/"
---


# Prüfer Code

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

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Prüfer Code with Costs**
**Variation**: Each edge has a cost, find minimum cost tree with given Prüfer code.
**Approach**: Use weighted Prüfer code construction with cost optimization.
```python
def cost_based_prufer_code(n, edges, edge_costs, target_prufer):
    # Build weighted adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = edge_costs.get((a, b), 1)
        adj[a].append((b, cost))
        adj[b].append((a, cost))
    
    # Construct tree from Prüfer code
    tree_edges = tree_from_prufer(target_prufer)
    
    # Calculate total cost
    total_cost = 0
    for a, b in tree_edges:
        # Find minimum cost edge between a and b"
        min_cost = float('inf')
        for neighbor, cost in adj[a]:
            if neighbor == b:
                min_cost = min(min_cost, cost)
        total_cost += min_cost
    
    return total_cost, tree_edges
```

#### 2. **Prüfer Code with Constraints**
**Variation**: Limited budget, restricted edges, or specific tree requirements.
**Approach**: Use constraint satisfaction with Prüfer code construction.
```python
def constrained_prufer_code(n, edges, budget, restricted_edges, target_prufer):
    # Build adjacency list excluding restricted edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        if (a, b) not in restricted_edges and (b, a) not in restricted_edges:
            adj[a].append(b)
            adj[b].append(a)
    
    # Check if target Prüfer code is feasible
    tree_edges = tree_from_prufer(target_prufer)
    
    # Check if all required edges are available
    for a, b in tree_edges:
        if (a, b) in restricted_edges or (b, a) in restricted_edges:
            return None  # Not feasible
    
    # Check budget constraint
    total_cost = len(tree_edges)  # Simplified cost
    if total_cost > budget:
        return None  # Exceeds budget
    
    return tree_edges
```

#### 3. **Prüfer Code with Probabilities**
**Variation**: Each edge has a probability, find expected Prüfer code.
**Approach**: Use probabilistic Prüfer code construction or Monte Carlo simulation.
```python
def probabilistic_prufer_code(n, edges, edge_probabilities, num_samples=1000):
    import random
    
    # Build adjacency list with probabilities
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        prob = edge_probabilities.get((a, b), 0.5)
        adj[a].append((b, prob))
        adj[b].append((a, prob))
    
    # Monte Carlo simulation
    prufer_samples = []
    for _ in range(num_samples):
        # Sample edges based on probabilities
        sampled_edges = []
        for a, b in edges:
            prob = edge_probabilities.get((a, b), 0.5)
            if random.random() < prob:
                sampled_edges.append((a, b))
        
        # Check if sampled edges form a tree
        if len(sampled_edges) == n - 1:
            try:
                prufer = prufer_code_construction(n, sampled_edges)
                prufer_samples.append(prufer)
            except:
                continue
    
    # Calculate expected Prüfer code
    if prufer_samples:
        expected_prufer = []
        for i in range(n - 2):
            values = [prufer[i] for prufer in prufer_samples]
            expected_prufer.append(sum(values) / len(values))
        return expected_prufer
    
    return None
```

#### 4. **Prüfer Code with Multiple Criteria**
**Variation**: Optimize for multiple objectives (cost, probability, tree properties).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_prufer_code(n, edges, criteria_weights, target_prufer):
    # criteria_weights = {'cost': 0.4, 'probability': 0.3, 'diameter': 0.3}
    
    def calculate_tree_score(tree_attributes):
        return (criteria_weights['cost'] * tree_attributes['cost'] + 
                criteria_weights['probability'] * tree_attributes['probability'] + 
                criteria_weights['diameter'] * tree_attributes['diameter'])
    
    # Construct tree from Prüfer code
    tree_edges = tree_from_prufer(target_prufer)
    
    # Calculate tree attributes
    tree_attrs = {
        'cost': len(tree_edges),  # Simplified cost
        'probability': 0.5,  # Simplified probability
        'diameter': calculate_tree_diameter(n, tree_edges)  # Tree diameter
    }
    
    score = calculate_tree_score(tree_attrs)
    return score, tree_edges

def calculate_tree_diameter(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Find diameter using BFS
    def bfs_diameter(start):
        from collections import deque
        queue = deque([(start, 0)])
        visited = [False] * (n + 1)
        visited[start] = True
        max_dist = 0
        farthest_node = start
        
        while queue:
            node, dist = queue.popleft()
            if dist > max_dist:
                max_dist = dist
                farthest_node = node
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, dist + 1))
        
        return farthest_node, max_dist
    
    # Find diameter
    farthest1, _ = bfs_diameter(1)
    farthest2, diameter = bfs_diameter(farthest1)
    return diameter
```

#### 5. **Prüfer Code with Dynamic Updates**
**Variation**: Tree structure can be modified dynamically.
**Approach**: Use dynamic tree algorithms or incremental updates.
```python
class DynamicPruferCode:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.degree = [0] * (n + 1)
        self.prufer_cache = None
    
    def add_edge(self, a, b):
        self.adj[a].append(b)
        self.adj[b].append(a)
        self.degree[a] += 1
        self.degree[b] += 1
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        self.adj[a].remove(b)
        self.adj[b].remove(a)
        self.degree[a] -= 1
        self.degree[b] -= 1
        self.invalidate_cache()
    
    def invalidate_cache(self):
        self.prufer_cache = None
    
    def get_prufer_code(self):
        if self.prufer_cache is None:
            self.prufer_cache = self.compute_prufer_code()
        return self.prufer_cache
    
    def compute_prufer_code(self):
        import heapq
        
        # Initialize leaves
        leaves = []
        for i in range(1, self.n + 1):
            if self.degree[i] == 1:
                heapq.heappush(leaves, i)
        
        # Construct Prüfer code
        prufer = []
        remaining = set(range(1, self.n + 1))
        
        for _ in range(self.n - 2):
            leaf = heapq.heappop(leaves)
            neighbor = next(n for n in self.adj[leaf] if n in remaining)
            
            prufer.append(neighbor)
            remaining.remove(leaf)
            self.degree[leaf] -= 1
            self.degree[neighbor] -= 1
            
            if self.degree[neighbor] == 1:
                heapq.heappush(leaves, neighbor)
        
        return prufer
```

### Related Problems & Concepts

#### 1. **Tree Encoding Problems**
- **Prüfer Code**: Unique tree representation
- **Tree Reconstruction**: Build tree from encoding
- **Tree Isomorphism**: Check if trees are isomorphic
- **Tree Enumeration**: Count different trees

#### 2. **Graph Theory Problems**
- **Tree Properties**: Unique paths, leaf nodes, internal nodes
- **Tree Traversal**: Navigate tree structure
- **Tree Construction**: Build trees with specific properties
- **Tree Algorithms**: BFS, DFS, diameter calculation

#### 3. **Combinatorics Problems**
- **Tree Counting**: Count labeled/unlabeled trees
- **Permutation Problems**: Ordering of tree nodes
- **Combination Problems**: Selecting tree edges
- **Enumeration Problems**: Listing all possible trees

#### 4. **Algorithm Problems**
- **Priority Queue**: Efficient minimum element selection
- **Heap Operations**: Insert, delete, extract minimum
- **Tree Algorithms**: Tree construction, traversal
- **Graph Algorithms**: Graph representation, manipulation

#### 5. **Data Structure Problems**
- **Tree Data Structures**: Binary trees, general trees
- **Graph Representations**: Adjacency list, adjacency matrix
- **Priority Queues**: Heap implementation
- **Set Operations**: Efficient set manipulation

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large trees
- **Edge Cases**: Robust tree operations

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient tree traversal
- **Sliding Window**: Optimal subtree problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Graph Theory**
- **Tree Properties**: Unique paths, leaf nodes, internal nodes
- **Tree Algorithms**: BFS, DFS, diameter calculation
- **Tree Enumeration**: Counting different trees
- **Tree Isomorphism**: Checking tree equivalence

#### 2. **Combinatorics**
- **Tree Counting**: Cayley's formula, labeled trees
- **Permutation Theory**: Ordering and arrangements
- **Enumeration**: Systematic listing of objects
- **Bijection**: One-to-one correspondences

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special tree cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime trees

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Tree and graph problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Tree Problems**: Tree traversal, tree construction
- **Graph Problems**: Graph representation, graph algorithms
- **Combinatorics Problems**: Tree counting, enumeration
- **Algorithm Problems**: Priority queues, heaps 