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

## Example
```
Input:
4
3 7
4 1
2 1
8 1
3 7
4 2
2 1
8 4
3 5
4 1
2 2
8 9
1 1
10 3

Output:
Case #1: 2
Case #2: 6
Case #3: 11
Case #4: 3
```
In doubled units, the capacity is 2L. A stick costs 2a fully inside and a when hanging.
- **Case 2:** capacity 14. Hanging the 8 and the 4 costs 8 + 4 = 12 and gives value 4 + 2 = 6. Adding the 2 inside would cost 4 more (16 > 14).
- **Case 4:** a lone length-10 stick in a length-1 container still fits centred, giving 3.

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

    # A lone stick can always be placed with its centre inside, whatever its length.
    result = max(result, max(v for _, v in sticks))

    print(f"Case #{case}: {result}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × L)
- **Space Complexity:** O(L)

### Key Insight
At most 2 sticks can hang over the edges, one per side, and a hanging stick uses only half its length of container space. So run a knapsack over (capacity used, sticks hanging ∈ {0, 1, 2}), doubling all lengths so that halves become integers.

One special case: a single stick fits on its own no matter how long it is (centre it in the container), so the answer is at least max(vᵢ).
