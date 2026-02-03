---
layout: simple
title: "Digit Queries - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/digit_queries_analysis
difficulty: Medium
tags: [math, digit-counting, number-theory, binary-search]
prerequisites: []
---

# Digit Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Math / Number Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Digit Counting by Range |
| **CSES Link** | [Digit Queries](https://cses.fi/problemset/task/2431) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how to count digits in number ranges (1-digit, 2-digit, etc.)
- [ ] Calculate which number contains a specific digit position
- [ ] Handle 1-indexed positions correctly
- [ ] Apply mathematical analysis to avoid brute force enumeration

---

## Problem Statement

**Problem:** Consider an infinite string formed by concatenating all positive integers: "123456789101112131415...". Given a position k, find the digit at that position.

**Input:**
- Line 1: q - number of queries
- Lines 2 to q+1: k - position to query (1-indexed)

**Output:**
- For each query, print the digit at position k

**Constraints:**
- 1 <= q <= 1000
- 1 <= k <= 10^18

### Example

```
Input:
3
7
19
12

Output:
7
4
1
```

**Explanation:**
- Position 7: The string is "1234567..." so position 7 is '7'
- Position 19: The string is "12345678910111213141..." - position 19 is '4' (from "14")
- Position 12: The string is "123456789101..." - position 12 is '1' (from "11")

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we find the digit at position k without building the entire string?

The key insight is that numbers can be grouped by their digit length. All 1-digit numbers (1-9) contribute exactly 9 digits. All 2-digit numbers (10-99) contribute 90 x 2 = 180 digits. This pattern lets us quickly narrow down which "range" contains position k.

### Breaking Down the Problem

1. **What are we looking for?** The digit at position k in the infinite concatenated string.
2. **What information do we have?** The position k (1-indexed).
3. **What's the relationship between input and output?** We need to find which number contains position k, then extract the specific digit.

### Digit Counting by Range

| Digit Length | Number Range | Count of Numbers | Total Digits |
|--------------|--------------|------------------|--------------|
| 1 | 1 - 9 | 9 | 9 x 1 = 9 |
| 2 | 10 - 99 | 90 | 90 x 2 = 180 |
| 3 | 100 - 999 | 900 | 900 x 3 = 2700 |
| d | 10^(d-1) to 10^d - 1 | 9 x 10^(d-1) | 9 x 10^(d-1) x d |

### Analogies

Think of this like finding a word in a book where:
- Chapter 1 has 9 one-letter words (positions 1-9)
- Chapter 2 has 90 two-letter words (positions 10-189)
- Chapter 3 has 900 three-letter words (positions 190-2889)

To find which word contains position k, first find the chapter, then the word, then the letter.

---

## Solution 1: Brute Force

### Idea

Generate the string character by character until we reach position k.

### Algorithm

1. Start with an empty string
2. Append each positive integer (1, 2, 3, ...) to the string
3. Stop when the string length reaches k
4. Return the character at position k-1 (0-indexed)

### Code

```python
def solve_brute_force(k):
    """
    Brute force solution - generates string until position k.

    Time: O(k)
    Space: O(k)
    """
    s = ""
    num = 1
    while len(s) < k:
        s += str(num)
        num += 1
    return int(s[k - 1])
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(k) | Must generate all digits up to position k |
| Space | O(k) | Stores entire string up to position k |

### Why This Works (But Is Slow)

This correctly builds the string and returns the right digit, but with k up to 10^18, we cannot possibly generate that many characters. We need a mathematical approach.

---

## Solution 2: Optimal Solution (Mathematical Analysis)

### Key Insight

> **The Trick:** Group numbers by digit length, skip entire groups, then pinpoint the exact number and digit.

### Algorithm

1. **Find the digit length range:** Determine how many digits the target number has
2. **Find the exact number:** Calculate which number in that range contains position k
3. **Find the exact digit:** Determine which digit within that number

### Step-by-Step Approach

```
For position k:

Step 1: Find digit length (len)
  - 1-digit numbers cover positions 1 to 9
  - 2-digit numbers cover positions 10 to 189
  - Keep subtracting until k falls within a range

Step 2: Find the number (num)
  - first_num = 10^(len-1)  (first number with 'len' digits)
  - num = first_num + (k - 1) / len

Step 3: Find the digit position within num
  - digit_pos = (k - 1) % len
  - Return digit at that position
```

### Dry Run Example

Let's trace through with `k = 19`:

```
Initial: k = 19

Step 1: Find digit length
  Len=1: count = 9 * 1 = 9 digits (positions 1-9)
         k = 19 > 9, so subtract: k = 19 - 9 = 10
         Move to len=2

  Len=2: count = 90 * 2 = 180 digits (positions 10-189)
         k = 10 <= 180, so we're in the 2-digit range
         Final: len = 2, k = 10 (position within 2-digit numbers)

Step 2: Find the number
  first_num = 10^(2-1) = 10
  number_index = (10 - 1) / 2 = 9 / 2 = 4
  num = 10 + 4 = 14

Step 3: Find the digit
  digit_pos = (10 - 1) % 2 = 9 % 2 = 1
  str(14)[1] = '4'

Result: 4
```

### Visual Diagram

```
Position:  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ...
String:    1 2 3 4 5 6 7 8 9 1  0  1  1  1  2  1  3  1  4  1  5 ...
                             |--10-|--11-|--12-|--13-|--14-|--15-|
                                                          ^
                                                     k=19 = '4'

Digit Ranges:
  1-digit: positions  1 -  9   (9 positions)
  2-digit: positions 10 - 189  (180 positions)
  3-digit: positions 190 - 2889 (2700 positions)
```

### Code

**Python Solution:**

```python
def solve(k):
    """
    Optimal solution using digit counting by range.

    Time: O(log k) - number of digit lengths is O(log k)
    Space: O(1) - only using a few variables
    """
    # Step 1: Find the digit length containing position k
    digit_len = 1
    count = 9  # 9 one-digit numbers
    start = 1  # first number with current digit length

    while k > digit_len * count:
        k -= digit_len * count
        digit_len += 1
        count *= 10
        start *= 10

    # Step 2: Find which number contains position k
    # k is now 1-indexed position within the current digit-length range
    number_index = (k - 1) // digit_len
    num = start + number_index

    # Step 3: Find which digit within the number
    digit_index = (k - 1) % digit_len

    return int(str(num)[digit_index])


def main():
    q = int(input())
    for _ in range(q):
        k = int(input())
        print(solve(k))


if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int solve(long long k) {
    // Step 1: Find the digit length containing position k
    int digit_len = 1;
    long long count = 9;  // 9 one-digit numbers
    long long start = 1;  // first number with current digit length

    while (k > digit_len * count) {
        k -= digit_len * count;
        digit_len++;
        count *= 10;
        start *= 10;
    }

    // Step 2: Find which number contains position k
    // k is now 1-indexed position within the current digit-length range
    long long number_index = (k - 1) / digit_len;
    long long num = start + number_index;

    // Step 3: Find which digit within the number
    int digit_index = (k - 1) % digit_len;

    string num_str = to_string(num);
    return num_str[digit_index] - '0';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;

    while (q--) {
        long long k;
        cin >> k;
        cout << solve(k) << "\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(log k) | Loop runs once per digit length, max ~19 for k <= 10^18 |
| Space | O(1) | Only stores a few variables (string conversion is O(log k) but constant) |

---

## Common Mistakes

### Mistake 1: Off-by-One with 1-Indexed Positions

```python
# WRONG - treating k as 0-indexed
number_index = k // digit_len
digit_index = k % digit_len

# CORRECT - k is 1-indexed, so subtract 1
number_index = (k - 1) // digit_len
digit_index = (k - 1) % digit_len
```

**Problem:** CSES problems typically use 1-indexed positions.
**Fix:** Always subtract 1 before dividing to convert to 0-indexed calculations.

### Mistake 2: Incorrect Digit Range Boundaries

```python
# WRONG - confusing count vs total digits
while k > count:  # count is number of numbers, not digits!
    k -= count
    ...

# CORRECT - multiply count by digit_len to get total digits
while k > digit_len * count:
    k -= digit_len * count
    ...
```

**Problem:** Mixing up "number of numbers" with "number of digits".
**Fix:** Total digits in a range = (count of numbers) x (digits per number).

### Mistake 3: Integer Overflow

```cpp
// WRONG - int can overflow for large k
int k, count = 9, start = 1;

// CORRECT - use long long
long long k, count = 9, start = 1;
```

**Problem:** With k up to 10^18, intermediate calculations can overflow 32-bit integers.
**Fix:** Use `long long` in C++ or Python's arbitrary precision integers.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| First position | k = 1 | 1 | First digit is '1' |
| Last 1-digit | k = 9 | 9 | Position 9 is '9' |
| First 2-digit | k = 10 | 1 | Position 10 is '1' from "10" |
| Transition point | k = 189 | 9 | Last digit of "99" |
| Start of 3-digit | k = 190 | 1 | First digit of "100" |
| Very large k | k = 10^18 | varies | Must handle without overflow |

---

## When to Use This Pattern

### Use This Approach When:
- You need to find positions in concatenated number sequences
- The position k is too large to simulate
- Numbers follow a predictable length pattern

### Don't Use When:
- The sequence has irregular patterns (not consecutive integers)
- k is small enough for brute force (k < 10^6)
- Numbers are not grouped by digit length

### Pattern Recognition Checklist:
- [ ] Infinite or very large concatenated string? -> **Consider digit counting**
- [ ] Numbers grouped by length (1-digit, 2-digit, ...)? -> **Use range analysis**
- [ ] Need to find position without building string? -> **Mathematical approach**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Trailing Zeros](https://cses.fi/problemset/task/1618) | Basic math/counting problem |
| [Number Spiral](https://cses.fi/problemset/task/1071) | Mathematical position finding |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [LeetCode - Nth Digit](https://leetcode.com/problems/nth-digit/) | Same problem, different constraints |
| [Counting Digits](https://cses.fi/problemset/task/2220) | Count occurrences of digits 0-9 |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LeetCode - Find Kth Bit](https://leetcode.com/problems/find-kth-bit-in-nth-binary-string/) | Recursive string construction |
| [Magic String](https://leetcode.com/problems/magical-string/) | Self-describing sequences |

---

## Key Takeaways

1. **The Core Idea:** Group numbers by digit length to skip entire ranges at once.
2. **Time Optimization:** From O(k) brute force to O(log k) by mathematical analysis.
3. **Space Trade-off:** O(1) space since we calculate positions instead of building strings.
4. **Pattern:** This is a classic "digit counting" problem - recognize it by concatenated number sequences.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Calculate digit counts for any range (1-digit, 2-digit, etc.)
- [ ] Handle 1-indexed positions correctly
- [ ] Explain why the time complexity is O(log k)

---

## Additional Resources

- [CP-Algorithms: Digit DP](https://cp-algorithms.com/dynamic_programming/digit_dp.html)
- [CSES Problem Set](https://cses.fi/problemset/)
- [Wikipedia: Champernowne Constant](https://en.wikipedia.org/wiki/Champernowne_constant) - The mathematical sequence this problem is based on
