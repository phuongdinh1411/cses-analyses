---
layout: simple
title: "Book Shop - 0/1 Knapsack Problem"
permalink: /problem_soulutions/dynamic_programming/book_shop_analysis
difficulty: Medium
tags: [dp, knapsack, 0-1-knapsack, 2d-dp]
prerequisites: [coin_combinations_i]
cses_link: https://cses.fi/problemset/task/1158
---

# Book Shop

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Maximize pages with limited budget |
| Pattern | 0/1 Knapsack |
| Time Complexity | O(n * x) |
| Space Complexity | O(x) optimized, O(n * x) naive |
| Key Insight | Each book: take it or leave it |

## Learning Goals

By solving this problem, you will learn:
1. **0/1 Knapsack Pattern**: The fundamental "take or leave" decision framework
2. **2D to 1D DP Optimization**: How to reduce space from O(n * x) to O(x)
3. **Reverse Iteration**: Why iterating backwards is critical in 1D knapsack

## Problem Statement

You are in a book shop with `n` books. Each book has a price and number of pages. You have a budget of `x`. Maximize the total number of pages you can buy.

**Input:**
- Line 1: `n` (number of books), `x` (budget)
- Line 2: `h1, h2, ..., hn` (prices of each book)
- Line 3: `s1, s2, ..., sn` (pages of each book)

**Output:** Maximum total pages

**Constraints:**
- 1 <= n <= 1000
- 1 <= x <= 100000
- 1 <= price, pages <= 1000

### Example

```
Input:
4 10
4 8 5 3
5 12 8 1

Output:
13
```

**Explanation:**
- Book 1: price=4, pages=5
- Book 2: price=8, pages=12
- Book 3: price=5, pages=8
- Book 4: price=3, pages=1

Best choice: Buy Book 1 (price 4) + Book 3 (price 5) = cost 9, pages = 5 + 8 = 13

## Intuition

This is the classic **0/1 Knapsack** problem. For each book, you have exactly two choices:
1. **Take it**: Add its pages to your total, subtract its price from budget
2. **Leave it**: Skip this book, keep your budget unchanged

This "take or leave" pattern is the essence of 0/1 Knapsack. Unlike unbounded knapsack (Coin Combinations), you can only use each item once.

```
For each book i with price p and pages v:
    Choice 1: Skip book i -> pages = what we had before
    Choice 2: Take book i -> pages = (best with budget-p) + v

    Answer = max(Choice 1, Choice 2)
```

## DP State Definition (2D)

### State
`dp[i][j]` = maximum pages using the **first i books** with a budget of exactly **j**

### Transition
For book `i` with `price[i]` and `pages[i]`:

```
dp[i][j] = max(
    dp[i-1][j],                           # Skip book i
    dp[i-1][j-price[i]] + pages[i]        # Take book i (if affordable)
)
```

### Base Case
`dp[0][j] = 0` for all j (with 0 books, we get 0 pages)

### Answer
`dp[n][x]` = max pages using all n books with budget x

## Detailed Dry Run

Let's trace through with: n=3, x=6, prices=[2, 3, 4], pages=[3, 4, 5]

### 2D DP Table Construction

```
Initial: dp[0][j] = 0 for all j

Books: Book 1 (p=2, v=3), Book 2 (p=3, v=4), Book 3 (p=4, v=5)

After Book 1 (price=2, pages=3):
Budget:  0   1   2   3   4   5   6
dp[1]:   0   0   3   3   3   3   3
              ^---take book 1 at budget 2+

After Book 2 (price=3, pages=4):
Budget:  0   1   2   3   4   5   6
dp[2]:   0   0   3   4   4   7   7
                  ^---take book 2   ^---take both

After Book 3 (price=4, pages=5):
Budget:  0   1   2   3   4   5   6
dp[3]:   0   0   3   4   5   7   8
                      ^---book 3    ^---books 1+3

Final answer: dp[3][6] = 8 (Book 1 + Book 3)
```

### Step-by-Step for dp[3][6]

```
Budget = 6, considering Book 3 (price=4, pages=5):
- Skip: dp[2][6] = 7 (from books 1+2)
- Take: dp[2][6-4] + 5 = dp[2][2] + 5 = 3 + 5 = 8

max(7, 8) = 8

Selected: Book 1 (price 2, pages 3) + Book 3 (price 4, pages 5) = 8 pages
```

## Space Optimization: 2D to 1D

Key insight: `dp[i][j]` only depends on `dp[i-1][...]` (previous row).

We can use a single 1D array if we iterate **budget in reverse**.

### Why Reverse Iteration?

**Forward iteration (WRONG for 0/1):**
```python
for budget in range(price, x+1):  # LEFT to RIGHT
    dp[budget] = max(dp[budget], dp[budget-price] + pages)
```
Problem: When computing `dp[5]`, we might use an already-updated `dp[3]`, which means we used the same book twice!

**Reverse iteration (CORRECT):**
```python
for budget in range(x, price-1, -1):  # RIGHT to LEFT
    dp[budget] = max(dp[budget], dp[budget-price] + pages)
```
When computing `dp[5]`, `dp[3]` hasn't been updated yet, so it still represents the state before considering this book.

### Visual: Why Order Matters

```
Processing Book 1 (price=2, pages=3), budget x=6:

FORWARD (Wrong - uses book twice):
dp: [0, 0, 0, 0, 0, 0, 0]
j=2: dp[2] = max(0, dp[0]+3) = 3    -> [0,0,3,0,0,0,0]
j=3: dp[3] = max(0, dp[1]+3) = 3    -> [0,0,3,3,0,0,0]
j=4: dp[4] = max(0, dp[2]+3) = 6    -> [0,0,3,3,6,0,0]  BUG! Used book twice!

REVERSE (Correct - each book used once):
dp: [0, 0, 0, 0, 0, 0, 0]
j=6: dp[6] = max(0, dp[4]+3) = 3    -> [0,0,0,0,0,0,3]
j=5: dp[5] = max(0, dp[3]+3) = 3    -> [0,0,0,0,0,3,3]
j=4: dp[4] = max(0, dp[2]+3) = 3    -> [0,0,0,0,3,3,3]
j=3: dp[3] = max(0, dp[1]+3) = 3    -> [0,0,0,3,3,3,3]
j=2: dp[2] = max(0, dp[0]+3) = 3    -> [0,0,3,3,3,3,3]  Correct!
```

## Implementation

### Python - 2D Version (Clear but uses more memory)

```python
def book_shop_2d(n, x, prices, pages):
    """
    2D DP solution - easier to understand
    Time: O(n * x), Space: O(n * x)
    """
    # dp[i][j] = max pages using first i books with budget j
    dp = [[0] * (x + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        price = prices[i - 1]
        page = pages[i - 1]

        for j in range(x + 1):
            # Option 1: Skip this book
            dp[i][j] = dp[i - 1][j]

            # Option 2: Take this book (if affordable)
            if j >= price:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - price] + page)

    return dp[n][x]
```

### Python - 1D Version (Space Optimized)

```python
def book_shop_1d(n, x, prices, pages):
    """
    1D DP solution - space optimized
    Time: O(n * x), Space: O(x)
    """
    dp = [0] * (x + 1)

    for i in range(n):
        price = prices[i]
        page = pages[i]

        # CRITICAL: Iterate budget in REVERSE
        for j in range(x, price - 1, -1):
            dp[j] = max(dp[j], dp[j - price] + page)

    return dp[x]

# Read input and solve
def main():
    n, x = map(int, input().split())
    prices = list(map(int, input().split()))
    pages = list(map(int, input().split()))
    print(book_shop_1d(n, x, prices, pages))

if __name__ == "__main__":
    main()
```

### C++ - 2D Version

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, x;
    cin >> n >> x;

    vector<int> price(n), pages(n);
    for (int i = 0; i < n; i++) cin >> price[i];
    for (int i = 0; i < n; i++) cin >> pages[i];

    // dp[i][j] = max pages using first i books with budget j
    vector<vector<int>> dp(n + 1, vector<int>(x + 1, 0));

    for (int i = 1; i <= n; i++) {
        int p = price[i - 1];
        int v = pages[i - 1];

        for (int j = 0; j <= x; j++) {
            dp[i][j] = dp[i - 1][j];  // Skip
            if (j >= p) {
                dp[i][j] = max(dp[i][j], dp[i - 1][j - p] + v);  // Take
            }
        }
    }

    cout << dp[n][x] << "\n";
    return 0;
}
```

### C++ - 1D Version (Recommended)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, x;
    cin >> n >> x;

    vector<int> price(n), pages(n);
    for (int i = 0; i < n; i++) cin >> price[i];
    for (int i = 0; i < n; i++) cin >> pages[i];

    vector<int> dp(x + 1, 0);

    for (int i = 0; i < n; i++) {
        // CRITICAL: Iterate budget in REVERSE
        for (int j = x; j >= price[i]; j--) {
            dp[j] = max(dp[j], dp[j - price[i]] + pages[i]);
        }
    }

    cout << dp[x] << "\n";
    return 0;
}
```

## Why Iterate Budget in Reverse? (Key Concept)

This is the most important concept in 0/1 Knapsack space optimization.

| Iteration Order | What Happens | Result |
|-----------------|--------------|--------|
| Forward (left to right) | `dp[j-price]` may already include current book | Same book used multiple times (Unbounded Knapsack) |
| Reverse (right to left) | `dp[j-price]` is from previous book iteration | Each book used at most once (0/1 Knapsack) |

**Memory trick:**
- **Forward** = **Infinite** items (Unbounded)
- **Reverse** = **Restricted** to one (0/1)

## Common Mistakes

### Mistake 1: Forward Iteration in 1D

```python
# WRONG - This solves UNBOUNDED knapsack (each book can be bought multiple times)
for j in range(price, x + 1):
    dp[j] = max(dp[j], dp[j - price] + page)

# CORRECT - 0/1 knapsack (each book bought at most once)
for j in range(x, price - 1, -1):
    dp[j] = max(dp[j], dp[j - price] + page)
```

### Mistake 2: Forgetting Affordability Check

```python
# WRONG - May access negative index
for j in range(x, -1, -1):
    dp[j] = max(dp[j], dp[j - price] + page)  # j - price could be negative!

# CORRECT - Only consider budgets where we can afford the book
for j in range(x, price - 1, -1):
    dp[j] = max(dp[j], dp[j - price] + page)
```

### Mistake 3: Off-by-One in 2D Indexing

```python
# WRONG - prices and pages are 0-indexed
for i in range(1, n + 1):
    price = prices[i]  # IndexError when i = n

# CORRECT
for i in range(1, n + 1):
    price = prices[i - 1]  # Adjust for 0-indexing
```

### Mistake 4: Not Initializing Base Case

```python
# Implicit but important: dp[0] = 0
# With budget 0, we can buy 0 pages
dp = [0] * (x + 1)  # This correctly initializes base case
```

## Complexity Analysis

| Version | Time | Space | Notes |
|---------|------|-------|-------|
| 2D DP | O(n * x) | O(n * x) | Clearer logic, can reconstruct solution |
| 1D DP | O(n * x) | O(x) | Space optimized, preferred for CSES |

For this problem: n <= 1000, x <= 100000
- 2D: ~100 million integers = ~400 MB (might TLE or MLE)
- 1D: ~100 thousand integers = ~400 KB (efficient)

## Related Problems

### CSES Problems
- [Minimizing Coins](https://cses.fi/problemset/task/1634) - Unbounded knapsack variant
- [Coin Combinations I](https://cses.fi/problemset/task/1635) - Counting ways (unbounded)
- [Coin Combinations II](https://cses.fi/problemset/task/1636) - Counting combinations
- [Money Sums](https://cses.fi/problemset/task/1745) - Subset sum variant

### LeetCode Problems
- [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) - 0/1 Knapsack
- [494. Target Sum](https://leetcode.com/problems/target-sum/) - 0/1 Knapsack with +/-
- [474. Ones and Zeroes](https://leetcode.com/problems/ones-and-zeroes/) - 2D Knapsack
- [518. Coin Change II](https://leetcode.com/problems/coin-change-ii/) - Unbounded variant

## Summary

| Concept | Key Point |
|---------|-----------|
| Problem Type | 0/1 Knapsack (take or leave each item) |
| State | `dp[i][j]` = max value with first i items, capacity j |
| Transition | `max(skip, take)` = `max(dp[i-1][j], dp[i-1][j-w] + v)` |
| Base Case | `dp[0][j] = 0` (no items = no value) |
| Space Optimization | Use 1D array with **reverse** iteration |
| Critical Detail | Reverse iteration ensures each item used at most once |
