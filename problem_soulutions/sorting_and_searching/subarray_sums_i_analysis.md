---
layout: simple
title: "Subarray Sums I - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/subarray_sums_i_analysis
difficulty: Easy
tags: [prefix-sum, hash-map, counting, sliding-window]
prerequisites: []
---

# Subarray Sums I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix Sum + Hash Map |
| **CSES Link** | [https://cses.fi/problemset/task/1660](https://cses.fi/problemset/task/1660) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how prefix sums enable O(1) subarray sum calculations
- [ ] Use a hash map to count occurrences of prefix sums
- [ ] Apply the "complement counting" pattern: if prefix[j] - prefix[i] = x, then we need prefix[i] = prefix[j] - x
- [ ] Handle the base case of prefix sum = 0 (subarray starting from index 0)

---

## Problem Statement

**Problem:** Given an array of n positive integers and a target sum x, count the number of subarrays that have sum exactly equal to x.

**Input:**
- Line 1: Two integers n (array size) and x (target sum)
- Line 2: n positive integers a_1, a_2, ..., a_n

**Output:**
- One integer: the count of subarrays with sum equal to x

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= x <= 10^9
- 1 <= a_i <= 10^9 (all elements are positive)

### Example

```
Input:
5 7
2 4 1 2 7

Output:
3
```

**Explanation:**
The subarrays with sum 7 are:
1. [2, 4, 1] at indices 1-3: 2 + 4 + 1 = 7
2. [4, 1, 2] at indices 2-4: 4 + 1 + 2 = 7
3. [7] at index 5: 7 = 7

Total: 3 subarrays

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently check if any subarray sums to x without checking all O(n^2) subarrays?

The key insight is that the sum of subarray arr[i..j] equals prefix[j] - prefix[i-1]. So if we want prefix[j] - prefix[i-1] = x, we need prefix[i-1] = prefix[j] - x. This transforms the problem into: "For each position j, how many previous prefix sums equal (current_prefix - x)?"

### Breaking Down the Problem

1. **What are we looking for?** Count of subarrays with sum exactly x
2. **What information do we have?** Array of positive integers, target sum x
3. **What's the relationship?** sum(arr[i..j]) = prefix[j] - prefix[i-1] = x

### Why This Works

```
If we have: prefix_sum[j] - prefix_sum[i-1] = x
Then:       prefix_sum[i-1] = prefix_sum[j] - x

So at each position j, we count how many times we've seen
the value (prefix_sum[j] - x) in our previous prefix sums.
```

### Analogies

Think of this like a financial ledger. Your running balance (prefix sum) at any point tells you the total so far. To find a period where you earned exactly x dollars, you look for a previous balance that is exactly x less than your current balance.

---

## Solution 1: Brute Force

### Idea

Check every possible subarray by trying all pairs of start and end positions.

### Algorithm

1. For each starting position i from 0 to n-1
2. For each ending position j from i to n-1
3. Calculate sum of arr[i..j] and check if it equals x
4. Count all matching subarrays

### Code

```python
def solve_brute_force(n, x, arr):
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
            if current_sum == x:
                count += 1

    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Nested loops over all subarray pairs |
| Space | O(1) | Only storing count and current_sum |

### Why This Works (But Is Slow)

This correctly checks every possible subarray, but with n up to 2*10^5, we'd have up to 4*10^10 operations which is far too slow.

---

## Solution 2: Optimal Solution (Prefix Sum + Hash Map)

### Key Insight

> **The Trick:** Instead of checking all subarrays, maintain a hash map of prefix sum frequencies and look up complements in O(1).

### The Prefix Sum Property

| Concept | Formula |
|---------|---------|
| Prefix sum at j | prefix[j] = arr[0] + arr[1] + ... + arr[j] |
| Subarray sum i to j | sum(arr[i..j]) = prefix[j] - prefix[i-1] |
| Target condition | prefix[j] - prefix[i-1] = x |
| What we need to find | prefix[i-1] = prefix[j] - x |

**In plain English:** At each position, count how many times we've seen a prefix sum that is exactly x less than the current prefix sum.

### Base Case: Why We Initialize with {0: 1}

We must initialize the hash map with {0: 1} because:
- If a subarray starting from index 0 has sum x, then prefix[j] = x
- We need prefix[j] - x = 0 to exist in our map
- The "empty prefix" before index 0 has sum 0

### Algorithm

1. Initialize hash map with {0: 1} (empty prefix)
2. Initialize prefix_sum = 0 and count = 0
3. For each element in array:
   - Add element to prefix_sum
   - Add count_map[prefix_sum - x] to count (if exists)
   - Increment count_map[prefix_sum] by 1
4. Return count

### Dry Run Example

Let's trace through with input `n = 5, x = 7, arr = [2, 4, 1, 2, 7]`:

```
Initial state:
  count_map = {0: 1}  (empty prefix)
  prefix_sum = 0
  count = 0

Step 1: Process arr[0] = 2
  prefix_sum = 0 + 2 = 2
  complement = 2 - 7 = -5
  -5 not in count_map -> count += 0
  count_map = {0: 1, 2: 1}
  count = 0

Step 2: Process arr[1] = 4
  prefix_sum = 2 + 4 = 6
  complement = 6 - 7 = -1
  -1 not in count_map -> count += 0
  count_map = {0: 1, 2: 1, 6: 1}
  count = 0

Step 3: Process arr[2] = 1
  prefix_sum = 6 + 1 = 7
  complement = 7 - 7 = 0
  0 IS in count_map with count 1 -> count += 1
  count_map = {0: 1, 2: 1, 6: 1, 7: 1}
  count = 1
  (Found subarray [2,4,1] from index 0 to 2)

Step 4: Process arr[3] = 2
  prefix_sum = 7 + 2 = 9
  complement = 9 - 7 = 2
  2 IS in count_map with count 1 -> count += 1
  count_map = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1}
  count = 2
  (Found subarray [4,1,2] from index 1 to 3)

Step 5: Process arr[4] = 7
  prefix_sum = 9 + 7 = 16
  complement = 16 - 7 = 9
  9 IS in count_map with count 1 -> count += 1
  count_map = {0: 1, 2: 1, 6: 1, 7: 1, 9: 1, 16: 1}
  count = 3
  (Found subarray [7] from index 4 to 4)

Final answer: 3
```

### Visual Diagram

```
Array:       [2,   4,   1,   2,   7]
Index:        0    1    2    3    4

Prefix:       2    6    7    9   16
              |    |    |    |    |
              v    v    v    v    v
Target x=7:

Step 3: prefix=7, need 0 (found!) -> subarray [0..2] = [2,4,1]
Step 4: prefix=9, need 2 (found!) -> subarray [1..3] = [4,1,2]
Step 5: prefix=16, need 9 (found!) -> subarray [4..4] = [7]

Subarrays with sum 7:
[2, 4, 1]     sum = 7  ✓
   [4, 1, 2]  sum = 7  ✓
            [7] sum = 7  ✓
```

### Code (Python)

```python
from collections import defaultdict

def solve_optimal(n, x, arr):
    """
    Optimal solution using prefix sum + hash map.

    Time: O(n) - single pass
    Space: O(n) - hash map storage
    """
    count_map = defaultdict(int)
    count_map[0] = 1  # Empty prefix (crucial!)

    prefix_sum = 0
    count = 0

    for num in arr:
        prefix_sum += num

        # How many times have we seen (prefix_sum - x)?
        complement = prefix_sum - x
        count += count_map[complement]

        # Add current prefix sum to map
        count_map[prefix_sum] += 1

    return count


def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0

    n = int(input_data[idx])
    x = int(input_data[idx + 1])
    idx += 2

    arr = [int(input_data[idx + i]) for i in range(n)]

    print(solve_optimal(n, x, arr))


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    long long x;
    cin >> n >> x;

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    // Hash map to count prefix sum frequencies
    map<long long, long long> count_map;
    count_map[0] = 1;  // Empty prefix (crucial!)

    long long prefix_sum = 0;
    long long count = 0;

    for (int i = 0; i < n; i++) {
        prefix_sum += arr[i];

        // How many times have we seen (prefix_sum - x)?
        long long complement = prefix_sum - x;
        if (count_map.count(complement)) {
            count += count_map[complement];
        }

        // Add current prefix sum to map
        count_map[prefix_sum]++;
    }

    cout << count << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array, O(1) hash map operations |
| Space | O(n) | Hash map stores at most n+1 prefix sums |

---

## Common Mistakes

### Mistake 1: Forgetting the Initial Prefix Sum of 0

```python
# WRONG
count_map = {}  # Missing initial {0: 1}
```

**Problem:** If a subarray starting from index 0 has sum equal to x, we need to find complement = x - x = 0 in the map. Without initializing {0: 1}, we miss all subarrays that start from index 0.

**Fix:** Always initialize with `count_map[0] = 1`.

### Mistake 2: Adding to Map Before Checking

```python
# WRONG - may count current element against itself
for num in arr:
    prefix_sum += num
    count_map[prefix_sum] += 1      # Adding BEFORE checking
    count += count_map[prefix_sum - x]  # May incorrectly match itself
```

**Problem:** This can cause issues when prefix_sum - x equals prefix_sum (when x = 0), though this problem has positive x.

**Fix:** Always check for complement BEFORE adding current prefix to the map.

### Mistake 3: Integer Overflow

```python
# Potential issue with some languages
prefix_sum = 0  # May overflow if elements are large
```

**Problem:** With n up to 2*10^5 and elements up to 10^9, the prefix sum can reach 2*10^14, which exceeds 32-bit integer range.

**Fix:** Use `long long` in C++ or let Python handle large integers naturally.

### Mistake 4: Using Wrong Index in Subarray Identification

When debugging, remember that if complement = prefix_sum - x was found at position i, the subarray runs from position (i+1) to current position j.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element equals x | `n=1, x=5, arr=[5]` | 1 | Single element is valid subarray |
| No valid subarray | `n=3, x=100, arr=[1,2,3]` | 0 | No subarray sums to 100 |
| Entire array equals x | `n=3, x=6, arr=[1,2,3]` | 1 | Whole array is one valid subarray |
| Multiple overlapping | `n=4, x=3, arr=[1,1,1,1]` | 2 | [1,1,1] at positions 0-2 and 1-3 |
| Large values | `n=2, x=10^9, arr=[10^9, 10^9]` | 2 | Handle large numbers |
| All same elements | `n=5, x=2, arr=[1,1,1,1,1]` | 4 | [1,1] appears 4 times |

---

## When to Use This Pattern

### Use This Approach When:
- Counting subarrays with a specific sum
- Need O(n) time complexity for subarray sum problems
- Subarrays are contiguous (not subsequences)
- Looking for exact sum matches

### Don't Use When:
- Elements can be negative AND you need to track ranges (use different technique)
- Looking for subsequences (not contiguous subarrays)
- Need to return the actual subarrays (not just count)
- Problem requires sliding window (when all elements are positive and you want exact count, both work)

### Pattern Recognition Checklist:
- [ ] Counting contiguous subarrays with target sum? -> **Prefix Sum + Hash Map**
- [ ] Array has only positive elements? -> **Sliding Window also works**
- [ ] Need sum in a range [lo, hi]? -> **May need two-pass approach**
- [ ] Need to handle negative numbers? -> **See Subarray Sums II**

---

## Alternative: Two-Pointer / Sliding Window

Since all elements are **positive**, we can also use a sliding window approach:

```python
def solve_sliding_window(n, x, arr):
    """
    Alternative using sliding window (works because all elements are positive).

    Time: O(n)
    Space: O(1)
    """
    left = 0
    current_sum = 0
    count = 0

    for right in range(n):
        current_sum += arr[right]

        # Shrink window while sum > x
        while current_sum > x and left <= right:
            current_sum -= arr[left]
            left += 1

        # Check if current window has sum = x
        if current_sum == x:
            count += 1

    return count
```

**Note:** This approach only works because all elements are positive. With negative numbers, you must use the prefix sum + hash map approach (see Subarray Sums II).

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Basic prefix sum concept |
| [Two Sum](https://leetcode.com/problems/two-sum/) | Hash map for complement lookup |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Subarray Sums II (CSES 1661)](https://cses.fi/problemset/task/1661) | Allows negative numbers |
| [Subarray Sum Equals K (LeetCode 560)](https://leetcode.com/problems/subarray-sum-equals-k/) | Same technique, different platform |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Subarray Divisibility (CSES 1662)](https://cses.fi/problemset/task/1662) | Counting based on modular arithmetic |
| [Maximum Subarray Sum (CSES 1643)](https://cses.fi/problemset/task/1643) | Finding max sum instead of counting |
| [Count of Range Sum (LeetCode 327)](https://leetcode.com/problems/count-of-range-sum/) | Sum in a range, more complex |

---

## Key Takeaways

1. **The Core Idea:** Transform "find subarray with sum x" into "find previous prefix sum that differs by x"
2. **Time Optimization:** From O(n^2) brute force to O(n) using hash map for O(1) complement lookups
3. **Space Trade-off:** Use O(n) space to store prefix sum frequencies
4. **Critical Base Case:** Always initialize hash map with {0: 1} for subarrays starting at index 0
5. **Pattern:** This is the "prefix sum + complement counting" pattern, foundational for many array problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why we initialize the hash map with {0: 1}
- [ ] Draw the prefix sum array for any given input
- [ ] Trace through the algorithm step by step
- [ ] Implement both Python and C++ solutions from memory
- [ ] Explain the difference between this problem and Subarray Sums II

---

## Additional Resources

- [CP-Algorithms: Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sums.html)
- [CSES Subarray Sums I](https://cses.fi/problemset/task/1660) - Two pointers on positive values
- [LeetCode - Subarray Sum Pattern](https://leetcode.com/tag/prefix-sum/)
