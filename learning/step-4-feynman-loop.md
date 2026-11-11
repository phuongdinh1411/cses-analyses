# Step 4 — Feynman Loop: Heap (Data Structures & Algorithms)

## Simple Explanation (ELI12)

### The Core Idea
A heap is like a tournament line — the best player (min or max) is always at the front, automatically.

### Structure
- A **complete binary tree** where every parent beats its children
- **Min-heap**: parent ≤ children (root = smallest)
- **Max-heap**: parent ≥ children (root = largest)
- NOT fully sorted — only the root is guaranteed min/max

### Array Representation
```
Tree:  1, 3, 2, 7, 4, 5, 6
Index: 0  1  2  3  4  5  6

parent(i)      = (i-1) // 2
left_child(i)  = 2*i + 1
right_child(i) = 2*i + 2
```

### Insert (Sift-Up)
1. Append to end
2. Bubble up — swap with parent while smaller than parent
- O(log n)

### Extract-Min (Sift-Down)
1. Remove root, put last element at root
2. Bubble down — swap with smaller child while larger than children
- O(log n)

### Python Usage
```python
import heapq
heapq.heappush(heap, val)       # insert
heapq.heappop(heap)             # extract min
# Max-heap: push -val, pop and negate
```

### When to Use
- Always get min/max → O(1)
- Remove min/max → O(log n)
- Top-K, scheduling, streaming, shortest path
