---
layout: simple
title: "Biweekly Contest 170"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-170/
---

# Biweekly Contest 170

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | November 22, 2025 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-170/) |

---

## Problems

### Q1. Minimum Number of Flips to Reverse Binary String

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-number-of-flips-to-reverse-binary-string/) |

#### Problem Description

You are given a **positive** integer `n`.

Let `s` be the **binary representation** of `n` without leading zeros.

The **reverse** of a binary string `s` is obtained by writing the characters of `s` in the opposite order.

You may flip any bit in `s` (change `0 → 1` or `1 → 0`). Each flip affects **exactly** one bit.

Return the **minimum** number of flips required to make `s` equal to the reverse of its original form.

 

**Example 1:**

**Input:** n = 7

**Output:** 0

**Explanation:**

The binary representation of 7 is `"111"`. Its reverse is also `"111"`, which is the same. Hence, no flips are needed.

**Example 2:**

**Input:** n = 10

**Output:** 4

**Explanation:**

The binary representation of 10 is `"1010"`. Its reverse is `"0101"`. All four bits must be flipped to make them equal. Thus, the minimum number of flips required is 4.

 

**Constraints:**

	- `1 <= n <= 10^9`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** We need to make the binary string equal to its reverse. Compare s[i] with s[n-1-i] and count mismatches.

**Hint 1:** Convert n to binary and compare with its reverse.
**Hint 2:** The minimum flips equals the number of positions where the original and reversed strings differ.
**Hint 3:** This is simply counting the Hamming distance between s and reversed(s).

**Approach:**
1. Convert n to its binary representation (without leading zeros)
2. Reverse the binary string
3. Count positions where the two strings differ
4. Return the count

```python
def minFlips(n):
  s = bin(n)[2:]  # Binary without '0b' prefix
  rev = s[::-1]

  flips = 0
  for i in range(len(s)):
    if s[i] != rev[i]:
      flips += 1

  return flips
```

**Time Complexity:** O(log n) for the number of bits
**Space Complexity:** O(log n) for storing the binary string

</details>

---

### Q2. Total Waviness of Numbers in Range I

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/total-waviness-of-numbers-in-range-i/) |

#### Problem Description

You are given two integers `num1` and `num2` representing an **inclusive** range `[num1, num2]`.

The **waviness** of a number is defined as the total count of its **peaks** and **valleys**:

	- A digit is a **peak** if it is **strictly greater** than both of its immediate neighbors.
	- A digit is a **valley** if it is **strictly less** than both of its immediate neighbors.
	- The first and last digits of a number **cannot** be peaks or valleys.
	- Any number with fewer than 3 digits has a waviness of 0.

Return the total sum of waviness for all numbers in the range `[num1, num2]`.

 

**Example 1:**

**Input:** num1 = 120, num2 = 130

**Output:** 3

**Explanation:**

In the range `[120, 130]`:

	- `120`: middle digit 2 is a peak, waviness = 1.
	- `121`: middle digit 2 is a peak, waviness = 1.
	- `130`: middle digit 3 is a peak, waviness = 1.
	- All other numbers in the range have a waviness of 0.

Thus, total waviness is `1 + 1 + 1 = 3`.

**Example 2:**

**Input:** num1 = 198, num2 = 202

**Output:** 3

**Explanation:**

In the range `[198, 202]`:

	- `198`: middle digit 9 is a peak, waviness = 1.
	- `201`: middle digit 0 is a valley, waviness = 1.
	- `202`: middle digit 0 is a valley, waviness = 1.
	- All other numbers in the range have a waviness of 0.

Thus, total waviness is `1 + 1 + 1 = 3`.

**Example 3:**

**Input:** num1 = 4848, num2 = 4848

**Output:** 2

**Explanation:**

Number `4848`: the second digit 8 is a peak, and the third digit 4 is a valley, giving a waviness of 2.

 

**Constraints:**

	- `1 <= num1 <= num2 <= 10^5`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** With small constraints (up to 10^5), we can iterate through each number and compute its waviness directly.

**Hint 1:** For each number, convert to string and check each middle digit.
**Hint 2:** A digit at position i (not first or last) is a peak if digits[i-1] < digits[i] > digits[i+1].
**Hint 3:** A digit at position i is a valley if digits[i-1] > digits[i] < digits[i+1].

**Approach:**
1. Iterate through each number in [num1, num2]
2. For each number, convert to string of digits
3. For each middle position, check if it's a peak or valley
4. Sum all waviness values

```python
def totalWaviness(num1, num2):
  def waviness(n):
    s = str(n)
    if len(s) < 3:
      return 0
    count = 0
    for i in range(1, len(s) - 1):
      prev, curr, next_ = int(s[i-1]), int(s[i]), int(s[i+1])
      # Peak: strictly greater than both neighbors
      if curr > prev and curr > next_:
        count += 1
      # Valley: strictly less than both neighbors
      elif curr < prev and curr < next_:
        count += 1
    return count

  total = 0
  for num in range(num1, num2 + 1):
    total += waviness(num)
  return total
```

**Time Complexity:** O((num2 - num1) * d) where d is the max number of digits
**Space Complexity:** O(d) for the string conversion

</details>

---

### Q3. Lexicographically Smallest Negated Permutation that Sums to Target

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/lexicographically-smallest-negated-permutation-that-sums-to-target/) |

#### Problem Description

You are given a positive integer `n` and an integer `target`.

Return the **lexicographically smallest** array of integers of size `n` such that:

	- The **sum** of its elements equals `target`.
	- The **absolute values** of its elements form a **permutation** of size `n`.

If no such array exists, return an empty array.

A **permutation** of size `n` is a rearrangement of integers `1, 2, ..., n`.

 

**Example 1:**

**Input:** n = 3, target = 0

**Output:** [-3,1,2]

**Explanation:**

The arrays that sum to 0 and whose absolute values form a permutation of size 3 are:

	- `[-3, 1, 2]`
	- `[-3, 2, 1]`
	- `[-2, -1, 3]`
	- `[-2, 3, -1]`
	- `[-1, -2, 3]`
	- `[-1, 3, -2]`
	- `[1, -3, 2]`
	- `[1, 2, -3]`
	- `[2, -3, 1]`
	- `[2, 1, -3]`
	- `[3, -2, -1]`
	- `[3, -1, -2]`

The lexicographically smallest one is `[-3, 1, 2]`.

**Example 2:**

**Input:** n = 1, target = 10000000000

**Output:** []

**Explanation:**

There are no arrays that sum to 10000000000 and whose absolute values form a permutation of size 1. Therefore, the answer is `[]`.

 

**Constraints:**

	- `1 <= n <= 10^5`
	- `-10^10 <= target <= 10^10`

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** The sum of 1+2+...+n = n(n+1)/2. If we negate some numbers, the sum changes by -2*x for each negated number x. So we need to find which numbers to negate.

**Hint 1:** Total sum S = n(n+1)/2. If we negate a subset with sum X, new sum = S - 2X. So target = S - 2X, meaning X = (S - target)/2.
**Hint 2:** Check if (S - target) is even and non-negative, and X <= S.
**Hint 3:** Greedily pick largest numbers first for negation (to make lexicographically smallest result), then assign remaining numbers.

**Approach:**
1. Calculate S = n(n+1)/2
2. Check if (S - target)/2 is a valid sum we can form (X must be between 0 and S, and (S-target) must be even)
3. Use greedy: to get lexicographically smallest, we want negative numbers first (smaller values are better at the front)
4. Find which numbers to negate such that their sum equals X

```python
def lexicographicallySmallestPermutation(n, target):
  S = n * (n + 1) // 2

  # target = S - 2X, so X = (S - target) / 2
  diff = S - target
  if diff < 0 or diff % 2 != 0:
    return []

  X = diff // 2
  if X > S:
    return []

  # Find which numbers to negate (their sum should be X)
  # Greedy: pick from largest to smallest
  to_negate = set()
  remaining = X
  for i in range(n, 0, -1):
    if i <= remaining:
      to_negate.add(i)
      remaining -= i

  if remaining != 0:
    return []

  # Build result: for lexicographically smallest,
  # place negative numbers (sorted) first, then positive numbers (sorted)
  negatives = sorted([-x for x in to_negate])
  positives = sorted([x for x in range(1, n + 1) if x not in to_negate])

  return negatives + positives
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q4. Total Waviness of Numbers in Range II

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii/) |

#### Problem Description

You are given two integers `num1` and `num2` representing an **inclusive** range `[num1, num2]`.

The **waviness** of a number is defined as the total count of its **peaks** and **valleys**:

	- A digit is a **peak** if it is **strictly greater** than both of its immediate neighbors.
	- A digit is a **valley** if it is **strictly less** than both of its immediate neighbors.
	- The first and last digits of a number **cannot** be peaks or valleys.
	- Any number with fewer than 3 digits has a waviness of 0.

Return the total sum of waviness for all numbers in the range `[num1, num2]`.

 

**Example 1:**

**Input:** num1 = 120, num2 = 130

**Output:** 3

**Explanation:**

In the range `[120, 130]`:

	- `120`: middle digit 2 is a peak, waviness = 1.
	- `121`: middle digit 2 is a peak, waviness = 1.
	- `130`: middle digit 3 is a peak, waviness = 1.
	- All other numbers in the range have a waviness of 0.

Thus, total waviness is `1 + 1 + 1 = 3`.

**Example 2:**

**Input:** num1 = 198, num2 = 202

**Output:** 3

**Explanation:**

In the range `[198, 202]`:

	- `198`: middle digit 9 is a peak, waviness = 1.
	- `201`: middle digit 0 is a valley, waviness = 1.
	- `202`: middle digit 0 is a valley, waviness = 1.
	- All other numbers in the range have a waviness of 0.

Thus, total waviness is `1 + 1 + 1 = 3`.

**Example 3:**

**Input:** num1 = 4848, num2 = 4848

**Output:** 2

**Explanation:**

Number `4848`: the second digit 8 is a peak, and the third digit 4 is a valley, giving a waviness of 2.

 

**Constraints:**

	- `1 <= num1 <= num2 <= 10^15`​​​​​​​

<details>
<summary><strong>Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** With range up to 10^15, we cannot iterate through each number. Use digit DP to count waviness efficiently.

**Hint 1:** Use digit DP with states: current position, previous digit, second previous digit, tight constraint, and whether we've started.
**Hint 2:** Track both count of numbers and sum of waviness. A digit contributes to waviness if it forms a peak or valley.
**Hint 3:** Compute totalWaviness(num2) - totalWaviness(num1 - 1) to get the answer for the range.

**Approach:**
1. Implement digit DP that tracks: position, prev digit, prev-prev digit, tight bound, leading zeros
2. At each position, check if prev digit forms a peak/valley (needs prev-prev and current digit)
3. Track both count of valid numbers and sum of waviness contributions
4. Use inclusion-exclusion: answer = f(num2) - f(num1-1)

```python
def totalWaviness(num1, num2):
  from functools import lru_cache

  def solve(num):
    if num < 100:
      return 0
    digits = [int(d) for d in str(num)]
    n = len(digits)

    @lru_cache(maxsize=None)
    def dp(pos, prev2, prev1, tight, started):
      # Returns (count, waviness_sum)
      if pos == n:
        return (1, 0) if started else (0, 0)

      limit = digits[pos] if tight else 9
      total_count, total_waviness = 0, 0

      for d in range(0, limit + 1):
        new_tight = tight and (d == limit)
        new_started = started or (d > 0)

        if not new_started:
          cnt, wav = dp(pos + 1, -1, -1, new_tight, False)
        elif not started and d > 0:
          cnt, wav = dp(pos + 1, -1, d, new_tight, True)
        elif prev1 == -1:
          cnt, wav = dp(pos + 1, -1, d, new_tight, True)
        else:
          cnt, wav = dp(pos + 1, prev1, d, new_tight, True)
          # Check if prev1 is a peak or valley
          if prev2 != -1:
            if prev2 < prev1 > d or prev2 > prev1 < d:
              wav += cnt

        total_count += cnt
        total_waviness += wav

      return (total_count, total_waviness)

    _, result = dp(0, -1, -1, True, False)
    return result

  return solve(num2) - solve(num1 - 1)
```

**Time Complexity:** O(d * 10^3) where d is number of digits (up to 16)
**Space Complexity:** O(d * 10^2) for memoization

</details>

---

