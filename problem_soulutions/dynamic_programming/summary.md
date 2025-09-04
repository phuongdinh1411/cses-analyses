---
layout: simple
title: "Dynamic Programming Summary"
permalink: /problem_soulutions/dynamic_programming/summary
---

# Dynamic Programming

Welcome to the Dynamic Programming section! This category covers techniques for solving complex problems by breaking them down into simpler subproblems.

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

## Learning Path

### For Beginners (Start Here)
1. Start with **Dice Combinations** for basic counting
2. Move to **Minimizing Coins** for optimization
3. Try **Grid Paths** for 2D DP
4. Learn knapsack with **Book Shop**

### Intermediate Level
1. Master sequence problems with **Increasing Subsequence**
2. Practice string DP with **Edit Distance**
3. Explore optimization with **Rectangle Cutting**
4. Study game theory with **Removal Game**

### Advanced Level
1. Challenge yourself with **Counting Towers**
2. Master advanced counting with **Two Sets II**
3. Solve complex array problems with **Array Description**
4. Tackle string problems with **Longest Common Subsequence**

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

## Tips for Success

1. **Define States Clearly**: Key to correct solutions
2. **Draw State Diagrams**: Visualize transitions
3. **Start Simple**: Begin with recursive solution
4. **Optimize Later**: First make it work, then improve

## Common Pitfalls to Avoid

1. **Wrong State Definition**: Missing important information
2. **Incorrect Transitions**: Invalid state updates
3. **Memory Limit**: Too many states
4. **Time Limit**: Inefficient transitions

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

---

Ready to start? Begin with [Dice Combinations](dice_combinations_analysis) and work your way through the problems in order of difficulty!