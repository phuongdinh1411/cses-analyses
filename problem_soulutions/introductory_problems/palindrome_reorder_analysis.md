---
layout: simple
title: Palindrome Reorder Analysis
permalink: /problem_soulutions/introductory_problems/palindrome_reorder_analysis/
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
```cpp
string palindromeReorder(string s) {
    vector<int> freq(26, 0);
    
    // Count character frequencies
    for (char c : s) {
        freq[c - 'A']++;
    }
    
    // Check feasibility
    int odd_count = 0;
    for (int f : freq) {
        if (f % 2 == 1) odd_count++;
    }
    
    if (odd_count > 1) {
        return "NO SOLUTION";
    }
    
    // Construct palindrome
    string first_half = "";
    string middle = "";
    
    for (int i = 0; i < 26; i++) {
        if (freq[i] > 0) {
            if (freq[i] % 2 == 1) {
                middle = string(1, 'A' + i);
                freq[i]--;
            }
            first_half += string(freq[i] / 2, 'A' + i);
        }
    }
    
    string second_half = first_half;
    reverse(second_half.begin(), second_half.end());
    
    return first_half + middle + second_half;
}
```

### Method 2: Two Pointers Approach
```cpp
string palindromeReorderTwoPointers(string s) {
    vector<int> freq(26, 0);
    
    // Count frequencies
    for (char c : s) {
        freq[c - 'A']++;
    }
    
    // Check feasibility
    int odd_count = 0;
    for (int f : freq) {
        if (f % 2 == 1) odd_count++;
    }
    
    if (odd_count > 1) {
        return "NO SOLUTION";
    }
    
    // Use two pointers to construct
    vector<char> result(s.length());
    int left = 0, right = s.length() - 1;
    
    for (int i = 0; i < 26; i++) {
        if (freq[i] % 2 == 1) {
            // Place odd character in middle
            result[s.length() / 2] = 'A' + i;
            freq[i]--;
        }
        
        // Place pairs symmetrically
        while (freq[i] > 0) {
            result[left++] = 'A' + i;
            result[right--] = 'A' + i;
            freq[i] -= 2;
        }
    }
    
    return string(result.begin(), result.end());
}
```

### Method 3: Greedy Construction
```cpp
string palindromeReorderGreedy(string s) {
    map<char, int> freq;
    
    // Count frequencies
    for (char c : s) {
        freq[c]++;
    }
    
    // Find odd character
    char odd_char = 0;
    for (auto& [c, count] : freq) {
        if (count % 2 == 1) {
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
```cpp
string palindromeReorderBit(string s) {
    int freq = 0;
    
    // Use bits to track odd/even frequencies
    for (char c : s) {
        freq ^= (1 << (c - 'A'));
    }
    
    // Check if more than one bit is set
    if (freq && (freq & (freq - 1))) {
        return "NO SOLUTION";
    }
    
    // Construct palindrome using bit manipulation
    // Implementation continues...
}
```

### 2. In-place Construction
```cpp
string palindromeReorderInplace(string s) {
    vector<int> freq(26, 0);
    
    // Count frequencies
    for (char c : s) {
        freq[c - 'A']++;
    }
    
    // Check feasibility
    int odd_count = 0;
    for (int f : freq) {
        if (f % 2 == 1) odd_count++;
    }
    
    if (odd_count > 1) {
        return "NO SOLUTION";
    }
    
    // Construct in-place
    int left = 0, right = s.length() - 1;
    
    for (int i = 0; i < 26; i++) {
        if (freq[i] % 2 == 1) {
            s[s.length() / 2] = 'A' + i;
            freq[i]--;
        }
        
        while (freq[i] > 0) {
            s[left++] = 'A' + i;
            s[right--] = 'A' + i;
            freq[i] -= 2;
        }
    }
    
    return s;
}
```

### 3. Parallel Processing
```cpp
string palindromeReorderParallel(string s) {
    // For very large strings, use parallel frequency counting
    // Divide string into chunks and process in parallel
    // Merge results and construct palindrome
    
    // Implementation for parallel processing...
}
```

## Related Problems
- [Creating Strings](../creating_strings_analysis/)
- [String Reorder](../string_reorder_analysis/)
- [Permutations](../permutations_analysis/)

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
