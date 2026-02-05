---
title: "Coordinate Compression - Efficient Value Mapping"
category: Techniques
difficulty: Easy-Medium
---

# Coordinate Compression - Efficient Value Mapping

## Problem Overview

| Aspect | Details |
|--------|---------|
| Technique | Map large/sparse values to small consecutive integers |
| Use Case | When value range is huge but count of distinct values is small |
| Benefit | Enables array indexing, reduces memory, speeds up algorithms |
| Time | O(n log n) for sorting + O(1) per lookup |
| Space | O(n) for mapping |

## What is Coordinate Compression?

Coordinate compression maps a set of values to consecutive integers [0, k-1] where k is the number of distinct values, preserving relative order.

**Example:**
```
Original:  [1000000, 5, 999999, 5, 500000]
Distinct sorted: [5, 500000, 999999, 1000000]
Mapping:   5->0, 500000->1, 999999->2, 1000000->3
Compressed: [3, 0, 2, 0, 1]
```

**Why useful:**
- Original range: 0 to 10^9 (can't create array this large)
- Compressed range: 0 to 4 (easy to index)

## When to Use

| Scenario | Without Compression | With Compression |
|----------|--------------------|--------------------|
| Segment tree on values | O(10^9) space | O(n) space |
| Counting sort on large values | Impossible | O(n) |
| 2D grid with sparse points | Memory limit | Feasible |

## Implementation

### Python Solution
```python
def compress(arr):
  """
  Compress array values to consecutive integers.
  Returns compressed array and mappings.
  """
  # Get sorted unique values
  sorted_unique = sorted(set(arr))

  # Create value -> compressed index mapping
  val_to_idx = {v: i for i, v in enumerate(sorted_unique)}

  # Compress the array
  compressed = [val_to_idx[v] for v in arr]

  return compressed, val_to_idx, sorted_unique

# Example usage
arr = [1000000, 5, 999999, 5, 500000]
compressed, mapping, original = compress(arr)
print(f"Compressed: {compressed}")  # [3, 0, 2, 0, 1]
print(f"Mapping: {mapping}")        # {5: 0, 500000: 1, 999999: 2, 1000000: 3}
```

### Common Applications

### 1. Range Queries with Large Values

```python
def count_in_range(arr, queries):
  """
  Count elements in range [l, r] for each query.
  Values can be up to 10^9.
  """
  # Compress values
  compressed, val_to_idx, sorted_vals = compress(arr)
  n_unique = len(sorted_vals)

  # Build frequency array on compressed values
  freq = [0] * n_unique
  for c in compressed:
    freq[c] += 1

  # Build prefix sum for range queries
  prefix = [0] * (n_unique + 1)
  for i in range(n_unique):
    prefix[i + 1] = prefix[i] + freq[i]

  results = []
  for l, r in queries:
    # Find compressed indices for l and r
    l_idx = bisect.bisect_left(sorted_vals, l)
    r_idx = bisect.bisect_right(sorted_vals, r)
    results.append(prefix[r_idx] - prefix[l_idx])

  return results
```

### 2. 2D Coordinate Compression

```python
def compress_2d(points):
  """
  Compress both x and y coordinates independently.
  """
  xs = sorted(set(p[0] for p in points))
  ys = sorted(set(p[1] for p in points))

  x_map = {x: i for i, x in enumerate(xs)}
  y_map = {y: i for i, y in enumerate(ys)}

  compressed_points = [(x_map[x], y_map[y]) for x, y in points]
  return compressed_points, len(xs), len(ys)

# Example: Points with coordinates up to 10^9
points = [(1000000000, 1), (5, 999999999), (1000000000, 999999999)]
comp_points, w, h = compress_2d(points)
# Now can create w x h grid instead of 10^9 x 10^9
```

### 3. Segment Tree on Values

```python
class SegmentTreeOnValues:
  """
  Segment tree indexed by values (after compression).
  Useful for: count of elements in value range, etc.
  """
  def __init__(self, arr):
    self.compressed, self.mapping, self.original = compress(arr)
    self.n = len(self.original)
    self.tree = [0] * (4 * self.n)

    # Insert compressed values
    for c in self.compressed:
      self._update(1, 0, self.n - 1, c, 1)

  def _update(self, node, start, end, idx, delta):
    if start == end:
      self.tree[node] += delta
    else:
      mid = (start + end) // 2
      if idx <= mid:
        self._update(2 * node, start, mid, idx, delta)
      else:
        self._update(2 * node + 1, mid + 1, end, idx, delta)
      self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

  def count_in_range(self, l, r):
    """Count elements with value in [l, r]."""
    # Map to compressed indices
    import bisect
    l_idx = bisect.bisect_left(self.original, l)
    r_idx = bisect.bisect_right(self.original, r) - 1
    if l_idx > r_idx:
      return 0
    return self._query(1, 0, self.n - 1, l_idx, r_idx)
```

## Complexity Analysis

| Operation | Time | Notes |
|-----------|------|-------|
| Sort unique values | O(n log n) | One-time preprocessing |
| Build mapping | O(n) | Hash map or sorted array |
| Compress one value | O(1) or O(log n) | Hash map vs binary search |
| **Total compression** | **O(n log n)** | Dominated by sorting |

## Common Mistakes

1. **Not handling duplicates:** Use `set()` before sorting
2. **Off-by-one in binary search:** Use `lower_bound` vs `upper_bound` correctly
3. **Forgetting to decompress:** Store original values if needed for output
4. **Compressing queries separately:** Query values might not be in original array

## When NOT to Use

- Values already small (0 to n-1)
- Only need to compare values (not index them)
- Single pass algorithm that doesn't need random access

## Key Takeaways

- Coordinate compression reduces large value ranges to [0, k-1]
- Essential for segment trees and BITs on value ranges
- O(n log n) preprocessing enables O(1) or O(log n) lookups
- Preserve original values if output needs them
- Common in competitive programming for handling 10^9 value ranges
