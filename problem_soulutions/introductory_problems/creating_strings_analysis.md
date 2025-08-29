---
layout: simple
title: "Creating Strings"
permalink: /problem_soulutions/introductory_problems/creating_strings_analysis
---

# Creating Strings

## Problem Description

**Problem**: Given a string, generate all possible permutations of its characters.

**Input**: A string s (1 ≤ |s| ≤ 8)

**Output**: 
- First line: number of distinct permutations
- Next lines: each permutation on a separate line (in lexicographic order)

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Generate all possible arrangements of characters in the string
- Handle duplicate characters correctly
- Output in lexicographic (alphabetical) order
- Count the total number of distinct permutations

**Key Observations:**
- For a string of length n, there are n! total arrangements
- But with duplicates, we get fewer distinct permutations
- We need to avoid generating duplicate permutations

### Step 2: Using Built-in Permutations
**Idea**: Use Python's itertools.permutations to generate all permutations.

```python
from itertools import permutations

def solve_with_itertools(s):
    # Generate all permutations
    perms = set(permutations(s))  # Use set to remove duplicates
    
    # Convert to strings and sort
    result = [''.join(p) for p in perms]
    result.sort()
    
    return result
```

**Why this works:**
- `itertools.permutations()` generates all possible arrangements
- Using a set automatically removes duplicates
- Sorting ensures lexicographic order

### Step 3: Manual Permutation Generation
**Idea**: Implement permutation generation manually using backtracking.

```python
def solve_manual(s):
    def generate_permutations(chars, current, used, result):
        if len(current) == len(chars):
            result.append(''.join(current))
            return
        
        for i in range(len(chars)):
            if not used[i]:
                # Skip duplicates
                if i > 0 and chars[i] == chars[i-1] and not used[i-1]:
                    continue
                
                used[i] = True
                current.append(chars[i])
                generate_permutations(chars, current, used, result)
                current.pop()
                used[i] = False
    
    chars = list(s)
    chars.sort()  # Sort to handle duplicates properly
    result = []
    generate_permutations(chars, [], [False] * len(chars), result)
    return result
```

**Why this works:**
- Backtracking generates all possible arrangements
- We skip duplicate characters to avoid duplicate permutations
- Sorting the input helps with duplicate detection

### Step 4: Complete Solution
**Putting it all together:**

```python
from itertools import permutations

def solve_creating_strings():
    s = input().strip()
    
    # Generate all permutations and remove duplicates
    perms = set(permutations(s))
    
    # Convert to strings and sort
    result = [''.join(p) for p in perms]
    result.sort()
    
    # Print output
    print(len(result))
    for perm in result:
        print(perm)

# Main execution
if __name__ == "__main__":
    solve_creating_strings()
```

**Why this works:**
- Simple and efficient using built-in functions
- Automatically handles duplicates
- Produces correct output format

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("abc", 6),      # 3! = 6 permutations
        ("aab", 3),      # 3!/2! = 3 distinct permutations
        ("aaa", 1),      # Only 1 distinct permutation
    ]
    
    for s, expected_count in test_cases:
        result = solve_test(s)
        print(f"String: {s}")
        print(f"Expected count: {expected_count}")
        print(f"Got count: {len(result)}")
        print(f"Permutations: {result}")
        print(f"{'✓ PASS' if len(result) == expected_count else '✗ FAIL'}")
        print()

def solve_test(s):
    perms = set(permutations(s))
    result = [''.join(p) for p in perms]
    result.sort()
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Generation**: O(n!) - we generate all n! permutations
- **Sorting**: O(n! × n × log(n!)) - sorting n! strings of length n
- **Overall**: O(n! × n × log(n!))

### Space Complexity
- O(n! × n) - storing all permutations

### Why This Solution Works
- **Complete**: Generates all possible arrangements
- **Correct**: Handles duplicates properly
- **Efficient**: Uses optimized built-in functions

## 🎯 Key Insights

### 1. **Permutation Counting**
- For string with unique characters: n! permutations
- With duplicates: n! / (count1! × count2! × ...)

### 2. **Duplicate Handling**
- Use set to automatically remove duplicates
- Or implement duplicate skipping in manual generation

### 3. **Lexicographic Order**
- Sort the result list to get alphabetical order
- Or generate permutations in order using next_permutation

## 🔗 Related Problems

- **[Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)**: Generate permutations of numbers
- **[String Reorder](/cses-analyses/problem_soulutions/introductory_problems/string_reorder_analysis)**: String manipulation
- **[Gray Code](/cses-analyses/problem_soulutions/introductory_problems/gray_code_analysis)**: Generate sequences

## 🎯 Problem Variations

### Variation 1: K-th Permutation
**Problem**: Find the k-th lexicographical permutation of the string.

```python
def kth_string_permutation(s, k):
    from math import factorial
    
    chars = list(s)
    chars.sort()
    result = []
    k -= 1  # Convert to 0-based indexing
    
    while chars:
        n = len(chars)
        fact = factorial(n - 1)
        index = k // fact
        result.append(chars.pop(index))
        k %= fact
    
    return ''.join(result)
```

### Variation 2: Permutations with Constraints
**Problem**: Generate permutations where certain characters must maintain relative order.

```python
def constrained_string_permutations(s, constraints):
    # constraints: list of (a, b) where char a must come before char b
    # This requires topological sorting approach
    pass
```

### Variation 3: Partial Permutations
**Problem**: Generate all permutations of length k from string of length n.

```python
def partial_string_permutations(s, k):
    from itertools import permutations
    return [''.join(p) for p in permutations(s, k)]
```

### Variation 4: Permutations with Repetition
**Problem**: Generate all possible strings by rearranging characters (allowing repetition).

```python
def string_combinations_with_repetition(s, length):
    from itertools import product
    return [''.join(p) for p in product(s, repeat=length)]
```

### Variation 5: Unique Permutations Only
**Problem**: Generate only unique permutations (handle duplicates efficiently).

```python
def unique_string_permutations(s):
    from itertools import permutations
    perms = set(permutations(s))
    return [''.join(p) for p in sorted(perms)]
```

## 📚 Learning Points

1. **Combinatorics**: Understanding permutation counting
2. **Backtracking**: Manual permutation generation
3. **Duplicate Handling**: Avoiding redundant permutations
4. **Built-in Functions**: Using language features efficiently

---

**This is a great introduction to combinatorics and backtracking!** 🎯
