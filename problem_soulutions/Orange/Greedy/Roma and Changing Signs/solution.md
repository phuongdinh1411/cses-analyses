# Roma and Changing Signs

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

## Problem Statement

Roma works in a company that sells TVs. Now he has to prepare a report for the last year.

Roma has got a list of the company's incomes. The list is a sequence that consists of n integers. The total income of the company is the sum of all integers in sequence. Roma decided to perform exactly k changes of signs of several numbers in the sequence. He can also change the sign of a number one, two or more times.

The operation of changing a number's sign is the operation of multiplying this number by -1.

Help Roma perform the changes so as to make the total income of the company (the sum of numbers in the resulting sequence) maximum. Note that Roma should perform exactly k changes.

## Input Format
- The first line contains two integers n and k (1 ≤ n, k ≤ 10^5), showing how many numbers are in the sequence and how many swaps are to be made.
- The second line contains a non-decreasing sequence, consisting of n integers ai (|ai| ≤ 10^4). The numbers in the lines are separated by single spaces. Please note that the given sequence is sorted in non-decreasing order.

## Output Format
In the single line print the answer to the problem - the maximum total income that we can obtain after exactly k changes.

## Example
```
Input:
3 2
-1 -1 1

Output:
3
```
Array: [-1, -1, 1], k=2. Flip both negatives: [1, 1, 1]. Sum = 3. If k=3, flip the smallest element back: sum would be 1+1-1=1.

## Solution

### Approach
1. First, flip all negative numbers to positive (starting from the most negative) as long as we have operations left.
2. After flipping all negatives, if we still have operations left:
   - If remaining operations is even, we can flip any number twice (no net change)
   - If remaining operations is odd, flip the smallest absolute value number once

### Python Solution

```python
def solve():
  n, k = map(int, input().split())
  a = list(map(int, input().split()))

  # Flip negative numbers starting from smallest (most negative)
  for i in range(n):
    if a[i] < 0 and k > 0:
      a[i] = -a[i]
      k -= 1

  # Sort again to find the minimum element
  a.sort()

  # If k is odd, flip the smallest element
  if k % 2 == 1:
    a[0] = -a[0]

  print(sum(a))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log n) due to sorting
- **Space Complexity:** O(n) for storing the array
