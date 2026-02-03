# Dreamoon and WiFi

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

## Problem Statement

Dreamoon is standing at the position 0 on a number line. Drazil is sending a list of commands through Wi-Fi to Dreamoon's smartphone and Dreamoon follows them.

Each command is one of the following two types:
1. Go 1 unit towards the positive direction, denoted as `+`
2. Go 1 unit towards the negative direction, denoted as `-`

But the Wi-Fi condition is so poor that Dreamoon's smartphone reports some of the commands can't be recognized and Dreamoon knows that some of them might even be wrong though successfully recognized. Dreamoon decides to follow every recognized command and toss a fair coin to decide those unrecognized ones (that means, he moves to 1 unit to the negative or positive direction with the same probability 0.5).

You are given an original list of commands sent by Drazil and list received by Dreamoon. What is the probability that Dreamoon ends in the position originally supposed to be final by Drazil's commands?

## Input Format
- The first line contains a string s1 - the commands Drazil sends to Dreamoon, consisting only of characters in the set {+, -}.
- The second line contains a string s2 - the commands Dreamoon's smartphone recognizes, consisting only of characters in the set {+, -, ?}. ? denotes an unrecognized command.
- Lengths of two strings are equal and do not exceed 10.

## Output Format
Output a single real number corresponding to the probability. The answer will be considered correct if its relative or absolute error doesn't exceed 10^-9.

## Solution

### Approach
1. Calculate the target position from s1
2. Use backtracking to explore all possible outcomes for '?' characters
3. Count how many outcomes lead to the target position
4. Probability = valid_outcomes / total_outcomes

Since string length ≤ 10, there are at most 2^10 = 1024 possible outcomes.

### Python Solution

```python
def solve():
    s1 = input().strip()
    s2 = input().strip()

    # Calculate target position from s1
    target = sum(1 if c == '+' else -1 for c in s1)

    # Count '?' in s2
    question_marks = s2.count('?')

    if question_marks == 0:
        # No uncertainty - either we reach target or not
        position = sum(1 if c == '+' else -1 for c in s2)
        print(1.0 if position == target else 0.0)
        return

    # Calculate fixed position from known commands
    fixed_position = sum(1 if c == '+' else (-1 if c == '-' else 0) for c in s2)

    # Each '?' can be +1 or -1
    # Total outcomes = 2^question_marks
    total_outcomes = 2 ** question_marks
    valid_outcomes = 0

    # Try all combinations for '?' characters
    for mask in range(total_outcomes):
        pos = fixed_position
        for i in range(question_marks):
            if mask & (1 << i):
                pos += 1
            else:
                pos -= 1

        if pos == target:
            valid_outcomes += 1

    print(f"{valid_outcomes / total_outcomes:.12f}")

if __name__ == "__main__":
    solve()
```

### Recursive Solution

```python
def solve():
    s1 = input().strip()
    s2 = input().strip()

    target = sum(1 if c == '+' else -1 for c in s1)

    valid = [0]
    total = [0]

    def backtrack(idx, position):
        if idx == len(s2):
            total[0] += 1
            if position == target:
                valid[0] += 1
            return

        if s2[idx] == '+':
            backtrack(idx + 1, position + 1)
        elif s2[idx] == '-':
            backtrack(idx + 1, position - 1)
        else:  # '?'
            backtrack(idx + 1, position + 1)
            backtrack(idx + 1, position - 1)

    backtrack(0, 0)

    if total[0] == 0:
        print(0.0)
    else:
        print(f"{valid[0] / total[0]:.12f}")

if __name__ == "__main__":
    solve()
```

### Mathematical Solution (Using Combinatorics)

```python
from math import comb

def solve():
    s1 = input().strip()
    s2 = input().strip()

    target = sum(1 if c == '+' else -1 for c in s1)
    fixed = sum(1 if c == '+' else (-1 if c == '-' else 0) for c in s2)
    q = s2.count('?')

    if q == 0:
        print(1.0 if fixed == target else 0.0)
        return

    # We need to reach target from fixed using q moves of ±1
    # Let p = number of +1 moves, then q-p = number of -1 moves
    # fixed + p - (q - p) = target
    # fixed + 2p - q = target
    # p = (target - fixed + q) / 2

    diff = target - fixed + q
    if diff < 0 or diff % 2 != 0 or diff > 2 * q:
        print(0.0)
        return

    p = diff // 2
    # Number of ways = C(q, p)
    # Total ways = 2^q
    probability = comb(q, p) / (2 ** q)
    print(f"{probability:.12f}")

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(2^n) for backtracking, O(n) for mathematical solution
- **Space Complexity:** O(n) for recursion stack

### Key Insight
This problem can be solved efficiently using combinatorics. If we have q question marks and need to make p positive moves to reach the target, the probability is C(q,p) / 2^q.
