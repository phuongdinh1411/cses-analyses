---
layout: simple
title: "Longest Common Subsequence - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/longest_common_subsequence_analysis
difficulty: Medium
tags: [dp, string-dp, 2d-dp, lcs]
prerequisites: [edit_distance]
cses_link: https://cses.fi/problemset/task/3403
---

# Longest Common Subsequence (LCS)

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find the length of the longest common subsequence between two strings |
| Input | Two strings s1 and s2 |
| Output | Length of the longest common subsequence |
| Constraints | 1 <= |s1|, |s2| <= 5000 |
| Time Complexity | O(n * m) |
| Space Complexity | O(n * m), optimizable to O(min(n, m)) |

## Learning Goals

- **LCS Pattern**: The fundamental pattern for finding common subsequences
- **2D String DP**: Building a DP table indexed by positions in two strings
- **Subsequence Reconstruction**: Backtracking to find the actual LCS

## Problem Statement

Given two strings, find the length of their longest common subsequence. A subsequence is derived by deleting some (or no) elements without changing the order of remaining elements.

### Example

```
s1 = "ABCD", s2 = "ABDC"

Common subsequences: "A", "AB", "ABD" (length 3), "ABC" (length 3)
Answer: 3 (LCS can be "ABD" or "ABC")
```

## Intuition

At each position when comparing characters:
1. **Characters Match**: Extend LCS by 1 from dp[i-1][j-1]
2. **Characters Differ**: Take max(exclude s1[i-1], exclude s2[j-1])

## DP State

```
dp[i][j] = length of LCS of s1[0..i-1] and s2[0..j-1]
```

## State Transition

```
If s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1     # Match: extend LCS

Else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # Take best of excluding either char
```

## Base Cases

```
dp[i][0] = 0    # LCS with empty string is 0
dp[0][j] = 0    # LCS with empty string is 0
```

## Visual DP Table

For s1 = "ABCD" and s2 = "ABDC":

```
        ""   A    B    D    C
    +----+----+----+----+----+
 "" |  0 |  0 |  0 |  0 |  0 |
    +----+----+----+----+----+
  A |  0 |  1 |  1 |  1 |  1 |
    +----+----+----+----+----+
  B |  0 |  1 |  2 |  2 |  2 |
    +----+----+----+----+----+
  C |  0 |  1 |  2 |  2 |  3 |
    +----+----+----+----+----+
  D |  0 |  1 |  2 |  3 |  3 |
    +----+----+----+----+----+

Answer: dp[4][4] = 3
```

## Reconstructing the Actual LCS

Backtrack from dp[m][n]:
1. If s1[i-1] == s2[j-1]: add char, move to (i-1, j-1)
2. Else if dp[i-1][j] > dp[i][j-1]: move to (i-1, j)
3. Else: move to (i, j-1)
4. Stop at i=0 or j=0, then reverse result

### Backtracking Example

For s1="ABCD", s2="ABDC", from dp[4][4]=3:
```
(4,4): D!=C, dp[3][4]=dp[4][3]=3 -> go (4,3)
(4,3): D==D -> add 'D', go (3,2)
(3,2): C!=B, dp[2][2]>dp[3][1] -> go (2,2)
(2,2): B==B -> add 'B', go (1,1)
(1,1): A==A -> add 'A', go (0,0)
Result reversed: "ABD"
```

## Detailed Dry Run

s1 = "ACE", s2 = "ABCDE":

```
dp[1][1]: A==A -> dp[0][0]+1 = 1
dp[1][2]: A!=B -> max(0,1) = 1
dp[1][3]: A!=C -> max(0,1) = 1
dp[2][1]: C!=A -> max(1,0) = 1
dp[2][2]: C!=B -> max(1,1) = 1
dp[2][3]: C==C -> dp[1][2]+1 = 2
dp[3][1]: E!=A -> max(1,0) = 1
dp[3][2]: E!=B -> max(1,1) = 1
dp[3][3]: E!=C -> max(2,1) = 2
dp[3][4]: E!=D -> max(2,2) = 2
dp[3][5]: E==E -> dp[2][4]+1 = 3

Final: dp[3][5] = 3 (LCS = "ACE")
```

## Implementation

### Python Solution

```python
def lcs_length(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]


def lcs_string(s1: str, s2: str) -> str:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(lcs))


if __name__ == "__main__":
    s1, s2 = input(), input()
    print(lcs_length(s1, s2))
```

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

int lcsLength(const string& s1, const string& s2) {
    int m = s1.length(), n = s2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1])
                dp[i][j] = dp[i-1][j-1] + 1;
            else
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
        }
    }
    return dp[m][n];
}

string lcsString(const string& s1, const string& s2) {
    int m = s1.length(), n = s2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1])
                dp[i][j] = dp[i-1][j-1] + 1;
            else
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
        }
    }

    // Backtrack
    string lcs;
    int i = m, j = n;
    while (i > 0 && j > 0) {
        if (s1[i-1] == s2[j-1]) {
            lcs += s1[i-1];
            i--; j--;
        } else if (dp[i-1][j] > dp[i][j-1]) {
            i--;
        } else {
            j--;
        }
    }
    reverse(lcs.begin(), lcs.end());
    return lcs;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    string s1, s2;
    cin >> s1 >> s2;
    cout << lcsLength(s1, s2) << "\n";
    return 0;
}
```

### Space-Optimized Solution (Python)

```python
def lcs_length_optimized(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    m, n = len(s1), len(s2)

    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]
```

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| 0-indexed confusion | Accessing s1[i] instead of s1[i-1] | DP is 1-based, strings are 0-based |
| Wrong base cases | Forgetting dp[i][0]=dp[0][j]=0 | Base cases are all 0 |
| Confusing with Edit Distance | Using min instead of max | LCS maximizes, Edit Distance minimizes |
| Wrong backtracking | Not reversing result | Build backward, then reverse |

## Connection to Edit Distance

LCS and Edit Distance are closely related:
```
Edit Distance (deletions only) = len(s1) + len(s2) - 2 * LCS(s1, s2)
```

| Aspect | LCS | Edit Distance |
|--------|-----|---------------|
| Goal | Maximize | Minimize |
| Match | dp[i-1][j-1] + 1 | dp[i-1][j-1] (no cost) |
| No match | max(dp[i-1][j], dp[i][j-1]) | 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) |
| Base case | 0 | Length of other string |

## Related Problems

**LeetCode:**
- [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) - Same problem
- [583. Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) - Uses LCS
- [1035. Uncrossed Lines](https://leetcode.com/problems/uncrossed-lines/) - LCS in disguise
- [72. Edit Distance](https://leetcode.com/problems/edit-distance/) - Related string DP

## Key Takeaways

1. **State**: dp[i][j] = LCS of prefixes s1[0..i-1] and s2[0..j-1]
2. **Transition**: Match extends diagonal, no match takes max of excluding either
3. **Reconstruction**: Backtrack from dp[m][n], add on matches, follow larger neighbor otherwise
4. **Relationship**: LCS is foundational for Edit Distance and many string problems
