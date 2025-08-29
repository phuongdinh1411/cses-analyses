---
layout: simple
title: "Palindrome Reorder Analysis"
permalink: /problem_soulutions/introductory_problems/palindrome_reorder_analysis
---


# Palindrome Reorder Analysis

## Problem Description

Given a string, determine if it can be rearranged to form a palindrome. If possible, output one such palindrome; otherwise, output "NO SOLUTION".

## Key Insights

### 1. Palindrome Properties
- **Even length**: All characters must appear even number of times
- **Odd length**: All characters except one must appear even number of times
- **Character frequency**: Count occurrences of each character

### 2. Feasibility Check
- Count frequency of each character
- For even length: all frequencies must be even
- For odd length: exactly one frequency must be odd

### 3. Construction Strategy
- Use half of each character pair for first half
- Place odd character in middle (if exists)
- Mirror the first half for second half

## Solution Approach

### Method 1: Frequency Counting
```python
def palindrome_reorder(s):
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Construct palindrome
    first_half = ""
    middle = ""
    
    for i in range(26):
        if freq[i] > 0:
            if freq[i] % 2 == 1:
                middle = chr(ord('A') + i)
                freq[i] -= 1
            first_half += chr(ord('A') + i) * (freq[i] // 2)
    
    second_half = first_half[::-1]
    
    return first_half + middle + second_half
```

### Method 2: Two Pointers Approach
```python
def palindrome_reorder_two_pointers(s):
    freq = [0] * 26
    
    # Count frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Use two pointers to construct
    result = [''] * len(s)
    left, right = 0, len(s) - 1
    
    for i in range(26):
        if freq[i] % 2 == 1:
            # Place odd character in middle
            result[len(s) // 2] = chr(ord('A') + i)
            freq[i] -= 1
        
        # Place pairs symmetrically
        while freq[i] > 0:
            result[left] = chr(ord('A') + i)
            result[right] = chr(ord('A') + i)
            left += 1
            right -= 1
            freq[i] -= 2
    
    return ''.join(result)
```

### Method 3: Greedy Construction
```python
def palindrome_reorder_greedy(s):
    from collections import Counter
    
    freq = Counter(s)
    
    # Find odd character
    odd_char = None
    for c, count in freq.items():
        if count % 2 == 1:
```
            if (odd_char != 0) {
                return "NO SOLUTION";
            }
            odd_char = c;
        }
    }
    
    // Construct palindrome
    string result;
    
    // Add first half
    for (auto& [c, count] : freq) {
        result += string(count / 2, c);
    }
    
    // Add middle character if exists
    if (odd_char != 0) {
        result += odd_char;
    }
    
    // Add second half (reverse of first half)
    string first_half = result.substr(0, result.length() - (odd_char != 0 ? 1 : 0));
    reverse(first_half.begin(), first_half.end());
    result += first_half;
    
    return result;
}
```

## Time Complexity
- **Time**: O(n) - where n is string length
- **Space**: O(1) - constant space for frequency array

## Example Walkthrough

**Input**: "AABBC"

**Process**:
1. Count frequencies: A=2, B=2, C=1
2. Check feasibility: 1 odd frequency (C) ✓
3. Construct first half: "AB"
4. Add middle: "ABC"
5. Add second half: "ABCBA"

**Output**: "ABCBA"

## Problem Variations

### Variation 1: Lexicographically Smallest
**Problem**: Find lexicographically smallest palindrome.

**Approach**: Sort characters before constructing.

### Variation 2: All Possible Palindromes
**Problem**: Generate all possible palindromes.

**Approach**: Use backtracking with permutations.

### Variation 3: Minimum Operations
**Problem**: Find minimum swaps to make palindrome.

**Approach**: Use greedy approach with inversions.

### Variation 4: Weighted Characters
**Problem**: Each character has a weight. Find minimum weight palindrome.

**Approach**: Use dynamic programming.

### Variation 5: Constrained Positions
**Problem**: Some positions must have specific characters.

**Approach**: Modify construction to respect constraints.

### Variation 6: Different Alphabets
**Problem**: Use different character sets (digits, symbols).

**Solution**: Extend frequency counting to larger alphabet.

## Advanced Optimizations

### 1. Bit Manipulation
```python
def palindrome_reorder_bit(s):
    freq = 0
    
    # Use bits to track odd/even frequencies
    for c in s:
        freq ^= (1 << (ord(c) - ord('A')))
    
    # Check if more than one bit is set
    if freq and (freq & (freq - 1)):
        return "NO SOLUTION"
    
    # Construct palindrome using bit manipulation
    # Implementation continues...
    return s
```

### 2. In-place Construction
```python
def palindrome_reorder_inplace(s):
    freq = [0] * 26
    
    # Count frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Convert to list for in-place modification
    s_list = list(s)
    
    # Construct in-place
    left, right = 0, len(s) - 1
    
    for i in range(26):
        if freq[i] % 2 == 1:
            s_list[len(s) // 2] = chr(ord('A') + i)
            freq[i] -= 1
        
        while freq[i] > 0:
            s_list[left] = chr(ord('A') + i)
            s_list[right] = chr(ord('A') + i)
            left += 1
            right -= 1
            freq[i] -= 2
    
    return ''.join(s_list)
```

### 3. Parallel Processing
```python
def palindrome_reorder_parallel(s):
    # For very large strings, use parallel frequency counting
    # Divide string into chunks and process in parallel
    # Merge results and construct palindrome
    
    # Implementation for parallel processing...
    return s
```

## Related Problems
- [Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)
- [String Reorder](/cses-analyses/problem_soulutions/introductory_problems/string_reorder_analysis)
- [Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)

## Practice Problems
1. **CSES**: Palindrome Reorder
2. **LeetCode**: Similar palindrome problems
3. **AtCoder**: String manipulation problems

## Key Takeaways
1. **Frequency counting** is essential for palindrome construction
2. **Feasibility check** must be done before construction
3. **Symmetrical placement** ensures palindrome property
4. **Bit manipulation** can optimize frequency tracking
5. **In-place construction** saves memory
6. **Lexicographical ordering** requires careful character placement
7. **Edge cases** like single characters need special handling
