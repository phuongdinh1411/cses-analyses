---
layout: simple
title: "Distinct Numbers - Count Unique Elements"
permalink: /problem_soulutions/sorting_and_searching/distinct_numbers_analysis
difficulty: Easy
tags: [sorting, set, counting]
cses_link: https://cses.fi/problemset/task/1621
---

# Distinct Numbers

## Problem Overview

| Aspect | Details |
|--------|---------|
| Difficulty | Easy |
| Time Limit | 1.00 s |
| Memory Limit | 512 MB |
| Input Size | n <= 2 x 10^5 |
| Key Technique | Set or Sorting |

## Learning Goals

- Use hash sets to track unique elements efficiently
- Apply sorting to group duplicates for counting
- Understand time-space tradeoffs between approaches

## Problem Statement

Given `n` integers, count how many **distinct** values exist in the array.

**Input:**
- Line 1: Integer `n` (number of elements)
- Line 2: `n` integers separated by spaces

**Output:**
- One integer: the count of distinct values

**Example:**
```
Input:
5
2 3 2 2 3

Output:
2
```
The values are 2 and 3, so the answer is 2.

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= x_i <= 10^9

## Approach 1: Hash Set

**Idea:** Add all elements to a set. The set automatically handles duplicates.

**Time Complexity:** O(n) average
**Space Complexity:** O(n)

### Python
```python
def count_distinct_set(arr):
    return len(set(arr))

# Full solution with input
n = int(input())
arr = list(map(int, input().split()))
print(len(set(arr)))
```

### C++
```cpp
#include <iostream>
#include <unordered_set>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    unordered_set<int> seen;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        seen.insert(x);
    }

    cout << seen.size() << "\n";
    return 0;
}
```

## Approach 2: Sorting

**Idea:** Sort the array. After sorting, duplicates are adjacent. Count positions where `arr[i] != arr[i-1]`.

**Time Complexity:** O(n log n)
**Space Complexity:** O(1) if sorting in-place

### Python
```python
def count_distinct_sort(arr):
    if not arr:
        return 0
    arr.sort()
    count = 1  # First element is always distinct
    for i in range(1, len(arr)):
        if arr[i] != arr[i-1]:
            count += 1
    return count

# Full solution with input
n = int(input())
arr = list(map(int, input().split()))
arr.sort()
count = 1
for i in range(1, n):
    if arr[i] != arr[i-1]:
        count += 1
print(count)
```

### C++
```cpp
#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    int arr[200001];
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    sort(arr, arr + n);

    int count = 1;  // First element is always distinct
    for (int i = 1; i < n; i++) {
        if (arr[i] != arr[i-1]) {
            count++;
        }
    }

    cout << count << "\n";
    return 0;
}
```

## Comparison: When to Use Which?

| Approach | Time | Space | Best When |
|----------|------|-------|-----------|
| Set | O(n) avg | O(n) | Need speed, memory is available |
| Sort | O(n log n) | O(1) | Memory constrained, or need sorted order later |

**Practical Notes:**
- Set approach is simpler and faster on average
- Sorting approach uses less memory
- For CSES constraints (n <= 2 x 10^5), both approaches work well

## Common Mistakes

1. **Forgetting the first element in sorting approach:**
   ```python
   # WRONG: starts count at 0
   count = 0
   for i in range(1, n):
       if arr[i] != arr[i-1]:
           count += 1

   # CORRECT: starts count at 1 (first element is always distinct)
   count = 1
   for i in range(1, n):
       if arr[i] != arr[i-1]:
           count += 1
   ```

2. **Off-by-one in loop bounds:**
   ```python
   # WRONG: will cause index error
   for i in range(n):
       if arr[i] != arr[i-1]:  # arr[-1] when i=0!

   # CORRECT: start from index 1
   for i in range(1, n):
       if arr[i] != arr[i-1]:
   ```

3. **Empty array edge case:** Always check if array is empty before processing.

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | LeetCode | Return true/false instead of count |
| [Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | LeetCode | Check duplicates within distance k |
| [Single Number](https://leetcode.com/problems/single-number/) | LeetCode | Find element that appears once |
| [Distinct Values Queries](https://cses.fi/problemset/task/1734) | CSES | Range queries for distinct count |
