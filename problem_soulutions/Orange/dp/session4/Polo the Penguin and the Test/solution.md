# Polo the Penguin and the Test

## Problem Information
- **Source:** Codechef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Polo has N different questions on his test. For each question i:
- Ci = number of tests containing this question
- Pi = points for correct answer
- Ti = time needed to learn this question

Polo has W minutes total. Maximize the total points he can get.

## Input Format
- T test cases
- Each test case:
  - First line: N (questions), W (available time)
  - Next N lines: Ci, Pi, Ti for each question

## Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 100
- 1 ≤ Ci, Pi, Ti ≤ 100
- 1 ≤ W ≤ 100

## Output Format
For each test case, print maximum points achievable.

## Example
```
Input:
1
3 7
1 2 3
2 3 5
1 4 2

Output:
10
```
3 questions, 7 minutes available. Question 1: appears in 1 test, 2 points each, takes 3 min -> value 2. Question 2: 2 tests * 3 points = 6, takes 5 min. Question 3: 1 test * 4 points = 4, takes 2 min. Best: Q2 (5 min, 6 pts) + Q3 (2 min, 4 pts) = 7 min, 10 points.

## Solution

### Approach
This is a 0/1 Knapsack problem:
- Each question is an item
- Weight = Ti (time to learn)
- Value = Ci × Pi (total points from all tests)
- Capacity = W (total time available)

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, w = map(int, input().split())

    questions = []
    for _ in range(n):
      c, p, ti = map(int, input().split())
      questions.append((ti, c * p))  # (time_cost, value)

    # 0/1 Knapsack
    dp = [0] * (w + 1)

    for time_cost, value in questions:
      for capacity in range(w, time_cost - 1, -1):
        dp[capacity] = max(dp[capacity], dp[capacity - time_cost] + value)

    print(dp[w])

if __name__ == "__main__":
  solve()
```

### Alternative Solution with 2D DP

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, w = map(int, input().split())

    questions = []
    for _ in range(n):
      c, p, ti = map(int, input().split())
      questions.append((ti, c * p))

    # 2D DP for clarity
    # dp[i][j] = max value using first i questions with capacity j
    dp = [[0] * (w + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
      time_cost, value = questions[i - 1]
      for j in range(w + 1):
        # Don't take question i
        dp[i][j] = dp[i - 1][j]
        # Take question i (if possible)
        if j >= time_cost:
          dp[i][j] = max(dp[i][j], dp[i - 1][j - time_cost] + value)

    print(dp[n][w])

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × W)
- **Space Complexity:** O(W) with optimization

### Key Insight
Each question appears in Ci tests and gives Pi points per test, so total value is Ci × Pi. Learning a question takes Ti time. This maps directly to 0/1 knapsack: select questions to maximize total value within time budget W.
