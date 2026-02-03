---
layout: simple
title: "Pattern Recognition Guide"
permalink: /quick_reference/pattern_recognition
---

# Pattern Recognition Guide

Master the art of identifying which algorithm to use based on problem characteristics.

## Quick Decision Flowchart

```
START: Read problem carefully
            |
            v
    What is the INPUT?
            |
    +-------+-------+-------+-------+
    |       |       |       |       |
  Array   String   Graph   Tree   Number
    |       |       |       |       |
    v       v       v       v       v
  [A]     [S]     [G]     [T]     [N]
```

---

## [A] Array Problems

```
Array Problem
      |
      v
Is it about SUBARRAYS?
      |
+-----+-----+
|           |
YES         NO
|           |
v           v
[A1]      [A2]
```

### [A1] Subarray Problems

| If problem says... | Use this technique | Example |
|-------------------|-------------------|---------|
| "contiguous subarray with sum X" | Sliding Window / Prefix Sum + Hash | Subarray Sum Equals K |
| "longest/shortest subarray with property" | Two Pointers / Sliding Window | Longest Substring Without Repeat |
| "maximum/minimum subarray sum" | Kadane's Algorithm | Maximum Subarray |
| "count subarrays with property" | Prefix Sum + Hash Map | Count Subarrays with Sum |
| "subarray with k distinct elements" | Sliding Window + Hash Map | Subarrays with K Distinct |

**Decision Tree**:
```
Subarray Problem
       |
       v
All elements positive?
       |
+------+------+
|             |
YES           NO
|             |
v             v
Sliding     Prefix Sum
Window      + Hash Map
```

### [A2] Non-Subarray Array Problems

| If problem says... | Use this technique |
|-------------------|-------------------|
| "pair with sum X" (sorted) | Two Pointers |
| "pair with sum X" (unsorted) | Hash Map |
| "next greater/smaller element" | Monotonic Stack |
| "merge intervals" | Sort + Greedy |
| "k-th largest/smallest" | Heap / Quick Select |
| "majority element" | Boyer-Moore Voting |

---

## [S] String Problems

```
String Problem
      |
      v
What are you looking for?
      |
+-----+-----+-----+-----+
|     |     |     |     |
Pattern  Palindrome  Substring  Anagram
Match       |         Count      |
|           |           |        |
v           v           v        v
KMP/Z    Manacher   Suffix    Sliding
Algorithm   or DP    Array    Window
```

### Pattern Matching
| Scenario | Algorithm | Time |
|----------|-----------|------|
| Single pattern | KMP or Z-algorithm | O(n+m) |
| Multiple patterns | Aho-Corasick | O(n + total pattern length) |
| With wildcards | DP or Regex | Varies |

### Palindrome Problems
| Scenario | Algorithm |
|----------|-----------|
| Longest palindromic substring | Manacher's O(n) or DP O(n^2) |
| Palindrome partitioning | Backtracking + DP |
| Check if palindrome | Two Pointers |

### Substring/Subsequence
| Problem Type | Technique |
|--------------|-----------|
| Longest Common Subsequence | DP O(n*m) |
| Longest Common Substring | DP or Suffix Array |
| Count distinct substrings | Suffix Array |
| Shortest unique substring | Sliding Window |

---

## [G] Graph Problems

```
Graph Problem
      |
      v
What type of graph?
      |
+-----+-----+-----+
|     |     |     |
Unweighted  Weighted  DAG
    |          |       |
    v          v       v
  BFS/DFS  Dijkstra  Topo
           /Bellman  Sort
```

### Shortest Path Decision

| Graph Type | Negative Edges? | Single Source? | Algorithm |
|------------|-----------------|----------------|-----------|
| Unweighted | N/A | Yes | BFS |
| Weighted | No | Yes | Dijkstra |
| Weighted | Yes | Yes | Bellman-Ford |
| Weighted | Yes/No | All pairs | Floyd-Warshall |

### Connectivity Problems

| Problem | Algorithm |
|---------|-----------|
| "Are A and B connected?" | BFS/DFS or Union-Find |
| "Number of connected components" | DFS/BFS counting |
| "Minimum edges to connect all" | MST (Kruskal/Prim) |
| "Find bridges/articulation points" | Tarjan's Algorithm |
| "Strongly connected components" | Kosaraju's/Tarjan's |

### Special Graph Problems

| If problem involves... | Use |
|-----------------------|-----|
| Bipartite checking | BFS/DFS 2-coloring |
| Cycle detection (directed) | DFS with colors |
| Cycle detection (undirected) | Union-Find or DFS |
| Topological ordering | Kahn's or DFS |
| Maximum flow | Edmonds-Karp / Dinic |
| Eulerian path | Hierholzer's |

---

## [T] Tree Problems

```
Tree Problem
      |
      v
What operation?
      |
+-----+-----+-----+
|     |     |     |
Query   DP    Path
  |     |     Query
  v     v       |
LCA  Tree    +--+--+
     DP      |     |
            HLD  Euler
                 Tour
```

### Tree Query Problems

| Query Type | Technique |
|------------|-----------|
| Lowest Common Ancestor | Binary Lifting |
| Path sum/min/max | LCA + Precomputation |
| Subtree queries | Euler Tour + Segment Tree |
| Path updates | Heavy-Light Decomposition |
| k-th ancestor | Binary Lifting |

### Tree DP

| Pattern | State Definition |
|---------|------------------|
| Subtree problems | dp[node] = answer for subtree rooted at node |
| Include/exclude | dp[node][0/1] = answer with node excluded/included |
| Rerooting | Compute for one root, then update for others |

---

## [N] Number/Math Problems

```
Number Problem
      |
      v
What type?
      |
+-----+-----+-----+-----+
|     |     |     |     |
Count  Optimize  Prime  Combinatorics
ways    value    related    |
|        |        |         v
v        v        v      nCr/nPr
DP    Binary   Sieve    Factorials
      Search
```

### Counting Problems

| If counting... | Technique |
|----------------|-----------|
| Ways to reach target | DP |
| Permutations with constraints | Backtracking / DP |
| Combinations | nCr with modular inverse |
| Partitions | Partition DP |

### Optimization Problems

| Keywords | Technique |
|----------|-----------|
| "minimum/maximum satisfying condition" | Binary Search on Answer |
| "optimal way to do X" | DP or Greedy |
| "minimum cost" | Dijkstra / DP |

---

## Keyword-to-Algorithm Mapping

### High-Confidence Keywords

| Keyword/Phrase | Algorithm | Confidence |
|----------------|-----------|------------|
| "shortest path" | BFS/Dijkstra/Bellman-Ford | Very High |
| "topological order" | Kahn's / DFS | Very High |
| "connected components" | DFS/BFS/Union-Find | Very High |
| "lowest common ancestor" | Binary Lifting | Very High |
| "next greater element" | Monotonic Stack | Very High |
| "longest increasing subsequence" | DP + Binary Search | Very High |
| "minimum spanning tree" | Kruskal's / Prim's | Very High |

### Medium-Confidence Keywords

| Keyword/Phrase | Likely Algorithm | Consider Also |
|----------------|------------------|---------------|
| "subarray" | Sliding Window | Prefix Sum, DP |
| "substring" | Sliding Window | DP, Suffix structures |
| "palindrome" | Two Pointers/DP | Manacher's |
| "anagram" | Sorting/Hash Map | Sliding Window |
| "parentheses" | Stack | DP |
| "intervals" | Sorting + Greedy | Sweep Line |

### Constraint-Based Selection

| Constraint | Max Complexity | Suitable Algorithms |
|------------|----------------|---------------------|
| n <= 10 | O(n!) | Brute force, All permutations |
| n <= 20 | O(2^n) | Bitmask DP, Backtracking |
| n <= 500 | O(n^3) | Floyd-Warshall, Interval DP |
| n <= 5000 | O(n^2) | Simple DP, Nested loops |
| n <= 10^5 | O(n log n) | Sorting, Binary Search, Segment Tree |
| n <= 10^6 | O(n) | Linear scan, Two Pointers |
| n <= 10^9 | O(log n) | Binary Search, Math formula |

---

## Common Patterns by Problem Type

### Two Sum Variants

| Variant | Solution |
|---------|----------|
| Two Sum (unsorted) | Hash Map O(n) |
| Two Sum (sorted) | Two Pointers O(n) |
| Three Sum | Sort + Two Pointers O(n^2) |
| Four Sum | Sort + Two Pointers O(n^3) |
| Two Sum BST | Inorder + Two Pointers |

### Sliding Window Indicators

**Use Sliding Window when**:
- Looking for subarrays/substrings
- Need contiguous elements
- Have a constraint on window (size, sum, distinct count)
- Can answer "add element" and "remove element" efficiently

### DP Indicators

**Use DP when**:
- Problem asks for count/optimization
- Has overlapping subproblems
- Has optimal substructure
- Keywords: "minimum", "maximum", "count ways", "possible"

### Binary Search Indicators

**Use Binary Search when**:
- Array is sorted
- Looking for boundary (first/last occurrence)
- Answer has monotonic property
- Keywords: "minimum X such that", "maximum X satisfying"

---

## Practice Problems by Pattern

### Binary Search on Answer
1. [Factory Machines](/problem_soulutions/sorting_and_searching/factory_machines_analysis)
2. [Array Division](/problem_soulutions/sorting_and_searching/array_division_analysis)

### Sliding Window
1. [Playlist](/problem_soulutions/sorting_and_searching/playlist_analysis)
2. [Maximum Subarray Sum II](/problem_soulutions/sliding_window/maximum_subarray_sum_ii_analysis)

### Monotonic Stack
1. [Nearest Smaller Values](/problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis)

### Graph BFS/DFS
1. [Counting Rooms](/problem_soulutions/graph_algorithms/counting_rooms_analysis)
2. [Labyrinth](/problem_soulutions/graph_algorithms/labyrinth_analysis)

### Tree DP
1. [Subordinates](/problem_soulutions/tree_algorithms/subordinates_analysis)
2. [Tree Matching](/problem_soulutions/tree_algorithms/tree_matching_analysis)

---

## Quick Reference Card

```
+------------------+-------------------+------------------+
| I SEE...         | I THINK...        | I USE...         |
+------------------+-------------------+------------------+
| Sorted array     | Binary search     | bisect_left/right|
| Subarray sum     | Prefix sum        | prefix[r]-prefix[l]|
| Next greater     | Monotonic stack   | while stack and..|
| Shortest path    | BFS (unweighted)  | deque + visited  |
| Min/max path     | Dijkstra          | heapq + distance |
| All pairs        | Floyd-Warshall    | 3 nested loops   |
| Connected?       | Union-Find        | find + union     |
| Count ways       | DP                | dp[i] = ...      |
| Distinct items   | Hash Set          | set()            |
| Frequency        | Hash Map          | Counter/dict     |
+------------------+-------------------+------------------+
```
