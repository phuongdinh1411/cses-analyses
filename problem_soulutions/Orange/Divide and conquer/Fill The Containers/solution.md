# Fill The Containers

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

A conveyor belt has a number of vessels of different capacities each filled to the brim with milk. The milk from conveyor belt is to be filled into 'm' containers. The constraints are:

1. Whenever milk from a vessel is poured into a container, the milk in the vessel must be completely poured into that container only. That is, milk from the same vessel cannot be poured into different containers.
2. The milk from the vessel must be poured into the container in order which they appear in the conveyor belt. That is, you cannot randomly pick up a vessel from the conveyor belt and fill the container.
3. The ith container must be filled with milk only from those vessels that appear earlier to those that fill jth container, for all i < j.

Given the number of containers 'm', you have to fill the containers with milk from all the vessels, without leaving any milk in the vessel. Your job is to find out the minimal possible capacity of the container which has maximal capacity.

## Input Format
- Each test case consists of 2 lines.
- First line: n (1 ≤ n ≤ 1000) number of vessels and m (1 ≤ m ≤ 1000000) number of containers.
- Second line: capacity c (1 ≤ c ≤ 1000000) of each vessel in order.
- Multiple test cases terminated by EOF.

## Output Format
For each test case, print the minimal possible capacity of the container with maximal capacity.

## Example
```
Input:
5 3
1 2 3 4 5

Output:
6
```
5 vessels with capacities [1,2,3,4,5] need to be distributed into 3 containers. Optimal distribution: container 1 gets {1,2,3} = 6, container 2 gets {4} = 4, container 3 gets {5} = 5. The maximum container capacity is 6, which is minimal.

## Solution

### Approach
This is a classic binary search on answer problem. We binary search on the maximum container capacity and check if it's feasible to distribute all milk into m containers with that capacity.

- Lower bound: maximum single vessel capacity (can't split a vessel)
- Upper bound: sum of all vessels (one container takes all)

### Python Solution

```python
import sys

def can_fill(vessels, max_capacity, m):
    """Check if we can fill all vessels into m containers with given max capacity"""
    containers_used = 1
    current_sum = 0

    for vessel in vessels:
        if vessel > max_capacity:
            return False

        if current_sum + vessel > max_capacity:
            containers_used += 1
            current_sum = vessel
            if containers_used > m:
                return False
        else:
            current_sum += vessel

    return True

def solve():
    for line in sys.stdin:
        parts = line.split()
        n, m = int(parts[0]), int(parts[1])

        vessels = list(map(int, input().split()))

        # Binary search on maximum container capacity
        low, high = max(vessels), sum(vessels)
        result = high

        while low <= high:
            mid = (low + high) // 2

            if can_fill(vessels, mid, m):
                result = mid
                high = mid - 1
            else:
                low = mid + 1

        print(result)

if __name__ == "__main__":
    solve()
```

### Alternative Solution

```python
def min_max_capacity(vessels, m):
  def feasible(capacity):
    containers = 1
    current = 0

    for v in vessels:
      if v > capacity:
        return False
      if current + v > capacity:
        containers += 1
        current = v
      else:
        current += v

    return containers <= m

  lo, hi = max(vessels), sum(vessels)

  while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
      hi = mid
    else:
      lo = mid + 1

  return lo

def solve():
  import sys
  lines = sys.stdin.read().strip().split('\n')
  i = 0

  while i < len(lines):
    n, m = map(int, lines[i].split())
    vessels = list(map(int, lines[i + 1].split()))
    print(min_max_capacity(vessels, m))
    i += 2

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log S) where S is the sum of all vessel capacities
- **Space Complexity:** O(n) for storing vessel capacities

### Key Insight
This is the "minimize the maximum" pattern, which is typically solved with binary search. The key insight is that if we can fill containers with a maximum capacity of X, we can definitely fill them with any capacity > X. This monotonicity allows binary search.

The check function greedily fills each container until it would overflow, then starts a new container. If we use more than m containers, the capacity is too small.
