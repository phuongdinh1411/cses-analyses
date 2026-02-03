---
layout: simple
title: "Concert Tickets"
permalink: /problem_soulutions/sorting_and_searching/concert_tickets_analysis
difficulty: Easy
tags: [sorting, multiset, binary-search, balanced-bst]
cses_link: https://cses.fi/problemset/task/1091
---

# Concert Tickets

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Assign tickets to customers based on maximum price |
| Core Operation | Find and remove largest element <= x |
| Data Structure | Multiset (balanced BST with duplicates) |
| Time Complexity | O((n + m) log n) |
| Space Complexity | O(n) |

## Learning Goals

By completing this problem, you will learn:
- **Multiset operations**: Insert, find, and delete in O(log n)
- **Finding floor element**: Largest value <= target using upper_bound
- **C++ multiset**: Standard library balanced BST with duplicate support
- **Python alternatives**: sortedcontainers.SortedList or manual binary search

## Problem Statement

There are **n** tickets with prices and **m** customers with maximum budgets.

**Process each customer in order:**
- Find the most expensive ticket with price <= customer's max budget
- If found: customer buys it (ticket removed), print the price
- If not found: print -1

**Constraints:**
- 1 <= n, m <= 2 x 10^5
- 1 <= prices, budgets <= 10^9

**Example:**
```
Input:
5 3
5 3 7 8 5
4 8 3

Output:
3
8
-1
```

## Key Insight

We need a data structure that supports three operations efficiently:
1. **Insert** all ticket prices initially
2. **Find largest <= x** for each customer's budget
3. **Remove** that element after purchase

A **multiset** (self-balancing BST) provides all three in O(log n).

### Why upper_bound, not lower_bound?

```
multiset: {3, 5, 5, 7, 8}
Customer budget: 6

lower_bound(6) -> points to 7 (first >= 6)
upper_bound(6) -> points to 7 (first > 6)

For budget 5:
lower_bound(5) -> points to first 5 (first >= 5)
upper_bound(5) -> points to 7 (first > 5)
--upper_bound(5) -> points to second 5 (largest <= 5)
```

**Rule:** `--upper_bound(x)` gives the largest element <= x.

## Visual Diagram

```
Initial multiset: {3, 5, 5, 7, 8}

Customer 1 (budget = 4):
  {3, 5, 5, 7, 8}
       ^
  upper_bound(4) points to 5
  --upper_bound(4) points to 3
  Result: 3, remove it

  Multiset after: {5, 5, 7, 8}

Customer 2 (budget = 8):
  {5, 5, 7, 8}
              ^(end)
  upper_bound(8) points to end()
  --upper_bound(8) points to 8
  Result: 8, remove it

  Multiset after: {5, 5, 7}

Customer 3 (budget = 3):
  {5, 5, 7}
   ^
  upper_bound(3) points to 5
  --upper_bound(3) = begin() - 1 (invalid!)
  Check: upper_bound(3) == begin()? Yes
  Result: -1

Output: 3, 8, -1
```

## Dry Run

| Step | Customer Budget | Multiset State | upper_bound | Result | Action |
|------|-----------------|----------------|-------------|--------|--------|
| 0 | - | {3,5,5,7,8} | - | - | Initial |
| 1 | 4 | {3,5,5,7,8} | ->5 | 3 | Remove 3 |
| 2 | 8 | {5,5,7,8} | ->end | 8 | Remove 8 |
| 3 | 3 | {5,5,7} | ->5 (begin) | -1 | No ticket |

## C++ Solution with Multiset

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    multiset<int> tickets;
    for (int i = 0; i < n; i++) {
        int price;
        cin >> price;
        tickets.insert(price);
    }

    for (int i = 0; i < m; i++) {
        int budget;
        cin >> budget;

        // Find first element > budget
        auto it = tickets.upper_bound(budget);

        if (it == tickets.begin()) {
            // No ticket <= budget exists
            cout << -1 << "\n";
        } else {
            // Move to largest element <= budget
            --it;
            cout << *it << "\n";
            tickets.erase(it);  // Remove this specific element
        }
    }

    return 0;
}
```

**Key points:**
- `upper_bound(x)` returns iterator to first element > x
- If `upper_bound == begin()`, no element <= x exists
- `--upper_bound` gives largest element <= x
- `erase(iterator)` removes exactly one element (important for duplicates)

## Python Solution with SortedList

**Note:** `sortedcontainers` is not in Python's standard library. Install with `pip install sortedcontainers`.

```python
from sortedcontainers import SortedList

def solve():
    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    budgets = list(map(int, input().split()))

    tickets = SortedList(prices)
    results = []

    for budget in budgets:
        # bisect_right returns index of first element > budget
        idx = tickets.bisect_right(budget)

        if idx == 0:
            # No ticket <= budget
            results.append(-1)
        else:
            # Index idx-1 is largest element <= budget
            ticket_price = tickets[idx - 1]
            results.append(ticket_price)
            tickets.remove(ticket_price)

    print('\n'.join(map(str, results)))

solve()
```

### Alternative: Manual Binary Search (Standard Library Only)

```python
import bisect

def solve():
    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    budgets = list(map(int, input().split()))

    tickets = sorted(prices)
    results = []

    for budget in budgets:
        idx = bisect.bisect_right(tickets, budget) - 1

        if idx < 0:
            results.append(-1)
        else:
            results.append(tickets[idx])
            tickets.pop(idx)  # O(n) operation - slower!

    print('\n'.join(map(str, results)))

solve()
```

**Warning:** The manual approach has O(n) deletion, making total complexity O(nm). This may TLE on large inputs. Use `SortedList` for O(log n) operations.

## Common Mistakes

### 1. Using lower_bound Instead of upper_bound

```cpp
// WRONG: lower_bound finds first >= x
auto it = tickets.lower_bound(budget);
--it;  // This fails when budget equals an element

// Example: multiset = {3, 5, 8}, budget = 5
// lower_bound(5) -> points to 5
// --lower_bound(5) -> points to 3 (WRONG! Should be 5)
```

### 2. Iterator Invalidation After Erase

```cpp
// WRONG: Using iterator after erase
auto it = tickets.upper_bound(budget);
--it;
tickets.erase(it);
cout << *it;  // UNDEFINED BEHAVIOR! Iterator is invalid

// CORRECT: Save value before erase
auto it = tickets.upper_bound(budget);
--it;
int price = *it;  // Save first
tickets.erase(it);
cout << price;
```

### 3. Forgetting begin() Check

```cpp
// WRONG: No check for empty result
auto it = tickets.upper_bound(budget);
--it;  // CRASH if upper_bound returns begin()!
cout << *it;

// CORRECT: Always check
auto it = tickets.upper_bound(budget);
if (it == tickets.begin()) {
    cout << -1;
} else {
    --it;
    cout << *it;
    tickets.erase(it);
}
```

### 4. Using erase(value) Instead of erase(iterator)

```cpp
// WRONG for duplicates: Removes ALL elements with this value
tickets.erase(5);  // Removes ALL 5s!

// CORRECT: Removes exactly one element
auto it = tickets.find(5);
tickets.erase(it);  // Removes only ONE 5
```

## Complexity Analysis

| Operation | Multiset (C++) | SortedList (Python) | List + bisect (Python) |
|-----------|----------------|---------------------|------------------------|
| Insert | O(log n) | O(log n) | O(n) |
| Find <= x | O(log n) | O(log n) | O(log n) |
| Delete | O(log n) | O(log n) | O(n) |
| **Total** | **O((n+m) log n)** | **O((n+m) log n)** | **O(nm)** |

## Related Problems

- [CSES - Apartments](https://cses.fi/problemset/task/1084) - Similar matching with tolerance
- [CSES - Traffic Lights](https://cses.fi/problemset/task/1163) - Multiset for interval tracking
- [LeetCode 729 - My Calendar I](https://leetcode.com/problems/my-calendar-i/) - Interval insertion with overlap check
