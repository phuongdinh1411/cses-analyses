---
layout: simple
title: "Subarray Sums II - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/subarray_sums_ii_analysis
difficulty: Medium
tags: [prefix-sum, hash-map, subarray, counting]
prerequisites: [subarray_sums_i]
---

# Subarray Sums II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1661](https://cses.fi/problemset/task/1661) |
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix Sum + Hash Map |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Use prefix sums to reduce subarray sum queries to O(1)
- [ ] Apply the "complement counting" technique with hash maps
- [ ] Handle negative numbers in subarray sum problems (unlike Subarray Sums I)
- [ ] Recognize when sliding window fails and hash map is needed

---

## Problem Statement

**Problem:** Given an array of n integers (can be negative, zero, or positive) and a target sum x, count the number of subarrays whose sum equals x.

**Input:**
- Line 1: Two integers n and x (array size and target sum)
- Line 2: n integers a[1], a[2], ..., a[n] (array elements)

**Output:**
- Print one integer: the number of subarrays whose sum equals x

**Constraints:**
- 1 <= n <= 2 x 10^5
- -10^9 <= x <= 10^9
- -10^9 <= a[i] <= 10^9

### Example

```
Input:
5 7
2 4 1 2 7

Output:
3
```

**Explanation:** The subarrays with sum 7 are:
- [2, 4, 1] at indices 0-2: 2 + 4 + 1 = 7
- [4, 1, 2] at indices 1-3: 4 + 1 + 2 = 7
- [7] at index 4: 7 = 7

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How is this different from Subarray Sums I?

In Subarray Sums I, all numbers are **positive**, so we can use sliding window: if the current sum exceeds the target, shrinking the window always reduces the sum. But with **negative numbers**, shrinking might increase or decrease the sum unpredictably. Sliding window breaks!

### The Prefix Sum Insight

Any subarray sum can be expressed as the difference of two prefix sums:

```
sum(arr[i..j]) = prefix[j+1] - prefix[i]
```

If we want `sum(arr[i..j]) = target`, then:

```
prefix[j+1] - prefix[i] = target
prefix[i] = prefix[j+1] - target
```

So for each position j, we need to count how many earlier prefix sums equal `prefix[j+1] - target`.

### Why Hash Map?

Instead of checking all previous prefix sums (O(n) each), we store prefix sum frequencies in a hash map for O(1) lookup.

### Analogy

Think of it like a cash register. Your running total (prefix sum) is 15, and you need to find how many times in the past your total was 8 (because 15 - 8 = 7, your target). A hash map acts like a ledger tracking all past totals.

---

## Solution 1: Brute Force

### Idea

Check every possible subarray and count those with sum equal to target.

### Algorithm

1. For each starting index i (0 to n-1):
2. For each ending index j (i to n-1):
3. Calculate sum of arr[i..j] and check if it equals target

### Code

```python
def solve_brute_force(n, arr, target):
 """
 Check all O(n^2) subarrays.

 Time: O(n^2) with prefix sums, O(n^3) without
 Space: O(n) for prefix sums
 """
 count = 0
 prefix = [0] * (n + 1)
 for i in range(n):
  prefix[i + 1] = prefix[i] + arr[i]

 for i in range(n):
  for j in range(i, n):
   if prefix[j + 1] - prefix[i] == target:
    count += 1
 return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Two nested loops over indices |
| Space | O(n) | Prefix sum array |

### Why This Works (But Is Slow)

Correctly enumerates all subarrays, but for n = 2 x 10^5, we need 4 x 10^10 operations - far too slow.

---

## Solution 2: Optimal Solution (Prefix Sum + Hash Map)

### Key Insight

> **The Trick:** For each prefix sum, count how many previous prefix sums equal `current_prefix - target` using a hash map.

### Algorithm

1. Initialize `prefix_count = {0: 1}` (empty prefix has sum 0)
2. Track running `prefix_sum = 0` and `count = 0`
3. For each element:
   - Add element to prefix_sum
   - Add `prefix_count[prefix_sum - target]` to count (if exists)
   - Increment `prefix_count[prefix_sum]`
4. Return count

### Why Initialize with {0: 1}?

This handles subarrays starting from index 0. If `prefix_sum == target`, we need to find how many times we've seen `prefix_sum - target = 0`. The empty prefix (before any element) has sum 0.

### Dry Run Example

Let's trace through `arr = [2, 4, 1, 2, 7], target = 7`:

```
Initial: prefix_sum = 0, count = 0, prefix_count = {0: 1}

Step 1: arr[0] = 2
  prefix_sum = 0 + 2 = 2
  Look for 2 - 7 = -5 in map? NO
  count = 0
  prefix_count = {0: 1, 2: 1}

Step 2: arr[1] = 4
  prefix_sum = 2 + 4 = 6
  Look for 6 - 7 = -1 in map? NO
  count = 0
  prefix_count = {0: 1, 2: 1, 6: 1}

Step 3: arr[2] = 1
  prefix_sum = 6 + 1 = 7
  Look for 7 - 7 = 0 in map? YES! count += 1
  count = 1  (found subarray [2,4,1])
  prefix_count = {0: 1, 2: 1, 6: 1, 7: 1}

Step 4: arr[3] = 2
  prefix_sum = 7 + 2 = 9
  Look for 9 - 7 = 2 in map? YES! count += 1
  count = 2  (found subarray [4,1,2])
  prefix_count = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1}

Step 5: arr[4] = 7
  prefix_sum = 9 + 7 = 16
  Look for 16 - 7 = 9 in map? YES! count += 1
  count = 3  (found subarray [7])
  prefix_count = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1, 16: 1}

Final answer: 3
```

### Visual Diagram

```
Array:     [2,    4,    1,    2,    7]
Index:      0     1     2     3     4

Prefix:  0    2    6    7    9    16
         ^              ^
         |              |
         +-- diff = 7 --+  (subarray [2,4,1])

         ^                   ^
         |                   |
         +---- diff = 9 ----+  ... wait, that's not 7

              ^         ^
              |         |
              +- diff=7-+  (subarray [4,1,2], since 9-2=7)

                             ^    ^
                             |    |
                             +-7--+  (subarray [7], since 16-9=7)
```

### Code

**Python:**

```python
import sys
from collections import defaultdict

def solve(n, arr, target):
 """
 Count subarrays with sum equal to target.

 Time: O(n) - single pass
 Space: O(n) - hash map for prefix sums
 """
 count = 0
 prefix_sum = 0
 prefix_count = defaultdict(int)
 prefix_count[0] = 1  # Empty prefix

 for num in arr:
  prefix_sum += num
  # How many previous prefixes give us target sum?
  count += prefix_count[prefix_sum - target]
  # Record current prefix
  prefix_count[prefix_sum] += 1

 return count

def main():
 input_data = sys.stdin.read().split()
 n = int(input_data[0])
 x = int(input_data[1])
 arr = list(map(int, input_data[2:2+n]))
 print(solve(n, arr, x))

if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array, O(1) hash map operations |
| Space | O(n) | Hash map stores at most n+1 distinct prefix sums |

---

## Common Mistakes

### Mistake 1: Forgetting to Initialize prefix_count[0] = 1

```python
# WRONG
prefix_count = defaultdict(int)
# prefix_count[0] = 1  <- Missing!

for num in arr:
 prefix_sum += num
 count += prefix_count[prefix_sum - target]
 prefix_count[prefix_sum] += 1
```

**Problem:** Misses subarrays starting from index 0. If `arr = [7]` and `target = 7`, the answer should be 1, but this returns 0.

**Fix:** Always initialize with `prefix_count[0] = 1` to represent the empty prefix.

**Problem:** With values up to 10^9 and n up to 2 x 10^5, prefix sums can reach 2 x 10^14, exceeding int range.

**Fix:** Use `long long` for prefix sums and the count variable.

### Mistake 3: Adding to Map Before Checking

```python
# WRONG - counts subarray of length 0
for num in arr:
 prefix_sum += num
 prefix_count[prefix_sum] += 1  # Added first
 count += prefix_count[prefix_sum - target]  # Then checked
```

**Problem:** If `target = 0`, this incorrectly counts each element as a valid subarray (matching itself).

**Fix:** Always check **before** adding the current prefix to the map.

### Mistake 4: Using Sliding Window (Wrong Approach)

```python
# WRONG - doesn't work with negative numbers
left = 0
current_sum = 0
for right in range(n):
 current_sum += arr[right]
 while current_sum > target and left <= right:
  current_sum -= arr[left]
  left += 1
 if current_sum == target:
  count += 1
```

**Problem:** Sliding window assumes shrinking reduces sum, which fails with negatives.

**Fix:** Use prefix sum + hash map approach instead.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element match | `n=1, arr=[5], x=5` | 1 | The element itself is a valid subarray |
| No solution | `n=3, arr=[1,2,3], x=10` | 0 | No subarray sums to 10 |
| All elements valid | `n=3, arr=[0,0,0], x=0` | 6 | All 6 subarrays sum to 0 |
| Negative numbers | `n=4, arr=[1,-1,1,-1], x=0` | 4 | Subarrays: [1,-1], [-1,1], [1,-1], [1,-1,1,-1] |
| Large values | `n=2, arr=[10^9, 10^9], x=2*10^9` | 1 | Only full array sums to target |
| Negative target | `n=3, arr=[-1,-2,-3], x=-3` | 2 | Subarrays: [-1,-2] and [-3] |
| Duplicate prefix sums | `n=4, arr=[1,-1,1,-1], x=0` | 4 | Multiple prefixes with same sum |

---

## When to Use This Pattern

### Use Prefix Sum + Hash Map When:
- Finding subarrays with a specific sum (this problem)
- Array contains negative numbers or zeros
- Counting subarrays divisible by k (Subarray Divisibility)
- Finding longest subarray with sum k

### Use Sliding Window Instead When:
- All elements are **positive** (Subarray Sums I)
- Looking for minimum/maximum length subarray with sum >= k
- The "shrink" operation is monotonic

### Pattern Recognition Checklist:
- [ ] Subarray sum problem? --> Consider prefix sums
- [ ] Negative numbers present? --> Hash map, not sliding window
- [ ] Need to count/find all? --> Hash map for O(n) solution
- [ ] Need specific sum? --> Complement technique (`prefix - target`)

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subarray Sums I (CSES 1660)](https://cses.fi/problemset/task/1660) | Positive-only version, use sliding window |
| [Two Sum (LeetCode)](https://leetcode.com/problems/two-sum/) | Same complement technique, simpler context |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Subarray Sum Equals K (LeetCode 560)](https://leetcode.com/problems/subarray-sum-equals-k/) | Same problem, different platform |
| [Subarray Divisibility (CSES 1662)](https://cses.fi/problemset/task/1662) | Count subarrays divisible by n |
| [Continuous Subarray Sum (LeetCode 523)](https://leetcode.com/problems/continuous-subarray-sum/) | Divisibility variant with length >= 2 |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Count Number of Nice Subarrays (LeetCode 1248)](https://leetcode.com/problems/count-number-of-nice-subarrays/) | Prefix count of odd numbers |
| [Binary Subarrays With Sum (LeetCode 930)](https://leetcode.com/problems/binary-subarrays-with-sum/) | Binary array variant |
| [Subarray Sums with Constraints](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/) | Maximum length variant |

---

## Key Takeaways

1. **The Core Idea:** Transform subarray sums into prefix sum differences, then use hash map to count complements.
2. **Time Optimization:** From O(n^2) brute force to O(n) with hash map lookups.
3. **Space Trade-off:** O(n) space for hash map enables linear time.
4. **Key Difference from Subarray Sums I:** Negative numbers break sliding window; must use prefix + hash map.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why sliding window fails with negative numbers
- [ ] Derive the `prefix[j] - prefix[i] = target` relationship
- [ ] Explain why we initialize with `{0: 1}`
- [ ] Handle integer overflow in C++
- [ ] Solve this problem in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Prefix Sums](https://cp-algorithms.com/others/prefix_sums.html)
- [LeetCode Discuss: Subarray Sum Pattern](https://leetcode.com/problems/subarray-sum-equals-k/discuss/341399/)
- [CSES Subarray Sums II](https://cses.fi/problemset/task/1661) - Prefix sum with negative values
