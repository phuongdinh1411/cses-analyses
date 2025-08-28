---
layout: simple
title: "Array Description
permalink: /problem_soulutions/dynamic_programming/array_description_analysis/
---

# Array Description

## Problem Statement
You are given an array of n integers. Your task is to find the number of ways to fill the array with integers between 1 and m so that the absolute difference between any two adjacent numbers is at most 1.

### Input
The first input line has two integers n and m: the size of the array and the maximum value.
The second line has n integers x1,x2,…,xn: the contents of the array. You may change any number to any integer between 1 and m, and you may leave the number as it is.

### Output
Print the number of ways modulo 10^9+7.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 100
- 0 ≤ xi ≤ m (0 means the number is unknown)

### Example
```
Input:
3 5
2 0 2

Output:
3
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(m^n)
**Description**: Try all possible values for unknown positions recursively.

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
```"
**Why this is inefficient**: We're trying all possible values for unknown positions, which leads to exponential complexity. For each unknown position, we try all m values, leading to O(m^n) complexity.

### Improvement 1: Recursive with Memoization - O(n*m²)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def array_description_memoization(n, m, arr):
    MOD = 10**9 + 7
    memo = {}
    
    def count_ways(index, prev_val):
        if (index, prev_val) in memo:
            return memo[(index, prev_val)]
        
        if index == n:
            return 1
        
        current_val = arr[index]
        
        if current_val != 0:
            # Fixed value, check if valid
            if abs(current_val - prev_val) <= 1:
                result = count_ways(index + 1, current_val)
            else:
                result = 0
        else:
            # Try all possible values
            ways = 0
            for val in range(1, m + 1):
                if abs(val - prev_val) <= 1:
                    ways += count_ways(index + 1, val)
            result = ways % MOD
        
        memo[(index, prev_val)] = result
        return result
    
    # Handle first element specially
    if arr[0] != 0:
        return count_ways(1, arr[0])
    else:
        ways = 0
        for val in range(1, m + 1):
            ways += count_ways(1, val)
        return ways % MOD
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n*m²) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n*m²)
**Description**: Use iterative DP to build the solution from smaller subproblems.

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
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each position and previous value, we calculate the number of valid ways.

### Alternative: Optimized DP with State Compression - O(n*m)
**Description**: Use state compression to optimize the DP solution.

```python
def array_description_optimized(n, m, arr):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to fill array from position i with previous value j
    dp = [[0] * (m + 1) for _ in range(2)]  # Use only 2 rows
    
    # Base case: end of array
    for j in range(m + 1):
        dp[0][j] = 1
    
    # Fill from right to left
    for i in range(n - 1, -1, -1):
        current_val = arr[i]
        curr_row = i % 2
        next_row = (i + 1) % 2
        
        # Clear current row
        for j in range(m + 1):
            dp[curr_row][j] = 0
        
        if current_val != 0:
            # Fixed value
            for prev_val in range(m + 1):
                if abs(current_val - prev_val) <= 1:
                    dp[curr_row][prev_val] = dp[next_row][current_val]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        dp[curr_row][prev_val] = (dp[curr_row][prev_val] + dp[next_row][val]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        return dp[0][0]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
        return result
```

**Why this works**: This approach uses only 2 rows instead of n rows, reducing space complexity from O(n*m) to O(m).

## Final Optimal Solution

```python
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
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(m^n) | O(n) | Try all combinations |
| Memoization | O(n*m²) | O(n*m) | Store subproblem results |
| Bottom-Up DP | O(n*m²) | O(n*m) | Build solution iteratively |
| Optimized DP | O(n*m²) | O(m) | Use state compression |

## Key Insights for Other Problems

### 1. **Dynamic Programming for Constraint Satisfaction**
**Principle**: Use DP to count valid configurations that satisfy given constraints.
**Applicable to**:
- Constraint satisfaction problems
- Counting problems
- State machine problems
- Algorithm design

**Example Problems**:
- Array description
- Constraint satisfaction
- Counting problems
- State machine problems

### 2. **State Definition for Constraint Problems**
**Principle**: Define states that capture the essential information for constraint-based problems.
**Applicable to**:
- Dynamic programming
- Constraint problems
- State machine problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- Constraint problems
- State machine problems
- Algorithm design

### 3. **Handling Fixed vs Variable Values**
**Principle**: Distinguish between fixed and variable values in constraint problems.
**Applicable to**:
- Constraint problems
- Dynamic programming
- Algorithm design
- Problem solving

**Example Problems**:
- Constraint problems
- Dynamic programming
- Algorithm design
- Problem solving

### 4. **State Compression in DP**
**Principle**: Use state compression techniques to optimize space usage in DP problems.
**Applicable to**:
- Dynamic programming
- Memory optimization
- Algorithm optimization
- Performance improvement

**Example Problems**:
- Dynamic programming
- Memory optimization
- Algorithm optimization
- Performance improvement

## Notable Techniques

### 1. **Constraint DP Pattern**
```python
# Define DP state for constraint problems
dp = [[0] * (max_val + 1) for _ in range(n + 1)]
for i in range(n):
    for prev_val in range(max_val + 1):
        for curr_val in range(1, max_val + 1):
            if constraint_satisfied(prev_val, curr_val):
                dp[i][prev_val] += dp[i+1][curr_val]
```

### 2. **State Compression Pattern**
```python
# Use only 2 rows for space optimization
dp = [[0] * (max_val + 1) for _ in range(2)]
curr_row = i % 2
next_row = (i + 1) % 2
```

### 3. **Fixed vs Variable Handling**
```python
# Handle fixed and variable values differently
if current_val != 0:
    # Fixed value
    if constraint_satisfied(prev_val, current_val):
        dp[i][prev_val] = dp[i+1][current_val]
else:
    # Variable value
    for val in range(1, max_val + 1):
        if constraint_satisfied(prev_val, val):
            dp[i][prev_val] += dp[i+1][val]
```

## Edge Cases to Remember

1. **n = 1**: Handle single element array
2. **m = 1**: Only one possible value
3. **All values fixed**: Check if valid
4. **All values variable**: Handle properly
5. **Large n**: Use efficient DP approach

## Problem-Solving Framework

1. **Identify constraint nature**: This is a constraint satisfaction problem
2. **Define state**: dp[i][j] = ways to fill from position i with previous value j
3. **Define transitions**: Consider constraint satisfaction
4. **Handle fixed values**: Check constraints for fixed values
5. **Handle variable values**: Try all valid values

---

*This analysis shows how to efficiently solve constraint satisfaction problems using dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Array Description with Different Constraints**
**Problem**: Change the constraint to allow absolute difference of at most k instead of 1.
```python
def array_description_with_k_diff(n, m, arr, k):
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
                if abs(current_val - prev_val) <= k:
                    dp[i][prev_val] = dp[i + 1][current_val]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= k:
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        return dp[0][0]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
        return result
```

#### **Variation 2: Array Description with Sum Constraints**
**Problem**: Add constraint that sum of adjacent elements must be at most s.
```python
def array_description_with_sum_constraint(n, m, arr, max_sum):
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
                if prev_val + current_val <= max_sum:
                    dp[i][prev_val] = dp[i + 1][current_val]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if prev_val + val <= max_sum:
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        return dp[0][0]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
        return result
```

#### **Variation 3: Array Description with Pattern Constraints**
**Problem**: Ensure the array follows a specific pattern (e.g., alternating, increasing, etc.).
```python
def array_description_with_pattern(n, m, arr, pattern_type):
    MOD = 10**9 + 7
    
    # dp[i][j][k] = number of ways to fill array from position i with previous value j and pattern state k
    dp = [[[0] * 2 for _ in range(m + 1)] for _ in range(n + 1)]
    
    # Base case: end of array
    for j in range(m + 1):
        for k in range(2):
            dp[n][j][k] = 1
    
    # Fill from right to left
    for i in range(n - 1, -1, -1):
        current_val = arr[i]
        
        if current_val != 0:
            # Fixed value
            for prev_val in range(m + 1):
                for k in range(2):
                    if pattern_type == "alternating":
                        if (i % 2 == 0 and current_val > prev_val) or (i % 2 == 1 and current_val < prev_val):
                            dp[i][prev_val][k] = dp[i + 1][current_val][1 - k]
                    elif pattern_type == "increasing":
                        if current_val > prev_val:
                            dp[i][prev_val][k] = dp[i + 1][current_val][k]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for k in range(2):
                    for val in range(1, m + 1):
                        if pattern_type == "alternating":
                            if (i % 2 == 0 and val > prev_val) or (i % 2 == 1 and val < prev_val):
                                dp[i][prev_val][k] = (dp[i][prev_val][k] + dp[i + 1][val][1 - k]) % MOD
                        elif pattern_type == "increasing":
                            if val > prev_val:
                                dp[i][prev_val][k] = (dp[i][prev_val][k] + dp[i + 1][val][k]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        return dp[0][0][0]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val][0]) % MOD
        return result
```

#### **Variation 4: Array Description with Cost Minimization**
**Problem**: Find the minimum cost to fill the array while satisfying constraints.
```python
def array_description_with_cost(n, m, arr, costs):
    # costs[i][j] = cost to set position i to value j
    
    # dp[i][j] = minimum cost to fill array from position i with previous value j
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    
    # Base case: end of array
    for j in range(m + 1):
        dp[n][j] = 0
    
    # Fill from right to left
    for i in range(n - 1, -1, -1):
        current_val = arr[i]
        
        if current_val != 0:
            # Fixed value
            for prev_val in range(m + 1):
                if abs(current_val - prev_val) <= 1:
                    dp[i][prev_val] = dp[i + 1][current_val] + costs[i][current_val]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        dp[i][prev_val] = min(dp[i][prev_val], dp[i + 1][val] + costs[i][val])
    
    # Handle first element
    if arr[0] != 0:
        return dp[0][0]
    else:
        min_cost = float('inf')
        for val in range(1, m + 1):
            min_cost = min(min_cost, dp[0][val])
        return min_cost
```

#### **Variation 5: Array Description with Probability**
**Problem**: Each value has a probability of being chosen, find expected number of valid arrays.
```python
def array_description_with_probability(n, m, arr, probabilities):
    # probabilities[i][j] = probability of choosing value j at position i
    
    # dp[i][j] = expected number of valid arrays from position i with previous value j
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    
    # Base case: end of array
    for j in range(m + 1):
        dp[n][j] = 1.0
    
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
                        dp[i][prev_val] += dp[i + 1][val] * probabilities[i][val]
    
    # Handle first element
    if arr[0] != 0:
        return dp[0][0]
    else:
        result = 0.0
        for val in range(1, m + 1):
            result += dp[0][val] * probabilities[0][val]
        return result
```

### 🔗 **Related Problems & Concepts**

#### **1. Constraint Satisfaction Problems**
- **Boolean Satisfiability**: Find satisfying assignments
- **Graph Coloring**: Color vertices with constraints
- **Sudoku**: Fill grid with constraints
- **N-Queens**: Place queens without conflicts

#### **2. Dynamic Programming Patterns**
- **2D DP**: Two state variables (position, previous value)
- **3D DP**: Three state variables (position, previous value, additional state)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Counting Problems**
- **Combinatorial Counting**: Count valid configurations
- **Inclusion-Exclusion**: Count with constraints
- **Generating Functions**: Algebraic approach to counting
- **Burnside's Lemma**: Count orbits under group actions

#### **4. Optimization Problems**
- **Minimum Cost**: Find minimum cost solution
- **Maximum Value**: Find maximum value solution
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **5. Algorithmic Techniques**
- **Recursive Backtracking**: Try all valid configurations
- **Memoization**: Cache computed results
- **Bottom-Up DP**: Build solution iteratively
- **State Space Search**: Explore all possible states

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    result = array_description_dp(n, m, arr)
    print(result)
```

#### **2. Range Queries on Array Descriptions**
```python
def range_array_description_queries(n, m, arr, queries):
    # Precompute for all subarrays
    dp = [[[0] * (m + 1) for _ in range(n + 1)] for _ in range(n + 1)]
    
    # Fill DP for all possible subarrays
    for start in range(n):
        for end in range(start, n):
            # Calculate array description for subarray arr[start:end+1]
            pass
    
    # Answer queries
    for start, end in queries:
        print(dp[start][end][0])
```

#### **3. Interactive Array Description Problems**
```python
def interactive_array_description_game():
    n, m = map(int, input("Enter n and m: ").split())
    arr = list(map(int, input("Enter array: ").split()))
    
    print(f"Array: {arr}")
    print(f"Find ways to fill with values 1 to {m} with adjacent difference ≤ 1")
    
    player_guess = int(input("Enter number of ways: "))
    actual_ways = array_description_dp(n, m, arr)
    
    if player_guess == actual_ways:
        print("Correct!")
    else:
        print(f"Wrong! Number of ways is {actual_ways}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorial Analysis**
- **Catalan Numbers**: Count valid sequences
- **Partition Theory**: Mathematical study of partitions
- **Generating Functions**: Represent sequences algebraically
- **Asymptotic Analysis**: Behavior for large arrays

#### **2. Advanced DP Techniques**
- **Digit DP**: Count arrays with specific properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split problems into subproblems
- **Persistent Data Structures**: Maintain array history

#### **3. Constraint Theory**
- **Constraint Propagation**: Propagate constraints efficiently
- **Arc Consistency**: Ensure constraint consistency
- **Backtracking**: Systematic search with constraints
- **Local Search**: Heuristic constraint satisfaction

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Constraint Satisfaction**: Solve constraint problems
- **Backtracking**: Systematic search algorithms
- **Local Search**: Heuristic optimization
- **Branch and Bound**: Exact optimization

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting principles and techniques
- **Constraint Theory**: Mathematical study of constraints
- **Optimization Theory**: Finding optimal solutions
- **Probability Theory**: Random constraint processes

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Algorithm Design**: Creating efficient solutions

---

*This analysis demonstrates the power of dynamic programming for constraint satisfaction problems and shows various extensions and applications.* 