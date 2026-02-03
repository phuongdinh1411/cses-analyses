---
layout: simple
title: "Digit Sum - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming_at/digit_sum_analysis
difficulty: Hard
tags: [digit-dp, dynamic-programming, modular-arithmetic, counting]
---

# Digit Sum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - Problem S](https://atcoder.jp/contests/dp/tasks/dp_s) |
| **Difficulty** | Hard |
| **Category** | Dynamic Programming (Digit DP) |
| **Key Technique** | Digit DP with Tight Constraint |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the digit DP framework and when to apply it
- [ ] Handle "tight" constraints when building numbers digit by digit
- [ ] Track modular remainders efficiently as DP states
- [ ] Count numbers in a range satisfying digit-based conditions

---

## Problem Statement

**Problem:** Given a string K representing a positive integer and an integer D, count how many positive integers less than or equal to K have a digit sum divisible by D. Return the count modulo 10^9 + 7.

**Input:**
- Line 1: K (a string representing a positive integer)
- Line 2: D (the divisor)

**Output:**
- A single integer: the count modulo 10^9 + 7

**Constraints:**
- 1 <= |K| <= 10^4 (K can have up to 10,000 digits)
- 1 <= D <= 100

### Example

```
Input:
30
4

Output:
6
```

**Explanation:** The numbers from 1 to 30 with digit sum divisible by 4 are: 4, 8, 13, 17, 22, 26. Their digit sums are 4, 8, 4, 8, 4, 8 respectively, all divisible by 4.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count numbers up to K with a specific digit property when K is too large to iterate?

This is a classic **digit DP** problem. We cannot iterate through all numbers from 1 to K since K can have up to 10,000 digits. Instead, we build numbers digit by digit and use DP to count valid configurations.

### Breaking Down the Problem

1. **What are we looking for?** Count of numbers in [1, K] where digit_sum % D == 0
2. **What information do we have?** The upper bound K and divisor D
3. **What's the relationship?** We need to track partial digit sums modulo D as we construct numbers

### The Digit DP Framework

Think of building a number digit by digit from left to right. At each position, we need to know:
1. **Position**: Which digit are we filling?
2. **Tight constraint**: Can we still pick any digit, or are we bounded by K?
3. **Current state**: What is our digit sum so far (modulo D)?

---

## Solution: Digit DP

### Key Insight

> **The Trick:** Build numbers digit by digit, tracking (position, is_tight, sum_mod_D) to count valid numbers without enumeration.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[pos][tight][sum_mod]` | Count of ways to complete the number from position `pos` onwards |

- **pos**: Current digit position (0 to n-1)
- **tight**: Whether we're still bounded by K (1) or free to choose any digit (0)
- **sum_mod**: Current digit sum modulo D

**In plain English:** How many ways can we fill the remaining digits such that the final digit sum is divisible by D?

### State Transition

```
For each digit d in [0, limit]:
    new_tight = tight AND (d == K[pos])
    new_sum = (sum_mod + d) % D
    dp[pos][tight][sum_mod] += dp[pos+1][new_tight][new_sum]
```

**Why?** When `tight=1`, we can only choose digits up to K[pos]. Once we choose a smaller digit, we become "free" (tight=0) and can use digits 0-9 for remaining positions.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `pos == n` | 1 if sum_mod == 0, else 0 | Completed number; check if digit sum is divisible by D |

### Algorithm

1. Convert K to array of digits
2. Use memoization/tabulation for states (pos, tight, sum_mod)
3. For each state, try all valid digits and recurse
4. Subtract 1 from result (to exclude 0) and return

### Dry Run Example

Let's trace through with `K = "30"`, `D = 4`:

```
K = "30", digits = [3, 0], D = 4, n = 2

Call dp(pos=0, tight=1, sum_mod=0):
  limit = 3 (tight, so bounded by K[0])

  d=0: dp(1, 0, 0)  -> sum_mod=0
  d=1: dp(1, 0, 1)  -> sum_mod=1
  d=2: dp(1, 0, 2)  -> sum_mod=2
  d=3: dp(1, 1, 3)  -> sum_mod=3, still tight

For dp(1, 0, 0) [not tight, sum=0]:
  limit = 9 (free to choose any digit)
  d=0: sum=0, divisible by 4? YES -> count 1 (number "00")
  d=4: sum=4, divisible by 4? YES -> count 1 (number "04")
  d=8: sum=8, divisible by 4? YES -> count 1 (number "08")
  ... = 3 valid numbers

For dp(1, 0, 1) [not tight, sum=1]:
  d=3: sum=4, YES -> count 1 (number "13")
  d=7: sum=8, YES -> count 1 (number "17")
  ... = 2 valid numbers

For dp(1, 0, 2) [not tight, sum=2]:
  d=2: sum=4, YES -> count 1 (number "22")
  d=6: sum=8, YES -> count 1 (number "26")
  ... = 2 valid numbers

For dp(1, 1, 3) [tight, sum=3]:
  limit = 0 (bounded by K[1]=0)
  d=0: sum=3, NOT divisible by 4 -> 0

Total from dp(0,1,0) = 3+2+2+0 = 7
Subtract 1 for "00" (we want 1 to K, not 0 to K)
Final answer: 7 - 1 = 6
```

### Visual Diagram

```
Building numbers <= 30 digit by digit:

Position:    0       1
K digits:   [3]     [0]
             |       |
             v       v
        +---+---+   +-----------+
tight=1 |0|1|2|3|   | 0 only    | (when first digit is 3)
        +-+-+-+-+   +-----------+
          | | |
          v v v
tight=0   +-------+
          |0-9    | (when first digit < 3)
          +-------+

Track: sum_mod_D at each step
Goal: sum_mod == 0 at the end
```

### Code (Python)

```python
def solve():
    """
    Digit DP solution for counting numbers with digit sum divisible by D.

    Time: O(n * 2 * D * 10) = O(n * D)
    Space: O(n * D) for memoization
    """
    MOD = 10**9 + 7

    K = input().strip()
    D = int(input().strip())

    n = len(K)
    digits = [int(c) for c in K]

    # Memoization: (pos, tight, sum_mod) -> count
    memo = {}

    def dp(pos, tight, sum_mod):
        # Base case: all digits processed
        if pos == n:
            return 1 if sum_mod == 0 else 0

        state = (pos, tight, sum_mod)
        if state in memo:
            return memo[state]

        # Determine digit range
        limit = digits[pos] if tight else 9

        result = 0
        for d in range(limit + 1):
            new_tight = tight and (d == limit)
            new_sum = (sum_mod + d) % D
            result = (result + dp(pos + 1, new_tight, new_sum)) % MOD

        memo[state] = result
        return result

    # dp(0, True, 0) counts numbers from 0 to K
    # Subtract 1 to exclude 0 (we want 1 to K)
    ans = (dp(0, True, 0) - 1 + MOD) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;
string K;
int D, n;
map<tuple<int, int, int>, long long> memo;

long long dp(int pos, int tight, int sum_mod) {
    // Base case: all digits processed
    if (pos == n) {
        return (sum_mod == 0) ? 1 : 0;
    }

    auto state = make_tuple(pos, tight, sum_mod);
    if (memo.count(state)) {
        return memo[state];
    }

    // Determine digit range
    int limit = tight ? (K[pos] - '0') : 9;

    long long result = 0;
    for (int d = 0; d <= limit; d++) {
        int new_tight = tight && (d == limit);
        int new_sum = (sum_mod + d) % D;
        result = (result + dp(pos + 1, new_tight, new_sum)) % MOD;
    }

    memo[state] = result;
    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> K >> D;
    n = K.size();

    // dp(0, 1, 0) counts 0 to K; subtract 1 to exclude 0
    long long ans = (dp(0, 1, 0) - 1 + MOD) % MOD;
    cout << ans << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * D * 10) | n positions, D sum states, 10 digit choices |
| Space | O(n * D) | Memoization table (tight has constant factor 2) |

---

## Common Mistakes

### Mistake 1: Forgetting to Exclude Zero

```python
# WRONG
ans = dp(0, True, 0)  # Includes 0 in the count

# CORRECT
ans = (dp(0, True, 0) - 1 + MOD) % MOD  # Exclude 0
```

**Problem:** The digit DP counts from 0 to K, but we want 1 to K.
**Fix:** Subtract 1 from the result (with proper modulo handling).

### Mistake 2: Incorrect Tight Transition

```python
# WRONG
new_tight = (d == limit)  # Forgets to check if already tight

# CORRECT
new_tight = tight and (d == limit)
```

**Problem:** Once we're not tight, we stay not tight.
**Fix:** Only remain tight if we were tight AND chose the max digit.

### Mistake 3: Negative Modulo

```python
# WRONG
ans = (dp(0, True, 0) - 1) % MOD  # Can be negative!

# CORRECT
ans = (dp(0, True, 0) - 1 + MOD) % MOD  # Always positive
```

**Problem:** In some languages, `(-1) % MOD` can be negative.
**Fix:** Add MOD before taking modulo.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single digit | K="9", D=3 | 3 | Numbers 3, 6, 9 have digit sum divisible by 3 |
| D equals 1 | K="100", D=1 | 100 | Every number has digit sum divisible by 1 |
| Large K | K="9"*10000, D=100 | varies | Tests efficiency with 10,000 digits |
| K itself valid | K="12", D=3 | 4 | 3, 6, 9, 12 (includes K when valid) |

---

## When to Use This Pattern

### Use Digit DP When:
- Counting numbers in range [0, K] with digit-based properties
- K is too large to iterate (often given as string)
- Property depends on digits, not the number's value
- Need to track cumulative properties (sum, product, count of specific digits)

### Don't Use When:
- K is small enough to iterate directly (K < 10^6)
- Property depends on number theory (use math instead)
- Looking for specific numbers, not counting them

### Pattern Recognition Checklist:
- [ ] Is K given as a string (large number)? -> **Consider digit DP**
- [ ] Does the problem ask "count numbers with property X"? -> **Digit DP likely**
- [ ] Can the property be computed digit by digit? -> **Digit DP applicable**
- [ ] Is the property about digit sum/product/pattern? -> **Classic digit DP**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [AtCoder DP Contest - Problem A (Frog)](https://atcoder.jp/contests/dp/tasks/dp_a) | Basic DP introduction |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [LeetCode 233 - Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) | Count specific digit occurrences |
| [LeetCode 357 - Count Numbers with Unique Digits](https://leetcode.com/problems/count-numbers-with-unique-digits/) | Digit uniqueness constraint |
| [CSES - Counting Numbers](https://cses.fi/problemset/task/2220) | Count in range [a, b] with digit constraint |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [LeetCode 902 - Numbers At Most N Given Digit Set](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/) | Restricted digit choices |
| [LeetCode 1012 - Numbers With Repeated Digits](https://leetcode.com/problems/numbers-with-repeated-digits/) | Tracking used digits with bitmask |

---

## Key Takeaways

1. **The Core Idea:** Build numbers digit by digit, using DP to count valid configurations
2. **State Design:** (position, is_tight, accumulated_property) covers most digit DP problems
3. **Tight Constraint:** Critical for ensuring we only count numbers <= K
4. **Pattern:** Digit DP is essential for counting problems with large numeric bounds

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain what "tight" means and how it transitions
- [ ] Identify digit DP problems by their characteristics
- [ ] Implement the basic digit DP template from memory
- [ ] Extend this pattern to other digit properties (count of 7s, alternating digits, etc.)

---

## Additional Resources

- [AtCoder DP Contest](https://atcoder.jp/contests/dp) - Educational DP problem set
- [CP-Algorithms: Digit DP](https://cp-algorithms.com/dynamic_programming/digit-dp.html)
- [CSES Counting Numbers](https://cses.fi/problemset/task/2220) - Digit DP application
