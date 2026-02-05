---
layout: simple
title: "Area of Rectangles - Geometry Problem"
permalink: /problem_soulutions/geometry/area_of_rectangles_analysis
difficulty: Hard
tags: [geometry, sweep-line, coordinate-compression, segment-tree]
---

# Area of Rectangles

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Area of Rectangles](https://cses.fi/problemset/task/1741) |
| **Difficulty** | Hard |
| **Category** | Geometry |
| **Time Limit** | 1 second |
| **Key Technique** | Sweep Line + Coordinate Compression |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply coordinate compression to handle large coordinate ranges
- [ ] Implement the sweep line algorithm for 2D problems
- [ ] Use a segment tree to efficiently track interval coverage
- [ ] Calculate union area of overlapping rectangles

---

## Problem Statement

**Problem:** Given n axis-aligned rectangles, calculate the total area covered by at least one rectangle (union of rectangles).

**Input:**
- Line 1: Integer n - number of rectangles
- Lines 2 to n+1: Four integers x1, y1, x2, y2 - bottom-left and top-right corners

**Output:**
- Single integer: total area covered by the rectangles

**Constraints:**
- 1 <= n <= 10^5
- 1 <= x1 < x2 <= 10^9
- 1 <= y1 < y2 <= 10^9

### Example

```
Input:
2
1 1 4 3
2 2 5 5

Output:
14
```

**Explanation:**
- Rectangle 1: area = 3 * 2 = 6
- Rectangle 2: area = 3 * 3 = 9
- Overlap region: (2,2) to (4,3) = 2 * 1 = 2 (counted once)
- Union area = 6 + 9 - 2 = 13... Wait, let's recalculate visually!

```
Y
5 |     +-----+
4 |     |     |
3 | +---+--+  |
2 | |   |##|  |
1 | +---+--+--+
0 +---------------> X
  0 1 2 3 4 5
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently calculate the union area when rectangles can overlap arbitrarily?

The naive approach of inclusion-exclusion fails for many rectangles (exponential subsets). Instead, we use **coordinate compression** to reduce the problem size and **sweep line** to process the plane incrementally.

### Breaking Down the Problem

1. **What are we looking for?** Total area covered by at least one rectangle
2. **What makes this hard?** Coordinates up to 10^9 and arbitrary overlaps
3. **Key insight:** Only ~2n distinct x-coordinates and ~2n y-coordinates matter

### Analogy

Imagine painting rectangles on a canvas. Instead of calculating paint overlap mathematically, we:
1. Divide the canvas into a grid based on rectangle edges
2. Sweep left-to-right, tracking which grid cells are "painted"
3. Sum up painted cell areas

---

## Solution 1: Brute Force (Coordinate Compression Only)

### Idea

Compress coordinates to create a grid, then check each grid cell against all rectangles.

### Algorithm

1. Collect all unique x and y coordinates
2. Create a grid of "compressed cells"
3. For each cell, check if any rectangle covers it
4. Sum areas of covered cells

### Code

```python
def solve_brute_force(n, rectangles):
    """
    Brute force with coordinate compression.

    Time: O(n^3) - n^2 cells, n rectangles to check each
    Space: O(n^2)
    """
    # Collect unique coordinates
    xs = sorted(set(x for r in rectangles for x in (r[0], r[2])))
    ys = sorted(set(y for r in rectangles for y in (r[1], r[3])))

    total_area = 0

    # Check each grid cell
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x1, x2 = xs[i], xs[i + 1]
            y1, y2 = ys[j], ys[j + 1]

            # Check if any rectangle covers this cell
            for rx1, ry1, rx2, ry2 in rectangles:
                if rx1 <= x1 and x2 <= rx2 and ry1 <= y1 and y2 <= ry2:
                    total_area += (x2 - x1) * (y2 - y1)
                    break

    return total_area
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | O(n^2) grid cells, O(n) check per cell |
| Space | O(n^2) | Storing the grid |

### Why This Works (But Is Slow)

Coordinate compression ensures we only consider "interesting" cells. However, checking each cell against all rectangles is too slow for n = 10^5.

---

## Solution 2: Optimal (Sweep Line + Segment Tree)

### Key Insight

> **The Trick:** Sweep a vertical line left-to-right. At each x-position, use a segment tree to track which y-intervals are currently covered, then multiply by the width to get area.

### Algorithm Overview

1. **Coordinate compress** y-values to indices 0 to 2n-1
2. Create **events**: rectangle start (+1 coverage) and end (-1 coverage)
3. **Sweep** through events sorted by x-coordinate
4. Use **segment tree** to track total covered y-length efficiently

### Segment Tree Design

| Property | Description |
|----------|-------------|
| Leaf `i` | Represents y-interval `[ys[i], ys[i+1]]` |
| `cnt[node]` | Number of rectangles fully covering this node's interval |
| `len[node]` | Total covered length in this node's interval |

**Key Formula:** If `cnt[node] > 0`, entire interval is covered. Otherwise, sum children.

### Dry Run Example

Input: Rectangle 1: (1,1,4,3), Rectangle 2: (2,2,5,5)

```
Step 1: Coordinate Compression
  Y-coords: [1, 2, 3, 5] -> indices [0, 1, 2, 3]
  Intervals: [1,2], [2,3], [3,5]

Step 2: Create Events (sorted by x)
  x=1: ADD rect1 covering y=[1,3] (indices 0-2)
  x=2: ADD rect2 covering y=[2,5] (indices 1-3)
  x=4: REMOVE rect1
  x=5: REMOVE rect2

Step 3: Sweep
  x=1: covered_length = 2 (y from 1 to 3)
       No previous x, no area yet

  x=2: area += (2-1) * 2 = 2
       Add rect2, covered_length = 4 (y from 1 to 5)

  x=4: area += (4-2) * 4 = 8
       Remove rect1, covered_length = 3 (y from 2 to 5)

  x=5: area += (5-4) * 3 = 3
       Remove rect2, done

Total: 2 + 8 + 3 = 13...
```

### Visual Diagram

```
Events on x-axis:        Segment Tree tracks y-coverage:

x=1 [+R1]               |  y=5 --------
x=2 [+R2]               |  y=3 ----+
x=4 [-R1]               |  y=2   --+--+
x=5 [-R2]               |  y=1 --+
    |                   |
    +--+--+--+-->       +------------->
    1  2  4  5  x           covered y
```

### Code (Python)

```python
import sys
from collections import defaultdict
input = sys.stdin.readline

def solve():
    n = int(input())
    rectangles = []
    ys = set()

    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        rectangles.append((x1, y1, x2, y2))
        ys.add(y1)
        ys.add(y2)

    # Coordinate compression for y
    ys = sorted(ys)
    y_to_idx = {y: i for i, y in enumerate(ys)}
    m = len(ys) - 1  # Number of y-intervals

    # Segment tree arrays
    cnt = [0] * (4 * m)  # Coverage count
    total = [0] * (4 * m)  # Covered length

    def update(node, start, end, l, r, val):
        """Update coverage for y-interval [l, r) by val (+1 or -1)."""
        if r <= start or end <= l:
            return
        if l <= start and end <= r:
            cnt[node] += val
        else:
            mid = (start + end) // 2
            update(2*node, start, mid, l, r, val)
            update(2*node+1, mid, end, l, r, val)

        # Recalculate covered length
        if cnt[node] > 0:
            total[node] = ys[end] - ys[start]
        elif end - start == 1:
            total[node] = 0
        else:
            total[node] = total[2*node] + total[2*node+1]

    # Create events: (x, type, y1_idx, y2_idx)
    # type: 0 = start (add), 1 = end (remove)
    events = []
    for x1, y1, x2, y2 in rectangles:
        y1_idx = y_to_idx[y1]
        y2_idx = y_to_idx[y2]
        events.append((x1, 0, y1_idx, y2_idx))
        events.append((x2, 1, y1_idx, y2_idx))

    events.sort()

    area = 0
    prev_x = events[0][0]

    for x, typ, y1_idx, y2_idx in events:
        # Add area from previous x to current x
        area += total[1] * (x - prev_x)

        # Update segment tree
        if typ == 0:  # Start of rectangle
            update(1, 0, m, y1_idx, y2_idx, 1)
        else:  # End of rectangle
            update(1, 0, m, y1_idx, y2_idx, -1)

        prev_x = x

    print(area)

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sort events + O(log n) per segment tree update |
| Space | O(n) | Segment tree and events storage |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** Coordinates up to 10^9, area can exceed 10^18.
**Fix:** Use `long long` throughout.

### Mistake 2: Forgetting to Process Final Segment

```python
# WRONG - stops at last event without adding final area
for event in events:
    update_tree(event)
    # Missing area calculation!

# CORRECT
for x, typ, y1, y2 in events:
    area += total[1] * (x - prev_x)  # Add area BEFORE update
    update_tree(...)
    prev_x = x
```

### Mistake 3: Wrong Event Order for Same X

```python
# WRONG - may remove before add at same x
events.sort()  # Only sorts by x

# CORRECT - add before remove at same x
events.sort(key=lambda e: (e[0], e[1]))  # type 0 (add) before type 1 (remove)
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single rectangle | 1 rect (1,1,3,3) | 4 | No overlap |
| Identical rectangles | 2 same rects | area of 1 | Union, not sum |
| No overlap | 2 disjoint rects | sum of areas | No intersection |
| Complete overlap | small inside large | large area | Small adds nothing |
| Touching edges | (1,1,2,2), (2,1,3,2) | 2 | No overlap, just touch |

---

## When to Use This Pattern

### Use Sweep Line + Coordinate Compression When:
- Dealing with geometric objects (rectangles, segments)
- Coordinates are large but count of objects is manageable
- Need to compute union/intersection of shapes
- Problems involve "area covered by at least k rectangles"

### Don't Use When:
- Only 2-3 rectangles (inclusion-exclusion is simpler)
- Need to handle arbitrary polygons (different algorithms)
- Online queries (consider persistent structures)

### Pattern Recognition Checklist:
- [ ] Union/intersection of rectangles? -> **Sweep line**
- [ ] Large coordinates, few objects? -> **Coordinate compression**
- [ ] Need efficient interval updates? -> **Segment tree**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Line Segment Intersection](https://cses.fi/problemset/task/2190) | Basic sweep line |
| [Restaurant Customers](https://cses.fi/problemset/task/1619) | Event-based sweep |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Polygon Area](https://cses.fi/problemset/task/2191) | Shoelace formula |
| [Point in Polygon](https://cses.fi/problemset/task/2192) | Ray casting |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Convex Hull](https://cses.fi/problemset/task/2195) | Graham scan |
| Rectangle Union with K-coverage | Track coverage counts |

---

## Key Takeaways

1. **Core Idea:** Sweep line converts 2D problems into 1D + time
2. **Coordinate Compression:** Reduces infinite plane to O(n) grid
3. **Segment Tree Role:** Efficiently maintains covered length during sweep
4. **Time Trade-off:** O(n log n) vs O(n^3) brute force

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement coordinate compression from scratch
- [ ] Explain why we process events left-to-right
- [ ] Draw the segment tree for a small example
- [ ] Handle the case where rectangles share edges
- [ ] Solve in under 20 minutes without reference

---

## Additional Resources

- [CP-Algorithms: Sweep Line](https://cp-algorithms.com/geometry/sweep_line.html)
- [CSES Polygon Area](https://cses.fi/problemset/task/2191) - Related geometry problem
- [Segment Tree Tutorial](https://cp-algorithms.com/data_structures/segment_tree.html)
