---
layout: simple
title: "Palindrome Reorder"
permalink: /problem_soulutions/introductory_problems/palindrome_reorder_analysis
---

# Palindrome Reorder

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand palindrome properties and string rearrangement problems
- Apply character frequency analysis to determine palindrome feasibility
- Implement efficient palindrome construction algorithms with proper character arrangement
- Optimize palindrome construction using frequency analysis and string manipulation
- Handle edge cases in palindrome problems (impossible palindromes, single characters, large strings)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Palindrome properties, character frequency analysis, string rearrangement, string construction
- **Data Structures**: Character frequency tracking, string manipulation, palindrome construction, character counting
- **Mathematical Concepts**: Palindrome theory, character frequency analysis, string mathematics, combinatorics
- **Programming Skills**: String manipulation, character frequency counting, palindrome construction, algorithm implementation
- **Related Problems**: String problems, Palindrome problems, Character frequency, String manipulation

## Problem Description

**Problem**: Given a string, determine if it can be rearranged to form a palindrome. If possible, output one such palindrome; otherwise, output "NO SOLUTION".

**Input**: A string s (1 ≤ |s| ≤ 10⁶)

**Output**: A palindrome if possible, or "NO SOLUTION".

**Constraints**:
- 1 ≤ |s| ≤ 10⁶
- String contains only uppercase letters A-Z
- Must determine palindrome feasibility
- If possible, construct one palindrome
- If impossible, output "NO SOLUTION"

**Example**:
```
Input: AAAACACBA

Output: AAACBCAAA

Explanation: The string can be rearranged to form the palindrome "AAACBCAAA".
```

## Visual Example

### Input and Character Frequency Analysis
```
Input: s = "AAAACACBA"

Character frequency analysis:
A: 5 occurrences
B: 1 occurrence  
C: 2 occurrences

Frequency pattern: [5, 1, 2, 0, 0, ..., 0]
Odd frequencies: A=5 (odd), B=1 (odd), C=2 (even)
Odd count: 2 > 1 → Cannot form palindrome
```

### Palindrome Feasibility Check
```
For string "AAAACACBA":

Step 1: Count character frequencies
A: 5, B: 1, C: 2

Step 2: Check odd frequencies
- A has 5 (odd)
- B has 1 (odd)  
- C has 2 (even)
- Total odd frequencies: 2

Step 3: Palindrome rule
- Even length: all frequencies must be even
- Odd length: exactly one frequency can be odd
- Current: 2 odd frequencies > 1 → Impossible
```

### Palindrome Construction Process
```
For string "AAAACACBA" (impossible case):
Result: "NO SOLUTION"

For string "AAAACACB" (possible case):
Character frequencies: A=4, B=1, C=2
Odd frequencies: B=1 (only one odd) → Possible

Construction:
1. First half: "AAC" (half of each even frequency)
2. Middle: "B" (the odd frequency character)
3. Second half: "CAA" (reverse of first half)
4. Result: "AAC" + "B" + "CAA" = "AACBCAA"
```

### Key Insight
The solution works by:
1. Counting character frequencies in the string
2. Checking palindrome feasibility using frequency rules
3. Constructing palindrome using frequency analysis
4. Time complexity: O(n) for frequency counting and construction
5. Space complexity: O(1) for frequency array (26 characters)

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Permutation Check (Inefficient)

**Key Insights from Brute Force Solution:**
- Generate all permutations and check if any is a palindrome
- Simple but computationally expensive approach
- Not suitable for large strings due to factorial growth
- Straightforward implementation but poor scalability

**Algorithm:**
1. Generate all possible permutations of the string
2. Check each permutation to see if it's a palindrome
3. Return the first palindrome found or "NO SOLUTION"
4. Handle edge cases correctly

**Visual Example:**
```
Brute force: Check all permutations
For string "AAB":

All permutations: ["AAB", "ABA", "BAA"]
Check each:
- "AAB" → Not palindrome (AAB ≠ BAA)
- "ABA" → Palindrome (ABA = ABA) ✓
- "BAA" → Not palindrome (BAA ≠ AAB)

Result: "ABA"
```

**Implementation:**
```python
from itertools import permutations

def palindrome_reorder_brute_force(s):
    # Generate all permutations
    perms = set(permutations(s))
    
    for perm in perms:
        perm_str = ''.join(perm)
        if perm_str == perm_str[::-1]:  # Check if palindrome
            return perm_str
    
    return "NO SOLUTION"

def solve_palindrome_reorder_brute_force():
    s = input().strip()
    result = palindrome_reorder_brute_force(s)
    print(result)
```

**Time Complexity:** O(n! × n) for generating and checking all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's inefficient:**
- O(n! × n) time complexity grows factorially
- Not suitable for competitive programming with n up to 10⁶
- Memory-intensive for large strings
- Poor performance with factorial growth

### Approach 2: Character Frequency Analysis (Better)

**Key Insights from Frequency Analysis Solution:**
- Use character frequency counting to determine feasibility
- Much more efficient than brute force approach
- Standard method for palindrome problems
- Can handle larger strings than brute force approach

**Algorithm:**
1. Count frequency of each character in the string
2. Check if palindrome is possible using frequency rules
3. If possible, construct palindrome using frequency analysis
4. Return constructed palindrome or "NO SOLUTION"

**Visual Example:**
```
Frequency analysis: Count and check
For string "AAAACACBA":

Step 1: Count frequencies
A: 5, B: 1, C: 2

Step 2: Check odd frequencies
Odd count: 2 (A=5, B=1)
Since odd count > 1 → Impossible

Result: "NO SOLUTION"
```

**Implementation:**
```python
def palindrome_reorder_frequency(s):
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

def solve_palindrome_reorder_frequency():
    s = input().strip()
    result = palindrome_reorder_frequency(s)
    print(result)
```

**Time Complexity:** O(n) for frequency counting and construction
**Space Complexity:** O(1) for frequency array

**Why it's better:**
- O(n) time complexity is much better than O(n!)
- Uses frequency analysis for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Frequency Analysis with Early Termination (Optimal)

**Key Insights from Optimized Solution:**
- Use optimized frequency analysis with early termination
- Most efficient approach for palindrome construction
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Count character frequencies in single pass
2. Check feasibility with early termination
3. Construct palindrome efficiently using frequency analysis
4. Leverage mathematical properties for optimal solution

**Visual Example:**
```
Optimized approach: Early termination
For string "AAAACACBA":

Step 1: Count frequencies with early termination
A: 5, B: 1, C: 2
Odd count: 2 > 1 → Early termination

Result: "NO SOLUTION" (no need to construct)
```

**Implementation:**
```python
def palindrome_reorder_optimized(s):
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility with early termination
    odd_count = 0
    odd_char = -1
    
    for i in range(26):
        if freq[i] % 2 == 1:
            odd_count += 1
            odd_char = i
            if odd_count > 1:
                return "NO SOLUTION"
    
    # Construct palindrome efficiently
    first_half = ""
    middle = ""
    
    for i in range(26):
        if freq[i] > 0:
            if i == odd_char:
                middle = chr(ord('A') + i)
                freq[i] -= 1
            first_half += chr(ord('A') + i) * (freq[i] // 2)
    
    second_half = first_half[::-1]
    return first_half + middle + second_half

def solve_palindrome_reorder():
    s = input().strip()
    result = palindrome_reorder_optimized(s)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_palindrome_reorder()
```

**Time Complexity:** O(n) for frequency counting and construction
**Space Complexity:** O(1) for frequency array

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses early termination for efficient feasibility check
- Most efficient approach for competitive programming
- Standard method for palindrome construction optimization

## 🎯 Problem Variations

### Variation 1: Palindrome with Lowercase Letters
**Problem**: Handle both uppercase and lowercase letters in palindrome construction.

**Link**: [CSES Problem Set - Palindrome with Lowercase](https://cses.fi/problemset/task/palindrome_lowercase)

```python
def palindrome_reorder_lowercase(s):
    freq = [0] * 52  # 26 uppercase + 26 lowercase
    
    for c in s:
        if c.isupper():
            freq[ord(c) - ord('A')] += 1
        else:
            freq[ord(c) - ord('a') + 26] += 1
    
    odd_count = sum(1 for f in freq if f % 2 == 1)
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Construct palindrome with case preservation
    first_half = ""
    middle = ""
    
    for i in range(52):
        if freq[i] > 0:
            char = chr(ord('A') + i) if i < 26 else chr(ord('a') + i - 26)
            if freq[i] % 2 == 1:
                middle = char
                freq[i] -= 1
            first_half += char * (freq[i] // 2)
    
    second_half = first_half[::-1]
    return first_half + middle + second_half
```

### Variation 2: Longest Palindrome Subsequence
**Problem**: Find the longest palindrome that can be formed as a subsequence.

**Link**: [CSES Problem Set - Longest Palindrome Subsequence](https://cses.fi/problemset/task/longest_palindrome_subsequence)

```python
def longest_palindrome_subsequence(s):
    freq = [0] * 26
    
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Count pairs and odd characters
    pairs = 0
    odd_chars = 0
    
    for f in freq:
        pairs += f // 2
        if f % 2 == 1:
            odd_chars += 1
    
    # Longest palindrome length
    return pairs * 2 + min(odd_chars, 1)
```

### Variation 3: Minimum Insertions for Palindrome
**Problem**: Find minimum number of insertions needed to make string a palindrome.

**Link**: [CSES Problem Set - Minimum Insertions for Palindrome](https://cses.fi/problemset/task/minimum_insertions_palindrome)

```python
def minimum_insertions_palindrome(s):
    freq = [0] * 26
    
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    odd_count = sum(1 for f in freq if f % 2 == 1)
    
    # Minimum insertions = max(0, odd_count - 1)
    return max(0, odd_count - 1)
```

## 🔗 Related Problems

- **[String Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: String problems
- **[Palindrome Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Palindrome problems
- **[Character Frequency Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Character frequency problems
- **[String Manipulation Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: String manipulation problems

## 📚 Learning Points

1. **Palindrome Properties**: Essential for understanding palindrome construction
2. **Character Frequency Analysis**: Key technique for efficient feasibility checking
3. **String Manipulation**: Important for understanding palindrome construction
4. **Mathematical Analysis**: Critical for understanding frequency rules
5. **Algorithm Optimization**: Foundation for many string manipulation algorithms
6. **Early Termination**: Critical for competitive programming efficiency

## 📝 Summary

The Palindrome Reorder problem demonstrates palindrome properties and character frequency analysis concepts for efficient palindrome construction. We explored three approaches:

1. **Brute Force Permutation Check**: O(n! × n) time complexity using permutation generation, inefficient for large strings
2. **Character Frequency Analysis**: O(n) time complexity using frequency counting, better approach for palindrome construction
3. **Optimized Frequency Analysis with Early Termination**: O(n) time complexity with early termination, optimal approach for palindrome construction

The key insights include understanding palindrome properties, using character frequency analysis for efficient feasibility checking, and applying mathematical analysis for optimal performance. This problem serves as an excellent introduction to string manipulation algorithms and palindrome construction optimization.
