---
layout: simple
title: "String Transformation - String Algorithms"
permalink: /problem_soulutions/string_algorithms/string_transformation_analysis
difficulty: Medium
tags: [strings, bfs, dp, transformation, bwt]
---

# String Transformation

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | String Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | BFS / Dynamic Programming |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Model string transformations as graph traversal problems
- [ ] Apply BFS to find shortest transformation paths
- [ ] Recognize when memoization improves transformation algorithms
- [ ] Handle cyclic transformation rules correctly

---

## Problem Statement

**Problem:** Given two strings `s` and `t`, and a set of transformation rules, find the minimum number of transformations needed to convert `s` into `t`.

**Input:**
- Line 1: String `s` (source string)
- Line 2: String `t` (target string)
- Line 3: Integer `n` (number of transformation rules)
- Next `n` lines: Two strings `a` and `b` (transform substring `a` into `b`)

**Output:**
- Minimum number of transformations, or `-1` if impossible

**Constraints:**
- 1 <= |s|, |t| <= 100
- 1 <= n <= 100
- 1 <= |a|, |b| <= 10

### Example

```
Input:
abc
def
3
ab cd
bc ef
cd de

Output:
2
```

**Explanation:**
- Start: "abc"
- Apply "ab" -> "cd": "abc" -> "cdc"
- Apply "cd" -> "de": "cdc" -> "dec" (or use different path)
- Minimum steps to reach "def": 2

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we model string transformations systematically?

Think of each unique string as a **node** in a graph. Each transformation rule creates **edges** between nodes. Finding the minimum transformations is equivalent to finding the **shortest path** from source to target.

### Breaking Down the Problem

1. **What are we looking for?** The shortest sequence of rule applications
2. **What information do we have?** Start string, target string, and valid transformations
3. **What's the relationship?** Each rule application moves us to a new "state" (string)

### Analogies

Think of this like a word ladder puzzle. Each transformation rule is a valid "move" that changes your current word. You want to reach the target word in the fewest moves possible.

---

## Solution 1: Brute Force (DFS with Backtracking)

### Idea

Try all possible sequences of transformations recursively until we reach the target or exhaust possibilities.

### Algorithm

1. Start with source string
2. Try applying each rule at every possible position
3. Recursively continue from each new string
4. Track minimum transformations to reach target

### Code

```python
def solve_brute_force(s: str, t: str, rules: list) -> int:
    """
    Brute force DFS solution.

    Time: O(n! * m) where n = number of rules, m = string length
    Space: O(n) recursion depth
    """
    def dfs(current: str, depth: int, visited: set) -> int:
        if current == t:
            return depth
        if depth > len(s) * 2 or current in visited:
            return float('inf')

        visited.add(current)
        min_steps = float('inf')

        for pattern, replacement in rules:
            pos = 0
            while True:
                pos = current.find(pattern, pos)
                if pos == -1:
                    break
                new_str = current[:pos] + replacement + current[pos + len(pattern):]
                min_steps = min(min_steps, dfs(new_str, depth + 1, visited.copy()))
                pos += 1

        return min_steps

    result = dfs(s, 0, set())
    return result if result != float('inf') else -1
```

```cpp
#include <string>
#include <vector>
#include <set>
#include <climits>
using namespace std;

class BruteForce {
public:
    int solve(string s, string t, vector<pair<string, string>>& rules) {
        set<string> visited;
        int result = dfs(s, t, rules, 0, visited);
        return result == INT_MAX ? -1 : result;
    }

private:
    int dfs(string& current, string& target,
            vector<pair<string, string>>& rules,
            int depth, set<string>& visited) {
        if (current == target) return depth;
        if (depth > current.size() * 2) return INT_MAX;
        if (visited.count(current)) return INT_MAX;

        visited.insert(current);
        int minSteps = INT_MAX;

        for (auto& [pattern, replacement] : rules) {
            size_t pos = 0;
            while ((pos = current.find(pattern, pos)) != string::npos) {
                string newStr = current.substr(0, pos) + replacement +
                               current.substr(pos + pattern.size());
                set<string> newVisited = visited;
                minSteps = min(minSteps, dfs(newStr, target, rules, depth + 1, newVisited));
                pos++;
            }
        }
        return minSteps;
    }
};
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * m) | All permutations of rules, string operations |
| Space | O(n) | Recursion depth and visited set |

### Why This Works (But Is Slow)

Correctness is guaranteed because we explore ALL possible transformation sequences. However, we waste time revisiting the same strings through different paths and don't exploit the shortest-path nature of the problem.

---

## Solution 2: Optimal BFS Solution

### Key Insight

> **The Trick:** BFS naturally finds the shortest path in an unweighted graph. Each string state is a node, each transformation is an edge.

### Algorithm

1. Initialize queue with source string at distance 0
2. For each string, try all applicable rules at all positions
3. First time we reach target, return the distance
4. Use visited set to avoid reprocessing

### Dry Run Example

Let's trace through with `s = "abc"`, `t = "def"`, rules = `[("ab","cd"), ("bc","ef"), ("cd","de")]`:

```
Initial state:
  queue = [("abc", 0)]
  visited = {"abc"}

Step 1: Process "abc" at distance 0
  Apply "ab"->"cd" at pos 0: "cdc"
    "cdc" not visited, add to queue
  Apply "bc"->"ef" at pos 1: "aef"
    "aef" not visited, add to queue
  queue = [("cdc", 1), ("aef", 1)]
  visited = {"abc", "cdc", "aef"}

Step 2: Process "cdc" at distance 1
  Apply "cd"->"de" at pos 0: "dec"
    "dec" not visited, add to queue
  Apply "cd"->"de" at pos 1: "cde" (if applicable)
  ...continue until target found

Step 3: Process "aef" at distance 1
  No rules match, skip

...eventually find "def" at distance 2
```

### Visual Diagram

```
String State Graph:

    "abc" (start)
      |
   +--+--+
   |     |
 "cdc" "aef"
   |
 "dec"
   |
  ...
   |
 "def" (target)

BFS explores level by level:
Level 0: abc
Level 1: cdc, aef, ...
Level 2: dec, def, ...  <-- Found at level 2!
```

### Code

```python
from collections import deque

def solve_bfs(s: str, t: str, rules: list) -> int:
    """
    Optimal BFS solution - finds shortest transformation path.

    Time: O(S * R * L) where S = unique states, R = rules, L = string length
    Space: O(S) for visited set and queue
    """
    if s == t:
        return 0

    queue = deque([(s, 0)])
    visited = {s}

    while queue:
        current, dist = queue.popleft()

        for pattern, replacement in rules:
            pos = 0
            while True:
                pos = current.find(pattern, pos)
                if pos == -1:
                    break

                new_str = current[:pos] + replacement + current[pos + len(pattern):]

                if new_str == t:
                    return dist + 1

                if new_str not in visited:
                    visited.add(new_str)
                    queue.append((new_str, dist + 1))

                pos += 1

    return -1


# Main function for competitive programming
def main():
    s = input().strip()
    t = input().strip()
    n = int(input().strip())
    rules = []
    for _ in range(n):
        parts = input().strip().split()
        rules.append((parts[0], parts[1]))

    print(solve_bfs(s, t, rules))

if __name__ == "__main__":
    main()
```

```cpp
#include <bits/stdc++.h>
using namespace std;

int solveBFS(string s, string t, vector<pair<string, string>>& rules) {
    if (s == t) return 0;

    queue<pair<string, int>> q;
    unordered_set<string> visited;

    q.push({s, 0});
    visited.insert(s);

    while (!q.empty()) {
        auto [current, dist] = q.front();
        q.pop();

        for (auto& [pattern, replacement] : rules) {
            size_t pos = 0;
            while ((pos = current.find(pattern, pos)) != string::npos) {
                string newStr = current.substr(0, pos) + replacement +
                               current.substr(pos + pattern.size());

                if (newStr == t) return dist + 1;

                if (visited.find(newStr) == visited.end()) {
                    visited.insert(newStr);
                    q.push({newStr, dist + 1});
                }
                pos++;
            }
        }
    }
    return -1;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    int n;
    cin >> s >> t >> n;

    vector<pair<string, string>> rules(n);
    for (int i = 0; i < n; i++) {
        cin >> rules[i].first >> rules[i].second;
    }

    cout << solveBFS(s, t, rules) << "\n";
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(S * R * L) | S = reachable states, R = rules, L = string length |
| Space | O(S) | Visited set stores all seen strings |

---

## Common Mistakes

### Mistake 1: Not Handling All Occurrences of a Pattern

```python
# WRONG - only finds first occurrence
pos = current.find(pattern)
if pos != -1:
    new_str = current[:pos] + replacement + current[pos + len(pattern):]
```

**Problem:** A pattern may appear multiple times; each creates a different transformation.
**Fix:** Use a while loop to find ALL occurrences.

### Mistake 2: Forgetting to Check if Already at Target

```python
# WRONG - missing base case
def solve(s, t, rules):
    queue = deque([(s, 0)])
    # ... proceeds to BFS even if s == t
```

**Problem:** Wastes computation and may return wrong answer.
**Fix:** Check `if s == t: return 0` at the start.

### Mistake 3: Not Checking Visited Before Adding

```python
# WRONG - adds to queue then checks
queue.append((new_str, dist + 1))
if new_str not in visited:  # Too late!
    visited.add(new_str)
```

**Problem:** Same string gets added to queue multiple times, causing TLE.
**Fix:** Check `if new_str not in visited` BEFORE appending.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Already equal | s="abc", t="abc" | 0 | No transformation needed |
| Impossible | s="abc", t="xyz", no matching rules | -1 | No path exists |
| Single char change | s="a", t="b", rule=("a","b") | 1 | Direct transformation |
| Multiple paths | Various rules lead to target | Minimum | BFS finds shortest |
| Empty rules | n=0 | 0 or -1 | Only 0 if s==t |

---

## When to Use This Pattern

### Use This Approach When:
- Problem asks for "minimum number of operations"
- Each operation transforms current state to a new state
- State space is finite (bounded string lengths)

### Don't Use When:
- State space is infinite or very large (consider A* or heuristics)
- Need to find ALL paths, not just shortest (use DFS with backtracking)
- Transformations have different costs (use Dijkstra instead)

### Pattern Recognition Checklist:
- [ ] Convert X to Y with minimum operations? **Consider BFS**
- [ ] Each operation creates a new valid state? **Model as graph**
- [ ] States can be revisited? **Use visited set**
- [ ] Looking for ANY path, not shortest? **DFS might be simpler**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Word Search](https://leetcode.com/problems/word-search/) | Basic string grid traversal |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Word Ladder (LeetCode)](https://leetcode.com/problems/word-ladder/) | Single character changes |
| [String Matching (CSES)](https://cses.fi/problemset/task/1753) | Pattern matching foundation |
| [Finding Borders (CSES)](https://cses.fi/problemset/task/1732) | String structure analysis |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Word Ladder II (LeetCode)](https://leetcode.com/problems/word-ladder-ii/) | Find ALL shortest paths |
| [Edit Distance (LeetCode)](https://leetcode.com/problems/edit-distance/) | DP for transformation cost |
| [Finding Periods (CSES)](https://cses.fi/problemset/task/1733) | Advanced string properties |

---

## Key Takeaways

1. **The Core Idea:** Model string transformations as graph traversal; BFS finds shortest paths
2. **Time Optimization:** From O(n!) brute force to O(S*R*L) BFS by avoiding redundant exploration
3. **Space Trade-off:** Use O(S) space for visited set to gain polynomial time
4. **Pattern:** This is a classic state-space search problem

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why BFS guarantees the shortest path
- [ ] Identify when string transformation problems need BFS vs DFS vs DP
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: BFS](https://cp-algorithms.com/graph/bfs.html)
- [CSES Problem Set - String Algorithms](https://cses.fi/problemset/list/)
- [Competitive Programming Handbook - String Algorithms](https://cses.fi/book/book.pdf)
