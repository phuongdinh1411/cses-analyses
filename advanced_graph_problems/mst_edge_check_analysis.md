# CSES MST Edge Check - Problem Analysis

## Problem Statement
Given a weighted undirected graph with n nodes and m edges, for each edge determine if it belongs to the minimum spanning tree (MST).

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has three integers a, b, and c: there is an edge between nodes a and b with weight c.

### Output
For each edge, print "YES" if it belongs to the MST, or "NO" otherwise.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2*10^5
- 1 ≤ a,b ≤ n
- 1 ≤ c ≤ 10^9

### Example
```
Input:
4 5
1 2 1
2 3 2
3 4 3
1 3 4
2 4 5

Output:
YES
YES
YES
NO
NO
```

## Solution Progression

### Approach 1: Kruskal's Algorithm with Edge Tracking - O(m log m + m α(n))
**Description**: Use Kruskal's algorithm to find the MST and track which edges are included.

```python
def mst_edge_check_naive(n, m, edges):
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x[2])
    
    # Union-Find data structure
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True
    
    # Find MST edges
    mst_edges = set()
    for a, b, c in sorted_edges:
        if union(a, b):
            mst_edges.add((a, b, c))
    
    # Check each edge
    result = []
    for edge in edges:
        if edge in mst_edges:
            result.append("YES")
        else:
            result.append("NO")
    
    return result
```

**Why this is inefficient**: This approach works but doesn't handle multiple edges with the same weight correctly.

### Improvement 1: Kruskal's with Edge Indexing - O(m log m + m α(n))
**Description**: Use Kruskal's algorithm with proper edge indexing to handle duplicates.

```python
def mst_edge_check_improved(n, m, edges):
    # Add indices to edges
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    sorted_edges = sorted(indexed_edges, key=lambda x: x[3])
    
    # Union-Find data structure
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True
    
    # Find MST edges
    mst_edge_indices = set()
    for idx, a, b, c in sorted_edges:
        if union(a, b):
            mst_edge_indices.add(idx)
    
    # Check each edge
    result = []
    for i in range(m):
        if i in mst_edge_indices:
            result.append("YES")
        else:
            result.append("NO")
    
    return result
```

**Why this improvement works**: Proper edge indexing handles multiple edges with the same weight correctly.

### Approach 2: Optimized MST Edge Check - O(m log m + m α(n))
**Description**: Use Kruskal's algorithm with optimized implementation.

```python
def mst_edge_check_optimal(n, m, edges):
    # Add indices to edges
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    sorted_edges = sorted(indexed_edges, key=lambda x: x[3])
    
    # Union-Find data structure
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True
    
    # Find MST edges
    mst_edge_indices = set()
    edges_added = 0
    
    for idx, a, b, c in sorted_edges:
        if edges_added == n - 1:  # MST is complete
            break
        if union(a, b):
            mst_edge_indices.add(idx)
            edges_added += 1
    
    # Check each edge
    result = []
    for i in range(m):
        if i in mst_edge_indices:
            result.append("YES")
        else:
            result.append("NO")
    
    return result
```

**Why this improvement works**: Early termination when MST is complete improves efficiency.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

def check_mst_edges(n, m, edges):
    # Add indices to edges
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    sorted_edges = sorted(indexed_edges, key=lambda x: x[3])
    
    # Union-Find data structure
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True
    
    # Find MST edges
    mst_edge_indices = set()
    edges_added = 0
    
    for idx, a, b, c in sorted_edges:
        if edges_added == n - 1:  # MST is complete
            break
        if union(a, b):
            mst_edge_indices.add(idx)
            edges_added += 1
    
    # Check each edge
    result = []
    for i in range(m):
        if i in mst_edge_indices:
            result.append("YES")
        else:
            result.append("NO")
    
    return result

result = check_mst_edges(n, m, edges)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Kruskal's with Edge Tracking | O(m log m + m α(n)) | O(n + m) | Basic MST construction |
| Kruskal's with Edge Indexing | O(m log m + m α(n)) | O(n + m) | Proper edge handling |
| Optimized MST Edge Check | O(m log m + m α(n)) | O(n + m) | Early termination |

## Key Insights for Other Problems

### 1. **MST Edge Identification**
**Principle**: An edge belongs to the MST if it's included when running Kruskal's algorithm.
**Applicable to**: MST problems, graph connectivity problems, edge analysis problems

### 2. **Union-Find Data Structure**
**Principle**: Union-Find efficiently tracks connected components during MST construction.
**Applicable to**: Graph connectivity problems, MST algorithms, component tracking problems

### 3. **Edge Weight Sorting**
**Principle**: Kruskal's algorithm processes edges in ascending order of weight.
**Applicable to**: MST problems, greedy algorithms, sorting-based graph problems

## Notable Techniques

### 1. **Union-Find Implementation**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

### 2. **Kruskal's Algorithm**
```python
def kruskal_mst(n, edges):
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x[2])
    
    # Union-Find
    uf = UnionFind(n)
    mst_edges = []
    
    for a, b, c in sorted_edges:
        if uf.union(a, b):
            mst_edges.append((a, b, c))
    
    return mst_edges
```

### 3. **MST Edge Checking**
```python
def check_mst_edges(n, edges):
    # Add indices
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort by weight
    sorted_edges = sorted(indexed_edges, key=lambda x: x[3])
    
    # Kruskal's algorithm
    uf = UnionFind(n)
    mst_indices = set()
    
    for idx, a, b, c in sorted_edges:
        if uf.union(a, b):
            mst_indices.add(idx)
    
    return mst_indices
```

## Problem-Solving Framework

1. **Identify problem type**: This is an MST edge identification problem
2. **Choose approach**: Use Kruskal's algorithm with edge indexing
3. **Initialize data structures**: Set up Union-Find and edge indexing
4. **Sort edges**: Sort edges by weight for Kruskal's algorithm
5. **Run Kruskal's**: Build MST and track included edges
6. **Check edges**: Determine which edges belong to MST
7. **Return result**: Output YES/NO for each edge

---

*This analysis shows how to efficiently determine which edges belong to the minimum spanning tree using Kruskal's algorithm.* 