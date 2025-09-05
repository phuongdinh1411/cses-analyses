---
layout: simple
title: "Repetitions"
permalink: /problem_soulutions/introductory_problems/repetitions_analysis
---

# Repetitions

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand string analysis and consecutive character counting problems
- [ ] **Objective 2**: Apply sliding window or linear scanning to find maximum consecutive repetitions
- [ ] **Objective 3**: Implement efficient string analysis algorithms with proper consecutive character tracking
- [ ] **Objective 4**: Optimize string analysis using linear scanning and consecutive character counting
- [ ] **Objective 5**: Handle edge cases in string analysis (single character, no repetitions, large strings)

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

**Example**:
```
Input: ATTCGGGA

Output: 3

Explanation: The longest repetition is "GGG" with length 3.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the longest substring with only one character type
- Handle DNA sequence (A, C, G, T)
- Return the length of this longest repetition

**Key Observations:**
- We need to find consecutive same characters
- Can scan the string once to find all repetitions
- Need to track current repetition length and maximum found
- Edge case: last group of characters

### Step 2: Simple Iterative Approach
**Idea**: Scan the string and count consecutive same characters.

```python
def repetitions_simple(sequence):
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
```

**Why this works:**
- Scan string once from left to right
- Count consecutive same characters
- Update maximum when character changes
- Handle last group of characters

### Step 3: Optimized Single Pass
**Idea**: Optimize the approach with cleaner code and better handling.

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
```

**Why this is better:**
- Update maximum inside the loop
- Cleaner logic flow
- Same time complexity but more readable

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_repetitions():
    sequence = input().strip()
    
    n = len(sequence)
    if n == 0:
        print(0)
        return
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    print(max_length)

# Main execution
if __name__ == "__main__":
    solve_repetitions()
```

**Why this works:**
- Efficient single-pass algorithm
- Handles all edge cases correctly
- Clean and readable implementation

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("ATTCGGGA", 3),
        ("AAAA", 4),
        ("ACGT", 1),
        ("A", 1),
        ("AAACCCGGGTTT", 3),
        ("", 0),
    ]
    
    for sequence, expected in test_cases:
        result = solve_test(sequence)
        print(f"Input: '{sequence}'")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(sequence):
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the string
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Efficient**: Linear time complexity
- **Complete**: Handles all cases including edge cases
- **Simple**: Easy to understand and implement

## 🎨 Visual Example

### Input Example
```
Input: "ATTCGGGA"
Output: 3 (longest repetition is "GGG")
```

### String Analysis
```
String: A T T C G G G A
Index:  0 1 2 3 4 5 6 7

Character groups:
- A (position 0): length 1
- TT (positions 1-2): length 2
- C (position 3): length 1
- GGG (positions 4-6): length 3 ← longest
- A (position 7): length 1
```

### Step-by-Step Process
```
Initialize: max_length = 1, current_length = 1

i=0: A (start)
i=1: T ≠ A → reset current_length = 1
i=2: T = T → current_length = 2, max_length = 2
i=3: C ≠ T → reset current_length = 1
i=4: G ≠ C → reset current_length = 1
i=5: G = G → current_length = 2, max_length = 2
i=6: G = G → current_length = 3, max_length = 3
i=7: A ≠ G → reset current_length = 1

Final result: max_length = 3
```

### Algorithm Visualization
```
String: A T T C G G G A
        │ │ │ │ │ │ │ │
        │ │ │ │ │ │ │ └─ A (length 1)
        │ │ │ │ │ │ └─── G (length 3) ← max
        │ │ │ │ │ └───── G (length 3)
        │ │ │ │ └─────── G (length 3)
        │ │ │ └───────── C (length 1)
        │ │ └─────────── T (length 2)
        │ └───────────── T (length 2)
        └─────────────── A (length 1)

Repetitions found:
- A: 1 occurrence
- TT: 2 consecutive T's
- C: 1 occurrence  
- GGG: 3 consecutive G's ← longest
- A: 1 occurrence
```

### Different Examples
```
Example 1: "AAAA" → 4 (all A's)
Example 2: "ABCD" → 1 (no repetitions)
Example 3: "AABBCC" → 2 (AA, BB, CC all length 2)
Example 4: "TTTTGGGGG" → 5 (GGGGG is longest)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Single Pass     │ O(n)         │ O(1)         │ Scan once    │
│                 │              │              │ and track    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Two Pointers    │ O(n)         │ O(1)         │ Expand       │
│                 │              │              │ windows      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Regex           │ O(n)         │ O(n)         │ Pattern      │
│                 │              │              │ matching     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Single Pass Algorithm**
- Scan the string once from left to right
- Track current repetition length
- Update maximum when needed

### 2. **Character Comparison**
- Compare each character with the previous one
- If same, increment current length
- If different, reset current length

### 3. **Edge Case Handling**
- Handle empty string
- Handle single character
- Don't forget the last group of characters

## 🎯 Problem Variations

### Variation 1: Find All Repetitions
**Problem**: Find all repetitions and their positions.

```python
def find_all_repetitions(sequence):
    n = len(sequence)
    repetitions = []
    
    if n == 0:
        return repetitions
    
    current_char = sequence[0]
    current_length = 1
    start_pos = 0
    
    for i in range(1, n):
        if sequence[i] == current_char:
            current_length += 1
        else:
            if current_length > 1:
                repetitions.append((current_char, current_length, start_pos))
            current_char = sequence[i]
            current_length = 1
            start_pos = i
    
    # Don't forget the last group
    if current_length > 1:
        repetitions.append((current_char, current_length, start_pos))
    
    return repetitions
```

### Variation 2: Minimum Repetition Length
**Problem**: Find the shortest repetition (minimum length ≥ 2).

```python
def shortest_repetition(sequence):
    n = len(sequence)
    if n < 2:
        return -1  # No repetition possible
    
    min_length = float('inf')
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            if current_length >= 2:
                min_length = min(min_length, current_length)
            current_length = 1
    
    # Check last group
    if current_length >= 2:
        min_length = min(min_length, current_length)
    
    return min_length if min_length != float('inf') else -1
```

### Variation 3: K-th Longest Repetition
**Problem**: Find the k-th longest repetition.

```python
def kth_longest_repetition(sequence, k):
    n = len(sequence)
    repetitions = []
    
    if n == 0:
        return -1
    
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            if current_length >= 2:
                repetitions.append(current_length)
            current_length = 1
    
    # Check last group
    if current_length >= 2:
        repetitions.append(current_length)
    
    # Sort in descending order
    repetitions.sort(reverse=True)
    
    if k <= len(repetitions):
        return repetitions[k - 1]
    else:
        return -1
```

### Variation 4: Repetitions with Different Characters
**Problem**: Find longest substring with at most k different characters.

```python
def longest_substring_k_chars(sequence, k):
    n = len(sequence)
    if n == 0:
        return 0
    
    char_count = {}
    max_length = 0
    start = 0
    
    for end in range(n):
        char = sequence[end]
        char_count[char] = char_count.get(char, 0) + 1
        
        # Shrink window if we have more than k different characters
        while len(char_count) > k:
            start_char = sequence[start]
            char_count[start_char] -= 1
            if char_count[start_char] == 0:
                del char_count[start_char]
            start += 1
        
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

### Variation 5: DNA Pattern Matching
**Problem**: Find longest repetition that matches a specific pattern.

```python
def pattern_repetition(sequence, pattern):
    n = len(sequence)
    pattern_len = len(pattern)
    
    if n < pattern_len:
        return 0
    
    max_length = 0
    current_length = 0
    
    for i in range(n - pattern_len + 1):
        # Check if substring matches pattern
        substring = sequence[i:i + pattern_len]
        if substring == pattern:
            current_length += pattern_len
            max_length = max(max_length, current_length)
        else:
            current_length = 0
    
    return max_length
```

## 🔗 Related Problems

- **[String Reorder](/cses-analyses/problem_soulutions/introductory_problems/string_reorder_analysis)**: String manipulation
- **[Palindrome Reorder](/cses-analyses/problem_soulutions/introductory_problems/palindrome_reorder_analysis)**: String analysis
- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: String problems

## 📚 Learning Points

1. **Single Pass Algorithms**: Efficient string processing
2. **Character Comparison**: Comparing adjacent elements
3. **Edge Case Handling**: Empty strings and single characters
4. **Sliding Window**: Pattern for substring problems

---

**This is a great introduction to string processing and single-pass algorithms!** 🎯 