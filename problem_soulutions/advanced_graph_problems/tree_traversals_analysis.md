---
layout: simple
title: "Tree Traversals"
permalink: /cses-analyses/problem_soulutions/advanced_graph_problems/tree_traversals_analysis
---


# Tree Traversals

## Problem Statement
Given a tree with n nodes, find the preorder, inorder, and postorder traversals of the tree.

### Input
The first input line has one integer n: the number of nodes.
Then there are n-1 lines describing the tree edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print three lines: the preorder, inorder, and postorder traversals.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4
1 2
2 3
3 4

Output:
1 2 3 4
4 3 2 1
4 3 2 1
```

## Solution Progression

### Approach 1: DFS Traversals - O(n)
**Description**: Use DFS to perform the three tree traversals.

```python
def tree_traversals_naive(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    # DFS traversal
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Visit children
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Inorder: visit node between children (for binary trees)
        # For general trees, we can visit after all children
        inorder.append(node)
        
        # Postorder: visit node after children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder
```

**Why this is inefficient**: The inorder traversal for general trees is not well-defined, and we need to handle the tree structure properly.

### Improvement 1: Proper Tree Traversals - O(n)
**Description**: Implement proper tree traversals with correct handling of general trees.

```python
def tree_traversals_proper(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Get children (excluding parent)
        children = [child for child in adj[node] if child != parent]
        
        # For inorder in general trees, visit node after first half of children
        if children:
            # Visit first half of children
            for i in range(len(children) // 2):
                dfs(children[i], node)
            
            # Visit node (inorder)
            inorder.append(node)
            
            # Visit second half of children
            for i in range(len(children) // 2, len(children)):
                dfs(children[i], node)
        else:
            # Leaf node
            inorder.append(node)
        
        # Postorder: visit node after all children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder
```

**Why this improvement works**: Properly handles general trees by defining inorder traversal as visiting the node after the first half of children.

## Final Optimal Solution

```python
n = int(input())
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_tree_traversals(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder: visit node before children
        preorder.append(node)
        
        # Get children (excluding parent)
        children = [child for child in adj[node] if child != parent]
        
        # For inorder in general trees, visit node after first half of children
        if children:
            # Visit first half of children
            for i in range(len(children) // 2):
                dfs(children[i], node)
            
            # Visit node (inorder)
            inorder.append(node)
            
            # Visit second half of children
            for i in range(len(children) // 2, len(children)):
                dfs(children[i], node)
        else:
            # Leaf node
            inorder.append(node)
        
        # Postorder: visit node after all children
        postorder.append(node)
    
    # Start from root (assuming node 1 is root)
    dfs(1, -1)
    
    return preorder, inorder, postorder

preorder, inorder, postorder = find_tree_traversals(n, edges)
print(*preorder)
print(*inorder)
print(*postorder)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS Traversals | O(n) | O(n) | Simple tree traversal |
| Proper Traversals | O(n) | O(n) | Correct handling of general trees |

## Key Insights for Other Problems

### 1. **Tree Traversal Properties**
**Principle**: Different traversal orders provide different views of the tree structure.
**Applicable to**: Tree problems, traversal problems, tree reconstruction problems

### 2. **DFS for Tree Traversals**
**Principle**: Use DFS to implement different traversal orders by controlling when to visit nodes.
**Applicable to**: Tree traversal problems, graph traversal problems, tree problems

### 3. **General Tree Handling**
**Principle**: General trees (not binary) require special handling for inorder traversal.
**Applicable to**: Tree problems, traversal problems, tree structure problems

## Notable Techniques

### 1. **DFS Tree Traversal**
```python
def dfs_traversal(adj, root):
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder
        preorder.append(node)
        
        children = [child for child in adj[node] if child != parent]
        
        if children:
            # Visit first half
            for i in range(len(children) // 2):
                dfs(children[i], node)
            
            # Inorder
            inorder.append(node)
            
            # Visit second half
            for i in range(len(children) // 2, len(children)):
                dfs(children[i], node)
        else:
            inorder.append(node)
        
        # Postorder
        postorder.append(node)
    
    dfs(root, -1)
    return preorder, inorder, postorder
```

### 2. **Binary Tree Traversal**
```python
def binary_tree_traversal(root):
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node):
        if not node:
            return
        
        # Preorder: node -> left -> right
        preorder.append(node.val)
        dfs(node.left)
        
        # Inorder: left -> node -> right
        inorder.append(node.val)
        dfs(node.right)
        
        # Postorder: left -> right -> node
        postorder.append(node.val)
    
    dfs(root)
    return preorder, inorder, postorder
```

### 3. **Iterative Traversals**
```python
def iterative_preorder(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Push children in reverse order
        for child in reversed(node.children):
            stack.append(child)
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a tree traversal problem
2. **Choose approach**: Use DFS with proper traversal order control
3. **Initialize data structure**: Build adjacency list from edges
4. **Implement traversals**: Use DFS with different visit timings
5. **Handle general trees**: Define inorder for non-binary trees
6. **Process children**: Visit children in appropriate order
7. **Return result**: Output all three traversal sequences

---

*This analysis shows how to efficiently perform tree traversals using DFS with proper order control.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Tree Traversals with Costs**
**Variation**: Each edge has a cost, find minimum cost traversal paths.
**Approach**: Use weighted tree traversal with cost optimization.
```python
def cost_based_tree_traversals(n, edges, edge_costs):
    # Build weighted adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = edge_costs.get((a, b), 1)
        adj[a].append((b, cost))
        adj[b].append((a, cost))
    
    # Initialize traversal lists and costs
    preorder = []
    inorder = []
    postorder = []
    preorder_cost = 0
    inorder_cost = 0
    postorder_cost = 0
    
    def dfs(node, parent, current_cost):
        nonlocal preorder_cost, inorder_cost, postorder_cost
        
        # Preorder: visit node before children
        preorder.append(node)
        preorder_cost += current_cost
        
        # Get children with costs
        children = [(child, cost) for child, cost in adj[node] if child != parent]
        
        if children:
            # Visit first half of children
            for i in range(len(children) // 2):
                child, cost = children[i]
                dfs(child, node, current_cost + cost)
            
            # Inorder: visit node between children
            inorder.append(node)
            inorder_cost += current_cost
            
            # Visit second half of children
            for i in range(len(children) // 2, len(children)):
                child, cost = children[i]
                dfs(child, node, current_cost + cost)
        else:
            inorder.append(node)
            inorder_cost += current_cost
        
        # Postorder: visit node after children
        postorder.append(node)
        postorder_cost += current_cost
    
    # Start from root
    dfs(1, -1, 0)
    
    return (preorder, inorder, postorder), (preorder_cost, inorder_cost, postorder_cost)
```

#### 2. **Tree Traversals with Constraints**
**Variation**: Limited budget, restricted paths, or specific traversal requirements.
**Approach**: Use constraint satisfaction with traversal optimization.
```python
def constrained_tree_traversals(n, edges, budget, restricted_edges):
    # Build adjacency list excluding restricted edges
    adj = [[] for _ in range(n + 1)]
    for a, b in edges: if (a, b) not in restricted_edges and (b, a) not in 
restricted_edges: adj[a].append(b)
            adj[b].append(a)
    
    # Initialize traversal lists
    preorder = []
    inorder = []
    postorder = []
    current_cost = 0
    
    def dfs(node, parent):
        nonlocal current_cost
        
        if current_cost >= budget:
            return
        
        # Preorder
        preorder.append(node)
        current_cost += 1
        
        # Get available children
        children = [child for child in adj[node] if child != parent]
        
        if children and current_cost < budget:
            # Visit first half
            for i in range(len(children) // 2):
                if current_cost < budget:
                    dfs(children[i], node)
            
            # Inorder
            if current_cost < budget:
                inorder.append(node)
                current_cost += 1
            
            # Visit second half
            for i in range(len(children) // 2, len(children)):
                if current_cost < budget:
                    dfs(children[i], node)
        else:
            inorder.append(node)
            current_cost += 1
        
        # Postorder
        if current_cost < budget:
            postorder.append(node)
            current_cost += 1
    
    # Start from root
    dfs(1, -1)
    
    return preorder, inorder, postorder, current_cost
```

#### 3. **Tree Traversals with Probabilities**
**Variation**: Each node has a probability of being visited, find expected traversal.
**Approach**: Use probabilistic traversal or Monte Carlo simulation.
```python
def probabilistic_tree_traversals(n, edges, node_probabilities, num_samples=1000):
    import random
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Monte Carlo simulation
    preorder_samples = []
    inorder_samples = []
    postorder_samples = []
    
    for _ in range(num_samples):
        # Sample nodes based on probabilities
        visited_nodes = set()
        for i in range(1, n + 1):
            prob = node_probabilities.get(i, 0.5)
            if random.random() < prob:
                visited_nodes.add(i)
        
        # Perform traversals on sampled nodes
        preorder = []
        inorder = []
        postorder = []
        
        def dfs(node, parent):
            if node not in visited_nodes:
                return
            
            # Preorder
            preorder.append(node)
            
            children = [child for child in adj[node] if child != parent and child in visited_nodes]
            
            if children:
                # Visit first half
                for i in range(len(children) // 2):
                    dfs(children[i], node)
                
                # Inorder
                inorder.append(node)
                
                # Visit second half
                for i in range(len(children) // 2, len(children)):
                    dfs(children[i], node)
            else:
                inorder.append(node)
            
            # Postorder
            postorder.append(node)
        
        # Start from root if visited
        if 1 in visited_nodes:
            dfs(1, -1)
        
        preorder_samples.append(preorder)
        inorder_samples.append(inorder)
        postorder_samples.append(postorder)
    
    # Calculate expected traversals
    def average_traversal(samples):
        if not samples:
            return []
        
        max_len = max(len(sample) for sample in samples)
        expected = []
        
        for i in range(max_len):
            values = [sample[i] for sample in samples if i < len(sample)]
            if values:
                expected.append(sum(values) / len(values))
        
        return expected
    
    expected_preorder = average_traversal(preorder_samples)
    expected_inorder = average_traversal(inorder_samples)
    expected_postorder = average_traversal(postorder_samples)
    
    return expected_preorder, expected_inorder, expected_postorder
```

#### 4. **Tree Traversals with Multiple Criteria**
**Variation**: Optimize for multiple objectives (visit count, cost, probability).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_tree_traversals(n, edges, criteria_weights):
    # criteria_weights = {'visit_count': 0.4, 'cost': 0.3, 'probability': 0.3}
    
    def calculate_traversal_score(traversal_attributes):
        return (criteria_weights['visit_count'] * traversal_attributes['visit_count'] + 
                criteria_weights['cost'] * traversal_attributes['cost'] + 
                criteria_weights['probability'] * traversal_attributes['probability'])
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Perform traversals
    preorder = []
    inorder = []
    postorder = []
    
    def dfs(node, parent):
        # Preorder
        preorder.append(node)
        
        children = [child for child in adj[node] if child != parent]
        
        if children:
            # Visit first half
            for i in range(len(children) // 2):
                dfs(children[i], node)
            
            # Inorder
            inorder.append(node)
            
            # Visit second half
            for i in range(len(children) // 2, len(children)):
                dfs(children[i], node)
        else:
            inorder.append(node)
        
        # Postorder
        postorder.append(node)
    
    # Start from root
    dfs(1, -1)
    
    # Calculate traversal attributes
    def get_traversal_attributes(traversal):
        return {
            'visit_count': len(traversal),
            'cost': len(traversal),  # Simplified cost
            'probability': 0.5  # Simplified probability
        }
    
    preorder_attrs = get_traversal_attributes(preorder)
    inorder_attrs = get_traversal_attributes(inorder)
    postorder_attrs = get_traversal_attributes(postorder)
    
    preorder_score = calculate_traversal_score(preorder_attrs)
    inorder_score = calculate_traversal_score(inorder_attrs)
    postorder_score = calculate_traversal_score(postorder_attrs)
    
    return (preorder, inorder, postorder), (preorder_score, inorder_score, postorder_score)
```

#### 5. **Tree Traversals with Dynamic Updates**
**Variation**: Tree structure can be modified dynamically.
**Approach**: Use dynamic tree algorithms or incremental updates.
```python
class DynamicTreeTraversals:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.traversal_cache = None
    
    def add_edge(self, a, b):
        self.adj[a].append(b)
        self.adj[b].append(a)
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        self.adj[a].remove(b)
        self.adj[b].remove(a)
        self.invalidate_cache()
    
    def invalidate_cache(self):
        self.traversal_cache = None
    
    def get_traversals(self):
        if self.traversal_cache is None:
            self.traversal_cache = self.compute_traversals()
        return self.traversal_cache
    
    def compute_traversals(self):
        preorder = []
        inorder = []
        postorder = []
        
        def dfs(node, parent):
            # Preorder
            preorder.append(node)
            
            children = [child for child in self.adj[node] if child != parent]
            
            if children:
                # Visit first half
                for i in range(len(children) // 2):
                    dfs(children[i], node)
                
                # Inorder
                inorder.append(node)
                
                # Visit second half
                for i in range(len(children) // 2, len(children)):
                    dfs(children[i], node)
            else:
                inorder.append(node)
            
            # Postorder
            postorder.append(node)
        
        # Start from root
        dfs(1, -1)
        
        return preorder, inorder, postorder
```

### Related Problems & Concepts

#### 1. **Tree Traversal Problems**
- **Preorder Traversal**: Visit node before children
- **Inorder Traversal**: Visit node between children
- **Postorder Traversal**: Visit node after children
- **Level Order Traversal**: Visit nodes level by level

#### 2. **Tree Structure Problems**
- **Tree Construction**: Build trees from traversals
- **Tree Reconstruction**: Reconstruct tree from traversal data
- **Tree Properties**: Tree height, diameter, size
- **Tree Operations**: Insert, delete, search operations

#### 3. **Graph Traversal Problems**
- **DFS**: Depth-first search on graphs
- **BFS**: Breadth-first search on graphs
- **Graph Traversal**: Traverse graph structures
- **Path Finding**: Find paths in graphs

#### 4. **Algorithm Problems**
- **Recursive Algorithms**: Recursive tree traversal
- **Iterative Algorithms**: Iterative tree traversal
- **Stack/Queue Usage**: Using data structures for traversal
- **Tree Algorithms**: Tree-specific algorithms

#### 5. **Data Structure Problems**
- **Tree Data Structures**: Binary trees, general trees
- **Graph Representations**: Adjacency list, adjacency matrix
- **Stack Operations**: Push, pop, peek operations
- **Queue Operations**: Enqueue, dequeue operations

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

#### 1. **Tree Theory**
- **Tree Properties**: Height, diameter, size, degree
- **Tree Types**: Binary trees, general trees, rooted trees
- **Tree Operations**: Insertion, deletion, searching
- **Tree Analysis**: Analyzing tree structure

#### 2. **Graph Theory**
- **Graph Traversal**: DFS, BFS, and variations
- **Graph Properties**: Connectivity, cycles, paths
- **Graph Algorithms**: Traversal algorithms
- **Graph Analysis**: Analyzing graph structure

#### 3. **Combinatorics**
- **Tree Counting**: Count different tree structures
- **Traversal Counting**: Count different traversal orders
- **Permutation Problems**: Ordering of tree nodes
- **Enumeration**: Listing all possible traversals

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
- **Graph Problems**: Graph traversal, path finding
- **Algorithm Problems**: DFS, BFS, recursive algorithms
- **Data Structure Problems**: Trees, graphs, stacks, queues 