---
layout: simple
title: "Weekly Contest 483"
permalink: /problem_soulutions/leetcode_contests/weekly-contest-483/
---

# Weekly Contest 483

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | January 04, 2026 |
| **Time** | 09:30 UTC |
| **Duration** | 140 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/weekly-contest-483/) |

---

## Problems

### Q1. Largest Even Number

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/largest-even-number/) |

#### Problem Description

You are given a string `s` consisting only of the characters `'1'` and `'2'`.

You may delete any number of characters from `s` without changing the order of the remaining characters.

Return the **largest possible resultant string** that represents an **even** integer. If there is no such string, return the empty string `""`.

**Example 1:**

**Input:** s = "1112"

**Output:** "1112"

**Explanation:**

The string already represents the largest possible even number, so no deletions are needed.

**Example 2:**

**Input:** s = "221"

**Output:** "22"

**Explanation:**

Deleting `'1'` results in the largest possible even number which is equal to 22.

**Constraints:**

- `1 <= s.length <= 100`
- `s` consists only of the characters `'1'` and `'2'`.

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** For a number to be even, it must end in '2'. To maximize the number, we want to keep as many digits as possible.

**Hint 1:** Find the rightmost '2' in the string. Everything up to and including that '2' can form the largest even number.

**Hint 2:** If there's no '2', we can't form an even number - return "".

**Hint 3:** We want to keep all characters from the start up to (and including) the last '2'.

**Approach:**
1. Find the last occurrence of '2'
2. If found, return s[0:last_2_index+1]
3. If not found, return ""

```python
def largestEvenNumber(s):
  # Find rightmost '2'
  last_2 = s.rfind('2')
  if last_2 == -1:
    return ""
  return s[:last_2 + 1]
```

**Time Complexity:** O(n)
**Space Complexity:** O(1) (excluding output)

</details>

---

### Q2. Word Squares II

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/word-squares-ii/) |

#### Problem Description

You are given a string array `words`, consisting of **distinct** 4-letter strings, each containing lowercase English letters.

A **word square** consists of 4 **distinct** words: `top`, `left`, `right` and `bottom`, arranged as follows:

- `top` forms the **top row**.
- `bottom` forms the **bottom row**.
- `left` forms the **left column** (top to bottom).
- `right` forms the **right column** (top to bottom).

It must satisfy:

- `top[0] == left[0]`, `top[3] == right[0]`
- `bottom[0] == left[3]`, `bottom[3] == right[3]`

Return all valid **distinct** word squares, sorted in **ascending lexicographic** order by the 4-tuple `(top, left, right, bottom)`.

**Constraints:**

- `4 <= words.length <= 15`
- `words[i].length == 4`
- All `words[i]` are **distinct**.

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Build index structures for quick lookup by character positions, then enumerate valid combinations.

**Hint 1:** Create dictionaries mapping character positions to words. E.g., words starting with 'a', words ending with 'b', etc.

**Hint 2:** The corner constraints link the four words: top[0]=left[0], top[3]=right[0], bottom[0]=left[3], bottom[3]=right[3].

**Hint 3:** Enumerate all valid (top, left, right, bottom) combinations that satisfy the constraints.

**Approach:**
1. Build index: char_at_pos[pos][char] = list of words
2. For each choice of top, filter valid left (left[0] == top[0])
3. For each (top, left), filter valid right (right[0] == top[3])
4. For each (top, left, right), filter valid bottom (bottom[0] == left[3], bottom[3] == right[3])
5. Ensure all 4 words are distinct

```python
def wordSquares(words):
  from collections import defaultdict

  # Index words by character at each position
  by_pos = defaultdict(lambda: defaultdict(list))
  for word in words:
    for i, c in enumerate(word):
      by_pos[i][c].append(word)

  results = []

  for top in words:
    # left[0] == top[0]
    for left in by_pos[0][top[0]]:
      if left == top:
        continue
      # right[0] == top[3]
      for right in by_pos[0][top[3]]:
        if right in (top, left):
          continue
        # bottom[0] == left[3], bottom[3] == right[3]
        for bottom in by_pos[0][left[3]]:
          if bottom in (top, left, right):
            continue
          if bottom[3] == right[3]:
            results.append([top, left, right, bottom])

  # Sort by (top, left, right, bottom)
  results.sort()
  return results
```

**Time Complexity:** O(n^4) worst case, but pruned by constraints
**Space Complexity:** O(n)

</details>

---

### Q3. Minimum Cost to Make Two Binary Strings Equal

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-cost-to-make-two-binary-strings-equal/) |

#### Problem Description

You are given two binary strings `s` and `t`, both of length `n`, and three **positive** integers `flipCost`, `swapCost`, and `crossCost`.

You are allowed to apply the following operations any number of times (in any order):

- Choose any index `i` and flip `s[i]` or `t[i]`. Cost: `flipCost`.
- Choose two **distinct** indices `i` and `j`, and swap `s[i]` and `s[j]` or `t[i]` and `t[j]`. Cost: `swapCost`.
- Choose an index `i` and swap `s[i]` with `t[i]`. Cost: `crossCost`.

Return the **minimum** total cost to make `s` and `t` equal.

**Constraints:**

- `n == s.length == t.length`
- `1 <= n <= 10^5`
- `1 <= flipCost, swapCost, crossCost <= 10^9`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Focus on positions where s[i] != t[i]. Classify mismatches as (0,1) or (1,0) type.

**Hint 1:** At position i, if s[i]=0, t[i]=1, call it type A. If s[i]=1, t[i]=0, call it type B.

**Hint 2:** A cross-swap at i fixes that position with cost crossCost.

**Hint 3:** Two type-A positions can be fixed together with 2*flipCost or via swaps. Similarly for two type-B positions.

**Hint 4:** One type-A and one type-B can be fixed with 2*crossCost (swap both cross) or 2*flipCost.

**Approach:**
1. Count type-A and type-B mismatches
2. Pair up same types: cost = min(2*flipCost, swapCost + 2*crossCost, ...)
3. Handle remaining unpaired mismatches with flips

```python
def minCost(s, t, flipCost, swapCost, crossCost):
  type_a = 0  # s[i]='0', t[i]='1'
  type_b = 0  # s[i]='1', t[i]='0'

  for i in range(len(s)):
    if s[i] != t[i]:
      if s[i] == '0':
        type_a += 1
      else:
        type_b += 1

  # Pair same types: each pair costs min(2*flipCost, X)
  # Pair different types: each costs min(2*flipCost, 2*crossCost)

  # Cost to fix a pair of same type (e.g., two type-A)
  same_pair_cost = min(2 * flipCost, 2 * crossCost)

  # Cost to fix one type-A and one type-B together
  diff_pair_cost = min(2 * flipCost, 2 * crossCost)

  # Single mismatch cost
  single_cost = flipCost

  total = 0

  # Pair as many same types as possible
  pairs_a = type_a // 2
  pairs_b = type_b // 2
  total += pairs_a * same_pair_cost
  total += pairs_b * same_pair_cost

  remaining_a = type_a % 2
  remaining_b = type_b % 2

  # If both have one remaining, pair them
  if remaining_a == 1 and remaining_b == 1:
    total += diff_pair_cost
  elif remaining_a == 1:
    total += single_cost
  elif remaining_b == 1:
    total += single_cost

  return total
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

</details>

---

### Q4. Minimum Cost to Merge Sorted Lists

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/minimum-cost-to-merge-sorted-lists/) |

#### Problem Description

You are given a 2D integer array `lists`, where each `lists[i]` is a non-empty array of integers **sorted** in **non-decreasing** order.

You may **repeatedly** choose two lists `a` and `b` and merge them. The **cost** to merge is:

`len(a) + len(b) + abs(median(a) - median(b))`

Return the **minimum total cost** to merge all lists into one.

**Constraints:**

- `2 <= lists.length <= 12`
- `1 <= lists[i].length <= 500`
- `-10^9 <= lists[i][j] <= 10^9`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** With only up to 12 lists, we can use bitmask DP to try all merge orders.

**Hint 1:** The order of merging matters due to the median difference term.

**Hint 2:** Use DP with bitmask: dp[mask] = (min_cost, merged_list_info) for merging lists in mask.

**Hint 3:** For each mask, try splitting into two submasks and compute merge cost.

**Approach:**
1. Precompute merged list for each subset (via memoization)
2. dp[mask] = minimum cost to merge all lists in mask into one
3. For each mask, try all ways to split into two non-empty submasks
4. Cost = dp[submask1] + dp[submask2] + merge_cost(result1, result2)

```python
def minMergeCost(lists):
  n = len(lists)
  INF = float('inf')

  # Precompute sorted merged list for each mask
  from functools import lru_cache

  @lru_cache(maxsize=None)
  def merged_list(mask):
    result = []
    for i in range(n):
      if mask & (1 << i):
        result.extend(lists[i])
    result.sort()
    return tuple(result)

  def median(arr):
    m = len(arr)
    return arr[(m - 1) // 2]

  def merge_cost(arr1, arr2):
    return len(arr1) + len(arr2) + abs(median(arr1) - median(arr2))

  # dp[mask] = min cost to merge all lists in mask
  dp = [INF] * (1 << n)

  # Base case: single list costs 0
  for i in range(n):
    dp[1 << i] = 0

  for mask in range(1, 1 << n):
    if bin(mask).count('1') <= 1:
      continue

    # Try all ways to split mask into two non-empty parts
    submask = mask
    while submask > 0:
      other = mask ^ submask
      if other > 0 and submask < other:  # Avoid counting twice
        cost = dp[submask] + dp[other]
        cost += merge_cost(merged_list(submask), merged_list(other))
        dp[mask] = min(dp[mask], cost)
      submask = (submask - 1) & mask

  return dp[(1 << n) - 1]
```

**Time Complexity:** O(3^n * S) where S is total elements
**Space Complexity:** O(2^n * S)

</details>

---

