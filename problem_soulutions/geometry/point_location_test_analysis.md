---
layout: simple
title: "Point Location Test - Geometry Problem"
permalink: /problem_soulutions/geometry/point_location_test_analysis
difficulty: Easy
tags: [geometry, cross-product, computational-geometry]
---

# Point Location Test

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Point Location Test](https://cses.fi/problemset/task/2189) |
| **Difficulty** | Easy |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Cross Product |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and compute the 2D cross product of vectors
- [ ] Determine the orientation of three points (left, right, collinear)
- [ ] Apply cross product to solve point-line position problems
- [ ] Handle edge cases with collinear points

---

## Problem Statement

**Problem:** Given a line defined by two points and a query point, determine if the query point is on the left side, right side, or directly on the line.

**Input:**
- Line 1: Number of test cases `t`
- Next `t` lines: Six integers `x1 y1 x2 y2 x3 y3` representing:
  - Point P1 = (x1, y1) and P2 = (x2, y2) define the line
  - Point P3 = (x3, y3) is the query point

**Output:**
- For each test case: `LEFT`, `RIGHT`, or `TOUCH`

**Constraints:**
- 1 <= t <= 10^5
- -10^9 <= x, y <= 10^9

### Example

```
Input:
3
1 1 5 3 2 3
1 1 5 3 4 1
1 1 5 3 3 2

Output:
LEFT
RIGHT
TOUCH
```

**Explanation:**
- P3(2,3) is to the LEFT of the line from P1(1,1) to P2(5,3)
- P3(4,1) is to the RIGHT of the line from P1(1,1) to P2(5,3)
- P3(3,2) lies ON the line from P1(1,1) to P2(5,3)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we mathematically determine which side of a line a point lies on?

The **cross product** of two 2D vectors tells us the orientation of the turn from one vector to another. If we form vectors from P1 to P2 and from P1 to P3, the sign of their cross product reveals the position of P3 relative to the line P1-P2.

### Breaking Down the Problem

1. **What are we looking for?** The relative position of point P3 with respect to the directed line from P1 to P2.
2. **What information do we have?** Three points defining two vectors from a common origin.
3. **What's the relationship?** The cross product sign indicates LEFT (positive), RIGHT (negative), or ON LINE (zero).

### The Cross Product Formula

For vectors **A** = (ax, ay) and **B** = (bx, by):

```
Cross Product = ax * by - ay * bx
```

This value represents the signed area of the parallelogram formed by the two vectors.

### Visual Understanding

```
              P3 (query point)
             /
            /   Cross > 0: LEFT
           /
    P1----+---------------->P2
           \
            \   Cross < 0: RIGHT
             \
              P3' (another query point)

When standing at P1 and looking toward P2:
- LEFT means P3 is on your left hand side
- RIGHT means P3 is on your right hand side
```

---

## Solution: Cross Product Approach

### Key Insight

> **The Trick:** Compute the cross product of vectors (P1->P2) and (P1->P3). The sign tells us the orientation.

### Algorithm

1. Create vector **v1** from P1 to P2: `v1 = (x2 - x1, y2 - y1)`
2. Create vector **v2** from P1 to P3: `v2 = (x3 - x1, y3 - y1)`
3. Compute cross product: `cross = v1.x * v2.y - v1.y * v2.x`
4. Determine position based on sign:
   - `cross > 0`: P3 is on the LEFT
   - `cross < 0`: P3 is on the RIGHT
   - `cross == 0`: P3 is on the LINE (TOUCH)

### Dry Run Example

Let's trace through with P1=(1,1), P2=(5,3), P3=(2,3):

```
Step 1: Compute vector v1 (P1 to P2)
  v1 = (5-1, 3-1) = (4, 2)

Step 2: Compute vector v2 (P1 to P3)
  v2 = (2-1, 3-1) = (1, 2)

Step 3: Compute cross product
  cross = v1.x * v2.y - v1.y * v2.x
  cross = 4 * 2 - 2 * 1
  cross = 8 - 2 = 6

Step 4: Determine position
  cross = 6 > 0  -->  LEFT
```

### Visual Diagram

```
y
^
|       P3(2,3)
|      /
|     /  v2=(1,2)     P2(5,3)
|    /              /
|   P1(1,1)-------/
|         v1=(4,2)
|
+-------------------------> x

Cross = 4*2 - 2*1 = 6 > 0  -->  P3 is LEFT of line P1-P2
```

### Code (Python)

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    results = []

    for _ in range(t):
        x1, y1, x2, y2, x3, y3 = map(int, input().split())

        # Vector from P1 to P2
        v1x, v1y = x2 - x1, y2 - y1
        # Vector from P1 to P3
        v2x, v2y = x3 - x1, y3 - y1

        # Cross product: v1 x v2
        cross = v1x * v2y - v1y * v2x

        if cross > 0:
            results.append("LEFT")
        elif cross < 0:
            results.append("RIGHT")
        else:
            results.append("TOUCH")

    print('\n'.join(results))

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        long long x1, y1, x2, y2, x3, y3;
        cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3;

        // Vector from P1 to P2
        long long v1x = x2 - x1, v1y = y2 - y1;
        // Vector from P1 to P3
        long long v2x = x3 - x1, v2y = y3 - y1;

        // Cross product: v1 x v2
        long long cross = v1x * v2y - v1y * v2x;

        if (cross > 0) {
            cout << "LEFT\n";
        } else if (cross < 0) {
            cout << "RIGHT\n";
        } else {
            cout << "TOUCH\n";
        }
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(t) | Single computation per test case |
| Space | O(1) | Only store vector components |

---

## Common Mistakes

### Mistake 1: Integer Overflow

```cpp
// WRONG - may overflow with int
int cross = (x2-x1) * (y3-y1) - (y2-y1) * (x3-x1);

// CORRECT - use long long
long long cross = (long long)(x2-x1) * (y3-y1) - (long long)(y2-y1) * (x3-x1);
```

**Problem:** With coordinates up to 10^9, the cross product can exceed 2^31.
**Fix:** Use `long long` in C++ or Python's arbitrary precision integers.

### Mistake 2: Wrong Vector Direction

```python
# WRONG - computing (P2 to P1) instead of (P1 to P2)
v1x, v1y = x1 - x2, y1 - y2

# CORRECT - vector from P1 TO P2
v1x, v1y = x2 - x1, y2 - y1
```

**Problem:** Reversing vector direction flips the sign, swapping LEFT and RIGHT.
**Fix:** Always compute vectors consistently from the first point.

### Mistake 3: Confusing Output Labels

```python
# WRONG - CSES wants "TOUCH" not "ON_LINE"
if cross == 0:
    return "ON_LINE"  # Will get Wrong Answer!

# CORRECT
if cross == 0:
    return "TOUCH"
```

**Problem:** The expected output format is specific to the problem.
**Fix:** Always check the exact output format required.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Collinear points | P1=(0,0), P2=(2,2), P3=(1,1) | TOUCH | P3 lies exactly on line |
| Horizontal line | P1=(0,0), P2=(5,0), P3=(3,1) | LEFT | Point above horizontal line |
| Vertical line | P1=(0,0), P2=(0,5), P3=(1,3) | RIGHT | Point right of vertical line |
| Large coordinates | P1=(10^9,10^9), P2=(-10^9,-10^9), P3=(0,1) | LEFT | Test overflow handling |
| Same start/end | P1=(1,1), P2=(1,1), P3=(2,2) | TOUCH | Degenerate line (cross=0) |

---

## When to Use This Pattern

### Use Cross Product When:
- Determining point-line relative position (left/right/on)
- Computing orientation of three points
- Checking if a turn is clockwise or counterclockwise
- Building convex hull algorithms
- Line segment intersection detection

### Pattern Recognition Checklist:
- [ ] Need to know which side of a line a point is on? --> **Cross Product**
- [ ] Checking turn direction in path? --> **Cross Product**
- [ ] Computing signed area? --> **Cross Product**
- [ ] Building convex hull? --> **Cross Product for orientation**

### The Cross Product Template

```python
def cross_product(o, a, b):
    """
    Compute cross product of vectors OA and OB.
    Returns:
      > 0 if O->A->B is counterclockwise (B is LEFT of OA)
      < 0 if O->A->B is clockwise (B is RIGHT of OA)
      = 0 if O, A, B are collinear
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
```

---

## Related Problems

### CSES Geometry Problems
| Problem | Key Concept |
|---------|-------------|
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Cross product for segment tests |
| [Polygon Area](https://cses.fi/problemset/task/2191) | Cross product for signed area |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Ray casting with orientation |
| [Convex Hull](https://cses.fi/problemset/task/2195) | Cross product for turn direction |

### Similar Difficulty
| Problem | Technique |
|---------|-----------|
| [Polygon Lattice Points](https://cses.fi/problemset/task/2193) | Pick's theorem with area |
| [Minimum Euclidean Distance](https://cses.fi/problemset/task/2194) | Divide and conquer geometry |

---

## Key Takeaways

1. **The Core Idea:** The cross product sign reveals point-line relative position.
2. **Formula:** `cross = (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)`
3. **Interpretation:** Positive = LEFT, Negative = RIGHT, Zero = TOUCH
4. **Watch Out:** Integer overflow with large coordinates - use `long long`.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain what the cross product represents geometrically
- [ ] Derive the formula from the definition of cross product
- [ ] Implement the solution in under 5 minutes
- [ ] Apply cross product to convex hull orientation checks

---

## Additional Resources

- [CP-Algorithms: Cross Product](https://cp-algorithms.com/geometry/oriented-triangle-area.html)
- [Computational Geometry - Princeton](https://www.cs.princeton.edu/courses/archive/fall00/cs126/lectures/c13-2x2.pdf)
- [CSES Point Location Test](https://cses.fi/problemset/task/2189) - Cross product applications
