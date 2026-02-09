# The Monk and Prateek

## Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

## Problem Statement

The Monk is testing Prateek with a hash function called the r3gz3n function:

`f(n) = N ⊕ (sum of digits of N)`

For example, f(81) = 81 ⊕ (8 + 1) = 81 ⊕ 9 = 88.

Given a list of N numbers, find:
1. The value of the r3gz3n function which occurs the maximum number of times
2. The number of collisions with the hash function

**Notes:**
- If all values are unique, print the maximum hashed value
- If multiple hashed values have the same maximum count, print the smallest one

## Input Format
- First line: N (number of numbers)
- Second line: N integers separated by space

## Constraints
- 1 ≤ N ≤ 10^5
- 1 ≤ Nᵢ ≤ 10^7

## Output Format
Print two integers: the value with maximum occurrences (or max value if all unique) and the number of collisions.

## Example
```
Input:
3
12 22 32

Output:
44 1
```
f(12) = 12 XOR (1+2) = 12 XOR 3 = 15. f(22) = 22 XOR 4 = 18. f(32) = 32 XOR 5 = 37. All unique, so output max value 37 and 0 collisions... Let me recalculate: 12=1100, 3=0011, XOR=1111=15. 22=10110, 4=00100, XOR=10010=18. 32=100000, 5=000101, XOR=100101=37. Output: 37 0.

## Solution

### Approach
1. Compute the hash value for each number: `f(n) = n XOR digit_sum(n)`
2. Use a hash map to count occurrences of each hash value
3. Count collisions (when a hash value already exists)
4. Find the most frequent hash value (smallest if tie)

### Python Solution

```python
def digit_sum(n):
  total = 0
  while n:
    total += n % 10
    n //= 10
  return total

def r3gz3n(n):
  return n ^ digit_sum(n)

def solve():
  n = int(input())
  numbers = list(map(int, input().split()))

  hash_count = {}
  collisions = 0
  max_hash = float('-inf')

  for num in numbers:
    h = r3gz3n(num)
    max_hash = max(max_hash, h)

    if h in hash_count:
      collisions += 1
      hash_count[h] += 1
    else:
      hash_count[h] = 1

  # Find most frequent hash value
  if collisions == 0:
    # All unique - return max hash value
    print(max_hash, 0)
  else:
    # Find value with maximum count (smallest if tie)
    max_count = max(hash_count.values())
    most_frequent = min(h for h, c in hash_count.items() if c == max_count)
    print(most_frequent, collisions)

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
from collections import Counter

def solve():
  n = int(input())
  nums = list(map(int, input().split()))

  def hash_func(x):
    return x ^ sum(int(d) for d in str(x))

  hashes = [hash_func(x) for x in nums]
  count = Counter(hashes)

  collisions = len(hashes) - len(count)

  if collisions == 0:
    result = max(hashes)
  else:
    max_freq = max(count.values())
    result = min(h for h, c in count.items() if c == max_freq)

  print(result, collisions)

if __name__ == "__main__":
  solve()
```

### One-liner Style

```python
from collections import Counter

def solve():
  n = int(input())
  nums = list(map(int, input().split()))

  h = lambda x: x ^ sum(map(int, str(x)))
  hashes = [h(x) for x in nums]
  cnt = Counter(hashes)
  colls = len(hashes) - len(cnt)

  if colls == 0:
    print(max(hashes), 0)
  else:
    mx = max(cnt.values())
    print(min(k for k, v in cnt.items() if v == mx), colls)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × D) where D is the average number of digits (at most 8 for 10^7)
- **Space Complexity:** O(N) for the hash count map

### Key Insight
A collision occurs when two different input numbers produce the same hash value. The total number of collisions is `total_numbers - unique_hash_values`. When finding the most frequent hash value with ties, we need to return the smallest one.
