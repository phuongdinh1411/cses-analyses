---
layout: simple
title: "Frog 1"
permalink: /problem_soulutions/dynamic_programming_at/frog_1_analysis
---

# Frog 1

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand 1D dynamic programming with linear transitions
- Apply DP to solve minimum cost path problems
- Recognize when to use bottom-up vs top-down DP approaches
- Implement space-optimized DP solutions
- Handle edge cases in DP problems

## 📋 Problem Description

There are N stones, numbered 1, 2, ..., N. For each i (1 ≤ i ≤ N), the height of Stone i is h_i. There is a frog who is initially on Stone 1. He will repeat the following action some number of times to reach Stone N:
- If the frog is currently on Stone i, jump to Stone i+1 or Stone i+2. Here, a cost of |h_i - h_j| is incurred, where j is the stone to land on.

Find the minimum possible total cost incurred before the frog reaches Stone N.

**Input**: 
- First line: N (2 ≤ N ≤ 10^5)
- Second line: h_1, h_2, ..., h_N (1 ≤ h_i ≤ 10^4)

**Output**: 
- Print the minimum total cost

**Constraints**:
- 2 ≤ N ≤ 10^5
- 1 ≤ h_i ≤ 10^4

**Example**:
```
Input:
6
30 10 60 10 60 50

Output:
40

Explanation**: 
Optimal path: Stone 1 → Stone 2 → Stone 4 → Stone 6
Cost: |30-10| + |10-10| + |10-50| = 20 + 0 + 40 = 40
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution (Brute Force)

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Try all possible paths from stone 1 to stone N
- **Complete Enumeration**: Explore all possible jump sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible paths from the current stone to the destination.

**Algorithm**:
- Start from stone 1
- At each stone i, try jumping to i+1 and i+2
- Calculate the cost for each path
- Return the minimum cost path

**Visual Example**:
```
Stones: [30, 10, 60, 10, 60, 50]
        0   1   2   3   4   5

Recursive exploration:
┌─────────────────────────────────────┐
│ From stone 0:                       │
│ - Jump to 1: cost=20, then recurse  │
│ - Jump to 2: cost=30, then recurse  │
│                                     │
│ From stone 1:                       │
│ - Jump to 2: cost=50, then recurse  │
│ - Jump to 3: cost=0, then recurse   │
│ ... (explores all paths)            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def frog_1_recursive(n, heights):
    """
    Recursive solution for Frog 1 problem
    
    Args:
        n: number of stones
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    def min_cost(i):
        """Calculate minimum cost from stone i to stone n-1"""
        # Base case: already at destination
        if i == n - 1:
            return 0
        
        # Base case: can only jump to destination
        if i == n - 2:
            return abs(heights[i] - heights[n - 1])
        
        # Try jumping to i+1
        cost1 = abs(heights[i] - heights[i + 1]) + min_cost(i + 1)
        
        # Try jumping to i+2
        cost2 = abs(heights[i] - heights[i + 2]) + min_cost(i + 2)
        
        return min(cost1, cost2)
    
    return min_cost(0)

# Example usage
n = 6
heights = [30, 10, 60, 10, 60, 50]
result = frog_1_recursive(n, heights)
print(f"Minimum cost: {result}")  # Output: 40
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to recalculating the same subproblems multiple times.

---

### Approach 2: Memoized Recursive Solution

**Key Insights from Memoized Solution**:
- **Memoization**: Store results of subproblems to avoid recomputation
- **Top-Down DP**: Recursive approach with caching
- **Efficient**: O(n) time complexity
- **Memory Trade-off**: O(n) space for memoization

**Key Insight**: Use memoization to cache results of subproblems and avoid redundant calculations.

**Algorithm**:
- Use recursion with memoization
- Store computed results in a dictionary/array
- Return cached results when available

**Visual Example**:
```
Memoization table:
dp[0] = min cost from stone 0 to N-1
dp[1] = min cost from stone 1 to N-1
...
dp[N-1] = 0 (base case)

When computing dp[i], check if already computed.
```

**Implementation**:
```python
def frog_1_memoized(n, heights):
    """
    Memoized recursive solution for Frog 1 problem
    
    Args:
        n: number of stones
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
        
        # Base case: can only jump to destination
        if i == n - 2:
            cost = abs(heights[i] - heights[n - 1])
            memo[i] = cost
            return cost
        
        # Try jumping to i+1
        cost1 = abs(heights[i] - heights[i + 1]) + min_cost(i + 1)
        
        # Try jumping to i+2
        cost2 = abs(heights[i] - heights[i + 2]) + min_cost(i + 2)
        
        result = min(cost1, cost2)
        memo[i] = result
        return result
    
    return min_cost(0)

# Example usage
n = 6
heights = [30, 10, 60, 10, 60, 50]
result = frog_1_memoized(n, heights)
print(f"Minimum cost: {result}")  # Output: 40
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Uses memoization to achieve O(n) time complexity.

**Implementation Considerations**:
- **Memoization**: Store results to avoid recomputation
- **Top-Down Approach**: Natural recursive structure
- **Memory Management**: Consider stack depth for large n

---

### Approach 3: Bottom-Up Dynamic Programming (Optimal)

**Key Insights from Bottom-Up DP Solution**:
- **Bottom-Up DP**: Build solution from base cases
- **Iterative Approach**: No recursion stack overhead
- **Efficient**: O(n) time, O(n) space
- **Optimal**: Best approach for this problem

**Key Insight**: Build the solution iteratively from the destination backwards, or from start forwards.

#### 📌 **DP State Definition**

**What does `dp[i]` represent?**
- `dp[i]` = **minimum cost** to reach stone N-1 (destination) starting from stone i
- This is a 1D DP array where index i represents the current stone position
- `dp[n-1]` = 0 (base case: already at destination)
- `dp[0]` = our final answer (minimum cost from stone 0 to stone N-1)

**In plain language:**
- For each stone position i, we store the minimum cost to reach the destination
- We can compute dp[i] by considering jumps to i+1 and i+2

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to minimize? The total cost to reach stone N-1
- What information do we need? For each stone, the minimum cost to reach the destination

**Step 2: Define the DP State** (See DP State Definition section above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i]`?
- From stone i, we can jump to i+1 or i+2
- Cost to jump from i to j is |h_i - h_j|
- Therefore: `dp[i] = min(dp[i+1] + |h_i - h_{i+1}|, dp[i+2] + |h_i - h_{i+2}|)`
- For each possible jump, add the jump cost to the minimum cost from the destination stone

**Step 4: Determine Base Cases**
- `dp[n-1] = 0`: Already at destination, no cost
- `dp[n-2] = |h_{n-2} - h_{n-1}|`: Only one possible jump to destination

**Step 5: Identify the Answer**
- The answer is `dp[0]` - the minimum cost from stone 0 to stone N-1

#### 📊 **Visual DP Table Construction**

For `n = 6, heights = [30, 10, 60, 10, 60, 50]`:
```
Step-by-step DP table filling (backwards):

dp[5] = 0  (base case: at destination)

dp[4] = |60 - 50| = 10  (only one jump possible)

dp[3] = min(
    dp[4] + |10 - 60| = 10 + 50 = 60,
    dp[5] + |10 - 50| = 0 + 40 = 40
) = 40

dp[2] = min(
    dp[3] + |60 - 10| = 40 + 50 = 90,
    dp[4] + |60 - 60| = 10 + 0 = 10
) = 10

dp[1] = min(
    dp[2] + |10 - 60| = 10 + 50 = 60,
    dp[3] + |10 - 10| = 40 + 0 = 40
) = 40

dp[0] = min(
    dp[1] + |30 - 10| = 40 + 20 = 60,
    dp[2] + |30 - 60| = 10 + 30 = 40
) = 40

Final answer: dp[0] = 40
```

**Algorithm**:
- Initialize `dp[n-1] = 0`
- Initialize `dp[n-2] = |h_{n-2} - h_{n-1}|`
- For i from n-3 down to 0:
  - `dp[i] = min(dp[i+1] + |h_i - h_{i+1}|, dp[i+2] + |h_i - h_{i+2}|)`
- Return `dp[0]`

**Visual Example**:
```
DP table for n=6, heights=[30, 10, 60, 10, 60, 50]:

┌─────────────────────────────────────┐
│ Stone:  0   1   2   3   4   5      │
│ Height: 30  10  60  10  60  50     │
│ DP:     40  40  10  40  10  0      │
│                                     │
│ Optimal path: 0→2→4→5              │
│ Cost: 40 (30+10+0 = 40)            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def frog_1_dp(n, heights):
    """
    Bottom-up DP solution for Frog 1 problem
    
    Args:
        n: number of stones
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    # Create DP table
    dp = [0] * n
    
    # Base case: already at destination
    dp[n - 1] = 0
    
    # Base case: one jump to destination
    if n >= 2:
        dp[n - 2] = abs(heights[n - 2] - heights[n - 1])
    
    # Fill DP table backwards
    for i in range(n - 3, -1, -1):
        # Try jumping to i+1
        cost1 = dp[i + 1] + abs(heights[i] - heights[i + 1])
        
        # Try jumping to i+2
        cost2 = dp[i + 2] + abs(heights[i] - heights[i + 2])
        
        dp[i] = min(cost1, cost2)
    
    return dp[0]

# Example usage
n = 6
heights = [30, 10, 60, 10, 60, 50]
result = frog_1_dp(n, heights)
print(f"Minimum cost: {result}")  # Output: 40
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses bottom-up DP for O(n) time and space complexity.

**Implementation Details**:
- **Bottom-Up Approach**: Build solution from base cases
- **Iterative**: No recursion stack overhead
- **Space Efficient**: Can be optimized to O(1) if only last two values needed

---

### Approach 4: Space-Optimized DP Solution

**Key Insights from Space-Optimized Solution**:
- **Space Optimization**: Only need last two DP values
- **Rolling Variables**: Use variables instead of array
- **Efficient**: O(n) time, O(1) space
- **Optimal Complexity**: Best space complexity

**Key Insight**: Since we only need dp[i+1] and dp[i+2] to compute dp[i], we can use just two variables.

**Algorithm**:
- Use two variables to track last two DP values
- Update them as we iterate backwards
- Return the final result

**Implementation**:
```python
def frog_1_space_optimized(n, heights):
    """
    Space-optimized DP solution for Frog 1 problem
    
    Args:
        n: number of stones
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    # Base cases
    if n == 1:
        return 0
    
    # Only need last two values
    prev2 = 0  # dp[n-1]
    prev1 = abs(heights[n - 2] - heights[n - 1])  # dp[n-2]
    
    # Fill DP backwards using only two variables
    for i in range(n - 3, -1, -1):
        # Try jumping to i+1 and i+2
        cost1 = prev1 + abs(heights[i] - heights[i + 1])
        cost2 = prev2 + abs(heights[i] - heights[i + 2])
        
        current = min(cost1, cost2)
        
        # Update for next iteration
        prev2, prev1 = prev1, current
    
    return prev1

# Example usage
n = 6
heights = [30, 10, 60, 10, 60, 50]
result = frog_1_space_optimized(n, heights)
print(f"Minimum cost: {result}")  # Output: 40
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses O(1) space while maintaining O(n) time complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Complete enumeration of all paths |
| Memoized | O(n) | O(n) | Cache subproblem results |
| Bottom-Up DP | O(n) | O(n) | Build solution iteratively |
| Space-Optimized DP | O(n) | O(1) | Only need last two values |

### Time Complexity
- **Time**: O(n) - Single pass through all stones
- **Space**: O(1) - Only two variables needed for space-optimized version

### Why This Solution Works
- **Optimal Substructure**: Minimum cost to reach destination from stone i depends on minimum costs from stones i+1 and i+2
- **Overlapping Subproblems**: Same subproblems are solved multiple times in recursive approach
- **DP Optimization**: Bottom-up approach avoids redundant calculations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Frog 1 - Forward DP Approach**
**Problem**: Solve using forward DP (building from start to end).

**Key Differences**: Iterate from 0 to n-1 instead of backwards

**Solution Approach**: Define dp[i] as minimum cost from stone 0 to stone i

**Implementation**:
```python
def frog_1_forward_dp(n, heights):
    """
    Forward DP solution for Frog 1 problem
    
    Args:
        n: number of stones
        heights: list of stone heights
    
    Returns:
        int: minimum total cost
    """
    dp = [float('inf')] * n
    dp[0] = 0  # Starting at stone 0, cost is 0
    
    for i in range(n):
        # Try jumping to i+1
        if i + 1 < n:
            cost = dp[i] + abs(heights[i] - heights[i + 1])
            dp[i + 1] = min(dp[i + 1], cost)
        
        # Try jumping to i+2
        if i + 2 < n:
            cost = dp[i] + abs(heights[i] - heights[i + 2])
            dp[i + 2] = min(dp[i + 2], cost)
    
    return dp[n - 1]

# Example usage
n = 6
heights = [30, 10, 60, 10, 60, 50]
result = frog_1_forward_dp(n, heights)
print(f"Minimum cost: {result}")  # Output: 40
```

#### **2. Frog 1 - Path Reconstruction**
**Problem**: Not just find minimum cost, but also reconstruct the optimal path.

**Key Differences**: Track parent/previous stone for each optimal choice

**Solution Approach**: Maintain parent array to reconstruct path

**Implementation**:
```python
def frog_1_with_path(n, heights):
    """
    DP solution with path reconstruction for Frog 1 problem
    
    Args:
        n: number of stones
        heights: list of stone heights
    
    Returns:
        tuple: (minimum cost, optimal path)
    """
    dp = [0] * n
    parent = [-1] * n
    
    dp[n - 1] = 0
    if n >= 2:
        dp[n - 2] = abs(heights[n - 2] - heights[n - 1])
        parent[n - 2] = n - 1
    
    for i in range(n - 3, -1, -1):
        cost1 = dp[i + 1] + abs(heights[i] - heights[i + 1])
        cost2 = dp[i + 2] + abs(heights[i] - heights[i + 2])
        
        if cost1 <= cost2:
            dp[i] = cost1
            parent[i] = i + 1
        else:
            dp[i] = cost2
            parent[i] = i + 2
    
    # Reconstruct path
    path = [0]
    current = 0
    while parent[current] != -1:
        current = parent[current]
        path.append(current)
    
    return dp[0], path

# Example usage
n = 6
heights = [30, 10, 60, 10, 60, 50]
cost, path = frog_1_with_path(n, heights)
print(f"Minimum cost: {cost}")  # Output: 40
print(f"Optimal path: {path}")  # Output: [0, 2, 4, 5]
```

#### **3. Frog 1 - Multiple Destinations**
**Problem**: Find minimum cost to reach any of multiple destination stones.

**Key Differences**: Have multiple possible destination stones

**Solution Approach**: Initialize multiple base cases

**Implementation**:
```python
def frog_1_multiple_destinations(n, heights, destinations):
    """
    DP solution for reaching any of multiple destinations
    
    Args:
        n: number of stones
        heights: list of stone heights
        destinations: set of destination stone indices
    
    Returns:
        int: minimum total cost to reach any destination
    """
    dp = [float('inf')] * n
    
    # Initialize base cases for all destinations
    for dest in destinations:
        dp[dest] = 0
    
    # Fill DP backwards
    for i in range(n - 1, -1, -1):
        if i in destinations:
            continue  # Already initialized
        
        if i + 1 < n:
            cost1 = dp[i + 1] + abs(heights[i] - heights[i + 1])
            dp[i] = min(dp[i], cost1)
        
        if i + 2 < n:
            cost2 = dp[i + 2] + abs(heights[i] - heights[i + 2])
            dp[i] = min(dp[i], cost2)
    
    return dp[0]

# Example usage
n = 6
heights = [30, 10, 60, 10, 60, 50]
destinations = {4, 5}  # Can end at stone 4 or 5
result = frog_1_multiple_destinations(n, heights, destinations)
print(f"Minimum cost: {result}")
```

### Related Problems

#### **CSES Problems**
- [Minimizing Coins](https://cses.fi/problemset/task/1634) - Similar DP pattern
- [Removing Digits](https://cses.fi/problemset/task/1637) - Similar state transitions

#### **LeetCode Problems**
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) - Similar structure
- [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) - Almost identical problem
- [Jump Game II](https://leetcode.com/problems/jump-game-ii/) - Similar jumping pattern

#### **AtCoder Problems**
- [Frog 2](https://atcoder.jp/contests/dp/tasks/dp_b) - Extension with k jumps
- [Frog 3](https://atcoder.jp/contests/dp/tasks/dp_z) - Advanced version with convex hull trick

#### **Problem Categories**
- **1D DP**: Linear state space, simple transitions
- **Minimum Path**: Finding optimal paths
- **Cost Optimization**: Minimizing costs

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming Introduction](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP fundamentals
- [1D DP Problems](https://cp-algorithms.com/dynamic_programming/1d-dp.html) - Linear DP techniques

### **Practice Problems**
- [AtCoder DP Contest Problem A](https://atcoder.jp/contests/dp/tasks/dp_a) - Original problem
- [AtCoder DP Contest Problem B](https://atcoder.jp/contests/dp/tasks/dp_b) - Next in series
- [LeetCode Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) - Similar problem

### **Further Reading**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms) - Dynamic Programming chapter
- [Competitive Programming Handbook](https://cses.fi/book/book.pdf) - DP section

