---
layout: simple
title: "Removal Game"
difficulty: Hard
tags: [dp, game-theory, interval-dp, minimax]
prerequisites: [rectangle_cutting]
cses_link: https://cses.fi/problemset/task/1097
---

# Removal Game

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Two players alternately remove elements from either end of an array |
| Goal | Maximize first player's score assuming both play optimally |
| Technique | Interval DP with game theory (minimax) |
| Time Complexity | O(n^2) |
| Space Complexity | O(n^2) |

## Learning Goals

After solving this problem, you will understand:
1. **Game Theory DP**: How to model two-player games where both players play optimally
2. **Interval DP**: Working with subarray states dp[i][j]
3. **Optimal Play Assumption**: The opponent always makes the best move for themselves

## Problem Statement

There is a list of `n` numbers. Two players take turns removing a number from either the left or right end. Each player adds the removed number to their score. Both players play optimally to maximize their own score.

Find the maximum possible score for the first player.

**Input:**
- First line: integer `n` (1 <= n <= 5000)
- Second line: `n` integers (each between 1 and 10^9)

**Output:**
- Maximum score for the first player

**Example:**
```
Input:
4
4 5 1 3

Output:
8

Explanation:
- Player 1 takes 4 (left): score = 4, remaining = [5, 1, 3]
- Player 2 takes 5 (left): remaining = [1, 3]
- Player 1 takes 3 (right): score = 4 + 3 = 7, remaining = [1]
- Player 2 takes 1: game ends
Wait, that gives 7. Let's try another strategy:
- Player 1 takes 3 (right): score = 3, remaining = [4, 5, 1]
- Player 2 takes 5 (optimally): remaining = [4, 1]
- Player 1 takes 4 (left): score = 3 + 4 = 7, remaining = [1]
- Player 2 takes 1: game ends
Or:
- Player 1 takes 4 (left): score = 4, remaining = [5, 1, 3]
- Player 2 takes 3 (right): remaining = [5, 1]
- Player 1 takes 5 (left): score = 4 + 5 = 9, remaining = [1]
But player 2 plays optimally! They would take 5, not 3.
Optimal play gives Player 1 a score of 8.
```

## Key Insight

**Your goal is to maximize YOUR score, but the opponent also plays optimally.**

The critical realization: instead of tracking each player's score separately (which requires knowing whose turn it is), we can track the **difference** between the current player's score and the opponent's score.

## The Difference Formulation

Think about it this way:
- Let `your_score` = total points you collect
- Let `opponent_score` = total points opponent collects
- We want to maximize `your_score`

Instead, maximize `diff = your_score - opponent_score`

Why? Because when it's your turn and you take a value `v`:
- You gain `v`
- Then it becomes opponent's turn on the remaining subarray
- Whatever the opponent can achieve on that subarray (their best `diff`), that's **bad** for you

So: `your_diff = v - opponent's_best_diff_on_remaining`

## DP State Definition

```
dp[i][j] = maximum (current player's score - opponent's score)
           for subarray arr[i..j] when it's the current player's turn
```

This elegantly handles turn-taking: both players use the same formula because each player wants to maximize their own advantage.

## State Transition

For subarray [i..j], the current player can:
1. **Take left element arr[i]**: Get `arr[i]`, opponent plays optimally on [i+1..j]
2. **Take right element arr[j]**: Get `arr[j]`, opponent plays optimally on [i..j-1]

```
dp[i][j] = max(arr[i] - dp[i+1][j], arr[j] - dp[i][j-1])
```

Why subtract `dp[i+1][j]`? Because `dp[i+1][j]` is the opponent's best advantage on that subarray. From your perspective, their advantage is your disadvantage.

## Base Case

```
dp[i][i] = arr[i]
```

When only one element remains, the current player takes it. Their score is `arr[i]`, opponent gets 0, so diff = `arr[i]`.

## Final Answer

We have `dp[0][n-1]` = (Player1's score - Player2's score) for the full array.

We also know: `Player1's score + Player2's score = total_sum`

Solving these two equations:
```
Let diff = dp[0][n-1]
Let total = sum of all elements

Player1 + Player2 = total
Player1 - Player2 = diff

Adding: 2 * Player1 = total + diff
Therefore: Player1 = (total + diff) / 2
```

## Why This Formula Works

If we denote:
- `your = your_score`
- `opp = opponent_score`
- `total = your + opp` (all elements must be taken)
- `diff = your - opp` (what dp[0][n-1] gives us)

Then:
```
your + opp = total
your - opp = diff
-----------------
2 * your = total + diff
your = (total + diff) / 2
```

## Detailed Dry Run

**Array: [4, 5, 1, 3]**

Build dp table bottom-up (by increasing length):

**Length 1 (base cases):**
```
dp[0][0] = 4
dp[1][1] = 5
dp[2][2] = 1
dp[3][3] = 3
```

**Length 2:**
```
dp[0][1]: max(4 - dp[1][1], 5 - dp[0][0]) = max(4-5, 5-4) = max(-1, 1) = 1
dp[1][2]: max(5 - dp[2][2], 1 - dp[1][1]) = max(5-1, 1-5) = max(4, -4) = 4
dp[2][3]: max(1 - dp[3][3], 3 - dp[2][2]) = max(1-3, 3-1) = max(-2, 2) = 2
```

**Length 3:**
```
dp[0][2]: max(4 - dp[1][2], 1 - dp[0][1]) = max(4-4, 1-1) = max(0, 0) = 0
dp[1][3]: max(5 - dp[2][3], 3 - dp[1][2]) = max(5-2, 3-4) = max(3, -1) = 3
```

**Length 4:**
```
dp[0][3]: max(4 - dp[1][3], 3 - dp[0][2]) = max(4-3, 3-0) = max(1, 3) = 3
```

**Final calculation:**
```
total = 4 + 5 + 1 + 3 = 13
diff = dp[0][3] = 3
Player1's score = (13 + 3) / 2 = 8
```

## Python Implementation

```python
def removal_game(n: int, arr: list) -> int:
    """
    Find maximum score for first player in removal game.

    Args:
        n: Length of array
        arr: List of integers

    Returns:
        Maximum score achievable by first player
    """
    # dp[i][j] = max(current player's score - opponent's score) for arr[i..j]
    dp = [[0] * n for _ in range(n)]

    # Base case: single elements
    for i in range(n):
        dp[i][i] = arr[i]

    # Fill by increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            take_left = arr[i] - dp[i + 1][j]
            take_right = arr[j] - dp[i][j - 1]
            dp[i][j] = max(take_left, take_right)

    # Calculate first player's actual score
    total_sum = sum(arr)
    diff = dp[0][n - 1]
    return (total_sum + diff) // 2


def main():
    n = int(input())
    arr = list(map(int, input().split()))
    print(removal_game(n, arr))


if __name__ == "__main__":
    main()
```

## C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<long long> arr(n);
    long long total_sum = 0;
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
        total_sum += arr[i];
    }

    // dp[i][j] = max(current player's score - opponent's score) for arr[i..j]
    vector<vector<long long>> dp(n, vector<long long>(n, 0));

    // Base case: single elements
    for (int i = 0; i < n; i++) {
        dp[i][i] = arr[i];
    }

    // Fill by increasing length
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;
            long long take_left = arr[i] - dp[i + 1][j];
            long long take_right = arr[j] - dp[i][j - 1];
            dp[i][j] = max(take_left, take_right);
        }
    }

    // Calculate first player's actual score
    long long diff = dp[0][n - 1];
    long long answer = (total_sum + diff) / 2;

    cout << answer << "\n";

    return 0;
}
```

## Common Mistakes

### 1. Not Understanding the Difference Formulation

**Wrong approach:** Trying to track whose turn it is with an extra state parameter.
```python
# Overly complicated - don't do this
dp[i][j][turn]  # turn = 0 or 1
```

**Correct approach:** Use the difference formulation where both players maximize the same quantity.

### 2. Forgetting to Subtract

**Wrong:**
```python
dp[i][j] = max(arr[i] + dp[i+1][j], arr[j] + dp[i][j-1])  # WRONG!
```

**Correct:**
```python
dp[i][j] = max(arr[i] - dp[i+1][j], arr[j] - dp[i][j-1])  # Subtract!
```

The subtraction captures that the opponent's gain is your loss.

### 3. Integer Overflow

With n up to 5000 and values up to 10^9, the total sum can be up to 5 * 10^12. Use `long long` in C++.

### 4. Wrong Final Formula

**Wrong:** Returning `dp[0][n-1]` directly (this is the difference, not the score).

**Correct:** Return `(total_sum + dp[0][n-1]) / 2`.

## Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n^2) - fill n^2 states, O(1) per state |
| Space | O(n^2) - 2D DP table |

## Related Problems

| Problem | Platform | Similarity |
|---------|----------|------------|
| [Stone Game](https://leetcode.com/problems/stone-game/) | LeetCode | Nearly identical (even length, always win) |
| [Predict the Winner](https://leetcode.com/problems/predict-the-winner/) | LeetCode | Same core idea |
| [Stone Game II](https://leetcode.com/problems/stone-game-ii/) | LeetCode | Extended version with M parameter |
| [Stone Game III](https://leetcode.com/problems/stone-game-iii/) | LeetCode | Take 1, 2, or 3 from one end |
| [Rectangle Cutting](https://cses.fi/problemset/task/1744) | CSES | Interval DP pattern |

## Key Takeaways

1. **Game theory DP** often uses the "difference" formulation to avoid tracking turns
2. **Interval DP** pattern: dp[i][j] for subarray, fill by increasing length
3. **Minimax principle**: Your gain minus opponent's best response
4. The formula `answer = (total + diff) / 2` converts difference back to actual score
