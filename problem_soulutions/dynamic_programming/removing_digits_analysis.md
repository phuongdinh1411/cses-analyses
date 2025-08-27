# CSES Removing Digits - Problem Analysis

## Problem Statement
You are given an integer n. On each step, you may subtract one of the digits from the number. How many steps are required to make the number equal to 0?

For example, if n=27, you can subtract 2 or 7. If you subtract 2, you get 25, and if you subtract 7, you get 20. The minimum number of steps is 5.

### Input
The only input line contains an integer n.

### Output
Print one integer: the minimum number of steps.

### Constraints
- 1 ≤ n ≤ 10^6

### Example
```
Input:
27

Output:
5
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(d^n)
**Description**: Try all possible digit removals recursively.

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
        for digit in digits:
            if digit > 0 and i >= digit:
                dp[i] = min(dp[i], 1 + dp[i - digit])
    
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
for digit in digits:
    if digit > 0 and i >= digit:
        dp[i] = min(dp[i], 1 + dp[i - digit])
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