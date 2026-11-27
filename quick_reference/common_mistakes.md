---
layout: simple
title: "Common Mistakes"
permalink: /quick_reference/common_mistakes
---


# Common Mistakes and Pitfalls (Python interviews)

### In 60 seconds
- **Complexity traps:** `list.pop(0)`, `x in list`, slicing in a loop, and string `+=` look O(1) but are O(n).
- **Python-specific traps:** mutable defaults, `[[0]*m]*n` aliasing, recursion limit (~1000), float `==`.
- **Edge cases to say out loud:** empty input, one element, duplicates, negatives, all-equal values, max size.
- **Not a Python problem:** integer overflow (ints are unbounded) and negative `%` with a positive modulus (the result is already in `[0, m)`). Mention them only when porting to C++/Java.

> **Say this in the interview:** "Before coding I'll list the edge cases — empty, single, duplicates, negatives — and check that every inner operation is O(1)."

---

## Hidden O(n) operations

| Looks cheap | Actually | Use instead |
|---|---|---|
| `lst.pop(0)`, `lst.insert(0, x)` | O(n) shift | `collections.deque` (`popleft`, `appendleft`) |
| `x in lst` | O(n) scan | `set` / `dict` membership, O(1) average |
| `lst[i:j]`, `s[i:j]` inside a loop | O(j − i) copy each time | Pass indices, not slices |
| `s += piece` in a loop | Can be O(n²) total (CPython sometimes optimises, don't rely on it) | Collect in a list, `"".join(parts)` |
| `min(lst)` / `max(lst)` inside a loop | O(n) per call | Heap, monotonic deque, or running value |
| `sorted(...)` inside a loop | O(n log n) per call | Sort once; `bisect` or `SortedList` for updates |

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)
assert q.popleft() == 1          # O(1), unlike list.pop(0)

parts = [str(i) for i in range(5)]
assert "".join(parts) == "01234"  # O(total length)
```

## Python-specific traps

```python
# 1. Mutable default argument is shared across calls
def add_bad(x, acc=[]):
    acc.append(x)
    return acc

def add_good(x, acc=None):
    acc = [] if acc is None else acc
    acc.append(x)
    return acc

add_bad(1); assert add_bad(2) == [1, 2]          # surprise
add_good(1); assert add_good(2) == [2]

# 2. Grid aliasing: every row is the same list object
bad = [[0] * 3] * 2
bad[0][0] = 1
assert bad == [[1, 0, 0], [1, 0, 0]]
good = [[0] * 3 for _ in range(2)]
good[0][0] = 1
assert good == [[1, 0, 0], [0, 0, 0]]

# 3. Floats: compare with a tolerance, never ==
import math
assert 0.1 + 0.2 != 0.3
assert math.isclose(0.1 + 0.2, 0.3)

# 4. Integer square root: float sqrt is wrong for large n
n = (10**8 + 1) ** 2 - 1
assert int(n ** 0.5) != math.isqrt(n)            # float rounds up
assert math.isqrt(n) == 10**8

# 5. Python % with a positive modulus is already non-negative
assert -7 % 3 == 2                                # no ((a % m) + m) % m needed
assert -7 // 3 == -3                              # floor division, unlike C++/Java truncation
```

**Recursion depth:** CPython's default limit is about 1000 frames and Python has no tail-call optimisation. For DFS on 10⁵ nodes, use an explicit stack (or `sys.setrecursionlimit` plus a larger thread stack as a last resort).

```python
def dfs_iterative(adj: dict[int, list[int]], start: int) -> list[int]:
    order, stack, seen = [], [start], {start}
    while stack:
        u = stack.pop()
        order.append(u)
        for v in reversed(adj.get(u, [])):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return order

assert dfs_iterative({0: [1, 2], 1: [3]}, 0) == [0, 1, 3, 2]
```

## Edge cases that break "correct" code

```python
def second_largest(arr: list[int]) -> int | None:
    """Second largest *distinct* value; sorted(arr)[-2] fails on [5, 5] and [7]."""
    first = second = None
    for x in arr:
        if first is None or x > first:
            first, second = x, first
        elif x != first and (second is None or x > second):
            second = x
    return second

assert second_largest([3, 5, 5]) == 3
assert second_largest([5, 5]) is None
assert second_largest([]) is None

def two_sum(arr: list[int], target: int) -> tuple[int, int] | None:
    """Store indices, not values: arr.index() is O(n) and wrong with duplicates."""
    seen: dict[int, int] = {}
    for i, x in enumerate(arr):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i
    return None

assert two_sum([3, 3], 6) == (0, 1)
assert two_sum([1, 2], 7) is None
```

| Edge case | Typical failure |
|---|---|
| Empty input | `max([])`, `arr[0]`, division by `len(arr)` raise |
| One element | `arr[-2]`, `range(1, n)` loops never run |
| Duplicates | `arr.index`, `set` conversion, strict `<` vs `<=` in binary search |
| Negatives / zero | Sliding-window "shrink while sum > k" assumes non-negative values; product signs flip |
| All equal | Partition-based quickselect degrades; rank ties |
| Max constraints | O(n²) at n = 10⁵ is 10¹⁰ operations — too slow |

## Choosing the algorithm from constraints

Use the [constraint-size cheat sheet](/pattern/decision-map#9-constraint-size-cheat-sheet). One Python-specific adjustment: CPython runs roughly 10⁷ simple operations per second, about 10× fewer than C++, so an O(n²) solution at n = 10⁴ (10⁸ steps) is already too slow.

## Checklist

1. **Before coding:** restate the problem, read constraints, list edge cases, state the target complexity.
2. **While coding:** keep every inner-loop operation O(1); use indices instead of slices.
3. **After coding:** dry-run one normal case and two edge cases out loud; re-state time and space.

See also: [Code Templates](/quick_reference/code_templates) and the [pattern decision map](/pattern/decision-map).
