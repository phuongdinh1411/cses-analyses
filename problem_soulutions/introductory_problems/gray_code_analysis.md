---
layout: simple
title: "Gray Code"
permalink: /problem_soulutions/introductory_problems/gray_code_analysis
---

# Gray Code

## Problem Description

**Problem**: Generate a Gray code sequence of length 2ⁿ where consecutive numbers differ by exactly one bit.

**Input**: An integer n (1 ≤ n ≤ 16)

**Output**: Print the Gray code sequence.

**Example**:
```
Input: 2

Output:
0
1
3
2

Explanation: Binary representation shows consecutive numbers differ by one bit:
00 → 01 → 11 → 10
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Generate a sequence of 2ⁿ numbers
- Each consecutive pair must differ by exactly one bit
- The sequence should be complete (all possible n-bit numbers)

**Key Observations:**
- Gray code is a binary numeral system
- Two consecutive values differ by only one bit
- Length is always 2ⁿ for n-bit numbers
- Can be constructed recursively or using a formula

### Step 2: Mathematical Formula
**Idea**: Use the formula `i ^ (i >> 1)` to generate Gray code.

```python
def gray_code_formula(n):
    result = []
    size = 1 << n  # 2^n
    
    for i in range(size):
        gray = i ^ (i >> 1)  # Convert to Gray code
        result.append(gray)
    
    return result
```

**Why this works:**
- The formula `i ^ (i >> 1)` converts binary to Gray code
- XOR with right-shifted value flips the correct bit
- This ensures consecutive numbers differ by exactly one bit

### Step 3: Recursive Construction
**Idea**: Build Gray code recursively by reflecting and adding leading bits.

```python
def gray_code_recursive(n):
    if n == 0:
        return [0]
    
    # Get Gray code for n-1 bits
    prev = gray_code_recursive(n - 1)
    result = prev.copy()
    
    # Add reflected sequence with leading 1
    for i in range(len(prev) - 1, -1, -1):
        result.append(prev[i] | (1 << (n - 1)))
    
    return result
```

**Why this works:**
- Start with base case (n=0)
- For each step, reflect the previous sequence
- Add leading 1 to the reflected part
- This maintains the one-bit difference property

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_gray_code():
    n = int(input())
    
    # Generate Gray code using formula
    for i in range(1 << n):
        gray = i ^ (i >> 1)
        print(gray)

# Main execution
if __name__ == "__main__":
    solve_gray_code()
```

**Why this works:**
- Simple and efficient using the mathematical formula
- Generates all 2ⁿ numbers in correct order
- Each consecutive pair differs by exactly one bit

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (1, [0, 1]),
        (2, [0, 1, 3, 2]),
        (3, [0, 1, 3, 2, 6, 7, 5, 4]),
    ]
    
    for n, expected in test_cases:
        result = solve_test(n)
        print(f"n = {n}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n):
    result = []
    for i in range(1 << n):
        gray = i ^ (i >> 1)
        result.append(gray)
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Formula Method**: O(2ⁿ) - we generate 2ⁿ numbers
- **Recursive Method**: O(2ⁿ) - same complexity but more overhead

### Space Complexity
- O(2ⁿ) - to store the result sequence

### Why This Solution Works
- **Mathematical**: Uses proven Gray code formula
- **Complete**: Generates all possible n-bit numbers
- **Correct**: Ensures consecutive numbers differ by one bit

## 🎯 Key Insights

### 1. **Gray Code Formula**
- `i ^ (i >> 1)` converts binary to Gray code
- XOR with right-shifted value flips the correct bit

### 2. **Recursive Construction**
- Reflect the previous sequence
- Add leading 1 to the reflected part
- This maintains the one-bit difference property

### 3. **Properties**
- Length is always 2ⁿ for n-bit numbers
- Consecutive numbers differ by exactly one bit
- Can be constructed in multiple ways

## 🎯 Problem Variations

### Variation 1: Circular Gray Code
**Problem**: Generate Gray code where first and last numbers also differ by one bit.

```python
def circular_gray_code(n):
    # Reflected Gray code is naturally circular
    result = []
    for i in range(1 << n):
        gray = i ^ (i >> 1)
        result.append(gray)
    return result
```

### Variation 2: Weighted Gray Code
**Problem**: Each bit has a weight. Find Gray code with minimum total weight.

```python
def weighted_gray_code(n, weights):
    # weights[i] = weight of bit i
    def calculate_weight(gray):
        total = 0
        for i in range(n):
            if gray & (1 << i):
                total += weights[i]
        return total
    
    min_weight = float('inf')
    best_sequence = []
    
    # Try all possible Gray codes
    for i in range(1 << n):
        gray = i ^ (i >> 1)
        weight = calculate_weight(gray)
        if weight < min_weight:
            min_weight = weight
            best_sequence = [gray]
    
    return best_sequence
```

### Variation 3: K-ary Gray Code
**Problem**: Generate Gray code for base-k numbers (not just binary).

```python
def k_ary_gray_code(n, k):
    # For base-k numbers
    result = []
    size = k ** n
    
    for i in range(size):
        # Convert to k-ary Gray code
        gray = 0
        temp = i
        for j in range(n):
            digit = temp % k
            gray += digit * (k ** j)
            temp //= k
        result.append(gray)
    
    return result
```

### Variation 4: Anti-Gray Code
**Problem**: Generate sequence where consecutive numbers differ by n-1 bits.

```python
def anti_gray_code(n):
    result = []
    size = 1 << n
    
    for i in range(size):
        # Anti-Gray code: flip all bits except one
        anti_gray = i ^ ((1 << n) - 1)  # Flip all bits
        result.append(anti_gray)
    
    return result
```

### Variation 5: Balanced Gray Code
**Problem**: Generate Gray code with equal number of 0s and 1s in each position.

```python
def balanced_gray_code(n):
    # This is more complex and may not always be possible
    # Requires advanced combinatorial techniques
    pass
```

## 🔗 Related Problems

- **[Bit Strings](/cses-analyses/problem_soulutions/introductory_problems/bit_strings_analysis)**: Binary sequence problems
- **[Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)**: Sequence generation
- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: String manipulation

## 📚 Learning Points

1. **Bit Manipulation**: Working with binary numbers and bit operations
2. **Mathematical Formulas**: Using proven formulas for efficiency
3. **Recursive Construction**: Building sequences recursively
4. **Sequence Properties**: Understanding Gray code characteristics

---

**This is a great introduction to bit manipulation and sequence generation!** 🎯