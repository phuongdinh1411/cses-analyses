AI generated content


# CSES Problem Solving Techniques Complete Summary

## Overview
This document summarizes all the key techniques, algorithms, and problem-solving approaches covered in the CSES problem set analyses. Each technique includes identification criteria, when to apply, and key insights.

---

## 📊 Completed Sections
- **Introductory Problems**: 10 problems
- **Dynamic Programming**: 17 problems
- **Graph Algorithms**: 36 problems
- **Tree Algorithms**: 15 problems
- **Range Queries**: 20 problems
- **Sliding Window**: 15 problems
- **Sorting and Searching**: 35 problems
- **String Algorithms**: 14 problems
- **Advanced Graph Problems**: 28 problems
- **Counting Problems**: 19 problems
- **Geometry**: 16 problems
- **Total**: 225 problems with detailed analyses

---

## 🚀 Introductory Problems Techniques

### 1. **Basic Algorithms**
**Identification**: Problems asking for "simple operations", "basic calculations"
**When to Apply**:
- When you need to implement basic mathematical operations
- When you need to simulate simple processes
- When you need to handle basic data structures

**Key Patterns**:
```python
# Collatz Conjecture (3n+1 problem)
def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Missing Number in Array
def find_missing_number(arr, n):
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum
```

**Examples**: Weird Algorithm, Missing Number, Repetitions

### 2. **Mathematical Concepts**
**Identification**: Problems asking for "count", "calculate", "mathematical formulas"
**When to Apply**:
- When you need to count combinations/permutations
- When you need to calculate mathematical series
- When you need to handle large numbers with modular arithmetic

**Key Patterns**:
```python
# Modular Exponentiation
def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

# Factorial with modulo
def factorial_mod(n, mod):
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % mod
    return result
```

**Examples**: Bit Strings, Trailing Zeros, Two Sets

### 3. **Pattern Recognition**
**Identification**: Problems asking for "find pattern", "construct sequence"
**When to Apply**:
- When you need to identify mathematical patterns
- When you need to construct sequences
- When you need to find optimal arrangements

**Key Patterns**:
```python
# Number Spiral Pattern
def generate_spiral(n):
    spiral = [[0] * n for _ in range(n)]
    # Implementation for spiral pattern
    return spiral

# Permutation Generation
def generate_permutations(n):
    from itertools import permutations
    return list(permutations(range(1, n + 1)))
```

**Examples**: Number Spiral, Permutations, Two Knights

---

## 🎯 Dynamic Programming Techniques

### 1. **1D Dynamic Programming**
**Identification**: Problems asking for "optimal", "maximum", "minimum", "ways to do something"
**When to Apply**:
- When you have overlapping subproblems
- When you need to find optimal solutions
- When you can break problem into smaller subproblems

**Key Patterns**:
```python
# Coin Change Problem
def coin_combinations(coins, target):
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, target + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[target]

# Longest Increasing Subsequence
def lis(arr):
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

**Examples**: Dice Combinations, Minimizing Coins, Money Sums

### 2. **2D Dynamic Programming**
**Identification**: Problems with "grid", "matrix", "two variables"
**When to Apply**:
- When you have two-dimensional state space
- When you need to process grids or matrices
- When you have two independent variables

**Key Patterns**:
```python
# Grid Paths
def grid_paths(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '.':
                if i > 0:
                    dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
                if j > 0:
                    dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp[m-1][n-1]
```

**Examples**: Grid Paths, Rectangle Cutting, Edit Distance

### 3. **State Machine DP**
**Identification**: Problems with "states", "transitions", "conditions"
**When to Apply**:
- When you have multiple states to track
- When you need to model state transitions
- When you have conditional logic

**Key Patterns**:
```python
# State Machine Example
def state_machine_dp(n):
    # dp[i][state] represents ways to reach state at position i
    dp = [[0] * 3 for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(n):
        # State transitions based on problem requirements
        dp[i+1][0] = (dp[i][0] + dp[i][1]) % MOD
        dp[i+1][1] = dp[i][0]
        dp[i+1][2] = dp[i][1]
    
    return sum(dp[n]) % MOD
```

**Examples**: Array Description, Counting Towers

---

## 🌐 Graph Algorithms Techniques

### 1. **Graph Traversal**
**Identification**: Problems asking for "connected components", "reachable nodes", "traversal"
**When to Apply**:
- When you need to explore graph structure
- When you need to find connected components
- When you need to visit all reachable nodes

**Key Patterns**:
```python
# DFS Traversal
def dfs(graph, start, visited):
    stack = [start]
    visited.add(start)
    
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

# BFS Traversal
def bfs(graph, start):
    queue = deque([start])
    visited = {start}
    distance = {start: 0}
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    return distance
```

**Examples**: Counting Rooms, Labyrinth, Building Roads

### 2. **Shortest Path Algorithms**
**Identification**: Problems asking for "shortest path", "minimum distance", "route finding"
**When to Apply**:
- When you need to find shortest paths
- When you have weighted edges
- When you need to find minimum distances

**Key Patterns**:
```python
# Dijkstra's Algorithm
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distances[node]:
            continue
            
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

# Bellman-Ford Algorithm
def bellman_ford(edges, n, start):
    distances = [float('inf')] * n
    distances[start] = 0
    
    for _ in range(n - 1):
        for u, v, w in edges:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
    
    return distances
```

**Examples**: Shortest Routes I, Shortest Routes II, High Score

### 3. **Graph Connectivity**
**Identification**: Problems asking for "strongly connected", "components", "connectivity"
**When to Apply**:
- When you need to find connected components
- When you need to check connectivity
- When you need to find bridges or articulation points

**Key Patterns**:
```python
# Kosaraju's Algorithm for SCC
def kosaraju(graph, n):
    # First DFS to get finishing order
    visited = [False] * n
    order = []
    
    def dfs1(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs1(neighbor)
        order.append(node)
    
    for i in range(n):
        if not visited[i]:
            dfs1(i)
    
    # Transpose graph
    transposed = [[] for _ in range(n)]
    for i in range(n):
        for j in graph[i]:
            transposed[j].append(i)
    
    # Second DFS to find SCCs
    visited = [False] * n
    sccs = []
    
    def dfs2(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in transposed[node]:
            if not visited[neighbor]:
                dfs2(neighbor, component)
    
    for node in reversed(order):
        if not visited[node]:
            component = []
            dfs2(node, component)
            sccs.append(component)
    
    return sccs
```

**Examples**: Building Teams, Round Trip, Planets and Kingdoms

### 4. **Maximum Flow**
**Identification**: Problems asking for "maximum flow", "network", "capacity"
**When to Apply**:
- When you have source and sink nodes
- When you have capacity constraints
- When you need to find maximum throughput

**Key Patterns**:
```python
# Ford-Fulkerson Algorithm
def ford_fulkerson(graph, source, sink):
    def dfs(node, flow, visited):
        if node == sink:
            return flow
        
        visited.add(node)
        for neighbor, capacity in graph[node].items():
            if neighbor not in visited and capacity > 0:
                path_flow = dfs(neighbor, min(flow, capacity), visited)
                if path_flow > 0:
                    graph[node][neighbor] -= path_flow
                    graph[neighbor][node] += path_flow
                    return path_flow
        return 0
    
    max_flow = 0
    while True:
        flow = dfs(source, float('inf'), set())
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Examples**: Download Speed, Police Chase, School Dance

---

## 🌳 Tree Algorithms Techniques

### 1. **Tree Traversal**
**Identification**: Problems asking for "tree traversal", "subtree", "ancestor"
**When to Apply**:
- When you need to process tree nodes
- When you need to find subtree properties
- When you need to traverse tree structure

**Key Patterns**:
```python
# DFS Tree Traversal
def dfs_tree(tree, node, parent):
    for child in tree[node]:
        if child != parent:
            dfs_tree(tree, child, node)

# BFS Tree Traversal
def bfs_tree(tree, root):
    queue = deque([root])
    visited = {root}
    
    while queue:
        node = queue.popleft()
        for child in tree[node]:
            if child not in visited:
                visited.add(child)
                queue.append(child)
```

**Examples**: Subordinates, Tree Matching

### 2. **Tree Diameter**
**Identification**: Problems asking for "diameter", "longest path", "tree distance"
**When to Apply**:
- When you need to find longest path in tree
- When you need to find tree diameter
- When you need to find farthest nodes

**Key Patterns**:
```python
# Find Tree Diameter
def tree_diameter(tree, n):
    def dfs(node, parent):
        max_depth = 0
        second_max_depth = 0
        
        for child in tree[node]:
            if child != parent:
                depth = dfs(child, node)
                if depth > max_depth:
                    second_max_depth = max_depth
                    max_depth = depth
                elif depth > second_max_depth:
                    second_max_depth = depth
        
        diameter[0] = max(diameter[0], max_depth + second_max_depth)
        return max_depth + 1
    
    diameter = [0]
    dfs(0, -1)
    return diameter[0]
```

**Examples**: Tree Diameter, Tree Distances I, Tree Distances II

### 3. **Lowest Common Ancestor (LCA)**
**Identification**: Problems asking for "LCA", "ancestor queries", "tree queries"
**When to Apply**:
- When you need to find common ancestors
- When you need to answer tree queries
- When you need to find path between nodes

**Key Patterns**:
```python
# Binary Lifting for LCA
class LCA:
    def __init__(self, tree, n):
        self.n = n
        self.log = 20
        self.parent = [[-1] * self.log for _ in range(n)]
        self.depth = [0] * n
        
        # Build parent table
        self.build_parent_table(tree, 0, -1)
    
    def build_parent_table(self, tree, node, parent):
        self.parent[node][0] = parent
        if parent != -1:
            self.depth[node] = self.depth[parent] + 1
        
        for child in tree[node]:
            if child != parent:
                self.build_parent_table(tree, child, node)
        
        # Fill parent table
        for j in range(1, self.log):
            if self.parent[node][j-1] != -1:
                self.parent[node][j] = self.parent[self.parent[node][j-1]][j-1]
    
    def get_lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        # Bring u to same level as v
        for j in range(self.log-1, -1, -1):
            if self.depth[u] - (1 << j) >= self.depth[v]:
                u = self.parent[u][j]
        
        if u == v:
            return u
        
        # Find LCA
        for j in range(self.log-1, -1, -1):
            if self.parent[u][j] != self.parent[v][j]:
                u = self.parent[u][j]
                v = self.parent[v][j]
        
        return self.parent[u][0]
```

**Examples**: Company Queries II, Distance Queries

### 4. **Tree DP**
**Identification**: Problems asking for "tree optimization", "subtree properties"
**When to Apply**:
- When you need to optimize tree properties
- When you need to process subtrees
- When you have tree-based constraints

**Key Patterns**:
```python
# Tree DP Example
def tree_dp(tree, n):
    def dfs(node, parent):
        # Process children first
        children_results = []
        for child in tree[node]:
            if child != parent:
                children_results.append(dfs(child, node))
        
        # Combine results based on problem requirements
        result = 0
        # Implementation depends on specific problem
        return result
    
    return dfs(0, -1)
```

**Examples**: Tree Matching, Counting Paths, Subtree Queries

---

## 🔍 Range Queries Techniques

### 1. **Prefix Sum**
**Identification**: Problems asking for "sum of range", "static range queries"
**When to Apply**:
- When you need to answer range sum queries efficiently
- When the array is static (no updates)
- When you have many queries on the same array

**Key Pattern**:
```python
def build_prefix_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

**Examples**: Static Range Sum Queries, Forest Queries

### 2. **Binary Indexed Tree (Fenwick Tree)**
**Identification**: Problems with "dynamic range queries", "point updates"
**When to Apply**:
- When you need both range queries and point updates
- When you need to maintain running sums efficiently
- When you need to answer range queries in O(log n)

**Key Implementation**:
```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, idx, val):
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & -idx
    
    def query(self, idx):
        result = 0
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & -idx
        return result
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)
```

**Examples**: Dynamic Range Sum Queries, Salary Queries

### 3. **Segment Tree**
**Identification**: Problems with "range minimum/maximum", "range updates"
**When to Apply**:
- When you need range queries for min/max/sum
- When you need range updates
- When you need complex range operations

**Key Pattern**:
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(arr, 1, 0, self.n - 1)
    
    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build(arr, 2 * node, start, mid)
            self.build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
    
    def query(self, node, start, end, left, right):
        if right < start or left > end:
            return float('inf')
        if left <= start and right >= end:
            return self.tree[node]
        
        mid = (start + end) // 2
        return min(
            self.query(2 * node, start, mid, left, right),
            self.query(2 * node + 1, mid + 1, end, left, right)
        )
```

**Examples**: Dynamic Range Minimum Queries, Subarray Minimum Queries

---

## 🪟 Sliding Window Techniques

### 1. **Fixed Size Window**
**Identification**: Problems asking for "subarray of size k", "window of length k"
**When to Apply**:
- When you need to process fixed-size subarrays
- When you need to maintain a window of constant size
- When you need to slide a window and update statistics

**Key Pattern**:
```python
def fixed_size_window(arr, k):
    n = len(arr)
    if n < k:
        return []
    
    # Initialize first window
    window_sum = sum(arr[:k])
    result = [window_sum]
    
    # Slide window
    for i in range(k, n):
        window_sum = window_sum - arr[i-k] + arr[i]
        result.append(window_sum)
    
    return result
```

**Examples**: Fixed Length Subarray Sum, Sliding Window Sum

### 2. **Variable Size Window**
**Identification**: Problems asking for "longest/shortest subarray", "subarray with property"
**When to Apply**:
- When you need to find optimal subarray size
- When you need to satisfy certain conditions
- When you need to minimize/maximize window size

**Key Pattern**:
```python
def variable_size_window(arr, target):
    n = len(arr)
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0
```

**Examples**: Longest Subarray with Sum, Shortest Subarray with Sum

---

## 🔍 Sorting and Searching Techniques

### 1. **Binary Search**
**Identification**: Problems asking for "find minimum/maximum", "optimization"
**When to Apply**:
- When you need to find optimal value
- When you have monotonic property
- When you need to search in sorted data

**Key Patterns**:
```python
# Binary search on answer
def binary_search_answer(arr, target):
    left, right = 0, max(arr)
    
    while left < right:
        mid = (left + right) // 2
        if can_achieve(arr, mid, target):
            right = mid
        else:
            left = mid + 1
    
    return left

# Binary search on sorted array
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

**Examples**: Factory Machines, Room Allocation, Array Division

### 2. **Greedy Algorithms**
**Identification**: Problems asking for "optimal arrangement", "best strategy"
**When to Apply**:
- When you can make locally optimal choices
- When you need to maximize/minimize some value
- When you have clear ordering criteria

**Key Pattern**:
```python
def greedy_algorithm(items):
    # Sort by some criteria
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    result = []
    for item in items:
        if is_valid_choice(item, result):
            result.append(item)
    
    return result
```

**Examples**: Movie Festival, Tasks and Deadlines, Reading Books

---

## 📝 String Algorithms Techniques

### 1. **KMP Algorithm**
**Identification**: Problems asking for "pattern matching", "string search"
**When to Apply**:
- When you need to find pattern in text
- When you need to find all occurrences
- When you need to build failure function

**Key Implementation**:
```python
def build_lps(pattern):
    n = len(pattern)
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = build_lps(pattern)
    
    i = j = 0
    positions = []
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions
```

**Examples**: String Matching, Pattern Positions

### 2. **Z-Algorithm**
**Identification**: Problems asking for "prefix matching", "border finding"
**When to Apply**:
- When you need to find all prefixes that match suffixes
- When you need to find borders of strings
- When you need to find longest common prefix

**Key Implementation**:
```python
def z_algorithm(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1
    
    return z
```

**Examples**: Finding Borders, Finding Periods

---

## 🌐 Advanced Graph Problems Techniques

### 1. **Matrix Exponentiation**
**Identification**: Problems asking for "walks of length k", "paths of length k"
**When to Apply**:
- When you need to count walks/paths of specific length
- When you have adjacency matrix representation
- When you need to find reachability after k steps

**Key Patterns**:
```python
def matrix_power(matrix, power, mod):
    n = len(matrix)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    while power > 0:
        if power % 2 == 1:
            result = matrix_multiply(result, matrix, mod)
        matrix = matrix_multiply(matrix, matrix, mod)
        power //= 2
    
    return result

def matrix_multiply(a, b, mod):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % mod
    
    return result
```

**Examples**: Fixed Length Walk Queries, Fixed Length Path Queries

### 2. **Strongly Connected Components**
**Identification**: Problems asking for "SCC", "condensation", "component analysis"
**When to Apply**:
- When you need to find strongly connected components
- When you need to analyze graph structure
- When you need to find condensation graph

**Key Patterns**:
```python
# Tarjan's Algorithm for SCC
def tarjan_scc(graph, n):
    index = 0
    indices = [-1] * n
    lowlinks = [-1] * n
    on_stack = [False] * n
    stack = []
    sccs = []
    
    def strongconnect(node):
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack[node] = True
        
        for neighbor in graph[node]:
            if indices[neighbor] == -1:
                strongconnect(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif on_stack[neighbor]:
                lowlinks[node] = min(lowlinks[node], indices[neighbor])
        
        if lowlinks[node] == indices[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)
    
    for i in range(n):
        if indices[i] == -1:
            strongconnect(i)
    
    return sccs
```

**Examples**: New Flight Routes, Strongly Connected Edges

### 3. **2-SAT**
**Identification**: Problems asking for "satisfiability", "logical constraints", "boolean variables"
**When to Apply**:
- When you have boolean variables with constraints
- When you need to find satisfying assignment
- When you have implications between variables

**Key Patterns**:
```python
def solve_2sat(n, clauses):
    # Build implication graph
    graph = [[] for _ in range(2 * n)]
    
    for a, b in clauses:
        # a -> b and ~b -> ~a
        graph[neg(a, n)].append(b)
        graph[neg(b, n)].append(a)
    
    # Find SCCs
    sccs = kosaraju(graph, 2 * n)
    
    # Check for contradiction
    assignment = [False] * n
    for scc in sccs:
        for var in scc:
            if var < n and neg(var, n) in scc:
                return None  # Unsatisfiable
    
    return assignment

def neg(var, n):
    return var + n if var < n else var - n
```

**Examples**: Giant Pizza

---

## 🔢 Counting Problems Techniques

### 1. **Combinatorics**
**Identification**: Problems asking for "count", "number of ways", "combinations"
**When to Apply**:
- When you need to count arrangements
- When you need to count combinations/permutations
- When you need to count valid configurations

**Key Patterns**:
```python
# Combinations with modulo
def combination(n, k, mod):
    if k > n:
        return 0
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % mod
    
    # Precompute inverse factorials
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], mod-2, mod)
    for i in range(n-1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i+1)) % mod
    
    return (fact[n] * inv_fact[k] * inv_fact[n-k]) % mod

# Permutations with constraints
def count_permutations(n, constraints):
    # Implementation depends on specific constraints
    pass
```

**Examples**: Counting Permutations, Counting Sequences

### 2. **Inclusion-Exclusion Principle**
**Identification**: Problems asking for "count excluding", "overlapping counts"
**When to Apply**:
- When you need to count elements in union of sets
- When you need to exclude overlapping cases
- When you have multiple conditions to satisfy

**Key Patterns**:
```python
def inclusion_exclusion(sets):
    n = len(sets)
    total = 0
    
    for mask in range(1, 1 << n):
        intersection = set(range(1000))  # Universal set
        for i in range(n):
            if mask & (1 << i):
                intersection &= sets[i]
        
        if bin(mask).count('1') % 2 == 1:
            total += len(intersection)
        else:
            total -= len(intersection)
    
    return total
```

**Examples**: Grid Completion, Counting Reorders

### 3. **Dynamic Programming for Counting**
**Identification**: Problems asking for "count with constraints", "state-based counting"
**When to Apply**:
- When you need to count with specific constraints
- When you have overlapping subproblems in counting
- When you need to track state for counting

**Key Patterns**:
```python
def count_with_dp(n, constraints):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(n):
        for j in range(n + 1):
            if dp[i][j] > 0:
                # Apply constraints and update next state
                for next_val in range(n + 1):
                    if is_valid_transition(j, next_val, constraints):
                        dp[i + 1][next_val] = (dp[i + 1][next_val] + dp[i][j]) % MOD
    
    return sum(dp[n]) % MOD
```

**Examples**: Grid Paths II, Counting Bishops

---

## 🌐 Geometry Techniques

### 1. **Sweep Line Algorithm**
**Identification**: Problems asking for "line segment intersections", "rectangle union", "geometric events"
**When to Apply**:
- When you need to process geometric events in sorted order
- When you need to find intersections between line segments
- When you need to calculate union area of rectangles

**Key Patterns**:
```python
def sweep_line(events):
    events.sort()  # Sort by x-coordinate or time
    active_set = set()
    
    for event in events:
        if event.type == 'start':
            active_set.add(event.segment)
        else:  # end event
            active_set.remove(event.segment)
        
        # Process active segments
        process_active_segments(active_set)
```

**Examples**: Line Segment Intersection, Area of Rectangles, Intersection Points

### 2. **Divide and Conquer**
**Identification**: Problems asking for "closest pair", "geometric optimization"
**When to Apply**:
- When you need to find closest pair of points
- When you have spatial structure that can be divided
- When you need to optimize geometric properties

**Key Patterns**:
```python
def closest_pair(points):
    n = len(points)
    if n <= 3:
        return brute_force_closest_pair(points)
    
    # Divide
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]
    
    # Conquer
    left_min = closest_pair(left_points)
    right_min = closest_pair(right_points)
    
    # Combine
    min_dist = min(left_min, right_min)
    strip = [p for p in points if abs(p[0] - points[mid][0]) < min_dist]
    
    return min(min_dist, strip_closest_pair(strip))
```

**Examples**: Minimum Euclidean Distance

### 3. **Convex Hull Algorithms**
**Identification**: Problems asking for "convex hull", "boundary", "farthest pair"
**When to Apply**:
- When you need to find the smallest convex polygon containing all points
- When you need to find boundary of a set of points
- When you need to find farthest pair of points

**Key Patterns**:
```python
def convex_hull(points):
    if len(points) < 3:
        return points
    
    # Sort points by x-coordinate
    points = sorted(points)
    
    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    return lower[:-1] + upper[:-1]
```

**Examples**: Convex Hull

### 4. **Geometric Formulas**
**Identification**: Problems asking for "area", "lattice points", "polygon properties"
**When to Apply**:
- When you need to calculate polygon area
- When you need to count lattice points in polygons
- When you need to use geometric theorems

**Key Patterns**:
```python
# Shoelace Formula for polygon area
def polygon_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2

# Pick's Theorem for lattice points
def picks_theorem(area, boundary_points):
    # I = A - B/2 + 1
    # where I = interior lattice points
    #       A = area
    #       B = boundary lattice points
    interior_points = area - boundary_points // 2 + 1
    return interior_points
```

**Examples**: Polygon Area, Polygon Lattice Points

### 5. **Point Location**
**Identification**: Problems asking for "point in polygon", "containment", "spatial queries"
**When to Apply**:
- When you need to test if a point is inside a polygon
- When you need to perform spatial queries
- When you need to determine point containment

**Key Patterns**:
```python
# Ray Casting Algorithm
def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    
    for i in range(n):
        j = (i + 1) % n
        if ((polygon[i][1] > y) != (polygon[j][1] > y) and
            x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) / 
                (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            inside = not inside
    
    return inside
```

**Examples**: Point in Polygon, Point Location Test

### 6. **Distance Problems**
**Identification**: Problems asking for "minimum distance", "maximum distance", "all pairs distance"
**When to Apply**:
- When you need to find minimum/maximum distances between points
- When you need to calculate all pairs distances
- When you need to optimize distance-based problems

**Key Patterns**:
```python
# Euclidean distance
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Manhattan distance
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Cross product for orientation
def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
```

**Examples**: Minimum Euclidean Distance, Maximum Manhattan Distance, All Manhattan Distances

---

## 🎯 Problem-Solving Framework

### 1. **Problem Analysis**
1. **Read carefully**: Understand the problem statement and constraints
2. **Identify type**: Determine if it's a counting, graph, range query, or other type of problem
3. **Look for patterns**: Check if it matches known problem types
4. **Consider constraints**: Use constraints to guide algorithm selection

### 2. **Algorithm Selection**
1. **Brute force first**: Start with a simple solution to understand the problem
2. **Identify inefficiencies**: Look for overlapping subproblems, repeated calculations
3. **Choose appropriate technique**: Based on problem type and constraints
4. **Consider edge cases**: Handle special cases and boundary conditions

### 3. **Implementation Strategy**
1. **Start with pseudocode**: Plan the solution before coding
2. **Implement incrementally**: Build the solution step by step
3. **Test with examples**: Verify with small test cases
4. **Optimize if needed**: Look for further optimizations

### 4. **Complexity Analysis**
1. **Time complexity**: Analyze the main algorithm
2. **Space complexity**: Consider memory usage
3. **Trade-offs**: Understand time vs space trade-offs
4. **Optimization opportunities**: Look for ways to improve

---

## 🔍 Technique Identification Guide

### **Introductory Problems**
- **Keywords**: "basic", "simple", "calculate", "count"
- **Patterns**: Mathematical formulas, simple algorithms, pattern recognition
- **Constraints**: Usually small input sizes, basic operations

### **Dynamic Programming Problems**
- **Keywords**: "optimal", "maximum", "minimum", "ways", "count"
- **Patterns**: Overlapping subproblems, optimal substructure, state transitions
- **Constraints**: Often involve large numbers (modulo 10^9 + 7)

### **Graph Problems**
- **Keywords**: "nodes", "edges", "path", "cycle", "connected", "traversal"
- **Patterns**: Graph traversal, shortest paths, connectivity, flow
- **Constraints**: Graph size, edge weights, directed/undirected

### **Tree Problems**
- **Keywords**: "tree", "parent", "child", "subtree", "ancestor", "diameter"
- **Patterns**: Tree traversal, diameter, distances, LCA, tree DP
- **Constraints**: Tree structure, node relationships

### **Range Query Problems**
- **Keywords**: "range", "query", "sum/min/max", "update"
- **Patterns**: Static vs dynamic, point vs range updates
- **Constraints**: Query count, update frequency

### **Sliding Window Problems**
- **Keywords**: "subarray", "window", "consecutive", "k elements"
- **Patterns**: Fixed vs variable size, optimization problems
- **Constraints**: Array size, window size, target values

### **Sorting and Searching Problems**
- **Keywords**: "sort", "search", "find", "optimal", "minimum/maximum"
- **Patterns**: Binary search, greedy, sweep line
- **Constraints**: Array size, search space, optimization goals

### **String Algorithm Problems**
- **Keywords**: "pattern", "match", "substring", "rotation", "border"
- **Patterns**: Pattern matching, string processing, lexicographic order
- **Constraints**: String length, pattern length, query count

### **Advanced Graph Problems**
- **Keywords**: "walks", "paths", "cycles", "SCC", "2-SAT", "matrix"
- **Patterns**: Matrix exponentiation, SCC algorithms, satisfiability
- **Constraints**: Graph properties, matrix operations

### **Counting Problems**
- **Keywords**: "count", "number of ways", "how many", "combinations"
- **Patterns**: Combinatorics, inclusion-exclusion, DP for counting
- **Constraints**: Often involve large numbers (modulo 10^9 + 7)

### **Geometry Problems**
- **Keywords**: "points", "lines", "polygons", "intersection", "distance", "area"
- **Patterns**: Spatial relationships, geometric properties, coordinate systems
- **Constraints**: Precision requirements, coordinate ranges, geometric constraints

---

## 📚 Key Mathematical Concepts

### **Modular Arithmetic**
- **Fermat's Little Theorem**: a^(p-1) ≡ 1 (mod p) for prime p
- **Modular Inverse**: a^(-1) ≡ a^(p-2) (mod p)
- **Fast Exponentiation**: Binary exponentiation for large powers

### **Combinatorics**
- **Combinations**: C(n,k) = n! / (k! * (n-k)!)
- **Permutations**: P(n,k) = n! / (n-k)!
- **Catalan Numbers**: C(n) = (2n)! / ((n+1)! * n!)

### **Graph Theory**
- **Euler's Formula**: V - E + F = 2 for planar graphs
- **Handshake Lemma**: Sum of degrees = 2 * number of edges
- **Tree Properties**: n nodes, n-1 edges, no cycles

### **String Theory**
- **Border**: A string that is both prefix and suffix
- **Period**: Length of shortest repeating pattern
- **Z-Array**: Longest common prefix with string prefix

---

## 🎯 Interview Preparation Tips

### **Before the Interview**
1. **Practice problems**: Solve problems from each category
2. **Understand trade-offs**: Know when to use each technique
3. **Implement from scratch**: Be able to code algorithms without reference
4. **Analyze complexity**: Always consider time and space complexity

### **During the Interview**
1. **Clarify the problem**: Ask questions to understand requirements
2. **Start simple**: Begin with brute force or simple solution
3. **Optimize incrementally**: Improve the solution step by step
4. **Communicate clearly**: Explain your thought process

### **Common Pitfalls**
1. **Not reading constraints**: Always check input size and limits
2. **Ignoring edge cases**: Handle boundary conditions
3. **Over-engineering**: Don't use complex solutions for simple problems
4. **Not testing**: Always verify with examples

---

## 📈 Progress Tracking

### **Completed Sections**
- ✅ Introductory Problems (10/10)
- ✅ Dynamic Programming (17/17)
- ✅ Graph Algorithms (36/36)
- ✅ Tree Algorithms (15/15)
- ✅ Range Queries (20/20)
- ✅ Sliding Window (15/15)
- ✅ Sorting and Searching (35/35)
- ✅ String Algorithms (14/14)
- ✅ Advanced Graph Problems (28/28)
- ✅ Counting Problems (19/19)
- ✅ Geometry (16/16)
- **Total**: 225 problems with detailed analyses

### **Next Steps**
- Continue with other CSES sections
- Practice implementing each technique
- Focus on problem identification and algorithm selection
- Build intuition for when to apply each technique

---

*This summary provides a comprehensive guide to all techniques covered in the CSES problem set analyses. Use it as a reference for interview preparation and problem-solving practice.* 