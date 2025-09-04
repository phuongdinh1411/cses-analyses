---
layout: simple
title: "Sorting And Searching Summary"
permalink: /problem_soulutions/sorting_and_searching/summary
---

# Sorting and Searching

Welcome to the Sorting and Searching section! This category covers fundamental algorithms for organizing and finding data efficiently.

## Problem Categories

### Basic Sorting
- [CSES Distinct Numbers](cses_distinct_numbers_analysis) - Count unique elements
- [CSES Apartments](cses_apartments_analysis) - Matching problem with sorting
- [CSES Stick Lengths](cses_stick_lengths_analysis) - Minimize differences
- [CSES Towers](cses_towers_analysis) - Building towers with constraints

### Two-Pointer Technique
- [CSES Sum of Two Values](cses_sum_of_two_values_analysis) - Find pair with given sum
- [Sum of Three Values](sum_of_three_values_analysis) - Find triplet with given sum
- [Sum of Four Values](sum_of_four_values_analysis) - Find quadruplet with given sum
- [Nearest Smaller Values](nearest_smaller_values_analysis) - Find nearest smaller elements

### Sliding Window
- [CSES Playlist](cses_playlist_analysis) - Maximum unique elements window
- [Subarray Sums I](subarray_sums_i_analysis) - Find subarrays with given sum
- [Subarray Sums II](subarray_sums_ii_analysis) - Advanced subarray sum problems
- [Subarray Divisibility](subarray_divisibility_analysis) - Divisible subarrays

### Binary Search
- [Factory Machines](factory_machines_analysis) - Binary search on answer
- [Array Division](array_division_analysis) - Divide array optimally
- [Sliding Median](sliding_median_analysis) - Maintain median in window

### Greedy Algorithms
- [CSES Movie Festival](cses_movie_festival_analysis) - Activity selection
- [Tasks and Deadlines](tasks_and_deadlines_analysis) - Optimal task scheduling
- [Reading Books](reading_books_analysis) - Minimize reading time

### Advanced Problems
- [Collecting Numbers](collecting_numbers_analysis) - Array traversal order
- [Collecting Numbers II](collecting_numbers_ii_analysis) - Dynamic array traversal
- [Collecting Numbers III](collecting_numbers_iii_analysis) - Complex array traversal
- [Collecting Numbers IV](collecting_numbers_iv_analysis) - Advanced array traversal
- [Collecting Numbers V](collecting_numbers_v_analysis) - Expert array traversal

### Range Problems
- [Nested Ranges Check](nested_ranges_check_analysis) - Check range containment
- [Nested Ranges Count](nested_ranges_count_analysis) - Count contained ranges
- [Room Allocation](room_allocation_analysis) - Minimize room allocations

### Specialized Problems
- [Josephus Problem I](josephus_problem_i_analysis) - Circular elimination game
- [Josephus Problem II](josephus_problem_ii_analysis) - Advanced elimination game
- [Traffic Lights](traffic_lights_analysis) - Dynamic range maintenance

## Learning Path

### For Beginners (Start Here)
1. Start with **CSES Distinct Numbers** for basic sorting
2. Move to **CSES Apartments** for simple matching
3. Try **CSES Sum of Two Values** for two-pointer technique
4. Learn sliding window with **CSES Playlist**

### Intermediate Level
1. Master binary search with **Factory Machines**
2. Practice greedy algorithms with **CSES Movie Festival**
3. Explore range problems with **Nested Ranges Check**
4. Study array traversal with **Collecting Numbers**

### Advanced Level
1. Challenge yourself with **Josephus Problems**
2. Master advanced array problems with **Collecting Numbers V**
3. Solve complex range problems with **Traffic Lights**
4. Tackle optimization with **Tasks and Deadlines**

## Key Concepts & Techniques

### Sorting Techniques

#### Comparison-Based Sorting
- **Quick Sort**: General-purpose sorting
  - *When to use*: General sorting, average case performance
  - *Time*: O(n log n) average, O(n²) worst case
  - *Space*: O(log n)
  - *Applications*: General sorting, in-place sorting
- **Merge Sort**: Stable sorting
  - *When to use*: When stability is required, guaranteed O(n log n)
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Stable sorting, external sorting
- **Heap Sort**: In-place sorting
  - *When to use*: When you need in-place O(n log n) sorting
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: In-place sorting, priority queues

#### Non-Comparison Sorting
- **Counting Sort**: Integer sorting
  - *When to use*: Small integer ranges, linear time needed
  - *Time*: O(n + k) where k is range
  - *Space*: O(k)
  - *Applications*: Integer sorting, frequency counting
- **Radix Sort**: Multi-digit sorting
  - *When to use*: Multi-digit numbers, strings
  - *Time*: O(d(n + k)) where d is digits
  - *Space*: O(n + k)
  - *Applications*: String sorting, multi-key sorting

#### Custom Sorting
- **Custom Comparators**: Special sorting criteria
  - *When to use*: When default ordering not suitable
  - *Implementation*: Define comparison function
  - *Applications*: Multi-criteria sorting, complex objects
- **Stable Sorting**: Preserve relative order
  - *When to use*: When relative order of equal elements matters
  - *Implementation*: Use stable algorithms (merge sort, counting sort)
  - *Applications*: Multi-key sorting, user experience

### Searching Algorithms

#### Binary Search
- **Standard Binary Search**: Find exact element
  - *When to use*: Sorted array, find specific value
  - *Time*: O(log n)
  - *Space*: O(1)
  - *Applications*: Element search, duplicate detection
- **Lower/Upper Bound**: Find insertion points
  - *When to use*: Find first/last occurrence, insertion position
  - *Time*: O(log n)
  - *Space*: O(1)
  - *Applications*: Range queries, insertion operations
- **Binary Search on Answer**: Find optimal value
  - *When to use*: Optimization problems, monotonic functions
  - *Time*: O(log n) per search
  - *Space*: O(1)
  - *Applications*: Optimization, decision problems

#### Two-Pointer Technique
- **Opposite Direction**: Start from ends
  - *When to use*: Sorted array, find pairs
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Two sum, palindrome checking
- **Same Direction**: Both pointers move forward
  - *When to use*: Sliding window, subarray problems
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Subarray sum, window problems
- **Fast and Slow**: Different speeds
  - *When to use*: Cycle detection, middle finding
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Cycle detection, linked list problems

#### Sliding Window
- **Fixed Size Window**: Constant window size
  - *When to use*: Fixed-size subarray problems
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Subarray sum, window statistics
- **Variable Size Window**: Dynamic window size
  - *When to use*: Optimization problems, constraint satisfaction
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Longest subarray, minimum window
- **Two-Pointer Window**: Expand/contract window
  - *When to use*: When window size depends on content
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Substring problems, optimization

### Data Structures for Sorting & Searching

#### Priority Queues (Heaps)
- **Min-Heap**: Smallest element at top
  - *When to use*: When you need minimum element
  - *Time*: O(log n) insert/extract
  - *Space*: O(n)
  - *Applications*: Dijkstra's algorithm, top-k problems
- **Max-Heap**: Largest element at top
  - *When to use*: When you need maximum element
  - *Time*: O(log n) insert/extract
  - *Space*: O(n)
  - *Applications*: Priority scheduling, max-k problems
- **Custom Heaps**: Custom comparison
  - *When to use*: When default ordering not suitable
  - *Time*: O(log n) insert/extract
  - *Space*: O(n)
  - *Applications*: Multi-criteria priority, complex objects

#### Sets and Maps
- **Hash Set/Map**: Fast lookup
  - *When to use*: When you need fast lookup/insertion
  - *Time*: O(1) average, O(n) worst case
  - *Space*: O(n)
  - *Applications*: Duplicate detection, frequency counting
- **Tree Set/Map**: Ordered data
  - *When to use*: When you need ordered data
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Range queries, ordered statistics
- **Multi-Set/Map**: Allow duplicates
  - *When to use*: When duplicates are allowed
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Frequency counting, multi-sets

#### Advanced Data Structures
- **Segment Tree**: Range queries
  - *When to use*: Range queries with updates
  - *Time*: O(log n) per query/update
  - *Space*: O(n)
  - *Applications*: Range sum/min/max, range updates
- **Binary Indexed Tree**: Point updates, range queries
  - *When to use*: Point updates with range queries
  - *Time*: O(log n) per query/update
  - *Space*: O(n)
  - *Applications*: Range sum, inversion counting
- **Ordered Set**: Dynamic ordered data
  - *When to use*: When you need dynamic ordered data
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Dynamic ranking, order statistics

### Specialized Techniques

#### Greedy Algorithms
- **Activity Selection**: Choose optimal activities
  - *When to use*: When you need to select non-overlapping activities
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: Scheduling, resource allocation
- **Huffman Coding**: Optimal prefix codes
  - *When to use*: When you need optimal compression
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Data compression, encoding
- **Fractional Knapsack**: Greedy knapsack
  - *When to use*: When you can take fractions of items
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: Resource allocation, optimization

#### Range Problems
- **Interval Scheduling**: Schedule non-overlapping intervals
  - *When to use*: When you need to schedule intervals
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: Meeting scheduling, resource allocation
- **Range Merging**: Merge overlapping ranges
  - *When to use*: When you need to merge overlapping intervals
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Calendar merging, interval analysis
- **Range Containment**: Check if ranges contain each other
  - *When to use*: When you need to check range relationships
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Range analysis, containment queries

### Optimization Techniques

#### Time Optimization
- **Precomputation**: Compute values once
  - *When to use*: When same calculations repeated
  - *Example*: Precompute prefix sums for range queries
- **Caching**: Store computed results
  - *When to use*: When calculations are expensive
  - *Example*: Cache sorted arrays for multiple searches
- **Early Termination**: Stop when condition met
  - *When to use*: When exact result not needed
  - *Example*: Stop binary search when range is small enough

#### Space Optimization
- **In-place Sorting**: Sort without extra space
  - *When to use*: When memory is limited
  - *Example*: Heap sort, quick sort
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy sorting, on-demand computation
- **Compression**: Reduce memory usage
  - *When to use*: When data has patterns
  - *Example*: Run-length encoding, delta compression

#### Algorithm Selection
- **Choose Right Algorithm**: Based on problem constraints
  - *When to use*: When multiple algorithms available
  - *Example*: Use counting sort for small ranges, merge sort for stability
- **Hybrid Approaches**: Combine multiple techniques
  - *When to use*: When single approach not optimal
  - *Example*: Introsort (quick sort + heap sort + insertion sort)
- **Adaptive Algorithms**: Adjust based on input
  - *When to use*: When input characteristics vary
  - *Example*: Adaptive quick sort, timsort

## Tips for Success

1. **Master Binary Search**: Essential for many problems
2. **Understand Two Pointers**: Key technique for arrays
3. **Practice Sliding Window**: Important pattern
4. **Learn Greedy Strategies**: Optimal local choices

## Common Pitfalls to Avoid

1. **Off-by-One Errors**: Be careful with array indices
2. **Integer Overflow**: Use appropriate data types
3. **Time Complexity**: Watch for inefficient solutions
4. **Edge Cases**: Consider boundary conditions

---

Ready to start? Begin with [CSES Distinct Numbers](cses_distinct_numbers_analysis) and work your way through the problems in order of difficulty!