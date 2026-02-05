---
layout: simple
title: "Subarray Divisibility - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/subarray_divisibility_analysis
difficulty: Medium
tags: [prefix-sum, modular-arithmetic, hash-map, counting]
prerequisites: [prefix_sums_basics, modular_arithmetic]
---

# Subarray Divisibility

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix Sums + Modular Arithmetic |
| **CSES Link** | [https://cses.fi/problemset/task/1662](https://cses.fi/problemset/task/1662) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply prefix sums with modular arithmetic to count subarrays
- [ ] Use the pigeonhole principle to optimize counting problems
- [ ] Handle negative modulo correctly in different programming languages
- [ ] Recognize when prefix sum remainder counting leads to O(n) solutions

---

## Problem Statement

**Problem:** Given an array of n integers, count the number of subarrays whose sum is divisible by n.

**Input:**
- Line 1: Integer n (1 <= n <= 2 x 10^5)
- Line 2: n integers a[1], a[2], ..., a[n] (-10^9 <= a[i] <= 10^9)

**Output:**
- Print one integer: the number of subarrays whose sum is divisible by n

**Constraints:**
- 1 <= n <= 2 x 10^5
- -10^9 <= a[i] <= 10^9

### Example

```
Input:
5
3 1 2 7 4

Output:
1
```

**Explanation:** The subarray [1, 2, 7] (indices 1-3, 0-indexed) has sum 10, which is divisible by 5.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently determine if a subarray sum is divisible by n?

The key insight is that if `prefix[i] % n == prefix[j] % n` for i < j, then the sum of elements from index i+1 to j is divisible by n. This is because:
- `sum(i+1, j) = prefix[j] - prefix[i]`
- If both have the same remainder when divided by n, their difference is divisible by n.

### Breaking Down the Problem

1. **What are we looking for?** Count of subarrays with sum divisible by n
2. **What information do we have?** Array elements and the divisor (which equals array length)
3. **What's the relationship between input and output?** Two prefix sums with the same remainder mod n define a valid subarray

### The Mathematical Foundation

For subarray `arr[i+1...j]` to have sum divisible by n:
```
sum(i+1, j) = prefix[j] - prefix[i]
sum(i+1, j) % n == 0
=> (prefix[j] - prefix[i]) % n == 0
=> prefix[j] % n == prefix[i] % n
```

**Key Insight:** If `prefix[i] % n == prefix[j] % n`, then the subarray sum from i+1 to j is divisible by n.

---

## Solution 1: Brute Force

### Idea

Check all possible subarrays and count those with sum divisible by n.

### Algorithm

1. For each starting position i
2. For each ending position j >= i
3. Calculate subarray sum and check divisibility
4. Increment count if divisible

### Code

```python
def solve_brute_force(n, arr):
 """
 Brute force: check all subarrays.

 Time: O(n^2)
 Space: O(1)
 """
 count = 0
 for i in range(n):
  current_sum = 0
  for j in range(i, n):
   current_sum += arr[j]
   if current_sum % n == 0:
    count += 1
 return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Nested loops over all subarrays |
| Space | O(1) | Only tracking current sum and count |

### Why This Works (But Is Slow)

This approach correctly checks every possible subarray but is too slow for n up to 2 x 10^5. We need O(n) or O(n log n) solution.

---

## Solution 2: Optimal - Prefix Sum Remainder Counting

### Key Insight

> **The Trick:** Count prefix sums with the same remainder mod n. Each pair of such prefix sums defines a valid subarray.

If we have `k` prefix sums with the same remainder `r`, we can form `C(k,2) = k*(k-1)/2` valid subarrays from them.

### Algorithm

1. Compute prefix sums while tracking remainders
2. For each prefix sum, calculate `prefix[i] % n`
3. Handle negative remainders by adding n
4. Count frequency of each remainder
5. For each remainder with frequency f, add `f*(f-1)/2` to answer

### Dry Run Example

Let's trace through with input `n = 5, arr = [3, 1, 2, 7, 4]`:

```
Initial state:
  prefix = 0
  remainder_count = {0: 1}  // Initialize with 0 for empty prefix
  result = 0

Step 1: Process arr[0] = 3
  prefix = 0 + 3 = 3
  remainder = 3 % 5 = 3
  Count of remainder 3 so far = 0
  result += 0
  remainder_count = {0: 1, 3: 1}

Step 2: Process arr[1] = 1
  prefix = 3 + 1 = 4
  remainder = 4 % 5 = 4
  Count of remainder 4 so far = 0
  result += 0
  remainder_count = {0: 1, 3: 1, 4: 1}

Step 3: Process arr[2] = 2
  prefix = 4 + 2 = 6
  remainder = 6 % 5 = 1
  Count of remainder 1 so far = 0
  result += 0
  remainder_count = {0: 1, 3: 1, 4: 1, 1: 1}

Step 4: Process arr[3] = 7
  prefix = 6 + 7 = 13
  remainder = 13 % 5 = 3
  Count of remainder 3 so far = 1  <-- MATCH!
  result += 1
  remainder_count = {0: 1, 3: 2, 4: 1, 1: 1}

  // This means subarray from index 1 to 3: [1, 2, 7] = 10, divisible by 5

Step 5: Process arr[4] = 4
  prefix = 13 + 4 = 17
  remainder = 17 % 5 = 2
  Count of remainder 2 so far = 0
  result += 0
  remainder_count = {0: 1, 3: 2, 4: 1, 1: 1, 2: 1}

Final result = 1
```

### Visual Diagram

```
Array:    [3,  1,  2,  7,  4]
Index:     0   1   2   3   4

Prefix:    0   3   4   6  13  17
           ^               ^
           |               |
           +---------------+
           Both have remainder 3 when divided by 5

Subarray [1, 2, 7]: sum = 10, divisible by 5
```

### Code

```python
def solve_optimal(n, arr):
 """
 Optimal solution using prefix sum remainders.

 Time: O(n) - single pass
 Space: O(n) - hash map for remainder counts
 """
 remainder_count = {0: 1}  # Empty prefix has sum 0
 prefix = 0
 result = 0

 for num in arr:
  prefix += num
  # Handle negative modulo
  remainder = prefix % n
  if remainder < 0:
   remainder += n

  # Add count of previous prefix sums with same remainder
  result += remainder_count.get(remainder, 0)
  remainder_count[remainder] = remainder_count.get(remainder, 0) + 1

 return result


# Main execution for CSES
def main():
 n = int(input())
 arr = list(map(int, input().split()))
 print(solve_optimal(n, arr))

if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through the array |
| Space | O(n) | Hash map stores at most n distinct remainders |

---

## Common Mistakes

### Mistake 1: Not Handling Negative Modulo

```python
# WRONG (in languages where % can return negative)
remainder = prefix % n

# CORRECT
remainder = prefix % n
if remainder < 0:
 remainder += n

# Or in C++:
remainder = ((prefix % n) + n) % n
```

**Problem:** In C++ and some other languages, `-7 % 5` returns `-2`, not `3`.
**Fix:** Always normalize negative remainders by adding n.

### Mistake 2: Forgetting to Initialize remainder_count[0] = 1

```python
# WRONG
remainder_count = {}

# CORRECT
remainder_count = {0: 1}  # Empty prefix counts!
```

**Problem:** Missing subarrays that start from index 0 and have sum divisible by n.
**Fix:** Initialize with `{0: 1}` to account for the empty prefix (prefix[0] = 0).

### Mistake 3: Using Array Instead of Long Long for Large Sums

**Problem:** With elements up to 10^9 and n up to 2 x 10^5, prefix sum can overflow int.
**Fix:** Use `long long` for prefix sums.

### Mistake 4: Misunderstanding the Counting Formula

```python
# WRONG: Adding 1 for each matching remainder found
result += 1  # Only counts one pair

# CORRECT: Add count of all previous matches
result += remainder_count.get(remainder, 0)
```

**Problem:** Each new prefix with remainder r can pair with ALL previous prefixes with remainder r.
**Fix:** Add the current count before incrementing it.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element divisible | `n=1, arr=[5]` | `1` | Any single element sum is divisible by 1 |
| All zeros | `n=3, arr=[0,0,0]` | `6` | Every subarray sums to 0 |
| No valid subarray | `n=3, arr=[1,1,1]` | `1` | Only [1,1,1] sums to 3, divisible by 3 |
| Negative elements | `n=3, arr=[-1,2,-1]` | `1` | Subarray [-1,2,-1] sums to 0 |
| Large values | `n=2, arr=[10^9, 10^9]` | `1` | Handle overflow with long long |

---

## When to Use This Pattern

### Use This Approach When:
- Counting subarrays with sum divisible by k
- Need O(n) solution for subarray sum problems
- Prefix sums are applicable and remainders can be efficiently counted

### Don't Use When:
- Looking for subarrays with sum equal to a specific target (use hash map with prefix sums directly)
- Need to find the actual subarrays, not just count them
- Problem involves product instead of sum (different approach needed)

### Pattern Recognition Checklist:
- [ ] Counting subarrays with sum property? --> **Consider prefix sums**
- [ ] Divisibility condition? --> **Consider modular arithmetic**
- [ ] Need pairs with same property? --> **Consider hash map counting**
- [ ] Can reduce to "count pairs"? --> **Use formula C(k,2) = k*(k-1)/2**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subarray Sums I (CSES)](https://cses.fi/problemset/task/1660) | Basic prefix sum + hash map |
| [Subarray Sums II (CSES)](https://cses.fi/problemset/task/1661) | Handles negative numbers |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Subarray Sum Equals K (LeetCode)](https://leetcode.com/problems/subarray-sum-equals-k/) | Target sum instead of divisibility |
| [Continuous Subarray Sum (LeetCode)](https://leetcode.com/problems/continuous-subarray-sum/) | Divisible by k with length >= 2 |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Subarray Sums Divisible by K (LeetCode)](https://leetcode.com/problems/subarray-sums-divisible-by-k/) | Generalized to any k |
| [Make Sum Divisible by P (LeetCode)](https://leetcode.com/problems/make-sum-divisible-by-p/) | Remove minimum elements |

---

## Key Takeaways

1. **The Core Idea:** Two prefix sums with the same remainder mod n define a subarray divisible by n
2. **Time Optimization:** From O(n^2) brute force to O(n) using hash map for remainder counting
3. **Space Trade-off:** O(n) space for hash map enables single-pass O(n) time
4. **Pattern:** Prefix Sum + Modular Arithmetic + Counting Pairs

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why same remainders imply divisible subarray sum
- [ ] Handle negative modulo correctly
- [ ] Implement the solution in under 10 minutes
- [ ] Identify similar problems that use this pattern

---

## Additional Resources

- [CP-Algorithms: Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sum.html)
- [CSES Subarray Divisibility](https://cses.fi/problemset/task/1662) - Prefix sum with modular arithmetic
- [LeetCode Modular Arithmetic Problems](https://leetcode.com/tag/math/)
