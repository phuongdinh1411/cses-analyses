---
layout: simple
title: "Longest Substring Without Repeating Characters - Sliding Window"
permalink: /problem_soulutions/sliding_window/longest_substring_without_repeating_analysis
difficulty: Medium
tags: [sliding-window, two-pointers, hash-set, string]
---

# Longest Substring Without Repeating Characters

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window / Two Pointers |
| **Time Limit** | 1 second |
| **Key Technique** | Sliding Window with Hash Set |
| **LeetCode** | [Problem #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when to apply the sliding window technique
- [ ] Use a hash set to track distinct elements in a window
- [ ] Implement variable-size sliding window with character constraints
- [ ] Shrink windows efficiently when constraints are violated

---

## Problem Statement

**Problem:** Given a string `s`, find the length of the longest substring without repeating characters.

**Input:**
- A string `s` containing characters

**Output:**
- A single integer: the length of the longest substring with all unique characters

**Constraints:**
- 0 <= |s| <= 10^5
- s consists of English letters, digits, symbols, and spaces

### Example

```
Input:
abcabcbb

Output:
3
```

**Explanation:** The longest substring without repeating characters is "abc", which has length 3. Other valid substrings of length 3 include "bca" and "cab".

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently find the longest contiguous segment with all unique elements?

When you see "longest/shortest substring/subarray" with some constraint, think **sliding window**. The constraint here is "no repeating characters," which we can track with a hash set.

### Breaking Down the Problem

1. **What are we looking for?** Maximum length of a contiguous substring
2. **What constraint must be satisfied?** All characters in the substring must be unique
3. **What changes as we scan?** The window expands when we see a new character, shrinks when we see a duplicate

### Analogy

Think of this like a caterpillar crawling along a string. The caterpillar's body (window) can stretch to include new unique characters, but when it encounters a character already in its body, it must pull up its tail until the duplicate is removed.

---

## Solution 1: Brute Force

### Idea

Check every possible substring and verify if it contains all unique characters.

### Algorithm

1. For each starting position `i` from 0 to n-1
2. For each ending position `j` from `i` to n-1
3. Check if substring `s[i..j]` has all unique characters
4. Track the maximum length found

### Code (Python)

```python
def longest_substring_brute(s: str) -> int:
    """
    Brute force: check all substrings.
    Time: O(n^3), Space: O(n)
    """
    n = len(s)
    max_len = 0

    for i in range(n):
        for j in range(i, n):
            substring = s[i:j+1]
            if len(set(substring)) == len(substring):  # All unique
                max_len = max(max_len, j - i + 1)

    return max_len
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | O(n^2) substrings, O(n) to check each |
| Space | O(n) | Set to store substring characters |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every possible substring. However, we do redundant work: when expanding from `s[i..j]` to `s[i..j+1]`, we rebuild the entire set instead of incrementally updating it.

---

## Solution 2: Optimal - Sliding Window with Hash Set

### Key Insight

> **The Trick:** Use two pointers to maintain a window of unique characters. When we find a duplicate, shrink from the left until the duplicate is removed.

### Algorithm

1. Initialize `left = 0`, `max_len = 0`, and an empty hash set `seen`
2. For each `right` from 0 to n-1:
   - While `s[right]` is already in `seen`:
     - Remove `s[left]` from `seen`
     - Increment `left`
   - Add `s[right]` to `seen`
   - Update `max_len = max(max_len, right - left + 1)`
3. Return `max_len`

### Dry Run Example

Let's trace through with input `s = "abcabcbb"`:

```
Initial: left=0, seen={}, max_len=0

right=0, char='a':
  'a' not in seen
  seen = {'a'}
  window = "a", max_len = 1

right=1, char='b':
  'b' not in seen
  seen = {'a','b'}
  window = "ab", max_len = 2

right=2, char='c':
  'c' not in seen
  seen = {'a','b','c'}
  window = "abc", max_len = 3

right=3, char='a':
  'a' IN seen! Shrink from left
    remove 'a', left=1, seen = {'b','c'}
  'a' not in seen now
  seen = {'b','c','a'}
  window = "bca", max_len = 3

right=4, char='b':
  'b' IN seen! Shrink from left
    remove 'b', left=2, seen = {'c','a'}
  'b' not in seen now
  seen = {'c','a','b'}
  window = "cab", max_len = 3

right=5, char='c':
  'c' IN seen! Shrink from left
    remove 'c', left=3, seen = {'a','b'}
  'c' not in seen now
  seen = {'a','b','c'}
  window = "abc", max_len = 3

right=6, char='b':
  'b' IN seen! Shrink from left
    remove 'a', left=4, seen = {'b','c'}
  'b' still in seen!
    remove 'b', left=5, seen = {'c'}
  'b' not in seen now
  seen = {'c','b'}
  window = "cb", max_len = 3

right=7, char='b':
  'b' IN seen! Shrink from left
    remove 'c', left=6, seen = {'b'}
  'b' still in seen!
    remove 'b', left=7, seen = {}
  'b' not in seen now
  seen = {'b'}
  window = "b", max_len = 3

Final: max_len = 3
```

### Visual Diagram

```
String: a b c a b c b b
Index:  0 1 2 3 4 5 6 7

Step 3:  [a b c]          max=3
              L     R

Step 4:    [b c a]        max=3 (shrink left, add 'a')
              L   R

Step 5:      [c a b]      max=3
                L   R

Step 6:        [a b c]    max=3
                  L   R

Final answer: 3 (substrings "abc", "bca", "cab" all work)
```

### Code (Python)

```python
def longest_substring_optimal(s: str) -> int:
    """
    Sliding window with hash set.
    Time: O(n), Space: O(min(n, alphabet_size))
    """
    seen = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Shrink window while duplicate exists
        while s[right] in seen:
            seen.remove(s[left])
            left += 1

        # Add current character and update max
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each character is added and removed from set at most once |
| Space | O(min(n, m)) | Set stores at most min(n, alphabet_size) characters |

---

## Alternative: Optimized Jump with Hash Map

Instead of shrinking one character at a time, we can jump directly to the position after the last occurrence of the duplicate character.

### Code (Python)

```python
def longest_substring_jump(s: str) -> int:
    """
    Optimized: jump left pointer directly using last index map.
    Time: O(n), Space: O(min(n, alphabet_size))
    """
    last_index = {}  # char -> last seen index
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in last_index and last_index[char] >= left:
            left = last_index[char] + 1  # Jump past the duplicate

        last_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Common Mistakes

### Mistake 1: Forgetting to Remove Character Before Incrementing Left

```python
# WRONG
while s[right] in seen:
    left += 1              # Moved left but didn't remove s[left-1]!
    seen.remove(s[left])   # Wrong index

# CORRECT
while s[right] in seen:
    seen.remove(s[left])   # Remove BEFORE incrementing
    left += 1
```

**Problem:** The set becomes inconsistent with the actual window.
**Fix:** Always remove the character at `left` before incrementing `left`.

### Mistake 2: Not Checking if Duplicate is Within Current Window

```python
# WRONG (for the jump optimization)
if char in last_index:
    left = last_index[char] + 1  # May jump backwards!

# CORRECT
if char in last_index and last_index[char] >= left:
    left = last_index[char] + 1
```

**Problem:** The duplicate might be from before the current window started.
**Fix:** Only update `left` if the duplicate is within the current window.

### Mistake 3: Using Dictionary Instead of Set (Overcomplicated)

```python
# OVERCOMPLICATED
char_count = {}
char_count[s[right]] = char_count.get(s[right], 0) + 1
while char_count[s[right]] > 1:
    char_count[s[left]] -= 1
    if char_count[s[left]] == 0:
        del char_count[s[left]]
    left += 1

# SIMPLER (use a set when you only need presence/absence)
seen = set()
while s[right] in seen:
    seen.remove(s[left])
    left += 1
seen.add(s[right])
```

**Problem:** Tracking counts when you only need to track presence.
**Fix:** Use a set for simpler "contains duplicate" checks.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Empty string | `""` | 0 | No characters |
| Single character | `"a"` | 1 | One unique character |
| All same characters | `"aaaa"` | 1 | Only one unique at a time |
| All unique | `"abcd"` | 4 | Entire string is the answer |
| Duplicate at end | `"abca"` | 3 | "abc" or "bca" |
| Space character | `" "` | 1 | Space counts as a character |
| Mixed characters | `"a1!a"` | 3 | "a1!" or "1!a" |

---

## When to Use This Pattern

### Use Sliding Window + Hash Set When:
- Finding longest/shortest substring with distinct elements
- Counting subarrays/substrings with unique constraint
- Problems involving "at most K distinct" elements

### Don't Use When:
- Looking for subsequences (not contiguous)
- Order of elements matters beyond position
- Need to track exact counts, not just presence

### Pattern Recognition Checklist:
- [ ] Contiguous subarray/substring? --> **Consider sliding window**
- [ ] Constraint on distinct/unique elements? --> **Use hash set**
- [ ] "At most K distinct"? --> **Track count of distinct, shrink when > K**
- [ ] "Longest without repeating"? --> **This exact pattern**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Intro to sliding/expanding window concept |
| [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Basic hash set usage |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Longest Substring with At Most Two Distinct](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/) | Allow 2 distinct instead of 0 duplicates |
| [Longest Substring with At Most K Distinct](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) | Generalized to K distinct characters |
| [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | Same as "at most 2 distinct" |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Shrinking to find minimum |
| [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Window with modification budget |
| [Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) | Fixed-size word matching |

### CSES Related Problems

| Problem | Concept |
|---------|---------|
| [Playlist](https://cses.fi/problemset/task/1141) | Same pattern - longest with unique elements |
| [Subarray Distinct Values](https://cses.fi/problemset/task/2428) | Count subarrays with at most K distinct |

---

## Key Takeaways

1. **The Core Idea:** Maintain a window of unique characters using a hash set, expanding right and shrinking left when duplicates appear.

2. **Time Optimization:** From O(n^3) brute force to O(n) by avoiding redundant set rebuilding.

3. **Space Trade-off:** O(min(n, alphabet_size)) space for O(n) time.

4. **Pattern:** This is the classic "sliding window with hash set" pattern for distinct element constraints.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem in under 10 minutes without looking at the solution
- [ ] Explain why each character is processed at most twice (O(n) time)
- [ ] Implement both the set-based and map-based approaches
- [ ] Adapt this pattern for "at most K distinct" problems
- [ ] Identify this pattern when you see "longest substring with unique/distinct"

---

## Complete Solution Template

```python
# Python - Copy-paste ready
def lengthOfLongestSubstring(s: str) -> int:
    seen = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

