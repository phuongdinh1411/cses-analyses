# Splitting Numbers

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

## Problem Statement

We define the operation of splitting a binary number n into two numbers a(n), b(n) as follows:

Let 0 ≤ i1 < i2 < ... < ik be the indices of the bits (with the least significant bit having index 0) in n that are 1. Then:
- The indices of the bits of a(n) that are 1 are i1, i3, i5, ... (odd-positioned 1s)
- The indices of the bits of b(n) that are 1 are i2, i4, i6, ... (even-positioned 1s)

For example, if n is 110110101 in binary:
- The 1-bits are at positions: 0, 2, 4, 5, 7, 8 (from right to left)
- a gets positions 0, 4, 7 → 010010001 in binary
- b gets positions 2, 5, 8 → 100100100 in binary

## Input Format
- Each test case consists of a single integer n between 1 and 2^31 - 1 in decimal format.
- Input is terminated by a line containing '0' which should not be processed.

## Output Format
For each test case, output a single line containing a(n) and b(n) separated by a single space, both in decimal format.

## Solution

### Approach
1. Find all positions where n has a 1-bit
2. Assign odd-indexed positions (1st, 3rd, 5th, ...) to a
3. Assign even-indexed positions (2nd, 4th, 6th, ...) to b
4. Reconstruct the numbers

### Python Solution

```python
def solve():
 while True:
  n = int(input())
  if n == 0:
   break

  # Find all bit positions that are 1
  one_positions = []
  temp = n
  pos = 0
  while temp:
   if temp & 1:
    one_positions.append(pos)
   temp >>= 1
   pos += 1

  # Split into a and b
  a = 0
  b = 0

  for i, bit_pos in enumerate(one_positions):
   if i % 2 == 0:  # 1st, 3rd, 5th, ... (0-indexed: 0, 2, 4, ...)
    a |= (1 << bit_pos)
   else:           # 2nd, 4th, 6th, ... (0-indexed: 1, 3, 5, ...)
    b |= (1 << bit_pos)

  print(a, b)

if __name__ == "__main__":
 solve()
```

### Alternative Solution (More Concise)

```python
def split_number(n):
 a, b = 0, 0
 count = 0  # Count of 1-bits encountered
 bit_pos = 0

 while n:
  if n & 1:  # Current bit is 1
   if count % 2 == 0:
    a |= (1 << bit_pos)
   else:
    b |= (1 << bit_pos)
   count += 1
  n >>= 1
  bit_pos += 1

 return a, b

def solve():
 while True:
  n = int(input())
  if n == 0:
   break

  a, b = split_number(n)
  print(a, b)

if __name__ == "__main__":
 solve()
```

### One-liner Style Solution

```python
def solve():
 while True:
  n = int(input())
  if n == 0:
   break

  bits = [(i, 1 << i) for i in range(32) if n & (1 << i)]
  a = sum(val for i, (_, val) in enumerate(bits) if i % 2 == 0)
  b = sum(val for i, (_, val) in enumerate(bits) if i % 2 == 1)

  print(a, b)

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(log n) - we process each bit once
- **Space Complexity:** O(log n) for storing bit positions (or O(1) for the alternative solution)

### Example Walkthrough
For n = 437 (110110101 in binary):
- 1-bits at positions: 0, 2, 4, 5, 7, 8
- a gets positions 0, 4, 8 → 100010001 = 273
- b gets positions 2, 5, 7 → 010100100 = 164
- Output: 273 164
