# Boxes of Chocolates

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Pippy has chocolates in nested boxes. She wants to share with N friends equally. If she can't divide equally, her cat Kittu gets the remainder.

Each box can contain smaller boxes inside. Only the smallest boxes contain actual chocolates. Calculate the total chocolates and find the remainder when divided by N.

## Input Format
- T test cases
- Each test case:
  - First line: N (friends), B (boxes)
  - Next B lines: K followed by K integers a1, a2, ..., aK describing nested structure
  - ai indicates boxes inside, last number is chocolate count in smallest boxes

## Constraints
- T, B, K < 101
- N, ai < 10001

## Output Format
For each test case, print the remainder (chocolates for Kittu).

## Example
```
Input:
1
5 2
3 2 3 4
2 4 5

Output:
4
```
With N=5 friends and B=2 boxes: First box has structure 2 x 3 x 4 = 24 chocolates. Second box has 4 x 5 = 20 chocolates. Total = 44. Remainder when divided by 5 is 44 % 5 = 4.

## Solution

### Approach
Parse the nested box structure recursively or iteratively. Calculate total chocolates by multiplying counts through nesting levels. Use modular arithmetic to avoid overflow.

The structure: a1 boxes each containing a2 boxes, each containing a3, etc. Final number is chocolates per smallest box.
Total = a1 × a2 × ... × aK (where aK is chocolates in smallest box)

### Python Solution

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

### Alternative Solution with Detailed Comments

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

### Recursive Interpretation

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

### Complexity Analysis
- **Time Complexity:** O(B × K) per test case
- **Space Complexity:** O(K)

### Key Insight
Each box description gives a nested structure where the total chocolates is the product of all values. The first K-1 values are box counts at each nesting level, and the last value is chocolates per smallest box. Use modular arithmetic throughout to handle large products.
