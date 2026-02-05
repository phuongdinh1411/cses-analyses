---
layout: simple
title: "Advanced Algorithms"
permalink: /quick_reference/advanced_algorithms
---


# Advanced Algorithms Reference

## 🎯 Advanced Dynamic Programming

### 🔢 State Compression DP
**When to use**: When state space is large but can be compressed
**Technique**: Use bitmasks or other compact representations

```python
# Example: Traveling Salesman Problem
def tsp_dp(graph):
    n = len(graph)
    dp = [[float('inf')] * (1 << n) for _ in range(n)]
    dp[0][1] = 0  # Start at city 0
    
    for mask in range(1 << n):
        for curr in range(n):
            if not (mask & (1 << curr)):
                continue
            for next_city in range(n):
                if mask & (1 << next_city):
                    continue
                new_mask = mask | (1 << next_city)
                dp[next_city][new_mask] = min(
                    dp[next_city][new_mask],
                    dp[curr][mask] + graph[curr][next_city]
                )
    
    return min(dp[i][(1 << n) - 1] + graph[i][0] for i in range(1, n))
```

### 🎯 Digit DP
**When to use**: Problems involving digit manipulation or counting
**Technique**: DP on digits with state tracking

```python
# Example: Count numbers with digit sum = target
def digit_dp(n, target):
    digits = list(map(int, str(n)))
    
    def solve(pos, tight, sum_so_far, dp):
        if pos == len(digits):
            return 1 if sum_so_far == target else 0
        
        state = (pos, tight, sum_so_far)
        if state in dp:
            return dp[state]
        
        limit = digits[pos] if tight else 9
        result = 0
        
        for d in range(limit + 1):
            new_tight = tight and (d == limit)
            new_sum = sum_so_far + d
            if new_sum <= target:
                result += solve(pos + 1, new_tight, new_sum, dp)
        
        dp[state] = result
        return result
    
    return solve(0, True, 0, {})
```

### 🎯 Convex Hull Trick
**When to use**: Optimization problems with linear functions
**Technique**: Maintain convex hull of lines for efficient queries

```python
# Example: Optimizing linear functions
class ConvexHullTrick:
    def __init__(self):
        self.lines = []  # (slope, intercept)
    
    def add_line(self, slope, intercept):
        while len(self.lines) >= 2:
            m1, b1 = self.lines[-2]
            m2, b2 = self.lines[-1]
            m3, b3 = slope, intercept
            
            # Check if line 3 is better than line 2
            if (b3 - b1) * (m2 - m1) <= (b2 - b1) * (m3 - m1):
                self.lines.pop()
            else:
                break
        
        self.lines.append((slope, intercept))
    
    def query(self, x):
        # Binary search for best line
        left, right = 0, len(self.lines) - 1
        while left < right:
            mid = (left + right) // 2
            if self.get_value(mid, x) < self.get_value(mid + 1, x):
                left = mid + 1
            else:
                right = mid
        
        return self.get_value(left, x)
    
    def get_value(self, idx, x):
        m, b = self.lines[idx]
        return m * x + b
```

## 🌐 Advanced Graph Algorithms

### 🔄 Heavy-Light Decomposition
**When to use**: Tree queries and updates on paths
**Technique**: Decompose tree into heavy chains

```python
class HeavyLightDecomposition:
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.size = [0] * n
        self.depth = [0] * n
        self.parent = [-1] * n
        self.chain_head = [0] * n
        self.chain_id = [0] * n
        self.pos = [0] * n
        self.chain_size = [0] * n
        self.chain_count = 0
        self.pos_count = 0
        
        self.dfs_size(0, -1)
        self.decompose(0, -1)
    
    def dfs_size(self, u, p):
        self.parent[u] = p
        self.size[u] = 1
        
        for v in self.tree[u]:
            if v != p:
                self.depth[v] = self.depth[u] + 1
                self.dfs_size(v, u)
                self.size[u] += self.size[v]
    
    def decompose(self, u, p):
        self.chain_id[u] = self.chain_count
        self.pos[u] = self.pos_count
        self.pos_count += 1
        
        if self.chain_size[self.chain_count] == 0:
            self.chain_head[self.chain_count] = u
        
        self.chain_size[self.chain_count] += 1
        
        # Find heavy child
        heavy_child = -1
        max_size = 0
        for v in self.tree[u]:
            if v != p and self.size[v] > max_size:
                max_size = self.size[v]
                heavy_child = v
        
        # Continue heavy chain
        if heavy_child != -1:
            self.decompose(heavy_child, u)
        
        # Start new chains for light children
        for v in self.tree[u]:
            if v != p and v != heavy_child:
                self.chain_count += 1
                self.decompose(v, u)
    
    def lca(self, u, v):
        while self.chain_id[u] != self.chain_id[v]:
            if self.depth[self.chain_head[self.chain_id[u]]] < self.depth[self.chain_head[self.chain_id[v]]]:
                u, v = v, u
            u = self.parent[self.chain_head[self.chain_id[u]]]
        
        return u if self.depth[u] < self.depth[v] else v
```

### 🔄 Link-Cut Trees
**When to use**: Dynamic tree operations
**Technique**: Self-balancing binary search trees

```python
class LinkCutTree:
    def __init__(self, n):
        self.n = n
        self.parent = [-1] * n
        self.left = [-1] * n
        self.right = [-1] * n
        self.flip = [False] * n
        self.size = [1] * n
    
    def access(self, v):
        self.splay(v)
        if self.right[v] != -1:
            self.parent[self.right[v]] = -1
            self.right[v] = -1
            self.update_size(v)
        
        while self.parent[v] != -1:
            w = self.parent[v]
            self.splay(w)
            if self.right[w] != -1:
                self.parent[self.right[w]] = -1
            self.right[w] = v
            self.parent[v] = w
            self.update_size(w)
            v = w
        
        self.splay(v)
        return v
    
    def link(self, v, w):
        self.access(v)
        self.access(w)
        self.parent[v] = w
    
    def cut(self, v):
        self.access(v)
        if self.left[v] != -1:
            self.parent[self.left[v]] = -1
            self.left[v] = -1
            self.update_size(v)
    
    def lca(self, v, w):
        self.access(v)
        return self.access(w)
    
    def splay(self, v):
        while self.parent[v] != -1:
            p = self.parent[v]
            if self.parent[p] == -1:
                self.rotate(v)
            else:
                g = self.parent[p]
                if (self.left[g] == p) == (self.left[p] == v):
                    self.rotate(p)
                    self.rotate(v)
                else:
                    self.rotate(v)
                    self.rotate(v)
    
    def rotate(self, v):
        p = self.parent[v]
        g = self.parent[p]
        
        if self.left[p] == v:
            self.left[p] = self.right[v]
            if self.right[v] != -1:
                self.parent[self.right[v]] = p
            self.right[v] = p
        else:
            self.right[p] = self.left[v]
            if self.left[v] != -1:
                self.parent[self.left[v]] = p
            self.left[v] = p
        
        self.parent[p] = v
        self.parent[v] = g
        
        if g != -1:
            if self.left[g] == p:
                self.left[g] = v
            else:
                self.right[g] = v
        
        self.update_size(p)
        self.update_size(v)
    
    def update_size(self, v):
        self.size[v] = 1
        if self.left[v] != -1:
            self.size[v] += self.size[self.left[v]]
        if self.right[v] != -1:
            self.size[v] += self.size[self.right[v]]
```

## 🔢 Advanced Data Structures

### 📊 Persistent Segment Trees
**When to use**: Need to query historical versions
**Technique**: Create new nodes for updates

```python
class PersistentSegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.versions = []
        self.next_node = 0
        self.nodes = []
        
        # Create initial version
        self.versions.append(self.build(0, self.n - 1, arr))
    
    def build(self, start, end, arr):
        if start == end:
            node = self.create_node(arr[start])
            return node
        
        mid = (start + end) // 2
        left = self.build(start, mid, arr)
        right = self.build(mid + 1, end, arr)
        
        node = self.create_node(left.val + right.val)
        node.left = left
        node.right = right
        return node
    
    def create_node(self, val):
        node = Node(val)
        self.nodes.append(node)
        return node
    
    def update(self, version, pos, val):
        new_root = self.update_node(self.versions[version], 0, self.n - 1, pos, val)
        self.versions.append(new_root)
        return len(self.versions) - 1
    
    def update_node(self, node, start, end, pos, val):
        if start == end:
            new_node = self.create_node(val)
            return new_node
        
        mid = (start + end) // 2
        new_node = self.create_node(node.val)
        
        if pos <= mid:
            new_node.left = self.update_node(node.left, start, mid, pos, val)
            new_node.right = node.right
        else:
            new_node.left = node.left
            new_node.right = self.update_node(node.right, mid + 1, end, pos, val)
        
        new_node.val = new_node.left.val + new_node.right.val
        return new_node
    
    def query(self, version, left, right):
        return self.query_node(self.versions[version], 0, self.n - 1, left, right)
    
    def query_node(self, node, start, end, left, right):
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return node.val
        
        mid = (start + end) // 2
        return (self.query_node(node.left, start, mid, left, right) +
                self.query_node(node.right, mid + 1, end, left, right))

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

### 📊 Sparse Table (2D)
**When to use**: 2D range queries
**Technique**: Precompute for all powers of 2

```python
class SparseTable2D:
    def __init__(self, matrix):
        self.n = len(matrix)
        self.m = len(matrix[0])
        self.log_n = self.log2(self.n)
        self.log_m = self.log2(self.m)
        
        # dp[i][j][k][l] = min/max of rectangle from (i,j) to (i+2^k-1, j+2^l-1)
        self.dp = [[[[0 for _ in range(self.log_m + 1)] 
                    for _ in range(self.log_n + 1)] 
                    for _ in range(self.m)] 
                    for _ in range(self.n)]
        
        # Initialize
        for i in range(self.n):
            for j in range(self.m):
                self.dp[i][j][0][0] = matrix[i][j]
        
        # Build sparse table
        for k in range(1, self.log_n + 1):
            for i in range(self.n - (1 << k) + 1):
                for j in range(self.m):
                    self.dp[i][j][k][0] = min(
                        self.dp[i][j][k-1][0],
                        self.dp[i + (1 << (k-1))][j][k-1][0]
                    )
        
        for l in range(1, self.log_m + 1):
            for i in range(self.n):
                for j in range(self.m - (1 << l) + 1):
                    self.dp[i][j][0][l] = min(
                        self.dp[i][j][0][l-1],
                        self.dp[i][j + (1 << (l-1))][0][l-1]
                    )
        
        for k in range(1, self.log_n + 1):
            for l in range(1, self.log_m + 1):
                for i in range(self.n - (1 << k) + 1):
                    for j in range(self.m - (1 << l) + 1):
                        self.dp[i][j][k][l] = min(
                            self.dp[i][j][k-1][l-1],
                            self.dp[i + (1 << (k-1))][j][l-1],
                            self.dp[i][j + (1 << (l-1))][k-1],
                            self.dp[i + (1 << (k-1))][j + (1 << (l-1))][k-1]
                        )
    
    def log2(self, x):
        return 0 if x <= 1 else 1 + self.log2(x // 2)
    
    def query(self, x1, y1, x2, y2):
        k = self.log2(x2 - x1 + 1)
        l = self.log2(y2 - y1 + 1)
        
        return min(
            self.dp[x1][y1][k][l],
            self.dp[x2 - (1 << k) + 1][y1][k][l],
            self.dp[x1][y2 - (1 << l) + 1][k][l],
            self.dp[x2 - (1 << k) + 1][y2 - (1 << l) + 1][k][l]
        )
```

## 🎯 Advanced Optimization Techniques

### 🔄 Meet in the Middle
**When to use**: Problems with exponential complexity
**Technique**: Split problem into two halves

```python
# Example: Subset sum with large n
def meet_in_middle_subset_sum(arr, target):
    n = len(arr)
    mid = n // 2
    
    # Generate all subsets of first half
    left_sums = set()
    for mask in range(1 << mid):
        total = sum(arr[i] for i in range(mid) if mask & (1 << i))
        left_sums.add(total)
    
    # Check second half
    for mask in range(1 << (n - mid)):
        total = sum(arr[i + mid] for i in range(n - mid) if mask & (1 << i))
        if target - total in left_sums:
            return True
    
    return False
```

### 🔄 Parallel Binary Search
**When to use**: Multiple queries with monotonic answers
**Technique**: Process all queries simultaneously

```python
# Example: Find k-th smallest element in range
def parallel_binary_search(queries, arr):
    n = len(arr)
    q = len(queries)
    
    # Sort queries by their target k
    sorted_queries = sorted(enumerate(queries), key=lambda x: x[1][2])
    
    # Binary search on answer
    left, right = 0, n - 1
    answers = [0] * q
    
    while left <= right:
        mid = (left + right) // 2
        
        # Count elements <= mid for each query
        counts = [0] * q
        for i, (query_idx, (l, r, k)) in enumerate(sorted_queries):
            # Count elements <= arr[mid] in range [l, r]
            count = sum(1 for j in range(l, r + 1) if arr[j] <= arr[mid])
            counts[i] = count
        
        # Update answers based on counts
        for i, (query_idx, (l, r, k)) in enumerate(sorted_queries):
            if counts[i] >= k:
                answers[query_idx] = arr[mid]
                right = mid - 1
            else:
                left = mid + 1
    
    return answers
```

### 🔄 Mo's Algorithm with Updates
**When to use**: Range queries with point updates
**Technique**: Handle updates in query order

```python
class MoWithUpdates:
    def __init__(self, arr):
        self.arr = arr.copy()
        self.n = len(arr)
        self.block_size = int(self.n ** (2/3))
        self.queries = []
        self.updates = []
    
    def add_query(self, l, r, t):
        self.queries.append((l, r, t, len(self.queries)))
    
    def add_update(self, pos, val):
        self.updates.append((pos, val))
    
    def solve(self):
        # Sort queries by (block_l, block_r, time)
        self.queries.sort(key=lambda q: (
            q[0] // self.block_size,
            q[1] // self.block_size,
            q[2]
        ))
        
        curr_l, curr_r, curr_t = 0, -1, -1
        answers = [0] * len(self.queries)
        freq = [0] * (max(self.arr) + 1)
        distinct = 0
        
        for l, r, t, idx in self.queries:
            # Apply updates
            while curr_t < t:
                curr_t += 1
                pos, val = self.updates[curr_t]
                old_val = self.arr[pos]
                
                # Remove old value
                freq[old_val] -= 1
                if freq[old_val] == 0:
                    distinct -= 1
                
                # Add new value
                freq[val] += 1
                if freq[val] == 1:
                    distinct += 1
                
                self.arr[pos] = val
            
            # Revert updates
            while curr_t > t:
                pos, val = self.updates[curr_t]
                new_val = self.arr[pos]
                
                # Remove new value
                freq[new_val] -= 1
                if freq[new_val] == 0:
                    distinct -= 1
                
                # Add old value
                freq[val] += 1
                if freq[val] == 1:
                    distinct += 1
                
                self.arr[pos] = val
                curr_t -= 1
            
            # Move pointers
            while curr_l > l:
                curr_l -= 1
                freq[self.arr[curr_l]] += 1
                if freq[self.arr[curr_l]] == 1:
                    distinct += 1
            
            while curr_r < r:
                curr_r += 1
                freq[self.arr[curr_r]] += 1
                if freq[self.arr[curr_r]] == 1:
                    distinct += 1
            
            while curr_l < l:
                freq[self.arr[curr_l]] -= 1
                if freq[self.arr[curr_l]] == 0:
                    distinct -= 1
                curr_l += 1
            
            while curr_r > r:
                freq[self.arr[curr_r]] -= 1
                if freq[self.arr[curr_r]] == 0:
                    distinct -= 1
                curr_r -= 1
            
            answers[idx] = distinct
        
        return answers
```

## 🎯 Advanced Mathematical Techniques

### 🔢 Fast Fourier Transform (FFT)
**When to use**: Polynomial multiplication, convolution
**Technique**: Convert to frequency domain

```python
import math
import cmath

def fft(a, inverse=False):
    n = len(a)
    if n == 1:
        return a
    
    # Split into even and odd
    even = a[::2]
    odd = a[1::2]
    
    # Recursive FFT
    even_fft = fft(even, inverse)
    odd_fft = fft(odd, inverse)
    
    # Combine results
    result = [0] * n
    angle = 2 * math.pi / n
    if inverse:
        angle = -angle
    
    for k in range(n // 2):
        w = cmath.exp(1j * angle * k)
        result[k] = even_fft[k] + w * odd_fft[k]
        result[k + n // 2] = even_fft[k] - w * odd_fft[k]
    
    if inverse:
        result = [x / n for x in result]
    
    return result

def multiply_polynomials(a, b):
    # Pad with zeros
    n = 1
    while n < len(a) + len(b) - 1:
        n *= 2
    
    a_padded = a + [0] * (n - len(a))
    b_padded = b + [0] * (n - len(b))
    
    # FFT
    a_fft = fft(a_padded)
    b_fft = fft(b_padded)
    
    # Multiply in frequency domain
    c_fft = [a_fft[i] * b_fft[i] for i in range(n)]
    
    # Inverse FFT
    c = fft(c_fft, inverse=True)
    
    # Return real parts
    return [round(x.real) for x in c[:len(a) + len(b) - 1]]
```

### 🔢 Chinese Remainder Theorem (CRT)
**When to use**: Modular arithmetic with multiple moduli
**Technique**: Combine solutions from different moduli

```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def chinese_remainder_theorem(remainders, moduli):
    n = len(remainders)
    if n == 0:
        return 0, 1
    
    # Start with first equation
    result = remainders[0]
    mod = moduli[0]
    
    # Combine with each remaining equation
    for i in range(1, n):
        # Solve: result + k * mod ≡ remainders[i] (mod moduli[i])
        # k * mod ≡ remainders[i] - result (mod moduli[i])
        
        diff = (remainders[i] - result) % moduli[i]
        if diff < 0:
            diff += moduli[i]
        
        # Find k such that k * mod ≡ diff (mod moduli[i])
        gcd, x, y = extended_gcd(mod, moduli[i])
        if diff % gcd != 0:
            raise ValueError("No solution exists")
        
        k = (diff // gcd) * x % (moduli[i] // gcd)
        result += k * mod
        mod = mod * (moduli[i] // gcd)
    
    return result, mod
```

## 🚀 Performance Optimization

### ⚡ Fast I/O
```python
import sys
input = sys.stdin.readline
print = sys.stdout.write

# For multiple test cases
def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    # ... solution code ...
    print(f"{result}\n")

t = int(input())
for _ in range(t):
    solve()
```

### ⚡ Memory Optimization
```python
# Use generators for large datasets
def generate_numbers(n):
    for i in range(n):
        yield i

# Use __slots__ for classes with many instances
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Use bytearray for large boolean arrays
visited = bytearray(n)  # More memory efficient than list
```

### ⚡ Algorithm Optimization
```python
# Use built-in functions when possible
max_val = max(arr)  # Faster than manual loop
sum_val = sum(arr)  # Optimized C implementation

# Use list comprehensions
squares = [x*x for x in arr]  # Faster than append in loop

# Use sets for membership testing
if x in my_set:  # O(1) vs O(n) for lists
    pass
```
