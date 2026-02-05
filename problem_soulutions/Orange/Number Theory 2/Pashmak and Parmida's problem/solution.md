# Pashmak and Parmida's problem

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 256MB

## Problem Statement

Given array a of n integers, define f(l, r, x) = count of indices k where l ≤ k ≤ r and a[k] = x.

Count pairs (i, j) where 1 ≤ i < j ≤ n and f(1, i, a[i]) > f(j, n, a[j]).

## Input Format
- First line: n (1 ≤ n ≤ 10^6)
- Second line: n integers a1, a2, ..., an (1 ≤ ai ≤ 10^9)

## Output Format
Print the count of valid pairs.

## Solution

### Approach
1. Compute L[i] = f(1, i, a[i]) = count of a[i] in prefix [1..i]
2. Compute R[j] = f(j, n, a[j]) = count of a[j] in suffix [j..n]
3. Count pairs where L[i] > R[j] with i < j

This is an inversion count problem! Use merge sort or BIT/Fenwick tree.

### Python Solution

```python
def solve():
 import sys
 from collections import defaultdict

 input = sys.stdin.readline

 n = int(input())
 a = list(map(int, input().split()))

 # Compute L[i] = f(1, i, a[i])
 L = [0] * n
 count_left = defaultdict(int)
 for i in range(n):
  count_left[a[i]] += 1
  L[i] = count_left[a[i]]

 # Compute R[j] = f(j, n, a[j])
 R = [0] * n
 count_right = defaultdict(int)
 for j in range(n - 1, -1, -1):
  count_right[a[j]] += 1
  R[j] = count_right[a[j]]

 # Count pairs (i, j) where i < j and L[i] > R[j]
 # This is inversion count: count pairs where L[i] > R[j] for i < j

 # Use merge sort or BIT
 # BIT approach: process from right to left
 # For each j, count how many i < j have L[i] > R[j]

 # Compress R values (they're at most n)
 # BIT[x] = count of positions j seen so far with R[j] = x

 # Process from left to right:
 # For position i, we want to count j > i with R[j] < L[i]
 # Process from right to left:
 # At position i, count positions j > i (already processed) with R[j] < L[i]

 max_val = n + 1
 BIT = [0] * (max_val + 1)

 def update(idx, delta=1):
  while idx <= max_val:
   BIT[idx] += delta
   idx += idx & (-idx)

 def query(idx):
  total = 0
  while idx > 0:
   total += BIT[idx]
   idx -= idx & (-idx)
  return total

 result = 0

 # Process from right to left
 for i in range(n - 1, -1, -1):
  # Count j > i (already in BIT) with R[j] < L[i]
  if L[i] > 1:
   result += query(L[i] - 1)

  # Add R[i] to BIT
  update(R[i])

 print(result)

if __name__ == "__main__":
 solve()
```

### Alternative Solution with Merge Sort

```python
def solve():
 import sys
 from collections import defaultdict

 input = sys.stdin.readline

 n = int(input())
 a = list(map(int, input().split()))

 # Compute L and R
 L = [0] * n
 R = [0] * n

 cnt = defaultdict(int)
 for i in range(n):
  cnt[a[i]] += 1
  L[i] = cnt[a[i]]

 cnt.clear()
 for j in range(n - 1, -1, -1):
  cnt[a[j]] += 1
  R[j] = cnt[a[j]]

 # Count inversions: pairs (i, j) with i < j and L[i] > R[j]
 def merge_count(arr, temp, left, mid, right):
  i = left
  j = mid + 1
  k = left
  count = 0

  while i <= mid and j <= right:
   if arr[i][0] <= arr[j][0]:
    temp[k] = arr[i]
    i += 1
   else:
    temp[k] = arr[j]
    count += (mid - i + 1)
    j += 1
   k += 1

  while i <= mid:
   temp[k] = arr[i]
   i += 1
   k += 1

  while j <= right:
   temp[k] = arr[j]
   j += 1
   k += 1

  for i in range(left, right + 1):
   arr[i] = temp[i]

  return count

 def merge_sort_count(arr, temp, left, right):
  count = 0
  if left < right:
   mid = (left + right) // 2
   count += merge_sort_count(arr, temp, left, mid)
   count += merge_sort_count(arr, temp, mid + 1, right)
   count += merge_count(arr, temp, left, mid, right)
  return count

 # Create pairs (R[j], original_index) but we need L[i] > R[j]
 # Actually need: pairs where earlier L > later R

 # Use modified approach: create array where arr[i] = (L[i], R[i])
 # ... this gets complex, BIT is cleaner

 # Stick with BIT solution
 max_val = n + 1
 BIT = [0] * (max_val + 2)

 def update(idx):
  idx += 1
  while idx <= max_val + 1:
   BIT[idx] += 1
   idx += idx & (-idx)

 def query(idx):
  idx += 1
  total = 0
  while idx > 0:
   total += BIT[idx]
   idx -= idx & (-idx)
  return total

 result = 0
 for i in range(n - 1, -1, -1):
  if L[i] > 1:
   result += query(L[i] - 2)  # R[j] < L[i] means R[j] <= L[i]-1
  update(R[i] - 1)

 print(result)

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)

### Key Insight
Precompute L[i] (count of a[i] in prefix) and R[j] (count of a[j] in suffix). The problem becomes: count pairs (i,j) with i < j and L[i] > R[j]. This is a modified inversion count, solvable with BIT: process right-to-left, for each position count how many larger indices have smaller R values.
