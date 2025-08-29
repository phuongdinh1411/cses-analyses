---
layout: simple
title: "Palindrome Reorder"
permalink: /problem_soulutions/introductory_problems/palindrome_reorder_analysis
---

# Palindrome Reorder

## Problem Description

**Problem**: Given a string, determine if it can be rearranged to form a palindrome. If possible, output one such palindrome; otherwise, output "NO SOLUTION".

**Input**: A string s (1 ≤ |s| ≤ 10⁶)

**Output**: A palindrome if possible, or "NO SOLUTION".

**Example**:
```
Input: AAAACACBA

Output: AAACBCAAA

Explanation: The string can be rearranged to form the palindrome "AAACBCAAA".
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Check if a string can be rearranged into a palindrome
- If possible, construct one such palindrome
- If not possible, return "NO SOLUTION"

**Key Observations:**
- Palindrome reads the same forwards and backwards
- Character frequencies determine feasibility
- Even length: all characters must have even frequency
- Odd length: exactly one character can have odd frequency

### Step 2: Feasibility Check
**Idea**: Count character frequencies and check if palindrome is possible.

```python
def check_palindrome_feasibility(s):
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Count odd frequencies
    odd_count = sum(1 for f in freq if f % 2 == 1)
    
    # Check feasibility
    if odd_count > 1:
        return False  # Cannot form palindrome
    
    return True  # Can form palindrome
```

**Why this works:**
- Count frequency of each character
- For palindrome, at most one character can have odd frequency
- If more than one odd frequency, palindrome is impossible

### Step 3: Palindrome Construction
**Idea**: Build the palindrome using character frequencies.

```python
def construct_palindrome(s):
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

**Why this works:**
- Use half of each character pair for first half
- Place odd character in middle (if exists)
- Mirror first half for second half

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_palindrome_reorder():
    s = input().strip()
    
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    if odd_count > 1:
        print("NO SOLUTION")
        return
    
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
    
    print(first_half + middle + second_half)

# Main execution
if __name__ == "__main__":
    solve_palindrome_reorder()
```

**Why this works:**
- Efficient frequency counting approach
- Handles all cases correctly
- Constructs palindrome systematically

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("AAAACACBA", "AAACBCAAA"),
        ("AAB", "ABA"),
        ("ABC", "NO SOLUTION"),
        ("AAAA", "AAAA"),
        ("A", "A"),
    ]
    
    for s, expected in test_cases:
        result = solve_test(s)
        print(f"Input: '{s}'")
        print(f"Expected: '{expected}', Got: '{result}'")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(s):
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - where n is string length
- **Space**: O(1) - constant space for frequency array

### Why This Solution Works
- **Efficient**: Linear time complexity
- **Complete**: Handles all cases including edge cases
- **Correct**: Follows palindrome properties

## 🎯 Key Insights

### 1. **Palindrome Properties**
- Reads the same forwards and backwards
- Character frequencies determine feasibility
- At most one character can have odd frequency

### 2. **Frequency Analysis**
- Count occurrences of each character
- Check if palindrome is possible
- Use frequencies to construct palindrome

### 3. **Construction Strategy**
- Use half of each character pair for first half
- Place odd character in middle (if exists)
- Mirror first half for second half

## 🎯 Problem Variations

### Variation 1: Lexicographically Smallest Palindrome
**Problem**: Find the lexicographically smallest palindrome.

```python
def lexicographically_smallest_palindrome(s):
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Construct lexicographically smallest palindrome
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

### Variation 2: All Possible Palindromes
**Problem**: Generate all possible palindromes.

```python
def all_palindromes(s):
    from itertools import permutations
    
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    if odd_count > 1:
        return []
    
    # Generate all possible first halves
    first_half_chars = []
    middle = ""
    
    for i in range(26):
        if freq[i] > 0:
            if freq[i] % 2 == 1:
                middle = chr(ord('A') + i)
                freq[i] -= 1
            first_half_chars.extend([chr(ord('A') + i)] * (freq[i] // 2))
    
    # Generate all permutations of first half
    palindromes = set()
    for perm in permutations(first_half_chars):
        first_half = ''.join(perm)
        second_half = first_half[::-1]
        palindrome = first_half + middle + second_half
        palindromes.add(palindrome)
    
    return sorted(palindromes)
```

### Variation 3: Minimum Changes to Make Palindrome
**Problem**: Find minimum changes needed to make string a palindrome.

```python
def min_changes_for_palindrome(s):
    n = len(s)
    changes = 0
    
    # Count mismatched pairs
    for i in range(n // 2):
        if s[i] != s[n - 1 - i]:
            changes += 1
    
    return changes
```

### Variation 4: Palindrome with Constraints
**Problem**: Create palindrome with certain characters in specific positions.

```python
def constrained_palindrome(s, constraints):
    # constraints is a dict: {position: character}
    n = len(s)
    result = [''] * n
    
    # Apply constraints
    for pos, char in constraints.items():
        if pos < n:
            result[pos] = char
            # Mirror constraint
            if pos != n - 1 - pos:
                result[n - 1 - pos] = char
    
    # Check if constraints are compatible
    for i in range(n // 2):
        if result[i] and result[n - 1 - i] and result[i] != result[n - 1 - i]:
            return "NO SOLUTION"
    
    # Fill remaining positions
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Subtract used characters
    for char in result:
        if char:
            freq[ord(char) - ord('A')] -= 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Fill remaining positions
    for i in range(n // 2):
        if not result[i]:
            # Find available character
            for j in range(26):
                if freq[j] >= 2:
                    result[i] = chr(ord('A') + j)
                    result[n - 1 - i] = chr(ord('A') + j)
                    freq[j] -= 2
                    break
    
    # Handle middle character for odd length
    if n % 2 == 1 and not result[n // 2]:
        for j in range(26):
            if freq[j] % 2 == 1:
                result[n // 2] = chr(ord('A') + j)
                break
    
    return ''.join(result)
```

### Variation 5: Palindrome with Minimum Cost
**Problem**: Create palindrome with minimum cost of character changes.

```python
def min_cost_palindrome(s, costs):
    # costs[i][j] = cost to change character i to j
    n = len(s)
    total_cost = 0
    
    for i in range(n // 2):
        char1 = ord(s[i]) - ord('A')
        char2 = ord(s[n - 1 - i]) - ord('A')
        
        if char1 != char2:
            # Find minimum cost to make them equal
            min_cost = float('inf')
            for target in range(26):
                cost = costs[char1][target] + costs[char2][target]
                min_cost = min(min_cost, cost)
            total_cost += min_cost
    
    return total_cost
```

## 🔗 Related Problems

- **[String Reorder](/cses-analyses/problem_soulutions/introductory_problems/string_reorder_analysis)**: String manipulation
- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: String generation
- **[Repetitions](/cses-analyses/problem_soulutions/introductory_problems/repetitions_analysis)**: String analysis

## 📚 Learning Points

1. **Palindrome Properties**: Understanding palindrome characteristics
2. **Frequency Analysis**: Counting character occurrences
3. **String Construction**: Building strings systematically
4. **Feasibility Checking**: Determining if solution exists

---

**This is a great introduction to palindrome problems and string manipulation!** 🎯
