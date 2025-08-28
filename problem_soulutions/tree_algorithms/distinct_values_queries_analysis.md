---
layout: simple
title: CSES Distinct Values Queries - Problem Analysis
permalink: /problem_soulutions/tree_algorithms/distinct_values_queries_analysis/
---

# CSES Distinct Values Queries - Problem Analysis

## Problem Statement
Given a tree with n nodes, each node has a color. Process q queries. Each query asks for the number of distinct colors in the subtree of a node.

### Input
The first input line has two integers n and q: the number of nodes and the number of queries.
The second line has n integers c1,c2,…,cn: the colors of the nodes.
Then there are n-1 lines describing the edges. Each line has two integers a and b: an edge between nodes a and b.
Finally, there are q lines describing the queries. Each line has one integer s: the node to query.

### Output
Print the answer to each query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ ci ≤ 10^9
- 1 ≤ a,b,s ≤ n

### Example
```
Input:
5 3
1 2 1 3 2
1 2
1 3
2 4
2 5
1
2
3

Output:
3
2
1
```

## Solution Progression

### Approach 1: Count Distinct Colors for Each Query - O(q × n)
**Description**: For each query, traverse the subtree and count distinct colors.

```python
def distinct_values_queries_naive(n, colors, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def count_distinct_colors(node):
        visited = [False] * (n + 1)
        color_set = set()
        
        def dfs(current):
            visited[current] = True
            color_set.add(colors[current])
            
            for child in adj[current]:
                if not visited[child]:
                    dfs(child)
        
        dfs(node)
        return len(color_set)
    
    results = []
    for query in queries:
        count = count_distinct_colors(query)
        results.append(count)
    
    return results
```

**Why this is inefficient**: For each query, we need to traverse the entire subtree, leading to O(q × n) time complexity.

### Improvement 1: Euler Tour with Mo's Algorithm - O(n√n)
**Description**: Use Euler Tour to flatten the tree and apply Mo's algorithm for range distinct queries.

```python
def distinct_values_queries_mo(n, colors, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Euler Tour arrays
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    euler_tour = []
    
    def dfs(node, parent):
        in_time[node] = len(euler_tour)
        euler_tour.append(colors[node])
        
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        out_time[node] = len(euler_tour) - 1
    
    # Build Euler Tour
    dfs(1, -1)
    
    # Mo's algorithm for range distinct queries
    class MoAlgorithm:
        def __init__(self, arr):
            self.arr = arr
            self.n = len(arr)
            self.block_size = int(self.n ** 0.5)
            self.freq = {}
            self.distinct_count = 0
        
        def add(self, index):
            color = self.arr[index]
            if color not in self.freq:
                self.freq[color] = 0
            self.freq[color] += 1
            if self.freq[color] == 1:
                self.distinct_count += 1
        
        def remove(self, index):
            color = self.arr[index]
            self.freq[color] -= 1
            if self.freq[color] == 0:
                self.distinct_count -= 1
        
        def get_distinct_count(self):
            return self.distinct_count
    
    # Process queries using Mo's algorithm
    mo = MoAlgorithm(euler_tour)
    
    # Sort queries by block for Mo's algorithm
    query_blocks = []
    for i, query in enumerate(queries):
        left = in_time[query]
        right = out_time[query]
        block = left // mo.block_size
        query_blocks.append((block, right, left, i))
    
    query_blocks.sort()
    
    # Process queries
    current_left = 0
    current_right = -1
    results = [0] * len(queries)
    
    for block, right, left, query_idx in query_blocks:
        # Move to the query range
        while current_right < right:
            current_right += 1
            mo.add(current_right)
        
        while current_right > right:
            mo.remove(current_right)
            current_right -= 1
        
        while current_left < left:
            mo.remove(current_left)
            current_left += 1
        
        while current_left > left:
            current_left -= 1
            mo.add(current_left)
        
        results[query_idx] = mo.get_distinct_count()
    
    return results
```

**Why this improvement works**: Euler Tour converts subtree queries to range queries, and Mo's algorithm handles range distinct queries efficiently.

## Final Optimal Solution

```python
n, q = map(int, input().split())
colors = [0] + list(map(int, input().split()))

# Read edges
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))

# Read queries
queries = []
for _ in range(q):
    s = int(input())
    queries.append(s)

# Build adjacency list
adj = [[] for _ in range(n + 1)]
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)

# Euler Tour arrays
in_time = [0] * (n + 1)
out_time = [0] * (n + 1)
euler_tour = []

def dfs(node, parent):
    in_time[node] = len(euler_tour)
    euler_tour.append(colors[node])
    
    for child in adj[node]:
        if child != parent:
            dfs(child, node)
    
    out_time[node] = len(euler_tour) - 1

# Build Euler Tour
dfs(1, -1)

# Mo's algorithm for range distinct queries
class MoAlgorithm:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.block_size = int(self.n ** 0.5)
        self.freq = {}
        self.distinct_count = 0
    
    def add(self, index):
        color = self.arr[index]
        if color not in self.freq:
            self.freq[color] = 0
        self.freq[color] += 1
        if self.freq[color] == 1:
            self.distinct_count += 1
    
    def remove(self, index):
        color = self.arr[index]
        self.freq[color] -= 1
        if self.freq[color] == 0:
            self.distinct_count -= 1
    
    def get_distinct_count(self):
        return self.distinct_count

# Process queries using Mo's algorithm
mo = MoAlgorithm(euler_tour)

# Sort queries by block for Mo's algorithm
query_blocks = []
for i, query in enumerate(queries):
    left = in_time[query]
    right = out_time[query]
    block = left // mo.block_size
    query_blocks.append((block, right, left, i))

query_blocks.sort()

# Process queries
current_left = 0
current_right = -1
results = [0] * len(queries)

for block, right, left, query_idx in query_blocks:
    # Move to the query range
    while current_right < right:
        current_right += 1
        mo.add(current_right)
    
    while current_right > right:
        mo.remove(current_right)
        current_right -= 1
    
    while current_left < left:
        mo.remove(current_left)
        current_left += 1
    
    while current_left > left:
        current_left -= 1
        mo.add(current_left)
    
    results[query_idx] = mo.get_distinct_count()

# Print results
for result in results:
    print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(n) | Traverse subtree for each query |
| Euler Tour + Mo's Algorithm | O(n√n) | O(n) | Convert subtree to range queries |

## Key Insights for Other Problems

### 1. **Distinct Values Problems**
**Principle**: Use frequency counting to track distinct elements efficiently.
**Applicable to**: Counting problems, distinct element problems, frequency problems

### 2. **Euler Tour for Subtree Queries**
**Principle**: Flatten tree into array to enable range operations.
**Applicable to**: Tree problems, subtree problems, range query applications

### 3. **Mo's Algorithm for Range Queries**
**Principle**: Use Mo's algorithm for offline range distinct queries.
**Applicable to**: Range problems, offline queries, distinct counting problems

## Notable Techniques

### 1. **Euler Tour Construction**
```python
def build_euler_tour(adj, n, colors):
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    euler_tour = []
    
    def dfs(node, parent):
        in_time[node] = len(euler_tour)
        euler_tour.append(colors[node])
        
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        out_time[node] = len(euler_tour) - 1
    
    dfs(1, -1)
    return in_time, out_time, euler_tour
```

### 2. **Mo's Algorithm Implementation**
```python
class MoAlgorithm:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.block_size = int(self.n ** 0.5)
        self.freq = {}
        self.distinct_count = 0
    
    def add(self, index):
        color = self.arr[index]
        if color not in self.freq:
            self.freq[color] = 0
        self.freq[color] += 1
        if self.freq[color] == 1:
            self.distinct_count += 1
    
    def remove(self, index):
        color = self.arr[index]
        self.freq[color] -= 1
        if self.freq[color] == 0:
            self.distinct_count -= 1
    
    def get_distinct_count(self):
        return self.distinct_count
```

### 3. **Subtree to Range Conversion**
```python
def subtree_to_range(in_time, out_time, node):
    return in_time[node], out_time[node]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a distinct values query problem in trees
2. **Choose approach**: Use Euler Tour to convert subtree to range queries
3. **Build Euler Tour**: Flatten tree into array with in/out times
4. **Implement Mo's Algorithm**: Handle range distinct queries efficiently
5. **Process queries**: Convert subtree queries to range queries

---

*This analysis shows how to efficiently count distinct values in subtrees using Euler Tour and Mo's algorithm.* 