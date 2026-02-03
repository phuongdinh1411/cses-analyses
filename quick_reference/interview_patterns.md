---
layout: simple
title: "Interview Patterns"
permalink: /quick_reference/interview_patterns
---

# Interview Patterns

Mapping common interview patterns to CSES problems for practice.

## Top 15 Interview Patterns

### 1. Two Pointers
**When to use**: Sorted arrays, finding pairs, palindromes

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Two Sum II | [Sum of Two Values](/problem_soulutions/sorting_and_searching/sum_of_two_values_analysis) | Opposite pointers on sorted array |
| 3Sum | [Sum of Three Values](/problem_soulutions/sorting_and_searching/sum_of_three_values_analysis) | Fix one, two-pointer on rest |
| Container With Most Water | - | Move pointer with smaller height |
| Trapping Rain Water | - | Track max from both sides |

**Interview Tips**:
- Always ask: "Is the array sorted?"
- Two pointers often reduce O(n^2) to O(n)
- Watch for duplicates handling

---

### 2. Sliding Window
**When to use**: Subarray/substring problems with constraints

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Longest Substring Without Repeating | [Playlist](/problem_soulutions/sorting_and_searching/playlist_analysis) | Expand right, shrink left on duplicate |
| Minimum Window Substring | [Minimum Window Substring](/problem_soulutions/sliding_window/minimum_window_substring_analysis) | Track character counts |
| Maximum Average Subarray | [Fixed Length Subarray Sum](/problem_soulutions/sliding_window/fixed_length_subarray_sum_analysis) | Fixed window |
| Subarray Sum Equals K | [Subarray Sums I](/problem_soulutions/sorting_and_searching/subarray_sums_i_analysis) | Prefix sum + hash map |

**Template**:
```python
def sliding_window(arr):
    left = 0
    for right in range(len(arr)):
        # Add arr[right] to window

        while window_is_invalid():
            # Remove arr[left] from window
            left += 1

        # Update answer with current window
```

---

### 3. Binary Search
**When to use**: Sorted data, finding boundaries, optimization

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Search in Rotated Sorted Array | - | Find pivot, then binary search |
| Find Minimum in Rotated Sorted Array | - | Binary search for pivot |
| Koko Eating Bananas | [Factory Machines](/problem_soulutions/sorting_and_searching/factory_machines_analysis) | Binary search on answer |
| Split Array Largest Sum | [Array Division](/problem_soulutions/sorting_and_searching/array_division_analysis) | Binary search on answer |

**Binary Search on Answer Pattern**:
```python
def binary_search_answer(lo, hi, is_feasible):
    while lo < hi:
        mid = (lo + hi) // 2
        if is_feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

### 4. BFS/DFS
**When to use**: Graph traversal, shortest path, connected components

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Number of Islands | [Counting Rooms](/problem_soulutions/graph_algorithms/counting_rooms_analysis) | DFS/BFS from each unvisited cell |
| Clone Graph | - | BFS with hash map for mapping |
| Word Ladder | [Labyrinth](/problem_soulutions/graph_algorithms/labyrinth_analysis) | BFS for shortest path |
| Course Schedule | [Topological Sorting](/problem_soulutions/graph_algorithms/topological_sorting_analysis) | DFS with cycle detection |

**BFS Template** (Shortest Path):
```python
from collections import deque

def bfs(graph, start, target):
    visited = {start}
    queue = deque([(start, 0)])

    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1
```

---

### 5. Dynamic Programming
**When to use**: Optimization, counting, overlapping subproblems

| Pattern | LeetCode Classic | CSES Equivalent |
|---------|-----------------|-----------------|
| Fibonacci | Climbing Stairs | [Dice Combinations](/problem_soulutions/dynamic_programming/dice_combinations_analysis) |
| Coin Change | Coin Change | [Minimizing Coins](/problem_soulutions/dynamic_programming/minimizing_coins_analysis) |
| LCS | Longest Common Subsequence | [LCS](/problem_soulutions/dynamic_programming/longest_common_subsequence_analysis) |
| LIS | Longest Increasing Subsequence | [Increasing Subsequence](/problem_soulutions/dynamic_programming/increasing_subsequence_analysis) |
| 0/1 Knapsack | Partition Equal Subset Sum | [Book Shop](/problem_soulutions/dynamic_programming/book_shop_analysis) |
| Grid DP | Unique Paths | [Grid Paths](/problem_soulutions/dynamic_programming/grid_paths_analysis) |

**DP Framework**:
1. Define state: What does `dp[i]` represent?
2. Find recurrence: How does `dp[i]` relate to smaller subproblems?
3. Set base cases
4. Define iteration order
5. Return answer

---

### 6. Backtracking
**When to use**: Generate all combinations, permutations, solutions

| LeetCode Classic | Pattern | Key Template |
|-----------------|---------|--------------|
| Subsets | Generate all subsets | Include/exclude each element |
| Permutations | Generate all orderings | Swap elements |
| Combination Sum | Find combinations to target | Prune when sum exceeds |
| N-Queens | Constraint satisfaction | Track constraints efficiently |

**Backtracking Template**:
```python
def backtrack(path, choices):
    if is_solution(path):
        results.append(path.copy())
        return

    for choice in choices:
        if is_valid(choice):
            path.append(choice)
            backtrack(path, remaining_choices)
            path.pop()  # Backtrack
```

---

### 7. Heap / Priority Queue
**When to use**: K-th largest/smallest, merge sorted lists, scheduling

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Kth Largest Element | - | Min-heap of size k |
| Merge K Sorted Lists | - | Min-heap of list heads |
| Meeting Rooms II | [Room Allocation](/problem_soulutions/sorting_and_searching/room_allocation_analysis) | Min-heap of end times |
| Find Median from Data Stream | - | Two heaps (max + min) |

**Heap Tips**:
- Python's `heapq` is min-heap
- For max-heap: negate values
- K-th largest: use min-heap of size k
- K-th smallest: use max-heap of size k

---

### 8. Union-Find
**When to use**: Connected components, cycle detection, dynamic connectivity

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Number of Connected Components | [Building Roads](/problem_soulutions/graph_algorithms/building_roads_analysis) | Union all edges |
| Redundant Connection | [Road Construction](/problem_soulutions/graph_algorithms/road_construction_analysis) | Cycle = union returns false |
| Accounts Merge | - | Union by common emails |

**Union-Find Template**:
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

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

---

### 9. Monotonic Stack
**When to use**: Next greater/smaller element, histogram problems

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Next Greater Element I | [Nearest Smaller Values](/problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis) | Decreasing stack |
| Largest Rectangle in Histogram | - | Stack + area calculation |
| Daily Temperatures | - | Store indices, decreasing stack |

**Pattern**:
- Next Greater: Decreasing stack
- Next Smaller: Increasing stack
- Pop when current breaks monotonicity

---

### 10. Trie (Prefix Tree)
**When to use**: Prefix matching, autocomplete, word search

| LeetCode Classic | Key Operations |
|-----------------|----------------|
| Implement Trie | insert, search, startsWith |
| Word Search II | DFS + Trie for multiple words |
| Longest Word in Dictionary | BFS on Trie |

---

### 11. Intervals
**When to use**: Scheduling, merging, overlapping

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Merge Intervals | - | Sort by start, merge overlapping |
| Insert Interval | - | Find position, merge |
| Non-overlapping Intervals | [Movie Festival](/problem_soulutions/sorting_and_searching/movie_festival_analysis) | Sort by end, greedy |
| Meeting Rooms | [Restaurant Customers](/problem_soulutions/sorting_and_searching/restaurant_customers_analysis) | Sweep line |

**Interval Tips**:
- Usually sort by start or end time
- Sweep line for counting overlaps
- Greedy (by end time) for maximum non-overlapping

---

### 12. Tree Traversal
**When to use**: Tree problems, path finding, subtree queries

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Maximum Depth of Binary Tree | [Tree Diameter](/problem_soulutions/tree_algorithms/tree_diameter_analysis) | DFS, return depth |
| Validate BST | - | Inorder traversal is sorted |
| Lowest Common Ancestor | [Company Queries II](/problem_soulutions/tree_algorithms/company_queries_ii_analysis) | Binary lifting or parent tracking |
| Path Sum | [Path Queries](/problem_soulutions/tree_algorithms/path_queries_analysis) | DFS with running sum |

---

### 13. Topological Sort
**When to use**: Dependencies, ordering constraints, DAG

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Course Schedule | [Topological Sorting](/problem_soulutions/graph_algorithms/topological_sorting_analysis) | Check if valid ordering exists |
| Course Schedule II | [Topological Sorting](/problem_soulutions/graph_algorithms/topological_sorting_analysis) | Return the ordering |
| Alien Dictionary | - | Build graph from constraints |

---

### 14. Bit Manipulation
**When to use**: Subsets, XOR properties, optimization

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Single Number | [Missing Number](/problem_soulutions/introductory_problems/missing_number_analysis) | XOR all elements |
| Subsets | [Apple Division](/problem_soulutions/introductory_problems/apple_division_analysis) | Bitmask enumeration |
| Counting Bits | - | DP with bit pattern |

**Useful Bit Operations**:
```python
x & (x - 1)    # Remove lowest set bit
x & (-x)       # Get lowest set bit
x | (1 << i)   # Set i-th bit
x & ~(1 << i)  # Clear i-th bit
(x >> i) & 1   # Get i-th bit
```

---

### 15. Math & Combinatorics
**When to use**: Counting problems, probability, number theory

| LeetCode Classic | CSES Equivalent | Key Insight |
|-----------------|-----------------|-------------|
| Unique Paths | [Grid Paths](/problem_soulutions/dynamic_programming/grid_paths_analysis) | Combinatorics: C(m+n-2, m-1) |
| Count Primes | - | Sieve of Eratosthenes |
| Pow(x, n) | [Bit Strings](/problem_soulutions/introductory_problems/bit_strings_analysis) | Binary exponentiation |

---

## Interview Problem-Solving Framework

### Step 1: Understand (3-5 minutes)
- Repeat the problem in your own words
- Ask clarifying questions
- Identify input/output format
- Note constraints

### Step 2: Examples (2-3 minutes)
- Walk through given examples
- Create edge case examples
- Verify understanding

### Step 3: Approach (5-10 minutes)
- Start with brute force
- Identify the pattern
- Propose optimized solution
- Discuss time/space complexity

### Step 4: Code (15-20 minutes)
- Write clean, readable code
- Use meaningful variable names
- Add comments for complex logic
- Handle edge cases

### Step 5: Test (5 minutes)
- Trace through with examples
- Test edge cases
- Fix bugs if any

---

## Common Follow-Up Questions

| Original Problem | Follow-Up | Technique |
|-----------------|-----------|-----------|
| Two Sum | Three Sum | Sort + Two Pointers |
| Two Sum | Two Sum with duplicates | Handle during iteration |
| Find Cycle | Find cycle start | Fast/slow pointers |
| BFS shortest path | Print the path | Track parent nodes |
| DP count ways | Print all ways | Backtracking |
| Find element | Find k elements | Heap |
| Range sum | Range update | Segment tree / BIT |

---

## Quick Pattern Recognition

```
+------------------+---------------------------+
| I see...         | I think...                |
+------------------+---------------------------+
| "subarray"       | Sliding Window / Prefix   |
| "shortest path"  | BFS / Dijkstra            |
| "connected"      | DFS / Union-Find          |
| "all permutations| Backtracking              |
| "k-th largest"   | Heap                      |
| "next greater"   | Monotonic Stack           |
| "dependencies"   | Topological Sort          |
| "minimum coins"  | DP                        |
| "intervals"      | Sort + Greedy             |
| "prefix match"   | Trie                      |
+------------------+---------------------------+
```

---

## Practice Recommendations

### Week 1-2: Arrays & Strings
Focus on: Two Pointers, Sliding Window, Binary Search

### Week 3-4: Trees & Graphs
Focus on: BFS, DFS, Tree Traversal

### Week 5-6: Dynamic Programming
Focus on: 1D DP, 2D DP, Common patterns

### Week 7-8: Advanced Topics
Focus on: Heaps, Union-Find, Backtracking

### Daily Practice
- 1 Easy (10-15 min)
- 1 Medium (20-30 min)
- Review 2 previously solved problems
