# The Closest Pair Problem

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a set of points in a two dimensional space, you will have to find the distance between the closest two points.

## Input Format
- The input contains several testcases.
- Each testcase starts with an integer N (0 ≤ N ≤ 10000), which denotes the number of points in this test.
- The next N lines contain the coordinates of N two-dimensional points. The first of the two numbers denotes the X-coordinate and the latter denotes the Y-coordinate.
- The input is terminated by a test in which N = 0. This test should not be processed.
- The value of the coordinates will be less than 40000 and non-negative.

## Output Format
For each test produce a single line of output containing a floating point number (with four digits after the decimal point) denoting the distance between the closest two points. If there is no such two points whose distance is less than 10000, print the line "INFINITY".

## Example
```
Input:
5
0 0
1 0
2 0
3 0
4 0
0

Output:
1.0000
```
Five points on a line. Closest pair is any adjacent points (e.g., (0,0) and (1,0)) with distance 1.0000.

## Solution

### Approach
This is a classic divide and conquer problem:
1. Sort all points by x-coordinate
2. Divide the points into two halves
3. Recursively find the minimum distance in each half
4. Find the minimum distance across the dividing line (the strip)
5. For the strip, only consider points within distance d from the middle line, sorted by y-coordinate

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

def closest_pair(points):
    n = len(points)

    # Base case: use brute force for small sets
    if n <= 3:
        return brute_force(points)

    mid = n // 2
    mid_point = points[mid]

    # Recursively find minimum in left and right halves
    d = min(closest_pair(points[:mid]), closest_pair(points[mid:]))

    # Build strip using list comprehension
    strip = [p for p in points if abs(p[0] - mid_point[0]) < d]

    # Find closest points in strip
    return min(d, strip_closest(strip, d))

def solve():
    while True:
        n = int(input())
        if n == 0:
            break

        # Read points using list comprehension
        points = [tuple(map(float, input().split())) for _ in range(n)]

        # Sort by x coordinate
        points.sort(key=lambda p: p[0])

        if n < 2:
            print("INFINITY")
            continue

        result = closest_pair(points)
        print(f"{result:.4f}" if result < 10000 else "INFINITY")

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log² n) - can be optimized to O(n log n)
- **Space Complexity:** O(n)

### Key Insight
The clever observation is that for points in the strip, when sorted by y-coordinate, each point needs to be compared with at most 7 other points (due to geometric constraints). This keeps the strip processing linear.
