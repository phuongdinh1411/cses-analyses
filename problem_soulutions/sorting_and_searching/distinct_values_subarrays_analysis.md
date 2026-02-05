---
layout: simple
title: "Distinct Values Subarrays - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/distinct_values_subarrays_analysis
difficulty: Medium
tags: [sliding-window, hash-set, two-pointers, counting]
---

# Distinct Values Subarrays

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1.00 s |
| **CSES Link** | [Distinct Values Subarrays](https://cses.fi/problemset/task/3420) |
| **Key Technique** | Sliding Window with Hash Set |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the sliding window technique to count valid subarrays
- [ ] Use hash sets efficiently to track distinct elements in a window
- [ ] Derive counting formulas based on window boundaries
- [ ] Recognize the "count all subarrays with a property" pattern

---

## Problem Statement

**Problem:** Given an array of n integers, count the number of subarrays where each element is distinct.

**Input:**
- Line 1: An integer n (array size)
- Line 2: n integers x_1, x_2, ..., x_n (array contents)

**Output:**
- Print the number of subarrays with all distinct elements

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= x_i <= 10^9

### Example

```
Input:
4
1 2 1 3

Output:
8
```

**Explanation:** The valid subarrays are:
- [1] (index 0)
- [2] (index 1)
- [1] (index 2)
- [3] (index 3)
- [1,2] (indices 0-1)
- [2,1] (indices 1-2)
- [1,3] (indices 2-3)
- [2,1,3] (indices 1-3)

Total: 8 subarrays with all distinct elements.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count all subarrays where every element appears exactly once?

The crucial insight is that if a subarray `[l, r]` has all distinct elements, then every subarray `[l', r]` where `l <= l' <= r` also has all distinct elements. This monotonic property makes the sliding window technique applicable.

### Breaking Down the Problem

1. **What are we looking for?** Count of subarrays with no repeated elements
2. **What information do we have?** An array of integers, possibly with duplicates
3. **What's the relationship between input and output?** For each ending position, we need to find how many valid starting positions exist

### Analogies

Think of this problem like looking through a sliding window on a train. As you move forward (extend right), the view expands. If you see something you've already seen (duplicate), you must close the left part of the window until the duplicate is gone. At each position, count how many "unique views" (valid subarrays) end at that point.

---

## Solution 1: Brute Force

### Idea

Check every possible subarray and verify if all its elements are distinct using a set.

### Algorithm

1. For each starting position i (0 to n-1)
2. For each ending position j (i to n-1)
3. Check if subarray [i, j] has all distinct elements
4. If yes, increment count

### Code

```python
def count_distinct_subarrays_brute(arr):
    """
    Brute force: Check all subarrays.

    Time: O(n^3) - O(n^2) subarrays, O(n) to build set
    Space: O(n) - set for each subarray
    """
    n = len(arr)
    count = 0

    for i in range(n):
        for j in range(i, n):
            subarray = arr[i:j+1]
            if len(subarray) == len(set(subarray)):
                count += 1

    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | O(n^2) subarrays, O(n) to check each |
| Space | O(n) | Set stores up to n elements |

### Why This Works (But Is Slow)

The brute force is correct because it exhaustively checks every subarray. However, we recreate the set for each subarray, leading to redundant work. If [i, j] has all distinct elements, we don't leverage this when checking [i, j+1].

---

## Solution 2: Optimal - Sliding Window with Hash Set

### Key Insight

> **The Trick:** Maintain a window [left, right] where all elements are distinct. For each `right`, find the smallest valid `left`. All subarrays [left', right] where left <= left' <= right are valid, contributing (right - left + 1) subarrays.

### Why Sliding Window Works

The key observation is **monotonicity**: if adding element at position `right` creates a duplicate, we must shrink from the left until the duplicate is removed. The left pointer only moves forward, giving us O(n) total movements.

### Algorithm

1. Initialize left = 0, count = 0, and an empty hash set
2. For each right from 0 to n-1:
   - While arr[right] is already in the set:
     - Remove arr[left] from the set
     - Increment left
   - Add arr[right] to the set
   - Add (right - left + 1) to count (all valid subarrays ending at right)
3. Return count

### Dry Run Example

Let's trace through with input `arr = [1, 2, 1, 3]`:

```
Initial state:
  left = 0, count = 0, seen = {}

Step 1: right = 0, arr[right] = 1
  1 not in seen
  Add 1 to seen: {1}
  Subarrays ending at 0: [1]
  count += (0 - 0 + 1) = 1
  count = 1

Step 2: right = 1, arr[right] = 2
  2 not in seen
  Add 2 to seen: {1, 2}
  Subarrays ending at 1: [2], [1,2]
  count += (1 - 0 + 1) = 2
  count = 3

Step 3: right = 2, arr[right] = 1
  1 IS in seen!
  Remove arr[0]=1, left=1, seen={2}
  Now 1 not in seen
  Add 1 to seen: {2, 1}
  Subarrays ending at 2: [1], [2,1]
  count += (2 - 1 + 1) = 2
  count = 5

Step 4: right = 3, arr[right] = 3
  3 not in seen
  Add 3 to seen: {2, 1, 3}
  Subarrays ending at 3: [3], [1,3], [2,1,3]
  count += (3 - 1 + 1) = 3
  count = 8

Final answer: 8
```

### Visual Diagram

```
Array: [1, 2, 1, 3]
Index:  0  1  2  3

right=0: [1]           left=0  +1 subarray   count=1
         ^
         L,R

right=1: [1, 2]        left=0  +2 subarrays  count=3
         ^--^
         L  R

right=2: [_, 2, 1]     left=1  +2 subarrays  count=5
            ^--^       (shrink left because 1 was duplicate)
            L  R

right=3: [_, 2, 1, 3]  left=1  +3 subarrays  count=8
            ^-----^
            L     R
```

### Code

**Python Solution:**

```python
def count_distinct_subarrays(arr):
    """
    Optimal solution using sliding window with hash set.

    Time: O(n) - each element added/removed at most once
    Space: O(n) - hash set stores at most n elements
    """
    n = len(arr)
    count = 0
    left = 0
    seen = set()

    for right in range(n):
        # Shrink window until arr[right] is not a duplicate
        while arr[right] in seen:
            seen.remove(arr[left])
            left += 1

        # Add current element to window
        seen.add(arr[right])

        # All subarrays [left..right], [left+1..right], ..., [right..right] are valid
        count += right - left + 1

    return count


def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    print(count_distinct_subarrays(arr))


if __name__ == "__main__":
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element added and removed from set at most once |
| Space | O(n) | Hash set stores at most n distinct elements |

---

## Common Mistakes

### Mistake 1: Forgetting to Count All Valid Subarrays

```python
# WRONG - Only counts subarrays of maximum length
count = 0
for right in range(n):
    while arr[right] in seen:
        seen.remove(arr[left])
        left += 1
    seen.add(arr[right])
    count += 1  # WRONG: Only counts 1 subarray per position
```

**Problem:** This only counts n subarrays (one per ending position), missing shorter valid subarrays.

**Fix:** Add `(right - left + 1)` to count all valid subarrays ending at `right`.

### Mistake 2: Using Wrong Data Structure

```python
# WRONG - List instead of set
seen = []
while arr[right] in seen:  # O(n) lookup!
    seen.remove(arr[left])
    left += 1
```

**Problem:** Using a list makes membership checking O(n), resulting in O(n^2) total time.

**Fix:** Use a hash set for O(1) average lookup and removal.

### Mistake 3: Integer Overflow

**Problem:** For n = 2*10^5 with all distinct elements, answer is n*(n+1)/2 which exceeds int range.

**Fix:** Use `long long` for the count variable in C++.

### Mistake 4: Not Handling Large Values

```python
# WRONG - Assuming values fit in a small range
count_array = [0] * 100  # Won't work for x_i up to 10^9
```

**Problem:** Array indexing fails for large values.

**Fix:** Use hash set which handles any value range.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, arr=[5]` | 1 | Only one subarray [5] |
| All same | `n=3, arr=[2,2,2]` | 3 | Only single-element subarrays valid |
| All distinct | `n=3, arr=[1,2,3]` | 6 | All 6 subarrays valid: 3+2+1 |
| Two elements | `n=2, arr=[1,1]` | 2 | [1] and [1], but not [1,1] |
| Alternating | `n=4, arr=[1,2,1,2]` | 6 | Single elements (4) + [1,2] twice (2) |
| Large values | `n=2, arr=[10^9, 1]` | 3 | [10^9], [1], [10^9, 1] |

---

## When to Use This Pattern

### Use This Approach When:
- Counting subarrays with a "all elements satisfy X" property
- The property has monotonicity (shrinking from left maintains/restores validity)
- You need to track presence/absence of elements in current window
- O(n) time complexity is required

### Don't Use When:
- You need to find subarrays with exactly K distinct values (use "at most K" subtraction trick)
- The property doesn't have monotonicity with respect to window shrinking
- You need the actual subarrays, not just the count

### Pattern Recognition Checklist:
- [ ] Counting subarrays where all elements are distinct? -> **Sliding window + hash set**
- [ ] At most K distinct values? -> **Sliding window with frequency map**
- [ ] Exactly K distinct values? -> **atMost(K) - atMost(K-1) technique**
- [ ] Need frequency of each element in window? -> **Use hash map instead of hash set**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Playlist (CSES 1141)](https://cses.fi/problemset/task/1141) | Find longest subarray with distinct elements |
| [Longest Substring Without Repeating Characters (LC 3)](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Classic sliding window for longest distinct substring |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Distinct Values Queries (CSES 1734)](https://cses.fi/problemset/task/1734) | Offline queries about distinct values in ranges |
| [Fruit Into Baskets (LC 904)](https://leetcode.com/problems/fruit-into-baskets/) | At most 2 distinct values |
| [Sliding Window Distinct Values (CSES 3222)](https://cses.fi/problemset/task/3222) | Count distinct in fixed-size windows |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Subarrays with K Different Integers (LC 992)](https://leetcode.com/problems/subarrays-with-k-different-integers/) | Exactly K distinct using subtraction |
| [Distinct Values Subarrays II (CSES 2428)](https://cses.fi/problemset/task/2428) | Count distinct values across all subarrays |
| [Count Number of Nice Subarrays (LC 1248)](https://leetcode.com/problems/count-number-of-nice-subarrays/) | Exactly K odd numbers using same technique |

---

## Key Takeaways

1. **The Core Idea:** Use sliding window to maintain a window where all elements are distinct, counting valid subarrays ending at each position.

2. **Time Optimization:** Instead of O(n^2) checking all subarrays, we use the monotonicity of "all distinct" property to achieve O(n).

3. **Space Trade-off:** We use O(n) space for the hash set to enable O(1) duplicate checking.

4. **Counting Formula:** For each position `right` with valid window starting at `left`, there are `(right - left + 1)` valid subarrays ending at `right`.

5. **Pattern:** This is the "sliding window for counting subarrays with property" pattern - applicable whenever the property exhibits monotonicity.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why each element is added/removed at most once (O(n) proof)
- [ ] Derive the counting formula `(right - left + 1)`
- [ ] Identify when to use hash set vs hash map
- [ ] Implement in your preferred language in under 10 minutes
- [ ] Extend to "exactly K distinct" using the subtraction technique

---

## Additional Resources

- [CP-Algorithms: Two Pointers Method](https://cp-algorithms.com/others/two_pointers.html)
- [CSES Distinct Values Queries](https://cses.fi/problemset/task/1734) - Query distinct values in range
- [LeetCode Sliding Window Pattern](https://leetcode.com/tag/sliding-window/)
