---
layout: simple
title: "Subarray Mode Queries - Range Queries Problem"
permalink: /problem_soulutions/range_queries/subarray_mode_queries_analysis
difficulty: Hard
tags: [range-queries, mo-algorithm, sqrt-decomposition, frequency-counting]
---

# Subarray Mode Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Mo's Algorithm / Sqrt Decomposition |
| **CSES Link** | [Sliding Window Mode](https://cses.fi/problemset/task/3224) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply Mo's Algorithm to answer offline range queries efficiently
- [ ] Maintain frequency counts while adding/removing elements from a range
- [ ] Track the mode (most frequent element) dynamically using auxiliary data structures
- [ ] Understand when sqrt decomposition provides optimal time complexity

---

## Problem Statement

**Problem:** Given an array of n integers and q queries, for each query [l, r], find the mode (most frequent element) in the subarray from index l to r. If multiple elements have the same frequency, return the smallest one.

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers (the array elements)
- Next q lines: Two integers l and r for each query (1-indexed)

**Output:**
- q lines: The mode of each queried subarray

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= q <= 2 x 10^5
- 1 <= arr[i] <= 10^9
- 1 <= l <= r <= n

### Example

```
Input:
8 4
2 7 1 3 2 7 2 1
1 4
2 6
3 8
1 8

Output:
2
7
2
2
```

**Explanation:**
- Query [1,4]: Array [2,7,1,3] - all elements appear once, mode = 1 (smallest)
- Query [2,6]: Array [7,1,3,2,7] - 7 appears twice, mode = 7
- Query [3,8]: Array [1,3,2,7,2,1] - 1 and 2 appear twice, mode = 1 (smallest)
- Query [1,8]: Array [2,7,1,3,2,7,2,1] - 2 appears 3 times, mode = 2

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently answer multiple range frequency queries on a static array?

This is a classic **offline range query** problem. Unlike segment trees which work well for associative operations (sum, min, max), finding the mode requires tracking all element frequencies - which doesn't compose nicely when merging ranges. Mo's Algorithm excels here because it processes queries in a special order that minimizes the total number of add/remove operations.

### Breaking Down the Problem

1. **What are we looking for?** The most frequent element in a range; ties broken by smallest value.
2. **What information do we have?** A static array and multiple query ranges.
3. **What's the relationship?** We need to count frequencies in arbitrary subarrays efficiently.

### Why Standard Data Structures Fail

- **Segment Trees:** Cannot merge "mode" results from child nodes efficiently
- **Prefix Sums:** Work for sum queries, but mode requires full frequency distribution
- **Brute Force:** O(n) per query is too slow for q = 2 x 10^5 queries

### The Key Insight

Mo's Algorithm reorders queries to minimize pointer movements. By sorting queries by block (sqrt(n) sized chunks of left endpoints), we achieve O((n + q) * sqrt(n)) total operations.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the subarray and count frequencies using a hash map.

### Algorithm

1. For each query [l, r]
2. Count frequency of each element in arr[l..r]
3. Find element with maximum frequency (smallest if tied)

### Code

```python
from collections import Counter

def solve_brute_force(n: int, arr: list, queries: list) -> list:
  """
  Brute force solution - count frequencies for each query.

  Time: O(q * n)
  Space: O(n)
  """
  results = []

  for l, r in queries:
    # Convert to 0-indexed
    l -= 1

    # Count frequencies in range
    freq = Counter(arr[l:r])

    # Find mode: max frequency, then min value for ties
    max_freq = max(freq.values())
    mode = min(val for val, cnt in freq.items() if cnt == max_freq)

    results.append(mode)

  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(n) | Hash map stores at most n elements |

### Why This Works (But Is Slow)

Correctness is guaranteed - we examine every element. However, with n = q = 2 x 10^5, we perform up to 4 x 10^10 operations, which is far too slow.

---

## Solution 2: Mo's Algorithm (Optimal)

### Key Insight

> **The Trick:** Process queries offline in a special order that minimizes total pointer movements to O((n + q) * sqrt(n)).

### Mo's Algorithm Overview

| Concept | Description |
|---------|-------------|
| **Block Size** | sqrt(n) - divides array into chunks |
| **Query Ordering** | Sort by (left / block_size, right) |
| **Pointer Movement** | Maintain current range [cur_l, cur_r], expand/shrink to reach query |

**Why this ordering works:** Within a block, left pointer moves at most sqrt(n). Across all queries, right pointer is monotonic within each block, giving O(n) per block.

### Data Structures Needed

To track mode efficiently during add/remove:
1. `freq[x]` - frequency of element x in current range
2. `count[f]` - set of elements with frequency f
3. `max_freq` - current maximum frequency

### Algorithm

1. Compress coordinates (values can be up to 10^9)
2. Sort queries by (l // block_size, r)
3. Process queries in order, maintaining [cur_l, cur_r]
4. For each query, expand/shrink to match, updating frequency structures
5. Answer = smallest element with max_freq

### Dry Run Example

Let's trace through with `arr = [2, 7, 1, 3, 2]` and queries `[(1,3), (2,4), (1,5)]`:

```
Coordinate Compression:
  Values: [1, 2, 3, 7] -> Indices: {1:0, 2:1, 3:2, 7:3}

Block size = sqrt(5) = 2

Sort queries by (l//2, r):
  (1,3) -> block 0, r=3
  (2,4) -> block 1, r=4
  (1,5) -> block 0, r=5

Sorted order: [(1,3), (1,5), (2,4)]

Initial: cur_l=1, cur_r=0 (empty range)
         freq = [0,0,0,0], max_freq = 0

Query 1: [1,3] = [2,7,1]
  Add arr[1]=2: freq[1]++, freq=[0,1,0,0], max_freq=1
  Add arr[2]=7: freq[3]++, freq=[0,1,0,1], max_freq=1
  Add arr[3]=1: freq[0]++, freq=[1,1,0,1], max_freq=1
  Mode = min(1,2,7) = 1

Query 2: [1,5] = [2,7,1,3,2]
  Add arr[4]=3: freq[2]++, freq=[1,1,1,1], max_freq=1
  Add arr[5]=2: freq[1]++, freq=[1,2,1,1], max_freq=2
  Mode = 2 (only element with freq 2)

Query 3: [2,4] = [7,1,3]
  Remove arr[1]=2: freq[1]--, freq=[1,1,1,1], max_freq=1
  Remove arr[5]=2: freq[1]--, freq=[1,0,1,1], max_freq=1
  Mode = min(7,1,3) = 1
```

### Code

```python
import sys
from math import isqrt
from collections import defaultdict
from sortedcontainers import SortedList

def solve_mo_algorithm(n: int, arr: list, queries: list) -> list:
  """
  Mo's Algorithm for subarray mode queries.

  Time: O((n + q) * sqrt(n) * log(n))
  Space: O(n)
  """
  input = sys.stdin.readline

  # Coordinate compression
  sorted_vals = sorted(set(arr))
  compress = {v: i for i, v in enumerate(sorted_vals)}
  compressed = [compress[x] for x in arr]

  # Block size for Mo's algorithm
  block_size = max(1, isqrt(n))

  # Attach original indices and sort queries
  indexed_queries = [(l-1, r-1, i) for i, (l, r) in enumerate(queries)]
  indexed_queries.sort(key=lambda x: (x[0] // block_size, x[1]))

  # Frequency tracking
  freq = [0] * len(sorted_vals)
  count = defaultdict(SortedList)  # count[f] = sorted list of elements with frequency f
  count[0] = SortedList(range(len(sorted_vals)))
  max_freq = 0

  def add(idx):
    nonlocal max_freq
    val = compressed[idx]
    old_freq = freq[val]
    count[old_freq].remove(val)
    freq[val] += 1
    count[freq[val]].add(val)
    max_freq = max(max_freq, freq[val])

  def remove(idx):
    nonlocal max_freq
    val = compressed[idx]
    old_freq = freq[val]
    count[old_freq].remove(val)
    freq[val] -= 1
    count[freq[val]].add(val)
    # Update max_freq if needed
    if old_freq == max_freq and len(count[old_freq]) == 0:
      max_freq -= 1

  def get_mode():
    if max_freq == 0:
      return sorted_vals[count[0][0]]
    return sorted_vals[count[max_freq][0]]

  # Process queries
  results = [0] * len(queries)
  cur_l, cur_r = 0, -1

  for l, r, orig_idx in indexed_queries:
    # Expand/shrink to reach [l, r]
    while cur_r < r:
      cur_r += 1
      add(cur_r)
    while cur_l > l:
      cur_l -= 1
      add(cur_l)
    while cur_r > r:
      remove(cur_r)
      cur_r -= 1
    while cur_l < l:
      remove(cur_l)
      cur_l += 1

    results[orig_idx] = get_mode()

  return results


def main():
  input_data = sys.stdin.read().split()
  idx = 0
  n, q = int(input_data[idx]), int(input_data[idx+1])
  idx += 2
  arr = [int(input_data[idx+i]) for i in range(n)]
  idx += n
  queries = []
  for _ in range(q):
    l, r = int(input_data[idx]), int(input_data[idx+1])
    queries.append((l, r))
    idx += 2

  results = solve_mo_algorithm(n, arr, queries)
  print('\n'.join(map(str, results)))


if __name__ == "__main__":
  main()
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) * sqrt(n) * log(n)) | Mo's algorithm with set operations |
| Space | O(n) | Frequency arrays and sets |

---

## Common Mistakes

### Mistake 1: Wrong Query Ordering

```python
# WRONG - sorting only by left endpoint
queries.sort(key=lambda x: x[0])

# CORRECT - sort by block, then by right endpoint
queries.sort(key=lambda x: (x[0] // block_size, x[1]))
```

**Problem:** Without block-based sorting, pointer movements can be O(n) per query.
**Fix:** Use Mo's ordering: (left // block_size, right).

### Mistake 2: Forgetting to Update max_freq on Remove

```python
# WRONG
def remove(idx):
  val = compressed[idx]
  count[freq[val]].remove(val)
  freq[val] -= 1
  count[freq[val]].add(val)
  # Missing: update max_freq!
```

**Problem:** max_freq stays high even when no elements have that frequency.
**Fix:** Check if the old frequency bucket is now empty and was the max.

### Mistake 3: Off-by-One in Indexing

```python
# WRONG - 1-indexed input used directly as 0-indexed
for l, r in queries:
  while cur_r < r:  # r should be r-1 for 0-indexed
    add(++cur_r)
```

**Problem:** Accessing arr[n] causes index out of bounds.
**Fix:** Convert to 0-indexed: `l -= 1; r -= 1` before processing.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, arr=[5], query=[1,1]` | 5 | Only one element |
| All same | `n=5, arr=[3,3,3,3,3], query=[1,5]` | 3 | Clear mode |
| All unique | `n=3, arr=[1,2,3], query=[1,3]` | 1 | Tie-break: smallest |
| Large values | `arr=[10^9], query=[1,1]` | 10^9 | Coordinate compression handles this |
| Full range query | `query=[1,n]` | Global mode | Tests initialization |

---

## When to Use This Pattern

### Use Mo's Algorithm When:
- Queries are offline (known in advance)
- Adding/removing elements is O(1) or O(log n)
- No efficient segment tree composition exists
- Query count q is comparable to n

### Do Not Use When:
- Queries must be answered online (in order)
- Updates to the array are required (use other structures)
- Simple composition exists (sum, min, max - use segment tree)

### Pattern Recognition Checklist:
- [ ] Multiple range queries on static array? **Consider Mo's Algorithm**
- [ ] Need to track frequencies in range? **Mo's + frequency structures**
- [ ] Online queries required? **Consider persistent data structures**
- [ ] Associative operation (sum, min)? **Use Segment Tree instead**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Basic prefix sum technique |
| [Distinct Values Queries](https://cses.fi/problemset/task/1734) | Mo's Algorithm introduction |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Sliding Window Mode](https://cses.fi/problemset/task/3224) | Fixed window size variant |
| [Sliding Window Median](https://cses.fi/problemset/task/1076) | Median instead of mode |
| [Majority Element II](https://leetcode.com/problems/majority-element-ii/) | Single query, special frequency |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Range Updates and Sums](https://cses.fi/problemset/task/1735) | Lazy propagation |
| [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Top-k tracking |

---

## Key Takeaways

1. **The Core Idea:** Mo's Algorithm reorders queries to minimize total element additions/removals
2. **Time Optimization:** From O(q * n) brute force to O((n + q) * sqrt(n))
3. **Space Trade-off:** O(n) for frequency tracking structures
4. **Pattern:** Offline range queries where segment trees do not apply

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why Mo's ordering minimizes total operations
- [ ] Implement coordinate compression correctly
- [ ] Handle the mode tracking with add/remove in O(log n)
- [ ] Identify when Mo's Algorithm is the right approach
