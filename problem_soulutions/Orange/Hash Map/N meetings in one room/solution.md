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

## Example
```
Input:
1
6
1 3 0 5 8 5
2 4 6 7 9 9

Output:
1 2 4 5
```
6 meetings with starts [1,3,0,5,8,5] and ends [2,4,6,7,9,9]. Sort by end time: meeting 1(1-2), meeting 2(3-4), meeting 3(0-6), meeting 4(5-7), meeting 5(8-9), meeting 6(5-9). Select: 1 (ends 2), 2 (starts 3 > 2, ends 4), 4 (starts 5 > 4, ends 7), 5 (starts 8 > 7, ends 9). Output: 1 2 4 5.

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

    # Use enumerate and zip for cleaner iteration
    # Create list of (end_time, start_time, original_index)
    meetings = sorted(
      (end, start, i + 1)
      for i, (start, end) in enumerate(zip(starts, ends))
    )

    result = []
    last_end = -1

    # Use tuple unpacking
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

    # Use enumerate and zip with list comprehension
    meetings = [
      (end, start, i + 1)
      for i, (start, end) in enumerate(zip(starts, ends))
    ]

    # Sort by end time, then by start time
    meetings.sort(key=lambda x: (x[0], x[1]))

    selected = []
    prev_end = 0

    # Tuple unpacking in loop
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
