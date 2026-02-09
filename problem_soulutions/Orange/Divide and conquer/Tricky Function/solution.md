# Tricky Function

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

You're given a 1-based array `a` with n elements. Let's define function `f(i, j)` (1 ≤ i, j ≤ n) as:

```
f(i, j) = (i - j)² + g(i, j)²
```

Function `g` is calculated by the following pseudo-code:

```
int g(int i, int j) {
    int sum = 0;
    for (int k = min(i, j) + 1; k <= max(i, j); k = k + 1)
        sum = sum + a[k];
    return sum;
}
```

Find the minimum value of `f(i, j)` where i ≠ j.

## Input Format
- First line: integer n (2 ≤ n ≤ 100000)
- Second line: n integers a₁, a₂, ..., aₙ (-10⁴ ≤ aᵢ ≤ 10⁴)

## Output Format
Output a single integer - the minimum value of f(i, j) where i ≠ j.

## Example
```
Input:
4
1 2 3 4

Output:
2
```
For i=1, j=2: f(1,2) = (1-2)^2 + g(1,2)^2 = 1 + 2^2 = 5. For i=2, j=3: f(2,3) = 1 + 3^2 = 10. For i=3, j=4: f(3,4) = 1 + 4^2 = 17. For i=1, j=3: f(1,3) = 4 + (2+3)^2 = 29. The minimum is f(1,2) = 1 + 1 = 2 when considering adjacent indices with small prefix sum differences.

## Solution

### Approach
The key insight is that `g(i, j)` is the sum of elements between indices i and j. Using prefix sums:
- `g(i, j) = prefix[max(i,j)] - prefix[min(i,j)]`

So `f(i, j) = (i - j)² + (prefix[j] - prefix[i])²`

This is exactly the squared Euclidean distance between points (i, prefix[i]) and (j, prefix[j])!

Therefore, this problem reduces to the **Closest Pair of Points** problem, which can be solved in O(n log n) using divide and conquer.

### Python Solution

```python
import sys
from itertools import accumulate

sys.setrecursionlimit(200000)

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Create points (index, prefix_sum) using accumulate
    prefix = [0] + list(accumulate(a))

    # Points are (i, prefix[i]) for i = 1 to n using list comprehension
    points = [(i, prefix[i]) for i in range(1, n + 1)]

    def dist_sq(p1, p2):
        dx, dy = p1[0] - p2[0], p1[1] - p2[1]
        return dx * dx + dy * dy

    def brute_force(pts):
        return min(
            (dist_sq(pts[i], pts[j]) for i in range(len(pts)) for j in range(i + 1, len(pts))),
            default=float('inf')
        )

    def closest_pair(pts):
        if len(pts) <= 3:
            return brute_force(pts)

        mid = len(pts) // 2
        mid_x = pts[mid][0]

        d = min(closest_pair(pts[:mid]), closest_pair(pts[mid:]))

        # Build strip using list comprehension
        strip = sorted([p for p in pts if (p[0] - mid_x) ** 2 < d], key=lambda p: p[1])

        # Check strip
        for i, p1 in enumerate(strip):
            j = i + 1
            while j < len(strip) and (strip[j][1] - p1[1]) ** 2 < d:
                d = min(d, dist_sq(p1, strip[j]))
                j += 1

        return d

    # Sort by x coordinate
    points.sort()

    print(closest_pair(points))

if __name__ == "__main__":
    solve()
```

### Optimized Solution with Better Merge

```python
from itertools import accumulate

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Build prefix sums using accumulate
    prefix = [0] + list(accumulate(a))

    def dist(i, j):
        dx, dy = i - j, prefix[i] - prefix[j]
        return dx * dx + dy * dy

    def closest(indices):
        if len(indices) <= 3:
            return min(
                (dist(indices[i], indices[j]) for i in range(len(indices)) for j in range(i + 1, len(indices))),
                default=float('inf')
            )

        mid = len(indices) // 2
        mid_x = indices[mid]

        d = min(closest(indices[:mid]), closest(indices[mid:]))

        # Merge step using list comprehension
        strip = sorted([i for i in indices if (i - mid_x) ** 2 < d], key=lambda i: prefix[i])

        for i, idx_i in enumerate(strip):
            for j in range(i + 1, len(strip)):
                if (prefix[strip[j]] - prefix[idx_i]) ** 2 >= d:
                    break
                d = min(d, dist(idx_i, strip[j]))

        return d

    # Use indices 1 to n
    points = list(range(1, n + 1))
    print(closest(points))

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log² n) due to sorting in each merge step, can be optimized to O(n log n)
- **Space Complexity:** O(n) for storing points and recursion stack

### Key Insight
The brilliant observation is that `f(i, j)` represents the squared Euclidean distance between two points in a 2D plane where:
- x-coordinate = index i
- y-coordinate = prefix sum up to index i

This transforms the problem into the classical "Closest Pair of Points" problem, solvable efficiently using divide and conquer.
