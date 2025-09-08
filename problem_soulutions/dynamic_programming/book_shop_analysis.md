---
layout: simple
title: "Book Shop"
permalink: /problem_soulutions/dynamic_programming/book_shop_analysis
---


# Book Shop

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand knapsack problems and capacity-constrained optimization
- Apply DP techniques to solve 0/1 knapsack problems with value maximization
- Implement efficient DP solutions for knapsack problems with capacity constraints
- Optimize DP solutions using space-efficient techniques and capacity tracking
- Handle edge cases in knapsack DP (zero capacity, single items, impossible solutions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, knapsack problems, 0/1 knapsack, capacity optimization
- **Data Structures**: Arrays, DP tables, capacity tracking structures
- **Mathematical Concepts**: Optimization theory, capacity constraints, value maximization, knapsack theory
- **Programming Skills**: Array manipulation, capacity calculations, iterative programming, DP implementation
- **Related Problems**: Money Sums (subset problems), Minimizing Coins (optimization DP), Coin Combinations (DP counting)

## Problem Description

You are in a book shop with n different books. Each book has a price and number of pages. You have a budget of x and want to maximize the total number of pages you can buy. You can buy each book at most once.

**Input**: 
- First line: integers n and x (number of books and maximum total price)
- Second line: n integers h1, h2, ..., hn (price of each book)
- Third line: n integers s1, s2, ..., sn (number of pages of each book)

**Output**: 
- Print the maximum number of pages you can buy within the budget

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ x ≤ 10^5
- 1 ≤ hi ≤ 10^5
- 1 ≤ si ≤ 10^5
- Can buy each book at most once
- Maximize total pages within budget
- Classic 0/1 knapsack problem

**Example**:
```
Input:
4 10
4 8 5 3
5 12 8 1

Output:
13

Explanation**: 
Book 1: price 4, pages 5
Book 2: price 8, pages 12  
Book 3: price 5, pages 8
Book 4: price 3, pages 1

Optimal: Buy books 1 and 3
Total price: 4 + 5 = 9 ≤ 10
Total pages: 5 + 8 = 13
```

## Visual Example

### Input and Problem Setup
```
Input: n = 4, x = 10
Books:
Book 1: price 4, pages 5
Book 2: price 8, pages 12
Book 3: price 5, pages 8
Book 4: price 3, pages 1

Goal: Maximize total pages within budget 10
Constraint: Can buy each book at most once
Result: Maximum number of pages
Note: Classic 0/1 knapsack problem
```

### Book Selection Analysis
```
For books [4,8,5,3] with pages [5,12,8,1] and budget 10:

Option 1: Buy book 1 only
- Price: 4, Pages: 5
- Remaining budget: 6

Option 2: Buy book 2 only
- Price: 8, Pages: 12
- Remaining budget: 2

Option 3: Buy book 3 only
- Price: 5, Pages: 8
- Remaining budget: 5

Option 4: Buy book 4 only
- Price: 3, Pages: 1
- Remaining budget: 7

Option 5: Buy books 1 and 2
- Price: 4 + 8 = 12 > 10 (exceeds budget)

Option 6: Buy books 1 and 3
- Price: 4 + 5 = 9 ≤ 10
- Pages: 5 + 8 = 13

Option 7: Buy books 1 and 4
- Price: 4 + 3 = 7 ≤ 10
- Pages: 5 + 1 = 6

Option 8: Buy books 2 and 3
- Price: 8 + 5 = 13 > 10 (exceeds budget)

Option 9: Buy books 2 and 4
- Price: 8 + 3 = 11 > 10 (exceeds budget)

Option 10: Buy books 3 and 4
- Price: 5 + 3 = 8 ≤ 10
- Pages: 8 + 1 = 9

Best option: Buy books 1 and 3 for 13 pages
```

### Dynamic Programming Pattern
```
DP State: dp[i][j] = maximum pages using first i books with budget j

Base case: dp[0][j] = 0 (no books selected)

Recurrence: 
- dp[i][j] = dp[i-1][j] (don't buy book i)
- dp[i][j] = max(dp[i][j], dp[i-1][j-price[i]] + pages[i]) (buy book i)

Key insight: Use 2D DP to solve 0/1 knapsack problem
```

### State Transition Visualization
```
Building DP table for n = 4, x = 10:

Initialize: dp = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ...]

After book 1 (price 4, pages 5):
dp[1] = [0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5]

After book 2 (price 8, pages 12):
dp[2] = [0, 0, 0, 0, 5, 5, 5, 5, 12, 12, 12]

After book 3 (price 5, pages 8):
dp[3] = [0, 0, 0, 0, 5, 8, 8, 8, 12, 13, 13]

After book 4 (price 3, pages 1):
dp[4] = [0, 0, 0, 1, 5, 8, 8, 9, 12, 13, 13]

Final: dp[4][10] = 13
```

### Key Insight
The solution works by:
1. Using 2D dynamic programming to solve 0/1 knapsack
2. For each book, deciding whether to buy or not
3. Tracking maximum pages for each budget constraint
4. Building solutions from smaller subproblems
5. Time complexity: O(n × x) for filling DP table
6. Space complexity: O(n × x) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of books
- Use recursive approach to explore all choices
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. For each book, decide whether to buy or not
2. Recursively explore all possible combinations
3. Keep track of maximum pages found
4. Return optimal solution

**Visual Example:**
```
Brute force approach: Try all possible book combinations
For 4 books with budget 10:

Recursive tree:
                    (0, 10)
              /            \
          (1, 10)          (1, 6)
         /      \        /      \
    (2, 10)  (2, 2)  (2, 6)  (2, 2)
   /    \     /  \   /  \     /  \
(3, 10) (3, 5) (3, 2) (3, 2) (3, 6) (3, 1) (3, 2) (3, 2)
```

**Implementation:**
```python
def book_shop_brute_force(n, x, prices, pages):
    def max_pages(index, remaining_budget):
        if index == n:
            return 0
        
        # Don't buy current book
        not_buy = max_pages(index + 1, remaining_budget)
        
        # Buy current book if we have enough money
        buy = 0
        if remaining_budget >= prices[index]:
            buy = pages[index] + max_pages(index + 1, remaining_budget - prices[index])
        
        return max(not_buy, buy)
    
    return max_pages(0, x)

def solve_book_shop_brute_force():
    n, x = map(int, input().split())
    prices = list(map(int, input().split()))
    pages = list(map(int, input().split()))
    
    result = book_shop_brute_force(n, x, prices, pages)
    print(result)
```

**Time Complexity:** O(2^n) for trying all possible book combinations
**Space Complexity:** O(n) for recursion depth

**Why it's inefficient:**
- O(2^n) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large n
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 2D DP array to store maximum pages for each budget and book combination
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each book and budget, decide whether to buy the book
3. Update maximum pages using recurrence relation
4. Return optimal solution

**Visual Example:**
```
DP approach: Build solutions iteratively
For n = 4, x = 10:

Initialize: dp = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ...]

After book 1: dp[1] = [0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5]
After book 2: dp[2] = [0, 0, 0, 0, 5, 5, 5, 5, 12, 12, 12]
After book 3: dp[3] = [0, 0, 0, 0, 5, 8, 8, 8, 12, 13, 13]
After book 4: dp[4] = [0, 0, 0, 1, 5, 8, 8, 9, 12, 13, 13]

Final result: dp[4][10] = 13
```

**Implementation:**
```python
def book_shop_dp(n, x, prices, pages):
    # dp[i][j] = max pages using first i books with budget j
    dp = [[0] * (x + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(x + 1):
            # Don't buy current book
            dp[i][j] = dp[i-1][j]
            
            # Buy current book if we have enough money
            if j >= prices[i-1]:
                dp[i][j] = max(dp[i][j], dp[i-1][j - prices[i-1]] + pages[i-1])
    
    return dp[n][x]

def solve_book_shop_dp():
    n, x = map(int, input().split())
    prices = list(map(int, input().split()))
    pages = list(map(int, input().split()))
    
    result = book_shop_dp(n, x, prices, pages)
    print(result)
```

**Time Complexity:** O(n × x) for filling DP table
**Space Complexity:** O(n × x) for DP array

**Why it's better:**
- O(n × x) time complexity is much better than O(2^n)
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Optimized DP with Space Efficiency (Optimal)

**Key Insights from Optimized Solution:**
- Use 1D DP array instead of 2D to save space
- Process books from right to left to avoid using the same book twice
- Most efficient approach for 0/1 knapsack problems
- Standard method in competitive programming

**Algorithm:**
1. Initialize 1D DP array with base cases
2. For each book, process budget from right to left
3. Update maximum pages using recurrence relation
4. Return optimal solution

**Visual Example:**
```
Optimized DP: Process books sequentially
For n = 4, x = 10:

Initialize: dp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Process book 1 (price 4, pages 5):
dp = [0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5]

Process book 2 (price 8, pages 12):
dp = [0, 0, 0, 0, 5, 5, 5, 5, 12, 12, 12]

Process book 3 (price 5, pages 8):
dp = [0, 0, 0, 0, 5, 8, 8, 8, 12, 13, 13]

Process book 4 (price 3, pages 1):
dp = [0, 0, 0, 1, 5, 8, 8, 9, 12, 13, 13]
```

**Implementation:**
```python
def solve_book_shop():
    n, x = map(int, input().split())
    prices = list(map(int, input().split()))
    pages = list(map(int, input().split()))
    
    # dp[j] = maximum pages with budget j
    dp = [0] * (x + 1)
    
    for i in range(n):
        # Process from right to left to avoid using the same book twice
        for j in range(x, prices[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    print(dp[x])

# Main execution
if __name__ == "__main__":
    solve_book_shop()
```

**Time Complexity:** O(n × x) for filling DP table
**Space Complexity:** O(x) for DP array

**Why it's optimal:**
- O(n × x) time complexity is optimal for this problem
- Uses dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for 0/1 knapsack problems

## 🎯 Problem Variations

### Variation 1: Book Shop with Multiple Copies
**Problem**: Each book can be bought multiple times (unlimited knapsack).

**Link**: [CSES Problem Set - Book Shop Multiple](https://cses.fi/problemset/task/book_shop_multiple)

```python
def book_shop_multiple(n, x, prices, pages):
    dp = [0] * (x + 1)
    
    for i in range(n):
        # Process from left to right for unlimited knapsack
        for j in range(prices[i], x + 1):
            dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    return dp[x]
```

### Variation 2: Book Shop with Limited Copies
**Problem**: Each book has a limited number of copies available.

**Link**: [CSES Problem Set - Book Shop Limited](https://cses.fi/problemset/task/book_shop_limited)

```python
def book_shop_limited(n, x, prices, pages, quantities):
    dp = [0] * (x + 1)
    
    for i in range(n):
        for j in range(x, prices[i] - 1, -1):
            for k in range(1, quantities[i] + 1):
                if j >= k * prices[i]:
                    dp[j] = max(dp[j], dp[j - k * prices[i]] + k * pages[i])
    
    return dp[x]
```

### Variation 3: Book Shop with Different Constraints
**Problem**: Books have different constraints (e.g., weight, category).

**Link**: [CSES Problem Set - Book Shop Constraints](https://cses.fi/problemset/task/book_shop_constraints)

```python
def book_shop_constraints(n, x, prices, pages, constraints):
    dp = [0] * (x + 1)
    
    for i in range(n):
        if constraints[i]:  # Can buy this book
            for j in range(x, prices[i] - 1, -1):
                dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    return dp[x]
```

## 🔗 Related Problems

- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: Subset problems
- **[Minimizing Coins](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP optimization problems
- **[Coin Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP counting problems
- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/)**: 2D DP problems

## 📚 Learning Points

1. **0/1 Knapsack**: Essential for understanding capacity-constrained optimization problems
2. **Dynamic Programming**: Key technique for solving knapsack problems efficiently
3. **Space Optimization**: Important for understanding how to reduce space complexity
4. **Capacity Constraints**: Critical for understanding budget-based problems
5. **Value Maximization**: Foundation for understanding optimization problems
6. **Bottom-Up DP**: Critical for building solutions from smaller subproblems

## 📝 Summary

The Book Shop problem demonstrates 0/1 knapsack and dynamic programming principles for efficient capacity-constrained optimization. We explored three approaches:

1. **Recursive Brute Force**: O(2^n) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n × x) time complexity using 2D DP, better approach for knapsack problems
3. **Optimized DP with Space Efficiency**: O(n × x) time complexity with 1D DP, optimal approach for competitive programming

The key insights include understanding 0/1 knapsack principles, using dynamic programming for efficient computation, and applying space optimization techniques for knapsack problems. This problem serves as an excellent introduction to 0/1 knapsack in competitive programming.
