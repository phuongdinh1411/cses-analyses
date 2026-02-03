---
layout: simple
title: "Stirling Numbers - Combinatorics"
permalink: /problem_soulutions/counting_problems/stirling_numbers_analysis
difficulty: Hard
tags: [combinatorics, dp, counting, permutations, partitions]
---

# Stirling Numbers (First and Second Kind)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Combinatorics / DP |
| **Key Technique** | Dynamic Programming with Recurrence Relations |
| **Applications** | Counting permutations by cycles, set partitions |

### Learning Goals

After studying this topic, you will be able to:
- [ ] Define and distinguish Stirling numbers of the first and second kind
- [ ] Compute Stirling numbers using DP recurrence relations
- [ ] Apply Stirling numbers to count permutations with k cycles
- [ ] Apply Stirling numbers to count ways to partition a set into k non-empty subsets
- [ ] Handle the sign convention for unsigned vs signed Stirling numbers of the first kind

---

## Problem Statement

### Stirling Numbers of the Second Kind: S(n, k)

**Definition:** S(n, k) counts the number of ways to partition a set of n distinct elements into exactly k non-empty, unordered subsets.

**Example:** S(4, 2) = 7 means there are 7 ways to partition {1, 2, 3, 4} into 2 non-empty subsets.

### Stirling Numbers of the First Kind: s(n, k)

**Definition:** The unsigned Stirling number of the first kind |s(n, k)| counts the number of permutations of n elements with exactly k disjoint cycles.

**Sign Convention:** The signed version satisfies: s(n, k) = (-1)^(n-k) * |s(n, k)|

**Example:** |s(4, 2)| = 11 means there are 11 permutations of 4 elements with exactly 2 cycles.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count structured arrangements when order partially matters?

Stirling numbers bridge the gap between simple counting and complex combinatorics:
- **Second Kind S(n,k):** Think of distributing n labeled balls into k identical boxes (non-empty)
- **First Kind |s(n,k)|:** Think of arranging n people into k circular tables

### Breaking Down the Problem

1. **What are we looking for?** Number of ways to structure n elements into k groups
2. **What information do we have?** The total count n and target groups k
3. **What's the relationship?** Each new element either joins an existing group or starts a new one

### Analogies

**Second Kind:** Imagine seating n guests at k identical round tables where every table must have at least one guest. The tables are indistinguishable, but guests are distinguishable.

**First Kind:** Imagine n runners in a relay race forming k separate relay teams, where each team runs in a cycle (the order within each team matters cyclically).

---

## Recurrence Relations

### Stirling Numbers of the Second Kind

```
S(n, k) = k * S(n-1, k) + S(n-1, k-1)
```

**Why?**
- `k * S(n-1, k)`: Element n joins one of k existing subsets (k choices)
- `S(n-1, k-1)`: Element n forms its own singleton subset

### Stirling Numbers of the First Kind (Unsigned)

```
|s(n, k)| = (n-1) * |s(n-1, k)| + |s(n-1, k-1)|
```

**Why?**
- `(n-1) * |s(n-1, k)|`: Element n is inserted after one of (n-1) existing elements in some cycle
- `|s(n-1, k-1)|`: Element n forms its own 1-cycle (fixed point)

### Base Cases

| Case | S(n, k) | \|s(n, k)\| | Reason |
|------|---------|-------------|--------|
| `S(0, 0)` | 1 | 1 | Empty partition of empty set |
| `S(n, 0)` for n > 0 | 0 | 0 | Cannot partition non-empty set into 0 subsets |
| `S(0, k)` for k > 0 | 0 | 0 | Cannot create non-empty subsets from nothing |
| `S(n, n)` | 1 | 1 | Each element in its own subset/cycle |
| `S(n, 1)` | 1 | (n-1)! | One subset: 1 way; One cycle: (n-1)! arrangements |

---

## Dry Run: Computing S(4, 2) and |s(4, 2)|

### Computing S(4, 2) - Second Kind

**Goal:** Count partitions of {1,2,3,4} into 2 non-empty subsets.

```
Build the DP table bottom-up:

n\k |  0    1    2    3    4
----+------------------------
 0  |  1    0    0    0    0
 1  |  0    1    0    0    0
 2  |  0    1    1    0    0
 3  |  0    1    3    1    0
 4  |  0    1    7    6    1

Computing S(4, 2):
  S(4, 2) = 2 * S(3, 2) + S(3, 1)
          = 2 * 3 + 1
          = 7
```

**The 7 partitions of {1,2,3,4} into 2 subsets:**
1. {1} | {2,3,4}
2. {2} | {1,3,4}
3. {3} | {1,2,4}
4. {4} | {1,2,3}
5. {1,2} | {3,4}
6. {1,3} | {2,4}
7. {1,4} | {2,3}

### Computing |s(4, 2)| - First Kind (Unsigned)

**Goal:** Count permutations of {1,2,3,4} with exactly 2 cycles.

```
Build the DP table bottom-up:

n\k |  0    1    2    3    4
----+------------------------
 0  |  1    0    0    0    0
 1  |  0    1    0    0    0
 2  |  0    1    1    0    0
 3  |  0    2    3    1    0
 4  |  0    6   11    6    1

Computing |s(4, 2)|:
  |s(4, 2)| = 3 * |s(3, 2)| + |s(3, 1)|
            = 3 * 3 + 2
            = 11
```

**The 11 permutations with 2 cycles (in cycle notation):**
1. (1)(234) - 1 fixed, 2->3->4->2
2. (1)(243) - 1 fixed, 2->4->3->2
3. (2)(134)
4. (2)(143)
5. (3)(124)
6. (3)(142)
7. (4)(123)
8. (4)(132)
9. (12)(34)
10. (13)(24)
11. (14)(23)

---

## Common Mistakes

### Mistake 1: Confusing the Two Kinds

```python
# WRONG: Using second kind formula for first kind
s[n][k] = k * s[n-1][k] + s[n-1][k-1]  # This is S(n,k)!

# CORRECT: First kind uses (n-1) multiplier
s[n][k] = (n-1) * s[n-1][k] + s[n-1][k-1]
```

**Problem:** The recurrences look similar but have different multipliers.
**Fix:** Remember - Second kind: k (choices of subset), First kind: (n-1) (positions to insert).

### Mistake 2: Sign Errors in First Kind

```python
# WRONG: Ignoring sign for signed Stirling numbers
signed_s = unsigned_s  # Missing sign!

# CORRECT: Apply sign based on parity
signed_s = ((-1) ** (n - k)) * unsigned_s
```

**Problem:** The signed version alternates based on (n-k).
**Fix:** Use `(-1)^(n-k)` factor when signed version is needed.

### Mistake 3: Wrong Base Cases

```python
# WRONG: Forgetting S(n,1) for first kind
s[n][1] = 1  # This is for second kind!

# CORRECT: First kind single cycle
s[n][1] = factorial(n - 1)  # (n-1)! circular arrangements
```

**Problem:** S(n,1) = 1 but |s(n,1)| = (n-1)!
**Fix:** Remember that one cycle of n elements has (n-1)! arrangements.

### Mistake 4: Integer Overflow

```python
# WRONG: No modular arithmetic for large values
S[n][k] = k * S[n-1][k] + S[n-1][k-1]

# CORRECT: Apply modulo at each step
MOD = 10**9 + 7
S[n][k] = (k * S[n-1][k] + S[n-1][k-1]) % MOD
```

---

## Edge Cases

| Case | S(n, k) | \|s(n, k)\| | Reason |
|------|---------|-------------|--------|
| n = 0, k = 0 | 1 | 1 | Empty partition exists |
| n > 0, k = 0 | 0 | 0 | Impossible |
| k > n | 0 | 0 | More groups than elements |
| n = k | 1 | 1 | Singletons only |
| k = 1 | 1 | (n-1)! | One group/one cycle |
| k = n - 1 | C(n,2) | C(n,2) | One pair, rest singletons |

---

## When to Use This Pattern

### Use Stirling Numbers of the Second Kind When:
- Partitioning labeled objects into unlabeled groups
- Counting surjections (onto functions) from n to k elements
- Distribution problems with identical boxes
- Computing Bell numbers (sum over all k)

### Use Stirling Numbers of the First Kind When:
- Counting permutations by cycle structure
- Analyzing random permutations
- Computing rising/falling factorials
- Problems involving derangements generalized to k cycles

### Pattern Recognition Checklist:
- [ ] Partitioning a set into groups? Check if order within groups matters
- [ ] Counting permutations? Check if cycle structure is relevant
- [ ] Distribution problem? Determine if containers are distinguishable
- [ ] Polynomial expansion? Check for falling factorial connections

---

## Solutions

### Python Implementation

```python
def stirling_second_kind(n: int, k: int, mod: int = None) -> int:
    """
    Compute S(n, k) - Stirling number of the second kind.
    Counts partitions of n elements into k non-empty subsets.

    Time: O(n * k)
    Space: O(k) with space optimization
    """
    if k > n or k < 0:
        return 0
    if k == 0:
        return 1 if n == 0 else 0

    # Space-optimized DP
    dp = [0] * (k + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        # Traverse right to left to avoid overwriting
        for j in range(min(i, k), 0, -1):
            dp[j] = j * dp[j] + dp[j - 1]
            if mod:
                dp[j] %= mod

    return dp[k]


def stirling_first_kind_unsigned(n: int, k: int, mod: int = None) -> int:
    """
    Compute |s(n, k)| - Unsigned Stirling number of the first kind.
    Counts permutations of n elements with exactly k cycles.

    Time: O(n * k)
    Space: O(k) with space optimization
    """
    if k > n or k < 0:
        return 0
    if k == 0:
        return 1 if n == 0 else 0

    # Space-optimized DP
    dp = [0] * (k + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        # Traverse right to left to avoid overwriting
        for j in range(min(i, k), 0, -1):
            dp[j] = (i - 1) * dp[j] + dp[j - 1]
            if mod:
                dp[j] %= mod
        dp[0] = 0  # s(i, 0) = 0 for i > 0

    return dp[k]


def stirling_second_kind_table(n: int, mod: int = None) -> list:
    """
    Build full table of S(i, j) for 0 <= i <= n, 0 <= j <= i.

    Time: O(n^2)
    Space: O(n^2)
    """
    S = [[0] * (n + 1) for _ in range(n + 1)]
    S[0][0] = 1

    for i in range(1, n + 1):
        for j in range(1, i + 1):
            S[i][j] = j * S[i-1][j] + S[i-1][j-1]
            if mod:
                S[i][j] %= mod

    return S


def stirling_first_kind_table(n: int, mod: int = None) -> list:
    """
    Build full table of |s(i, j)| for 0 <= i <= n, 0 <= j <= i.

    Time: O(n^2)
    Space: O(n^2)
    """
    s = [[0] * (n + 1) for _ in range(n + 1)]
    s[0][0] = 1

    for i in range(1, n + 1):
        for j in range(1, i + 1):
            s[i][j] = (i - 1) * s[i-1][j] + s[i-1][j-1]
            if mod:
                s[i][j] %= mod

    return s


# Example usage
if __name__ == "__main__":
    print("S(4, 2) =", stirling_second_kind(4, 2))  # Output: 7
    print("|s(4, 2)| =", stirling_first_kind_unsigned(4, 2))  # Output: 11

    # Print full tables
    print("\nStirling Second Kind Table S(n,k):")
    S = stirling_second_kind_table(5)
    for i in range(6):
        print(f"n={i}:", S[i][:i+1])

    print("\nStirling First Kind Table |s(n,k)|:")
    s = stirling_first_kind_table(5)
    for i in range(6):
        print(f"n={i}:", s[i][:i+1])
```

### C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1e9 + 7;

class StirlingNumbers {
public:
    // Compute S(n, k) - Stirling second kind
    static long long secondKind(int n, int k) {
        if (k > n || k < 0) return 0;
        if (k == 0) return (n == 0) ? 1 : 0;

        vector<long long> dp(k + 1, 0);
        dp[0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int j = min(i, k); j >= 1; j--) {
                dp[j] = (1LL * j * dp[j] % MOD + dp[j-1]) % MOD;
            }
            dp[0] = 0;
        }

        return dp[k];
    }

    // Compute |s(n, k)| - Unsigned Stirling first kind
    static long long firstKindUnsigned(int n, int k) {
        if (k > n || k < 0) return 0;
        if (k == 0) return (n == 0) ? 1 : 0;

        vector<long long> dp(k + 1, 0);
        dp[0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int j = min(i, k); j >= 1; j--) {
                dp[j] = (1LL * (i - 1) * dp[j] % MOD + dp[j-1]) % MOD;
            }
            dp[0] = 0;
        }

        return dp[k];
    }

    // Build full table for S(n, k)
    static vector<vector<long long>> secondKindTable(int n) {
        vector<vector<long long>> S(n + 1, vector<long long>(n + 1, 0));
        S[0][0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                S[i][j] = (1LL * j * S[i-1][j] % MOD + S[i-1][j-1]) % MOD;
            }
        }

        return S;
    }

    // Build full table for |s(n, k)|
    static vector<vector<long long>> firstKindTable(int n) {
        vector<vector<long long>> s(n + 1, vector<long long>(n + 1, 0));
        s[0][0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                s[i][j] = (1LL * (i - 1) * s[i-1][j] % MOD + s[i-1][j-1]) % MOD;
            }
        }

        return s;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "S(4, 2) = " << StirlingNumbers::secondKind(4, 2) << "\n";  // 7
    cout << "|s(4, 2)| = " << StirlingNumbers::firstKindUnsigned(4, 2) << "\n";  // 11

    // Print tables
    cout << "\nStirling Second Kind Table:\n";
    auto S = StirlingNumbers::secondKindTable(5);
    for (int i = 0; i <= 5; i++) {
        cout << "n=" << i << ": ";
        for (int j = 0; j <= i; j++) {
            cout << S[i][j] << " ";
        }
        cout << "\n";
    }

    cout << "\nStirling First Kind Table (unsigned):\n";
    auto s = StirlingNumbers::firstKindTable(5);
    for (int i = 0; i <= 5; i++) {
        cout << "n=" << i << ": ";
        for (int j = 0; j <= i; j++) {
            cout << s[i][j] << " ";
        }
        cout << "\n";
    }

    return 0;
}
```

---

## Applications and Identities

### Key Identities

**Sum to factorial (First Kind):**
```
Sum over k from 0 to n of |s(n, k)| = n!
```
All permutations partitioned by cycle count.

**Sum to Bell number (Second Kind):**
```
B(n) = Sum over k from 0 to n of S(n, k)
```
Bell number counts all partitions of n elements.

**Falling Factorial Expansion:**
```
x^(n) = x(x-1)(x-2)...(x-n+1) = Sum over k of s(n,k) * x^k
```

**Rising Factorial Expansion:**
```
x^n = Sum over k of S(n,k) * x^(k)
```
where x^(k) is the falling factorial.

**Surjections Count:**
```
Number of surjections from n to k = k! * S(n, k)
```

### Practical Applications

| Application | Stirling Type | Formula |
|-------------|---------------|---------|
| Distribute n items into k identical boxes | Second Kind | S(n, k) |
| Onto functions from n-set to k-set | Second Kind | k! * S(n, k) |
| Permutations with k cycles | First Kind | \|s(n, k)\| |
| Expected cycles in random permutation | First Kind | H_n (harmonic) |
| Polynomial basis conversion | Both | Coefficient formulas |

---

## Related Problems

### Prerequisites (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Counting Combinations (CSES)](https://cses.fi/problemset/task/1079) | Basic combinatorics |
| [Distributing Apples (CSES)](https://cses.fi/problemset/task/1716) | Stars and bars method |

### Direct Applications
| Problem | Connection |
|---------|------------|
| [Creating Strings II (CSES)](https://cses.fi/problemset/task/1715) | Multinomial coefficients |
| [Codeforces - Mashmokh and ACM](https://codeforces.com/contest/414/problem/B) | S(n,k) with divisibility |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Codeforces - Count Good Substrings](https://codeforces.com/contest/451/problem/D) | Combinatorics with constraints |
| [AtCoder - Choose Integers (ABC)](https://atcoder.jp/contests/abc156/tasks/abc156_d) | Counting arrangements |

---

## Key Takeaways

1. **The Core Idea:** Stirling numbers count structured partitions - either unordered subsets (Second Kind) or cyclic arrangements (First Kind).

2. **Recurrence Pattern:** Both follow similar DP structure: new element either extends existing structure or creates new one.

3. **Sign Convention:** Unsigned first kind for counting; signed first kind for polynomial identities.

4. **Applications:** Foundation for Bell numbers, surjection counting, and polynomial basis transformations.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Write both recurrences from memory
- [ ] Compute small values by hand (up to n=5)
- [ ] Explain the combinatorial meaning of each kind
- [ ] Implement space-optimized DP in under 10 minutes
- [ ] Apply to counting surjections and set partitions
