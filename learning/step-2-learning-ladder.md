# Step 2 — Learning Ladder: Heap (Data Structures & Algorithms)

## Level 1: Complete Beginner — "I understand what a heap IS"

### What you should understand
- A heap is a complete binary tree stored in an array
- Two types: Min-Heap (root = smallest) and Max-Heap (root = largest)
- Heap property: every parent ≤ (min-heap) or ≥ (max-heap) its children
- Index math:
  - parent(i)      = (i - 1) // 2
  - left_child(i)  = 2*i + 1
  - right_child(i) = 2*i + 2

### Mastery looks like
- Can draw a min/max-heap from a list by hand
- Can identify whether a given array is a valid heap
- Can explain index math without notes

### Key concepts
- Complete binary tree definition
- Heap property (structural + ordering)
- Array representation and index formulas

### 🏁 Milestone
Given [3, 1, 6, 5, 2, 4], draw it as a tree, verify if it's a valid min-heap.

### 🛠️ Exercise
Draw [1, 3, 2, 7, 4, 5] as a tree. Is it a valid min-heap? Why?

### ⚠️ Common mistakes
- Confusing complete binary tree with full binary tree
- Thinking the heap is fully sorted — only root is guaranteed min/max
- Getting index formula wrong for 1-indexed vs 0-indexed

### ✅ Self-check
"Can I explain the heap property and index formulas to someone without notes?"

---

## Level 2: Basic Understanding — "I can insert and remove from a heap"

### What you should understand
- Sift-up: after insert, bubble new element up → O(log n)
- Sift-down: after removing root, move last to root, bubble down → O(log n)
- Build-heap: convert unsorted array to heap in O(n) (not O(n log n)!)

### Mastery looks like
- Can trace insert and delete-min step by step on paper
- Can implement MinHeap from scratch in Python (~40 lines)
- Can explain why build-heap is O(n)

### Key concepts
- Insert = append + sift-up
- Extract-min = swap root with last + pop last + sift-down
- Build-heap = sift-down all non-leaves from right to left

### 🏁 Milestone
Implement MinHeap with push(), pop(), peek() — without using heapq.

### 🛠️ Exercise
```python
class MinHeap:
    def __init__(self): self.heap = []
    def push(self, val): ...   # sift-up
    def pop(self): ...         # sift-down
    def peek(self): ...
```
Test: push [5,3,8,1,2], repeated pops should give [1,2,3,5,8].

### ⚠️ Common mistakes
- Forgetting bounds check in sift-down
- Only checking left child, ignoring right
- Wrong start index in build-heap (should be n//2 - 1)

### ✅ Self-check
"Can I implement push and pop from memory and explain why each is O(log n)?"

---

## Level 3: Practical User — "I can use Python's heapq to solve real problems"

### What you should understand
- heapq is min-heap only — max-heap requires negation (-val)
- Key API: heappush, heappop, heapify, nlargest, nsmallest
- Tuples: heappush(heap, (priority, value))
- Top-K pattern: O(n log k) vs O(n log n) sort

### Key API
```python
import heapq
heapq.heappush(heap, val)
heapq.heappop(heap)
heapq.heapify(lst)           # O(n), in-place
heapq.nlargest(k, lst)
heapq.nsmallest(k, lst)
# Max-heap: push -val, pop and negate
```

### 🏁 Milestone
Solve LeetCode 215 (Kth Largest) and 347 (Top K Frequent) using heapq.

### ⚠️ Common mistakes
- Using nlargest() for streaming — it reprocesses everything
- Equal priorities causing tuple comparison errors
- Forgetting to negate on extract from max-heap

### ✅ Self-check
"Can I solve a Top-K problem in under 10 minutes without googling the API?"

---

## Level 4: Problem Solver — "I recognize heap patterns in hard problems"

### The 6 Core Heap Patterns
| Pattern | Example Problems |
|---|---|
| Top-K | 215, 347, 973, 1337 |
| K-way Merge | 23, 378 |
| Two-Heap (median) | 295 |
| Greedy + Heap | 621, 1405, 502 |
| Lazy Deletion | 1642, 2402 |
| Heap + BFS/Dijkstra | 743, 778, 1631 |

### 🏁 Milestone
Solve LeetCode 295 (Find Median from Data Stream).

### ⚠️ Common mistakes
- Using full sort when heap gives better complexity
- Forgetting to rebalance two-heap sizes
- Not storing enough info in K-way merge tuple

### ✅ Self-check
"Can I name all 6 patterns and give one example problem for each from memory?"

---

## Level 5: Confident Practitioner — "I derive, optimize, explain under pressure"

### What you should understand
- Amortized analysis: why build-heap is O(n) (sum of heights / harmonic series)
- Heap sort: in-place O(n log n), cache-unfriendly vs quicksort
- When heaps beat other structures (vs sorted list, BST, monotonic deque)
- Advanced variants: Binomial (merge in O(log n)), Fibonacci (decrease-key O(1))
- Lazy deletion when heapq has no remove()

### 🏁 Milestone
Solve LeetCode 1675 (Minimize Deviation in Array).

### ⚠️ Common mistakes
- Reaching for Fibonacci heap in interviews (almost never right answer)
- No decrease-key in heapq — use lazy deletion
- Forgetting heap sort is unstable

### ✅ Self-check
"Can I solve a hard heap problem in 25 min, explain the pattern, and handle 2 follow-ups?"

---

## Visual Skill Map
```
Level 1 ──── Level 2 ──── Level 3 ──── Level 4 ──── Level 5
  │              │              │              │              │
Understand    sift-up/      heapq API      6 patterns    Expert +
structure     sift-down     + Top-K        + two-heap    trade-offs
```
