# Mattey Multiplication

## Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 512MB

## Problem Statement

Given N and M, write an equation using left shift operators whose result equals N * M.

The equation should be in the form: (N<<p₁) + (N<<p₂) + ... + (N<<pₖ) where p₁ ≥ p₂ ≥ ... ≥ pₖ and k is minimum.

## Input Format
- First line: T (number of test cases)
- Next T lines: two integers N, M

## Constraints
- 1 ≤ T ≤ 5 × 10^4
- 1 ≤ N, M ≤ 10^16

## Output Format
For each test case, print the equation.

## Solution

### Approach
N × M = N × (sum of powers of 2 in M's binary representation)

If M = 2^a + 2^b + 2^c + ..., then:
N × M = (N << a) + (N << b) + (N << c) + ...

Find all bit positions where M has a 1, then output in decreasing order.

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, m = map(int, input().split())

    # Find positions of 1-bits in M
    positions = []
    bit_pos = 0

    while m > 0:
      if m & 1:
        positions.append(bit_pos)
      m >>= 1
      bit_pos += 1

    # Output in decreasing order
    terms = []
    for pos in reversed(positions):
      terms.append(f"({n}<<{pos})")

    print(" + ".join(terms))

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, m = map(int, input().split())

    # Get binary representation and find 1-bit positions
    binary = bin(m)[2:]  # Remove '0b' prefix
    length = len(binary)

    terms = []
    for i, bit in enumerate(binary):
      if bit == '1':
        shift = length - 1 - i
        terms.append(f"({n}<<{shift})")

    print(" + ".join(terms))

if __name__ == "__main__":
  solve()
```

### One-liner Style

```python
def solve():
  t = int(input())
  for _ in range(t):
    n, m = map(int, input().split())
    bits = [i for i in range(m.bit_length()) if m & (1 << i)]
    print(" + ".join(f"({n}<<{b})" for b in reversed(bits)))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(log M) per test case
- **Space Complexity:** O(log M) for storing bit positions

### Key Insight
Multiplication can be decomposed into additions of left shifts:
- N × 5 = N × (4 + 1) = N × (2² + 2⁰) = (N << 2) + (N << 0)
- N × 13 = N × (8 + 4 + 1) = (N << 3) + (N << 2) + (N << 0)

The minimum k is achieved by using exactly the 1-bits in M's binary representation.

### Example
N = 2, M = 5 (binary: 101)
- 1-bits at positions: 0, 2
- Output: (2<<2) + (2<<0) = 8 + 2 = 10 = 2 × 5 ✓
