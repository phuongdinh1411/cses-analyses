---
layout: simple
title: "Biweekly Contest 171"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-171/
---

# Biweekly Contest 171

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | December 06, 2025 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-171/) |

---

## Problems

### Q1. Complete Prime Number

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/complete-prime-number/) |

#### Problem Description

You are given an integer `num`.

A number `num` is called a **Complete Prime Number** if every **prefix** and every **suffix** of `num` is **prime**.

Return `true` if `num` is a Complete Prime Number, otherwise return `false`.

**Note**:

	- A **prefix** of a number is formed by the **first** `k` digits of the number.
	- A **suffix** of a number is formed by the **last** `k` digits of the number.
	- Single-digit numbers are considered Complete Prime Numbers only if they are **prime**.

 

**Example 1:**

**Input:** num = 23

**Output:** true

**Explanation:**

	- **​​​​​​​**Prefixes of `num = 23` are 2 and 23, both are prime.
	- Suffixes of `num = 23` are 3 and 23, both are prime.
	- All prefixes and suffixes are prime, so 23 is a Complete Prime Number and the answer is `true`.

**Example 2:**

**Input:** num = 39

**Output:** false

**Explanation:**

	- Prefixes of `num = 39` are 3 and 39. 3 is prime, but 39 is not prime.
	- Suffixes of `num = 39` are 9 and 39. Both 9 and 39 are not prime.
	- At least one prefix or suffix is not prime, so 39 is not a Complete Prime Number and the answer is `false`.

**Example 3:**

**Input:** num = 7

**Output:** true

**Explanation:**

	- 7 is prime, so all its prefixes and suffixes are prime and the answer is `true`.

 

**Constraints:**

	- `1 <= num <= 10^9`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** A number is a Complete Prime Number if and only if every prefix and every suffix of its digits forms a prime number.

**Hint 1:** Convert the number to a string to easily extract prefixes and suffixes.
**Hint 2:** For each prefix (first k digits) and suffix (last k digits), convert back to integer and check if prime.
**Hint 3:** Use a simple primality test - for numbers up to 10^9, checking divisibility up to sqrt(n) is efficient.

**Approach:**
1. Convert the number to a string
2. Generate all prefixes (s[:1], s[:2], ..., s[:n])
3. Generate all suffixes (s[-1:], s[-2:], ..., s[-n:])
4. For each prefix and suffix, check if it's prime
5. Return true only if all prefixes and suffixes are prime

```python
def isCompletePrime(num):
  def is_prime(n):
    if n < 2:
      return False
    if n == 2:
      return True
    if n % 2 == 0:
      return False
    for i in range(3, int(n**0.5) + 1, 2):
      if n % i == 0:
        return False
    return True

  s = str(num)
  n = len(s)

  # Check all prefixes
  for i in range(1, n + 1):
    prefix = int(s[:i])
    if not is_prime(prefix):
      return False

  # Check all suffixes
  for i in range(1, n + 1):
    suffix = int(s[-i:])
    if not is_prime(suffix):
      return False

  return True
```

**Time Complexity:** O(d * sqrt(num)) where d is the number of digits
**Space Complexity:** O(d) for storing the string representation

</details>

---

### Q2. Minimum Operations to Make Binary Palindrome

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-operations-to-make-binary-palindrome/) |

#### Problem Description

You are given an integer array `nums`.

For each element `nums[i]`, you may perform the following operations **any** number of times (including zero):

	- Increase `nums[i]` by 1, or
	- Decrease `nums[i]` by 1.

A number is called a **binary palindrome** if its binary representation without leading zeros reads the same forward and backward.

Your task is to return an integer array `ans`, where `ans[i]` represents the **minimum** number of operations required to convert `nums[i]` into a **binary palindrome**.

 

**Example 1:**

**Input:** nums = [1,2,4]

**Output:** [0,1,1]

**Explanation:**

One optimal set of operations:

	
		
			`nums[i]`
			Binary(`nums[i]`)
			Nearest

			Palindrome
			Binary

			(Palindrome)
			Operations Required
			`ans[i]`
		
	
	
		
			1
			1
			1
			1
			Already palindrome
			0
		
		
			2
			10
			3
			11
			Increase by 1
			1
		
		
			4
			100
			3
			11
			Decrease by 1
			1
		
	

Thus, `ans = [0, 1, 1]`.

**Example 2:**

**Input:** nums = [6,7,12]

**Output:** [1,0,3]

**Explanation:**

One optimal set of operations:

	
		
			`nums[i]`
			Binary(`nums[i]`)
			Nearest

			Palindrome
			Binary

			(Palindrome)
			Operations Required
			`ans[i]`
		
	
	
		
			6
			110
			5
			101
			Decrease by 1
			1
		
		
			7
			111
			7
			111
			Already palindrome
			0
		
		
			12
			1100
			15
			1111
			Increase by 3
			3
		
	

Thus, `ans = [1, 0, 3]`.

 

**Constraints:**

	- `1 <= nums.length <= 5000`
	- `^​​​​​​​1 <= nums[i] <=^ 5000`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Since nums[i] <= 5000, we can precompute all binary palindromes up to a reasonable range and use binary search to find the nearest one.

**Hint 1:** A binary palindrome reads the same forward and backward in binary (e.g., 5 = "101", 7 = "111").
**Hint 2:** Precompute all binary palindromes up to around 10000 (to cover nearest neighbors for values up to 5000).
**Hint 3:** For each number, find the closest binary palindrome using binary search or linear scan.

**Approach:**
1. Generate all binary palindromes up to a safe upper bound
2. For each number in nums, find the nearest binary palindrome
3. Return the absolute difference as the number of operations

```python
def minOperations(nums):
  def is_binary_palindrome(n):
    b = bin(n)[2:]
    return b == b[::-1]

  # Precompute all binary palindromes up to 10000+
  palindromes = []
  for i in range(1, 10001):
    if is_binary_palindrome(i):
      palindromes.append(i)

  def find_nearest(n):
    # Binary search for closest palindrome
    import bisect
    idx = bisect.bisect_left(palindromes, n)
    candidates = []
    if idx < len(palindromes):
      candidates.append(palindromes[idx])
    if idx > 0:
      candidates.append(palindromes[idx - 1])
    return min(abs(n - c) for c in candidates)

  return [find_nearest(x) for x in nums]
```

**Time Complexity:** O(M + N * log(M)) where M is the number of binary palindromes and N is len(nums)
**Space Complexity:** O(M) for storing palindromes

</details>

---

### Q3. Maximize Points After Choosing K Tasks

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/maximize-points-after-choosing-k-tasks/) |

#### Problem Description

You are given two integer arrays, `technique1` and `technique2`, each of length `n`, where `n` represents the number of tasks to complete.

	- If the `i^th` task is completed using technique 1, you earn `technique1[i]` points.
	- If it is completed using technique 2, you earn `technique2[i]` points.

You are also given an integer `k`, representing the **minimum** number of tasks that **must** be completed using technique 1.

You **must** complete **at least** `k` tasks using technique 1 (they do not need to be the first `k` tasks).

The remaining tasks may be completed using **either** technique.

Return an integer denoting the **maximum total points** you can earn.

 

**Example 1:**

**Input:** technique1 = [5,2,10], technique2 = [10,3,8], k = 2

**Output:** 22

**Explanation:**

We must complete at least `k = 2` tasks using `technique1`.

Choosing `technique1[1]` and `technique1[2]` (completed using technique 1), and `technique2[0]` (completed using technique 2), yields the maximum points: `2 + 10 + 10 = 22`.

**Example 2:**

**Input:** technique1 = [10,20,30], technique2 = [5,15,25], k = 2

**Output:** 60

**Explanation:**

We must complete at least `k = 2` tasks using `technique1`.

Choosing all tasks using technique 1 yields the maximum points: `10 + 20 + 30 = 60`.

**Example 3:**

**Input:** technique1 = [1,2,3], technique2 = [4,5,6], k = 0

**Output:** 15

**Explanation:**

Since `k = 0`, we are not required to choose any task using `technique1`.

Choosing all tasks using technique 2 yields the maximum points: `4 + 5 + 6 = 15`.

 

**Constraints:**

	- `1 <= n == technique1.length == technique2.length <= 10^5`
	- `1 <= technique1[i], technique2​​​​​​​[i] <= 10^​​​​​​​5`
	- `0 <= k <= n`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** For each task, compute the "gain" of using technique2 over technique1 (t2[i] - t1[i]). We must use technique1 for at least k tasks, so we should pick the k tasks with the smallest gain (or largest loss) for technique1.

**Hint 1:** Start by assuming we use technique2 for all tasks to get maximum base score.
**Hint 2:** We must "sacrifice" some tasks to technique1 - pick the k tasks where switching hurts the least.
**Hint 3:** Sort tasks by the difference (technique2[i] - technique1[i]) and select the k smallest differences.

**Approach:**
1. Compute the total if we use technique2 for all tasks
2. Calculate diff[i] = technique2[i] - technique1[i] for each task
3. Sort diffs in ascending order
4. For the k smallest diffs, we "switch" from technique2 to technique1
5. The answer is sum(technique2) - sum of k smallest diffs

```python
def maxPoints(technique1, technique2, k):
  n = len(technique1)

  # Start with all technique2
  total = sum(technique2)

  # Calculate the cost of switching from technique2 to technique1
  # If diff[i] > 0, we lose points by switching to technique1
  # If diff[i] < 0, we gain points by switching to technique1
  diffs = [technique2[i] - technique1[i] for i in range(n)]

  # Sort and take k smallest (most beneficial to switch)
  diffs.sort()

  # Switch k tasks to technique1
  for i in range(k):
    total -= diffs[i]

  return total
```

**Time Complexity:** O(n log n) for sorting
**Space Complexity:** O(n) for storing differences

</details>

---

### Q4. Minimum Inversion Count in Subarrays of Fixed Length

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-inversion-count-in-subarrays-of-fixed-length/) |

#### Problem Description

You are given an integer array `nums` of length `n` and an integer `k`.

An **inversion** is a pair of indices `(i, j)` from `nums` such that `i < j` and `nums[i] > nums[j]`.

The **inversion count** of a **subarray** is the number of inversions within it.

Return the **minimum** inversion count among all **subarrays** of `nums` with length `k`.

 

**Example 1:**

**Input:** nums = [3,1,2,5,4], k = 3

**Output:** 0

**Explanation:**

We consider all subarrays of length `k = 3` (indices below are relative to each subarray):

	- `[3, 1, 2]` has 2 inversions: `(0, 1)` and `(0, 2)`.
	- `[1, 2, 5]` has 0 inversions.
	- `[2, 5, 4]` has 1 inversion: `(1, 2)`.

The minimum inversion count among all subarrays of length `3` is 0, achieved by subarray `[1, 2, 5]`.

**Example 2:**

**Input:** nums = [5,3,2,1], k = 4

**Output:** 6

**Explanation:**

There is only one subarray of length `k = 4`: `[5, 3, 2, 1]`.

Within this subarray, the inversions are: `(0, 1)`, `(0, 2)`, `(0, 3)`, `(1, 2)`, `(1, 3)`, and `(2, 3)`.

Total inversions is 6, so the minimum inversion count is 6.

**Example 3:**

**Input:** nums = [2,1], k = 1

**Output:** 0

**Explanation:**

All subarrays of length `k = 1` contain only one element, so no inversions are possible.

The minimum inversion count is therefore 0.

 

**Constraints:**

	- `1 <= n == nums.length <= 10^5`
	- `1 <= nums[i] <= 10^9`
	- `1 <= k <= n`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Use a sliding window and maintain the inversion count efficiently. When sliding the window, we need to track how many elements are affected by adding/removing one element.

**Hint 1:** First compute the inversion count for the initial window using merge sort or BIT/Fenwick tree.
**Hint 2:** When sliding the window, the element leaving affects inversions with all elements that remain.
**Hint 3:** Use a data structure (BIT/sorted list) to efficiently count elements greater than or less than a given value.

**Approach:**
1. Use coordinate compression since values can be up to 10^9
2. Compute inversions for first window using a Fenwick tree
3. Slide the window: when removing left element, subtract inversions it contributed; when adding right element, add new inversions
4. Track minimum across all windows

```python
def minInversionCount(nums, k):
  from sortedcontainers import SortedList

  n = len(nums)
  if k == 1:
    return 0

  sl = SortedList()
  inversions = 0

  # Build initial window and count inversions
  for i in range(k):
    # Count elements greater than nums[i] already in window
    inversions += len(sl) - sl.bisect_right(nums[i])
    sl.add(nums[i])

  min_inv = inversions

  # Slide the window
  for i in range(k, n):
    # Remove nums[i-k] from window
    left = nums[i - k]
    # Count inversions involving left element
    # Elements less than left that come after it
    inversions -= sl.bisect_left(left)
    sl.remove(left)

    # Add nums[i] to window
    right = nums[i]
    # Count elements greater than right already in window
    inversions += len(sl) - sl.bisect_right(right)
    sl.add(right)

    min_inv = min(min_inv, inversions)

  return min_inv
```

**Time Complexity:** O(n log k) using SortedList operations
**Space Complexity:** O(k) for the sorted container

</details>

---

