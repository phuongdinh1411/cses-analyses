---
layout: simple
title: "Biweekly Contest 169"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-169/
---

# Biweekly Contest 169

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | November 08, 2025 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-169/) |

---

## Problems

### Q1. Minimum Moves to Equal Array Elements III

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-iii/) |

#### Problem Description

You are given an integer array `nums`.

In one move, you may **increase** the value of any single element `nums[i]` by 1.

Return the **minimum total** number of **moves** required so that all elements in `nums` become **equal**.

 

**Example 1:**

**Input:** nums = [2,1,3]

**Output:** 3

**Explanation:**

To make all elements equal:

	- Increase `nums[0] = 2` by 1 to make it 3.
	- Increase `nums[1] = 1` by 1 to make it 2.
	- Increase `nums[1] = 2` by 1 to make it 3.

Now, all elements of `nums` are equal to 3. The minimum total moves is `3`.

**Example 2:**

**Input:** nums = [4,4,5]

**Output:** 2

**Explanation:**

To make all elements equal:

	- Increase `nums[0] = 4` by 1 to make it 5.
	- Increase `nums[1] = 4` by 1 to make it 5.

Now, all elements of `nums` are equal to 5. The minimum total moves is `2`.

 

**Constraints:**

	- `1 <= nums.length <= 100`
	- `1 <= nums[i] <= 100`

<details markdown="1">
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Since we can only increase values, the optimal target is the maximum element in the array.

**Hint 1:** We need all elements to become equal, and we can only increase.
**Hint 2:** The target must be at least max(nums) since we can't decrease any element.
**Hint 3:** Choosing target = max(nums) minimizes the total operations.

**Approach:**
1. Find the maximum value in the array
2. For each element, calculate how much we need to increase it to reach the maximum
3. Sum all the increases

```python
def minMoves(nums):
  target = max(nums)
  total_moves = 0
  for num in nums:
    total_moves += target - num
  return total_moves
```

**Alternative one-liner:**
```python
def minMoves(nums):
  return sum(max(nums) - x for x in nums)
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

</details>

---

### Q2. Count Subarrays With Majority Element I

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/count-subarrays-with-majority-element-i/) |

#### Problem Description

You are given an integer array `nums` and an integer `target`.

Return the number of **subarrays** of `nums` in which `target` is the **majority element**.

The **majority element** of a subarray is the element that appears **strictly** **more than half** of the times in that subarray.

 

**Example 1:**

**Input:** nums = [1,2,2,3], target = 2

**Output:** 5

**Explanation:**

Valid subarrays with `target = 2` as the majority element:

	- `nums[1..1] = [2]`
	- `nums[2..2] = [2]`
	- `nums[1..2] = [2,2]`
	- `nums[0..2] = [1,2,2]`
	- `nums[1..3] = [2,2,3]`

So there are 5 such subarrays.

**Example 2:**

**Input:** nums = [1,1,1,1], target = 1

**Output:** 10

**Explanation: **

**​​​​​​​**All 10 subarrays have 1 as the majority element.

**Example 3:**

**Input:** nums = [1,2,3], target = 4

**Output:** 0

**Explanation:**

`target = 4` does not appear in `nums` at all. Therefore, there cannot be any subarray where 4 is the majority element. Hence the answer is 0.

 

**Constraints:**

	- `1 <= nums.length <= 1000`
	- `1 <= nums[i] <= 10^​​​​​​​9`
	- `1 <= target <= 10^9`

<details markdown="1">
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** With n <= 1000, we can use O(n^2) brute force to check all subarrays.

**Hint 1:** For each starting index i, extend to ending index j and track the count of target.
**Hint 2:** Target is majority if count(target) > (j - i + 1) / 2.
**Hint 3:** Maintain a running count of target as you extend the subarray.

**Approach:**
1. For each starting position i
2. Extend ending position j from i to n-1
3. Maintain count of target in the current subarray
4. Check if target count > half of subarray length
5. Count valid subarrays

```python
def countSubarrays(nums, target):
  n = len(nums)
  count = 0

  for i in range(n):
    target_count = 0
    for j in range(i, n):
      if nums[j] == target:
        target_count += 1
      length = j - i + 1
      # Majority means strictly more than half
      if target_count > length // 2:
        count += 1

  return count
```

**Alternative using target_count * 2 > length:**
```python
def countSubarrays(nums, target):
  n = len(nums)
  count = 0
  for i in range(n):
    target_cnt = 0
    for j in range(i, n):
      if nums[j] == target:
        target_cnt += 1
      if target_cnt * 2 > j - i + 1:
        count += 1
  return count
```

**Time Complexity:** O(n^2)
**Space Complexity:** O(1)

</details>

---

### Q3. Longest Non-Decreasing Subarray After Replacing at Most One Element

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/longest-non-decreasing-subarray-after-replacing-at-most-one-element/) |

#### Problem Description

You are given an integer array `nums`.

You are allowed to replace **at most** one element in the array with any other integer value of your choice.

Return the length of the **longest non-decreasing subarray** that can be obtained after performing at most one replacement.

An array is said to be **non-decreasing** if each element is greater than or equal to its previous one (if it exists).

 

**Example 1:**

**Input:** nums = [1,2,3,1,2]

**Output:** 4

**Explanation:**

Replacing `nums[3] = 1` with 3 gives the array [1, 2, 3, 3, 2].

The longest non-decreasing subarray is [1, 2, 3, 3], which has a length of 4.

**Example 2:**

**Input:** nums = [2,2,2,2,2]

**Output:** 5

**Explanation:**

All elements in `nums` are equal, so it is already non-decreasing and the entire `nums` forms a subarray of length 5.

 

**Constraints:**

	- `1 <= nums.length <= 10^5`
	- `-10^9 <= nums[i] <= 10^9`​​​​​​​

<details markdown="1">
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** We can replace at most one element. Consider: (1) no replacement, (2) replace one element to bridge two non-decreasing segments.

**Hint 1:** First compute non-decreasing length ending at each index and starting at each index.
**Hint 2:** For each position, try replacing it to connect the segment ending before it with the segment starting after it.
**Hint 3:** When replacing position i, we need nums[i-1] <= new_value <= nums[i+1] to be possible.

**Approach:**
1. Compute prefix[i] = length of non-decreasing subarray ending at i
2. Compute suffix[i] = length of non-decreasing subarray starting at i
3. Base answer = max(prefix) (no replacement needed)
4. For each position i, try replacing nums[i] to merge prefix[i-1] and suffix[i+1]

```python
def longestNonDecreasingSubarray(nums):
  n = len(nums)
  if n == 1:
    return 1

  # prefix[i] = length of non-decreasing ending at i
  prefix = [1] * n
  for i in range(1, n):
    if nums[i] >= nums[i - 1]:
      prefix[i] = prefix[i - 1] + 1

  # suffix[i] = length of non-decreasing starting at i
  suffix = [1] * n
  for i in range(n - 2, -1, -1):
    if nums[i] <= nums[i + 1]:
      suffix[i] = suffix[i + 1] + 1

  # Base case: no replacement
  result = max(prefix)

  # Try replacing each position
  for i in range(n):
    # Case 1: Replace nums[i], extend prefix ending at i-1
    if i > 0:
      # Can extend by 1 (just replacing nums[i])
      result = max(result, prefix[i - 1] + 1)

    # Case 2: Replace nums[i], extend suffix starting at i+1
    if i < n - 1:
      result = max(result, suffix[i + 1] + 1)

    # Case 3: Bridge prefix[i-1] and suffix[i+1] through position i
    if i > 0 and i < n - 1:
      if nums[i - 1] <= nums[i + 1]:
        result = max(result, prefix[i - 1] + 1 + suffix[i + 1])

  return result
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q4. Count Subarrays With Majority Element II

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/count-subarrays-with-majority-element-ii/) |

#### Problem Description

You are given an integer array `nums` and an integer `target`.

Return the number of **subarrays** of `nums` in which `target` is the **majority element**.

The **majority element** of a subarray is the element that appears **strictly more than half** of the times in that subarray.

 

**Example 1:**

**Input:** nums = [1,2,2,3], target = 2

**Output:** 5

**Explanation:**

Valid subarrays with `target = 2` as the majority element:

	- `nums[1..1] = [2]`
	- `nums[2..2] = [2]`
	- `nums[1..2] = [2,2]`
	- `nums[0..2] = [1,2,2]`
	- `nums[1..3] = [2,2,3]`

So there are 5 such subarrays.

**Example 2:**

**Input:** nums = [1,1,1,1], target = 1

**Output:** 10

**Explanation: **

**​​​​​​​**All 10 subarrays have 1 as the majority element.

**Example 3:**

**Input:** nums = [1,2,3], target = 4

**Output:** 0

**Explanation:**

`target = 4` does not appear in `nums` at all. Therefore, there cannot be any subarray where 4 is the majority element. Hence the answer is 0.

 

**Constraints:**

	- `1 <= nums.length <= 10^​​​​​​​5`
	- `1 <= nums[i] <= 10^​​​​​​​9`
	- `1 <= target <= 10^9`

<details markdown="1">
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Transform the problem: assign +1 to target positions, -1 to non-target positions. A subarray has target as majority iff the sum of transformed values > 0.

**Hint 1:** Create array where arr[i] = 1 if nums[i] == target, else -1.
**Hint 2:** A subarray [i, j] has target as majority iff prefix_sum[j+1] - prefix_sum[i] > 0.
**Hint 3:** Count pairs (i, j) where prefix_sum[j] > prefix_sum[i] and i < j. This is counting inversions in reverse.

**Approach:**
1. Transform nums: +1 for target, -1 for others
2. Compute prefix sums
3. Count pairs where prefix[j] > prefix[i] for i < j
4. Use merge sort or BIT to count such pairs efficiently

```python
def countSubarrays(nums, target):
  n = len(nums)

  # Transform: +1 for target, -1 for others
  arr = [1 if x == target else -1 for x in nums]

  # Compute prefix sums (with prefix[0] = 0)
  prefix = [0] * (n + 1)
  for i in range(n):
    prefix[i + 1] = prefix[i] + arr[i]

  # Count pairs (i, j) where i < j and prefix[i] < prefix[j]
  # This is counting non-inversions (ascending pairs)
  def merge_count(arr):
    if len(arr) <= 1:
      return arr, 0

    mid = len(arr) // 2
    left, left_count = merge_count(arr[:mid])
    right, right_count = merge_count(arr[mid:])

    count = left_count + right_count
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
      if left[i] < right[j]:
        # All remaining right elements are greater than left[i]
        count += len(right) - j
        merged.append(left[i])
        i += 1
      else:
        merged.append(right[j])
        j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged, count

  _, result = merge_count(prefix)
  return result
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

</details>

---

