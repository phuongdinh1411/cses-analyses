---
layout: simple
title: "Knapsack Variants — 75 Problems by Knapsack Pattern"
permalink: /pattern/knapsack-dp-youknowwho
---

# Knapsack Variants — 75 Problems Grouped by Knapsack Pattern

Source: [YouKn0wWho Academy — Knapsack and Basic DP](https://youkn0wwho.academy/topic-list/knapsack).

This page groups all 75 by the **specific knapsack variant** each problem is, not by generic DP buckets. Knapsack problems differ along two axes:

- **Item multiplicity** — how many times an item may be taken: *0/1* (once), *bounded* (≤ k times), *unbounded* (∞), *grouped* (pick ≤1 / exactly-structure per group).
- **DP index (what the array is keyed on)** — *capacity/weight*, *value* (dual, when weights are huge), or *feasibility/count* (boolean "reachable sum" or "number of ways").

Every true-knapsack problem below is tagged `[multiplicity · index]`. The last section holds problems the source files under this topic that are **not knapsack** (general DP) — separated honestly so you drill the real pattern.

---

## Knapsack-Variant Map

| § | Knapsack variant | Signature | Problems |
|---|------------------|-----------|----------|
| A | **0/1 knapsack** (capacity index) | each item once; capacity loop **backward** | 10 |
| B | **Unbounded knapsack** | item reused; capacity loop **forward** | 6 |
| C | **Bounded / multiple knapsack** | item ≤ k times; binary-split or deque | 3 |
| D | **Subset-sum feasibility** (0/1, boolean) | `dp[s] |= dp[s-x]` | 7 |
| E | **Counting knapsack** (# ways to hit sum) | `dp[s] += dp[s-x]`; +erase via modinv | 6 |
| F | **Value-indexed knapsack** (dual) | huge capacity → DP on value, store min weight | 5 |
| G | **Grouped knapsack** | items partitioned into groups | 4 |
| H | **Knapsack ⊕ extra structure** | knapsack fused w/ seg-tree / tree / query / CHT | 8 |
| — | *Not knapsack* — general DP filed here | linear / grid / interval / game / state-machine | 30 |

True knapsack (tag appearances across A-H): 49.
True knapsack (unique problem IDs): 45.
General DP mixed in (unique, non-knapsack): 30.
Total unique problems: 75.

---

## A. 0/1 Knapsack — `[0/1 · capacity]`

Each item taken at most once; DP keyed on remaining capacity; **inner capacity loop runs high→low** so an item can't be reused in one pass. The namesake.

| # | Problem | Source | What's the "weight" / "value" |
|---|---------|--------|-------------------------------|
| 2 | ⭐ [Knapsack 1 (dp_d)](https://atcoder.jp/contests/dp/tasks/dp_d) | AtCoder | textbook: weight=W, value=v |
| 10 | [Book Shop](https://cses.fi/problemset/task/1158) | CSES | weight=price, value=pages |
| 32 | [Dima and Salad](https://codeforces.com/problemset/problem/366/C) | CF | weight = `a-k·b` (shifted), value=a |
| 41 | [Round Subset](https://codeforces.com/contest/837/problem/D) | CF | weight = #factor-5s, value = min(Σ2, Σ5) |
| 52 | [Knapsack](https://codeforces.com/problemset/problem/1132/E) | CF | small distinct weights, huge counts (→ bounded, see C) |
| 68 | [Money Buys Happiness](https://codeforces.com/problemset/problem/1974/E) | CF | weight=cost, value=happiness |
| 67 | [Happy City & Uncle Max](https://codeforces.com/group/Rilx5irOux/contest/619634/problem/I) | CF | budget-constrained 0/1 |
| 63 | [Lightweight Knapsack](https://atcoder.jp/contests/abc442/tasks/abc442_g) | AtCoder | weight-optimized 0/1 |
| 51 | [Mr. Kitayuta, Treasure Hunter](https://codeforces.com/problemset/problem/506/A) | CF | 0/1 over jump-lengths, offset state |
| 21 | [Knapsack](https://codeforces.com/contest/1446/problem/A) | CF | 0/1 feasibility + greedy construction |

---

## B. Unbounded Knapsack — `[unbounded · capacity]`

Each item reusable infinitely; **inner capacity loop runs low→high** so re-picking is allowed.

| # | Problem | Source | Note |
|---|---------|--------|------|
| 6 | ⭐ [Minimizing Coins](https://cses.fi/problemset/task/1634) | CSES | min item count to reach sum |
| 3 | [Coin Combinations I](https://cses.fi/problemset/task/1635) | CSES | **ordered** count (coin loop inside) |
| 38 | [Coin Combinations II](https://cses.fi/problemset/task/1636) | CSES | **unordered** count (coin loop outside) — the loop-order contrast |
| 7 | [Removing Digits](https://cses.fi/problemset/task/1637) | CSES | unbounded min-steps |
| 50 | [Smithing Skill](https://codeforces.com/contest/1989/problem/D) | CF | unbounded + number-theory pruning |
| 55 | [Ski Lessons](https://www.acmicpc.net/problem/6114) | BOJ | unbounded choice over time |

> #3 and #38 are the single most important pair in the whole list: identical recurrence, loop order swapped → ordered vs unordered. Coins-unbounded (#38) is the canonical **unordered** form; Coin-Combos-I (#3) the **ordered** (= sequence-counting) form.

---

## C. Bounded / Multiple Knapsack — `[≤k · capacity]`

Each item usable a **limited** number of times. Naive = expand into copies; efficient = binary-splitting (powers of 2) or monotonic-deque sliding window.

| # | Problem | Source | Technique |
|---|---------|--------|-----------|
| 66 | ⭐ [Knapsack 3](https://dmoj.ca/problem/knapsack) | DMOJ | bounded, deque / binary-split |
| 65 | [Knapsack 4](https://dmoj.ca/problem/knapsack4) | DMOJ | large-capacity bounded trick |
| 52 | [Knapsack](https://codeforces.com/problemset/problem/1132/E) | CF | few weight classes, high counts → multiple knapsack |

---

## D. Subset-Sum Feasibility — `[0/1 · feasibility]` (plus one counting-borderline)

Boolean 0/1 knapsack: "which totals are reachable using each item once?" Bitset-friendly. No value — only reachability.

| # | Problem | Source | Note |
|---|---------|--------|------|
| 13 | ⭐ [Money Sums](https://cses.fi/problemset/task/1745) | CSES | all reachable subset sums |
| 15 | [Two Sets II](https://cses.fi/problemset/task/1093) | CSES | counting-borderline from subset-sum backbone |
| 8 | [The Values You Can Make](https://codeforces.com/contest/687/problem/C) | CF | 2D: reachable (total, sub-amount) |
| 24 | [Colored Balls](https://codeforces.com/problemset/problem/1954/D) | CF | partition feasibility |
| 27 | [Arpa & Mehrdad's Hoses](https://codeforces.com/contest/742/problem/D) | CF | DSU groups → grouped subset-sum (also G) |
| 29 | [Modulo Sum](https://codeforces.com/contest/577/problem/B) | CF | reachable sums mod m (+ pigeonhole) |
| 70 | [Cloud Computing](https://oj.uz/problem/view/CEOI18_clo) | oj.uz | resource feasibility over sorted events |

---

## E. Counting Knapsack — `[· count]` (including borderline count DP)

DP counts **how many ways** to reach a sum (not just feasibility). Add-and-erase variants need modular inverse to "remove" an item online.

| # | Problem | Source | Note |
|---|---------|--------|------|
| 1 | ⭐ [Dice Combinations](https://cses.fi/problemset/task/1633) | CSES | `dp[n]=Σdp[n-k]` — ordered-count, the gateway |
| 39 | [#(subset sum=K) Add & Erase](https://atcoder.jp/contests/abc321/tasks/abc321_f) | AtCoder | online count; erase via modinv |
| 53 | [Unbearable Lightness of Weights](https://codeforces.com/contest/1078/problem/B) | CF | subset-sum count with item removal |
| 42 | [Cow Poetry](https://usaco.org/index.php?page=viewproblem2&cpid=897) | USACO | count knapsack over syllable budget |
| 20 | [Coins (dp_i)](https://atcoder.jp/contests/dp/tasks/dp_i) | AtCoder | probability knapsack (= weighted count) |
| 12 | [Counting Towers](https://cses.fi/problemset/task/2413) | CSES | counting DP (borderline — state-machine count) |

---

## F. Value-Indexed Knapsack (dual) — `[0/1 · value]`

When **capacity is huge (10^9) but total value is small**, you can't index by weight. Flip the axis: `dp[value] = min weight to achieve that value`, then take the largest value whose min weight ≤ capacity. The key "aha" of advanced basic-knapsack.

| # | Problem | Source | Why the flip |
|---|---------|--------|--------------|
| 45 | ⭐ [Knapsack 2 (dp_e)](https://atcoder.jp/contests/dp/tasks/dp_e) | AtCoder | W≤10^9, Σv≤10^5 → DP on value |
| 40 | [Talent Show](https://usaco.org/index.php?page=viewproblem2&cpid=839) | USACO | binary-search ratio + value knapsack |
| 25 | [Minimizing the Sum](https://codeforces.com/problemset/problem/1969/C) | CF | budget on #ops → knapsack indexed by ops |
| 35 | [Max Straight](https://atcoder.jp/contests/abc446/tasks/abc446_d) | AtCoder | value-oriented optimization |
| 75 | [Range Knapsack Query](https://atcoder.jp/contests/abc426/tasks/abc426_g) | AtCoder | value-indexed 0/1 under range queries (also H) |

---

## G. Grouped Knapsack — `[grouped · capacity]`

Items partitioned into groups; per group a constrained choice (pick ≤1, or pick a prefix, or a within-group sub-knapsack).

| # | Problem | Source | Group structure |
|---|---------|--------|-----------------|
| 54 | ⭐ [Porcelain](https://codeforces.com/contest/148/problem/E) | CF | each shelf = group; take prefix+suffix (inner knapsack per shelf) |
| 43 | [Exercise](https://usaco.org/index.php?page=viewproblem2&cpid=1043) | USACO | prime-cycle groups → group knapsack for LCM |
| 44 | [Maximal Orders of Permutations](https://szkopul.edu.pl/problemset/problem/lGqKS9urITMjTXhpdaHqyoEL/site/?key=statement) | Szkopuł | prime-power groups (pick one power per prime) |
| 27 | [Arpa & Mehrdad's Hoses](https://codeforces.com/contest/742/problem/D) | CF | friend-circles = groups (all-or-individuals) |

---

## H. Knapsack ⊕ Extra Structure

A knapsack core fused with a second technique: segment tree, tree DP, offline range queries, convex hull / divide-and-conquer.

| # | Problem | Source | Fusion |
|---|---------|--------|--------|
| 75 | [Range Knapsack Query](https://atcoder.jp/contests/abc426/tasks/abc426_g) | AtCoder | 0/1 knapsack + offline range queries (D&C on DP) |
| 72 | [Moorio Kart](https://usaco.org/index.php?page=viewproblem2&cpid=925) | USACO | tree DP + knapsack (count w/ factorials) |
| 59 | [Wi-Fi](https://codeforces.com/contest/1216/problem/F) | CF | DP + segment-tree range-min |
| 70 | [Cloud Computing](https://oj.uz/problem/view/CEOI18_clo) | oj.uz | event-sort + knapsack-over-resources |
| 58 | [Maximum Color Segment](https://codeforces.com/problemset/problem/2172/L) | CF | DP + segment reasoning |
| 33 | [Product Queries](https://codeforces.com/contest/2193/problem/E) | CF | DP + query structure |
| 73 | [Kocke](https://qoj.ac/problem/8116) | QOJ | heavy combined knapsack |
| 74 | [Sorting Pancakes](https://codeforces.com/contest/1675/problem/G) | CF | partition DP + knapsack-style transition |

---

## Not Knapsack — General DP Filed Under This Topic

These share the "basic DP" half of the topic but are **not** knapsack variants. Grouped by their actual DP shape so you don't mislabel them.

**Linear / sequence DP**
| # | Problem | Source | Shape |
|---|---------|--------|-------|
| 11 | [Array Description](https://cses.fi/problemset/task/1746) | CSES | `dp[i][v]`, neighbor constraint |
| 60 | [Fibonacci Paths](https://codeforces.com/contest/2176/problem/D) | CF | linear recurrence on path |
| 36 | [Block Sequence](https://codeforces.com/problemset/problem/1881/E) | CF | delete-or-jump backward DP |
| 64 | [Looking at Towers (easy)](https://codeforces.com/contest/2144/problem/E1) | CF | prefix-partition |
| 57 | [Pictures with Kittens (easy)](https://codeforces.com/contest/1077/problem/F1) | CF | pick-k with spacing (windowed DP) |
| 56 | [Yet Another Minimization](https://codeforces.com/contest/1637/problem/D) | CF | split-into-k cost DP |
| 62 | [Marble Council](https://codeforces.com/contest/2166/problem/D) | CF | partition DP |

**Grid / two-sequence DP**
| # | Problem | Source | Shape |
|---|---------|--------|-------|
| 9 | [Grid Paths](https://cses.fi/problemset/task/1638) | CSES | path count, blocked cells |
| 19 | [Grid 1 (dp_h)](https://atcoder.jp/contests/dp/tasks/dp_h) | AtCoder | twin of #9 |
| 69 | [Grid 2 (dp_y)](https://atcoder.jp/contests/dp/tasks/dp_y) | AtCoder | grid paths + inclusion-exclusion |
| 18 | [LCS (dp_f)](https://atcoder.jp/contests/dp/tasks/dp_f) | AtCoder | longest common subsequence |
| 26 | [The Least Round Way](https://codeforces.com/contest/2/problem/B) | CF | grid min-trailing-zeros |
| 34 | [Pizza Delivery](https://codeforces.com/contest/2193/problem/F) | CF | grid DP |
| 37 | [Minimal Grid Path](https://cses.fi/problemset/task/3359/) | CSES | lexicographically-min path |
| 71 | [Colorful Subsequence](https://atcoder.jp/contests/abc345/tasks/abc345_e) | AtCoder | subsequence DP |

**Interval / game DP**
| # | Problem | Source | Shape |
|---|---------|--------|-------|
| 14 | [Removal Game](https://cses.fi/problemset/task/1097) | CSES | ends-minimax |
| 47 | [Deque (dp_l)](https://atcoder.jp/contests/dp/tasks/dp_l) | AtCoder | ends-minimax twin |
| 46 | [Stones (dp_k)](https://atcoder.jp/contests/dp/tasks/dp_k) | AtCoder | game / grundy |
| 49 | [Slimes (dp_n)](https://atcoder.jp/contests/dp/tasks/dp_n) | AtCoder | interval merge-cost (matrix-chain) |
| 48 | [Candies (dp_m)](https://atcoder.jp/contests/dp/tasks/dp_m) | AtCoder | prefix-sum DP |

**State-machine / adjacent-choice DP**
| # | Problem | Source | Shape |
|---|---------|--------|-------|
| 17 | [Vacation (dp_c)](https://atcoder.jp/contests/dp/tasks/dp_c) | AtCoder | no-two-consecutive-same |
| 31 | [Vacations](https://codeforces.com/problemset/problem/698/A) | CF | rest/contest/gym adjacency |
| 4 | [Frog 1 (dp_a)](https://atcoder.jp/contests/dp/tasks/dp_a) | AtCoder | jump 1–2 |
| 5 | [Frog 2 (dp_b)](https://atcoder.jp/contests/dp/tasks/dp_b) | AtCoder | jump ≤k |
| 16 | [Fruit Feast](https://usaco.org/index.php?page=viewproblem2&cpid=574) | USACO | 2-state reachability |
| 22 | [Mortal Kombat Tower](https://codeforces.com/problemset/problem/1418/C) | CF | parity/skip |
| 28 | [New Rating](https://codeforces.com/contest/2029/problem/C) | CF | skip-interval |
| 61 | [Equalization](https://codeforces.com/problemset/problem/2075/D) | CF | factor-structured DP |
| 30 | [Interesting Binary (easy)](https://www.codechef.com/problems/P5BAR) | CodeChef | digit DP |
| 23 | [Where is the Ghost](https://toph.co/p/where-is-the-ghost) | Toph | DP + combinatorics |

---

## The Core Knapsack Decision Tree

```
Is each item limited?
├─ reusable ∞ times ................. UNBOUNDED (B)   loop capacity LOW→HIGH
├─ at most once ..................... 0/1              loop capacity HIGH→LOW
│   ├─ need max/min value .......... 0/1 knapsack (A)
│   ├─ only "reachable?" ........... subset-sum feasibility (D)
│   ├─ "how many ways?" ............ counting knapsack (E)
│   └─ capacity huge, value small .. VALUE-INDEXED dual (F)
├─ at most k times .................. BOUNDED (C)      binary-split / deque
└─ items come in groups ............. GROUPED (G)      inner choice per group
```

**Two reflexes to build:**
1. **Loop direction = multiplicity.** Backward capacity loop ⇒ each item once (0/1). Forward ⇒ reusable (unbounded). Memorize this; it's the #1 knapsack bug.
2. **Index the small axis.** If capacity ≫ total value, index the DP on *value* and minimize weight (F). If both small, index on capacity (A).

---

## Cross-Reference to This Repo

- CSES knapsack/coin problems → `problem_soulutions/` (Minimizing Coins, Coin Combinations I/II, Book Shop, Money Sums, Two Sets II, Dice Combinations).
- AtCoder DP contest knapsacks (dp_d, dp_e) → `problem_soulutions/dynamic_programming_at/`.
- General pattern theory → `pattern/DP.md`.

*Variant tags are by knapsack mechanics (item multiplicity × DP index). ~26 of the 75 are general DP the source filed under this topic for curriculum flow, not knapsack — kept in a clearly-labeled section so the real pattern stays clean. A few problems carry a secondary tag (e.g. #27 is both subset-sum and grouped; #75 is value-indexed and query-fused).*
