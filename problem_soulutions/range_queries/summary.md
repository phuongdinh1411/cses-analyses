---
layout: simple
title: "Range Queries Summary"
permalink: /problem_soulutions/range_queries/summary
---

# Range Queries

Welcome to the Range Queries section! This category covers efficient data structures and algorithms for handling queries on ranges of data.

## Problem Categories

### Static Range Queries
- [Static Range Sum Queries](static_range_sum_queries_analysis) - Basic prefix sums
- [Static Range Minimum Queries](static_range_minimum_queries_analysis) - Sparse table
- [Range XOR Queries](range_xor_queries_analysis) - XOR over ranges
- [Range Interval Queries](range_interval_queries_analysis) - Interval-based queries

### Dynamic Range Queries
- [Dynamic Range Sum Queries](dynamic_range_sum_queries_analysis) - Fenwick tree
- [Range Update Queries](range_update_queries_analysis) - Lazy propagation
- [Forest Queries](forest_queries_analysis) - 2D range sums
- [Hotel Queries](hotel_queries_analysis) - Binary search on segment tree

### Subarray Queries
- [Subarray Sum Queries](subarray_sum_queries_analysis) - Dynamic subarray sums
- [Subarray Minimum Queries](subarray_minimum_queries_analysis) - Range minimum
- [Subarray XOR Queries](subarray_xor_queries_analysis) - XOR operations
- [Subarray Distinct Values Queries](subarray_distinct_values_queries_analysis) - Distinct elements
- [Subarray Mode Queries](subarray_mode_queries_analysis) - Most frequent element
- [Subarray OR Queries](subarray_or_queries_analysis) - Bitwise OR

### Advanced Queries
- [List Removals](list_removals_analysis) - Dynamic array operations
- [Salary Queries](salary_queries_analysis) - Range counting
- [Prefix Sum Queries](prefix_sum_queries_analysis) - Advanced prefix sums
- [Pizzeria Queries](pizzeria_queries_analysis) - Distance queries
- [Visible Buildings Queries](visible_buildings_queries_analysis) - Geometric queries

## Learning Path

### For Beginners (Start Here)
1. Start with **Static Range Sum Queries** for basic concepts
2. Move to **Static Range Minimum Queries** for RMQ
3. Try **Dynamic Range Sum Queries** for updates
4. Learn 2D queries with **Forest Queries**

### Intermediate Level
1. Master segment trees with **Range Update Queries**
2. Practice subarray queries with **Subarray Sum Queries**
3. Explore distinct values with **Subarray Distinct Values Queries**
4. Study advanced operations with **Subarray OR Queries**

### Advanced Level
1. Challenge yourself with **Salary Queries**
2. Master complex queries with **Pizzeria Queries**
3. Solve geometric problems with **Visible Buildings Queries**
4. Tackle dynamic operations with **List Removals**

## Key Concepts & Techniques

### Data Structures

#### Prefix Sum Array
- **When to use**: Static range sum queries, no updates
- **Time**: O(n) preprocessing, O(1) per query
- **Space**: O(n)
- **Applications**: Range sum, range average, cumulative queries
- **Implementation**: `prefix[i] = prefix[i-1] + arr[i]`

#### Segment Tree
- **When to use**: Range queries with updates, flexible operations
- **Time**: O(n) construction, O(log n) per query/update
- **Space**: O(n)
- **Applications**: Range sum/min/max, range updates, custom operations
- **Implementation**: Binary tree with range information at each node

#### Fenwick Tree (Binary Indexed Tree)
- **When to use**: Point updates with range queries, space-efficient
- **Time**: O(n) construction, O(log n) per query/update
- **Space**: O(n)
- **Applications**: Range sum, point updates, inversion counting
- **Implementation**: Array with bit manipulation for indexing

#### Sparse Table
- **When to use**: Static range minimum/maximum queries, no updates
- **Time**: O(n log n) preprocessing, O(1) per query
- **Space**: O(n log n)
- **Applications**: Range minimum/maximum, GCD, range AND/OR
- **Implementation**: 2D array with powers of 2 ranges

#### Sqrt Decomposition
- **When to use**: Simple range queries, easy implementation
- **Time**: O(√n) per query/update
- **Space**: O(√n)
- **Applications**: Range sum, range updates, simple operations
- **Implementation**: Divide array into √n blocks

### Query Types & Operations

#### Range Sum Queries
- **When to use**: Summing elements in a range
- **Data Structure**: Prefix array, segment tree, Fenwick tree
- **Time**: O(1) with prefix, O(log n) with trees
- **Applications**: Subarray sums, cumulative statistics
- **Implementation**: `sum(l,r) = prefix[r] - prefix[l-1]`

#### Range Minimum/Maximum Queries (RMQ)
- **When to use**: Finding min/max in a range
- **Data Structure**: Sparse table, segment tree
- **Time**: O(1) with sparse table, O(log n) with segment tree
- **Applications**: Range statistics, optimization problems
- **Implementation**: Precompute min/max for all power-of-2 ranges

#### Range Update Queries
- **When to use**: Modifying all elements in a range
- **Data Structure**: Segment tree with lazy propagation
- **Time**: O(log n) per update
- **Space**: O(n)
- **Applications**: Range addition, range assignment
- **Implementation**: Defer updates until necessary

#### Point Update Queries
- **When to use**: Modifying single elements
- **Data Structure**: Segment tree, Fenwick tree
- **Time**: O(log n) per update
- **Applications**: Single element changes, dynamic arrays
- **Implementation**: Update leaf and propagate up

### Advanced Techniques

#### Lazy Propagation
- **When to use**: Range updates in segment trees
- **Time**: O(log n) per update, O(log n) per query
- **Space**: O(n)
- **Applications**: Range addition, range multiplication, range assignment
- **Implementation**: Store pending updates at internal nodes

#### Binary Search on Answer
- **When to use**: Finding optimal value in range
- **Time**: O(log n) per search
- **Space**: O(1)
- **Applications**: Finding k-th smallest, optimization problems
- **Implementation**: Binary search with range query check

#### Coordinate Compression
- **When to use**: Large coordinate ranges, discrete values
- **Time**: O(n log n) preprocessing
- **Space**: O(n)
- **Applications**: Large coordinate spaces, discrete optimization
- **Implementation**: Sort and map to smaller range

#### Mo's Algorithm
- **When to use**: Offline range queries, multiple queries
- **Time**: O((n+q)√n) where q is number of queries
- **Space**: O(n)
- **Applications**: Range distinct values, range frequency
- **Implementation**: Sort queries by block, use two pointers

### 2D Range Queries

#### 2D Prefix Sum
- **When to use**: 2D range sum queries, no updates
- **Time**: O(n²) preprocessing, O(1) per query
- **Space**: O(n²)
- **Applications**: Submatrix sums, image processing
- **Implementation**: `prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1] + arr[i][j]`

#### 2D Segment Tree
- **When to use**: 2D range queries with updates
- **Time**: O(n²) construction, O(log² n) per query/update
- **Space**: O(n²)
- **Applications**: 2D range operations, matrix queries
- **Implementation**: Segment tree of segment trees

#### 2D Fenwick Tree
- **When to use**: 2D point updates with range queries
- **Time**: O(n²) construction, O(log² n) per query/update
- **Space**: O(n²)
- **Applications**: 2D range sums, point updates
- **Implementation**: 2D array with 2D bit manipulation

### Specialized Data Structures

#### Persistent Segment Tree
- **When to use**: Version control, time-travel queries
- **Time**: O(log n) per query/update
- **Space**: O(n log n)
- **Applications**: Version history, temporal queries
- **Implementation**: Create new nodes for each update

#### Dynamic Segment Tree
- **When to use**: Large coordinate ranges, sparse data
- **Time**: O(log n) per query/update
- **Space**: O(n log n)
- **Applications**: Large ranges, sparse updates
- **Implementation**: Create nodes on demand

#### Merge Sort Tree
- **When to use**: Range counting, range k-th element
- **Time**: O(n log n) construction, O(log² n) per query
- **Space**: O(n log n)
- **Applications**: Range counting, range statistics
- **Implementation**: Segment tree with sorted arrays

#### Wavelet Tree
- **When to use**: Range k-th element, range counting
- **Time**: O(log n) per query
- **Space**: O(n log n)
- **Applications**: Range statistics, string processing
- **Implementation**: Binary tree based on bit values

### Optimization Techniques

#### Space Optimization
- **Rolling Arrays**: When only previous values needed
  - *When to use*: DP with range queries
  - *Example*: Range DP with rolling array
- **In-place Updates**: Modify array in place
  - *When to use*: When original array not needed
  - *Example*: In-place range updates

#### Time Optimization
- **Batch Processing**: Process multiple queries together
  - *When to use*: Offline queries
  - *Example*: Mo's algorithm for multiple queries
- **Precomputation**: Compute common values once
  - *When to use*: Repeated calculations
  - *Example*: Precompute powers for modular arithmetic

#### Memory Optimization
- **Lazy Allocation**: Allocate memory on demand
  - *When to use*: Sparse data structures
  - *Example*: Dynamic segment tree
- **Memory Pool**: Reuse allocated memory
  - *When to use*: Frequent allocation/deallocation
  - *Example*: Persistent segment tree with memory pool

## Tips for Success

1. **Master Prefix Sums**: Foundation for range queries
2. **Understand Segment Trees**: Most versatile structure
3. **Learn Lazy Propagation**: Essential for updates
4. **Practice Implementation**: Code data structures

## Common Pitfalls to Avoid

1. **Off-by-One Errors**: In range boundaries
2. **Memory Limits**: With large arrays
3. **Time Limits**: With inefficient updates
4. **Integer Overflow**: In sum calculations

## Advanced Topics

### Segment Tree Variations
- **Persistent Segment Tree**: Version control
- **Dynamic Segment Tree**: Space optimization
- **2D Segment Tree**: Matrix operations
- **Merge Sort Tree**: Range counting

### Optimization Techniques
- **Memory Optimization**: Space-efficient structures
- **Update Optimization**: Lazy propagation
- **Query Optimization**: Binary search
- **Batch Processing**: Offline algorithms

### Special Cases
- **Empty Ranges**: Handling edge cases
- **Large Numbers**: Modular arithmetic
- **Dynamic Ranges**: Online updates
- **Multiple Operations**: Combined queries

---

Ready to start? Begin with [Static Range Sum Queries](static_range_sum_queries_analysis) and work your way through the problems in order of difficulty!