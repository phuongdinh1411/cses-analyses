# Step 6 — Cheat Sheet: Heap (Data Structures & Algorithms)

## Definition
A complete binary tree stored in an array where every parent ≤ (min-heap) or ≥ (max-heap) its children.
Root = always global min or max. NOT fully sorted.

---

## Key Formulas
```
parent(i)       = (i - 1) // 2
left_child(i)   = 2*i + 1
right_child(i)  = 2*i + 2
height          = floor(log₂ n)
last non-leaf   = n//2 - 1
```

---

## Time Complexities
| Operation   | Time     | Notes               |
|-------------|----------|---------------------|
| peek        | O(1)     | index 0             |
| push        | O(log n) | sift-up             |
| pop         | O(log n) | sift-down           |
| build-heap  | O(n)     | NOT O(n log n)      |
| search      | O(n)     | unsupported natively|

---

## Python heapq API
```python
import heapq
heapq.heapify(lst)                    # O(n) in-place
heapq.heappush(heap, val)             # O(log n)
heapq.heappop(heap)                   # O(log n) returns min
heap[0]                               # O(1) peek
heapq.nlargest(k, iterable)
heapq.nsmallest(k, iterable)
# Max-heap: push -val, pop and negate
# Tiebreaker: push (priority, counter, obj)
```

---

## The 6 Patterns

| Pattern          | Key Idea                            | Problems      |
|------------------|-------------------------------------|---------------|
| Top-K            | min-heap size K, evict small        | 215, 347, 973 |
| Two-Heap         | max-heap lower + min-heap upper     | 295           |
| K-way Merge      | (val, list_i, elem_j) tuples        | 23, 378       |
| Greedy + Heap    | always pick highest priority        | 621, 1046     |
| Lazy Deletion    | mark removed, skip on pop           | 1642, 2402    |
| Dijkstra         | (dist, node), skip stale entries    | 743, 1631     |

---

## Pattern Templates

```python
# TOP-K
heap = []
for num in nums:
    heapq.heappush(heap, num)
    if len(heap) > k: heapq.heappop(heap)
return heap[0]

# TWO-HEAP
lower, upper = [], []
def add(num):
    heapq.heappush(lower, -num)
    if lower and upper and -lower[0] > upper[0]:
        heapq.heappush(upper, -heapq.heappop(lower))
    if len(lower) > len(upper) + 1:
        heapq.heappush(upper, -heapq.heappop(lower))
    elif len(upper) > len(lower):
        heapq.heappush(lower, -heapq.heappop(upper))

# LAZY DELETION
removed = defaultdict(int)
def remove(val): removed[val] += 1
def get_min():
    while heap and removed[heap[0]]: removed[heap[0]] -= 1; heapq.heappop(heap)
    return heap[0]

# DIJKSTRA
heap = [(0, src)]; dist[src] = 0
while heap:
    d, u = heapq.heappop(heap)
    if d > dist[u]: continue
    for w, v in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(heap, (dist[v], v))
```

---

## Common Mistakes
| Mistake | Fix |
|---|---|
| Max-heap for Top-K largest | Use min-heap size K |
| Forgetting to negate on pop | -heapq.heappop(heap) |
| Non-comparable objects | (priority, counter, obj) |
| build-heap is O(n log n) | It's O(n) |
| Removing from heap middle | Lazy deletion |
| One invariant in two-heap | Check BOTH ordering + size |
| No stale check in Dijkstra | if d > dist[u]: continue |

---

## Checklist Before Using
- [ ] Need repeated min/max access?
- [ ] O(log n) insert/delete acceptable?
- [ ] Using heapq? (min-only — negate for max)
- [ ] Equal priorities? (add tiebreaker)
- [ ] Need remove arbitrary? (lazy deletion)
- [ ] Building from list? (heapify not repeated push)

---

## 5 Rapid-Fire Questions
1. What is at index 0 of a min-heap? → The global minimum
2. After extracting min, what goes to root? → The last element
3. Why is build-heap O(n)? → Short sift distances near leaves (sum of heights)
4. Max-heap in Python? → Push -val, pop and negate
5. Pattern for streaming median? → Two-Heap
