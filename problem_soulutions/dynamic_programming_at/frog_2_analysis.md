---
layout: simple
title: "Frog 2 - AtCoder Educational DP Contest Problem B"
permalink: /problem_soulutions/dynamic_programming_at/frog_2_analysis
---

# Frog 2 - AtCoder Educational DP Contest Problem B

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Extend 1D DP to handle multiple transition options
- Generalize DP solutions from fixed transitions to variable transitions
- Apply DP to problems with k-step transitions
- Optimize DP solutions for multiple possible moves
- Recognize patterns in DP transition generalization

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic Programming, state transitions, 1D DP
- **Data Structures**: Arrays, iteration
- **Mathematical Concepts**: Minimum value computation, optimization
- **Programming Skills**: Loop optimization, array manipulation
- **Related Problems**: Frog 1 (AtCoder DP A), Climbing Stairs (LeetCode)

## 📋 Problem Description

There are N stones, numbered 1, 2, ..., N. For each i (1 ≤ i ≤ N), the height of Stone i is h_i. There is a frog who is initially on Stone 1. He will repeat the following action some number of times to reach Stone N:
- If the frog is currently on Stone i, jump to one of Stone i+1, i+2, ..., i+K. Here, a cost of |h_i - h_j| is incurred, where j is the stone to land on.

Find the minimum possible total cost incurred before the frog reaches Stone N.

**Input**: 
- First line: N, K (2 ≤ N ≤ 10^5, 1 ≤ K ≤ 100)
- Second line: h_1, h_2, ..., h_N (1 ≤ h_i ≤ 10^4)

**Output**: 
- Print the minimum total cost

**Constraints**:
- 2 ≤ N ≤ 10^5
- 1 ≤ K ≤ 100
- 1 ≤ h_i ≤ 10^4

**Example**:
```
Input:
5 3
10 30 40 50 20

Output:
30

Explanation**: 
Optimal path: Stone 1 → Stone 5
Cost: |10-20| = 10 (if K ≥ 4, can jump directly)
Or: Stone 1 → Stone 2 → Stone 5
Cost: |10-30| + |30-20| = 20 + 10 = 30
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution (Brute Force)

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Try all possible paths with k-step jumps
- **Complete Enumeration**: Explore all possible jump sequences
- **Simple Implementation**: Easy to understand
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible paths with jumps of 1 to K steps.

**Algorithm**:
- Start from stone 1
- At each stone i, try jumping to i+1, i+2, ..., i+K
- Calculate the cost for each path
- Return the minimum cost path

**Visual Example**:
```
Stones: [10, 30, 40, 50, 20], K = 3
        0   1   2   3   4

Recursive exploration from stone 0:
┌─────────────────────────────────────┐
│ From stone 0:                       │
│ - Jump to 1: cost=20, then recurse  │
│ - Jump to 2: cost=30, then recurse  │
│ - Jump to 3: cost=40, then recurse  │
│ ... (explores all paths)            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def frog_2_recursive(n, k, heights):
    """
    Recursive solution for Frog 2 problem
    
    Args:
        n: number of stones
        k: maximum jump distance
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    def min_cost(i):
        """Calculate minimum cost from stone i to stone n-1"""
        # Base case: already at destination
        if i == n - 1:
            return 0
        
        # Try all possible jumps (1 to k steps)
        min_path_cost = float('inf')
        for jump in range(1, min(k + 1, n - i)):
            next_stone = i + jump
            cost = abs(heights[i] - heights[next_stone]) + min_cost(next_stone)
            min_path_cost = min(min_path_cost, cost)
        
        return min_path_cost
    
    return min_cost(0)

# Example usage
n, k = 5, 3
heights = [10, 30, 40, 50, 20]
result = frog_2_recursive(n, k, heights)
print(f"Minimum cost: {result}")  # Output: 30
```

**Time Complexity**: O(K^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to recalculating the same subproblems multiple times.

---

### Approach 2: Memoized Recursive Solution

**Key Insights from Memoized Solution**:
- **Memoization**: Store results of subproblems
- **Top-Down DP**: Recursive approach with caching
- **Efficient**: O(n*K) time complexity
- **Memory Trade-off**: O(n) space for memoization

**Key Insight**: Use memoization to cache results of subproblems and avoid redundant calculations.

**Implementation**:
```python
def frog_2_memoized(n, k, heights):
    """
    Memoized recursive solution for Frog 2 problem
    
    Args:
        n: number of stones
        k: maximum jump distance
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    memo = {}
    
    def min_cost(i):
        """Calculate minimum cost from stone i to stone n-1"""
        # Check memo
        if i in memo:
            return memo[i]
        
        # Base case: already at destination
        if i == n - 1:
            memo[i] = 0
            return 0
        
        # Try all possible jumps (1 to k steps)
        min_path_cost = float('inf')
        for jump in range(1, min(k + 1, n - i)):
            next_stone = i + jump
            cost = abs(heights[i] - heights[next_stone]) + min_cost(next_stone)
            min_path_cost = min(min_path_cost, cost)
        
        memo[i] = min_path_cost
        return min_path_cost
    
    return min_cost(0)

# Example usage
n, k = 5, 3
heights = [10, 30, 40, 50, 20]
result = frog_2_memoized(n, k, heights)
print(f"Minimum cost: {result}")  # Output: 30
```

**Time Complexity**: O(n*K)
**Space Complexity**: O(n)

**Why it's better**: Uses memoization to achieve O(n*K) time complexity.

---

### Approach 3: Bottom-Up Dynamic Programming (Optimal)

**Key Insights from Bottom-Up DP Solution**:
- **Bottom-Up DP**: Build solution from base cases
- **Iterative Approach**: No recursion stack overhead
- **Efficient**: O(n*K) time, O(n) space
- **Optimal**: Best approach for this problem

**Key Insight**: Build the solution iteratively from the destination backwards.

#### 📌 **DP State Definition**

**What does `dp[i]` represent?**
- `dp[i]` = **minimum cost** to reach stone N-1 (destination) starting from stone i
- This is a 1D DP array where index i represents the current stone position
- `dp[n-1]` = 0 (base case: already at destination)
- `dp[0]` = our final answer (minimum cost from stone 0 to stone N-1)

**In plain language:**
- For each stone position i, we store the minimum cost to reach the destination
- We can compute dp[i] by considering jumps to i+1, i+2, ..., i+K

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to minimize? The total cost to reach stone N-1
- What information do we need? For each stone, the minimum cost to reach the destination

**Step 2: Define the DP State** (See DP State Definition section above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i]`?
- From stone i, we can jump to i+1, i+2, ..., i+K (up to n-1)
- Cost to jump from i to j is |h_i - h_j|
- Therefore: `dp[i] = min(dp[j] + |h_i - h_j|)` for all j in [i+1, min(i+K, n-1)]

**Step 4: Determine Base Cases**
- `dp[n-1] = 0`: Already at destination, no cost

**Step 5: Identify the Answer**
- The answer is `dp[0]` - the minimum cost from stone 0 to stone N-1

#### 📊 **Visual DP Table Construction**

For `n = 5, k = 3, heights = [10, 30, 40, 50, 20]`:
```
Step-by-step DP table filling (backwards):

dp[4] = 0  (base case: at destination)

dp[3] = min(
    dp[4] + |50 - 20| = 0 + 30 = 30
) = 30

dp[2] = min(
    dp[3] + |40 - 50| = 30 + 10 = 40,
    dp[4] + |40 - 20| = 0 + 20 = 20
) = 20

dp[1] = min(
    dp[2] + |30 - 40| = 20 + 10 = 30,
    dp[3] + |30 - 50| = 30 + 20 = 50,
    dp[4] + |30 - 20| = 0 + 10 = 10
) = 10

dp[0] = min(
    dp[1] + |10 - 30| = 10 + 20 = 30,
    dp[2] + |10 - 40| = 20 + 30 = 50,
    dp[3] + |10 - 50| = 30 + 40 = 70
) = 30

Final answer: dp[0] = 30
```

**Algorithm**:
- Initialize `dp[n-1] = 0`
- For i from n-2 down to 0:
  - For each jump distance j from 1 to min(K, n-1-i):
    - `next_stone = i + j`
    - `cost = dp[next_stone] + |h_i - h_{next_stone}|`
    - `dp[i] = min(dp[i], cost)`
- Return `dp[0]`

**Visual Example**:
```
DP table for n=5, k=3, heights=[10, 30, 40, 50, 20]:

┌─────────────────────────────────────┐
│ Stone:  0   1   2   3   4           │
│ Height: 10  30  40  50  20          │
│ DP:     30  10  20  30  0           │
│                                     │
│ Optimal path: 0→1→4                 │
│ Cost: 30 (20+10 = 30)              │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def frog_2_dp(n, k, heights):
    """
    Bottom-up DP solution for Frog 2 problem
    
    Args:
        n: number of stones
        k: maximum jump distance
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    # Create DP table
    dp = [float('inf')] * n
    
    # Base case: already at destination
    dp[n - 1] = 0
    
    # Fill DP table backwards
    for i in range(n - 2, -1, -1):
        # Try all possible jumps (1 to k steps)
        for jump in range(1, min(k + 1, n - i)):
            next_stone = i + jump
            cost = dp[next_stone] + abs(heights[i] - heights[next_stone])
            dp[i] = min(dp[i], cost)
    
    return dp[0]

# Example usage
n, k = 5, 3
heights = [10, 30, 40, 50, 20]
result = frog_2_dp(n, k, heights)
print(f"Minimum cost: {result}")  # Output: 30
```

**Time Complexity**: O(n*K)
**Space Complexity**: O(n)

**Why it's optimal**: Uses bottom-up DP for O(n*K) time and O(n) space complexity.

**Implementation Details**:
- **Bottom-Up Approach**: Build solution from destination backwards
- **Iterative**: No recursion stack overhead
- **Multiple Transitions**: Consider all possible jump distances

---

### Approach 4: Forward DP Solution

**Key Insights from Forward DP Solution**:
- **Forward DP**: Build solution from start to end
- **Alternative Approach**: Define state as minimum cost to reach stone i
- **Same Complexity**: O(n*K) time, O(n) space

**Key Insight**: Define dp[i] as minimum cost to reach stone i from stone 0.

**Algorithm**:
- Initialize `dp[0] = 0`
- For each stone i from 1 to n-1:
  - For each previous stone j from max(0, i-K) to i-1:
    - `cost = dp[j] + |h_j - h_i|`
    - `dp[i] = min(dp[i], cost)`
- Return `dp[n-1]`

**Implementation**:
```python
def frog_2_forward_dp(n, k, heights):
    """
    Forward DP solution for Frog 2 problem
    
    Args:
        n: number of stones
        k: maximum jump distance
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    # Create DP table
    dp = [float('inf')] * n
    
    # Base case: starting at stone 0, cost is 0
    dp[0] = 0
    
    # Fill DP table forwards
    for i in range(1, n):
        # Try all possible previous stones (within k distance)
        for j in range(max(0, i - k), i):
            cost = dp[j] + abs(heights[j] - heights[i])
            dp[i] = min(dp[i], cost)
    
    return dp[n - 1]

# Example usage
n, k = 5, 3
heights = [10, 30, 40, 50, 20]
result = frog_2_forward_dp(n, k, heights)
print(f"Minimum cost: {result}")  # Output: 30
```

**Time Complexity**: O(n*K)
**Space Complexity**: O(n)

**Why it's equivalent**: Forward and backward DP have the same complexity, choose based on problem structure.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(K^n) | O(n) | Complete enumeration of all paths |
| Memoized | O(n*K) | O(n) | Cache subproblem results |
| Bottom-Up DP | O(n*K) | O(n) | Build solution iteratively |
| Forward DP | O(n*K) | O(n) | Build from start to end |

### Time Complexity
- **Time**: O(n*K) - For each of n stones, consider K possible jumps
- **Space**: O(n) - DP array of size n

### Why This Solution Works
- **Optimal Substructure**: Minimum cost to reach destination from stone i depends on minimum costs from stones i+1 to i+K
- **Overlapping Subproblems**: Same subproblems are solved multiple times
- **DP Optimization**: Bottom-up approach avoids redundant calculations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Frog 2 - Path Reconstruction**
**Problem**: Find minimum cost and reconstruct the optimal path.

**Implementation**:
```python
def frog_2_with_path(n, k, heights):
    """
    DP solution with path reconstruction for Frog 2 problem
    
    Args:
        n: number of stones
        k: maximum jump distance
        heights: list of stone heights
    
    Returns:
        tuple: (minimum cost, optimal path)
    """
    dp = [float('inf')] * n
    parent = [-1] * n
    
    dp[n - 1] = 0
    
    for i in range(n - 2, -1, -1):
        for jump in range(1, min(k + 1, n - i)):
            next_stone = i + jump
            cost = dp[next_stone] + abs(heights[i] - heights[next_stone])
            
            if cost < dp[i]:
                dp[i] = cost
                parent[i] = next_stone
    
    # Reconstruct path
    path = [0]
    current = 0
    while parent[current] != -1:
        current = parent[current]
        path.append(current)
    
    return dp[0], path

# Example usage
n, k = 5, 3
heights = [10, 30, 40, 50, 20]
cost, path = frog_2_with_path(n, k, heights)
print(f"Minimum cost: {cost}")
print(f"Optimal path: {path}")
```

#### **2. Frog 2 - Multiple Constraints**
**Problem**: Add constraints like maximum number of jumps or energy limits.

**Implementation**:
```python
def frog_2_with_constraints(n, k, heights, max_jumps):
    """
    DP solution with maximum jumps constraint
    
    Args:
        n: number of stones
        k: maximum jump distance
        heights: list of stone heights
        max_jumps: maximum number of jumps allowed
    
    Returns:
        int: minimum total cost, or -1 if impossible
    """
    # dp[i][j] = min cost to reach stone n-1 from stone i using at most j jumps
    dp = [[float('inf')] * (max_jumps + 1) for _ in range(n)]
    
    dp[n - 1][0] = 0  # At destination with 0 jumps
    
    for i in range(n - 2, -1, -1):
        for jumps_remaining in range(1, max_jumps + 1):
            for jump in range(1, min(k + 1, n - i)):
                next_stone = i + jump
                cost = abs(heights[i] - heights[next_stone])
                
                if dp[next_stone][jumps_remaining - 1] != float('inf'):
                    total_cost = dp[next_stone][jumps_remaining - 1] + cost
                    dp[i][jumps_remaining] = min(dp[i][jumps_remaining], total_cost)
    
    result = min(dp[0])
    return result if result != float('inf') else -1

# Example usage
n, k = 5, 3
heights = [10, 30, 40, 50, 20]
max_jumps = 3
result = frog_2_with_constraints(n, k, heights, max_jumps)
print(f"Minimum cost: {result}")
```

### Related Problems

#### **AtCoder Problems**
- [Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) - Previous problem (K=2)
- [Frog 3](https://atcoder.jp/contests/dp/tasks/dp_z) - Advanced version with convex hull trick

#### **LeetCode Problems**
- [Jump Game II](https://leetcode.com/problems/jump-game-ii/) - Similar jumping pattern
- [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) - Similar structure

#### **CSES Problems**
- [Minimizing Coins](https://cses.fi/problemset/task/1634) - Similar DP pattern

#### **Problem Categories**
- **1D DP with Multiple Transitions**: Linear state space, multiple transition options
- **Minimum Path**: Finding optimal paths with constraints
- **Cost Optimization**: Minimizing costs with multiple choices

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming Introduction](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP fundamentals
- [1D DP Problems](https://cp-algorithms.com/dynamic_programming/1d-dp.html) - Linear DP techniques

### **Practice Problems**
- [AtCoder DP Contest Problem B](https://atcoder.jp/contests/dp/tasks/dp_b) - Original problem
- [AtCoder DP Contest Problem A](https://atcoder.jp/contests/dp/tasks/dp_a) - Previous problem
- [AtCoder DP Contest Problem Z](https://atcoder.jp/contests/dp/tasks/dp_z) - Advanced version

### **Further Reading**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms) - Dynamic Programming chapter
- [Competitive Programming Handbook](https://cses.fi/book/book.pdf) - DP section

