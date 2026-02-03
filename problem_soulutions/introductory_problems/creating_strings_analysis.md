---
layout: simple
title: "Creating Strings - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/creating_strings_analysis
difficulty: Easy
tags: [backtracking, permutations, strings, recursion]
prerequisites: []
---

# Creating Strings

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Backtracking / Strings |
| **Time Limit** | 1 second |
| **Key Technique** | Backtracking with Frequency Counting |
| **CSES Link** | [Creating Strings](https://cses.fi/problemset/task/1622) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Generate all unique permutations of a string with duplicate characters
- [ ] Use character frequency counting to avoid generating duplicate permutations
- [ ] Apply backtracking to enumerate all valid solutions
- [ ] Ensure lexicographic ordering in permutation generation

---

## Problem Statement

**Problem:** Given a string, your task is to generate all different strings that can be created using its characters.

**Input:**
- Line 1: A string of length n

**Output:**
- Line 1: The number of strings
- Following lines: The strings in alphabetical order

**Constraints:**
- 1 <= n <= 8
- String contains only lowercase letters a-z

### Example

```
Input:
aabac

Output:
20
aaabc
aaacb
aabac
aabca
aacab
aacba
abaac
abaca
abcaa
acaab
acaba
acbaa
baaac
baaca
bacaa
bcaaa
caaab
caaba
cabaa
cbaaa
```

**Explanation:** The string "aabac" has 5 characters with frequencies: a=3, b=1, c=1. The total unique permutations = 5!/(3!*1!*1!) = 120/6 = 20.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we generate all permutations while handling duplicate characters efficiently?

The key insight is that if we simply generate all permutations (like using `itertools.permutations`), we will create duplicate strings when the input has repeated characters. For example, "aab" has 3! = 6 permutations of positions, but only 3 unique strings.

### Breaking Down the Problem

1. **What are we looking for?** All unique arrangements of characters
2. **What information do we have?** The input string and its character frequencies
3. **What's the relationship between input and output?** The number of unique permutations = n! / (f1! * f2! * ... * fk!) where fi is the frequency of each character

### Analogies

Think of this problem like arranging colored balls in a row. If you have 2 red balls and 1 blue ball, swapping the two red balls doesn't create a new arrangement. We only care about which color is in which position, not which specific ball.

---

## Solution 1: Brute Force (Generate and Deduplicate)

### Idea

Generate all n! permutations, store them in a set to remove duplicates, then sort.

### Algorithm

1. Generate all permutations using standard library
2. Add each permutation to a set (automatically removes duplicates)
3. Sort the unique permutations
4. Output the count and sorted list

### Code

```python
def solve_brute_force(s):
    """
    Brute force: generate all permutations, deduplicate with set.

    Time: O(n! * n) - generate all permutations, each of length n
    Space: O(n! * n) - store all unique permutations
    """
    from itertools import permutations

    # Generate all permutations and deduplicate
    unique = set(''.join(p) for p in permutations(s))

    # Sort lexicographically
    result = sorted(unique)

    return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * n) | Generate n! permutations, each string comparison is O(n) |
| Space | O(n! * n) | Store all unique permutations |

### Why This Works (But Is Inefficient)

This approach is correct because a set automatically removes duplicates. However, it's inefficient because we generate all n! permutations even when many are duplicates. For "aaaaaaaa" (8 a's), we generate 8! = 40320 permutations just to keep 1 unique result.

---

## Solution 2: Optimal - Backtracking with Frequency Counting

### Key Insight

> **The Trick:** Instead of tracking which positions we've used, track how many of each character we've used. This naturally avoids generating duplicates.

By iterating through characters in sorted order and using each character only as many times as it appears, we:
1. Never generate duplicates (same character sequence)
2. Automatically produce output in lexicographic order

### Algorithm

1. Count frequency of each character
2. Get sorted list of unique characters
3. Use backtracking to build permutations:
   - At each position, try each character that still has remaining count
   - Recurse with decreased count
   - Restore count when backtracking
4. When current string length equals input length, we have a complete permutation

### Dry Run Example

Let's trace through with input `s = "aab"`:

```
Initial state:
  char_count = {'a': 2, 'b': 1}
  chars = ['a', 'b']  (sorted unique characters)
  result = []

Backtrack(current=""):
  Position 0, try each available char:

  Try 'a': count['a']=2 > 0, use it
    count['a'] = 1
    Backtrack(current="a"):
      Position 1, try each available char:

      Try 'a': count['a']=1 > 0, use it
        count['a'] = 0
        Backtrack(current="aa"):
          Position 2, try each available char:

          Try 'a': count['a']=0, SKIP
          Try 'b': count['b']=1 > 0, use it
            count['b'] = 0
            Backtrack(current="aab"):
              len("aab") == 3, COMPLETE!
              result.append("aab")
            count['b'] = 1 (restore)
        count['a'] = 1 (restore)

      Try 'b': count['b']=1 > 0, use it
        count['b'] = 0
        Backtrack(current="ab"):
          Position 2, try each available char:

          Try 'a': count['a']=1 > 0, use it
            Backtrack(current="aba"):
              len("aba") == 3, COMPLETE!
              result.append("aba")
        count['b'] = 1 (restore)
    count['a'] = 2 (restore)

  Try 'b': count['b']=1 > 0, use it
    count['b'] = 0
    Backtrack(current="b"):
      Position 1, try each available char:

      Try 'a': count['a']=2 > 0, use it
        count['a'] = 1
        Backtrack(current="ba"):
          Try 'a': count['a']=1 > 0
            Backtrack(current="baa"):
              len("baa") == 3, COMPLETE!
              result.append("baa")
    count['b'] = 1 (restore)

Final result: ["aab", "aba", "baa"]
```

### Visual Diagram

```
Decision Tree for "aab":

                    ""
                   / \
                 'a'  'b'
                 /      \
              "a"       "b"
             /   \        \
           'a'   'b'      'a'
           /       \        \
        "aa"      "ab"     "ba"
          |         |        |
         'b'       'a'      'a'
          |         |        |
       "aab"     "aba"    "baa"
          |         |        |
       OUTPUT    OUTPUT   OUTPUT

Note: Each branch only uses available characters
      Sorted char order ensures lexicographic output
```

### Code

**Python Solution:**

```python
def solve(s):
    """
    Optimal solution using backtracking with character frequency.

    Time: O(n! / (f1! * f2! * ... * fk!)) - only unique permutations
    Space: O(n) - recursion depth + character count storage
    """
    from collections import Counter

    n = len(s)
    char_count = Counter(s)
    chars = sorted(char_count.keys())  # Sorted for lexicographic order
    result = []

    def backtrack(current):
        if len(current) == n:
            result.append(current)
            return

        for c in chars:
            if char_count[c] > 0:
                char_count[c] -= 1
                backtrack(current + c)
                char_count[c] += 1

    backtrack("")
    return result


def main():
    s = input().strip()
    result = solve(s)
    print(len(result))
    print('\n'.join(result))


if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
string s;
map<char, int> charCount;
vector<char> chars;
vector<string> result;

void backtrack(string& current) {
    if (current.length() == n) {
        result.push_back(current);
        return;
    }

    for (char c : chars) {
        if (charCount[c] > 0) {
            charCount[c]--;
            current.push_back(c);
            backtrack(current);
            current.pop_back();
            charCount[c]++;
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> s;
    n = s.length();

    // Count character frequencies
    for (char c : s) {
        charCount[c]++;
    }

    // Get sorted unique characters
    for (auto& p : charCount) {
        chars.push_back(p.first);
    }

    // Generate permutations
    string current = "";
    backtrack(current);

    // Output
    cout << result.size() << "\n";
    for (const string& str : result) {
        cout << str << "\n";
    }

    return 0;
}
```

**Alternative C++ using next_permutation:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string s;
    cin >> s;

    // Sort to start from lexicographically smallest
    sort(s.begin(), s.end());

    vector<string> result;
    do {
        result.push_back(s);
    } while (next_permutation(s.begin(), s.end()));

    cout << result.size() << "\n";
    for (const string& str : result) {
        cout << str << "\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(k * P) where P = n!/(f1!*...*fk!) | P unique permutations, k characters to try at each step |
| Space | O(n + P*n) | Recursion depth O(n), result storage O(P*n) |

For the worst case (all unique characters), P = n! which matches brute force. But for strings with duplicates, this is significantly faster.

---

## Common Mistakes

### Mistake 1: Not Handling Duplicates

```python
# WRONG - generates duplicate permutations
def wrong_solve(s, index, current, result):
    if index == len(s):
        result.append(current)
        return
    for i in range(len(s)):
        if not used[i]:
            used[i] = True
            wrong_solve(s, index + 1, current + s[i], result)
            used[i] = False
```

**Problem:** Treating positions as distinct means swapping two 'a's creates a "new" permutation.
**Fix:** Use character frequency counting instead of position tracking.

### Mistake 2: Forgetting to Sort for Lexicographic Order

```python
# WRONG - output may not be in alphabetical order
char_count = Counter(s)
for c in char_count:  # Dictionary order, not alphabetical!
    if char_count[c] > 0:
        ...
```

**Problem:** Iterating over a Counter doesn't guarantee alphabetical order.
**Fix:** Sort the unique characters: `chars = sorted(char_count.keys())`

### Mistake 3: String Concatenation in Hot Loop (Python)

```python
# INEFFICIENT
def backtrack(current):  # current is a string
    ...
    backtrack(current + c)  # Creates new string each time
```

**Problem:** String concatenation creates a new string object each time, O(n) per operation.
**Fix:** Use a list and join at the end, or accept the overhead for small n (n <= 8 is fine).

### Mistake 4: Not Restoring State After Backtracking

```python
# WRONG - count never restored
char_count[c] -= 1
backtrack(current + c)
# Missing: char_count[c] += 1
```

**Problem:** After returning from recursion, the character count stays decremented.
**Fix:** Always restore state after the recursive call.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `a` | `1\na` | Only one permutation possible |
| All same characters | `aaaa` | `1\naaaa` | Only one unique arrangement |
| All unique characters | `abc` | `6\nabc\nacb\nbac\nbca\cab\ncba` | Full 3! = 6 permutations |
| Two characters | `ab` | `2\nab\nba` | Simple swap |
| Maximum length, all same | `aaaaaaaa` | `1\naaaaaaaa` | Worst case for brute force |
| Maximum length, all unique | `abcdefgh` | `40320\n...` | 8! = 40320 permutations |

---

## When to Use This Pattern

### Use Backtracking with Frequency Counting When:
- Generating permutations with repeated elements
- You need output in a specific order (lexicographic)
- The state can be represented by counts rather than positions
- Pruning identical branches is important for efficiency

### Use Standard Library (next_permutation) When:
- Implementation simplicity is preferred
- The language provides efficient built-in support
- String length is small (n <= 8)

### Pattern Recognition Checklist:
- [ ] Need all arrangements of elements? -> **Permutation problem**
- [ ] Elements can repeat? -> **Use frequency counting**
- [ ] Need lexicographic order? -> **Sort characters first**
- [ ] Want to avoid duplicates? -> **Track counts, not positions**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Permutations (LeetCode 46)](https://leetcode.com/problems/permutations/) | Basic permutation without duplicates |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Permutations II (LeetCode 47)](https://leetcode.com/problems/permutations-ii/) | Same concept with array input |
| [Apple Division (CSES)](https://cses.fi/problemset/task/1623) | Backtracking to enumerate subsets |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Chessboard and Queens (CSES)](https://cses.fi/problemset/task/1624) | Backtracking with constraints |
| [Grid Paths (CSES)](https://cses.fi/problemset/task/1625) | Backtracking with pruning |
| [Letter Combinations (LeetCode 17)](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Backtracking with multiple choices per position |

---

## Key Takeaways

1. **The Core Idea:** Use character frequencies instead of position tracking to naturally avoid duplicates
2. **Time Optimization:** Only generate each unique permutation once, not n! / k! redundant ones
3. **Space Trade-off:** O(n) for recursion depth vs O(n!) for storing all permutations
4. **Pattern:** Classic backtracking with state represented as frequency counts

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why frequency counting avoids duplicates
- [ ] Implement in both Python and C++ in under 10 minutes
- [ ] Calculate the number of unique permutations using the formula n!/(f1!*f2!*...*fk!)
- [ ] Identify when to use this pattern in new problems

---

## Additional Resources

- [CP-Algorithms: Generating Permutations](https://cp-algorithms.com/combinatorics/generating_permutations.html)
- [CSES Creating Strings I](https://cses.fi/problemset/task/1622) - Generate permutations
- [Backtracking Tutorial](https://cp-algorithms.com/others/backtracking.html)
