---
layout: simple
title: "Knuth-Morris-Pratt"
permalink: /problem_soulutions/Orange/Knuth-Morris-Pratt/
---
# Knuth-Morris-Pratt

Problems involving string pattern matching using the KMP algorithm, which achieves linear time complexity through preprocessing of the pattern.

## Problems

### Find String Roots

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

The Nth root of a string S is a string T such that T concatenated N times equals S. For example:
- S = "abcabcabcabc" has 4th root T = "abc"
- For N = 2, the 2nd root is "abcabc"
- For N = 1, any string S is its own 1st root

Find the maximum N such that the Nth root of S exists.

#### Input Format
- Multiple test cases, one per line
- Each line: a non-empty string S (≤ 10⁵ characters)
- Input ends with "*"

#### Output Format
For each test case, print the greatest N such that the Nth root exists.

#### Solution

##### Approach
Use KMP failure function. If the string has period P, then N = len(S) / P.
The period P = len(S) - failure[len(S)-1].
N is valid only if len(S) is divisible by P.

##### Python Solution

```python
def compute_failure(s):
    """KMP failure function"""
    n = len(s)
    fail = [0] * n

    for i in range(1, n):
        j = fail[i - 1]
        while j > 0 and s[i] != s[j]:
            j = fail[j - 1]
        if s[i] == s[j]:
            j += 1
        fail[i] = j

    return fail

def solve():
    while True:
        s = input().strip()
        if s == '*':
            break

        n = len(s)
        fail = compute_failure(s)

        # Period of the string
        period = n - fail[n - 1]

        # Check if n is divisible by period
        if n % period == 0:
            print(n // period)
        else:
            print(1)

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    while True:
        s = input().strip()
        if s == '*':
            break

        n = len(s)

        # Build KMP prefix function
        pi = [0] * n
        for i in range(1, n):
            j = pi[i - 1]
            while j > 0 and s[i] != s[j]:
                j = pi[j - 1]
            if s[i] == s[j]:
                j += 1
            pi[i] = j

        # The smallest period is n - pi[n-1]
        # If n is divisible by this period, that's our answer
        smallest_period = n - pi[n - 1]

        if n % smallest_period == 0:
            print(n // smallest_period)
        else:
            print(1)  # String is not periodic, only 1st root exists

if __name__ == "__main__":
    solve()
```

##### One-liner

```python
def kmp_period(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i-1]
        while j and s[i] != s[j]: j = pi[j-1]
        pi[i] = j + (s[i] == s[j])
    p = n - pi[-1]
    return n // p if n % p == 0 else 1

while True:
    s = input().strip()
    if s == '*': break
    print(kmp_period(s))
```

##### Complexity Analysis
- **Time Complexity:** O(|S|) per string
- **Space Complexity:** O(|S|) for failure array

##### Key Insight
The KMP failure function reveals the string's periodic structure. If fail[n-1] = k, then the first k characters match the last k characters, meaning the string has period (n-k). The maximum N is n/period if n is divisible by the period.

---

### Gaint and Sifat

#### Problem Information
- **Source:** Codechef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Sifat needs to find how many times word s occurs as a substring in sentence S (after removing all spaces from S).

#### Input Format
- First line: T (1 ≤ T ≤ 30) - number of test cases
- Each test case: two lines
  - First line: sentence S
  - Second line: word s

#### Constraints
- 1 ≤ |S| ≤ 100000
- 1 ≤ |s| ≤ |S|

#### Output Format
For each case, print case number and count of occurrences of s in S (spaces removed).

#### Solution

##### Approach
1. Remove all spaces from S
2. Use KMP algorithm to count occurrences of pattern s in text S

##### Python Solution

```python
def kmp_count(text, pattern):
    """Count occurrences of pattern in text using KMP"""
    if not pattern:
        return 0

    # Build failure function
    m = len(pattern)
    fail = [0] * m

    for i in range(1, m):
        j = fail[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        fail[i] = j

    # Search
    count = 0
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = fail[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            count += 1
            j = fail[j - 1]  # Continue searching for overlapping matches

    return count

def solve():
    t = int(input())

    for case in range(1, t + 1):
        S = input().replace(' ', '')  # Remove all spaces
        s = input().strip()

        count = kmp_count(S, s)
        print(f"Case {case}: {count}")

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    t = int(input())

    for case in range(1, t + 1):
        text = input().replace(' ', '')
        pattern = input().strip()

        # Build KMP prefix function
        def build_lps(p):
            lps = [0] * len(p)
            length = 0
            i = 1
            while i < len(p):
                if p[i] == p[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                elif length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
            return lps

        lps = build_lps(pattern)

        # KMP search
        count = 0
        i = j = 0
        while i < len(text):
            if text[i] == pattern[j]:
                i += 1
                j += 1
                if j == len(pattern):
                    count += 1
                    j = lps[j - 1]
            elif j != 0:
                j = lps[j - 1]
            else:
                i += 1

        print(f"Case {case}: {count}")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(|S| + |s|) per test case
- **Space Complexity:** O(|s|) for failure function

##### Key Insight
After removing spaces from S, this becomes a standard string matching problem. KMP algorithm efficiently counts all (possibly overlapping) occurrences of the pattern in linear time.

---

### MUH and Cube Walls

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Bears have a wall of n towers with heights a₁, a₂, ..., aₙ. Elephant Horace has a wall of w towers with heights b₁, b₂, ..., bw.

Horace can "see an elephant" on a segment of w contiguous towers in the bears' wall if the heights match as a sequence (allowing raising/lowering the entire wall uniformly).

Count segments where Horace can "see an elephant".

#### Input Format
- First line: n and w (1 ≤ n, w ≤ 2×10⁵)
- Second line: n integers aᵢ (1 ≤ aᵢ ≤ 10⁹) - bears' wall heights
- Third line: w integers bᵢ (1 ≤ bᵢ ≤ 10⁹) - elephant's wall heights

#### Output Format
Print the number of segments where Horace can "see an elephant".

#### Solution

##### Approach
Two walls match if their "shape" (differences between consecutive heights) is the same. Convert both walls to difference arrays and use KMP to count pattern matches.

##### Python Solution

```python
def solve():
    n, w = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    # Edge case: single tower always matches
    if w == 1:
        print(n)
        return

    # Convert to difference arrays
    diff_a = [a[i+1] - a[i] for i in range(n-1)]
    diff_b = [b[i+1] - b[i] for i in range(w-1)]

    # KMP to count occurrences of diff_b in diff_a
    pattern = diff_b
    text = diff_a
    m = len(pattern)

    if m == 0:
        print(n)
        return

    # Build failure function
    fail = [0] * m
    for i in range(1, m):
        j = fail[i-1]
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j-1]
        if pattern[i] == pattern[j]:
            j += 1
        fail[i] = j

    # Search
    count = 0
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = fail[j-1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            count += 1
            j = fail[j-1]

    print(count)

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def kmp_search(text, pattern):
    if not pattern:
        return len(text) + 1

    # Build LPS array
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1

    # Search
    count = 0
    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                count += 1
                j = lps[j - 1]
        elif j:
            j = lps[j - 1]
        else:
            i += 1

    return count

def solve():
    n, w = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    if w == 1:
        print(n)
        return

    # Compute differences
    da = [a[i+1] - a[i] for i in range(n-1)]
    db = [b[i+1] - b[i] for i in range(w-1)]

    print(kmp_search(da, db))

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N + W)
- **Space Complexity:** O(W) for failure function

##### Key Insight
Two sequences of heights have the same "shape" if their consecutive differences are identical. Converting both walls to difference arrays reduces this to exact pattern matching, solvable with KMP.

---

### Maximum Profit

#### Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

#### Problem Statement

Given stock prices for N days and at most K transactions allowed, find the maximum profit. A transaction is buying then selling. You cannot buy a new stock until the previous transaction is completed.

#### Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: K (max transactions)
  - Second line: N (number of days)
  - Third line: N prices

#### Constraints
- 1 ≤ T ≤ 100
- 0 < K ≤ 10
- 2 ≤ N ≤ 30
- 0 ≤ A[i] ≤ 1000

#### Output Format
Print maximum profit (0 if no profit possible).

#### Solution

##### Approach
Use DP with states: `dp[t][d]` = max profit using at most t transactions up to day d.

For each day, either:
1. Don't trade: `dp[t][d] = dp[t][d-1]`
2. Complete a transaction: buy on day j, sell on day d
   `dp[t][d] = max(dp[t-1][j-1] + price[d] - price[j])` for all j < d

##### Python Solution

```python
def solve():
    t = int(input())

    for _ in range(t):
        k = int(input())
        n = int(input())
        prices = list(map(int, input().split()))

        if n <= 1 or k == 0:
            print(0)
            continue

        # If k >= n/2, we can do unlimited transactions
        if k >= n // 2:
            profit = sum(max(0, prices[i+1] - prices[i]) for i in range(n-1))
            print(profit)
            continue

        # DP approach
        # dp[t][d] = max profit with at most t transactions ending on or before day d
        dp = [[0] * n for _ in range(k + 1)]

        for t in range(1, k + 1):
            max_diff = -prices[0]  # max of (dp[t-1][j] - prices[j])

            for d in range(1, n):
                # Don't sell on day d
                dp[t][d] = dp[t][d-1]

                # Sell on day d (bought on some earlier day j)
                dp[t][d] = max(dp[t][d], prices[d] + max_diff)

                # Update max_diff for future days
                max_diff = max(max_diff, dp[t-1][d] - prices[d])

        print(dp[k][n-1])

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    T = int(input())

    for _ in range(T):
        k = int(input())
        n = int(input())
        prices = list(map(int, input().split()))

        if n <= 1:
            print(0)
            continue

        # dp[i][j][0] = max profit at day i with j transactions, not holding
        # dp[i][j][1] = max profit at day i with j transactions, holding

        INF = float('inf')
        dp = [[[-INF, -INF] for _ in range(k + 2)] for _ in range(n + 1)]
        dp[0][0][0] = 0

        for i in range(n):
            for j in range(k + 1):
                # Not holding stock
                if dp[i][j][0] > -INF:
                    # Stay not holding
                    dp[i+1][j][0] = max(dp[i+1][j][0], dp[i][j][0])
                    # Buy stock
                    dp[i+1][j][1] = max(dp[i+1][j][1], dp[i][j][0] - prices[i])

                # Holding stock
                if dp[i][j][1] > -INF:
                    # Stay holding
                    dp[i+1][j][1] = max(dp[i+1][j][1], dp[i][j][1])
                    # Sell stock (complete transaction)
                    dp[i+1][j+1][0] = max(dp[i+1][j+1][0], dp[i][j][1] + prices[i])

        ans = max(dp[n][j][0] for j in range(k + 1))
        print(max(0, ans))

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × K)
- **Space Complexity:** O(N × K)

##### Key Insight
This is the "Best Time to Buy and Sell Stock" problem with at most K transactions. The optimized DP tracks `max_diff` to avoid an O(N²) inner loop, reducing complexity from O(N²K) to O(NK).

---

### Password

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given string s, find the longest substring t that is:
1. A prefix of s
2. A suffix of s
3. Appears somewhere in the middle of s (not at the very beginning or end)

If no such substring exists, print "Just a legend".

#### Input Format
- Single line: string s (length 1 to 10⁶), consisting of lowercase Latin letters

#### Output Format
Print the substring t, or "Just a legend" if it doesn't exist.

#### Solution

##### Approach
Use KMP failure function:
1. Find all prefix-suffix lengths using failure function
2. Check which of these also appear in the middle
3. Return the longest valid one

##### Python Solution

```python
def solve():
    s = input().strip()
    n = len(s)

    if n < 3:
        print("Just a legend")
        return

    # Build KMP failure function
    fail = [0] * n
    for i in range(1, n):
        j = fail[i - 1]
        while j > 0 and s[i] != s[j]:
            j = fail[j - 1]
        if s[i] == s[j]:
            j += 1
        fail[i] = j

    # Find all valid prefix-suffix lengths
    prefix_suffix_lens = set()
    length = fail[n - 1]
    while length > 0:
        prefix_suffix_lens.add(length)
        length = fail[length - 1]

    # Find lengths that appear in the middle (positions 1 to n-2)
    middle_lens = set()
    for i in range(n - 2):  # Exclude last position
        if fail[i] > 0:
            middle_lens.add(fail[i])

    # Find longest length that is both prefix-suffix AND appears in middle
    valid_lens = prefix_suffix_lens & middle_lens

    if not valid_lens:
        print("Just a legend")
    else:
        max_len = max(valid_lens)
        print(s[:max_len])

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    s = input().strip()
    n = len(s)

    # KMP failure function
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j

    # Count occurrences of each prefix (by its length)
    cnt = [0] * (n + 1)
    for i in range(n):
        cnt[pi[i]] += 1

    # Accumulate: prefix of length k includes prefix of length pi[k-1]
    for i in range(n - 1, 0, -1):
        cnt[pi[i - 1]] += cnt[i]

    # Find valid prefix-suffix that appears >= 3 times
    # (start, end, middle)
    length = pi[n - 1]
    while length > 0:
        # cnt[length] >= 2 means it appears at least twice besides being suffix
        # But we need it to appear in the middle
        # Check if this prefix appears at position other than 0 and n-length
        if cnt[length] >= 3:
            print(s[:length])
            return
        # Or if it appears as a prefix of the suffix prefix
        if cnt[length] >= 2 and pi[length - 1] > 0:
            print(s[:pi[length - 1]])
            return
        length = pi[length - 1]

    print("Just a legend")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

##### Key Insight
The KMP failure function gives us all prefix-suffix matches. We need to find one that also appears in the middle. Track which lengths appear in the middle (via fail[i] for i in [0, n-2]), then find the longest one that's also a prefix-suffix.

---

### Text Editor

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given text A, pattern B, and minimum count n, find the longest prefix of B that appears at least n times in A. If no such prefix exists, print "IMPOSSIBLE".

#### Input Format
- First line: text A (1 ≤ |A| ≤ 10⁵)
- Second line: pattern B (1 ≤ |B| ≤ |A|)
- Third line: integer n (1 ≤ n ≤ |A|)

#### Output Format
Print the longest prefix of B that appears at least n times in A, or "IMPOSSIBLE".

#### Solution

##### Approach
1. For each prefix of B (length 1, 2, ..., |B|), count occurrences in A
2. Find the longest prefix with count ≥ n
3. Use KMP for efficient counting

##### Python Solution

```python
def count_occurrences(text, pattern):
    """Count occurrences of pattern in text using KMP"""
    if not pattern:
        return len(text) + 1

    # Build failure function for pattern
    m = len(pattern)
    fail = [0] * m
    for i in range(1, m):
        j = fail[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        fail[i] = j

    # Search
    count = 0
    j = 0
    for char in text:
        while j > 0 and char != pattern[j]:
            j = fail[j - 1]
        if char == pattern[j]:
            j += 1
        if j == m:
            count += 1
            j = fail[j - 1]

    return count

def solve():
    A = input().strip()
    B = input().strip()
    n = int(input())

    # Binary search on prefix length
    # Or linear search from longest to shortest

    result = ""

    # Try each prefix length from longest to shortest
    for length in range(len(B), 0, -1):
        prefix = B[:length]
        if count_occurrences(A, prefix) >= n:
            result = prefix
            break

    if result:
        print(result)
    else:
        print("IMPOSSIBLE")

if __name__ == "__main__":
    solve()
```

##### Optimized

```python
def solve():
    A = input().strip()
    B = input().strip()
    n = int(input())

    # Build KMP failure function for B
    m = len(B)
    fail = [0] * m
    for i in range(1, m):
        j = fail[i - 1]
        while j > 0 and B[i] != B[j]:
            j = fail[j - 1]
        if B[i] == B[j]:
            j += 1
        fail[i] = j

    # Count occurrences of each prefix length
    # cnt[k] = number of times prefix of length k appears in A
    cnt = [0] * (m + 1)

    j = 0
    for char in A:
        while j > 0 and char != B[j]:
            j = fail[j - 1]
        if j < m and char == B[j]:
            j += 1

        # Prefix of length j matched here
        cnt[j] += 1

    # Propagate counts: if prefix of length k appears, so does prefix of length fail[k-1]
    for k in range(m, 0, -1):
        cnt[fail[k - 1]] += cnt[k]

    # Find longest prefix with count >= n
    for length in range(m, 0, -1):
        if cnt[length] >= n:
            print(B[:length])
            return

    print("IMPOSSIBLE")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(|A| + |B|)
- **Space Complexity:** O(|B|)

##### Key Insight
When matching pattern B against text A, at each position we've matched some prefix of B. Count how many times each prefix length is reached. Then propagate counts downward (longer prefix matches imply shorter prefix matches) to get total counts.

---

### e-Coins

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

E-coins have two values: conventional value and InfoTechnological value. The e-modulus is calculated as:
`sqrt(X*X + Y*Y)` where X is sum of conventional values and Y is sum of InfoTechnological values.

Find the minimum number of e-coins needed to achieve a target e-modulus S.

#### Input Format
- Multiple test cases
- First line of each case: m (number of e-coin types) and S (target e-modulus)
- Next m lines: conventional and InfoTechnological values of each e-coin type

#### Output Format
For each case, print minimum coins needed, or "not possible" if impossible.

#### Solution

##### Approach
This is a 2D coin change problem. Use BFS or DP:
- State: (sum_conventional, sum_info)
- Target: find state where sqrt(x² + y²) = S, i.e., x² + y² = S²
- Minimize number of coins

##### Python Solution

```python
from collections import deque

def solve():
    import sys
    input_data = sys.stdin.read().split('\n')
    idx = 0

    n = int(input_data[idx])
    idx += 1

    for _ in range(n):
        parts = input_data[idx].split()
        m, S = int(parts[0]), int(parts[1])
        idx += 1

        coins = []
        for _ in range(m):
            parts = input_data[idx].split()
            coins.append((int(parts[0]), int(parts[1])))
            idx += 1

        target_sq = S * S

        # BFS to find minimum coins
        # dist[x][y] = minimum coins to reach sum (x, y)
        INF = float('inf')
        dist = [[INF] * (S + 1) for _ in range(S + 1)]
        dist[0][0] = 0

        queue = deque([(0, 0)])

        while queue:
            x, y = queue.popleft()

            for cx, cy in coins:
                nx, ny = x + cx, y + cy

                if nx <= S and ny <= S and dist[nx][ny] == INF:
                    dist[nx][ny] = dist[x][y] + 1

                    if nx * nx + ny * ny == target_sq:
                        print(dist[nx][ny])
                        break

                    queue.append((nx, ny))
            else:
                continue
            break
        else:
            # Check all valid endpoints
            found = False
            for x in range(S + 1):
                for y in range(S + 1):
                    if x * x + y * y == target_sq and dist[x][y] != INF:
                        print(dist[x][y])
                        found = True
                        break
                if found:
                    break
            if not found:
                print("not possible")

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve_case():
    line = input().split()
    m, S = int(line[0]), int(line[1])

    coins = []
    for _ in range(m):
        parts = input().split()
        coins.append((int(parts[0]), int(parts[1])))

    target_sq = S * S
    INF = float('inf')

    # dp[x][y] = min coins to achieve sums (x, y)
    dp = [[INF] * (S + 1) for _ in range(S + 1)]
    dp[0][0] = 0

    # Process like unbounded knapsack
    for cx, cy in coins:
        for x in range(S + 1):
            for y in range(S + 1):
                if dp[x][y] < INF:
                    nx, ny = x + cx, y + cy
                    if nx <= S and ny <= S:
                        dp[nx][ny] = min(dp[nx][ny], dp[x][y] + 1)

    # Find minimum among valid targets
    ans = INF
    for x in range(S + 1):
        for y in range(S + 1):
            if x * x + y * y == target_sq:
                ans = min(ans, dp[x][y])

    if ans == INF:
        print("not possible")
    else:
        print(ans)

def solve():
    n = int(input())
    for _ in range(n):
        solve_case()

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(M × S²) for DP
- **Space Complexity:** O(S²)

##### Key Insight
This is a 2D variant of the coin change problem. Instead of reaching a single target value, we need to reach any (x, y) pair where x² + y² = S². BFS finds the minimum number of coins efficiently.

