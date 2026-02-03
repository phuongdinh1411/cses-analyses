---
layout: simple
title: "Subarrays with K Distinct Values - Sliding Window"
permalink: /problem_soulutions/sliding_window/subarray_with_k_distinct_analysis
difficulty: Medium
tags: [sliding-window, two-pointers, hash-map, counting]
---

# Subarrays with K Distinct Values

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window / Two Pointers |
| **Time Limit** | 1 second |
| **Key Technique** | atMost(k) - atMost(k-1) Decomposition |
| **Similar To** | [LeetCode 992](https://leetcode.com/problems/subarrays-with-k-different-integers/) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the atMost(k) - atMost(k-1) technique to count exact occurrences
- [ ] Implement sliding window with hash map for distinct element tracking
- [ ] Recognize when "exactly k" problems need decomposition into "at most k"
- [ ] Count subarrays efficiently using the right pointer contribution formula

---

## Problem Statement

**Problem:** Given an array of integers, count the number of contiguous subarrays that contain exactly k distinct values.

**Input:**
- Line 1: n (array size) and k (required distinct count)
- Line 2: n space-separated integers

**Output:**
- Single integer: count of subarrays with exactly k distinct values

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= k <= n
- 1 <= arr[i] <= 10^9

### Example

```
Input:
5 2
1 2 1 2 3

Output:
7
```

**Explanation:** The 7 subarrays with exactly 2 distinct values are:
- [1,2] (indices 0-1)
- [2,1] (indices 1-2)
- [1,2] (indices 2-3)
- [2,3] (indices 3-4)
- [1,2,1] (indices 0-2)
- [2,1,2] (indices 1-3)
- [1,2,1,2] (indices 0-3)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why can't we directly count subarrays with exactly k distinct values using a simple sliding window?

The problem is that "exactly k" doesn't have a monotonic property. When you expand a window, you might go from k-1 to k distinct (good) or from k to k+1 (bad). There's no clean way to know when to shrink.

### The Breakthrough Insight

**Exactly(k) = AtMost(k) - AtMost(k-1)**

This decomposition works because:
- AtMost(k) counts subarrays with 1, 2, ..., or k distinct values
- AtMost(k-1) counts subarrays with 1, 2, ..., or k-1 distinct values
- The difference gives us subarrays with EXACTLY k distinct values

### Why AtMost(k) Is Easier

"At most k" has a beautiful monotonic property:
- If a window has <= k distinct values, ALL its subarrays also have <= k distinct
- This means we can count all valid subarrays ending at each position

---

## Solution 1: Brute Force

### Idea

Check every possible subarray and count distinct elements using a set.

### Code

```python
def count_subarrays_brute(arr, k):
    """
    Brute force: check all subarrays.
    Time: O(n^2), Space: O(n)
    """
    n = len(arr)
    count = 0
    for i in range(n):
        distinct = set()
        for j in range(i, n):
            distinct.add(arr[j])
            if len(distinct) == k:
                count += 1
            elif len(distinct) > k:
                break  # Optimization: no point continuing
    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Nested loops, early break helps average case |
| Space | O(n) | Set can hold up to n distinct values |

---

## Solution 2: Optimal - AtMost Decomposition

### Key Insight

> **The Trick:** Convert "exactly k" into "at most k" minus "at most k-1"

### The AtMost Function

For a window ending at index `right` with `left` as the leftmost valid position:
- Number of valid subarrays ending at `right` = `right - left + 1`
- This counts: [left..right], [left+1..right], ..., [right..right]

### Algorithm

1. Implement `atMost(k)` using sliding window
2. Return `atMost(k) - atMost(k-1)`

### Dry Run Example

Input: `arr = [1, 2, 1, 2, 3], k = 2`

**Computing atMost(2):**

```
right=0: arr[0]=1, window=[1], distinct=1, count += 1
         Subarrays: [1]

right=1: arr[1]=2, window=[1,2], distinct=2, count += 2
         Subarrays: [2], [1,2]

right=2: arr[2]=1, window=[1,2,1], distinct=2, count += 3
         Subarrays: [1], [2,1], [1,2,1]

right=3: arr[3]=2, window=[1,2,1,2], distinct=2, count += 4
         Subarrays: [2], [1,2], [2,1,2], [1,2,1,2]

right=4: arr[4]=3, window=[1,2,1,2,3], distinct=3 > k!
         Shrink: remove arr[0]=1, window=[2,1,2,3], distinct=3
         Shrink: remove arr[1]=2, window=[1,2,3], distinct=3
         Shrink: remove arr[2]=1, window=[2,3], distinct=2, count += 2
         Subarrays: [3], [2,3]

atMost(2) = 1 + 2 + 3 + 4 + 2 = 12
```

**Computing atMost(1):**

```
right=0: count += 1   (window [1])
right=1: distinct=2, shrink to [2], count += 1
right=2: distinct=2, shrink to [1], count += 1
right=3: distinct=2, shrink to [2], count += 1
right=4: distinct=2, shrink to [3], count += 1

atMost(1) = 5
```

**Result:** Exactly(2) = atMost(2) - atMost(1) = 12 - 5 = **7**

### Visual Diagram

```
Array: [1, 2, 1, 2, 3]    k = 2

AtMost(2) subarrays:
  [1]  [2]  [1]  [2]  [3]     <- length 1: 5
  [1,2]  [2,1]  [1,2]  [2,3]  <- length 2: 4
  [1,2,1]  [2,1,2]            <- length 3: 2
  [1,2,1,2]                   <- length 4: 1
  Total: 12

AtMost(1) subarrays:
  [1]  [2]  [1]  [2]  [3]     <- length 1: 5
  Total: 5

Exactly(2) = 12 - 5 = 7
```

### Code

**Python:**

```python
def subarrays_with_k_distinct(arr, k):
    """
    Count subarrays with exactly k distinct values.
    Time: O(n), Space: O(k)
    """
    def at_most(k):
        if k < 0:
            return 0
        count = {}
        left = 0
        result = 0

        for right in range(len(arr)):
            # Add right element
            count[arr[right]] = count.get(arr[right], 0) + 1

            # Shrink window if too many distinct
            while len(count) > k:
                count[arr[left]] -= 1
                if count[arr[left]] == 0:
                    del count[arr[left]]
                left += 1

            # Count all valid subarrays ending at right
            result += right - left + 1

        return result

    return at_most(k) - at_most(k - 1)


# Alternative: Find longest subarray with exactly k distinct
def longest_with_k_distinct(arr, k):
    """
    Find length of longest subarray with at most k distinct.
    Time: O(n), Space: O(k)
    """
    count = {}
    left = 0
    max_len = 0

    for right in range(len(arr)):
        count[arr[right]] = count.get(arr[right], 0) + 1

        while len(count) > k:
            count[arr[left]] -= 1
            if count[arr[left]] == 0:
                del count[arr[left]]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
```

**C++:**

```cpp
#include <bits/stdc++.h>
using namespace std;

long long atMost(vector<int>& arr, int k) {
    if (k < 0) return 0;

    unordered_map<int, int> count;
    int left = 0;
    long long result = 0;

    for (int right = 0; right < arr.size(); right++) {
        count[arr[right]]++;

        while (count.size() > k) {
            count[arr[left]]--;
            if (count[arr[left]] == 0) {
                count.erase(arr[left]);
            }
            left++;
        }

        result += right - left + 1;
    }

    return result;
}

long long subarraysWithKDistinct(vector<int>& arr, int k) {
    return atMost(arr, k) - atMost(arr, k - 1);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, k;
    cin >> n >> k;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    cout << subarraysWithKDistinct(arr, k) << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Two passes through array, each element visited at most twice per pass |
| Space | O(k) | Hash map stores at most k+1 distinct elements |

---

## Common Mistakes

### Mistake 1: Forgetting to Handle k-1 Edge Case

```python
# WRONG - crashes when k = 0
def at_most(k):
    # ... code assumes k >= 0

# CORRECT
def at_most(k):
    if k < 0:
        return 0
    # ... rest of code
```

**Problem:** When k=1, we call atMost(0), which should return 0.
**Fix:** Add base case check at the start.

### Mistake 2: Counting Logic Error

```python
# WRONG - only counts when exactly k distinct
if len(count) == k:
    result += right - left + 1

# CORRECT - counts when at most k distinct
# No condition needed; the while loop ensures len(count) <= k
result += right - left + 1
```

**Problem:** atMost must count ALL valid windows, not just those with exactly k.

### Mistake 3: Not Deleting Zero-Count Entries

```python
# WRONG - map size stays inflated
count[arr[left]] -= 1
left += 1

# CORRECT - remove entry when count reaches 0
count[arr[left]] -= 1
if count[arr[left]] == 0:
    del count[arr[left]]
left += 1
```

**Problem:** Hash map size becomes unreliable if zero-count entries remain.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| k = 1 | `[1,1,1], k=1` | 6 | All subarrays valid: 3+2+1=6 |
| k = n | `[1,2,3], k=3` | 1 | Only full array has all 3 |
| All same | `[5,5,5], k=2` | 0 | Only 1 distinct exists |
| k > distinct count | `[1,2], k=3` | 0 | Impossible |
| Single element | `[7], k=1` | 1 | Only [7] |

---

## When to Use This Pattern

### Use AtMost Decomposition When:
- Counting subarrays with **exactly** k of something
- Direct "exactly k" window doesn't have monotonic property
- The "at most" version has clean shrinking condition

### Pattern Recognition Checklist:
- [ ] Problem asks for "exactly k distinct"? -> **atMost(k) - atMost(k-1)**
- [ ] Problem asks for "at most k distinct"? -> **Single sliding window**
- [ ] Problem asks for "at least k distinct"? -> **Total - atMost(k-1)**

### Common Applications:
- Subarrays with exactly k distinct elements
- Substrings with exactly k unique characters
- Windows with exactly k types/categories

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [LeetCode 3: Longest Substring Without Repeating](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Basic sliding window for distinct elements |
| [LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | Sliding window with hash map |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [LeetCode 992: Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) | Same problem |
| [LeetCode 340: Longest Substring with At Most K Distinct](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) | Find max length instead of count |
| [LeetCode 904: Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | At most 2 distinct (k=2) |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [LeetCode 1248: Count Nice Subarrays](https://leetcode.com/problems/count-number-of-nice-subarrays/) | Exactly k odd numbers |
| [LeetCode 930: Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | Exactly k ones |
| [CSES: Playlist](https://cses.fi/problemset/task/1141) | Longest unique subsequence |

---

## Key Takeaways

1. **The Core Idea:** Transform "exactly k" into subtraction of two "at most" counts
2. **Why It Works:** "At most k" has monotonic property; "exactly k" doesn't
3. **Counting Formula:** For window [left, right], count = right - left + 1
4. **Space Trade-off:** O(k) space for O(n) time vs O(n^2) brute force

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why exactly(k) = atMost(k) - atMost(k-1)
- [ ] Implement atMost function from scratch
- [ ] Handle edge case when k = 1 (calls atMost(0))
- [ ] Apply this pattern to "exactly k odd numbers" variant
- [ ] Solve in under 15 minutes without reference
