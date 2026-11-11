# Step 3 — Learn in 20 Hours: Heap (Data Structures & Algorithms)

## The 20% That Gives 80% of Results

| Core Area | Why It Matters |
|---|---|
| 1. Heap property + array representation | Foundation |
| 2. Sift-up / Sift-down | Every heap op is built on these |
| 3. Python heapq API + max-heap trick | Your actual interview tool |
| 4. Top-K pattern | Most frequent heap interview category |
| 5. Two-Heap pattern | Streaming median, partitioning |
| 6. K-way Merge + Lazy Deletion | Unlocks hard problems |

---

## Session 1 — Mental Model & Structure (2 hrs)
**Goal:** Build correct picture of what a heap IS
- Concepts: Complete binary tree, heap property, array index formulas
- Exercise: Visualgo — insert [5,3,8,1,9,2,7] and predict each sift
- Resource: Visualgo (30 min) + CLRS §6.1–6.2 (30 min)
- Outcome: Can draw any array as heap tree, verify heap property, state index formulas

Review: (1) What makes a tree "complete"? (2) Parent of index 5? (3) Is [1,3,2,7,4,5] valid min-heap? (4) Height of n-element heap? (5) Why array vs tree nodes?

## Session 2 — Sift-Up & Sift-Down (2 hrs)
**Goal:** Implement insert and extract-min from scratch
- Concepts: Sift-up (insert), sift-down (extract-min), both O(log n)
- Exercise: Implement MinHeap with push/pop. Test: push [5,3,8,1,2], pops → [1,2,3,5,8]
- Resource: CLRS §6.2–6.3
- Outcome: Working MinHeap from memory

## Session 3 — Build-Heap + heapq Basics (2 hrs)
**Goal:** Learn O(n) build-heap, switch to Python heapq
- Concepts: heapify(), heappush/pop, max-heap via negation
- Exercise: Implement build-heap manually, then with heapify(). Write max-heap pattern.
- Resource: Python heapq docs + CLRS §6.3
- Outcome: Explain why heapify is O(n), fluent with heapq API

## Session 4 — Top-K Pattern (2 hrs)
**Goal:** Master most common heap interview pattern
- Concepts: Min-heap of size K, evict when size > K, O(n log k)
- Exercise: LeetCode 703, 215, 347
- Resource: NeetCode "Kth Largest Element"
- Pattern: push each element, pop when size > k, root = Kth largest

## Session 5 — Custom Priorities + Scheduling (2 hrs)
**Goal:** Use tuples in heaps for priority-based problems
- Concepts: (priority, value) tuples, lexicographic comparison, greedy scheduling
- Exercise: LeetCode 621 (Task Scheduler), 1046 (Last Stone Weight)
- Resource: NeetCode "Task Scheduler"

## Session 6 — Two-Heap Pattern (2 hrs)
**Goal:** Master the two-heap trick for streaming problems
- Concepts: max-heap lower half + min-heap upper half, balance sizes, median
- Exercise: LeetCode 295 (Find Median from Data Stream)
- Resource: NeetCode "Find Median from Data Stream"
- Invariants: |lower| - |upper| <= 1, lower.top <= upper.top

## Session 7 — K-way Merge Pattern (2 hrs)
**Goal:** Merge K sorted structures efficiently
- Concepts: Push (val, list_idx, elem_idx) for each list head. Pop min, push next from same list. O(n log k)
- Exercise: LeetCode 23 (Merge K Sorted Lists), 378 (Kth Smallest in Matrix)
- Resource: NeetCode "Merge K Sorted Lists"

## Session 8 — Lazy Deletion Pattern (2 hrs)
**Goal:** Remove arbitrary elements from heap
- Concepts: Mark as deleted, skip on pop, use counter/set for tracking
- Exercise: LeetCode 1642, design add/remove/getMin structure
- Key: heapq has no remove() — lazy deletion is the workaround

## Session 9 — Heap + Dijkstra (2 hrs)
**Goal:** Apply heap to shortest path problems
- Concepts: Push (distance, node), always process closest unvisited. O((V+E) log V)
- Exercise: LeetCode 743 (Network Delay Time), 1631 (Path With Minimum Effort)
- Note: `if d > dist[u]: continue` is lazy deletion applied to Dijkstra

## Session 10 — Review + Capstone (2 hrs)
**Goal:** Pattern recognition under pressure
- Exercise: LeetCode 1675 (Minimize Deviation) + re-solve 2 weakest problems
- Pattern drill: match 6 problems to their patterns from memory

---

## Capstone Project: Live Leaderboard
```
add_score(player_id, score)  → O(log n)
get_top_k(k)                 → O(k log n)
remove_player(player_id)     → O(log n) amortized
get_median_score()           → O(log n)
```
Exercises: Top-K + Lazy Deletion + Two-Heap in one project.

---

## Time Summary
| Sessions | Focus | Hours |
|---|---|---|
| 1–3 | Foundation | 6 hrs |
| 4–5 | Top-K + Scheduling | 4 hrs |
| 6–7 | Two-Heap + K-way Merge | 4 hrs |
| 8–9 | Lazy Deletion + Dijkstra | 4 hrs |
| 10 | Review + Capstone | 2 hrs |
| **Total** | | **20 hrs** |
