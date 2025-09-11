---
layout: simple
title: "String Reorder"
permalink: /problem_soulutions/introductory_problems/string_reorder_analysis
---

# String Reorder

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand lexicographic ordering and string sorting concepts
- Apply sorting algorithms to find lexicographically smallest string arrangements
- Implement efficient string sorting algorithms with proper lexicographic ordering
- Optimize string sorting using character frequency counting and lexicographic ordering
- Handle edge cases in string sorting (duplicate characters, large strings, lexicographic ordering)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String sorting, lexicographic ordering, character frequency counting, string arrangement
- **Data Structures**: String manipulation, character frequency tracking, sorting data structures, lexicographic ordering
- **Mathematical Concepts**: Lexicographic ordering, string mathematics, sorting theory, character frequency analysis
- **Programming Skills**: String sorting, character frequency counting, lexicographic ordering, algorithm implementation
- **Related Problems**: String problems, Sorting problems, Lexicographic ordering, Character frequency

## Problem Description

**Problem**: Given a string, find the lexicographically smallest string that can be obtained by reordering its characters.

**Input**: A string s (1 ≤ |s| ≤ 10⁶)

**Output**: The lexicographically smallest string that can be obtained by reordering the characters of s.

**Constraints**:
- 1 ≤ |s| ≤ 10⁶
- String contains only uppercase letters A-Z
- Find lexicographically smallest arrangement
- Handle duplicate characters correctly
- Preserve all original characters

**Example**:
```
Input: "CAB"

Output: "ABC"

Explanation: By reordering the characters, we can get "ABC", "ACB", "BAC", "BCA", "CAB", "CBA". 
The lexicographically smallest is "ABC".
```

## Visual Example

### Input and Character Analysis
```
Input: s = "CAB"

Character frequency:
A: 1 occurrence
B: 1 occurrence
C: 1 occurrence

ASCII values:
A = 65, B = 66, C = 67

Lexicographic order: A < B < C
```

### Lexicographic Ordering Process
```
For string "CAB":

All possible arrangements:
1. ABC ← lexicographically smallest
2. ACB
3. BAC
4. BCA
5. CAB (original)
6. CBA

Lexicographic comparison:
- Compare characters from left to right
- First differing character determines order
- A < B < C in ASCII order
```

### Character Frequency Construction
```
Frequency counting approach:
For "CAB":

Step 1: Count frequencies
freq[A] = 1, freq[B] = 1, freq[C] = 1

Step 2: Construct result
result = ""
for i in range(26):
    result += chr(ord('A') + i) * freq[i]

Result: "A" + "B" + "C" = "ABC"
```

### Key Insight
The solution works by:
1. Counting frequency of each character
2. Constructing result by placing characters in lexicographic order
3. Repeating each character according to its frequency
4. Time complexity: O(n) for counting and construction
5. Space complexity: O(1) for frequency array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Generate All Permutations (Inefficient)

**Key Insights from Permutation Generation Solution:**
- Generate all possible character arrangements
- Find the lexicographically smallest among all permutations
- Simple but computationally expensive approach
- Not suitable for large strings due to factorial growth

**Algorithm:**
1. Generate all possible permutations of the string
2. Find the lexicographically smallest permutation
3. Return the result

**Visual Example:**
```
Permutation generation: Generate all arrangements
For string "CAB":

All permutations:
ABC, ACB, BAC, BCA, CAB, CBA

Find minimum: "ABC"
```

**Implementation:**
```python
from itertools import permutations

def string_reorder_permutations(s):
    # Generate all permutations
    perms = [''.join(p) for p in permutations(s)]
    
    # Find lexicographically smallest
    return min(perms)

def solve_string_reorder_permutations():
    s = input().strip()
    result = string_reorder_permutations(s)
    print(result)
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's inefficient:**
- O(n! × n) time complexity grows factorially
- Not suitable for competitive programming with n up to 10⁶
- Memory-intensive for large strings
- Poor performance with exponential growth

### Approach 2: Simple Sorting (Better)

**Key Insights from Sorting Solution:**
- Sort characters directly to get lexicographically smallest arrangement
- More efficient than permutation generation
- Standard method for lexicographic ordering
- Can handle large strings efficiently

**Algorithm:**
1. Convert string to list of characters
2. Sort the characters in ascending order
3. Join back to form the result string

**Visual Example:**
```
Simple sorting: Sort characters directly
For string "CAB":

Step 1: Convert to list → ['C', 'A', 'B']
Step 2: Sort → ['A', 'B', 'C']
Step 3: Join → "ABC"
```

**Implementation:**
```python
def string_reorder_sorting(s):
    # Sort the string directly
    return ''.join(sorted(s))

def solve_string_reorder_sorting():
    s = input().strip()
    result = string_reorder_sorting(s)
    print(result)
```

**Time Complexity:** O(n log n) for sorting
**Space Complexity:** O(n) for temporary list

**Why it's better:**
- O(n log n) time complexity is much better than O(n!)
- Uses efficient sorting algorithms
- Suitable for competitive programming
- Handles large strings efficiently

### Approach 3: Character Frequency Counting (Optimal)

**Key Insights from Frequency Counting Solution:**
- Count frequency of each character
- Construct result by placing characters in lexicographic order
- Most efficient approach for this problem
- Standard method in competitive programming

**Algorithm:**
1. Count frequency of each character using array
2. Iterate through characters in lexicographic order
3. Append each character according to its frequency
4. Construct the final result

**Visual Example:**
```
Frequency counting: Count and construct
For string "CAB":

Step 1: Count frequencies
freq[A] = 1, freq[B] = 1, freq[C] = 1

Step 2: Construct result
result = ""
for i in range(26):
    result += chr(ord('A') + i) * freq[i]

Result: "A" + "B" + "C" = "ABC"
```

**Implementation:**
```python
def string_reorder_optimal(s):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct lexicographically smallest string
    result = ""
    for i in range(26):
        result += chr(ord('A') + i) * freq[i]
    
    return result

def solve_string_reorder():
    s = input().strip()
    result = string_reorder_optimal(s)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_string_reorder()
```

**Time Complexity:** O(n) for counting and construction
**Space Complexity:** O(1) for frequency array

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses constant space for frequency counting
- Most efficient approach for competitive programming
- Handles all cases correctly

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Lexicographically Largest String
**Problem**: Find the lexicographically largest string that can be obtained by reordering.

**Link**: [CSES Problem Set - Lexicographically Largest String](https://cses.fi/problemset/task/lexicographically_largest_string)

```python
def lexicographically_largest(s):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct lexicographically largest string
    result = ""
    for i in range(25, -1, -1):  # Reverse order
        result += chr(ord('A') + i) * freq[i]
    
    return result
```

### Variation 2: String Reorder with Custom Order
**Problem**: Reorder string according to a custom character ordering.

**Link**: [CSES Problem Set - Custom String Reorder](https://cses.fi/problemset/task/custom_string_reorder)

```python
def custom_string_reorder(s, custom_order):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct result according to custom order
    result = ""
    for c in custom_order:
        result += c * freq[ord(c) - ord('A')]
    
    return result
```

### Variation 3: String Reorder with Constraints
**Problem**: Reorder string while satisfying certain constraints.

**Link**: [CSES Problem Set - Constrained String Reorder](https://cses.fi/problemset/task/constrained_string_reorder)

```python
def constrained_string_reorder(s, constraints):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Apply constraints and construct result
    result = ""
    for i in range(26):
        char = chr(ord('A') + i)
        if constraints(char, freq[i]):
            result += char * freq[i]
    
    return result
```

### Related Problems

#### **CSES Problems**
- [String Reorder](https://cses.fi/problemset/task/1754) - Basic string reordering
- [Creating Strings](https://cses.fi/problemset/task/1622) - String generation problems
- [Palindrome Reorder](https://cses.fi/problemset/task/1755) - String manipulation problems

#### **LeetCode Problems**
- [Custom Sort String](https://leetcode.com/problems/custom-sort-string/) - Sort string according to custom order
- [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/) - Sort characters by frequency
- [Reorder Data in Log Files](https://leetcode.com/problems/reorder-data-in-log-files/) - Reorder log entries
- [Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/) - Sort array by parity

#### **Problem Categories**
- **String Manipulation**: Character frequency counting, string construction, lexicographic ordering
- **Sorting**: Character sorting, frequency-based sorting, custom ordering
- **Lexicographic Ordering**: String comparison, alphabetical ordering, dictionary ordering
- **Algorithm Design**: String algorithms, sorting algorithms, frequency analysis

## 📚 Learning Points

1. **Lexicographic Ordering**: Essential for understanding string comparison
2. **Character Frequency Counting**: Key technique for efficient string manipulation
3. **Sorting Algorithms**: Important for understanding string ordering
4. **String Construction**: Critical for understanding string building
5. **Algorithm Optimization**: Foundation for many string algorithms
6. **Mathematical Analysis**: Critical for understanding string properties

## 📝 Summary

The String Reorder problem demonstrates lexicographic ordering and character frequency counting concepts for efficient string manipulation. We explored three approaches:

1. **Generate All Permutations**: O(n! × n) time complexity using permutation generation, inefficient for large strings
2. **Simple Sorting**: O(n log n) time complexity using character sorting, better approach for string ordering
3. **Character Frequency Counting**: O(n) time complexity using frequency counting and construction, optimal approach for competitive programming

The key insights include understanding lexicographic ordering principles, using character frequency counting for efficient construction, and applying optimization techniques for optimal performance. This problem serves as an excellent introduction to string algorithms and lexicographic ordering in competitive programming.
