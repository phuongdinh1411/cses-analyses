# Minimize Absolute Difference

## Problem Information
- **Source:** TopCoder
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

You are given an array x that contains exactly five positive integers. You want to put four of them instead of the question marks into the following expression: `|(? / ?) - (? / ?)|`. Your goal is to make the value of the expression as small as possible.

More formally, you have the expression: `|(x[a] / x[b]) - (x[c] / x[d])|`. Here, `/` denotes real division (e.g., 7/2 = 3.5) and `||` denotes absolute value. You want to find four distinct subscripts a, b, c, d for which the value of the expression is minimized.

Output the optimal subscripts {a, b, c, d}. If there are multiple optimal answers, return the lexicographically smallest one.

## Input Format
- Input contains five integers, each separated by space.
- Each integer will be between 1 and 10000, inclusive.

## Output Format
- Output four integers, separated by space, that represent the optimal answer (indices a, b, c, d).

## Solution

### Approach
Since we only have 5 numbers and need to choose 4 with specific positions, we can enumerate all permutations. There are P(5,4) = 120 possible arrangements. For each arrangement, calculate the absolute difference and track the minimum.

### Python Solution

```python
from itertools import permutations

def solve():
 x = list(map(int, input().split()))

 min_diff = float('inf')
 best_indices = None

 # Try all permutations of 4 indices from 5
 for perm in permutations(range(5), 4):
  a, b, c, d = perm
  # Calculate |(x[a]/x[b]) - (x[c]/x[d])|
  diff = abs(x[a] / x[b] - x[c] / x[d])

  # Update if better, or if same but lexicographically smaller
  if diff < min_diff or (diff == min_diff and list(perm) < list(best_indices)):
   min_diff = diff
   best_indices = perm

 print(' '.join(map(str, best_indices)))

if __name__ == "__main__":
 solve()
```

### Alternative Solution with Explicit Enumeration

```python
def solve():
 x = list(map(int, input().split()))

 min_diff = float('inf')
 best = None

 # Generate all permutations of 4 distinct indices
 for a in range(5):
  for b in range(5):
   if b == a:
    continue
   for c in range(5):
    if c == a or c == b:
     continue
    for d in range(5):
     if d == a or d == b or d == c:
      continue

     diff = abs(x[a] / x[b] - x[c] / x[d])
     indices = (a, b, c, d)

     if diff < min_diff:
      min_diff = diff
      best = indices
     elif diff == min_diff and indices < best:
      best = indices

 print(' '.join(map(str, best)))

if __name__ == "__main__":
 solve()
```

### Solution with Fraction Comparison (Avoid Floating Point)

```python
from fractions import Fraction
from itertools import permutations

def solve():
 x = list(map(int, input().split()))

 min_diff = Fraction(10**9, 1)
 best_indices = None

 for perm in permutations(range(5), 4):
  a, b, c, d = perm
  # Use fractions for exact comparison
  frac1 = Fraction(x[a], x[b])
  frac2 = Fraction(x[c], x[d])
  diff = abs(frac1 - frac2)

  if diff < min_diff or (diff == min_diff and list(perm) < list(best_indices)):
   min_diff = diff
   best_indices = perm

 print(' '.join(map(str, best_indices)))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(P(5,4)) = O(120) = O(1) constant
- **Space Complexity:** O(1)

### Key Insight
With only 5 numbers and needing to pick 4 positions, brute force is the best approach. The total number of permutations is P(5,4) = 5!/(5-4)! = 120, which is trivial to enumerate. To handle the "lexicographically smallest" requirement when there are ties, we ensure to check permutations in lexicographical order or explicitly compare.
