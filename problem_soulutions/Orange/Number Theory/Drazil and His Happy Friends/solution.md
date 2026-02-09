# Drazil and His Happy Friends

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Drazil has many friends. Some of them are happy and some of them are unhappy. Drazil wants to make all his friends become happy. So he invented the following plan.

There are n boys and m girls among his friends. Let's number them from 0 to n-1 and 0 to m-1 separately. In i-th day, Drazil invites (i % n)-th boy and (i % m)-th girl to have dinner together (as Drazil is programmer, i starts from 0). If one of those two people is happy, the other one will also become happy. Otherwise, those two people remain in their states. Once a person becomes happy (or if he/she was happy originally), he stays happy forever.

Drazil wants to know whether he can use this plan to make all his friends become happy at some moment.

## Input Format
- The first line contains two integers n and m (1 ≤ n, m ≤ 100).
- The second line contains an integer b (0 ≤ b ≤ n), denoting the number of happy boys, followed by b distinct integers x1, x2, ..., xb (0 ≤ xi < n), denoting the indices of happy boys.
- The third line contains an integer g (0 ≤ g ≤ m), denoting the number of happy girls, followed by g distinct integers y1, y2, ..., yg (0 ≤ yj < m), denoting the indices of happy girls.
- It is guaranteed that there is at least one person that is unhappy.

## Output Format
If Drazil can make all his friends become happy by this plan, print "Yes". Otherwise, print "No".

## Example
```
Input:
2 3
0
1 0

Output:
Yes
```
There are 2 boys and 3 girls. Boy 0 is initially happy, and girl 0 is initially happy. On day 0: boy 0 meets girl 0 (both happy). Day 1: boy 1 meets girl 1 (boy 1 becomes happy). Day 2: boy 0 meets girl 2 (girl 2 becomes happy). All friends become happy.

## Solution

### Approach
The key insight is based on number theory:
- On day i, boy (i % n) meets girl (i % m)
- The pattern repeats after LCM(n, m) days
- We simulate for n × m days (which is sufficient since LCM(n,m) ≤ n×m)
- If happiness can spread, it will within this period

### Python Solution

```python
def solve():
  n, m = map(int, input().split())

  # Read happy boys using tuple unpacking
  line = list(map(int, input().split()))
  b, *boys = line
  happy_boys = set(boys)

  # Read happy girls using tuple unpacking
  line = list(map(int, input().split()))
  g, *girls = line
  happy_girls = set(girls)

  # Simulate for n * m days (covers full cycle)
  for day in range(n * m):
    boy, girl = day % n, day % m

    # If either is happy, both become happy
    if boy in happy_boys or girl in happy_girls:
      happy_boys.add(boy)
      happy_girls.add(girl)

  # Simplified conditional output
  print("Yes" if len(happy_boys) == n and len(happy_girls) == m else "No")

if __name__ == "__main__":
  solve()
```

### Alternative Solution using GCD

```python
import math

def solve():
  n, m = map(int, input().split())

  line = list(map(int, input().split()))
  b = line[0]
  happy_boys = [False] * n
  for i in range(1, b + 1):
    happy_boys[line[i]] = True

  line = list(map(int, input().split()))
  g = line[0]
  happy_girls = [False] * m
  for i in range(1, g + 1):
    happy_girls[line[i]] = True

  # Simulate for lcm(n, m) days - use n*m as upper bound
  lcm = (n * m) // math.gcd(n, m)

  for day in range(lcm):
    boy = day % n
    girl = day % m

    if happy_boys[boy] or happy_girls[girl]:
      happy_boys[boy] = True
      happy_girls[girl] = True

  if all(happy_boys) and all(happy_girls):
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n × m)
- **Space Complexity:** O(n + m)

### Key Insight
The meeting pattern between boys and girls forms a cycle based on LCM(n, m). If happiness cannot spread to everyone within this cycle, it never will.
