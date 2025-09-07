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

**Problem**: You are in a book shop with n different books. Each book has a price and number of pages. You have a budget of x and want to maximize the total number of pages you can buy. You can buy each book at most once.

**Input**: 
- n, x: number of books and maximum total price
- h1, h2, ..., hn: price of each book
- s1, s2, ..., sn: number of pages of each book

**Output**: Maximum number of pages you can buy within the budget.

**Example**:
```
Input:
4 10
4 8 5 3
5 12 8 1

Output:
13

Explanation: 
We can buy books with prices [4, 5, 1] = 10 (within budget)
Total pages: 5 + 8 + 1 = 14

Or buy books with prices [4, 3, 3] = 10 (within budget)  
Total pages: 5 + 1 + 1 = 7

Actually, the optimal solution is:
Buy books with prices [4, 5, 1] = 10
Total pages: 5 + 8 + 1 = 14

Wait, let me recalculate:
Book 1: price 4, pages 5
Book 2: price 8, pages 12  
Book 3: price 5, pages 8
Book 4: price 3, pages 1

Optimal: Buy books 1 and 3
Total price: 4 + 5 = 9 ≤ 10
Total pages: 5 + 8 = 13
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Choose a subset of books to buy
- Maximize total pages within budget constraint
- Each book can be bought at most once
- This is a 0/1 knapsack problem

**Key Observations:**
- For each book, we have 2 choices: buy or don't buy
- We need to track remaining budget
- This is a classic dynamic programming problem
- Can use 2D DP table

### Step 2: Dynamic Programming Approach
**Idea**: Use 2D DP table to store maximum pages for each budget and book combination.

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
```

**Why this works:**
- Uses optimal substructure property
- Handles all cases correctly
- Efficient implementation
- O(n*x) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_book_shop():
    n, x = map(int, input().split())
    prices = list(map(int, input().split()))
    pages = list(map(int, input().split()))
    
    # dp[i][j] = max pages using first i books with budget j
    dp = [[0] * (x + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(x + 1):
            # Don't buy current book
            dp[i][j] = dp[i-1][j]
            
            # Buy current book if we have enough money
            if j >= prices[i-1]:
                dp[i][j] = max(dp[i][j], dp[i-1][j - prices[i-1]] + pages[i-1])
    
    print(dp[n][x])

# Main execution
if __name__ == "__main__":
    solve_book_shop()
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
        (4, 10, [4, 8, 5, 3], [5, 12, 8, 1], 13),
        (3, 5, [2, 3, 4], [3, 4, 5], 7),
        (2, 3, [1, 2], [2, 3], 5),
    ]
    
    for n, x, prices, pages, expected in test_cases:
        result = solve_test(n, x, prices, pages)
        print(f"n={n}, x={x}, prices={prices}, pages={pages}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}, x={x}"
        print("✓ Passed")
        print()

def solve_test(n, x, prices, pages):
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n*x) - we fill a 2D DP table
- **Space**: O(n*x) - we store the entire DP table

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes optimal book selection using optimal substructure
- **State Transition**: dp[i][j] = max(dp[i-1][j], dp[i-1][j-price[i-1]] + pages[i-1])
- **Base Case**: dp[0][j] = 0 for all j (no books selected)
- **Optimal Substructure**: Optimal solution can be built from smaller subproblems

## 🎨 Visual Example

### Input Example
```
n = 4, x = 10
Prices: [4, 8, 5, 3]
Pages:  [5, 12, 8, 1]
```

### All Possible Book Combinations
```
Books:
Book 1: Price 4, Pages 5
Book 2: Price 8, Pages 12
Book 3: Price 5, Pages 8
Book 4: Price 3, Pages 1

Budget: 10

All valid combinations:
1. Buy Book 1 only: Price = 4 ≤ 10, Pages = 5
2. Buy Book 2 only: Price = 8 ≤ 10, Pages = 12
3. Buy Book 3 only: Price = 5 ≤ 10, Pages = 8
4. Buy Book 4 only: Price = 3 ≤ 10, Pages = 1
5. Buy Books 1,3: Price = 4+5 = 9 ≤ 10, Pages = 5+8 = 13
6. Buy Books 1,4: Price = 4+3 = 7 ≤ 10, Pages = 5+1 = 6
7. Buy Books 2,4: Price = 8+3 = 11 > 10 (invalid)
8. Buy Books 3,4: Price = 5+3 = 8 ≤ 10, Pages = 8+1 = 9
9. Buy Books 1,3,4: Price = 4+5+3 = 12 > 10 (invalid)

Maximum pages: 13 (Books 1 and 3)
```

### DP State Representation
```
dp[i][j] = maximum pages using first i books with budget j

For books [4,8,5,3] with pages [5,12,8,1] and budget 10:

Base case: dp[0][j] = 0 for all j (no books selected)

dp[1][j] = maximum pages using only book 1 with budget j
- dp[1][0] = 0, dp[1][1] = 0, dp[1][2] = 0, dp[1][3] = 0
- dp[1][4] = 5, dp[1][5] = 5, ..., dp[1][10] = 5

dp[2][j] = maximum pages using books 1,2 with budget j
- dp[2][0] = 0, dp[2][1] = 0, dp[2][2] = 0, dp[2][3] = 0
- dp[2][4] = 5, dp[2][5] = 5, dp[2][6] = 5, dp[2][7] = 5
- dp[2][8] = max(5, 12) = 12, dp[2][9] = 12, dp[2][10] = 12

dp[3][j] = maximum pages using books 1,2,3 with budget j
- dp[3][0] = 0, dp[3][1] = 0, dp[3][2] = 0, dp[3][3] = 0
- dp[3][4] = 5, dp[3][5] = max(5, 8) = 8, dp[3][6] = 8
- dp[3][7] = 8, dp[3][8] = max(12, 8) = 12, dp[3][9] = max(12, 5+8) = 13
- dp[3][10] = max(12, 5+8) = 13

dp[4][j] = maximum pages using all books with budget j
- dp[4][0] = 0, dp[4][1] = 0, dp[4][2] = 0, dp[4][3] = max(0, 1) = 1
- dp[4][4] = max(5, 1) = 5, dp[4][5] = max(8, 1) = 8
- dp[4][6] = 8, dp[4][7] = max(8, 5+1) = 8, dp[4][8] = max(12, 8+1) = 12
- dp[4][9] = max(13, 8+1) = 13, dp[4][10] = max(13, 5+8+1) = 13
```

### DP Table Construction
```
Books: [4,8,5,3] (prices), [5,12,8,1] (pages)
Budget: 10

Step 1: Base case (no books)
dp[0][j] = 0 for all j

Step 2: Book 1 (price 4, pages 5)
dp[1][j] = 0 for j < 4, dp[1][j] = 5 for j ≥ 4

Step 3: Book 2 (price 8, pages 12)
dp[2][j] = dp[1][j] for j < 8
dp[2][8] = max(dp[1][8], dp[1][0] + 12) = max(5, 0 + 12) = 12
dp[2][9] = max(dp[1][9], dp[1][1] + 12) = max(5, 0 + 12) = 12
dp[2][10] = max(dp[1][10], dp[1][2] + 12) = max(5, 0 + 12) = 12

Step 4: Book 3 (price 5, pages 8)
dp[3][j] = dp[2][j] for j < 5
dp[3][5] = max(dp[2][5], dp[2][0] + 8) = max(5, 0 + 8) = 8
dp[3][6] = max(dp[2][6], dp[2][1] + 8) = max(5, 0 + 8) = 8
dp[3][7] = max(dp[2][7], dp[2][2] + 8) = max(5, 0 + 8) = 8
dp[3][8] = max(dp[2][8], dp[2][3] + 8) = max(12, 0 + 8) = 12
dp[3][9] = max(dp[2][9], dp[2][4] + 8) = max(12, 5 + 8) = 13
dp[3][10] = max(dp[2][10], dp[2][5] + 8) = max(12, 5 + 8) = 13

Step 5: Book 4 (price 3, pages 1)
dp[4][j] = dp[3][j] for j < 3
dp[4][3] = max(dp[3][3], dp[3][0] + 1) = max(0, 0 + 1) = 1
dp[4][4] = max(dp[3][4], dp[3][1] + 1) = max(5, 0 + 1) = 5
dp[4][5] = max(dp[3][5], dp[3][2] + 1) = max(8, 0 + 1) = 8
dp[4][6] = max(dp[3][6], dp[3][3] + 1) = max(8, 0 + 1) = 8
dp[4][7] = max(dp[3][7], dp[3][4] + 1) = max(8, 5 + 1) = 8
dp[4][8] = max(dp[3][8], dp[3][5] + 1) = max(12, 8 + 1) = 12
dp[4][9] = max(dp[3][9], dp[3][6] + 1) = max(13, 8 + 1) = 13
dp[4][10] = max(dp[3][10], dp[3][7] + 1) = max(13, 8 + 1) = 13

Final result: dp[4][10] = 13
```

### Visual DP Table
```
Books: [4,8,5,3] (prices), [5,12,8,1] (pages)
Budget: 10

DP Table (maximum pages):
     0  1  2  3  4  5  6  7  8  9 10
0:    0  0  0  0  0  0  0  0  0  0  0
1:    0  0  0  0  5  5  5  5  5  5  5
2:    0  0  0  0  5  5  5  5 12 12 12
3:    0  0  0  0  5  8  8  8 12 13 13
4:    0  0  0  1  5  8  8  8 12 13 13

Each cell shows maximum pages using first i books with budget j
```

### Optimal Selection Reconstruction
```
Starting from dp[4][10] = 13:
- Current: 4 books, budget 10, pages = 13
- Check: dp[3][10] = 13 (same as dp[4][10])
- Book 4 not selected, move to dp[3][10]

- Current: 3 books, budget 10, pages = 13
- Check: dp[2][10] = 12 (less than dp[3][10])
- Book 3 selected, move to dp[2][5]

- Current: 2 books, budget 5, pages = 8
- Check: dp[1][5] = 5 (less than dp[2][5])
- Book 2 not selected, move to dp[1][5]

- Current: 1 book, budget 5, pages = 5
- Check: dp[0][5] = 0 (less than dp[1][5])
- Book 1 selected, move to dp[0][1]

- Current: 0 books, budget 1, pages = 0

Selected books: Book 1 (price 4, pages 5) + Book 3 (price 5, pages 8)
Total price: 4 + 5 = 9 ≤ 10
Total pages: 5 + 8 = 13
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(2^n)       │ O(n)         │ Try all      │
│                 │              │              │ combinations │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Memoized        │ O(n*x)       │ O(n*x)       │ Cache        │
│ Recursion       │              │              │ results      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bottom-up DP    │ O(n*x)       │ O(n*x)       │ Build from   │
│                 │              │              │ base cases   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Space-optimized │ O(n*x)       │ O(x)         │ Use only     │
│ DP              │              │              │ current row  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Book Shop Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: n, x,    │
              │ prices, pages   │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize DP   │
              │ table           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Set base case:  │
              │ dp[0][j] = 0    │
              │ for all j       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For i = 1 to n: │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For j = 0 to x: │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ dp[i][j] =      │
              │ max(dp[i-1][j], │
              │ dp[i-1][j-price[i-1]] │
              │ + pages[i-1])   │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return dp[n][x] │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Dynamic Programming for Knapsack Problems**
- Choose optimal subset with constraints
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **2D DP Table**
- Use 2D table for item selection problems
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **0/1 Knapsack Pattern**
- Each item can be chosen at most once
- Important for understanding
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Unbounded Knapsack
**Problem**: You can buy each book multiple times.

```python
def unbounded_book_shop(n, x, prices, pages):
    # dp[j] = max pages with budget j
    dp = [0] * (x + 1)
    
    for j in range(1, x + 1):
        for i in range(n):
            if j >= prices[i]:
                dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    return dp[x]

# Example usage
result = unbounded_book_shop(4, 10, [4, 8, 5, 3], [5, 12, 8, 1])
print(f"Unbounded max pages: {result}")
```

### Variation 2: Fractional Knapsack
**Problem**: You can buy fractional parts of books.

```python
def fractional_book_shop(n, x, prices, pages):
    # Sort by pages per price ratio
    books = [(pages[i] / prices[i], prices[i], pages[i]) for i in range(n)]
    books.sort(reverse=True)
    
    total_pages = 0
    remaining_budget = x
    
    for ratio, price, pages in books:
        if remaining_budget >= price:
            total_pages += pages
            remaining_budget -= price
        else:
            # Buy fractional part
            fraction = remaining_budget / price
            total_pages += pages * fraction
            break
    
    return total_pages

# Example usage
result = fractional_book_shop(4, 10, [4, 8, 5, 3], [5, 12, 8, 1])
print(f"Fractional max pages: {result}")
```

### Variation 3: Multiple Constraints
**Problem**: Books have both price and weight constraints.

```python
def constrained_book_shop(n, x, w, prices, pages, weights):
    # dp[i][j][k] = max pages using first i books with budget j and weight k
    dp = [[[0] * (w + 1) for _ in range(x + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(x + 1):
            for k in range(w + 1):
                # Don't buy current book
                dp[i][j][k] = dp[i-1][j][k]
                
                # Buy current book if constraints are satisfied
                if j >= prices[i-1] and k >= weights[i-1]:
                    dp[i][j][k] = max(dp[i][j][k], 
                                    dp[i-1][j - prices[i-1]][k - weights[i-1]] + pages[i-1])
    
    return dp[n][x][w]

# Example usage
result = constrained_book_shop(4, 10, 5, [4, 8, 5, 3], [5, 12, 8, 1], [2, 3, 2, 1])
print(f"Constrained max pages: {result}")
```

### Variation 4: Book Shop with Discounts
**Problem**: Books have volume discounts.

```python
def discounted_book_shop(n, x, prices, pages, discounts):
    # dp[i][j] = max pages using first i books with budget j
    dp = [[0] * (x + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(x + 1):
            # Don't buy current book
            dp[i][j] = dp[i-1][j]
            
            # Buy current book with discount
            discounted_price = prices[i-1] * (1 - discounts[i-1])
            if j >= discounted_price:
                dp[i][j] = max(dp[i][j], dp[i-1][j - discounted_price] + pages[i-1])
    
    return dp[n][x]

# Example usage
discounts = [0.1, 0.2, 0.15, 0.05]  # 10%, 20%, 15%, 5% discounts
result = discounted_book_shop(4, 10, [4, 8, 5, 3], [5, 12, 8, 1], discounts)
print(f"Discounted max pages: {result}")
```

### Variation 5: Book Shop with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def optimized_book_shop(n, x, prices, pages):
    # Use 1D DP array to save space
    dp = [0] * (x + 1)
    
    for i in range(n):
        for j in range(x, prices[i] - 1, -1):  # Reverse order to avoid overcounting
            dp[j] = max(dp[j], dp[j - prices[i]] + pages[i])
    
    return dp[x]

# Example usage
result = optimized_book_shop(4, 10, [4, 8, 5, 3], [5, 12, 8, 1])
print(f"Optimized max pages: {result}")
```

## 🔗 Related Problems

- **[Coin Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar knapsack problems
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar subset problems
- **[Knapsack Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: General knapsack problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for knapsack problems
2. **2D DP Tables**: Important for item selection problems
3. **0/1 Knapsack**: Important for understanding constraints
4. **Space Optimization**: Important for performance improvement

---

**This is a great introduction to dynamic programming for knapsack problems!** 🎯
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