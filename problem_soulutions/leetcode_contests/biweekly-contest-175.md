---
layout: simple
title: "Biweekly Contest 175"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-175/
---

# Biweekly Contest 175

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | January 31, 2026 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-175/) |

---

## Problems

### Q1. Reverse Letters Then Special Characters in a String

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/reverse-letters-then-special-characters-in-a-string/) |

#### Problem Description

You are given a string `s` consisting of lowercase English letters and special characters.

Your task is to perform these **in order**:

- **Reverse** the **lowercase letters** and place them back into the positions originally occupied by letters.
- **Reverse** the **special characters** and place them back into the positions originally occupied by special characters.

Return the resulting string after performing the reversals.

**Example 1:**

**Input:** s = ")ebc#da@f("

**Output:** "(fad@cb#e)"

**Constraints:**

- `1 <= s.length <= 100`
- `s` consists only of lowercase English letters and the special characters in `"!@#$%^&*()"`.

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Separate letters and special characters, reverse each group, then reassemble.

**Hint 1:** Extract all letters in order, extract all special characters in order.

**Hint 2:** Reverse both extracted lists.

**Hint 3:** Place them back in their original type positions.

**Approach:**
1. Collect letters and their indices
2. Collect special chars and their indices
3. Reverse both character lists
4. Place reversed chars back at the tracked indices

```python
def reverseLettersThenSpecial(s):
  letters = []
  specials = []
  letter_pos = []
  special_pos = []

  for i, c in enumerate(s):
    if c.isalpha():
      letters.append(c)
      letter_pos.append(i)
    else:
      specials.append(c)
      special_pos.append(i)

  letters.reverse()
  specials.reverse()

  result = list(s)
  for i, pos in enumerate(letter_pos):
    result[pos] = letters[i]
  for i, pos in enumerate(special_pos):
    result[pos] = specials[i]

  return ''.join(result)
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q2. Minimum K to Reduce Array Within Limit

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-k-to-reduce-array-within-limit/) |

#### Problem Description

You are given a **positive** integer array `nums`.

For a positive integer `k`, define `nonPositive(nums, k)` as the **minimum** number of **operations** needed to make every element of `nums` **non-positive**. In one operation, you can choose an index `i` and reduce `nums[i]` by `k`.

Return the **minimum** value of `k` such that `nonPositive(nums, k) <= k^2`.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Binary search on k. For a given k, compute total operations needed.

**Hint 1:** Operations for element x with step k: ceil(x/k) = (x + k - 1) // k.

**Hint 2:** Total operations = sum of ceil(nums[i]/k) for all i.

**Hint 3:** Binary search for minimum k where total_ops <= k².

**Approach:**
1. Binary search on k from 1 to max(nums)
2. For each k, compute total operations
3. Find minimum k where total_ops <= k²

```python
def minK(nums):
  def ops_needed(k):
    return sum((x + k - 1) // k for x in nums)

  # Binary search for minimum k
  left, right = 1, max(nums)

  while left < right:
    mid = (left + right) // 2
    if ops_needed(mid) <= mid * mid:
      right = mid
    else:
      left = mid + 1

  return left
```

**Time Complexity:** O(n log M) where M = max(nums)
**Space Complexity:** O(1)

</details>

---

### Q3. Longest Strictly Increasing Subsequence With Non-Zero Bitwise AND

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/longest-strictly-increasing-subsequence-with-non-zero-bitwise-and/) |

#### Problem Description

You are given an integer array `nums`.

Return the length of the **longest strictly increasing subsequence** in `nums` whose bitwise **AND** is **non-zero**. If no such subsequence exists, return 0.

**Example 1:**

**Input:** nums = [5,4,7]

**Output:** 2

**Explanation:**

One longest strictly increasing subsequence is `[5, 7]`. The bitwise AND is `5 AND 7 = 5`, which is non-zero.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** For AND to be non-zero, all elements must share at least one common bit set to 1.

**Hint 1:** For each bit position b, find the longest increasing subsequence among numbers that have bit b set.

**Hint 2:** Use standard LIS algorithm (O(n log n)) for each of the 30 bit positions.

**Hint 3:** The answer is the maximum LIS length across all bit positions.

**Approach:**
1. For each bit position 0-29
2. Filter numbers with that bit set
3. Find LIS of filtered numbers
4. Return maximum LIS length found

```python
import bisect

def longestIncreasingSubseq(nums):
  def lis_length(arr):
    if not arr:
      return 0
    tails = []
    for x in arr:
      pos = bisect.bisect_left(tails, x)
      if pos == len(tails):
        tails.append(x)
      else:
        tails[pos] = x
    return len(tails)

  result = 0
  for bit in range(30):
    mask = 1 << bit
    filtered = [x for x in nums if x & mask]
    result = max(result, lis_length(filtered))

  return result
```

**Time Complexity:** O(30 * n log n) = O(n log n)
**Space Complexity:** O(n)

</details>

---

### Q4. Minimum Partition Score

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 7 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-partition-score/) |

#### Problem Description

You are given an integer array `nums` and an integer `k`.

Your task is to partition `nums` into **exactly** `k` subarrays and return the **minimum possible score** among all valid partitions.

The **score** of a partition is the **sum** of the **values** of all its subarrays.

The **value** of a subarray is defined as `sumArr * (sumArr + 1) / 2`, where `sumArr` is the sum of its elements.

**Constraints:**

- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10^4`
- `1 <= k <= nums.length`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Use DP with prefix sums. The value function s*(s+1)/2 is convex, which affects the optimal partition strategy.

**Hint 1:** dp[i][j] = minimum score to partition nums[0:i] into j subarrays.

**Hint 2:** Transition: dp[i][j] = min(dp[m][j-1] + value(sum(nums[m:i]))) for all valid m.

**Hint 3:** Precompute prefix sums for efficient range sum queries.

**Approach:**
1. Compute prefix sums
2. dp[i][j] = min score to partition first i elements into j parts
3. Base: dp[0][0] = 0
4. Transition: try all possible last partition boundaries

```python
def minPartitionScore(nums, k):
  n = len(nums)

  # Prefix sums
  prefix = [0] * (n + 1)
  for i in range(n):
    prefix[i + 1] = prefix[i] + nums[i]

  def value(s):
    return s * (s + 1) // 2

  def range_sum(i, j):
    return prefix[j] - prefix[i]

  # dp[i][j] = min score to partition nums[0:i] into j parts
  INF = float('inf')
  dp = [[INF] * (k + 1) for _ in range(n + 1)]
  dp[0][0] = 0

  for i in range(1, n + 1):
    for j in range(1, min(i, k) + 1):
      for m in range(j - 1, i):
        s = range_sum(m, i)
        dp[i][j] = min(dp[i][j], dp[m][j - 1] + value(s))

  return dp[n][k]
```

**Time Complexity:** O(n² * k)
**Space Complexity:** O(n * k)

</details>

---

