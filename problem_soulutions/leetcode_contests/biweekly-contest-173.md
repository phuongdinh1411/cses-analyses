---
layout: simple
title: "Biweekly Contest 173"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-173/
---

# Biweekly Contest 173

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | January 03, 2026 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-173/) |

---

## Problems

### Q1. Reverse String Prefix

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/reverse-string-prefix/) |

#### Problem Description

You are given a string `s` and an integer `k`.

Reverse the first `k` characters of `s` and return the resulting string.

**Example 1:**

**Input:** s = "abcd", k = 2

**Output:** "bacd"

**Constraints:**

- `1 <= s.length <= 100`
- `s` consists of lowercase English letters.
- `1 <= k <= s.length`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Simple string slicing and reversal.

**Hint 1:** Extract the first k characters, reverse them.

**Hint 2:** Concatenate with the remaining characters.

**Approach:**
1. Take s[:k] and reverse it
2. Concatenate with s[k:]

```python
def reversePrefix(s, k):
  return s[:k][::-1] + s[k:]
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q2. Minimum Subarray Length With Distinct Sum At Least K

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-subarray-length-with-distinct-sum-at-least-k/) |

#### Problem Description

You are given an integer array `nums` and an integer `k`.

Return the **minimum** length of a **subarray** whose sum of **distinct** values is **at least** `k`. If no such subarray exists, return -1.

**Example 1:**

**Input:** nums = [2,2,3,1], k = 4

**Output:** 2

**Explanation:**

The subarray `[2, 3]` has distinct elements `{2, 3}` whose sum is `2 + 3 = 5`, which is at least `k = 4`. Thus, the answer is 2.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`
- `1 <= k <= 10^9`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Use sliding window with a set/counter to track distinct elements in the current window.

**Hint 1:** Maintain a window [left, right] and track distinct sum.

**Hint 2:** Expand right to add elements, shrink left when distinct sum >= k.

**Hint 3:** When an element is added/removed, update the distinct sum accordingly.

**Approach:**
1. Use two pointers for sliding window
2. Track count of each element in window
3. When count[x] goes 0->1, add x to distinct_sum; when 1->0, subtract x
4. Minimize window length when distinct_sum >= k

```python
def minSubarrayLength(nums, k):
  from collections import defaultdict

  n = len(nums)
  count = defaultdict(int)
  distinct_sum = 0
  min_len = float('inf')
  left = 0

  for right in range(n):
    x = nums[right]
    if count[x] == 0:
      distinct_sum += x
    count[x] += 1

    while distinct_sum >= k:
      min_len = min(min_len, right - left + 1)
      y = nums[left]
      count[y] -= 1
      if count[y] == 0:
        distinct_sum -= y
      left += 1

  return min_len if min_len != float('inf') else -1
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q3. Find Maximum Value in a Constrained Sequence

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/find-maximum-value-in-a-constrained-sequence/) |

#### Problem Description

You are given an integer `n`, a 2D integer array `restrictions`, and an integer array `diff` of length `n - 1`.

Construct a sequence `a[0], a[1], ..., a[n-1]` such that:

- `a[0]` is 0.
- All elements are **non-negative**.
- For every index `i` (0 <= i <= n-2), `abs(a[i] - a[i+1]) <= diff[i]`.
- For each `restrictions[i] = [idx, maxVal]`, `a[idx] <= maxVal`.

Return the **largest** value in the optimal sequence.

**Constraints:**

- `2 <= n <= 10^5`
- `1 <= restrictions.length <= n - 1`
- `1 <= diff[i] <= 10`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Compute bounds from restrictions, then find maximum achievable value at each position.

**Hint 1:** From a[0] = 0, compute max possible a[i] without restrictions (cumulative sum of diff).

**Hint 2:** For each restriction, it limits values before and after that index.

**Hint 3:** Propagate constraints from restrictions to neighboring indices.

**Approach:**
1. Initialize upper bounds: upper[i] = sum(diff[0:i]) (max reachable from a[0]=0)
2. Apply restrictions: upper[idx] = min(upper[idx], maxVal)
3. Propagate: for each i, upper[i] <= upper[i-1] + diff[i-1] and upper[i] <= upper[i+1] + diff[i]
4. Find max(upper)

```python
def maxValue(n, restrictions, diff):
  # Compute initial upper bounds (without restrictions)
  upper = [0] * n
  for i in range(1, n):
    upper[i] = upper[i-1] + diff[i-1]

  # Apply restrictions
  INF = float('inf')
  for idx, maxVal in restrictions:
    upper[idx] = min(upper[idx], maxVal)

  # Propagate constraints forward
  for i in range(1, n):
    upper[i] = min(upper[i], upper[i-1] + diff[i-1])

  # Propagate constraints backward
  for i in range(n-2, -1, -1):
    upper[i] = min(upper[i], upper[i+1] + diff[i])

  return max(upper)
```

**Time Complexity:** O(n + r) where r = number of restrictions
**Space Complexity:** O(n)

</details>

---

### Q4. Count Routes to Climb a Rectangular Grid

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/count-routes-to-climb-a-rectangular-grid/) |

#### Problem Description

You are given a string array `grid` of size `n x m`. You want to count routes from any cell in the bottom row to any cell in the top row.

Constraints:
- Move to another available cell within Euclidean distance `d`
- Each move stays on same row or goes to row directly above
- Cannot stay on same row for two consecutive turns

Return the number of routes modulo `10^9 + 7`.

**Constraints:**

- `1 <= n, m <= 750`
- `1 <= d <= 750`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** DP with state (row, col, just_stayed). Need to track if last move was a horizontal stay.

**Hint 1:** dp[r][c][stayed] = number of ways to reach cell (r,c) where 'stayed' indicates if we just made a horizontal move.

**Hint 2:** Precompute reachable cells from each cell for efficiency.

**Hint 3:** If stayed=True, next move MUST go up. If stayed=False, can go horizontal or up.

**Approach:**
1. Precompute which cells are reachable from each cell within distance d
2. DP from bottom row to top row
3. Track whether previous move was horizontal

```python
def countRoutes(grid, d):
  MOD = 10**9 + 7
  n = len(grid)
  m = len(grid[0])

  # Check if cell is available
  def available(r, c):
    return 0 <= r < n and 0 <= c < m and grid[r][c] == '.'

  # Euclidean distance squared
  def dist_sq(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2

  d_sq = d * d

  # dp[r][c][stayed] = ways to be at (r,c) with 'stayed' indicating last move was horizontal
  # stayed = 0: can move horizontal or up
  # stayed = 1: must move up next

  from collections import defaultdict
  dp = [[defaultdict(int) for _ in range(m)] for _ in range(n)]

  # Initialize: start from bottom row
  for c in range(m):
    if available(n-1, c):
      dp[n-1][c][0] = 1

  # Process row by row from bottom to top
  for r in range(n-1, -1, -1):
    for c in range(m):
      if not available(r, c):
        continue

      for stayed in [0, 1]:
        ways = dp[r][c][stayed]
        if ways == 0:
          continue

        # Horizontal move (stay on same row) - only if stayed=0
        if stayed == 0 and r > 0:  # Not on top row and didn't just stay
          for nc in range(m):
            if nc != c and available(r, nc) and dist_sq(r, c, r, nc) <= d_sq:
              dp[r][nc][1] = (dp[r][nc][1] + ways) % MOD

        # Move up (to row r-1)
        if r > 0:
          for nc in range(m):
            if available(r-1, nc) and dist_sq(r, c, r-1, nc) <= d_sq:
              dp[r-1][nc][0] = (dp[r-1][nc][0] + ways) % MOD

  # Count ways to reach top row (row 0)
  result = 0
  for c in range(m):
    result = (result + dp[0][c][0] + dp[0][c][1]) % MOD

  # Add routes that end at starting cells (single cell routes)
  if n == 1:
    for c in range(m):
      if available(0, c):
        result = (result + 1) % MOD

  return result
```

**Time Complexity:** O(n * m² * d) with optimization
**Space Complexity:** O(n * m)

</details>

---

