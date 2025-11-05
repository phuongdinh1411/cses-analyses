---
layout: simple
title: "Coins - AtCoder Educational DP Contest Problem I"
permalink: /problem_soulutions/dynamic_programming_at/coins_analysis
---

# Coins - AtCoder Educational DP Contest Problem I

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand probability DP problems
- Apply DP to solve probability/expectation problems
- Handle floating-point precision in DP
- Recognize when to use probability DP patterns
- Optimize probability DP computations

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic Programming, probability theory, expectation
- **Data Structures**: Arrays, 2D arrays
- **Mathematical Concepts**: Probability, expectation, conditional probability
- **Programming Skills**: Floating-point arithmetic, DP implementation
- **Related Problems**: Dice roll problems, probability DP

## 📋 Problem Description

There are N coins, numbered 1, 2, ..., N. For each i (1 ≤ i ≤ N), when Coin i is tossed, it comes up heads with probability p_i and tails with probability 1-p_i. Taro has tossed all N coins. Find the probability of having more heads than tails.

**Input**: 
- First line: N (1 ≤ N ≤ 3000)
- Second line: p_1, p_2, ..., p_N (0 < p_i < 1)

**Output**: 
- Print the probability (with absolute error ≤ 10^-9)

**Constraints**:
- 1 ≤ N ≤ 3000
- 0 < p_i < 1

**Example**:
```
Input:
3
0.30 0.60 0.80

Output:
0.612

Explanation**: 
We need more heads than tails, i.e., at least 2 heads out of 3.
P(2 heads) = 0.3*0.6*0.2 + 0.3*0.4*0.8 + 0.7*0.6*0.8 = 0.036 + 0.096 + 0.336 = 0.468
P(3 heads) = 0.3*0.6*0.8 = 0.144
Total = 0.468 + 0.144 = 0.612
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution (Brute Force)

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Try all possible outcomes
- **Complete Enumeration**: Explore all 2^N coin outcomes
- **Simple Implementation**: Easy to understand
- **Inefficient**: Exponential time complexity

**Why it doesn't work**: With N up to 3000, 2^3000 is computationally infeasible.

---

### Approach 2: Dynamic Programming (Optimal)

**Key Insights from DP Solution**:
- **DP Approach**: Use DP to count probabilities
- **State Definition**: dp[i][j] = probability of getting j heads from first i coins
- **Efficient**: O(N^2) time complexity
- **Optimal**: Best approach for this problem

**Key Insight**: Use 2D DP where dp[i][j] represents the probability of getting exactly j heads from the first i coins.

#### 📌 **DP State Definition**

**What does `dp[i][j]` represent?**
- `dp[i][j]` = **probability** of getting exactly j heads from the first i coins
- i ranges from 0 to N (number of coins considered)
- j ranges from 0 to i (number of heads possible)
- `dp[N][j]` stores probability of j heads from all N coins
- Answer: Sum of `dp[N][j]` for all j > N/2

**In plain language:**
- For each number of coins and each number of heads, we store the probability
- We can compute dp[i][j] by considering the i-th coin being heads or tails

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to compute? Probability of more heads than tails
- What information do we need? For each number of coins, probability of each number of heads

**Step 2: Define the DP State** (See DP State Definition section above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i][j]`?
- We consider coin i (0-indexed)
- Option 1: Coin i is heads → probability = p_i * dp[i-1][j-1]
- Option 2: Coin i is tails → probability = (1-p_i) * dp[i-1][j]
- Therefore: `dp[i][j] = p_i * dp[i-1][j-1] + (1-p_i) * dp[i-1][j]`

**Step 4: Determine Base Cases**
- `dp[0][0] = 1`: Zero coins, zero heads, probability 1
- `dp[0][j] = 0` for j > 0: Impossible to have heads with zero coins

**Step 5: Identify the Answer**
- Sum of `dp[N][j]` for all j such that j > N/2

#### 📊 **Visual DP Table Construction**

For `N=3, p=[0.3, 0.6, 0.8]`:
```
Step-by-step DP table filling:

Base case:
dp[0][0] = 1

For i=1 (first coin, p=0.3):
dp[1][0] = (1-0.3) * dp[0][0] = 0.7 * 1 = 0.7
dp[1][1] = 0.3 * dp[0][0] = 0.3 * 1 = 0.3

For i=2 (second coin, p=0.6):
dp[2][0] = (1-0.6) * dp[1][0] = 0.4 * 0.7 = 0.28
dp[2][1] = 0.6 * dp[1][0] + 0.4 * dp[1][1] = 0.6*0.7 + 0.4*0.3 = 0.42 + 0.12 = 0.54
dp[2][2] = 0.6 * dp[1][1] = 0.6 * 0.3 = 0.18

For i=3 (third coin, p=0.8):
dp[3][0] = 0.2 * dp[2][0] = 0.2 * 0.28 = 0.056
dp[3][1] = 0.8 * dp[2][0] + 0.2 * dp[2][1] = 0.8*0.28 + 0.2*0.54 = 0.224 + 0.108 = 0.332
dp[3][2] = 0.8 * dp[2][1] + 0.2 * dp[2][2] = 0.8*0.54 + 0.2*0.18 = 0.432 + 0.036 = 0.468
dp[3][3] = 0.8 * dp[2][2] = 0.8 * 0.18 = 0.144

Answer: dp[3][2] + dp[3][3] = 0.468 + 0.144 = 0.612
```

**Algorithm**:
- Initialize `dp[0][0] = 1`
- For i from 1 to N:
  - For j from 0 to i:
    - `dp[i][j] = p[i-1] * dp[i-1][j-1] + (1-p[i-1]) * dp[i-1][j]`
- Sum `dp[N][j]` for all j > N/2
- Return the sum

**Implementation**:
```python
def coins_dp(n, probabilities):
    """
    DP solution for Coins problem
    
    Args:
        n: number of coins
        probabilities: list of probabilities p_i
    
    Returns:
        float: probability of more heads than tails
    """
    # dp[i][j] = probability of j heads from first i coins
    dp = [[0.0] * (n + 1) for _ in range(n + 1)]
    
    # Base case: zero coins, zero heads
    dp[0][0] = 1.0
    
    # Fill DP table
    for i in range(1, n + 1):
        p = probabilities[i - 1]
        for j in range(i + 1):
            # Option 1: Current coin is tails
            if j <= i - 1:
                dp[i][j] += (1 - p) * dp[i - 1][j]
            
            # Option 2: Current coin is heads
            if j > 0:
                dp[i][j] += p * dp[i - 1][j - 1]
    
    # Sum probabilities for more heads than tails
    result = 0.0
    for j in range(n // 2 + 1, n + 1):
        result += dp[n][j]
    
    return result

# Example usage
n = 3
probabilities = [0.30, 0.60, 0.80]
result = coins_dp(n, probabilities)
print(f"Probability: {result:.3f}")  # Output: 0.612
```

**Time Complexity**: O(N^2)
**Space Complexity**: O(N^2)

**Why it's optimal**: Uses DP for O(N^2) time complexity, which is optimal for this problem.

---

### Approach 3: Space-Optimized DP Solution

**Key Insights from Space-Optimized Solution**:
- **Space Optimization**: Only need previous row
- **Rolling Array**: Use 1D array instead of 2D
- **Efficient**: O(N^2) time, O(N) space
- **Optimal Space**: Best space complexity

**Implementation**:
```python
def coins_space_optimized(n, probabilities):
    """
    Space-optimized DP solution for Coins problem
    
    Args:
        n: number of coins
        probabilities: list of probabilities p_i
    
    Returns:
        float: probability of more heads than tails
    """
    # Only need 1D array: dp[j] = probability of j heads
    dp = [0.0] * (n + 1)
    dp[0] = 1.0  # Base case: zero heads
    
    # Process each coin
    for i in range(n):
        p = probabilities[i]
        # Iterate backwards to avoid using updated values
        for j in range(i + 1, -1, -1):
            # Update: j heads can come from (j-1) heads + current head
            # or j heads + current tail
            if j > 0:
                dp[j] = p * dp[j - 1] + (1 - p) * dp[j]
            else:
                dp[j] = (1 - p) * dp[j]
    
    # Sum probabilities for more heads than tails
    result = 0.0
    for j in range(n // 2 + 1, n + 1):
        result += dp[j]
    
    return result

# Example usage
n = 3
probabilities = [0.30, 0.60, 0.80]
result = coins_space_optimized(n, probabilities)
print(f"Probability: {result:.3f}")  # Output: 0.612
```

**Time Complexity**: O(N^2)
**Space Complexity**: O(N)

**Why it's optimal**: Uses O(N) space while maintaining O(N^2) time complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^N) | O(N) | Not feasible |
| DP | O(N^2) | O(N^2) | Probability DP |
| Space-Optimized DP | O(N^2) | O(N) | Only need previous row |

### Time Complexity
- **Time**: O(N^2) - For each of N coins, consider up to N possible heads
- **Space**: O(N) - Only one array of size N+1 needed for space-optimized version

### Why This Solution Works
- **Optimal Substructure**: Probability of j heads from i coins depends on probabilities from i-1 coins
- **Overlapping Subproblems**: Same subproblems are computed multiple times
- **DP Optimization**: Bottom-up approach computes probabilities efficiently
- **Probability Theory**: Uses conditional probability and independence

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Coins - Exact Number of Heads**
**Problem**: Find probability of getting exactly k heads.

**Implementation**:
```python
def coins_exact_heads(n, probabilities, k):
    """
    Probability of exactly k heads
    
    Args:
        n: number of coins
        probabilities: list of probabilities
        k: exact number of heads desired
    
    Returns:
        float: probability of exactly k heads
    """
    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    
    for i in range(n):
        p = probabilities[i]
        for j in range(i + 1, -1, -1):
            if j > 0:
                dp[j] = p * dp[j - 1] + (1 - p) * dp[j]
            else:
                dp[j] = (1 - p) * dp[j]
    
    return dp[k] if k <= n else 0.0

# Example usage
n = 3
probabilities = [0.30, 0.60, 0.80]
result = coins_exact_heads(n, probabilities, 2)
print(f"Probability of exactly 2 heads: {result:.3f}")
```

#### **2. Coins - At Least k Heads**
**Problem**: Find probability of getting at least k heads.

**Implementation**:
```python
def coins_at_least_heads(n, probabilities, k):
    """
    Probability of at least k heads
    
    Args:
        n: number of coins
        probabilities: list of probabilities
        k: minimum number of heads
    
    Returns:
        float: probability of at least k heads
    """
    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    
    for i in range(n):
        p = probabilities[i]
        for j in range(i + 1, -1, -1):
            if j > 0:
                dp[j] = p * dp[j - 1] + (1 - p) * dp[j]
            else:
                dp[j] = (1 - p) * dp[j]
    
    result = 0.0
    for j in range(k, n + 1):
        result += dp[j]
    
    return result

# Example usage
n = 3
probabilities = [0.30, 0.60, 0.80]
result = coins_at_least_heads(n, probabilities, 2)
print(f"Probability of at least 2 heads: {result:.3f}")
```

### Related Problems

#### **AtCoder Problems**
- [Sushi](https://atcoder.jp/contests/dp/tasks/dp_j) - Similar expectation DP

#### **LeetCode Problems**
- Probability and expectation DP problems

#### **Problem Categories**
- **Probability DP**: Dynamic programming with probabilities
- **Expectation DP**: Computing expected values
- **Conditional Probability**: Using conditional probabilities in DP

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming Introduction](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP fundamentals
- [Probability DP](https://cp-algorithms.com/dynamic_programming/probability-dp.html) - Probability DP techniques

### **Practice Problems**
- [AtCoder DP Contest Problem I](https://atcoder.jp/contests/dp/tasks/dp_i) - Original problem

### **Further Reading**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms) - Dynamic Programming chapter
- Probability theory textbooks

