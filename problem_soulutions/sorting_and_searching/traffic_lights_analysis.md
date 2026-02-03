---
layout: simple
title: "Traffic Lights - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/traffic_lights_analysis
difficulty: Medium
tags: [set, multiset, binary-search, dynamic-maximum]
---

# Traffic Lights

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Set + Multiset for Dynamic Maximum Tracking |
| **CSES Link** | [Traffic Lights](https://cses.fi/problemset/task/1163) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Use a set to maintain sorted positions with O(log n) insertion
- [ ] Use a multiset to track segment lengths and find maximum in O(log n)
- [ ] Handle dynamic updates where inserting splits one segment into two
- [ ] Choose between set vs multiset based on whether duplicates are possible

---

## Problem Statement

**Problem:** There is a street of length x with traffic lights initially at positions 0 and x. You need to add n traffic lights one at a time. After each addition, report the length of the longest segment between consecutive traffic lights.

**Input:**
- Line 1: Two integers x and n (street length and number of traffic lights)
- Line 2: n integers representing positions of traffic lights to add

**Output:**
- n integers: the longest segment length after each traffic light is added

**Constraints:**
- 1 <= x <= 10^9
- 1 <= n <= 2 * 10^5
- 0 < position < x (lights are always between endpoints)

### Example

```
Input:
8 3
3 6 2

Output:
5 3 3
```

**Explanation:**

```
Initial:     [0]─────────────────────────[8]
             └────────── 8 ──────────────┘

After 3:     [0]───────[3]───────────────[8]
             └── 3 ──┘ └────── 5 ────────┘   Max = 5

After 6:     [0]───────[3]─────────[6]───[8]
             └── 3 ──┘ └── 3 ────┘ └─ 2 ─┘   Max = 3

After 2:     [0]───[2]─[3]─────────[6]───[8]
             └─ 2 ─┘└1┘└── 3 ────┘ └─ 2 ─┘   Max = 3
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When we add a light at position p, what changes? Only ONE segment gets split into TWO.

The critical insight is that adding a traffic light is a **local operation** - it only affects the segment containing the new position. We do not need to recalculate all segments.

### Breaking Down the Problem

1. **What are we looking for?** The maximum gap between consecutive lights after each insertion
2. **What information do we need to track?**
   - All current light positions (to find neighbors of new light)
   - All current segment lengths (to quickly find maximum)
3. **What's the relationship?** Adding position p between positions L and R:
   - Removes segment of length (R - L)
   - Adds two segments of length (p - L) and (R - p)

### Analogies

Think of this like cutting a rope: when you make a cut, you do not affect other pieces of rope. You only split one piece into two. To find the longest piece at any time, you need to track all piece lengths efficiently.

---

## Solution 1: Brute Force

### Idea

After each insertion, sort all positions and scan to find the maximum gap.

### Algorithm

1. Maintain a list of all traffic light positions
2. For each new position, add it to the list
3. Sort the list
4. Scan consecutive pairs to find maximum gap

### Code

```python
def solve_brute_force(x, positions):
    """
    Brute force: sort and scan after each insertion.

    Time: O(n^2 log n)
    Space: O(n)
    """
    lights = [0, x]
    result = []

    for pos in positions:
        lights.append(pos)
        lights.sort()

        max_gap = 0
        for i in range(len(lights) - 1):
            max_gap = max(max_gap, lights[i + 1] - lights[i])

        result.append(max_gap)

    return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 log n) | n insertions, each requires O(n log n) sort + O(n) scan |
| Space | O(n) | Store all positions |

### Why This Works (But Is Slow)

Sorting guarantees positions are in order, and scanning finds the correct maximum. However, we redo work: we sort already-sorted data and scan all segments when only one changed.

---

## Solution 2: Optimal Solution (Set + Multiset)

### Key Insight

> **The Trick:** Use a **set** to find neighbors in O(log n) and a **multiset** to track all segment lengths and find maximum in O(1).

### Data Structure Choice

| Structure | Purpose | Operations |
|-----------|---------|------------|
| `set<int>` | Store light positions in sorted order | O(log n) insert, O(log n) find neighbors |
| `multiset<int>` | Store all segment lengths | O(log n) insert/delete, O(1) find max |

**Why multiset not set?** Segment lengths can have duplicates (e.g., two segments of length 3).

### Algorithm

1. Initialize set with {0, x} and multiset with {x}
2. For each new position p:
   - Find left neighbor L and right neighbor R using set iterators
   - Remove old segment length (R - L) from multiset
   - Add new segment lengths (p - L) and (R - p) to multiset
   - Insert p into set
   - Maximum is the last element of multiset

### Dry Run Example

Let's trace through with `x = 8, positions = [3, 6, 2]`:

```
Initial state:
  positions = {0, 8}
  segments  = {8}         Max = 8

Step 1: Add position 3
  Find neighbors: L = 0, R = 8
  Old segment: 8 - 0 = 8
  New segments: 3 - 0 = 3, 8 - 3 = 5

  Remove 8 from segments
  Add 3 and 5 to segments

  positions = {0, 3, 8}
  segments  = {3, 5}      Max = 5
  Output: 5

Step 2: Add position 6
  Find neighbors: L = 3, R = 8
  Old segment: 8 - 3 = 5
  New segments: 6 - 3 = 3, 8 - 6 = 2

  Remove 5 from segments
  Add 3 and 2 to segments

  positions = {0, 3, 6, 8}
  segments  = {2, 3, 3}   Max = 3
  Output: 3

Step 3: Add position 2
  Find neighbors: L = 0, R = 3
  Old segment: 3 - 0 = 3
  New segments: 2 - 0 = 2, 3 - 2 = 1

  Remove ONE 3 from segments (multiset removes one instance)
  Add 2 and 1 to segments

  positions = {0, 2, 3, 6, 8}
  segments  = {1, 2, 2, 3}    Max = 3
  Output: 3
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int x, n;
    cin >> x >> n;

    set<int> positions;          // Traffic light positions
    multiset<int> segments;      // Segment lengths (allows duplicates)

    // Initialize with endpoints
    positions.insert(0);
    positions.insert(x);
    segments.insert(x);

    while (n--) {
        int p;
        cin >> p;

        // Find neighbors using set iterators
        auto it = positions.upper_bound(p);  // First element > p
        int right = *it;
        int left = *prev(it);                // Element just before

        // Remove old segment, add two new segments
        segments.erase(segments.find(right - left));  // Remove ONE instance
        segments.insert(p - left);
        segments.insert(right - p);

        // Add new position
        positions.insert(p);

        // Maximum is the last element
        cout << *segments.rbegin() << " \n"[n == 0];
    }

    return 0;
}
```

### Code (Python)

Python does not have a built-in multiset. We use `sortedcontainers.SortedList` for an efficient implementation:

```python
from sortedcontainers import SortedList

def solve_optimal(x, positions):
    """
    Optimal solution using sorted containers.

    Time: O(n log n)
    Space: O(n)
    """
    lights = SortedList([0, x])    # Positions in sorted order
    segments = SortedList([x])     # Segment lengths (allows duplicates)
    result = []

    for p in positions:
        # Find neighbors using bisect
        idx = lights.bisect_left(p)
        right = lights[idx]
        left = lights[idx - 1]

        # Remove old segment, add two new segments
        segments.remove(right - left)
        segments.add(p - left)
        segments.add(right - p)

        # Add new position
        lights.add(p)

        # Maximum is the last element
        result.append(segments[-1])

    return result

# For CSES submission (without external libraries)
from bisect import bisect_left, insort

def solve_for_submission(x, positions):
    """
    Solution using built-in bisect (O(n) per insert, but works for n <= 2*10^5).
    """
    lights = [0, x]
    segments = [x]
    result = []

    for p in positions:
        idx = bisect_left(lights, p)
        right = lights[idx]
        left = lights[idx - 1]

        # Remove old segment
        segments.remove(right - left)

        # Add new segments
        insort(segments, p - left)
        insort(segments, right - p)

        # Insert new light
        lights.insert(idx, p)

        result.append(segments[-1])

    return result

# Read input and solve
if __name__ == "__main__":
    x, n = map(int, input().split())
    positions = list(map(int, input().split()))
    print(*solve_for_submission(x, positions))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | n insertions, each O(log n) for set/multiset operations |
| Space | O(n) | Store n+2 positions and n+1 segments |

---

## Common Mistakes

### Mistake 1: Using set instead of multiset for segments

```cpp
// WRONG - set does not allow duplicates
set<int> segments;
segments.insert(3);
segments.insert(3);  // Second 3 is ignored!
segments.erase(3);   // Now segments is empty, but should have one 3 left
```

**Problem:** Multiple segments can have the same length. Set ignores duplicates.
**Fix:** Use `multiset<int>` which allows duplicate values.

### Mistake 2: Using erase(value) instead of erase(find(value))

```cpp
// WRONG - erases ALL instances of the value
segments.erase(right - left);  // If there are multiple segments of this length, all are removed!

// CORRECT - erases only ONE instance
segments.erase(segments.find(right - left));
```

**Problem:** `multiset::erase(value)` removes all elements equal to value.
**Fix:** Use `multiset::erase(multiset::find(value))` to remove exactly one instance.

### Mistake 3: Wrong neighbor finding logic

```cpp
// WRONG - lower_bound gives element >= p, but p already exists check needed
auto it = positions.lower_bound(p);

// CORRECT - upper_bound gives element > p (guaranteed different)
auto it = positions.upper_bound(p);
int right = *it;
int left = *prev(it);
```

**Problem:** If p already exists, lower_bound returns p itself.
**Fix:** Use `upper_bound` which always returns the first element strictly greater than p.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single light in middle | x=10, pos=[5] | 5 | Splits 10 into 5,5. Max = 5 |
| Light near start | x=10, pos=[1] | 9 | Splits into 1,9. Max = 9 |
| Light near end | x=10, pos=[9] | 9 | Splits into 9,1. Max = 9 |
| Sequential insertions | x=10, pos=[5,2,8] | 5 4 4 | Each split affects maximum |
| Large x | x=10^9, pos=[500000000] | 500000000 | Handle large values correctly |

---

## When to Use This Pattern

### Use This Approach When:
- You need to track the maximum/minimum of a changing collection
- Insertions split existing items into multiple pieces
- You need O(log n) updates and O(1) or O(log n) queries
- The collection can have duplicate values

### Don't Use When:
- You need range queries (use segment tree instead)
- You need to frequently access by index (use balanced BST with order statistics)
- Memory is extremely constrained (multiset has overhead)

### Pattern Recognition Checklist:
- [ ] Inserting elements that split intervals? Use **set for positions + multiset for lengths**
- [ ] Need dynamic max/min of a collection? Consider **multiset or priority queue**
- [ ] Need to find neighbors of a value? Use **set with upper_bound/lower_bound**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Room Allocation](https://cses.fi/problemset/task/1164) | Practice with set and interval management |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Josephus Problem II](https://cses.fi/problemset/task/2163) | Indexed set for order statistics |
| [My Calendar I](https://leetcode.com/problems/my-calendar-i/) | Interval booking with no overlap |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Range Module](https://leetcode.com/problems/range-module/) | Interval insertion with merging |
| [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) | Merge sort or segment tree approach |

---

## Key Takeaways

1. **The Core Idea:** Adding a position only affects one segment - use this locality for efficiency
2. **Time Optimization:** From O(n^2 log n) to O(n log n) by tracking segments separately
3. **Space Trade-off:** O(n) extra space for segment lengths enables O(log n) updates
4. **Pattern:** Set + Multiset is powerful for dynamic interval problems with max/min queries

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why multiset is needed instead of set for segment lengths
- [ ] Implement the C++ solution using set/multiset in under 15 minutes
- [ ] Handle the "erase one instance" gotcha correctly
- [ ] Trace through a small example showing segment updates

---

## Additional Resources

- [CP-Algorithms: Set and Multiset](https://cp-algorithms.com/)
- [CSES Problem Set](https://cses.fi/problemset/)
- [SortedContainers Documentation](http://www.grantjenks.com/docs/sortedcontainers/)
