# Samu and her Birthday Party

## Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Samu is planning a birthday party and wants to select dishes for the menu. She has N friends and K available dishes. Each friend has preferences represented as a binary string where '1' means they like that dish.

Find the minimum number of dishes to include in the menu so that every friend has at least one dish they like.

## Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: N (friends) and K (dishes)
  - Next N lines: binary strings of length K representing preferences

## Constraints
- 1 ≤ T ≤ 10
- 1 ≤ N ≤ 500
- 1 ≤ K ≤ 10

## Output Format
Minimum number of dishes needed so all friends are happy.

## Solution

### Approach
Since K ≤ 10, we can enumerate all 2^K possible subsets of dishes. For each subset, check if every friend likes at least one dish in it. Track the minimum subset size that satisfies everyone.

### Python Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  n, k = map(int, input().split())
  preferences = []

  for _ in range(n):
   pref = input().strip()
   # Convert to integer bitmask
   mask = int(pref, 2)
   preferences.append(mask)

  min_dishes = k  # Worst case: need all dishes

  # Try all subsets of dishes (1 to 2^k - 1)
  for subset in range(1, 1 << k):
   # Check if all friends are satisfied
   all_satisfied = True

   for pref in preferences:
    # Friend is satisfied if they like at least one dish in subset
    if (pref & subset) == 0:
     all_satisfied = False
     break

   if all_satisfied:
    # Count dishes in this subset
    dish_count = bin(subset).count('1')
    min_dishes = min(min_dishes, dish_count)

  print(min_dishes)

if __name__ == "__main__":
 solve()
```

### Optimized Solution with Early Termination

```python
def popcount(x):
 count = 0
 while x:
  count += x & 1
  x >>= 1
 return count

def solve():
 t = int(input())

 for _ in range(t):
  n, k = map(int, input().split())
  preferences = []

  for _ in range(n):
   pref = input().strip()
   preferences.append(int(pref, 2))

  min_dishes = k

  # Enumerate subsets by number of bits (for early termination)
  for subset in range(1, 1 << k):
   bits = popcount(subset)

   # Skip if we already found a better solution
   if bits >= min_dishes:
    continue

   # Check if all friends satisfied
   if all(pref & subset for pref in preferences):
    min_dishes = bits

  print(min_dishes)

if __name__ == "__main__":
 solve()
```

### Alternative: Iterate by Subset Size

```python
from itertools import combinations

def solve():
 t = int(input())

 for _ in range(t):
  n, k = map(int, input().split())
  preferences = []

  for _ in range(n):
   pref = input().strip()
   preferences.append(int(pref, 2))

  # Try subsets of increasing size
  for size in range(1, k + 1):
   found = False

   for dishes in combinations(range(k), size):
    subset = sum(1 << d for d in dishes)

    if all(pref & subset for pref in preferences):
     print(size)
     found = True
     break

   if found:
    break

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(2^K × N) per test case
- **Space Complexity:** O(N) for storing preferences

### Key Insight
This is a Set Cover problem variant. With K ≤ 10, brute force over all 2^10 = 1024 subsets is feasible. A friend is satisfied by a subset if their preference mask AND the subset mask is non-zero (at least one common dish).
