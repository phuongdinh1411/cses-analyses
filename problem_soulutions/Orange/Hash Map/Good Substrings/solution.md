# Good Substrings

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

You've got string s, consisting of small English letters. Some of the English letters are good, the rest are bad.

A substring s[l...r] (1 ≤ l ≤ r ≤ |s|) of string s = s1s2...s|s| (where |s| is the length of string s) is string sl, sl+1, ..., sr.

The substring s[l...r] is good, if among the letters sl, sl+1, ..., sr there are at most k bad ones.

Your task is to find the number of distinct good substrings of the given string s. Two substrings s[x...y] and s[p...q] are considered distinct if their content is different, i.e. s[x...y] ≠ s[p...q].

## Input Format
- The first line of the input is the non-empty string s, consisting of small English letters, the string's length is at most 1500 characters.
- The second line of the input is the string of characters 0 and 1, the length is exactly 26 characters. Character equals 1 means the i-th English letter is good, otherwise it's bad.
- The third line of the input consists a single integer k (0 ≤ k ≤ |s|) - the maximum acceptable number of bad characters in a good substring.

## Output Format
Print a single integer - the number of distinct good substrings of string s.

## Solution

### Approach
We need to count distinct substrings with at most k bad characters. Two approaches:

1. **Hash Set**: Store all good substrings in a set and count unique ones
2. **Trie**: Use a Trie to efficiently store and count unique substrings

The Trie approach is more efficient for this problem.

### Python Solution using Set

```python
def solve():
 s = input().strip()
 good_bad = input().strip()
 k = int(input())

 def is_bad(c):
  return good_bad[ord(c) - ord('a')] == '0'

 n = len(s)
 good_substrings = set()

 for i in range(n):
  bad_count = 0
  substring = ""
  for j in range(i, n):
   substring += s[j]
   if is_bad(s[j]):
    bad_count += 1

   if bad_count > k:
    break

   good_substrings.add(substring)

 print(len(good_substrings))

if __name__ == "__main__":
 solve()
```

### Python Solution using Trie (More Efficient)

```python
class TrieNode:
 def __init__(self):
  self.children = {}
  self.is_end = False

def solve():
 s = input().strip()
 good_bad = input().strip()
 k = int(input())

 def is_bad(c):
  return good_bad[ord(c) - ord('a')] == '0'

 n = len(s)
 root = TrieNode()
 count = 0

 for i in range(n):
  bad_count = 0
  node = root

  for j in range(i, n):
   c = s[j]
   if is_bad(c):
    bad_count += 1

   if bad_count > k:
    break

   if c not in node.children:
    node.children[c] = TrieNode()
    count += 1  # New unique substring found

   node = node.children[c]

 print(count)

if __name__ == "__main__":
 solve()
```

### Python Solution using Rolling Hash

```python
def solve():
 s = input().strip()
 good_bad = input().strip()
 k = int(input())

 def is_bad(c):
  return good_bad[ord(c) - ord('a')] == '0'

 n = len(s)
 MOD = 10**18 + 9
 BASE = 31

 good_substrings = set()

 for i in range(n):
  bad_count = 0
  hash_val = 0
  power = 1

  for j in range(i, n):
   if is_bad(s[j]):
    bad_count += 1

   if bad_count > k:
    break

   # Rolling hash
   hash_val = (hash_val * BASE + ord(s[j]) - ord('a') + 1) % MOD
   good_substrings.add((j - i + 1, hash_val))  # (length, hash) pair

 print(len(good_substrings))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(n²) for generating all substrings
- **Space Complexity:** O(n²) in worst case for storing substrings

### Key Insight
Using a Trie allows us to efficiently detect when a new unique substring is found - it happens exactly when we create a new node in the Trie.
