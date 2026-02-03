# Palindromic characteristics

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

## Problem Statement

The palindromic characteristics of string s is a sequence of |s| integers, where the k-th number is the count of non-empty substrings that are k-palindromes.

A string is a 1-palindrome if it reads the same forward and backward.
A string is a k-palindrome (k > 1) if:
1. Its left half equals its right half
2. Both halves are (k-1)-palindromes

Count the number of k-palindrome substrings for each k from 1 to |s|.

## Input Format
- Single line: string s (1 ≤ |s| ≤ 5000, lowercase)

## Output Format
Print |s| integers - the palindromic characteristics.

## Solution

### Approach
1. First, find all palindromic substrings using Manacher's or DP
2. For each palindrome, compute its k-level
3. A palindrome of length L has k-level = 1 + k-level of its half (if half is palindrome)

Use DP:
- is_pal[i][j] = true if s[i:j+1] is palindrome
- k_level[i][j] = k-palindrome level of s[i:j+1]

### Python Solution

```python
def solve():
    s = input().strip()
    n = len(s)

    if n == 0:
        return

    # is_pal[i][j] = True if s[i:j+1] is palindrome
    is_pal = [[False] * n for _ in range(n)]

    # Base cases: single characters
    for i in range(n):
        is_pal[i][i] = True

    # Length 2
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])

    # Longer palindromes
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]

    # k_level[i][j] = k-palindrome level
    k_level = [[0] * n for _ in range(n)]

    # Compute k-levels for all palindromes
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if is_pal[i][j]:
                if length == 1:
                    k_level[i][j] = 1
                else:
                    # Half length
                    half_len = length // 2
                    half_end = i + half_len - 1
                    # Left half is s[i:i+half_len]
                    k_level[i][j] = 1 + k_level[i][half_end]

    # Count palindromes at each k-level
    count = [0] * (n + 1)

    for i in range(n):
        for j in range(i, n):
            if is_pal[i][j]:
                count[k_level[i][j]] += 1

    # A k-palindrome is also a (k-1)-palindrome, etc.
    # Propagate counts downward
    for k in range(n, 1, -1):
        count[k - 1] += count[k]

    # Output counts for k = 1 to n
    print(' '.join(map(str, count[1:n + 1])))

if __name__ == "__main__":
    solve()
```

### Optimized Solution

```python
def solve():
    s = input().strip()
    n = len(s)

    # is_pal[i][j] = True if s[i:j+1] is palindrome
    is_pal = [[False] * n for _ in range(n)]

    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]

    # k_level for each palindrome
    k_level = [[0] * n for _ in range(n)]

    # Process by increasing length to use computed half values
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if is_pal[i][j]:
                if length == 1:
                    k_level[i][j] = 1
                else:
                    half = (length - 1) // 2
                    # Left half: s[i : i + half + 1]
                    k_level[i][j] = 1 + k_level[i][i + half]

    # Count by k-level
    count = [0] * (n + 2)
    for i in range(n):
        for j in range(i, n):
            if is_pal[i][j]:
                count[k_level[i][j]] += 1

    # Propagate: k-palindrome is also (k-1)-palindrome
    for k in range(n, 0, -1):
        count[k - 1] += count[k]

    print(' '.join(map(str, count[1:n + 1])))

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(n²)
- **Space Complexity:** O(n²)

### Key Insight
First find all palindromic substrings with standard DP. Then compute k-levels: a palindrome's k-level is 1 + k-level of its left half (if half is also a palindrome). Finally, since a k-palindrome is also (k-1), (k-2), ... 1-palindrome, propagate counts downward.
