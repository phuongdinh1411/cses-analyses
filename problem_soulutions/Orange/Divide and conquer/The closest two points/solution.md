# The Closest Two Points

## Problem Information
- **Source:** Classic Algorithm Problem
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Given n points in a 2D plane, find the pair of points with the smallest Euclidean distance between them.

## Input Format
- First line: n (number of points)
- Next n lines: x y coordinates of each point

## Output Format
Output the minimum distance between any two points.

## Example
```
Input:
4
0 0
3 4
1 1
6 8

Output:
1.414214
```
Points: (0,0), (3,4), (1,1), (6,8). Distance (0,0)-(1,1) = sqrt(2) = 1.414214. Distance (0,0)-(3,4) = 5. Distance (3,4)-(6,8) = 5. The minimum is sqrt(2).

## Solution

### Approach
Use the classic Divide and Conquer algorithm:
1. Sort points by x-coordinate
2. Divide the points into two halves
3. Recursively find minimum distance in each half
4. Find minimum distance across the dividing line (strip region)
5. Return the overall minimum

The key insight is that we only need to check points within distance d of the dividing line, and for each such point, we only need to check at most 7 other points in the strip.

### Python Solution

```python
import math

def distance(p1, p2):
    dx, dy = p1[0] - p2[0], p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)

def brute_force(points):
    n = len(points)
    return min(
        (distance(points[i], points[j]) for i in range(n) for j in range(i + 1, n)),
        default=float('inf')
    )

def strip_closest(strip, d):
    min_dist = d
    # Sort by y coordinate
    strip.sort(key=lambda p: p[1])

    for i, p1 in enumerate(strip):
        j = i + 1
        while j < len(strip) and (strip[j][1] - p1[1]) < min_dist:
            min_dist = min(min_dist, distance(p1, strip[j]))
            j += 1

    return min_dist

def closest_pair(points_sorted_x):
    n = len(points_sorted_x)

    # Base case
    if n <= 3:
        return brute_force(points_sorted_x)

    mid = n // 2
    mid_point = points_sorted_x[mid]

    # Divide and conquer
    d = min(closest_pair(points_sorted_x[:mid]), closest_pair(points_sorted_x[mid:]))

    # Build strip using list comprehension
    strip = [p for p in points_sorted_x if abs(p[0] - mid_point[0]) < d]

    # Find closest in strip
    return strip_closest(strip, d)

def solve():
    n = int(input())

    # Read points using list comprehension
    points = [tuple(map(float, input().split())) for _ in range(n)]

    # Sort by x coordinate
    points.sort(key=lambda p: p[0])

    result = closest_pair(points)
    print(f"{result:.6f}")

if __name__ == "__main__":
    solve()
```

### Optimized Solution (Avoiding Repeated Sorting)

```python
import math

def solve():
    n = int(input())

    # Read points using list comprehension
    points = [tuple(map(float, input().split())) for _ in range(n)]

    def dist(p1, p2):
        dx, dy = p1[0] - p2[0], p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)

    def closest(px, py):
        n = len(px)

        if n <= 3:
            return min(
                (dist(px[i], px[j]) for i in range(n) for j in range(i + 1, n)),
                default=float('inf')
            )

        mid = n // 2
        mid_x = px[mid][0]

        # Split py into left and right using list comprehensions
        pyl = [p for p in py if p[0] <= mid_x]
        pyr = [p for p in py if p[0] > mid_x]

        # Handle edge case where all points go to one side
        if not pyl or not pyr:
            pyl, pyr = py[:mid], py[mid:]

        d = min(closest(px[:mid], pyl), closest(px[mid:], pyr))

        # Strip points sorted by y using list comprehension
        strip = [p for p in py if abs(p[0] - mid_x) < d]

        for i, p1 in enumerate(strip):
            j = i + 1
            while j < len(strip) and strip[j][1] - p1[1] < d:
                d = min(d, dist(p1, strip[j]))
                j += 1

        return d

    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])

    result = closest(px, py)
    print(f"{result:.6f}")

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting plus divide and conquer
- **Space Complexity:** O(n) for storing sorted arrays

### Key Insight
The divide and conquer approach works because:
1. The closest pair is either entirely in the left half, entirely in the right half, or spans both halves
2. For the spanning case, we only need to check a strip of width 2d around the dividing line
3. Within the strip, each point needs to be compared with at most 7 other points (geometric proof)

This reduces the naive O(n²) approach to O(n log n).
