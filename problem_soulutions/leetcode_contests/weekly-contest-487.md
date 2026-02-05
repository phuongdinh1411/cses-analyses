---
layout: simple
title: "Weekly Contest 487"
permalink: /problem_soulutions/leetcode_contests/weekly-contest-487/
---

# Weekly Contest 487

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | February 01, 2026 |
| **Time** | 09:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/weekly-contest-487/) |

---

## Problems

### Q1. Count Monobit Integers

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/count-monobit-integers/) |

#### Problem Description

You are given an integer `n`.

An integer is called **Monobit** if all bits in its binary representation are the same.

Return the count of **Monobit** integers in the range `[0, n]` (inclusive).

**Example 1:**

**Input:** n = 1

**Output:** 2

**Explanation:**
- The integers in the range `[0, 1]` have binary representations `"0"` and `"1"`.
- Each representation consists of identical bits. Thus, the answer is 2.

**Example 2:**

**Input:** n = 4

**Output:** 3

**Explanation:**
- The integers in the range `[0, 4]` include binaries `"0"`, `"1"`, `"10"`, `"11"`, and `"100"`.
- Only 0, 1 and 3 satisfy the Monobit condition. Thus, the answer is 3.

**Constraints:**
- `0 <= n <= 1000`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Monobit integers are either all 0s or all 1s in binary.

**Hint 1:** What numbers have all 1s in binary? They are: 1, 3, 7, 15, 31, ... (i.e., 2^k - 1)

**Hint 2:** The only number with all 0s is 0 itself.

**Approach:**
1. Start with count = 1 (for 0)
2. Generate all numbers of form 2^k - 1 (all 1s in binary)
3. Count how many are ≤ n

```python
def countMonobitIntegers(n):
  count = 1  # 0 is always monobit
  num = 1    # Start with 1 (binary: "1")
  while num <= n:
    count += 1
    num = num * 2 + 1  # Next all-1s number
  return count
```

**Time Complexity:** O(log n)
**Space Complexity:** O(1)

</details>

---

### Q2. Final Element After Subarray Deletions

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/final-element-after-subarray-deletions/) |

#### Problem Description

You are given an integer array `nums`.

Two players, Alice and Bob, play a game in turns, with Alice playing first.

- In each turn, the current player chooses any **subarray** `nums[l..r]` such that `r - l + 1 < m`, where `m` is the **current length** of the array.
- The selected **subarray is removed**, and the remaining elements are **concatenated** to form the new array.
- The game continues until **only one** element remains.

Alice aims to **maximize** the final element, while Bob aims to **minimize** it. Assuming both play optimally, return the value of the final remaining element.

**Example 1:**

**Input:** nums = [1,5,2]

**Output:** 2

**Explanation:**
- Alice removes `[1]`, array becomes `[5, 2]`.
- Bob removes `[5]`, array becomes `[2]`. Thus, the answer is 2.

**Example 2:**

**Input:** nums = [3,7]

**Output:** 7

**Explanation:**
Alice removes `[3]`, leaving the array `[7]`. Since Bob cannot play a turn now, the answer is 7.

**Constraints:**
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Think about how many total moves will be made.

**Hint 1:** Each move removes at least 1 element (and at most n-1 elements). The game ends when 1 element remains.

**Hint 2:** If array has length n, exactly n-1 elements need to be removed total.

**Hint 3:** Count the total number of turns. If n-1 is odd, Alice makes one more move than Bob. If n-1 is even, they make equal moves.

**Hint 4:** Think about what the final element must be based on who makes the last move.

**Approach:**
- If Alice has the final say (odd number of total removals needed), she can ensure the maximum element survives
- If Bob has the final say (even number of total removals needed), he can ensure the minimum element survives
- But actually, with optimal play, we need to think about what elements can possibly survive

**Key Pattern:**
- With n elements, (n-1) elements must be removed
- Alice moves on turns 1, 3, 5, ... and Bob moves on turns 2, 4, 6, ...
- The answer is the **median** element when sorted, adjusted by who has more control

```python
def finalElement(nums):
  n = len(nums)
  nums_sorted = sorted(nums)
  # With optimal play, result depends on parity
  if (n - 1) % 2 == 1:  # Alice has last move
    return nums_sorted[(n - 1) // 2 + 1]
  else:  # Bob has last move
    return nums_sorted[(n - 1) // 2]
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

</details>

---

### Q3. Design Ride Sharing System

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/design-ride-sharing-system/) |

#### Problem Description

A ride sharing system manages ride requests from riders and availability from drivers. Riders request rides, and drivers become available over time. The system should match riders and drivers in the order they arrive.

Implement the `RideSharingSystem` class:

- `RideSharingSystem()` Initializes the system.
- `void addRider(int riderId)` Adds a new rider with the given `riderId`.
- `void addDriver(int driverId)` Adds a new driver with the given `driverId`.
- `int[] matchDriverWithRider()` Matches the **earliest** available driver with the **earliest** waiting rider and removes both of them from the system. Returns `[driverId, riderId]` if a match is made, `[-1, -1]` otherwise.
- `void cancelRider(int riderId)` Cancels the ride request of the rider with the given `riderId` if the rider exists and has not yet been matched.

**Constraints:**
- `1 <= riderId, driverId <= 1000`
- Each `riderId` is **unique** among riders and is added at most **once**.
- Each `driverId` is **unique** among drivers and is added at most **once**.
- At most 1000 calls will be made in **total**.

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** This is a classic queue-based system with FIFO matching.

**Hint 1:** Use queues to maintain order of arrival for both riders and drivers.

**Hint 2:** For efficient cancellation, use a set to track cancelled riders.

**Hint 3:** When matching, skip any cancelled riders in the queue.

**Approach:**
1. Use a deque for riders and a deque for drivers (FIFO order)
2. Use a set to track cancelled rider IDs
3. On `matchDriverWithRider`: pop from both queues (skipping cancelled riders)
4. On `cancelRider`: just add to cancelled set (lazy deletion)

```python
from collections import deque

class RideSharingSystem:
  def __init__(self):
    self.riders = deque()
    self.drivers = deque()
    self.cancelled = set()
    self.matched_riders = set()

  def addRider(self, riderId):
    self.riders.append(riderId)

  def addDriver(self, driverId):
    self.drivers.append(driverId)

  def matchDriverWithRider(self):
    # Remove cancelled riders from front
    while self.riders and self.riders[0] in self.cancelled:
      self.cancelled.remove(self.riders.popleft())

    if not self.riders or not self.drivers:
      return [-1, -1]

    driver = self.drivers.popleft()
    rider = self.riders.popleft()
    self.matched_riders.add(rider)
    return [driver, rider]

  def cancelRider(self, riderId):
    if riderId not in self.matched_riders:
      self.cancelled.add(riderId)
```

**Time Complexity:** O(1) amortized for all operations
**Space Complexity:** O(n) where n is number of riders/drivers

</details>

---

### Q4. Longest Alternating Subarray After Removing At Most One Element

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/longest-alternating-subarray-after-removing-at-most-one-element/) |

#### Problem Description

You are given an integer array `nums`.

A subarray `nums[l..r]` is **alternating** if one of the following holds:

- `nums[l] < nums[l + 1] > nums[l + 2] < nums[l + 3] > ...`
- `nums[l] > nums[l + 1] < nums[l + 2] > nums[l + 3] < ...`

You can remove **at most one** element from `nums`. Then, you select an alternating subarray from `nums`.

Return the **maximum length** of the alternating subarray you can select.

**Example 1:**

**Input:** nums = [2,1,3,2]

**Output:** 4

**Explanation:** The entire array `[2, 1, 3, 2]` is alternating because `2 > 1 < 3 > 2`.

**Example 2:**

**Input:** nums = [3,2,1,2,3,2,1]

**Output:** 4

**Explanation:** Remove `nums[3]`. The array becomes `[3, 2, 1, 3, 2, 1]`. Select subarray `[2, 1, 3, 2]`.

**Constraints:**
- `2 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Precompute alternating lengths from left and right, then try removing each element.

**Hint 1:** First, compute the longest alternating subarray ending at each index (from left).

**Hint 2:** Also compute the longest alternating subarray starting at each index (from right).

**Hint 3:** For each position i, try removing nums[i] and check if left[i-1] and right[i+1] can be joined.

**Hint 4:** Two alternating sequences can be joined if the comparison direction at the junction is correct.

**Approach:**
1. Compute `left[i]` = length of longest alternating subarray ending at i
2. Compute `right[i]` = length of longest alternating subarray starting at i
3. Answer without removal = max(left[i]) for all i
4. For each i, try removing nums[i]:
   - Check if nums[i-1] and nums[i+1] have correct alternating relationship
   - If yes, can merge left[i-1] + right[i+1]

```python
def longestAlternatingSubarray(nums):
  n = len(nums)
  if n <= 2:
    return n if n == 1 or nums[0] != nums[1] else 1

  # left[i] = length of alternating subarray ending at i
  left = [1] * n
  for i in range(1, n):
    if (left[i-1] % 2 == 1 and nums[i] != nums[i-1]) or \
       (left[i-1] % 2 == 0 and ((left[i-1] // 2) % 2 == 0) != (nums[i] > nums[i-1])):
      # Check alternating pattern continues
      if (left[i-1] == 1 and nums[i] != nums[i-1]) or \
         (left[i-1] > 1 and isAlternating(nums, i-left[i-1]+1, i)):
        left[i] = left[i-1] + 1

  # Similar for right[i]
  right = [1] * n
  for i in range(n-2, -1, -1):
    if nums[i] != nums[i+1]:
      if canExtendRight(nums, i, right[i+1]):
        right[i] = right[i+1] + 1

  ans = max(left)

  # Try removing each element
  for i in range(1, n-1):
    if canMerge(nums, i, left[i-1], right[i+1]):
      ans = max(ans, left[i-1] + right[i+1])

  return ans
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

