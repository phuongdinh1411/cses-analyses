---
layout: simple
title: "Gray Code - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/gray_code_analysis
difficulty: Medium
tags: [bit-manipulation, gray-code, xor, recursion]
prerequisites: []
---

# Gray Code

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Bit Manipulation |
| **Time Limit** | 1 second |
| **Key Technique** | XOR Formula / Recursive Construction |
| **CSES Link** | [Gray Code](https://cses.fi/problemset/task/2205) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the mathematical formula for Gray code: `i ^ (i >> 1)`
- [ ] Apply bit manipulation to generate sequences with specific properties
- [ ] Recognize the mirror/reflection property of Gray codes
- [ ] Convert between binary and Gray code representations

---

## Problem Statement

**Problem:** Generate a Gray code sequence of n-bit strings where consecutive strings differ by exactly one bit.

**Input:**
- Line 1: An integer n (the number of bits)

**Output:**
- Print 2^n lines, each containing an n-bit Gray code string
- Any valid Gray code sequence is accepted

**Constraints:**
- 1 <= n <= 16

### Example

```
Input:
3

Output:
000
001
011
010
110
111
101
100
```

**Explanation:** Each consecutive pair differs by exactly one bit:
- 000 -> 001 (bit 0 changes)
- 001 -> 011 (bit 1 changes)
- 011 -> 010 (bit 0 changes)
- 010 -> 110 (bit 2 changes)
- 110 -> 111 (bit 0 changes)
- 111 -> 101 (bit 1 changes)
- 101 -> 100 (bit 0 changes)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we generate a sequence where adjacent values differ by exactly one bit?

The crucial insight is that **Gray code has a direct mathematical formula**: for any integer `i`, its Gray code is `i ^ (i >> 1)`. This formula naturally produces a sequence where consecutive values differ by exactly one bit.

### Why Does `i ^ (i >> 1)` Work?

Consider what happens when we go from `i` to `i + 1`:
- When incrementing, the rightmost 0 bit becomes 1, and all bits to its right (which were 1s) become 0
- The XOR with the right-shifted value "smooths" this transition, ensuring only one bit changes

```
Example: i = 5 (binary: 101)
  i     = 101
  i >> 1 = 010
  XOR    = 111  (Gray code for 5)

  i = 6 (binary: 110)
  i     = 110
  i >> 1 = 011
  XOR    = 101  (Gray code for 6)

  111 and 101 differ by exactly one bit!
```

### Alternative: Mirror Construction

Another way to understand Gray code is through the **mirror property**:
1. For n=1: [0, 1]
2. For n bits: Take (n-1)-bit Gray code, prepend 0 to all, then prepend 1 to the reversed sequence

```
n=1: [0, 1]
n=2: [00, 01] + [11, 10] = [00, 01, 11, 10]
n=3: [000, 001, 011, 010] + [110, 111, 101, 100]
```

---

## Solution 1: XOR Formula (Optimal)

### Key Insight

> **The Trick:** Gray code for integer i is simply `i ^ (i >> 1)`. This O(1) formula generates each code directly.

### Algorithm

1. Loop through all integers from 0 to 2^n - 1
2. For each integer i, compute Gray code as `i ^ (i >> 1)`
3. Convert the result to an n-bit binary string

### Dry Run Example

Let's trace through with input `n = 3`:

```
For n = 3, we generate 2^3 = 8 codes (indices 0 to 7)

i = 0: 0 ^ (0 >> 1) = 0 ^ 0 = 0 = 000
i = 1: 1 ^ (1 >> 1) = 1 ^ 0 = 1 = 001
i = 2: 2 ^ (2 >> 1) = 2 ^ 1 = 3 = 011
i = 3: 3 ^ (3 >> 1) = 3 ^ 1 = 2 = 010
i = 4: 4 ^ (4 >> 1) = 4 ^ 2 = 6 = 110
i = 5: 5 ^ (5 >> 1) = 5 ^ 2 = 7 = 111
i = 6: 6 ^ (6 >> 1) = 6 ^ 3 = 5 = 101
i = 7: 7 ^ (7 >> 1) = 7 ^ 3 = 4 = 100

Verification (adjacent codes differ by 1 bit):
000 -> 001: bit 0 flips
001 -> 011: bit 1 flips
011 -> 010: bit 0 flips
010 -> 110: bit 2 flips
110 -> 111: bit 0 flips
111 -> 101: bit 1 flips
101 -> 100: bit 0 flips
```

### Visual Diagram

```
Index (i)    Binary    i >> 1    XOR Result    Gray Code
---------    ------    ------    ----------    ---------
    0         000        000        000           000
    1         001        000        001           001
    2         010        001        011           011
    3         011        001        010           010
    4         100        010        110           110
    5         101        010        111           111
    6         110        011        101           101
    7         111        011        100           100

                 XOR operation visualized for i=6:

                   1 1 0   (i = 6)
                 ^ 0 1 1   (i >> 1 = 3)
                 -------
                   1 0 1   (Gray code = 5)
```

### Code

**Python:**
```python
def solve():
    n = int(input())
    for i in range(1 << n):  # 1 << n = 2^n
        gray = i ^ (i >> 1)
        print(format(gray, f'0{n}b'))

solve()
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    for (int i = 0; i < (1 << n); i++) {
        int gray = i ^ (i >> 1);
        for (int j = n - 1; j >= 0; j--) {
            cout << ((gray >> j) & 1);
        }
        cout << '\n';
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n) | 2^n codes, each taking O(n) to print |
| Space | O(1) | No additional data structures needed |

---

## Solution 2: Recursive Mirror Construction

### Key Insight

> **The Trick:** Build n-bit Gray code by prepending 0 to (n-1)-bit code, then prepending 1 to its reverse.

### Algorithm

1. Base case: 1-bit Gray code is ["0", "1"]
2. Recursively get (n-1)-bit Gray code
3. Prepend "0" to all codes
4. Prepend "1" to reversed codes
5. Concatenate both lists

### Code

**Python:**
```python
def gray_code_recursive(n):
    if n == 1:
        return ['0', '1']

    prev = gray_code_recursive(n - 1)

    # Prepend 0 to original, prepend 1 to reversed
    return ['0' + code for code in prev] + ['1' + code for code in reversed(prev)]

def solve():
    n = int(input())
    for code in gray_code_recursive(n):
        print(code)

solve()
```

**C++:**
```cpp
#include <bits/stdc++.h>
using namespace std;

vector<string> grayCode(int n) {
    if (n == 1) {
        return {"0", "1"};
    }

    vector<string> prev = grayCode(n - 1);
    vector<string> result;

    // Prepend 0 to original
    for (const string& code : prev) {
        result.push_back("0" + code);
    }

    // Prepend 1 to reversed
    for (int i = prev.size() - 1; i >= 0; i--) {
        result.push_back("1" + prev[i]);
    }

    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    for (const string& code : grayCode(n)) {
        cout << code << '\n';
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n) | Building 2^n strings of length n |
| Space | O(2^n * n) | Storing all Gray code strings |

---

## Common Mistakes

### Mistake 1: Wrong Bit Shift Direction

```python
# WRONG
gray = i ^ (i << 1)  # Left shift instead of right shift

# CORRECT
gray = i ^ (i >> 1)  # Right shift
```

**Problem:** Left shift produces incorrect results; the formula specifically requires right shift.
**Fix:** Always use right shift (`>>`) in the Gray code formula.

### Mistake 2: Incorrect Binary Padding

```python
# WRONG
print(bin(gray)[2:])  # Missing leading zeros

# CORRECT
print(format(gray, f'0{n}b'))  # Properly padded to n bits
```

**Problem:** Without padding, codes like 1 print as "1" instead of "001" for n=3.
**Fix:** Use format specifier to ensure n-bit output.

### Mistake 3: Off-by-One in Loop Range

```python
# WRONG
for i in range(2**n - 1):  # Missing the last code

# CORRECT
for i in range(2**n):  # Or equivalently: range(1 << n)
```

**Problem:** Missing the last Gray code in the sequence.
**Fix:** Loop should cover all 2^n values from 0 to 2^n - 1.

### Mistake 4: Printing Bits in Wrong Order (C++)

```cpp
// WRONG - prints bits in reverse order
for (int j = 0; j < n; j++) {
    cout << ((gray >> j) & 1);
}

// CORRECT - prints MSB first
for (int j = n - 1; j >= 0; j--) {
    cout << ((gray >> j) & 1);
}
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum n | n = 1 | `0` then `1` | Simplest Gray code |
| Power of 2 codes | n = 2 | 4 codes | 00, 01, 11, 10 |
| Maximum n | n = 16 | 65536 codes | Tests efficiency |
| Single bit change | Any n | Adjacent differ by 1 bit | Core Gray code property |

---

## When to Use This Pattern

### Use This Approach When:
- Generating sequences where adjacent elements differ minimally
- Encoding data for error reduction in transmission
- Solving Hamiltonian path problems on hypercubes
- Tower of Hanoi variations

### Don't Use When:
- Standard binary representation is required
- Order of bits must follow natural binary ordering
- Problem requires different adjacency constraints

### Pattern Recognition Checklist:
- [ ] Need sequence where neighbors differ by exactly 1 bit? -> **Gray code**
- [ ] Need to enumerate subsets in minimal-change order? -> **Gray code**
- [ ] Need Hamiltonian path on n-dimensional hypercube? -> **Gray code**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Bit Strings](https://cses.fi/problemset/task/1617) | Basic bit counting |
| [Two Sets](https://cses.fi/problemset/task/1092) | Understanding binary subsets |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Gray Code (LeetCode 89)](https://leetcode.com/problems/gray-code/) | Same concept, return as integers |
| [Circular Permutation](https://leetcode.com/problems/circular-permutation-in-binary-representation/) | Gray code with specific starting point |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Creating Strings](https://cses.fi/problemset/task/1622) | Permutation generation |
| [Apple Division](https://cses.fi/problemset/task/1623) | Subset enumeration with optimization |

---

## Key Takeaways

1. **The Core Idea:** Gray code for integer i is `i ^ (i >> 1)` - a simple XOR operation
2. **Time Optimization:** Direct formula gives O(1) per code vs O(2^n) backtracking
3. **Space Trade-off:** XOR approach uses O(1) space; recursive uses O(2^n)
4. **Pattern:** This belongs to the "bit manipulation" pattern family

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Write the XOR formula from memory: `i ^ (i >> 1)`
- [ ] Explain why adjacent Gray codes differ by exactly one bit
- [ ] Implement both iterative and recursive solutions
- [ ] Handle proper binary string formatting with leading zeros

---

## Additional Resources

- [CP-Algorithms: Gray Code](https://cp-algorithms.com/algebra/gray-code.html)
- [Wikipedia: Gray Code](https://en.wikipedia.org/wiki/Gray_code)
- [CSES Gray Code](https://cses.fi/problemset/task/2205) - Binary code generation
