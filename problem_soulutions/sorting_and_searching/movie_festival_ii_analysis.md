---
layout: simple
title: "Movie Festival II - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/movie_festival_ii_analysis
difficulty: Medium
tags: [greedy, multiset, interval-scheduling, sorting]
prerequisites: [movie_festival]
---

# Movie Festival II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Greedy + Multiset |
| **CSES Link** | [Movie Festival II](https://cses.fi/problemset/task/1632) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Extend interval scheduling from one resource to k resources
- [ ] Use multiset to efficiently track and update k member states
- [ ] Apply greedy selection with optimal member assignment
- [ ] Understand when sorted containers outperform heap-based approaches

---

## Problem Statement

**Problem:** In a movie festival, n movies will be shown. You have k club members who can watch movies. Each movie has a start time and end time. A member can watch at most one movie at a time, and movies cannot overlap (a member finishing a movie at time t can start another at time t). What is the maximum total number of movies the club members can watch?

**Input:**
- Line 1: Two integers n and k (number of movies and club members)
- Lines 2 to n+1: Two integers a and b (start and end time of each movie)

**Output:**
- One integer: the maximum number of movies that can be watched

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= k <= 2 x 10^5
- 1 <= a < b <= 10^9

### Example

```
Input:
5 2
1 5
8 10
3 6
2 5
6 9

Output:
4
```

**Explanation:** With k=2 members, we can schedule:
- Member 1: Movie [1,5] then [6,9]
- Member 2: Movie [2,5] then [8,10]

Total: 4 movies watched.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How does this differ from Movie Festival with one member?

This is an extension of the classic interval scheduling problem. With k=1 member, we simply sort by end time and greedily pick non-overlapping movies. With k members, we need to track each member's availability and assign each movie to the most suitable member.

### Breaking Down the Problem

1. **What are we looking for?** Maximum number of non-overlapping movies across k members.
2. **What information do we have?** Start/end times and number of members.
3. **What's the relationship?** Each member maintains their own "last end time" - we need to efficiently find and update the best member for each movie.

### The Key Insight

> **Greedy Strategy:** For each movie (sorted by end time), assign it to the member who finished most recently but still before this movie's start time.

Why assign to the member who finished most recently (among those available)?
- This leaves members with earlier end times free for potentially shorter movies that might fit later
- Maximizes flexibility for future assignments

### Analogies

Think of this problem like scheduling customers to k service counters. When a new customer arrives, you want to assign them to the counter that just became free (not one that's been idle for hours), because the recently-freed counter is better "utilized" and leaves the long-idle counters available for rush periods.

---

## Solution 1: Brute Force

### Idea

For each movie, try assigning it to each of the k members and check if valid. Use backtracking to explore all possibilities.

### Algorithm

1. Sort movies by end time
2. For each movie, try all k members
3. If member is available (their last end time <= movie start), assign and recurse
4. Track maximum movies achieved

### Code

```python
def solve_brute_force(movies, k):
 """
 Brute force: try all possible assignments.

 Time: O(k^n) - exponential
 Space: O(n) - recursion stack
 """
 movies.sort(key=lambda x: x[1])  # Sort by end time
 n = len(movies)

 def backtrack(idx, member_end_times):
  if idx == n:
   return 0

  # Option 1: Skip this movie
  best = backtrack(idx + 1, member_end_times)

  # Option 2: Try assigning to each member
  start, end = movies[idx]
  for i in range(k):
   if member_end_times[i] <= start:
    old_end = member_end_times[i]
    member_end_times[i] = end
    best = max(best, 1 + backtrack(idx + 1, member_end_times))
    member_end_times[i] = old_end

  return best

 return backtrack(0, [0] * k)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(k^n) | Each movie can go to k members or be skipped |
| Space | O(n) | Recursion depth |

### Why This Works (But Is Slow)

The brute force explores all valid assignments, guaranteeing the optimal answer. However, exponential time makes it impractical for n up to 2x10^5.

---

## Solution 2: Greedy with Linear Search (O(nk))

### Idea

Sort by end time and greedily assign each movie to an available member. Linear search through k members to find one that's free.

### Code

```python
def solve_greedy_linear(movies, k):
 """
 Greedy with linear search for available member.

 Time: O(n*k) after O(n log n) sort
 Space: O(k)
 """
 movies.sort(key=lambda x: x[1])  # Sort by end time
 member_ends = [0] * k  # Last end time for each member
 count = 0

 for start, end in movies:
  # Find any available member
  for i in range(k):
   if member_ends[i] <= start:
    member_ends[i] = end
    count += 1
    break

 return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(nk) | Linear search through k members for each movie |
| Space | O(k) | Track end times for k members |

This works but is too slow when both n and k are large (2x10^5 each).

---

## Solution 3: Optimal - Greedy with Multiset (O(n log k))

### Key Insight

> **The Trick:** Use a multiset (ordered set with duplicates) to store member end times. For each movie, use binary search to find the best available member in O(log k).

### Why Multiset?

We need a data structure that:
1. Allows duplicate values (multiple members can have same end time)
2. Supports efficient search for "largest value <= target" (upper_bound)
3. Supports efficient insertion and deletion

A **multiset** (C++) or **SortedList** (Python) provides all three in O(log k).

### Algorithm

1. Sort movies by end time
2. Initialize multiset with k zeros (all members available at time 0)
3. For each movie [start, end]:
   - Find the largest end time <= start (member who finished most recently but is still available)
   - If found: remove that end time, insert the new end time, increment count
   - If not found: skip this movie (no member available)
4. Return count

### Dry Run Example

Let's trace through with `n=5, k=2, movies=[[1,5], [8,10], [3,6], [2,5], [6,9]]`:

```
After sorting by end time:
  Movies: [[1,5], [2,5], [3,6], [6,9], [8,10]]

Initial state:
  Multiset: {0, 0}  (both members free at time 0)
  Count: 0

Step 1: Process movie [1,5]
  Find largest value <= 1 in {0, 0}
  Found: 0
  Remove 0, insert 5
  Multiset: {0, 5}, Count: 1

Step 2: Process movie [2,5]
  Find largest value <= 2 in {0, 5}
  Found: 0
  Remove 0, insert 5
  Multiset: {5, 5}, Count: 2

Step 3: Process movie [3,6]
  Find largest value <= 3 in {5, 5}
  Not found (5 > 3)
  Skip this movie
  Multiset: {5, 5}, Count: 2

Step 4: Process movie [6,9]
  Find largest value <= 6 in {5, 5}
  Found: 5
  Remove 5, insert 9
  Multiset: {5, 9}, Count: 3

Step 5: Process movie [8,10]
  Find largest value <= 8 in {5, 9}
  Found: 5
  Remove 5, insert 10
  Multiset: {9, 10}, Count: 4

Final answer: 4
```

### Visual Diagram

```
Movies sorted by end time:
  [1,5]  [2,5]  [3,6]  [6,9]  [8,10]

Timeline:
  Member 1: |--[1,5]--|        |--[6,9]--|
  Member 2:    |--[2,5]--|              |--[8,10]--|

  0    1    2    3    4    5    6    7    8    9    10
  |----|----|----|----|----|----|----|----|----|----|
       [===1,5===]
          [===2,5===]
             [===3,6===] X (no one available)
                        [====6,9====]
                                  [====8,10====]
```

### Code (Python)

```python
from sortedcontainers import SortedList

def solve_optimal(movies, k):
 """
 Optimal solution using SortedList (multiset equivalent).

 Time: O(n log n) for sort + O(n log k) for processing
 Space: O(k) for SortedList
 """
 movies.sort(key=lambda x: x[1])  # Sort by end time

 # Multiset of member end times (all start at 0)
 member_ends = SortedList([0] * k)
 count = 0

 for start, end in movies:
  # Find largest end time <= start
  # bisect_right gives index where start would be inserted
  # So index - 1 is the largest value <= start
  idx = member_ends.bisect_right(start) - 1

  if idx >= 0:
   # Found an available member
   member_ends.remove(member_ends[idx])
   member_ends.add(end)
   count += 1

 return count

# Main
def main():
 import sys
 input = sys.stdin.readline

 n, k = map(int, input().split())
 movies = []
 for _ in range(n):
  a, b = map(int, input().split())
  movies.append((a, b))

 print(solve_optimal(movies, k))

if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n + n log k) | Sorting + n multiset operations |
| Space | O(n + k) | Movies array + multiset |

---

## Common Mistakes

### Mistake 1: Sorting by Start Time Instead of End Time

**Problem:** Greedy interval scheduling MUST sort by end time to work correctly.
**Fix:** Always sort by end time for maximum non-overlapping intervals.

### Mistake 2: Using lower_bound Instead of upper_bound

**Problem:** `lower_bound` finds first element >= start, but we need the largest element <= start.
**Fix:** Use `upper_bound` and decrement (with boundary check).

### Mistake 3: Forgetting Boundary Check

**Problem:** If all members are busy (all end times > start), upper_bound returns begin().
**Fix:** Check if iterator equals begin() before decrementing.

### Mistake 4: Using set Instead of multiset

**Problem:** Multiple members can have the same end time. A set would collapse them.
**Fix:** Use multiset to handle duplicate end times.

### Mistake 5: Not Removing Before Inserting

**Problem:** Member count grows beyond k if we don't remove the old end time.
**Fix:** Always remove the old end time before inserting the new one.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single movie, single member | `n=1, k=1, [[1,2]]` | `1` | Trivial case |
| More members than movies | `n=2, k=5, [[1,2],[3,4]]` | `2` | All movies watched |
| All movies overlap | `n=3, k=1, [[1,5],[2,6],[3,7]]` | `1` | Only one can be watched |
| All movies overlap, k members | `n=3, k=3, [[1,5],[2,6],[3,7]]` | `3` | Each member takes one |
| Back-to-back movies | `n=3, k=1, [[1,2],[2,3],[3,4]]` | `3` | End time = start time is valid |
| Large time values | `n=2, k=1, [[1,10^9],[10^9,2*10^9]]` | `2` | Handle large integers |
| k larger than needed | `n=5, k=1000, ...` | `<=5` | Extra members don't help |

---

## When to Use This Pattern

### Use This Approach When:
- Scheduling tasks/events on multiple resources
- Finding maximum non-overlapping intervals with k parallel processors
- Any problem that extends single-resource greedy to k resources

### Don't Use When:
- k = 1 (simpler single-resource greedy suffices)
- Need to minimize resources instead of maximize tasks (use different approach)
- Intervals have weights/priorities (need DP or more complex greedy)

### Pattern Recognition Checklist:
- [ ] Interval scheduling with multiple resources? **Consider multiset + greedy**
- [ ] Need to track k states and efficiently update? **Consider ordered set/multiset**
- [ ] Finding "best available" among k options? **Binary search in sorted structure**

---

## Why Not Use a Heap?

A common question: why not use a min-heap instead of multiset?

**Heap limitation:** A heap efficiently gives the minimum, but we need the **largest value that is still <= start**. This requires:
1. Extract elements until we find one <= start
2. Put back all extracted elements > start

This is O(k) per operation in the worst case.

**Multiset advantage:** Binary search directly finds the target in O(log k).

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Movie Festival](https://cses.fi/problemset/task/1629) | Single member version - master this first |
| [LeetCode 435: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Minimum removals for non-overlap |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Room Allocation](https://cses.fi/problemset/task/1164) | Find minimum rooms needed (opposite direction) |
| [LeetCode 253: Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Minimum meeting rooms needed |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LeetCode 1235: Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Weighted interval scheduling with DP |
| [CSES: Task Assignment](https://cses.fi/problemset/task/2129) | Hungarian algorithm for optimal assignment |

---

## Key Takeaways

1. **The Core Idea:** Extend single-resource greedy to k resources using a multiset to track all member states.
2. **Time Optimization:** From O(nk) linear search to O(n log k) using binary search in sorted structure.
3. **Critical Operation:** Find largest value <= target efficiently with upper_bound then decrement.
4. **Pattern:** Multi-resource interval scheduling = greedy + ordered set with duplicates.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve Movie Festival (k=1) without looking at solution
- [ ] Explain why we sort by end time, not start time
- [ ] Implement multiset solution in both Python and C++
- [ ] Explain why multiset is better than heap for this problem
- [ ] Handle all edge cases correctly

---

## Additional Resources

- [CSES Movie Festival II](https://cses.fi/problemset/task/1632) - Multi-member scheduling
- [CP-Algorithms: Interval Scheduling](https://cp-algorithms.com/)
- [Python SortedContainers Documentation](http://www.grantjenks.com/docs/sortedcontainers/)
