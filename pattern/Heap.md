---
layout: simple
title: "Heap / Priority Queue Patterns"
permalink: /pattern/heap
---

# Heap / Priority Queue Patterns — Comprehensive Guide

A heap answers one question fast: **"what's the smallest (or largest) thing right now?"** — in O(log n) to push or pop, O(1) to peek. That single capability powers top-K queries, streaming medians, merging sorted streams, and greedy scheduling. When a problem repeatedly needs the current extreme of a changing set, a heap is almost always the answer.

This guide covers Python's `heapq` idioms first (including the max-heap gotcha), then walks 8 LeetCode problems across the main heap patterns.

---

## Quick Navigation: "I need to..."

| I need to... | Pattern | Section |
|--------------|---------|---------|
| **Kth largest / smallest** element | Fixed-size heap of size k | [4](#4-problem-215--kth-largest-element) |
| **Top K frequent** items | Heap over a count map | [5](#5-problem-347--top-k-frequent-elements) |
| **Merge K sorted** lists/arrays | Heap of the K heads | [6](#6-problem-23--merge-k-sorted-lists) |
| **Median of a stream** | Two heaps (max + min) | [7](#7-problem-295--find-median-from-data-stream) |
| **Schedule / interval** by earliest end | Min-heap of end times | [8](#8-problem-253--meeting-rooms-ii) |
| Repeatedly grab the **current extreme** | Greedy + heap | [9](#9-problem-1046--last-stone-weight) |

---

## Table of Contents

1. [What a Heap Is (and Isn't)](#1-what-a-heap-is-and-isnt)
2. [Python `heapq` Essentials](#2-python-heapq-essentials)
3. [The Fixed-Size-K Trick](#3-the-fixed-size-k-trick)
4. [Problem 215 — Kth Largest Element](#4-problem-215--kth-largest-element)
5. [Problem 347 — Top K Frequent Elements](#5-problem-347--top-k-frequent-elements)
6. [Problem 23 — Merge K Sorted Lists](#6-problem-23--merge-k-sorted-lists)
7. [Problem 295 — Find Median from Data Stream](#7-problem-295--find-median-from-data-stream)
8. [Problem 253 — Meeting Rooms II](#8-problem-253--meeting-rooms-ii)
9. [Problem 1046 — Last Stone Weight](#9-problem-1046--last-stone-weight)
10. [Master Comparison Table](#10-master-comparison-table)
11. [How to Identify This Pattern](#11-how-to-identify-this-pattern)
12. [Practice Order](#12-practice-order)

---

## 1. What a Heap Is (and Isn't)

A **binary heap** is a complete binary tree stored in an array, where every parent is ≤ its children (min-heap) or ≥ them (max-heap). The array layout makes navigation index arithmetic — no pointers:

```
Array:  [1, 3, 2, 7, 5, 4]
Index:   0  1  2  3  4  5

              1(0)
            /      \
          3(1)      2(2)          parent(i) = (i-1)//2
         /   \     /              left(i)   = 2i+1
       7(3)  5(4) 4(5)            right(i)  = 2i+2
```

What a heap gives you:

| Operation | Cost | |
|-----------|------|--|
| Peek min/max | **O(1)** | root is always the extreme |
| Push | **O(log n)** | bubble up |
| Pop min/max | **O(log n)** | swap root with last, bubble down |
| Build from n items | **O(n)** | heapify, not n pushes |

What a heap is **not**:
- **Not sorted.** Only the root is guaranteed extreme. `heap[1]` vs `heap[2]` have no defined order. Never index into a heap expecting sorted order.
- **Not searchable.** Finding an arbitrary element is O(n). Heaps are for extremes, not lookups — use a hash set/BST for membership.

`★ Insight ─────────────────────────────────────`
- The "complete tree in an array" layout is why heaps are cache-friendly and pointer-free: children live at `2i+1`, `2i+2`. That arithmetic *is* the data structure.
- If you need the *full* order, sorting is O(n log n) once. Heaps win when the set **changes over time** (push/pop interleaved) or you only need the **top few** of a large stream — cases where re-sorting repeatedly would be wasteful.
`─────────────────────────────────────────────────`

---

## 2. Python `heapq` Essentials

Python's `heapq` is a **min-heap** over a plain list. There is no max-heap class — you negate values (numbers) or use a tuple key.

```python
import heapq

h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappush(h, 2)
heapq.heappop(h)      # → 1  (smallest)
h[0]                  # → 2  (peek smallest, no removal)

# Build in O(n) from an existing list:
nums = [5, 1, 4, 2, 3]
heapq.heapify(nums)   # nums is now a valid min-heap, in place

# Pop-and-push in one O(log n) step (cheaper than pop then push):
heapq.heappushpop(h, x)   # push x, then pop-and-return the smallest
heapq.heapreplace(h, x)   # pop-and-return smallest, then push x
```

### Max-heap: negate

```python
# Max-heap of numbers — store negatives, negate on the way out.
maxh = []
heapq.heappush(maxh, -value)
largest = -heapq.heappop(maxh)
```

### Heap of tuples — custom priority

`heapq` compares tuples lexicographically, so pack `(priority, ...)`:

```python
h = []
heapq.heappush(h, (dist, node))    # ordered by dist, then node
heapq.heappush(h, (-freq, item))   # max-heap by freq via negation
```

> **Tie-break gotcha.** If two tuples have equal first elements, Python compares the *next* field. If that field is an object with no ordering (e.g. a `ListNode`), you get `TypeError: '<' not supported`. Fix by inserting a unique tiebreaker: `(priority, counter, obj)` with an incrementing `counter`. You'll see this in §6.

`★ Insight ─────────────────────────────────────`
- `heappushpop` / `heapreplace` aren't just convenience — they're one bubble-down instead of a bubble-up **and** a bubble-down. In the fixed-size-K pattern (§3) that halves the constant factor of the hot loop.
- Negation is the idiomatic Python max-heap. It's clean for numbers; for objects, prefer a `(−key, tiebreaker, obj)` tuple so you never rely on the object being comparable.
`─────────────────────────────────────────────────`

---

## 3. The Fixed-Size-K Trick

The single most useful heap pattern: to keep the **K largest** elements of a stream, maintain a **min-heap of size K**. The smallest of your K best sits at the root, ready to be evicted the moment something better arrives.

```python
def k_largest(nums, k):
    h = []                       # MIN-heap, size ≤ k
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)     # drop the smallest → keep top-k
    return h                     # the k largest (unsorted)
```

Counter-intuitive but correct: **K largest → min-heap**, **K smallest → max-heap**. The heap holds your survivors; its root is the weakest survivor, the first to be kicked out.

```
nums = [4,1,7,3,8,5], k=3

push 4        h=[4]
push 1        h=[1,4]
push 7        h=[1,4,7]
push 3 pop1   h=[3,4,7]     (3 beats the weakest, 1)
push 8 pop3   h=[4,7,8]
push 5 pop4   h=[5,7,8]     → 3 largest

Cost: O(n log k), not O(n log n) — big win when k ≪ n.
```

---

## 4. Problem 215 — Kth Largest Element

**Difficulty**: Medium

> Return the kth largest element in an unsorted array.

Fixed-size-K min-heap: after processing everything, the root **is** the kth largest (it's the smallest of the top k).

```python
def find_kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]      # smallest of the k largest = kth largest
```

```
nums=[3,2,1,5,6,4], k=2

keep 2 largest → after all pushes/pops h=[5,6]
h[0] = 5  = 2nd largest ✓
```

**Complexity**: O(n log k) time, O(k) space. (Quickselect gives O(n) average but O(n²) worst; the heap is the safe, simple choice and shines when nums arrives as a stream.)

---

## 5. Problem 347 — Top K Frequent Elements

**Difficulty**: Medium

> Return the k most frequent elements.

Count with a hash map, then run the fixed-size-K heap over `(freq, value)` pairs.

```python
from collections import Counter

def top_k_frequent(nums, k):
    freq = Counter(nums)
    h = []                                  # min-heap of (count, value)
    for value, count in freq.items():
        heapq.heappush(h, (count, value))
        if len(h) > k:
            heapq.heappop(h)                # evict least frequent survivor
    return [value for count, value in h]
```

```
nums=[1,1,1,2,2,3], k=2
freq = {1:3, 2:2, 3:1}

push (3,1)               h=[(3,1)]
push (2,2)               h=[(2,2),(3,1)]
push (1,3) pop (1,3)     h=[(2,2),(3,1)]   → [1,2]
```

**Complexity**: O(n log k). (A **bucket sort** by frequency gives O(n) — worth knowing when k is large; the heap wins for clarity and small k.)

---

## 6. Problem 23 — Merge K Sorted Lists

**Difficulty**: Hard

> Merge `k` sorted linked lists into one sorted list.

Keep a min-heap of the **current head** of each list. Pop the global minimum, append it, push that node's `next`. The heap size stays ≤ k.

```python
import heapq

def merge_k_lists(lists):
    h = []
    counter = 0                       # unique tiebreaker (see §2 gotcha)
    for node in lists:
        if node:
            heapq.heappush(h, (node.val, counter, node))
            counter += 1

    dummy = tail = ListNode(0)
    while h:
        val, _, node = heapq.heappop(h)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(h, (node.next.val, counter, node.next))
            counter += 1
    return dummy.next
```

```
lists = [[1,4,5],[1,3,4],[2,6]]

heap heads: (1,·,A) (1,·,B) (2,·,C)
pop 1(A) push 4(A)   →  out: 1
pop 1(B) push 3(B)   →  out: 1 1
pop 2(C) push 6(C)   →  out: 1 1 2
pop 3(B) push 4(B)   →  ... → 1 1 2 3 4 4 5 6
```

`★ Insight ─────────────────────────────────────`
- The `counter` tiebreaker is essential: two nodes can share a `val`, and Python would then try to compare `ListNode` objects and throw `TypeError`. The counter guarantees the tuple comparison always resolves on a number.
- Merging K lists this way is O(N log k) where N = total nodes — vastly better than concatenate-then-sort O(N log N) when k is small, and it streams (never holds all N in a sortable array).
`─────────────────────────────────────────────────`

**Complexity**: O(N log k) time, O(k) heap space.

---

## 7. Problem 295 — Find Median from Data Stream

**Difficulty**: Hard

> Support `addNum(x)` and `findMedian()` on a growing stream.

The **two-heaps** pattern. Split the numbers into a lower half (max-heap) and an upper half (min-heap). The median lives at the two roots.

```
       max-heap (lower half)      min-heap (upper half)
              [ ≤ median ]              [ ≥ median ]
                    ▲                        ▲
                 largest                  smallest
                 of low                   of high
                        \              /
                          the median
```

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (store negatives): lower half
        self.hi = []   # min-heap: upper half

    def addNum(self, x):
        # 1. push to lo, then move lo's max over to hi (keeps lo ≤ hi ordering)
        heapq.heappush(self.lo, -x)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # 2. rebalance sizes: lo may hold one extra
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]                    # odd count → lo has the middle
        return (-self.lo[0] + self.hi[0]) / 2     # even → average the two roots
```

```
add 1  lo=[1]                       median 1
add 2  lo=[1] hi=[2]                 median (1+2)/2 = 1.5
add 3  lo=[2,1] hi=[3]              median 2
add 4  lo=[2,1] hi=[3,4]           median (2+3)/2 = 2.5
```

`★ Insight ─────────────────────────────────────`
- The push-then-transfer dance guarantees the invariant "every element in `lo` ≤ every element in `hi`" without sorting. You always route a new number *through* one heap into the other, so the boundary self-corrects.
- Size invariant: `len(lo) == len(hi)` or `len(lo) == len(hi)+1`. That's what makes `findMedian` O(1) — the answer is always at the roots. Two heaps beat a sorted structure because insert is O(log n), not O(n).
`─────────────────────────────────────────────────`

**Complexity**: `addNum` O(log n), `findMedian` O(1).

---

## 8. Problem 253 — Meeting Rooms II

**Difficulty**: Medium

> Given meeting intervals, find the minimum number of rooms needed.

Sort by start time. A min-heap holds the **end times** of rooms currently in use. For each new meeting, if the earliest-ending room is free by its start, reuse it; else open a new room. The heap size at any point is the rooms in use.

```python
import heapq

def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])     # by start
    ends = []                              # min-heap of end times
    for start, end in intervals:
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)   # free the earliest room, put ours in
        else:
            heapq.heappush(ends, end)      # need a new room
    return len(ends)
```

```
intervals = [[0,30],[5,10],[15,20]]  sorted same

[0,30]  ends=[30]                     1 room
[5,10]  30>5 no free room → push      ends=[10,30]   2 rooms
[15,20] 10≤15 reuse → replace 10 w/20 ends=[20,30]   2 rooms

answer = 2
```

`★ Insight ─────────────────────────────────────`
- The heap's *size* is the answer — it tracks concurrent meetings directly. The root (earliest end) is exactly the room most likely to free up next, so checking it is sufficient; you never need to scan all rooms.
- Sorting by start + min-heap of ends is the canonical "interval resource allocation" combo. Same shape solves CPU-task and IPO-style scheduling — see the pattern echo in [Contribution Counting](/pattern/contribution-counting) for other sweep-line ideas.
`─────────────────────────────────────────────────`

**Complexity**: O(n log n) — dominated by the sort.

---

## 9. Problem 1046 — Last Stone Weight

**Difficulty**: Easy

> Repeatedly smash the two heaviest stones; if unequal, the difference goes back. Return the last remaining weight (or 0).

Pure greedy-on-extremes: always need the two largest → **max-heap** (negate).

```python
import heapq

def last_stone_weight(stones):
    h = [-s for s in stones]
    heapq.heapify(h)                    # O(n) build
    while len(h) > 1:
        a = -heapq.heappop(h)           # largest
        b = -heapq.heappop(h)           # second largest
        if a != b:
            heapq.heappush(h, -(a - b)) # remainder goes back
    return -h[0] if h else 0
```

```
stones=[2,7,4,1,8,1]  max-heap tops: 8,7 → 1 back
 → [4,2,1,1,1]  tops 4,2 → 2 back
 → [2,1,1,1]    tops 2,1 → 1 back
 → [1,1,1]      tops 1,1 → 0
 → [1]          → answer 1
```

**Complexity**: O(n log n). The heap makes "grab the current two biggest" O(log n) each round instead of O(n) rescans.

---

## 10. Master Comparison Table

| Problem | Heap type | What's in it | Key move |
|---------|-----------|--------------|----------|
| **215** Kth largest | Min, size k | candidate values | pop when size > k → root is answer |
| **347** Top K frequent | Min, size k | `(count, value)` | evict least frequent survivor |
| **23** Merge K lists | Min | `(val, tie, node)` | pop min, push its `.next` |
| **295** Median stream | Max + Min (two heaps) | lower / upper halves | route through, rebalance sizes |
| **253** Meeting rooms | Min | end times | reuse earliest-ending room |
| **1046** Last stone | Max | stone weights | smash top two, push diff |
| **621** Task scheduler | Max | task counts | run most-frequent, cooldown queue |
| **373** K smallest pairs | Min | `(sum, i, j)` | pop, push neighbors |

### What stays the same

```
1. Identify the "current extreme" the problem keeps asking for
2. Choose heap polarity (min vs max) — remember the K-largest/min-heap inversion
3. Push/pop to maintain either a size bound or an ordering invariant
4. The answer is at the root (or the roots, for two-heaps)
```

### What changes

Only **what you store** (value, tuple, end-time) and **the invariant** (fixed size k, or lower-half/upper-half balance).

---

## 11. How to Identify This Pattern

### Trigger: "current extreme of a changing set"

```
See any of these?
  ├── "kth largest/smallest", "top k"        → fixed-size-k heap (§3–5)
  ├── "merge k sorted"                        → heap of k heads (§6)
  ├── "median" / "balance two halves"         → two heaps (§7)
  ├── "minimum rooms/machines/CPUs"           → min-heap of end times (§8)
  ├── "repeatedly take the largest/smallest"  → greedy + heap (§9)
  └── "schedule by priority / deadline"       → priority queue
```

### Heap vs. the alternatives

| If... | Use |
|-------|-----|
| Need the top/bottom **few** of a large or streaming set | **Heap** (O(n log k)) |
| Need the **full** sorted order, once, static | **Sort** (O(n log n)) |
| Need ordered set with **arbitrary lookup/delete** | **Balanced BST / `SortedList`** |
| Need shortest paths on a weighted graph | **Heap-backed Dijkstra** ([Graph guide](/pattern/graph)) |

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Wanting max but using default min-heap | Negate values, or use `(−key, …)` tuples |
| K largest with a max-heap | Use a **min**-heap of size k (inversion, §3) |
| `TypeError` comparing tuples | Add a unique counter tiebreaker before the object (§6) |
| Indexing `heap[1]` expecting 2nd smallest | Heap isn't sorted — only `heap[0]` is meaningful |
| `n` pushes to build | Use `heapq.heapify(list)` — O(n), not O(n log n) |

---

## 12. Practice Order

```
Start here
    │
    ▼
 1046 (Easy)   ──── Max-heap basics: grab the top two
    │
    ▼
  215 (Medium) ──── Fixed-size-k min-heap (the core trick)
    │
    ▼
  347 (Medium) ──── Heap over a count map
    │
    ▼
  253 (Medium) ──── Min-heap of end times (interval scheduling)
    │
    ▼
   23 (Hard)   ──── Merge k streams + the tiebreaker gotcha
    │
    ▼
  295 (Hard)   ──── Two heaps for a streaming median
```

---

*Pattern mastered — whenever the problem keeps asking "what's the extreme now?", a heap answers in O(log n).*
