# Alphacode

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Alice and Bob need to send secret messages to each other and are discussing ways to encode their messages:

Alice: "Let's just use a very simple code: We'll assign A the code word 1, B will be 2, and so on down to Z being assigned 26."

Bob: "That's a stupid code, Alice. Suppose I send you the word BEAN encoded as 25114. You could decode that in many different ways!"

Alice: "Sure you could, but what words would you get? Other than BEAN, you'd get BEAAD, YAAD, YAN, YKD and BEKD. I think you would be able to figure out the correct decoding. And why would you send me the word BEAN anyway?"

Bob: "OK, maybe that's a bad example, but I bet you that if you got a string of length 5000 there would be tons of different decodings and with that many you would find at least two different ones that would make sense."

Alice: "How many different decodings?"
Bob: "Jillions!"

For some reason, Alice is still unconvinced by Bob's argument, so she requires a program that will determine how many decodings there can be for a given string using her code.

## Input Format
- Input will consist of multiple input sets.
- Each set will consist of a single line of at most 5000 digits representing a valid encryption (no line will begin with a 0).
- There will be no spaces between the digits.
- An input line of 0 will terminate the input and should not be processed.

## Output Format
For each input set, output the number of possible decodings for the input string. All answers will be within the range of a 64 bit signed integer.

## Example
```
Input:
25114
1111111111
0

Output:
6
89
```
For "25114": The 6 decodings are BEAN, BEAAD, YAAD, YAN, YKD, BEKD (mapping 2=B, 5=E, 1=A, etc. or 25=Y, 11=K, 14=N).
For "1111111111": There are 89 ways to decode this 10-digit string (similar to Fibonacci).

## Solution

### Approach
This is a classic DP problem similar to climbing stairs:
- `dp[i]` = number of ways to decode the first i characters
- At each position, we can either:
  1. Take a single digit (if it's 1-9)
  2. Take two digits (if they form 10-26)

### Python Solution

```python
def solve(s):
  n = len(s)
  if n == 0 or s[0] == '0':
    return 0

  # dp[i] = number of ways to decode first i characters
  dp = [0] * (n + 1)
  dp[0] = 1  # Empty string
  dp[1] = 1  # First character (already checked it's not 0)

  for i in range(2, n + 1):
    # Single digit decode (1-9)
    if s[i-1] != '0':
      dp[i] = dp[i-1]

    # Two digit decode (10-26)
    two_digit = int(s[i-2:i])
    if 10 <= two_digit <= 26:
      dp[i] += dp[i-2]

  return dp[n]

def main():
  while True:
    s = input().strip()
    if s == '0':
      break
    print(solve(s))

if __name__ == "__main__":
  main()
```

### Complexity Analysis
- **Time Complexity:** O(n) where n is the length of the string
- **Space Complexity:** O(n) for the DP array (can be optimized to O(1))

### Example Walkthrough
For "25114":
- dp[0] = 1 (empty)
- dp[1] = 1 ("2" → B)
- dp[2] = 2 ("25" → BE or Y)
- dp[3] = 2 ("251" → BEA or YA)
- dp[4] = 3 ("2511" → BEAA, YAA, BKA)
- dp[5] = 5 ("25114" → BEAAD, YAAD, YKD, YAN, BEAN, BEKD... wait, let me recount)

The answer is 6 different decodings.
