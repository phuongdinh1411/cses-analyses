---
layout: simple
title: "Pattern Mastery Program"
permalink: /pattern/mastery
---

# Pattern Mastery Program

The 18 technique guides in this folder are reference material. Reading them produces
*recognition* — the comfortable feeling of "yes, I've seen this" — which is not the same thing as
being able to write the code cold in an interview. This page is the other half: a schedule, a
per-pattern checklist with an explicit definition of "done", and drill formats that force
**recall** instead of recognition.

Start with the [Decision Map](/pattern/decision-map) if you have not read it. Routing is the skill
that actually gets tested, and it is the one most people skip.

---

## The Three Levels of Knowing a Pattern

Be honest about which level you are at, per pattern. Most people overestimate by one.

| Level | What it means | How you test it |
|-------|---------------|-----------------|
| **L1 — Recognise** | Shown the technique's name, you can explain what it does and when it applies | Read the guide's Quick Navigation table and explain each row without scrolling |
| **L2 — Recall** | Given a problem you have never seen, you can *name* the right technique and sketch the state/invariant | The Self-Test blocks; cold routing drills (§4) |
| **L3 — Reproduce** | You can write a correct, complete implementation from an empty file, with no reference, in under 15 minutes | Blank-page drills (§4) |

**L3 on the 8 core patterns beats L1 on all 18.** Depth is what survives interview pressure;
breadth without depth collapses the moment you have to actually type.

The core eight, in order of interview frequency:
[Two Pointers](/pattern/two-pointers), [Sliding Window](/pattern/sliding-window),
[Binary Search](/pattern/binary-search), [Prefix Sum](/pattern/prefix-sum),
[Stack & Queue](/pattern/stack-queue), [Heap](/pattern/heap), [DP](/pattern/dp),
[Graph](/pattern/graph).

---

## 1. Spaced Repetition Schedule

Spacing works because retrieval difficulty is what builds durable memory. Reviewing something you
still remember perfectly teaches you almost nothing; reviewing it right as it starts to fade is
where the learning happens.

The intervals, per pattern, counted from the day you first complete it:

```
Day 0    ── First pass: read the guide, write every template once by hand
Day 1    ── Self-Test only. No rereading first. Note which questions you miss.
Day 3    ── Blank-page drill: reproduce the core template from an empty file
Day 7    ── Solve 2 unseen problems from the guide's Practice Ladder
Day 14   ── Self-Test again + 1 hard problem
Day 30   ── Mixed routing drill (this pattern hidden among others)
Day 90   ── Blank-page drill again. If it still lands, the pattern is yours.
```

**The rule that makes this work:** attempt retrieval *before* reviewing. Opening the guide first
converts a hard, valuable recall attempt into cheap, worthless recognition. Sit with the blank
page even when it is uncomfortable — especially then.

**If you miss a question on Day N,** reset that pattern to Day 0 for that specific topic only, not
the whole guide. Missing the digit-DP `tight` question does not mean rereading all of DP.

### An 8-Week Cycle Over All 18 Guides

Two guides a week, with review days folded in. Adjust the pace, keep the structure.

| Week | New guides | Reviews due |
|------|-----------|-------------|
| 1 | [Two Pointers](/pattern/two-pointers), [Sliding Window](/pattern/sliding-window) | — |
| 2 | [Prefix Sum](/pattern/prefix-sum), [Binary Search](/pattern/binary-search) | Week 1 (Day 7) |
| 3 | [Stack & Queue](/pattern/stack-queue), [Heap](/pattern/heap) | Week 1 (Day 14), Week 2 (Day 7) |
| 4 | [DP](/pattern/dp) — spend the whole week here | Week 2 (Day 14), Week 3 (Day 7) |
| 5 | [Graph](/pattern/graph), [Tree](/pattern/tree) | Week 3 (Day 14), Week 4 (Day 7) |
| 6 | [Backtracking](/pattern/backtracking), [Bitmask](/pattern/bitmask), [Bitmask DP](/pattern/bitmask-dp-subset-partition) | Week 4 (Day 14), Week 5 (Day 7) |
| 7 | [Segment Tree](/pattern/segment-tree), [Fenwick Tree](/pattern/fenwick-tree), [Contribution Counting](/pattern/contribution-counting) | Week 5 (Day 14), Week 6 (Day 7) |
| 8 | [LCA](/pattern/lca), [Edge Contribution](/pattern/edge-contribution), [Digit DP](/pattern/digit-dp) | Week 6 (Day 14), Week 7 (Day 7), full [Decision Map](/pattern/decision-map) drill |

Week 4 is deliberately one guide. [DP](/pattern/dp) has 14 families and is the most common source
of interview failure; treating it as one week's worth of one pattern is the mistake.

---

## 2. Per-Pattern Mastery Checklist

For each pattern, "mastered" means all four boxes, not three. The **Reproduce cold** column is the
one that decides it — and it is the one everyone skips.

Copy this table and keep your own marks. `R` = recognise, `A` = answered the Self-Test cold,
`C` = reproduced from a blank page, `P` = solved the ladder's hard problem unaided.

| Pattern | The one invariant you must be able to state | Blank-page target (< 15 min) | R | A | C | P |
|---------|--------------------------------------------|------------------------------|---|---|---|---|
| [Two Pointers](/pattern/two-pointers) | One comparison rules out a whole row or column of the pair space | `three_sum` with duplicate skipping | ☐ | ☐ | ☐ | ☐ |
| [Sliding Window](/pattern/sliding-window) | Shrinking a valid window keeps it valid (monotone validity) | `min_window` (LC 76) with the `have`/`need` counter | ☐ | ☐ | ☐ | ☐ |
| [Prefix Sum](/pattern/prefix-sum) | `range = prefix(r) − prefix(l−1)`; needs an invertible op | Count subarrays summing to `k`, hash-map variant | ☐ | ☐ | ☐ | ☐ |
| [Binary Search](/pattern/binary-search) | The predicate is monotone: F…FT…T with one boundary | `lower_bound`, `upper_bound`, and one search-on-answer | ☐ | ☐ | ☐ | ☐ |
| [Stack & Queue](/pattern/stack-queue) | Each index is pushed once and popped once → amortized O(1) | `largest_rectangle_in_histogram` with the sentinel | ☐ | ☐ | ☐ | ☐ |
| [Heap](/pattern/heap) | Parent ≤ children, and nothing else is promised | Two-heap streaming median (LC 295) | ☐ | ☐ | ☐ | ☐ |
| [DP](/pattern/dp) | State must fully determine the future | 0/1 knapsack, LIS in O(n log n), one interval DP | ☐ | ☐ | ☐ | ☐ |
| [Graph](/pattern/graph) | Each algorithm's precondition (weights, acyclicity, direction) | Dijkstra with the stale-entry skip; Kahn's with the cycle check | ☐ | ☐ | ☐ | ☐ |
| [Tree](/pattern/tree) | Exactly one simple path between any two nodes | `tin`/`tout` flatten + subtree-sum query | ☐ | ☐ | ☐ | ☐ |
| [Backtracking](/pattern/backtracking) | Every mutation down needs an exact undo up | Permutations *with duplicates*, correctly deduplicated | ☐ | ☐ | ☐ | ☐ |
| [Bitmask](/pattern/bitmask) | A mask is membership only — order needs a second dimension | Submask enumeration + `popcount` loop | ☐ | ☐ | ☐ | ☐ |
| [Bitmask DP](/pattern/bitmask-dp-subset-partition) | Peel one complete group per step; O(3ⁿ) | LC 698 peel-off with lowest-bit canonicalisation | ☐ | ☐ | ☐ | ☐ |
| [Segment Tree](/pattern/segment-tree) | Merge must be associative with an identity | Build / point-update / range-query, no lazy | ☐ | ☐ | ☐ | ☐ |
| [Fenwick Tree](/pattern/fenwick-tree) | `i & -i` is the responsibility range; 1-indexed only | `update` + `query` + inversion counting | ☐ | ☐ | ☐ | ☐ |
| [Contribution Counting](/pattern/contribution-counting) | Swap the summation order; needs independent per-unit terms | Sum of subarray minimums, tie-breaks correct | ☐ | ☐ | ☐ | ☐ |
| [LCA](/pattern/lca) | `up[k][v] = up[k−1][up[k−1][v]]`, built level by level | Binary lifting: build + query + `dist` | ☐ | ☐ | ☐ | ☐ |
| [Edge Contribution](/pattern/edge-contribution) | Removing a tree edge splits it into exactly two parts | `Σ size[v] × (n − size[v])` in one DFS | ☐ | ☐ | ☐ | ☐ |
| [Digit DP](/pattern/digit-dp) | `tight` belongs in the memo key | `count(X)` with `pos`/`tight`/`started` | ☐ | ☐ | ☐ | ☐ |

If you can state the invariant column from memory for all 18 rows, your routing is in good shape
even where your implementations are not. That is the more valuable half.

---

## 3. Diagnosing Where You Actually Are

Different failures need different fixes. Match the symptom, not the mood.

| Symptom | What it means | The fix |
|---------|---------------|---------|
| "I read the solution and it made total sense" | L1 recognition only | Close it. Reproduce from a blank page. This is the single most common self-deception in interview prep. |
| "I knew it was DP but couldn't define the state" | Routing works, formulation does not | Drill format B (§4): state-only, no code. Ten problems in half an hour. |
| "I had the right idea but the code had bugs" | L2 not L3 | Blank-page drills. Type the template until the loop bounds are muscle memory. |
| "I had no idea where to start" | Routing gap | The [Decision Map](/pattern/decision-map) Self-Test, then drill format A. |
| "I solved it but way over time" | Formulation is slow, not absent | Time-box the *routing* step to 2 minutes and force a commitment. |
| "I get it in isolation but not mixed in" | Pattern-matched to context, not to the problem | Drill format D (§4): shuffled problems with no pattern label. |
| "Correct on samples, failed hidden tests" | Edge cases | Work the "When This Fails" section of the relevant guide, then re-solve. |

---

## 4. Drill Formats

### A. Cold routing (5 minutes, highest value per minute)

Take a problem you have never seen. Read *only* the statement and constraints. Before writing any
code, answer out loud:

1. Which family? (input shape + the ask)
2. Which specific technique inside it? (constraint size breaks ties)
3. What is the state or the invariant, in one sentence?
4. What is the complexity, and does it fit the constraints?

Then stop and check against the guide. **Do not solve it.** You are training routing in isolation,
which is the step that determines whether the other 40 minutes are even spent on the right thing.

Ten of these is worth more than one full solve, and takes less time.

### B. State-only drill (formulation without code)

For ten DP problems in a row, write *only*:

```
dp[...] = <one sentence: what this cell means>
transition: <the recurrence>
base:      <the base cases>
answer:    <which cell>
order:     <the iteration order that makes dependencies ready>
```

No implementation. Most DP failure is formulation failure, and mixing in the typing hides which
one you are actually bad at.

### C. Blank-page reproduction (the L3 test)

Empty file. No guide, no autocomplete, no internet. Write the template from the checklist for one
pattern. Then diff against the guide and — this is the part that matters — **write down each
difference and why yours was wrong**. A diff you do not explain teaches you nothing.

Target: under 15 minutes, compiles and runs, correct on the guide's traced example.

### D. Interleaved practice (do this once you have 5+ patterns)

Take twenty problems across five patterns, shuffle them, strip the labels, and solve in random
order. Blocked practice (twenty sliding-window problems in a row) makes you feel fast because the
context does the routing for you. Interleaved practice feels worse and transfers far better — and
an interview is interleaved by definition.

### E. Explain-it-back (the fastest gap detector)

Explain a pattern out loud to an imaginary interviewer, in under three minutes, covering: what
problem it solves, why the naive approach wastes work, the invariant, the complexity, and one
case where it fails. Every place you hedge or trail off is a genuine gap. This is faster than any
written test at finding them.

---

## 5. The 40 Problems That Cover Everything

If you only have time for a fixed list, this is the one. Every entry is the *canonical* instance
of a technique, so the set has near-zero redundancy.

**Two Pointers / Sliding Window (8)**: LC 167, 15, 11, 42, 3, 76, 424, 992
**Binary Search / Prefix Sum (6)**: LC 704, 33, 410, 1011, 560, 304
**Stack / Heap (6)**: LC 739, 84, 239, 215, 23, 295
**DP (8)**: LC 322, 416, 300, 1143, 312, 337, 233, 847
**Graph / Tree (7)**: LC 200, 743, 207, 1192, 236, 543, 834
**Bitmask / Backtracking (5)**: LC 78, 46, 51, 698, 1986

Work them in the order listed inside each group — each builds on the one before. Mark them with
the same R/A/C/P scheme as the checklist.

---

## 6. Common Ways This Goes Wrong

- **Reading more guides instead of drilling fewer.** New material feels productive and is the
  easiest way to avoid the discomfort of retrieval. If you have not blank-paged a pattern, do not
  start another one.
- **Reviewing while the memory is still fresh.** Zero difficulty, zero benefit. The whole point of
  spacing is to review at the edge of forgetting.
- **Checking the answer too early.** The thirty seconds of not-knowing is where the learning
  happens. Sit in it.
- **Blocked practice only.** Twenty problems of one pattern trains the pattern; it does not train
  choosing it, and choosing is what the interview tests.
- **Skipping the failure modes.** Knowing when a technique *does not* apply is most of what
  separates L2 from L3, and it is exactly what a good interviewer probes.
- **Chasing breadth before depth.** Eighteen patterns at L1 loses to eight at L3, every time.

---

## See Also

- [Pattern Decision Map](/pattern/decision-map) — the router. Drill this more than any single technique guide.
- Each guide's `## Self-Test` block — the Day 1 and Day 14 review material.
- Each guide's `## When This Fails` note — the L2-to-L3 material.

---

*Mastery is not more reading. It is retrieval under difficulty, spaced out over time, with the
blank page as the only honest judge.*
