---
layout: simple
title: "Counting Sequences - Combinatorics Problem"
permalink: /problem_soulutions/counting_problems/counting_sequences_analysis
difficulty: Easy
tags: [combinatorics, modular-arithmetic, exponentiation]
---

# Counting Sequences

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Combinatorics / Mathematics |
| **Time Limit** | 1 second |
| **Key Technique** | Modular Exponentiation |
| **CSES Link** | [Exponentiation](https://cses.fi/problemset/task/1095) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the multiplication principle for counting sequences
- [ ] Implement binary exponentiation for efficient power computation
- [ ] Handle modular arithmetic to prevent integer overflow
- [ ] Recognize when a counting problem reduces to a simple formula

---

## Problem Statement

**Problem:** Count the number of sequences of length k where each element can be any integer from 1 to n.

**Input:**
- Line 1: Two integers n and k (maximum element value and sequence length)

**Output:**
- The count of possible sequences, modulo 10^9 + 7

**Constraints:**
- 1 <= n, k <= 10^6

### Example

```
Input:
3 2

Output:
9
```

**Explanation:** With n=3 elements {1, 2, 3} and sequence length k=2:
- Position 1 can be: 1, 2, or 3 (3 choices)
- Position 2 can be: 1, 2, or 3 (3 choices)
- Total sequences: 3 x 3 = 9

All sequences: [1,1], [1,2], [1,3], [2,1], [2,2], [2,3], [3,1], [3,2], [3,3]

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** For each position in the sequence, how many choices do we have?

Each of the k positions can independently hold any of the n values. Since choices at one position do not affect choices at another, we use the **multiplication principle**: total = n x n x ... x n (k times) = n^k.

### Breaking Down the Problem

1. **What are we looking for?** Total count of distinct sequences
2. **What information do we have?** n possible values, k positions
3. **What's the relationship between input and output?** Each position multiplies our choices by n

### Analogies

Think of this like a combination lock with k dials, where each dial can show any number from 1 to n. The total number of possible codes is n^k.

---

## Solution 1: Brute Force (Recursive Enumeration)

### Idea

Generate all possible sequences by trying every value at each position recursively.

### Algorithm

1. Start at position 0
2. Try each value from 1 to n at the current position
3. Recurse to the next position
4. Count when we reach position k

### Code

```python
def count_sequences_brute(n, k, mod=10**9+7):
    """
    Brute force: enumerate all sequences recursively.

    Time: O(n^k) - generates all sequences
    Space: O(k) - recursion depth
    """
    def count(pos):
        if pos == k:
            return 1
        total = 0
        for _ in range(n):
            total = (total + count(pos + 1)) % mod
        return total

    return count(0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k) | Generates all n^k sequences |
| Space | O(k) | Recursion stack depth |

### Why This Works (But Is Slow)

The brute force correctly counts every sequence but becomes impossibly slow for large inputs. With n=1000, k=1000, we would need 1000^1000 operations!

---

## Solution 2: Optimal (Binary Exponentiation)

### Key Insight

> **The Trick:** The answer is simply n^k mod (10^9+7). Use binary exponentiation to compute this in O(log k) time.

### Mathematical Formula

```
Total sequences = n^k (mod 10^9 + 7)
```

**Why?** By the multiplication principle:
- Position 1: n choices
- Position 2: n choices (independent)
- ...
- Position k: n choices (independent)
- Total = n * n * ... * n = n^k

### Algorithm

1. Handle base cases (k=0 returns 1, n=0 returns 0)
2. Use binary exponentiation to compute n^k mod m
3. Return the result

### Dry Run Example

Let's trace through with `n = 3, k = 5`:

```
Computing 3^5 mod (10^9 + 7) using binary exponentiation:

k = 5 in binary = 101

Initial: result = 1, base = 3

Step 1: k = 5 (odd, bit = 1)
  result = 1 * 3 = 3
  base = 3 * 3 = 9
  k = 5 >> 1 = 2

Step 2: k = 2 (even, bit = 0)
  result stays 3
  base = 9 * 9 = 81
  k = 2 >> 1 = 1

Step 3: k = 1 (odd, bit = 1)
  result = 3 * 81 = 243
  base = 81 * 81 = 6561
  k = 1 >> 1 = 0

Done! Result = 243

Verify: 3^5 = 3*3*3*3*3 = 243 (correct!)
```

### Visual Diagram

```
Binary Exponentiation for n^k:

k in binary:  k = b_m b_{m-1} ... b_1 b_0

n^k = n^(2^0 * b_0) * n^(2^1 * b_1) * ... * n^(2^m * b_m)

Example: 3^5 = 3^(101 in binary)
       = 3^(4+0+1)
       = 3^4 * 3^1
       = 81 * 3 = 243

We square the base repeatedly and multiply when bit is 1:
  base: 3 -> 9 -> 81 -> ...
        ^        ^
        |        |
      b_0=1    b_2=1 (include these in result)
```

### Code

**Python:**
```python
def count_sequences(n, k, mod=10**9+7):
    """
    Count sequences using binary exponentiation.

    Time: O(log k)
    Space: O(1)
    """
    # Edge cases
    if k == 0:
        return 1
    if n == 0:
        return 0

    # Python's built-in pow handles modular exponentiation efficiently
    return pow(n, k, mod)


def count_sequences_manual(n, k, mod=10**9+7):
    """
    Manual implementation of binary exponentiation.
    """
    if k == 0:
        return 1
    if n == 0:
        return 0

    result = 1
    base = n % mod

    while k > 0:
        if k & 1:  # If k is odd (last bit is 1)
            result = (result * base) % mod
        base = (base * base) % mod
        k >>= 1  # Divide k by 2

    return result


# Example usage
if __name__ == "__main__":
    n, k = map(int, input().split())
    print(count_sequences(n, k))
```

**C++:**
```cpp
#include <iostream>
using namespace std;

const long long MOD = 1e9 + 7;

long long mod_pow(long long base, long long exp, long long mod) {
    // Binary exponentiation
    long long result = 1;
    base %= mod;

    while (exp > 0) {
        if (exp & 1) {  // If exp is odd
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1;  // Divide exp by 2
    }

    return result;
}

long long count_sequences(int n, int k) {
    if (k == 0) return 1;
    if (n == 0) return 0;
    return mod_pow(n, k, MOD);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    cout << count_sequences(n, k) << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(log k) | Binary exponentiation halves k each iteration |
| Space | O(1) | Only a few variables needed |

---

## Common Mistakes

### Mistake 1: Integer Overflow

```cpp
// WRONG - overflows for large n, k
long long result = 1;
for (int i = 0; i < k; i++) {
    result *= n;  // Overflows before taking mod!
}
return result % mod;
```

**Problem:** Multiplying before taking mod causes overflow.
**Fix:** Take mod after each multiplication: `result = (result * n) % mod;`

### Mistake 2: Slow Linear Exponentiation

```python
# WRONG - too slow for k up to 10^6
def slow_pow(n, k, mod):
    result = 1
    for _ in range(k):  # O(k) iterations!
        result = (result * n) % mod
    return result
```

**Problem:** O(k) is too slow when k can be 10^6.
**Fix:** Use binary exponentiation for O(log k) time.

### Mistake 3: Forgetting Edge Cases

```python
# WRONG - crashes or gives wrong answer for edge cases
def count_sequences(n, k, mod):
    return pow(n, k, mod)  # What if n=0? k=0?
```

**Problem:** n=0 should return 0 (no elements to choose), k=0 should return 1 (empty sequence).
**Fix:** Handle edge cases explicitly before the main computation.

### Mistake 4: Incorrect Mod Value

```python
# WRONG - using wrong modulo
MOD = 1e9 + 7  # This is a float!

# CORRECT
MOD = 10**9 + 7  # Integer
MOD = 1000000007  # Also integer
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Empty sequence | k = 0 | 1 | One way to have empty sequence |
| No elements | n = 0, k > 0 | 0 | Cannot form non-empty sequence |
| Single element | n = 1 | 1 | All positions must be 1 |
| Single position | k = 1 | n | Just n choices |
| Large values | n = 10^6, k = 10^6 | (computed) | Must use modular exponentiation |

---

## When to Use This Pattern

### Use Binary Exponentiation When:
- Computing large powers (a^b where b is large)
- Working with modular arithmetic
- Matrix exponentiation for DP optimization
- Computing Fibonacci numbers in O(log n)

### Recognize Counting with Multiplication Principle When:
- Choices at each step are independent
- No constraints between positions
- Answer is product of choices at each step

### Pattern Recognition Checklist:
- [ ] Are positions independent? --> **Multiplication principle**
- [ ] Need a^b for large b? --> **Binary exponentiation**
- [ ] Working with mod? --> **Take mod at each step**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Exponentiation](https://cses.fi/problemset/task/1095) | Basic modular exponentiation |
| [Exponentiation II](https://cses.fi/problemset/task/1712) | Fermat's little theorem extension |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Counting Rooms](https://cses.fi/problemset/task/1192) | Flood fill counting |
| [Dice Combinations](https://cses.fi/problemset/task/1633) | DP instead of direct formula |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Bracket Sequences I](https://cses.fi/problemset/task/2064) | Catalan numbers |
| [Counting Necklaces](https://cses.fi/problemset/task/2209) | Burnside's lemma |
| [Graph Paths I](https://cses.fi/problemset/task/1723) | Matrix exponentiation |

---

## Key Takeaways

1. **The Core Idea:** Counting sequences with n choices and k positions = n^k
2. **Time Optimization:** Binary exponentiation reduces O(k) to O(log k)
3. **Space Trade-off:** O(1) space - no arrays needed
4. **Pattern:** Multiplication principle + modular arithmetic

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why the answer is n^k using the multiplication principle
- [ ] Implement binary exponentiation from scratch
- [ ] Handle modular arithmetic correctly to avoid overflow
- [ ] Identify when a counting problem reduces to a power formula

---

## Additional Resources

- [CP-Algorithms: Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CP-Algorithms: Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html)
- [CSES Distributing Apples](https://cses.fi/problemset/task/1716) - Stars and bars counting
