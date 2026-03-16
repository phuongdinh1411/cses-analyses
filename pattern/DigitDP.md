---
layout: simple
title: "Digit DP — Counting Numbers with Properties"
permalink: /pattern/digit-dp
---

# Digit DP — Counting Numbers with Properties

A comprehensive walkthrough of the Digit DP technique and LeetCode problems that use it, from the core template to its variants.

---

## Pattern Overview

**Trigger**: "Count numbers in range [low, high] satisfying some digit property"

All problems share:
- **Range reduction**: `count(low, high) = count(0, high) - count(0, low - 1)`
- **Build digit by digit** from left to right
- **Four core parameters**: `pos`, `state`, `tight`, `started`
- **Memoization** with `lru_cache`

---

## Table of Contents

1. [Core Template](#1-core-template)
2. [Understanding Each Parameter](#2-understanding-each-parameter)
3. [Common State Choices](#3-common-state-choices)
4. [Problem 3791 — Balanced Integers in a Range](#4-problem-3791--balanced-integers-in-a-range)
5. [Problem 2376 — Count Special Integers](#5-problem-2376--count-special-integers)
6. [Problem 233 — Number of Digit One](#6-problem-233--number-of-digit-one)
7. [Problem 902 — Numbers At Most N Given Digit Set](#7-problem-902--numbers-at-most-n-given-digit-set)
8. [Problem 1012 — Numbers With Repeated Digits](#8-problem-1012--numbers-with-repeated-digits)
9. [Problem 2719 — Count of Integers (Digit Sum Bounds)](#9-problem-2719--count-of-integers-digit-sum-bounds)
10. [Problem 2827 — Number of Beautiful Integers](#10-problem-2827--number-of-beautiful-integers)
11. [Master Comparison Table](#11-master-comparison-table)
12. [How to Identify This Pattern](#12-how-to-identify-this-pattern)

---

## 1. Core Template

```python
from functools import lru_cache

def count(num):
    """Count numbers from 1 to num satisfying the property."""
    if num <= 0:
        return 0
    digits = [int(c) for c in str(num)]
    n = len(digits)

    @lru_cache(maxsize=None)
    def dp(pos, state, tight, started):
        """
        pos     — current digit position (0 to n-1)
        state   — problem-specific tracking
        tight   — are we still bounded by num's digits?
        started — have we placed a non-zero digit yet?
        """
        if pos == n:
            if not started:
                return 0             # number is 0, usually excluded
            return check(state)      # does this number satisfy the property?

        limit = digits[pos] if tight else 9
        result = 0

        for d in range(0, limit + 1):
            new_tight = tight and (d == limit)
            new_started = started or (d != 0)
            new_state = transition(state, d, new_started)

            result += dp(pos + 1, new_state, new_tight, new_started)

        return result

    ans = dp(0, initial_state, True, False)
    dp.cache_clear()
    return ans

# Final answer
answer = count(high) - count(low - 1)
```

The only thing that changes between problems:
- **`state`**: what you track (sum, diff, mask, remainder...)
- **`transition`**: how state updates when placing digit `d`
- **`check`**: what condition to verify at the end

---

## 2. Understanding Each Parameter

### `pos` — Current Position

```
digits of N = [3, 5, 2, 8, 1]
               0  1  2  3  4   ← pos moves left to right
```

We build the number one digit at a time, from the most significant.

### `tight` — Upper Bound Constraint

Controls which digits we can place at the current position.

```
N = 352

pos=0, tight=True, limit=3:
  d=0: tight=False (0 < 3, now free forever)
  d=1: tight=False (1 < 3)
  d=2: tight=False (2 < 3)
  d=3: tight=True  (3 == 3, still bounded)

pos=1 after placing 3, tight=True, limit=5:
  d=0..4: tight=False
  d=5:    tight=True → next digit limited to 2

pos=2 after placing 3,5, tight=True, limit=2:
  d=0..2: valid     (number ≤ 352)
  d=3..9: FORBIDDEN (would exceed 352)
```

**Rule**: `tight` stays True only if **every** digit placed so far equals N's corresponding digit.

### `started` — Leading Zeros

Handles the fact that `007` is actually `7` (a 1-digit number, not 3-digit).

```
started=False → still in leading zeros (haven't placed a real digit)
started=True  → placed at least one non-zero digit

Transition: new_started = started or (d != 0)
```

Without this, we'd incorrectly treat leading zeros as real digits, breaking problems that depend on digit count or position.

### `state` — Problem-Specific

This is what makes each problem unique. See next section.

---

## 3. Common State Choices

| Problem Type | State | Transition | Check |
|---|---|---|---|
| Digit sum = S | `remaining` | `remaining - d` | `remaining == 0` |
| Digit sum in [a, b] | `sum` | `sum + d` | `a <= sum <= b` |
| No repeated digits | `mask` (bitmask) | `mask \| (1 << d)` | always 1 (just count) |
| Divisible by K | `remainder` | `(rem * 10 + d) % K` | `rem == 0` |
| Balanced (odd=even sum) | `diff` | `diff ± d` | `diff == 0` |
| Count of specific digit | `count` | `count + (d == target)` | `count == k` |
| No adjacent same digits | `last_digit` | `d` | always 1 |
| Even/odd digit counts | `(even_cnt, odd_cnt)` | increment based on d | `even_cnt == odd_cnt` |

---

## 4. Problem 3791 — Balanced Integers in a Range

**Difficulty**: Hard

> Count numbers in [low, high] with ≥ 2 digits where sum of odd-position digits = sum of even-position digits.

### Key State

Track `diff = odd_sum - even_sum` and `length` (digit count).

```
Number: 1 3 3 1
Pos:    1 2 3 4
Odd:    1   3   = 4    → diff += d at odd positions
Even:     3   1 = 4    → diff -= d at even positions
diff = 0 → balanced ✓
```

### Solution

```python
class Solution:
    def countBalancedIntegers(self, low: int, high: int) -> int:

        def count(num):
            if num < 10:
                return 0
            digits = [int(c) for c in str(num)]
            n = len(digits)
            OFFSET = 82  # shift diff to non-negative range

            @lru_cache(maxsize=None)
            def dp(pos, diff, tight, started, length):
                if pos == n:
                    if not started or length < 2:
                        return 0
                    return 1 if diff == OFFSET else 0

                limit = digits[pos] if tight else 9
                result = 0

                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    new_started = started or (d != 0)
                    new_length = length + (1 if new_started else 0)

                    if new_started:
                        actual_pos = new_length
                        if actual_pos % 2 == 1:  # odd position
                            new_diff = diff + d
                        else:                     # even position
                            new_diff = diff - d
                    else:
                        new_diff = diff

                    result += dp(pos + 1, new_diff, new_tight, new_started, new_length)

                return result

            ans = dp(0, OFFSET, True, False, 0)
            dp.cache_clear()
            return ans

        return count(high) - count(low - 1)
```

**State**: `(pos, diff, tight, started, length)` — diff tracks odd_sum - even_sum, length tracks digit count.

**Complexity**: O(n × 163 × 2 × 2 × n × 10) ≈ O(n² × 6520)

---

## 5. Problem 2376 — Count Special Integers

**Difficulty**: Hard

> Count numbers in [1, n] with all distinct digits.

### Key State

Use a **bitmask** to track which digits have been used.

```
Number: 3 1 5
mask after '3': 0b1000       (bit 3 set)
mask after '1': 0b1010       (bits 1,3 set)
mask after '5': 0b101010     (bits 1,3,5 set)

Try placing '3' again → bit 3 already set → skip
```

### Solution

```python
class Solution:
    def countSpecialNumbers(self, n: int) -> int:
        digits = [int(c) for c in str(n)]
        L = len(digits)

        @lru_cache(maxsize=None)
        def dp(pos, mask, tight, started):
            if pos == L:
                return 1 if started else 0

            limit = digits[pos] if tight else 9
            result = 0

            for d in range(0, limit + 1):
                if started and (mask & (1 << d)):
                    continue  # digit already used

                new_tight = tight and (d == limit)
                new_started = started or (d != 0)
                new_mask = mask | (1 << d) if new_started else 0

                result += dp(pos + 1, new_mask, new_tight, new_started)

            return result

        return dp(0, 0, True, False)
```

**State**: `(pos, mask, tight, started)` — mask is 10-bit bitmask of used digits.

**Complexity**: O(n × 1024 × 2 × 2 × 10) where n = digit count

---

## 6. Problem 233 — Number of Digit One

**Difficulty**: Hard

> Count total number of digit 1 appearing in all numbers from 1 to n.

### Key Difference

Instead of counting **numbers**, count **total occurrences** of digit 1.

### Solution

```python
class Solution:
    def countDigitOne(self, n: int) -> int:
        digits = [int(c) for c in str(n)]
        L = len(digits)

        @lru_cache(maxsize=None)
        def dp(pos, count, tight, started):
            if pos == L:
                return count if started else 0

            limit = digits[pos] if tight else 9
            result = 0

            for d in range(0, limit + 1):
                new_tight = tight and (d == limit)
                new_started = started or (d != 0)
                new_count = count + (1 if d == 1 else 0)

                result += dp(pos + 1, new_count, new_tight, new_started)

            return result

        return dp(0, 0, True, False)
```

**State**: `(pos, count, tight, started)` — count tracks how many 1's placed so far.

**Note**: The base case returns `count` (not 0 or 1) because we're summing occurrences, not counting numbers.

---

## 7. Problem 902 — Numbers At Most N Given Digit Set

**Difficulty**: Hard

> Given a sorted array of digits (strings), count numbers ≤ n using only those digits.

### Key Difference

Instead of `d in range(0, limit+1)`, only iterate over the **allowed** digits.

### Solution

```python
class Solution:
    def atMostNGivenDigitSet(self, digits_set: list[str], n: int) -> int:
        allowed = [int(d) for d in digits_set]
        digits = [int(c) for c in str(n)]
        L = len(digits)

        @lru_cache(maxsize=None)
        def dp(pos, tight, started):
            if pos == L:
                return 1 if started else 0

            limit = digits[pos] if tight else 9
            result = 0

            if not started:
                # Option: place nothing (stay in leading zeros)
                result += dp(pos + 1, False, False)

            for d in allowed:
                if d > limit:
                    break
                new_tight = tight and (d == limit)
                result += dp(pos + 1, new_tight, True)

            return result

        return dp(0, True, False)
```

**State**: `(pos, tight, started)` — minimal state since any combination of allowed digits is valid.

---

## 8. Problem 1012 — Numbers With Repeated Digits

**Difficulty**: Hard

> Count numbers in [1, n] with at least one repeated digit.

### Key Idea

Use complement: `answer = n - count_of_special_numbers(n)` where special = all digits distinct (Problem 2376).

```python
class Solution:
    def numDupDigitsAtMostN(self, n: int) -> int:
        # Count numbers with ALL distinct digits, subtract from n
        digits = [int(c) for c in str(n)]
        L = len(digits)

        @lru_cache(maxsize=None)
        def dp(pos, mask, tight, started):
            if pos == L:
                return 1 if started else 0

            limit = digits[pos] if tight else 9
            result = 0

            for d in range(0, limit + 1):
                if started and (mask & (1 << d)):
                    continue
                new_tight = tight and (d == limit)
                new_started = started or (d != 0)
                new_mask = mask | (1 << d) if new_started else 0
                result += dp(pos + 1, new_mask, new_tight, new_started)

            return result

        all_distinct = dp(0, 0, True, False)
        return n - all_distinct
```

**Technique**: Complement counting — sometimes it's easier to count what you **don't** want.

---

## 9. Problem 2719 — Count of Integers (Digit Sum Bounds)

**Difficulty**: Hard

> Count numbers in [num1, num2] whose digit sum is in [min_sum, max_sum].

### Solution

```python
class Solution:
    def count(self, num1: str, num2: str, min_sum: int, max_sum: int) -> int:
        MOD = 10**9 + 7

        def solve(num_str):
            digits = [int(c) for c in num_str]
            n = len(digits)

            @lru_cache(maxsize=None)
            def dp(pos, dsum, tight):
                if dsum > max_sum:
                    return 0  # pruning
                if pos == n:
                    return 1 if min_sum <= dsum <= max_sum else 0

                limit = digits[pos] if tight else 9
                result = 0

                for d in range(0, limit + 1):
                    result += dp(pos + 1, dsum + d, tight and (d == limit))

                return result % MOD

            ans = dp(0, 0, True)
            dp.cache_clear()
            return ans

        # count(num2) - count(num1) + check(num1)
        ans2 = solve(num2)
        ans1 = solve(num1)

        # Check if num1 itself is valid
        s = sum(int(c) for c in num1)
        num1_valid = 1 if min_sum <= s <= max_sum else 0

        return (ans2 - ans1 + num1_valid) % MOD
```

**State**: `(pos, dsum, tight)` — no `started` needed since leading zeros don't affect digit sum.

**Note**: Inputs are strings (can be very large), so we use string-based subtraction: `count(num2) - count(num1) + check(num1)` instead of `count(num2) - count(num1 - 1)`.

---

## 10. Problem 2827 — Number of Beautiful Integers

**Difficulty**: Hard

> Count numbers in [low, high] where count of even digits = count of odd digits AND number is divisible by k.

### Key State

Track **two** things simultaneously: digit parity balance and remainder.

```python
class Solution:
    def numberOfBeautifulIntegers(self, low: int, high: int, k: int) -> int:

        def count(num):
            if num <= 0:
                return 0
            digits = [int(c) for c in str(num)]
            n = len(digits)

            @lru_cache(maxsize=None)
            def dp(pos, diff, rem, tight, started):
                """
                diff = count_even_digits - count_odd_digits
                rem  = number mod k so far
                """
                if pos == n:
                    if not started:
                        return 0
                    return 1 if diff == 0 and rem == 0 else 0

                limit = digits[pos] if tight else 9
                result = 0

                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    new_started = started or (d != 0)

                    if new_started:
                        new_diff = diff + (1 if d % 2 == 0 else -1)
                        new_rem = (rem * 10 + d) % k
                    else:
                        new_diff = diff
                        new_rem = 0

                    result += dp(pos + 1, new_diff, new_rem, new_tight, new_started)

                return result

            ans = dp(0, 0, 0, True, False)
            dp.cache_clear()
            return ans

        return count(high) - count(low - 1)
```

**State**: `(pos, diff, rem, tight, started)` — combines two properties in one DP.

**Complexity**: O(n × (2n+1) × k × 2 × 2 × 10) where n = digit count

---

## 11. Master Comparison Table

| Problem | State | Transition | Check | Time |
|---------|-------|------------|-------|------|
| **3791** Balanced | `diff, length` | `diff ± d` based on position parity | `diff == 0, length ≥ 2` | O(n² × 163) |
| **2376** Special | `mask` (10-bit) | `mask \| (1 << d)` | `started` | O(n × 1024) |
| **233** Digit One | `count` | `count + (d == 1)` | return `count` | O(n × n) |
| **902** Digit Set | — | only place allowed digits | `started` | O(n × \|set\|) |
| **1012** Repeated | `mask` | `mask \| (1 << d)` | complement: `n - distinct` | O(n × 1024) |
| **2719** Sum Bounds | `dsum` | `dsum + d` | `min ≤ sum ≤ max` | O(n × S) |
| **2827** Beautiful | `diff, rem` | `diff ± 1`, `(rem*10+d)%k` | `diff == 0, rem == 0` | O(n² × k) |

---

## 12. How to Identify This Pattern

### Trigger: "Count numbers in a range with digit property"

```
See "count numbers in [L, R]"?
  └── Yes → Digit DP likely
        │
        ├── Property depends on digit sum?
        │     └── State: sum or remaining_sum
        │
        ├── Property depends on which digits appear?
        │     └── State: bitmask of used digits
        │
        ├── Property depends on divisibility?
        │     └── State: remainder mod k
        │
        ├── Property depends on digit positions?
        │     └── State: diff (odd vs even position sums)
        │
        ├── Property depends on adjacent digits?
        │     └── State: last_digit
        │
        └── Multiple properties combined?
              └── Combine states (diff + rem, mask + sum, etc.)
```

### The Universal Steps

```
1. Range reduction
   count(low, high) = count(high) - count(low - 1)

2. Convert number to digit array

3. dp(pos, state, tight, started)
        │     │      │       │
        │     │      │       └── leading zeros handled
        │     │      └── still bounded by limit?
        │     └── problem-specific (THE KEY VARIABLE)
        │
        └── which digit position (left to right)

4. Base case: pos == n → check state

5. Loop: d from 0 to (digits[pos] if tight else 9)

6. Transition: update state based on d
```

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Forgetting leading zeros | Use `started` parameter |
| Off-by-one in range | `count(high) - count(low - 1)` |
| State too large | Use diff instead of two sums, remainder instead of full value |
| Not clearing cache | Call `dp.cache_clear()` between `count(high)` and `count(low-1)` |
| String inputs (2719) | Use `count(num2) - count(num1) + valid(num1)` |

---

## Practice Order

```
Start here
    │
    ▼
  902 (Hard)  ──── Simplest: restricted digit set, minimal state
    │
    ▼
  233 (Hard)  ──── Count occurrences instead of numbers
    │
    ▼
 2376 (Hard)  ──── Bitmask state for unique digits
    │
    ▼
 1012 (Hard)  ──── Complement counting + bitmask
    │
    ▼
 2719 (Hard)  ──── Digit sum with bounds, string inputs
    │
    ▼
 3791 (Hard)  ──── Position-dependent state + length tracking
    │
    ▼
 2827 (Hard)  ──── Combined state: parity balance + divisibility
```

---

*Pattern mastered — same template, different pluggable state and transitions.*
