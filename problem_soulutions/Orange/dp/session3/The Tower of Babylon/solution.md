# The Tower of Babylon

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

The Babylonians have n types of blocks with unlimited supply. Each block type has dimensions (xi, yi, zi). Blocks can be rotated to use any two dimensions as the base.

Build the tallest tower by stacking blocks such that each block's base dimensions are strictly smaller than the block below it.

## Input Format
- Multiple test cases
- Each test case:
  - First line: n (number of block types, n ≤ 30)
  - Next n lines: three integers (xi, yi, zi)
- Input ends with n = 0

## Output Format
For each test case: "Case X: maximum height = H"

## Solution

### Approach
1. Generate all rotations of each block (3 orientations per block: each dimension as height)
2. Sort blocks by base area (or by one base dimension)
3. Apply LIS-style DP: for each block, find the tallest tower ending with that block

A block can be placed on another if both base dimensions are strictly smaller.

### Python Solution

```python
def solve():
 case = 0

 while True:
  n = int(input())
  if n == 0:
   break

  case += 1

  # Generate all rotations
  blocks = []  # (base1, base2, height)

  for _ in range(n):
   dims = list(map(int, input().split()))
   x, y, z = dims

   # All 3 rotations (choosing each dimension as height)
   # Store as (min_base, max_base, height) for consistent comparison
   rotations = [
    (min(y, z), max(y, z), x),
    (min(x, z), max(x, z), y),
    (min(x, y), max(x, y), z)
   ]

   for rot in rotations:
    blocks.append(rot)

  # Sort by base area (or by first dimension)
  blocks.sort()

  m = len(blocks)

  # dp[i] = max height of tower with blocks[i] on top
  dp = [b[2] for b in blocks]  # Initialize with just the block's height

  for i in range(1, m):
   for j in range(i):
    # blocks[j] can be below blocks[i] if strictly smaller base
    if blocks[j][0] < blocks[i][0] and blocks[j][1] < blocks[i][1]:
     dp[i] = max(dp[i], dp[j] + blocks[i][2])

  max_height = max(dp)
  print(f"Case {case}: maximum height = {max_height}")

if __name__ == "__main__":
 solve()
```

### Alternative Solution

```python
def solve():
 import sys
 input = sys.stdin.readline
 case = 0

 while True:
  n = int(input())
  if n == 0:
   break

  case += 1
  blocks = []

  for _ in range(n):
   x, y, z = map(int, input().split())

   # Generate all orientations
   # (width, depth, height) - width <= depth for consistency
   dims = sorted([x, y, z])
   a, b, c = dims

   # Three unique orientations
   blocks.append((a, b, c))  # smallest two as base
   blocks.append((a, c, b))  # smallest and largest as base
   blocks.append((b, c, a))  # two largest as base

  # Remove duplicates and sort
  blocks = list(set(blocks))
  blocks.sort()

  m = len(blocks)
  dp = [0] * m

  for i in range(m):
   dp[i] = blocks[i][2]  # height of current block

   for j in range(i):
    if blocks[j][0] < blocks[i][0] and blocks[j][1] < blocks[i][1]:
     dp[i] = max(dp[i], dp[j] + blocks[i][2])

  print(f"Case {case}: maximum height = {max(dp)}")

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(n² × 9) = O(n²) since at most 3n blocks after rotation
- **Space Complexity:** O(n)

### Key Insight
Each block can be oriented in 3 ways (choosing which dimension is height). Generate all orientations, then this becomes a DAG longest path problem. Sort by base dimensions and use DP where dp[i] = max tower height with block i on top. A block j can support block i if both of j's base dimensions are strictly smaller.
