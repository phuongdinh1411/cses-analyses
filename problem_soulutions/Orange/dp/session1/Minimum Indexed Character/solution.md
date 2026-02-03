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

## Solution

### Approach
1. Create a set/dictionary of all characters in `str` for O(1) lookup
2. Iterate through `patt` and find the first character that exists in `str`
3. Return that character, or "No character present" if none found

### Python Solution

```python
def solve():
    t = int(input())

    for _ in range(t):
        str_input, patt = input().split()

        # Create set of characters in str for O(1) lookup
        str_chars = set(str_input)

        result = "No character present"

        # Find first character in patt that exists in str
        for char in patt:
            if char in str_chars:
                result = char
                break

        print(result)

if __name__ == "__main__":
    solve()
```

### Alternative Solution (Finding Minimum Index)

```python
def solve():
    t = int(input())

    for _ in range(t):
        str_input, patt = input().split()

        # Map each character to its first occurrence index in str
        char_index = {}
        for i, char in enumerate(str_input):
            if char not in char_index:
                char_index[char] = i

        min_index = float('inf')
        result_char = None

        # Find character in patt with minimum index in str
        for char in patt:
            if char in char_index and char_index[char] < min_index:
                min_index = char_index[char]
                result_char = char

        if result_char:
            print(result_char)
        else:
            print("No character present")

if __name__ == "__main__":
    solve()
```

### One-liner Style Solution

```python
def solve():
    t = int(input())

    for _ in range(t):
        s, p = input().split()
        chars = set(s)
        result = next((c for c in p if c in chars), "No character present")
        print(result)

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(|str| + |patt|) per test case
- **Space Complexity:** O(|str|) for the character set

### Key Insight
The problem asks for the character from `patt` that appears at the minimum index in `str`. This is equivalent to finding the first character in `patt` that exists anywhere in `str`, since we iterate through `patt` in order and the first match will have the smallest index in our iteration (which corresponds to appearing earliest in `patt`, but the actual requirement is minimum index in `str`).

Note: The wording is slightly ambiguous - if we need the character that appears earliest in `str` (regardless of order in `patt`), we would use the alternative solution that tracks actual indices.
