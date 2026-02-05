# Lotto

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

In the German Lotto you have to select 6 numbers from the set {1, 2, ..., 49}. A popular strategy to play Lotto - although it doesn't increase your chance of winning - is to select a subset S containing k (k > 6) of these 49 numbers, and then play several games with choosing numbers only from S.

For example, for k = 8 and S = {1, 2, 3, 5, 8, 13, 21, 34} there are 28 possible games:
[1, 2, 3, 5, 8, 13], [1, 2, 3, 5, 8, 21], [1, 2, 3, 5, 8, 34], [1, 2, 3, 5, 13, 21], ..., [3, 5, 8, 13, 21, 34].

Your job is to write a program that reads in the number k and the set S and then prints all possible games choosing numbers only from S.

## Input Format
- Input will contain one or more test cases.
- Each test case consists of one line containing several integers separated by spaces.
- The first integer on the line will be the number k (6 < k < 13). Then k integers, specifying the set S, will follow in ascending order.
- Input will be terminated by a value of zero (0) for k.

## Output Format
- For each test case, print all possible games, each game on one line.
- The numbers of each game have to be sorted in ascending order and separated by exactly one space.
- The games themselves have to be sorted lexicographically.
- Test cases have to be separated by exactly one blank line. Do not put a blank line after the last test case.

## Solution

### Approach
Generate all combinations of 6 numbers from the given set using backtracking. Since the input is already sorted, the output will automatically be in lexicographical order.

### Python Solution

```python
def solve():
 first_case = True

 while True:
  line = input().split()
  k = int(line[0])

  if k == 0:
   break

  numbers = list(map(int, line[1:k+1]))

  if not first_case:
   print()  # Blank line between test cases
  first_case = False

  # Generate all combinations of 6 numbers
  def generate_combinations(start, current):
   if len(current) == 6:
    print(' '.join(map(str, current)))
    return

   for i in range(start, len(numbers)):
    current.append(numbers[i])
    generate_combinations(i + 1, current)
    current.pop()

  generate_combinations(0, [])

if __name__ == "__main__":
 solve()
```

### Using itertools

```python
from itertools import combinations

def solve():
 first_case = True

 while True:
  line = input().split()
  k = int(line[0])

  if k == 0:
   break

  numbers = list(map(int, line[1:k+1]))

  if not first_case:
   print()
  first_case = False

  # Generate all combinations of 6 numbers
  for combo in combinations(numbers, 6):
   print(' '.join(map(str, combo)))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(C(k, 6)) = O(k! / (6! × (k-6)!)) combinations
- **Space Complexity:** O(6) for the current combination

### Example
For k=7 and S={1, 2, 3, 4, 5, 6, 7}:
- C(7,6) = 7 combinations
- Output: all 6-element subsets in lexicographical order
