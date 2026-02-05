---
layout: simple
title: "Restaurant Customers"
difficulty: Easy
tags: [sorting, sweep-line, events]
cses_link: https://cses.fi/problemset/task/1619
permalink: /problem_soulutions/sorting_and_searching/restaurant_customers_analysis
---

# Restaurant Customers

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find maximum simultaneous customers in a restaurant |
| Input | n customers with arrival and leaving times |
| Output | Maximum number of customers at any point in time |
| Constraints | 1 <= n <= 2x10^5, 1 <= arrival < leaving <= 10^9 |
| Core Technique | Sweep Line / Event Processing |

## Learning Goals

After solving this problem, you will understand:
- **Sweep line technique**: Processing events in sorted time order
- **Event-based processing**: Converting intervals to discrete events
- How to track running counts efficiently during a sweep

## Problem Statement

You are given n customers, each with an arrival time and a leaving time. Find the maximum number of customers that are in the restaurant at the same time.

**Example:**
```
Input:
3
5 8
2 4
3 9

Output:
2
```

## Key Insight

Instead of checking every time point, convert the problem into **events**:
- Each arrival = `+1` (customer enters)
- Each leaving = `-1` (customer exits)

Sort all events by time, then sweep through them while tracking the running count.

**Critical tie-breaking rule**: When an arrival and departure happen at the same time, the problem states `arrival < leaving`, so a customer present at time `t` means `arrival <= t < leaving`. Process departures (`-1`) before arrivals (`+1`) at the same timestamp to avoid counting a leaving customer and arriving customer as simultaneous.

## Event Processing Algorithm

```
1. Create events:
   - For each customer (a, b): add (a, +1) and (b, -1)

2. Sort events by (time, type):
   - type = -1 comes before type = +1 at same time

3. Sweep through events:
   - Maintain current_count
   - Update max_count after each event
```

## Visual Diagram

```
Customers: (5,8), (2,4), (3,9)

Timeline:
Time:    2    3    4    5    6    7    8    9
         |    |    |    |    |    |    |    |
Cust 2:  [====]
Cust 3:  [========================]
Cust 1:            [==============]

Events (sorted):
  t=2: +1 -> count=1
  t=3: +1 -> count=2  <-- max
  t=4: -1 -> count=1
  t=5: +1 -> count=2  <-- also max
  t=8: -1 -> count=1
  t=9: -1 -> count=0

Maximum simultaneous customers: 2
```

## Dry Run

| Step | Time | Event | Current Count | Max Count |
|------|------|-------|---------------|-----------|
| 1    | 2    | +1    | 1             | 1         |
| 2    | 3    | +1    | 2             | 2         |
| 3    | 4    | -1    | 1             | 2         |
| 4    | 5    | +1    | 2             | 2         |
| 5    | 8    | -1    | 1             | 2         |
| 6    | 9    | -1    | 0             | 2         |

**Answer: 2**

## Python Solution

```python
def max_customers(customers):
    """
    Find maximum simultaneous customers using sweep line.

    Args:
        customers: list of (arrival, departure) tuples

    Returns:
        Maximum number of customers at any time
    """
    events = []

    # Create events: (time, type)
    # type: -1 for departure, +1 for arrival
    # Using -1/+1 ensures departures sort before arrivals at same time
    for arrival, departure in customers:
        events.append((arrival, 1))     # arrival = +1
        events.append((departure, -1))  # departure = -1

    # Sort by time, then by type (departures first due to -1 < 1)
    events.sort()

    current = 0
    max_count = 0

    for time, delta in events:
        current += delta
        max_count = max(max_count, current)

    return max_count


# CSES submission format
def solve():
    n = int(input())
    customers = []
    for _ in range(n):
        a, b = map(int, input().split())
        customers.append((a, b))

    print(max_customers(customers))


if __name__ == "__main__":
    solve()
```

## Why Tie-Breaking Matters

Consider a case where one customer leaves at time 5 and another arrives at time 5:
- Customer A: (3, 5) - leaves at 5
- Customer B: (5, 8) - arrives at 5

**Correct interpretation**: Customer A has left before B arrives (they are NOT simultaneous).

If we process arrivals before departures at the same time:
- t=5: +1 (B arrives) -> count=2  **WRONG!**
- t=5: -1 (A leaves) -> count=1

If we process departures before arrivals (correct):
- t=5: -1 (A leaves) -> count=0
- t=5: +1 (B arrives) -> count=1  **CORRECT!**

The sorting trick: Use `-1` for departures, `+1` for arrivals. When sorting pairs, `(5, -1)` comes before `(5, 1)` automatically.

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Wrong tie-breaking order | Over-counts at boundaries | Use -1 for departures, +1 for arrivals |
| Forgetting to update max after each event | Missing the true maximum | Always update max_count after adding delta |
| Using wrong interval semantics | Incorrect boundary handling | Understand: customer present when arrival <= t < leaving |
| Not sorting events | Random order gives wrong answer | Always sort by (time, type) |

## Complexity Analysis

| Metric | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n log n) | Sorting 2n events dominates |
| Space | O(n) | Storing 2n events |

The sweep itself is O(n), but sorting is O(n log n), making that the bottleneck.

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | LeetCode | Find minimum rooms needed |
| [Car Pooling](https://leetcode.com/problems/car-pooling/) | LeetCode | Capacity constraint added |
| [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) | LeetCode | Online queries |
| [Movie Festival](https://cses.fi/problemset/task/1629) | CSES | Select maximum non-overlapping |

## Summary

The sweep line technique transforms interval problems into event processing:

1. **Model**: Convert intervals to +1/-1 events
2. **Sort**: Order events by time (with proper tie-breaking)
3. **Sweep**: Linear scan tracking running count
4. **Answer**: Maximum count observed during sweep

This pattern applies to many interval overlap, scheduling, and resource allocation problems.
