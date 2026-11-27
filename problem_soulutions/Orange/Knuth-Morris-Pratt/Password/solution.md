# Password

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Given string s, find the longest substring t that is:
1. A prefix of s
2. A suffix of s
3. Appears somewhere in the middle of s (not at the very beginning or end)

If no such substring exists, print "Just a legend".

## Input Format
- Single line: string s (length 1 to 10⁶), consisting of lowercase Latin letters

## Output Format
Print the substring t, or "Just a legend" if it doesn't exist.

## Example
```
Input:
fixprefixsuffix

Output:
fix
```
"fix" is a prefix (starts at position 0), a suffix (ends at last position), and appears in the middle as part of "prefix". It satisfies all three conditions.

```
Input:
abcdabc

Output:
Just a legend
```
"abc" is both prefix and suffix, but doesn't appear in the middle (positions 1-5).

## Solution

### Approach
Let `pi` be the KMP prefix function and `border = pi[n-1]`, the longest prefix that is also a suffix.
1. If some `pi[i]` with i < n-1 is at least `border`, then a copy of `s[:border]` ends at i. That copy is neither the prefix nor the suffix, so `border` is the answer.
2. Otherwise try the next-shorter border, `pi[border-1]`. It occurs inside the copy of `s[:border]` that sits at the end of the string, so it is automatically in the middle.
3. If neither exists, print "Just a legend".

### Python Solution

```python
def solve():
  s = input().strip()
  n = len(s)
  pi = [0] * n
  for i in range(1, n):
    j = pi[i - 1]
    while j > 0 and s[i] != s[j]:
      j = pi[j - 1]
    if s[i] == s[j]:
      j += 1
    pi[i] = j

  border = pi[-1]
  if border and max(pi[:-1]) >= border:
    print(s[:border])
  elif border and pi[border - 1]:
    print(s[:pi[border - 1]])
  else:
    print("Just a legend")


if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

### Key Insight
The candidates are the chain of borders `pi[n-1]`, `pi[pi[n-1]-1]`, and so on, and only the top two ever matter. The longest border wins if any interior `pi[i]` reaches it. Otherwise the second border always works, because it occurs inside the suffix copy of the first.

