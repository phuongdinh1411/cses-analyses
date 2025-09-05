---
layout: simple
title: "Array Description"
permalink: /problem_soulutions/dynamic_programming/array_description_analysis
---


# Array Description

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand constraint satisfaction problems and array filling with constraints
- [ ] **Objective 2**: Apply DP techniques to solve constraint satisfaction problems with adjacent constraints
- [ ] **Objective 3**: Implement efficient DP solutions for constraint satisfaction and array filling
- [ ] **Objective 4**: Optimize DP solutions using space-efficient techniques and constraint tracking
- [ ] **Objective 5**: Handle edge cases in constraint DP (single elements, all known, impossible constraints)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, constraint satisfaction, array filling, constraint handling
- **Data Structures**: Arrays, DP tables, constraint tracking structures
- **Mathematical Concepts**: Constraint theory, array properties, constraint satisfaction, modular arithmetic
- **Programming Skills**: Array manipulation, constraint checking, iterative programming, DP implementation
- **Related Problems**: Counting Sequences (constraint counting), Coin Combinations (DP counting), Constraint problems

## Problem Description

**Problem**: You are given an array of n integers. Your task is to find the number of ways to fill the array with integers between 1 and m so that the absolute difference between any two adjacent numbers is at most 1.

**Input**: 
- n, m: size of array and maximum value
- x1, x2, ..., xn: array contents (0 means unknown, can be filled with 1 to m)

**Output**: Number of ways to fill the array modulo 10^9+7.

**Example**:
```
Input:
3 5
2 0 2

Output:
3

Explanation: 
For the array [2, 0, 2], we need to fill the middle position (0) with a value between 1 and 5.
Valid fillings where adjacent differences ≤ 1:
- [2, 1, 2] ✓ (|2-1|≤1, |1-2|≤1)
- [2, 2, 2] ✓ (|2-2|≤1, |2-2|≤1)  
- [2, 3, 2] ✓ (|2-3|≤1, |3-2|≤1)
Total: 3 ways
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

### Step 2: Dynamic Programming Approach
**Description**: Use dynamic programming to efficiently compute the solution.

```python
def array_description_dp(n, m, arr):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to fill array from position i with previous value j
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base case: empty array
    for j in range(1, m + 1):
        dp[n][j] = 1
    
    # Fill DP table from right to left
    for i in range(n - 1, -1, -1):
        for prev_val in range(1, m + 1):
            current_val = arr[i]
            
            if current_val != 0:
                # Fixed value, check if valid
                if abs(current_val - prev_val) <= 1:
                    dp[i][prev_val] = dp[i + 1][current_val]
                else:
                    dp[i][prev_val] = 0
            else:
                # Try all possible values
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        return dp[1][arr[0]]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[1][val]) % MOD
        return result
```

**Why this improvement works**: We use a 2D DP table where dp[i][j] represents the number of ways to fill the array from position i onwards, given that the previous value was j. This avoids recalculating the same subproblems.
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

### Step 3: Complete Solution
**Putting it all together:**

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
        result = dp[0][0]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
    
    print(result)

# Main execution
if __name__ == "__main__":
    solve_array_description()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((3, 5, [2, 0, 2]), 3),
        ((2, 3, [0, 0]), 9),
        ((1, 2, [0]), 2),
        ((2, 2, [1, 0]), 2),
        ((3, 3, [1, 0, 3]), 0),
    ]
    
    for (n, m, arr), expected in test_cases:
        result = solve_test(n, m, arr)
        print(f"n={n}, m={m}, arr={arr}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}, m={m}, arr={arr}"
        print("✓ Passed")
        print()

def solve_test(n, m, arr):
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
        result = dp[0][0]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n*m²) - we fill a 2D DP table and try all possible values
- **Space**: O(n*m) - we store the entire DP table

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes valid array fillings using optimal substructure
- **State Transition**: dp[i][prev_val] = sum(dp[i+1][val]) for all valid values
- **Base Case**: dp[n][j] = 1 for all j (empty array)
- **Optimal Substructure**: Optimal solution can be built from smaller subproblems

## 🎨 Visual Example

### Input Example
```
n = 3, m = 5
Array: [2, 0, 2]
```

### All Valid Fillings
```
Array: [2, 0, 2]
Index:  0  1  2

Constraint: |arr[i] - arr[i+1]| ≤ 1

Valid fillings for position 1 (0 means unknown):
- [2, 1, 2] ✓ (|2-1|≤1, |1-2|≤1)
- [2, 2, 2] ✓ (|2-2|≤1, |2-2|≤1)
- [2, 3, 2] ✓ (|2-3|≤1, |3-2|≤1)

Invalid fillings:
- [2, 0, 2] ✗ (0 not in range [1,5])
- [2, 4, 2] ✗ (|2-4|>1)
- [2, 5, 2] ✗ (|2-5|>1)

Total valid ways: 3
```

### DP State Representation
```
dp[i][j] = number of ways to fill array from position i with previous value j

For array [2, 0, 2]:
dp[3][j] = 1 for all j (empty array, base case)

dp[2][j] = 1 for all j (only one position left, must be 2)
- dp[2][1] = 1 (can fill with 2)
- dp[2][2] = 1 (can fill with 2)
- dp[2][3] = 1 (can fill with 2)
- dp[2][4] = 1 (can fill with 2)
- dp[2][5] = 1 (can fill with 2)

dp[1][j] = sum of dp[2][k] for all k where |j-k|≤1
- dp[1][1] = dp[2][1] + dp[2][2] = 1 + 1 = 2
- dp[1][2] = dp[2][1] + dp[2][2] + dp[2][3] = 1 + 1 + 1 = 3
- dp[1][3] = dp[2][2] + dp[2][3] + dp[2][4] = 1 + 1 + 1 = 3
- dp[1][4] = dp[2][3] + dp[2][4] + dp[2][5] = 1 + 1 + 1 = 3
- dp[1][5] = dp[2][4] + dp[2][5] = 1 + 1 = 2

dp[0][j] = sum of dp[1][k] for all k where |j-k|≤1
- dp[0][1] = dp[1][1] + dp[1][2] = 2 + 3 = 5
- dp[0][2] = dp[1][1] + dp[1][2] + dp[1][3] = 2 + 3 + 3 = 8
- dp[0][3] = dp[1][2] + dp[1][3] + dp[1][4] = 3 + 3 + 3 = 9
- dp[0][4] = dp[1][3] + dp[1][4] + dp[1][5] = 3 + 3 + 2 = 8
- dp[0][5] = dp[1][4] + dp[1][5] = 3 + 2 = 5

Since position 0 is fixed to 2: dp[0][2] = 8
```

### DP Table Construction
```
Array: [2, 0, 2]
Index:  0  1  2

Step 1: Base case (empty array)
dp[3][j] = 1 for all j

Step 2: Position 2 (fixed to 2)
dp[2][j] = 1 for all j (can always fill with 2)

Step 3: Position 1 (unknown, can be 1-5)
dp[1][1] = dp[2][1] + dp[2][2] = 1 + 1 = 2
dp[1][2] = dp[2][1] + dp[2][2] + dp[2][3] = 1 + 1 + 1 = 3
dp[1][3] = dp[2][2] + dp[2][3] + dp[2][4] = 1 + 1 + 1 = 3
dp[1][4] = dp[2][3] + dp[2][4] + dp[2][5] = 1 + 1 + 1 = 3
dp[1][5] = dp[2][4] + dp[2][5] = 1 + 1 = 2

Step 4: Position 0 (fixed to 2)
dp[0][2] = dp[1][1] + dp[1][2] + dp[1][3] = 2 + 3 + 3 = 8

Final result: 8 ways
```

### Visual DP Table
```
Position: 0  1  2  3
Value 1:  5  2  1  1
Value 2:  8  3  1  1
Value 3:  9  3  1  1
Value 4:  8  3  1  1
Value 5:  5  2  1  1

Each cell shows number of ways to fill from that position with that value
```

### Constraint Propagation
```
Array: [2, 0, 2]
Index:  0  1  2

Position 0: fixed to 2
Position 1: unknown, can be 1-5
Position 2: fixed to 2

Constraint: |arr[i] - arr[i+1]| ≤ 1

From position 0 (value 2):
- Position 1 can be: 1, 2, 3 (|2-1|≤1, |2-2|≤1, |2-3|≤1)

From position 1 (value 1):
- Position 2 can be: 1, 2 (|1-1|≤1, |1-2|≤1)

From position 1 (value 2):
- Position 2 can be: 1, 2, 3 (|2-1|≤1, |2-2|≤1, |2-3|≤1)

From position 1 (value 3):
- Position 2 can be: 2, 3, 4 (|3-2|≤1, |3-3|≤1, |3-4|≤1)

But position 2 is fixed to 2, so only valid values for position 1 are: 1, 2, 3
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(m^n)       │ O(n)         │ Try all      │
│                 │              │              │ combinations │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Memoized        │ O(n*m)       │ O(n*m)       │ Cache        │
│ Recursion       │              │              │ results      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bottom-up DP    │ O(n*m)       │ O(n*m)       │ Build from   │
│                 │              │              │ base cases   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Space-optimized │ O(n*m)       │ O(m)         │ Use only     │
│ DP              │              │              │ current row  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Array Description Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: n, m,    │
              │ array           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize DP   │
              │ table           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Set base case:  │
              │ dp[n][j] = 1    │
              │ for all j       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For i = n-1     │
              │ to 0:           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ If arr[i] = 0:  │
              │ (unknown)       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For j = 1 to m: │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ dp[i][j] = sum  │
              │ of dp[i+1][k]   │
              │ where |j-k|≤1   │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return dp[0]    │
              │ [arr[0]]        │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Dynamic Programming for Constraint Satisfaction**
- Find valid configurations satisfying constraints
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **2D DP Table**
- Use 2D table for position and value combinations
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Constraint Propagation**
- Propagate constraints through the array
- Important for understanding
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Array Description with Different Constraints
**Problem**: Change the constraint to maximum difference of k.

```python
def array_description_with_k(n, m, arr, k):
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
        result = dp[0][0]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[0][val]) % MOD
    
    return result

# Example usage
result = array_description_with_k(3, 5, [2, 0, 2], 2)
print(f"Array description with k=2: {result}")
```

### Variation 2: Array Description with Range Constraints
**Problem**: Each position has a specific range of allowed values.

```python
def array_description_with_ranges(n, m, arr, ranges):
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
                if abs(current_val - prev_val) <= 1 and ranges[i][0] <= current_val <= ranges[i][1]:
                    dp[i][prev_val] = dp[i + 1][current_val]
        else:
            # Try all possible values in range
            for prev_val in range(m + 1):
                for val in range(ranges[i][0], ranges[i][1] + 1):
                    if abs(val - prev_val) <= 1:
                        dp[i][prev_val] = (dp[i][prev_val] + dp[i + 1][val]) % MOD
    
    # Handle first element
    if arr[0] != 0:
        result = dp[0][0]
    else:
        result = 0
        for val in range(ranges[0][0], ranges[0][1] + 1):
            result = (result + dp[0][val]) % MOD
    
    return result

# Example usage
ranges = [(1, 3), (2, 4), (1, 3)]  # Allowed range for each position
result = array_description_with_ranges(3, 5, [2, 0, 2], ranges)
print(f"Array description with ranges: {result}")
```

### Variation 3: Array Description with Cost Minimization
**Problem**: Find the minimum cost to fill the array.

```python
def array_description_with_costs(n, m, arr, costs):
    MOD = 10**9 + 7
    
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
                    dp[i][prev_val] = dp[i + 1][current_val]
        else:
            # Try all possible values
            for prev_val in range(m + 1):
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        cost = costs[i][val] + dp[i + 1][val]
                        dp[i][prev_val] = min(dp[i][prev_val], cost)
    
    # Handle first element
    if arr[0] != 0:
        result = dp[0][0]
    else:
        result = float('inf')
        for val in range(1, m + 1):
            result = min(result, costs[0][val] + dp[0][val])
    
    return result if result != float('inf') else -1

# Example usage
costs = [[0, 1, 2, 3, 4], [0, 2, 1, 3, 2], [0, 1, 3, 2, 1]]  # Cost for each position and value
result = array_description_with_costs(3, 5, [2, 0, 2], costs)
print(f"Array description with minimum cost: {result}")
```

### Variation 4: Array Description with Probability
**Problem**: Find the probability of valid array configurations.

```python
def array_description_probability(n, m, arr, probabilities):
    # dp[i][j] = probability of valid array from position i with previous value j
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    
    # Base case: empty array
    for j in range(1, m + 1):
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
                        dp[i][prev_val] += probabilities[i][val] * dp[i + 1][val]
    
    # Handle first element
    if arr[0] != 0:
        result = dp[0][0]
    else:
        result = 0.0
        for val in range(1, m + 1):
            result += probabilities[0][val] * dp[0][val]
    
    return result

# Example usage
probabilities = [[0.2, 0.3, 0.2, 0.2, 0.1], [0.1, 0.4, 0.3, 0.1, 0.1], [0.3, 0.2, 0.2, 0.2, 0.1]]
result = array_description_probability(3, 5, [2, 0, 2], probabilities)
print(f"Array description probability: {result:.6f}")
```

### Variation 5: Array Description with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def optimized_array_description(n, m, arr):
    MOD = 10**9 + 7
    
    # Use 1D DP array to save space
    dp = [0] * (m + 1)
    
    # Base case: empty array
    for j in range(1, m + 1):
        dp[j] = 1
    
    # Fill from right to left
    for i in range(n - 1, -1, -1):
        new_dp = [0] * (m + 1)
        current_val = arr[i]
        
        for prev_val in range(1, m + 1):
            if current_val != 0:
                # Fixed value
                if abs(current_val - prev_val) <= 1:
                    new_dp[prev_val] = dp[current_val]
                else:
                    new_dp[prev_val] = 0
            else:
                # Try all possible values
                for val in range(1, m + 1):
                    if abs(val - prev_val) <= 1:
                        new_dp[prev_val] = (new_dp[prev_val] + dp[val]) % MOD
        
        dp = new_dp
    
    # Handle first element
    if arr[0] != 0:
        result = dp[arr[0]]
    else:
        result = 0
        for val in range(1, m + 1):
            result = (result + dp[val]) % MOD
    
    return result

# Example usage
result = optimized_array_description(3, 5, [2, 0, 2])
print(f"Optimized array description: {result}")
```

## 🔗 Related Problems

- **[Dynamic Programming Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar DP problems
- **[Constraint Satisfaction Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar constraint problems
- **[Counting Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: General counting problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for constraint satisfaction problems
2. **2D DP Tables**: Important for position and value combinations
3. **Constraint Propagation**: Important for understanding valid configurations
4. **Space Optimization**: Important for performance improvement

---

**This is a great introduction to dynamic programming for constraint satisfaction problems!** 🎯
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