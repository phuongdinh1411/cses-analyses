---
layout: simple
title: "Repetitions"
permalink: /problem_soulutions/introductory_problems/repetitions_analysis
---

# Repetitions

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand string analysis and consecutive character counting problems
- Apply sliding window or linear scanning to find maximum consecutive repetitions
- Implement efficient string analysis algorithms with proper consecutive character tracking
- Optimize string analysis using linear scanning and consecutive character counting
- Handle edge cases in string analysis (single character, no repetitions, large strings)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String analysis, consecutive character counting, sliding window, linear scanning
- **Data Structures**: String processing, character tracking, consecutive counting, maximum tracking
- **Mathematical Concepts**: String mathematics, consecutive analysis, maximum finding, string theory
- **Programming Skills**: String processing, consecutive character counting, maximum tracking, algorithm implementation
- **Related Problems**: String problems, Consecutive counting, Maximum finding, String analysis

## Problem Description

**Problem**: You are given a DNA sequence consisting of characters A, C, G, and T. Find the longest repetition in the sequence. This is a maximum-length substring containing only one type of character.

**Input**: A string of n characters (1 ≤ n ≤ 10⁶)

**Output**: Print one integer: the length of the longest repetition.

**Constraints**:
- 1 ≤ n ≤ 10⁶
- String contains only characters A, C, G, T
- Need to find maximum consecutive same characters
- Return the length of longest repetition
- Handle edge cases (single character, no repetitions)

**Example**:
```
Input: ATTCGGGA

Output: 3

Explanation: The longest repetition is "GGG" with length 3.
```

## Visual Example

### Input and Character Analysis
```
Input: ATTCGGGA
Characters: A, T, T, C, G, G, G, A

Character analysis:
A: position 0, length 1
T: positions 1-2, length 2
C: position 3, length 1
G: positions 4-6, length 3 ← Longest repetition
A: position 7, length 1
```

### Consecutive Character Tracking
```
Step-by-step tracking:
Position 0: A (current_length = 1, max_length = 1)
Position 1: T (current_length = 1, max_length = 1)
Position 2: T (current_length = 2, max_length = 2)
Position 3: C (current_length = 1, max_length = 2)
Position 4: G (current_length = 1, max_length = 2)
Position 5: G (current_length = 2, max_length = 2)
Position 6: G (current_length = 3, max_length = 3)
Position 7: A (current_length = 1, max_length = 3)

Final result: 3
```

### Key Insight
The solution works by:
1. Scanning the string from left to right
2. Tracking consecutive same characters
3. Updating maximum length when character changes
4. Time complexity: O(n) for single pass
5. Space complexity: O(1) for constant variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force with Nested Loops (Inefficient)

**Key Insights from Brute Force Solution:**
- Check every possible substring to find the longest repetition
- Simple but computationally expensive approach
- Not suitable for large strings
- Straightforward implementation but poor performance

**Algorithm:**
1. For each starting position, check all possible ending positions
2. For each substring, check if all characters are the same
3. Track the maximum length found
4. Return the maximum length

**Visual Example:**
```
Brute force: Check all substrings
For "ATTCGGGA":
- Check A: length 1
- Check AT: different characters
- Check ATT: different characters
- Check T: length 1
- Check TT: length 2
- Check TTC: different characters
- Check C: length 1
- Check CG: different characters
- Check G: length 1
- Check GG: length 2
- Check GGG: length 3 ← Maximum
- Check GGGA: different characters
- Check A: length 1
```

**Implementation:**
```python
def repetitions_brute_force(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    
    # Check all possible substrings
    for i in range(n):
        for j in range(i, n):
            # Check if all characters in substring are the same
            if all(sequence[i] == sequence[k] for k in range(i, j + 1)):
                max_length = max(max_length, j - i + 1)
    
    return max_length

def solve_repetitions_brute_force():
    sequence = input().strip()
    result = repetitions_brute_force(sequence)
    print(result)
```

**Time Complexity:** O(n³) for nested loops and character checking
**Space Complexity:** O(1) for storing variables

**Why it's inefficient:**
- O(n³) time complexity is too slow for large strings
- Not suitable for competitive programming with n up to 10^6
- Inefficient for long strings
- Poor performance with large inputs

### Approach 2: Simple Linear Scanning (Better)

**Key Insights from Simple Linear Scanning Solution:**
- Use linear scanning to find consecutive same characters
- Much more efficient than brute force approach
- Standard method for consecutive character counting
- Can handle larger inputs than brute force

**Algorithm:**
1. Scan the string from left to right
2. Count consecutive same characters
3. Update maximum when character changes
4. Handle the last group of characters

**Visual Example:**
```
Simple linear scanning for "ATTCGGGA":
- A: current_length = 1, max_length = 1
- T: current_length = 1, max_length = 1
- T: current_length = 2, max_length = 2
- C: current_length = 1, max_length = 2
- G: current_length = 1, max_length = 2
- G: current_length = 2, max_length = 2
- G: current_length = 3, max_length = 3
- A: current_length = 1, max_length = 3
```

**Implementation:**
```python
def repetitions_simple_linear(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1
    
    # Don't forget the last group
    max_length = max(max_length, current_length)
    
    return max_length

def solve_repetitions_simple():
    sequence = input().strip()
    result = repetitions_simple_linear(sequence)
    print(result)
```

**Time Complexity:** O(n) for single pass through the string
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- O(n) time complexity is much better than O(n³)
- Uses linear scanning for efficient solution
- Suitable for competitive programming
- Efficient for all practical cases

### Approach 3: Optimized Linear Scanning (Optimal)

**Key Insights from Optimized Linear Scanning Solution:**
- Use optimized linear scanning with cleaner code
- Most efficient approach for consecutive character counting
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized linear scanning
2. Update maximum inside the loop for cleaner logic
3. Handle edge cases efficiently
4. Return the maximum length found

**Visual Example:**
```
Optimized linear scanning for "ATTCGGGA":
- Optimized scanning with cleaner logic
- Update maximum inside the loop
- Handle edge cases efficiently
- Final result: 3
```

**Implementation:**
```python
def repetitions_optimized(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length

def solve_repetitions():
    sequence = input().strip()
    result = repetitions_optimized(sequence)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_repetitions()
```

**Time Complexity:** O(n) for single pass through the string
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(n) time complexity is optimal for string scanning problems
- Uses optimized linear scanning
- Most efficient approach for competitive programming
- Standard method for consecutive character counting

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Repetitions with Different Characters
**Problem**: Find longest repetition with any character set.

**Link**: [CSES Problem Set - Repetitions Different Characters](https://cses.fi/problemset/task/repetitions_different_characters)

```python
def repetitions_different_characters(sequence, allowed_chars):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1] and sequence[i] in allowed_chars:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length
```

### Variation 2: Repetitions with Minimum Length
**Problem**: Find longest repetition with minimum length constraint.

**Link**: [CSES Problem Set - Repetitions Minimum Length](https://cses.fi/problemset/task/repetitions_minimum_length)

```python
def repetitions_minimum_length(sequence, min_length):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
            if current_length >= min_length:
                max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length if max_length >= min_length else 0
```

### Variation 3: Repetitions with Character Frequency
**Problem**: Find longest repetition considering character frequency.

**Link**: [CSES Problem Set - Repetitions Character Frequency](https://cses.fi/problemset/task/repetitions_character_frequency)

```python
def repetitions_character_frequency(sequence, char_freq):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1] and char_freq[sequence[i]] > 0:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length
```

### Related Problems

#### **CSES Problems**
- [Repetitions](https://cses.fi/problemset/task/1069) - Find longest repetition
- [Palindrome Reorder](https://cses.fi/problemset/task/1755) - String manipulation problems
- [Creating Strings](https://cses.fi/problemset/task/1622) - String generation problems

#### **LeetCode Problems**
- [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) - Find longest consecutive sequence
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) - Find longest substring without repeats
- [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) - Find longest palindrome
- [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) - Find longest common prefix

#### **Problem Categories**
- **String Processing**: Consecutive character counting, string analysis, pattern recognition
- **Linear Scanning**: Efficient string traversal, consecutive element counting, maximum finding
- **String Analysis**: Character frequency, string patterns, consecutive sequences
- **Algorithm Design**: Linear algorithms, string optimization, pattern matching

## 📚 Learning Points

1. **String Analysis**: Essential for understanding consecutive character problems
2. **Linear Scanning**: Key technique for efficient string processing
3. **Consecutive Counting**: Important for understanding string patterns
4. **Maximum Finding**: Critical for understanding optimization problems
5. **String Processing**: Foundation for many string algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Repetitions problem demonstrates fundamental string analysis concepts for finding consecutive character patterns. We explored three approaches:

1. **Brute Force with Nested Loops**: O(n³) time complexity using nested loops to check all substrings, inefficient for large strings
2. **Simple Linear Scanning**: O(n) time complexity using linear scanning to count consecutive characters, better approach for string analysis problems
3. **Optimized Linear Scanning**: O(n) time complexity with optimized linear scanning, optimal approach for consecutive character counting

The key insights include understanding string analysis principles, using linear scanning for efficient consecutive character counting, and applying algorithm optimization techniques for optimal performance. This problem serves as an excellent introduction to string analysis and consecutive character counting algorithms.
