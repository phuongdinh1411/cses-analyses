---
layout: simple
title: "Counting Towers
permalink: /problem_soulutions/dynamic_programming/counting_towers_analysis/
---

# Counting Towers

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
```"
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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Counting Towers with Different Block Sizes**
**Problem**: Allow blocks of size 1×1, 1×2, 2×1, and 2×2.
```python
def counting_towers_extended_blocks(n):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to build tower of height i with state j
    # States: 0=empty, 1=left filled, 2=right filled, 3=both filled
    dp = [[0] * 4 for _ in range(n + 1)]
    
    # Base case
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        # From empty state
        dp[i][0] = (dp[i-1][0] + dp[i-1][1] + dp[i-1][2] + dp[i-1][3]) % MOD
        # From left filled
        dp[i][1] = (dp[i-1][0] + dp[i-1][2]) % MOD
        # From right filled
        dp[i][2] = (dp[i-1][0] + dp[i-1][1]) % MOD
        # From both filled
        dp[i][3] = dp[i-1][0] % MOD
    
    return dp[n][0]
```

#### **Variation 2: Counting Towers with Width Constraints**
**Problem**: Towers have width w instead of 2.
```python
def counting_towers_variable_width(n, w):
    MOD = 10**9 + 7
    
    # dp[i][mask] = number of ways to build tower of height i with state mask
    # mask represents which positions are filled (0 to 2^w - 1)
    dp = [[0] * (1 << w) for _ in range(n + 1)]
    
    # Base case
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for prev_mask in range(1 << w):
            # Try all possible configurations for current level
            for curr_mask in range(1 << w):
                if is_valid_configuration(prev_mask, curr_mask, w):
                    dp[i][curr_mask] = (dp[i][curr_mask] + dp[i-1][prev_mask]) % MOD
    
    return dp[n][0]

def is_valid_configuration(prev_mask, curr_mask, w):
    # Check if configuration is valid (no gaps, proper connections)
    # Implementation depends on specific rules
    return True  # Placeholder
```

#### **Variation 3: Counting Towers with Color Constraints**
**Problem**: Each block has a color, and adjacent blocks must have different colors.
```python
def counting_towers_with_colors(n, colors):
    MOD = 10**9 + 7
    
    # dp[i][state][color] = number of ways with height i, state, and last color
    dp = [[[0] * colors for _ in range(2)] for _ in range(n + 1)]
    
    # Base case
    for c in range(colors):
        dp[0][0][c] = 1
    
    for i in range(1, n + 1):
        for state in range(2):
            for prev_color in range(colors):
                for curr_color in range(colors):
                    if curr_color != prev_color:  # Different colors
                        if state == 0:  # Empty state
                            dp[i][0][curr_color] = (dp[i][0][curr_color] + dp[i-1][0][prev_color]) % MOD
                            dp[i][1][curr_color] = (dp[i][1][curr_color] + dp[i-1][0][prev_color]) % MOD
                        elif state == 1:  # One vertical
                            dp[i][0][curr_color] = (dp[i][0][curr_color] + dp[i-1][1][prev_color]) % MOD
    
    return sum(dp[n][0][c] for c in range(colors)) % MOD
```

#### **Variation 4: Counting Towers with Height Constraints**
**Problem**: Each block has a maximum height, and towers must be stable.
```python
def counting_towers_with_height_constraints(n, max_block_height):
    MOD = 10**9 + 7
    
    # dp[i][j][k] = number of ways with height i, state j, and current block height k
    dp = [[[0] * (max_block_height + 1) for _ in range(2)] for _ in range(n + 1)]
    
    # Base case
    dp[0][0][0] = 1
    
    for i in range(1, n + 1):
        for state in range(2):
            for block_height in range(max_block_height + 1):
                if state == 0:  # Empty state
                    # Place horizontal blocks
                    dp[i][0][0] = (dp[i][0][0] + dp[i-1][0][block_height]) % MOD
                    # Place vertical block
                    if block_height < max_block_height:
                        dp[i][1][block_height + 1] = (dp[i][1][block_height + 1] + dp[i-1][0][block_height]) % MOD
                elif state == 1:  # One vertical
                    # Complete the vertical block
                    dp[i][0][0] = (dp[i][0][0] + dp[i-1][1][block_height]) % MOD
    
    return dp[n][0][0]
```

#### **Variation 5: Counting Towers with Symmetry Constraints**
**Problem**: Count only towers that are symmetric (left-right mirror images).
```python
def counting_symmetric_towers(n):
    MOD = 10**9 + 7
    
    # For symmetric towers, we only need to consider half the width
    # dp[i][j] = number of ways to build symmetric tower of height i with state j
    dp = [[0] * 2 for _ in range(n + 1)]
    
    # Base case
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        # From empty state
        dp[i][0] = (dp[i-1][0] + dp[i-1][1]) % MOD  # Horizontal or vertical
        # From one vertical state (must be symmetric)
        dp[i][1] = dp[i-1][0] % MOD  # Only horizontal to maintain symmetry
    
    return dp[n][0]
```

### 🔗 **Related Problems & Concepts**

#### **1. Construction Problems**
- **Tiling Problems**: Cover area with tiles
- **Domino Tilings**: Count domino arrangements
- **Polyomino Problems**: Count polyomino arrangements
- **Building Problems**: Count building configurations

#### **2. Dynamic Programming Patterns**
- **State Machine DP**: Model complex transitions
- **2D DP**: Two state variables (height, state)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Counting Problems**
- **Combinatorial Counting**: Count valid configurations
- **Inclusion-Exclusion**: Count with constraints
- **Generating Functions**: Algebraic approach to counting
- **Burnside's Lemma**: Count orbits under group actions

#### **4. Algorithmic Techniques**
- **Recursive Backtracking**: Try all valid configurations
- **Memoization**: Cache computed results
- **Bottom-Up DP**: Build solution iteratively
- **State Space Search**: Explore all possible states

#### **5. Mathematical Concepts**
- **Combinatorics**: Count valid arrangements
- **Symmetry**: Exploit symmetric properties
- **Modular Arithmetic**: Handle large numbers
- **Recurrence Relations**: Find closed-form solutions

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    result = counting_towers_optimized(n)
    print(result)
```

#### **2. Range Queries on Tower Counts**
```python
def range_tower_queries(max_n, queries):
    # Precompute for all heights up to max_n
    dp = [0] * (max_n + 1)
    
    # Fill DP table
    dp[0] = 1
    prev_empty = 1
    prev_vertical = 0
    
    for i in range(1, max_n + 1):
        curr_empty = (prev_empty + prev_vertical) % MOD
        curr_vertical = prev_empty % MOD
        dp[i] = curr_empty
        prev_empty = curr_empty
        prev_vertical = curr_vertical
    
    # Answer queries
    for l, r in queries:
        total = sum(dp[i] for i in range(l, r + 1)) % MOD
        print(total)
```

#### **3. Interactive Tower Problems**
```python
def interactive_tower_game():
    n = int(input("Enter tower height: "))
    
    print(f"Find number of different towers of height {n}")
    
    player_guess = int(input("Enter number of towers: "))
    actual_count = counting_towers_optimized(n)
    
    if player_guess == actual_count:
        print("Correct!")
    else:
        print(f"Wrong! Number of towers is {actual_count}")
```

### 🧮 **Mathematical Extensions**

#### **1. Recurrence Relations**
- **Linear Recurrences**: Find closed-form solutions
- **Fibonacci-like Sequences**: Analyze growth patterns
- **Generating Functions**: Represent sequences algebraically
- **Asymptotic Analysis**: Behavior for large heights

#### **2. Advanced DP Techniques**
- **Digit DP**: Count towers with specific properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split problems into subproblems
- **Persistent Data Structures**: Maintain tower history

#### **3. Symmetry Analysis**
- **Group Theory**: Analyze symmetric properties
- **Burnside's Lemma**: Count orbits under symmetries
- **Polya Enumeration**: Count objects up to symmetry
- **Automorphism Groups**: Study symmetry groups

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Tiling Algorithms**: Cover area with tiles
- **Construction Algorithms**: Build objects systematically
- **Counting Algorithms**: Count valid configurations
- **Symmetry Algorithms**: Exploit symmetric properties

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting principles and techniques
- **Group Theory**: Study of symmetries
- **Recurrence Relations**: Mathematical sequences
- **Modular Arithmetic**: Handle large numbers

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **State Machines**: Model complex transitions
- **Algorithm Design**: Creating efficient solutions

---

*This analysis demonstrates the power of dynamic programming for construction counting problems and shows various extensions and applications.* 