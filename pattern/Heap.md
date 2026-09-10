---
layout: simple
title: "Heap / Priority Queue Patterns"
permalink: /pattern/heap
---

# Heap / Priority Queue Patterns — Comprehensive Guide

A heap answers one question fast: **"what's the smallest (or largest) thing right now?"** — in O(log n) to push or pop, O(1) to peek. That single capability powers top-K queries, streaming medians, merging sorted streams, and greedy scheduling. When a problem repeatedly needs the current extreme of a changing set, a heap is almost always the answer.

This guide covers Python's `heapq` idioms first (including the max-heap gotcha), then walks 12 LeetCode problems across the main heap patterns.

---

## From-Scratch Idea: What Makes a Problem a Heap Problem

Suppose you need the smallest element of a collection, repeatedly, while the collection keeps
changing. Weigh the obvious options:

| Approach | Find the min | Insert | Why it fails |
|----------|-------------|--------|--------------|
| Unsorted list | O(n) scan | O(1) | Every query rescans everything |
| Sorted list | O(1) | **O(n)** shift | Insertion destroys the win |
| Re-sort each time | O(1) | O(n log n) | Absurd, but it is the instinct to resist |

Each row is fast at one operation and slow at the other, because each maintains **total order** —
far more than the question needs. You never asked for the ordering of elements 5 and 6. You asked
for the minimum.

A heap is what you get by keeping *just enough* order to answer that: **every parent is ≤ its
children**, and nothing else is promised. That single invariant is weak enough to repair in
O(log n) after a change (walk one root-to-leaf path) and strong enough to put the answer at the
root, readable in O(1).

> **The trade in one line: give up total order, keep the extreme.** A heap is the minimum
> structure that survives insertions while still answering "what is smallest right now?"

### The two questions that identify it

1. **Am I asking for an extreme repeatedly, interleaved with changes to the set?** Once, on fixed
   data → sort or quickselect. Repeatedly, with insertions in between → heap.
2. **Do I need only the extreme, or arbitrary access?** Membership tests, deletion of a specific
   element, or predecessor queries → you want a balanced BST / ordered set, not a heap. A heap
   cannot find an arbitrary element faster than O(n).

### The disguises

Heap problems rarely say "heap". They say:

- "**k-th largest / smallest**" → fixed-size heap of size `k` (§3, §4, §13)
- "**top k** frequent / closest / most valuable" → heap over a derived key (§5)
- "merge **k sorted** streams" → heap of `k` cursors (§6, §15)
- "**median** of a stream" → two heaps facing each other (§7, §14)
- "minimum number of **rooms / machines / platforms**" → min-heap of end times (§8)
- "repeatedly take the two largest and ..." → greedy on a max-heap (§9)
- "**shortest path** with weights" → heap is the engine, not the answer
  ([Graph Patterns §2](/pattern/graph))

Every one of those is the same sentence: *the next thing I need is the current extreme of a set
that keeps changing.*

---

## Master LeetCode Comparison Table

| LC # | Title | Diff | Heap shape | The invariant | Cost |
|------|-------|------|-----------|---------------|------|
| **215** | Kth Largest Element in an Array | Medium | Min-heap, size `k` | root = k-th largest | O(n log k) |
| **703** | Kth Largest Element in a Stream | Easy | Min-heap, size `k` | same, maintained online | O(log k)/add |
| **347** | Top K Frequent Elements | Medium | Min-heap of `(count, item)`, size `k` | root = least frequent of the top k | O(n log k) |
| **23** | Merge k Sorted Lists | Hard | Min-heap of `k` list heads | root = global next smallest | O(N log k) |
| **373** | K Smallest Pairs | Medium | Min-heap of frontier pairs | root = next smallest sum | O(k log k) |
| **632** | Smallest Range Covering K Lists | Hard | Min-heap of `k` cursors + running max | range = `[heap_min, cur_max]` | O(N log k) |
| **295** | Find Median from Data Stream | Hard | Two heaps | `max(lo) ≤ min(hi)`, sizes differ by ≤ 1 | O(log n)/add |
| **480** | Sliding Window Median | Hard | Two heaps + lazy deletion | same, with expiry | O(n log n) |
| **253** | Meeting Rooms II | Medium | Min-heap of end times | heap size = rooms in use | O(n log n) |
| **621** | Task Scheduler | Medium | Max-heap of counts + cooldown queue | root = most remaining work | O(n log Σ) |
| **1046** | Last Stone Weight | Easy | Max-heap (negated) | root = heaviest stone | O(n log n) |
| **264** | Ugly Number II | Medium | Min-heap + seen set | root = next ugly number | O(n log n) |

Read the **Heap shape** column top to bottom: one bounded heap → a heap of cursors → two heaps
facing each other → a heap plus a second structure. That progression is the learning ladder.

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
| Know **why `heapify` is O(n)** | The height-sum argument | [10](#10-why-heapify-is-on) |
| Sort by a **custom key**, or fix a `TypeError` on ties | Tuple trick / counter / `__lt__` | [11](#11-custom-comparators-in-python) |
| **Delete or update** an arbitrary element | Lazy deletion | [12](#12-lazy-deletion-the-indexed-heap-substitute) |
| K-th largest in a **stream** | Fixed-size heap, online | [13](#13-problem-703--kth-largest-element-in-a-stream) |
| Median of a **sliding window** | Two heaps + lazy deletion | [14](#14-problem-480--sliding-window-median) |
| Smallest range covering **k lists** | Heap of cursors + running max | [15](#15-problem-632--smallest-range-covering-elements-from-k-lists) |
| Decide **heap vs sort vs quickselect vs BST** | The decision table | [16](#16-heap-vs-sort-vs-quickselect-vs-balanced-bst) |

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
10. [Why `heapify` Is O(n)](#10-why-heapify-is-on)
11. [Custom Comparators in Python](#11-custom-comparators-in-python)
12. [Lazy Deletion: the Indexed-Heap Substitute](#12-lazy-deletion-the-indexed-heap-substitute)
13. [Problem 703 — Kth Largest Element in a Stream](#13-problem-703--kth-largest-element-in-a-stream)
14. [Problem 480 — Sliding Window Median](#14-problem-480--sliding-window-median)
15. [Problem 632 — Smallest Range Covering Elements from K Lists](#15-problem-632--smallest-range-covering-elements-from-k-lists)
16. [Heap vs Sort vs Quickselect vs Balanced BST](#16-heap-vs-sort-vs-quickselect-vs-balanced-bst)
17. [Master Comparison Table](#17-master-comparison-table)
18. [How to Identify This Pattern](#18-how-to-identify-this-pattern)
19. [Practice Order](#19-practice-order)
20. [Pattern Recognition Cheat Sheet](#20-pattern-recognition-cheat-sheet)

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

### Sift-up (push) and sift-down (pop), swap by swap

Push and pop both restore the heap property by walking **one element** along a single root-to-leaf path — that's the O(log n).

Start with this valid min-heap and `heappush(0)`. The new value is appended at the end (index 5), then **sifts up** while it's smaller than its parent (`parent(i) = (i-1)//2`):

```
[1, 3, 2, 7, 4]            1
 append 0 at idx 5:      /   \
                       3      2
                      / \    /
                     7   4  0(5)     0 < parent 2 → swap

[1, 3, 0, 7, 4, 2]         1
 0 now at idx 2:         /   \
                       3      0(2)   0 < parent 1 → swap
                      / \    /
                     7   4  2

[0, 3, 1, 7, 4, 2]         0          0 is root → stop
                         /   \
                       3      1
                      / \    /
                     7   4  2
```

Now `heappop()`: return the root `0`, move the **last** element (`2`) into the root slot, then **sift down**, swapping with the *smaller* child while it's larger (`left(i)=2i+1`, `right(i)=2i+2`):

```
pop 0, move 2 to root:
[2, 3, 1, 7, 4]            2          children 3, 1 → smaller is 1
                         /   \        2 > 1 → swap
                       3      1
                      / \
                     7   4

[1, 3, 2, 7, 4]            1          2 now at idx 2, no children → stop
                         /   \
                       3      2
                      / \
                     7   4
```

We're back to the original array — one path down, O(log n).

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
- Sorting by start + min-heap of ends is the canonical "interval resource allocation" combo. The same shape solves CPU-task scheduling (LC 621) and IPO-style profit selection (LC 502).
`─────────────────────────────────────────────────`

**Complexity**: O(n log n) — the sort and the heap loop are both O(n log n), so neither dominates
asymptotically; the sort just has the larger constant.

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

## 10. Why `heapify` Is O(n)

Section 1 claims building a heap from `n` items costs O(n), not O(n log n). That looks wrong —
there are `n` items and sifting one down is O(log n) — so here is why it holds. You will be asked
this in interviews, and the argument generalises.

`heapify` sifts down every internal node, from the last one up to the root. The cost of sifting a
node down is bounded by its **height** (distance to the deepest leaf below it), not by the tree's
total height. And the tree is overwhelmingly bottom-heavy:

```
height h   how many nodes at that height   work each   total work
--------   ----------------------------   ---------   ----------
   0        n/2   (the leaves)                 0            0
   1        n/4                                1          n/4
   2        n/8                                2         2n/8
   3        n/16                               3         3n/16
   ...
   h        n/2^(h+1)                          h       h·n/2^(h+1)
```

Sum the last column:

```
total = n · Σ(h=1..log n)  h / 2^(h+1)  <  n · Σ(h=1..∞) h / 2^(h+1)  =  n · 1  =  O(n)
```

The series `Σ h/2^(h+1)` converges to 1 — that is the whole trick. Half the nodes are leaves and
cost nothing; only the single root pays the full `log n`.

`★ Insight ─────────────────────────────────────`
- **Sifting down beats sifting up, and the asymmetry is structural.** Building by `n` successive pushes sifts *up*, where cost is depth — and most nodes are deep, so that genuinely is O(n log n). `heapify` sifts *down*, where cost is height — and most nodes are short. Same tree, opposite distribution, different complexity class.
- Practical consequence: `heapq.heapify(lst)` on an existing list is strictly better than looping `heappush`. If you have all the data up front, never build by pushing.
`─────────────────────────────────────────────────`

---

## 11. Custom Comparators in Python

`heapq` has no `key=` parameter. It compares whatever you push using `<`. There are three ways to
control the ordering, and picking the wrong one causes a specific, confusing crash.

### The tuple trick (use this by default)

Push `(sort_key, payload)`. Tuples compare element by element.

```python
import heapq

tasks = [(3, "write"), (1, "read"), (2, "review")]
heapq.heapify(tasks)
heapq.heappop(tasks)            # (1, 'read')
```

### The tie-break problem

If two keys are equal, Python moves on to compare the *second* element. When that second element
is not comparable — a dict, a custom object, a `ListNode` — you get:

```
TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'
```

This is the single most common heap error in Python, and it is **data-dependent**: your code
passes every test until two items happen to tie. Fix it with a monotonically increasing counter
as a guaranteed-unique middle element:

```python
import heapq
from itertools import count

tiebreak = count()              # 0, 1, 2, ... never repeats

heap = []
heapq.heappush(heap, (priority, next(tiebreak), some_object))
```

The counter also gives you **FIFO order among equal priorities** for free, which is often what you
actually wanted.

### Wrapper class (when the object owns its ordering)

If the ordering is intrinsic to the type, define `__lt__` once instead of decorating every push:

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Job:
    priority: int
    name: str = field(compare=False)   # excluded from comparison entirely

heap = [Job(3, "write"), Job(1, "read")]
heapq.heapify(heap)
heapq.heappop(heap)             # Job(priority=1, name='read')
```

### Max-heaps

`heapq` is min-only. Negate for numbers; for tuples negate just the key:

```python
heapq.heappush(heap, -value)                    # numbers
heapq.heappush(heap, (-count, word))            # max by count, min by word
```

Watch out: negating a tuple's key **reverses that field only**. In `(-count, word)`, ties on
`count` break by *ascending* `word` — which is usually what LC 692-style problems want, but it is
easy to get backwards without noticing.

---

## 12. Lazy Deletion: the Indexed-Heap Substitute

A binary heap cannot delete or update an arbitrary element — finding it is O(n). Yet Dijkstra
conceptually wants "decrease this node's key", and streaming problems want "remove the item that
just expired". The standard answer is not a fancier heap. It is **lazy deletion**: never remove
anything, just push the new version and ignore stale entries when they surface.

### Pattern A — stale-entry skip (Dijkstra's version)

Push a fresh `(dist, node)` on every improvement. When popping, discard any entry whose distance
no longer matches the best known:

```python
import heapq

def dijkstra(src, adj, n):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:          # stale: a better path was found after this was pushed
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
```

The heap can hold up to `E` entries instead of `V`, but `log E = O(log V)` for simple graphs, so
the complexity stays **O((V + E) log V)**. You trade a little memory for not implementing a
decrease-key. Full context in [Graph Patterns §2](/pattern/graph).

### Pattern B — deletion counter (arbitrary removals)

When you must remove specific values that are not "improvements", keep a tally of pending
deletions and purge from the top before every read:

```python
import heapq
from collections import defaultdict

class LazyHeap:
    def __init__(self):
        self.heap = []
        self.pending = defaultdict(int)   # value -> how many copies to discard
        self.size = 0                     # logical size, excluding pending

    def push(self, x):
        heapq.heappush(self.heap, x)
        self.size += 1

    def remove(self, x):                  # O(1); the real work is deferred
        self.pending[x] += 1
        self.size -= 1

    def _purge(self):
        while self.heap and self.pending[self.heap[0]] > 0:
            self.pending[self.heap[0]] -= 1
            heapq.heappop(self.heap)

    def top(self):
        self._purge()
        return self.heap[0] if self.heap else None

    def pop(self):
        self._purge()
        self.size -= 1
        return heapq.heappop(self.heap)
```

Every element is pushed once and popped at most once, so all operations are **amortized
O(log n)** even though a single `_purge` can pop many entries.

`★ Insight ─────────────────────────────────────`
- **Keep `size` separately.** `len(self.heap)` counts ghosts. Any logic that branches on the structure's size — "is the left heap bigger by more than one?" in a two-heap median — must use the logical count, or it will rebalance against phantom elements.
- **Purge before reading, not after writing.** Deferring all cleanup to the read path is what keeps `remove` at O(1) and keeps the amortized bound honest. Purging eagerly on every removal reintroduces the O(n) search you were avoiding.
- This is the machinery behind §14 (sliding-window median) and behind every "priority queue with cancellable tasks" design question.
`─────────────────────────────────────────────────`

---

## 13. Problem 703 — Kth Largest Element in a Stream

> Design a class initialised with `k` and a stream. Each `add(val)` returns the k-th largest
> element **among everything seen so far**.

The pure application of the fixed-size-k trick from §3: keep a **min**-heap holding exactly the
`k` largest values seen. Its root is, by construction, the k-th largest.

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = list(nums)
        heapq.heapify(self.heap)              # O(n), not n pushes — see §10
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)          # evict the smallest; k largest remain
        return self.heap[0]
```

```
k = 3, nums = [4,5,8,2]
  heapify -> pop down to size 3  ->  heap holds {4,5,8}, root = 4

add(3):  push 3 -> {3,4,5,8}, size 4 > 3 -> pop 3  -> {4,5,8}   return 4
add(5):  push 5 -> {4,5,5,8}, pop 4              -> {5,5,8}   return 5
add(10): push 10 -> {5,5,8,10}, pop 5            -> {5,8,10}  return 5
add(9):  push 9 -> {5,8,9,10}, pop 5             -> {8,9,10}  return 8
add(4):  push 4 -> {4,8,9,10}, pop 4             -> {8,9,10}  return 8
```

**Complexity**: O(n) to construct, **O(log k)** per `add`, O(k) space.

`★ Insight ─────────────────────────────────────`
- **The heap's polarity is the opposite of the word in the problem.** "K-th *largest*" wants a **min**-heap, because you need cheap access to the *smallest of the k largest* — that is the one to evict. Getting this backwards is the most common heap mistake, and the code still runs; it just returns nonsense.
- **O(log k), not O(log n), is the point.** Bounding the heap at `k` means the cost per element never grows with the length of the stream. For an unbounded stream that is the difference between viable and not.
`─────────────────────────────────────────────────`

---

## 14. Problem 480 — Sliding Window Median

> Given an array and a window size `k`, return the median of every window.

This is §7's two-heap median plus the one thing §7 never had to handle: **elements leaving**. And
a binary heap cannot remove an arbitrary element — which is exactly what §12's lazy deletion is
for. This problem is where the two techniques meet.

Structure: `lo` is a max-heap (negated) holding the smaller half, `hi` is a min-heap holding the
larger half. Invariants: every element of `lo` ≤ every element of `hi`, and
`len(lo) == len(hi)` or `len(lo) == len(hi) + 1`.

The key accounting device is `balance`, a **relative** count: `+1` means `lo` gained one logical
element relative to `hi`. Adding one element and removing one gives `balance ∈ {−2, 0, +2}`, so at
most **one** transfer is ever needed to restore the invariant.

```python
import heapq
from collections import defaultdict

def median_sliding_window(nums, k):
    lo, hi = [], []                       # lo: max-heap (negated), hi: min-heap
    pending = defaultdict(int)            # value -> copies logically removed

    for x in nums[:k]:                    # seed: everything into lo, then split
        heapq.heappush(lo, -x)
    for _ in range(k // 2):
        heapq.heappush(hi, -heapq.heappop(lo))

    def median():
        return float(-lo[0]) if k % 2 else (-lo[0] + hi[0]) / 2.0

    result = [median()]

    for i in range(k, len(nums)):
        incoming, outgoing = nums[i], nums[i - k]
        balance = 0

        if incoming <= -lo[0]:
            heapq.heappush(lo, -incoming); balance += 1
        else:
            heapq.heappush(hi, incoming);  balance -= 1

        balance += -1 if outgoing <= -lo[0] else 1   # which side the leaver was on
        pending[outgoing] += 1

        if balance > 0:                   # balance is -2, 0, or +2
            heapq.heappush(hi, -heapq.heappop(lo))
        elif balance < 0:
            heapq.heappush(lo, -heapq.heappop(hi))

        while lo and pending[-lo[0]] > 0:            # purge stale roots
            pending[-lo[0]] -= 1
            heapq.heappop(lo)
        while hi and pending[hi[0]] > 0:
            pending[hi[0]] -= 1
            heapq.heappop(hi)

        result.append(median())

    return result
```

```
nums = [1,3,-1,-3,5,3,6,7], k = 3   (k odd -> median = -lo[0])

seed on [1,3,-1]:  lo = {1,3,-1} -> move k//2 = 1 up -> lo = {1,-1}, hi = {3}
                   median = 1                                    emit 1

i=3  in=-3 out=1
     -3 <= 1  -> lo, balance +1
     out 1 <= 1 -> was in lo, balance -1     balance = 0, no transfer
     purge: lo root is 1, pending[1]=1 -> pop.  lo = {-1,-3}, hi = {3}
     median = -1                                                 emit -1
i=4  in=5  out=3
     5 > -1   -> hi, balance -1
     out 3 > -1 -> was in hi, balance +1     balance = 0
     purge: hi root 3 is pending -> pop.  lo = {-1,-3}, hi = {5}
     median = -1                                                 emit -1
i=5  in=3  out=-1
     3 > -1 -> hi, balance -1
     out -1 <= -1 -> was in lo, balance -1   balance = -2 -> move hi.min(3) to lo
     purge: lo root -1 is pending -> pop.  lo = {-3,3}... root = 3
     median = 3                                                  emit 3
i=6  in=6  out=-3   ->  ... same mechanics ...                   emit 5
i=7  in=7  out=5    ->  ...                                      emit 6

answer = [1, -1, -1, 3, 5, 6]  ✓
```

**Complexity**: O(n log n) time, O(k) live elements plus the deferred ghosts.

`★ Insight ─────────────────────────────────────`
- **Track a relative `balance`, not two absolute sizes.** Absolute counts have to agree with `len(lo)` and `len(hi)`, which include ghosts — so they drift. A relative delta only records what *this step* changed, and since one insert plus one delete can shift it by at most 2, a single transfer always restores the invariant. This is the difference between a version that works and one that fails only on inputs where a deletion happens to land at a root.
- **Purge at the roots only, and only after rebalancing.** A stale value buried in the middle of a heap is harmless: it is not the median, and by the time it reaches a root the purge loop removes it. You never need to find it.
- **Deciding which heap the evicted value lived in** is a comparison against `lo`'s top, not a search. O(1) versus O(k) — searching would defeat the entire design.
- If your language has an order-statistic tree or a `SortedList` (Python's `sortedcontainers`), this problem is ten lines. The two-heap version is what you write when all you have is a binary heap, which is the point of the exercise.
`─────────────────────────────────────────────────`

---

## 15. Problem 632 — Smallest Range Covering Elements from K Lists

> Given `k` sorted lists, find the smallest range `[a, b]` that contains at least one number from
> each list.

The reframe: a range covers all lists exactly when you have picked one element per list and the
range spans them. So maintain **one pointer per list** — a heap of the `k` current elements — and
track the running maximum separately. The current candidate range is always
`[heap_min, running_max]`.

To shrink it, you must raise the minimum, and the only way to do that is to advance the list that
owns the minimum. That is a pop-and-push. When any list runs out, no smaller range is reachable.

```python
import heapq

def smallest_range(nums):
    heap = [(row[0], i, 0) for i, row in enumerate(nums)]   # (value, list index, position)
    heapq.heapify(heap)
    cur_max = max(row[0] for row in nums)

    best = (heap[0][0], cur_max)

    while True:
        val, i, j = heapq.heappop(heap)
        if cur_max - val < best[1] - best[0]:
            best = (val, cur_max)

        if j + 1 == len(nums[i]):        # this list is exhausted -> cannot cover any more
            return list(best)

        nxt = nums[i][j + 1]
        cur_max = max(cur_max, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))
```

```
nums = [[4,10,15,24,26], [0,9,12,20], [5,18,22,30]]

heap = {(0,l1), (4,l0), (5,l2)}   cur_max = 5   range [0,5]  width 5   best=[0,5]
pop 0  -> advance l1 to 9    cur_max = 9   heap {(4,l0),(5,l2),(9,l1)}
pop 4  -> range [4,9] width 5, not better; advance l0 to 10, cur_max=10
pop 5  -> range [5,10] width 5, not better; advance l2 to 18, cur_max=18
pop 9  -> range [9,18] width 9; advance l1 to 12
pop 10 -> range [10,18] width 8; advance l0 to 15
pop 12 -> range [12,18] width 6; advance l1 to 20, cur_max=20
pop 15 -> range [15,20] width 5, ties best; advance l0 to 24, cur_max=24
pop 18 -> range [18,24] width 6; advance l2 to 22
pop 20 -> range [20,24] width 4  -> BEST = [20,24]; advance l1 -> exhausted
return [20,24]  ✓
```

**Complexity**: O(N log k) where `N` is the total number of elements, O(k) space.

`★ Insight ─────────────────────────────────────`
- **The maximum does not need a heap.** It only ever increases — each newly pushed element is at least as large as the one it replaced in a sorted list — so a running scalar tracks it in O(1). Recognising that one side of a two-sided problem is monotone saves you a whole data structure.
- **Termination is the subtle part.** You stop when the *first* list is exhausted, not when the heap empties. Once a list has nothing left, every future range would exclude it, so no valid range remains.
- Same skeleton as merge-k-sorted-lists (§6): a heap of `k` cursors advancing through sorted runs. Once you see that shape, LC 373 (k smallest pairs) and LC 786 (k-th smallest prime fraction) are the same problem wearing different clothes.
`─────────────────────────────────────────────────`

---

## 16. Heap vs Sort vs Quickselect vs Balanced BST

Choosing wrong here is rarely a wrong answer — it is usually a needless log factor, or a TLE on
the largest test case. The deciding question is **how many times you ask, and whether the set
changes between asks.**

| Situation | Use | Cost | Why not the others |
|-----------|-----|------|--------------------|
| One-shot k-th largest, array fits in memory, order not needed after | **Quickselect** | O(n) average | Sorting does O(n log n) to produce order you throw away |
| One-shot "give me the top k, sorted" | **Sort** | O(n log n) | Simple, cache-friendly; a heap wins only when `k << n` |
| Top k where `k << n`, or a **stream** with no known length | **Fixed-size heap** | O(n log k) | Sorting needs all the data at once; a stream has no "all" |
| Repeated extract-min while **inserting** new items (Dijkstra, scheduling, merge-k) | **Heap** | O(log n) per op | Sorting once is invalid — the set keeps changing |
| Need the k-th element *and* arbitrary deletions / predecessor queries | **Balanced BST / order-statistic tree** | O(log n) per op | A heap cannot find or delete an arbitrary element |
| Need the extreme of a **sliding window** | **Monotonic deque** | O(n) total | A heap gives O(n log k) and needs lazy deletion; the deque is strictly better ([Stack & Queue §5](/pattern/stack-queue)) |

The trap worth naming: **a heap is not a sorted container.** If you find yourself popping the
entire heap to get sorted output, you wrote an O(n log n) sort with a worse constant. Just sort.

---

## 17. Master Comparison Table

| Problem | Heap type | What's in it | Key move |
|---------|-----------|--------------|----------|
| **215** Kth largest | Min, size k | candidate values | pop when size > k → root is answer |
| **347** Top K frequent | Min, size k | `(count, value)` | evict least frequent survivor |
| **23** Merge K lists | Min | `(val, tie, node)` | pop min, push its `.next` |
| **295** Median stream | Max + Min (two heaps) | lower / upper halves | route through, rebalance sizes |
| **253** Meeting rooms | Min | end times | reuse earliest-ending room |
| **1046** Last stone | Max | stone weights | smash top two, push diff |

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

## 18. How to Identify This Pattern

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

## 19. Practice Order

```
Start here
    │
    ▼
 1046 (Easy)   ──── heappush/heappop warm-up: build a max-heap, grab the top two
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
  703 (Easy*)  ──── The same fixed-size trick, but online
    │
    ▼
  347 (Medium) ──── Heap over a count map
    │
    ▼
  253 (Medium) ──── Min-heap of end times (interval scheduling)
    │
    ▼
   23 (Hard)   ──── Merge k streams + the tiebreaker gotcha (§11)
    │
    ▼
  632 (Hard)   ──── Heap of cursors + a running max
    │
    ▼
  295 (Hard)   ──── Two heaps for a streaming median
    │
    ▼
  480 (Hard)   ──── The capstone: two heaps + lazy deletion (§12)
```

---

## 20. Pattern Recognition Cheat Sheet

### Signal → heap shape

| You see in the problem statement | Reach for | Polarity |
|----------------------------------|-----------|----------|
| "k-th largest" | Min-heap capped at `k` | **Min** (evict the smallest of the k largest) |
| "k-th smallest" | Max-heap capped at `k` | **Max** (evict the largest of the k smallest) |
| "top k frequent / closest / best" | Heap of `(key, item)` capped at `k` | Min on the key you want to keep large |
| "merge k sorted ..." | Heap of `k` cursors | Min |
| "median of a stream / window" | Two heaps facing each other | Max on the low half, min on the high half |
| "minimum rooms / machines / platforms" | Min-heap of end times | Min |
| "repeatedly combine the two largest" | Max-heap (negate) | Max |
| "shortest path, non-negative weights" | Heap inside Dijkstra | Min — see [Graph §2](/pattern/graph) |
| "maximum of every window of size k" | **Not a heap** → monotonic deque | — [Stack & Queue §5](/pattern/stack-queue) |
| "k-th smallest, one query, order not needed after" | **Not a heap** → quickselect | — O(n) average |

### Bug checklist

1. **Is the polarity inverted?** "K-th largest" needs a *min*-heap. Wrong polarity still runs and
   returns a plausible-looking wrong number.
2. **Can two pushed tuples tie on their first element?** If the next element is not comparable,
   you get a `TypeError` on *some* inputs only. Add a counter tiebreaker (§11).
3. **Did you negate consistently?** Negate on push *and* on read. A single missed negation flips
   one comparison and silently corrupts the ordering.
4. **Are you using `len(heap)` where you meant the logical size?** With lazy deletion those differ
   (§12, §14).
5. **Did you build with `heapify` or with a push loop?** `heapify` is O(n) and the loop is
   O(n log n) (§10).
6. **Are you popping the whole heap to produce sorted output?** Then you wrote a slow sort. Sort.

---

## The Heap Toolbox at a Glance

```
              "What is the extreme of this changing set, right now?"
                                    │
        ┌───────────────┬───────────┴────────┬────────────────────┐
        │               │                    │                    │
   ONE BOUNDED      HEAP OF K            TWO HEAPS          HEAP + FRIEND
   HEAP (size k)    CURSORS              FACING              structure
        │               │                    │                    │
   root = the      root = global        max(lo) <= min(hi)   heap + count map,
   k-th extreme    next smallest        sizes within 1       + seen set,
        │               │                    │               + lazy deletion
   215 kth largest  23  merge k        295 stream median    621 task scheduler
   703 kth stream   373 k pairs        480 window median    264 ugly numbers
   347 top k freq   632 smallest range                      Dijkstra (§12)
   1046 stones                                              253 meeting rooms
```

**The one question that picks the branch**: is there *one* extreme to track (bounded heap), *k*
parallel streams to advance (cursors), a *split point* to maintain (two heaps), or does the heap
need help remembering what is still valid (heap + friend)?

---

## When This Fails

A heap gives you the extreme of a changing set. It is the wrong structure when:

- **You need arbitrary access.** Finding, deleting, or updating a specific element is O(n). Use a
  balanced BST or an order-statistic tree.
- **The extreme is over a sliding window.** A heap needs lazy deletion and gives O(n log k); a
  monotonic deque gives O(n) ([Stack & Queue §5](/pattern/stack-queue)).
- **You need one k-th element from static data.** Quickselect is O(n) average and does not build
  anything. Reach for a heap only when the set changes or the data streams.
- **You are producing fully sorted output.** Popping the whole heap is an O(n log n) sort with a
  worse constant than the built-in. Just sort.
- **Weights can be negative** (in a shortest-path context). Dijkstra's greedy finalisation is
  invalid; that is Bellman-Ford's job, not the heap's fault.

## Self-Test

Answer these from memory, out loud or on paper, *before* looking. Recognition is not
recall: rereading an explanation feels like knowing, and it is not. A question you cannot answer
cold names the exact section to revisit — you do not need to reread the guide.


**1. What is the heap invariant, and what does it deliberately *not* promise?**

<details markdown="1">
<summary>Answer</summary>

Every parent is ≤ its children (min-heap). It promises nothing about siblings or about any relationship other than parent-child. That weakness is the point: it is cheap enough to restore in O(log n) after a change, while still keeping the answer at the root.

</details>

**2. You need the k-th *largest* element. Which heap, and why that one?**

<details markdown="1">
<summary>Answer</summary>

A **min**-heap of size `k`. It holds the `k` largest values seen, and its root is the smallest of those — which is exactly the k-th largest, and also exactly the element to evict when a bigger one arrives. Reaching for a max-heap here is the most common heap error, and the code still runs.

</details>

**3. Why is `heapify` O(n) when pushing `n` items is O(n log n)?**

<details markdown="1">
<summary>Answer</summary>

`heapify` sifts **down**, where a node's cost is its *height*, and most nodes are near the leaves (half have height 0 and cost nothing). Summing `Σ h·n/2^(h+1)` converges to `n`. Pushing sifts **up**, where cost is *depth*, and most nodes are deep — which genuinely is O(n log n). Same tree, opposite distribution.

</details>

**4. Your heap of tuples raises `TypeError: '<' not supported`. What happened?**

<details markdown="1">
<summary>Answer</summary>

Two entries tied on the first element, so Python moved on to compare the second — and that one is not orderable (a dict, a node, a custom object). It is data-dependent, so it passes tests until a tie occurs. Fix: insert a unique increasing counter as the middle element, which also gives FIFO order among equal priorities.

</details>

**5. A binary heap cannot decrease-key. How does Dijkstra manage?**

<details markdown="1">
<summary>Answer</summary>

Lazy deletion: push a fresh `(dist, node)` on every improvement and skip stale pops with `if d > dist[u]: continue`. The heap may hold up to `E` entries instead of `V`, but `log E = O(log V)`, so the complexity is unchanged.

</details>

**6. Two-heap median: state the invariants.**

<details markdown="1">
<summary>Answer</summary>

`lo` is a max-heap holding the smaller half, `hi` a min-heap holding the larger half; every element of `lo` is ≤ every element of `hi`; and their sizes differ by at most one. The median is then `lo`'s root (odd total) or the mean of the two roots (even).

</details>

**7. With lazy deletion, why can you not use `len(heap)` for balance decisions?**

<details markdown="1">
<summary>Answer</summary>

It counts entries you have already logically removed. Track a separate logical size, or better a *relative* balance delta — absolute counts have to stay in sync with the physical heaps and inevitably drift.

</details>

**8. When is a heap the wrong answer for "the k smallest"?**

<details markdown="1">
<summary>Answer</summary>

When the data is static, in memory, and you only ask once: quickselect is O(n) average. And if you need the k smallest *in sorted order* and `k` is close to `n`, just sort. The heap wins for streams, for repeated queries interleaved with insertions, and when `k << n`.

</details>

---

## See Also

- [Graph Patterns §2](/pattern/graph) — Dijkstra and Prim are heaps with a graph wrapped around them; the lazy-deletion pattern in §13 is exactly what they need.
- [Sliding Window](/pattern/sliding-window) — for window *maximum*, a monotonic deque beats a heap at O(n) vs O(n log n). Reach for the heap only when you need a window *median* or *k-th* (§14).
- [Binary Search](/pattern/binary-search) — quickselect and binary-search-on-value are the O(n)-average alternatives to a heap for a one-shot k-th element.
- [Stack & Queue §5](/pattern/stack-queue) — the monotonic deque, the heap's main rival for windowed extremes.
- [Segment Tree](/pattern/segment-tree) — when you need arbitrary deletion or a k-th query by value, which a binary heap cannot do.
- [Pattern Decision Map](/pattern/decision-map) — the router: which technique does a cold problem call for?
- [Pattern Mastery Program](/pattern/mastery) — the spaced-repetition schedule, mastery checklist, and drill formats that turn reading into recall.

---

*Pattern mastered — whenever the problem keeps asking "what's the extreme now?", a heap answers in O(log n).*
