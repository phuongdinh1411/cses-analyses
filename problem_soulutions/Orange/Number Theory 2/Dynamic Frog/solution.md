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
1
3 10
B-3 S-5 B-7

Output:
Case 1: 5
```
River width is 10. Rocks at positions 3 (big), 5 (small), 7 (big). Going: jumps are 3, 2, 2, 3 (max=3). Returning: small rock at 5 is gone, jumps are 3, 4, 3 (max=4). Actually, the maximum jump is 5 when considering the return trip without the small rock.

## Solution

### Approach
Since small rocks can only be used once, and frog must go and return:
- Going: Can use any rocks
- Returning: Small rocks are gone

Key insight: Process rocks by position. For the return trip, small rocks won't exist, so the frog must jump over gaps where small rocks were.

Strategy: On the way there, use all rocks. On return, only big rocks remain. The answer is the maximum of:
1. Max jump on the way there (using all rocks)
2. Max jump on return (only big rocks + banks)

### Python Solution

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    parts = input().split()
    n, d = int(parts[0]), int(parts[1])

    rocks = []
    for i in range(n):
      rock = parts[2 + i] if len(parts) > 2 + i else input().split()[0]
      rock_type, dist = rock[0], int(rock[2:])
      rocks.append((dist, rock_type))

    rocks.sort()

    # Build position lists using list comprehension
    all_positions = [0] + [dist for dist, _ in rocks] + [d]
    big_positions = [0] + [dist for dist, rtype in rocks if rtype == 'B'] + [d]

    # Calculate max jumps using zip for consecutive pairs
    max_jump_go = max(b - a for a, b in zip(all_positions, all_positions[1:]))
    max_jump_return = max(b - a for a, b in zip(big_positions, big_positions[1:]))

    print(f"Case {case}: {max(max_jump_go, max_jump_return)}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Single Pass

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    line = input().split()
    n, d = int(line[0]), int(line[1])

    rocks = []
    idx = 2
    while len(rocks) < n:
      if idx < len(line):
        rocks.append(line[idx])
        idx += 1
      else:
        rocks.extend(input().split())

    # Parse rocks
    parsed = []
    for rock in rocks:
      rock_type = rock[0]
      pos = int(rock.split('-')[1])
      parsed.append((pos, rock_type))

    parsed.sort()

    # Calculate jumps
    all_pos = [0] + [p for p, _ in parsed] + [d]
    big_pos = [0] + [p for p, t in parsed if t == 'B'] + [d]

    max_go = max(all_pos[i] - all_pos[i-1] for i in range(1, len(all_pos)))
    max_return = max(big_pos[i] - big_pos[i-1] for i in range(1, len(big_pos)))

    print(f"Case {case}: {max(max_go, max_return)}")

if __name__ == "__main__":
  solve()
```

### Input Parsing Variant

```python
def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  t = int(data[idx])
  idx += 1

  for case in range(1, t + 1):
    n = int(data[idx])
    d = int(data[idx + 1])
    idx += 2

    rocks = []
    for _ in range(n):
      rock = data[idx]
      idx += 1
      rock_type = rock[0]
      pos = int(rock[2:])
      rocks.append((pos, rock_type))

    rocks.sort()

    # All positions for going
    all_pos = [0] + [p for p, _ in rocks] + [d]
    # Big rocks only for return
    big_pos = [0] + [p for p, t in rocks if t == 'B'] + [d]

    max_go = max(all_pos[i] - all_pos[i-1] for i in range(1, len(all_pos)))
    max_ret = max(big_pos[i] - big_pos[i-1] for i in range(1, len(big_pos)))

    print(f"Case {case}: {max(max_go, max_ret)}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting
- **Space Complexity:** O(N)

### Key Insight
The frog uses all rocks going forward, but small rocks disappear after one use. On the return trip, only big rocks remain. The answer is the maximum of the largest gap in each direction. Going: gaps between consecutive rocks (including banks). Returning: gaps between consecutive big rocks only.
