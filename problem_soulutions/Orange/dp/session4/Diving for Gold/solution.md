# Diving for Gold

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

John the diver wants to recover gold from a shipwreck. He has limited air (t seconds underwater). Each treasure has:
- Depth di
- Gold value vi
- Time to descend: w × di
- Time to ascend: 2w × di

Total time for treasure i: 3w × di

Find the maximum gold John can recover and which treasures to take.

## Input Format
- Multiple test cases (blank line separated)
- Each test case:
  - First line: t (time limit) and w (constant)
  - Second line: n (number of treasures)
  - Next n lines: di and vi (depth and gold value)

## Output Format
For each test case:
- Line 1: Maximum gold
- Line 2: Number of treasures recovered
- Following lines: depth and gold of each recovered treasure (in input order)

## Solution

### Approach
This is a 0/1 Knapsack problem.
- Weight of item i: 3 × w × di (time cost)
- Value of item i: vi (gold)
- Capacity: t (time limit)

Track which items are selected for reconstruction.

### Python Solution

```python
def solve():
  import sys
  data = sys.stdin.read().strip().split('\n')
  idx = 0
  first = True

  while idx < len(data):
    # Skip empty lines
    while idx < len(data) and not data[idx].strip():
      idx += 1

    if idx >= len(data):
      break

    t, w = map(int, data[idx].split())
    idx += 1

    n = int(data[idx])
    idx += 1

    treasures = []
    for _ in range(n):
      d, v = map(int, data[idx].split())
      treasures.append((d, v))
      idx += 1

    # Calculate time cost for each treasure
    costs = [3 * w * d for d, v in treasures]
    values = [v for d, v in treasures]

    # 0/1 Knapsack
    # dp[c] = max gold with time capacity c
    dp = [0] * (t + 1)
    # For reconstruction: track which items
    parent = [[-1] * (t + 1) for _ in range(n + 1)]

    for i in range(n):
      for c in range(t, costs[i] - 1, -1):
        if dp[c - costs[i]] + values[i] > dp[c]:
          dp[c] = dp[c - costs[i]] + values[i]

    # Reconstruction with separate tracking
    # Re-run with full tracking
    dp2 = [[0] * (t + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
      for c in range(t + 1):
        dp2[i][c] = dp2[i-1][c]
        if c >= costs[i-1] and dp2[i-1][c - costs[i-1]] + values[i-1] > dp2[i][c]:
          dp2[i][c] = dp2[i-1][c - costs[i-1]] + values[i-1]

    # Backtrack to find items
    selected = []
    c = t
    for i in range(n, 0, -1):
      if dp2[i][c] != dp2[i-1][c]:
        selected.append(i - 1)
        c -= costs[i-1]

    selected.reverse()

    # Output
    if not first:
      print()
    first = False

    print(dp[t])
    print(len(selected))
    for i in selected:
      print(treasures[i][0], treasures[i][1])

if __name__ == "__main__":
  solve()
```

### Space-Optimized with Reconstruction

```python
def solve():
  import sys
  input_data = sys.stdin.read().strip().split('\n')
  idx = 0
  first = True

  while idx < len(input_data):
    while idx < len(input_data) and not input_data[idx].strip():
      idx += 1

    if idx >= len(input_data):
      break

    t, w = map(int, input_data[idx].split())
    idx += 1

    n = int(input_data[idx])
    idx += 1

    treasures = []
    for _ in range(n):
      d, v = map(int, input_data[idx].split())
      treasures.append((d, v))
      idx += 1

    # Time costs
    costs = [3 * w * d for d, v in treasures]
    values = [v for d, v in treasures]

    # DP with item tracking
    # dp[c] = (max_value, set of item indices)
    INF = float('inf')
    dp = [(0, []) for _ in range(t + 1)]

    for i in range(n):
      for c in range(t, costs[i] - 1, -1):
        prev_val, prev_items = dp[c - costs[i]]
        new_val = prev_val + values[i]

        if new_val > dp[c][0]:
          dp[c] = (new_val, prev_items + [i])

    max_gold, selected = dp[t]

    if not first:
      print()
    first = False

    print(max_gold)
    print(len(selected))
    for i in selected:
      print(treasures[i][0], treasures[i][1])

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n × t)
- **Space Complexity:** O(n × t) for reconstruction, O(t) for value only

### Key Insight
Classic 0/1 knapsack where each treasure's "weight" is the time cost (3 × w × depth) and "value" is the gold. Track selected items during DP for reconstruction. Output must preserve original input order of selected treasures.
