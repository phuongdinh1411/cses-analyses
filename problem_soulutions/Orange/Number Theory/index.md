---
layout: simple
title: "Number Theory"
permalink: /problem_soulutions/Orange/Number Theory/
---
# Number Theory

Problems involving mathematical concepts such as prime numbers, divisibility, modular arithmetic, and other number-theoretic algorithms.

## Problems

### Boxes of Chocolates

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Pippy has chocolates in nested boxes. She wants to share with N friends equally. If she can't divide equally, her cat Kittu gets the remainder.

Each box can contain smaller boxes inside. Only the smallest boxes contain actual chocolates. Calculate the total chocolates and find the remainder when divided by N.

#### Input Format
- T test cases
- Each test case:
  - First line: N (friends), B (boxes)
  - Next B lines: K followed by K integers a1, a2, ..., aK describing nested structure
  - ai indicates boxes inside, last number is chocolate count in smallest boxes

#### Constraints
- T, B, K < 101
- N, ai < 10001

#### Output Format
For each test case, print the remainder (chocolates for Kittu).

#### Solution

##### Approach
Parse the nested box structure recursively or iteratively. Calculate total chocolates by multiplying counts through nesting levels. Use modular arithmetic to avoid overflow.

The structure: a1 boxes each containing a2 boxes, each containing a3, etc. Final number is chocolates per smallest box.
Total = a1 × a2 × ... × aK (where aK is chocolates in smallest box)

##### Python Solution

```python
def solve():
    t = int(input())

    for _ in range(t):
        n, b = map(int, input().split())

        total = 0

        for _ in range(b):
            line = list(map(int, input().split()))
            k = line[0]
            values = line[1:k+1]

            # Calculate chocolates from this box structure
            # Product of all values
            product = 1
            for v in values:
                product = (product * v) % n

            total = (total + product) % n

        print(total)

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    t = int(input())

    for _ in range(t):
        n, b = map(int, input().split())

        total_chocolates = 0

        for _ in range(b):
            parts = list(map(int, input().split()))
            k = parts[0]
            box_structure = parts[1:k+1]

            # The structure means:
            # box_structure[0] boxes, each containing
            # box_structure[1] boxes, each containing
            # ... and so on
            # Final value is chocolates in smallest box

            # Total from this box = product of all values
            chocolates = 1
            for val in box_structure:
                chocolates *= val
                chocolates %= n  # Keep modular to avoid overflow

            total_chocolates += chocolates
            total_chocolates %= n

        print(total_chocolates)

if __name__ == "__main__":
    solve()
```

##### Recursive

```python
def solve():
    t = int(input())

    for _ in range(t):
        n, b = map(int, input().split())

        total = 0

        for _ in range(b):
            line = input().split()
            k = int(line[0])
            values = [int(line[i]) for i in range(1, k + 1)]

            # Nested boxes: multiply all levels
            product = 1
            for v in values:
                product = (product * v) % n

            total = (total + product) % n

        print(total)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(B × K) per test case
- **Space Complexity:** O(K)

##### Key Insight
Each box description gives a nested structure where the total chocolates is the product of all values. The first K-1 values are box counts at each nesting level, and the last value is chocolates per smallest box. Use modular arithmetic throughout to handle large products.

---

### Drazil and His Happy Friends

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Drazil has many friends. Some of them are happy and some of them are unhappy. Drazil wants to make all his friends become happy. So he invented the following plan.

There are n boys and m girls among his friends. Let's number them from 0 to n-1 and 0 to m-1 separately. In i-th day, Drazil invites (i % n)-th boy and (i % m)-th girl to have dinner together (as Drazil is programmer, i starts from 0). If one of those two people is happy, the other one will also become happy. Otherwise, those two people remain in their states. Once a person becomes happy (or if he/she was happy originally), he stays happy forever.

Drazil wants to know whether he can use this plan to make all his friends become happy at some moment.

#### Input Format
- The first line contains two integers n and m (1 ≤ n, m ≤ 100).
- The second line contains an integer b (0 ≤ b ≤ n), denoting the number of happy boys, followed by b distinct integers x1, x2, ..., xb (0 ≤ xi < n), denoting the indices of happy boys.
- The third line contains an integer g (0 ≤ g ≤ m), denoting the number of happy girls, followed by g distinct integers y1, y2, ..., yg (0 ≤ yj < m), denoting the indices of happy girls.
- It is guaranteed that there is at least one person that is unhappy.

#### Output Format
If Drazil can make all his friends become happy by this plan, print "Yes". Otherwise, print "No".

#### Solution

##### Approach
The key insight is based on number theory:
- On day i, boy (i % n) meets girl (i % m)
- The pattern repeats after LCM(n, m) days
- We simulate for n × m days (which is sufficient since LCM(n,m) ≤ n×m)
- If happiness can spread, it will within this period

##### Python Solution

```python
def solve():
    n, m = map(int, input().split())

    # Read happy boys
    line = list(map(int, input().split()))
    b = line[0]
    happy_boys = set(line[1:b+1]) if b > 0 else set()

    # Read happy girls
    line = list(map(int, input().split()))
    g = line[0]
    happy_girls = set(line[1:g+1]) if g > 0 else set()

    # Simulate for n * m days (covers full cycle)
    for day in range(n * m):
        boy = day % n
        girl = day % m

        # If either is happy, both become happy
        if boy in happy_boys or girl in happy_girls:
            happy_boys.add(boy)
            happy_girls.add(girl)

    # Check if everyone is happy
    if len(happy_boys) == n and len(happy_girls) == m:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
import math

def solve():
    n, m = map(int, input().split())

    line = list(map(int, input().split()))
    b = line[0]
    happy_boys = [False] * n
    for i in range(1, b + 1):
        happy_boys[line[i]] = True

    line = list(map(int, input().split()))
    g = line[0]
    happy_girls = [False] * m
    for i in range(1, g + 1):
        happy_girls[line[i]] = True

    # Simulate for lcm(n, m) days - use n*m as upper bound
    lcm = (n * m) // math.gcd(n, m)

    for day in range(lcm):
        boy = day % n
        girl = day % m

        if happy_boys[boy] or happy_girls[girl]:
            happy_boys[boy] = True
            happy_girls[girl] = True

    if all(happy_boys) and all(happy_girls):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n × m)
- **Space Complexity:** O(n + m)

##### Key Insight
The meeting pattern between boys and girls forms a cycle based on LCM(n, m). If happiness cannot spread to everyone within this cycle, it never will.

---

### Gargari and Bishops

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Place two bishops on an n×n chessboard such that:
1. No cell is attacked by both bishops
2. Sum of values of all attacked cells is maximized

Bishops attack along diagonals. A cell is attacked if it's on any diagonal of a bishop.

#### Input Format
- First line: n (2 ≤ n ≤ 2000)
- Next n lines: n integers aij (0 ≤ aij ≤ 10^9) - cell values

#### Output Format
- Line 1: Maximum total value
- Line 2: x1, y1, x2, y2 (positions of two bishops, 1-indexed)

#### Solution

##### Approach
Two diagonals through (i, j):
- Main diagonal: i - j (constant)
- Anti-diagonal: i + j (constant)

Two bishops don't share cells if they're on diagonals of different "parity":
- Bishop 1 on cell where (i + j) is even
- Bishop 2 on cell where (i + j) is odd

Precompute sum of each diagonal, then for each cell compute total attack value. Find best cell for each parity.

##### Python Solution

```python
def solve():
    n = int(input())
    board = []
    for _ in range(n):
        row = list(map(int, input().split()))
        board.append(row)

    # Diagonal sums
    # Main diagonal: indexed by i - j (range: -(n-1) to n-1)
    # Anti diagonal: indexed by i + j (range: 0 to 2n-2)

    main_diag = {}  # i - j -> sum
    anti_diag = {}  # i + j -> sum

    for i in range(n):
        for j in range(n):
            d1 = i - j
            d2 = i + j

            main_diag[d1] = main_diag.get(d1, 0) + board[i][j]
            anti_diag[d2] = anti_diag.get(d2, 0) + board[i][j]

    # For each cell, compute bishop value (don't double count the cell itself)
    # bishop_value[i][j] = main_diag[i-j] + anti_diag[i+j] - board[i][j]

    best_even = (-1, -1, -1)  # (value, i, j)
    best_odd = (-1, -1, -1)

    for i in range(n):
        for j in range(n):
            val = main_diag[i - j] + anti_diag[i + j] - board[i][j]
            parity = (i + j) % 2

            if parity == 0:
                if val > best_even[0]:
                    best_even = (val, i, j)
            else:
                if val > best_odd[0]:
                    best_odd = (val, i, j)

    total = best_even[0] + best_odd[0]
    # Convert to 1-indexed
    x1, y1 = best_even[1] + 1, best_even[2] + 1
    x2, y2 = best_odd[1] + 1, best_odd[2] + 1

    print(total)
    print(x1, y1, x2, y2)

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]

    # Diagonal sums using arrays
    # Main: i - j + (n-1) maps to range [0, 2n-2]
    # Anti: i + j maps to range [0, 2n-2]

    main = [0] * (2 * n - 1)
    anti = [0] * (2 * n - 1)

    for i in range(n):
        for j in range(n):
            main[i - j + n - 1] += board[i][j]
            anti[i + j] += board[i][j]

    # Find best positions for each parity
    best = [(-1, 0, 0), (-1, 0, 0)]  # [even_parity, odd_parity]

    for i in range(n):
        for j in range(n):
            score = main[i - j + n - 1] + anti[i + j] - board[i][j]
            parity = (i + j) % 2

            if score > best[parity][0]:
                best[parity] = (score, i + 1, j + 1)

    total = best[0][0] + best[1][0]
    print(total)
    print(best[0][1], best[0][2], best[1][1], best[1][2])

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n²)
- **Space Complexity:** O(n)

##### Key Insight
Two bishops on cells with different (i+j) parity never share diagonals. Precompute sum for each diagonal, then for each cell compute total attack value in O(1). This avoids O(n³) brute force. The cell itself appears in both its diagonals, so subtract it once to avoid double-counting.

---

### Ones

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

For any integer n (not divisible by 2 or 5), find the smallest number consisting only of 1s that is divisible by n.

Output the number of digits in this smallest "repunit".

#### Input Format
- Multiple test cases until EOF
- Each line: integer n (0 < n ≤ 10000, not divisible by 2 or 5)

#### Output Format
For each n, print the number of 1s in the smallest repunit divisible by n.

#### Solution

##### Approach
A repunit with k digits is: (10^k - 1) / 9

We need the smallest k such that n divides (10^k - 1) / 9.

Since gcd(n, 9) might not be 1, we work with: find smallest k where 10^k ≡ 1 (mod 9n/gcd(9,n))

Simpler approach: directly compute remainders.
- Start with remainder = 1
- Keep appending 1s: remainder = (remainder * 10 + 1) % n
- Count until remainder = 0

##### Python Solution

```python
def solve():
    import sys

    for line in sys.stdin:
        n = int(line.strip())
        if n == 0:
            continue

        # Find smallest repunit divisible by n
        # repunit(k) = 111...1 (k ones) = (10^k - 1) / 9

        remainder = 1 % n
        count = 1

        while remainder != 0:
            remainder = (remainder * 10 + 1) % n
            count += 1

        print(count)

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def min_repunit_digits(n):
    """
    Find minimum k such that 111...1 (k ones) is divisible by n.

    The number with k ones is: (10^k - 1) / 9

    We iterate: r_1 = 1, r_k = r_{k-1} * 10 + 1
    Stop when r_k ≡ 0 (mod n)
    """
    if n == 1:
        return 1

    remainder = 1
    digits = 1

    while remainder % n != 0:
        remainder = (remainder * 10 + 1) % n
        digits += 1

    return digits

def solve():
    import sys
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        n = int(line)
        print(min_repunit_digits(n))

if __name__ == "__main__":
    solve()
```

##### Mathematical

```python
def solve():
    """
    For n not divisible by 2 or 5, a repunit divisible by n always exists.

    By pigeonhole principle, since there are only n possible remainders,
    within n+1 iterations we must find a repeat, and since we start at 1,
    we'll eventually hit 0.
    """
    import sys

    for line in sys.stdin:
        n = int(line.strip())

        r = 1
        k = 1

        while r != 0:
            r = (r * 10 + 1) % n
            k += 1

        print(k)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n) per test case (at most n iterations by pigeonhole)
- **Space Complexity:** O(1)

##### Key Insight
A repunit 111...1 with k digits equals (10^k - 1)/9. Since n is coprime with 10 (not divisible by 2 or 5), by Fermat's little theorem a solution exists. We simulate building the repunit digit by digit, tracking remainder mod n, until we find remainder 0.

---

### Play with Floor and Ceil

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

For any integers x and k, there exist integers p and q such that:
x = p × floor(x/k) + q × ceil(x/k)

Given x and k, find p and q.

#### Input Format
- T test cases (1 ≤ T ≤ 1000)
- Each test case: two positive integers x and k (< 10^8)

#### Output Format
For each test case, print p and q (space-separated).

#### Solution

##### Approach
Let a = floor(x/k) and b = ceil(x/k).

If x is divisible by k: a = b = x/k, so x = (x/k) × k means p + q = k works.
Simple solution: p = k, q = 0.

If x is not divisible by k: b = a + 1.
We need: p × a + q × (a + 1) = x
→ (p + q) × a + q = x
→ p × a + q × a + q = x

Using Extended Euclidean Algorithm to solve: p × a + q × b = x
Since gcd(a, b) = gcd(a, a+1) = 1, solution always exists.

##### Python Solution

```python
def extended_gcd(a, b):
    """Returns (gcd, x, y) such that a*x + b*y = gcd"""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def solve():
    t = int(input())

    for _ in range(t):
        x, k = map(int, input().split())

        a = x // k          # floor(x/k)
        b = (x + k - 1) // k  # ceil(x/k)

        if a == b:
            # x is divisible by k
            # x = p*a + q*a = (p+q)*a
            # So p + q = x/a = k
            print(k, 0)
        else:
            # a and b differ by 1, gcd(a, b) = 1
            # Solve p*a + q*b = x using extended Euclidean
            gcd, p0, q0 = extended_gcd(a, b)

            # p0*a + q0*b = 1
            # So (p0*x)*a + (q0*x)*b = x
            p = p0 * x
            q = q0 * x

            print(p, q)

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    t = int(input())

    for _ in range(t):
        x, k = map(int, input().split())

        floor_val = x // k
        ceil_val = -(-x // k)  # Ceiling division trick

        if floor_val == ceil_val:
            # x divisible by k
            print(k, 0)
        else:
            # floor_val and ceil_val differ by 1
            # ceil_val = floor_val + 1
            # Need: p * floor_val + q * (floor_val + 1) = x
            # Let r = x % k (remainder)
            # Then x = floor_val * k + r
            # And ceil_val = floor_val + 1

            # p * floor_val + q * ceil_val = x
            # With gcd = 1, use extended Euclidean
            a, b = floor_val, ceil_val

            # Extended GCD for consecutive integers
            # gcd(a, a+1) = 1
            # a*1 + (a+1)*(-a) + (a+1) = a - a^2 - a + a + 1 = 1
            # So: a*(-a) + (a+1)*(a+1-1) = a*(-a) + (a+1)*a = -a^2 + a^2 + a = a... wrong

            # Direct: a*1 + b*0 when b=a (not applicable here)
            # For a, a+1: 1 = (a+1) - a = a*(-1) + (a+1)*1
            # So p0 = -1, q0 = 1 gives a*(-1) + (a+1)*1 = 1

            p = -x
            q = x

            print(p, q)

if __name__ == "__main__":
    solve()
```

##### Simplified

```python
def solve():
    t = int(input())

    for _ in range(t):
        x, k = map(int, input().split())

        a = x // k  # floor
        b = (x + k - 1) // k  # ceil

        if a == b:
            print(k, 0)
        else:
            # gcd(a, a+1) = 1
            # a * (-1) + (a+1) * 1 = 1
            # Multiply by x: a * (-x) + (a+1) * x = x
            print(-x, x)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(1) per test case
- **Space Complexity:** O(1)

##### Key Insight
When floor(x/k) ≠ ceil(x/k), they differ by exactly 1, making gcd = 1. For consecutive integers a and a+1: a×(-1) + (a+1)×1 = 1. Multiply by x to get the solution: p = -x, q = x. When floor = ceil, x is divisible by k, and p = k, q = 0 works.

---

### Problem Makes Problem

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

How many ways can you make n by adding k non-negative integers?

For example, n=4 with k=3 has 15 solutions (like 0+0+4, 0+1+3, 1+1+2, etc.).

#### Input Format
- T test cases
- Each test case: two integers n and k

#### Output Format
For each test case, print the number of ways modulo 10^9+7.

#### Solution

##### Approach
This is the Stars and Bars combinatorics problem.

The number of ways to distribute n identical items into k distinct bins (where bins can be empty) is:
C(n + k - 1, k - 1) = C(n + k - 1, n)

Use modular arithmetic and precompute factorials for efficient computation.

##### Python Solution

```python
def solve():
    MOD = 10**9 + 7
    MAX = 2 * 10**6 + 10

    # Precompute factorials and inverse factorials
    fact = [1] * MAX
    for i in range(1, MAX):
        fact[i] = fact[i-1] * i % MOD

    # Modular inverse using Fermat's little theorem
    inv_fact = [1] * MAX
    inv_fact[MAX-1] = pow(fact[MAX-1], MOD-2, MOD)
    for i in range(MAX-2, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD

    t = int(input())
    for case in range(1, t+1):
        n, k = map(int, input().split())

        # Stars and Bars: C(n + k - 1, k - 1)
        result = nCr(n + k - 1, k - 1)
        print(f"Case {case}: {result}")

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    MOD = 10**9 + 7

    # Precompute
    MAXN = 2000005
    fact = [1] * MAXN
    inv = [1] * MAXN
    inv_fact = [1] * MAXN

    for i in range(2, MAXN):
        fact[i] = fact[i-1] * i % MOD
        inv[i] = (MOD - MOD // i) * inv[MOD % i] % MOD
        inv_fact[i] = inv_fact[i-1] * inv[i] % MOD

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD

    t = int(input())
    for case in range(1, t + 1):
        n, k = map(int, input().split())
        # Ways = C(n+k-1, k-1)
        ans = C(n + k - 1, k - 1)
        print(f"Case {case}: {ans}")

if __name__ == "__main__":
    solve()
```

### Lucas Theorem Solution (for larger moduli)

```python
def solve():
    MOD = 10**9 + 7

    def power(base, exp, mod):
        result = 1
        base %= mod
        while exp > 0:
            if exp & 1:
                result = result * base % mod
            exp >>= 1
            base = base * base % mod
        return result

    def mod_inverse(a, mod):
        return power(a, mod - 2, mod)

    # Precompute factorials up to expected max
    MAX = 2 * 10**6 + 5
    fact = [1] * MAX
    for i in range(1, MAX):
        fact[i] = fact[i-1] * i % MOD

    inv_fact = [1] * MAX
    inv_fact[MAX-1] = mod_inverse(fact[MAX-1], MOD)
    for i in range(MAX-2, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD

    def nCr(n, r):
        if r > n or r < 0:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD

    t = int(input())
    for case in range(1, t+1):
        n, k = map(int, input().split())
        print(f"Case {case}: {nCr(n + k - 1, k - 1)}")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(MAX) for precomputation, O(1) per query
- **Space Complexity:** O(MAX)

##### Key Insight
This is the classic "Stars and Bars" combinatorics problem. We need to place n identical objects (stars) into k bins using k-1 dividers (bars). The total positions are n + k - 1, and we choose k - 1 for bars (or equivalently n for stars): C(n + k - 1, k - 1).

---

### Train Time Table

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

A train line has stations A and B. Trains travel both ways. After arriving, a train needs turnaround time T before it can depart again.

Given all trips (departure/arrival times), find the minimum trains needed at each station to cover all departures.

#### Input Format
- N test cases
- Each test case:
  - First line: T (turnaround time in minutes)
  - Second line: NA, NB (trips from A to B, and B to A)
  - Next NA lines: departure and arrival times for A→B trips (HH:MM format)
  - Next NB lines: departure and arrival times for B→A trips

#### Output Format
For each test case: "Case #x: a b" where a = trains starting at A, b = trains starting at B.

#### Solution

##### Approach
Use greedy simulation with events:
1. Create events for all departures and arrivals
2. Sort by time
3. Track available trains at each station
4. When a train departs, use an available one or add a new train
5. When a train arrives (after turnaround), it becomes available

##### Python Solution

```python
def solve():
    n = int(input())

    for case in range(1, n + 1):
        t = int(input())  # turnaround time
        na, nb = map(int, input().split())

        def parse_time(s):
            h, m = map(int, s.split(':'))
            return h * 60 + m

        events = []  # (time, type, station)
        # type: 0 = departure, 1 = arrival (ready after turnaround)

        for _ in range(na):
            dep, arr = input().split()
            dep_time = parse_time(dep)
            arr_time = parse_time(arr) + t  # ready after turnaround
            events.append((dep_time, 0, 'A'))  # depart from A
            events.append((arr_time, 1, 'B'))  # arrive at B (available)

        for _ in range(nb):
            dep, arr = input().split()
            dep_time = parse_time(dep)
            arr_time = parse_time(arr) + t
            events.append((dep_time, 0, 'B'))  # depart from B
            events.append((arr_time, 1, 'A'))  # arrive at A (available)

        # Sort: by time, then arrivals before departures (type 1 before 0)
        events.sort(key=lambda x: (x[0], -x[1]))

        available = {'A': 0, 'B': 0}
        needed = {'A': 0, 'B': 0}

        for time, event_type, station in events:
            if event_type == 0:  # departure
                if available[station] > 0:
                    available[station] -= 1
                else:
                    needed[station] += 1
            else:  # arrival (train becomes available)
                available[station] += 1

        print(f"Case #{case}: {needed['A']} {needed['B']}")

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
import heapq

def solve():
    n = int(input())

    for case in range(1, n + 1):
        t = int(input())
        na, nb = map(int, input().split())

        def to_minutes(s):
            h, m = s.split(':')
            return int(h) * 60 + int(m)

        # Collect all trips
        trips_from_a = []
        trips_from_b = []

        for _ in range(na):
            parts = input().split()
            dep = to_minutes(parts[0])
            arr = to_minutes(parts[1])
            trips_from_a.append((dep, arr))

        for _ in range(nb):
            parts = input().split()
            dep = to_minutes(parts[0])
            arr = to_minutes(parts[1])
            trips_from_b.append((dep, arr))

        trips_from_a.sort()
        trips_from_b.sort()

        # available_at_X is a min-heap of times when trains become available at X
        available_a = []
        available_b = []
        trains_a = 0
        trains_b = 0

        # Process trips from A
        for dep, arr in trips_from_a:
            # Check if train available at A before dep
            while available_a and available_a[0] <= dep:
                heapq.heappop(available_a)
                # Train is ready but we'll use one
            if available_a and available_a[0] <= dep:
                heapq.heappop(available_a)
            else:
                # Need to check heap properly
                pass

        # Actually, let's use the event-based approach properly
        # Reset and redo

        events = []
        for dep, arr in trips_from_a:
            events.append((dep, 0, 'A'))
            events.append((arr + t, 1, 'B'))
        for dep, arr in trips_from_b:
            events.append((dep, 0, 'B'))
            events.append((arr + t, 1, 'A'))

        events.sort(key=lambda x: (x[0], -x[1]))

        avail = {'A': 0, 'B': 0}
        need = {'A': 0, 'B': 0}

        for tm, typ, st in events:
            if typ == 0:
                if avail[st] > 0:
                    avail[st] -= 1
                else:
                    need[st] += 1
            else:
                avail[st] += 1

        print(f"Case #{case}: {need['A']} {need['B']}")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O((NA + NB) log(NA + NB))
- **Space Complexity:** O(NA + NB)

##### Key Insight
Model as an event simulation. Each trip creates two events: departure (needs a train) and arrival (train becomes available after turnaround). Process events chronologically. When departing, use an available train if possible, otherwise allocate a new one. Sort ties so arrivals process before departures at the same time.

