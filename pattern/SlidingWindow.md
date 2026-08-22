---
layout: simple
title: "Sliding Window Patterns"
permalink: /pattern/sliding-window
---

# Sliding Window Patterns — Comprehensive Guide

The sliding window turns an O(n²) scan over every subarray/substring into a single O(n) pass. The core idea: keep a **contiguous window** `[left, right]` over the array, extend `right` to include new elements, and shrink `left` only when the window breaks a constraint. Each element enters the window once and leaves at most once, so the whole scan is O(n) even though the window is constantly resizing.

This guide builds from the two window *shapes* (fixed and variable), then walks 9 LeetCode problems that plug into them.

---

## Quick Navigation: "I need to..."

| I need to... | Window shape | Section |
|--------------|--------------|---------|
| Best/sum of every window of **fixed size k** | Fixed | [3](#3-fixed-size-window) |
| **Max in each** window of size k | Fixed + monotonic deque | [8](#8-problem-239--sliding-window-maximum) |
| **Longest** substring/subarray under a constraint | Variable (grow, shrink when invalid) | [4](#4-variable-window--longest) |
| **Shortest** subarray meeting a target | Variable (shrink while still valid) | [5](#5-variable-window--shortest) |
| Count / match by **character frequency** | Variable + count map | [6](#6-frequency-window--anagrams--permutations) |
| Longest window with **≤ k exceptions** | Variable + violation counter | [9](#9-problem-424--longest-repeating-character-replacement) |

---

## Table of Contents

1. [The Core Idea: Why Windows Beat Nested Loops](#1-the-core-idea-why-windows-beat-nested-loops)
2. [The Two Window Shapes](#2-the-two-window-shapes)
3. [Fixed-Size Window](#3-fixed-size-window)
4. [Variable Window — Longest](#4-variable-window--longest)
5. [Variable Window — Shortest](#5-variable-window--shortest)
6. [Frequency Window — Anagrams & Permutations](#6-frequency-window--anagrams--permutations)
7. [The Universal Variable-Window Template](#7-the-universal-variable-window-template)
8. [Problem 239 — Sliding Window Maximum](#8-problem-239--sliding-window-maximum)
9. [Problem 424 — Longest Repeating Character Replacement](#9-problem-424--longest-repeating-character-replacement)
10. [Master Comparison Table](#10-master-comparison-table)
11. [How to Identify This Pattern](#11-how-to-identify-this-pattern)
12. [Practice Order](#12-practice-order)

---

## 1. The Core Idea: Why Windows Beat Nested Loops

The brute force for "best subarray of length k" recomputes each window from scratch:

```
nums = [1, 3, -1, -3, 5], k = 3

Brute force: for each start i, sum nums[i..i+k-1]
  i=0: 1 + 3 + (-1) = 3      ← re-adds 3 and -1
  i=1: 3 + (-1) + (-3) = -1  ← re-adds -1 and -3
  i=2: (-1) + (-3) + 5 = 1

Every element is touched k times → O(n·k)
```

The window insight: consecutive windows **overlap almost entirely**. Sliding from `[i..i+k-1]` to `[i+1..i+k]` only removes one element and adds one:

```
window sum: 3
slide →  add nums[3]=-3, drop nums[0]=1  → 3 - 1 + (-3) = -1
slide →  add nums[4]=5,  drop nums[1]=3  → -1 - 3 + 5 = 1
```

Each element is added once and removed once → **O(n)**.

`★ Insight ─────────────────────────────────────`
- The window is a *summary* you maintain incrementally. Recomputing it from scratch each step throws away the overlap — that's the whole cost you're eliminating.
- Sliding window only works when the answer for a window can be **updated in O(1)** from the neighbor (add one, drop one). If updating needs a full rescan, you gain nothing — reach for a different structure (see §8's deque).
`─────────────────────────────────────────────────`

---

## 2. The Two Window Shapes

```
FIXED window                          VARIABLE window
size k never changes                  size grows and shrinks

[■ ■ ■] · · ·                          [■] · · · · ·
· [■ ■ ■] · ·        right always      [■ ■] · · · ·     right always advances;
· · [■ ■ ■] ·        advances by 1;    [■ ■ ■] · · ·     left advances ONLY when
· · · [■ ■ ■]        left follows       [■ ■] · · · ·    a constraint is violated
                     k behind
```

- **Fixed**: `left` and `right` move in lockstep, exactly `k` apart. Use when the problem *names* a size ("window of size k", "every k consecutive").
- **Variable**: `right` marches forward always; `left` jumps in only to restore validity. Use when the problem asks for the **longest / shortest** window satisfying a condition.

Almost every "substring / subarray with property X" problem is a variable window. That's the workhorse — master §7's template and most of these problems collapse to filling in three blanks.

---

## 3. Fixed-Size Window

**Problem (LC 643 style)**: maximum average of any contiguous subarray of length `k`.

```python
def max_sum_fixed(nums, k):
    window = sum(nums[:k])   # first window
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]  # add new, drop old
        best = max(best, window)
    return best
```

```
nums = [1, 12, -5, -6, 50, 3], k = 4

first window [1,12,-5,-6]        sum = 2
right=4: +50 -1  → [12,-5,-6,50] sum = 51
right=5: +3 -12  → [-5,-6,50,3]  sum = 42

best = 51
```

The `nums[right] - nums[right - k]` line is the entire trick: `right - k` is the element leaving on the left as `right` enters on the right.

---

## 4. Variable Window — Longest

**Problem (LC 3)**: longest substring **without repeating characters**.

Grow `right`. The moment a duplicate appears, shrink `left` until the window is valid again.

```python
def length_of_longest_substring(s):
    seen = {}          # char → last index seen
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1   # jump left past the duplicate
        seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

```
s = "abcabcbb"

right=0 'a'  window "a"      best=1
right=1 'b'  window "ab"     best=2
right=2 'c'  window "abc"    best=3
right=3 'a'  dup! left→1     window "bca"   best=3
right=4 'b'  dup! left→2     window "cab"   best=3
right=5 'c'  dup! left→3     window "abc"   best=3
right=6 'b'  dup! left→5     window "cb"
right=7 'b'  dup! left→7     window "b"

best = 3  ("abc")
```

`★ Insight ─────────────────────────────────────`
- The guard `seen[ch] >= left` matters: a duplicate *outside* the current window (to the left of `left`) is stale and must not drag `left` backward. Windows only ever grow from the left — `left` is monotonic non-decreasing.
- "Longest valid" windows shrink **just enough** to become valid, then immediately try to grow again. Contrast with "shortest" (§5), which shrinks **as much as possible** while staying valid.
`─────────────────────────────────────────────────`

---

## 5. Variable Window — Shortest

**Problem (LC 209)**: smallest length of a contiguous subarray with `sum >= target` (positive nums).

Grow `right` to reach the target, then shrink `left` greedily while the sum stays `>= target`.

```python
def min_subarray_len(target, nums):
    left = 0
    window = 0
    best = float('inf')
    for right, x in enumerate(nums):
        window += x
        while window >= target:          # shrink while STILL valid
            best = min(best, right - left + 1)
            window -= nums[left]
            left += 1
    return best if best != float('inf') else 0
```

```
target = 7, nums = [2,3,1,2,4,3]

right=0 win=2
right=1 win=5
right=2 win=6
right=3 win=8 ≥7 → record len 4 [2,3,1,2], shrink win=6 left=1
right=4 win=10≥7 → record len 4 [3,1,2,4], shrink win=7 left=2
                   win=7 ≥7 → record len 3 [1,2,4],   shrink win=6 left=3
right=5 win=9 ≥7 → record len 3 [2,4,3],   shrink win=7 left=4
                   win=7 ≥7 → record len 2 [4,3],     shrink win=3 left=5

best = 2  (subarray [4,3])
```

> **Why this needs non-negative numbers.** Growing `right` monotonically increases the sum, and shrinking `left` monotonically decreases it — that monotonicity is what lets `left` never backtrack. With negatives, adding an element can *decrease* the sum, so the window is no longer monotonic and a plain sliding window breaks. For arrays with negatives, use **prefix sum + monotonic deque** (see the [Prefix Sum guide](/pattern/prefix-sum)).

---

## 6. Frequency Window — Anagrams & Permutations

**Problem (LC 438)**: find all start indices of anagrams of `p` in `s`.

A fixed window of size `len(p)`, but validity is checked by **frequency match**, not a scalar. Track how many characters currently have the *correct* count.

```python
from collections import Counter

def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    need = Counter(p)
    window = Counter()
    k = len(p)
    result = []
    for right, ch in enumerate(s):
        window[ch] += 1
        if right >= k:                    # drop the element leaving on the left
            left_ch = s[right - k]
            window[left_ch] -= 1
            if window[left_ch] == 0:
                del window[left_ch]
        if window == need:                # exact frequency match
            result.append(right - k + 1)
    return result
```

```
s = "cbaebabacd", p = "abc"  (need = {a:1,b:1,c:1}), k=3
index:  c0 b1 a2 e3 b4 a5 b6 a7 c8 d9

right=2 window {c,b,a}  == need → append 2-3+1 = 0
right=3 add e, drop c   {b,a,e} ✗
right=4 add b, drop b   {a,e,b} ✗
...
right=8 add c, drop a   {b,a,c} == need → append 8-3+1 = 6

result = [0, 6]
```

Comparing two `Counter`s each step is O(26) = O(1) for lowercase letters. LC 567 (permutation-in-string) is the same window — return `True` on first match instead of collecting all.

---

## 7. The Universal Variable-Window Template

Nearly every variable-window problem fits this skeleton. You fill in three blanks: **what state the window tracks**, **when it's invalid**, and **what you record**.

```python
def sliding_window(s):
    state = {}          # window contents (count map, sum, etc.)
    left = 0
    answer = 0

    for right in range(len(s)):
        # 1. EXPAND: add s[right] to state
        add(state, s[right])

        # 2. SHRINK: while window violates the constraint, remove s[left]
        while is_invalid(state):
            remove(state, s[left])
            left += 1

        # 3. RECORD: window [left..right] is now valid
        answer = max(answer, right - left + 1)

    return answer
```

| Blank | "Longest without repeats" | "Longest with ≤ k distinct" | "Min sum ≥ target" |
|-------|---------------------------|-----------------------------|--------------------|
| `state` | char count map | char count map | running sum |
| `is_invalid` | any count > 1 | `len(map) > k` | (invert: shrink while **valid**) |
| `record` | `right-left+1` on each step | `right-left+1` on each step | `right-left+1` inside shrink loop |

`★ Insight ─────────────────────────────────────`
- **Longest** problems record *after* the shrink loop (window is maximal-valid). **Shortest** problems record *inside* the shrink loop (each shrink is a candidate minimum). Getting this placement wrong is the #1 sliding-window bug.
- `is_invalid` should test a condition that only becomes true by *adding* and only becomes false by *removing*. If your condition can flip both ways on an add, a monotonic window won't work.
`─────────────────────────────────────────────────`

---

## 8. Problem 239 — Sliding Window Maximum

**Difficulty**: Hard

> Return the maximum of every fixed window of size `k`.

Naively rescanning each window is O(n·k). A running max doesn't work — when the current max *leaves* the window, you'd have to rescan to find the next one. The fix: a **monotonic decreasing deque** holding indices whose values could still become a window max.

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()        # indices, values decreasing front→back
    result = []
    for right, x in enumerate(nums):
        # drop indices that fell out of the window on the left
        if dq and dq[0] <= right - k:
            dq.popleft()
        # drop smaller values from the back — they can never be the max
        # while x is in the window
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(right)
        if right >= k - 1:
            result.append(nums[dq[0]])   # front = window max
    return result
```

```
nums = [1,3,-1,-3,5,3,6,7], k = 3

right=0 dq=[0]                      (val 1)
right=1 3≥1 pop 0, dq=[1]           (val 3)
right=2 dq=[1,2]                    → max nums[1]=3
right=3 dq=[1,2,3]                  → max 3
right=4 5 pops 3,2,1; expire? dq=[4] → max 5
right=5 dq=[4,5]                    → max 5
right=6 6 pops 5,4; dq=[6]          → max 6
right=7 dq=[6,7]                    → max 7

result = [3,3,5,5,6,7]
```

`★ Insight ─────────────────────────────────────`
- The deque is the window's max — but stored so the *runner-up* is already waiting behind the front. When the max expires, the next-largest is instantly at the front. That's why we can afford O(1) amortized instead of rescanning.
- Each index is pushed once and popped once, so despite the inner `while`, the total work is O(n). This "monotonic deque" is the bridge between sliding window and the [Stack & Queue guide](/pattern/stack-queue).
`─────────────────────────────────────────────────`

---

## 9. Problem 424 — Longest Repeating Character Replacement

**Difficulty**: Medium

> Longest substring where you may replace at most `k` characters so all chars become the same.

A window is valid when `(window length) - (count of the most frequent char) <= k` — i.e. the non-majority chars, which are what you'd replace, number at most `k`.

```python
from collections import defaultdict

def character_replacement(s, k):
    count = defaultdict(int)
    left = 0
    max_freq = 0        # highest single-char count seen in the window
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        # replacements needed = window size - most common char count
        if (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

```
s = "AABABBA", k = 1

right=0 A count{A:1} maxf=1 win"A"    best=1
right=1 A {A:2} maxf=2 win"AA"        best=2
right=2 B {A:2,B:1} maxf=2 need 1 ok  best=3 "AAB"
right=3 A {A:3,B:1} maxf=3 win"AABA"  need 4-3=1 ok  best=4
right=4 B {A:3,B:2} maxf=3 need 5-3=2>1 → shrink left→1  win"ABAB"
right=5 B {A:2,B:3} maxf=3 need 5-3=2>1 → shrink left→2  win"BABB"
right=6 A stale maxf=3 need 5-3=2>1 → shrink left→3       best stays 4

best = 4
```

> **The subtle bit**: `max_freq` is never decreased when the window shrinks. That looks like a bug but isn't — the answer `best` can only grow when a *larger* window is valid, which requires a `max_freq` at least as high as the stale one. Keeping the stale value never produces a wrong-larger answer, and it keeps the loop O(n) instead of O(26n). This is a well-known, deliberate trick.

---

## 10. Master Comparison Table

| Problem | Shape | Window state | Shrink condition | Record |
|---------|-------|--------------|------------------|--------|
| **643** Max avg | Fixed k | running sum | (lockstep) | each step |
| **3** No repeats | Variable longest | last-seen index | duplicate in window | after shrink |
| **209** Min sum ≥ target | Variable shortest | running sum | while `sum ≥ target` | inside shrink |
| **340** ≤ k distinct | Variable longest | char count map | `len(map) > k` | after shrink |
| **438 / 567** Anagram | Fixed \|p\| | char count map | (fixed size) | on frequency match |
| **239** Window max | Fixed k | monotonic deque | index expired | front of deque |
| **424** Char replace | Variable longest | char count + max_freq | `len - max_freq > k` | after shrink |
| **904** Fruit baskets | Variable longest | ≤ 2 distinct | `len(map) > 2` | after shrink |
| **1004** Max ones (flip k) | Variable longest | zero count | `zeros > k` | after shrink |

### What stays the same

```
1. right marches forward, one step per iteration
2. update window state with the entering element
3. restore validity by moving left (never backward)
4. record the answer at the right moment
```

### What changes

Only three things: the **state** you track, the **invalid** test, and **when** you record. Everything else is boilerplate.

---

## 11. How to Identify This Pattern

### Trigger: contiguous subarray/substring + optimize or count

```
See "contiguous subarray" or "substring" + one of:
  ├── "of size k" / "every k consecutive"   → FIXED window (§3)
  ├── "longest ... such that <constraint>"  → VARIABLE longest (§4, §7)
  ├── "shortest / minimum ... at least X"   → VARIABLE shortest (§5)
  ├── "maximum in each window"              → FIXED + monotonic deque (§8)
  └── "matches a frequency / anagram"       → FREQUENCY window (§6)
```

### Sliding window vs. the alternatives

| If... | Use |
|-------|-----|
| Window updates in O(1) (add one / drop one), values non-negative | **Sliding window** |
| Array has **negative** numbers and you need sum constraints | **Prefix sum + hash/deque** ([guide](/pattern/prefix-sum)) |
| Two indices move but **not** as a resizing window (e.g. sorted pair-sum) | **Two Pointers** ([guide](/pattern/two-pointers)) |
| Need max/min of window but not contiguous | **Heap** ([guide](/pattern/heap)) |

`★ Insight ─────────────────────────────────────`
- Sliding window is a *special case* of two pointers where both pointers only move forward and the region between them is the object of interest. Two pointers is broader (pointers may move toward each other, or over two arrays). If the window resizes based on a running constraint, it's sliding window; if the pointers converge on a sorted structure, it's two pointers.
`─────────────────────────────────────────────────`

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Recording answer in wrong place | Longest → after shrink loop; shortest → inside shrink loop |
| `left` moving backward | It must be monotonic; guard stale duplicates with `seen[ch] >= left` |
| Using sliding window with negatives | Doesn't work for sum constraints — switch to prefix sum |
| Off-by-one on window size | Size = `right - left + 1`; fixed window drops `nums[right - k]` |
| Rescanning the window for max | Use a monotonic deque (§8), not `max(window)` each step |

---

## 12. Practice Order

```
Start here
    │
    ▼
  643 (Easy)   ──── Fixed window: the add-one/drop-one mechanic
    │
    ▼
   3 (Medium)  ──── Variable longest: shrink on duplicate
    │
    ▼
  209 (Medium) ──── Variable shortest: shrink while valid
    │
    ▼
  438 (Medium) ──── Frequency window: Counter equality
    │
    ▼
  424 (Medium) ──── Longest with ≤ k violations (the max_freq trick)
    │
    ▼
  239 (Hard)   ──── Monotonic deque for window max
```

---

*Pattern mastered — one pointer marches, the other follows only to keep the window honest.*
