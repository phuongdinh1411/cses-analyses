---
layout: simple
title: "Subarray Distinct Values - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/distinct_values_subsequences_analysis
difficulty: Medium
tags: [sliding-window, hash-map, two-pointers, counting]
---

# Subarray Distinct Values

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1.00 s |
| **CSES Link** | [Subarray Distinct Values](https://cses.fi/problemset/task/2428) |
| **Key Technique** | Sliding Window / Two Pointers |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the sliding window technique to count valid subarrays
- [ ] Use hash maps efficiently to track element frequencies in a window
- [ ] Derive counting formulas based on window boundaries
- [ ] Recognize the "count subarrays with at most K distinct values" pattern

---

## Problem Statement

**Problem:** Given an array of n integers and a value k, count the number of subarrays that have at most k distinct values.

**Input:**
- Line 1: Two integers n and k (array size and maximum distinct values)
- Line 2: n integers x_1, x_2, ..., x_n (array contents)

**Output:**
- Print the number of subarrays with at most k distinct values

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= k <= n
- 1 <= x_i <= 10^9

### Example

```
Input:
5 2
1 2 3 1 1

Output:
10
```

**Explanation:** The valid subarrays with at most 2 distinct values are:
- Length 1: [1], [2], [3], [1], [1] (5 subarrays)
- Length 2: [1,2], [2,3], [1,1] (3 subarrays - note [3,1] has 2 distinct)
- Length 3: [1,1] within [3,1,1] gives us [1,1,1]? No, [3,1,1] has 2 distinct values
- Actually: [3,1,1] has {3,1} = 2 distinct values, so it counts!
- Length 4: [1,1] pattern - no length 4 with <= 2 distinct

Wait, let me recount properly:
- Single elements: [1], [2], [3], [1], [1] = 5 subarrays
- Two elements: [1,2], [2,3], [3,1], [1,1] = 4 subarrays (all have <= 2 distinct)
- Three elements: [3,1,1] has {3,1} = 2 distinct, so counts = 1 subarray

Total = 5 + 4 + 1 = 10 subarrays.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count all subarrays where the number of distinct elements is at most k?

The crucial insight is that if we fix the right endpoint of a subarray, there exists a leftmost position such that all subarrays from that position to the right have at most k distinct values. This monotonic property makes the sliding window technique applicable.

### Breaking Down the Problem

1. **What are we looking for?** Count of subarrays with at most k distinct elements
2. **What information do we have?** An array of integers and limit k
3. **What's the relationship between input and output?** For each ending position, count how many valid starting positions exist

### Analogies

Think of this problem like a DJ mixing tracks. You can only play at most k different songs at any time. As you move through your playlist (extend the window right), you add new songs. If you exceed k unique songs, you must drop the oldest ones (shrink from left) until you're back to k or fewer. At each moment, count how many valid "mixes" (subarrays) end at that point.

---

## Solution 1: Brute Force

### Idea

Check every possible subarray and count distinct elements using a set.

### Algorithm

1. For each starting position i (0 to n-1)
2. For each ending position j (i to n-1)
3. Count distinct elements in subarray [i, j]
4. If distinct count <= k, increment result

### Code

```python
def count_subarrays_brute(arr, k):
    """
    Brute force solution - check all subarrays.

    Time: O(n^2)
    Space: O(n)
    """
    n = len(arr)
    count = 0

    for i in range(n):
        distinct = set()
        for j in range(i, n):
            distinct.add(arr[j])
            if len(distinct) <= k:
                count += 1
            else:
                break  # Further extension only adds more distinct

    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Two nested loops, with early break optimization |
| Space | O(n) | Set can hold up to n distinct elements |

### Why This Works (But Is Slow)

The brute force correctly checks all O(n^2) subarrays. The early break when distinct > k helps but doesn't change worst case. For large n (up to 2*10^5), this approach times out.

---

## Solution 2: Optimal Solution (Sliding Window)

### Key Insight

> **The Trick:** For each right endpoint, find the smallest left endpoint such that the window has at most k distinct values. All subarrays ending at right and starting from left to right are valid.

### Data Structure

| Component | Purpose |
|-----------|---------|
| `freq` map | Track frequency of each element in current window |
| `left` pointer | Left boundary of sliding window |
| `distinct_count` | Number of distinct elements (size of freq with non-zero values) |

**In plain English:** We maintain a window [left, right] where the number of distinct elements is always at most k. When we extend right and exceed k distinct elements, we shrink from left.

### The Counting Formula

When we have a valid window [left, right] with at most k distinct elements:
- Number of valid subarrays ending at `right` = `right - left + 1`

This is because every subarray [left, right], [left+1, right], ..., [right, right] is valid.

### Algorithm

1. Initialize left pointer at 0, freq map empty
2. For each right from 0 to n-1:
   - Add arr[right] to freq map
   - While distinct count > k:
     - Remove arr[left] from window (decrement freq, delete if 0)
     - Increment left
   - Add (right - left + 1) to answer

### Dry Run Example

Let's trace through with input `n=5, k=2, arr=[1, 2, 3, 1, 1]`:

```
Initial: left=0, freq={}, count=0

Step 1: right=0, arr[right]=1
  freq = {1: 1}, distinct=1
  distinct(1) <= k(2), valid
  count += (0 - 0 + 1) = 1
  count = 1

Step 2: right=1, arr[right]=2
  freq = {1: 1, 2: 1}, distinct=2
  distinct(2) <= k(2), valid
  count += (1 - 0 + 1) = 2
  count = 3

Step 3: right=2, arr[right]=3
  freq = {1: 1, 2: 1, 3: 1}, distinct=3
  distinct(3) > k(2), shrink!
    Remove arr[0]=1: freq = {1: 0, 2: 1, 3: 1} -> {2: 1, 3: 1}
    left = 1, distinct=2
  distinct(2) <= k(2), valid
  count += (2 - 1 + 1) = 2
  count = 5

Step 4: right=3, arr[right]=1
  freq = {2: 1, 3: 1, 1: 1}, distinct=3
  distinct(3) > k(2), shrink!
    Remove arr[1]=2: freq = {3: 1, 1: 1}, distinct=2
    left = 2
  distinct(2) <= k(2), valid
  count += (3 - 2 + 1) = 2
  count = 7

Step 5: right=4, arr[right]=1
  freq = {3: 1, 1: 2}, distinct=2
  distinct(2) <= k(2), valid
  count += (4 - 2 + 1) = 3
  count = 10

Final answer: 10
```

### Visual Diagram

```
Array: [1, 2, 3, 1, 1]    k = 2

right=0: [1]           distinct={1}     count+=1  total=1
          ^
          L,R

right=1: [1, 2]        distinct={1,2}   count+=2  total=3
          ^  ^
          L  R

right=2: [1, 2, 3]     distinct={1,2,3} > k, shrink!
             [2, 3]    distinct={2,3}   count+=2  total=5
             ^  ^
             L  R

right=3:    [2, 3, 1]  distinct={2,3,1} > k, shrink!
               [3, 1]  distinct={3,1}   count+=2  total=7
                ^  ^
                L  R

right=4:      [3, 1, 1] distinct={3,1}  count+=3  total=10
               ^     ^
               L     R
```

### Code

```python
def count_subarrays_optimal(arr, k):
    """
    Optimal solution using sliding window.

    Time: O(n) - each element added and removed at most once
    Space: O(min(n, k)) - hash map stores at most k+1 distinct elements
    """
    n = len(arr)
    freq = {}
    left = 0
    count = 0

    for right in range(n):
        # Add arr[right] to window
        freq[arr[right]] = freq.get(arr[right], 0) + 1

        # Shrink window while we have more than k distinct values
        while len(freq) > k:
            freq[arr[left]] -= 1
            if freq[arr[left]] == 0:
                del freq[arr[left]]
            left += 1

        # All subarrays ending at right with start in [left, right] are valid
        count += right - left + 1

    return count


def solve():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    k = int(input_data[idx]); idx += 1
    arr = [int(input_data[idx + i]) for i in range(n)]

    print(count_subarrays_optimal(arr, k))


if __name__ == "__main__":
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element is added and removed from window at most once |
| Space | O(min(n, k)) | Hash map stores at most k+1 distinct elements |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** With n up to 2*10^5, the count can reach n*(n+1)/2 which exceeds int range.
**Fix:** Use `long long` for the count variable.

### Mistake 2: Not Removing Zero-Frequency Entries

```python
# WRONG - doesn't clean up freq map
freq[arr[left]] -= 1
left += 1

# CORRECT - delete entry when frequency becomes 0
freq[arr[left]] -= 1
if freq[arr[left]] == 0:
    del freq[arr[left]]
left += 1
```

**Problem:** The distinct count is based on map size. Zero-frequency entries inflate the count.
**Fix:** Delete map entries when their frequency drops to 0.

### Mistake 3: Off-by-One in Counting

```python
# WRONG - missing +1
count += right - left

# CORRECT
count += right - left + 1
```

**Problem:** The number of subarrays from index `left` to `right` is `right - left + 1`, not `right - left`.
**Fix:** Remember to add 1 for inclusive counting.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| All same elements | `[1,1,1], k=1` | 6 | All n*(n+1)/2 subarrays valid |
| All different, k=n | `[1,2,3], k=3` | 6 | All subarrays valid |
| All different, k=1 | `[1,2,3], k=1` | 3 | Only single elements valid |
| Single element | `[5], k=1` | 1 | Only one subarray |
| Large k | `[1,2], k=100` | 3 | k >= n means all valid |

---

## When to Use This Pattern

### Use This Approach When:
- Counting subarrays with a constraint on distinct elements
- The constraint has a monotonic property (valid window remains valid when shrunk)
- You need O(n) time complexity
- Problems involving "at most K" constraints

### Don't Use When:
- Looking for subsequences (non-contiguous elements)
- The constraint is "exactly K" distinct (use subtraction trick instead)
- No monotonic property exists in the constraint

### Pattern Recognition Checklist:
- [ ] Counting subarrays? Consider sliding window
- [ ] "At most K" constraint? Standard sliding window
- [ ] "Exactly K" constraint? Use atMost(k) - atMost(k-1)
- [ ] Need to track frequencies? Use hash map

### Related Pattern: Exactly K Distinct

To count subarrays with **exactly K** distinct values:
```python
def exactly_k_distinct(arr, k):
    return at_most_k_distinct(arr, k) - at_most_k_distinct(arr, k - 1)
```

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Basic sliding window with distinct constraint |
| [Distinct Numbers (CSES)](https://cses.fi/problemset/task/1621) | Simple distinct counting |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) | Exactly K distinct (uses subtraction trick) |
| [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | At most 2 distinct values |
| [Longest Substring with At Most K Distinct](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) | Find length instead of count |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Distinct Values Queries (CSES)](https://cses.fi/problemset/task/1734) | Offline queries + Mo's algorithm |
| [Count Vowel Substrings](https://leetcode.com/problems/count-vowel-substrings-of-a-string/) | Additional constraints on elements |

---

## Key Takeaways

1. **The Core Idea:** Use sliding window to maintain at most K distinct elements; count subarrays by window size at each step.
2. **Time Optimization:** From O(n^2) brute force to O(n) by avoiding redundant work with two pointers.
3. **Space Trade-off:** O(min(n, k)) space for hash map to gain linear time.
4. **Pattern:** This is the "at most K" sliding window pattern - memorize it!

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why each element is processed at most twice
- [ ] Derive the counting formula (right - left + 1)
- [ ] Implement the "exactly K" variant using subtraction
- [ ] Identify this pattern in new problems

---

## Additional Resources

- [CSES Subarray Distinct Values](https://cses.fi/problemset/task/2428) - Count distinct values in subarrays
- [Two Pointers Technique - CP Algorithms](https://cp-algorithms.com/data_structures/segment_tree.html)
- [Sliding Window Pattern - LeetCode Explore](https://leetcode.com/explore/learn/card/array-and-string/205/array-two-pointer-technique/)
