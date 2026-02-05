# Pick The Sticks

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 5000ms
- **Memory Limit:** 512MB

## Problem Statement

Place gold sticks of various lengths on a container of length L. Sticks can overlap the container ends as long as their center of gravity remains inside. Maximize the total value of sticks placed.

Key insight: At most 2 sticks can hang over edges (one on each side), and they can extend by up to half their length.

## Input Format
- T test cases
- Each test case:
  - First line: N (sticks), L (container length)
  - Next N lines: ai (stick length), vi (stick value)

## Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 500
- 1 ≤ L ≤ 1000
- 1 ≤ ai ≤ 1000
- 1 ≤ vi ≤ 10^9

## Output Format
For each test case: "Case #x: y" where y is maximum value.

## Solution

### Approach
Modified 0/1 knapsack with states tracking how many sticks hang over edges (0, 1, or 2).

dp[i][j][k] = max value using capacity j with k sticks hanging over edges (k ∈ {0, 1, 2})

For a hanging stick, it only uses half its length of container space.

### Python Solution

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    n, L = map(int, input().split())

    sticks = []
    for _ in range(n):
      a, v = map(int, input().split())
      sticks.append((a, v))

    # Multiply L by 2 to avoid floating point
    L *= 2

    # dp[capacity][hanging_count] = max value
    # hanging_count: 0, 1, or 2
    INF = float('-inf')

    # Initialize
    dp = [[INF] * 3 for _ in range(L + 1)]
    dp[0][0] = 0

    for a, v in sticks:
      full_len = a * 2  # full stick length (doubled)
      half_len = a      # half length (since L is doubled)

      # Process in reverse for 0/1 knapsack
      new_dp = [row[:] for row in dp]

      for c in range(L + 1):
        for h in range(3):
          if dp[c][h] == INF:
            continue

          # Option 1: Place stick fully inside (uses full length)
          if c + full_len <= L:
            new_dp[c + full_len][h] = max(new_dp[c + full_len][h], dp[c][h] + v)

          # Option 2: Place stick hanging over edge (uses half length)
          if h < 2 and c + half_len <= L:
            new_dp[c + half_len][h + 1] = max(new_dp[c + half_len][h + 1], dp[c][h] + v)

      dp = new_dp

    # Find maximum value
    result = 0
    for c in range(L + 1):
      for h in range(3):
        if dp[c][h] != INF:
          result = max(result, dp[c][h])

    print(f"Case #{case}: {result}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    n, L = map(int, input().split())

    sticks = []
    for _ in range(n):
      a, v = map(int, input().split())
      sticks.append((a, v))

    # Use 2*L to handle half-lengths as integers
    capacity = 2 * L
    NEG_INF = float('-inf')

    # dp[c][e] = max value with c capacity used and e edge slots used (0, 1, 2)
    dp = [[NEG_INF] * 3 for _ in range(capacity + 1)]
    dp[0][0] = 0

    for length, value in sticks:
      full_cost = 2 * length  # fully inside
      half_cost = length       # hanging (uses only half)

      # Process backwards
      for c in range(capacity, -1, -1):
        for e in range(3):
          if dp[c][e] == NEG_INF:
            continue

          # Option A: place fully inside
          nc = c + full_cost
          if nc <= capacity:
            dp[nc][e] = max(dp[nc][e], dp[c][e] + value)

          # Option B: place hanging
          if e < 2:
            nc = c + half_cost
            if nc <= capacity:
              dp[nc][e + 1] = max(dp[nc][e + 1], dp[c][e] + value)

    # Get max value
    ans = 0
    for c in range(capacity + 1):
      for e in range(3):
        if dp[c][e] != NEG_INF:
          ans = max(ans, dp[c][e])

    print(f"Case #{case}: {ans}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × L)
- **Space Complexity:** O(L)

### Key Insight
At most 2 sticks can hang over edges (one per side). A hanging stick uses only half its length of container space. Use 3D DP tracking: capacity used and number of hanging sticks (0/1/2). Multiply lengths by 2 to handle half-lengths as integers.
