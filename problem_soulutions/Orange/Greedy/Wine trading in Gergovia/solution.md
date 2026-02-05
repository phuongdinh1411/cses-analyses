# Wine Trading in Gergovia

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Gergovia consists of one street, and every inhabitant of the city is a wine salesman. Everyone buys wine from other inhabitants of the city. Every day each inhabitant decides how much wine he wants to buy or sell. Interestingly, demand and supply is always the same, so that each inhabitant gets what he wants.

There is one problem, however: Transporting wine from one house to another results in work. Since all wines are equally good, the inhabitants of Gergovia don't care which persons they are doing trade with, they are only interested in selling or buying a specific amount of wine.

In this problem you are asked to reconstruct the trading during one day in Gergovia. For simplicity we will assume that the houses are built along a straight line with equal distance between adjacent houses. Transporting one bottle of wine from one house to an adjacent house results in one unit of work.

## Input Format
- The input consists of several test cases.
- Each test case starts with the number of inhabitants N (2 ≤ N ≤ 100000).
- The following line contains n integers ai (-1000 ≤ ai ≤ 1000).
- If ai ≥ 0, it means that the inhabitant living in the i-th house wants to buy ai bottles of wine.
- If ai < 0, he wants to sell -ai bottles of wine.
- You may assume that the numbers ai sum up to 0.
- The last test case is followed by a line containing 0.

## Output Format
For each test case print the minimum amount of work units needed so that every inhabitant has his demand fulfilled.

## Solution

### Approach
The key insight is to think about the flow of wine between adjacent houses. At each position, we track the cumulative "debt" - how much wine needs to flow past that point. The total work is the sum of absolute values of this running balance.

### Python Solution

```python
def solve():
  while True:
    n = int(input())
    if n == 0:
      break

    a = list(map(int, input().split()))

    # Calculate total work using prefix sum approach
    total_work = 0
    carry = 0  # Wine that needs to be transported to the right

    for i in range(n):
      carry += a[i]
      total_work += abs(carry)

    print(total_work)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n) per test case
- **Space Complexity:** O(n) for storing the array

### Explanation
Think of it as: between each pair of adjacent houses, some wine needs to flow. If house i has demand `a[i]`, the wine flowing between house i and i+1 is the cumulative sum up to i. The work done is |cumulative_sum| for each edge.
