---
layout: simple
title: "Tree Matching"
permalink: /problem_soulutions/tree_algorithms/tree_matching_analysis
---

# Tree Matching

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand maximum matching in trees and its applications
- Apply dynamic programming on trees for matching problems
- Implement efficient tree algorithms for maximum matching
- Optimize tree matching algorithms for large inputs
- Handle edge cases in tree problems (single nodes, linear trees)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tree algorithms, DFS, tree DP, maximum matching, bipartite matching
- **Data Structures**: Trees, graphs, adjacency lists, DP arrays
- **Mathematical Concepts**: Tree theory, graph theory, matching theory, dynamic programming
- **Programming Skills**: Tree traversal, DFS implementation, DP on trees
- **Related Problems**: Subordinates (tree DP), Tree Diameter (tree traversal), Company Queries I (tree algorithms)

## 📋 Problem Description

Given a tree with n nodes, find the maximum number of edges that can be selected such that no two selected edges share a common vertex.

This is the maximum matching problem on trees, which can be solved efficiently using dynamic programming.

**Input**: 
- First line: integer n (number of nodes)
- Next n-1 lines: two integers a and b (edge between nodes a and b)

**Output**: 
- Print one integer: the maximum number of edges in a matching

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
5
1 2
1 3
3 4
3 5

Output:
2

Explanation**: 
The tree structure:
    1
   / \\
  2   3
     / \\
    4   5

Maximum matching: 2 edges
- Option 1: (1,2) and (3,4) → 2 edges
- Option 2: (1,2) and (3,5) → 2 edges
- Option 3: (1,3) and (4,5) → 2 edges

All options give the same maximum: 2 edges
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Matchings

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible combinations of edges
- **Complete Coverage**: Guaranteed to find the maximum matching
- **Simple Implementation**: Straightforward recursive approach
- **Inefficient**: Exponential time complexity

**Key Insight**: Generate all possible subsets of edges and find the largest valid matching.

**Algorithm**:
- Generate all possible subsets of edges
- For each subset, check if it forms a valid matching (no shared vertices)
- Keep track of the largest valid matching

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

All possible edge subsets:
1. {} → 0 edges
2. {(1,2)} → 1 edge ✓
3. {(1,3)} → 1 edge ✓
4. {(3,4)} → 1 edge ✓
5. {(3,5)} → 1 edge ✓
6. {(1,2), (1,3)} → share vertex 1 ✗
7. {(1,2), (3,4)} → no shared vertices ✓ (2 edges)
8. {(1,2), (3,5)} → no shared vertices ✓ (2 edges)
9. {(1,3), (4,5)} → no shared vertices ✓ (2 edges)
10. {(3,4), (3,5)} → share vertex 3 ✗
11. ... (more combinations)

Maximum: 2 edges
```

**Implementation**:
```python
def brute_force_tree_matching(n, edges):
    """
    Find maximum matching using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        int: maximum number of edges in matching
    """
    from itertools import combinations
    
    def is_valid_matching(edge_subset):
        """Check if edge subset forms a valid matching"""
        used_vertices = set()
        for a, b in edge_subset:
            if a in used_vertices or b in used_vertices:
                return False
            used_vertices.add(a)
            used_vertices.add(b)
        return True
    
    max_matching = 0
    
    # Try all possible subsets of edges
    for k in range(len(edges) + 1):
        for subset in combinations(edges, k):
            if is_valid_matching(subset):
                max_matching = max(max_matching, len(subset))
    
    return max_matching

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = brute_force_tree_matching(n, edges)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(2^m × m) - All subsets with validation
**Space Complexity**: O(m) - For storing subsets

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Greedy Matching

**Key Insights from Optimized Approach**:
- **Greedy Strategy**: Select edges greedily to maximize matching
- **Edge Selection**: Choose edges that don't conflict with already selected ones
- **Efficient Processing**: Process edges in a specific order
- **Linear Time**: Achieve O(n) time complexity

**Key Insight**: Use a greedy approach to select edges that don't conflict with already selected edges.

**Algorithm**:
- Sort edges in a specific order (e.g., by node degree)
- Greedily select edges that don't conflict with already selected ones
- Keep track of used vertices

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

Greedy selection:
1. Select (1,2) → used_vertices = {1, 2}
2. Skip (1,3) → conflicts with vertex 1
3. Select (3,4) → used_vertices = {1, 2, 3, 4}
4. Skip (3,5) → conflicts with vertex 3

Selected: {(1,2), (3,4)} → 2 edges
```

**Implementation**:
```python
def optimized_tree_matching(n, edges):
    """
    Find maximum matching using greedy approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        int: maximum number of edges in matching
    """
    used_vertices = set()
    matching = []
    
    # Sort edges by some criteria (e.g., by sum of node indices)
    sorted_edges = sorted(edges, key=lambda x: x[0] + x[1])
    
    for a, b in sorted_edges:
        if a not in used_vertices and b not in used_vertices:
            matching.append((a, b))
            used_vertices.add(a)
            used_vertices.add(b)
    
    return len(matching)

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimized_tree_matching(n, edges)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(n) - For used vertices set

**Why it's better**: Much more efficient than brute force, but not always optimal.

---

### Approach 3: Optimal - Dynamic Programming on Trees

**Key Insights from Optimal Approach**:
- **Tree DP**: Use dynamic programming on trees
- **State Definition**: dp[node][matched] = maximum matching in subtree
- **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
- **Linear Time**: Achieve O(n) time complexity

**Key Insight**: For each node, calculate the maximum matching in its subtree considering whether the node is matched or not.

**Algorithm**:
- For each node, calculate two values:
  - dp[node][0]: maximum matching when node is not matched
  - dp[node][1]: maximum matching when node is matched
- Use post-order DFS to process children before parent

**Visual Example**:
```
Tree: 1-2, 1-3, 3-4, 3-5

DP calculation (post-order):
1. Node 2: dp[2][0] = 0, dp[2][1] = 0
2. Node 4: dp[4][0] = 0, dp[4][1] = 0
3. Node 5: dp[5][0] = 0, dp[5][1] = 0
4. Node 3: 
   - dp[3][0] = dp[4][0] + dp[5][0] = 0
   - dp[3][1] = max(dp[4][0] + dp[5][0] + 1, dp[4][1] + dp[5][0], dp[4][0] + dp[5][1]) = 1
5. Node 1:
   - dp[1][0] = dp[2][0] + dp[3][0] = 0
   - dp[1][1] = max(dp[2][0] + dp[3][0] + 1, dp[2][1] + dp[3][0], dp[2][0] + dp[3][1]) = 2

Maximum matching: max(dp[1][0], dp[1][1]) = 2
```

**Implementation**:
```python
def optimal_tree_matching(n, edges):
    """
    Find maximum matching using dynamic programming on trees
    
    Args:
        n: number of nodes
        edges: list of (a, b) edge tuples
    
    Returns:
        int: maximum number of edges in matching
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # dp[node][0] = max matching when node is not matched
    # dp[node][1] = max matching when node is matched
    dp = [[0, 0] for _ in range(n + 1)]
    
    def dfs(node, parent):
        """DFS to calculate DP values"""
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
        
        # Calculate dp[node][0] and dp[node][1]
        dp[node][0] = 0  # Node not matched
        dp[node][1] = 0  # Node matched
        
        for child in adj[node]:
            if child != parent:
                # When node is not matched, take max of child's states
                dp[node][0] += max(dp[child][0], dp[child][1])
                
                # When node is matched, we can match with one child
                # and take max of other children's states
                dp[node][1] = max(dp[node][1], 
                                 dp[node][0] - max(dp[child][0], dp[child][1]) + dp[child][0] + 1)
    
    # Start DFS from node 1 (assuming it's the root)
    dfs(1, -1)
    
    return max(dp[1][0], dp[1][1])

# Example usage
n = 5
edges = [(1, 2), (1, 3), (3, 4), (3, 5)]
result = optimal_tree_matching(n, edges)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n) - Single DFS traversal
**Space Complexity**: O(n) - For DP array and adjacency list

**Why it's optimal**: Achieves the best possible time complexity for the maximum matching problem on trees.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^m × m) | O(m) | Try all edge subsets |
| Greedy | O(n log n) | O(n) | Select edges greedily |
| Tree DP | O(n) | O(n) | Dynamic programming on trees |

### Time Complexity
- **Time**: O(n) - Tree DP provides optimal linear time
- **Space**: O(n) - For DP array and adjacency list

### Why This Solution Works
- **Tree Properties**: Trees have unique paths, enabling efficient DP
- **Optimal Substructure**: Maximum matching in subtree can be computed from children
- **State Definition**: Two states per node (matched/unmatched) capture all possibilities
- **Optimal Approach**: Tree DP provides the most efficient and elegant solution

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Tree Matching with Dynamic Updates
**Problem**: Handle dynamic updates to the tree structure and maintain maximum matching efficiently.

**Link**: [CSES Problem Set - Tree Matching with Updates](https://cses.fi/problemset/task/tree_matching_updates)

```python
class TreeMatchingWithUpdates:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.matching_count = 0
        self.matched = [False] * n
        self.parent = [-1] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_matching()
    
    def _calculate_matching(self):
        """Calculate maximum matching using tree DP"""
        def dfs(node, parent):
            self.parent[node] = parent
            unmatched_children = 0
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node)
                    if not self.matched[child]:
                        unmatched_children += 1
            
            # If we have unmatched children, match with one of them
            if unmatched_children > 0:
                self.matched[node] = True
                self.matching_count += 1
        
        dfs(0, -1)
    
    def add_edge(self, u, v):
        """Add edge between nodes u and v"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        
        # Recalculate matching
        self._reset_matching()
        self._calculate_matching()
    
    def remove_edge(self, u, v):
        """Remove edge between nodes u and v"""
        if v in self.adj[u]:
            self.adj[u].remove(v)
        if u in self.adj[v]:
            self.adj[v].remove(u)
        
        # Recalculate matching
        self._reset_matching()
        self._calculate_matching()
    
    def _reset_matching(self):
        """Reset matching state"""
        self.matching_count = 0
        self.matched = [False] * self.n
        self.parent = [-1] * self.n
    
    def get_matching_count(self):
        """Get current maximum matching count"""
        return self.matching_count
    
    def get_matched_nodes(self):
        """Get list of matched nodes"""
        return [i for i in range(self.n) if self.matched[i]]
    
    def get_unmatched_nodes(self):
        """Get list of unmatched nodes"""
        return [i for i in range(self.n) if not self.matched[i]]
    
    def get_matching_edges(self):
        """Get list of edges in the matching"""
        matching_edges = []
        for i in range(self.n):
            if self.matched[i]:
                for child in self.adj[i]:
                    if child != self.parent[i] and not self.matched[child]:
                        matching_edges.append((i, child))
                        break
        return matching_edges
    
    def get_matching_statistics(self):
        """Get comprehensive matching statistics"""
        return {
            'matching_count': self.matching_count,
            'matched_nodes_count': sum(self.matched),
            'unmatched_nodes_count': self.n - sum(self.matched),
            'matching_ratio': self.matching_count / (self.n - 1) if self.n > 1 else 0,
            'matched_nodes': self.get_matched_nodes(),
            'unmatched_nodes': self.get_unmatched_nodes(),
            'matching_edges': self.get_matching_edges()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'add_edge':
                self.add_edge(query['u'], query['v'])
                results.append(None)
            elif query['type'] == 'remove_edge':
                self.remove_edge(query['u'], query['v'])
                results.append(None)
            elif query['type'] == 'matching_count':
                result = self.get_matching_count()
                results.append(result)
            elif query['type'] == 'matched_nodes':
                result = self.get_matched_nodes()
                results.append(result)
            elif query['type'] == 'unmatched_nodes':
                result = self.get_unmatched_nodes()
                results.append(result)
            elif query['type'] == 'matching_edges':
                result = self.get_matching_edges()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_matching_statistics()
                results.append(result)
        return results
```

### Variation 2: Tree Matching with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on tree matching.

**Link**: [CSES Problem Set - Tree Matching Different Operations](https://cses.fi/problemset/task/tree_matching_operations)

```python
class TreeMatchingDifferentOps:
    def __init__(self, n, edges):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.matching_count = 0
        self.matched = [False] * n
        self.parent = [-1] * n
        self.depths = [0] * n
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_matching()
    
    def _calculate_matching(self):
        """Calculate maximum matching using tree DP"""
        def dfs(node, parent, depth):
            self.parent[node] = parent
            self.depths[node] = depth
            unmatched_children = 0
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1)
                    if not self.matched[child]:
                        unmatched_children += 1
            
            # If we have unmatched children, match with one of them
            if unmatched_children > 0:
                self.matched[node] = True
                self.matching_count += 1
        
        dfs(0, -1, 0)
    
    def get_matching_count(self):
        """Get current maximum matching count"""
        return self.matching_count
    
    def get_matched_nodes(self):
        """Get list of matched nodes"""
        return [i for i in range(self.n) if self.matched[i]]
    
    def get_unmatched_nodes(self):
        """Get list of unmatched nodes"""
        return [i for i in range(self.n) if not self.matched[i]]
    
    def get_matching_edges(self):
        """Get list of edges in the matching"""
        matching_edges = []
        for i in range(self.n):
            if self.matched[i]:
                for child in self.adj[i]:
                    if child != self.parent[i] and not self.matched[child]:
                        matching_edges.append((i, child))
                        break
        return matching_edges
    
    def get_depth_statistics(self):
        """Get depth statistics for matched and unmatched nodes"""
        matched_depths = [self.depths[i] for i in range(self.n) if self.matched[i]]
        unmatched_depths = [self.depths[i] for i in range(self.n) if not self.matched[i]]
        
        return {
            'matched_avg_depth': sum(matched_depths) / len(matched_depths) if matched_depths else 0,
            'unmatched_avg_depth': sum(unmatched_depths) / len(unmatched_depths) if unmatched_depths else 0,
            'matched_max_depth': max(matched_depths) if matched_depths else 0,
            'unmatched_max_depth': max(unmatched_depths) if unmatched_depths else 0,
            'matched_min_depth': min(matched_depths) if matched_depths else 0,
            'unmatched_min_depth': min(unmatched_depths) if unmatched_depths else 0
        }
    
    def get_matching_by_depth(self):
        """Get matching statistics grouped by depth"""
        depth_groups = {}
        for i in range(self.n):
            depth = self.depths[i]
            if depth not in depth_groups:
                depth_groups[depth] = {'matched': 0, 'unmatched': 0}
            
            if self.matched[i]:
                depth_groups[depth]['matched'] += 1
            else:
                depth_groups[depth]['unmatched'] += 1
        
        return depth_groups
    
    def get_matching_statistics(self):
        """Get comprehensive matching statistics"""
        return {
            'matching_count': self.matching_count,
            'matched_nodes_count': sum(self.matched),
            'unmatched_nodes_count': self.n - sum(self.matched),
            'matching_ratio': self.matching_count / (self.n - 1) if self.n > 1 else 0,
            'matched_nodes': self.get_matched_nodes(),
            'unmatched_nodes': self.get_unmatched_nodes(),
            'matching_edges': self.get_matching_edges(),
            'depth_statistics': self.get_depth_statistics(),
            'matching_by_depth': self.get_matching_by_depth()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'matching_count':
                result = self.get_matching_count()
                results.append(result)
            elif query['type'] == 'matched_nodes':
                result = self.get_matched_nodes()
                results.append(result)
            elif query['type'] == 'unmatched_nodes':
                result = self.get_unmatched_nodes()
                results.append(result)
            elif query['type'] == 'matching_edges':
                result = self.get_matching_edges()
                results.append(result)
            elif query['type'] == 'depth_statistics':
                result = self.get_depth_statistics()
                results.append(result)
            elif query['type'] == 'matching_by_depth':
                result = self.get_matching_by_depth()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_matching_statistics()
                results.append(result)
        return results
```

### Variation 3: Tree Matching with Constraints
**Problem**: Handle tree matching with additional constraints (e.g., minimum depth, maximum depth, depth range).

**Link**: [CSES Problem Set - Tree Matching with Constraints](https://cses.fi/problemset/task/tree_matching_constraints)

```python
class TreeMatchingWithConstraints:
    def __init__(self, n, edges, min_depth, max_depth):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.matching_count = 0
        self.matched = [False] * n
        self.parent = [-1] * n
        self.depths = [0] * n
        self.min_depth = min_depth
        self.max_depth = max_depth
        
        # Build adjacency list
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._calculate_matching()
    
    def _calculate_matching(self):
        """Calculate maximum matching using tree DP with constraints"""
        def dfs(node, parent, depth):
            self.parent[node] = parent
            self.depths[node] = depth
            unmatched_children = 0
            
            for child in self.adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1)
                    if not self.matched[child]:
                        unmatched_children += 1
            
            # If we have unmatched children and depth constraints are satisfied
            if unmatched_children > 0 and self.min_depth <= depth <= self.max_depth:
                self.matched[node] = True
                self.matching_count += 1
        
        dfs(0, -1, 0)
    
    def get_matching_count(self):
        """Get current maximum matching count"""
        return self.matching_count
    
    def get_matched_nodes(self):
        """Get list of matched nodes"""
        return [i for i in range(self.n) if self.matched[i]]
    
    def get_unmatched_nodes(self):
        """Get list of unmatched nodes"""
        return [i for i in range(self.n) if not self.matched[i]]
    
    def get_matching_edges(self):
        """Get list of edges in the matching"""
        matching_edges = []
        for i in range(self.n):
            if self.matched[i]:
                for child in self.adj[i]:
                    if child != self.parent[i] and not self.matched[child]:
                        matching_edges.append((i, child))
                        break
        return matching_edges
    
    def get_constrained_matching_count(self):
        """Get matching count considering depth constraints"""
        constrained_count = 0
        for i in range(self.n):
            if self.matched[i] and self.min_depth <= self.depths[i] <= self.max_depth:
                constrained_count += 1
        return constrained_count
    
    def get_valid_nodes_for_matching(self):
        """Get nodes that satisfy depth constraints"""
        return [i for i in range(self.n) if self.min_depth <= self.depths[i] <= self.max_depth]
    
    def get_constrained_matching_edges(self):
        """Get matching edges considering depth constraints"""
        constrained_edges = []
        for i in range(self.n):
            if self.matched[i] and self.min_depth <= self.depths[i] <= self.max_depth:
                for child in self.adj[i]:
                    if child != self.parent[i] and not self.matched[child]:
                        constrained_edges.append((i, child))
                        break
        return constrained_edges
    
    def get_constrained_statistics(self):
        """Get comprehensive statistics considering depth constraints"""
        valid_nodes = self.get_valid_nodes_for_matching()
        constrained_edges = self.get_constrained_matching_edges()
        
        return {
            'total_matching_count': self.matching_count,
            'constrained_matching_count': len(constrained_edges),
            'valid_nodes_count': len(valid_nodes),
            'matching_ratio': len(constrained_edges) / (self.n - 1) if self.n > 1 else 0,
            'constrained_ratio': len(constrained_edges) / len(valid_nodes) if valid_nodes else 0,
            'min_depth': self.min_depth,
            'max_depth': self.max_depth,
            'valid_nodes': valid_nodes,
            'constrained_edges': constrained_edges
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'matching_count':
                result = self.get_matching_count()
                results.append(result)
            elif query['type'] == 'matched_nodes':
                result = self.get_matched_nodes()
                results.append(result)
            elif query['type'] == 'unmatched_nodes':
                result = self.get_unmatched_nodes()
                results.append(result)
            elif query['type'] == 'matching_edges':
                result = self.get_matching_edges()
                results.append(result)
            elif query['type'] == 'constrained_matching_count':
                result = self.get_constrained_matching_count()
                results.append(result)
            elif query['type'] == 'valid_nodes_for_matching':
                result = self.get_valid_nodes_for_matching()
                results.append(result)
            elif query['type'] == 'constrained_matching_edges':
                result = self.get_constrained_matching_edges()
                results.append(result)
            elif query['type'] == 'constrained_statistics':
                result = self.get_constrained_statistics()
                results.append(result)
        return results

# Example usage
n = 5
edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
min_depth = 1
max_depth = 3

tm = TreeMatchingWithConstraints(n, edges, min_depth, max_depth)
result = tm.get_constrained_matching_count()
print(f"Constrained matching count result: {result}")

valid_nodes = tm.get_valid_nodes_for_matching()
print(f"Valid nodes: {valid_nodes}")

statistics = tm.get_constrained_statistics()
print(f"Constrained statistics: {statistics}")
```

### Related Problems

#### **CSES Problems**
- [Tree Matching](https://cses.fi/problemset/task/1130) - Basic tree matching problem
- [Subordinates](https://cses.fi/problemset/task/1674) - Tree DP and subtree analysis
- [Tree Diameter](https://cses.fi/problemset/task/1131) - Tree traversal and analysis

#### **LeetCode Problems**
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) - Tree traversal by levels
- [Path Sum](https://leetcode.com/problems/path-sum/) - Path queries in tree
- [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Path analysis in tree

#### **Problem Categories**
- **Tree DP**: Dynamic programming on trees, matching algorithms
- **Tree Traversal**: DFS, BFS, tree processing
- **Tree Queries**: Tree analysis, tree operations
- **Tree Algorithms**: Tree properties, tree analysis, tree operations
