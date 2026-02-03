---
layout: simple
title: "Learning Roadmap"
permalink: /quick_reference/learning_roadmap
---

# Learning Roadmap

A structured path to master Data Structures & Algorithms, from beginner to advanced.

## Visual Learning Path

```
                    START HERE
                        |
                        v
            +-------------------+
            |  1. FOUNDATIONS   |
            |  (Weeks 1-4)      |
            +-------------------+
                        |
        +---------------+---------------+
        |                               |
        v                               v
+---------------+               +---------------+
| Arrays &      |               | Basic Math &  |
| Strings       |               | Bit Manip     |
+---------------+               +---------------+
        |                               |
        +---------------+---------------+
                        |
                        v
            +-------------------+
            |  2. CORE PATTERNS |
            |  (Weeks 5-12)     |
            +-------------------+
                        |
    +-------+-------+-------+-------+
    |       |       |       |       |
    v       v       v       v       v
+------+ +------+ +------+ +------+ +------+
|Binary| | Two  | |Sliding| |Hash | |Stack |
|Search| |Pointer| |Window| | Map | |Queue |
+------+ +------+ +------+ +------+ +------+
                        |
                        v
            +-------------------+
            |  3. INTERMEDIATE  |
            |  (Weeks 13-24)    |
            +-------------------+
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
+---------------+ +---------------+ +---------------+
| Dynamic       | | Graph         | | Tree          |
| Programming   | | Algorithms    | | Algorithms    |
+---------------+ +---------------+ +---------------+
                        |
                        v
            +-------------------+
            |  4. ADVANCED      |
            |  (Weeks 25-36)    |
            +-------------------+
                        |
    +-------+-------+-------+-------+
    |       |       |       |       |
    v       v       v       v       v
+------+ +------+ +------+ +------+ +------+
|Segment| |String| |Geometry| |Advanced| |Number|
| Tree  | | Algo | |        | | Graph  | |Theory|
+------+ +------+ +------+ +------+ +------+
                        |
                        v
                    MASTERY!
```

## Phase 1: Foundations (Weeks 1-4)

### Week 1-2: Arrays & Basic Operations
**Goal**: Understand array manipulation and time complexity

| Topic | Key Concepts | CSES Problems | LeetCode Problems |
|-------|--------------|---------------|-------------------|
| Array Basics | Traversal, modification | [Weird Algorithm](/problem_soulutions/introductory_problems/weird_algorithm_analysis) | Two Sum, Best Time to Buy and Sell Stock |
| Prefix Sums | Range queries | [Static Range Sum](/problem_soulutions/range_queries/static_range_sum_queries_analysis) | Running Sum, Subarray Sum Equals K |
| Basic Sorting | Comparison sorts | [Distinct Numbers](/problem_soulutions/sorting_and_searching/distinct_numbers_analysis) | Sort an Array |

**Practice Checklist**:
- [ ] Implement array reversal in O(n)
- [ ] Calculate prefix sums
- [ ] Use sorting to solve problems

### Week 3-4: Math & Bit Manipulation
**Goal**: Master number theory basics and bit operations

| Topic | Key Concepts | CSES Problems | LeetCode Problems |
|-------|--------------|---------------|-------------------|
| Modular Arithmetic | MOD operations | [Bit Strings](/problem_soulutions/introductory_problems/bit_strings_analysis) | Pow(x, n) |
| GCD/LCM | Euclidean algorithm | [Common Divisors](/problem_soulutions/counting_problems/counting_combinations_analysis) | GCD of Strings |
| Bit Operations | AND, OR, XOR, shifts | [Missing Number](/problem_soulutions/introductory_problems/missing_number_analysis) | Single Number, Counting Bits |

---

## Phase 2: Core Patterns (Weeks 5-12)

### Week 5-6: Binary Search
**Goal**: Master binary search variants

```
Binary Search Decision Tree:
                Is array sorted?
                     |
            +--------+--------+
            |                 |
           YES               NO
            |                 |
    Standard Binary     Can you define
       Search           monotonic property?
            |                 |
            v           +-----+-----+
    Find exact      YES           NO
    element          |             |
                Binary Search   Use other
                on Answer       technique
```

| Topic | Key Concepts | CSES Problems |
|-------|--------------|---------------|
| Standard Search | Find element | [Apartments](/problem_soulutions/sorting_and_searching/apartments_analysis) |
| Lower/Upper Bound | First/last occurrence | [Concert Tickets](/problem_soulutions/sorting_and_searching/concert_tickets_analysis) |
| Binary Search on Answer | Min/max satisfying condition | [Factory Machines](/problem_soulutions/sorting_and_searching/factory_machines_analysis) |

### Week 7-8: Two Pointers
**Goal**: Master pointer techniques

| Pattern | When to Use | CSES Problems |
|---------|-------------|---------------|
| Opposite Direction | Sorted arrays, palindromes | [Sum of Two Values](/problem_soulutions/sorting_and_searching/sum_of_two_values_analysis) |
| Same Direction | Subarrays, windows | [Ferris Wheel](/problem_soulutions/sorting_and_searching/ferris_wheel_analysis) |
| Fast & Slow | Cycle detection | [Planets Cycles](/problem_soulutions/graph_algorithms/planets_cycles_analysis) |

### Week 9-10: Sliding Window
**Goal**: Solve subarray/substring problems efficiently

| Pattern | Template | CSES Problems |
|---------|----------|---------------|
| Fixed Window | Maintain window of size k | [Maximum Subarray Sum II](/problem_soulutions/sliding_window/maximum_subarray_sum_ii_analysis) |
| Variable Window | Expand/contract based on condition | [Playlist](/problem_soulutions/sorting_and_searching/playlist_analysis) |
| With Hash Map | Track element frequencies | [Subarray Distinct Values](/problem_soulutions/sliding_window/subarray_distinct_values_analysis) |

### Week 11-12: Hash Maps & Stacks
**Goal**: Use hash-based and stack-based solutions

| Topic | Key Concepts | CSES Problems |
|-------|--------------|---------------|
| Hash Map Counting | Frequency tracking | [Subarray Sums I](/problem_soulutions/sorting_and_searching/subarray_sums_i_analysis) |
| Monotonic Stack | Next greater/smaller | [Nearest Smaller Values](/problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis) |
| Stack Applications | Parentheses, evaluation | Tower problems |

---

## Phase 3: Intermediate (Weeks 13-24)

### Week 13-16: Dynamic Programming
**Goal**: Master DP patterns

```
DP Decision Tree:
            Does problem have optimal substructure?
                        |
                +-------+-------+
                |               |
               YES             NO
                |               |
        Does it have      Use other
        overlapping       technique
        subproblems?
                |
        +-------+-------+
        |               |
       YES             NO
        |               |
    Use DP        Use Divide
    (memoize)     & Conquer
```

**DP Progression Path**:
1. **1D DP**: [Dice Combinations](/problem_soulutions/dynamic_programming/dice_combinations_analysis) → [Coin Combinations](/problem_soulutions/dynamic_programming/coin_combinations_i_analysis)
2. **2D DP**: [Grid Paths](/problem_soulutions/dynamic_programming/grid_paths_analysis) → [Edit Distance](/problem_soulutions/dynamic_programming/edit_distance_analysis)
3. **Knapsack**: [Book Shop](/problem_soulutions/dynamic_programming/book_shop_analysis) → [Money Sums](/problem_soulutions/dynamic_programming/money_sums_analysis)
4. **Interval DP**: [Removal Game](/problem_soulutions/dynamic_programming/removal_game_analysis)

### Week 17-20: Graph Algorithms
**Goal**: Master graph traversal and shortest paths

**Graph Learning Path**:
```
BFS/DFS → Shortest Paths → MST → Advanced
    |           |            |        |
    v           v            v        v
Counting    Dijkstra     Kruskal's  SCC
Rooms       Bellman-Ford  Prim's    Topological
Labyrinth   Floyd-Warshall         Sort
```

| Week | Topics | CSES Problems |
|------|--------|---------------|
| 17 | BFS/DFS basics | [Counting Rooms](/problem_soulutions/graph_algorithms/counting_rooms_analysis), [Labyrinth](/problem_soulutions/graph_algorithms/labyrinth_analysis) |
| 18 | Shortest paths | [Shortest Routes I](/problem_soulutions/graph_algorithms/shortest_routes_i_analysis), [Message Route](/problem_soulutions/graph_algorithms/message_route_analysis) |
| 19 | Connectivity | [Building Roads](/problem_soulutions/graph_algorithms/building_roads_analysis), [Road Reparation](/problem_soulutions/graph_algorithms/road_reparation_analysis) |
| 20 | Advanced | [Topological Sorting](/problem_soulutions/graph_algorithms/topological_sorting_analysis), [SCC](/problem_soulutions/graph_algorithms/strongly_connected_components_analysis) |

### Week 21-24: Tree Algorithms
**Goal**: Master tree traversal and queries

| Topic | Key Concepts | CSES Problems |
|-------|--------------|---------------|
| Tree Traversal | DFS, BFS on trees | [Subordinates](/problem_soulutions/tree_algorithms/subordinates_analysis) |
| Tree DP | DP on tree structure | [Tree Matching](/problem_soulutions/tree_algorithms/tree_matching_analysis) |
| LCA | Binary lifting | [Company Queries II](/problem_soulutions/tree_algorithms/company_queries_ii_analysis) |
| Path Queries | Euler tour, HLD | [Path Queries](/problem_soulutions/tree_algorithms/path_queries_analysis) |

---

## Phase 4: Advanced (Weeks 25-36)

### Week 25-28: Range Queries
| Topic | Data Structure | CSES Problems |
|-------|----------------|---------------|
| Point Updates | Fenwick Tree (BIT) | [Dynamic Range Sum](/problem_soulutions/range_queries/dynamic_range_sum_queries_analysis) |
| Range Updates | Segment Tree + Lazy | [Range Update Queries](/problem_soulutions/range_queries/range_update_queries_analysis) |
| 2D Queries | 2D Structures | [Forest Queries](/problem_soulutions/range_queries/forest_queries_analysis) |

### Week 29-32: String Algorithms
| Topic | Algorithm | CSES Problems |
|-------|-----------|---------------|
| Pattern Matching | KMP, Z-algorithm | [String Matching](/problem_soulutions/string_algorithms/string_matching_analysis) |
| Palindromes | Manacher's | [Longest Palindrome](/problem_soulutions/string_algorithms/longest_palindrome_analysis) |
| Suffix Structures | Suffix Array | [Distinct Substrings](/problem_soulutions/string_algorithms/distinct_substrings_analysis) |

### Week 33-36: Geometry & Advanced Topics
| Topic | Key Concepts | CSES Problems |
|-------|--------------|---------------|
| Basic Geometry | Cross product, convex hull | [Convex Hull](/problem_soulutions/geometry/convex_hull_analysis) |
| Advanced Graph | Max flow, 2-SAT | [Download Speed](/problem_soulutions/graph_algorithms/download_speed_analysis) |
| Counting | Combinatorics | [Counting Problems](/problem_soulutions/counting_problems/summary) |

---

## Daily Practice Schedule

### Weekday (1-2 hours)
```
30 min: Review previous concepts
45 min: Solve 1-2 new problems
15 min: Study solution if stuck
```

### Weekend (3-4 hours)
```
1 hour: Virtual contest or timed practice
1 hour: Learn new technique
1 hour: Solve medium/hard problems
1 hour: Review and make notes
```

---

## Progress Tracking

### Skill Checkpoints

**Beginner Complete When**:
- [ ] Can solve any array/string manipulation in O(n)
- [ ] Understand Big-O notation
- [ ] Know when to use each basic data structure

**Intermediate Complete When**:
- [ ] Can identify DP problems and write recurrence
- [ ] Can implement BFS/DFS from scratch
- [ ] Can use binary search on answer

**Advanced Complete When**:
- [ ] Can implement segment tree with lazy propagation
- [ ] Can solve graph problems with multiple algorithms
- [ ] Can identify and apply string algorithms

---

## Resources by Phase

### Phase 1
- [Introductory Problems](/problem_soulutions/introductory_problems/summary)
- Basic complexity analysis

### Phase 2
- [Sorting and Searching](/problem_soulutions/sorting_and_searching/summary)
- [Sliding Window](/problem_soulutions/sliding_window/summary)

### Phase 3
- [Dynamic Programming](/problem_soulutions/dynamic_programming/summary)
- [Graph Algorithms](/problem_soulutions/graph_algorithms/summary)
- [Tree Algorithms](/problem_soulutions/tree_algorithms/summary)

### Phase 4
- [Range Queries](/problem_soulutions/range_queries/summary)
- [String Algorithms](/problem_soulutions/string_algorithms/summary)
- [Geometry](/problem_soulutions/geometry/summary)

---

**Remember**: Consistency beats intensity. 1 hour daily is better than 7 hours once a week!
