# Message Spreading

## Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

There are N students in a class, each with a different funny story. They want to share stories by sending electronic messages. A sender includes all stories they know, and each message has only one recipient.

Find the minimum number of messages needed so everyone gets all the funny stories.

## Input Format
- First line: T (number of test cases)
- Each test case: N (number of students)

## Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 10⁵

## Output Format
For each test case, print the minimum number of messages needed.

## Solution

### Approach
This is a classic problem. With N students:
- First, everyone sends their story to one person (N-1 messages, one person has all stories)
- Then that person sends to everyone else (N-1 messages)

But we can optimize: use a tree-like broadcast structure.
- Minimum messages = 2*(N-1) for N ≥ 2
- For N = 1: 0 messages needed

Actually, the optimal is **2*(N-1)** for N > 1.

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())

    if n == 1:
      print(0)
    else:
      # Minimum messages = 2 * (n - 1)
      # First phase: gather all stories to one person (n-1 messages)
      # Second phase: distribute from that person (n-1 messages)
      print(2 * (n - 1))

if __name__ == "__main__":
  solve()
```

### Mathematical Proof

```python
def solve():
  """
  For N students to all know all N stories:

  Lower bound: Each student except the "collector" must send at least once
  to contribute their story = N-1 messages minimum for gathering.

  Each student except the "distributor" must receive at least once
  to get all stories = N-1 messages minimum for distributing.

  Total minimum = 2*(N-1)

  This is achievable:
  Round 1: Students 2,3,...,N each send to student 1 (N-1 messages)
      Now student 1 knows all stories
  Round 2: Student 1 sends to students 2,3,...,N (N-1 messages)
      Now everyone knows all stories
  """
  t = int(input())

  for _ in range(t):
    n = int(input())
    print(max(0, 2 * (n - 1)))

if __name__ == "__main__":
  solve()
```

### One-liner Solution

```python
t = int(input())
for _ in range(t):
  n = int(input())
  print(2 * n - 2 if n > 1 else 0)
```

### Complexity Analysis
- **Time Complexity:** O(1) per test case
- **Space Complexity:** O(1)

### Key Insight
This is an information dissemination problem. The minimum number of messages is 2(N-1):
- Phase 1 (Aggregation): N-1 messages to collect all stories at one person
- Phase 2 (Broadcast): N-1 messages to distribute to everyone else
