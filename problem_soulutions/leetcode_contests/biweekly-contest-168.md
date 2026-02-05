---
layout: simple
title: "Biweekly Contest 168"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-168/
---

# Biweekly Contest 168

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | October 25, 2025 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-168/) |

---

## Problems

### Q1. Lexicographically Smallest String After Reverse

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/lexicographically-smallest-string-after-reverse/) |

#### Problem Description

You are given a string `s` of length `n` consisting of lowercase English letters.

You must perform **exactly** one operation by choosing any integer `k` such that `1 <= k <= n` and either:

	- reverse the **first** `k` characters of `s`, or
	- reverse the **last** `k` characters of `s`.

Return the **lexicographically smallest** string that can be obtained after **exactly** one such operation.

 

**Example 1:**

**Input:** s = "dcab"

**Output:** "acdb"

**Explanation:**

	- Choose `k = 3`, reverse the first 3 characters.
	- Reverse `"dca"` to `"acd"`, resulting string `s = "acdb"`, which is the lexicographically smallest string achievable.

**Example 2:**

**Input:** s = "abba"

**Output:** "aabb"

**Explanation:**

	- Choose `k = 3`, reverse the last 3 characters.
	- Reverse `"bba"` to `"abb"`, so the resulting string is `"aabb"`, which is the lexicographically smallest string achievable.

**Example 3:**

**Input:** s = "zxy"

**Output:** "xzy"

**Explanation:**

	- Choose `k = 2`, reverse the first 2 characters.
	- Reverse `"zx"` to `"xz"`, so the resulting string is `"xzy"`, which is the lexicographically smallest string achievable.

 

**Constraints:**

	- `1 <= n == s.length <= 1000`
	- `s` consists of lowercase English letters.

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** We must perform exactly one reverse operation. Try all possible reverses and pick the lexicographically smallest result.

**Hint 1:** For reversing first k characters: result = s[:k][::-1] + s[k:]
**Hint 2:** For reversing last k characters: result = s[:-k] + s[-k:][::-1]
**Hint 3:** Try all k from 1 to n for both operations and track the minimum.

**Approach:**
1. Initialize the answer as the original string (which happens with k=1 for either operation)
2. Try reversing first k characters for k = 1 to n
3. Try reversing last k characters for k = 1 to n
4. Return the lexicographically smallest result

```python
def lexicographicallySmallestString(s):
  n = len(s)
  result = s  # k=1 gives original string

  # Try reversing first k characters
  for k in range(1, n + 1):
    candidate = s[:k][::-1] + s[k:]
    if candidate < result:
      result = candidate

  # Try reversing last k characters
  for k in range(1, n + 1):
    candidate = s[:-k] + s[-k:][::-1] if k < n else s[::-1]
    if candidate < result:
      result = candidate

  return result
```

**Optimized version:**
```python
def lexicographicallySmallestString(s):
  n = len(s)
  candidates = []

  for k in range(1, n + 1):
    candidates.append(s[:k][::-1] + s[k:])  # Reverse first k
    candidates.append(s[:n-k] + s[n-k:][::-1])  # Reverse last k

  return min(candidates)
```

**Time Complexity:** O(n^2) for generating and comparing all candidates
**Space Complexity:** O(n) for storing candidates

</details>

---

### Q2. Maximize Sum of Squares of Digits

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/maximize-sum-of-squares-of-digits/) |

#### Problem Description

You are given two **positive** integers `num` and `sum`.

A positive integer `n` is **good** if it satisfies both of the following:

	- The number of digits in `n` is **exactly** `num`.
	- The sum of digits in `n` is **exactly** `sum`.

The **score** of a **good** integer `n` is the sum of the squares of digits in `n`.

Return a **string** denoting the **good** integer `n` that achieves the **maximum** **score**. If there are multiple possible integers, return the **maximum **​​​​​​​one. If no such integer exists, return an empty string.

 

**Example 1:**

**Input:** num = 2, sum = 3

**Output:** "30"

**Explanation:**

There are 3 good integers: 12, 21, and 30.

	- The score of 12 is `1^2 + 2^2 = 5`.
	- The score of 21 is `2^2 + 1^2 = 5`.
	- The score of 30 is `3^2 + 0^2 = 9`.

The maximum score is 9, which is achieved by the good integer 30. Therefore, the answer is `"30"`.

**Example 2:**

**Input:** num = 2, sum = 17

**Output:** "98"

**Explanation:**

There are 2 good integers: 89 and 98.

	- The score of 89 is `8^2 + 9^2 = 145`.
	- The score of 98 is `9^2 + 8^2 = 145`.

The maximum score is 145. The maximum good integer that achieves this score is 98. Therefore, the answer is `"98"`.

**Example 3:**

**Input:** num = 1, sum = 10

**Output:** ""

**Explanation:**

There are no integers that have exactly 1 digit and whose digits sum to 10. Therefore, the answer is `""`.

 

**Constraints:**

	- `1 <= num <= 2 * 10^5`
	- `1 <= sum <= 2 * 10^6`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** To maximize sum of squares, we want digits as large as possible since f(x)=x^2 is convex. Place 9s first, then fill remaining with what's needed.

**Hint 1:** First check feasibility: sum must be between 1 and 9*num (can't have leading zero).
**Hint 2:** For max score, use as many 9s as possible. If sum >= 9, place a 9.
**Hint 3:** To get the maximum number (for ties), place larger digits at the front.

**Approach:**
1. Check if solution exists: 1 <= sum <= 9*num
2. Greedily place digits from left to right
3. At each position, place the largest digit possible while ensuring remaining positions can still sum to remaining value

```python
def maxSumOfSquares(num, sum_val):
  # Check feasibility
  # First digit must be >= 1, remaining can be 0-9
  if sum_val < 1 or sum_val > 9 * num:
    return ""

  result = []
  remaining_sum = sum_val
  remaining_pos = num

  for i in range(num):
    remaining_pos -= 1
    # Min digit at this position: ensures remaining can reach remaining_sum
    min_digit = 0 if i > 0 else 1  # First digit can't be 0
    # Max sum achievable with remaining positions
    max_remaining = 9 * remaining_pos

    # Find the largest digit we can place
    for d in range(9, min_digit - 1, -1):
      if d <= remaining_sum and remaining_sum - d <= max_remaining:
        # Also ensure first digit is not 0
        if i == 0 and d == 0:
          continue
        result.append(str(d))
        remaining_sum -= d
        break
    else:
      return ""

  return ''.join(result)
```

**Alternative greedy approach:**
```python
def maxSumOfSquares(num, sum_val):
  if sum_val < 1 or sum_val > 9 * num:
    return ""

  digits = []
  remaining = sum_val

  for i in range(num):
    # Positions left after this one
    left = num - i - 1
    # Try placing largest possible digit
    for d in range(9, -1, -1):
      # First digit can't be 0
      if i == 0 and d == 0:
        continue
      new_remaining = remaining - d
      # Check if remaining positions can achieve new_remaining
      if 0 <= new_remaining <= 9 * left:
        digits.append(str(d))
        remaining = new_remaining
        break

  return ''.join(digits) if remaining == 0 else ""
```

**Time Complexity:** O(num)
**Space Complexity:** O(num)

</details>

---

### Q3. Minimum Operations to Transform Array

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-operations-to-transform-array/) |

#### Problem Description

You are given two integer arrays `nums1` of length `n` and `nums2` of length `n + 1`.

You want to transform `nums1` into `nums2` using the **minimum** number of operations.

You may perform the following operations **any** number of times, each time choosing an index `i`:

	- **Increase** `nums1[i]` by 1.
	- **Decrease** `nums1[i]` by 1.
	- **Append** `nums1[i]` to the **end** of the array.

Return the **minimum** number of operations required to transform `nums1` into `nums2`.

 

**Example 1:**

**Input:** nums1 = [2,8], nums2 = [1,7,3]

**Output:** 4

**Explanation:**

	
		
			Step
			`i`
			Operation
			`nums1[i]`
			Updated `nums1`
		
	
	
		
			1
			0
			Append
			-
			[2, 8, 2]
		
		
			2
			0
			Decrement
			Decreases to 1
			[1, 8, 2]
		
		
			3
			1
			Decrement
			Decreases to 7
			[1, 7, 2]
		
		
			4
			2
			Increment
			Increases to 3
			[1, 7, 3]
		
	

Thus, after 4 operations `nums1` is transformed into `nums2`.

**Example 2:**

**Input:** nums1 = [1,3,6], nums2 = [2,4,5,3]

**Output:** 4

**Explanation:**

	
		
			Step
			`i`
			Operation
			`nums1[i]`
			Updated `nums1`
		
	
	
		
			1
			1
			Append
			-
			[1, 3, 6, 3]
		
		
			2
			0
			Increment
			Increases to 2
			[2, 3, 6, 3]
		
		
			3
			1
			Increment
			Increases to 4
			[2, 4, 6, 3]
		
		
			4
			2
			Decrement
			Decreases to 5
			[2, 4, 5, 3]
		
	

Thus, after 4 operations `nums1` is transformed into `nums2`.

**Example 3:**

**Input:** nums1 = [2], nums2 = [3,4]

**Output:** 3

**Explanation:**

	
		
			Step
			`i`
			Operation
			`nums1[i]`
			Updated `nums1`
		
	
	
		
			1
			0
			Increment
			Increases to 3
			[3]
		
		
			2
			0
			Append
			-
			[3, 3]
		
		
			3
			1
			Increment
			Increases to 4
			[3, 4]
		
	

Thus, after 3 operations `nums1` is transformed into `nums2`.

 

**Constraints:**

	- `1 <= n == nums1.length <= 10^5`
	- `nums2.length == n + 1`
	- `1 <= nums1[i], nums2[i] <= 10^5`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** We need to match each position in nums2 with a position in nums1. One element from nums1 must be duplicated (via append). Find optimal matching.

**Hint 1:** Since nums2 has n+1 elements and nums1 has n, we must append exactly one element from nums1.
**Hint 2:** Try each possible matching of nums1 positions to nums2 positions, with one nums1 element used twice.
**Hint 3:** For each element in nums1, calculate cost = |nums1[i] - nums2[j]| for matching i to j.

**Approach:**
1. For each nums1[i], we can assign it to any nums2[j]
2. One nums1[i] will be appended (used for a second position)
3. Use greedy or DP: sort and try to minimize total cost
4. Key insight: each nums1[i] maps to exactly one or two nums2 positions

```python
def minOperations(nums1, nums2):
  n = len(nums1)
  # nums2 has n+1 elements

  # Try each position in nums1 as the one to duplicate
  min_cost = float('inf')

  for dup_idx in range(n):
    # We'll use nums1[dup_idx] for two positions in nums2
    # Greedy matching: sort both and match
    # Actually, optimal is to match sorted arrays

    # Cost for matching nums1[i] to nums2[i] for i in [0, n)
    # and nums1[dup_idx] to nums2[n]
    # But positions matter!

    pass

  # Better approach: DP or observe structure
  # Actually, the positions correspond directly!
  # nums1[i] -> nums2[i], and one nums1[j] -> nums2[n] via append

  # Cost = sum(|nums1[i] - nums2[i]|) + |nums1[j] - nums2[n]|
  # where j is chosen optimally

  base_cost = sum(abs(nums1[i] - nums2[i]) for i in range(n))

  # Find best j to duplicate for position n
  min_total = float('inf')
  for j in range(n):
    cost = base_cost + abs(nums1[j] - nums2[n])
    min_total = min(min_total, cost)

  return min_total
```

**Corrected optimal solution:**
```python
def minOperations(nums1, nums2):
  n = len(nums1)

  # Base cost: match nums1[i] to nums2[i] directly
  base_cost = sum(abs(nums1[i] - nums2[i]) for i in range(n))

  # Additional cost: duplicate one nums1[j] for nums2[n]
  min_extra = min(abs(nums1[j] - nums2[n]) for j in range(n))

  return base_cost + min_extra
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

</details>

---

### Q4. Count Ways to Choose Coprime Integers from Rows

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/count-ways-to-choose-coprime-integers-from-rows/) |

#### Problem Description

You are given a `m x n` matrix `mat` of positive integers.

Return an integer denoting the number of ways to choose **exactly one** integer from each row of `mat` such that the **greatest common divisor** of all chosen integers is 1.

Since the answer may be very large, return it **modulo** `10^9 + 7`.

 

**Example 1:**

**Input:** mat = [[1,2],[3,4]]

**Output:** 3

**Explanation:**

	
		
			Chosen integer in the first row
			Chosen integer in the second row
			Greatest common divisor of chosen integers
		
		
			1
			3
			1
		
		
			1
			4
			1
		
		
			2
			3
			1
		
		
			2
			4
			2
		
	

3 of these combinations have a greatest common divisor of 1. Therefore, the answer is 3.

**Example 2:**

**Input:** mat = [[2,2],[2,2]]

**Output:** 0

**Explanation:**

Every combination has a greatest common divisor of 2. Therefore, the answer is 0.

 

**Constraints:**

	- `1 <= m == mat.length <= 150`
	- `1 <= n == mat[i].length <= 150`
	- `1 <= mat[i][j] <= 150`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Use DP with GCD as state. Since values are at most 150, there are at most 150 distinct GCD values possible.

**Hint 1:** Track counts of each possible GCD value as we process rows.
**Hint 2:** When processing a new row, for each (prev_gcd, count) pair and each element in the row, compute new GCD.
**Hint 3:** The answer is the count of ways where final GCD = 1.

**Approach:**
1. Initialize DP: dp[g] = number of ways to achieve GCD = g
2. For each row, compute new DP based on previous DP and current row elements
3. For each prev_gcd and each element in current row, new_gcd = gcd(prev_gcd, element)
4. Final answer is dp[1]

```python
def countWays(mat):
  from math import gcd
  from collections import defaultdict

  MOD = 10**9 + 7
  m, n = len(mat), len(mat[0])

  # dp[g] = number of ways to achieve gcd = g
  dp = defaultdict(int)

  # Initialize with first row
  for val in mat[0]:
    dp[val] = (dp[val] + 1) % MOD

  # Process remaining rows
  for row_idx in range(1, m):
    new_dp = defaultdict(int)
    for prev_gcd, count in dp.items():
      for val in mat[row_idx]:
        new_gcd = gcd(prev_gcd, val)
        new_dp[new_gcd] = (new_dp[new_gcd] + count) % MOD
    dp = new_dp

  return dp[1]
```

**Optimized with array instead of dict:**
```python
def countWays(mat):
  from math import gcd

  MOD = 10**9 + 7
  m, n = len(mat), len(mat[0])
  MAX_VAL = 151

  # dp[g] = number of ways to achieve gcd = g
  dp = [0] * MAX_VAL

  # Initialize with first row
  for val in mat[0]:
    dp[val] = (dp[val] + 1) % MOD

  # Process remaining rows
  for row_idx in range(1, m):
    new_dp = [0] * MAX_VAL
    for prev_gcd in range(1, MAX_VAL):
      if dp[prev_gcd] == 0:
        continue
      for val in mat[row_idx]:
        new_gcd = gcd(prev_gcd, val)
        new_dp[new_gcd] = (new_dp[new_gcd] + dp[prev_gcd]) % MOD
    dp = new_dp

  return dp[1]
```

**Time Complexity:** O(m * n * MAX_VAL) where MAX_VAL = 150
**Space Complexity:** O(MAX_VAL)

</details>

---

