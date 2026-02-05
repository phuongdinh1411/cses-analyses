---
layout: simple
title: "Biweekly Contest 172"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-172/
---

# Biweekly Contest 172

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | December 20, 2025 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-172/) |

---

## Problems

### Q1. Minimum Number of Operations to Have Distinct Elements

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-number-of-operations-to-have-distinct-elements/) |

#### Problem Description

You are given an integer array `nums`.

In one operation, you remove the **first three elements**. If there are fewer than three elements remaining, **all** remaining elements are removed.

Repeat until the array is empty or contains no duplicate values.

Return the number of operations required.

**Example 1:**

**Input:** nums = [3,8,3,6,5,8]

**Output:** 1

**Explanation:**

In the first operation, we remove the first three elements. The remaining elements `[6, 5, 8]` are all distinct.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Simulate the process. After removing 3k elements, check if remaining elements are distinct.

**Hint 1:** For each operation count (0, 1, 2, ...), check if elements from index 3*ops onwards are all distinct.

**Hint 2:** Use a set to check for duplicates.

**Hint 3:** Stop when all distinct or array is empty.

**Approach:**
1. Start with ops = 0
2. Check if nums[3*ops:] has all distinct elements
3. If yes, return ops. If array becomes empty, return ops.
4. Otherwise, increment ops and repeat

```python
def minOperations(nums):
  n = len(nums)
  ops = 0

  while True:
    start = 3 * ops
    if start >= n:
      return ops

    remaining = nums[start:]
    if len(remaining) == len(set(remaining)):
      return ops

    ops += 1
```

**Time Complexity:** O(n²) worst case, but typically O(n)
**Space Complexity:** O(n)

</details>

---

### Q2. Maximum Sum of Three Numbers Divisible by Three

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/maximum-sum-of-three-numbers-divisible-by-three/) |

#### Problem Description

You are given an integer array `nums`.

Choose **exactly three** integers such that their sum is divisible by three.

Return the **maximum** possible sum. If no such triplet exists, return 0.

**Example 1:**

**Input:** nums = [4,2,3,1]

**Output:** 9

**Explanation:**

The valid triplets whose sum is divisible by 3 are: `(4, 2, 3)` with sum 9, `(2, 3, 1)` with sum 6. Maximum is 9.

**Constraints:**

- `3 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Group numbers by their remainder mod 3. To get sum divisible by 3, we need remainders that sum to 0 (mod 3).

**Hint 1:** Group numbers: r0 (remainder 0), r1 (remainder 1), r2 (remainder 2).

**Hint 2:** Valid combinations: (r0, r0, r0), (r1, r1, r1), (r2, r2, r2), (r0, r1, r2).

**Hint 3:** For each valid combination, pick the largest elements.

**Approach:**
1. Sort each remainder group in descending order
2. Try all valid combinations of 3 elements
3. Return maximum sum

```python
def maxSumDivisibleByThree(nums):
  # Group by remainder
  groups = [[], [], []]
  for x in nums:
    groups[x % 3].append(x)

  # Sort each group descending
  for g in groups:
    g.sort(reverse=True)

  result = 0

  # Helper to get top k elements from a group
  def top_k(g, k):
    return g[:k] if len(g) >= k else None

  # Case 1: Three from r0
  if len(groups[0]) >= 3:
    result = max(result, sum(groups[0][:3]))

  # Case 2: Three from r1
  if len(groups[1]) >= 3:
    result = max(result, sum(groups[1][:3]))

  # Case 3: Three from r2
  if len(groups[2]) >= 3:
    result = max(result, sum(groups[2][:3]))

  # Case 4: One from each group
  if groups[0] and groups[1] and groups[2]:
    result = max(result, groups[0][0] + groups[1][0] + groups[2][0])

  return result
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

</details>

---

### Q3. Maximum Score After Binary Swaps

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/maximum-score-after-binary-swaps/) |

#### Problem Description

You are given an integer array `nums` and a binary string `s` of the same length.

Initially, your score is 0. Each index `i` where `s[i] = '1'` contributes `nums[i]` to the score.

You may swap adjacent characters in `s` where `s[i] = '0'` and `s[i+1] = '1'`.

Return the **maximum possible score**.

**Example 1:**

**Input:** nums = [2,1,5,2,3], s = "01010"

**Output:** 7

**Constraints:**

- `n == nums.length == s.length`
- `1 <= n <= 10^5`
- `1 <= nums[i] <= 10^9`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** The swap operation can only move '1's to the left (never right). Each '1' can move as far left as possible until blocked by another '1'.

**Hint 1:** Count the number of '1's in s. Call it k.

**Hint 2:** After optimal swaps, the k '1's will occupy some subset of positions.

**Hint 3:** Each '1' can reach any position to its left that isn't blocked. The leftmost k positions with highest nums values among reachable positions.

**Approach:**
1. For each '1' at position i, it can move to any position in [0, i]
2. We have k '1's, and we want to place them optimally
3. Greedy: sort positions by nums value, take best k positions that are achievable

```python
def maxScore(nums, s):
  n = len(nums)
  ones_positions = [i for i in range(n) if s[i] == '1']
  k = len(ones_positions)

  if k == 0:
    return 0

  # Each '1' at position p can reach any position <= p
  # We want to select k positions for k '1's to maximize score

  # The rightmost '1' can go to any position 0 to ones_positions[-1]
  # The second rightmost can go to any position 0 to ones_positions[-2]
  # etc.

  # Greedy: assign largest nums[i] to '1's that can reach them
  # Process from right to left: for each '1', pick best available position

  available = list(range(n))  # All positions
  selected_values = []

  # Sort ones_positions in descending order (process rightmost first)
  ones_positions.sort(reverse=True)

  for one_pos in ones_positions:
    # This '1' can reach positions 0 to one_pos
    # Find the position with max nums value in [0, one_pos] that's still available
    best_val = -1
    best_idx = -1
    for i, pos in enumerate(available):
      if pos <= one_pos and nums[pos] > best_val:
        best_val = nums[pos]
        best_idx = i
    if best_idx != -1:
      selected_values.append(best_val)
      available.pop(best_idx)

  return sum(selected_values)
```

**Optimized with sorting:**

```python
def maxScore(nums, s):
  n = len(nums)
  k = s.count('1')
  if k == 0:
    return 0

  # Find rightmost position of each '1'
  one_positions = [i for i in range(n) if s[i] == '1']

  # For optimal assignment: pair largest reachable nums with '1's
  # Sort (nums[i], i) and greedily assign

  indexed = [(nums[i], i) for i in range(n)]
  indexed.sort(reverse=True)

  # one_positions sorted ascending, need k positions
  # one_positions[j] means j-th '1' can reach positions 0..one_positions[j]

  result = 0
  used = 0
  one_idx = k - 1  # Start from rightmost '1'

  for val, pos in indexed:
    if used == k:
      break
    # Check if any remaining '1' can reach this position
    # A '1' at one_positions[j] can reach pos if pos <= one_positions[j]
    if one_idx >= 0 and pos <= one_positions[one_idx]:
      result += val
      used += 1
      one_idx -= 1

  return result
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

</details>

---

### Q4. Last Remaining Integer After Alternating Deletion Operations

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/last-remaining-integer-after-alternating-deletion-operations/) |

#### Problem Description

You are given an integer `n`.

Write integers from 1 to `n` in a sequence. Alternately apply:

- **Operation 1**: Starting from the left, delete every second number.
- **Operation 2**: Starting from the right, delete every second number.

Return the last remaining integer.

**Example:**

**Input:** n = 8

**Output:** 3

**Constraints:**

- `1 <= n <= 10^15`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** This is the Josephus problem variant. Track the leftmost element, step size, and direction.

**Hint 1:** After operation 1 (left-to-right), the leftmost element always changes.

**Hint 2:** After operation 2 (right-to-left), the leftmost element changes only if count is odd.

**Hint 3:** The step doubles after each operation. Track (left, step, count, direction).

**Approach:**
1. Track: left (current leftmost), step (gap between consecutive elements), count (remaining elements), dir (True=left-to-right)
2. When deleting from left, left += step
3. When deleting from right with odd count, left += step
4. After each operation: count //= 2, step *= 2

```python
def lastRemaining(n):
  left = 1
  step = 1
  count = n
  from_left = True

  while count > 1:
    if from_left:
      # Delete from left: leftmost always removed
      left += step
    else:
      # Delete from right: leftmost removed only if count is odd
      if count % 2 == 1:
        left += step

    count //= 2
    step *= 2
    from_left = not from_left

  return left
```

**Time Complexity:** O(log n)
**Space Complexity:** O(1)

</details>

---

