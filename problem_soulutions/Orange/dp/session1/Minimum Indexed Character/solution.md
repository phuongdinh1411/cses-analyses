# Minimum Indexed Character

## Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a string `str` and another string `patt`. Find the character in `patt` that is present at the minimum index in `str`. If no character of `patt` is present in `str` then print "No character present".

## Input Format
- The first line of input contains an integer T denoting the number of test cases.
- Each test case contains two strings `str` and `patt` respectively.
- 1 ≤ T ≤ 10^5
- The total length of two strings in all test cases is not larger than 2 × 10^5.

## Output Format
Output the character in `patt` that is present at the minimum index in `str`. Print "No character present" (without quotes) if no character of `patt` is present in `str`.

## Example
```
Input:
2
geeksforgeeks gek
adcba bc

Output:
g
c
```
Test 1: In "geeksforgeeks", characters g, e, k from pattern appear at indices 0, 1, 3. The minimum index is 0 (character 'g').
Test 2: In "adcba", 'c' first appears at index 2 and 'b' at index 3, so the answer is 'c'.

## Solution

### Approach
1. Record the first index of each character of `str` in a dictionary.
2. Among the characters of `patt` that occur in `str`, print the one with the smallest recorded index.
3. If none occur, print "No character present".

Do not just return the first character of `patt` found in `str`. That answers a different question: for "adcba" and "bc" it would give 'b', but 'c' occurs earlier.

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    str_input, patt = input().split()

    # Map each character to its first occurrence index in str using enumerate
    char_index = {}
    for i, char in enumerate(str_input):
      if char not in char_index:
        char_index[char] = i

    # Find character in patt with minimum index in str using min with key
    valid_chars = [c for c in patt if c in char_index]

    if valid_chars:
      print(min(valid_chars, key=lambda c: char_index[c]))
    else:
      print("No character present")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(|str| + |patt|) per test case
- **Space Complexity:** O(|str|) for the character set

### Key Insight
The problem asks for the character from `patt` that appears at the minimum index in `str`. This is equivalent to finding the first character in `patt` that exists anywhere in `str`, since we iterate through `patt` in order and the first match will have the smallest index in our iteration (which corresponds to appearing earliest in `patt`, but the actual requirement is minimum index in `str`).

Note: The wording is slightly ambiguous - if we need the character that appears earliest in `str` (regardless of order in `patt`), we would use the alternative solution that tracks actual indices.
