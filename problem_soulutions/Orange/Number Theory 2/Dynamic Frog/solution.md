# Dynamic Frog

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

A frog needs to cross a river of distance D using rocks. Rocks are either:
- Big (B): Can be used multiple times
- Small (S): Can only be used once (must be used going AND coming back)

The frog must go from left bank to right bank and return. Minimize the maximum single jump distance.

## Input Format
- T test cases
- Each test case:
  - First line: N (rocks), D (river width)
  - Second line: N rock descriptions as "S-M" or "B-M" where M is distance from left bank

## Output Format
For each case: "Case X: Y" where Y is the minimized maximum jump.

## Example
```
Input:
3
1 10
B-5
1 10
S-5
2 10
B-3 S-6

Output:
Case 1: 5
Case 2: 10
Case 3: 7
```
- **Case 1:** both trips use the big rock at 5, so every jump is 5.
- **Case 2:** the small rock helps only one trip, and the other must jump the full 10.
- **Case 3:** the stone list is [0, 0, 3, 3, 6, 10, 10]. One trip goes 0 → 3 → 10, the other 10 → 6 → 3 → 0, so the largest jump is 7.

## Solution

### Approach
Big rocks and the two banks can be used on both trips, so list each of them twice. A small rock can be used once, so list it once. Sort the list.

In an optimal plan the two trips alternate through this sorted list: one trip lands on even indices, the other on odd ones. Each jump therefore spans two consecutive list entries, and the answer is `max(stones[i+2] - stones[i])`.

The intuitive plan of using every rock going and only big rocks returning is wrong. With D = 10 and small rocks at 3 and 6, it gives 10, while splitting the small rocks gives 7.

### Python Solution

```python
import sys


def solve():
  data = sys.stdin.read().split()
  idx = 0
  t = int(data[idx]); idx += 1

  for case in range(1, t + 1):
    n, d = int(data[idx]), int(data[idx + 1]); idx += 2

    # Big rocks serve both trips, so list them twice; banks too.
    stones = [0, 0, d, d]
    for rock in data[idx:idx + n]:
      kind, pos = rock[0], int(rock[2:])
      stones += [pos, pos] if kind == 'B' else [pos]
    idx += n
    stones.sort()

    # Alternate stones between the two trips: trip one takes even indices, trip two odd ones.
    best = max(stones[i + 2] - stones[i] for i in range(len(stones) - 2))
    print(f"Case {case}: {best}")


if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting
- **Space Complexity:** O(N)

### Key Insight
Duplicate every stone that both trips may use, then let the trips alternate. The worst jump is the largest gap between list entries two apart.

