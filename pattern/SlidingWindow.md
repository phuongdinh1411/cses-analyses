---
layout: simple
title: "Sliding Window Patterns"
permalink: /pattern/sliding-window
---

# Sliding Window Patterns — Comprehensive Guide

The sliding window turns an O(n²) scan over every subarray/substring into a single O(n) pass. The core idea: keep a **contiguous window** `[left, right]` over the array, extend `right` to include new elements, and shrink `left` only when the window breaks a constraint. Each element enters the window once and leaves at most once, so the whole scan is O(n) even though the window is constantly resizing.

This guide builds from the two window *shapes* (fixed and variable), then walks 13 LeetCode problems that plug into them.

---

## From-Scratch Idea: What Makes a Problem Sliding Window

Take the brute force for "longest substring with at most 2 distinct characters":

```python
best = 0
for i in range(n):
    for j in range(i, n):
        if distinct(s[i:j+1]) <= 2:
            best = max(best, j - i + 1)
```

O(n²) windows, each costing O(n) to check — O(n³) total. Now notice two things the brute force
throws away every iteration:

1. **The window `[i, j+1]` is the window `[i, j]` plus one character.** Recomputing `distinct`
   from scratch discards everything you learned one step ago. Maintain a running count map and
   each extension is O(1).
2. **If `[i, j]` is already invalid, every longer window starting at `i` is also invalid.** So the
   inner loop should stop, not keep going — and more than that, when you advance `i`, the new
   `j` never has to restart from `i`. It can resume where it was.

That second point is the real theorem, and it needs one property to hold:

> **Shrinking a window can never turn a valid window invalid** (equivalently: validity is
> inherited by sub-windows). Call this *monotone validity*.

With monotone validity, `left` never needs to move backwards. Both pointers only ever advance, so
across the whole run they take at most `2n` steps total — O(n), no matter how much the window
resizes in between.

### The two questions that identify it

1. **Is the answer a contiguous region?** A subarray or substring, not a subsequence and not a
   pair. Non-contiguous → this is not your pattern.
2. **Is validity monotone?** Does removing an element from a valid window keep it valid? "At most
   k distinct" — yes. "Sum ≥ target with all-positive numbers" — yes. "Sum ≥ target **with
   negatives**" — **no**, and §13 shows what to do instead.

### Where it breaks, and the two escapes

| The constraint | Monotone? | What to do |
|---|---|---|
| "at most k ..." | Yes | Plain window |
| "sum ≥ target", all non-negative | Yes | Plain window (§5) |
| "sum ≥ target", **negatives present** | **No** | Prefix sums + monotonic deque (§13) |
| "**exactly** k distinct" | **No** | `atMost(k) − atMost(k−1)` (§12) |
| "maximum in every window" | N/A — not a validity question | Monotonic deque (§8) |

Both escapes are worth knowing cold: they turn "sliding window does not apply" back into "sliding
window applies twice" or "sliding window on a different axis."

---

## Master LeetCode Comparison Table

| LC # | Title | Diff | Shape | What the window tracks | Cost |
|------|-------|------|-------|------------------------|------|
| **643** | Maximum Average Subarray I | Easy | Fixed size `k` | running sum | O(n) / O(1) |
| **3** | Longest Substring Without Repeating | Medium | Variable, longest | last-seen index per char | O(n) / O(Σ) |
| **209** | Minimum Size Subarray Sum | Medium | Variable, shortest | running sum (all positive) | O(n) / O(1) |
| **438** | Find All Anagrams in a String | Medium | Fixed + freq map | character counts vs target | O(n) / O(Σ) |
| **567** | Permutation in String | Medium | Fixed + freq map | same as 438, boolean answer | O(n) / O(Σ) |
| **424** | Longest Repeating Char Replacement | Medium | Variable + violation count | `windowLen − maxFreq ≤ k` | O(n) / O(Σ) |
| **1004** | Max Consecutive Ones III | Medium | Variable + violation count | number of zeros flipped | O(n) / O(1) |
| **239** | Sliding Window Maximum | Hard | Fixed + monotonic deque | indices in decreasing value order | O(n) / O(k) |
| **340** | Longest Substring with At Most K Distinct | Medium | Variable, longest | `len(count) ≤ k` | O(n) / O(k) |
| **76** | Minimum Window Substring | Hard | Variable, shortest | `have == need` quota counter | O(n) / O(Σ) |
| **992** | Subarrays with K Different Integers | Hard | Two windows | `atMost(k) − atMost(k−1)` | O(n) / O(k) |
| **862** | Shortest Subarray with Sum ≥ K | Hard | Prefix sums + deque | monotone prefix candidates | O(n) / O(n) |

The **Shape** column is the one to internalise. Only four things ever appear there: fixed size,
variable-longest, variable-shortest, and "not really a window — a deque over a derived array".

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
| **Shortest** window covering all of a target multiset | Variable + quota counter | [10](#10-problem-76--minimum-window-substring) |
| Longest window with **at most k distinct** | Variable + count map | [11](#11-problem-340--longest-substring-with-at-most-k-distinct-characters) |
| **Count** subarrays with **exactly** k distinct | Two `atMost` windows | [12](#12-counting-exactly-k-the-atmost-reduction) |
| Shortest subarray with sum ≥ k, **negatives allowed** | Prefix sums + deque | [13](#13-problem-862--shortest-subarray-with-sum-at-least-k-negatives-allowed) |

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
10. [Problem 76 — Minimum Window Substring](#10-problem-76--minimum-window-substring)
11. [Problem 340 — Longest Substring with At Most K Distinct Characters](#11-problem-340--longest-substring-with-at-most-k-distinct-characters)
12. [Counting Exactly K: the `atMost` Reduction](#12-counting-exactly-k-the-atmost-reduction)
13. [Problem 862 — Shortest Subarray with Sum at Least K](#13-problem-862--shortest-subarray-with-sum-at-least-k-negatives-allowed)
14. [Master Comparison Table](#14-master-comparison-table)
15. [How to Identify This Pattern](#15-how-to-identify-this-pattern)
16. [Practice Order](#16-practice-order)
17. [Pattern Recognition Cheat Sheet](#17-pattern-recognition-cheat-sheet)

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

> **Why this needs non-negative numbers.** Growing `right` monotonically increases the sum, and shrinking `left` monotonically decreases it — that monotonicity is what lets `left` never backtrack. With negatives, adding an element can *decrease* the sum, so the window is no longer monotonic and a plain sliding window breaks. For arrays with negatives you need **prefix sum + monotonic deque**, which is exactly what [§13 (LC 862)](#13-problem-862--shortest-subarray-with-sum-at-least-k-negatives-allowed) below builds — read this section first, then go see how the assumption gets repaired.

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

## 10. Problem 76 — Minimum Window Substring

> Given strings `s` and `t`, return the shortest substring of `s` containing **every character of
> `t`, including duplicates**. `s = "ADOBECODEBANC"`, `t = "ABC"` → `"BANC"`.

This is the hardest shape in the family, and it is hard for one specific reason: the validity test
is "the window covers a *multiset*", and re-checking that from scratch is O(alphabet) per step.
The fix is a single integer, `have`, counting **how many distinct characters have met their
required quota**. The window is valid exactly when `have == need`, which is an O(1) test.

```python
from collections import Counter

def min_window(s, t):
    if not t or not s:
        return ""

    required = Counter(t)
    need = len(required)          # distinct chars that must hit quota
    have = 0                      # how many have hit it right now
    window = {}

    best_len, best_lo = float('inf'), 0
    lo = 0

    for hi, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in required and window[ch] == required[ch]:
            have += 1             # note: == not >=, so we count each char once

        while have == need:                     # valid -> shrink to find the minimum
            if hi - lo + 1 < best_len:
                best_len, best_lo = hi - lo + 1, lo

            left = s[lo]
            window[left] -= 1
            if left in required and window[left] < required[left]:
                have -= 1         # dropped below quota: window just became invalid
            lo += 1

    return "" if best_len == float('inf') else s[best_lo:best_lo + best_len]
```

```
s = "ADOBECODEBANC", t = "ABC"   ->  required = {A:1, B:1, C:1}, need = 3

hi=0  A   window{A:1}  have=1
hi=1  D   have=1
hi=2  O   have=1
hi=3  B   window{B:1}  have=2
hi=4  E   have=2
hi=5  C   window{C:1}  have=3  -> VALID, shrink:
          "ADOBEC" len 6  -> best = (6, 0)
          drop A: window{A:0} < 1  -> have=2, lo=1
hi=6  O   have=2
hi=7  D   have=2
hi=8  E   have=2
hi=9  B   window{B:2}  == required? no (2 != 1) -> have stays 2
hi=10 A   window{A:1}  == 1 -> have=3  -> VALID, shrink:
          "DOBECODEBA" len 10  -> not better
          drop D,O,B,E,C... each time re-check quota
          when C is dropped: window{C:0} < 1 -> have=2, lo=6
hi=11 N   have=2
hi=12 C   window{C:1}  -> have=3  -> VALID, shrink:
          "ODEBANC" len 7 -> not better
          ... shrink to "BANC" len 4  -> best = (4, 9)
          drop B: have=2, stop

answer = "BANC"  ✓
```

**Complexity**: O(|s| + |t|) time — each index enters and leaves the window once — and
O(|alphabet|) space.

`★ Insight ─────────────────────────────────────`
- **`have` is the whole design.** Without it you would compare two dictionaries on every step, turning an O(n) scan into O(n · alphabet). Collapsing a multi-part validity condition into one counter is the move that makes hard window problems tractable — look for it whenever "valid" means "k separate conditions all hold".
- **The `==` in both updates is deliberate, not sloppy.** Incrementing on `window[ch] == required[ch]` (not `>=`) means a character that overshoots its quota does not inflate `have`. Symmetrically, decrementing on `window[left] < required[left]` (not `<=`) means dropping a surplus copy does not falsely invalidate the window. Swap either comparison and the answer is silently wrong on inputs with duplicates.
- This is the **shortest**-flavour template (§5): grow unconditionally, and shrink *while still valid*, recording as you go. Compare with §4's longest flavour, which shrinks *while invalid* and records after.
`─────────────────────────────────────────────────`

---

## 11. Problem 340 — Longest Substring with At Most K Distinct Characters

> Return the length of the longest substring containing at most `k` distinct characters.
> `s = "eceba"`, `k = 2` → `3` (`"ece"`).

The canonical "at most" window, and worth doing carefully because §12 turns it into a counting
tool. Grow right; while the window holds more than `k` distinct characters, shrink from the left.
The `count` dict's *size* is the distinct count, so validity is O(1) to test.

```python
def length_of_longest_substring_k_distinct(s, k):
    if k == 0:
        return 0

    count = {}
    lo = 0
    best = 0

    for hi, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1

        while len(count) > k:                  # invalid -> shrink
            left = s[lo]
            count[left] -= 1
            if count[left] == 0:
                del count[left]                # MUST delete, or len() lies
            lo += 1

        best = max(best, hi - lo + 1)

    return best
```

```
s = "eceba", k = 2

hi=0 'e'  count{e:1}         len=1 <= 2   window "e"    best=1
hi=1 'c'  count{e:1,c:1}     len=2 <= 2   window "ec"   best=2
hi=2 'e'  count{e:2,c:1}     len=2 <= 2   window "ece"  best=3
hi=3 'b'  count{e:2,c:1,b:1} len=3 > 2 -> shrink:
            drop 'e' -> count{e:1,c:1,b:1}  still 3, lo=1
            drop 'c' -> count{e:1,b:1}      now 2,   lo=2
          window "eb"   best=3
hi=4 'a'  count{e:1,b:1,a:1} len=3 > 2 -> shrink:
            drop 'e' -> count{b:1,a:1}      now 2,   lo=3
          window "ba"   best=3

answer = 3  ✓
```

**Complexity**: O(n) time, O(k) space.

`★ Insight ─────────────────────────────────────`
- **`del count[left]` when the count hits zero is load-bearing.** `len(count)` is your validity test, and a key sitting at zero still counts toward `len`. Leave it in and the window over-shrinks — a silent wrong answer, not a crash. This is the single most common bug in distinct-character windows.
- The same skeleton with `len(count) > k` swapped for a different predicate solves LC 3 (`k = 1` per character, i.e. all distinct), LC 159 (`k = 2`), and LC 904 (fruit baskets, `k = 2` in disguise). Recognising the disguise is most of the work.
`─────────────────────────────────────────────────`

---

## 12. Counting Exactly K: the `atMost` Reduction

Here is a question the window template cannot answer directly: **"how many subarrays have
*exactly* K distinct values?"** (LC 992). Windows are built to find a *longest* or *shortest*
region, not to count regions, and "exactly K" is not a monotone property — growing a window can
move you from exactly-K to exactly-(K+1) and there is no clean shrink rule.

The fix is a reduction that is worth memorising because it recurs constantly:

```
exactly(K) = atMost(K) - atMost(K - 1)
```

Every subarray with at most `K` distinct values either has at most `K−1`, or has exactly `K`.
Subtract and only the exactly-`K` ones survive. And `atMost` *is* monotone — it is the §11 window
verbatim, with one extra line.

The counting line is the second thing to internalise:

```python
def subarrays_with_k_distinct(nums, k):
    def at_most(limit):
        if limit < 0:
            return 0
        count = {}
        lo = 0
        total = 0

        for hi, x in enumerate(nums):
            count[x] = count.get(x, 0) + 1
            while len(count) > limit:
                count[nums[lo]] -= 1
                if count[nums[lo]] == 0:
                    del count[nums[lo]]
                lo += 1

            total += hi - lo + 1     # every window ending at hi is valid
        return total

    return at_most(k) - at_most(k - 1)
```

**Why `total += hi - lo + 1`?** Once the window `[lo, hi]` is valid, *every* suffix of it that
ends at `hi` is also valid — a shorter window cannot have more distinct values. Those suffixes are
`[lo, hi], [lo+1, hi], ..., [hi, hi]`, and there are exactly `hi - lo + 1` of them. So one addition
per step counts every valid subarray, with no double counting: each subarray is counted once, at
its own right endpoint.

```
nums = [1,2,1,2,3], k = 2

at_most(2):
  hi=0 [1]        lo=0  += 1   total=1
  hi=1 [1,2]      lo=0  += 2   total=3
  hi=2 [1,2,1]    lo=0  += 3   total=6
  hi=3 [1,2,1,2]  lo=0  += 4   total=10
  hi=4 adds 3 -> 3 distinct, shrink lo to 2 ([1,2,3] still 3) then 3 -> [2,3] ok, lo=3
                  += 4-3+1 = 2   total=12

at_most(1):
  hi=0 [1]        lo=0  += 1   total=1
  hi=1 shrink to [2]     lo=1  += 1   total=2
  hi=2 shrink to [1]     lo=2  += 1   total=3
  hi=3 shrink to [2]     lo=3  += 1   total=4
  hi=4 shrink to [3]     lo=4  += 1   total=5

exactly(2) = 12 - 5 = 7  ✓
```

**Complexity**: O(n) time (two linear passes), O(k) space.

`★ Insight ─────────────────────────────────────`
- **Reduce non-monotone to monotone.** The window needs a predicate where "valid" survives shrinking. "Exactly K" does not; "at most K" does. Whenever a constraint reads *exactly*, try expressing it as a difference of two *at most* problems before concluding windows do not apply. Same trick handles "exactly K odd numbers" (LC 1248) and "exactly K ones".
- **`total += hi - lo + 1` is the counting idiom for the whole family**, not a trick specific to this problem. Any time a window is valid and validity is inherited by suffixes, that one line counts every qualifying subarray in O(1) per step.
`─────────────────────────────────────────────────`

---

## 13. Problem 862 — Shortest Subarray with Sum at Least K (negatives allowed)

> Return the length of the shortest **non-empty** subarray with sum ≥ `k`, where `nums` may
> contain **negative** numbers. `nums = [2,-1,2]`, `k = 3` → `3`.

This problem exists to teach you where the plain window breaks. Section 5's shortest-subarray
template assumes that extending a window *increases* the sum, so that once you are at or above the
target you can shrink. With negatives that is false: a longer window can have a smaller sum, so
"shrink while valid" throws away windows that would have become valid later.

The repair is to stop working on the array and work on its **prefix sums**:

```
P[0] = 0,  P[i] = nums[0] + ... + nums[i-1]
sum(nums[i..j-1]) = P[j] - P[i]
```

The question becomes: for each `j`, find the **largest** `i < j` with `P[i] <= P[j] - k`. Now run a
**monotonic deque** over the prefix array holding indices with increasing `P` values:

- **Pop from the front** while `P[j] - P[front] >= k`. That front index gives a valid subarray, and
  it is the longest one still available — so record it and discard it, because any later `j` would
  only produce a longer answer with the same start.
- **Pop from the back** while `P[j] <= P[back]`. A later index with a smaller-or-equal prefix is
  strictly better as a future start: it is closer to `j` *and* subtracts less. The back index can
  never win again.

```python
from collections import deque

def shortest_subarray(nums, k):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x

    best = n + 1
    dq = deque()                      # indices into prefix, increasing prefix values

    for j in range(n + 1):
        while dq and prefix[j] - prefix[dq[0]] >= k:
            best = min(best, j - dq.popleft())
        while dq and prefix[j] <= prefix[dq[-1]]:
            dq.pop()
        dq.append(j)

    return best if best <= n else -1
```

```
nums = [2,-1,2], k = 3   ->  prefix = [0, 2, 1, 3]

j=0  P=0  front: dq empty
          back:  dq empty            dq=[0]              (P: 0)
j=1  P=2  front: 2 - P[0]=0 -> 2 >= 3? no
          back:  2 <= P[0]=0? no     dq=[0,1]            (P: 0,2)
j=2  P=1  front: 1 - 0 = 1 >= 3? no
          back:  1 <= P[1]=2? yes -> pop 1
                 1 <= P[0]=0? no     dq=[0,2]            (P: 0,1)
j=3  P=3  front: 3 - P[0]=0 -> 3 >= 3? YES -> best = 3-0 = 3, popleft
                 3 - P[2]=1 -> 2 >= 3? no
          back:  3 <= P[2]=1? no     dq=[2,3]

answer = 3  ✓   (the whole array; no shorter subarray reaches 3)
```

**Complexity**: O(n) time — each index is pushed once and popped once — and O(n) space.

`★ Insight ─────────────────────────────────────`
- **Negatives do not kill the window; they kill the *array* as the axis.** Move to prefix sums and the monotonicity you need comes back, because now you are searching for a *value* in a structure you control rather than relying on the input's sign.
- **Two pops, two different reasons.** The front pop *harvests* answers (this start works, and it is the longest still available). The back pop *prunes* dominated candidates (a smaller prefix arriving later beats a larger one arriving earlier on both axes). Every monotonic-deque problem has this same two-rule shape — see [Stack & Queue §5](/pattern/stack-queue) for the general form.
- Contrast with LC 209 (all-positive version): there the plain two-pointer window is enough, because with no negatives the prefix array is already increasing and the deque would never pop from the back.
`─────────────────────────────────────────────────`

---

## 14. Master Comparison Table

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

## 15. How to Identify This Pattern

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

## 16. Practice Order

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
  340 (Medium) ──── At-most-k distinct (remember to delete zero counts)
    │
    ▼
  239 (Hard)   ──── Monotonic deque for window max
    │
    ▼
  76 (Hard)    ──── Quota counter: collapse a multiset test into one int
    │
    ▼
  992 (Hard)   ──── The atMost(k) - atMost(k-1) reduction
    │
    ▼
  862 (Hard)   ──── Where the plain window dies: negatives + prefix deque
```

---

## 17. Pattern Recognition Cheat Sheet

### Signal → shape

| You see in the problem statement | Shape | Key state |
|----------------------------------|-------|-----------|
| "every subarray of size k", "average of k" | Fixed | running aggregate, add one / drop one |
| "longest substring such that ..." | Variable, longest | grow always; shrink **while invalid**; record after the shrink |
| "minimum length subarray such that ..." | Variable, shortest | grow always; shrink **while valid**; record before the shrink |
| "at most k distinct / k replacements / k zeros" | Variable + counter | `len(count)` or a violation tally |
| "anagram", "permutation of t", "contains all of t" | Fixed or variable + freq map | a `have`/`need` quota counter, not dict equality |
| "**exactly** k ..." and it asks to **count** | Two windows | `atMost(k) − atMost(k−1)` (§12) |
| "maximum / minimum **of each** window" | Fixed + monotonic deque | indices in monotone value order (§8) |
| "sum ≥ target" **with negative numbers** | Not a plain window | prefix sums + deque (§13) |
| "subsequence" (not contiguous) | **Not this pattern** | → [DP](/pattern/dp) |

### The two templates, side by side

The difference is one word in the `while`, and it flips where you record the answer:

```python
# LONGEST: shrink while INVALID, record after
for hi in range(n):
    add(hi)
    while not valid():
        remove(lo); lo += 1
    best = max(best, hi - lo + 1)      # window is valid here

# SHORTEST: shrink while VALID, record before
for hi in range(n):
    add(hi)
    while valid():
        best = min(best, hi - lo + 1)  # record, THEN break it
        remove(lo); lo += 1
```

### Bug checklist

1. **Did you delete zero-count keys?** If `len(count)` is your validity test, a lingering zero
   entry silently breaks it (§11).
2. **Are you using `==` or `>=` in the quota update?** In LC 76, `>=` overcounts `have` on
   duplicate characters (§10).
3. **Does `left` ever move backwards?** It must not. If your logic needs it to, validity is not
   monotone and you need §12 or §13.
4. **Fixed-size windows: are you recording only once the window is full?** Emitting before
   `hi >= k-1` produces answers for undersized windows.
5. **Are there negatives?** Check this explicitly before trusting a shrink-while-valid loop.

---

## The Sliding Window Toolbox at a Glance

```
                  Contiguous region + monotone validity
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   FIXED SIZE k             VARIABLE                 NOT A PLAIN WINDOW
   add hi, drop hi-k        grow hi always           the axis is wrong
        │                        │                        │
        │              ┌─────────┴─────────┐              │
        │         LONGEST             SHORTEST            │
        │      shrink while         shrink while          │
        │        INVALID               VALID              │
        │              │                   │              │
   643 avg k       3   no repeats     209 min sum   992 exactly-k -> atMost diff
   438 anagram     424 k replace      76  min window 862 negatives -> prefix+deque
   567 permutation 1004 k zeros                      239 window max -> deque
                   340 k distinct
```

**The one question that picks the branch**: is the window size *given* (fixed), *discovered*
(variable), or is the thing you need not a validity question at all (deque / reduction)?

---

## When This Fails

The window requires **monotone validity**: shrinking a valid window must leave it valid. When
that fails, the plain template silently returns a wrong answer rather than crashing.

- **"Sum at least k" with negative numbers.** Growing the window can *decrease* the sum, so
  shrink-while-valid discards windows that would have qualified later. Fix: prefix sums plus a
  monotonic deque (§13).
- **"Exactly k distinct".** Not monotone in either direction. Fix: `atMost(k) − atMost(k−1)` (§12).
- **The answer is a subsequence, not a substring.** Windows only produce contiguous regions.
  That is [DP](/pattern/dp) territory.
- **The window needs the maximum, not validity.** "Max of each window" is not a constraint
  problem at all — it is a monotonic deque
  ([Stack & Queue §5](/pattern/stack-queue)).

The tell that you are fighting the pattern: you want to move `left` *backwards*. That is never
legal in a sliding window, and wanting to is the signal to switch tools.

## Self-Test

Answer these from memory, out loud or on paper, *before* looking. Recognition is not
recall: rereading an explanation feels like knowing, and it is not. A question you cannot answer
cold names the exact section to revisit — you do not need to reread the guide.


**1. What property must hold for a sliding window to be correct, and what is the tell that it does not?**

<details markdown="1">
<summary>Answer</summary>

Monotone validity: removing an element from a valid window leaves it valid. The tell that it fails is wanting to move `left` backwards. `left` must only ever advance — that is what makes the whole scan O(n).

</details>

**2. Why is the window O(n) despite the inner `while` loop?**

<details markdown="1">
<summary>Answer</summary>

Both pointers only advance, and each is bounded by `n`. So across the entire run they take at most `2n` steps combined, regardless of how much the window resizes in between. This is amortized analysis, not a claim that each step is O(1).

</details>

**3. Longest versus shortest: what is the one-word difference in the template?**

<details markdown="1">
<summary>Answer</summary>

Longest shrinks **while invalid** and records *after* the shrink loop (the window is valid at that point). Shortest shrinks **while valid** and records *inside* the loop, before breaking the window. Same skeleton, inverted condition, and the recording point moves with it.

</details>

**4. You need to count subarrays with exactly K distinct values. Why can't the window do it directly, and what is the fix?**

<details markdown="1">
<summary>Answer</summary>

"Exactly K" is not monotone — shrinking can drop you below K and growing can push you above, with no clean shrink rule. Fix: `exactly(K) = atMost(K) − atMost(K−1)`. Every at-most-K subarray either has at most K−1 or exactly K, so the difference isolates the ones you want, and `atMost` *is* monotone.

</details>

**5. In `atMost`, why is the count `total += hi - lo + 1`?**

<details markdown="1">
<summary>Answer</summary>

Once `[lo, hi]` is valid, every suffix ending at `hi` is also valid (a shorter window cannot have more distinct values). There are `hi - lo + 1` such suffixes. Counting at each right endpoint means every subarray is counted exactly once.

</details>

**6. What goes wrong if you leave zero-count keys in the frequency map?**

<details markdown="1">
<summary>Answer</summary>

`len(count)` is the validity test, and a key sitting at zero still counts toward `len`. The window over-shrinks — a silent wrong answer, not a crash. Always `del` when a count reaches zero.

</details>

**7. In minimum window substring, why increment `have` on `window[ch] == required[ch]` rather than `>=`?**

<details markdown="1">
<summary>Answer</summary>

`have` counts *distinct characters that have met quota*. With `>=`, a character exceeding its quota would increment `have` again and falsely mark the window valid. Symmetrically the decrement uses `<` so that dropping a surplus copy does not falsely invalidate. Both comparisons break only on inputs with duplicates.

</details>

**8. Negatives are present and you need the shortest subarray with sum ≥ k. What changes?**

<details markdown="1">
<summary>Answer</summary>

Stop using the array as the axis. Build prefix sums and run a monotonic deque over them: pop the front while `P[j] − P[front] >= k` (harvest an answer), pop the back while `P[j] <= P[back]` (prune a dominated candidate). Monotonicity returns because you now control the structure being searched.

</details>

---

## See Also

- [Two Pointers](/pattern/two-pointers) — the sibling technique; §11 draws the line between them.
- [Prefix Sum](/pattern/prefix-sum) — what to reach for when the array has negatives and the window loses its monotonicity.
- [Stack & Queue §5](/pattern/stack-queue) — the monotonic deque behind §8, with the amortized-O(1) argument in full.
- [Heap / Priority Queue](/pattern/heap) — for a window *median* or *k-th* value, where a deque cannot help.
- [Binary Search](/pattern/binary-search) — the fallback when the window is not monotone: search the answer and verify each candidate in a linear pass.
- [Pattern Decision Map](/pattern/decision-map) — the router: which technique does a cold problem call for?
- [Pattern Mastery Program](/pattern/mastery) — the spaced-repetition schedule, mastery checklist, and drill formats that turn reading into recall.

---

*Pattern mastered — one pointer marches, the other follows only to keep the window honest.*
