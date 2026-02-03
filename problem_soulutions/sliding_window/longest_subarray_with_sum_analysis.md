---
layout: simple
title: "Longest Subarray with Sum - Sliding Window / Hash Map"
permalink: /problem_soulutions/sliding_window/longest_subarray_with_sum_analysis
difficulty: Medium
tags: [sliding-window, two-pointers, prefix-sum, hash-map]
---

# Longest Subarray with Sum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window / Prefix Sum |
| **Time Limit** | 1 second |
| **Key Technique** | Two Pointers (positive arrays) / Hash Map (general) |
| **CSES Link** | [Subarray Sums I](https://cses.fi/problemset/task/1660) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply sliding window technique for variable-size window problems
- [ ] Use prefix sums with hash maps for subarray sum problems
- [ ] Choose between sliding window and hash map based on constraints
- [ ] Handle edge cases involving empty subarrays and zero sums

---

## Problem Statement

**Problem:** Given an array of integers and a target sum, find the length of the longest contiguous subarray that sums to the target value.

**Input:**
- Line 1: n (array size) and x (target sum)
- Line 2: n space-separated integers

**Output:**
- Length of longest subarray with sum equal to target (0 if none exists)

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= x <= 10^9
- 1 <= a[i] <= 10^9 (for sliding window variant)
- -10^9 <= a[i] <= 10^9 (for hash map variant)

### Example

```
Input:
8 8
3 1 4 1 5 9 2 6

Output:
4
```

**Explanation:** The subarray [3, 1, 4] has sum 8 and length 3. The subarray [1, 4, 1, 2] = wait, let's check: we need sum = 8. Subarray [3, 1, 4] = 8 with length 3. Subarray [1, 5, 2] is not contiguous. The longest valid subarray is [3, 1, 4] with length 3.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When do we expand the window, and when do we shrink it?

For **positive integers only**: Use sliding window. When sum exceeds target, shrink from left. When sum equals target, record the length.

For **arrays with negative numbers**: Sliding window does not work because removing elements might increase or decrease the sum unpredictably. Use prefix sum + hash map instead.

### Breaking Down the Problem

1. **What are we looking for?** Maximum length subarray with exact sum
2. **What information do we have?** Array elements and target sum
3. **What is the relationship?** Subarray sum = prefix[j] - prefix[i-1]

### Analogies

Think of this like a worm crawling along a number line. The worm's body (window) expands and contracts to maintain a specific "weight" (sum). For positive-only arrays, the worm knows that stretching always adds weight and shrinking always reduces it.

---

## Solution 1: Sliding Window (Positive Arrays Only)

### Key Insight

> **The Trick:** With positive numbers, window sum is monotonic - expanding increases sum, shrinking decreases sum.

### Algorithm

1. Initialize left pointer at 0, current_sum at 0, max_length at 0
2. Expand right pointer through the array
3. Add arr[right] to current_sum
4. While current_sum > target, shrink by moving left pointer right
5. If current_sum == target, update max_length
6. Return max_length

### Dry Run Example

Let's trace through with input `arr = [2, 1, 5, 1, 3, 2], target = 8`:

```
Initial state:
  left = 0, current_sum = 0, max_length = 0

Step 1: right = 0, arr[0] = 2
  current_sum = 0 + 2 = 2
  2 < 8, no shrink needed
  2 != 8, don't update max_length
  Window: [2], sum = 2

Step 2: right = 1, arr[1] = 1
  current_sum = 2 + 1 = 3
  3 < 8, no shrink needed
  Window: [2, 1], sum = 3

Step 3: right = 2, arr[2] = 5
  current_sum = 3 + 5 = 8
  8 == 8, update max_length = 3
  Window: [2, 1, 5], sum = 8

Step 4: right = 3, arr[3] = 1
  current_sum = 8 + 1 = 9
  9 > 8, shrink: subtract arr[0]=2, left=1, sum=7
  7 < 8, stop shrinking
  Window: [1, 5, 1], sum = 7

Step 5: right = 4, arr[4] = 3
  current_sum = 7 + 3 = 10
  10 > 8, shrink: subtract arr[1]=1, left=2, sum=9
  9 > 8, shrink: subtract arr[2]=5, left=3, sum=4
  Window: [1, 3], sum = 4

Step 6: right = 5, arr[5] = 2
  current_sum = 4 + 2 = 6
  Window: [1, 3, 2], sum = 6

Final: max_length = 3 (subarray [2, 1, 5])
```

### Visual Diagram

```
Array: [2, 1, 5, 1, 3, 2]  Target: 8

  left=0               right=2
    |                    |
    v                    v
   [2,  1,  5] 1,  3,  2
    └────────┘
    sum = 8, length = 3
```

### Code

**Python:**
```python
def longest_subarray_positive(arr, target):
    """
    Sliding window for positive-only arrays.
    Time: O(n), Space: O(1)
    """
    n = len(arr)
    left = 0
    current_sum = 0
    max_length = 0

    for right in range(n):
        current_sum += arr[right]

        # Shrink window while sum exceeds target
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1

        # Check if we found target sum
        if current_sum == target:
            max_length = max(max_length, right - left + 1)

    return max_length
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

int longestSubarrayPositive(vector<int>& arr, long long target) {
    int n = arr.size();
    int left = 0;
    long long currentSum = 0;
    int maxLength = 0;

    for (int right = 0; right < n; right++) {
        currentSum += arr[right];

        // Shrink window while sum exceeds target
        while (currentSum > target && left <= right) {
            currentSum -= arr[left];
            left++;
        }

        // Check if we found target sum
        if (currentSum == target) {
            maxLength = max(maxLength, right - left + 1);
        }
    }

    return maxLength;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element visited at most twice (once by right, once by left) |
| Space | O(1) | Only tracking pointers and sum |

---

## Solution 2: Hash Map (General - Works with Negatives)

### Key Insight

> **The Trick:** If prefix[j] - prefix[i] = target, then subarray (i, j] has sum = target. Store first occurrence of each prefix sum to maximize length.

### Algorithm

1. Initialize hash map with {0: -1} (empty prefix at index -1)
2. Compute running prefix sum
3. For each index, check if (prefix_sum - target) exists in map
4. If found, compute length and update max
5. Store first occurrence of each prefix sum

### Dry Run Example

Let's trace through with `arr = [-2, 1, -3, 4, -1, 2], target = 3`:

```
Initial: prefix_map = {0: -1}, prefix_sum = 0, max_length = 0

i=0: prefix_sum = -2
  Look for -2 - 3 = -5 (not found)
  Store: {0: -1, -2: 0}

i=1: prefix_sum = -1
  Look for -1 - 3 = -4 (not found)
  Store: {0: -1, -2: 0, -1: 1}

i=2: prefix_sum = -4
  Look for -4 - 3 = -7 (not found)
  Store: {0: -1, -2: 0, -1: 1, -4: 2}

i=3: prefix_sum = 0
  Look for 0 - 3 = -3 (not found)
  0 already in map, don't overwrite (keep first occurrence)

i=4: prefix_sum = -1
  Look for -1 - 3 = -4 (found at index 2!)
  length = 4 - 2 = 2, max_length = 2
  -1 already in map, don't overwrite

i=5: prefix_sum = 1
  Look for 1 - 3 = -2 (found at index 0!)
  length = 5 - 0 = 5, max_length = 5
  Store: {0: -1, -2: 0, -1: 1, -4: 2, 1: 5}

Result: max_length = 5 (subarray [1, -3, 4, -1, 2])
```

### Code

**Python:**
```python
def longest_subarray_general(arr, target):
    """
    Hash map approach for arrays with any integers.
    Time: O(n), Space: O(n)
    """
    prefix_map = {0: -1}  # Handle subarrays starting at index 0
    prefix_sum = 0
    max_length = 0

    for i, num in enumerate(arr):
        prefix_sum += num

        # Check if (prefix_sum - target) exists
        if prefix_sum - target in prefix_map:
            length = i - prefix_map[prefix_sum - target]
            max_length = max(max_length, length)

        # Store first occurrence only (for maximum length)
        if prefix_sum not in prefix_map:
            prefix_map[prefix_sum] = i

    return max_length
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

int longestSubarrayGeneral(vector<int>& arr, long long target) {
    unordered_map<long long, int> prefixMap;
    prefixMap[0] = -1;  // Handle subarrays starting at index 0

    long long prefixSum = 0;
    int maxLength = 0;

    for (int i = 0; i < arr.size(); i++) {
        prefixSum += arr[i];

        // Check if (prefixSum - target) exists
        if (prefixMap.count(prefixSum - target)) {
            int length = i - prefixMap[prefixSum - target];
            maxLength = max(maxLength, length);
        }

        // Store first occurrence only
        if (!prefixMap.count(prefixSum)) {
            prefixMap[prefixSum] = i;
        }
    }

    return maxLength;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array |
| Space | O(n) | Hash map stores up to n prefix sums |

---

## Common Mistakes

### Mistake 1: Using Sliding Window with Negative Numbers

```python
# WRONG - Does not work with negative numbers!
def wrong_approach(arr, target):
    left = 0
    current_sum = 0
    for right in range(len(arr)):
        current_sum += arr[right]
        while current_sum > target:  # May never trigger or wrong shrink
            current_sum -= arr[left]
            left += 1
```

**Problem:** Negative numbers break monotonicity. Shrinking might increase the sum!
**Fix:** Use hash map approach for arrays with negative numbers.

### Mistake 2: Overwriting Prefix Sum Index

```python
# WRONG - Overwrites first occurrence
prefix_map[prefix_sum] = i  # Always updates

# CORRECT - Keep first occurrence for maximum length
if prefix_sum not in prefix_map:
    prefix_map[prefix_sum] = i
```

**Problem:** Overwriting gives shorter subarrays.
**Fix:** Only store the first occurrence of each prefix sum.

### Mistake 3: Forgetting Base Case {0: -1}

```python
# WRONG - Missing base case
prefix_map = {}  # Misses subarrays starting at index 0

# CORRECT
prefix_map = {0: -1}  # Handles arr[0:j] subarrays
```

**Problem:** Cannot find subarrays that start at index 0.
**Fix:** Initialize with {0: -1} to handle empty prefix.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| No solution | `[1,2,3], target=10` | 0 | No subarray sums to 10 |
| Single element | `[5], target=5` | 1 | Element itself is the answer |
| Entire array | `[1,2,3], target=6` | 3 | Whole array is valid |
| Target = 0 | `[1,-1,2,-2], target=0` | 4 | Sum of all elements is 0 |
| All same values | `[2,2,2,2], target=4` | 2 | Multiple valid windows |
| Large values | `[10^9, 10^9], target=2*10^9` | 2 | Use long long in C++ |

---

## When to Use This Pattern

### Use Sliding Window When:
- All array elements are positive (or all non-negative)
- You need O(1) space complexity
- Finding contiguous subarrays with sum constraints

### Use Hash Map When:
- Array contains negative numbers
- Need to find exact sum (not "at most" or "at least")
- Willing to trade O(n) space for simpler logic

### Pattern Recognition Checklist:
- [ ] Contiguous subarray problem? Consider sliding window or prefix sum
- [ ] All positive elements? Sliding window works
- [ ] Contains negatives? Must use hash map
- [ ] Finding maximum length? Store first occurrence of prefix sum
- [ ] Finding minimum length? Store last occurrence of prefix sum

---

## Related Problems

### CSES Problems
| Problem | Link | Relationship |
|---------|------|--------------|
| Subarray Sums I | [CSES 1660](https://cses.fi/problemset/task/1660) | Count subarrays (positive only) |
| Subarray Sums II | [CSES 1661](https://cses.fi/problemset/task/1661) | Count subarrays (with negatives) |
| Subarray Divisibility | [CSES 1662](https://cses.fi/problemset/task/1662) | Modular arithmetic variant |
| Maximum Subarray Sum | [CSES 1643](https://cses.fi/problemset/task/1643) | Kadane's algorithm |

### LeetCode Problems
| Problem | Difficulty | Key Difference |
|---------|------------|----------------|
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Count instead of max length |
| [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Minimum length, sum >= target |
| [Maximum Size Subarray Sum Equals k](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/) | Medium | Same problem |
| [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | Medium | Binary array variant |

---

## Key Takeaways

1. **Choose Your Weapon:** Sliding window for positive arrays, hash map for general arrays
2. **Monotonicity Matters:** Sliding window requires predictable sum behavior when expanding/shrinking
3. **First Occurrence:** For maximum length, store first occurrence of each prefix sum
4. **Base Case:** Always initialize with {0: -1} to handle subarrays starting at index 0
5. **Overflow:** Use long long in C++ for large sums

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement sliding window solution for positive arrays without looking
- [ ] Implement hash map solution for general arrays without looking
- [ ] Explain why sliding window fails with negative numbers
- [ ] Identify which approach to use based on constraints
- [ ] Handle all edge cases correctly
