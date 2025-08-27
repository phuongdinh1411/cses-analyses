# CSES Counting Towers - Problem Analysis

## Problem Statement
Your task is to count the number of different towers of height n. All towers have a width of 2 and height of n. The blocks have dimensions 2×1 and 1×2.

For example, when n=3, there are 5 different towers.

### Input
The first input line contains an integer t: the number of tests.
After this, there are t lines, each containing an integer n.

### Output
For each test, print the number of towers modulo 10^9+7.

### Constraints
- 1 ≤ t ≤ 10^5
- 1 ≤ n ≤ 10^6

### Example
```
Input:
3
1
2
3

Output:
1
2
5
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(2^n)
**Description**: Try all possible ways to build towers recursively.

```python
def counting_towers_brute_force(n):
    MOD = 10**9 + 7
    
    def count_towers(height, state):
        if height == 0:
            return 1
        
        ways = 0
        
        # Try different configurations for current level
        if state == 0:  # Empty state
            # Place 2 horizontal blocks
            ways += count_towers(height - 1, 0)
            # Place 1 vertical block
            ways += count_towers(height - 1, 1)
        elif state == 1:  # One vertical block
            # Place 1 horizontal block
            ways += count_towers(height - 1, 0)
        
        return ways % MOD
    
    return count_towers(n, 0)
```

**Why this is inefficient**: We're trying all possible configurations, which leads to exponential complexity. For each level, we have multiple choices, leading to O(2^n) complexity.

### Improvement 1: Recursive with Memoization - O(n)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def counting_towers_memoization(n):
    MOD = 10**9 + 7
    memo = {}
    
    def count_towers(height, state):
        if (height, state) in memo:
            return memo[(height, state)]
        
        if height == 0:
            return 1
        
        ways = 0
        
        if state == 0:  # Empty state
            ways += count_towers(height - 1, 0)  # 2 horizontal
            ways += count_towers(height - 1, 1)  # 1 vertical
        elif state == 1:  # One vertical block
            ways += count_towers(height - 1, 0)  # 1 horizontal
        
        memo[(height, state)] = ways % MOD
        return memo[(height, state)]
    
    return count_towers(n, 0)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def counting_towers_dp(n):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to build tower of height i with state j
    # j = 0: empty state, j = 1: one vertical block
    dp = [[0] * 2 for _ in range(n + 1)]
    
    # Base case: height 0
    dp[0][0] = 1
    dp[0][1] = 0
    
    for i in range(1, n + 1):
        # From empty state
        dp[i][0] = (dp[i-1][0] + dp[i-1][1]) % MOD  # 2 horizontal or 1 vertical
        # From one vertical state
        dp[i][1] = dp[i-1][0] % MOD  # 1 horizontal
    
    return dp[n][0]
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each height, we consider the possible states and transitions.

### Alternative: Optimized DP with State Compression - O(n)
**Description**: Use state compression to optimize the DP solution.

```python
def counting_towers_optimized(n):
    MOD = 10**9 + 7
    
    # Use only 2 variables for current and previous states
    prev_empty = 1
    prev_vertical = 0
    
    for i in range(1, n + 1):
        curr_empty = (prev_empty + prev_vertical) % MOD
        curr_vertical = prev_empty % MOD
        
        prev_empty = curr_empty
        prev_vertical = curr_vertical
    
    return prev_empty
```

**Why this works**: We can optimize space by using only 2 variables instead of a 2D array, since we only need the previous state to calculate the current state.

## Final Optimal Solution

```python
t = int(input())
MOD = 10**9 + 7

for _ in range(t):
    n = int(input())
    
    # Use only 2 variables for current and previous states
    prev_empty = 1
    prev_vertical = 0
    
    for i in range(1, n + 1):
        curr_empty = (prev_empty + prev_vertical) % MOD
        curr_vertical = prev_empty % MOD
        
        prev_empty = curr_empty
        prev_vertical = curr_vertical
    
    print(prev_empty)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n) | O(n) | Try all configurations |
| Memoization | O(n) | O(n) | Store subproblem results |
| Bottom-Up DP | O(n) | O(n) | Build solution iteratively |
| Optimized DP | O(n) | O(1) | Use state compression |

## Key Insights for Other Problems

### 1. **Dynamic Programming for Construction Problems**
**Principle**: Use DP to count the number of ways to construct objects with given constraints.
**Applicable to**:
- Construction problems
- Counting problems
- State machine problems
- Algorithm design

**Example Problems**:
- Counting towers
- Construction problems
- Counting problems
- State machine problems

### 2. **State Machine DP**
**Principle**: Use state machines to model complex transitions in DP problems.
**Applicable to**:
- State machine problems
- Dynamic programming
- Transition problems
- Algorithm design

**Example Problems**:
- State machine problems
- Dynamic programming
- Transition problems
- Algorithm design

### 3. **State Compression in DP**
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

### 4. **Modular Arithmetic in Counting**
**Principle**: Use modular arithmetic to handle large numbers in counting problems.
**Applicable to**:
- Large number problems
- Counting problems
- Modular arithmetic
- Algorithm optimization

**Example Problems**:
- Large number calculations
- Counting problems
- Modular arithmetic
- Algorithm optimization

## Notable Techniques

### 1. **State Machine DP Pattern**
```python
# Define states and transitions
dp = [[0] * num_states for _ in range(n + 1)]
for i in range(1, n + 1):
    for state in range(num_states):
        for next_state in possible_transitions(state):
            dp[i][next_state] += dp[i-1][state]
```

### 2. **State Compression Pattern**
```python
# Use variables instead of arrays for space optimization
prev_state1 = 1
prev_state2 = 0
for i in range(1, n + 1):
    curr_state1 = prev_state1 + prev_state2
    curr_state2 = prev_state1
    prev_state1 = curr_state1
    prev_state2 = curr_state2
```

### 3. **Modular Arithmetic Pattern**
```python
# Use modular arithmetic for large numbers
MOD = 10**9 + 7
result = (result + value) % MOD
```

## Edge Cases to Remember

1. **n = 1**: Return 1 (only one way)
2. **n = 2**: Return 2 (two ways)
3. **Large n**: Use efficient DP approach
4. **Multiple test cases**: Process each case independently
5. **Modular arithmetic**: Take modulo at each step

## Problem-Solving Framework

1. **Identify construction nature**: This is a construction counting problem
2. **Define states**: Empty state and vertical block state
3. **Define transitions**: How states change between levels
4. **Handle base case**: Height 0 has one way
5. **Use state compression**: Optimize space usage

---

*This analysis shows how to efficiently solve construction counting problems using dynamic programming.* 