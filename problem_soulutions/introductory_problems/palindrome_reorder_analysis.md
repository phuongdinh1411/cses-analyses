---
layout: simple
title: "Palindrome Reorder - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/palindrome_reorder_analysis
difficulty: Easy
tags: [string, frequency-counting, palindrome, greedy]
---

# Palindrome Reorder

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1755](https://cses.fi/problemset/task/1755) |
| **Difficulty** | Easy |
| **Category** | String / Frequency Counting |
| **Time Limit** | 1 second |
| **Key Technique** | Character Frequency + Palindrome Construction |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply character frequency analysis to determine if a string can form a palindrome
- [ ] Understand the mathematical rule: at most one character can have an odd frequency
- [ ] Construct palindromes efficiently by placing characters symmetrically
- [ ] Handle both even and odd length palindrome construction

---

## Problem Statement

**Problem:** Given a string, reorder its characters to form a palindrome. If no palindrome can be formed, output "NO SOLUTION".

**Input:**
- A single string of length n (1 <= n <= 10^6), containing only uppercase letters A-Z

**Output:**
- A palindrome formed by reordering the input string, or "NO SOLUTION" if impossible

**Constraints:**
- 1 <= n <= 10^6
- String contains only uppercase letters (A-Z)

### Example

```
Input:
AAAACACBA

Output:
AACABACAA
```

**Explanation:** The string "AAAACACBA" has characters: A(6), B(1), C(2). Since only one character (B) has an odd count, we can form a palindrome by placing B in the middle and arranging A's and C's symmetrically.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When can a string be rearranged into a palindrome?

A palindrome reads the same forwards and backwards. For this to happen:
- **Even-length string:** Every character must appear an even number of times (each character pairs with itself on the opposite side)
- **Odd-length string:** Exactly one character can appear an odd number of times (placed in the middle)

### Breaking Down the Problem

1. **What are we looking for?** A valid arrangement where string[i] = string[n-1-i] for all i
2. **What information do we have?** Character frequencies
3. **What's the relationship between input and output?** If at most one character has odd frequency, palindrome is possible

### Analogies

Think of building a palindrome like filling seats on both sides of an aisle. Characters with even counts fill seats symmetrically on both sides. At most one "odd" person can sit in the middle aisle seat.

---

## Solution: Frequency Counting + Construction

### Key Insight

> **The Trick:** Count character frequencies. If more than one character has an odd count, it's impossible. Otherwise, build the palindrome by placing half of each character on the left, the odd character (if any) in the middle, and mirror the left side for the right.

### Algorithm

1. Count the frequency of each character
2. Check validity: count how many characters have odd frequency
   - If more than 1 character has odd frequency -> "NO SOLUTION"
3. Build the palindrome:
   - For each character, add `count // 2` copies to the left half
   - Remember the character with odd count (if any)
   - Place the odd character in the middle
   - Mirror the left half to create the right half

### Dry Run Example

Let's trace through with input `AAAACACBA` (9 characters):

```
Step 1: Count frequencies
  A: 6, B: 1, C: 2

Step 2: Check validity
  Characters with odd frequency: B (count = 1)
  Total odd = 1 <= 1, so palindrome is POSSIBLE

Step 3: Build palindrome
  Left half (count // 2 for each):
    A: 6 // 2 = 3 -> "AAA"
    C: 2 // 2 = 1 -> "C"

  Left   = "AAAC"
  Middle = "B" (odd-count character)
  Right  = reverse("AAAC") = "CAAA"

  Result = "AAAC" + "B" + "CAAA" = "AAACBCAAA"
```

### Visual Diagram

```
Input: AAAACACBA (9 characters)

Frequency Count:
  +-----+-------+--------+
  | Char| Count | Parity |
  +-----+-------+--------+
  |  A  |   6   |  even  |
  |  B  |   1   |  odd   | <- middle character
  |  C  |   2   |  even  |
  +-----+-------+--------+

Construction:
  Left half:  A A A C  (6/2=3 A's + 2/2=1 C)
  Middle:     B        (the odd-count character)
  Right half: C A A A  (mirror of left)

  Result: A A A C B C A A A
          |-----|   |-----|
           left  mid  right
```

### Code (Python)

```python
def solve():
    s = input().strip()

    # Step 1: Count frequencies
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1

    # Step 2: Check validity - count odd frequencies
    odd_char = None
    odd_count = 0

    for char, count in freq.items():
        if count % 2 == 1:
            odd_count += 1
            odd_char = char

    # More than one odd frequency -> impossible
    if odd_count > 1:
        print("NO SOLUTION")
        return

    # Step 3: Build palindrome
    left_half = []

    for char, count in freq.items():
        # Add half of each character to left side
        left_half.append(char * (count // 2))

    left = ''.join(left_half)
    middle = odd_char if odd_char else ''
    right = left[::-1]

    print(left + middle + right)

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    cin >> s;

    // Step 1: Count frequencies
    int freq[26] = {0};
    for (char c : s) {
        freq[c - 'A']++;
    }

    // Step 2: Check validity - count odd frequencies
    int oddCount = 0;
    char oddChar = '\0';

    for (int i = 0; i < 26; i++) {
        if (freq[i] % 2 == 1) {
            oddCount++;
            oddChar = 'A' + i;
        }
    }

    // More than one odd frequency -> impossible
    if (oddCount > 1) {
        cout << "NO SOLUTION" << endl;
        return 0;
    }

    // Step 3: Build palindrome
    string left = "";

    for (int i = 0; i < 26; i++) {
        // Add half of each character to left side
        left += string(freq[i] / 2, 'A' + i);
    }

    string middle = (oddChar != '\0') ? string(1, oddChar) : "";
    string right = left;
    reverse(right.begin(), right.end());

    cout << left << middle << right << endl;

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass to count frequencies, O(n) to build result |
| Space | O(n) | Store the result string; frequency array is O(26) = O(1) |

---

## Common Mistakes

### Mistake 1: Forgetting the Odd Count Rule

```python
# WRONG - Not checking odd count validity
def solve_wrong(s):
    freq = Counter(s)
    # Directly trying to build palindrome without validation
    left = ''.join(c * (freq[c] // 2) for c in freq)
    return left + left[::-1]  # Loses characters with odd counts!
```

**Problem:** If a character has an odd count, one instance is lost when doing `count // 2 * 2`.
**Fix:** First validate that at most one character has odd count, then handle the middle character.

### Mistake 2: Incorrect Middle Character Handling

```python
# WRONG - Adding ALL odd-count characters to middle
middle = ''.join(c for c, cnt in freq.items() if cnt % 2 == 1)
# This adds multiple characters to middle if multiple have odd counts
```

**Problem:** Multiple characters in the middle breaks palindrome symmetry.
**Fix:** Only one character can be in the middle. If multiple have odd counts, output "NO SOLUTION".

### Mistake 3: Off-by-One in Construction

```python
# WRONG - Forgetting to include the middle odd character
left = ''.join(c * (freq[c] // 2) for c in freq)
result = left + left[::-1]  # Missing the middle character!
```

**Problem:** If a character has odd frequency, the "extra" one must go in the middle.
**Fix:** Explicitly handle the middle character when odd_count == 1.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `A` | `A` | Already a palindrome, one odd is allowed |
| All same character | `AAAA` | `AAAA` | Even count, symmetric |
| Two different chars (both odd) | `AB` | `NO SOLUTION` | Two odd counts (A:1, B:1) |
| Two same chars | `AA` | `AA` | Even count, valid |
| Multiple odds | `ABC` | `NO SOLUTION` | Three odd counts |
| Large even palindrome | `AABB` | `ABBA` or `BAAB` | All even counts |
| All 26 letters once | `ABC...Z` | `NO SOLUTION` | 26 odd counts |

---

## When to Use This Pattern

### Use This Approach When:
- You need to check if a string can form a palindrome
- You need to rearrange characters to form a palindrome
- The problem involves character frequency analysis
- Order of input doesn't matter, only frequencies

### Don't Use When:
- You need to check if a string IS already a palindrome (use two pointers)
- You need to find palindromic substrings (use different algorithms like Manacher's)
- Character positions matter, not just frequencies

### Pattern Recognition Checklist:
- [ ] Rearranging characters to form palindrome? -> **Frequency counting**
- [ ] Check if palindrome possible? -> **Count odd frequencies <= 1**
- [ ] Need the actual palindrome? -> **Build left + middle + reversed(left)**

---

## Related Problems

| Difficulty | Problem | Key Concept |
|------------|---------|-------------|
| Easier | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Basic frequency counting |
| Similar | [Longest Palindrome](https://leetcode.com/problems/longest-palindrome/) | Max length palindrome from chars |
| Harder | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | DP + backtracking |
| Harder | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Expand around center |

---

## Key Takeaways

1. **The Core Idea:** A string can form a palindrome if and only if at most one character has an odd frequency
2. **Time Optimization:** Single pass counting + linear construction = O(n) total
3. **Space Trade-off:** O(26) for frequency array, O(n) for result string
4. **Pattern:** Frequency counting + greedy construction for palindrome problems

---

## Practice Checklist

- [ ] Explain why at most one odd frequency is allowed
- [ ] Construct a palindrome from character frequencies
- [ ] Implement in under 10 minutes without reference
