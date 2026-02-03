---
layout: simple
title: "String Reorder - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/string_reorder_analysis
difficulty: Easy
tags: [sorting, strings, frequency-counting, greedy]
prerequisites: []
---

# String Reorder

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Strings / Sorting |
| **Time Limit** | 1 second |
| **Key Technique** | Character Frequency Counting / Sorting |
| **CSES Link** | [String Reorder](https://cses.fi/problemset/task/1756) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand lexicographic ordering of characters
- [ ] Use character frequency counting for efficient string manipulation
- [ ] Build strings from character frequencies in sorted order
- [ ] Choose between sorting-based and counting-based approaches

---

## Problem Statement

**Problem:** Given a string, reorder its characters to create the lexicographically smallest possible string.

**Input:** A string s consisting of lowercase letters

**Output:** The lexicographically smallest string using all characters

**Constraints:**
- 1 <= |s| <= 10^6
- String contains only lowercase letters a-z

### Example

```
Input:  dcba
Output: abcd

Input:  monkey
Output: ekmnoy
```

**Explanation:** Sorting characters gives the lexicographically smallest arrangement.

---

## Intuition: How to Think About This Problem

> **Key Question:** What arrangement of characters produces the smallest string lexicographically?

The lexicographically smallest string places the smallest characters first. Since 'a' < 'b' < ... < 'z', we simply need all characters in ascending order.

**Analogy:** Think of organizing books alphabetically - 'd', 'c', 'b', 'a' becomes 'a', 'b', 'c', 'd'.

---

## Solution 1: Sorting Approach

### Idea

Simply sort all characters in the string and concatenate them.

### Code

**Python:**
```python
def solve_sorting(s):
    """
    Time: O(n log n) - sorting dominates
    Space: O(n) - storing sorted characters
    """
    return ''.join(sorted(s))

def main():
    s = input().strip()
    print(solve_sorting(s))

if __name__ == "__main__":
    main()
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    cin >> s;
    sort(s.begin(), s.end());
    cout << s << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Standard comparison sort |
| Space | O(n) | Storage for sorted result |

---

## Solution 2: Optimal - Counting Sort

### Key Insight

> **The Trick:** Since we only have 26 possible characters (a-z), we can count frequencies and rebuild the string in O(n) time.

### Algorithm

1. Count frequency of each character (array of size 26)
2. Iterate through characters 'a' to 'z'
3. For each character, append it frequency[char] times to result

### Dry Run Example

Input: `s = "dcba"`

```
Step 1: Count frequencies
  'd' -> freq[3] = 1
  'c' -> freq[2] = 1
  'b' -> freq[1] = 1
  'a' -> freq[0] = 1

  freq = [1, 1, 1, 1, 0, 0, ..., 0]
         ^a  ^b  ^c  ^d

Step 2: Build result
  i=0: append 'a' x 1 -> "a"
  i=1: append 'b' x 1 -> "ab"
  i=2: append 'c' x 1 -> "abc"
  i=3: append 'd' x 1 -> "abcd"

Result: "abcd"
```

### Code

**Python:**
```python
def solve_counting(s):
    """
    Counting sort: O(n) time, O(1) space.
    """
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('a')] += 1

    result = []
    for i in range(26):
        if freq[i] > 0:
            result.append(chr(ord('a') + i) * freq[i])

    return ''.join(result)

def main():
    s = input().strip()
    print(solve_counting(s))

if __name__ == "__main__":
    main()
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    cin >> s;

    int freq[26] = {0};
    for (char c : s) {
        freq[c - 'a']++;
    }

    string result;
    result.reserve(s.length());

    for (int i = 0; i < 26; i++) {
        result.append(freq[i], 'a' + i);
    }

    cout << result << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass to count, single pass to build |
| Space | O(1) | Fixed 26-element array |

---

## Common Mistakes

### Mistake 1: Inefficient String Concatenation (Python)

```python
# WRONG - O(n^2) due to string immutability
result = ""
for i in range(26):
    for j in range(freq[i]):
        result += chr(ord('a') + i)

# CORRECT - O(n) using list and join
result = []
for i in range(26):
    if freq[i] > 0:
        result.append(chr(ord('a') + i) * freq[i])
return ''.join(result)
```

### Mistake 2: Off-by-One in Character Index

```python
# WRONG - uses raw ASCII value (97 for 'a')
freq[ord(c)]

# CORRECT - normalize to 0-25 range
freq[ord(c) - ord('a')]
```

---

## Edge Cases

| Case | Input | Output | Why |
|------|-------|--------|-----|
| Single character | `a` | `a` | Already sorted |
| Already sorted | `abc` | `abc` | No change needed |
| Reverse sorted | `zyx` | `xyz` | Complete reversal |
| All same | `aaaa` | `aaaa` | No reordering needed |
| With repeats | `zzzzaaaabbbb` | `aaaabbbbzzzz` | Group same characters |

---

## When to Use This Pattern

### Use Counting Sort When:
- Input has a small, fixed alphabet (like lowercase letters)
- You need O(n) time complexity
- Characters can be mapped to array indices

### Use Standard Sorting When:
- Input alphabet is large or unknown
- Implementation simplicity is preferred

### Pattern Recognition Checklist:
- [ ] Need to reorder characters? -> **Consider sorting or counting**
- [ ] Fixed small alphabet? -> **Counting sort is optimal**
- [ ] Need lexicographically smallest/largest? -> **Sort ascending/descending**

---

## Related Problems

### Easier
| Problem | Why It Helps |
|---------|--------------|
| [Repetitions (CSES)](https://cses.fi/problemset/task/1069) | Basic character iteration |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Palindrome Reorder (CSES)](https://cses.fi/problemset/task/1755) | Arrange into palindrome |
| [Sort Characters By Frequency (LeetCode)](https://leetcode.com/problems/sort-characters-by-frequency/) | Sort by frequency, not alphabetically |

### Harder
| Problem | New Concept |
|---------|-------------|
| [Creating Strings (CSES)](https://cses.fi/problemset/task/1622) | Generate all permutations |
| [Reorganize String (LeetCode)](https://leetcode.com/problems/reorganize-string/) | No two adjacent characters same |

---

## Key Takeaways

1. **Core Idea:** Sorting characters produces lexicographically smallest arrangement
2. **Time Optimization:** Counting sort achieves O(n) for fixed alphabets
3. **Space Trade-off:** O(26) = O(1) fixed space vs O(n) for general sorting
4. **Pattern:** Counting sort is powerful when alphabet size is bounded

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain the difference between O(n log n) and O(n) solutions
- [ ] Implement counting sort from memory
- [ ] Identify when counting sort is applicable

---

## Additional Resources

- [CP-Algorithms: Counting Sort](https://cp-algorithms.com/sorting/counting-sort.html)
- [CSES Creating Strings I](https://cses.fi/problemset/task/1622) - String permutations
