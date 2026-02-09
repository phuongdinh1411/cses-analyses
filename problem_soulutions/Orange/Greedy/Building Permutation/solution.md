# Building Permutation

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

## Problem Statement

Permutation p is an ordered set of integers p1, p2, ..., pn, consisting of n distinct positive integers, each of them doesn't exceed n. We'll denote the i-th element of permutation p as pi. We'll call number n the size or the length of permutation p1, p2, ..., pn.

You have a sequence of integers a1, a2, ..., an. In one move, you are allowed to decrease or increase any number by one. Count the minimum number of moves needed to build a permutation from this sequence.

## Input Format
- The first line contains integer n (1 ≤ n ≤ 3 × 10^5) - the size of the sought permutation.
- The second line contains n integers a1, a2, ..., an (-10^9 ≤ ai ≤ 10^9).

## Output Format
Print a single number - the minimum number of moves.

## Sample Test

**Input:**
```
2
3 0
```

**Output:**
```
2
```

**Input:**
```
3
-1 -1 2
```

**Output:**
```
6
```

## Solution

### Approach
The key insight is that to minimize the total number of moves, we should sort the array and then match each element to the corresponding position in the permutation [1, 2, 3, ..., n]. After sorting, the i-th smallest element should become i.

### Python Solution

```python
def solve():
    n = int(input())
    a = sorted(map(int, input().split()))

    # Calculate minimum moves using enumerate and sum with generator
    total_moves = sum(abs(val - (i + 1)) for i, val in enumerate(a))

    print(total_moves)

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log n) due to sorting
- **Space Complexity:** O(n) for storing the array
