---
layout: simple
title: "Longest Palindrome - String Algorithms"
permalink: /problem_soulutions/string_algorithms/longest_palindrome_analysis
difficulty: Medium
tags: [strings, manacher, palindrome, center-expansion]
prerequisites: []
---

# Longest Palindrome

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Longest Palindrome](https://cses.fi/problemset/task/1111) |
| **Difficulty** | Medium |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Manacher's Algorithm |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand why brute force palindrome detection is inefficient
- [ ] Apply center expansion technique for palindrome finding
- [ ] Implement Manacher's algorithm for O(n) palindrome detection
- [ ] Handle both odd and even length palindromes uniformly
- [ ] Use the mirror property to avoid redundant computations

---

## Problem Statement

**Problem:** Given a string, find the longest palindromic substring.

**Input:**
- Line 1: A string s consisting of lowercase letters

**Output:**
- Print the longest palindromic substring (if multiple exist, print any one)

**Constraints:**
- 1 <= |s| <= 10^6
- String contains only lowercase English letters (a-z)

### Example

```
Input:
babad

Output:
bab
```

**Explanation:** The string "babad" has two longest palindromes of length 3: "bab" and "aba". Either is a valid answer.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently find palindromes without checking every substring?

A palindrome is symmetric around its center. Instead of checking all O(n^2) substrings, we can expand outward from each potential center. Manacher's algorithm takes this further by reusing information from previously found palindromes.

### Breaking Down the Problem

1. **What are we looking for?** The longest substring that reads the same forwards and backwards.
2. **What information do we have?** A string of characters.
3. **What's the relationship between input and output?** We need to find the maximum-length symmetric substring.

### Analogies

Think of finding a palindrome like finding the widest mirror reflection in a string. Each character can be the center of a mirror, and we expand outward to find how far the reflection extends perfectly.

---

## Solution 1: Center Expansion (Recommended for Interviews)

### Idea

For each position in the string, treat it as a potential center and expand outward while characters match. Handle both odd-length (single center) and even-length (two adjacent centers) palindromes.

### Algorithm

1. For each index i, expand around center (i, i) for odd-length palindromes
2. For each index i, expand around center (i, i+1) for even-length palindromes
3. Track the longest palindrome found
4. Return the longest palindrome substring

### Code (Python)

```python
def longest_palindrome_expand(s: str) -> str:
    """
    Find longest palindrome using center expansion.
    Time: O(n^2), Space: O(1)
    """
    if not s:
        return ""

    def expand(left: int, right: int) -> int:
        """Expand around center and return palindrome length."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    start, max_len = 0, 1

    for i in range(len(s)):
        len1 = expand(i, i)      # Odd length
        len2 = expand(i, i + 1)  # Even length
        curr_len = max(len1, len2)

        if curr_len > max_len:
            max_len = curr_len
            start = i - (curr_len - 1) // 2

    return s[start:start + max_len]

# Read input and solve
s = input().strip()
print(longest_palindrome_expand(s))
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int expand(const string& s, int left, int right) {
    while (left >= 0 && right < s.size() && s[left] == s[right]) {
        left--;
        right++;
    }
    return right - left - 1;
}

string longestPalindromeExpand(const string& s) {
    if (s.empty()) return "";

    int start = 0, maxLen = 1;

    for (int i = 0; i < s.size(); i++) {
        int len1 = expand(s, i, i);
        int len2 = expand(s, i, i + 1);
        int currLen = max(len1, len2);

        if (currLen > maxLen) {
            maxLen = currLen;
            start = i - (currLen - 1) / 2;
        }
    }

    return s.substr(start, maxLen);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    cout << longestPalindromeExpand(s) << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Each center can expand up to n characters |
| Space | O(1) | Only storing indices |

---

## Solution 2: Manacher's Algorithm (Optimal)

### Key Insight

> **The Trick:** Transform the string to handle even/odd lengths uniformly, then use previously computed palindrome information to skip redundant expansions.

### Algorithm Overview

1. **Transform string:** Insert separators (e.g., '#') between characters to handle even-length palindromes
2. **Mirror property:** If position i is within a known palindrome centered at c, use the mirror position's value as a starting point
3. **Expand only when necessary:** Only expand beyond what the mirror tells us

### Visual Explanation

```
Original: "babad"
Transformed: "#b#a#b#a#d#"

The '#' characters ensure every palindrome has odd length in the transformed string.

Mirror property:
    center = c, right boundary = r
    For position i within r:
        mirror = 2*c - i
        P[i] >= min(P[mirror], r - i)
```

### Dry Run Example

Let's trace through with input `s = "babad"`:

```
Transformed: "#b#a#b#a#d#"
Indices:      0 1 2 3 4 5 6 7 8 9 10

Initial: center=0, right=0, P = [0,0,0,0,0,0,0,0,0,0,0]

i=1 (char 'b'):
  i >= right, so start fresh
  Expand: P[1] = 1 (palindrome "#b#")
  Update: center=1, right=2

i=2 (char '#'):
  i >= right, expand: P[2] = 0

i=3 (char 'a'):
  mirror = 2*1 - 3 = -1 (invalid), start fresh
  Expand: P[3] = 3 (palindrome "#b#a#b#")
  Update: center=3, right=6

i=4 (char '#'):
  i < right, mirror = 2*3 - 4 = 2, P[mirror]=0
  P[4] = min(0, 6-4) = 0

i=5 (char 'a'):
  i < right, mirror = 2*3 - 5 = 1, P[mirror]=1
  P[5] = min(1, 6-5) = 1
  Expand: P[5] = 3 (palindrome "#a#b#a#")
  Update: center=5, right=8

... continue for remaining positions

Maximum P[i] = 3 at indices 3 or 5
Original palindrome length = 3, which gives "bab" or "aba"
```

### Code (Python)

```python
def longest_palindrome_manacher(s: str) -> str:
    """
    Find longest palindrome using Manacher's algorithm.
    Time: O(n), Space: O(n)
    """
    if not s:
        return ""

    # Transform: "abc" -> "#a#b#c#"
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n  # p[i] = radius of palindrome centered at i
    center = right = 0
    max_len, max_center = 0, 0

    for i in range(n):
        # Use mirror property if within current right boundary
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])

        # Expand around center i
        while (i + p[i] + 1 < n and i - p[i] - 1 >= 0 and
               t[i + p[i] + 1] == t[i - p[i] - 1]):
            p[i] += 1

        # Update center and right boundary
        if i + p[i] > right:
            center, right = i, i + p[i]

        # Track maximum
        if p[i] > max_len:
            max_len, max_center = p[i], i

    # Convert back to original string indices
    start = (max_center - max_len) // 2
    return s[start:start + max_len]

# Read input and solve
s = input().strip()
print(longest_palindrome_manacher(s))
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

string longestPalindromeManacher(const string& s) {
    if (s.empty()) return "";

    // Transform: "abc" -> "#a#b#c#"
    string t = "#";
    for (char c : s) {
        t += c;
        t += '#';
    }

    int n = t.size();
    vector<int> p(n, 0);  // p[i] = radius of palindrome centered at i
    int center = 0, right = 0;
    int maxLen = 0, maxCenter = 0;

    for (int i = 0; i < n; i++) {
        // Use mirror property if within current right boundary
        if (i < right) {
            int mirror = 2 * center - i;
            p[i] = min(right - i, p[mirror]);
        }

        // Expand around center i
        while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 &&
               t[i + p[i] + 1] == t[i - p[i] - 1]) {
            p[i]++;
        }

        // Update center and right boundary
        if (i + p[i] > right) {
            center = i;
            right = i + p[i];
        }

        // Track maximum
        if (p[i] > maxLen) {
            maxLen = p[i];
            maxCenter = i;
        }
    }

    // Convert back to original string indices
    int start = (maxCenter - maxLen) / 2;
    return s.substr(start, maxLen);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    cout << longestPalindromeManacher(s) << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each position is expanded at most once total |
| Space | O(n) | Transformed string and radius array |

---

## Common Mistakes

### Mistake 1: Forgetting Even-Length Palindromes

```python
# WRONG - only handles odd length
for i in range(n):
    length = expand(i, i)  # Missing even-length check!
```

**Problem:** Even-length palindromes like "abba" have no single center character.
**Fix:** Also expand around (i, i+1) or use Manacher's transformation.

### Mistake 2: Off-by-One in Index Conversion

```python
# WRONG - incorrect conversion from transformed to original
start = max_center - max_len  # Should divide by 2!
```

**Problem:** The transformed string is ~2x longer than original.
**Fix:** Use `start = (max_center - max_len) // 2`

### Mistake 3: Boundary Check Order

```python
# WRONG - may access out of bounds before checking
while t[i + p[i] + 1] == t[i - p[i] - 1] and i + p[i] + 1 < n:
```

**Problem:** Array access happens before bounds check.
**Fix:** Check bounds first: `while i + p[i] + 1 < n and i - p[i] - 1 >= 0 and ...`

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `"a"` | `"a"` | Single char is always a palindrome |
| All same characters | `"aaaa"` | `"aaaa"` | Entire string is palindrome |
| No palindrome > 1 | `"abcd"` | `"a"` (or any single char) | Each char is a palindrome of length 1 |
| Even-length palindrome | `"abba"` | `"abba"` | Must handle even-length case |
| Entire string | `"racecar"` | `"racecar"` | Whole string is the answer |
| Multiple longest | `"babad"` | `"bab"` or `"aba"` | Either is valid |

---

## When to Use This Pattern

### Use Center Expansion When:
- Interview setting (simpler to implement correctly)
- O(n^2) is acceptable for the given constraints
- You need to explain your solution clearly

### Use Manacher's Algorithm When:
- String length is large (10^5 or more)
- Strict O(n) time complexity is required
- You are comfortable with the implementation

### Pattern Recognition Checklist:
- [ ] Looking for palindromic substrings? -> **Consider center expansion**
- [ ] Need O(n) time for palindrome problems? -> **Consider Manacher's**
- [ ] Need count of all palindromic substrings? -> **Manacher's gives all radii**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Valid Palindrome (LeetCode 125)](https://leetcode.com/problems/valid-palindrome/) | Basic palindrome check |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Palindromic Substrings (LeetCode 647)](https://leetcode.com/problems/palindromic-substrings/) | Count all palindromes instead of finding longest |
| [Palindrome Queries (CSES 2420)](https://cses.fi/problemset/task/2420) | Query-based palindrome checking |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Longest Palindromic Subsequence (LeetCode 516)](https://leetcode.com/problems/longest-palindromic-subsequence/) | DP for non-contiguous palindrome |
| [Palindrome Partitioning II (LeetCode 132)](https://leetcode.com/problems/palindrome-partitioning-ii/) | DP with palindrome precomputation |

---

## Key Takeaways

1. **The Core Idea:** Palindromes are symmetric around their center; expand outward to find them.
2. **Time Optimization:** Manacher's algorithm reuses previous palindrome information via the mirror property.
3. **Space Trade-off:** O(n) space in Manacher's buys O(n) time (vs O(n^2) for center expansion).
4. **Pattern:** String transformation (adding separators) can unify handling of different cases.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement center expansion without looking at the solution
- [ ] Explain why Manacher's algorithm is O(n)
- [ ] Handle both odd and even length palindromes
- [ ] Convert between transformed and original string indices

---

## Additional Resources

- [CP-Algorithms: Manacher's Algorithm](https://cp-algorithms.com/string/manacher.html)
- [CSES Longest Palindrome](https://cses.fi/problemset/task/1111) - Manacher's algorithm
