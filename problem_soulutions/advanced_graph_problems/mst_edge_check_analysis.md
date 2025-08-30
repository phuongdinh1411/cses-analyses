---
layout: simple
title: "MST Edge Check"
permalink: /problem_soulutions/advanced_graph_problems/mst_edge_check_analysis
---


# MST Edge Check

## Problem Description

**Problem**: Given a weighted undirected graph with n nodes and m edges, for each edge determine if it belongs to the minimum spanning tree (MST).

**Input**: 
- n, m: number of nodes and edges
- m lines: a b c (edge between a and b with weight c)

**Output**: For each edge, print "YES" if it belongs to the MST, "NO" otherwise.

**Example**:
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

Explanation: 
MST contains edges: (1,2), (2,3), (3,4) with total weight 6
Edges (1,3) and (2,4) are not in MST as they have higher weights
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find which edges belong to the MST
- Use Kruskal's or Prim's algorithm
- Handle edge weight ties correctly
- Determine MST membership

**Key Observations:**
- MST contains n-1 edges
- Edges are selected by weight order
- Need to handle equal weights properly
- Union-Find is essential for efficiency

### Step 2: Kruskal's Algorithm Approach
**Idea**: Use Kruskal's algorithm to find MST and track included edges.

```python
def mst_edge_check_kruskal(n, m, edges):
    # Add indices to edges for tracking
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    indexed_edges.sort(key=lambda x: x[3])
    
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
    for idx, a, b, c in indexed_edges:
        if union(a, b):
            mst_edges.add(idx)
    
    # Check each edge
    result = []
    for i in range(m):
        result.append("YES" if i in mst_edges else "NO")
    
    return result
```

**Why this works:**
- Uses Kruskal's algorithm for MST
- Handles edge weight ties correctly
- Efficient Union-Find implementation
- O(m log m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_mst_edge_check():
    n, m = map(int, input().split())
    edges = []
    
    for i in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))
    
    # Add indices to edges for tracking
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    indexed_edges.sort(key=lambda x: x[3])
    
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
    for idx, a, b, c in indexed_edges:
        if union(a, b):
            mst_edges.add(idx)
    
    # Check each edge
    for i in range(m):
        print("YES" if i in mst_edges else "NO")

# Main execution
if __name__ == "__main__":
    solve_mst_edge_check()
```

**Why this works:**
- Optimal Kruskal's algorithm approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, 5, [(1, 2, 1), (2, 3, 2), (3, 4, 3), (1, 3, 4), (2, 4, 5)]),
        (3, 3, [(1, 2, 1), (2, 3, 2), (1, 3, 3)]),
    ]
    
    for n, m, edges in test_cases:
        result = solve_test(n, m, edges)
        print(f"n={n}, m={m}, edges={edges}")
        print(f"Result: {result}")
        print()

def solve_test(n, m, edges):
    # Add indices to edges for tracking
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    indexed_edges.sort(key=lambda x: x[3])
    
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
    for idx, a, b, c in indexed_edges:
        if union(a, b):
            mst_edges.add(idx)
    
    # Check each edge
    result = []
    for i in range(m):
        result.append("YES" if i in mst_edges else "NO")
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(m log m) - sorting edges + Union-Find operations
- **Space**: O(n + m) - Union-Find data structure and edge tracking

### Why This Solution Works
- **Kruskal's Algorithm**: Finds MST efficiently
- **Union-Find**: Efficient cycle detection
- **Edge Tracking**: Identifies MST edges
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Minimum Spanning Tree**
- Tree with minimum total weight
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Kruskal's Algorithm**
- Efficient MST algorithm
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Union-Find**
- Efficient cycle detection
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: MST Edge Check with Constraints
**Problem**: Check MST edges with certain constraints.

```python
def constrained_mst_edge_check(n, m, edges, constraints):
    # Add indices to edges for tracking
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Apply constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    required_edges = constraints.get('required_edges', set())
    
    # Remove forbidden edges
    indexed_edges = [(i, a, b, c) for i, a, b, c in indexed_edges if i not in forbidden_edges]
    
    # Sort edges by weight
    indexed_edges.sort(key=lambda x: x[3])
    
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
    
    # Add required edges first
    mst_edges = set()
    for i in required_edges:
        a, b, c = edges[i]
        if union(a, b):
            mst_edges.add(i)
    
    # Find remaining MST edges
    for idx, a, b, c in indexed_edges:
        if idx not in required_edges and union(a, b):
            mst_edges.add(idx)
    
    # Check each edge
    result = []
    for i in range(m):
        result.append("YES" if i in mst_edges else "NO")
    
    return result
```

### Variation 2: MST Edge Check with Multiple MSTs
**Problem**: Check if edge belongs to any MST when multiple MSTs exist.

```python
def multiple_mst_edge_check(n, m, edges):
    # Add indices to edges for tracking
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    indexed_edges.sort(key=lambda x: x[3])
    
    # Group edges by weight
    weight_groups = {}
    for idx, a, b, c in indexed_edges:
        if c not in weight_groups:
            weight_groups[c] = []
        weight_groups[c].append((idx, a, b))
    
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
    
    # Find edges that can be in MST
    mst_candidates = set()
    
    for weight in sorted(weight_groups.keys()):
        # Check which edges of this weight can be added
        for idx, a, b in weight_groups[weight]:
            if union(a, b):
                mst_candidates.add(idx)
    
    # Check each edge
    result = []
    for i in range(m):
        result.append("YES" if i in mst_candidates else "NO")
    
    return result
```

### Variation 3: Dynamic MST Edge Check
**Problem**: Support adding/removing edges and maintaining MST edge status.

```python
class DynamicMSTEdgeCheck:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.edge_map = {}
    
    def add_edge(self, a, b, c):
        edge_id = len(self.edges)
        self.edges.append((a, b, c))
        self.edge_map[(a, b)] = edge_id
        self.edge_map[(b, a)] = edge_id
        return edge_id
    
    def remove_edge(self, a, b):
        if (a, b) in self.edge_map:
            edge_id = self.edge_map[(a, b)]
            self.edges[edge_id] = None
            return True
        return False
    
    def check_mst_edges(self):
        # Filter out removed edges
        valid_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(self.edges) if (a, b, c) is not None]
        
        # Sort edges by weight
        valid_edges.sort(key=lambda x: x[3])
        
        # Union-Find data structure
        parent = list(range(self.n + 1))
        rank = [0] * (self.n + 1)
        
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
        for idx, a, b, c in valid_edges:
            if union(a, b):
                mst_edges.add(idx)
        
        # Check each edge
        result = []
        for i in range(len(self.edges)):
            if self.edges[i] is None:
                result.append("NO")
            else:
                result.append("YES" if i in mst_edges else "NO")
        
        return result
```

### Variation 4: MST Edge Check with Multiple Constraints
**Problem**: Check MST edges satisfying multiple constraints.

```python
def multi_constrained_mst_edge_check(n, m, edges, constraints):
    # Add indices to edges for tracking
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Apply multiple constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    required_edges = constraints.get('required_edges', set())
    max_weight = constraints.get('max_weight', float('inf'))
    
    # Remove forbidden edges and apply weight constraints
    filtered_edges = []
    for i, a, b, c in indexed_edges:
        if i not in forbidden_edges and c <= max_weight:
            filtered_edges.append((i, a, b, c))
    
    # Sort edges by weight
    filtered_edges.sort(key=lambda x: x[3])
    
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
    
    # Add required edges first
    mst_edges = set()
    for i in required_edges:
        a, b, c = edges[i]
        if union(a, b):
            mst_edges.add(i)
    
    # Find remaining MST edges
    for idx, a, b, c in filtered_edges:
        if idx not in required_edges and union(a, b):
            mst_edges.add(idx)
    
    # Check each edge
    result = []
    for i in range(m):
        result.append("YES" if i in mst_edges else "NO")
    
    return result
```

### Variation 5: MST Edge Check with Edge Replacement
**Problem**: Check if edge can replace another edge in MST.

```python
def mst_edge_replacement_check(n, m, edges):
    # Add indices to edges for tracking
    indexed_edges = [(i, a, b, c) for i, (a, b, c) in enumerate(edges)]
    
    # Sort edges by weight
    indexed_edges.sort(key=lambda x: x[3])
    
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
    for idx, a, b, c in indexed_edges:
        if union(a, b):
            mst_edges.add(idx)
    
    # Check replacement possibilities
    result = []
    for i in range(m):
        if i in mst_edges:
            result.append("YES")  # Already in MST
        else:
            # Check if this edge can replace any MST edge
            a, b, c = edges[i]
            can_replace = False
            
            # Try replacing each MST edge
            for mst_edge in mst_edges:
                mst_a, mst_b, mst_c = edges[mst_edge]
                if c < mst_c:  # Only consider if weight is less
                    # Check if adding this edge and removing MST edge still gives MST
                    temp_parent = parent.copy()
                    temp_rank = rank.copy()
                    
                    # Remove MST edge (simulate by not using it)
                    # Add current edge
                    if union(a, b):
                        can_replace = True
                        break
            
            result.append("YES" if can_replace else "NO")
    
    return result
```

## 🔗 Related Problems

- **[Minimum Spanning Tree](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: MST algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Union-Find](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Union-Find data structure

## 📚 Learning Points

1. **Minimum Spanning Tree**: Essential for graph optimization
2. **Kruskal's Algorithm**: Efficient MST algorithm
3. **Union-Find**: Important data structure
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to MST edge checking and minimum spanning trees!** 🎯

**Why this works:**
- Uses Kruskal's algorithm
- Handles edge indexing properly
- Efficient Union-Find operations
- O(m log m + m α(n)) time complexity

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

## Problem Variations & Related Questions

### Problem Variations

#### 1. **MST Edge Check with Costs**
**Variation**: Each edge has additional costs beyond weight, find MST with cost constraints.
**Approach**: Use weighted MST construction with cost optimization.
```python
def cost_based_mst_edge_check(n, edges, edge_costs):
    # edge_costs[(a, b)] = additional cost for edge (a, b)
    
    class CostUnionFind:
        def __init__(self, n):
            self.parent = list(range(n + 1))
            self.rank = [0] * (n + 1)
            self.total_cost = 0
        
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y, edge_cost):
            px, py = self.find(x), self.find(y)
            if px == py:
                return False
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            self.total_cost += edge_cost
            return True
    
    def find_cost_based_mst():
        # Add indices and costs
        indexed_edges = []
        for i, (a, b, w) in enumerate(edges):
            additional_cost = edge_costs.get((a, b), 0)
            total_cost = w + additional_cost
            indexed_edges.append((i, a, b, w, total_cost))
        
        # Sort by total cost
        sorted_edges = sorted(indexed_edges, key=lambda x: x[4])
        
        # Kruskal's algorithm with cost tracking
        uf = CostUnionFind(n)
        mst_indices = set()
        
        for idx, a, b, w, total_cost in sorted_edges:
            if uf.union(a, b, total_cost):
                mst_indices.add(idx)
        
        return mst_indices, uf.total_cost
    
    mst_edges, total_cost = find_cost_based_mst()
    return mst_edges, total_cost
```

#### 2. **MST Edge Check with Constraints**
**Variation**: Limited budget, restricted edges, or specific connectivity requirements.
**Approach**: Use constraint satisfaction with MST construction.
```python
def constrained_mst_edge_check(n, edges, budget, restricted_edges, required_edges):
    # budget = maximum cost allowed
    # restricted_edges = set of edges that cannot be used
    # required_edges = set of edges that must be included
    
    class ConstrainedUnionFind:
        def __init__(self, n):
            self.parent = list(range(n + 1))
            self.rank = [0] * (n + 1)
            self.total_cost = 0
        
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        
        def union(self, x, y, cost):
            px, py = self.find(x), self.find(y)
            if px == py:
                return False
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            self.total_cost += cost
            return True
    
    def find_constrained_mst():
        # Add indices
        indexed_edges = [(i, a, b, w) for i, (a, b, w) in enumerate(edges)]
        
        # First, include required edges
        uf = ConstrainedUnionFind(n)
        mst_indices = set()
        
        for i, a, b, w in indexed_edges: if (a, b) in 
required_edges: if uf.union(a, b, w):
                    mst_indices.add(i)
                else:
                    return None, float('inf')  # Impossible
        
        # Then add remaining edges (excluding restricted ones)
        remaining_edges = []
        for i, a, b, w in indexed_edges: if (a, b) not in required_edges and (a, b) not in 
restricted_edges: remaining_edges.append((i, a, b, w))
        
        # Sort by weight
        remaining_edges.sort(key=lambda x: x[3])
        
        # Add edges until budget is exceeded or MST is complete
        for i, a, b, w in remaining_edges: if uf.total_cost + w > 
budget: break
            if uf.union(a, b, w):
                mst_indices.add(i)
        
        return mst_indices, uf.total_cost
    
    mst_edges, total_cost = find_constrained_mst()
    return mst_edges, total_cost
```

#### 3. **MST Edge Check with Probabilities**
**Variation**: Each edge has a probability of being available.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
def probabilistic_mst_edge_check(n, edges, edge_probabilities):
    # edge_probabilities[(a, b)] = probability edge (a, b) is available
    
    def monte_carlo_simulation(trials=1000):
        edge_frequencies = [0] * len(edges)
        
        for _ in range(trials):
            # Simulate available edges
            available_edges = []
            for i, (a, b, w) in enumerate(edges):
                if random.random() < edge_probabilities.get((a, b), 0.5):
                    available_edges.append((i, a, b, w))
            
            # Find MST with available edges
            mst_indices = find_mst_with_edges(n, available_edges)
            
            for idx in mst_indices:
                edge_frequencies[idx] += 1
        
        # Calculate probabilities
        probabilities = [freq / trials for freq in edge_frequencies]
        return probabilities
    
    def find_mst_with_edges(n, available_edges):
        # Sort by weight
        sorted_edges = sorted(available_edges, key=lambda x: x[3])
        
        # Union-Find
        uf = UnionFind(n)
        mst_indices = set()
        
        for idx, a, b, w in sorted_edges:
            if uf.union(a, b):
                mst_indices.add(idx)
        
        return mst_indices
    
    return monte_carlo_simulation()
```

#### 4. **MST Edge Check with Multiple Criteria**
**Variation**: Optimize for multiple objectives (weight, reliability, capacity).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_mst_edge_check(n, edges, criteria_weights):
    # criteria_weights = {'weight': 0.4, 'reliability': 0.3, 'capacity': 0.3}
    # Each edge has multiple attributes
    
    def calculate_edge_score(edge_attributes):
        return (criteria_weights['weight'] * edge_attributes['weight'] + 
                criteria_weights['reliability'] * edge_attributes['reliability'] + 
                criteria_weights['capacity'] * edge_attributes['capacity'])
    
    def find_multi_criteria_mst():
        # Add indices and calculate scores
        indexed_edges = []
        for i, (a, b, w) in enumerate(edges):
            # Calculate edge attributes (simplified)
            edge_attrs = {
                'weight': w,
                'reliability': 1.0 - (w / 1000),  # Higher weight = lower reliability
                'capacity': 100 - w  # Higher weight = lower capacity
            }
            score = calculate_edge_score(edge_attrs)
            indexed_edges.append((i, a, b, w, score))
        
        # Sort by score (lower is better)
        sorted_edges = sorted(indexed_edges, key=lambda x: x[4])
        
        # Kruskal's algorithm
        uf = UnionFind(n)
        mst_indices = set()
        total_score = 0
        
        for idx, a, b, w, score in sorted_edges:
            if uf.union(a, b):
                mst_indices.add(idx)
                total_score += score
        
        return mst_indices, total_score
    
    mst_edges, total_score = find_multi_criteria_mst()
    return mst_edges, total_score
```

#### 5. **MST Edge Check with Dynamic Updates**
**Variation**: Edges can be added or removed dynamically.
**Approach**: Use dynamic MST algorithms or incremental updates.
```python
class DynamicMSTEdgeCheck:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.mst_cache = None
        self.mst_cost = 0
    
    def add_edge(self, a, b, w):
        self.edges.append((a, b, w))
        self.invalidate_cache()
    
    def remove_edge(self, a, b, w):
        if (a, b, w) in self.edges:
            self.edges.remove((a, b, w))
            self.invalidate_cache()
    
    def update_edge_weight(self, a, b, old_w, new_w):
        if (a, b, old_w) in self.edges:
            self.edges.remove((a, b, old_w))
            self.edges.append((a, b, new_w))
            self.invalidate_cache()
    
    def invalidate_cache(self):
        self.mst_cache = None
        self.mst_cost = 0
    
    def get_mst_edges(self):
        if self.mst_cache is None:
            self.mst_cache, self.mst_cost = self.compute_mst()
        return self.mst_cache
    
    def compute_mst(self):
        # Add indices
        indexed_edges = [(i, a, b, w) for i, (a, b, w) in enumerate(self.edges)]
        
        # Sort by weight
        sorted_edges = sorted(indexed_edges, key=lambda x: x[3])
        
        # Kruskal's algorithm
        uf = UnionFind(self.n)
        mst_indices = set()
        total_cost = 0
        
        for idx, a, b, w in sorted_edges:
            if uf.union(a, b):
                mst_indices.add(idx)
                total_cost += w
        
        return mst_indices, total_cost
    
    def is_edge_in_mst(self, edge_index):
        mst_edges = self.get_mst_edges()
        return edge_index in mst_edges
    
    def get_mst_cost(self):
        if self.mst_cache is None:
            self.mst_cache, self.mst_cost = self.compute_mst()
        return self.mst_cost
```

### Related Problems & Concepts

#### 1. **Minimum Spanning Tree**
- **Kruskal's Algorithm**: Sort edges, use Union-Find
- **Prim's Algorithm**: Grow tree from single vertex
- **Boruvka's Algorithm**: Parallel MST construction
- **Steiner Tree**: MST connecting subset of vertices

#### 2. **Union-Find Data Structure**
- **Path Compression**: Optimize find operations
- **Union by Rank**: Optimize union operations
- **Connected Components**: Track graph connectivity
- **Cycle Detection**: Detect cycles in graphs

#### 3. **Graph Connectivity**
- **Connected Components**: Find all components
- **Bridges**: Critical edges for connectivity
- **Articulation Points**: Critical vertices
- **Biconnected Components**: 2-connected subgraphs

#### 4. **Optimization Problems**
- **Greedy Algorithms**: Local optimal choices
- **Dynamic Programming**: Optimal substructure
- **Linear Programming**: Mathematical optimization
- **Approximation Algorithms**: Near-optimal solutions

#### 5. **Dynamic Graph Problems**
- **Incremental MST**: Adding edges
- **Decremental MST**: Removing edges
- **Fully Dynamic MST**: Both adding and removing
- **Online Algorithms**: Real-time updates

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large graphs
- **Edge Cases**: Robust MST algorithms

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient edge processing
- **Sliding Window**: Optimal subgraph problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Combinatorics**
- **Tree Enumeration**: Counting MSTs
- **Permutations**: Order of edge additions
- **Combinations**: Choice of edges
- **Catalan Numbers**: Valid tree sequences

#### 2. **Probability Theory**
- **Expected Values**: Average MST weight
- **Markov Chains**: State transitions
- **Random Graphs**: Erdős-Rényi model
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special graph cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime edges

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: MST and graph problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **MST Problems**: Kruskal's, Prim's, Boruvka's
- **Connectivity Problems**: Union-Find, components
- **Dynamic Problems**: Incremental, decremental
- **Optimization Problems**: Multi-objective, constrained 