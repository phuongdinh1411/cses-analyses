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
 members = []

 for i in range(n):
  s, b = map(int, input().split())
  members.append((s, b, i + 1))  # (strength, beauty, original_index)

 # Sort by strength ascending, then beauty descending (for same strength)
 members.sort(key=lambda x: (x[0], -x[1]))

 # LIS on beauty with index tracking
 # dp[i] = smallest ending beauty for LIS of length i+1
 # parent tracking for reconstruction

 dp = []  # (beauty, index in members)
 dp_idx = []  # index in members array for each dp entry
 parent = [-1] * n
 pos = [-1] * n  # position in LIS for each member

 for i, (s, b, orig_idx) in enumerate(members):
  # Binary search for position
  idx = bisect.bisect_left(dp, b)

  if idx == len(dp):
   dp.append(b)
   dp_idx.append(i)
  else:
   dp[idx] = b
   dp_idx[idx] = i

  pos[i] = idx
  if idx > 0:
   parent[i] = dp_idx[idx - 1]

 # Reconstruct LIS
 lis_length = len(dp)
 result = []

 # Find the last element in LIS
 curr = dp_idx[lis_length - 1]
 while curr != -1:
  result.append(members[curr][2])  # original index
  curr = parent[curr]

 result.reverse()

 print(lis_length)
 print(' '.join(map(str, result)))

if __name__ == "__main__":
 solve()
```

### Alternative Solution - Cleaner Reconstruction

```python
import bisect

def solve():
 n = int(input())
 members = []

 for i in range(n):
  s, b = map(int, input().split())
  members.append((s, b, i + 1))

 # Sort: strength ascending, beauty descending for same strength
 members.sort(key=lambda x: (x[0], -x[1]))

 # Extract beauties for LIS
 beauties = [m[1] for m in members]

 # LIS with reconstruction
 tails = []  # tails[i] = smallest ending value for LIS of length i+1
 tail_indices = []
 predecessor = [-1] * n
 lis_pos = [0] * n

 for i in range(n):
  b = beauties[i]
  pos = bisect.bisect_left(tails, b)

  if pos == len(tails):
   tails.append(b)
   tail_indices.append(i)
  else:
   tails[pos] = b
   tail_indices[pos] = i

  lis_pos[i] = pos
  if pos > 0:
   predecessor[i] = tail_indices[pos - 1]

 # Reconstruct
 lis_len = len(tails)
 path = []
 idx = tail_indices[-1]

 while idx != -1:
  path.append(members[idx][2])
  idx = predecessor[idx]

 path.reverse()

 print(lis_len)
 print(' '.join(map(str, path)))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(N log N)
- **Space Complexity:** O(N)

### Key Insight
After sorting by strength, the problem reduces to LIS on beauty. The key trick: for same strength, sort beauty descending to prevent selecting multiple members with same strength (as that would mean one hates the other if beauties differ). LIS with binary search gives O(N log N) complexity.
