# Examination Papers

## Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

A professor needs to transfer examination papers from one box to another while maintaining descending order of marks. The rules are:

1. Can only withdraw/place papers from/on top of a pile
2. Three locations available: source box (Chemistry), destination box (CS), and table
3. Papers on the table must be in a single pile
4. A paper with lower marks never comes below a paper with higher marks

This is the classic Tower of Hanoi problem! Compute the number of moves required to transfer N papers.

## Input Format
- First line: T (number of test cases)
- Next T lines: N (number of papers)

## Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 10^9

## Output Format
Print the number of moves required modulo 10^9 + 7 for each test case.

## Solution

### Approach
This is exactly the Tower of Hanoi problem:
- 3 pegs: source, destination, auxiliary (table)
- N disks (papers) of different sizes
- Rule: smaller disk must always be on top

The minimum number of moves for Tower of Hanoi with N disks is **2^N - 1**.

### Python Solution

```python
MOD = 10**9 + 7

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        # Tower of Hanoi formula: 2^n - 1
        result = (pow(2, n, MOD) - 1) % MOD
        print(result)

if __name__ == "__main__":
    solve()
```

### Solution with Fast Modular Exponentiation

```python
MOD = 10**9 + 7

def mod_pow(base, exp, mod):
    """Fast modular exponentiation"""
    result = 1
    base %= mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod

    return result

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        result = (mod_pow(2, n, MOD) - 1 + MOD) % MOD
        print(result)

if __name__ == "__main__":
    solve()
```

### One-liner Solution

```python
def solve():
    M = 10**9 + 7
    t = int(input())
    for _ in range(t):
        print((pow(2, int(input()), M) - 1) % M)

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(log N) for modular exponentiation
- **Space Complexity:** O(1)

### Key Insight
This is the Tower of Hanoi in disguise:
- Chemistry box = Source peg
- CS box = Destination peg
- Table = Auxiliary peg
- Papers ordered by marks = Disks of different sizes

The recurrence relation:
- T(1) = 1
- T(n) = 2 × T(n-1) + 1

Solving: T(n) = 2^n - 1

Since N can be up to 10^9, we need fast modular exponentiation to compute 2^N mod (10^9 + 7).
