---
layout: simple
title: "Array Division - Binary Search on Answer"
permalink: /problem_soulutions/sorting_and_searching/array_division_analysis
difficulty: Medium
tags: [binary-search, greedy, array-partitioning, optimization]
prerequisites: [binary_search_basics, greedy_algorithms]
---

# Array Division

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Binary Search on Answer + Greedy Check |
| **CSES Link** | [https://cses.fi/problemset/task/1085](https://cses.fi/problemset/task/1085) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when to apply binary search on the answer space
- [ ] Understand the monotonic property that enables binary search optimization
- [ ] Implement a greedy feasibility check for array partitioning
- [ ] Set correct binary search bounds for min-max optimization problems

---

## Problem Statement

**Problem:** Given an array of n positive integers, divide it into exactly k contiguous subarrays such that the maximum sum among all subarrays is minimized. Find this minimum possible maximum sum.

**Input:**
- Line 1: Two integers n and k (array size and number of subarrays)
- Line 2: n integers representing the array elements

**Output:**
- Print one integer: the minimum possible maximum sum

**Constraints:**
- 1 <= k <= n <= 2 x 10^5
- 1 <= a[i] <= 10^9

### Example

```
Input:
5 3
4 2 4 5 1

Output:
6
```

**Explanation:**
- Optimal division: [4, 2] | [4] | [5, 1]
- Subarray sums: 6, 4, 6
- Maximum sum = max(6, 4, 6) = 6
- No division into 3 subarrays can achieve a maximum sum less than 6.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** If we can check whether a given maximum sum M is achievable, can we find the minimum such M efficiently?

The answer is YES, because of the **monotonic property**: If we can divide the array with maximum sum M, we can also divide it with any maximum sum greater than M. This means we can binary search on the answer.

### Breaking Down the Problem

1. **What are we looking for?** The minimum value M such that we can divide the array into k subarrays where each subarray sum <= M.

2. **What is the search space?**
   - Lower bound: max(arr) - even one element must fit in a subarray
   - Upper bound: sum(arr) - all elements in one subarray

3. **How to check feasibility?** Greedily assign elements to subarrays: keep adding elements until the sum exceeds M, then start a new subarray.

### Analogies

Think of this problem like loading trucks with packages:
- You have k trucks and n packages in a fixed order
- Each truck has capacity M (what we're trying to minimize)
- Packages must be loaded in order (no reordering)
- Goal: Find the smallest truck capacity where k trucks suffice

---

## Solution 1: Brute Force with Dynamic Programming

### Idea

Use DP where dp[i][j] = minimum maximum sum when dividing the first i elements into j subarrays.

### Algorithm

1. Initialize dp[i][1] = sum of first i elements
2. For each position i and subarray count j, try all split points
3. Return dp[n][k]

### Code

```python
def solve_brute_force(n, k, arr):
 """
 DP solution - works but O(n^2 * k).

 Time: O(n^2 * k)
 Space: O(n * k)
 """
 INF = float('inf')
 prefix = [0] * (n + 1)
 for i in range(n):
  prefix[i + 1] = prefix[i] + arr[i]

 dp = [[INF] * (k + 1) for _ in range(n + 1)]

 # Base case: divide first i elements into 1 subarray
 for i in range(1, n + 1):
  dp[i][1] = prefix[i]

 for i in range(1, n + 1):
  for j in range(2, min(i + 1, k + 1)):
   for split in range(j - 1, i):
    subarray_sum = prefix[i] - prefix[split]
    dp[i][j] = min(dp[i][j], max(dp[split][j - 1], subarray_sum))

 return dp[n][k]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 * k) | Three nested loops |
| Space | O(n * k) | DP table |

### Why This Works (But Is Slow)

The DP correctly explores all possible divisions, but with n up to 2 x 10^5, O(n^2) is too slow. We need a better approach.

---

## Solution 2: Optimal - Binary Search on Answer

### Key Insight

> **The Trick:** Instead of finding the optimal division directly, binary search on the answer M and check if division is possible with maximum sum <= M using a greedy approach.

### Why Binary Search Works

The feasibility function is monotonic:
- If M is too small: we need more than k subarrays (NOT feasible)
- If M is just right or larger: we need at most k subarrays (feasible)

This monotonic property allows binary search to find the minimum feasible M.

### Greedy Check Algorithm

To check if max sum M is achievable:
1. Start with first subarray, current_sum = 0
2. For each element:
   - If adding it keeps current_sum <= M, add it
   - Otherwise, start a new subarray with this element
3. If total subarrays <= k, M is achievable

### Algorithm

1. Set left = max(arr), right = sum(arr)
2. Binary search: mid = (left + right) / 2
3. If can_divide(mid) is True, try smaller: right = mid
4. Otherwise, need larger: left = mid + 1
5. Return left when left == right

### Dry Run Example

Let's trace through with input `n=5, k=3, arr=[4, 2, 4, 5, 1]`:

```
Search space: left=5 (max element), right=16 (total sum)

Iteration 1: mid = (5 + 16) / 2 = 10
  Greedy check with max_sum = 10:
    [4] sum=4, [4,2] sum=6, [4,2,4] sum=10 <= 10, continue
    [4,2,4,5] sum=15 > 10, start new: [5]
    [5,1] sum=6 <= 10
    Subarrays: [4,2,4], [5,1] = 2 subarrays <= 3? YES
  can_divide(10) = True -> right = 10

Iteration 2: mid = (5 + 10) / 2 = 7
  Greedy check with max_sum = 7:
    [4] sum=4, [4,2] sum=6, [4,2,4] sum=10 > 7, start new: [4]
    [4,5] sum=9 > 7, start new: [5]
    [5,1] sum=6 <= 7
    Subarrays: [4,2], [4], [5,1] = 3 subarrays <= 3? YES
  can_divide(7) = True -> right = 7

Iteration 3: mid = (5 + 7) / 2 = 6
  Greedy check with max_sum = 6:
    [4] sum=4, [4,2] sum=6, [4,2,4] sum=10 > 6, start new: [4]
    [4,5] sum=9 > 6, start new: [5]
    [5,1] sum=6 <= 6
    Subarrays: [4,2], [4], [5,1] = 3 subarrays <= 3? YES
  can_divide(6) = True -> right = 6

Iteration 4: mid = (5 + 6) / 2 = 5
  Greedy check with max_sum = 5:
    [4] sum=4, [4,2] sum=6 > 5, start new: [2]
    [2,4] sum=6 > 5, start new: [4]
    [4,5] sum=9 > 5, start new: [5]
    [5,1] sum=6 > 5, start new: [1]
    Subarrays: [4], [2], [4], [5], [1] = 5 subarrays <= 3? NO
  can_divide(5) = False -> left = 6

Termination: left = 6, right = 6 -> Answer = 6
```

### Visual Diagram

```
Array: [4, 2, 4, 5, 1]  k = 3

Binary Search on Answer:
         5                    10                   16
         |---------------------|---------------------|
         max(arr)              mid                sum(arr)

Answer = 6: Optimal division
    [4, 2]  |  [4]  |  [5, 1]
    sum=6      sum=4    sum=6
              max = 6
```

### Code

**Python Solution:**

```python
import sys
input = sys.stdin.readline

def solve():
 n, k = map(int, input().split())
 arr = list(map(int, input().split()))

 def can_divide(max_sum):
  """
  Check if array can be divided into at most k subarrays
  where each subarray sum <= max_sum.

  Greedy: pack as many elements as possible into each subarray.
  """
  subarrays = 1
  current_sum = 0

  for num in arr:
   if current_sum + num <= max_sum:
    current_sum += num
   else:
    subarrays += 1
    current_sum = num
    if subarrays > k:
     return False

  return True

 # Binary search bounds
 left = max(arr)      # At least one element per subarray
 right = sum(arr)     # All elements in one subarray

 # Binary search for minimum feasible max_sum
 while left < right:
  mid = (left + right) // 2
  if can_divide(mid):
   right = mid  # Try smaller max_sum
  else:
   left = mid + 1  # Need larger max_sum

 print(left)

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log S) | Binary search (log S iterations) with O(n) check each |
| Space | O(1) | Only a few variables (excluding input storage) |

Where S = sum(arr), so log S <= 64 for typical constraints.

---

## Common Mistakes

### Mistake 1: Wrong Lower Bound

```python
# WRONG - might be less than the largest element
left = 1

# CORRECT - must fit the largest element
left = max(arr)
```

**Problem:** If left < max(arr), we would try to fit a single element into a subarray with capacity less than that element.
**Fix:** Lower bound must be max(arr) since each element must fit in some subarray.

### Mistake 2: Incorrect Greedy Check Logic

```python
# WRONG - starting new subarray even when not needed
if current_sum + num > max_sum:
 subarrays += 1
 current_sum = 0  # Bug: should be current_sum = num
 current_sum += num
```

**Problem:** When starting a new subarray, the current element should be its first element.
**Fix:** Set current_sum = num when starting a new subarray.

**Problem:** With n = 2 x 10^5 elements each up to 10^9, sum can reach 2 x 10^14.
**Fix:** Use `long long` for sums and binary search bounds.

### Mistake 4: Off-by-One in Subarray Count

```python
# WRONG - counting subarrays incorrectly
subarrays = 0  # Should start at 1
for num in arr:
 if current_sum + num > max_sum:
  subarrays += 1
  current_sum = num
 else:
  current_sum += num
# Forgot to count the last subarray!
```

**Problem:** Starting count at 0 and not accounting for the final subarray.
**Fix:** Start with subarrays = 1 (we always have at least one subarray).

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k = n | `n=3, k=3, arr=[1,2,3]` | 3 | Each element is its own subarray, max is 3 |
| k = 1 | `n=3, k=1, arr=[1,2,3]` | 6 | All elements in one subarray |
| Single element | `n=1, k=1, arr=[5]` | 5 | Only one way to divide |
| All same | `n=4, k=2, arr=[5,5,5,5]` | 10 | Best split: [5,5] and [5,5] |
| Large values | `n=2, k=2, arr=[10^9, 10^9]` | 10^9 | Test long long handling |

---

## When to Use This Pattern

### Use Binary Search on Answer When:
- You need to minimize/maximize some value
- There is a monotonic feasibility function
- Checking feasibility is faster than direct computation
- The answer space is bounded and searchable

### Pattern Recognition Checklist:
- [ ] Minimize maximum or maximize minimum? -> **Consider binary search on answer**
- [ ] Can you check "is X achievable" efficiently? -> **Greedy check often works**
- [ ] Does achievability have monotonic property? -> **Binary search applies**

### Common Problem Types:
- Minimize maximum load/sum/time across workers/machines/days
- Maximize minimum distance/capacity/value
- Allocate resources with constraints

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Binary Search](https://cses.fi/problemset/task/1083) | Basic binary search mechanics |
| [Factory Machines](https://cses.fi/problemset/task/1620) | Binary search on answer, simpler check |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Split Array Largest Sum (LeetCode 410)](https://leetcode.com/problems/split-array-largest-sum/) | Identical problem |
| [Capacity To Ship Packages (LeetCode 1011)](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Days instead of subarrays |
| [Koko Eating Bananas (LeetCode 875)](https://leetcode.com/problems/koko-eating-bananas/) | Similar binary search pattern |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimize Max Distance to Gas Station (LeetCode 774)](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) | Continuous search space |
| [Magnetic Force Between Balls (LeetCode 1552)](https://leetcode.com/problems/magnetic-force-between-two-balls/) | Maximize minimum variant |

---

## Key Takeaways

1. **The Core Idea:** Binary search on the answer when feasibility is monotonic
2. **Time Optimization:** From O(n^2 * k) DP to O(n log S) binary search
3. **Space Trade-off:** Reduced from O(n * k) to O(1)
4. **Pattern:** "Minimize maximum" problems often yield to binary search on answer

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why the greedy check works
- [ ] Implement the binary search with correct bounds
- [ ] Handle edge cases (k=1, k=n, large values)
- [ ] Identify this pattern in new problems

---

## Additional Resources

- [CP-Algorithms: Binary Search](https://cp-algorithms.com/num_methods/binary_search.html)
- [CSES Array Division](https://cses.fi/problemset/task/1085) - Binary search the answer
- [Binary Search on Answer Pattern](https://usaco.guide/silver/binary-search-ans)
