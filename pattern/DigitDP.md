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

## Quick Navigation: I need to...

| Symptom in the problem | The `state` you add | Go to |
|---|---|---|
| "count numbers in `[L, R]` with **digit sum** = S / in `[a,b]`" | running sum / remaining | [2719](#9-problem-2719--count-of-integers-digit-sum-bounds) |
| "count numbers with **all distinct digits**" | 10-bit `mask` | [2376](#5-problem-2376--count-special-integers) |
| "count numbers with **at least one repeated digit**" | 10-bit `mask` + complement | [1012](#8-problem-1012--numbers-with-repeated-digits) |
| "**how many times** does digit X appear across `1..n`" | occurrence `count` (return it, not 0/1) | [233](#6-problem-233--number-of-digit-one) |
| "only these digits are **allowed**" | none — iterate the allowed set | [902](#7-problem-902--numbers-at-most-n-given-digit-set) |
| "sum of **odd-position** digits = sum of **even-position**" | `diff` + `length` | [3791](#4-problem-3791--balanced-integers-in-a-range) |
| "**divisible by k** AND some digit property" | `rem` (+ second state) | [2827](#10-problem-2827--number-of-beautiful-integers) |
| "which digit families exist / what state do I pick" | — | [§3 Common State Choices](#3-common-state-choices), [§12 identify router](#12-how-to-identify-this-pattern) |
| "range endpoints are **strings** too big for `int`" | string-subtraction trick | [2719 note](#9-problem-2719--count-of-integers-digit-sum-bounds) |

---

## Table of Contents

0. [Why This Pattern Exists](#0-why-this-pattern-exists)
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

## 0. Why This Pattern Exists

**The problem**: "How many integers in `[1, 10^18]` have digit sum exactly 30?"

Your first instinct is a loop:

```python
count = 0
for x in range(1, 10**18 + 1):   # 10^18 iterations — never finishes
    if digit_sum(x) == 30:
        count += 1
```

At a billion iterations/second this takes **~30 years**. The range is too big to enumerate. Yet the *answer* isn't astronomically large, and most numbers are boring — we're wasting time re-examining digits we've already reasoned about.

**The key realization**: we don't care about each number individually. We care about **choices, digit by digit**. Build the number left to right, one digit at a time. There are only 18 positions, and at each position only 10 possible digits — that's a tiny decision tree, not 10^18 leaves.

```
Counting numbers ≤ 316 with some property:

        first digit d0
       /     |      \
     0..2    3       (d0 can't exceed 3, the leading digit of 316)
    (free)  (still "tight" — bounded by 316)
```

Two numbers that reach position `pos` with the **same running digit-sum** and the **same freedom** (are we still hugging the upper bound `316`, or free to use 0–9?) have the **identical count of completions**. That's the overlapping-subproblem signal — memoize on `(pos, digit_sum_so_far, tight)` and the 10^18 problem collapses to a few thousand states.

`★ Insight ─────────────────────────────────────`
- Digit DP trades "iterate over **numbers**" for "iterate over **prefixes of digits**". 10^18 numbers, but only `18 positions × ~small state × 2 tight-flags` distinct subproblems.
- The whole pattern is: **fix the digits left-to-right, remember just enough about the prefix to finish counting, and cache**. Everything below is variations on *what* "just enough" means (a sum, a mask, a remainder…).
`─────────────────────────────────────────────────`

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
    # dp is a fresh closure per call, so its cache can't leak into other
    # bounds. This clear only frees memory early (optional) — it is NOT
    # required for correctness with this nested-function layout.
    dp.cache_clear()
    return ans

# Final answer
answer = count(high) - count(low - 1)
```

The only thing that changes between problems:
- **`state`**: what you track (sum, diff, mask, remainder...)
- **`transition`**: how state updates when placing digit `d`
- **`check`**: what condition to verify at the end

`★ Insight ─────────────────────────────────────`
- The `count(high) - count(low - 1)` split is the whole reason Digit DP only ever solves "**count from 1 to N**". You never write range logic — you write one upper-bound counter and subtract two calls. A property that holds on `[L,R]` becomes `f(R) - f(L-1)`, exactly like a prefix sum on the number line.
- `count()` is `count(1..num)`, so the caller must pass `low - 1`, NOT `low`. Off-by-one here is the #1 Digit DP bug — the `count(low-1)` call is what excludes everything below `low`.
- The four parameters split cleanly: `pos` + `tight` + `started` are the **skeleton** (identical in every problem); only `state` carries the problem. Learn the skeleton once and each new problem is just "what's the state?".
`─────────────────────────────────────────────────`

### A Tiny Recursion Trace

Count integers in `[0, 13]` with **no digit 4**. Digits of 13 = `[1, 3]`, so `n = 2`. Nodes are `(pos, tight)`:

```
(pos0, tight)                      d ∈ 0..1  (limit = digits[0] = 1)
 ├─ d=0 → (pos1, free)             d ∈ 0..9, skip 4  → 9 completions (0..9 minus 4)
 ├─ d=1 → (pos1, tight)            d ∈ 0..3, skip nothing → 4 completions (10,11,12,13)
 │
 └─ but d=0 branches into (pos1, free); ANY later prefix that reaches (pos1, free)
    reuses the SAME memoized node — no digit 4 free-count is computed once.
```

`(pos1, free)` = 9 and `(pos1, tight)` = 4, so the root returns 9 + 4 = 13 (every value 0..13 except 4). The `free` node is where memo hits pay off: on larger bounds many distinct tight-prefixes drop into the identical `(pos, free, state)` subtree and collapse to one cached value.

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

`★ Insight ─────────────────────────────────────`
- `tight` is a **one-way door**: once you place a digit *below* the bound, `new_tight = tight and (d == limit)` goes False and stays False for the rest of the number. There's exactly one tight path (the prefix that equals N so far) and everything that falls off it lands in the same free subtree.
- That is precisely why memoization works. A `tight=True` state has a *unique* prefix, so it's visited once and barely benefits from caching — the payoff is all the `tight=False` states, where thousands of different prefixes collapse onto the same `(pos, state, False)` node. **Never memoize on `tight=True` expecting reuse; do memoize the free states.**
- Most bugs come from computing `limit` wrong: it's `digits[pos]` **only when tight**, else `9`. Flip that and you either overcount (freely using 9s under a tight bound) or undercount.
`─────────────────────────────────────────────────`

### `started` — Leading Zeros

Handles the fact that `007` is actually `7` (a 1-digit number, not 3-digit).

```
started=False → still in leading zeros (haven't placed a real digit)
started=True  → placed at least one non-zero digit

Transition: new_started = started or (d != 0)
```

Without this, we'd incorrectly treat leading zeros as real digits, breaking problems that depend on digit count or position.

`★ Insight ─────────────────────────────────────`
- `started` exists so a leading `0` is a **non-choice**, not a placed digit. Before `started`, the `0` you "place" must skip the state transition (see 2376/3791: `new_mask` / `new_diff` only update `if new_started`). Forget that guard and `007` looks like it "used digit 0" or "has length 3" — wrong for distinct-digit or position-parity problems.
- Not every problem needs it. **Digit-sum problems (2719) drop `started` entirely** — leading zeros add 0 to the sum, so they're harmless. Add `started` only when leading zeros would corrupt the state: digit *count*, position parity, first-digit rules, or "no repeated digit" (where a phantom leading 0 falsely marks 0 as used).
`─────────────────────────────────────────────────`

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

`★ Insight ─────────────────────────────────────`
- This is the one problem that breaks the "return 0/1" reflex. Every other guide problem asks *how many numbers* qualify (base case returns 1); 233 asks *how many 1's total*, so the base case returns the accumulated `count`. Same skeleton, one-word change in the payload.
- Equivalent reframing: `dp` here computes a **sum over numbers of (their digit-1 count)**, which by linearity equals summing 1 each time a 1 is *placed*. Both views give the same answer — the accumulate-in-state version shown is the one that generalizes to "count digit X" or "count pairs" with no new machinery.
`─────────────────────────────────────────────────`

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

`★ Insight ─────────────────────────────────────`
- The loop changes from `for d in range(0, limit+1)` to `for d in allowed` — you iterate the *permitted* digits, not all ten. Because `allowed` is sorted, `if d > limit: break` is a clean early cutoff under the tight bound.
- The separate `if not started: dp(pos+1, False, False)` branch is how you count **shorter** numbers. Staying in leading-zeros one more position means "this number has fewer digits than N" — that single line is what lets a 3-digit bound also count all the valid 1- and 2-digit numbers.
- No `state` at all here: once digits are drawn only from `allowed`, *every* completion is valid, so there's nothing to check but "did we start". Minimal-state problems are the best place to first internalize the bare `pos/tight/started` skeleton.
`─────────────────────────────────────────────────`

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

`★ Insight ─────────────────────────────────────`
- Two independent conditions ("even-count = odd-count" AND "divisible by k") become **two independent state dimensions** carried side by side — `diff` and `rem` — and the check is just `diff == 0 and rem == 0`. You never multiply the problems; you widen the state tuple. This is the general recipe for "property A AND property B".
- The `rem` transition `(rem * 10 + d) % k` is Horner's method: it's the running number mod k, updated one digit at a time so you never build the full (possibly huge) integer. This is *the* reason divisibility fits Digit DP — the remainder is a tiny bounded state even when the number isn't.
- Cost multiplies too: state count is `pos × diff-range × k × ...`. If `k` is large this DP gets heavy — divisibility problems are only cheap because `rem < k` and `k` is small.
`─────────────────────────────────────────────────`

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
| Sharing one cache across bounds | Define `@lru_cache` on a **nested** `dp` inside `count()` so each call gets a fresh cache (as in the template). A module/class-level cache reused across different `digits` gives wrong answers — clear it or key on the digits. |
| String inputs (2719) | Use `count(num2) - count(num1) + valid(num1)` |

---

## Practice Order

Start on an easier on-ramp before the all-Hard core. The first two need little or no `state` (or none at all), so you learn the `pos/tight/started` skeleton in isolation, then layer state on.

```
Start here
    │
    ▼
  357 (Medium) ──── Count Numbers with Unique Digits: warm-up, closed-form or trivial
    │               mask DP — meet the pos/tight skeleton with the lightest state
    ▼
  902 (Hard)   ──── Simplest full template: restricted digit set, minimal state
    │
    ▼
  233 (Hard)   ──── Count occurrences instead of numbers
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

## When This Fails

Digit DP counts numbers by building them digit by digit, so it needs the property to be
**decidable from a small running summary**:

- **The property is not digit-local.** "Is `x` prime?" or "is `x` a perfect square?" cannot be
  tracked in a compact state as you place digits. Digit DP does not apply.
- **The state explodes.** A state that must remember the entire prefix (say, all digits seen in
  order) is `10^d` states — no better than enumeration. Digit DP pays off only when the summary
  is small: a count, a remainder, a mask, a parity.
- **You forgot `started` where leading zeros matter.** Counting numbers *with distinct digits*
  must not treat the leading zeros of a short number as digits. If a leading zero would be
  counted, you need the flag.
- **The bound is exclusive or the range is on the wrong side.** `count(R) − count(L−1)` assumes
  `count` is inclusive. Off by one here shifts every answer by one number.

## Self-Test

Answer these from memory, out loud or on paper, *before* looking. Recognition is not
recall: rereading an explanation feels like knowing, and it is not. A question you cannot answer
cold names the exact section to revisit — you do not need to reread the guide.


**1. What is the standard range trick, and what does it assume?**

<details markdown="1">
<summary>Answer</summary>

`answer([L, R]) = count(R) − count(L − 1)`, where `count(X)` counts qualifying values in `[0, X]`. It assumes `count` is inclusive of its bound. For huge `L` given as a string, subtract by decrementing the string rather than converting.

</details>

**2. What do the four standard parameters mean?**

<details markdown="1">
<summary>Answer</summary>

`pos`: which digit index you are placing. `tight`: whether the prefix so far exactly matches the bound, which caps the current digit. `started`: whether a non-zero digit has appeared yet, distinguishing real digits from leading padding. Plus the problem-specific state (a digit sum, a remainder, a mask).

</details>

**3. Why must `tight` be in the memo key but the bound itself need not be?**

<details markdown="1">
<summary>Answer</summary>

The bound is fixed for the whole call, so it is context, not state. `tight` varies between paths reaching the same `pos` and genuinely changes how many completions exist — cache them together and you get wrong counts.

</details>

**4. When can you omit `started`, and when is omitting it a bug?**

<details markdown="1">
<summary>Answer</summary>

Omit it when leading zeros are harmless — counting occurrences of the digit 1 from 0 upward, for instance. It is required whenever a leading zero would be miscounted as a real digit: distinct-digit problems, digit-set membership, first-digit constraints.

</details>

**5. What is the upper limit for the current digit when `tight` is true?**

<details markdown="1">
<summary>Answer</summary>

The corresponding digit of the bound. Placing exactly that digit keeps `tight` for the next position; placing anything smaller frees the remaining positions to range over all ten digits.

</details>

**6. What kinds of running state actually work here?**

<details markdown="1">
<summary>Answer</summary>

Small summaries: a digit sum (bounded by `9d`), a remainder mod `m`, a bitmask of digits used (`2^10`), a count, a parity, the previous digit. Anything requiring the full prefix defeats the purpose.

</details>

**7. How would you count the *sum* of qualifying numbers rather than how many there are?**

<details markdown="1">
<summary>Answer</summary>

Return a pair `(count, sum)` from the recursion. When you place digit `d` at a position with place value `p`, the contribution is `sum_child + d · p · count_child` — the child's own sum plus this digit repeated once for each completion beneath it.

</details>

---

## See Also

- [Dynamic Programming §12](/pattern/dp) — digit DP's place among the other DP families, if you arrived from the general DP guide.
- [Bitmask Techniques](/pattern/bitmask) — when your digit state is a *set* of seen digits (LC 1012, 2376), the mask machinery lives there.
- [Binary Search](/pattern/binary-search) — the other technique that survives `n <= 10^18`; if the property is not digit-local, search the answer instead of building it digit by digit.
- [Pattern Decision Map](/pattern/decision-map) — the router: which technique does a cold problem call for?
- [Pattern Mastery Program](/pattern/mastery) — the spaced-repetition schedule, mastery checklist, and drill formats that turn reading into recall.

---

*Pattern mastered — same template, different pluggable state and transitions.*
