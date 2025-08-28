---
layout: simple
title: "Book Shop"permalink: /problem_soulutions/dynamic_programming/book_shop_analysis
---


# Book Shop

## Problem Statement
You are in a book shop which sells n different books. You know the price and number of pages of each book.

You have decided that the total price of your books will be at most x. What is the maximum number of pages you can buy? You can buy each book at most once.

### Input
The first input line contains two integers n and x: the number of books and the maximum total price.
The second line contains n integers h1,h2,…,hn: the price of each book.
The third line contains n integers s1,s2,…,sn: the number of pages of each book.

### Output
Print one integer: the maximum number of pages.

### Constraints
- 1 ≤ n ≤ 1000
- 1 ≤ x ≤ 10^5
- 1 ≤ hi,si ≤ 1000

### Example
```
Input:
4 10
4 8 5 3
5 12 8 1

Output:
13
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(2^n)
**Description**: Try all possible combinations of books recursively.

```python
def book_shop_brute_force(n, x, prices, pages):
    def max_pages(index, remaining_money):
        if index == n:
            return 0
        if remaining_money < 0:
            return float('-inf')
        
        # Don't buy current book
        not_buy = max_pages(index + 1, remaining_money)
        
        # Buy current book
        buy = float('-inf')
        if remaining_money >= prices[index]:
            buy = pages[index] + max_pages(index + 1, remaining_money - prices[index])
        
        return max(not_buy, buy)
    
    return max_pages(0, x)
```

**Why this is inefficient**: We're trying all possible combinations of books, which leads to exponential complexity. For each book, we have 2 choices (buy or don't buy), leading to O(2^n) complexity.

### Improvement 1: Recursive with Memoization - O(n*x)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def book_shop_memoization(n, x, prices, pages):
    memo = {}
    
    def max_pages(index, remaining_money):
        if (index, remaining_money) in memo:
            return memo[(index, remaining_money)]
        
        if index == n:
            return 0
        if remaining_money < 0:
            return float('-inf')
        
        # Don't buy current book
        not_buy = max_pages(index + 1, remaining_money)
        
        # Buy current book
        buy = float('-inf')
        if remaining_money >= prices[index]:
            buy = pages[index] + max_pages(index + 1, remaining_money - prices[index])
        
        memo[(index, remaining_money)] = max(not_buy, buy)
        return memo[(index, remaining_money)]
    
    return max_pages(0, x)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n*x) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n*x)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def book_shop_dp(n, x, prices, pages):
    # dp[i][j] = maximum pages using first i books with budget j
    dp = [[0] * (x + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(x + 1):
            # Don't buy current book
            dp[i][j] = dp[i-1][j]
            
            # Buy current book if we have enough money
            if j >= prices[i-1]:
                dp[i][j] = max(dp[i][j], dp[i-1][j - prices[i-1]] + pages[i-1])
    
    return dp[n][x]
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each book and budget, we decide whether to buy the book or not.

### Alternative: Space-Optimized DP - O(n*x)
**Description**: Use a space-optimized DP approach with only one row.

```python
def book_shop_optimized(n, x, prices, pages):
    # dp[j] = maximum pages with budget j
    dp = [0] * (x + 1)
    
    for i in range(n):
        # Process from right to left to avoid using the same book twice
        for j in range(x, prices[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    return dp[x]
```

**Why this works**: We can optimize space by using only one row and processing from right to left to avoid using the same book multiple times.

## Final Optimal Solution

```python
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
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n) | O(n) | Try all combinations |
| Memoization | O(n*x) | O(n*x) | Store subproblem results |
| Bottom-Up DP | O(n*x) | O(n*x) | Build solution iteratively |
| Space-Optimized DP | O(n*x) | O(x) | Use single row optimization |

## Key Insights for Other Problems

### 1. **0/1 Knapsack Problem**
**Principle**: This is a classic 0/1 knapsack problem where each item can be used at most once.
**Applicable to**:
- Knapsack problems
- Resource allocation
- Optimization problems
- Dynamic programming

**Example Problems**:
- 0/1 knapsack
- Resource allocation
- Optimization problems
- Dynamic programming

### 2. **Space Optimization in DP**
**Principle**: Use space optimization techniques to reduce memory usage in DP problems.
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

### 3. **State Definition for Knapsack**
**Principle**: Define states that capture the essential information for knapsack problems.
**Applicable to**:
- Dynamic programming
- Knapsack problems
- State machine problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- Knapsack problems
- State machine problems
- Algorithm design

### 4. **Processing Order in DP**
**Principle**: Process items in a specific order to avoid using the same item multiple times.
**Applicable to**:
- Dynamic programming
- Knapsack problems
- Algorithm design
- Optimization problems

**Example Problems**:
- Dynamic programming
- Knapsack problems
- Algorithm design
- Optimization problems

## Notable Techniques

### 1. **Knapsack DP Pattern**
```python
# Define DP state for knapsack
dp = [0] * (capacity + 1)
for item in items:
    for j in range(capacity, item.weight - 1, -1):
        dp[j] = max(dp[j], dp[j - item.weight] + item.value)
```

### 2. **Space Optimization Pattern**
```python
# Use single row for space optimization
dp = [0] * (capacity + 1)
for i in range(n):
    for j in range(capacity, weights[i] - 1, -1):
        dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
```

### 3. **State Transition Pattern**
```python
# Define state transitions for knapsack
dp[i][j] = max(dp[i-1][j], dp[i-1][j-weight] + value)
```

## Edge Cases to Remember

1. **x = 0**: Return 0 (no money to spend)
2. **n = 0**: Return 0 (no books available)
3. **All books too expensive**: Return 0
4. **Large x**: Use efficient DP approach
5. **Negative values**: Handle properly

## Problem-Solving Framework

1. **Identify knapsack nature**: This is a 0/1 knapsack problem
2. **Define state**: dp[j] = maximum pages with budget j
3. **Define transitions**: dp[j] = max(dp[j], dp[j-price] + pages)
4. **Handle base case**: dp[0] = 0
5. **Use space optimization**: Process from right to left

---

*This analysis shows how to efficiently solve 0/1 knapsack problems using dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Unbounded Knapsack (Multiple Copies)**
**Problem**: You can buy multiple copies of the same book.
```python
def unbounded_book_shop(n, x, prices, pages):
    # dp[j] = maximum pages with budget j (can buy multiple copies)
    dp = [0] * (x + 1)
    
    for i in range(n):
        # Process from left to right to allow multiple copies
        for j in range(prices[i], x + 1):
            dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    return dp[x]
```

#### **Variation 2: Book Shop with Categories**
**Problem**: Books belong to categories, and you can buy at most k books from each category.
```python
def categorized_book_shop(n, x, prices, pages, categories, max_per_category):
    # dp[j][cat] = maximum pages with budget j and category state cat
    dp = [[0] * (max_per_category + 1) for _ in range(x + 1)]
    
    for i in range(n):
        cat = categories[i]
        # Process from right to left to avoid using same book twice
        for j in range(x, prices[i] - 1, -1):
            for k in range(max_per_category, 0, -1):
                dp[j][k] = max(dp[j][k], dp[j - prices[i]][k - 1] + pages[i])
    
    return max(dp[x])
```

#### **Variation 3: Book Shop with Discounts**
**Problem**: Buying multiple books gives discounts based on quantity.
```python
def book_shop_with_discounts(n, x, prices, pages, discount_table):
    # discount_table[k] = discount percentage for buying k books
    dp = [[0] * (n + 1) for _ in range(x + 1)]
    
    for i in range(n):
        for j in range(x, prices[i] - 1, -1):
            for k in range(n, 0, -1):
                discount = discount_table.get(k, 0) / 100
                discounted_price = int(prices[i] * (1 - discount))
                if j >= discounted_price:
                    dp[j][k] = max(dp[j][k], dp[j - discounted_price][k - 1] + pages[i])
    
    return max(dp[x])
```

#### **Variation 4: Book Shop with Time Constraints**
**Problem**: Each book takes time to read, and you have limited time.
```python
def book_shop_with_time(n, x, prices, pages, reading_times, max_time):
    # dp[j][t] = maximum pages with budget j and time t
    dp = [[0] * (max_time + 1) for _ in range(x + 1)]
    
    for i in range(n):
        for j in range(x, prices[i] - 1, -1):
            for t in range(max_time, reading_times[i] - 1, -1):
                dp[j][t] = max(dp[j][t], dp[j - prices[i]][t - reading_times[i]] + pages[i])
    
    return max(dp[x])
```

#### **Variation 5: Book Shop with Preferences**
**Problem**: Each book has a preference score, maximize total preference.
```python
def book_shop_with_preferences(n, x, prices, pages, preferences):
    # dp[j] = maximum preference with budget j
    dp = [0] * (x + 1)
    
    for i in range(n):
        for j in range(x, prices[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - prices[i]] + preferences[i])
    
    return dp[x]
```

### 🔗 **Related Problems & Concepts**

#### **1. Knapsack Problems**
- **0/1 Knapsack**: Each item can be used at most once
- **Unbounded Knapsack**: Unlimited copies of each item
- **Fractional Knapsack**: Can take fractions of items
- **Multiple Knapsack**: Multiple knapsacks with constraints

#### **2. Dynamic Programming Patterns**
- **1D DP**: Single state variable (budget)
- **2D DP**: Two state variables (budget, additional constraint)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Optimization Problems**
- **Resource Allocation**: Optimal use of limited resources
- **Portfolio Optimization**: Optimal investment selection
- **Scheduling**: Optimal task arrangement
- **Inventory Management**: Optimal stock levels

#### **4. Algorithmic Techniques**
- **Greedy Algorithms**: Heuristic optimization
- **Branch and Bound**: Exact optimization
- **Dynamic Programming**: Optimal substructure
- **Linear Programming**: Mathematical optimization

#### **5. Mathematical Concepts**
- **Combinatorics**: Count valid combinations
- **Optimization Theory**: Find optimal solutions
- **Linear Algebra**: Matrix operations
- **Probability Theory**: Stochastic optimization

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    prices = list(map(int, input().split()))
    pages = list(map(int, input().split()))
    result = book_shop_dp(n, x, prices, pages)
    print(result)
```

#### **2. Range Queries on Book Shop Results**
```python
def range_book_shop_queries(n, x, prices, pages, queries):
    # Precompute for all budgets up to x
    dp = [0] * (x + 1)
    
    for i in range(n):
        for j in range(x, prices[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    # Answer queries
    for l, r in queries:
        max_pages = max(dp[i] for i in range(l, r + 1))
        print(max_pages)
```

#### **3. Interactive Book Shop Problems**
```python
def interactive_book_shop_game():
    n, x = map(int, input("Enter n and x: ").split())
    prices = list(map(int, input("Enter prices: ").split()))
    pages = list(map(int, input("Enter pages: ").split()))
    
    print(f"Books: {list(zip(prices, pages))}")
    print(f"Budget: {x}")
    
    player_guess = int(input("Enter maximum pages: "))
    actual_pages = book_shop_dp(n, x, prices, pages)
    
    if player_guess == actual_pages:
        print("Correct!")
    else:
        print(f"Wrong! Maximum pages is {actual_pages}")
```

### 🧮 **Mathematical Extensions**

#### **1. Optimization Theory**
- **Linear Programming**: Mathematical optimization
- **Integer Programming**: Discrete optimization
- **Convex Optimization**: Convex function optimization
- **Multi-objective Optimization**: Multiple goals

#### **2. Advanced DP Techniques**
- **Digit DP**: Count solutions with specific properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split problems into subproblems
- **Persistent Data Structures**: Maintain solution history

#### **3. Combinatorial Analysis**
- **Subset Sum**: Find subsets with given sum
- **Partition Problems**: Divide set into parts
- **Generating Functions**: Represent solutions algebraically
- **Asymptotic Analysis**: Behavior for large inputs

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Greedy Algorithms**: Heuristic optimization
- **Branch and Bound**: Exact optimization
- **Dynamic Programming**: Optimal substructure
- **Linear Programming**: Mathematical optimization

#### **2. Mathematical Concepts**
- **Optimization Theory**: Finding optimal solutions
- **Combinatorics**: Counting principles and techniques
- **Linear Algebra**: Matrix operations and transformations
- **Probability Theory**: Stochastic processes

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Algorithm Design**: Creating efficient solutions

---

*This analysis demonstrates the power of dynamic programming for knapsack problems and shows various extensions and applications.* 