---
layout: simple
title: "Bit Strings - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/bit_strings_analysis
difficulty: Easy
tags: [modular-arithmetic, exponentiation, combinatorics]
---

# Bit Strings

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 1617 - Bit Strings](https://cses.fi/problemset/task/1617) |
| **Difficulty** | Easy |
| **Category** | Introductory / Math |
| **Time Limit** | 1 second |
| **Key Technique** | Modular Exponentiation |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand why there are 2^n possible bit strings of length n
- [ ] Implement modular exponentiation (binary exponentiation)
- [ ] Apply modular arithmetic to avoid integer overflow
- [ ] Recognize when to use fast exponentiation for large powers

---

## Problem Statement

**Problem:** Calculate the number of bit strings of length n.

**Input:**
- Line 1: An integer n (the length of the bit string)

**Output:**
- The number of bit strings of length n, modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 10^6

### Example

```
Input:
3

Output:
8
```

**Explanation:** For n = 3, the possible bit strings are: 000, 001, 010, 011, 100, 101, 110, 111. That is 2^3 = 8 strings.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How many ways can we fill n positions where each position has 2 choices (0 or 1)?

Each position in the bit string can independently be either 0 or 1. Since there are n positions and 2 choices per position, the total count is 2 * 2 * 2 * ... (n times) = 2^n.

### Breaking Down the Problem

1. **What are we looking for?** The count of all possible binary strings of length n.
2. **What information do we have?** The length n.
3. **What is the relationship between input and output?** Output = 2^n mod (10^9 + 7).

### Analogies

Think of this like a binary counter with n digits. Starting from all zeros, you count up until all ones. The total number of states is exactly 2^n.

---

## Solution 1: Naive Approach (TLE)

### Idea

Multiply 2 by itself n times, taking modulo at each step.

### Algorithm

1. Initialize result = 1
2. Loop n times, multiply result by 2
3. Take modulo 10^9 + 7 at each step
4. Return result

### Code

```python
def solve_naive(n):
    """
    Naive solution: linear multiplication.

    Time: O(n)
    Space: O(1)
    """
    MOD = 10**9 + 7
    result = 1
    for _ in range(n):
        result = (result * 2) % MOD
    return result
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    long long result = 1;
    const long long MOD = 1e9 + 7;

    for (int i = 0; i < n; i++) {
        result = (result * 2) % MOD;
    }

    cout << result << endl;
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Loop runs n times |
| Space | O(1) | Only stores result |

### Why This Works (But Is Slow)

This approach is correct but performs n multiplications. For n up to 10^6, this is acceptable but not optimal. For larger constraints, we need a faster method.

---

## Solution 2: Binary Exponentiation (Optimal)

### Key Insight

> **The Trick:** Use binary exponentiation to compute 2^n in O(log n) time by repeatedly squaring.

Binary exponentiation exploits the fact that:
- If n is even: 2^n = (2^(n/2))^2
- If n is odd: 2^n = 2 * 2^(n-1)

This reduces the number of multiplications from n to log(n).

### How Binary Exponentiation Works

```
Example: 2^13

13 in binary = 1101 = 8 + 4 + 1

2^13 = 2^8 * 2^4 * 2^1

We compute powers of 2 by repeated squaring:
2^1 = 2
2^2 = 4
2^4 = 16
2^8 = 256

Then multiply the ones corresponding to set bits:
2^13 = 256 * 16 * 2 = 8192
```

### Algorithm

1. Initialize result = 1, base = 2
2. While exponent > 0:
   - If exponent is odd, multiply result by base
   - Square the base
   - Halve the exponent (integer division)
3. Take modulo at each multiplication
4. Return result

### Dry Run Example

Let us trace through with input `n = 10`:

```
Goal: Compute 2^10 mod (10^9 + 7)

Initial state:
  result = 1
  base = 2
  exp = 10

Step 1: exp = 10 (even)
  exp is even, do not multiply result
  base = 2 * 2 = 4
  exp = 10 / 2 = 5

Step 2: exp = 5 (odd)
  result = 1 * 4 = 4
  base = 4 * 4 = 16
  exp = 5 / 2 = 2

Step 3: exp = 2 (even)
  exp is even, do not multiply result
  base = 16 * 16 = 256
  exp = 2 / 2 = 1

Step 4: exp = 1 (odd)
  result = 4 * 256 = 1024
  base = 256 * 256 = 65536
  exp = 1 / 2 = 0

Final: result = 1024

Verification: 2^10 = 1024
```

### Visual Diagram

```
Computing 2^10:

Exponent in binary: 10 = 1010

     bit:     1    0    1    0
     pos:     3    2    1    0
   power:    2^8  2^4  2^2  2^1
   value:   256   16    4    2

Include:    YES   NO  YES   NO

Result = 2^8 * 2^2 = 256 * 4 = 1024
```

### Code

```python
def solve_optimal(n):
    """
    Optimal solution using binary exponentiation.

    Time: O(log n)
    Space: O(1)
    """
    MOD = 10**9 + 7

    def power(base, exp, mod):
        result = 1
        base = base % mod

        while exp > 0:
            # If exp is odd, multiply result with base
            if exp % 2 == 1:
                result = (result * base) % mod

            # Square the base
            base = (base * base) % mod

            # Halve the exponent
            exp //= 2

        return result

    return power(2, n, MOD)


# Main
n = int(input())
print(solve_optimal(n))
```

### C++ Solution

```cpp
#include <iostream>
using namespace std;

const long long MOD = 1e9 + 7;

long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    base = base % mod;

    while (exp > 0) {
        // If exp is odd, multiply result with base
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }

        // Square the base
        base = (base * base) % mod;

        // Halve the exponent
        exp /= 2;
    }

    return result;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    cout << power(2, n, MOD) << endl;

    return 0;
}
```

### Using Built-in Functions

Python has a built-in three-argument `pow()` that does modular exponentiation efficiently:

```python
n = int(input())
print(pow(2, n, 10**9 + 7))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(log n) | Exponent halves each iteration |
| Space | O(1) | Only constant variables used |

---

## Common Mistakes

### Mistake 1: Integer Overflow (C++)

```cpp
// WRONG - overflow for large intermediate results
long long result = 1;
for (int i = 0; i < n; i++) {
    result *= 2;  // Overflows before taking mod!
}
result %= MOD;
```

**Problem:** The result overflows before we apply modulo.
**Fix:** Apply modulo after each multiplication.

```cpp
// CORRECT
long long result = 1;
for (int i = 0; i < n; i++) {
    result = (result * 2) % MOD;
}
```

### Mistake 2: Forgetting Modulo in Exponentiation

```python
# WRONG - intermediate values overflow
def power(base, exp):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = result * base  # No modulo!
        base = base * base          # No modulo!
        exp //= 2
    return result % MOD
```

**Problem:** Even though Python handles big integers, this is slow and wrong for other languages.
**Fix:** Apply modulo at every multiplication step.

### Mistake 3: Using Wrong Data Type (C++)

```cpp
// WRONG - int overflow during multiplication
int result = 1;
int base = 2;
result = (result * base) % MOD;  // May overflow before mod
```

**Problem:** `int * int` can overflow before modulo is applied.
**Fix:** Use `long long` for all arithmetic involving modulo.

```cpp
// CORRECT
long long result = 1;
long long base = 2;
result = (result * base) % MOD;
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum n | n = 1 | 2 | 2^1 = 2 |
| Small n | n = 3 | 8 | 2^3 = 8 |
| Power of 2 | n = 10 | 1024 | 2^10 = 1024 |
| Large n | n = 1000000 | 470211272 | Result after mod |
| Mod boundary | n = 30 | 1073741824 | 2^30 (before mod kicks in) |

---

## When to Use This Pattern

### Use Binary Exponentiation When:
- Computing large powers (a^n where n can be very large)
- Working with modular arithmetic
- Need O(log n) time instead of O(n)
- Matrix exponentiation for recurrence relations

### Do Not Use When:
- n is very small (direct multiplication is fine)
- No modular arithmetic needed and result fits in data type

### Pattern Recognition Checklist:
- [ ] Need to compute a^n for large n? -> **Binary Exponentiation**
- [ ] Result must be modulo some value? -> **Apply mod at each step**
- [ ] Computing Fibonacci/recurrence for large n? -> **Matrix exponentiation**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Weird Algorithm](https://cses.fi/problemset/task/1068) | Basic loop and arithmetic |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Exponentiation](https://cses.fi/problemset/task/1095) | General a^b mod m |
| [Exponentiation II](https://cses.fi/problemset/task/1712) | a^(b^c) mod m using Fermat |
| [LeetCode: Pow(x, n)](https://leetcode.com/problems/powx-n/) | Handle negative exponents |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Fibonacci](https://cses.fi/problemset/task/1722) | Matrix exponentiation |
| [Graph Paths I](https://cses.fi/problemset/task/1723) | Matrix exponentiation for paths |

---

## Key Takeaways

1. **The Core Idea:** Count of n-bit strings is 2^n; use binary exponentiation for efficiency.
2. **Time Optimization:** Reduced from O(n) to O(log n) using repeated squaring.
3. **Space Trade-off:** O(1) space - no additional memory needed.
4. **Pattern:** This is the foundation for modular exponentiation used throughout competitive programming.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why there are 2^n bit strings of length n
- [ ] Implement binary exponentiation from scratch
- [ ] Handle modular arithmetic correctly to avoid overflow
- [ ] Solve this problem in under 5 minutes

---

## Additional Resources

- [CP-Algorithms: Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CSES Bit Strings](https://cses.fi/problemset/task/1617) - Binary exponentiation
- [Modular Arithmetic - Wikipedia](https://en.wikipedia.org/wiki/Modular_arithmetic)
