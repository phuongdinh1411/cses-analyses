# CSES Array Description - Problem Analysis

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
```

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