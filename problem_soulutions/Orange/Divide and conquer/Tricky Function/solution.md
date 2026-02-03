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
sys.setrecursionlimit(200000)

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Create points (index, prefix_sum)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    # Points are (i, prefix[i]) for i = 1 to n
    points = [(i, prefix[i]) for i in range(1, n + 1)]

    def dist_sq(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def brute_force(pts):
        min_d = float('inf')
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                min_d = min(min_d, dist_sq(pts[i], pts[j]))
        return min_d

    def closest_pair(pts):
        if len(pts) <= 3:
            return brute_force(pts)

        mid = len(pts) // 2
        mid_x = pts[mid][0]

        left = pts[:mid]
        right = pts[mid:]

        d_left = closest_pair(left)
        d_right = closest_pair(right)
        d = min(d_left, d_right)

        # Build strip
        strip = [p for p in pts if (p[0] - mid_x) ** 2 < d]
        strip.sort(key=lambda p: p[1])  # Sort by y (prefix sum)

        # Check strip
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1]) ** 2 < d:
                d = min(d, dist_sq(strip[i], strip[j]))
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
def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Build prefix sums
    prefix = [0]
    for x in a:
        prefix.append(prefix[-1] + x)

    # Points: (x=index, y=prefix_sum)
    points = list(range(n + 1))  # indices 0 to n

    def dist(i, j):
        dx = i - j
        dy = prefix[i] - prefix[j]
        return dx * dx + dy * dy

    def closest(indices):
        if len(indices) <= 3:
            min_d = float('inf')
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    min_d = min(min_d, dist(indices[i], indices[j]))
            return min_d

        mid = len(indices) // 2
        mid_x = indices[mid]

        d = min(closest(indices[:mid]), closest(indices[mid:]))

        # Merge step
        strip = [i for i in indices if (i - mid_x) ** 2 < d]
        strip.sort(key=lambda i: prefix[i])

        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (prefix[strip[j]] - prefix[strip[i]]) ** 2 >= d:
                    break
                d = min(d, dist(strip[i], strip[j]))

        return d

    # Sort indices by x coordinate (which is just the index itself)
    points.sort()

    # We need i != j, and since points start from 0, we use indices 1 to n
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
