---
layout: simple
title: "Playlist - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/playlist_analysis
difficulty: Easy
tags: [sliding-window, two-pointers, hash-set]
prerequisites: []
---

# Playlist

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Sliding Window with Hash Set |
| **CSES Link** | [Playlist](https://cses.fi/problemset/task/1141) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Identify problems that require the sliding window pattern
- [ ] Use a hash set to track unique elements in a window
- [ ] Implement window shrinking when duplicates are encountered
- [ ] Achieve O(n) time complexity for subarray problems

---

## Problem Statement

**Problem:** Find the longest contiguous sequence of songs where no song genre is repeated.

**Input:**
- Line 1: Integer n (number of songs)
- Line 2: n integers representing song genres

**Output:**
- The length of the longest subarray with all distinct elements

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= a[i] <= 10^9

### Example

```
Input:
8
1 2 1 3 2 7 4 5

Output:
5
```

**Explanation:** The longest subarray with distinct elements is [2, 7, 4, 5] or [3, 2, 7, 4, 5] with length 5. Starting from index 3 (value 3) to index 7 (value 5), all elements are unique.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently find the longest subarray where all elements are unique?

This is a classic sliding window problem. We maintain a window of consecutive elements and expand it when possible, shrinking it only when we encounter a duplicate.

### Breaking Down the Problem

1. **What are we looking for?** The maximum length of a contiguous subarray with all distinct elements.
2. **What information do we have?** An array of integers (song genres).
3. **What's the relationship between input and output?** We need to find the longest "valid" window where validity means no repeated elements.

### Analogies

Think of this like a caterpillar crawling along the array. The caterpillar's body represents our current window. When we see a new unique song, we extend the front. When we see a duplicate, we shrink from the back until the duplicate is removed.

---

## Solution 1: Brute Force

### Idea

Check every possible subarray and verify if all elements are distinct.

### Algorithm

1. For each starting position i
2. For each ending position j >= i
3. Check if subarray [i, j] has all distinct elements
4. Track the maximum length found

### Code

```python
def solve_brute_force(n, arr):
    """
    Brute force solution - check all subarrays.

    Time: O(n^3) - O(n^2) subarrays, O(n) to check each
    Space: O(n) - for the set
    """
    max_length = 0

    for i in range(n):
        for j in range(i, n):
            subarray = arr[i:j+1]
            if len(subarray) == len(set(subarray)):
                max_length = max(max_length, len(subarray))

    return max_length
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | O(n^2) subarrays, O(n) to convert to set |
| Space | O(n) | Set storage for checking uniqueness |

### Why This Works (But Is Slow)

We exhaustively check every subarray, guaranteeing we find the longest valid one. However, with n up to 2 x 10^5, O(n^3) is far too slow.

---

## Solution 2: Optimal - Sliding Window

### Key Insight

> **The Trick:** Use two pointers to maintain a window of unique elements. When we encounter a duplicate, shrink from the left until the duplicate is removed.

### Algorithm

1. Initialize left pointer at 0, maintain a set of elements in current window
2. Expand right pointer one element at a time
3. If the new element is already in the set, remove elements from the left until it's not
4. Add the new element to the set
5. Update max_length = max(max_length, right - left + 1)

### Dry Run Example

Let's trace through with input `n = 8, arr = [1, 2, 1, 3, 2, 7, 4, 5]`:

```
Initial: left = 0, seen = {}, max_length = 0

Step 1: right = 0, arr[0] = 1
  1 not in seen
  Add 1: seen = {1}
  max_length = max(0, 0-0+1) = 1

Step 2: right = 1, arr[1] = 2
  2 not in seen
  Add 2: seen = {1, 2}
  max_length = max(1, 1-0+1) = 2

Step 3: right = 2, arr[2] = 1
  1 IS in seen!
  Remove arr[0]=1: seen = {2}, left = 1
  Now 1 not in seen
  Add 1: seen = {2, 1}
  max_length = max(2, 2-1+1) = 2

Step 4: right = 3, arr[3] = 3
  3 not in seen
  Add 3: seen = {2, 1, 3}
  max_length = max(2, 3-1+1) = 3

Step 5: right = 4, arr[4] = 2
  2 IS in seen!
  Remove arr[1]=2: seen = {1, 3}, left = 2
  Now 2 not in seen
  Add 2: seen = {1, 3, 2}
  max_length = max(3, 4-2+1) = 3

Step 6: right = 5, arr[5] = 7
  7 not in seen
  Add 7: seen = {1, 3, 2, 7}
  max_length = max(3, 5-2+1) = 4

Step 7: right = 6, arr[6] = 4
  4 not in seen
  Add 4: seen = {1, 3, 2, 7, 4}
  max_length = max(4, 6-2+1) = 5

Step 8: right = 7, arr[7] = 5
  5 not in seen
  Add 5: seen = {1, 3, 2, 7, 4, 5}
  max_length = max(5, 7-2+1) = 6

Final answer: 5
```

### Visual Diagram

```
Array: [1, 2, 1, 3, 2, 7, 4, 5]
Index:  0  1  2  3  4  5  6  7

Step-by-step window movement:
[1]                          len=1  seen={1}
[1, 2]                       len=2  seen={1,2}
   [2, 1]                    len=2  seen={2,1}     (removed 1, added 1)
   [2, 1, 3]                 len=3  seen={2,1,3}
      [1, 3, 2]              len=3  seen={1,3,2}   (removed 2, added 2)
      [1, 3, 2, 7]           len=4  seen={1,3,2,7}
      [1, 3, 2, 7, 4]        len=5  seen={1,3,2,7,4}
      [1, 3, 2, 7, 4, 5]     len=6  seen={1,3,2,7,4,5}
```

### Code

#### Python

```python
def solve(n, arr):
    """
    Optimal solution using sliding window with hash set.

    Time: O(n) - each element added and removed at most once
    Space: O(n) - hash set storage
    """
    left = 0
    max_length = 0
    seen = set()

    for right in range(n):
        # Shrink window until arr[right] is not a duplicate
        while arr[right] in seen:
            seen.remove(arr[left])
            left += 1

        # Add current element to window
        seen.add(arr[right])

        # Update maximum length
        max_length = max(max_length, right - left + 1)

    return max_length


def main():
    n = int(input())
    arr = list(map(int, input().split()))
    print(solve(n, arr))


if __name__ == "__main__":
    main()
```

#### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    int left = 0;
    int max_length = 0;
    unordered_set<int> seen;

    for (int right = 0; right < n; right++) {
        // Shrink window until arr[right] is not a duplicate
        while (seen.count(arr[right])) {
            seen.erase(arr[left]);
            left++;
        }

        // Add current element to window
        seen.insert(arr[right]);

        // Update maximum length
        max_length = max(max_length, right - left + 1);
    }

    cout << max_length << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element is added and removed from the set at most once |
| Space | O(n) | Hash set can store up to n elements in worst case |

---

## Common Mistakes

### Mistake 1: Not Shrinking Window Properly

```python
# WRONG - only removes one element
if arr[right] in seen:
    seen.remove(arr[left])
    left += 1

# CORRECT - keeps removing until duplicate is gone
while arr[right] in seen:
    seen.remove(arr[left])
    left += 1
```

**Problem:** The duplicate might not be at position `left`. We need to keep shrinking until the duplicate element is removed.

**Fix:** Use a `while` loop, not an `if` statement.

### Mistake 2: Off-by-One in Window Length

```python
# WRONG
max_length = max(max_length, right - left)

# CORRECT
max_length = max(max_length, right - left + 1)
```

**Problem:** Window length is inclusive on both ends, so it's `right - left + 1`, not `right - left`.

**Fix:** Add 1 to the difference.

### Mistake 3: Adding Before Checking

```python
# WRONG - add before removing duplicates
seen.add(arr[right])
while arr[right] in seen:  # Always true!
    ...

# CORRECT - remove duplicates first, then add
while arr[right] in seen:
    seen.remove(arr[left])
    left += 1
seen.add(arr[right])
```

**Problem:** If we add the element first, it will always be in the set.

**Fix:** Check and shrink the window first, then add the new element.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, arr=[5]` | 1 | One element is always unique |
| All same | `n=5, arr=[1,1,1,1,1]` | 1 | Can only have one element at a time |
| All distinct | `n=5, arr=[1,2,3,4,5]` | 5 | Entire array is valid |
| Duplicate at end | `n=4, arr=[1,2,3,1]` | 3 | [1,2,3] or [2,3,1] |
| Large values | `n=2, arr=[10^9, 1]` | 2 | Handle large integers |

---

## When to Use This Pattern

### Use This Approach When:
- Finding the longest/shortest subarray with a property
- The property involves uniqueness or counting distinct elements
- You can determine validity by adding/removing one element
- You need O(n) time complexity

### Don't Use When:
- You need to find ALL valid subarrays (different counting technique)
- The validity condition can't be incrementally updated
- Non-contiguous subsequences are needed

### Pattern Recognition Checklist:
- [ ] Looking for longest subarray with unique elements? --> **Sliding window + hash set**
- [ ] Looking for longest substring without repeating characters? --> **Same pattern**
- [ ] Looking for subarray with at most K distinct elements? --> **Sliding window + hash map with counts**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Basic hash set usage |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | String version of same problem |
| [Distinct Values Queries](https://cses.fi/problemset/task/1734) | Count distinct values in ranges |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) | Allows up to K repeats |
| [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) | Exact K distinct elements |
| [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | At most 2 distinct values |

---

## Key Takeaways

1. **The Core Idea:** Maintain a window of unique elements using a hash set; shrink from the left when duplicates are found.
2. **Time Optimization:** From O(n^3) brute force to O(n) by avoiding redundant checks - each element is added and removed at most once.
3. **Space Trade-off:** We use O(n) space for the hash set to achieve O(n) time.
4. **Pattern:** This is the classic "longest substring/subarray without repeating elements" pattern.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why each element is processed at most twice (added once, removed once)
- [ ] Identify the sliding window pattern in new problems
- [ ] Implement in your preferred language in under 10 minutes
- [ ] Handle all edge cases correctly

---

## Additional Resources

- [CSES Playlist](https://cses.fi/problemset/task/1141) - Longest unique subarray
- [LeetCode Sliding Window Problems](https://leetcode.com/tag/sliding-window/)
