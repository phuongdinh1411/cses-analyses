# Little Deepu and Array

## Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Little Deepu has an array of positive elements. He performs M HIT operations where HIT(X) decreases the value of all elements greater than X by 1.

After all M operations, print the final array.

## Input Format
- First line: N (size of array)
- Second line: N elements of array
- Third line: M (number of operations)
- Next M lines: X value for each HIT operation

## Constraints
- 1 ≤ N ≤ 100000
- 1 ≤ Aᵢ ≤ 10^9
- 1 ≤ M ≤ 20000
- 1 ≤ X ≤ 10^9

## Output Format
Print the final array after M HIT operations.

## Solution

### Approach
Instead of simulating each HIT operation on the entire array (O(N*M)), we can:
1. Sort all HIT thresholds
2. For each element, count how many thresholds it exceeds
3. Subtract that count from the element

Key insight: If element A[i] > X, it gets decremented. So we count how many X values each element exceeds.

### Python Solution

```python
def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    m = int(input())

    hits = []
    for _ in range(m):
        hits.append(int(input()))

    # Sort hit thresholds
    hits.sort()

    # For each element, find how many hits affect it
    result = []
    for a in arr:
        # Count how many X values are < a (element will be decremented for each)
        # Binary search for position where hits[i] >= a
        import bisect
        count = bisect.bisect_left(hits, a)
        result.append(a - count)

    print(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()
```

### Optimized Solution with Preprocessing

```python
from bisect import bisect_left

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    m = int(input())
    hits = [int(input()) for _ in range(m)]

    # Sort hits for binary search
    hits.sort()

    # For each element, count hits where X < element
    # (element decreases by 1 for each such X)
    result = []
    for a in arr:
        # Number of X values strictly less than a
        decrements = bisect_left(hits, a)
        result.append(a - decrements)

    print(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()
```

### Alternative Solution (Handling Duplicates)

```python
from bisect import bisect_left

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    m = int(input())
    hits = sorted(int(input()) for _ in range(m))

    # Each HIT(X) decrements elements > X
    # So element A becomes A - (count of X where X < A)
    output = []
    for val in arr:
        # How many hit values are strictly less than val
        dec = bisect_left(hits, val)
        output.append(str(val - dec))

    print(' '.join(output))

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(N log M + M log M) - sorting hits and binary search for each element
- **Space Complexity:** O(M) for storing hit thresholds

### Key Insight
HIT(X) decrements all values > X. So for an element with value V:
- It gets decremented once for each X where X < V
- Final value = V - (count of X values < V)

Using binary search on sorted hit values gives us this count efficiently.
