---
layout: simple
title: "String Reorder"
permalink: /problem_soulutions/introductory_problems/string_reorder_analysis
---

# String Reorder

## Problem Description

**Problem**: Given a string, find the lexicographically smallest string that can be obtained by reordering its characters.

**Input**: A string s (1 ≤ |s| ≤ 10⁶)

**Output**: The lexicographically smallest string that can be obtained by reordering the characters of s.

**Example**:
```
Input: "CAB"

Output: "ABC"

Explanation: By reordering the characters, we can get "ABC", "ACB", "BAC", "BCA", "CAB", "CBA". 
The lexicographically smallest is "ABC".
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Reorder characters in a string
- Find the lexicographically smallest result
- Handle duplicate characters correctly

**Key Observations:**
- Lexicographical order: compare characters from left to right
- Smaller characters should come first
- Need to handle character frequencies
- Can use sorting or frequency counting

### Step 2: Simple Sorting Approach
**Idea**: Sort the characters to get lexicographically smallest string.

```python
def string_reorder_sort(s):
    # Sort the string directly
    return ''.join(sorted(s))
```

**Why this works:**
- Sorting arranges characters in ascending order
- This gives us the lexicographically smallest arrangement
- Handles duplicates correctly

### Step 3: Frequency Counting Approach
**Idea**: Count character frequencies and construct result systematically.

```python
def string_reorder_freq(s):
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

**Why this is better:**
- More explicit about handling frequencies
- O(n) time complexity
- Clear and readable implementation

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_string_reorder():
    s = input().strip()
    
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct lexicographically smallest string
    result = ""
    for i in range(26):
        result += chr(ord('A') + i) * freq[i]
    
    print(result)

# Main execution
if __name__ == "__main__":
    solve_string_reorder()
```

**Why this works:**
- Efficient frequency counting approach
- Handles all character frequencies correctly
- Produces lexicographically smallest result

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("CAB", "ABC"),
        ("AAB", "AAB"),
        ("CBA", "ABC"),
        ("ZZZ", "ZZZ"),
        ("ABCD", "ABCD"),
    ]
    
    for s, expected in test_cases:
        result = solve_test(s)
        print(f"Input: '{s}'")
        print(f"Expected: '{expected}', Got: '{result}'")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(s):
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    result = ""
    for i in range(26):
        result += chr(ord('A') + i) * freq[i]
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - where n is string length
- **Space**: O(1) - constant space for frequency array

### Why This Solution Works
- **Efficient**: Linear time complexity
- **Correct**: Handles all cases properly
- **Clear**: Easy to understand and implement

## 🎯 Key Insights

### 1. **Lexicographical Order**
- Compare characters from left to right
- Smaller characters come first
- Handle duplicates by placing them consecutively

### 2. **Character Frequency**
- Count occurrences of each character
- Place characters in sorted order
- Repeat characters according to their frequency

### 3. **Implementation Strategy**
- Use frequency counting for efficiency
- Sort characters by ASCII values
- Construct result systematically

## 🎯 Problem Variations

### Variation 1: Case-Insensitive Reorder
**Problem**: Find lexicographically smallest string ignoring case.

```python
def case_insensitive_reorder(s):
    # Convert to uppercase for comparison
    s_upper = s.upper()
    
    # Count frequencies (case-insensitive)
    freq = [0] * 26
    for c in s_upper:
        freq[ord(c) - ord('A')] += 1
    
    # Construct result
    result = ""
    for i in range(26):
        result += chr(ord('A') + i) * freq[i]
    
    return result
```

### Variation 2: Custom Character Order
**Problem**: Find lexicographically smallest string using custom character order.

```python
def custom_order_reorder(s, char_order):
    # char_order is a string defining the order of characters
    # e.g., "ZYX...CBA" for reverse alphabetical order
    
    # Create mapping from character to position
    char_to_pos = {c: i for i, c in enumerate(char_order)}
    
    # Count frequencies
    freq = [0] * len(char_order)
    for c in s:
        if c in char_to_pos:
            freq[char_to_pos[c]] += 1
    
    # Construct result using custom order
    result = ""
    for i in range(len(char_order)):
        result += char_order[i] * freq[i]
    
    return result
```

### Variation 3: Weighted Characters
**Problem**: Each character has a weight. Find string with minimum total weight.

```python
def weighted_reorder(s, weights):
    # weights[c] = weight of character c
    # Sort characters by weight (ascending)
    sorted_chars = sorted(s, key=lambda c: weights.get(c, 0))
    
    return ''.join(sorted_chars)
```

### Variation 4: Constrained Reorder
**Problem**: Reorder string with constraints (e.g., certain characters must be adjacent).

```python
def constrained_reorder(s, constraints):
    # constraints is a list of (char1, char2) pairs that must be adjacent
    # This is a more complex problem requiring graph theory
    
    # For simplicity, assume we need to keep certain pairs together
    # This would require finding connected components in a graph
    
    # Place constrained pairs first, then remaining characters
    used = set()
    result = ""
    
    # Handle constraints (simplified)
    for char1, char2 in constraints:
        if char1 in s and char2 in s:
            count1 = s.count(char1)
            count2 = s.count(char2)
            result += char1 * count1 + char2 * count2
            used.add(char1)
            used.add(char2)
    
    # Add remaining characters
    remaining = [c for c in s if c not in used]
    result += ''.join(sorted(remaining))
    
    return result
```

### Variation 5: K-th Lexicographically Smallest
**Problem**: Find the k-th lexicographically smallest string.

```python
def kth_lexicographical(s, k):
    from itertools import permutations
    
    # Generate all permutations and sort them
    perms = sorted(set(''.join(p) for p in permutations(s)))
    
    # Return k-th permutation (1-indexed)
    if k <= len(perms):
        return perms[k - 1]
    else:
        return "No such string exists"
```

## 🔗 Related Problems

- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: String manipulation
- **[Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)**: Permutation generation
- **[Palindrome Reorder](/cses-analyses/problem_soulutions/introductory_problems/palindrome_reorder_analysis)**: String reordering problems

## 📚 Learning Points

1. **Lexicographical Order**: Understanding string comparison
2. **Character Frequency**: Counting and handling duplicates
3. **Sorting Algorithms**: Using sorting for string manipulation
4. **String Construction**: Building strings systematically

---

**This is a great introduction to string manipulation and lexicographical ordering!** 🎯
