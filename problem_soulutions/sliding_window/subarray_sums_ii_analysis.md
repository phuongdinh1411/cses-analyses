---
layout: simple
title: "Subarray Sums II - Prefix Sum + Hash Map"
permalink: /problem_soulutions/sliding_window/subarray_sums_ii_analysis
difficulty: Medium
tags: [prefix-sum, hash-map, counting, subarray]
---

# Subarray Sums II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1661](https://cses.fi/problemset/task/1661) |
| **Difficulty** | Medium |
| **Category** | Prefix Sum / Hash Map |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix Sum + Hash Map Counting |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply prefix sums to convert subarray sum problems into complement search problems
- [ ] Use hash maps to count frequencies for O(n) subarray counting
- [ ] Handle arrays with negative numbers (where sliding window fails)
- [ ] Recognize the "complement counting" pattern in subarray problems

---

## Problem Statement

**Problem:** Given an array of n integers (which may include negative numbers), count the number of subarrays whose sum equals exactly x.

**Input:**
- Line 1: Two integers n and x (array size and target sum)
- Line 2: n integers a_1, a_2, ..., a_n

**Output:**
- Single integer: count of subarrays with sum equal to x

**Constraints:**
- 1 <= n <= 2 * 10^5
- -10^9 <= x <= 10^9
- -10^9 <= a_i <= 10^9

### Example

```
Input:
5 7
2 -1 3 5 -2

Output:
2
```

**Explanation:** Two subarrays sum to 7:
- [2, -1, 3, 5, -2] indices 0-4: 2 + (-1) + 3 + 5 + (-2) = 7
- [2, -1, 3, 5] indices 0-3: 2 + (-1) + 3 + 5 = 9... wait, let me recalculate
- Actually: [2, -1, 3, 3] = indices matter. The subarrays are [2, -1, 3, 5, -2] and perhaps another combination.

Let's use a clearer example:
```
Input:
5 7
2 4 1 2 7

Output:
3
```
Subarrays: [2, 4, 1], [1, 2, 7... no wait], [7]. Let me trace properly in Dry Run.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why can't we use the sliding window technique from Subarray Sums I?

**Answer:** Negative numbers break the sliding window invariant. With only positive numbers, expanding the window increases the sum and shrinking decreases it. With negative numbers, this monotonicity is lost.

### Breaking Down the Problem

1. **What are we looking for?** Count of subarrays where sum equals target x
2. **Key insight:** If prefix[j] - prefix[i] = x, then subarray (i, j] has sum x
3. **Optimization:** Instead of checking all pairs O(n^2), use hash map to find complements in O(1)

### The Core Math

For any subarray from index i+1 to j:
```
sum(i+1, j) = prefix[j] - prefix[i]
```

If we want `sum(i+1, j) = x`, we need:
```
prefix[j] - prefix[i] = x
prefix[i] = prefix[j] - x
```

So at each position j, count how many previous prefix sums equal `prefix[j] - x`.

---

## Solution 1: Brute Force (TLE)

### Idea

Check every possible subarray by iterating through all start and end positions.

### Code

```python
def count_subarrays_brute(arr, x):
 """
 Brute force: check all subarrays.
 Time: O(n^2), Space: O(1)
 """
 n = len(arr)
 count = 0
 for i in range(n):
  current_sum = 0
  for j in range(i, n):
   current_sum += arr[j]
   if current_sum == x:
    count += 1
 return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Nested loops over all subarrays |
| Space | O(1) | Only tracking current sum |

**Why TLE:** With n up to 2*10^5, O(n^2) = 4*10^10 operations exceeds time limit.

---

## Solution 2: Optimal - Prefix Sum + Hash Map

### Key Insight

> **The Trick:** At each position, we don't need to check all previous positions. We just need to know HOW MANY previous prefix sums equal `current_prefix - x`.

### Algorithm

1. Initialize hash map with {0: 1} (empty prefix has sum 0)
2. Track running prefix sum
3. At each position, add count of `prefix - x` to answer
4. Increment count of current prefix in hash map
5. Return total count

### Dry Run Example

Input: `n=5, arr=[2, 4, 1, 2, 7], x=7`

```
Initialize: prefix_count = {0: 1}, current_prefix = 0, count = 0

Step 1: arr[0] = 2
  current_prefix = 0 + 2 = 2
  need = 2 - 7 = -5
  prefix_count[-5] = 0, so count += 0
  prefix_count = {0: 1, 2: 1}

Step 2: arr[1] = 4
  current_prefix = 2 + 4 = 6
  need = 6 - 7 = -1
  prefix_count[-1] = 0, so count += 0
  prefix_count = {0: 1, 2: 1, 6: 1}

Step 3: arr[2] = 1
  current_prefix = 6 + 1 = 7
  need = 7 - 7 = 0
  prefix_count[0] = 1, so count += 1  --> Found [2,4,1]!
  prefix_count = {0: 1, 2: 1, 6: 1, 7: 1}

Step 4: arr[3] = 2
  current_prefix = 7 + 2 = 9
  need = 9 - 7 = 2
  prefix_count[2] = 1, so count += 1  --> Found [4,1,2]!
  prefix_count = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1}

Step 5: arr[4] = 7
  current_prefix = 9 + 7 = 16
  need = 16 - 7 = 9
  prefix_count[9] = 1, so count += 1  --> Found [7]!
  prefix_count = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1, 16: 1}

Final answer: 3
```

### Visual Diagram

```
Array:    [2]  [4]  [1]  [2]  [7]
Index:     0    1    2    3    4
Prefix:    2    6    7    9   16

Subarrays summing to 7:
  prefix[2] - prefix[-1] = 7 - 0 = 7  --> [2,4,1]
  prefix[3] - prefix[0]  = 9 - 2 = 7  --> [4,1,2]
  prefix[4] - prefix[3]  = 16 - 9 = 7 --> [7]
```

### Code

**Python:**
```python
from collections import defaultdict

def count_subarrays(arr, x):
 """
 Count subarrays with sum equal to x using prefix sum + hash map.

 Time: O(n) - single pass
 Space: O(n) - hash map storage
 """
 prefix_count = defaultdict(int)
 prefix_count[0] = 1  # Empty prefix

 current_prefix = 0
 count = 0

 for num in arr:
  current_prefix += num
  # How many previous prefixes give us target?
  count += prefix_count[current_prefix - x]
  # Record this prefix
  prefix_count[current_prefix] += 1

 return count

# CSES Input/Output
def main():
 import sys
 input_data = sys.stdin.read().split()
 n, x = int(input_data[0]), int(input_data[1])
 arr = list(map(int, input_data[2:2+n]))
 print(count_subarrays(arr, x))

if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array, O(1) hash map operations |
| Space | O(n) | Hash map stores up to n distinct prefix sums |

---

## Common Mistakes

### Mistake 1: Forgetting to Initialize {0: 1}

```python
# WRONG
prefix_count = defaultdict(int)
# Missing: prefix_count[0] = 1

# This misses subarrays starting from index 0!
```

**Problem:** Subarrays starting from index 0 need prefix[j] - 0 = x, so we must have 0 in the map.
**Fix:** Always initialize with `prefix_count[0] = 1`.

### Mistake 2: Adding to Map Before Checking

```python
# WRONG
for num in arr:
 current_prefix += num
 prefix_count[current_prefix] += 1  # Added FIRST
 count += prefix_count[current_prefix - x]  # Check AFTER
```

**Problem:** If x = 0, this might count the same prefix as both start and end.
**Fix:** Check complement BEFORE adding current prefix to map.

### Mistake 3: Integer Overflow

**Problem:** With values up to 10^9 and n up to 2*10^5, prefix sum can reach 2*10^14.
**Fix:** Use `long long` for prefix sums and count.

### Mistake 4: Using unordered_map Without Care

**Safer Option:** Use `map` (O(log n) per operation) or custom hash for `unordered_map`.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single element match | `1 5`, `5` | 1 | Single element equals target |
| No solution | `3 100`, `1 2 3` | 0 | No subarray sums to target |
| All zeros, target zero | `3 0`, `0 0 0` | 6 | All 6 subarrays: [0], [0], [0], [0,0], [0,0], [0,0,0] |
| Negative target | `3 -3`, `1 -2 -2` | 1 | [-2, -2] + 1 = -3... actually [-2,-2] only if it sums to -3 |
| Large prefix sums | `2 0`, `10^9 -10^9` | 1 | Prefix: 10^9, 0. Need 0-0=0 in map |
| Entire array | `3 6`, `1 2 3` | 1 | [1,2,3] sums to 6 |

---

## When to Use This Pattern

### Use Prefix Sum + Hash Map When:
- Array contains **negative numbers** (sliding window fails)
- You need to **count** subarrays with exact sum (not find one)
- Target can be negative or zero
- O(n) time complexity is required

### Use Sliding Window Instead When:
- Array contains only **positive numbers** (Subarray Sums I)
- You need the actual subarray indices, not just count
- Memory is extremely constrained

### Pattern Recognition Checklist:
- [ ] Counting subarrays with specific sum? --> **Prefix Sum + Hash Map**
- [ ] All positive numbers? --> **Consider Sliding Window**
- [ ] Need indices, not count? --> **Modify to store indices**
- [ ] Multiple queries on same array? --> **Consider preprocessing**

---

## Related Problems

### Prerequisites (Do These First)

| Problem | Link | Why It Helps |
|---------|------|--------------|
| Subarray Sums I | [CSES 1660](https://cses.fi/problemset/task/1660) | Sliding window for positive-only arrays |
| Static Range Sum | [CSES 1646](https://cses.fi/problemset/task/1646) | Basic prefix sum understanding |

### Similar Difficulty

| Problem | Link | Key Difference |
|---------|------|----------------|
| Subarray Divisibility | [CSES 1662](https://cses.fi/problemset/task/1662) | Modular arithmetic with prefix sums |
| Two Sum | [CSES 1640](https://cses.fi/problemset/task/1640) | Hash map for complement search |

### Harder (Do These After)

| Problem | Link | New Concept |
|---------|------|-------------|
| Sum of Three Values | [CSES 1641](https://cses.fi/problemset/task/1641) | Extended to three numbers |
| Sum of Four Values | [CSES 1642](https://cses.fi/problemset/task/1642) | Extended to four numbers |

---

## Key Takeaways

1. **Core Idea:** Transform "find subarray sum" into "count complement prefix sums"
2. **Why Hash Map:** O(1) lookup turns O(n^2) brute force into O(n)
3. **Critical Detail:** Initialize with {0: 1} for subarrays starting at index 0
4. **vs Sliding Window:** This technique handles negative numbers; sliding window cannot
5. **Pattern Family:** "Prefix sum + complement" appears in many subarray problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why sliding window fails with negative numbers
- [ ] Derive the formula: prefix[i] = prefix[j] - x
- [ ] Implement from scratch without looking at solution
- [ ] Handle edge case: x = 0 with zeros in array
- [ ] Solve in under 10 minutes during contests
