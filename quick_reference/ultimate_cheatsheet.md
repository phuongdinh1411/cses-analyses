---
layout: simple
title: "Ultimate Cheatsheet
permalink: /quick_reference/ultimate_cheatsheet/
---

# 🚀 Ultimate Cheatsheet - Complete Quick Reference Guide

## 📊 Quick Reference Guide

### 🎯 Dynamic Programming

<table>
<thead>
<tr>
<th>Problem Type</th>
<th>Algorithm</th>
<th>Time</th>
<th>Space</th>
<th>Key Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td>Coin Change</td>
<td>Unbounded Knapsack</td>
<td>O(n*target)</td>
<td>O(target)</td>
<td><code>dp[i] += dp[i-coin]</code></td>
</tr>
<tr>
<td>LIS</td>
<td>Binary Search</td>
<td>O(n log n)</td>
<td>O(n)</td>
<td><code>bisect.bisect_left(dp, x)</code></td>
</tr>
<tr>
<td>Grid Paths</td>
<td>2D DP</td>
<td>O(m*n)</td>
<td>O(m*n)</td>
<td><code>dp[i][j] = dp[i-1][j] + dp[i][j-1]</code></td>
</tr>
<tr>
<td>Edit Distance</td>
<td>String DP</td>
<td>O(m*n)</td>
<td>O(m*n)</td>
<td><code>dp[i][j] = min(insert, delete, replace)</code></td>
</tr>
</tbody>
</table>

### 🌐 Graph Algorithms

<table>
<thead>
<tr>
<th>Problem Type</th>
<th>Algorithm</th>
<th>Time</th>
<th>Space</th>
<th>Key Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td>Shortest Path</td>
<td>Dijkstra</td>
<td>O((V+E) log V)</td>
<td>O(V)</td>
<td><code>heapq.heappush(pq, (dist, node))</code></td>
</tr>
<tr>
<td>All Pairs</td>
<td>Floyd-Warshall</td>
<td>O(V³)</td>
<td>O(V²)</td>
<td><code>dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])</code></td>
</tr>
<tr>
<td>SCC</td>
<td>Kosaraju</td>
<td>O(V+E)</td>
<td>O(V+E)</td>
<td>DFS + Transpose + DFS</td>
</tr>
<tr>
<td>Topological Sort</td>"
<td>Kahn's</td>
<td>O(V+E)</td>
<td>O(V)</td>
<td><code>indegree[node] == 0</code></td>
</tr>
</tbody>
</table>

### 🌳 Tree Algorithms

<table>
<thead>
<tr>
<th>Problem Type</th>
<th>Algorithm</th>
<th>Time</th>
<th>Space</th>
<th>Key Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td>LCA</td>
<td>Binary Lifting</td>
<td>O(log n)</td>
<td>O(n log n)</td>
<td><code>parent[node][j] = parent[parent[node][j-1]][j-1]</code></td>
</tr>
<tr>
<td>Tree Diameter</td>
<td>DFS</td>
<td>O(n)</td>
<td>O(n)</td>
<td><code>max_depth + second_max_depth</code></td>
</tr>
<tr>
<td>Tree DP</td>
<td>Post-order</td>
<td>O(n)</td>
<td>O(n)</td>
<td><code>dfs(child) then combine results</code></td>
</tr>
</tbody>
</table>

### 🔍 Range Queries

<table>
<thead>
<tr>
<th>Problem Type</th>
<th>Algorithm</th>
<th>Time</th>
<th>Space</th>
<th>Key Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td>Static Sum</td>
<td>Prefix Sum</td>
<td>O(1)</td>
<td>O(n)</td>
<td><code>prefix[r+1] - prefix[l]</code></td>
</tr>
<tr>
<td>Dynamic Sum</td>
<td>Binary Indexed Tree</td>
<td>O(log n)</td>
<td>O(n)</td>
<td><code>update(idx, val)</code></td>
</tr>
<tr>
<td>Range Min</td>
<td>Segment Tree</td>
<td>O(log n)</td>
<td>O(4n)</td>
<td><code>min(left_child, right_child)</code></td>
</tr>
</tbody>
</table>

### 📝 String Algorithms

<table>
<thead>
<tr>
<th>Problem Type</th>
<th>Algorithm</th>
<th>Time</th>
<th>Space</th>
<th>Key Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td>Pattern Matching</td>
<td>KMP</td>
<td>O(n+m)</td>
<td>O(m)</td>
<td><code>build_lps(pattern)</code></td>
</tr>
<tr>
<td>Palindrome</td>
<td>Manacher</td>
<td>O(n)</td>
<td>O(n)</td>
<td><code>expand around center</code></td>
</tr>
<tr>
<td>Suffix Array</td>
<td>SA-IS</td>
<td>O(n)</td>
<td>O(n)</td>
<td><code>sort suffixes</code></td>
</tr>
</tbody>
</table>

### 🔍 Binary Search

<table>
<thead>
<tr>
<th>Problem Type</th>
<th>Algorithm</th>
<th>Time</th>
<th>Space</th>
<th>Key Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td>Find Element</td>
<td>Binary Search</td>
<td>O(log n)</td>
<td>O(1)</td>
<td><code>left <= right</code></td>
</tr>
<tr>
<td>Find Answer</td>
<td>Binary Search</td>
<td>O(log range)</td>
<td>O(1)</td>
<td><code>while left < right</code></td>
</tr>
<tr>
<td>Find Peak</td>
<td>Binary Search</td>
<td>O(log n)</td>
<td>O(1)</td>
<td><code>nums[mid] > nums[mid+1]</code></td>
</tr>
</tbody>
</table>

### 👆 Two Pointers

<table>
<thead>
<tr>
<th>Problem Type</th>
<th>Algorithm</th>
<th>Time</th>
<th>Space</th>
<th>Key Pattern</th>
</tr>
</thead>
<tbody>
<tr>
<td>Sorted Array</td>
<td>Two Pointers</td>
<td>O(n)</td>
<td>O(1)</td>
<td><code>left++ or right--</code></td>
</tr>
<tr>
<td>Sliding Window</td>
<td>Two Pointers</td>
<td>O(n)</td>
<td>O(1)</td>
<td><code>while condition: left++</code></td>
</tr>
<tr>
<td>Linked List</td>
<td>Fast/Slow</td>
<td>O(n)</td>
<td>O(1)</td>
<td><code>fast = fast.next.next</code></td>
</tr>
</tbody>
</table>

## 🎯 Problem-Solving Decision Tree

### 📋 Step 1: Read Problem Carefully
- **Identify keywords** in the problem statement
- **Note constraints** (n ≤ 10⁵, etc.)
- **Understand what's being asked**

### 🔍 Step 2: Problem Classification

#### 🤔 Is it an optimization problem?
- **Keywords**: "maximum", "minimum", "optimal", "best"
- **→ Dynamic Programming**

#### 🌐 Is it about connections/paths?
- **Keywords**: "shortest path", "connected", "reachable", "route"
- **→ Graph Algorithms**

#### 🌳 Is it hierarchical/tree-like?
- **Keywords**: "parent", "child", "subtree", "ancestor"
- **→ Tree Algorithms**

#### 📊 Is it about ranges/queries?
- **Keywords**: "range", "query", "sum", "minimum in range"
- **→ Range Queries**

#### 📝 Is it about strings?
- **Keywords**: "pattern", "substring", "palindrome", "match"
- **→ String Algorithms**

#### 🔍 Is it about searching?
- **Keywords**: "find", "search", "binary search"
- **→ Binary Search**

#### 👆 Is it about subarrays/windows?
- **Keywords**: "subarray", "window", "consecutive", "k elements"
- **→ Two Pointers/Sliding Window**

#### 🔢 Is it about counting?
- **Keywords**: "count", "number of ways", "how many"
- **→ Combinatorics/Counting**

## 🎯 Algorithm Selection Flowchart

```
Problem Statement
       ↓
Read Constraints
       ↓
Identify Keywords
       ↓
Choose Algorithm Category
       ↓
Select Specific Algorithm
       ↓
Implement Solution
       ↓
Test & Optimize
```

## 📏 Constraint-Based Algorithm Selection

### 🚀 For n ≤ 10⁶ (Large Input)
- **O(n) or O(n log n) required**
- **Avoid O(n²) algorithms**
- **Use efficient data structures**

### 🔍 For n ≤ 10⁵ (Medium Input)
- **O(n log n) acceptable**
- **Can use sorting + binary search**
- **Segment trees, BIT acceptable**

### 🎯 For n ≤ 10³ (Small Input)
- **O(n²) acceptable**
- **Can use brute force with optimization**
- **DP with 2D state space**

### 🔢 For n ≤ 20 (Very Small Input)
- **O(2ⁿ) acceptable**
- **Bitmask DP**
- **Backtracking**

## 🎯 Problem Identification Guide

### 🔍 Keywords → Algorithm
- **"optimal", "maximum", "minimum"** → Dynamic Programming
- **"shortest path", "connected"** → Graph Algorithms  
- **"subtree", "ancestor"** → Tree Algorithms
- **"range", "query"** → Range Queries
- **"pattern", "substring"** → String Algorithms
- **"find", "search"** → Binary Search
- **"subarray", "window"** → Two Pointers/Sliding Window

### 📏 Constraints → Algorithm Choice
- **n ≤ 10⁵, queries ≤ 10⁵** → O(n log n) or better
- **n ≤ 10³** → O(n²) acceptable
- **n ≤ 20** → Bitmask DP
- **n ≤ 10⁶** → O(n) required

## 🎨 Visual Learning Aids

### 🔍 Binary Search Flowchart
```
Start
  ↓
Set left = 0, right = n-1
  ↓
while left <= right:
  ↓
  mid = (left + right) // 2
  ↓
  if arr[mid] == target:
    ↓
    return mid
  ↓
  elif arr[mid] < target:
    ↓
    left = mid + 1
  ↓
  else:
    ↓
    right = mid - 1
  ↓
return -1
```

### 🌊 DFS Flowchart
```
Start
  ↓
Mark node as visited
  ↓
For each neighbor:
  ↓
  if neighbor not visited:
    ↓
    DFS(neighbor)
  ↓
End
```

### 🎯 DP Flowchart
```
Start
  ↓
Define DP state
  ↓
Set base cases
  ↓
For each state:
  ↓
  Fill DP table using transitions
  ↓
Return final answer
```

## 📈 Timeline Diagrams

### 👆 Sliding Window Timeline
```
Array: [1, 2, 3, 4, 5, 6, 7, 8]
       ↑     ↑
       L     R
       Window size = 3

Move R: [1, 2, 3, 4, 5, 6, 7, 8]
          ↑     ↑
          L     R

Move L: [1, 2, 3, 4, 5, 6, 7, 8]
             ↑     ↑
             L     R
```

### 🔍 Binary Search Timeline
```
Array: [1, 3, 5, 7, 9, 11, 13, 15]
       L           M           R
       ↑           ↑           ↑
       0           3           7

Target = 9
arr[M] = 7 < 9, so L = M + 1

Array: [1, 3, 5, 7, 9, 11, 13, 15]
                    L   M       R
                    ↑   ↑       ↑
                    4   5       7

arr[M] = 11 > 9, so R = M - 1
```

## 🌳 Tree Visualizations

### 🌳 Binary Tree Structure
```
       1
      / \
     2   3
    / \   \
   4   5   6
      /
     7
```

### 🌳 Tree Traversal Orders
```
Preorder:  1 → 2 → 4 → 5 → 7 → 3 → 6
Inorder:   4 → 2 → 7 → 5 → 1 → 3 → 6
Postorder: 4 → 7 → 5 → 2 → 6 → 3 → 1
```

### 🌳 LCA Example
```
       1
      / \
     2   3
    / \   \
   4   5   6
      /
     7

LCA(4, 7) = 2
LCA(4, 6) = 1
LCA(5, 7) = 5
```

## 📊 Grid Visualizations

### 🎯 2D DP Grid
```
Grid: 3x3
[1][1][1]
[1][2][3]
[1][3][6]

Paths to each cell:
- (0,0): 1 way
- (0,1): 1 way (right only)
- (1,0): 1 way (down only)
- (1,1): 2 ways (right+down or down+right)
```

### 🌐 Graph Adjacency Matrix
```
    A  B  C  D
A   0  1  1  0
B   1  0  0  1
C   1  0  0  1
D   0  1  1  0

1 = connected
0 = not connected
```

## 🔢 Mathematical Visualizations

### 📈 Prefix Sum Array
```
Original: [1, 2, 3, 4, 5]
Prefix:   [1, 3, 6, 10, 15]

Range sum(2,4) = prefix[4] - prefix[1] = 15 - 3 = 12
```

### 🔢 Binary Indexed Tree
```
Array: [1, 2, 3, 4, 5, 6, 7, 8]
BIT:   [1, 3, 3, 10, 5, 11, 7, 36]

Update: Add value to position and all ancestors
Query: Sum values from position to root
```

### 📊 Segment Tree
```
Array: [1, 2, 3, 4, 5, 6, 7, 8]
Tree:  [1, 2, 3, 4, 5, 6, 7, 8]
       [3, 7, 11, 15]
       [10, 26]
       [36]

Each node stores sum of its children
```

## 💡 Common Code Patterns

### 🔢 Modular Arithmetic
```python
MOD = 10**9 + 7
result = (result + value) % MOD
```

### 🔍 Binary Search Template
```python
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

### 🌊 DFS Template
```python
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

### 🎯 DP Template
```python
def dp_solution(n):
    dp = [0] * (n + 1)
    dp[0] = 1  # base case
    
    for i in range(1, n + 1):
        # fill dp[i] based on subproblems
        pass
    
    return dp[n]
```

## 🚨 Common Pitfalls

### ⏰ Time Complexity Mistakes
- **Nested loops**: O(n²) not O(n)
- **String operations**: O(n) not O(1)
- **List operations**: O(n) not O(1)

### 💾 Memory Issues
- **Large arrays**: Use sparse representation
- **Recursion depth**: Use iterative or tail recursion
- **String concatenation**: Use join() not +

### ⚠️ Edge Cases
- **Empty input**: Check len(arr) == 0
- **Single element**: Handle separately
- **Negative numbers**: Check bounds
- **Overflow**: Use modular arithmetic

## 📊 Complexity Reference

### 🔢 Common Complexities
- **O(1)**: Constant time operations
- **O(log n)**: Binary search, tree operations
- **O(n)**: Linear scan, single loop
- **O(n log n)**: Sorting, divide and conquer
- **O(n²)**: Nested loops, quadratic
- **O(2ⁿ)**: Exponential, backtracking
- **O(n!)**: Factorial, permutations

### 💾 Space Complexities
- **O(1)**: Constant extra space
- **O(n)**: Linear space (arrays, hash maps)
- **O(n²)**: 2D arrays, adjacency matrices
- **O(log n)**: Recursion stack depth

## 🎯 Quick Decision Rules

### 🎯 Dynamic Programming
- **"Find maximum/minimum"** + **"choices/decisions"**
- **"Count ways"** + **"constraints"**
- **"Optimal substructure"** (subproblems)

### 🌐 Graph Algorithms
- **"Shortest path"** → Dijkstra/Bellman-Ford
- **"All pairs shortest"** → Floyd-Warshall
- **"Connected components"** → DFS/BFS
- **"Topological order"** → Kahn's Algorithm

### 🌳 Tree Algorithms
- **"Lowest common ancestor"** → Binary Lifting
- **"Tree diameter"** → DFS twice
- **"Subtree queries"** → Euler Tour + Segment Tree

### 🔍 Range Queries
- **"Static queries"** → Prefix Sum/Sparse Table
- **"Dynamic queries"** → Segment Tree/BIT
- **"Range updates"** → Lazy Propagation

### 📝 String Algorithms
- **"Pattern matching"** → KMP
- **"Palindrome"** → Manacher
- **"Suffix operations"** → Suffix Array

## 🎨 Color-Coded Learning

### 🟢 Easy Problems (Green)
- Basic algorithms
- Simple data structures
- Straightforward implementation

### 🟡 Medium Problems (Yellow)
- Algorithm combinations
- Optimization required
- Edge cases important

### 🔴 Hard Problems (Red)
- Advanced algorithms
- Complex optimizations
- Multiple techniques needed

### 🔵 Special Problems (Blue)
- Mathematical insights
- Creative solutions
- Pattern recognition

## 🚀 Memory Aids

### 🎯 Algorithm Mnemonics
- **DP**: "Divide Problem" into subproblems
- **DFS**: "Deep First Search" - go deep before wide
- **BFS**: "Breadth First Search" - go wide before deep
- **BST**: "Binary Search Tree" - left < root < right

### 🎯 Pattern Recognition
- **"Find maximum/minimum"** → Optimization → DP
- **"Count ways"** → Combinatorics → DP
- **"Shortest path"** → Graph → BFS/Dijkstra
- **"Connected components"** → Graph → DFS/BFS

### 🎯 Constraint Patterns
- **n ≤ 10⁶** → O(n) or O(n log n) required
- **n ≤ 10³** → O(n²) acceptable
- **n ≤ 20** → O(2ⁿ) acceptable (bitmask)
- **queries ≤ 10⁵** → O(log n) per query

## 🎯 Emergency Quick Reference

### 🔍 Problem Type Identification
- **"maximum/minimum"** → Dynamic Programming
- **"shortest path"** → Graph Algorithms
- **"subtree/ancestor"** → Tree Algorithms
- **"range/query"** → Range Queries
- **"pattern/substring"** → String Algorithms
- **"find/search"** → Binary Search
- **"subarray/window"** → Sliding Window

### 📏 Constraint-Based Algorithm Choice
- **n ≤ 10⁶** → O(n) or O(n log n) required
- **n ≤ 10³** → O(n²) acceptable
- **n ≤ 20** → O(2ⁿ) acceptable (bitmask)
- **queries ≤ 10⁵** → O(log n) per query

### ⚠️ Common Pitfalls
- **Nested loops** = O(n²) not O(n)
- **String operations** = O(n) not O(1)
- **List operations** = O(n) not O(1)
- **Always check edge cases**
- **Handle integer overflow**

## 🎯 Success Checklist

### 📋 Before Solving
- [ ] Read problem carefully
- [ ] Identify keywords and constraints
- [ ] Choose appropriate algorithm
- [ ] Plan implementation approach

### 📋 During Solving
- [ ] Start with brute force if needed
- [ ] Optimize step by step
- [ ] Handle edge cases
- [ ] Test with examples

### 📋 After Solving
- [ ] Verify time complexity
- [ ] Check space complexity
- [ ] Test edge cases
- [ ] Review solution

## 🚀 Quick Tips

### 🎯 Problem-Solving
- **Start simple**: Don't overcomplicate
- **Test examples**: Always verify with small cases
- **Check constraints**: Choose algorithm accordingly
- **Handle edge cases**: Empty input, single element, etc.

### 🎯 Implementation
- **Use appropriate data structures**: Lists, sets, heaps, etc.
- **Optimize when needed**: Don't optimize prematurely
- **Write clean code**: Readable and maintainable
- **Add comments**: Explain complex logic

### 🎯 Learning
- **Practice regularly**: Consistency is key
- **Review solutions**: Understand why they work
- **Learn patterns**: Recognize common techniques
- **Build intuition**: Develop problem-solving sense

---

**Happy Problem Solving! 🚀**

*This ultimate cheatsheet combines all quick reference materials into one comprehensive guide for efficient problem-solving.* 