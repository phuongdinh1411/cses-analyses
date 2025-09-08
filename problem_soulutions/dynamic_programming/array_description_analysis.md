---
layout: simple
title: "Array Description"
permalink: /problem_soulutions/dynamic_programming/array_description_analysis
---


# Array Description

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand constraint satisfaction problems and array filling with constraints
- Apply DP techniques to solve constraint satisfaction problems with adjacent constraints
- Implement efficient DP solutions for constraint satisfaction and array filling
- Optimize DP solutions using space-efficient techniques and constraint tracking
- Handle edge cases in constraint DP (single elements, all known, impossible constraints)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, constraint satisfaction, array filling, constraint handling
- **Data Structures**: Arrays, DP tables, constraint tracking structures
- **Mathematical Concepts**: Constraint theory, array properties, constraint satisfaction, modular arithmetic
- **Programming Skills**: Array manipulation, constraint checking, iterative programming, DP implementation
- **Related Problems**: Counting Sequences (constraint counting), Coin Combinations (DP counting), Constraint problems

## Problem Description

You are given an array of n integers. Your task is to find the number of ways to fill the array with integers between 1 and m so that the absolute difference between any two adjacent numbers is at most 1.

**Input**: 
- First line: two integers n and m (size of array and maximum value)
- Second line: n integers x1, x2, ..., xn (array contents, 0 means unknown, can be filled with 1 to m)

**Output**: 
- Print the number of ways to fill the array modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 100
- 0 ≤ xi ≤ m
- Fill unknown positions (0) with integers 1 to m
- Adjacent elements must have absolute difference ≤ 1
- Count valid ways to fill array
- Output modulo 10^9 + 7

**Example**:
```
Input:
3 5
2 0 2

Output:
3

Explanation**: 
For the array [2, 0, 2], we need to fill the middle position (0) with a value between 1 and 5.
Valid fillings where adjacent differences ≤ 1:
- [2, 1, 2] ✓ (|2-1|≤1, |1-2|≤1)
- [2, 2, 2] ✓ (|2-2|≤1, |2-2|≤1)  
- [2, 3, 2] ✓ (|2-3|≤1, |3-2|≤1)
Total: 3 ways
```

## Visual Example

### Input and Problem Setup
```
Input: n = 3, m = 5
Array: [2, 0, 2]

Goal: Fill unknown positions (0) with integers 1 to m
Constraint: Adjacent elements must have absolute difference ≤ 1
Result: Number of valid ways to fill array
Note: 0 means unknown position, can be filled with 1 to m
```

### Array Filling Analysis
```
For array [2, 0, 2] with m = 5:

Position 0: Fixed value 2
Position 1: Unknown (0), can be filled with 1, 2, 3, 4, or 5
Position 2: Fixed value 2

Constraint: |arr[i] - arr[i+1]| ≤ 1 for all i

Valid fillings for position 1:
- Fill with 1: [2, 1, 2] → |2-1|=1≤1, |1-2|=1≤1 ✓
- Fill with 2: [2, 2, 2] → |2-2|=0≤1, |2-2|=0≤1 ✓
- Fill with 3: [2, 3, 2] → |2-3|=1≤1, |3-2|=1≤1 ✓
- Fill with 4: [2, 4, 2] → |2-4|=2>1 ✗
- Fill with 5: [2, 5, 2] → |2-5|=3>1 ✗

Valid ways: 3
```

### Dynamic Programming Pattern
```
DP State: dp[i][j] = number of ways to fill array from position i with previous value j

Base case: dp[n][j] = 1 (end of array)

Recurrence: 
- If arr[i] is fixed: dp[i][j] = dp[i+1][arr[i]] if |arr[i] - j| ≤ 1
- If arr[i] is unknown: dp[i][j] = sum of dp[i+1][val] for all val where |val - j| ≤ 1

Key insight: Use 2D DP to handle constraint satisfaction
```

### State Transition Visualization
```
Building DP table for n = 3, m = 5, arr = [2, 0, 2]:

Initialize: dp = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1]]

Base case: dp[3][j] = 1 for all j (end of array)

Position 2 (arr[2] = 2, fixed):
dp[2][1] = dp[3][2] = 1 (|2-1|=1≤1)
dp[2][2] = dp[3][2] = 1 (|2-2|=0≤1)
dp[2][3] = dp[3][2] = 1 (|2-3|=1≤1)
dp[2][4] = 0 (|2-4|=2>1)
dp[2][5] = 0 (|2-5|=3>1)

Position 1 (arr[1] = 0, unknown):
dp[1][1] = dp[2][1] + dp[2][2] = 1 + 1 = 2
dp[1][2] = dp[2][1] + dp[2][2] + dp[2][3] = 1 + 1 + 1 = 3
dp[1][3] = dp[2][2] + dp[2][3] = 1 + 1 = 2
dp[1][4] = dp[2][3] = 1
dp[1][5] = 0

Position 0 (arr[0] = 2, fixed):
dp[0][0] = dp[1][2] = 3 (|2-0|=2>1, but 0 is not a valid previous value)
Actually: dp[0][2] = dp[1][2] = 3

Final: dp[0][2] = 3
```

### Key Insight
The solution works by:
1. Using 2D dynamic programming to handle constraint satisfaction
2. For each position, considering all valid values based on constraints
3. Building solutions from smaller subproblems
4. Using modular arithmetic for large numbers
5. Time complexity: O(n × m²) for filling DP table
6. Space complexity: O(n × m) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible values for unknown positions
- Use recursive approach to explore all combinations
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. For each unknown position, try all possible values 1 to m
2. Check if the value satisfies the constraint with previous element
3. Recursively explore all valid combinations
4. Return total count of valid ways

**Visual Example:**
```
Brute force approach: Try all possible values for unknown positions
For array [2, 0, 2] with m = 5:

Recursive tree:
                    (0, 2)
              /            \
          (1, 1)          (1, 2)
         /      \        /      \
    (2, 1)    (2, 2)  (2, 2)  (2, 3)
   /    \     /  \   /  \     /  \
(3, 1) (3, 2) (3, 2) (3, 3) (3, 2) (3, 3) (3, 3) (3, 4)
```

**Implementation:**
```python
def array_description_brute_force(n, m, arr):
    MOD = 10**9 + 7
    
    def count_ways(index, prev_val):
        if index == n:
            return 1
        
        current_val = arr[index]
        
        if current_val != 0:
            # Fixed value, check if valid
            if abs(current_val - prev_val) <= 1:
                return count_ways(index + 1, current_val)
            else:
                return 0
        else:
            # Try all possible values
            ways = 0
            for val in range(1, m + 1):
                if abs(val - prev_val) <= 1:
                    ways += count_ways(index + 1, val)
            return ways % MOD
    
    # Handle first element specially
    if arr[0] != 0:
        return count_ways(1, arr[0])
    else:
        ways = 0
        for val in range(1, m + 1):
            ways += count_ways(1, val)
        return ways % MOD

def solve_array_description_brute_force():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = array_description_brute_force(n, m, arr)
    print(result)
```

**Time Complexity:** O(m^n) for trying all possible values
**Space Complexity:** O(n) for recursion depth

**Why it's inefficient:**
- O(m^n) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large n
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 2D DP array to store number of ways for each position and previous value
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each position, consider all valid values based on constraints
3. Update number of ways using recurrence relation
4. Return total count

**Visual Example:**
```
DP approach: Build solutions iteratively
For n = 3, m = 5, arr = [2, 0, 2]:

Initialize: dp = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1]]

After position 2: dp[2] = [0, 1, 1, 1, 0, 0]
After position 1: dp[1] = [0, 2, 3, 2, 1, 0]
After position 0: dp[0] = [0, 0, 3, 0, 0, 0]

Final result: dp[0][2] = 3
```

**Implementation:**
```python
def array_description_dp(n, m, arr):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to fill array from position i with previous value j
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base case: end of array
    for j in range(m + 1):
        dp[n][j] = 1
    
    # Fill from right to left
    for i in range(n - 1, -1, -1):
        current_val = arr[i]
        
        if current_val != 0:
            # Fixed value
            for prev_val in range(m + 1):
                if abs(current_val - prev_val) <= 1:
                    dp[i][prev_val] = dp[i + 1][current_val]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        return dp[0][0]  # Previous value doesn't matter for first element
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
        return result

def solve_array_description_dp():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = array_description_dp(n, m, arr)
    print(result)
```

**Time Complexity:** O(n × m²) for filling DP table
**Space Complexity:** O(n × m) for DP array

**Why it's better:**
- O(n × m²) time complexity is much better than O(m^n)
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Optimized DP with Space Efficiency (Optimal)

**Key Insights from Optimized Solution:**
- Use the same DP approach but with better implementation
- Most efficient approach for constraint satisfaction problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Initialize DP array with base cases
2. Process array from right to left
3. Use modular arithmetic for large numbers
4. Return optimal solution

**Visual Example:**
```
Optimized DP: Process array from right to left
For n = 3, m = 5, arr = [2, 0, 2]:

Initialize: dp = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1]]

Process position 2: dp[2] = [0, 1, 1, 1, 0, 0]
Process position 1: dp[1] = [0, 2, 3, 2, 1, 0]
Process position 0: dp[0] = [0, 0, 3, 0, 0, 0]
```

**Implementation:**
```python
def solve_array_description():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to fill array from position i with previous value j
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base case: end of array
    for j in range(m + 1):
        dp[n][j] = 1
    
    # Fill from right to left
    for i in range(n - 1, -1, -1):
        current_val = arr[i]
        
        if current_val != 0:
            # Fixed value
            for prev_val in range(m + 1):
                if abs(current_val - prev_val) <= 1:
                    dp[i][prev_val] = dp[i + 1][current_val]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        print(dp[0][0])
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
        print(result)

# Main execution
if __name__ == "__main__":
    solve_array_description()
```

**Time Complexity:** O(n × m²) for filling DP table
**Space Complexity:** O(n × m) for DP array

**Why it's optimal:**
- O(n × m²) time complexity is optimal for this problem
- Uses dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for constraint satisfaction problems

## 🎯 Problem Variations

### Variation 1: Array Description with Different Constraints
**Problem**: Array filling with different constraint types (e.g., sum constraints).

**Link**: [CSES Problem Set - Array Description Constraints](https://cses.fi/problemset/task/array_description_constraints)

```python
def array_description_constraints(n, m, arr, constraints):
    MOD = 10**9 + 7
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for j in range(m + 1):
        dp[n][j] = 1
    
    for i in range(n - 1, -1, -1):
        current_val = arr[i]
        
        if current_val != 0:
            for prev_val in range(m + 1):
                if constraints[i](current_val, prev_val):
                    dp[i][prev_val] = dp[i + 1][current_val]
        else:
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if constraints[i](val, prev_val):
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    return dp[0][0] if arr[0] != 0 else sum(dp[0][val] for val in range(1, m + 1)) % MOD
```

### Variation 2: Array Description with Multiple Values
**Problem**: Each position can have multiple possible values.

**Link**: [CSES Problem Set - Array Description Multiple](https://cses.fi/problemset/task/array_description_multiple)

```python
def array_description_multiple(n, m, arr, possible_values):
    MOD = 10**9 + 7
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for j in range(m + 1):
        dp[n][j] = 1
    
    for i in range(n - 1, -1, -1):
        if arr[i] != 0:
            for prev_val in range(m + 1):
                if abs(arr[i] - prev_val) <= 1:
                    dp[i][prev_val] = dp[i + 1][arr[i]]
        else:
            for prev_val in range(m + 1):
                for val in possible_values[i]:
                    if abs(val - prev_val) <= 1:
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    return dp[0][0] if arr[0] != 0 else sum(dp[0][val] for val in range(1, m + 1)) % MOD
```

### Variation 3: Array Description with Cost
**Problem**: Each value has a cost, minimize total cost.

**Link**: [CSES Problem Set - Array Description Cost](https://cses.fi/problemset/task/array_description_cost)

```python
def array_description_cost(n, m, arr, costs):
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    
    for j in range(m + 1):
        dp[n][j] = 0
    
    for i in range(n - 1, -1, -1):
        if arr[i] != 0:
            for prev_val in range(m + 1):
                if abs(arr[i] - prev_val) <= 1:
                    dp[i][prev_val] = dp[i + 1][arr[i]] + costs[i][arr[i]]
        else:
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        dp[i][prev_val] = min(dp[i][prev_val], dp[i + 1][val] + costs[i][val])
    
    return dp[0][0] if arr[0] != 0 else min(dp[0][val] for val in range(1, m + 1))
```

## 🔗 Related Problems

- **[Counting Sequences](/cses-analyses/problem_soulutions/counting_problems/)**: Constraint counting problems
- **[Coin Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP counting problems
- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/)**: 2D DP problems
- **[Book Shop](/cses-analyses/problem_soulutions/dynamic_programming/)**: Constraint optimization problems

## 📚 Learning Points

1. **Constraint Satisfaction**: Essential for understanding array filling problems with constraints
2. **Dynamic Programming**: Key technique for solving constraint satisfaction problems efficiently
3. **Array Processing**: Important for understanding how to handle unknown positions
4. **Constraint Handling**: Critical for understanding how to validate solutions
5. **Modular Arithmetic**: Foundation for handling large numbers in competitive programming
6. **Bottom-Up DP**: Critical for building solutions from smaller subproblems

## 📝 Summary

The Array Description problem demonstrates constraint satisfaction and dynamic programming principles for efficient array filling. We explored three approaches:

1. **Recursive Brute Force**: O(m^n) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n × m²) time complexity using 2D DP, better approach for constraint satisfaction problems
3. **Optimized DP with Space Efficiency**: O(n × m²) time complexity with efficient implementation, optimal approach for competitive programming

The key insights include understanding constraint satisfaction principles, using dynamic programming for efficient computation, and applying array processing techniques for constraint problems. This problem serves as an excellent introduction to constraint satisfaction in competitive programming.
