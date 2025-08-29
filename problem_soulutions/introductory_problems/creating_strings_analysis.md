---
layout: simple
title: "Creating Strings Analysis"
permalink: /cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis
---


# Creating Strings Analysis

## Problem Description

Given a string, find all distinct strings that can be created by reordering its characters. Output the number of distinct strings and list them in lexicographical order.

## Key Insights

### 1. Permutation Generation
- **Distinct permutations**: Handle duplicate characters correctly
- **Lexicographical order**: Generate permutations in sorted order
- **Efficiency**: Avoid generating duplicate permutations

### 2. Mathematical Formula
- **Total permutations**: n! / (f1! × f2! × ... × fk!)
- Where n is string length and fi is frequency of character i
- **Distinct count**: Use multinomial coefficient

### 3. Implementation Strategy
- Use next_permutation for lexicographical generation
- Handle duplicates by sorting first
- Count distinct permutations efficiently

## Solution Approach

### Method 1: Using itertools.permutations
```python
from itertools import permutations

def create_strings(s):
    result = []
    
    # Sort string to get lexicographically smallest permutation
    s_sorted = ''.join(sorted(s))
    
    # Generate all permutations
    for perm in permutations(s_sorted):
        result.append(''.join(perm))
    
    return result

def count_distinct_strings(s):
    from collections import Counter
    from math import factorial
    
    # Count character frequencies
    freq = Counter(s)
    
    # Calculate multinomial coefficient
    n = len(s)
    result = factorial(n)
    
    # Divide by factorial of each frequency
    for count in freq.values():
        if count > 1:
            result //= factorial(count)
    
    return result
```

### Method 2: Recursive Generation
```python
class StringCreator:
    def __init__(self):
        self.result = []
        self.current = []
        self.freq = {}
    
    def generate(self, pos, n):
        if pos == n:
            self.result.append(''.join(self.current))
            return
        
        for char in self.freq:
            if self.freq[char] > 0:
                self.freq[char] -= 1
                self.current[pos] = char
                self.generate(pos + 1, n)
                self.freq[char] += 1
    
    def create_strings_recursive(self, s):
        # Count frequencies
        self.freq = {}
        for c in s:
            self.freq[c] = self.freq.get(c, 0) + 1
        
        self.current = [''] * len(s)
        self.generate(0, len(s))
        return self.result
```

### Method 3: Iterative with Duplicate Handling
```python
from itertools import permutations

def create_strings_iterative(s):
    result = []
    
    # Sort to handle duplicates correctly
    s_sorted = ''.join(sorted(s))
    
    # Generate permutations and skip duplicates
    seen = set()
    for perm in permutations(s_sorted):
        perm_str = ''.join(perm)
        if perm_str not in seen:
            result.append(perm_str)
            seen.add(perm_str)
    
    return result
``` 
               result.back() == s) {
            // Skip duplicates
        }
    } while (next_permutation(s.begin(), s.end()));
    
    return result;
}
```

## Time Complexity
- **Method 1**: O(n! × n) - generate all permutations
- **Method 2**: O(n! × n) - recursive generation
- **Method 3**: O(n! × n) - iterative with duplicate handling

## Example Walkthrough

**Input**: "aab"

**Process**:
1. Sort string: "aab"
2. Generate permutations:
   - "aab" (original)
   - "aba" (swap b with second a)
   - "baa" (swap b with first a)
3. All are distinct

**Output**: 3 distinct strings: ["aab", "aba", "baa"]

## Problem Variations

### Variation 1: K-th Permutation
**Problem**: Find k-th lexicographical permutation.

**Solution**: Use mathematical approach or binary search.

### Variation 2: Constrained Permutations
**Problem**: Some characters must maintain relative order.

**Approach**: Use topological sorting or constraint satisfaction.

### Variation 3: Weighted Permutations
**Problem**: Each permutation has a weight. Find minimum/maximum weight.

**Solution**: Use dynamic programming or greedy approach.

### Variation 4: Circular Permutations
**Problem**: Consider rotations as equivalent.

**Approach**: Use Burnside's lemma or group theory.

### Variation 5: Partial Permutations
**Problem**: Generate permutations of length k from string of length n.

**Solution**: Use combination generation with permutation.

### Variation 6: Probabilistic Permutations
**Problem**: Each character has a probability. Find expected number of distinct permutations.

**Approach**: Use probability theory and expected values.

## Advanced Optimizations

### 1. Efficient Duplicate Handling
```python
from itertools import permutations

def create_strings_efficient(s):
    # Sort to get lexicographically smallest
    s_sorted = ''.join(sorted(s))
    
    # Use set to automatically handle duplicates
    unique_permutations = set()
    
    for perm in permutations(s_sorted):
        unique_permutations.add(''.join(perm))
    
    # Convert set to list
    return list(unique_permutations)
```

### 2. Mathematical Counting
```python
def count_permutations(s):
    from collections import Counter
    from math import factorial
    
    freq = Counter(s)
    n = len(s)
    numerator = factorial(n)
    denominator = 1
    
    # Calculate product of factorials of frequencies
    for count in freq.values():
        if count > 1:
            denominator *= factorial(count)
    
    return numerator // denominator
```

### 3. Memory Efficient Generation
```python
class MemoryEfficientStringCreator:
    def __init__(self):
        self.result = []
        self.s = ""
    
    def generate_permutations(self, start):
        if start == len(self.s) - 1:
            self.result.append(self.s)
            return
        
        used = set()
        for i in range(start, len(self.s)):
            if self.s[i] in used:
                continue
            used.add(self.s[i])
            
            # Swap characters
            self.s = self.s[:start] + self.s[i] + self.s[start+1:i] + self.s[start] + self.s[i+1:]
            self.generate_permutations(start + 1)
            # Swap back
            self.s = self.s[:start] + self.s[i] + self.s[start+1:i] + self.s[start] + self.s[i+1:]
    
    def create_strings(self, input_str):
        self.s = input_str
        self.s = ''.join(sorted(self.s))
        self.generate_permutations(0)
        return self.result
```

### 4. Parallel Generation
```python
def create_strings_parallel(s):
    # For large strings, use parallel processing
    # Divide permutation space and process in parallel
    # Merge results
    
    # Implementation for parallel processing...
    return []
```

## Related Problems
- [String Reorder](/cses-analyses/problem_soulutions/string_reorder_analysis)
- [Palindrome Reorder](/cses-analyses/problem_soulutions/palindrome_reorder_analysis)
- [Permutations](/cses-analyses/problem_soulutions/permutations_analysis)

## Practice Problems
1. **CSES**: Creating Strings
2. **LeetCode**: Similar permutation problems
3. **AtCoder**: String manipulation problems

## Key Takeaways
1. **next_permutation** is efficient for lexicographical generation
2. **Mathematical counting** helps avoid generating all permutations
3. **Duplicate handling** is crucial for correct results
4. **Memory efficiency** is important for large strings
5. **Lexicographical order** requires initial sorting
6. **Mathematical formulas** provide exact counts
7. **Optimization techniques** depend on problem constraints
