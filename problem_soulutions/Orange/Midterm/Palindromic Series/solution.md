# Palindromic Series

## Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Adobe is given a number N. He has to create an alphabetical string in lowercase from that number and check if it's a palindrome.

The mapping is: a = 0, b = 1, c = 2, ..., j = 9

For example: If the number is 61:
- The substring is "gb" (g=6, b=1)
- The length is 7 (6 + 1 = 7)
- Repeat "gb" to get 7 characters: "gbgbgbg"
- Check if "gbgbgbg" is a palindrome

**Note:** No number starts with zero. Consider alphabets a to j only (single digit numbers 0-9).

## Input Format
- First line: T (number of test cases)
- Each test case: A number N

## Constraints
- 1 ≤ T ≤ 10000
- 1 ≤ N ≤ 10^7

## Output Format
For each test case, print "YES" if the string is palindrome, "NO" otherwise.

## Solution

### Approach
1. Extract digits from N and compute their sum (length of final string)
2. Build the string by repeating the digits cyclically until reaching the sum length
3. Check if the resulting string is a palindrome

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = input().strip()
    digits = [int(d) for d in n]
    length = sum(digits)

    # Build string of given length by repeating digits
    result = []
    idx = 0
    for i in range(length):
      result.append(digits[idx])
      idx = (idx + 1) % len(digits)

    # Check palindrome
    is_palindrome = result == result[::-1]
    print("YES" if is_palindrome else "NO")

if __name__ == "__main__":
  solve()
```

### Optimized Solution (Without Building Full String)

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = input().strip()
    digits = [int(d) for d in n]
    length = sum(digits)
    num_digits = len(digits)

    # Check palindrome without building full string
    is_palindrome = True
    for i in range(length // 2):
      left_digit = digits[i % num_digits]
      right_digit = digits[(length - 1 - i) % num_digits]
      if left_digit != right_digit:
        is_palindrome = False
        break

    print("YES" if is_palindrome else "NO")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def is_palindrome_series(n_str):
  digits = list(n_str)
  length = sum(int(d) for d in digits)
  num_digits = len(digits)

  # Build and check
  s = ''.join(digits[i % num_digits] for i in range(length))
  return s == s[::-1]

def solve():
  t = int(input())
  for _ in range(t):
    n = input().strip()
    print("YES" if is_palindrome_series(n) else "NO")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(S) where S is the sum of digits (length of resulting string)
- **Space Complexity:** O(S) for storing the string, or O(D) where D is number of digits for optimized version

### Example Walkthrough
For N = 61:
- Digits: [6, 1]
- Sum: 6 + 1 = 7
- String: "6161616" (repeating [6,1] for 7 characters)
- As letters: "gbgbgbg"
- Is palindrome? Yes (reads same forwards and backwards)

For N = 12:
- Digits: [1, 2]
- Sum: 1 + 2 = 3
- String: "121"
- Is palindrome? Yes
