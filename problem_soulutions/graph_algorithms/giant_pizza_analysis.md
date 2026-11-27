---
layout: problem-analysis
title: "Giant Pizza"
difficulty: Hard
tags: [graph, 2-sat, scc, implication-graph]
cses_link: https://cses.fi/problemset/task/1684
---

# Giant Pizza - 2-SAT Problem

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem Type | 2-SAT (2-Satisfiability) |
| Core Technique | Implication Graph + SCC |
| Time Complexity | O(n + m) |
| Space Complexity | O(n + m) |
| Key Data Structure | Directed Graph |
| Difficulty | Hard |

## Learning Goals

By completing this problem, you will learn:

1. **2-SAT Fundamentals**: Understand satisfiability problems with clauses of exactly 2 literals
2. **Implication Graphs**: Transform logical clauses into directed graph edges
3. **Reduction to SCC**: Use Strongly Connected Components to determine satisfiability
4. **Assignment Extraction**: Derive valid assignments from SCC topological ordering

## Problem Statement

Uolevi's family is ordering a giant pizza with `m` possible toppings. Each of the `n` family members has exactly **two wishes**, and each wish says a topping should be included (+) or excluded (-).

**Goal**: Choose the toppings so that every family member gets **at least one** of their two wishes.

**Input**:
- Line 1: `n m` (n = number of family members, m = number of toppings)
- Next n lines: two wishes per person, e.g. `+ 1 - 3` means "include topping 1 OR exclude topping 3"

**Output**:
- If possible: one symbol per topping (+ include, - exclude). Any valid selection is accepted.
- If impossible: `IMPOSSIBLE`

**Constraints**:
- 1 <= n, m <= 10^5

**Example** (CSES sample):
```
Input:
3 5
+ 1 + 2
- 1 + 3
+ 4 - 2

Output (one valid answer):
+ + + + +
```

Any selection that satisfies everyone is accepted. The code below prints `+ + + + +`, which works: wish 1 gets topping 1, wish 2 gets topping 3, wish 3 gets topping 4.

## 2-SAT Basics

### What is 2-SAT?

2-SAT is a special case of the Boolean Satisfiability problem where each clause contains exactly 2 literals. A literal is either a variable (x) or its negation (NOT x).

**General Form**: (a OR b) AND (c OR d) AND ...

### Converting Clauses to Implications

The key insight: Every clause `(a OR b)` can be rewritten as two implications:

```
(a OR b) is equivalent to:
  - (NOT a) -> b    (if a is false, b must be true)
  - (NOT b) -> a    (if b is false, a must be true)
```

**Why this works**:
- If `a` is false and the clause must be true, then `b` must be true
- If `b` is false and the clause must be true, then `a` must be true

### Example Transformation

For wish "+ 1 - 2" (topping 1 included OR topping 2 excluded):
- Let x1 = "topping 1 is included", x2 = "topping 2 is included"
- Clause: (x1 OR NOT x2)
- Implications:
  - NOT x1 -> NOT x2
  - x2 -> x1

## Building the Implication Graph

### Node Representation

Create **2n nodes** for n variables:
- Node `2i`: Variable xi is TRUE
- Node `2i + 1`: Variable xi is FALSE

Alternative indexing (used in code):
- Positive literal xi: index `i` (0-indexed: `i-1`)
- Negative literal NOT xi: index `n + i` (or use XOR trick: `idx ^ 1`)

### Edge Construction

For each clause (a OR b):
1. Add edge: NOT a -> b
2. Add edge: NOT b -> a

```
Implication Graph Construction:

Variables: x1, x2, x3 (3 toppings)
Clause: (x1 OR NOT x2)

Nodes:     x1    NOT_x1    x2    NOT_x2    x3    NOT_x3
          [0]     [1]     [2]     [3]     [4]     [5]

Implications from (x1 OR NOT x2):
  NOT x1 -> NOT x2:  edge from [1] to [3]
  x2 -> x1:          edge from [2] to [0]
```

## Key Insight: Satisfiability Condition

**Theorem**: A 2-SAT formula is satisfiable if and only if no variable x and its negation NOT x belong to the same Strongly Connected Component.

**Why?**
- If x and NOT x are in the same SCC, there exists a path from x to NOT x AND from NOT x to x
- This means: if x is true, NOT x must be true (contradiction!)
- And: if NOT x is true, x must be true (contradiction!)

```
Satisfiability Check:

SCC Analysis:
+-------------------+     +-------------------+

|    SCC 1          |     |    SCC 2          |
|  x1, x3, NOT_x2   |     | NOT_x1, NOT_x3, x2|
+-------------------+     +-------------------+

Check each variable:
  x1 in SCC1, NOT_x1 in SCC2  -> Different SCCs (OK)
  x2 in SCC2, NOT_x2 in SCC1  -> Different SCCs (OK)
  x3 in SCC1, NOT_x3 in SCC2  -> Different SCCs (OK)

Result: SATISFIABLE
```

## Finding a Valid Assignment

### Algorithm: Process SCCs in Reverse Topological Order

After finding SCCs using Kosaraju's or Tarjan's algorithm, SCCs are naturally in reverse topological order.

**Assignment Rule**: For each variable x:
- If x appears in an SCC that comes **after** NOT x's SCC in topological order, set x = TRUE
- Equivalently: Compare SCC indices; assign based on which literal has larger SCC index

```
Assignment Strategy:

SCCs in reverse topological order (Kosaraju output):
  SCC[0]: {NOT_x1, x2, NOT_x3}  <- processed first
  SCC[1]: {x1, NOT_x2, x3}      <- processed second

SCC indices:
  scc[x1] = 1,     scc[NOT_x1] = 0
  scc[x2] = 0,     scc[NOT_x2] = 1
  scc[x3] = 1,     scc[NOT_x3] = 0

Assignment (if scc[x] > scc[NOT_x], then x = TRUE):
  x1: scc[x1]=1 > scc[NOT_x1]=0  -> x1 = TRUE  (+)
  x2: scc[x2]=0 < scc[NOT_x2]=1  -> x2 = FALSE (-)
  x3: scc[x3]=1 > scc[NOT_x3]=0  -> x3 = TRUE  (+)

Result: + - +
```

## Visual Diagram: Implication Graph

For the three wishes in the dry run below, `(x1 OR x2)`, `(NOT_x1 OR x2)` and `(x1 OR NOT_x2)`:

```
   SCC 0                       SCC 1
 +-------------------+      +-------------+
 | NOT_x1 <-> NOT_x2 | ---> |  x1 <-> x2  |
 +-------------------+      +-------------+

Every literal sits in a different SCC from its negation -> satisfiable.
The "true" side of each variable is the SCC that comes later in topological order.
```

## Dry Run

**Input** (3 family members, 2 toppings):
```
3 2
+ 1 + 2
- 1 + 2
+ 1 - 2
```

**Step 1: Wishes become clauses, clauses become two implications each**

Node numbering matches the code: x1 = 0, x2 = 1, NOT_x1 = 2, NOT_x2 = 3.
```
(x1 OR x2):      NOT_x1 -> x2  (2->1),  NOT_x2 -> x1     (3->0)
(NOT_x1 OR x2):  x1 -> x2      (0->1),  NOT_x2 -> NOT_x1 (3->2)
(x1 OR NOT_x2):  NOT_x1 -> NOT_x2 (2->3),  x2 -> x1      (1->0)
```

**Step 2: SCCs (Kosaraju)**
```
SCC 0 = {NOT_x1, NOT_x2}   (2 <-> 3)
SCC 1 = {x1, x2}           (0 <-> 1)
Condensation: SCC 0 -> SCC 1, and Kosaraju numbers SCCs in topological order
```

**Step 3: Check and assign**
```
x1: scc 1 vs NOT_x1: scc 0 -> different, and x1 is later -> x1 = TRUE (+)
x2: scc 1 vs NOT_x2: scc 0 -> different, and x2 is later -> x2 = TRUE (+)
Output: + +
```

**What breaks it:** add a fourth wish `- 1 - 2`, i.e. (NOT_x1 OR NOT_x2). It adds x1 -> NOT_x2 and x2 -> NOT_x1, so all four nodes collapse into one SCC. x1 and NOT_x1 now share an SCC, so the answer is `IMPOSSIBLE`. That makes sense: the four wishes forbid every combination of toppings 1 and 2.

## Python Implementation

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
  input_data = sys.stdin.read().split()
  idx = 0
  wishes, n = int(input_data[idx]), int(input_data[idx + 1])  # n = toppings = variables
  idx += 2

  # Build implication graph
  # Node indexing: variable i (1-indexed) -> positive: i-1, negative: n+i-1
  graph = defaultdict(list)
  reverse_graph = defaultdict(list)

  def pos(i):
    return i - 1

  def neg(i):
    return n + i - 1

  def get_node(sign, var):
    return pos(var) if sign == '+' else neg(var)

  def get_negation(node):
    if node < n:
      return node + n
    return node - n

  for _ in range(wishes):
    sign1, var1 = input_data[idx], int(input_data[idx + 1])
    sign2, var2 = input_data[idx + 2], int(input_data[idx + 3])
    idx += 4

    # Clause: (lit1 OR lit2)
    # Implications: NOT lit1 -> lit2, NOT lit2 -> lit1
    a = get_node(sign1, var1)
    b = get_node(sign2, var2)
    not_a = get_negation(a)
    not_b = get_negation(b)

    graph[not_a].append(b)
    graph[not_b].append(a)
    reverse_graph[b].append(not_a)
    reverse_graph[a].append(not_b)

  # Kosaraju's algorithm for SCC
  visited = [False] * (2 * n)
  order = []

  def dfs1(node):
    visited[node] = True
    for neighbor in graph[node]:
      if not visited[neighbor]:
        dfs1(neighbor)
    order.append(node)

  for i in range(2 * n):
    if not visited[i]:
      dfs1(i)

  visited = [False] * (2 * n)
  scc_id = [-1] * (2 * n)
  current_scc = 0

  def dfs2(node, scc):
    visited[node] = True
    scc_id[node] = scc
    for neighbor in reverse_graph[node]:
      if not visited[neighbor]:
        dfs2(neighbor, scc)

  for node in reversed(order):
    if not visited[node]:
      dfs2(node, current_scc)
      current_scc += 1

  # Check satisfiability and build assignment
  result = []
  for i in range(n):
    if scc_id[pos(i + 1)] == scc_id[neg(i + 1)]:
      print("IMPOSSIBLE")
      return
    # If positive literal has larger SCC id, set to TRUE
    if scc_id[pos(i + 1)] > scc_id[neg(i + 1)]:
      result.append('+')
    else:
      result.append('-')

  print(' '.join(result))

solve()
```

## Common Mistakes

### 1. Wrong Implication Direction

**Wrong**: For clause (a OR b), adding edges a -> b and b -> a
**Correct**: Add edges NOT_a -> b and NOT_b -> a

```
Remember: (a OR b) means "if a is false, b must be true"
So the implication is: NOT_a -> b (not a -> b)
```

### 2. Forgetting Both Implications

**Wrong**: Only adding one implication per clause
**Correct**: Each clause (a OR b) produces TWO edges

```
Clause (a OR b) requires:
  1. NOT_a -> b
  2. NOT_b -> a  <- Don't forget this one!
```

### 3. Incorrect Node Indexing

**Wrong**: Confusing positive and negative literal indices
**Correct**: Use consistent indexing scheme throughout

```
Common scheme:
  Variable i (1-indexed):
    Positive literal: index i
    Negative literal: index n + i

  Or use XOR trick for 0-indexed:
    Positive: 2*i
    Negative: 2*i + 1
    Negation: idx ^ 1
```

### 4. Wrong Assignment Logic

**Wrong**: Assigning TRUE when SCC index is smaller
**Correct**: Assign TRUE when positive literal's SCC index is LARGER

```
With Kosaraju's algorithm (outputs reverse topological order):
  If scc[x] > scc[NOT_x]: set x = TRUE
  If scc[x] < scc[NOT_x]: set x = FALSE
```

### 5. Stack Overflow on Large Inputs

**Wrong**: Using recursive DFS without increasing stack limit
**Correct**: Increase recursion limit or use iterative DFS

```python
# Python: Add at the start
import sys
sys.setrecursionlimit(300000)
```

## Complexity Analysis

**Time Complexity**: O(n + m)
- Building graph: O(m) for m clauses
- Kosaraju's algorithm: O(V + E) = O(2n + 2m) = O(n + m)
- Assignment extraction: O(n)

**Space Complexity**: O(n + m)
- Graph storage: O(n + m) for adjacency lists
- SCC tracking: O(n) for IDs and visited arrays
- Order stack: O(n)

## Related Concepts

- **3-SAT**: NP-complete, no polynomial solution known
- **Horn-SAT**: Special case solvable in linear time
- **MAX-2-SAT**: Optimization version, NP-hard
- **Kosaraju's Algorithm**: Two-pass DFS for SCC
- **Tarjan's Algorithm**: Single-pass DFS for SCC
