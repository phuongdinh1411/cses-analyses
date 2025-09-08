---
layout: simple
title: "Creating Strings"
permalink: /problem_soulutions/introductory_problems/creating_strings_analysis
---

# Creating Strings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand permutation generation and string manipulation problems
- Apply backtracking or next_permutation to generate all permutations
- Implement efficient permutation generation algorithms with proper duplicate handling
- Optimize permutation generation using lexicographic ordering and duplicate elimination
- Handle edge cases in permutation problems (duplicate characters, large strings, lexicographic ordering)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Permutation generation, backtracking, next_permutation, string manipulation
- **Data Structures**: Strings, character arrays, permutation tracking, lexicographic ordering
- **Mathematical Concepts**: Permutations, combinatorics, lexicographic ordering, duplicate handling
- **Programming Skills**: String manipulation, permutation generation, backtracking, algorithm implementation
- **Related Problems**: Permutation problems, String manipulation, Backtracking, Combinatorics

## Problem Description

**Problem**: Given a string, generate all possible permutations of its characters.

**Input**: A string s (1 ≤ |s| ≤ 8)

**Output**: 
- First line: number of distinct permutations
- Next lines: each permutation on a separate line (in lexicographic order)

**Constraints**:
- 1 ≤ |s| ≤ 8
- String contains only lowercase letters a-z
- Generate all distinct permutations
- Output must be in lexicographic order
- Handle duplicate characters correctly

**Example**:
```
Input: aabac

Output:
20
aaabc
aaacb
aabac
aabca
aacab
aacba
abaac
abaca
abcaa
acaab
acaba
acbaa
baaac
baaca
bacaa
bcaaa
caaab
caaba
cabaa
cbaaa
```

## Visual Example

### Input and Character Analysis
```
Input: s = "aabac"

Character frequency:
a: 3 occurrences
b: 1 occurrence  
c: 1 occurrence

Total length: 5
Expected distinct permutations: 5! / (3! × 1! × 1!) = 120 / 6 = 20
```

### Permutation Generation Process
```
For string "aabac":

Step 1: Sort characters → "aaabc"
Step 2: Generate all permutations using backtracking
Step 3: Remove duplicates (handled by proper algorithm)
Step 4: Sort results lexicographically

Sample generation:
aaabc → aaacb → aabac → aabca → aacab → aacba
abaac → abaca → abcaa → acaab → acaba → acbaa
baaac → baaca → bacaa → bcaaa → caaab → caaba
cabaa → cbaaa
```

### Lexicographic Ordering
```
Lexicographic order (dictionary order):
- Compare characters from left to right
- First differing character determines order
- Shorter strings come before longer ones

Example ordering:
aaabc < aaacb < aabac < aabca < aacab < aacba
< abaac < abaca < abcaa < acaab < acaba < acbaa
< baaac < baaca < bacaa < bcaaa < caaab < caaba
< cabaa < cbaaa
```

### Key Insight
The solution works by:
1. Generating all possible character arrangements
2. Handling duplicate characters to avoid duplicate permutations
3. Sorting results in lexicographic order
4. Time complexity: O(n! × n × log(n!)) for generation and sorting
5. Space complexity: O(n! × n) for storing all permutations

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Naive Recursive Generation (Inefficient)

**Key Insights from Naive Recursive Solution:**
- Use simple recursion to generate all character arrangements
- Simple but generates many duplicate permutations
- Not suitable for strings with duplicate characters
- Straightforward implementation but poor efficiency

**Algorithm:**
1. Use recursion to try all possible character positions
2. Generate all arrangements without duplicate handling
3. Use set to remove duplicates after generation
4. Sort the results for lexicographic order

**Visual Example:**
```
Naive recursive generation: Generate all arrangements
For string "aab":

Recursive tree:
aab → aab, aba, aab, aba, baa, baa
(Note: duplicates generated)

After removing duplicates: aab, aba, baa
```

**Implementation:**
```python
def creating_strings_naive(s):
    def generate_all(chars, current, result):
        if len(current) == len(chars):
            result.add(''.join(current))
            return
        
        for i in range(len(chars)):
            current.append(chars[i])
            generate_all(chars, current, result)
            current.pop()
    
    result = set()
    generate_all(list(s), [], result)
    return sorted(list(result))

def solve_creating_strings_naive():
    s = input().strip()
    perms = creating_strings_naive(s)
    print(len(perms))
    for perm in perms:
        print(perm)
```

**Time Complexity:** O(n! × n) for generating all arrangements
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's inefficient:**
- Generates many duplicate permutations unnecessarily
- O(n! × n) time complexity is inefficient
- Not suitable for competitive programming
- Poor performance with duplicate characters

### Approach 2: Backtracking with Duplicate Handling (Better)

**Key Insights from Backtracking Solution:**
- Use backtracking with proper duplicate handling
- More efficient than naive recursion
- Standard method for permutation generation
- Can handle duplicate characters efficiently

**Algorithm:**
1. Sort the input string to group duplicate characters
2. Use backtracking with visited array
3. Skip duplicate characters at same level to avoid duplicates
4. Generate permutations in lexicographic order

**Visual Example:**
```
Backtracking with duplicate handling:
For string "aabac" → sorted: "aaabc"

Backtracking process:
Level 0: Try a, a, a, b, c
Level 1: For each choice, try remaining characters
Level 2: Continue until all positions filled

Duplicate handling:
- If chars[i] == chars[i-1] and not used[i-1], skip
- This prevents generating duplicate permutations
```

**Implementation:**
```python
def creating_strings_backtracking(s):
    def backtrack(chars, current, used, result):
        if len(current) == len(chars):
            result.append(''.join(current))
            return
        
        for i in range(len(chars)):
            if used[i]:
                continue
            
            # Skip duplicates
            if i > 0 and chars[i] == chars[i-1] and not used[i-1]:
                continue
            
            used[i] = True
            current.append(chars[i])
            backtrack(chars, current, used, result)
            current.pop()
            used[i] = False
    
    chars = list(s)
    chars.sort()  # Sort to handle duplicates properly
    result = []
    backtrack(chars, [], [False] * len(chars), result)
    return result

def solve_creating_strings_backtracking():
    s = input().strip()
    perms = creating_strings_backtracking(s)
    print(len(perms))
    for perm in perms:
        print(perm)
```

**Time Complexity:** O(n! × n) for generating distinct permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's better:**
- Handles duplicate characters efficiently
- Generates permutations in lexicographic order
- More efficient than naive approach
- Suitable for competitive programming

### Approach 3: Built-in itertools.permutations (Optimal)

**Key Insights from Built-in Solution:**
- Use Python's optimized itertools.permutations
- Most efficient approach for permutation generation
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use itertools.permutations to generate all arrangements
2. Convert to set to remove duplicates automatically
3. Convert back to list and sort for lexicographic order
4. Leverage built-in optimization for best performance

**Visual Example:**
```
Built-in itertools.permutations:
For string "aabac":

itertools.permutations("aabac") generates all arrangements
set() removes duplicates automatically
sorted() ensures lexicographic order

Result: 20 distinct permutations in lexicographic order
```

**Implementation:**
```python
from itertools import permutations

def creating_strings_optimal(s):
    # Generate all permutations and remove duplicates
    perms = set(permutations(s))
    
    # Convert to strings and sort
    result = [''.join(p) for p in perms]
    result.sort()
    
    return result

def solve_creating_strings():
    s = input().strip()
    perms = creating_strings_optimal(s)
    
    # Print output
    print(len(perms))
    for perm in perms:
        print(perm)

# Main execution
if __name__ == "__main__":
    solve_creating_strings()
```

**Time Complexity:** O(n! × n × log(n!)) for generation and sorting
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's optimal:**
- Uses optimized built-in functions
- Most efficient approach for competitive programming
- Handles all cases correctly
- Standard method for permutation problems

## 🎯 Problem Variations

### Variation 1: Permutations with Repetition
**Problem**: Generate all permutations allowing character repetition.

**Link**: [CSES Problem Set - Permutations with Repetition](https://cses.fi/problemset/task/permutations_with_repetition)

```python
def permutations_with_repetition(s, length):
    from itertools import product
    
    result = []
    for perm in product(s, repeat=length):
        result.append(''.join(perm))
    
    return sorted(result)
```

### Variation 2: K-Permutations
**Problem**: Generate all permutations of length k from a string.

**Link**: [CSES Problem Set - K-Permutations](https://cses.fi/problemset/task/k_permutations)

```python
def k_permutations(s, k):
    from itertools import permutations
    
    perms = set(permutations(s, k))
    result = [''.join(p) for p in perms]
    return sorted(result)
```

### Variation 3: Permutations with Constraints
**Problem**: Generate permutations satisfying certain constraints.

**Link**: [CSES Problem Set - Constrained Permutations](https://cses.fi/problemset/task/constrained_permutations)

```python
def constrained_permutations(s, constraints):
    from itertools import permutations
    
    perms = set(permutations(s))
    result = []
    
    for perm in perms:
        valid = True
        for constraint in constraints:
            if not constraint(''.join(perm)):
                valid = False
                break
        if valid:
            result.append(''.join(perm))
    
    return sorted(result)
```

## 🔗 Related Problems

- **[Permutation Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Permutation problems
- **[String Manipulation Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: String manipulation problems
- **[Backtracking Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Backtracking problems
- **[Combinatorics Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Combinatorics problems

## 📚 Learning Points

1. **Permutation Generation**: Essential for understanding combinatorial problems
2. **Duplicate Handling**: Key technique for efficient permutation generation
3. **Lexicographic Ordering**: Important for understanding string ordering
4. **Backtracking**: Critical for understanding recursive algorithms
5. **Built-in Functions**: Foundation for many competitive programming solutions
6. **Combinatorics**: Critical for understanding counting principles

## 📝 Summary

The Creating Strings problem demonstrates permutation generation and string manipulation concepts for efficient combinatorial problem solving. We explored three approaches:

1. **Naive Recursive Generation**: O(n! × n) time complexity using simple recursion, inefficient due to duplicate generation
2. **Backtracking with Duplicate Handling**: O(n! × n) time complexity using backtracking with proper duplicate handling, better approach for permutation generation
3. **Built-in itertools.permutations**: O(n! × n × log(n!)) time complexity using optimized built-in functions, optimal approach for competitive programming

The key insights include understanding permutation generation principles, using duplicate handling for efficient generation, and applying built-in optimization for optimal performance. This problem serves as an excellent introduction to combinatorial algorithms and string manipulation in competitive programming.
