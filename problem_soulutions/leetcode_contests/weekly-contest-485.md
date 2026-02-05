---
layout: simple
title: "Weekly Contest 485"
permalink: /problem_soulutions/leetcode_contests/weekly-contest-485/
---

# Weekly Contest 485

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | January 18, 2026 |
| **Time** | 09:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/weekly-contest-485/) |

---

## Problems

### Q1. Vowel-Consonant Score

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/vowel-consonant-score/) |

#### Problem Description

You are given a string `s` consisting of lowercase English letters, spaces, and digits.

Let `v` be the number of vowels in `s` and `c` be the number of consonants in `s`.

The **score** of the string `s` is defined as follows:

- If `c > 0`, the `score = floor(v / c)` where floor denotes **rounding down** to the nearest integer.
- Otherwise, the `score = 0`.

Return an integer denoting the score of the string.

**Example 1:**

**Input:** s = "cooear"

**Output:** 2

**Explanation:**

The string `s = "cooear"` contains `v = 4` vowels `('o', 'o', 'e', 'a')` and `c = 2` consonants `('c', 'r')`.

The score is `floor(v / c) = floor(4 / 2) = 2`.

**Constraints:**

- `1 <= s.length <= 100`
- `s` consists of lowercase English letters, spaces and digits.

<details>
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Simple counting problem - count vowels and consonants separately.

**Hint 1:** Vowels are 'a', 'e', 'i', 'o', 'u'. Everything else that's a letter is a consonant.

**Hint 2:** Skip spaces and digits when counting.

**Hint 3:** Handle the edge case where c = 0 (return 0).

**Approach:**
1. Iterate through each character
2. Count vowels and consonants (ignoring non-letters)
3. Return floor(v/c) if c > 0, else 0

```python
def vowelConsonantScore(s):
  vowels = set('aeiou')
  v = 0
  c = 0
  for char in s:
    if char.isalpha():
      if char in vowels:
        v += 1
      else:
        c += 1
  return v // c if c > 0 else 0
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

</details>

---

### Q2. Maximum Capacity Within Budget

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 4 |
| **Link** | [LeetCode](https://leetcode.com/problems/maximum-capacity-within-budget/) |

#### Problem Description

You are given two integer arrays `costs` and `capacity`, both of length `n`, where `costs[i]` represents the purchase cost of the `i^th` machine and `capacity[i]` represents its performance capacity.

You are also given an integer `budget`.

You may select **at most two distinct** machines such that the **total cost** of the selected machines is **strictly less** than `budget`.

Return the **maximum** achievable total capacity of the selected machines.

**Constraints:**

- `1 <= n == costs.length == capacity.length <= 10^5`
- `1 <= costs[i], capacity[i] <= 10^5`
- `1 <= budget <= 2 * 10^5`

<details>
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** We can select 0, 1, or 2 machines. For 2 machines, we need cost[i] + cost[j] < budget.

**Hint 1:** Try all pairs is O(n²) which may be too slow. Think about sorting or using a data structure.

**Hint 2:** Sort by cost. For each machine i, find the best machine j with cost[j] < budget - cost[i].

**Hint 3:** Use prefix maximum capacity for machines with cost up to a certain value.

**Approach:**
1. Create list of (cost, capacity) pairs and sort by cost
2. Build prefix max capacity array
3. For each machine, binary search to find valid partners
4. Also consider single machine selection

```python
import bisect

def maxCapacity(costs, capacity, budget):
  n = len(costs)
  machines = sorted(zip(costs, capacity))

  # Prefix max capacity for machines 0..i
  prefix_max = [0] * n
  prefix_max[0] = machines[0][1]
  for i in range(1, n):
    prefix_max[i] = max(prefix_max[i-1], machines[i][1])

  result = 0

  # Single machine
  for i in range(n):
    if machines[i][0] < budget:
      result = max(result, machines[i][1])

  # Two machines
  sorted_costs = [m[0] for m in machines]
  for i in range(n):
    cost_i = machines[i][0]
    cap_i = machines[i][1]
    max_partner_cost = budget - cost_i - 1

    if max_partner_cost <= 0:
      continue

    # Find rightmost index with cost <= max_partner_cost
    j = bisect.bisect_right(sorted_costs, max_partner_cost) - 1

    if j < 0:
      continue
    if j == i:
      j -= 1
    if j < 0:
      continue

    # Best capacity among machines 0..j (excluding i if needed)
    if j > i:
      best = prefix_max[j]
    elif j < i:
      best = prefix_max[j]
    else:
      best = prefix_max[j-1] if j > 0 else 0

    result = max(result, cap_i + best)

  return result
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(n)

</details>

---

### Q3. Design Auction System

| Field | Value |
|-------|-------|
| **Difficulty** | Medium |
| **Points** | 5 |
| **Link** | [LeetCode](https://leetcode.com/problems/design-auction-system/) |

#### Problem Description

You are asked to design an auction system that manages bids from multiple users in real time.

Implement the `AuctionSystem` class:

- `AuctionSystem()`: Initializes the `AuctionSystem` object.
- `void addBid(int userId, int itemId, int bidAmount)`: Adds a new bid for `itemId` by `userId` with `bidAmount`. If the same `userId` **already** has a bid on `itemId`, **replace** it with the new `bidAmount`.
- `void updateBid(int userId, int itemId, int newAmount)`: Updates the existing bid of `userId` for `itemId` to `newAmount`.
- `void removeBid(int userId, int itemId)`: Removes the bid of `userId` for `itemId`.
- `int getHighestBidder(int itemId)`: Returns the `userId` of the **highest** bidder for `itemId`. If multiple users have the **same highest** `bidAmount`, return the user with the **highest** `userId`. If no bids exist for the item, return -1.

**Constraints:**

- `1 <= userId, itemId <= 5 * 10^4`
- `1 <= bidAmount, newAmount <= 10^9`
- At most `5 * 10^4` total calls.

<details>
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Use nested dictionaries to track bids per item and per user, plus a sorted structure to efficiently find the highest bidder.

**Hint 1:** For each item, store a mapping: userId -> bidAmount.

**Hint 2:** For getHighestBidder, you need to find max(bidAmount, userId) efficiently.

**Hint 3:** Use a sorted set or heap per item to track (bidAmount, userId) pairs.

**Approach:**
1. Use dict of dict: itemId -> {userId: bidAmount}
2. For efficient max queries, use a sorted set per item: itemId -> SortedList of (-amount, -userId)
3. Handle updates by removing old entry and adding new one

```python
from sortedcontainers import SortedList

class AuctionSystem:
  def __init__(self):
    self.bids = {}  # itemId -> {userId: amount}
    self.sorted_bids = {}  # itemId -> SortedList of (-amount, -userId)

  def addBid(self, userId, itemId, bidAmount):
    if itemId not in self.bids:
      self.bids[itemId] = {}
      self.sorted_bids[itemId] = SortedList()

    # Remove old bid if exists
    if userId in self.bids[itemId]:
      old_amount = self.bids[itemId][userId]
      self.sorted_bids[itemId].remove((-old_amount, -userId))

    # Add new bid
    self.bids[itemId][userId] = bidAmount
    self.sorted_bids[itemId].add((-bidAmount, -userId))

  def updateBid(self, userId, itemId, newAmount):
    self.addBid(userId, itemId, newAmount)

  def removeBid(self, userId, itemId):
    if itemId in self.bids and userId in self.bids[itemId]:
      old_amount = self.bids[itemId][userId]
      self.sorted_bids[itemId].remove((-old_amount, -userId))
      del self.bids[itemId][userId]

  def getHighestBidder(self, itemId):
    if itemId not in self.sorted_bids or not self.sorted_bids[itemId]:
      return -1
    neg_amount, neg_user = self.sorted_bids[itemId][0]
    return -neg_user
```

**Time Complexity:** O(log n) for add/update/remove, O(1) for getHighestBidder
**Space Complexity:** O(total bids)

</details>

---

### Q4. Lexicographically Smallest String After Deleting Duplicate Characters

| Field | Value |
|-------|-------|
| **Difficulty** | Hard |
| **Points** | 6 |
| **Link** | [LeetCode](https://leetcode.com/problems/lexicographically-smallest-string-after-deleting-duplicate-characters/) |

#### Problem Description

You are given a string `s` that consists of lowercase English letters.

You can perform the following operation any number of times (possibly zero times):

- Choose any letter that appears **at least twice** in the current string `s` and delete any **one** occurrence.

Return the **lexicographically smallest** resulting string that can be formed this way.

**Example 1:**

**Input:** s = "aaccb"

**Output:** "aacb"

**Explanation:**

We can form the strings `"acb"`, `"aacb"`, `"accb"`, and `"aaccb"`. `"aacb"` is the lexicographically smallest one.

**Constraints:**

- `1 <= s.length <= 10^5`
- `s` contains lowercase English letters only.

<details>
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

**Key Insight:** Greedily keep smaller characters at the front, but we must keep at least one of each character that appears.

**Hint 1:** We want to maximize keeping 'a's at the beginning, then 'b's, etc.

**Hint 2:** Use a stack-based approach similar to "Remove Duplicate Letters" but we can keep multiple copies.

**Hint 3:** At each position, decide whether to keep or remove the current character based on what comes later.

**Approach:**
1. Count frequency of each character
2. Use a greedy approach: for each character, keep it if it makes the result lexicographically smaller
3. Track remaining counts and which characters must still appear

```python
def smallestString(s):
  from collections import Counter

  count = Counter(s)
  result = []
  in_result = Counter()

  for char in s:
    count[char] -= 1  # This char won't be available after this

    # While we can pop (current is smaller and stack top has more copies available)
    while result and char < result[-1] and count[result[-1]] + in_result[result[-1]] > 1:
      popped = result.pop()
      in_result[popped] -= 1

    result.append(char)
    in_result[char] += 1

  return ''.join(result)
```

**Alternative Approach - Keep all but one duplicate when beneficial:**

```python
def smallestString(s):
  # For lexicographically smallest, greedily remove characters
  # that are larger than a later occurrence
  from collections import Counter

  count = Counter(s)
  stack = []

  for char in s:
    count[char] -= 1

    while stack and stack[-1] > char and count[stack[-1]] > 0:
      stack.pop()

    stack.append(char)

  return ''.join(stack)
```

**Time Complexity:** O(n)
**Space Complexity:** O(n)

</details>

---

