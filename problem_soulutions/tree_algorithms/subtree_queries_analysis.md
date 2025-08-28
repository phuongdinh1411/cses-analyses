---
layout: simple
title: "Subtree Queries
permalink: /problem_soulutions/tree_algorithms/subtree_queries_analysis/
---

# Subtree Queries

## Problem Statement
Given a tree with n nodes, each node has a value. Process q queries. Each query is either:
1. Update the value of a node
2. Calculate the sum of values in the subtree of a node

### Input
The first input line has two integers n and q: the number of nodes and the number of queries.
The second line has n integers x1,x2,…,xn: the values of the nodes.
Then there are n-1 lines describing the edges. Each line has two integers a and b: an edge between nodes a and b.
Finally, there are q lines describing the queries. Each line has either:"
- "1 s x": update the value of node s to x
- "2 s": calculate the sum of values in the subtree of node s

### Output
Print the answer to each query of type 2.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9
- 1 ≤ a,b,s ≤ n

### Example
```
Input:
5 3
1 2 3 4 5
1 2
1 3
2 4
2 5
1 2 10
2 1
2 2

Output:
15
10
```

## Solution Progression

### Approach 1: Recalculate for Each Query - O(q × n)
**Description**: For each subtree sum query, traverse the subtree and calculate the sum. For updates, simply modify the value.

```python
def subtree_queries_naive(n, values, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def calculate_subtree_sum(node):
        visited = [False] * (n + 1)
        total = 0
        
        def dfs(current):
            nonlocal total
            visited[current] = True
            total += values[current]
            
            for child in adj[current]:
                if not visited[child]:
                    dfs(child)
        
        dfs(node)
        return total
    
    results = []
    for query in queries:
        if query[0] == 1:  # Update
            s, x = query[1], query[2]
            values[s] = x
        else:  # Subtree sum
            s = query[1]
            sum_val = calculate_subtree_sum(s)
            results.append(sum_val)
    
    return results
```

**Why this is inefficient**: For each subtree sum query, we need to traverse the entire subtree, leading to O(q × n) time complexity.

### Improvement 1: Euler Tour with Segment Tree - O(n + q log n)
**Description**: Use Euler Tour technique with Segment Tree to handle subtree queries efficiently.

```python
def subtree_queries_euler_tour(n, values, edges, queries):
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
        euler_tour.append(values[node])
        
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        out_time[node] = len(euler_tour) - 1
    
    # Build Euler Tour
    dfs(1, -1)
    
    # Build Segment Tree
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = self.tree[2 * index] + self.tree[2 * index + 1]
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = 0
            
            while left <= right:
                if left % 2 == 1:
                    result += self.tree[left]
                    left += 1
                if right % 2 == 0:
                    result += self.tree[right]
                    right -= 1
                left //= 2
                right //= 2
            
            return result
    
    # Initialize Segment Tree
    st = SegmentTree(euler_tour)
    
    results = []
    for query in queries:
        if query[0] == 1:  # Update
            s, x = query[1], query[2]
            # Update in Euler Tour
            st.update(in_time[s], x)
            values[s] = x
        else:  # Subtree sum
            s = query[1]
            # Query range in Euler Tour
            sum_val = st.query(in_time[s], out_time[s])
            results.append(sum_val)
    
    return results
```

**Why this improvement works**: Euler Tour converts subtree queries to range queries, which can be handled efficiently with Segment Tree.

## Final Optimal Solution

```python
n, q = map(int, input().split())
values = [0] + list(map(int, input().split()))

# Read edges
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))

# Read queries
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

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
    euler_tour.append(values[node])
    
    for child in adj[node]:
        if child != parent:
            dfs(child, node)
    
    out_time[node] = len(euler_tour) - 1

# Build Euler Tour
dfs(1, -1)

# Build Segment Tree
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, index, value):
        index += self.size
        self.tree[index] = value
        index //= 2
        while index >= 1:
            self.tree[index] = self.tree[2 * index] + self.tree[2 * index + 1]
            index //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = 0
        
        while left <= right:
            if left % 2 == 1:
                result += self.tree[left]
                left += 1
            if right % 2 == 0:
                result += self.tree[right]
                right -= 1
            left //= 2
            right //= 2
        
        return result

# Initialize Segment Tree
st = SegmentTree(euler_tour)

# Process queries
for query in queries:
    if query[0] == 1:  # Update
        s, x = query[1], query[2]
        # Update in Euler Tour
        st.update(in_time[s], x)
        values[s] = x
    else:  # Subtree sum
        s = query[1]
        # Query range in Euler Tour
        sum_val = st.query(in_time[s], out_time[s])
        print(sum_val)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(n) | Traverse subtree for each query |
| Euler Tour + Segment Tree | O(n + q log n) | O(n) | Convert subtree to range queries |

## Key Insights for Other Problems

### 1. **Subtree Query Problems**
**Principle**: Use Euler Tour to convert subtree queries to range queries.
**Applicable to**: Tree problems, subtree problems, range query problems

### 2. **Euler Tour Technique**
**Principle**: Flatten tree into array to enable range operations.
**Applicable to**: Tree problems, flattening problems, range query applications

### 3. **Segment Tree for Range Queries**
**Principle**: Use Segment Tree to handle range sum queries efficiently.
**Applicable to**: Range problems, query problems, tree-based data structures

## Notable Techniques

### 1. **Euler Tour Construction**
```python
def build_euler_tour(adj, n, values):
    in_time = [0] * (n + 1)
    out_time = [0] * (n + 1)
    euler_tour = []
    
    def dfs(node, parent):
        in_time[node] = len(euler_tour)
        euler_tour.append(values[node])
        
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        out_time[node] = len(euler_tour) - 1
    
    dfs(1, -1)
    return in_time, out_time, euler_tour
```

### 2. **Subtree Range Query**
```python
def subtree_range_query(in_time, out_time, node):
    return in_time[node], out_time[node]
```

### 3. **Segment Tree for Sum**
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, index, value):
        index += self.size
        self.tree[index] = value
        index //= 2
        while index >= 1:
            self.tree[index] = self.tree[2 * index] + self.tree[2 * index + 1]
            index //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = 0
        
        while left <= right:
            if left % 2 == 1:
                result += self.tree[left]
                left += 1
            if right % 2 == 0:
                result += self.tree[right]
                right -= 1
            left //= 2
            right //= 2
        
        return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a subtree query problem with updates
2. **Choose approach**: Use Euler Tour to convert subtree to range queries
3. **Build Euler Tour**: Flatten tree into array with in/out times
4. **Implement Segment Tree**: Handle range sum queries and updates
5. **Process queries**: Convert subtree queries to range queries

---

*This analysis shows how to efficiently handle subtree queries using Euler Tour and Segment Tree technique.* 