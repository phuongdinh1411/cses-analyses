# The Hamming Distance Problem

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

The Hamming distance between two strings of bits (binary integers) is the number of corresponding bit positions that differ. This can be found by using XOR on corresponding bits. For example:

```
A       0100101000
B       1101010100
A XOR B 1001111100
```

The Hamming distance (H) between these 10-bit strings is 6, the number of 1's in the XOR string.

Given N (length of bit strings) and H (Hamming distance), print all bit strings of length N that are Hamming distance H from the bit string containing all 0's. That is, all bit strings of length N with exactly H 1's, in ascending lexicographical order.

## Input Format
- The first line contains the number of datasets, followed by a blank line.
- Each dataset contains N and H on the same line.
- There is a blank line between test cases.
- Constraints: 1 ≤ H ≤ N ≤ 16

## Output Format
- For each dataset, print all possible bit strings of length N with exactly H 1's in ascending lexicographical order.
- Print a blank line between datasets.

## Solution

### Approach
Generate all binary strings of length N with exactly H ones. This is equivalent to finding all permutations of a string with (N-H) zeros and H ones.

### Python Solution using Permutations

```python
from itertools import permutations

def solve():
    t = int(input())
    input()  # Read blank line after number of test cases

    for case in range(t):
        line = input().split()
        n, h = int(line[0]), int(line[1])

        # Create base string: (n-h) zeros followed by h ones
        base = '0' * (n - h) + '1' * h

        # Generate all unique permutations in sorted order
        seen = set()
        results = []

        for perm in permutations(base):
            s = ''.join(perm)
            if s not in seen:
                seen.add(s)
                results.append(s)

        results.sort()
        for s in results:
            print(s)

        print()  # Blank line between datasets

        # Try to read blank line between datasets
        try:
            if case < t - 1:
                input()
        except:
            pass

if __name__ == "__main__":
    solve()
```

### Optimized Solution using Backtracking

```python
def solve():
    t = int(input())
    input()  # Read blank line

    for case in range(t):
        line = input().split()
        n, h = int(line[0]), int(line[1])

        def generate(pos, ones_left, current):
            if pos == n:
                if ones_left == 0:
                    print(current)
                return

            remaining = n - pos

            # Place 0 if we can still place all remaining 1s
            if remaining > ones_left:
                generate(pos + 1, ones_left, current + '0')

            # Place 1 if we still have 1s to place
            if ones_left > 0:
                generate(pos + 1, ones_left - 1, current + '1')

        generate(0, h, '')
        print()

        try:
            if case < t - 1:
                input()
        except:
            pass

if __name__ == "__main__":
    solve()
```

### Using itertools.combinations

```python
from itertools import combinations

def solve():
    t = int(input())
    input()

    for case in range(t):
        line = input().split()
        n, h = int(line[0]), int(line[1])

        # Choose h positions out of n to be 1s
        for positions in combinations(range(n), h):
            bits = ['0'] * n
            for pos in positions:
                bits[pos] = '1'
            print(''.join(bits))

        print()

        try:
            if case < t - 1:
                input()
        except:
            pass

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(C(N, H)) to generate all combinations
- **Space Complexity:** O(N) for the current string

### Key Insight
The number of valid strings is C(N, H) - choosing H positions out of N for the 1s. Using combinations directly is more efficient than generating all permutations.
