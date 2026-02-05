# Painting Fence

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Bizon the Champion isn't just attentive, he also is very hardworking.

Bizon the Champion decided to paint his old fence his favorite color, orange. The fence is represented as n vertical planks, put in a row. Adjacent planks have no gap between them. The planks are numbered from the left to the right starting from one, the i-th plank has the width of 1 meter and the height of ai meters.

Bizon the Champion bought a brush in the shop, the brush's width is 1 meter. He can make vertical and horizontal strokes with the brush. During a stroke the brush's full surface must touch the fence at all the time. What minimum number of strokes should Bizon the Champion do to fully paint the fence? Note that you are allowed to paint the same area of the fence multiple times.

## Input Format
- The first line contains integer n (1 ≤ n ≤ 5000) - the number of fence planks.
- The second line contains n space-separated integers a1, a2, ..., an (1 ≤ ai ≤ 10^9).

## Output Format
Print a single integer - the minimum number of strokes needed to paint the whole fence.

## Solution

### Approach
This is a classic divide and conquer problem. At each step, we have two choices:
1. **Vertical strokes**: Paint each plank vertically (costs = number of planks)
2. **Horizontal strokes**: Find the minimum height plank, paint horizontal strokes up to that height, then recursively solve for the remaining parts

Take the minimum of these two options.

### Python Solution

```python
import sys
sys.setrecursionlimit(10000)

def min_strokes(arr, left, right, painted_height):
 if left > right:
  return 0

 # Find the plank with minimum height in range
 min_idx = left
 for i in range(left, right + 1):
  if arr[i] < arr[min_idx]:
   min_idx = i

 # Option 1: Paint all planks vertically
 vertical_strokes = right - left + 1

 # Option 2: Paint horizontally up to minimum height, then divide
 min_height = arr[min_idx]
 horizontal_strokes = (min_height - painted_height)  # Paint up to min height

 # Recursively solve for left and right parts
 horizontal_strokes += min_strokes(arr, left, min_idx - 1, min_height)
 horizontal_strokes += min_strokes(arr, min_idx + 1, right, min_height)

 return min(vertical_strokes, horizontal_strokes)

def solve():
 n = int(input())
 arr = list(map(int, input().split()))

 print(min_strokes(arr, 0, n - 1, 0))

if __name__ == "__main__":
 solve()
```

### Optimized Solution with Segment Tree (for finding minimum)

```python
import sys
sys.setrecursionlimit(10000)

def build_segment_tree(arr, tree, node, start, end):
 if start == end:
  tree[node] = (arr[start], start)
 else:
  mid = (start + end) // 2
  build_segment_tree(arr, tree, 2*node, start, mid)
  build_segment_tree(arr, tree, 2*node+1, mid+1, end)
  tree[node] = min(tree[2*node], tree[2*node+1])

def query_min(tree, node, start, end, l, r):
 if r < start or end < l:
  return (float('inf'), -1)
 if l <= start and end <= r:
  return tree[node]
 mid = (start + end) // 2
 left_min = query_min(tree, 2*node, start, mid, l, r)
 right_min = query_min(tree, 2*node+1, mid+1, end, l, r)
 return min(left_min, right_min)

def min_strokes(arr, tree, n, left, right, painted_height):
 if left > right:
  return 0

 # Find minimum using segment tree
 min_val, min_idx = query_min(tree, 1, 0, n-1, left, right)

 # Option 1: Vertical strokes
 vertical = right - left + 1

 # Option 2: Horizontal strokes
 horizontal = (min_val - painted_height)
 horizontal += min_strokes(arr, tree, n, left, min_idx - 1, min_val)
 horizontal += min_strokes(arr, tree, n, min_idx + 1, right, min_val)

 return min(vertical, horizontal)

def solve():
 n = int(input())
 arr = list(map(int, input().split()))

 # Build segment tree for range minimum query
 tree = [(float('inf'), -1)] * (4 * n)
 build_segment_tree(arr, tree, 1, 0, n-1)

 print(min_strokes(arr, tree, n, 0, n - 1, 0))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(n²) for basic solution, O(n log n) with segment tree
- **Space Complexity:** O(n) for recursion stack

### Key Insight
The divide and conquer works because after painting horizontal strokes up to the minimum height, the fence splits into independent subproblems that can be solved separately.
