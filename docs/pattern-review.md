# Pattern Guide Review — Defect Log

Deep content review of all 19 guides in `pattern/` (22,244 lines). Every finding below was
verified directly against the source. Findings that could not be reproduced were dropped.

Status legend: `OPEN` — not yet fixed. `FIXED` — corrected in this pass.

---

## Summary

The algorithm code is almost entirely correct. Verified as correct: knapsack loop directions
(0/1 descending vs unbounded ascending), LIS `bisect_left` for strict increase, interval-DP
length-outer loop order, digit-DP `tight` included in the memo key, the submask idiom
`sub = (sub - 1) & mask`, backtracking `path[:]` copies on record, monotonic-stack strict vs
non-strict tie-breaks, binary-lifting depth-equalise-then-climb order, rerooting slide formulas,
the Floyd-Warshall `k`-outermost loop order, Tarjan low-link update rules, Dijkstra's stale-entry
skip, Bellman-Ford's `V-1` passes plus a `V`th detection pass, and the Fenwick `i & -i` walk
directions.

The defects are in the connective tissue: broken links, mislabelled problem routing, missing
complexity cases, duplicated topics with drifting notation, three under-built guides, and no
retrieval-practice material anywhere.

---

## Tier 1 — Factual defects

### 1.1 Links using the Jekyll baseurl (404 on the React SPA) — FIXED

The site has two frontends. Jekyll serves under `baseurl: /cses-analyses`; the React SPA
(`react-app/`, Vercel) serves under base `/`. A link written as `/cses-analyses/pattern/x`
resolves on Jekyll and 404s on the SPA. All internal links must be bare `/pattern/...`.

| File | Line | Link |
|------|------|------|
| `pattern/FenwickTree.md` | 9 | `/cses-analyses/pattern/segment-tree` |
| `pattern/FenwickTree.md` | 368 | `/cses-analyses/pattern/prefix-sum` |
| `pattern/FenwickTree.md` | 631 | `/cses-analyses/pattern/segment-tree` |
| `pattern/FenwickTree.md` | 632 | `/cses-analyses/pattern/prefix-sum` |
| `pattern/SegmentTree.md` | 554 | `/cses-analyses/pattern/fenwick-tree` |

### 1.2 Latent predicate bug in the binary-search-on-answer template — FIXED

`pattern/BinarySearch.md`, `can_split` (§3, ~line 463) and its repeats in the LC 410 walkthrough
(~621) and `can_ship` (~1337).

The greedy feasibility check starts a new part whenever the running sum would overflow, but never
checks that the single element itself fits:

```python
if current + num > max_sum:
    parts += 1
    current = num      # no check that num itself fits in max_sum
```

`can_split([8, 10], max_sum=9)` with `k=2` returns `True`, though no valid split exists. The bug
is masked in the guide because `lo = max(nums)` means the search never evaluates a `max_sum`
below the largest element — so the published LC 410 answer is still correct. It becomes a real
wrong answer the moment the predicate is copied without that `lo` initialisation, which is
exactly what a learner does.

Fix: guard the single element when starting a new part.

### 1.3 Code that raises NameError when copied — FIXED

`pattern/Graph.md` §15 (~2073-2117). Both `longest_path` and `count_paths` call `deque(...)`,
but neither block carries `from collections import deque`. Every other block in the file that
uses a deque has its own import (lines 179, 332, 540, 567, 813, 915, 968, 1354, 1728, 2018).

### 1.4 Quick-nav promises content the guide does not contain — FIXED

`pattern/Graph.md` lines 26-27 advertise "Ford-Fulkerson / Dinic's" and "Hopcroft-Karp /
Hungarian". §10 implements only Dinic's; §11 implements only Kuhn's DFS matching. Hopcroft-Karp
and the Hungarian algorithm appear nowhere in the file.

### 1.5 Problem routing errors — FIXED

| File | Line | Problem |
|------|------|---------|
| `pattern/TwoPointers.md` | 25 | "Merge two sorted arrays" routes to §9, which is LC 977 (Squares of a Sorted Array) — a merge from both ends of one array, not a merge of two arrays. |
| `pattern/TwoPointers.md` | 20 | "Container / trapping" routes to §7 (LC 11, Container With Most Water). Trapping Rain Water (LC 42) is a different problem and is not covered in the guide at all. |
| `pattern/Bitmask.md` | 48 | LC 698 (Partition to K Equal Sum Subsets) is filed under "Assignment DP `dp[mask]`". It is a k-way partition problem, not an assignment problem. |
| `pattern/FenwickTree.md` | 618 | Practice Order labels LC 493 as "Count Inversions". LC 493 is Reverse Pairs, which counts `nums[i] > 2 * nums[j]` — not plain inversions. The file's own master table (lines 88-89) has it right. LC 315 is the inversion-shaped problem. |
| `pattern/DP.md` | 643, 1483, 1857 | LC 1494 is filed under three different families: knapsack disguises, the LC 847 bitmask walkthrough, and DP on DAGs. It is a submask-partition problem, owned by `BitmaskDP_Subset_Partition.md` §9. |
| `pattern/DP.md` | 643 | LC 698 listed as a knapsack disguise. True only for `k=2`; for general `k` the knapsack template does not apply. |

### 1.6 Complexity omissions — FIXED

| File | Line | Issue |
|------|------|-------|
| `pattern/DP.md` | 1545 | Bitmask DP given as `O(2^N·N)` / `O(2^N·N²)` only. Missing `O(3^n)` for submask-partition enumeration, which `Bitmask.md` (780) and `BitmaskDP_Subset_Partition.md` (248) both state. |
| `pattern/DP.md` | 2171 | Cheat sheet row gives bitmask DP as `O(2^N * N)`, understating TSP and omitting `O(3^n)`. |
| `pattern/ContributionCounting.md` | 58 | "O(n) elements × O(1) per element". The monotonic-stack span computation in §3-4 is amortised O(1), not worst-case. |

### 1.7 Structural inconsistencies — FIXED

- `pattern/Graph.md` table of contents (103-120) lists §1-§16 but omits §0 (Graph
  Representations, line 124), §17 (Common Mistakes, 2249), and §18 (Practice Order, 2266).
- `pattern/Graph.md` has an unnumbered heading "Family F anchor: advanced graph patterns in
  LeetCode" (1944) sitting between §13 and §14, breaking the numbered scheme.

---

## Tier 2 — The cross-link web is one-directional

`DecisionMap.md` is the router and carries 45 outbound `/pattern/...` links. Almost nothing links
back, and the guides barely link to each other. Outbound sibling-link counts before this pass:

| Count | Files |
|-------|-------|
| 0 | Backtracking, BinarySearch, Bitmask, ContributionCounting, DP, DigitDP, EdgeContribution, FenwickTree, Graph, LCA, StackQueue, TwoPointers |
| 1 | BitmaskDP_Subset_Partition, PrefixSum, Tree |
| 2 | Heap |
| 3 | SegmentTree |
| 5 | SlidingWindow |
| 45 | DecisionMap (the router) |

Concrete silent hand-offs found:

- `ContributionCounting.md` line 78 says "edge contribution on trees" without linking
  `/pattern/edge-contribution`.
- `SlidingWindow.md` §8 links out to StackQueue; StackQueue §5 does not link back.
- `DP.md` never mentions that dedicated Digit DP, Bitmask, or Bitmask-DP guides exist.
- No guide links back to `/pattern/decision-map`.

---

## Tier 3 — Topics taught in two or three places with drifting notation

### 3.1 "Euler tour" means two incompatible things

| File | Convention | Length | Purpose |
|------|-----------|--------|---------|
| `Tree.md` §2 | `tin`/`tout`, no re-entry on backtrack | n entries | Subtree as a contiguous range for a segment tree / BIT |
| `LCA.md` §3 | Full tour, node re-appended on every backtrack | 2n−1 entries | RMQ over depths to answer LCA |

Both sections are titled "Euler tour". Neither warns the reader that the other exists or that the
conventions differ. This is the highest confusion risk in the folder.

### 3.2 LC 698 has two different algorithms with two different complexities

| File | Algorithm | Complexity |
|------|-----------|-----------|
| `Bitmask.md` (696-722) | `dp[mask]` = fill level of the current bucket mod target | `O(2^n · n)` |
| `BitmaskDP_Subset_Partition.md` (364-397) | Peel off one valid subset at a time via submask enumeration | `O(3^n)` |

Both are correct. Neither file acknowledges the other, so the differing complexity reads as a
contradiction.

### 3.3 The assignment-DP mask is inverted between two guides

`DP.md` (1466-1476) uses `mask` = set of **tasks** already assigned, deriving the worker as
`popcount(mask)`. `Bitmask.md` (565-575) uses `mask` = set of **workers** already used, deriving
the job as `popcount(mask)`. Both are valid duals; presented without comment they look like one
of them is wrong.

### 3.4 Near-verbatim duplicated implementations

| Topic | Locations |
|-------|-----------|
| Binary lifting LCA | `Tree.md` 436-473, `LCA.md` 417-476 |
| LC 236 walkthrough | `Tree.md` 545-552, `LCA.md` 199-206 (different example trees, so the two traces give different answers for the same node pair) |
| LC 337 tree-DP trace | `DP.md` 1280-1317, `Tree.md` 1229-1266 |
| LC 834 rerooting | `Tree.md` §5, `EdgeContribution.md` §5 |
| `max_sliding_window` | `StackQueue.md` 762-785, `SlidingWindow.md` 296-313 |
| `count_inversions` | `SegmentTree.md` 454-464, `FenwickTree.md` 379-388 |
| Kahn-based DAG DP | `Graph.md` §15, `DP.md` §14 |

Ownership decisions applied in this pass are recorded in the guides themselves via an explicit
"canonical guide" pointer at the top of each non-owning section.

---

## Tier 4 — Three guides missed the enhancement pass

`Heap.md` (537 lines), `SlidingWindow.md` (476), and `TwoPointers.md` (469) were last touched
Aug 21-22; every other guide was enhanced Aug 29 and runs 900-2,300 lines. All three lack the
From-Scratch derivation, an upfront Master LeetCode table, a Pattern Recognition Cheat Sheet, a
LeetCode Practice Ladder, and a Toolbox at a Glance.

Coverage holes, not just template holes:

- **Heap**: no lazy-deletion / indexed heap (needed for Dijkstra decrease-key), no justification
  for the `heapify` O(n) claim made at line 67, no custom-comparator wrapper pattern, no
  heap-vs-sort-vs-quickselect decision, missing LC 480 (sliding-window median), 703, 632, 264.
- **SlidingWindow**: no exactly-K reduction (`atMost(K) − atMost(K−1)`, the standard trick),
  missing LC 76 (minimum window substring), LC 340 (table row only, no worked example), LC 862
  (negatives, needs prefix sums plus a deque).
- **TwoPointers**: missing LC 42 (trapping rain water — advertised in the nav), LC 88 (real merge
  of two sorted arrays — advertised in the nav), LC 125 (valid palindrome), LC 142 (cycle entry
  point, mentioned in an insight box with no code).

---

## Tier 5 — No retrieval-practice material

Zero `Self-Test`, `Recall`, or equivalent sections across all 19 files. Most guides also lack a
"when this technique fails" section, so a learner has no way to distinguish "I recognise this
explanation" from "I can reproduce this cold". Reading is recognition; mastery needs recall.

Addressed by adding a `## Self-Test` block plus a "When this fails" note to every guide, and a
`pattern/Mastery.md` page (`permalink: /pattern/mastery`) carrying the spaced-repetition
schedule, per-pattern mastery checklist, and drill prompts.

---

## Non-defects (checked, deliberately not changed)

- `Tree.md` `lca()` (460-462) lifts by `diff` without a `-1` guard, unlike `LCA.md`'s `_lift`.
  With `LOG = 20` (line 434) and a correctly built table, `u` cannot become `-1` while lifting by
  a depth difference, so this is not a live bug. Documented `LOG` sizing was added instead.
- `Backtracking.md` line 1332 `result.append(path)` without a copy — `path` is a `str` there,
  which is immutable. Correct as written.
- `Backtracking.md` Hamiltonian path (1632-1644) returns before restoring `visited` on success.
  Harmless for a find-one-path goal.
- `StackQueue.md` / `Heap.md` median traces show heap contents as positive values while the code
  stores negated values in the low heap. Simplified notation, not a wrong algorithm.

---

# Round 2 — Pedagogical Audit (five parallel deep reviews)

Round 1 above targeted correctness and consistency. Round 2 asked a different question: **can a
self-learner reach mastery from these pages alone?** Each guide was read line by line against a
10-point rubric (motivation before mechanism, derivation vs assertion, worked traces, stated
invariants, hard parts not skipped, no code walls, sane progression, cross-file consistency,
coverage gaps, nothing misleading).

## Verified and fixed

| # | File | Defect | Verification |
|---|------|--------|--------------|
| 1 | `EdgeContribution.md` | `minEdgeReversals` had the two edge weights **swapped** (`with-arrow` charged 1, `against-arrow` charged 0), returning `(#edges − correct)` at every index. The problem statement was also inverted ("every node can reach `i`" instead of "from `i` you can reach every node"), and the trace was computed from the buggy weights. | Fixed all four (statement, weights, prose, trace). Re-verified against both LeetCode examples and **400 random directed trees** vs brute force: 0 mismatches. |
| 2 | `DP.md` | LC 329 trace table had two wrong cells (`dfs(0,2)` and `dfs(2,2)` shown as 1, actually 2) plus a self-contradictory inline note (`dfs(2,1)=1 (…2>1 yes)` — it is 4). | Recomputed the table programmatically; replaced with a corrected table and a corner-inward derivation. |
| 3 | `Tree.md` | Virtual-tree example **dropped query node 7** and listed `{1,3,5,8,9}`, which contains non-LCA nodes and contradicts its own diagram. | Replaced with query set `{3,9,10}` → `{1,3,5,9,10}`, hand-verified (`LCA(9,10)=5`), still hitting the `2K−1` bound, plus prose on why 2/7/8 compress away. |
| 4 | `Tree.md` | "LCA (with RMQ), O(1)" listed as a capability of the **`tin`/`tout`** Euler tour. That variant stores each node once and cannot support LCA-by-RMQ; it needs the `2N−1` backtracking tour. Directly contradicted the disambiguation added in Round 1. | Removed from the table, replaced with a callout explaining why, pointing to `LCA.md`. |
| 5 | `SlidingWindow.md` | The negatives caveat routed readers to `PrefixSum.md` for prefix-sum + monotonic deque — but **§13 of the same file** is exactly that (LC 862), 400 lines below. | Re-pointed to `§13` with a "read this, then see how the assumption gets repaired" handoff. |
| 6 | `StackQueue.md` | "This template solves: LC 239, 1425, 862, 1438" — only 239 is solved by the fixed-size template. 1425 runs over DP values, 862 over prefix sums with a variable window, 1438 needs two deques. | Reworded to "same tool, different shape", naming each variation and linking 862 to `SlidingWindow §13`. |
| 7 | `BitmaskDP_Subset_Partition.md` | Self-Test Q3 taught lowest-set-bit canonicalisation, but **every code block uses `sub < comp`** and the peel-off loops use neither. | Answer now distinguishes both tricks, says which code uses which, and notes the redundancy is harmless for `min`/`max` but wrong for **counting**. |
| 8 | `PrefixSum.md` | See-also cited "Binary Search §10" for lower-bound-over-prefix-array; §10 is *Python's bisect Module*. | Re-pointed to §2 (lower/upper bound) with §10 kept as the API reference. |
| 9 | `Bitmask.md` | Stale anchor `#pattern-1-traveling-salesman-problem-tsp` surviving the Round 1 heading rename. | Fixed; full link sweep now clean. |

## Reported but rejected after verification

Reviewer findings are not automatically defects. These were checked and left alone:

- **`EdgeContribution.md` LC 834 trace "wrong" (`sub[]` and pass-2 answers).** Hand-verified all
  six distance sums against the tree `0-1, 0-2, 0-3, 2-4, 4-5`: `[8,12,8,12,10,14]` is correct,
  as is `sub = [6,1,3,1,2,1]` and `answer[0]=8`. No change.
- **`Graph.md` undirected cycle detection "silently breaks on multi-edges".** Executed it: a
  doubled `u—v` returns `True`, which is *correct* — two parallel edges genuinely form a cycle in
  a multigraph. The node-skip catches it on `u`'s second pass over its list. The guide's own
  "When This Fails" bullet was the misleading part (it implied the template is broken), so that
  bullet was rewritten to name the real trap: accidental duplicate edges in the *input*.

## Open pedagogical backlog (not defects — enhancement work)

Ranked by mastery impact. Nothing here is wrong; it is material that is *missing* or misplaced.

1. **Derivations living only in Self-Test answers.** Dijkstra's exchange argument, Floyd-Warshall's
   "why `k` outermost", segment-tree `O(log n)` tiling, and Fenwick's lowbit responsibility range
   are all proved in Self-Test but merely asserted in the body. Self-Tests should *review* a
   derivation, not be the first place it appears.
2. **Missing traces on the hardest mechanics.** Lazy propagation (58 lines, no numbers), Tarjan
   SCC and articulation points (no `disc`/`low` walk), Dinic, Kuhn matching, two-BIT range
   update/query, `find_kth`, persistent segment tree.
3. **`Graph.md` is two documents.** It teaches Families A–D well and turns into a template catalog
   from §5 onward. §14 (multi-source BFS) is referenced from §1 but sits ~1600 lines later, after
   flow and 2-SAT.
4. **DP state design is asserted, not derived** — states appear fully formed rather than being
   built from a failed attempt. Same for the LIS `bisect_left` step and Edit Distance (routed but
   never taught).
5. **Union-Find inconsistency in `Graph.md`** — the LC 547 walkthrough attaches without rank while
   the guide says rank is load-bearing.
6. **Duplicate entries** in the `TwoPointers.md` and `Heap.md` practice ladders; LC 621 mentioned
   but never taught in `Heap.md`.

## Round 2 follow-up — cross-file and consistency fixes

| File | Defect | Resolution |
|------|--------|------------|
| `EdgeContribution.md` vs `Tree.md` | Both traced LC 834 and reached **different answers** (`[8,12,8,12,10,14]` vs `[8,12,6,10,10,10]`). Neither was arithmetically wrong — they used *different trees* under the same problem heading, and only `Tree.md` used the official LeetCode example. | Unified `EdgeContribution.md` onto the official tree `[[0,1],[0,2],[2,3],[2,4],[2,5]]`, stated up front that the file uses one running example, and rewrote §3's diagram, the pass-1 sum, and the pass-2 slide chain to match. Verified the code reproduces `[8,12,6,10,10,10]`. |
| `DP.md:75` | Claimed DP answers "never *give me any one valid answer*". False — the guide teaches LCS reconstruction 800 lines later, and many DP problems require returning the witness. | Rewritten to say DP's natural output is a number but reconstruction (full table / parent pointers) recovers the witness, with the warning that row-only space optimisation destroys exactly what reconstruction needs. Backtracking is now scoped to *all* answers or no optimal substructure. |
| `Heap.md` practice ladder | 347, 253, and 23 each appeared twice in sequence. | Removed the duplicate block, kept the `(§11)` annotation on the surviving LC 23 entry. |
| `TwoPointers.md` practice ladder | 11, 75, and 15 each appeared twice. | Removed the duplicate block; ladder now ascends once through to 141/142. |
| `Graph.md` LC 547 | The walkthrough's DSU attaches roots without rank while "When This Fails" calls rank load-bearing — a learner cannot tell which is right. | Added a note explaining that path compression alone gives O(log n) amortised and suffices at `n <= 200`, while the §9 class keeps rank for the α(n) bound at `n ≈ 10⁵`, with a rule of thumb for choosing. |
