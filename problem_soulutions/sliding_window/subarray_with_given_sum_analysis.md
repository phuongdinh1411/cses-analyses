---
layout: simple
title: "Subarray Sums I - Prefix Sum + Hash Map"
permalink: /problem_soulutions/sliding_window/subarray_with_given_sum_analysis
difficulty: Easy
tags: [prefix-sum, hash-map, subarray, counting]
prerequisites: []
---

# Subarray Sums I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Prefix Sum / Hash Map |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix Sum + Hash Map |
| **CSES Link** | [Subarray Sums I](https://cses.fi/problemset/task/1660) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the prefix sum technique for subarray problems
- [ ] Use hash maps to achieve O(1) lookups for complement values
- [ ] Count subarrays with a specific sum in O(n) time
- [ ] Recognize when to use prefix sum + hash map vs sliding window

---

## Problem Statement

**Problem:** Given an array of n positive integers and a target sum x, count the number of subarrays having sum exactly x.

**Input:**
- Line 1: Two integers n and x (array size and target sum)
- Line 2: n positive integers (array elements)

**Output:**
- Single integer: count of subarrays with sum equal to x

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= x <= 10^9
- 1 <= a[i] <= 10^9

### Example

```
Input:
5 7
2 4 1 2 7

Output:
3
```

**Explanation:** Three subarrays sum to 7:
- [2, 4, 1] at indices 0-2: 2 + 4 + 1 = 7
- [4, 1, 2] at indices 1-3: 4 + 1 + 2 = 7
- [7] at index 4: 7 = 7

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently check if any subarray sums to x?

The key insight is that if we know the prefix sum at every position, then the sum of any subarray arr[i..j] equals prefix[j] - prefix[i-1]. So finding a subarray with sum x means finding two prefix sums that differ by exactly x.

### Breaking Down the Problem

1. **What are we looking for?** Count of subarrays with sum equal to x
2. **What information do we have?** Array elements and target sum
3. **What is the relationship?** If prefix[j] - prefix[i] = x, then subarray from i+1 to j has sum x

### The Prefix Sum Trick

For any subarray sum from index i to j:
```
sum(arr[i..j]) = prefix[j] - prefix[i-1]
```

If we want this sum to equal x:
```
prefix[j] - prefix[i-1] = x
prefix[i-1] = prefix[j] - x
```

So at each position j, we need to count how many previous prefix sums equal `prefix[j] - x`.

---

## Solution 1: Brute Force

### Idea

Check all possible subarrays by trying every start and end position.

### Algorithm

1. For each starting index i from 0 to n-1
2. For each ending index j from i to n-1
3. Calculate sum of arr[i..j]
4. If sum equals x, increment count

### Code

```python
def count_subarrays_brute(arr, x):
 """
 Brute force: check all subarrays.

 Time: O(n^2)
 Space: O(1)
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
| Time | O(n^2) | Two nested loops over array |
| Space | O(1) | Only using variables |

### Why This Works (But Is Slow)

This checks every possible subarray, guaranteeing correctness. But with n up to 2*10^5, O(n^2) means up to 4*10^10 operations, which is too slow.

---

## Solution 2: Prefix Sum + Hash Map (Optimal)

### Key Insight

> **The Trick:** Store prefix sum frequencies in a hash map. At each position, look up how many times we have seen `current_prefix - x`.

### Algorithm

1. Initialize hash map with {0: 1} (empty prefix has sum 0)
2. Track running prefix sum
3. At each position, add count of (prefix_sum - x) from hash map
4. Store current prefix_sum in hash map

### Dry Run Example

Let's trace through with `arr = [2, 4, 1, 2, 7], x = 7`:

```
Initial: prefix_sum = 0, count = 0, freq = {0: 1}

i=0, arr[0]=2:
  prefix_sum = 0 + 2 = 2
  look for 2 - 7 = -5 in freq -> not found (0 matches)
  count = 0
  freq = {0: 1, 2: 1}

i=1, arr[1]=4:
  prefix_sum = 2 + 4 = 6
  look for 6 - 7 = -1 in freq -> not found (0 matches)
  count = 0
  freq = {0: 1, 2: 1, 6: 1}

i=2, arr[2]=1:
  prefix_sum = 6 + 1 = 7
  look for 7 - 7 = 0 in freq -> found! freq[0] = 1
  count = 0 + 1 = 1   (subarray [2,4,1] found)
  freq = {0: 1, 2: 1, 6: 1, 7: 1}

i=3, arr[3]=2:
  prefix_sum = 7 + 2 = 9
  look for 9 - 7 = 2 in freq -> found! freq[2] = 1
  count = 1 + 1 = 2   (subarray [4,1,2] found)
  freq = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1}

i=4, arr[4]=7:
  prefix_sum = 9 + 7 = 16
  look for 16 - 7 = 9 in freq -> found! freq[9] = 1
  count = 2 + 1 = 3   (subarray [7] found)
  freq = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1, 16: 1}

Final count = 3
```

### Visual Diagram

```
Array:  [2,  4,  1,  2,  7]
Index:   0   1   2   3   4

Prefix:  2   6   7   9  16
         |   |   |   |   |
         v   v   v   v   v

Looking for prefix differences = 7:
  prefix[2] - prefix[-1] = 7 - 0 = 7  -> [2,4,1]
  prefix[3] - prefix[0]  = 9 - 2 = 7  -> [4,1,2]
  prefix[4] - prefix[3]  = 16 - 9 = 7 -> [7]
```

### Code

**Python:**

```python
def count_subarrays(arr, x):
 """
 Count subarrays with sum equal to x using prefix sum + hash map.

 Time: O(n) - single pass
 Space: O(n) - hash map storage
 """
 prefix_sum = 0
 count = 0
 freq = {0: 1}  # Empty prefix has sum 0

 for num in arr:
  prefix_sum += num

  # How many previous prefixes give us target sum?
  complement = prefix_sum - x
  count += freq.get(complement, 0)

  # Store current prefix sum
  freq[prefix_sum] = freq.get(prefix_sum, 0) + 1

 return count


# Read input and solve
def main():
 n, x = map(int, input().split())
 arr = list(map(int, input().split()))
 print(count_subarrays(arr, x))


if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array |
| Space | O(n) | Hash map stores up to n prefix sums |

---

## Common Mistakes

### Mistake 1: Forgetting the Initial {0: 1}

```python
# WRONG - misses subarrays starting from index 0
freq = {}
for num in arr:
 prefix_sum += num
 count += freq.get(prefix_sum - x, 0)
 freq[prefix_sum] = freq.get(prefix_sum, 0) + 1
```

**Problem:** Without {0: 1}, we cannot find subarrays that start from index 0.

**Fix:** Always initialize with `freq = {0: 1}` to represent the empty prefix.

**Problem:** With values up to 10^9 and n up to 2*10^5, prefix sum can reach 2*10^14.

**Fix:** Use `long long` for prefix_sum, count, and map keys.

### Mistake 3: Storing Before Checking

```python
# WRONG - may count same element twice
for num in arr:
 prefix_sum += num
 freq[prefix_sum] = freq.get(prefix_sum, 0) + 1  # Store first
 count += freq.get(prefix_sum - x, 0)            # Then check
```

**Problem:** If x = 0, this would match the current prefix with itself.

**Fix:** Always check for complement BEFORE storing current prefix.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single element match | `n=1, x=5, arr=[5]` | 1 | Element equals target |
| No matches | `n=3, x=100, arr=[1,2,3]` | 0 | No subarray sums to 100 |
| All elements match | `n=3, x=1, arr=[1,1,1]` | 3 | Each element is a valid subarray |
| Entire array | `n=3, x=6, arr=[1,2,3]` | 1 | Only full array sums to 6 |
| Large values | `n=2, x=2e9, arr=[1e9,1e9]` | 1 | Handle large sums |

---

## When to Use This Pattern

### Use Prefix Sum + Hash Map When:
- Counting/finding subarrays with exact sum
- Array contains negative numbers (or general integers)
- You need O(n) time complexity

### Use Sliding Window Instead When:
- Array has only positive numbers AND
- You want existence check (not count) AND
- You want O(1) space complexity

### Pattern Recognition Checklist:
- [ ] Subarray sum problem? -> Consider prefix sum + hash map
- [ ] All positive values + existence only? -> Consider sliding window
- [ ] Need count of all subarrays with property? -> Likely prefix sum + hash map

---

## Related Problems

### CSES Problems

| Problem | Key Difference |
|---------|----------------|
| [Subarray Sums I](https://cses.fi/problemset/task/1660) | This problem (positive integers) |
| [Subarray Sums II](https://cses.fi/problemset/task/1661) | Includes negative integers |
| [Subarray Divisibility](https://cses.fi/problemset/task/1662) | Sum divisible by n |

### LeetCode Problems

| Problem | Key Difference |
|---------|----------------|
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Same technique, any integers |
| [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) | Sum divisible by k |
| [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | Binary array variant |

---

## Key Takeaways

1. **The Core Idea:** Use prefix sums so that subarray sum = difference of two prefix sums
2. **Time Optimization:** Hash map gives O(1) lookup for complement prefix sums
3. **Space Trade-off:** O(n) space for hash map enables O(n) time
4. **Critical Detail:** Initialize freq[0] = 1 to handle subarrays starting from index 0

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why prefix[j] - prefix[i-1] gives subarray sum from i to j
- [ ] Implement the solution without looking at code
- [ ] Handle the initialization of {0: 1} correctly
- [ ] Identify edge cases (single element, no matches, overflow)
- [ ] Solve in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Prefix Sums](https://cp-algorithms.com/data_structures/segment_tree.html)
- [CSES Subarray Sums I](https://cses.fi/problemset/task/1660) - Two pointers on subarrays
