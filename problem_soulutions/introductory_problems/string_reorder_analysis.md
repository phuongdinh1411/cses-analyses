---
layout: simple
title: "String Reorder Analysis"
permalink: /problem_soulutions/introductory_problems/string_reorder_analysis/
---


# String Reorder Analysis

## Problem Description

Given a string, find the lexicographically smallest string that can be obtained by reordering its characters.

## Key Insights

### 1. Lexicographical Order
- **Definition**: String A is lexicographically smaller than B if A comes before B in dictionary order
- **Comparison**: Compare characters from left to right
- **Strategy**: Place smallest characters first

### 2. Character Frequency
- Count frequency of each character
- Sort characters by their ASCII values
- Place characters in sorted order

### 3. Implementation Strategy
- Use frequency counting to handle duplicates
- Sort characters or use bucket sort
- Construct result string systematically

## Solution Approach

### Method 1: Sort and Count
```python
def string_reorder(s):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct lexicographically smallest string
    result = ""
    for i in range(26):
        result += chr(ord('A') + i) * freq[i]
    
    return result
```

### Method 2: Using Sort
```python
def string_reorder_sort(s):
    # Sort the string directly
    return ''.join(sorted(s))
```

### Method 3: Bucket Sort
```python
def string_reorder_bucket(s):
    # Use bucket sort for better performance
    buckets = [0] * 26
    
    # Count characters
    for c in s:
        buckets[ord(c) - ord('A')] += 1
    
    # Construct result
    result = ""
    for i in range(26):
        result += chr(ord('A') + i) * buckets[i]
    
    return result
```

### Method 4: Priority Queue
```python
import heapq

def string_reorder_pq(s):
    # Use priority queue (min heap)
    pq = []
    
    # Add all characters to priority queue
    for c in s:
        heapq.heappush(pq, c)
    
    # Extract characters in sorted order
    result = ""
    while pq:
        result += heapq.heappop(pq)
    
    return result
```

## Time Complexity
- **Method 1**: O(n) - where n is string length
- **Method 2**: O(n log n) - sorting
- **Method 3**: O(n) - bucket sort
- **Method 4**: O(n log n) - priority queue operations

## Example Walkthrough

**Input**: "CAB"

**Process**:
1. Count frequencies: A=1, B=1, C=1
2. Place characters in sorted order: A, B, C
3. Construct result: "ABC"

**Output**: "ABC"

## Problem Variations

### Variation 1: Case Insensitive
**Problem**: Ignore case when ordering.

**Solution**: Convert to same case before processing.

### Variation 2: Custom Ordering
**Problem**: Use custom character ordering.

**Approach**: Define custom comparison function.

### Variation 3: K-th Lexicographical
**Problem**: Find k-th lexicographically smallest reordering.

**Solution**: Use next_permutation or mathematical counting.

### Variation 4: Constrained Reordering
**Problem**: Some characters must maintain relative order.

**Approach**: Use stable sort or topological sorting.

### Variation 5: Weighted Characters
**Problem**: Each character has a weight. Find minimum weight reordering.

**Solution**: Sort by weight instead of character value.

### Variation 6: Multiple Strings
**Problem**: Reorder multiple strings to minimize total lexicographical order.

**Approach**: Use dynamic programming or greedy strategy.

## Advanced Optimizations

### 1. In-place Reordering
```python
def string_reorder_inplace(s):
    # Convert to list for in-place modification
    s_list = list(s)
    
    # Count frequencies
    freq = [0] * 26
    for c in s_list:
        freq[ord(c) - ord('A')] += 1
    
    # Reorder in-place
    pos = 0
    for i in range(26):
        for j in range(freq[i]):
            s_list[pos] = chr(ord('A') + i)
            pos += 1
    
    return ''.join(s_list)
```

### 2. Bit Manipulation
```python
def string_reorder_bit(s):
    # Use bit manipulation for small alphabets
    freq = 0
    
    # Count characters using bits
    for c in s:
        freq += (1 << (ord(c) - ord('A')))
    
    # Extract characters in order
    result = ""
    for i in range(26):
        if freq & (1 << i):
            result += chr(ord('A') + i)
    
    return result
```

### 3. Parallel Processing
```python
def string_reorder_parallel(s):
    # For very large strings, use parallel processing
    # Divide string into chunks and process in parallel
    # Merge results
    
    # Implementation for parallel processing...
    return ''.join(sorted(s))
```

### 4. Memory Efficient
```python
def string_reorder_memory_efficient(s):
    # Use minimal extra memory
    return ''.join(sorted(s))
```

## Related Problems
- [Creating Strings](../creating_strings_analysis/)
- [Palindrome Reorder](../palindrome_reorder_analysis/)
- [Permutations](../permutations_analysis/)

## Practice Problems
1. **CSES**: String Reorder
2. **LeetCode**: Similar string manipulation problems
3. **AtCoder**: Sorting and reordering problems

## Key Takeaways
1. **Lexicographical order** is based on character comparison
2. **Frequency counting** is efficient for character reordering
3. **Bucket sort** provides optimal time complexity
4. **In-place reordering** saves memory
5. **Custom ordering** requires custom comparison functions
6. **Edge cases** like empty strings need handling
7. **Performance optimization** depends on input size and constraints
