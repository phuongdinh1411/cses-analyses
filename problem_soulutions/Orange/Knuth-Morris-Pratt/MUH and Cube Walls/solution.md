# MUH and Cube Walls

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Bears have a wall of n towers with heights a₁, a₂, ..., aₙ. Elephant Horace has a wall of w towers with heights b₁, b₂, ..., bw.

Horace can "see an elephant" on a segment of w contiguous towers in the bears' wall if the heights match as a sequence (allowing raising/lowering the entire wall uniformly).

Count segments where Horace can "see an elephant".

## Input Format
- First line: n and w (1 ≤ n, w ≤ 2×10⁵)
- Second line: n integers aᵢ (1 ≤ aᵢ ≤ 10⁹) - bears' wall heights
- Third line: w integers bᵢ (1 ≤ bᵢ ≤ 10⁹) - elephant's wall heights

## Output Format
Print the number of segments where Horace can "see an elephant".

## Solution

### Approach
Two walls match if their "shape" (differences between consecutive heights) is the same. Convert both walls to difference arrays and use KMP to count pattern matches.

### Python Solution

```python
def solve():
    n, w = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    # Edge case: single tower always matches
    if w == 1:
        print(n)
        return

    # Convert to difference arrays
    diff_a = [a[i+1] - a[i] for i in range(n-1)]
    diff_b = [b[i+1] - b[i] for i in range(w-1)]

    # KMP to count occurrences of diff_b in diff_a
    pattern = diff_b
    text = diff_a
    m = len(pattern)

    if m == 0:
        print(n)
        return

    # Build failure function
    fail = [0] * m
    for i in range(1, m):
        j = fail[i-1]
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j-1]
        if pattern[i] == pattern[j]:
            j += 1
        fail[i] = j

    # Search
    count = 0
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = fail[j-1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            count += 1
            j = fail[j-1]

    print(count)

if __name__ == "__main__":
    solve()
```

### Alternative Solution

```python
def kmp_search(text, pattern):
    if not pattern:
        return len(text) + 1

    # Build LPS array
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1

    # Search
    count = 0
    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                count += 1
                j = lps[j - 1]
        elif j:
            j = lps[j - 1]
        else:
            i += 1

    return count

def solve():
    n, w = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    if w == 1:
        print(n)
        return

    # Compute differences
    da = [a[i+1] - a[i] for i in range(n-1)]
    db = [b[i+1] - b[i] for i in range(w-1)]

    print(kmp_search(da, db))

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(N + W)
- **Space Complexity:** O(W) for failure function

### Key Insight
Two sequences of heights have the same "shape" if their consecutive differences are identical. Converting both walls to difference arrays reduces this to exact pattern matching, solvable with KMP.
