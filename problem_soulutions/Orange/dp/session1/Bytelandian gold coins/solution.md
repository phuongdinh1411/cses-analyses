# Bytelandian Gold Coins

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

In Byteland they have a very strange monetary system. Each Bytelandian gold coin has an integer number written on it. A coin n can be exchanged in a bank into three coins: n/2, n/3 and n/4. But these numbers are all rounded down (the banks have to make a profit). You can also sell Bytelandian coins for American dollars. The exchange rate is 1:1. But you can not buy Bytelandian coins.

You have one gold coin. What is the maximum amount of American dollars you can get for it?

## Input Format
- The input will contain several test cases (not more than 10).
- Each testcase is a single line with a number n, 0 ≤ n ≤ 1000000000.
- It is the number written on your coin.

## Output Format
For each test case output a single line, containing the maximum amount of American dollars you can make.

## Solution

### Approach
This is a recursive problem with memoization:
- For a coin with value n, we can either:
  1. Keep it and get n dollars
  2. Exchange it for coins worth n/2, n/3, and n/4, then recursively find the max for each
- Answer is max(n, solve(n/2) + solve(n/3) + solve(n/4))

Since n can be up to 10^9, we use a dictionary for memoization instead of an array.

### Python Solution

```python
import sys
sys.setrecursionlimit(100000)

memo = {}

def solve(n):
    if n == 0:
        return 0

    if n in memo:
        return memo[n]

    # Either keep the coin or exchange it
    exchanged = solve(n // 2) + solve(n // 3) + solve(n // 4)
    result = max(n, exchanged)

    memo[n] = result
    return result

def main():
    try:
        while True:
            n = int(input())
            print(solve(n))
    except EOFError:
        pass

if __name__ == "__main__":
    main()
```

### Alternative Iterative Solution (Bottom-up)

```python
def solve_iterative(n):
    if n < 12:
        return n

    # Use dictionary for sparse memoization
    dp = {}

    def get_value(x):
        if x < 12:
            return x
        if x in dp:
            return dp[x]

        result = max(x, get_value(x // 2) + get_value(x // 3) + get_value(x // 4))
        dp[x] = result
        return result

    return get_value(n)

def main():
    try:
        while True:
            n = int(input())
            print(solve_iterative(n))
    except EOFError:
        pass

if __name__ == "__main__":
    main()
```

### Complexity Analysis
- **Time Complexity:** O(n) unique subproblems, but due to the division, it's actually O(log^3 n) approximately
- **Space Complexity:** O(log n) for recursion stack and memoization

### Key Insight
For small values of n (n < 12), it's always better to keep the coin since n/2 + n/3 + n/4 < n. For larger values, exchanging becomes profitable.
