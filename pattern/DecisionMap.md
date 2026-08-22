---
layout: simple
title: "Pattern Decision Map"
permalink: /pattern/decision-map
---

# Pattern Decision Map — Which Technique Do I Use?

You have 18 technique guides in this folder. This page is the **router** you read *before* them. Each guide answers "how does this technique work"; this page answers the earlier question: **"which one do I even reach for?"**

The core skill of a strong problem-solver is not memorizing algorithms — it is reading a fresh problem, spotting a few **surface cues** (the shape of the input, the exact thing being asked, the size of `n`), and mapping those cues to a technique family in seconds. This page makes that mapping explicit.

`★ Insight ─────────────────────────────────────`
- Selection is **cue-driven, not recall-driven**. Experts don't scan a mental list of 18 algorithms; they notice "sorted array + find a pair" and the answer arrives before they've named it. Train the cues, not the catalog.
- Two cues dominate: **input shape** (array / tree / graph / grid / set of choices) and **the ask** (find a pair / longest region / count ways / range query). Constraint size (`n`) is the tie-breaker when two techniques both fit.
- When two techniques both seem to fit, that's not failure — it's information. The tie-breaker table below exists because those confusions are *predictable*.
`─────────────────────────────────────────────────`

## How to use this map

1. **Read the problem once.** Note the input shape and what it asks for.
2. **Start at the master router** below — pick the branch matching the input shape.
3. **Drop into the family sub-map** it points to. Follow the yes/no cues to a leaf.
4. **Open the linked guide** in the table under that sub-map. The guide has the template, traces, and pitfalls.
5. **Stuck between two?** Check the [tie-breaker table](#8-tie-breakers-the-confusable-pairs). **Unsure about complexity budget?** Check the [constraint-size cheat sheet](#9-constraint-size-cheat-sheet).

---

## Table of Contents

1. [Master Router](#1-master-router)
2. [Array / String Family](#2-array--string-family)
3. [Tree Family](#3-tree-family)
4. [Graph Family](#4-graph-family)
5. [DP Family](#5-dp-family)
6. [Range-Query Structures](#6-range-query-structures)
7. [Subset / Small-n Family](#7-subset--small-n-family)
8. [Tie-Breakers: The Confusable Pairs](#8-tie-breakers-the-confusable-pairs)
9. [Constraint-Size Cheat Sheet](#9-constraint-size-cheat-sheet)
10. [Worked Routing Examples](#10-worked-routing-examples)
11. [Full Technique Index](#11-full-technique-index)

---

## 1. Master Router

Start here. The first question is always **"what shape is the input?"** — then a second cue narrows the family.

```mermaid
graph TD
    START["Read the problem.<br/>What is the input shape?"]

    START --> ARR["Array / String"]
    START --> TREE["Rooted / binary Tree"]
    START --> GRAPH["Graph:<br/>nodes + edges"]
    START --> CHOICE["Sequence of choices /<br/>count or optimize ways"]
    START --> RANGE["Static-ish array +<br/>many range queries"]
    START --> GRID["2-D grid / matrix"]
    START --> SMALL["Set of items,<br/>n very small (n ≤ 20)"]

    ARR --> AFAM["→ §2 Array / String family"]
    TREE --> TFAM["→ §3 Tree family"]
    GRAPH --> GFAM["→ §4 Graph family"]
    CHOICE --> DFAM["→ §5 DP family"]
    RANGE --> RFAM["→ §6 Range-query structures"]
    GRID --> GRFAM["→ Grid = implicit graph (§4)<br/>or grid DP (§5)"]
    SMALL --> SFAM["→ §7 Subset / small-n family"]
```

| Input shape / ask | Go to |
|-------------------|-------|
| Array or string, one pass, find a pair / window / running total | [§2 Array / String](#2-array--string-family) |
| Rooted or binary tree, ancestors / subtree aggregates | [§3 Tree](#3-tree-family) |
| Explicit nodes + edges, reachability / shortest path / connectivity | [§4 Graph](#4-graph-family) |
| "How many ways", "min/max cost of a sequence of decisions" | [§5 DP](#5-dp-family) |
| Fixed array, then thousands of `query(l,r)` and/or `update(i)` | [§6 Range structures](#6-range-query-structures) |
| 2-D grid: flood fill / shortest path in maze / connected regions | [§4 Graph](#4-graph-family) (grid is an implicit graph — each cell a node, neighbors = up/down/left/right) |
| 2-D grid: count paths / min path cost with movement rules | [§5 DP](#5-dp-family) (grid DP: `dp[r][c]` from top/left) |
| Pick a subset / assign items, `n ≤ 20` | [§7 Subset / small-n](#7-subset--small-n-family) |

---

## 2. Array / String Family

The workhorse family. The deciding cues: **is it sorted?**, **do I want a pair or a region?**, **do I need running totals?**

```mermaid
graph TD
    A["Array / String problem"]
    A --> A1["Find a PAIR / triplet,<br/>or in-place reorder?"]
    A --> A2["Longest / shortest<br/>contiguous REGION<br/>under a constraint?"]
    A --> A3["Many sum/count queries<br/>over ranges (no updates)?"]
    A --> A4["Search a sorted array,<br/>or 'minimize the max' /<br/>'maximize the min'?"]
    A --> A5["Need nearest greater/<br/>smaller element,<br/>or 'next warmer day'?"]
    A --> A6["Sum a quantity over<br/>ALL subarrays / pairs?"]
    A --> A7["Repeatedly need the<br/>smallest/largest, or<br/>streaming top-k?"]

    A1 --> TP["Two Pointers"]
    A2 --> SW["Sliding Window"]
    A3 --> PS["Prefix Sum"]
    A4 --> BS["Binary Search"]
    A5 --> MS["Monotonic Stack / Queue"]
    A6 --> CC["Contribution Counting"]
    A7 --> HP["Heap / Priority Queue"]
```

| You see... | Technique | Guide |
|------------|-----------|-------|
| Pair summing to target on **sorted** data; dedup / move-zeros in place; palindrome; 3Sum | Two Pointers | [Two Pointers](/pattern/two-pointers) |
| "Longest/shortest subarray where...", "at most k distinct", fixed-size window | Sliding Window | [Sliding Window](/pattern/sliding-window) |
| Repeated `sum(l..r)`, "subarray sums to k", running total, difference array | Prefix Sum | [Prefix Sum](/pattern/prefix-sum) |
| Sorted lookup; "smallest x such that feasible(x)"; minimize-the-max | Binary Search | [Binary Search](/pattern/binary-search) |
| Next greater element, stock span, largest rectangle, sliding-window max | Monotonic Stack / Queue | [Stack & Queue](/pattern/stack-queue) |
| "Sum of min over all subarrays", "total pairs where...", per-element contribution | Contribution Counting | [Contribution Counting](/pattern/contribution-counting) |
| "Top-k largest", "k closest", merge k sorted lists, running median, repeated extract-min | Heap / Priority Queue | [Heap / Priority Queue](/pattern/heap) |

---

## 3. Tree Family

Cue: the input is a **rooted tree** (or you can root it). The deciding question is what you aggregate — **paths up to ancestors**, **subtree totals**, or **the same total from every possible root**.

```mermaid
graph TD
    T["Rooted / binary tree"]
    T --> T1["Traverse / aggregate a subtree,<br/>diameter, path sums,<br/>DFS/BFS bookkeeping?"]
    T --> T2["Repeated 'lowest common<br/>ancestor' / distance<br/>between two nodes?"]
    T --> T3["Answer needed for EVERY node<br/>as root (sum of distances,<br/>edge counted once)?"]

    T1 --> TR["Tree Traversal / DP on Trees"]
    T2 --> LCA["LCA (binary lifting / Euler)"]
    T3 --> EC["Edge Contribution & Rerooting"]
```

| You see... | Technique | Guide |
|------------|-----------|-------|
| Subtree sums, tree diameter, tree DP, DFS/BFS traversal order | Tree Patterns | [Tree Patterns](/pattern/tree) |
| Many `lca(u,v)` queries, distance in tree, kth ancestor | LCA | [LCA](/pattern/lca) |
| "Sum of distances from every node", each edge's contribution, reroot in O(n) | Edge Contribution / Rerooting | [Edge Contribution & Rerooting](/pattern/edge-contribution) |

---

## 4. Graph Family

Cue: explicit **nodes + edges**. Then split by the ask, and for shortest-path split further by **edge weights**.

```mermaid
graph TD
    G["Graph: nodes + edges"]
    G --> G1["Shortest path?"]
    G --> G2["Connectivity / components /<br/>ordering / cycles?"]

    G1 --> W0["Unweighted<br/>(or all weight 1)"]
    G1 --> W1["Non-negative<br/>weights"]
    G1 --> W2["Negative<br/>weights allowed"]
    G1 --> W3["All-pairs,<br/>small V (≤ 400)"]

    W0 --> BFS["BFS"]
    W1 --> DIJ["Dijkstra"]
    W2 --> BF["Bellman-Ford"]
    W3 --> FW["Floyd-Warshall"]

    G2 --> C1["Cheapest set of edges<br/>connecting all nodes → MST"]
    G2 --> C2["Order respecting deps → Topo sort"]
    G2 --> C3["Groups reachable both ways → SCC / Union-Find"]
```

All graph shortest-path, connectivity, MST, topological-sort, and SCC material lives in one guide:

| You see... | Sub-technique | Guide |
|------------|---------------|-------|
| Fewest edges / unweighted shortest path | BFS | [Graph Patterns](/pattern/graph) |
| Non-negative weights, single source | Dijkstra | [Graph Patterns](/pattern/graph) |
| Negative edges, detect negative cycle | Bellman-Ford | [Graph Patterns](/pattern/graph) |
| All-pairs shortest path, dense small graph | Floyd-Warshall | [Graph Patterns](/pattern/graph) |
| Cheapest connecting tree | Kruskal / Prim (MST) | [Graph Patterns](/pattern/graph) |
| Dependency ordering, DAG | Topological sort | [Graph Patterns](/pattern/graph) |
| Mutually reachable groups / connectivity queries | SCC / Union-Find | [Graph Patterns](/pattern/graph) |

---

## 5. DP Family

Cue: **"count the number of ways"**, or **"min/max cost of a sequence of decisions"**, and greedy demonstrably fails. Then split by *what the state is built from*.

```mermaid
graph TD
    D["Count ways / optimize<br/>over a sequence of choices"]
    D --> D1["State = index / capacity /<br/>substring — classic DP?"]
    D --> D2["Counting numbers in [L,R]<br/>with a digit property?"]
    D --> D3["State = which subset<br/>is used, n ≤ 20?"]
    D --> D4["Need to ENUMERATE actual<br/>solutions, prune dead branches?"]

    D1 --> DP["Dynamic Programming"]
    D2 --> DD["Digit DP"]
    D3 --> BDP["Bitmask DP"]
    D4 --> BT["Backtracking"]
```

| You see... | Technique | Guide |
|------------|-----------|-------|
| Overlapping subproblems, "ways to", knapsack, LIS, edit distance, interval DP | Dynamic Programming | [Dynamic Programming](/pattern/dp) |
| "How many integers in `[L,R]` with digit property", huge upper bound | Digit DP | [Digit DP](/pattern/digit-dp) |
| Assign/permute a small set, TSP, "state = used mask", `n ≤ 20` | Bitmask DP | [Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition) |
| List all permutations/combinations/board fillings, prune infeasible paths | Backtracking | [Backtracking](/pattern/backtracking) |
| Set-membership tricks, XOR, subset iteration (building block for the above) | Bitmask Techniques | [Bitmask Techniques](/pattern/bitmask) |

---

## 6. Range-Query Structures

Cue: a mostly-fixed array plus **many** `query(l,r)` and/or `update(i)`. The deciding question: **are there updates**, and **is the operation invertible?**

```mermaid
graph TD
    R["Array + many range queries"]
    R --> R1["Any point/range UPDATES<br/>between queries?"]
    R1 -->|"No updates"| PSX["Prefix Sum"]
    R1 -->|"Yes, updates too"| R2["Is the op invertible?<br/>(sum / xor / count)"]
    R2 -->|"Invertible<br/>(sum, xor)"| FEN["Fenwick Tree (BIT)"]
    R2 -->|"Not invertible<br/>(min, max, gcd, assign)"| SEG["Segment Tree"]
```

| You see... | Technique | Guide |
|------------|-----------|-------|
| Range sums, **no updates** after building | Prefix Sum | [Prefix Sum](/pattern/prefix-sum) |
| Range **sum/xor** with point updates; simplest code | Fenwick Tree (BIT) | [Fenwick Tree (BIT)](/pattern/fenwick-tree) |
| Range **min/max/gcd/assign**, lazy propagation, non-invertible ops | Segment Tree | [Segment Tree](/pattern/segment-tree) |

`★ Insight ─────────────────────────────────────`
- The Fenwick-vs-Segment fork is entirely about **invertibility**. Fenwick answers `query(l,r)` as `prefix(r) − prefix(l−1)` — subtraction *requires* an inverse, so it works for sum and xor but not min/max. Segment Tree stores each node's answer directly and never subtracts, so it handles any associative op at the cost of ~2× the code.
- No updates at all? Don't build a tree. Prefix Sum is O(1) per query after O(n) setup — strictly simpler, strictly faster.
`─────────────────────────────────────────────────`

---

## 7. Subset / Small-n Family

Cue: pick a **subset** or **assignment** of items, and `n` is suspiciously small (`n ≤ 20`, sometimes `≤ 24`). Small `n` is a *loud* signal that `2ⁿ` enumeration is intended.

```mermaid
graph TD
    S["n very small (n ≤ 20),<br/>pick subset / assignment"]
    S --> S1["Just enumerate / test<br/>subsets, set membership,<br/>XOR tricks?"]
    S --> S2["Optimize over subsets with<br/>overlapping subproblems<br/>(TSP, partition, cover)?"]

    S1 --> BM["Bitmask Techniques"]
    S2 --> BMD["Bitmask DP"]
```

| You see... | Technique | Guide |
|------------|-----------|-------|
| Represent a set as an int, iterate subsets, XOR / AND / popcount tricks | Bitmask Techniques | [Bitmask Techniques](/pattern/bitmask) |
| "Min cost to partition/assign", TSP, set cover, `dp[mask]` over `2ⁿ` states | Bitmask DP | [Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition) |

---

## 8. Tie-Breakers: The Confusable Pairs

When two techniques both seem to fit, these are the *predictable* confusions and the one question that resolves each.

| Confused between | Ask yourself | Then pick |
|------------------|--------------|-----------|
| **Two Pointers** vs **Sliding Window** | Do both pointers move *forward* and I care about the *region between* them? | Yes → Sliding Window. Pointers converge from ends / I want the *pair* → Two Pointers. |
| **Fenwick** vs **Segment Tree** | Is the operation invertible (sum, xor)? | Invertible → Fenwick (less code). Min/max/assign/lazy → Segment Tree. |
| **Prefix Sum** vs **Fenwick** | Are there updates between queries? | No updates → Prefix Sum. Updates → Fenwick. |
| **LCA (Euler tour)** vs **Heavy-Light / path structures** | Just ancestors/distance, or updating values *along paths*? | Ancestor/distance queries → LCA. Path updates/queries → segment tree on chains (Tree guide). |
| **Backtracking** vs **DP** | Do I need to *list actual solutions*, or just *count/optimize*? | Enumerate solutions → Backtracking. Count/optimize with overlapping subproblems → DP. |
| **Contribution Counting** vs **direct DP/scan** | Does each element contribute *independently* to the total? | Independent per-element contribution → Contribution Counting. Contributions interact / threshold → DP or two-pointer. |
| **Heap** vs **Sort** vs **BST** | Do I need the *top-k / streaming min* repeatedly, or the *whole thing sorted once*? | Repeated extract-min / running top-k → Heap. One-shot full order → Sort. Ordered + dynamic membership → balanced BST / ordered set. |

---

## 9. Constraint-Size Cheat Sheet

The `n` bound in the problem statement quietly announces the intended complexity. Read it backwards: pick the loosest algorithm whose cost fits ~10⁸ operations.

| `n` bound | Budget you can afford | Techniques it points to |
|-----------|-----------------------|-------------------------|
| `n ≤ 20` | `O(2ⁿ)` / `O(2ⁿ · n)` | Bitmask, Bitmask DP, Backtracking |
| `n ≤ 100` | `O(n³)`... `O(n⁴)` | Floyd-Warshall, interval DP, small matrix DP |
| `n ≤ 500` | `O(n³)` | Floyd-Warshall, DP with 3 nested states |
| `n ≤ 5000` | `O(n²)` | Classic 2-D DP, `O(n²)` graph algorithms |
| `n ≤ 10⁵` | `O(n log n)` | Sort, Binary Search, Dijkstra, Segment/Fenwick Tree, Sliding Window |
| `n ≤ 10⁶` | `O(n)` / `O(n log log n)` | Two Pointers, Prefix Sum, single-pass DP, sieve |
| `n ≤ 10¹⁸` | `O(log n)` / closed form | Binary search on answer, matrix exponentiation, Digit DP, math |

`★ Insight ─────────────────────────────────────`
- The size bound is the cheapest cue and often the most decisive. `n ≤ 20` is a near-certain flag for exponential/bitmask; `n ≤ 10¹⁸` rules out anything that even touches every element, forcing `O(log n)` or closed-form.
- Use it as a *sanity filter*: if your candidate technique is `O(n²)` but `n = 10⁶`, you've picked the wrong family — go back to the router.
`─────────────────────────────────────────────────`

---

## 10. Worked Routing Examples

The router only pays off if you can *run it* on a cold problem. Here are five, each showing the cue-spotting walk — shape, then the ask, then constraint size — from problem text to a landed technique. Practice narrating this out loud; that inner monologue *is* the skill.

**Example 1** — *"Given a sorted array, find two numbers that add up to a target."*
- Shape: array. Ask: find a **pair**. Extra cue: **sorted**.
- Router → §2 Array/String → "find a PAIR?" → **Two Pointers** (opposite ends; sortedness makes the sum respond monotonically).

**Example 2** — *"Longest substring with at most 2 distinct characters."*
- Shape: string. Ask: **longest contiguous region** under a constraint ("at most 2 distinct").
- Router → §2 → "longest/shortest REGION?" → **Sliding Window** (grow right, shrink left when the distinct-count breaks).

**Example 3** — *"Count islands in a grid of land/water cells."*
- Shape: **2-D grid**. Ask: connected regions.
- Router → grid branch → "connected regions" → **§4 Graph**, grid-as-implicit-graph → flood fill with BFS/DFS (each cell a node, 4 neighbors).

**Example 4** — *"Number of ways to make amount N from given coin denominations."*
- Shape: set of choices (which coins). Ask: **count ways**. Greedy fails (denominations arbitrary).
- Router → §5 DP → "count ways / overlapping subproblems" → **Dynamic Programming** (`dp[amount]`, unbounded-knapsack shape).

**Example 5** — *"Assign N tasks to N workers minimizing total cost, N ≤ 18."*
- Shape: assignment over a small set. Loud cue: **N ≤ 18** → `2ⁿ` intended.
- Router → §7 Subset/small-n → "optimize over subsets, overlapping subproblems" → **Bitmask DP** (`dp[mask]` = min cost to assign the tasks in `mask`).

`★ Insight ─────────────────────────────────────`
- Notice the order every time: **shape → ask → size**. Shape picks the family, the ask picks the branch, and the constraint (Example 5's `N ≤ 18`) confirms or overrides. When size and ask disagree, size usually wins — it's the hardest cue to fake.
- Example 3 is the payoff of the grid reframing: there is no "island algorithm," only "grid is a graph, run flood fill." Reframers beat memorizers.
`─────────────────────────────────────────────────`

---

## 11. Full Technique Index

All 18 guides, with the one-line cue that should make you reach for each.

| Technique | Reach for it when... | Guide |
|-----------|----------------------|-------|
| Two Pointers | pair on sorted data / in-place reorder / palindrome | [Two Pointers](/pattern/two-pointers) |
| Sliding Window | longest/shortest contiguous region under a constraint | [Sliding Window](/pattern/sliding-window) |
| Prefix Sum | many range-sum queries, no updates; "subarray sums to k" | [Prefix Sum](/pattern/prefix-sum) |
| Binary Search | sorted lookup or "smallest x that is feasible" | [Binary Search](/pattern/binary-search) |
| Stack & Queue | nearest greater/smaller, monotonic stack, sliding-window max | [Stack & Queue](/pattern/stack-queue) |
| Contribution Counting | sum a quantity over all subarrays/pairs, per-element | [Contribution Counting](/pattern/contribution-counting) |
| Tree Patterns | subtree aggregates, tree diameter, DP on trees | [Tree Patterns](/pattern/tree) |
| LCA | repeated lowest-common-ancestor / tree distance queries | [LCA](/pattern/lca) |
| Edge Contribution & Rerooting | answer for every node as root, edge counted once | [Edge Contribution & Rerooting](/pattern/edge-contribution) |
| Graph Patterns | shortest path, connectivity, MST, topo sort, SCC | [Graph Patterns](/pattern/graph) |
| Dynamic Programming | count ways / optimize over overlapping subproblems | [Dynamic Programming](/pattern/dp) |
| Digit DP | count numbers in `[L,R]` with a digit property | [Digit DP](/pattern/digit-dp) |
| Bitmask Techniques | set-as-int, subset iteration, XOR / popcount tricks | [Bitmask Techniques](/pattern/bitmask) |
| Bitmask DP | optimize over subsets, `n ≤ 20`, TSP / partition | [Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition) |
| Backtracking | enumerate actual solutions, prune infeasible branches | [Backtracking](/pattern/backtracking) |
| Segment Tree | range min/max/assign with updates, lazy propagation | [Segment Tree](/pattern/segment-tree) |
| Fenwick Tree (BIT) | range sum/xor with point updates, minimal code | [Fenwick Tree (BIT)](/pattern/fenwick-tree) |
| Heap / Priority Queue | repeated extract-min, top-k, merge k lists, running median | [Heap / Priority Queue](/pattern/heap) |

---

*Selection mastered — read the cues, not the catalog. Input shape and the ask pick the family; constraint size breaks the tie.*
