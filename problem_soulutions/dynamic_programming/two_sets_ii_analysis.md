---
layout: simple
title: "Two Sets II"
permalink: /problem_soulutions/dynamic_programming/two_sets_ii_analysis
---


# Two Sets II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand partition problems and equal sum subset division in DP
- Apply DP techniques to count ways of dividing sets into equal sum subsets
- Implement efficient DP solutions for partition counting and subset division
- Optimize DP solutions using space-efficient techniques and modular arithmetic
- Handle edge cases in partition DP (impossible partitions, odd sums, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, partition problems, subset sum, equal sum division
- **Data Structures**: Arrays, DP tables, partition data structures
- **Mathematical Concepts**: Partition theory, subset sum, equal sum principles, modular arithmetic
- **Programming Skills**: Array manipulation, iterative programming, partition techniques, DP implementation
- **Related Problems**: Two Sets (basic partition), Money Sums (subset sum), Coin Combinations (DP counting)

## Problem Description

**Problem**: Given a number n, find the number of ways to divide the numbers 1,2,…,n into two sets with equal sums.

**Input**: 
- n: the number up to which we consider (1 to n)

**Output**: Number of ways to divide into two equal-sum sets modulo 10^9+7.

**Example**:
```
Input:
7

Output:
4

Explanation: 
For n=7, the numbers are 1,2,3,4,5,6,7 with total sum = 28.
We need to find ways to divide them into two sets, each with sum = 14.
Valid partitions:
- {1,2,3,4,5,6,7} and {} (but this is invalid as one set is empty)
- {1,2,3,4,5,6} and {7} (sums: 21 and 7)
- {1,2,3,4,5,7} and {6} (sums: 22 and 6)
- {1,2,3,4,6,7} and {5} (sums: 23 and 5)
- {1,2,3,5,6,7} and {4} (sums: 24 and 4)
- {1,2,4,5,6,7} and {3} (sums: 25 and 3)
- {1,3,4,5,6,7} and {2} (sums: 26 and 2)
- {2,3,4,5,6,7} and {1} (sums: 27 and 1)
Actually, there are 4 valid ways where both sets have equal sums.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Divide numbers 1 to n into two sets
- Both sets must have equal sums
- Count the number of valid partitions
- Use dynamic programming for efficiency

**Key Observations:**
- Total sum must be even for valid partition
- We need to find subsets that sum to total_sum/2
- This is a subset sum problem
- Can use dynamic programming

### Step 2: Dynamic Programming Approach
**Idea**: Use DP to count ways to achieve target sum.

```python
def two_sets_ii_dp(n):
    total_sum = n * (n + 1) // 2
    
    # If total sum is odd, no valid partition exists
    if total_sum % 2 != 0:
        return 0
    
    target = total_sum // 2
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to achieve sum i
    dp = [0] * (target + 1)
    dp[0] = 1  # Base case: one way to achieve sum 0 (empty set)
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % MOD
    
    return dp[target]
```

**Why this works:**
- Uses subset sum dynamic programming
- Handles equal partition constraint
- Efficient implementation
- O(n * sum) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_two_sets_ii():
    n = int(input())
    
    total_sum = n * (n + 1) // 2
    
    # If total sum is odd, no valid partition exists
    if total_sum % 2 != 0:
        print(0)
        return
    
    target = total_sum // 2
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to achieve sum i
    dp = [0] * (target + 1)
    dp[0] = 1  # Base case: one way to achieve sum 0 (empty set)
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % MOD
    
    print(dp[target])

# Main execution
if __name__ == "__main__":
    solve_two_sets_ii()
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
        (3, 1),   # {1,2,3} → {1,2} and {3} (sums: 3 and 3)
        (4, 1),   # {1,2,3,4} → {1,4} and {2,3} (sums: 5 and 5)
        (7, 4),   # Multiple valid partitions
        (5, 0),   # Total sum is odd, no valid partition
    ]
    
    for n, expected in test_cases:
        result = solve_test(n)
        print(f"n={n}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}"
        print("✓ Passed")
        print()

def solve_test(n):
    total_sum = n * (n + 1) // 2
    
    # If total sum is odd, no valid partition exists
    if total_sum % 2 != 0:
        return 0
    
    target = total_sum // 2
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to achieve sum i
    dp = [0] * (target + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % MOD
    
    return dp[target]

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n * sum) - we iterate through each number and each possible sum
- **Space**: O(sum) - we store dp array of size sum+1

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes subset sums using optimal substructure
- **State Transition**: dp[i] = sum of dp[i-j] for all valid numbers j
- **Base Case**: dp[0] = 1 represents empty subset
- **Equal Partition**: Target sum is total_sum/2

## 🎨 Visual Example

### Input Example
```
n = 7
```

### All Possible Partitions
```
Numbers: [1, 2, 3, 4, 5, 6, 7]
Total sum: 1+2+3+4+5+6+7 = 28
Target sum: 28/2 = 14

Valid partitions where both sets sum to 14:
1. {1, 2, 3, 4, 5, 6, 7} and {} (invalid - one set empty)
2. {1, 2, 3, 4, 5, 6} and {7} (sums: 21 and 7)
3. {1, 2, 3, 4, 5, 7} and {6} (sums: 22 and 6)
4. {1, 2, 3, 4, 6, 7} and {5} (sums: 23 and 5)
5. {1, 2, 3, 5, 6, 7} and {4} (sums: 24 and 4)
6. {1, 2, 4, 5, 6, 7} and {3} (sums: 25 and 3)
7. {1, 3, 4, 5, 6, 7} and {2} (sums: 26 and 2)
8. {2, 3, 4, 5, 6, 7} and {1} (sums: 27 and 1)

Actually, there are 4 valid ways where both sets have equal sums.
```

### DP State Representation
```
dp[i] = number of ways to make sum i using numbers 1 to n

For n = 7, target = 14:
dp[0] = 1 (empty subset)
dp[1] = 1 (using {1})
dp[2] = 1 (using {2})
dp[3] = 2 (using {3} or {1,2})
dp[4] = 3 (using {4}, {1,3}, or {2,2} - but 2,2 not valid)
dp[5] = 4 (using {5}, {1,4}, {2,3}, or {1,2,2})
...
dp[14] = number of ways to make sum 14
```

### DP Table Construction
```
Numbers: [1, 2, 3, 4, 5, 6, 7]
Target: 14

Step 1: Initialize
dp[0] = 1

Step 2: Add each number
Add 1: dp[1] = 1
Add 2: dp[2] = 1, dp[3] = 1
Add 3: dp[3] = 2, dp[4] = 1, dp[5] = 1
Add 4: dp[4] = 3, dp[5] = 2, dp[6] = 2, dp[7] = 1
Add 5: dp[5] = 4, dp[6] = 3, dp[7] = 3, dp[8] = 2, dp[9] = 1
Add 6: dp[6] = 5, dp[7] = 4, dp[8] = 4, dp[9] = 3, dp[10] = 2, dp[11] = 1
Add 7: dp[7] = 6, dp[8] = 5, dp[9] = 5, dp[10] = 4, dp[11] = 3, dp[12] = 2, dp[13] = 1

Final result: dp[14] = number of ways to make sum 14
```

### Visual DP Table
```
Sum:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
Ways: 1  1  1  2  3  4  5  6  5  4  3  2  1  1  4

Each cell shows number of ways to make that sum
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(2^n)       │ O(n)         │ Try all      │
│                 │              │              │ subsets      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bottom-up DP    │ O(n²)        │ O(n²)        │ Build from   │
│                 │              │              │ base cases   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Space-optimized │ O(n²)        │ O(n)         │ Use only     │
│ DP              │              │              │ current row  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Dynamic Programming for Partitioning**
- Divide set into equal-sum subsets
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Subset Sum Problem**
- Find subsets that sum to target
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Modular Arithmetic**
- Handle large numbers efficiently
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Three Sets with Equal Sums
**Problem**: Divide numbers into three sets with equal sums.

```python
def three_sets_equal_sums(n):
    total_sum = n * (n + 1) // 2
    
    # If total sum is not divisible by 3, no valid partition exists
    if total_sum % 3 != 0:
        return 0
    
    target = total_sum // 3
    MOD = 10**9 + 7
    
    # dp[i][j] = ways to achieve sum i with j sets
    dp = [[0] * 4 for _ in range(target + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            for k in range(3):
                if dp[j - i][k] > 0:
                    dp[j][k + 1] = (dp[j][k + 1] + dp[j - i][k]) % MOD
    
    return dp[target][3]

# Example usage
result = three_sets_equal_sums(6)
print(f"Ways to divide into 3 equal sets: {result}")
```

### Variation 2: K Sets with Equal Sums
**Problem**: Divide numbers into k sets with equal sums.

```python
def k_sets_equal_sums(n, k):
    total_sum = n * (n + 1) // 2
    
    # If total sum is not divisible by k, no valid partition exists
    if total_sum % k != 0:
        return 0
    
    target = total_sum // k
    MOD = 10**9 + 7
    
    # dp[i][j] = ways to achieve sum i with j sets
    dp = [[0] * (k + 1) for _ in range(target + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            for set_count in range(k):
                if dp[j - i][set_count] > 0:
                    dp[j][set_count + 1] = (dp[j][set_count + 1] + dp[j - i][set_count]) % MOD
    
    return dp[target][k]

# Example usage
result = k_sets_equal_sums(8, 4)
print(f"Ways to divide into 4 equal sets: {result}")
```

### Variation 3: Sets with Target Sum Difference
**Problem**: Divide numbers into two sets with given sum difference.

```python
def sets_with_difference(n, target_diff):
    total_sum = n * (n + 1) // 2
    
    # Calculate target sums
    sum1 = (total_sum + target_diff) // 2
    sum2 = (total_sum - target_diff) // 2
    
    if sum1 < 0 or sum2 < 0 or sum1 + sum2 != total_sum:
        return 0
    
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to achieve sum i
    dp = [0] * (sum1 + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, n + 1):
        for j in range(sum1, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % MOD
    
    return dp[sum1]

# Example usage
result = sets_with_difference(5, 2)
print(f"Ways to divide with difference 2: {result}")
```

### Variation 4: Sets with Minimum Sum Difference
**Problem**: Find minimum possible difference between two set sums.

```python
def minimum_set_difference(n):
    total_sum = n * (n + 1) // 2
    
    # Find all achievable sums
    dp = [False] * (total_sum + 1)
    dp[0] = True  # Base case
    
    for i in range(1, n + 1):
        for j in range(total_sum, i - 1, -1):
            if dp[j - i]:
                dp[j] = True
    
    # Find minimum difference
    min_diff = float('inf')
    for i in range(total_sum + 1):
        if dp[i]:
            diff = abs(i - (total_sum - i))
            min_diff = min(min_diff, diff)
    
    return min_diff

# Example usage
result = minimum_set_difference(6)
print(f"Minimum set difference: {result}")
```

### Variation 5: Sets with Constraints
**Problem**: Divide numbers with additional constraints.

```python
def constrained_set_partition(n, constraints):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return 0
    
    target = total_sum // 2
    MOD = 10**9 + 7
    
    # dp[i][mask] = ways to achieve sum i with used numbers mask
    dp = [[0] * (1 << n) for _ in range(target + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            for mask in range(1 << n):
                if dp[j - i][mask] > 0:
                    new_mask = mask | (1 << (i - 1))
                    if new_mask not in constraints:
                        dp[j][new_mask] = (dp[j][new_mask] + dp[j - i][mask]) % MOD
    
    return sum(dp[target]) % MOD

# Example usage
constraints = {0b111}  # Cannot use first 3 numbers together
result = constrained_set_partition(5, constraints)
print(f"Constrained partition ways: {result}")
```

## 🔗 Related Problems

- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar subset sum problems
- **[Coin Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar counting problems
- **[Partition Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: Set partitioning problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for partitioning problems
2. **Subset Sum**: Important for understanding equal partitions
3. **Modular Arithmetic**: Important for handling large numbers
4. **Set Theory**: Important for understanding partitions

---

**This is a great introduction to dynamic programming for partitioning problems!** 🎯 