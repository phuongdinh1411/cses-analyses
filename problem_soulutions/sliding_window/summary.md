---
layout: simple
title: "Sliding Window Summary"
permalink: /problem_soulutions/sliding_window/summary
---

# Sliding Window

Welcome to the Sliding Window section! This category covers efficient techniques for solving problems involving contiguous subarrays and substrings.

## Problem Categories

### Basic Sliding Window
- [Maximum Subarray Sum](maximum_subarray_sum_analysis) - Kadane's algorithm
- [Minimum Subarray Sum](minimum_subarray_sum_analysis) - Minimum sum window
- [Fixed Length Subarray Sum](fixed_length_subarray_sum_analysis) - Fixed size windows
- [Subarray with Given Sum](subarray_with_given_sum_analysis) - Target sum windows

### Window Properties
- [Subarray Maximums](subarray_maximums_analysis) - Maximum in windows
- [Subarray Minimums](subarray_minimums_analysis) - Minimum in windows
- [Subarray Distinct Values](subarray_distinct_values_analysis) - Unique elements
- [Subarray with K Distinct](subarray_with_k_distinct_analysis) - Exactly K distinct

### Sum Problems
- [Subarray Sums I](subarray_sums_i_analysis) - Basic sum windows
- [Subarray Sums II](subarray_sums_ii_analysis) - Advanced sum windows
- [Longest Subarray with Sum](longest_subarray_with_sum_analysis) - Maximum length
- [Shortest Subarray with Sum](shortest_subarray_with_sum_analysis) - Minimum length

### String Windows
- [Longest Substring Without Repeating](longest_substring_without_repeating_analysis) - Unique characters
- [Minimum Window Substring](minimum_window_substring_analysis) - Character coverage

### Advanced Applications
- [Sliding Window Advertisement](sliding_window_advertisement_analysis) - Real-world application

## Learning Path

### For Beginners (Start Here)
1. Start with **Maximum Subarray Sum** for basic concept
2. Move to **Fixed Length Subarray Sum** for fixed windows
3. Try **Subarray Sums I** for sum problems
4. Learn string windows with **Longest Substring Without Repeating**

### Intermediate Level
1. Master window properties with **Subarray Maximums**
2. Practice distinct values with **Subarray Distinct Values**
3. Explore sum problems with **Subarray Sums II**
4. Study length optimization with **Longest Subarray with Sum**

### Advanced Level
1. Challenge yourself with **Minimum Window Substring**
2. Master K distinct with **Subarray with K Distinct**
3. Solve complex sums with **Shortest Subarray with Sum**
4. Tackle real applications with **Sliding Window Advertisement**

## Key Concepts & Techniques

### Window Management

#### Window Size Types
- **Fixed Size Windows**: Constant length windows
  - *When to use*: When window size is predetermined
  - *Time*: O(n) where n is array length
  - *Space*: O(1) additional space
  - *Applications*: Fixed-size subarray problems, window statistics
  - *Implementation*: Maintain window boundaries, slide by one position
- **Variable Size Windows**: Dynamic length windows
  - *When to use*: When window size depends on content or constraints
  - *Time*: O(n) where n is array length
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Optimization problems, constraint satisfaction
  - *Implementation*: Expand/contract window based on conditions

#### Window Movement Techniques
- **Two Pointers**: Left and right boundaries
  - *When to use*: Most sliding window problems
  - *Time*: O(n) where n is array length
  - *Space*: O(1) additional space
  - *Applications*: Subarray problems, substring problems
  - *Implementation*: Move left/right pointers based on conditions
- **Sliding Technique**: Move window by one position
  - *When to use*: When you need to process all possible windows
  - *Time*: O(n) where n is array length
  - *Space*: O(1) additional space
  - *Applications*: Fixed-size windows, window statistics
  - *Implementation*: Remove leftmost element, add rightmost element

#### Window State Management
- **Property Maintenance**: Keep track of window properties
  - *When to use*: When you need to maintain window characteristics
  - *Time*: O(1) per update
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Distinct elements, sum maintenance, min/max tracking
  - *Implementation*: Use hash maps, counters, or data structures
- **State Updates**: Efficiently update window state
  - *When to use*: When window content changes
  - *Time*: O(1) per update
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Element counting, sum updates, property tracking
  - *Implementation*: Increment/decrement counters, update data structures

### Common Sliding Window Patterns

#### Two Pointers Technique
- **Opposite Direction**: Start from ends, move inward
  - *When to use*: Sorted arrays, find pairs
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Two sum, palindrome checking, sorted array problems
  - *Implementation*: Move pointers based on comparison
- **Same Direction**: Both pointers move forward
  - *When to use*: Sliding window, subarray problems
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Subarray sum, window problems, substring problems
  - *Implementation*: Move right pointer, adjust left pointer as needed

#### Hash Map for Counting
- **Element Frequency**: Count occurrences of elements
  - *When to use*: When you need to track element frequencies
  - *Time*: O(1) per update
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Distinct elements, frequency-based problems
  - *Implementation*: Use hash map to store element counts
- **Character Counting**: Count characters in string windows
  - *When to use*: String problems, character-based windows
  - *Time*: O(1) per update
  - *Space*: O(26) for lowercase letters
  - *Applications*: String problems, character frequency
  - *Implementation*: Use array or hash map for character counts

#### Monotonic Queue for Min/Max
- **Minimum Queue**: Maintain minimum in window
  - *When to use*: When you need minimum element in window
  - *Time*: O(1) amortized per operation
  - *Space*: O(n) in worst case
  - *Applications*: Sliding window minimum, optimization problems
  - *Implementation*: Use deque to maintain increasing order
- **Maximum Queue**: Maintain maximum in window
  - *When to use*: When you need maximum element in window
  - *Time*: O(1) amortized per operation
  - *Space*: O(n) in worst case
  - *Applications*: Sliding window maximum, optimization problems
  - *Implementation*: Use deque to maintain decreasing order

#### Prefix Sums for Quick Calculation
- **Range Sum**: Calculate sum of window quickly
  - *When to use*: When you need to calculate window sum frequently
  - *Time*: O(1) per query
  - *Space*: O(n) for prefix array
  - *Applications*: Subarray sum, window sum, range queries
  - *Implementation*: Precompute prefix sums, use difference for range
- **Cumulative Properties**: Track cumulative window properties
  - *When to use*: When you need cumulative window characteristics
  - *Time*: O(1) per update
  - *Space*: O(n) for prefix array
  - *Applications*: Cumulative sum, cumulative properties
  - *Implementation*: Maintain prefix array, update incrementally

### Advanced Sliding Window Techniques

#### Multiple Window Properties
- **Combined Conditions**: Multiple constraints on window
  - *When to use*: When window must satisfy multiple conditions
  - *Time*: O(n) where n is array length
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Complex window problems, multi-constraint problems
  - *Implementation*: Maintain multiple data structures for different properties
- **Nested Windows**: Windows within windows
  - *When to use*: When you need to consider nested window structures
  - *Time*: O(n²) in worst case
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Complex window problems, nested structures
  - *Implementation*: Use nested loops or recursive approaches

#### Optimization Techniques
- **State Compression**: Reduce memory usage
  - *When to use*: When memory is limited
  - *Time*: O(1) per update
  - *Space*: O(1) additional space
  - *Applications*: Memory-constrained problems, optimization
  - *Implementation*: Use bit manipulation or compact data structures
- **Lazy Updates**: Defer expensive operations
  - *When to use*: When updates are expensive
  - *Time*: O(1) per update, O(k) per query
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Expensive update operations, lazy evaluation
  - *Implementation*: Use lazy evaluation, batch updates

#### Specialized Data Structures
- **Ordered Set**: Maintain sorted order
  - *When to use*: When you need sorted window elements
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Sorted window problems, order statistics
  - *Implementation*: Use balanced binary search tree
- **Segment Tree**: Range queries on window
  - *When to use*: When you need range queries on window
  - *Time*: O(log n) per query/update
  - *Space*: O(n)
  - *Applications*: Range queries, window statistics
  - *Implementation*: Use segment tree for range operations

### Problem-Specific Techniques

#### Subarray Sum Problems
- **Target Sum**: Find subarray with given sum
  - *When to use*: When you need to find subarray with specific sum
  - *Time*: O(n)
  - *Space*: O(n) for hash map
  - *Applications*: Subarray sum, target sum problems
  - *Implementation*: Use hash map to store prefix sums
- **Maximum Sum**: Find subarray with maximum sum
  - *When to use*: When you need maximum sum subarray
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Maximum subarray sum, optimization
  - *Implementation*: Use Kadane's algorithm or sliding window

#### Distinct Elements Problems
- **K Distinct**: Find subarray with exactly K distinct elements
  - *When to use*: When you need subarray with specific number of distinct elements
  - *Time*: O(n)
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Distinct elements, counting problems
  - *Implementation*: Use hash map to count distinct elements
- **All Distinct**: Find subarray with all distinct elements
  - *When to use*: When you need subarray with all unique elements
  - *Time*: O(n)
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Unique elements, string problems
  - *Implementation*: Use hash map to track element presence

#### String Window Problems
- **Character Coverage**: Find window covering all characters
  - *When to use*: When you need window covering all required characters
  - *Time*: O(n)
  - *Space*: O(26) for lowercase letters
  - *Applications*: String problems, character coverage
  - *Implementation*: Use hash map to track character coverage
- **No Repeating**: Find window with no repeating characters
  - *When to use*: When you need window with unique characters
  - *Time*: O(n)
  - *Space*: O(26) for lowercase letters
  - *Applications*: String problems, unique characters
  - *Implementation*: Use hash map to track character frequency

### Optimization Strategies

#### Time Optimization
- **Early Termination**: Stop when condition met
  - *When to use*: When exact result not needed
  - *Example*: Stop when first valid window found
- **Batch Processing**: Process multiple windows together
  - *When to use*: When you need to process multiple windows
  - *Example*: Process all windows of same size together
- **Precomputation**: Compute values once
  - *When to use*: When same calculations repeated
  - *Example*: Precompute prefix sums for range queries

#### Space Optimization
- **In-place Updates**: Modify data in place
  - *When to use*: When original data not needed
  - *Example*: In-place window updates
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy window property computation
- **Memory Pool**: Reuse allocated memory
  - *When to use*: When memory allocation is expensive
  - *Example*: Reuse hash maps for different windows

## Tips for Success

1. **Master Two Pointers**: Essential technique
2. **Understand Window Properties**: What to maintain
3. **Learn State Management**: Efficient updates
4. **Practice Implementation**: Code common patterns

## Common Pitfalls to Avoid

1. **Window Boundaries**: Off-by-one errors
2. **State Updates**: Missing updates
3. **Memory Usage**: Inefficient storage
4. **Time Complexity**: Slow operations

## Advanced Topics

### Window Types
- **Fixed Size**: Constant length
- **Variable Size**: Dynamic length
- **Multiple Properties**: Combined conditions
- **Nested Windows**: Windows within windows

### Data Structures
- **Deque**: Efficient min/max
- **Hash Map**: Element counting
- **Segment Tree**: Range queries
- **Monotonic Queue**: Order maintenance

### Special Cases
- **Empty Windows**: Edge cases
- **Single Element**: Minimal windows
- **Full Array**: Maximum windows
- **No Solution**: Invalid cases

## Algorithm Complexities

### Basic Operations
- **Window Sliding**: O(1) per slide
- **Property Update**: O(1) typical
- **State Maintenance**: O(1) amortized
- **Result Calculation**: O(1) per window

### Advanced Operations
- **Distinct Counting**: O(1) amortized
- **Min/Max Maintenance**: O(1) amortized
- **Sum Calculation**: O(1) with prefix
- **String Processing**: O(1) per character

---

Ready to start? Begin with [Maximum Subarray Sum](maximum_subarray_sum_analysis) and work your way through the problems in order of difficulty!