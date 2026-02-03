---
layout: simple
title: "Repetitions - String Problem"
permalink: /problem_soulutions/introductory_problems/repetitions_analysis
difficulty: Easy
tags: [string, linear-scan, greedy]
---

# Repetitions

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 1069 - Repetitions](https://cses.fi/problemset/task/1069) |
| **Difficulty** | Easy |
| **Category** | String / Linear Scan |
| **Time Limit** | 1.0 seconds |
| **Key Technique** | Single Pass with Tracking |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Identify consecutive character counting problems
- [ ] Implement a single-pass linear scan algorithm
- [ ] Track current run length while updating global maximum
- [ ] Handle string boundary conditions correctly

---

## Problem Statement

**Problem:** Given a DNA sequence (string containing only A, C, G, T), find the length of the longest substring where all characters are the same.

**Input:**
- Line 1: A string of characters (A, C, G, T only)

**Output:**
- A single integer: the length of the longest repetition

**Constraints:**
- 1 <= |s| <= 10^6
- String contains only characters A, C, G, T

### Example

```
Input:
ATTCGGGA

Output:
3
```

**Explanation:** The longest repetition is "GGG" which has length 3. Other repetitions are "A" (1), "TT" (2), "C" (1), and "A" (1).

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we find the longest run of identical consecutive characters?

This is a classic **single-pass tracking** problem. As we scan through the string, we maintain two pieces of information:
1. The length of the current run of identical characters
2. The maximum run length seen so far

### Breaking Down the Problem

1. **What are we looking for?** The longest substring with all identical characters.
2. **What information do we have?** A string of DNA characters.
3. **What's the relationship between input and output?** We need to find the maximum count of any consecutive identical character sequence.

### Analogies

Think of this problem like counting consecutive red lights while driving. You keep track of:
- How many red lights you've hit in a row right now (current streak)
- The longest streak of red lights you've experienced so far (maximum streak)

Every time you hit a green light, your current streak resets to zero, but your maximum remains unchanged.

---

## Solution: Single Pass with Tracking

### Key Insight

> **The Trick:** We only need one pass through the string. When characters match, extend the current run. When they differ, compare the current run with the maximum and start a new run.

### Algorithm

1. Initialize `current_length = 1` and `max_length = 1`
2. Iterate through the string starting from index 1
3. If `s[i] == s[i-1]`: increment `current_length`
4. Else: update `max_length = max(max_length, current_length)` and reset `current_length = 1`
5. After the loop, do a final update of `max_length` (handles case where longest run is at the end)
6. Return `max_length`

### Dry Run Example

Let's trace through with input `ATTCGGGA`:

```
String: A  T  T  C  G  G  G  A
Index:  0  1  2  3  4  5  6  7

Initial: current = 1, max = 1

i=1: s[1]='T' vs s[0]='A' -> Different!
     max = max(1, 1) = 1
     current = 1

i=2: s[2]='T' vs s[1]='T' -> Same!
     current = 2

i=3: s[3]='C' vs s[2]='T' -> Different!
     max = max(1, 2) = 2
     current = 1

i=4: s[4]='G' vs s[3]='C' -> Different!
     max = max(2, 1) = 2
     current = 1

i=5: s[5]='G' vs s[4]='G' -> Same!
     current = 2

i=6: s[6]='G' vs s[5]='G' -> Same!
     current = 3

i=7: s[7]='A' vs s[6]='G' -> Different!
     max = max(2, 3) = 3
     current = 1

Final: max = max(3, 1) = 3

Answer: 3
```

### Visual Diagram

```
String: A T T C G G G A
        |---|   |-----|
         TT       GGG
        len=2    len=3 <-- Maximum!

Scanning left to right:
  A -> current=1, max=1
  T -> current=1, max=1  (reset)
  T -> current=2, max=2  (extend)
  C -> current=1, max=2  (reset)
  G -> current=1, max=2  (reset)
  G -> current=2, max=2  (extend)
  G -> current=3, max=3  (extend, new max!)
  A -> current=1, max=3  (reset)
```

### Code

**Python Solution:**

```python
def solve():
    """
    Find longest consecutive character run in DNA string.

    Time: O(n) - single pass
    Space: O(1) - only tracking two integers
    """
    s = input().strip()

    if len(s) == 0:
        print(0)
        return

    max_length = 1
    current_length = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1

    # Don't forget the final comparison!
    max_length = max(max_length, current_length)
    print(max_length)

if __name__ == "__main__":
    solve()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;

    if (s.empty()) {
        cout << 0 << "\n";
        return 0;
    }

    int max_length = 1;
    int current_length = 1;

    for (int i = 1; i < (int)s.size(); i++) {
        if (s[i] == s[i - 1]) {
            current_length++;
        } else {
            max_length = max(max_length, current_length);
            current_length = 1;
        }
    }

    // Final comparison for run ending at last character
    max_length = max(max_length, current_length);

    cout << max_length << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through the string |
| Space | O(1) | Only two integer variables needed |

---

## Common Mistakes

### Mistake 1: Forgetting Final Update

```python
# WRONG - Missing final comparison
for i in range(1, len(s)):
    if s[i] == s[i-1]:
        current_length += 1
    else:
        max_length = max(max_length, current_length)
        current_length = 1
print(max_length)  # Bug: misses run at end of string!
```

**Problem:** If the longest run ends at the last character, `max_length` never gets updated with it.

**Fix:** Always add `max_length = max(max_length, current_length)` after the loop.

### Mistake 2: Off-by-One in Loop Start

```python
# WRONG - Starting from index 0
for i in range(len(s)):
    if s[i] == s[i-1]:  # s[-1] when i=0 - accesses last character!
        ...
```

**Problem:** When `i=0`, `s[i-1]` accesses `s[-1]` (the last character in Python), causing incorrect comparison.

**Fix:** Start the loop from index 1: `for i in range(1, len(s))`.

### Mistake 3: Not Handling Empty/Single Character String

```python
# WRONG - Crashes on empty string
s = input()
for i in range(1, len(s)):  # This is fine
    ...
print(max_length)  # But max_length was never set if len(s) <= 1
```

**Problem:** If string has only one character, loop never executes but answer should be 1.

**Fix:** Initialize `max_length = 1` and handle empty string case separately.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `A` | `1` | One character is a run of length 1 |
| All same | `AAAAA` | `5` | Entire string is one run |
| All different | `ACGT` | `1` | No consecutive repeats |
| Longest at start | `AAACGT` | `3` | Ensure we capture early runs |
| Longest at end | `CGTAAA` | `3` | Ensure final update works |
| Alternating | `ATATAT` | `1` | No consecutive pairs |
| Maximum length | `A` * 10^6 | `1000000` | Performance test |

---

## When to Use This Pattern

### Use This Approach When:
- Counting consecutive identical elements in a sequence
- Finding longest/shortest runs of matching items
- Problems involving "streaks" or "consecutive" patterns
- Single-pass O(n) solution is required

### Don't Use When:
- You need to find runs of patterns (not single elements)
- The definition of "consecutive" involves non-adjacent elements
- You need all runs, not just the longest one

### Pattern Recognition Checklist:
- [ ] Looking for consecutive identical elements? -> **Single pass tracking**
- [ ] Need maximum/minimum of runs? -> **Track current and best**
- [ ] Processing sequence left to right? -> **Linear scan pattern**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Weird Algorithm](https://cses.fi/problemset/task/1068) | Basic simulation practice |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Missing Number](https://cses.fi/problemset/task/1083) | Single pass with different tracking |
| [Increasing Array](https://cses.fi/problemset/task/1094) | Track running sum instead of run length |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Max Consecutive Ones III (LeetCode)](https://leetcode.com/problems/max-consecutive-ones-iii/) | Sliding window with allowed flips |
| [Longest Substring Without Repeating Characters (LeetCode)](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Sliding window with hash set |

---

## Key Takeaways

1. **The Core Idea:** Track current run length and maximum seen; update maximum when run breaks.
2. **Time Optimization:** Single pass O(n) is optimal - we must read every character at least once.
3. **Space Trade-off:** O(1) space - only need two counters.
4. **Pattern:** This is the "consecutive element tracking" pattern, common in string and array problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why the final max comparison after the loop is necessary
- [ ] Identify edge cases (single char, all same, longest at end)
- [ ] Implement in your preferred language in under 5 minutes

---

## Additional Resources

- [CSES Repetitions](https://cses.fi/problemset/task/1069) - Longest consecutive run
- [Run-Length Encoding (Wikipedia)](https://en.wikipedia.org/wiki/Run-length_encoding) - Related concept
