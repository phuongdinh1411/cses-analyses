---
layout: simple
title: "Minimum Window Substring - Sliding Window Problem"
permalink: /problem_soulutions/sliding_window/minimum_window_substring_analysis
difficulty: Hard
tags: [sliding-window, two-pointers, hash-map, string]
---

# Minimum Window Substring

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Sliding Window / Two Pointers |
| **Time Limit** | 1 second |
| **Key Technique** | Variable-size sliding window with frequency tracking |
| **Similar To** | [Playlist (CSES 2429)](https://cses.fi/problemset/task/2429) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Implement a variable-size sliding window that expands and contracts
- [ ] Track character frequencies using hash maps efficiently
- [ ] Use a "formed" counter to track when window conditions are satisfied
- [ ] Recognize minimum window problems and apply the shrinking window pattern

---

## Problem Statement

**Problem:** Given two strings `s` and `t`, find the minimum length substring of `s` that contains all characters of `t` (including duplicates).

**Input:**
- Line 1: String `s` (the source string)
- Line 2: String `t` (the target characters)

**Output:**
- The minimum window substring, or empty string if no valid window exists

**Constraints:**
- 1 <= |s|, |t| <= 10^5
- `s` and `t` consist of uppercase and lowercase English letters

### Example

```
Input:
ADOBECODEBANC
ABC

Output:
BANC
```

**Explanation:** "BANC" is the smallest substring containing A, B, and C. Other valid windows like "ADOBEC" are longer.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently find the smallest window containing all required characters?

This is a classic **variable-size sliding window** problem. The key insight is that once we find a valid window, we should try to shrink it from the left to find the minimum.

### Breaking Down the Problem

1. **What are we looking for?** The shortest substring containing all characters from `t`
2. **What information do we track?** Character frequencies in current window vs required frequencies
3. **When do we expand?** When window doesn't contain all required characters
4. **When do we shrink?** When window contains all required characters

### Analogies

Think of this like adjusting a spotlight on a stage. You expand the spotlight (right pointer) until all actors (required characters) are visible. Then you narrow the spotlight from one side (left pointer) to find the tightest focus that still includes everyone.

---

## Solution 1: Brute Force

### Idea

Check every possible substring and find the smallest one containing all characters of `t`.

### Algorithm

1. Generate all substrings of `s`
2. For each substring, check if it contains all characters of `t`
3. Track the minimum length valid substring

### Code

```python
def min_window_brute(s: str, t: str) -> str:
 """
 Brute force: Check all substrings.
 Time: O(n^2 * m) where n = len(s), m = len(t)
 Space: O(m)
 """
 def contains_all(window: str, target: str) -> bool:
  from collections import Counter
  t_count = Counter(target)
  for c in window:
   if c in t_count:
    t_count[c] -= 1
    if t_count[c] == 0:
     del t_count[c]
  return len(t_count) == 0

 min_window = ""
 min_len = float('inf')

 for i in range(len(s)):
  for j in range(i + len(t), len(s) + 1):
   window = s[i:j]
   if contains_all(window, t) and len(window) < min_len:
    min_len = len(window)
    min_window = window

 return min_window
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 * m) | n^2 substrings, O(m) to check each |
| Space | O(m) | Counter for target string |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every substring. However, with n up to 10^5, O(n^2) operations would timeout.

---

## Solution 2: Optimal Sliding Window

### Key Insight

> **The Trick:** Use two pointers to maintain a window. Expand right to include characters, shrink left to minimize. Track how many required characters are "formed" (have sufficient count).

### State Tracking

| Variable | Purpose |
|----------|---------|
| `t_count` | Required frequency of each character in `t` |
| `window_count` | Current frequency of characters in window |
| `required` | Number of unique characters needed (len of t_count) |
| `formed` | Number of unique characters with sufficient count |

### Algorithm

1. Build frequency map of `t`
2. Expand window by moving right pointer
3. When a character count matches requirement, increment `formed`
4. When `formed == required`, try shrinking from left
5. Update minimum window when valid
6. Continue until right pointer exhausts `s`

### Dry Run Example

Input: `s = "ADOBECODEBANC"`, `t = "ABC"`

```
t_count = {A:1, B:1, C:1}, required = 3

Step 1: Expand right
  right=0 (A): window={A:1}, formed=1 (A matched)
  right=1 (D): window={A:1,D:1}, formed=1
  right=2 (O): window={A:1,D:1,O:1}, formed=1
  right=3 (B): window={A:1,D:1,O:1,B:1}, formed=2 (B matched)
  right=4 (E): window={...,E:1}, formed=2
  right=5 (C): window={...,C:1}, formed=3 (C matched!)

Step 2: Shrink left (formed == required)
  Window "ADOBEC" (len=6), update min_window
  left=0->1: Remove A, window={A:0,...}, formed=2 (A no longer matched)

Step 3: Continue expanding
  right=6 (O): formed=2
  right=7 (D): formed=2
  right=8 (E): formed=2
  right=9 (B): window={...,B:2}, formed=2 (already had B)
  right=10 (A): window={A:1,...}, formed=3!

Step 4: Shrink left again
  Window "DOBECODEBA" - shrink...
  Eventually reach "BANC" (len=4) - new minimum!

Final answer: "BANC"
```

### Visual Diagram

```
s: A D O B E C O D E B A N C
   0 1 2 3 4 5 6 7 8 9 10 11 12

Window 1: [A D O B E C]        len=6, valid
              L         R

Window 2: [B A N C]            len=4, valid (MINIMUM)
                    L     R
```

### Code

**Python:**
```python
from collections import Counter

def min_window(s: str, t: str) -> str:
 """
 Optimal sliding window solution.
 Time: O(n + m)
 Space: O(m)
 """
 if not s or not t or len(s) < len(t):
  return ""

 # Character frequency required
 t_count = Counter(t)
 required = len(t_count)

 # Window state
 window_count = {}
 formed = 0
 left = 0

 # Result tracking
 min_len = float('inf')
 result = (0, 0)

 for right in range(len(s)):
  # Expand: add s[right] to window
  char = s[right]
  window_count[char] = window_count.get(char, 0) + 1

  # Check if this character's count matches requirement
  if char in t_count and window_count[char] == t_count[char]:
   formed += 1

  # Shrink: contract window from left while valid
  while formed == required and left <= right:
   # Update result if current window is smaller
   if right - left + 1 < min_len:
    min_len = right - left + 1
    result = (left, right + 1)

   # Remove s[left] from window
   left_char = s[left]
   window_count[left_char] -= 1
   if left_char in t_count and window_count[left_char] < t_count[left_char]:
    formed -= 1
   left += 1

 return s[result[0]:result[1]] if min_len != float('inf') else ""
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + m) | Each character visited at most twice (once by right, once by left) |
| Space | O(m) | Hash maps store at most unique characters in `t` |

---

## Common Mistakes

### Mistake 1: Incrementing `formed` on Every Character Match

```python
# WRONG
if char in t_count:
 formed += 1  # Increments even if already have enough
```

**Problem:** We only want to increment `formed` when we reach the exact required count, not on every occurrence.

**Fix:** Check if count equals (not exceeds) the requirement:
```python
if char in t_count and window_count[char] == t_count[char]:
 formed += 1
```

### Mistake 2: Using Total Characters Instead of Unique Characters

```python
# WRONG
required = len(t)  # Total chars including duplicates
formed = 0

# This breaks when t has duplicates like "AAB"
```

**Problem:** With `t = "AAB"`, we need 2 A's and 1 B (2 unique chars to match), not 3 matches.

**Fix:** Use number of unique characters:
```python
required = len(t_count)  # Number of unique characters
```

### Mistake 3: Not Handling Empty Result

```python
# WRONG
return s[result[0]:result[1]]  # Crashes if no valid window found
```

**Fix:** Check for valid result:
```python
return s[result[0]:result[1]] if min_len != float('inf') else ""
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| No valid window | s="ABC", t="D" | "" | Target char not in source |
| t longer than s | s="A", t="ABC" | "" | Impossible to contain |
| Exact match | s="ABC", t="ABC" | "ABC" | Entire string is the window |
| Duplicate chars | s="AAAB", t="AA" | "AA" | Must handle frequency correctly |
| Single char | s="A", t="A" | "A" | Minimal case |
| Empty strings | s="", t="A" | "" | Handle empty input |

---

## When to Use This Pattern

### Use Variable-Size Sliding Window When:
- Finding minimum/maximum substring with a condition
- Window size depends on content, not fixed
- Need to track frequency/count of elements in window
- Can identify when to expand vs shrink

### Pattern Recognition Checklist:
- [ ] Looking for minimum length substring? -> **Expand then shrink**
- [ ] Looking for maximum length substring? -> **Shrink then expand**
- [ ] Need to track character frequencies? -> **Hash map + formed counter**
- [ ] Window validity based on content? -> **Variable-size window**

### Don't Use When:
- Window size is fixed (use fixed-size sliding window)
- No clear window validity condition
- Need to find all occurrences, not just optimal

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Longest Substring Without Repeating](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Basic variable window |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Playlist (CSES 2429)](https://cses.fi/problemset/task/2429) | Maximum window with unique elements |
| [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Fixed window size, anagram matching |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Substring with Concatenation](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) | Word-level windows |
| [Minimum Window Subsequence](https://leetcode.com/problems/minimum-window-subsequence/) | Subsequence ordering |

---

## Key Takeaways

1. **The Core Idea:** Expand window to satisfy condition, shrink to optimize
2. **Time Optimization:** Each pointer moves at most n times -> O(2n) = O(n)
3. **Space Trade-off:** O(m) space for frequency maps enables O(n) time
4. **Pattern:** Variable-size sliding window with "formed" counter for validation

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why each pointer moves at most n times
- [ ] Handle duplicates in the target string correctly
- [ ] Implement in your preferred language in under 15 minutes
- [ ] Identify similar problems that use this pattern
