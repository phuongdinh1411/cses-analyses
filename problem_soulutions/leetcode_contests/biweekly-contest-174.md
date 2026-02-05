---
layout: simple
title: "Biweekly Contest 174"
permalink: /problem_soulutions/leetcode_contests/biweekly-contest-174/
---

# Biweekly Contest 174

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | January 17, 2026 |
| **Time** | 21:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/biweekly-contest-174/) |

---

## Problems

### Q1. Best Reachable Tower

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/best-reachable-tower/) |

#### Problem Description

You are given a 2D integer array `towers`, where `towers[i] = [x_i, y_i, q_i]` represents the coordinates and quality factor of the `i^th` tower.

You are also given an integer array `center = [cx, cy]` and an integer `radius`.

A tower is **reachable** if its **Manhattan distance** from `center` is **less than or equal** to `radius`.

Return the coordinates of the tower with the **maximum** quality factor among reachable towers. If there's a tie, return the **lexicographically smallest** coordinate. If no tower is reachable, return `[-1, -1]`.

**Constraints:**

- `1 <= towers.length <= 10^5`
- `0 <= x_i, y_i, q_i, cx, cy <= 10^5`
- `0 <= radius <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Filter reachable towers, then find the one with max quality (with lexicographic tiebreaker).

**Hint 1:** Manhattan distance = |x - cx| + |y - cy|.

**Hint 2:** Among reachable towers, find max quality. For ties, use min coordinates.

**Approach:**
1. Filter towers where Manhattan distance <= radius
2. Sort by (-quality, x, y) to handle tiebreakers
3. Return the first tower's coordinates, or [-1, -1] if none

```python
def bestReachableTower(towers, center, radius):
  cx, cy = center
  reachable = []

  for x, y, q in towers:
    dist = abs(x - cx) + abs(y - cy)
    if dist <= radius:
      reachable.append((q, x, y))

  if not reachable:
    return [-1, -1]

  # Sort by quality desc, then coordinates asc
  reachable.sort(key=lambda t: (-t[0], t[1], t[2]))
  return [reachable[0][1], reachable[0][2]]
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

</details>

---

### Q2. Minimum Operations to Reach Target Array

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-operations-to-reach-target-array/) |

#### Problem Description

You are given two integer arrays `nums` and `target`, each of length `n`.

You may perform the following operation any number of times:

- Choose an integer value `x`
- Find all **maximal contiguous segments** where `nums[i] == x`
- For each such segment `[l, r]`, update **simultaneously**: `nums[l] = target[l], ..., nums[r] = target[r]`

Return the **minimum** number of operations required to make `nums` equal to `target`.

**Constraints:**

- `1 <= n == nums.length == target.length <= 10^5`
- `1 <= nums[i], target[i] <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Each distinct value in nums that needs to change requires exactly one operation.

**Hint 1:** When we choose x, ALL segments with value x get updated simultaneously.

**Hint 2:** So we need one operation per distinct value in nums (where that value differs from target at some position).

**Hint 3:** Count distinct values in nums at positions where nums[i] != target[i].

**Approach:**
1. Find positions where nums[i] != target[i]
2. Collect distinct values of nums at those positions
3. Return the count of distinct values

```python
def minOperations(nums, target):
  values_to_change = set()

  for i in range(len(nums)):
    if nums[i] != target[i]:
      values_to_change.add(nums[i])

  return len(values_to_change)
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q3. Number of Alternating XOR Partitions

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/number-of-alternating-xor-partitions/) |

#### Problem Description

You are given an integer array `nums` and two **distinct** integers `target1` and `target2`.

A **partition** is **valid** if the **bitwise XOR** of elements in its blocks **alternates** between `target1` and `target2`, starting with `target1`.

Return the number of valid partitions of `nums`, modulo `10^9 + 7`.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `0 <= nums[i], target1, target2 <= 10^5`
- `target1 != target2`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** DP where state tracks whether we need target1 or target2 for the next block.

**Hint 1:** Use prefix XOR to efficiently compute XOR of any subarray.

**Hint 2:** dp[i][0] = ways to partition nums[0:i] with last block having XOR = target1.

**Hint 3:** dp[i][1] = ways to partition nums[0:i] with last block having XOR = target2.

**Approach:**
1. Compute prefix XOR
2. dp[i][parity] = ways to partition up to index i, where parity indicates expected target
3. Use hash map to count prefix XOR values for O(n) solution

```python
def countPartitions(nums, target1, target2):
  MOD = 10**9 + 7
  n = len(nums)

  # Prefix XOR
  prefix_xor = [0] * (n + 1)
  for i in range(n):
    prefix_xor[i + 1] = prefix_xor[i] ^ nums[i]

  # dp approach with hash map
  # For block XOR to equal T: prefix_xor[j] ^ prefix_xor[i] = T
  # So we need prefix_xor[i] = prefix_xor[j] ^ T

  from collections import defaultdict

  # count0[x] = ways to reach state 0 (need target1 next) with prefix_xor = x
  # count1[x] = ways to reach state 1 (need target2 next) with prefix_xor = x

  count0 = defaultdict(int)
  count1 = defaultdict(int)
  count0[0] = 1  # Start: prefix_xor = 0, need target1

  result = 0

  for i in range(1, n + 1):
    cur_xor = prefix_xor[i]

    # Transition from state 0 (need target1)
    # Block XOR = cur_xor ^ prev_xor = target1
    # prev_xor = cur_xor ^ target1
    need = cur_xor ^ target1
    ways_from_0 = count0[need]

    # Transition from state 1 (need target2)
    need = cur_xor ^ target2
    ways_from_1 = count1[need]

    # After using target1, we're now in state 1 (need target2 next or can end)
    # After using target2, we're now in state 0 (need target1 next or can end)

    # Valid ending: must end with target1 or target2
    # Can end in state 0 (just placed target2) or state 1 (just placed target1)

    # If we end now after placing target1 (valid if it's the last block):
    # ways_from_0 counts partitions ending with target1
    result = (result + ways_from_0) % MOD

    # Update counts
    new_count0 = defaultdict(int)
    new_count1 = defaultdict(int)

    for x, cnt in count0.items():
      new_count0[x] = (new_count0[x] + cnt) % MOD
    for x, cnt in count1.items():
      new_count1[x] = (new_count1[x] + cnt) % MOD

    # After placing block ending at i with XOR=target1 from state 0
    new_count1[cur_xor] = (new_count1[cur_xor] + ways_from_0) % MOD
    # After placing block ending at i with XOR=target2 from state 1
    new_count0[cur_xor] = (new_count0[cur_xor] + ways_from_1) % MOD

    count0 = new_count0
    count1 = new_count1

  return result
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

### Q4. Minimum Edge Toggles on a Tree

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-edge-toggles-on-a-tree/) |

#### Problem Description

You are given an **undirected tree** with `n` nodes and two binary strings `start` and `target`.

In one operation, pick an edge and **toggle** both endpoints (flip '0' to '1' or '1' to '0').

Return an array of edge indices (in increasing order) whose operations transform `start` into `target`. If impossible, return `[-1]`.

**Constraints:**

- `2 <= n <= 10^5`
- `edges.length == n - 1`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Each node needs to flip diff[i] = start[i] XOR target[i] times (mod 2). Each edge toggle flips exactly 2 nodes.

**Hint 1:** Compute diff[i] = 1 if start[i] != target[i], else 0.

**Hint 2:** An edge toggle changes diff values at both endpoints.

**Hint 3:** For a solution to exist, sum(diff) must be even (since each edge changes 2 nodes).

**Hint 4:** Use DFS/BFS to determine which edges need toggling.

**Approach:**
1. Compute diff array
2. If sum(diff) is odd, return [-1]
3. Use a greedy/DP approach on the tree to select minimum edges
4. For minimum edges: process tree from leaves, toggle edge if child needs it

```python
def minEdgeToggles(n, edges, start, target):
  diff = [int(start[i] != target[i]) for i in range(n)]

  if sum(diff) % 2 == 1:
    return [-1]

  # Build adjacency list with edge indices
  from collections import defaultdict
  adj = defaultdict(list)
  for idx, (u, v) in enumerate(edges):
    adj[u].append((v, idx))
    adj[v].append((u, idx))

  # DFS from node 0, decide which edges to toggle
  result = []
  visited = [False] * n

  def dfs(node):
    visited[node] = True
    for neighbor, edge_idx in adj[node]:
      if not visited[neighbor]:
        dfs(neighbor)
        # After processing subtree, if neighbor needs toggle, use this edge
        if diff[neighbor] == 1:
          result.append(edge_idx)
          diff[neighbor] ^= 1
          diff[node] ^= 1

  dfs(0)

  # If root still needs toggle, impossible (shouldn't happen if sum was even)
  if diff[0] == 1:
    return [-1]

  result.sort()
  return result if result else []
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

