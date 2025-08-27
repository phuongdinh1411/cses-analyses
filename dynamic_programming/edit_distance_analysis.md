# CSES Edit Distance - Problem Analysis

## Problem Statement
The edit distance between two strings is the minimum number of operations required to transform one string into the other.

The allowed operations are:
- Insert a character
- Delete a character
- Replace a character

For example, the edit distance between "LOVE" and "MOVIE" is 2.

### Input
The first input line contains a string a, and the second line contains a string b.

### Output
Print one integer: the edit distance.

### Constraints
- 1 ≤ |a|,|b| ≤ 5000

### Example
```
Input:
LOVE
MOVIE

Output:
2
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(3^(n+m))
**Description**: Try all possible operations recursively.

```python
def edit_distance_brute_force(a, b):
    def min_operations(i, j):
        if i == len(a) and j == len(b):
            return 0
        if i == len(a):
            return len(b) - j  # Insert remaining characters
        if j == len(b):
            return len(a) - i  # Delete remaining characters
        
        if a[i] == b[j]:
            return min_operations(i + 1, j + 1)  # No operation needed
        
        # Try all three operations
        insert = 1 + min_operations(i, j + 1)      # Insert character
        delete = 1 + min_operations(i + 1, j)      # Delete character
        replace = 1 + min_operations(i + 1, j + 1) # Replace character
        
        return min(insert, delete, replace)
    
    return min_operations(0, 0)
```

**Why this is inefficient**: We're trying all possible operations, which leads to exponential complexity. For each position, we have 3 choices (insert, delete, replace), leading to O(3^(n+m)) complexity.

### Improvement 1: Recursive with Memoization - O(n*m)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def edit_distance_memoization(a, b):
    memo = {}
    
    def min_operations(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        
        if i == len(a) and j == len(b):
            return 0
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        
        if a[i] == b[j]:
            result = min_operations(i + 1, j + 1)
        else:
            insert = 1 + min_operations(i, j + 1)
            delete = 1 + min_operations(i + 1, j)
            replace = 1 + min_operations(i + 1, j + 1)
            result = min(insert, delete, replace)
        
        memo[(i, j)] = result
        return result
    
    return min_operations(0, 0)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n*m) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n*m)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def edit_distance_dp(a, b):
    n, m = len(a), len(b)
    
    # dp[i][j] = edit distance between a[:i] and b[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][0] = i  # Delete all characters from a
    for j in range(m + 1):
        dp[0][j] = j  # Insert all characters from b
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation needed
            else:
                insert = dp[i][j-1] + 1      # Insert character
                delete = dp[i-1][j] + 1      # Delete character
                replace = dp[i-1][j-1] + 1   # Replace character
                dp[i][j] = min(insert, delete, replace)
    
    return dp[n][m]
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each position, we consider all three operations and choose the minimum.

### Alternative: Space-Optimized DP - O(n*m)
**Description**: Use a space-optimized DP approach with only two rows.

```python
def edit_distance_optimized(a, b):
    n, m = len(a), len(b)
    
    # Use only 2 rows for space optimization
    dp = [[0] * (m + 1) for _ in range(2)]
    
    # Initialize first row
    for j in range(m + 1):
        dp[0][j] = j
    
    for i in range(1, n + 1):
        curr_row = i % 2
        prev_row = (i - 1) % 2
        
        dp[curr_row][0] = i  # Base case for current row
        
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[curr_row][j] = dp[prev_row][j-1]
            else:
                insert = dp[curr_row][j-1] + 1
                delete = dp[prev_row][j] + 1
                replace = dp[prev_row][j-1] + 1
                dp[curr_row][j] = min(insert, delete, replace)
    
    return dp[n % 2][m]
```

**Why this works**: We can optimize space by using only 2 rows instead of n+1 rows, since we only need the previous row to calculate the current row.

## Final Optimal Solution

```python
a = input().strip()
b = input().strip()

n, m = len(a), len(b)

# dp[i][j] = edit distance between a[:i] and b[:j]
dp = [[0] * (m + 1) for _ in range(n + 1)]

# Base cases
for i in range(n + 1):
    dp[i][0] = i
for j in range(m + 1):
    dp[0][j] = j

# Fill the DP table
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if a[i-1] == b[j-1]:
            dp[i][j] = dp[i-1][j-1]
        else:
            insert = dp[i][j-1] + 1
            delete = dp[i-1][j] + 1
            replace = dp[i-1][j-1] + 1
            dp[i][j] = min(insert, delete, replace)

print(dp[n][m])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(3^(n+m)) | O(n+m) | Try all operations |
| Memoization | O(n*m) | O(n*m) | Store subproblem results |
| Bottom-Up DP | O(n*m) | O(n*m) | Build solution iteratively |
| Space-Optimized DP | O(n*m) | O(m) | Use two rows optimization |

## Key Insights for Other Problems

### 1. **Dynamic Programming for String Problems**
**Principle**: Use DP to solve string manipulation and comparison problems.
**Applicable to**:
- String problems
- Edit distance
- Longest common subsequence
- String matching

**Example Problems**:
- Edit distance
- Longest common subsequence
- String matching
- String problems

### 2. **State Definition for String DP**
**Principle**: Define states that capture the essential information for string-based problems.
**Applicable to**:
- Dynamic programming
- String problems
- State machine problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- String problems
- State machine problems
- Algorithm design

### 3. **Space Optimization in String DP**
**Principle**: Use space optimization techniques to reduce memory usage in string DP problems.
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

### 4. **Base Case Handling in DP**
**Principle**: Handle base cases carefully in DP problems, especially for string problems.
**Applicable to**:
- Dynamic programming
- Base case handling
- Algorithm design
- Problem solving

**Example Problems**:
- Dynamic programming
- Base case handling
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **String DP Pattern**
```python
# Define DP state for string problems
dp = [[0] * (m + 1) for _ in range(n + 1)]
# Handle base cases
for i in range(n + 1):
    dp[i][0] = i
for j in range(m + 1):
    dp[0][j] = j
```

### 2. **State Transition Pattern**
```python
# Define state transitions for string problems
if a[i-1] == b[j-1]:
    dp[i][j] = dp[i-1][j-1]
else:
    dp[i][j] = min(dp[i][j-1] + 1, dp[i-1][j] + 1, dp[i-1][j-1] + 1)
```

### 3. **Space Optimization Pattern**
```python
# Use two rows for space optimization
dp = [[0] * (m + 1) for _ in range(2)]
curr_row = i % 2
prev_row = (i - 1) % 2
```

## Edge Cases to Remember

1. **Empty strings**: Handle base cases properly
2. **Identical strings**: Return 0
3. **One empty string**: Return length of other string
4. **Large strings**: Use efficient DP approach
5. **Base cases**: Initialize first row and column correctly

## Problem-Solving Framework

1. **Identify string nature**: This is a string comparison problem
2. **Define state**: dp[i][j] = edit distance between a[:i] and b[:j]
3. **Define transitions**: Consider insert, delete, and replace operations
4. **Handle base cases**: Initialize first row and column
5. **Use space optimization**: Consider two-row approach

---

*This analysis shows how to efficiently solve string comparison problems using dynamic programming.* 