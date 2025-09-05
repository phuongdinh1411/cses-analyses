---
layout: simple
title: "Removing Digits - Minimum Steps to Zero"
permalink: /problem_soulutions/dynamic_programming/removing_digits_analysis
---

# Removing Digits - Minimum Steps to Zero

## 📋 Problem Description

Given an integer n, find the minimum number of steps to reduce it to 0. In each step, you can subtract any digit from the current number.

This is a classic dynamic programming problem that requires finding the minimum number of steps to reduce a number to zero by subtracting its digits. The solution involves using bottom-up DP to build optimal solutions from smaller subproblems.

**Input**: 
- n: the starting integer

**Output**: 
- Minimum number of steps to reach 0

**Constraints**:
- 1 ≤ n ≤ 10⁶

**Example**:
```
Input:
27

Output:
5

Explanation**: 
Starting with 27, we can:
- Subtract 7: 27 → 20
- Subtract 2: 20 → 18
- Subtract 8: 18 → 10
- Subtract 1: 10 → 9
- Subtract 9: 9 → 0
Total: 5 steps (minimum)
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the minimum number of steps to reduce a number to zero by subtracting its digits
- **Key Insight**: Use dynamic programming to build optimal solutions from smaller subproblems
- **Challenge**: Avoid exponential time complexity with recursive approach

### Step 2: Initial Approach
**Recursive brute force (inefficient but correct):**

```python
def removing_digits_brute_force(n):
    def min_steps(num):
        if num == 0:
            return 0
        if num < 0:
            return float('inf')
        
        # Extract all digits
        digits = set()
        temp = num
        while temp > 0:
            digits.add(temp % 10)
            temp //= 10
        
        min_count = float('inf')
        for digit in digits:
            if digit > 0:  # Don't subtract 0
                result = min_steps(num - digit)
                if result != float('inf'):
                    min_count = min(min_count, 1 + result)
        
        return min_count
    
    return min_steps(n)
```

**Why this is inefficient**: We're trying all possible digit removals, which leads to exponential complexity. For each number, we try all its digits, leading to O(d^n) complexity where d is the number of digits.

### Improvement 1: Recursive with Memoization - O(n)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def removing_digits_memoization(n):
    memo = {}
    
    def min_steps(num):
        if num in memo:
            return memo[num]
        
        if num == 0:
            return 0
        if num < 0:
            return float('inf')
        
        # Extract all digits
        digits = set()
        temp = num
        while temp > 0:
            digits.add(temp % 10)
            temp //= 10
        
        min_count = float('inf')
        for digit in digits:
            if digit > 0:  # Don't subtract 0
                result = min_steps(num - digit)
                if result != float('inf'):
                    min_count = min(min_count, 1 + result)
        
        memo[num] = min_count
        return min_count
    
    return min_steps(n)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n) complexity.

### Step 3: Optimization/Alternative
**Dynamic Programming approach:**

```python
def removing_digits_dp(n):
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0 and i - digit >= 0:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            temp //= 10
    
    return dp[n]
```

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_removing_digits():
    n = int(input())
    
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0 and i - digit >= 0:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            temp //= 10
    
    print(dp[n])

# Main execution
if __name__ == "__main__":
    solve_removing_digits()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (27, 5),
        (10, 1),
        (123, 3),
        (1, 1),
        (999, 1),
    ]
    
    for n, expected in test_cases:
        result = solve_test(n)
        print(f"n={n}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}"
        print("✓ Passed")
        print()

def solve_test(n):
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0 and i - digit >= 0:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            temp //= 10
    
    return dp[n]

test_solution()
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(d^n) | O(n) | Try all digit removals |
| Memoized | O(n) | O(n) | Store subproblem results |
| Bottom-up DP | O(n) | O(n) | Build from smaller subproblems |

### Time Complexity
- **Time**: O(n*d) - we fill a 1D DP array and extract digits
- **Space**: O(n) - we store the entire DP array

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes minimum steps using optimal substructure
- **State Transition**: dp[i] = min(1 + dp[i-digit]) for all valid digits
- **Base Case**: dp[0] = 0
- **Optimal Substructure**: Optimal solution can be built from smaller subproblems

## 🎨 Visual Example

### Input Example
```
Starting Number: 27
```

### All Possible Paths to Zero
```
Starting with 27:

Path 1: 27 → 20 → 18 → 10 → 9 → 0 (5 steps)
- Subtract 7: 27 → 20
- Subtract 2: 20 → 18
- Subtract 8: 18 → 10
- Subtract 1: 10 → 9
- Subtract 9: 9 → 0

Path 2: 27 → 25 → 23 → 20 → 18 → 10 → 9 → 0 (7 steps)
- Subtract 2: 27 → 25
- Subtract 5: 25 → 23
- Subtract 3: 23 → 20
- Subtract 2: 20 → 18
- Subtract 8: 18 → 10
- Subtract 1: 10 → 9
- Subtract 9: 9 → 0

Minimum: 5 steps
```

### DP Table Construction
```
dp[i] = minimum steps to reduce i to 0

Initial state:
dp = [0, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞]
     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27

Base case: dp[0] = 0 (no steps needed for 0)

For each number i from 1 to 27:
  dp[i] = min(1 + dp[i-digit]) for all digits in i

dp[1] = min(1 + dp[0]) = min(1 + 0) = 1
dp[2] = min(1 + dp[0]) = min(1 + 0) = 1
dp[3] = min(1 + dp[0]) = min(1 + 0) = 1
...
dp[10] = min(1 + dp[9], 1 + dp[0]) = min(1 + 1, 1 + 0) = 1
dp[11] = min(1 + dp[10], 1 + dp[0]) = min(1 + 1, 1 + 0) = 1
...
dp[20] = min(1 + dp[18], 1 + dp[0]) = min(1 + 2, 1 + 0) = 1
dp[27] = min(1 + dp[20], 1 + dp[25]) = min(1 + 1, 1 + 2) = 2

Final: dp[27] = 2 steps
```

### Step-by-Step DP Process
```
Target: 27

Step 1: Initialize
dp[0] = 0 (base case)
All other dp[i] = ∞

Step 2: Calculate single digits
dp[1] = 1, dp[2] = 1, dp[3] = 1, ..., dp[9] = 1

Step 3: Calculate two-digit numbers
dp[10] = min(1 + dp[9], 1 + dp[0]) = min(2, 1) = 1
dp[11] = min(1 + dp[10], 1 + dp[0]) = min(2, 1) = 1
...
dp[20] = min(1 + dp[18], 1 + dp[0]) = min(3, 1) = 1

Step 4: Calculate target
dp[27] = min(1 + dp[20], 1 + dp[25]) = min(2, 3) = 2

Final result: dp[27] = 2 steps
```

### Visual DP Table
```
Number: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
Steps:  0  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  2

Key transitions:
27 → 20 (subtract 7): dp[27] = 1 + dp[20] = 1 + 1 = 2
27 → 25 (subtract 2): dp[27] = 1 + dp[25] = 1 + 1 = 2
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(10^n)      │ O(n)         │ Try all      │
│                 │              │              │ digit choices│
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP Bottom-up    │ O(n×log n)   │ O(n)         │ Build from   │
│                 │              │              │ smaller nums │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP Top-down     │ O(n×log n)   │ O(n)         │ Memoization  │
│                 │              │              │ with recursion│
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS             │ O(n×log n)   │ O(n)         │ Level by     │
│                 │              │              │ level search │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Removing Digits Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: number n │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize      │
              │ dp[0] = 0       │
              │ dp[i] = ∞       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For i = 1 to n: │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Extract all     │
              │ digits of i     │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each digit: │
              │ dp[i] = min(    │
              │ dp[i], 1 +      │
              │ dp[i-digit])    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return dp[n]    │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Dynamic Programming for Digit Problems**
- Find optimal substructure in digit problems
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **1D DP Array**
- Use 1D table for single number problems
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Digit Extraction**
- Extract digits efficiently
- Important for understanding
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Removing Digits with Different Costs
**Problem**: Different digits have different costs.

```python
def removing_digits_with_costs(n, costs):
    # dp[i] = minimum cost to reduce i to 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0 and i - digit >= 0:
                cost = costs.get(digit, 1)
                dp[i] = min(dp[i], cost + dp[i - digit])
            temp //= 10
    
    return dp[n] if dp[n] != float('inf') else -1

# Example usage
costs = {1: 2, 2: 3, 7: 1, 8: 4, 9: 2}
result = removing_digits_with_costs(27, costs)
print(f"Minimum cost to reduce 27: {result}")
```

### Variation 2: Removing Digits with Constraints
**Problem**: Can only remove certain digits.

```python
def removing_digits_with_constraints(n, allowed_digits):
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit in allowed_digits and i - digit >= 0:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            temp //= 10
    
    return dp[n] if dp[n] != float('inf') else -1

# Example usage
allowed = {1, 2, 5, 7}
result = removing_digits_with_constraints(27, allowed)
print(f"Minimum steps with constraints: {result}")
```

### Variation 3: Removing Digits with Multiple Numbers
**Problem**: Start with multiple numbers and reduce them all to 0.

```python
def removing_digits_multiple_numbers(numbers):
    max_num = max(numbers)
    
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (max_num + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, max_num + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0 and i - digit >= 0:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            temp //= 10
    
    # Sum up steps for all numbers
    total_steps = sum(dp[num] for num in numbers)
    return total_steps

# Example usage
numbers = [27, 15, 8]
result = removing_digits_multiple_numbers(numbers)
print(f"Total steps for all numbers: {result}")
```

### Variation 4: Removing Digits with Path Tracking
**Problem**: Find the actual sequence of digits removed.

```python
def removing_digits_with_path(n):
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    # prev[i] = previous number in optimal path
    prev = [-1] * (n + 1)
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0 and i - digit >= 0:
                if 1 + dp[i - digit] < dp[i]:
                    dp[i] = 1 + dp[i - digit]
                    prev[i] = i - digit
            temp //= 10
    
    # Reconstruct path
    path = []
    current = n
    while current > 0:
        path.append(current - prev[current])
        current = prev[current]
    
    return dp[n], path[::-1]

# Example usage
steps, path = removing_digits_with_path(27)
print(f"Steps: {steps}, Path: {path}")
```

### Variation 5: Removing Digits with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def optimized_removing_digits(n):
    # Use set for faster digit lookup
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        # Extract digits more efficiently
        digits = set()
        temp = i
        while temp > 0:
            digits.add(temp % 10)
            temp //= 10
        
        # Try all digits
        for digit in digits:
            if digit > 0 and i - digit >= 0:
                dp[i] = min(dp[i], 1 + dp[i - digit])
    
    return dp[n]

# Example usage
result = optimized_removing_digits(27)
print(f"Optimized minimum steps: {result}")
```

## 🔗 Related Problems

- **[Dynamic Programming Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar DP problems
- **[Digit Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar digit problems
- **[Optimization Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: General optimization problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for digit optimization problems
2. **1D DP Arrays**: Important for single number problems
3. **Digit Extraction**: Important for understanding number manipulation
4. **Path Reconstruction**: Important for understanding optimal solutions

---

**This is a great introduction to dynamic programming for digit optimization problems!** 🎯
            temp //= 10
        
        min_count = float('inf')
        for digit in digits:
            if digit > 0:  # Don't subtract 0
                result = min_steps(num - digit)
                if result != float('inf'):
                    min_count = min(min_count, 1 + result)
        
        memo[num] = min_count
        return memo[num]
    
    return min_steps(n)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def removing_digits_dp(n):
    # dp[i] = minimum steps to reach 0 from i
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case: 0 steps needed to reach 0
    
    for i in range(1, n + 1):
        # Extract all digits of i
        digits = set()
        temp = i
        while temp > 0:
            digits.add(temp % 10)
            temp //= 10
        
        # Try subtracting each digit
        for digit in digits: if digit > 0 and i >= 
digit: dp[i] = min(dp[i], 1 + dp[i - digit])
    
    return dp[n]
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each number i, we consider all its digits and find the minimum steps needed.

### Alternative: Optimized DP with Digit Extraction - O(n)
**Description**: Use a more efficient digit extraction method.

```python
def removing_digits_optimized(n):
    # dp[i] = minimum steps to reach 0 from i
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        # Extract digits more efficiently
        num = i
        while num > 0:
            digit = num % 10
            if digit > 0 and i >= digit:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            num //= 10
    
    return dp[n]
```

**Why this works**: This approach extracts digits more efficiently and processes them directly without storing them in a set.

## Final Optimal Solution

```python
n = int(input())

# dp[i] = minimum steps to reach 0 from i
dp = [float('inf')] * (n + 1)
dp[0] = 0  # Base case

for i in range(1, n + 1):
    # Extract all digits of i
    num = i
    while num > 0:
        digit = num % 10
        if digit > 0 and i >= digit:
            dp[i] = min(dp[i], 1 + dp[i - digit])
        num //= 10

print(dp[n])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(d^n) | O(n) | Try all digit removals |
| Memoization | O(n) | O(n) | Store subproblem results |
| Bottom-Up DP | O(n) | O(n) | Build solution iteratively |
| Optimized DP | O(n) | O(n) | Efficient digit extraction |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Dynamic Programming**: Build optimal solutions from smaller subproblems
- **Digit Manipulation**: Extract and process digits efficiently
- **Bottom-up Approach**: Iterative solution building
- **Optimization**: Find minimum steps efficiently

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Removing Digits with Path Reconstruction**
```python
def removing_digits_with_path(n):
    # Handle removing digits with path reconstruction
    
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit > 0 and i - digit >= 0:
                if dp[i - digit] + 1 < dp[i]:
                    dp[i] = dp[i - digit] + 1
                    parent[i] = digit
            temp //= 10
    
    if dp[n] == float('inf'):
        return -1, []
    
    # Reconstruct path
    path = []
    current = n
    while current > 0:
        digit = parent[current]
        path.append(digit)
        current -= digit
    
    return dp[n], path
```

#### **2. Removing Digits with Constraints**
```python
def removing_digits_constrained(n, allowed_digits):
    # Handle removing digits with constraints on allowed digits
    
    # dp[i] = minimum steps to reduce i to 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        # Extract all digits
        temp = i
        while temp > 0:
            digit = temp % 10
            if digit in allowed_digits and i - digit >= 0:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            temp //= 10
    
    return dp[n] if dp[n] != float('inf') else -1
```

#### **3. Removing Digits with Dynamic Updates**
```python
def removing_digits_dynamic(operations):
    # Handle removing digits with dynamic updates
    
    n = 0
    dp = [float('inf')] * (10**6 + 1)
    dp[0] = 0
    
    for operation in operations:
        if operation[0] == 'set_number':
            # Set new number
            n = operation[1]
            
            # Recalculate DP array
            dp = [float('inf')] * (n + 1)
            dp[0] = 0
            
            for i in range(1, n + 1):
                # Extract all digits
                temp = i
                while temp > 0:
                    digit = temp % 10
                    if digit > 0 and i - digit >= 0:
                        dp[i] = min(dp[i], 1 + dp[i - digit])
                    temp //= 10
        
        elif operation[0] == 'query':
            # Return current minimum steps
            yield dp[n] if n < len(dp) and dp[n] != float('inf') else -1
    
    return list(removing_digits_dynamic(operations))
```

## 🔗 Related Problems

### Links to Similar Problems
- **Dynamic Programming**: Digit DP, number theory problems
- **Optimization**: Minimum steps, shortest path problems
- **Number Theory**: Digit manipulation, number properties
- **Combinatorics**: Counting and optimization

## 📚 Learning Points

### Key Takeaways
- **Dynamic programming** is essential for optimization problems
- **Digit extraction** is a common technique in number problems
- **Bottom-up approach** is often more efficient than top-down
- **Path reconstruction** can be added for additional insights

## Key Insights for Other Problems

### 1. **Dynamic Programming for Minimization**
**Principle**: Use DP to find minimum steps or cost for problems with overlapping subproblems.
**Applicable to**:
- Minimization problems
- Step counting
- Cost optimization
- Path finding

**Example Problems**:
- Removing digits
- Minimum steps problems
- Cost optimization
- Path finding

### 2. **Digit Manipulation**
**Principle**: Extract and manipulate digits efficiently for number-based problems.
**Applicable to**:
- Number theory problems
- Digit manipulation
- Mathematical problems
- Algorithm design

**Example Problems**:
- Digit problems
- Number theory
- Mathematical problems
- Algorithm design

### 3. **State Definition for Number Problems**
**Principle**: Define states that capture the essential information for number-based problems.
**Applicable to**:
- Dynamic programming
- Number problems
- State machine problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- Number problems
- State machine problems
- Algorithm design

### 4. **Handling Impossible Cases**
**Principle**: Use special values (like infinity) to represent impossible cases in DP.
**Applicable to**:
- Dynamic programming
- Optimization problems
- Error handling
- Algorithm design

**Example Problems**:
- Dynamic programming
- Optimization problems
- Error handling
- Algorithm design

## Notable Techniques

### 1. **DP State Definition Pattern**
```python
# Define DP state for minimization
dp = [float('inf')] * (n + 1)
dp[0] = 0  # Base case
```

### 2. **Digit Extraction Pattern**
```python
# Extract digits efficiently
num = i
while num > 0:
    digit = num % 10
    # Process digit
    num //= 10
```

### 3. **State Transition Pattern**
```python
# Define state transitions for minimization
for digit in digits: if digit > 0 and i >= 
digit: dp[i] = min(dp[i], 1 + dp[i - digit])
```

## Edge Cases to Remember

1. **n = 0**: Return 0 (already at target)
2. **n = 1**: Return 1 (subtract 1)
3. **Single digit**: Handle efficiently
4. **Large n**: Use efficient DP approach
5. **Impossible cases**: Handle with infinity

## Problem-Solving Framework

1. **Identify minimization nature**: This is a minimization problem with overlapping subproblems
2. **Define state**: dp[i] = minimum steps to reach 0 from i
3. **Define transitions**: dp[i] = min(dp[i], 1 + dp[i-digit]) for all digits
4. **Handle base case**: dp[0] = 0
5. **Handle impossible cases**: Use infinity and check for impossible

---

*This analysis shows how to efficiently solve digit manipulation problems using dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Removing Digits with Costs**
**Problem**: Each digit has a different cost to remove, find minimum total cost.
```python
def removing_digits_with_costs(n, digit_costs):
    # digit_costs[i] = cost to remove digit i
    
    # dp[i] = minimum cost to reach 0 from i
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        num = i
        while num > 0:
            digit = num % 10
            if digit > 0 and i >= digit:
                dp[i] = min(dp[i], digit_costs[digit] + dp[i - digit])
            num //= 10
    
    return dp[n]
```

#### **Variation 2: Removing Digits with Constraints**
**Problem**: Can only remove digits that satisfy certain conditions (e.g., even digits only).
```python
def removing_digits_with_constraints(n, constraint_func):
    # constraint_func(digit) = True if digit can be removed
    
    # dp[i] = minimum steps to reach 0 from i
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, n + 1):
        num = i
        while num > 0:
            digit = num % 10
            if digit > 0 and constraint_func(digit) and i >= digit:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            num //= 10
    
    return dp[n] if dp[n] != float('inf') else -1
```

#### **Variation 3: Removing Digits with Probabilities**
**Problem**: Each digit removal has a probability of success, find expected minimum steps.
```python
def removing_digits_with_probabilities(n, success_probs):
    # success_probs[i] = probability of successfully removing digit i
    
    # dp[i] = expected minimum steps to reach 0 from i
    dp = [float('inf')] * (n + 1)
    dp[0] = 0.0  # Base case
    
    for i in range(1, n + 1):
        num = i
        while num > 0:
            digit = num % 10
            if digit > 0 and i >= digit:
                expected_steps = 1 / success_probs[digit] + dp[i - digit]
                dp[i] = min(dp[i], expected_steps)
            num //= 10
    
    return dp[n]
```

#### **Variation 4: Removing Digits with Multiple Targets**
**Problem**: Find minimum steps to reach any of multiple target numbers.
```python
def removing_digits_multiple_targets(n, targets):
    # targets = list of target numbers
    
    # dp[i] = minimum steps to reach any target from i
    dp = [float('inf')] * (n + 1)
    
    # Base cases for all targets
    for target in targets: if target <= 
n: dp[target] = 0
    
    for i in range(1, n + 1):
        if dp[i] == float('inf'):
            num = i
            while num > 0:
                digit = num % 10
                if digit > 0 and i >= digit:
                    dp[i] = min(dp[i], 1 + dp[i - digit])
                num //= 10
    
    return dp[n] if dp[n] != float('inf') else -1
```

#### **Variation 5: Removing Digits with Memory**
**Problem**: Remember which digits were removed and avoid repeating patterns.
```python
def removing_digits_with_memory(n, memory_size):
    # dp[i][last_digits] = minimum steps to reach 0 from i with memory of last digits
    
    # Use bit manipulation for memory
    dp = [[float('inf')] * (1 << memory_size) for _ in range(n + 1)]
    dp[0][0] = 0  # Base case
    
    for i in range(1, n + 1):
        for memory in range(1 << memory_size):
            if dp[i][memory] != float('inf'):
                num = i
                while num > 0:
                    digit = num % 10
                    if digit > 0 and i >= digit:
                        # Check if this digit pattern was used recently
                        new_memory = ((memory << 1) | (1 << (digit % memory_size))) & ((1 << memory_size) - 1)
                        if not (memory & (1 << (digit % memory_size))):  # Not used recently
                            dp[i - digit][new_memory] = min(dp[i - digit][new_memory], 1 + dp[i][memory])
                    num //= 10
    
    return min(dp[0])
```

### 🔗 **Related Problems & Concepts**

#### **1. Digit Manipulation Problems**
- **Digit DP**: Count numbers with specific digit properties
- **Number Theory**: Properties of numbers and digits
- **Mathematical Problems**: Problems involving digit operations
- **String Problems**: Treat numbers as strings

#### **2. Dynamic Programming Patterns**
- **1D DP**: Single state variable (number)
- **2D DP**: Two state variables (number, additional constraint)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Optimization Problems**
- **Minimum Steps**: Find minimum operations needed
- **Minimum Cost**: Find minimum cost solution
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **4. Algorithmic Techniques**
- **Greedy Algorithms**: Heuristic optimization
- **Branch and Bound**: Exact optimization
- **Dynamic Programming**: Optimal substructure
- **Linear Programming**: Mathematical optimization

#### **5. Mathematical Concepts**
- **Number Theory**: Properties of integers
- **Combinatorics**: Count valid digit combinations
- **Optimization Theory**: Find optimal solutions
- **Probability Theory**: Random digit processes

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    result = removing_digits_dp(n)
    print(result)
```

#### **2. Range Queries on Digit Removal Results**
```python
def range_digit_removal_queries(max_n, queries):
    # Precompute for all numbers up to max_n
    dp = [float('inf')] * (max_n + 1)
    dp[0] = 0
    
    for i in range(1, max_n + 1):
        num = i
        while num > 0:
            digit = num % 10
            if digit > 0 and i >= digit:
                dp[i] = min(dp[i], 1 + dp[i - digit])
            num //= 10
    
    # Answer queries
    for l, r in queries:
        min_steps = min(dp[i] for i in range(l, r + 1))
        print(min_steps)
```

#### **3. Interactive Digit Removal Problems**
```python
def interactive_digit_removal_game():
    n = int(input("Enter number: "))
    
    print(f"Find minimum steps to reach 0 from {n}")
    
    player_guess = int(input("Enter minimum steps: "))
    actual_steps = removing_digits_dp(n)
    
    if player_guess == actual_steps:
        print("Correct!")
    else:
        print(f"Wrong! Minimum steps is {actual_steps}")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Divisibility**: Properties of numbers and their digits
- **Modular Arithmetic**: Work with large numbers
- **Prime Factorization**: Analyze number properties
- **Digital Roots**: Sum of digits properties

#### **2. Advanced DP Techniques**
- **Digit DP**: Count numbers with specific properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split problems into subproblems
- **Persistent Data Structures**: Maintain number history

#### **3. Combinatorial Analysis**
- **Digit Permutations**: Analyze digit arrangements
- **Digit Combinations**: Count valid digit sets
- **Generating Functions**: Represent digit sequences algebraically
- **Asymptotic Analysis**: Behavior for large numbers

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Digit DP**: Count numbers with specific properties
- **Number Theory Algorithms**: Efficient number operations
- **Optimization Algorithms**: Find optimal solutions
- **Mathematical Algorithms**: Efficient mathematical operations

#### **2. Mathematical Concepts**
- **Number Theory**: Properties of integers and digits
- **Combinatorics**: Counting principles and techniques
- **Optimization Theory**: Finding optimal solutions
- **Probability Theory**: Random processes and outcomes

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Algorithm Design**: Creating efficient solutions

---

*This analysis demonstrates the power of dynamic programming for digit manipulation problems and shows various extensions and applications.* 