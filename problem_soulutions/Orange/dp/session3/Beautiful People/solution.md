# Beautiful People

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

A prestigious club has N members, each with strength Si and beauty Bi. Member i hates member j if Si < Sj and Bi > Bj, or Si > Sj and Bi < Bj.

For a party, select maximum members such that no two hate each other. Two members don't hate each other if Si ≤ Sj and Bi ≤ Bj (or vice versa).

## Input Format
- First line: N (number of members, 2 ≤ N ≤ 100,000)
- Next N lines: Si and Bi (1 ≤ Si, Bi ≤ 10^9)

## Output Format
- First line: maximum members that can be invited
- Second line: their indices (1-indexed)

## Example
```
Input:
3
1 1
1 2
2 1

Output:
2
1 2
```
Members: (1,1), (1,2), (2,1). Member 1 and 2 don't hate each other (1<=1, 1<=2). Member 1 and 3 don't hate each other (1<=2, 1>=1 - but S1<S3 and B1>B3? No: 1<2 and 1>1 is false). We can invite members 1 and 2, or 1 and 3. Maximum is 2.

## Solution

### Approach
This is a variant of Longest Increasing Subsequence (LIS) in 2D.

1. Sort members by strength Si
2. For members with same strength, sort by beauty Bi in descending order
3. Find LIS on beauty values

The descending sort for same strength ensures we don't pick two members with same strength but different beauty (which would hate each other).

### Python Solution

```python
import bisect

def solve():
  n = int(input())

  # Use list comprehension with enumerate for index tracking
  members = [
    (s, b, i + 1)
    for i in range(n)
    for s, b in [map(int, input().split())]
  ]

  # Sort by strength ascending, then beauty descending (for same strength)
  members.sort(key=lambda x: (x[0], -x[1]))

  # LIS on beauty with index tracking
  tails = []  # smallest ending beauty for each LIS length
  tail_indices = []  # index in members array for each tail entry
  parent = [-1] * n

  for i, (strength, beauty, orig_idx) in enumerate(members):
    # Binary search for position
    pos = bisect.bisect_left(tails, beauty)

    if pos == len(tails):
      tails.append(beauty)
      tail_indices.append(i)
    else:
      tails[pos] = beauty
      tail_indices[pos] = i

    if pos > 0:
      parent[i] = tail_indices[pos - 1]

  # Reconstruct LIS
  result = []
  curr = tail_indices[-1]
  while curr != -1:
    result.append(members[curr][2])  # original index
    curr = parent[curr]

  result.reverse()

  print(len(tails))
  print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

### Alternative Solution - Cleaner Reconstruction

```python
import bisect

def solve():
  n = int(input())

  # Read members with original index using enumerate-style
  members = [
    (*map(int, input().split()), i + 1)
    for i in range(n)
  ]

  # Sort: strength ascending, beauty descending for same strength
  members.sort(key=lambda x: (x[0], -x[1]))

  # LIS with reconstruction using enumerate
  tails = []
  tail_indices = []
  predecessor = [-1] * n

  for i, (_, beauty, _) in enumerate(members):
    pos = bisect.bisect_left(tails, beauty)

    if pos == len(tails):
      tails.append(beauty)
      tail_indices.append(i)
    else:
      tails[pos] = beauty
      tail_indices[pos] = i

    if pos > 0:
      predecessor[i] = tail_indices[pos - 1]

  # Reconstruct path
  path = []
  idx = tail_indices[-1]
  while idx != -1:
    path.append(members[idx][2])  # original index
    idx = predecessor[idx]

  path.reverse()

  print(len(tails))
  print(' '.join(map(str, path)))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N log N)
- **Space Complexity:** O(N)

### Key Insight
After sorting by strength, the problem reduces to LIS on beauty. The key trick: for same strength, sort beauty descending to prevent selecting multiple members with same strength (as that would mean one hates the other if beauties differ). LIS with binary search gives O(N log N) complexity.
