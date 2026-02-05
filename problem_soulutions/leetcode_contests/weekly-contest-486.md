---
layout: simple
title: "Weekly Contest 486"
permalink: /problem_soulutions/leetcode_contests/weekly-contest-486/
---

# Weekly Contest 486

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | January 25, 2026 |
| **Time** | 09:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/weekly-contest-486/) |

---

## Problems

### Q1. Minimum Prefix Removal to Make Array Strictly Increasing

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-prefix-removal-to-make-array-strictly-increasing/) |

#### Problem Description

You are given an integer array `nums`.

You need to remove **exactly** one prefix (possibly empty) from nums.

Return an integer denoting the **minimum** length of the removed prefix such that the remaining array is **strictly increasing**.

**Example 1:**

**Input:** nums = [1,-1,2,3,3,4,5]

**Output:** 4

**Explanation:**

Removing the `prefix = [1, -1, 2, 3]` leaves the remaining array `[3, 4, 5]` which is strictly increasing.

**Example 2:**

**Input:** nums = [4,3,-2,-5]

**Output:** 3

**Explanation:**

Removing the `prefix = [4, 3, -2]` leaves the remaining array `[-5]` which is strictly increasing.

**Example 3:**

**Input:** nums = [1,2,3,4]

**Output:** 0

**Explanation:**

The array `nums = [1, 2, 3, 4]` is already strictly increasing so removing an empty prefix is sufficient.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** We need to find the longest strictly increasing suffix.

**Hint 1:** Start from the end of the array and find the longest suffix that is strictly increasing.

**Hint 2:** Once you find where the strictly increasing property breaks (from right to left), everything before that point needs to be removed.

**Approach:**
1. Traverse from right to left
2. Keep track of where the strictly increasing suffix starts
3. The answer is the index where it breaks

```python
def minPrefixRemoval(nums):
  n = len(nums)
  # Find longest strictly increasing suffix
  i = n - 1
  while i > 0 and nums[i-1] < nums[i]:
    i -= 1
  return i
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

</details>

---

### Q2. Rotate Non Negative Elements

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/rotate-non-negative-elements/) |

#### Problem Description

You are given an integer array `nums` and an integer `k`.

Rotate only the **non-negative** elements of the array to the **left** by `k` positions, in a cyclic manner.

All **negative** elements must stay in their original positions and must not move.

After rotation, place the **non-negative** elements back into the array in the new order, filling only the positions that originally contained **non-negative** values and **skipping all negative** positions.

Return the resulting array.

**Example 1:**

**Input:** nums = [1,-2,3,-4], k = 3

**Output:** [3,-2,1,-4]

**Explanation:**

- The non-negative elements, in order, are `[1, 3]`.
- Left rotation with `k = 3` results in: `[1, 3] -> [3, 1] -> [1, 3] -> [3, 1]`
- Placing them back into the non-negative indices results in `[3, -2, 1, -4]`.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `-10^5 <= nums[i] <= 10^5`
- `0 <= k <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Extract non-negative elements, rotate them, and place them back.

**Hint 1:** First, extract all non-negative elements and their positions.

**Hint 2:** Rotate the extracted array by k % length positions.

**Hint 3:** Place the rotated elements back into their original positions.

**Approach:**
1. Extract non-negative elements and track their indices
2. Rotate the extracted array left by k % len (handle empty case)
3. Place rotated elements back at the tracked positions

```python
def rotateNonNegative(nums, k):
  # Extract non-negative elements and their positions
  non_neg = []
  positions = []
  for i, num in enumerate(nums):
    if num >= 0:
      non_neg.append(num)
      positions.append(i)

  if not non_neg:
    return nums

  # Rotate left by k
  m = len(non_neg)
  k = k % m
  non_neg = non_neg[k:] + non_neg[:k]

  # Place back
  result = nums[:]
  for i, pos in enumerate(positions):
    result[pos] = non_neg[i]

  return result
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q3. Pythagorean Distance Nodes in a Tree

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/pythagorean-distance-nodes-in-a-tree/) |

#### Problem Description

You are given an integer `n` and an undirected tree with `n` nodes numbered from 0 to `n - 1`. The tree is represented by a 2D array `edges` of length `n - 1`, where `edges[i] = [u_i, v_i]` indicates an undirected edge between `u_i` and `v_i`.

You are also given three **distinct** target nodes `x`, `y`, and `z`.

For any node `u` in the tree:

- Let `dx` be the distance from `u` to node `x`
- Let `dy` be the distance from `u` to node `y`
- Let `dz` be the distance from `u` to node `z`

The node `u` is called **special** if the three distances form a **Pythagorean Triplet**.

Return an integer denoting the number of special nodes in the tree.

**Constraints:**

- `4 <= n <= 10^5`
- `edges.length == n - 1`
- `x`, `y`, and `z` are pairwise **distinct**.

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** BFS from each target node to compute distances, then check Pythagorean condition for each node.

**Hint 1:** Run BFS three times - once from x, once from y, once from z - to get distance arrays.

**Hint 2:** For each node, sort the three distances and check if a² + b² = c².

**Hint 3:** Note that (0, a, a) satisfies 0² + a² = a² for any a.

**Approach:**
1. Build adjacency list from edges
2. Run BFS from x, y, z to compute dist_x[], dist_y[], dist_z[]
3. For each node u, check if sorted distances form Pythagorean triplet

```python
from collections import deque

def countSpecialNodes(n, edges, x, y, z):
  # Build adjacency list
  adj = [[] for _ in range(n)]
  for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)

  def bfs(start):
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    while queue:
      node = queue.popleft()
      for neighbor in adj[node]:
        if dist[neighbor] == -1:
          dist[neighbor] = dist[node] + 1
          queue.append(neighbor)
    return dist

  dx = bfs(x)
  dy = bfs(y)
  dz = bfs(z)

  count = 0
  for u in range(n):
    d = sorted([dx[u], dy[u], dz[u]])
    if d[0]**2 + d[1]**2 == d[2]**2:
      count += 1

  return count
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q4. Find Nth Smallest Integer With K One Bits

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/find-nth-smallest-integer-with-k-one-bits/) |

#### Problem Description

You are given two positive integers `n` and `k`.

Return an integer denoting the `n^th` smallest positive integer that has **exactly** `k` ones in its binary representation. It is guaranteed that the answer is **strictly less** than `2^50`.

**Example 1:**

**Input:** n = 4, k = 2

**Output:** 9

**Explanation:**

The 4 smallest positive integers that have exactly `k = 2` ones in their binary representations are:

- `3 = 11_2`
- `5 = 101_2`
- `6 = 110_2`
- `9 = 1001_2`

**Constraints:**

- `1 <= n <= 2^50`
- `1 <= k <= 50`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Use combinatorics to count how many numbers with k bits exist up to a certain length, then construct the answer bit by bit.

**Hint 1:** C(m, k) gives the count of m-bit numbers with exactly k ones (where the leading bit is 1).

**Hint 2:** Use binary search or greedy construction to find the n-th such number.

**Hint 3:** Think about it greedily: determine each bit from MSB to LSB by counting how many numbers would exist if we set that bit to 0 vs 1.

**Approach:**
1. First determine the bit length needed
2. Greedily construct the number bit by bit
3. At each position, count numbers if we place 0 vs 1, and decide accordingly

```python
from math import comb

def findNthNumber(n, k):
  # Find minimum bit length needed
  # Numbers with exactly k bits and m total bits: C(m-1, k-1) (leading 1 fixed)

  # First find how many bits we need
  total = 0
  bits = k
  while comb(bits, k) < n:
    bits += 1

  # Now construct the number greedily
  result = 0
  remaining = n
  ones_needed = k

  for pos in range(bits - 1, -1, -1):
    # Count numbers with 0 at this position
    if pos >= ones_needed - 1 and ones_needed > 0:
      count_with_zero = comb(pos, ones_needed)
    else:
      count_with_zero = 0

    if remaining > count_with_zero:
      # Place 1 at this position
      result |= (1 << pos)
      remaining -= count_with_zero
      ones_needed -= 1

  return result
```

**Time Complexity:** O(50 * 50) for computing combinations
**Space Complexity:** O(1)

</details>

---

