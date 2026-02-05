---
layout: simple
title: "Apartments - Greedy Matching with Two Pointers"
permalink: /problem_soulutions/sorting_and_searching/apartments_analysis
difficulty: Easy
tags: [sorting, two-pointers, greedy]
cses_link: https://cses.fi/problemset/task/1084
---

# Apartments - Greedy Matching with Two Pointers

## Problem Overview

| Attribute       | Details                                              |
|-----------------|------------------------------------------------------|
| Difficulty      | Easy                                                 |
| Category        | Sorting and Searching                                |
| Technique       | Two Pointers, Greedy                                 |
| Time Complexity | O(n log n + m log m)                                 |
| Space Complexity| O(1) (in-place sorting)                              |
| CSES Link       | [Apartments](https://cses.fi/problemset/task/1084)   |

## Learning Goals

By solving this problem, you will learn:
1. **Two-pointer technique**: How to efficiently traverse two sorted arrays simultaneously
2. **Greedy matching**: Why matching the smallest available option first leads to an optimal solution

## Problem Statement

There are **n applicants** and **m apartments**. Each applicant has a desired apartment size, and each apartment has an actual size. An applicant accepts an apartment if its size is within **k** units of their desired size.

**Goal**: Maximize the number of applicants who get an apartment.

**Input**:
- Line 1: Three integers n, m, k (applicants, apartments, tolerance)
- Line 2: n integers representing desired sizes
- Line 3: m integers representing apartment sizes

**Output**: Maximum number of successful matches

**Constraints**:
- 1 <= n, m <= 2 x 10^5
- 0 <= k <= 10^9
- 1 <= desired_size, apartment_size <= 10^9

**Example**:
```
Input:
4 3 5
60 45 80 60
30 60 75

Output:
2
```

## Key Insight

**Sort both arrays. Then greedily match the smallest unmatched applicant with the smallest suitable apartment.**

Why does greedy work here? If we match a larger apartment to a smaller applicant, we might "waste" it - a larger applicant who could only use that apartment gets nothing. By always using the smallest suitable apartment, we leave larger apartments available for applicants who need them.

## Two-Pointer Algorithm

After sorting both arrays, use two pointers `i` (applicants) and `j` (apartments):

```
For each comparison of applicant[i] and apartment[j]:

1. If apartment[j] < applicant[i] - k  (apartment too small)
   -> Move apartment pointer: j++
   -> This apartment is too small for current and all future applicants

2. If apartment[j] > applicant[i] + k  (apartment too big)
   -> Move applicant pointer: i++
   -> Current applicant cannot be satisfied (all remaining apartments are bigger)

3. If |apartment[j] - applicant[i]| <= k  (match found!)
   -> Increment count, move both pointers: i++, j++
```

## Visual Diagram: Pointer Movement

```
Sorted applicants: [45, 60, 60, 80]    k = 5
Sorted apartments: [30, 60, 75]

Step 1: i=0, j=0
  Applicant 45 wants [40, 50]
  Apartment 30 < 40 (too small)
  -> j++ (skip apartment)

         [45, 60, 60, 80]
          ^i
         [30, 60, 75]
              ^j

Step 2: i=0, j=1
  Applicant 45 wants [40, 50]
  Apartment 60 > 50 (too big)
  -> i++ (skip applicant, no suitable apartment)

         [45, 60, 60, 80]
              ^i
         [30, 60, 75]
              ^j

Step 3: i=1, j=1
  Applicant 60 wants [55, 65]
  Apartment 60 in range -> MATCH!
  -> i++, j++, count=1

         [45, 60, 60, 80]
                  ^i
         [30, 60, 75]
                  ^j

Step 4: i=2, j=2
  Applicant 60 wants [55, 65]
  Apartment 75 > 65 (too big)
  -> i++ (skip applicant)

         [45, 60, 60, 80]
                      ^i
         [30, 60, 75]
                  ^j

Step 5: i=3, j=2
  Applicant 80 wants [75, 85]
  Apartment 75 in range -> MATCH!
  -> i++, j++, count=2

Pointers exhausted. Result: 2 matches
```

## Dry Run

| Step | i | j | Applicant | Apt | Range       | Condition           | Action         | Count |
|------|---|---|-----------|-----|-------------|---------------------|----------------|-------|
| 1    | 0 | 0 | 45        | 30  | [40, 50]    | 30 < 40 (too small) | j++            | 0     |
| 2    | 0 | 1 | 45        | 60  | [40, 50]    | 60 > 50 (too big)   | i++            | 0     |
| 3    | 1 | 1 | 60        | 60  | [55, 65]    | 60 in range         | i++, j++, cnt++| 1     |
| 4    | 2 | 2 | 60        | 75  | [55, 65]    | 75 > 65 (too big)   | i++            | 1     |
| 5    | 3 | 2 | 80        | 75  | [75, 85]    | 75 in range         | i++, j++, cnt++| 2     |
| 6    | 4 | 3 | -         | -   | -           | i >= n, j >= m      | STOP           | 2     |

**Final Answer: 2**

## Python Solution

```python
def solve():
    n, m, k = map(int, input().split())
    applicants = sorted(map(int, input().split()))
    apartments = sorted(map(int, input().split()))

    count = 0
    i = j = 0

    while i < n and j < m:
        if apartments[j] < applicants[i] - k:
            # Apartment too small, try next apartment
            j += 1
        elif apartments[j] > applicants[i] + k:
            # Apartment too big, skip this applicant
            i += 1
        else:
            # Match found
            count += 1
            i += 1
            j += 1

    print(count)

solve()
```

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Not sorting arrays | Two-pointer technique requires sorted input | Always sort both arrays first |
| Moving wrong pointer when apartment is too big | Moving `j++` would skip apartments that might match later applicants | Move `i++` to skip the current applicant |
| Moving wrong pointer when apartment is too small | Moving `i++` wastes the apartment | Move `j++` since this apartment is useless for all remaining (larger) applicants |
| Using `abs()` only without directional checks | Works but misses optimization opportunity | Check direction to know which pointer to move |
| Off-by-one in tolerance check | Using `< k` instead of `<= k` | Condition should be `<= k` (inclusive) |

## Complexity Analysis

**Time Complexity**: O(n log n + m log m)
- Sorting applicants: O(n log n)
- Sorting apartments: O(m log m)
- Two-pointer traversal: O(n + m)
- Total: O(n log n + m log m) (sorting dominates)

**Space Complexity**: O(1)
- In-place sorting (or O(n + m) if sort creates copies)
- Only constant extra variables for pointers and count

## Why Greedy is Optimal

The greedy approach works because:
1. **No benefit in skipping**: If an apartment fits the current applicant, using it now is never worse than saving it
2. **Smallest-first is safe**: A smaller apartment that fits applicant A might not fit applicant B (who wants bigger), but a larger apartment would fit both - so use smaller ones first
3. **Exchange argument**: Any optimal solution can be transformed into our greedy solution without reducing matches

## Related Problems

- [CSES Ferris Wheel](https://cses.fi/problemset/task/1090) - Similar two-pointer matching
- [CSES Concert Tickets](https://cses.fi/problemset/task/1091) - Greedy matching with multiset
- [LeetCode 455: Assign Cookies](https://leetcode.com/problems/assign-cookies/) - Nearly identical problem
