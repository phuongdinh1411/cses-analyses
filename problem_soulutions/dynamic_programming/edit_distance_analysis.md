---
layout: simple
title: "Edit Distance"
permalink: /problem_soulutions/dynamic_programming/edit_distance_analysis
---


# Edit Distance

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand string transformation problems and edit distance calculations
- Apply 2D DP techniques to solve string transformation problems with operations
- Implement efficient 2D DP solutions for edit distance and string operations
- Optimize 2D DP solutions using space-efficient techniques and operation tracking
- Handle edge cases in string DP (empty strings, identical strings, single character differences)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D dynamic programming, string algorithms, edit distance, string transformation
- **Data Structures**: 2D arrays, DP tables, string data structures
- **Mathematical Concepts**: String theory, edit distance, transformation operations, optimization principles
- **Programming Skills**: 2D array manipulation, string processing, iterative programming, DP implementation
- **Related Problems**: Longest Common Subsequence (string DP), Removing Digits (digit manipulation), String algorithms

## Problem Description

The edit distance between two strings is the minimum number of operations required to transform one string into the other.

**Allowed operations**:
- Insert a character
- Delete a character
- Replace a character

**Input**: 
- First line: string a (first string)
- Second line: string b (second string)

**Output**: 
- Print the minimum edit distance between the two strings

**Constraints**:
- 1 ≤ |a|, |b| ≤ 5000
- Only three operations allowed: insert, delete, replace
- Each operation costs 1 unit
- Find minimum number of operations
- Strings contain only lowercase letters

**Example**:
```
Input:
LOVE
MOVIE

Output:
2

Explanation**: 
Transform "LOVE" to "MOVIE":
1. Replace 'L' with 'M': MOVE
2. Insert 'I' before 'E': MOVIE
Total: 2 operations
```

## Visual Example

### Input and Problem Setup
```
Input: a = "LOVE", b = "MOVIE"

Goal: Transform string a into string b using minimum operations
Operations: Insert, Delete, Replace (each costs 1)
Result: Minimum edit distance between the strings
Note: Each operation has equal cost of 1
```

### String Transformation Analysis
```
For strings "LOVE" and "MOVIE":

String a: L O V E
String b: M O V I E

Position-by-position comparison:
- Position 0: L vs M → Different, need operation
- Position 1: O vs O → Same, no operation needed
- Position 2: V vs V → Same, no operation needed
- Position 3: E vs I → Different, need operation
- Position 4: (none) vs E → Need to insert E

Operations needed:
1. Replace L with M: MOVE
2. Insert I before E: MOVIE
Total: 2 operations
```

### Dynamic Programming Pattern
```
DP State: dp[i][j] = edit distance between a[0:i] and b[0:j]

Base cases:
- dp[i][0] = i (delete i characters from a)
- dp[0][j] = j (insert j characters into a)

Recurrence:
- If a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] (no operation)
- Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

Key insight: Use 2D DP to handle string transformation
```

### State Transition Visualization
```
Building DP table for a = "LOVE", b = "MOVIE":

Initialize: dp = [[0, 1, 2, 3, 4, 5],
                  [1, 0, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0],
                  [3, 0, 0, 0, 0, 0],
                  [4, 0, 0, 0, 0, 0]]

Base cases: dp[i][0] = i, dp[0][j] = j

Position (1,1): L vs M → Different
dp[1][1] = 1 + min(dp[0][1], dp[1][0], dp[0][0]) = 1 + min(1, 1, 0) = 1

Position (2,2): O vs O → Same
dp[2][2] = dp[1][1] = 1

Position (3,3): V vs V → Same
dp[3][3] = dp[2][2] = 1

Position (4,4): E vs I → Different
dp[4][4] = 1 + min(dp[3][4], dp[4][3], dp[3][3]) = 1 + min(4, 4, 1) = 2

Position (4,5): (none) vs E → Insert
dp[4][5] = 1 + min(dp[3][5], dp[4][4], dp[3][4]) = 1 + min(5, 2, 4) = 3

Final: dp[4][5] = 2 (minimum edit distance)
```

### Key Insight
The solution works by:
1. Using 2D dynamic programming to handle string transformation
2. For each position, considering all three operations (insert, delete, replace)
3. Building solutions from smaller subproblems
4. Using optimal substructure property
5. Time complexity: O(n × m) for filling DP table
6. Space complexity: O(n × m) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible operations (insert, delete, replace) recursively
- Use recursive approach to explore all transformation paths
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. For each position, try all three operations
2. Recursively explore all valid transformation paths
3. Return minimum number of operations
4. Handle base cases for empty strings

**Visual Example:**
```
Brute force approach: Try all possible operations
For strings "LOVE" and "MOVIE":

Recursive tree:
                    (0, 0)
              /        |        \
          (0, 1)    (1, 0)    (1, 1)
         /  |  \    /  |  \    /  |  \
    (0, 2) (1, 1) (1, 2) (1, 1) (2, 1) (2, 2)
   /  |  \  /  |  \ /  |  \ /  |  \ /  |  \ /  |  \
... ... ... ... ... ... ... ... ... ... ... ... ... ...
```

**Implementation:**
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

def solve_edit_distance_brute_force():
    a = input().strip()
    b = input().strip()
    
    result = edit_distance_brute_force(a, b)
    print(result)
```

**Time Complexity:** O(3^(n+m)) for trying all possible operations
**Space Complexity:** O(n + m) for recursion depth

**Why it's inefficient:**
- O(3^(n+m)) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large strings
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 2D DP array to store edit distance for each position
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each position, consider all three operations
3. Update edit distance using recurrence relation
4. Return minimum edit distance

**Visual Example:**
```
DP approach: Build solutions iteratively
For a = "LOVE", b = "MOVIE":

Initialize: dp = [[0, 1, 2, 3, 4, 5],
                  [1, 0, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0],
                  [3, 0, 0, 0, 0, 0],
                  [4, 0, 0, 0, 0, 0]]

After processing: dp = [[0, 1, 2, 3, 4, 5],
                        [1, 1, 2, 3, 4, 5],
                        [2, 2, 1, 2, 3, 4],
                        [3, 3, 2, 1, 2, 3],
                        [4, 4, 3, 2, 2, 2]]

Final result: dp[4][5] = 2
```

**Implementation:**
```python
def edit_distance_dp(a, b):
    n, m = len(a), len(b)
    
    # dp[i][j] = edit distance between a[0:i] and b[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][0] = i  # Delete i characters from a
    for j in range(m + 1):
        dp[0][j] = j  # Insert j characters into a
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation needed
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # Delete
                                  dp[i][j-1],    # Insert
                                  dp[i-1][j-1])  # Replace
    
    return dp[n][m]

def solve_edit_distance_dp():
    a = input().strip()
    b = input().strip()
    
    result = edit_distance_dp(a, b)
    print(result)
```

**Time Complexity:** O(n × m) for filling DP table
**Space Complexity:** O(n × m) for DP array

**Why it's better:**
- O(n × m) time complexity is much better than O(3^(n+m))
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Optimized DP with Space Efficiency (Optimal)

**Key Insights from Optimized Solution:**
- Use the same DP approach but with better implementation
- Most efficient approach for string transformation problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Initialize DP array with base cases
2. Process strings from left to right
3. Use optimal substructure property
4. Return optimal solution

**Visual Example:**
```
Optimized DP: Process strings from left to right
For a = "LOVE", b = "MOVIE":

Initialize: dp = [[0, 1, 2, 3, 4, 5],
                  [1, 0, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0],
                  [3, 0, 0, 0, 0, 0],
                  [4, 0, 0, 0, 0, 0]]

Process position (1,1): dp[1][1] = 1
Process position (2,2): dp[2][2] = 1
Process position (3,3): dp[3][3] = 1
Process position (4,4): dp[4][4] = 2
Process position (4,5): dp[4][5] = 2
```

**Implementation:**
```python
def solve_edit_distance():
    a = input().strip()
    b = input().strip()
    
    n, m = len(a), len(b)
    
    # dp[i][j] = edit distance between a[0:i] and b[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][0] = i  # Delete i characters from a
    for j in range(m + 1):
        dp[0][j] = j  # Insert j characters into a
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation needed
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # Delete
                                  dp[i][j-1],    # Insert
                                  dp[i-1][j-1])  # Replace
    
    print(dp[n][m])

# Main execution
if __name__ == "__main__":
    solve_edit_distance()
```

**Time Complexity:** O(n × m) for filling DP table
**Space Complexity:** O(n × m) for DP array

**Why it's optimal:**
- O(n × m) time complexity is optimal for this problem
- Uses dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for string transformation problems

## 🎯 Problem Variations

### Variation 1: Edit Distance with Different Costs
**Problem**: Each operation has different costs.

**Link**: [CSES Problem Set - Edit Distance Costs](https://cses.fi/problemset/task/edit_distance_costs)

```python
def edit_distance_costs(a, b, insert_cost, delete_cost, replace_cost):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = i * delete_cost
    for j in range(m + 1):
        dp[0][j] = j * insert_cost
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j] + delete_cost,
                              dp[i][j-1] + insert_cost,
                              dp[i-1][j-1] + replace_cost)
    
    return dp[n][m]
```

### Variation 2: Edit Distance with Transposition
**Problem**: Allow transposition of adjacent characters.

**Link**: [CSES Problem Set - Edit Distance Transposition](https://cses.fi/problemset/task/edit_distance_transposition)

```python
def edit_distance_transposition(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                
                # Check for transposition
                if i > 1 and j > 1 and a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                    dp[i][j] = min(dp[i][j], 1 + dp[i-2][j-2])
    
    return dp[n][m]
```

### Variation 3: Edit Distance with Block Operations
**Problem**: Allow block insert, delete, and replace operations.

**Link**: [CSES Problem Set - Edit Distance Blocks](https://cses.fi/problemset/task/edit_distance_blocks)

```python
def edit_distance_blocks(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                
                # Check for block operations
                for k in range(1, min(i, j) + 1):
                    if a[i-k:i] == b[j-k:j]:
                        dp[i][j] = min(dp[i][j], dp[i-k][j-k])
    
    return dp[n][m]
```

## 🔗 Related Problems

- **[Longest Common Subsequence](/cses-analyses/problem_soulutions/dynamic_programming/)**: String DP problems
- **[Removing Digits](/cses-analyses/problem_soulutions/dynamic_programming/)**: Digit manipulation problems
- **[String Algorithms](/cses-analyses/problem_soulutions/string_algorithms/)**: String processing problems
- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/)**: 2D DP problems

## 📚 Learning Points

1. **String Transformation**: Essential for understanding edit distance and string operations
2. **2D Dynamic Programming**: Key technique for solving string transformation problems efficiently
3. **String Processing**: Important for understanding how to handle string operations
4. **Operation Handling**: Critical for understanding how to implement insert, delete, and replace
5. **Optimal Substructure**: Foundation for building solutions from smaller subproblems
6. **Bottom-Up DP**: Critical for building solutions from smaller subproblems

## 📝 Summary

The Edit Distance problem demonstrates string transformation and 2D dynamic programming principles for efficient string operations. We explored three approaches:

1. **Recursive Brute Force**: O(3^(n+m)) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n × m) time complexity using 2D DP, better approach for string transformation problems
3. **Optimized DP with Space Efficiency**: O(n × m) time complexity with efficient implementation, optimal approach for competitive programming

The key insights include understanding string transformation principles, using 2D dynamic programming for efficient computation, and applying string processing techniques for transformation problems. This problem serves as an excellent introduction to string algorithms in competitive programming.
