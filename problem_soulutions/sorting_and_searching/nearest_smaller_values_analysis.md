---
layout: simple
title: "Nearest Smaller Values - Monotonic Stack Problem"
permalink: /problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis
difficulty: Easy
tags: [monotonic-stack, stack, array]
---

# Nearest Smaller Values

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 1645 - Nearest Smaller Values](https://cses.fi/problemset/task/1645) |
| **Difficulty** | Easy |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Monotonic Stack (Increasing) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when and why to use a monotonic stack
- [ ] Maintain a stack in increasing order for efficient lookups
- [ ] Recognize the "nearest smaller/greater element" pattern
- [ ] Analyze why each element is pushed and popped at most once (amortized O(n))

---

## Problem Statement

**Problem:** Given an array of n integers, for each element find the nearest smaller element to its left. If no such element exists, output 0.

**Input:**
- Line 1: Integer n (size of array)
- Line 2: n space-separated integers representing the array

**Output:**
- n integers: For each position i, print the position (1-indexed) of the nearest smaller element to the left, or 0 if none exists.

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= a[i] <= 10^9

### Example

```
Input:
8
2 5 1 4 8 3 2 5

Output:
0 1 0 3 4 3 3 7
```

**Explanation:**
- Position 1 (value 2): No element to the left -> 0
- Position 2 (value 5): Element at position 1 (value 2) is smaller -> 1
- Position 3 (value 1): No smaller element to the left -> 0
- Position 4 (value 4): Element at position 3 (value 1) is smaller -> 3
- Position 5 (value 8): Element at position 4 (value 4) is smaller -> 4
- Position 6 (value 3): Element at position 3 (value 1) is smaller -> 3
- Position 7 (value 2): Element at position 3 (value 1) is smaller -> 3
- Position 8 (value 5): Element at position 7 (value 2) is smaller -> 7

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why can we use a stack here instead of checking all previous elements?

The crucial insight is that we only need to maintain **candidates** that could be the answer for future elements. If element A is larger than element B and A comes before B, then A will **never** be the answer for any future element - B will always be a better candidate (smaller and closer).

### Breaking Down the Problem

1. **What are we looking for?** The nearest (closest) smaller element to the left of each position.
2. **What information do we have?** All elements to the left of current position.
3. **What's the relationship?** Elements that are larger than or equal to the current element can never be the answer for this or any future element.

### The Monotonic Stack Insight

Think of it like a "bouncer at a club":
- New element arrives and checks the stack from top
- Any element >= current element gets "kicked out" (they'll never be useful again)
- The remaining top (if any) is our answer
- Then the new element joins the stack

This maintains a **strictly increasing** stack from bottom to top.

---

## Solution 1: Brute Force

### Idea

For each element, scan all previous elements from right to left and find the first one that is smaller.

### Algorithm

1. For each position i from 0 to n-1
2. Scan positions j from i-1 down to 0
3. Return the first j where arr[j] < arr[i]
4. If no such j exists, answer is 0

### Code

```python
def solve_brute_force(n, arr):
    """
    Brute force: Check all previous elements.

    Time: O(n^2)
    Space: O(1)
    """
    result = []
    for i in range(n):
        found = 0
        for j in range(i - 1, -1, -1):
            if arr[j] < arr[i]:
                found = j + 1  # 1-indexed
                break
        result.append(found)
    return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | For each element, potentially scan all previous elements |
| Space | O(1) | No extra space besides output |

### Why This Works (But Is Slow)

Correctness is guaranteed since we check every candidate. However, with n up to 2 x 10^5, O(n^2) = 4 x 10^10 operations is far too slow.

---

## Solution 2: Monotonic Stack (Optimal)

### Key Insight

> **The Trick:** Maintain a stack of (index, value) pairs in strictly increasing order of values. Elements that are >= current element will never be useful again, so we can safely remove them.

### Why Monotonic Stack Works

Consider processing element X:
1. Any stack element >= X cannot be the "nearest smaller" for X
2. Any stack element >= X cannot be the "nearest smaller" for any future element Y either, because:
   - If Y > X: X would be a better answer (smaller and closer)
   - If Y <= X: That element is still >= Y, so it's not smaller

Therefore, we can safely pop all elements >= X before checking the answer.

### Algorithm

1. Initialize empty stack (stores pairs of index and value)
2. For each element at position i:
   - Pop all stack elements with value >= arr[i]
   - If stack is non-empty, top element's index is our answer
   - Otherwise, answer is 0
   - Push current (i, arr[i]) onto stack
3. Output all answers

### Dry Run Example

Let's trace through `arr = [2, 5, 1, 4, 8, 3, 2, 5]`:

```
Stack format: [(index, value), ...]  (index is 1-based for clarity)

Step 1: Process arr[0] = 2
  Stack: []
  Pop condition: nothing to pop
  Answer: 0 (stack empty)
  Push (1, 2)
  Stack after: [(1, 2)]
  Output: [0]

Step 2: Process arr[1] = 5
  Stack: [(1, 2)]
  Pop condition: 2 < 5, don't pop
  Answer: 1 (top is (1, 2))
  Push (2, 5)
  Stack after: [(1, 2), (2, 5)]
  Output: [0, 1]

Step 3: Process arr[2] = 1
  Stack: [(1, 2), (2, 5)]
  Pop condition: 5 >= 1, pop (2, 5)
  Pop condition: 2 >= 1, pop (1, 2)
  Answer: 0 (stack empty)
  Push (3, 1)
  Stack after: [(3, 1)]
  Output: [0, 1, 0]

Step 4: Process arr[3] = 4
  Stack: [(3, 1)]
  Pop condition: 1 < 4, don't pop
  Answer: 3 (top is (3, 1))
  Push (4, 4)
  Stack after: [(3, 1), (4, 4)]
  Output: [0, 1, 0, 3]

Step 5: Process arr[4] = 8
  Stack: [(3, 1), (4, 4)]
  Pop condition: 4 < 8, don't pop
  Answer: 4 (top is (4, 4))
  Push (5, 8)
  Stack after: [(3, 1), (4, 4), (5, 8)]
  Output: [0, 1, 0, 3, 4]

Step 6: Process arr[5] = 3
  Stack: [(3, 1), (4, 4), (5, 8)]
  Pop condition: 8 >= 3, pop (5, 8)
  Pop condition: 4 >= 3, pop (4, 4)
  Pop condition: 1 < 3, don't pop
  Answer: 3 (top is (3, 1))
  Push (6, 3)
  Stack after: [(3, 1), (6, 3)]
  Output: [0, 1, 0, 3, 4, 3]

Step 7: Process arr[6] = 2
  Stack: [(3, 1), (6, 3)]
  Pop condition: 3 >= 2, pop (6, 3)
  Pop condition: 1 < 2, don't pop
  Answer: 3 (top is (3, 1))
  Push (7, 2)
  Stack after: [(3, 1), (7, 2)]
  Output: [0, 1, 0, 3, 4, 3, 3]

Step 8: Process arr[7] = 5
  Stack: [(3, 1), (7, 2)]
  Pop condition: 2 < 5, don't pop
  Answer: 7 (top is (7, 2))
  Push (8, 5)
  Stack after: [(3, 1), (7, 2), (8, 5)]
  Output: [0, 1, 0, 3, 4, 3, 3, 7]

Final Answer: 0 1 0 3 4 3 3 7
```

### Visual Diagram

```
Array: [2, 5, 1, 4, 8, 3, 2, 5]
Index:  1  2  3  4  5  6  7  8

Stack Evolution (showing values):

Step 1: [2]                    -> Answer: 0
Step 2: [2, 5]                 -> Answer: 1 (2 < 5)
Step 3: [1]                    -> Answer: 0 (2,5 popped)
Step 4: [1, 4]                 -> Answer: 3 (1 < 4)
Step 5: [1, 4, 8]              -> Answer: 4 (4 < 8)
Step 6: [1, 3]                 -> Answer: 3 (4,8 popped, 1 < 3)
Step 7: [1, 2]                 -> Answer: 3 (3 popped, 1 < 2)
Step 8: [1, 2, 5]              -> Answer: 7 (2 < 5)

Note: Stack always maintains STRICTLY INCREASING order
      [1] < [2] < [5] at the end
```

### Code (Python)

```python
import sys
from typing import List

def solve(n: int, arr: List[int]) -> List[int]:
    """
    Find nearest smaller element to the left using monotonic stack.

    Time: O(n) - each element pushed and popped at most once
    Space: O(n) - stack storage
    """
    result = []
    stack = []  # stores (index, value)

    for i in range(n):
        # Pop elements >= current (they'll never be useful again)
        while stack and stack[-1][1] >= arr[i]:
            stack.pop()

        # Top of stack is nearest smaller, or 0 if empty
        if stack:
            result.append(stack[-1][0] + 1)  # 1-indexed
        else:
            result.append(0)

        # Push current element
        stack.append((i, arr[i]))

    return result


def main():
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    arr = list(map(int, input_data[1:n+1]))

    result = solve(n, arr)
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    // Stack stores pairs: (index, value)
    stack<pair<int, int>> st;

    for (int i = 0; i < n; i++) {
        // Pop elements >= current
        while (!st.empty() && st.top().second >= arr[i]) {
            st.pop();
        }

        // Output answer (1-indexed, or 0 if none)
        if (st.empty()) {
            cout << 0;
        } else {
            cout << st.top().first + 1;
        }

        if (i < n - 1) cout << " ";

        // Push current element
        st.push({i, arr[i]});
    }

    cout << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each element is pushed once and popped at most once |
| Space | O(n) | Stack can hold up to n elements |

---

## Common Mistakes

### Mistake 1: Wrong Pop Condition

```python
# WRONG: Using > instead of >=
while stack and stack[-1][1] > arr[i]:
    stack.pop()
```

**Problem:** If stack top equals current element, it's NOT smaller, so it shouldn't be the answer.
**Fix:** Use `>=` to pop elements that are greater than OR equal to current.

### Mistake 2: Forgetting to Push Current Element

```python
# WRONG: Missing the push step
while stack and stack[-1][1] >= arr[i]:
    stack.pop()

if stack:
    result.append(stack[-1][0] + 1)
else:
    result.append(0)

# MISSING: stack.append((i, arr[i]))
```

**Problem:** Current element could be the nearest smaller for future elements.
**Fix:** Always push current element after finding its answer.

### Mistake 3: Off-by-One Index Error

```python
# WRONG: 0-indexed output
result.append(stack[-1][0])

# CORRECT: 1-indexed output as required
result.append(stack[-1][0] + 1)
```

**Problem:** CSES expects 1-indexed positions in output.
**Fix:** Add 1 when outputting the index.

### Mistake 4: Checking Before Popping All Invalid Elements

```python
# WRONG: Checking answer before popping all >= elements
if stack and stack[-1][1] < arr[i]:
    result.append(stack[-1][0] + 1)
else:
    while stack and stack[-1][1] >= arr[i]:
        stack.pop()
    # Now the answer check is in the wrong place!
```

**Problem:** You might return an element that isn't actually smaller.
**Fix:** Always pop ALL invalid elements first, then check the answer.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, arr=[5]` | `0` | No elements to the left |
| All same values | `n=3, arr=[4,4,4]` | `0 0 0` | Equal is not smaller |
| Strictly increasing | `n=4, arr=[1,2,3,4]` | `0 1 2 3` | Previous element is always smaller |
| Strictly decreasing | `n=4, arr=[4,3,2,1]` | `0 0 0 0` | Stack gets cleared each time |
| Minimum at start | `n=4, arr=[1,5,3,4]` | `0 1 1 3` | First element answers many |
| Minimum at end | `n=4, arr=[5,3,4,1]` | `0 0 2 0` | Last element clears stack |

---

## When to Use This Pattern

### Use Monotonic Stack When:
- Finding **nearest smaller/greater element** to left or right
- Computing **span** problems (stock span, histogram area)
- Problems involving **next greater element** or **previous smaller element**
- Optimizing nested loops where inner loop searches for first element satisfying a condition

### Don't Use When:
- You need the k-th smallest, not the nearest (use heap or sorting)
- The "nearest" condition has additional constraints (may need different approach)
- You need to answer queries on subarrays (may need segment tree)

### Pattern Recognition Checklist:
- [ ] Looking for nearest element with some comparison property? -> **Monotonic Stack**
- [ ] Need to process elements left-to-right maintaining some order? -> **Monotonic Stack**
- [ ] Brute force has nested loop where inner finds first matching element? -> **Monotonic Stack**

### Types of Monotonic Stacks

| Type | Pop Condition | Use Case |
|------|---------------|----------|
| Increasing (this problem) | `stack.top() >= current` | Nearest smaller to left |
| Decreasing | `stack.top() <= current` | Nearest greater to left |
| Non-decreasing | `stack.top() > current` | Nearest smaller or equal |
| Non-increasing | `stack.top() < current` | Nearest greater or equal |

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Basic stack operations |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | Finding greater instead of smaller |
| [Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | Circular array variant |
| [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Next greater with distance calculation |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Using both left and right boundaries |
| [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | 2D extension of histogram problem |
| [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | Counting subarrays using stack bounds |
| [Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges/) | Combining min and max monotonic stacks |

---

## Key Takeaways

1. **The Core Idea:** Maintain a stack of candidates in monotonic order; elements that violate the order will never be useful again.
2. **Time Optimization:** From O(n^2) brute force to O(n) because each element is pushed and popped at most once.
3. **Space Trade-off:** We use O(n) space for the stack to achieve linear time.
4. **Pattern:** This is the classic "Monotonic Stack" pattern for nearest element queries.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why the stack maintains increasing order
- [ ] Prove the O(n) time complexity (amortized analysis)
- [ ] Implement in both Python and C++ in under 10 minutes
- [ ] Solve the "nearest greater" variant by changing one comparison

---

## Additional Resources

- [CP-Algorithms: Stack](https://cp-algorithms.com/data_structures/stack_queue_modification.html)
- [CSES Problem Set](https://cses.fi/problemset/)
- [LeetCode Monotonic Stack Problems](https://leetcode.com/tag/monotonic-stack/)
