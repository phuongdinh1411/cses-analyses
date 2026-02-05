# N Meetings in One Room

## Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

There is one meeting room in Flipkart. There are n meetings in the form of (Sᵢ, Fᵢ) where Sᵢ is the start time and Fᵢ is the finish time of meeting i.

Find the maximum number of meetings that can be accommodated in the meeting room.

## Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: N (number of meetings)
  - Second line: N start times Sᵢ
  - Third line: N finish times Fᵢ

## Output Format
Print the order in which meetings should take place (1-indexed), separated by spaces.

## Solution

### Approach
This is the classic Activity Selection problem. Greedy approach:
1. Sort meetings by finish time
2. Select the meeting with earliest finish time
3. Skip all meetings that overlap with selected meeting
4. Repeat until no meetings left

### Python Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  n = int(input())
  starts = list(map(int, input().split()))
  ends = list(map(int, input().split()))

  # Create list of (end_time, start_time, original_index)
  meetings = [(ends[i], starts[i], i + 1) for i in range(n)]

  # Sort by end time
  meetings.sort()

  result = []
  last_end = -1

  for end, start, idx in meetings:
   if start > last_end:
    result.append(idx)
    last_end = end

  print(' '.join(map(str, result)))

if __name__ == "__main__":
 solve()
```

### Alternative Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  n = int(input())
  starts = list(map(int, input().split()))
  ends = list(map(int, input().split()))

  # Create meetings with 1-based index
  meetings = []
  for i in range(n):
   meetings.append((ends[i], starts[i], i + 1))

  # Sort by end time, then by start time
  meetings.sort(key=lambda x: (x[0], x[1]))

  selected = []
  prev_end = 0

  for end, start, idx in meetings:
   if start >= prev_end:
    selected.append(idx)
    prev_end = end

  print(' '.join(map(str, selected)))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting
- **Space Complexity:** O(N) for storing meetings

### Key Insight
The greedy choice is to always pick the meeting that ends earliest among non-conflicting meetings. This leaves maximum room for subsequent meetings. Sorting by end time and greedily selecting non-overlapping meetings gives the optimal solution.
