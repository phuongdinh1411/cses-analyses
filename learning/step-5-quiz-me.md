# Step 5 — Quiz Me: Heap (Data Structures & Algorithms)

## Q1 (Beginner) — Is [2,4,3,9,7,8,5] a valid min-heap?
**Answer:** Yes. Every parent ≤ its children. Check all pairs by index formulas.
**Gap:** Heaps are NOT fully sorted. Only parent-child ordering is enforced; siblings have no ordering.

## Q2 (Beginner) — Children of index 3 in a 0-indexed heap?
**Answer:** left = 2*3+1 = 7, right = 2*3+2 = 8
**Gap:** Don't confuse 0-indexed (2i+1, 2i+2) with 1-indexed (2i, 2i+1) formulas.

## Q3 (Beginner) — Time complexities: insert, extract-min, peek, build?
**Answer:** Insert O(log n), Extract O(log n), Peek O(1), Build O(n)
**Gap:** Build-heap is O(n) not O(n log n) — sum of heights proof (harmonic series).

## Q4 (Intermediate) — Kth Largest in a stream?
**Answer:** Min-heap of size K. Root = Kth largest. O(log k) per insertion.
**Gap:** Use min-heap NOT max-heap. Min-heap lets you evict the smallest of top-K cheaply.

## Q5 (Intermediate) — Tuple comparison in heapq?
```python
heap = [(2,'b'),(1,'z'),(1,'a'),(3,'a')]
# pops: (1,'a') then (1,'z')
```
**Answer:** Lexicographic comparison. Equal priority → compare second element ('a' < 'z').
**Gap:** Non-comparable objects cause TypeError. Fix: add unique counter as tiebreaker (priority, counter, obj).

## Q6 (Intermediate) — Streaming median in O(log n)?
**Answer:** Two-heap pattern — max-heap for lower half, min-heap for upper half.
**Invariants:** lower.top ≤ upper.top AND |len(lower) - len(upper)| ≤ 1
**Gap:** Must check BOTH invariants after every insertion.

## Q7 (Advanced) — Merge K sorted lists in O(n log k)?
**Answer:** K-way merge. Push (val, i, node) for each list head. Always pop min, push next from same list.
**Gap:** Need index i as tiebreaker — equal values cause TypeError when comparing ListNode objects.

## Q8 (Advanced) — remove(val) on a heap without decrease-key?
**Answer:** Lazy deletion. Mark val as removed in a counter. Skip on next pop.
**Gap:** Track logical size separately. Physical removal happens during cleanup, not during remove().

## Q9 (Expert) — Dijkstra processes same node multiple times?
**Answer:** No decrease-key in heapq → stale entries remain. Fix: `if d > dist[u]: continue`
**Gap:** This is lazy deletion applied to Dijkstra. A visited set also works but is less idiomatic.

## Q10 (Expert) — add/get_min/get_max/get_median all O(log n)?
**Answer:** Two-heap (median) + separate min-heap + max-heap. Or use SortedList from sortedcontainers.
**Gap:** Can't get global max from two-heap alone — it only guarantees median split.

---

## Score Guide
- 80–100: Ready for hard heap problems 🟢
- 60–79: Revisit Sessions 6–9 🟡
- 40–59: Review Sessions 3–5 + more LeetCode 🟠
- < 40: Restart from Sessions 1–3 🔴
