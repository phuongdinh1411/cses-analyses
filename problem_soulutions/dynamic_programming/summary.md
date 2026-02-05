---
layout: simple
title: "Dynamic Programming Summary"
permalink: /problem_soulutions/dynamic_programming/summary
---

# Dynamic Programming

Welcome to the Dynamic Programming section! This category covers techniques for solving complex problems by breaking them down into simpler subproblems.

## Key Concepts & Techniques

### DP Fundamentals
- **State Definition**: Choosing what to store
  - *When to use*: Define states that capture all necessary information for the problem
  - *Example*: `dp[i]` for 1D problems, `dp[i][j]` for 2D problems
- **Transition Function**: How states relate
  - *When to use*: Express how current state depends on previous states
  - *Example*: `dp[i] = dp[i-1] + dp[i-2]` for Fibonacci
- **Base Cases**: Starting points
  - *When to use*: Define initial conditions that don't depend on other states
  - *Example*: `dp[0] = 1, dp[1] = 1` for Fibonacci
- **Memoization**: Storing results
  - *When to use*: Avoid recomputing the same subproblems
  - *Example*: Use hash map or array to store computed values

### Common DP Patterns

#### 1D DP (Linear State Space)
- **When to use**: Problems with single parameter progression
- **Examples**: Fibonacci, coin change, longest increasing subsequence
- **State**: `dp[i]` represents solution for first i elements
- **Transition**: `dp[i] = f(dp[i-1], dp[i-2], ..., dp[0])`

#### 2D DP (Grid/Two Parameters)
- **When to use**: Problems with two independent parameters
- **Examples**: Grid paths, LCS, edit distance, knapsack
- **State**: `dp[i][j]` represents solution for parameters i and j
- **Transition**: `dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`

#### State Compression
- **When to use**: When only previous states are needed
- **Examples**: Fibonacci, rolling array optimization
- **Technique**: Use only necessary previous states
- **Memory**: Reduces O(n²) to O(n) or O(n) to O(1)

#### Path Problems
- **When to use**: Finding optimal paths in graphs/grids
- **Examples**: Shortest path, maximum path sum, path counting
- **State**: `dp[i][j]` represents best path to position (i,j)
- **Transition**: Consider all possible moves to current position

### Advanced DP Techniques

#### Bitmask DP
- **When to use**: Problems with subset selection or state representation
- **Examples**: TSP, subset problems, state machines
- **State**: Use bits to represent selected elements
- **Transition**: Update bitmask by adding/removing elements

#### Tree DP
- **When to use**: Problems on trees with parent-child relationships
- **Examples**: Tree diameter, tree coloring, tree matching
- **State**: `dp[node][state]` for each node and possible states
- **Transition**: Combine results from children nodes

#### Interval DP
- **When to use**: Problems on intervals or ranges
- **Examples**: Matrix chain multiplication, palindrome partitioning
- **State**: `dp[i][j]` represents solution for interval [i,j]
- **Transition**: Try all possible ways to split the interval

#### Digit DP
- **When to use**: Problems involving digits of numbers
- **Examples**: Count numbers with certain properties, digit sum problems
- **State**: `dp[pos][tight][sum]` for position, tight constraint, and sum
- **Transition**: Try all possible digits at current position

### Optimization Techniques

#### Space Optimization
- **Rolling Arrays**: When only previous states needed
  - *When to use*: 2D DP where only previous row/column matters
  - *Example*: Knapsack with rolling array
- **State Compression**: Using bits or compact representations
  - *When to use*: When state can be represented compactly
  - *Example*: Bitmask for subset problems

#### Time Optimization
- **Prefix Sums**: For range queries in DP
  - *When to use*: When transitions involve range sums
  - *Example*: Range sum queries in DP
- **Binary Search**: For optimization problems
  - *When to use*: When looking for optimal value
  - *Example*: Longest increasing subsequence with binary search

#### Transition Optimization
- **Precomputation**: Calculate common values once
  - *When to use*: When same calculations repeated
  - *Example*: Precompute factorials for combinations
- **Mathematical Formulas**: Direct calculation instead of DP
  - *When to use*: When closed-form solution exists
  - *Example*: Fibonacci with matrix exponentiation

## Problem Categories

### Basic DP Concepts
- [Dice Combinations](dice_combinations_analysis) - Count ways to get sum with dice
- [Minimizing Coins](minimizing_coins_analysis) - Coin change problem
- [Coin Combinations I](coin_combinations_i_analysis) - Unordered combinations
- [Coin Combinations II](coin_combinations_ii_analysis) - Ordered combinations
- [Removing Digits](removing_digits_analysis) - Minimize steps to zero

### Grid Problems
- [Grid Paths](grid_paths_analysis) - Count paths in grid
- [Minimal Grid Path](minimal_grid_path_analysis) - Find minimum cost path
- [Rectangle Cutting](rectangle_cutting_analysis) - Minimize cuts

### Sequence Problems
- [Array Description](array_description_analysis) - Valid array constructions
- [Increasing Subsequence](increasing_subsequence_analysis) - Longest increasing subsequence
- [Longest Common Subsequence](longest_common_subsequence_analysis) - LCS problem
- [Edit Distance](edit_distance_analysis) - String transformation

### Optimization Problems
- [Book Shop](book_shop_analysis) - Knapsack problem
- [Money Sums](money_sums_analysis) - Generate possible sums
- [Counting Towers](counting_towers_analysis) - Count tower arrangements
- [Removal Game](removal_game_analysis) - Game theory with DP
- [Two Sets II](two_sets_ii_analysis) - Count equal sum partitions

## Detailed Examples and Patterns

### Classic DP Problems with Solutions

#### 1. Fibonacci Sequence
```python
# Naive recursive approach - O(2^n)
def fibonacci_naive(n):
 if n <= 1:
  return n
 return fibonacci_naive(n-1) + fibonacci_naive(n-2)

# Memoized approach - O(n)
def fibonacci_memo(n, memo={}):
 if n in memo:
  return memo[n]
 if n <= 1:
  return n
 memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
 return memo[n]

# Bottom-up approach - O(n) time, O(1) space
def fibonacci_dp(n):
 if n <= 1:
  return n
 a, b = 0, 1
 for i in range(2, n + 1):
  a, b = b, a + b
 return b
```

#### 2. Longest Common Subsequence (LCS)
```python
def lcs(text1, text2):
 m, n = len(text1), len(text2)
 dp = [[0] * (n + 1) for _ in range(m + 1)]
 
 for i in range(1, m + 1):
  for j in range(1, n + 1):
   if text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
   else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
 
 return dp[m][n]

# Space-optimized version
def lcs_optimized(text1, text2):
 if len(text1) < len(text2):
  text1, text2 = text2, text1
 
 prev = [0] * (len(text2) + 1)
 curr = [0] * (len(text2) + 1)
 
 for i in range(1, len(text1) + 1):
  for j in range(1, len(text2) + 1):
   if text1[i-1] == text2[j-1]:
    curr[j] = prev[j-1] + 1
   else:
    curr[j] = max(prev[j], curr[j-1])
  prev, curr = curr, prev
 
 return prev[len(text2)]
```

#### 3. Knapsack Problem
```python
# 0/1 Knapsack - O(nW) time, O(nW) space
def knapsack_01(weights, values, capacity):
 n = len(weights)
 dp = [[0] * (capacity + 1) for _ in range(n + 1)]
 
 for i in range(1, n + 1):
  for w in range(capacity + 1):
   if weights[i-1] <= w:
    dp[i][w] = max(dp[i-1][w], 
       dp[i-1][w-weights[i-1]] + values[i-1])
   else:
    dp[i][w] = dp[i-1][w]
 
 return dp[n][capacity]

# Space-optimized version - O(nW) time, O(W) space
def knapsack_01_optimized(weights, values, capacity):
 dp = [0] * (capacity + 1)
 
 for i in range(len(weights)):
  for w in range(capacity, weights[i] - 1, -1):
   dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
 
 return dp[capacity]
```

### Advanced DP Patterns

#### 1. Digit DP
```python
def count_numbers_with_digit_sum(n, target_sum):
 def digit_dp(pos, tight, sum_so_far, memo):
  if pos == len(n):
   return 1 if sum_so_far == target_sum else 0
  
  if (pos, tight, sum_so_far) in memo:
   return memo[(pos, tight, sum_so_far)]
  
  limit = int(n[pos]) if tight else 9
  result = 0
  
  for digit in range(limit + 1):
   new_tight = tight and (digit == limit)
   new_sum = sum_so_far + digit
   result += digit_dp(pos + 1, new_tight, new_sum, memo)
  
  memo[(pos, tight, sum_so_far)] = result
  return result
 
 return digit_dp(0, True, 0, {})
```

#### 2. Tree DP
```python
def tree_diameter(tree):
 def dfs(node, parent):
  max_depth1 = max_depth2 = 0
  diameter = 0
  
  for child in tree[node]:
   if child != parent:
    child_depth, child_diameter = dfs(child, node)
    diameter = max(diameter, child_diameter)
    
    if child_depth > max_depth1:
     max_depth2 = max_depth1
     max_depth1 = child_depth
    elif child_depth > max_depth2:
     max_depth2 = child_depth
  
  diameter = max(diameter, max_depth1 + max_depth2)
  return max_depth1 + 1, diameter
 
 return dfs(0, -1)[1]
```

#### 3. Bitmask DP (TSP)
```python
def tsp_bitmask(distances):
 n = len(distances)
 dp = [[float('inf')] * (1 << n) for _ in range(n)]
 dp[0][1] = 0  # Start at city 0
 
 for mask in range(1 << n):
  for u in range(n):
   if not (mask & (1 << u)):
    continue
   for v in range(n):
    if mask & (1 << v):
     continue
    new_mask = mask | (1 << v)
    dp[v][new_mask] = min(dp[v][new_mask], 
         dp[u][mask] + distances[u][v])
 
 # Return to starting city
 result = float('inf')
 for u in range(1, n):
  result = min(result, dp[u][(1 << n) - 1] + distances[u][0])
 
 return result
```

### Practical Implementation Tips

#### 1. State Design Principles
- **Minimal State**: Include only information that affects the answer
- **State Compression**: Use bitmasks for small sets, coordinate compression for large ranges
- **State Ordering**: Order states to minimize transition complexity

#### 2. Transition Optimization
- **Precomputation**: Calculate common values once
- **Lazy Evaluation**: Compute transitions only when needed
- **Batch Processing**: Process multiple transitions together

#### 3. Memory Management
- **Rolling Arrays**: Use when only previous states needed
- **Memory Pool**: Reuse memory for similar problems
- **Lazy Allocation**: Allocate memory on demand

### Common DP Patterns and When to Use Them

#### 1. Linear DP
- **When**: Single parameter progression (Fibonacci, LIS, LCS)
- **State**: `dp[i]` = solution for first i elements
- **Transition**: `dp[i] = f(dp[i-1], dp[i-2], ..., dp[0])`

#### 2. 2D DP
- **When**: Two independent parameters (LCS, Edit Distance, Knapsack)
- **State**: `dp[i][j]` = solution for parameters i and j
- **Transition**: `dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`

#### 3. Interval DP
- **When**: Problems on intervals (Matrix Chain Multiplication, Palindrome Partitioning)
- **State**: `dp[i][j]` = solution for interval [i,j]
- **Transition**: Try all possible ways to split the interval

#### 4. Tree DP
- **When**: Problems on trees (Tree Diameter, Tree Coloring, Tree Matching)
- **State**: `dp[node][state]` = solution for subtree rooted at node
- **Transition**: Combine results from children nodes

#### 5. Bitmask DP
- **When**: Subset selection problems (TSP, Subset Sum, Assignment)
- **State**: `dp[mask]` = solution for subset represented by mask
- **Transition**: Add/remove elements from subset

### Advanced Optimization Techniques

#### 1. Convex Hull Trick
```python
# For DP with form: dp[i] = min(dp[j] + a[i] * b[j] + c[j])
class ConvexHullTrick:
 def __init__(self):
  self.lines = []
 
 def add_line(self, m, b):
  while len(self.lines) >= 2:
   x1, y1 = self.lines[-2]
   x2, y2 = self.lines[-1]
   x3, y3 = m, b
   
   if (y2 - y1) * (x3 - x2) >= (y3 - y2) * (x2 - x1):
    self.lines.pop()
   else:
    break
  
  self.lines.append((m, b))
 
 def query(self, x):
  while len(self.lines) >= 2:
   if self.lines[0][0] * x + self.lines[0][1] <= \
   self.lines[1][0] * x + self.lines[1][1]:
    self.lines.pop(0)
   else:
    break
  
  return self.lines[0][0] * x + self.lines[0][1]
```

#### 2. Divide and Conquer Optimization
```python
# For DP with form: dp[i][j] = min(dp[i-1][k] + cost(k, j))
def divide_conquer_dp(n, m, cost_func):
 dp = [[float('inf')] * m for _ in range(n)]
 
 # Base case
 for j in range(m):
  dp[0][j] = cost_func(0, j)
 
 def solve(l, r, opt_l, opt_r, i):
  if l > r:
   return
  
  mid = (l + r) // 2
  best_k = opt_l
  
  for k in range(opt_l, min(mid, opt_r) + 1):
   if dp[i-1][k] + cost_func(k, mid) < dp[i][mid]:
    dp[i][mid] = dp[i-1][k] + cost_func(k, mid)
    best_k = k
  
  solve(l, mid - 1, opt_l, best_k, i)
  solve(mid + 1, r, best_k, opt_r, i)
 
 for i in range(1, n):
  solve(0, m - 1, 0, m - 1, i)
 
 return dp[n-1][m-1]
```

### Debugging and Testing DP Solutions

#### 1. Common Debugging Techniques
- **State Validation**: Check if states are valid
- **Transition Verification**: Verify transition logic
- **Base Case Testing**: Test edge cases and base cases
- **Memory Usage**: Monitor memory consumption

#### 2. Testing Strategies
- **Small Test Cases**: Start with small examples
- **Edge Cases**: Test boundary conditions
- **Stress Testing**: Test with large inputs
- **Comparison**: Compare with brute force solution

## Tips for Success

1. **Define States Clearly**: Key to correct solutions
2. **Draw State Diagrams**: Visualize transitions
3. **Start Simple**: Begin with recursive solution
4. **Optimize Later**: First make it work, then improve
5. **Practice Patterns**: Learn common DP patterns
6. **Understand Complexity**: Know when DP is appropriate

## Common Pitfalls to Avoid

1. **Wrong State Definition**: Missing important information
2. **Incorrect Transitions**: Invalid state updates
3. **Memory Limit**: Too many states
4. **Time Limit**: Inefficient transitions
5. **Off-by-One Errors**: Indexing mistakes
6. **Integer Overflow**: Large number handling

## Advanced Topics

### State Space Design
- **Minimal States**: Including only necessary information
- **State Compression**: Using bits to save memory
- **State Transitions**: Efficient updates
- **Memory Management**: Space optimization

### Optimization Techniques
- **Rolling Arrays**: Space optimization
- **State Compression**: Bit manipulation
- **Prefix Optimization**: Faster queries
- **Transition Optimization**: Faster updates

### Special Cases
- **Empty States**: Handling edge cases
- **Invalid States**: Detecting impossibility
- **Overflow**: Handling large numbers
- **Modular Arithmetic**: Handling remainders

## 📚 **Additional Learning Resources**

### **LeetCode Pattern Integration**
For interview preparation and pattern recognition, complement your CSES learning with these LeetCode resources:

- **[Awesome LeetCode Resources](https://github.com/ashishps1/awesome-leetcode-resources)** - Comprehensive collection of LeetCode patterns, templates, and curated problem lists
- **[20 DP Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Essential dynamic programming patterns and techniques
- **[DP Pattern Templates](https://github.com/ashishps1/awesome-leetcode-resources#-must-read-leetcode-articles)** - Specific dynamic programming templates and optimization strategies

### **Related LeetCode Problems**
Practice these LeetCode problems to reinforce dynamic programming concepts:

- **1D DP Pattern**: [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/), [House Robber](https://leetcode.com/problems/house-robber/), [Coin Change](https://leetcode.com/problems/coin-change/)
- **2D DP Pattern**: [Unique Paths](https://leetcode.com/problems/unique-paths/), [Edit Distance](https://leetcode.com/problems/edit-distance/), [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)
- **Interval DP Pattern**: [Matrix Chain Multiplication](https://leetcode.com/problems/minimum-score-triangulation-of-polygon/), [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)
- **Tree DP Pattern**: [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/), [House Robber III](https://leetcode.com/problems/house-robber-iii/)

---

Ready to start? Begin with [Dice Combinations](dice_combinations_analysis) and work your way through the problems in order of difficulty!