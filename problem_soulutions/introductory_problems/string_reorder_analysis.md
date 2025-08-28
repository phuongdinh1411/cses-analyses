---
layout: simple
title: String Reorder Analysis
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
```cpp
string stringReorder(string s) {
    // Count character frequencies
    vector<int> freq(26, 0);
    for (char c : s) {
        freq[c - 'A']++;
    }
    
    // Construct lexicographically smallest string
    string result = "";
    for (int i = 0; i < 26; i++) {
        result += string(freq[i], 'A' + i);
    }
    
    return result;
}
```

### Method 2: Using Sort
```cpp
string stringReorderSort(string s) {
    // Sort the string directly
    sort(s.begin(), s.end());
    return s;
}
```

### Method 3: Bucket Sort
```cpp
string stringReorderBucket(string s) {
    // Use bucket sort for better performance
    vector<int> buckets(26, 0);
    
    // Count characters
    for (char c : s) {
        buckets[c - 'A']++;
    }
    
    // Construct result
    string result;
    for (int i = 0; i < 26; i++) {
        for (int j = 0; j < buckets[i]; j++) {
            result += ('A' + i);
        }
    }
    
    return result;
}
```

### Method 4: Priority Queue
```cpp
string stringReorderPQ(string s) {
    // Use priority queue (min heap)
    priority_queue<char, vector<char>, greater<char>> pq;
    
    // Add all characters to priority queue
    for (char c : s) {
        pq.push(c);
    }
    
    // Extract characters in sorted order
    string result = "";
    while (!pq.empty()) {
        result += pq.top();
        pq.pop();
    }
    
    return result;
}
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
```cpp
void stringReorderInplace(string& s) {
    // Count frequencies
    vector<int> freq(26, 0);
    for (char c : s) {
        freq[c - 'A']++;
    }
    
    // Reorder in-place
    int pos = 0;
    for (int i = 0; i < 26; i++) {
        for (int j = 0; j < freq[i]; j++) {
            s[pos++] = 'A' + i;
        }
    }
}
```

### 2. Bit Manipulation
```cpp
string stringReorderBit(string s) {
    // Use bit manipulation for small alphabets
    int freq = 0;
    
    // Count characters using bits
    for (char c : s) {
        freq += (1 << (c - 'A'));
    }
    
    // Extract characters in order
    string result = "";
    for (int i = 0; i < 26; i++) {
        if (freq & (1 << i)) {
            result += ('A' + i);
        }
    }
    
    return result;
}
```

### 3. Parallel Processing
```cpp
string stringReorderParallel(string s) {
    // For very large strings, use parallel processing
    // Divide string into chunks and process in parallel
    // Merge results
    
    // Implementation for parallel processing...
    return s;
}
```

### 4. Memory Efficient
```cpp
string stringReorderMemoryEfficient(string s) {
    // Use minimal extra memory
    sort(s.begin(), s.end());
    return s;
}
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
