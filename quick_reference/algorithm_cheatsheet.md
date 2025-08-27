# 🚀 CSES Algorithm Cheatsheet

## 📊 Quick Reference Guide

### 🎯 Dynamic Programming
| Problem Type | Algorithm | Time | Space | Key Pattern |
|-------------|-----------|------|-------|-------------|
| Coin Change | Unbounded Knapsack | O(n*target) | O(target) | `dp[i] += dp[i-coin]` |
| LIS | Binary Search | O(n log n) | O(n) | `bisect.bisect_left(dp, x)` |
| Grid Paths | 2D DP | O(m*n) | O(m*n) | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` |
| Edit Distance | String DP | O(m*n) | O(m*n) | `dp[i][j] = min(insert, delete, replace)` |

### 🌐 Graph Algorithms
| Problem Type | Algorithm | Time | Space | Key Pattern |
|-------------|-----------|------|-------|-------------|
| Shortest Path | Dijkstra | O((V+E) log V) | O(V) | `heapq.heappush(pq, (dist, node))` |
| All Pairs | Floyd-Warshall | O(V³) | O(V²) | `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` |
| SCC | Kosaraju | O(V+E) | O(V+E) | DFS + Transpose + DFS |
| Topological Sort | Kahn's | O(V+E) | O(V) | `indegree[node] == 0` |

### 🌳 Tree Algorithms
| Problem Type | Algorithm | Time | Space | Key Pattern |
|-------------|-----------|------|-------|-------------|
| LCA | Binary Lifting | O(log n) | O(n log n) | `parent[node][j] = parent[parent[node][j-1]][j-1]` |
| Tree Diameter | DFS | O(n) | O(n) | `max_depth + second_max_depth` |
| Tree DP | Post-order | O(n) | O(n) | `dfs(child) then combine results` |

### 🔍 Range Queries
| Problem Type | Algorithm | Time | Space | Key Pattern |
|-------------|-----------|------|-------|-------------|
| Static Sum | Prefix Sum | O(1) | O(n) | `prefix[r+1] - prefix[l]` |
| Dynamic Sum | Binary Indexed Tree | O(log n) | O(n) | `update(idx, val)` |
| Range Min | Segment Tree | O(log n) | O(4n) | `min(left_child, right_child)` |

### 📝 String Algorithms
| Problem Type | Algorithm | Time | Space | Key Pattern |
|-------------|-----------|------|-------|-------------|
| Pattern Matching | KMP | O(n+m) | O(m) | `build_lps(pattern)` |
| Palindrome | Manacher | O(n) | O(n) | `expand around center` |
| Suffix Array | SA-IS | O(n) | O(n) | `sort suffixes` |

### 🔍 Binary Search
| Problem Type | Algorithm | Time | Space | Key Pattern |
|-------------|-----------|------|-------|-------------|
| Find Element | Binary Search | O(log n) | O(1) | `left <= right` |
| Find Answer | Binary Search | O(log range) | O(1) | `while left < right` |
| Find Peak | Binary Search | O(log n) | O(1) | `nums[mid] > nums[mid+1]` |

### 👆 Two Pointers
| Problem Type | Algorithm | Time | Space | Key Pattern |
|-------------|-----------|------|-------|-------------|
| Sorted Array | Two Pointers | O(n) | O(1) | `left++ or right--` |
| Sliding Window | Two Pointers | O(n) | O(1) | `while condition: left++` |
| Linked List | Fast/Slow | O(n) | O(1) | `fast = fast.next.next` |

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
