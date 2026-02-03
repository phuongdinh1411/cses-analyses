# Trainsorting

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Erin is an engineer. She drives trains. She also arranges the cars within each train. She prefers to put the cars in decreasing order of weight, with the heaviest car at the front of the train.

Unfortunately, sorting train cars is not easy. One cannot simply pick up a car and place it somewhere else. It is impractical to insert a car within an existing train. A car may only be added to the beginning or end of the train.

Cars arrive at the train station in a predetermined order. When each car arrives, Erin can add it to the beginning or end of her train, or refuse to add it at all. The resulting train should be as long as possible, but the cars within it must be ordered by weight.

Given the weights of the cars in the order in which they arrive, what is the longest train that Erin can make?

## Input Format
- The first line is the number of test cases to follow.
- Each test case:
  - The first line contains an integer 0 ≤ n ≤ 2000, the number of cars.
  - Each of the following n lines contains a non-negative integer giving the weight of a car.
  - No two cars have the same weight.

## Output Format
Output a single integer giving the number of cars in the longest train that can be made with the given restrictions.

## Solution

### Approach
For each car, we can either:
1. Add it to the front (it must be heavier than current front)
2. Add it to the back (it must be lighter than current back)
3. Skip it

This can be solved using LIS (Longest Increasing Subsequence) and LDS (Longest Decreasing Subsequence):
- For each position i, find the LIS ending at i (cars that can be added to the back)
- For each position i, find the LDS ending at i (cars that can be added to the front)
- The answer is max(LIS[i] + LDS[i] - 1) for all i

### Python Solution

```python
def longest_increasing_subsequence(arr):
    """Returns array where lis[i] = length of LIS ending at index i"""
    n = len(arr)
    if n == 0:
        return []

    lis = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                lis[i] = max(lis[i], lis[j] + 1)

    return lis

def longest_decreasing_subsequence(arr):
    """Returns array where lds[i] = length of LDS ending at index i"""
    n = len(arr)
    if n == 0:
        return []

    lds = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] > arr[i]:
                lds[i] = max(lds[i], lds[j] + 1)

    return lds

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        if n == 0:
            print(0)
            continue

        weights = []
        for _ in range(n):
            weights.append(int(input()))

        # LIS[i] = longest increasing subsequence ending at i
        # This represents cars added to the back
        lis = longest_increasing_subsequence(weights)

        # LDS[i] = longest decreasing subsequence ending at i
        # This represents cars added to the front
        lds = longest_decreasing_subsequence(weights)

        # For each position i as the "pivot" car, the maximum train length is
        # LIS[i] + LDS[i] - 1 (subtract 1 because car i is counted twice)
        max_length = 0
        for i in range(n):
            max_length = max(max_length, lis[i] + lds[i] - 1)

        print(max_length)

if __name__ == "__main__":
    solve()
```

### Optimized O(n log n) Solution

```python
import bisect

def lis_lengths(arr):
    """O(n log n) LIS computation"""
    n = len(arr)
    lis = [1] * n
    tails = []

    for i, x in enumerate(arr):
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
        lis[i] = pos + 1

    return lis

def lds_lengths(arr):
    """O(n log n) LDS computation"""
    return lis_lengths([-x for x in arr])

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        if n == 0:
            print(0)
            continue

        weights = [int(input()) for _ in range(n)]

        lis = lis_lengths(weights)
        lds = lds_lengths(weights)

        max_length = max(lis[i] + lds[i] - 1 for i in range(n))
        print(max_length)

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(n²) for basic solution, O(n log n) for optimized
- **Space Complexity:** O(n)

### Key Insight
The train forms a "bitonic" sequence - increasing then decreasing. Each car can serve as the "pivot" point, with LIS to its left (back of train) and LDS to its right (front of train).
