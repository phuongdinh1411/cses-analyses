---
layout: simple
title: "Giant Pizza - 2-SAT Problem"
permalink: /problem_soulutions/graph_algorithms/giant_pizza_analysis
---

# Giant Pizza - 2-SAT Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand 2-SAT problems and satisfiability concepts in propositional logic
- Apply strongly connected components to solve 2-SAT problems with implication graphs
- Implement efficient 2-SAT algorithms with proper implication graph construction
- Optimize 2-SAT solutions using SCC algorithms and logical constraint handling
- Handle edge cases in 2-SAT problems (contradictory constraints, trivial satisfiability, complex implications)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2-SAT, strongly connected components, implication graphs, satisfiability algorithms, logical constraints
- **Data Structures**: Implication graphs, SCC data structures, graph representations, constraint tracking
- **Mathematical Concepts**: Propositional logic, satisfiability, implication graphs, logical constraints, graph theory
- **Programming Skills**: Graph construction, SCC algorithms, logical constraint handling, algorithm implementation
- **Related Problems**: Strongly Connected Components (SCC algorithms), Building Teams (graph coloring), Logical problems

## 📋 Problem Description

Given a list of pizza toppings preferences where each person likes some toppings and dislikes others, determine if it's possible to make a pizza that satisfies everyone's preferences.

This is a classic 2-SAT (2-Satisfiability) problem where we need to determine if there exists a truth assignment that satisfies all logical constraints. Each person's preference creates implications that must be satisfied.

**Input**: 
- First line: Two integers n and m (number of people and toppings)
- Next n lines: Two integers a and b (person likes topping a and dislikes topping b)

**Output**: 
- Print "YES" if it's possible to make a satisfying pizza, "NO" otherwise

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 10⁵
- 1 ≤ a, b ≤ m

**Example**:
```
Input:
3 3
1 2
2 3
3 1

Output:
YES
```

**Explanation**: 
- Person 1: likes topping 1, dislikes topping 2
- Person 2: likes topping 2, dislikes topping 3
- Person 3: likes topping 3, dislikes topping 1
- Solution: Include toppings 1, 2, 3 (satisfies all preferences)

## 🎯 Visual Example

### Input Preferences
```
People: 3, Toppings: 3
Preferences:
- Person 1: likes topping 1, dislikes topping 2
- Person 2: likes topping 2, dislikes topping 3
- Person 3: likes topping 3, dislikes topping 1
```

### 2-SAT Problem Construction
```
Step 1: Convert preferences to logical implications
- Person 1: likes 1, dislikes 2 → (1 ∨ ¬2)
- Person 2: likes 2, dislikes 3 → (2 ∨ ¬3)
- Person 3: likes 3, dislikes 1 → (3 ∨ ¬1)

Step 2: Build implication graph
- (1 ∨ ¬2) → (¬1 → ¬2) and (2 → 1)
- (2 ∨ ¬3) → (¬2 → ¬3) and (3 → 2)
- (3 ∨ ¬1) → (¬3 → ¬1) and (1 → 3)

Implication graph:
¬1 ──> ¬2 ──> ¬3 ──> ¬1
│      │      │      │
└──1───┼──2───┼──3───┘
        │      │
        └──────┘
```

### 2-SAT Algorithm Process
```
Step 1: Find strongly connected components (SCCs)
- SCC 1: {1, 2, 3}
- SCC 2: {¬1, ¬2, ¬3}

Step 2: Check for contradictions
- No variable and its negation in same SCC ✓
- 2-SAT is satisfiable

Step 3: Find satisfying assignment
- Process SCCs in reverse topological order
- Assign variables based on SCC order
- Solution: {1: true, 2: true, 3: true}
```

### Solution Verification
```
Pizza with toppings 1, 2, 3:
- Person 1: likes 1 ✓, dislikes 2 ✗ (but 2 is included)
- Person 2: likes 2 ✓, dislikes 3 ✗ (but 3 is included)
- Person 3: likes 3 ✓, dislikes 1 ✗ (but 1 is included)

Wait, this doesn't satisfy all preferences. Let me recalculate...

Correct solution: {1: true, 2: false, 3: true}
- Person 1: likes 1 ✓, dislikes 2 ✓ (2 not included)
- Person 2: likes 2 ✗ (2 not included), dislikes 3 ✓ (3 included)
- Person 3: likes 3 ✓, dislikes 1 ✓ (1 included)
```

### Key Insight
2-SAT algorithm works by:
1. Converting preferences to logical implications
2. Building implication graph
3. Finding strongly connected components
4. Checking for contradictions (variable and negation in same SCC)
5. Time complexity: O(n + m) for SCC detection
6. Space complexity: O(n + m) for graph representation

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Determine if pizza can satisfy all people's preferences
- **Key Insight**: This is a 2-SAT problem with logical implications
- **Challenge**: Convert preferences to logical constraints and check satisfiability

### Step 2: Initial Approach
**2-SAT with Kosaraju's algorithm for strongly connected components:**

```python
def giant_pizza_naive(n, m, preferences):
    # Build implication graph for 2-SAT
    # For each preference (a, b): if we choose a, we must not choose b
    # This creates implications: a -> ~b and b -> ~a
    
    # Graph has 2*m nodes: 1 to m for positive, m+1 to 2*m for negative
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b (if we choose a, we must not choose b)
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        
        # b -> ~a (if we choose b, we must not choose a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Use Kosaraju's algorithm to find SCCs
    visited = [False] * (2*m + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS to find SCCs
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check if any variable and its negation are in the same SCC
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO"
    
    return "YES"
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized 2-SAT Algorithm - O(n + m)
**Description**: Use optimized 2-SAT algorithm with better structure.

```python
def giant_pizza_optimized(n, m, preferences):
    # Build implication graph for 2-SAT
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b and b -> ~a
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Kosaraju's algorithm
    visited = [False] * (2*m + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check 2-SAT satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO"
    
    return "YES"
```

**Why this improvement works**: We use 2-SAT problem reduction with optimized Kosaraju's algorithm to check satisfiability efficiently.

### Step 3: Optimization/Alternative
**Enhanced 2-SAT with better graph construction:**

### Step 4: Complete Solution

```python
n, m = map(int, input().split())
preferences = []
for _ in range(n):
    a, b = map(int, input().split())
    preferences.append((a, b))

def check_giant_pizza(n, m, preferences):
    # Build implication graph for 2-SAT
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b and b -> ~a
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Kosaraju's algorithm
    visited = [False] * (2*m + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check 2-SAT satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO"
    
    return "YES"

result = check_giant_pizza(n, m, preferences)
print(result)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Satisfiable preferences (should return YES)
- **Test 2**: Unsatisfiable preferences (should return NO)
- **Test 3**: Single person preference (should return YES)
- **Test 4**: Conflicting preferences (should return NO)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| 2-SAT with Kosaraju's | O(n + m) | O(n + m) | Use 2-SAT reduction to SCC |
| Optimized 2-SAT | O(n + m) | O(n + m) | Optimized 2-SAT implementation |

## 🎨 Visual Example

### Input Example
```
3 people, 3 toppings:
Person 1: likes topping 1, dislikes topping 2
Person 2: likes topping 2, dislikes topping 3
Person 3: likes topping 3, dislikes topping 1
```

### Logical Constraints
```
Person 1: likes 1, dislikes 2
- If topping 2 is included, then topping 1 must be included
- Implication: ¬2 → 1 (if not 2, then 1)
- Equivalent: 2 ∨ 1

Person 2: likes 2, dislikes 3
- If topping 3 is included, then topping 2 must be included
- Implication: ¬3 → 2 (if not 3, then 2)
- Equivalent: 3 ∨ 2

Person 3: likes 3, dislikes 1
- If topping 1 is included, then topping 3 must be included
- Implication: ¬1 → 3 (if not 1, then 3)
- Equivalent: 1 ∨ 3
```

### Implication Graph
```
Variables: 1, 2, 3 (toppings)
Negations: ¬1, ¬2, ¬3

Implication graph:
¬2 → 1    (if not 2, then 1)
¬3 → 2    (if not 3, then 2)
¬1 → 3    (if not 1, then 3)

Graph edges:
¬2 ──→ 1
¬3 ──→ 2
¬1 ──→ 3

Also add contrapositives:
¬1 ──→ 3
¬2 ──→ 1
¬3 ──→ 2
```

### 2-SAT Reduction
```
Original clauses:
- (2 ∨ 1)
- (3 ∨ 2)
- (1 ∨ 3)

Convert to implications:
- (2 ∨ 1) → (¬2 → 1) and (¬1 → 2)
- (3 ∨ 2) → (¬3 → 2) and (¬2 → 3)
- (1 ∨ 3) → (¬1 → 3) and (¬3 → 1)

Implication graph:
¬2 → 1, ¬1 → 2
¬3 → 2, ¬2 → 3
¬1 → 3, ¬3 → 1
```

### Strongly Connected Components
```
SCC Analysis:
- SCC 1: {1, 2, 3} (all connected)
- SCC 2: {¬1, ¬2, ¬3} (all connected)

Check for conflicts:
- If 1 and ¬1 are in the same SCC → UNSATISFIABLE
- If 2 and ¬2 are in the same SCC → UNSATISFIABLE
- If 3 and ¬3 are in the same SCC → UNSATISFIABLE

In this case: No conflicts → SATISFIABLE
```

### Solution Construction
```
Topological order of SCCs:
1. SCC 2: {¬1, ¬2, ¬3}
2. SCC 1: {1, 2, 3}

Assignment:
- Process SCC 2 first: assign all to false
- Process SCC 1: assign all to true

Final assignment:
- Topping 1: true (include)
- Topping 2: true (include)
- Topping 3: true (include)

Verification:
- Person 1: likes 1 ✓, dislikes 2 ✗ (but 1 is included, so satisfied)
- Person 2: likes 2 ✓, dislikes 3 ✗ (but 2 is included, so satisfied)
- Person 3: likes 3 ✓, dislikes 1 ✗ (but 3 is included, so satisfied)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ 2-SAT with SCC  │ O(n + m)     │ O(n + m)     │ Implication  │
│                 │              │              │ graph        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Kosaraju's      │ O(n + m)     │ O(n + m)     │ Two DFS      │
│                 │              │              │ traversals   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Tarjan's        │ O(n + m)     │ O(n + m)     │ Single DFS   │
│                 │              │              │ with stack   │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **2-SAT Problem**: Boolean satisfiability with 2 variables per clause
- **Implication Graph**: Directed graph representing logical implications
- **Strongly Connected Components**: Used to check satisfiability
- **Kosaraju's Algorithm**: Efficient SCC finding algorithm

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. General SAT Problem**
```python
def general_sat(n, m, clauses):
    # Solve general SAT problem (not just 2-SAT)
    # clauses = list of clauses, each clause is a list of literals
    # Each literal is (variable, is_positive)
    
    def is_satisfiable():
        # Try all possible truth assignments
        for assignment in range(1 << m):
            satisfied = True
            for clause in clauses:
                clause_satisfied = False
                for var, is_positive in clause:
                    if (assignment >> (var - 1)) & 1 == is_positive:
                        clause_satisfied = True
                        break
                if not clause_satisfied:
                    satisfied = False
                    break
            if satisfied:
                return True
        return False
    
    return is_satisfiable()
```

#### **2. Weighted 2-SAT**
```python
def weighted_2sat(n, m, preferences, weights):
    # Solve 2-SAT with weights on variables
    # weights[i] = weight of variable i
    
    def build_weighted_graph():
        adj = [[] for _ in range(2*m + 1)]
        adj_rev = [[] for _ in range(2*m + 1)]
        
        for a, b in preferences:
            adj[a].append(b + m)
            adj_rev[b + m].append(a)
            adj[b].append(a + m)
            adj_rev[a + m].append(b)
        
        return adj, adj_rev
    
    def kosaraju_scc():
        adj, adj_rev = build_weighted_graph()
        visited = [False] * (2*m + 1)
        finish_order = []
        
        def first_dfs(node):
            visited[node] = True
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    first_dfs(neighbor)
            finish_order.append(node)
        
        for i in range(1, 2*m + 1):
            if not visited[i]:
                first_dfs(i)
        
        visited = [False] * (2*m + 1)
        scc_id = [0] * (2*m + 1)
        current_scc = 0
        
        def second_dfs(node, scc):
            visited[node] = True
            scc_id[node] = scc
            for neighbor in adj_rev[node]:
                if not visited[neighbor]:
                    second_dfs(neighbor, scc)
        
        for node in reversed(finish_order):
            if not visited[node]:
                current_scc += 1
                second_dfs(node, current_scc)
        
        return scc_id
    
    scc_id = kosaraju_scc()
    
    # Check satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return False, None
    
    # Find optimal assignment
    assignment = [False] * (m + 1)
    for i in range(1, m + 1):
        if scc_id[i] < scc_id[i + m]:
            assignment[i] = True
    
    return True, assignment
```

#### **3. Dynamic 2-SAT**
```python
def dynamic_2sat(n, m, preferences, queries):
    # Handle dynamic 2-SAT with adding/removing constraints
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    def add_constraint(a, b):
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    def remove_constraint(a, b):
        adj[a].remove(b + m)
        adj_rev[b + m].remove(a)
        adj[b].remove(a + m)
        adj_rev[a + m].remove(b)
    
    def check_satisfiability():
        # Run Kosaraju's algorithm
        visited = [False] * (2*m + 1)
        finish_order = []
        
        def first_dfs(node):
            visited[node] = True
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    first_dfs(neighbor)
            finish_order.append(node)
        
        for i in range(1, 2*m + 1):
            if not visited[i]:
                first_dfs(i)
        
        visited = [False] * (2*m + 1)
        scc_id = [0] * (2*m + 1)
        current_scc = 0
        
        def second_dfs(node, scc):
            visited[node] = True
            scc_id[node] = scc
            for neighbor in adj_rev[node]:
                if not visited[neighbor]:
                    second_dfs(neighbor, scc)
        
        for node in reversed(finish_order):
            if not visited[node]:
                current_scc += 1
                second_dfs(node, current_scc)
        
        # Check satisfiability
        for i in range(1, m + 1):
            if scc_id[i] == scc_id[i + m]:
                return False
        return True
    
    # Add initial constraints
    for a, b in preferences:
        add_constraint(a, b)
    
    results = []
    for query in queries:
        if query[0] == "ADD":
            _, a, b = query
            add_constraint(a, b)
        elif query[0] == "REMOVE":
            _, a, b = query
            remove_constraint(a, b)
        elif query[0] == "CHECK":
            results.append(check_satisfiability())
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **2-SAT**: Boolean satisfiability problems
- **Strongly Connected Components**: Graph connectivity problems
- **Constraint Satisfaction**: Constraint satisfaction problems
- **Graph Theory**: Fundamental graph theory concepts

## 📚 Learning Points

### Key Takeaways
- **2-SAT** is a special case of boolean satisfiability
- **Implication graphs** represent logical constraints
- **Strongly connected components** determine satisfiability
- **Kosaraju's algorithm** efficiently finds SCCs
- **Boolean logic** has many algorithmic applications

## Key Insights for Other Problems

### 1. **2-SAT Problem**
**Principle**: Reduce 2-SAT to strongly connected components problem.
**Applicable to**: Boolean satisfiability problems, constraint satisfaction problems

### 2. **Implication Graph**
**Principle**: Build directed graph where edges represent logical implications.
**Applicable to**: Logic problems, constraint problems, graph problems

### 3. **SCC for Satisfiability**
**Principle**: Use strongly connected components to check satisfiability.
**Applicable to**: 2-SAT problems, logic problems, constraint problems

## Notable Techniques

### 1. **2-SAT Problem Reduction**
```python
def build_2sat_graph(n, m, preferences):
    # Graph has 2*m nodes: 1 to m for positive, m+1 to 2*m for negative
    adj = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        # a -> ~b and b -> ~a
        adj[a].append(b + m)
        adj[b].append(a + m)
    
    return adj
```

### 2. **2-SAT Satisfiability Check**
```python
def check_2sat_satisfiability(m, scc_id):
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return False
    return True
```

### 3. **Implication Graph Construction**
```python
def build_implication_graph(preferences, m):
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    return adj, adj_rev
```

## Problem-Solving Framework

1. **Identify problem type**: This is a 2-SAT problem
2. **Choose approach**: Use 2-SAT reduction to strongly connected components
3. **Build implication graph**: Create directed graph with logical implications
4. **Find SCCs**: Use Kosaraju's algorithm to find strongly connected components
5. **Check satisfiability**: Verify no variable and its negation are in same SCC
6. **Return result**: Output "YES" if satisfiable, "NO" otherwise

---

*This analysis shows how to efficiently solve 2-SAT problems using strongly connected components.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Giant Pizza with Costs**
**Problem**: Each topping has a cost, find minimum cost satisfying assignment.
```python
def cost_based_giant_pizza(n, m, preferences, costs):
    # costs[i] = cost of topping i
    
    # Build implication graph
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Find strongly connected components using Kosaraju's algorithm
    finish_order = []
    visited = [False] * (2*m + 1)
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS to find SCCs
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO", -1
    
    # Find minimum cost assignment
    assignment = [False] * (m + 1)
    scc_assigned = [False] * (current_scc + 1)
    
    # Process SCCs in topological order
    for i in range(1, m + 1):
        if not scc_assigned[scc_id[i]]:
            # Choose the cheaper option between i and ~i
            cost_i = costs[i] if i <= m else 0
            cost_not_i = costs[i - m] if i > m else 0
            
            if cost_i <= cost_not_i:
                assignment[i] = True
                scc_assigned[scc_id[i]] = True
                scc_assigned[scc_id[i + m]] = True
            else:
                assignment[i + m] = True
                scc_assigned[scc_id[i]] = True
                scc_assigned[scc_id[i + m]] = True
    
    total_cost = sum(costs[i] for i in range(1, m + 1) if assignment[i])
    return "YES", total_cost
```

#### **Variation 2: Giant Pizza with Constraints**
**Problem**: Find satisfying assignment with additional constraints on topping combinations.
```python
def constrained_giant_pizza(n, m, preferences, constraints):
    # constraints = {'forbidden_combinations': [(a, b), ...], 'required_combinations': [(a, b), ...]}
    
    # Build implication graph with additional constraints
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    # Original preferences
    for a, b in preferences:
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Forbidden combinations: if a and b are forbidden, add a -> ~b and b -> ~a
    for a, b in constraints.get('forbidden_combinations', []):
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Required combinations: if a and b are required, add ~a -> b and ~b -> a
    for a, b in constraints.get('required_combinations', []):
        adj[a + m].append(b)
        adj_rev[b].append(a + m)
        adj[b + m].append(a)
        adj_rev[a].append(b + m)
    
    # Find strongly connected components
    finish_order = []
    visited = [False] * (2*m + 1)
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS to find SCCs
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO"
    
    return "YES"
```

#### **Variation 3: Giant Pizza with Probabilities**
**Problem**: Each topping has a probability of being available, find expected satisfiability.
```python
def probabilistic_giant_pizza(n, m, preferences, probabilities):
    # probabilities[i] = probability that topping i is available
    
    # Build implication graph
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Calculate expected satisfiability
    # For each preference (a, b), we need either a or b
    # Probability that a preference is satisfied = 1 - (1-p_a)(1-p_b)
    
    expected_satisfied = 0
    for a, b in preferences:
        p_a = probabilities[a]
        p_b = probabilities[b]
        prob_satisfied = 1 - (1 - p_a) * (1 - p_b)
        expected_satisfied += prob_satisfied
    
    return expected_satisfied / len(preferences)  # Average satisfaction rate
```

#### **Variation 4: Giant Pizza with Multiple Criteria**
**Problem**: Find satisfying assignment optimizing multiple objectives (cost, preference satisfaction, health).
```python
def multi_criteria_giant_pizza(n, m, preferences, costs, health_scores, preference_weights):
    # costs[i] = cost, health_scores[i] = health score, preference_weights[(a, b)] = weight of preference
    
    # Build implication graph
    adj = [[] for _ in range(2*m + 1)]
    adj_rev = [[] for _ in range(2*m + 1)]
    
    for a, b in preferences:
        adj[a].append(b + m)
        adj_rev[b + m].append(a)
        adj[b].append(a + m)
        adj_rev[a + m].append(b)
    
    # Find strongly connected components
    finish_order = []
    visited = [False] * (2*m + 1)
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, 2*m + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS to find SCCs
    visited = [False] * (2*m + 1)
    scc_id = [0] * (2*m + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_scc += 1
            second_dfs(node, current_scc)
    
    # Check satisfiability
    for i in range(1, m + 1):
        if scc_id[i] == scc_id[i + m]:
            return "NO", -1, -1, -1
    
    # Find optimal assignment considering multiple criteria
    assignment = [False] * (m + 1)
    scc_assigned = [False] * (current_scc + 1)
    
    for i in range(1, m + 1):
        if not scc_assigned[scc_id[i]]:
            # Calculate scores for both options
            cost_i = costs[i] if i <= m else 0
            health_i = health_scores[i] if i <= m else 0
            cost_not_i = costs[i - m] if i > m else 0
            health_not_i = health_scores[i - m] if i > m else 0
            
            # Weighted score (lower is better for cost, higher is better for health)
            score_i = cost_i - health_i
            score_not_i = cost_not_i - health_not_i
            
            if score_i <= score_not_i:
                assignment[i] = True
                scc_assigned[scc_id[i]] = True
                scc_assigned[scc_id[i + m]] = True
            else:
                assignment[i + m] = True
                scc_assigned[scc_id[i]] = True
                scc_assigned[scc_id[i + m]] = True
    
    total_cost = sum(costs[i] for i in range(1, m + 1) if assignment[i])
    total_health = sum(health_scores[i] for i in range(1, m + 1) if assignment[i])
    total_preference = sum(preference_weights.get((a, b), 1) for a, b in preferences 
                          if assignment[a] or assignment[b])
    
    return "YES", total_cost, total_health, total_preference
```

#### **Variation 5: Giant Pizza with Dynamic Updates**
**Problem**: Handle dynamic updates to preferences and check satisfiability after each update.
```python
def dynamic_giant_pizza(n, m, initial_preferences, updates):
    # updates = [(preference_to_add, preference_to_remove), ...]
    
    preferences = initial_preferences.copy()
    results = []
    
    for preference_to_add, preference_to_remove in updates:
        # Update preferences
        if preference_to_remove in preferences:
            preferences.remove(preference_to_remove)
        if preference_to_add:
            preferences.append(preference_to_add)
        
        # Rebuild implication graph
        adj = [[] for _ in range(2*m + 1)]
        adj_rev = [[] for _ in range(2*m + 1)]
        
        for a, b in preferences:
            adj[a].append(b + m)
            adj_rev[b + m].append(a)
            adj[b].append(a + m)
            adj_rev[a + m].append(b)
        
        # Find strongly connected components
        finish_order = []
        visited = [False] * (2*m + 1)
        
        def first_dfs(node):
            visited[node] = True
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    first_dfs(neighbor)
            finish_order.append(node)
        
        for i in range(1, 2*m + 1):
            if not visited[i]:
                first_dfs(i)
        
        # Second DFS to find SCCs
        visited = [False] * (2*m + 1)
        scc_id = [0] * (2*m + 1)
        current_scc = 0
        
        def second_dfs(node, scc):
            visited[node] = True
            scc_id[node] = scc
            for neighbor in adj_rev[node]:
                if not visited[neighbor]:
                    second_dfs(neighbor, scc)
        
        for node in reversed(finish_order):
            if not visited[node]:
                current_scc += 1
                second_dfs(node, current_scc)
        
        # Check satisfiability
        satisfiable = True
        for i in range(1, m + 1):
            if scc_id[i] == scc_id[i + m]:
                satisfiable = False
                break
        
        results.append("YES" if satisfiable else "NO")
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Boolean Satisfiability Problems**
- **2-SAT**: Boolean satisfiability with 2 variables per clause
- **3-SAT**: Boolean satisfiability with 3 variables per clause
- **k-SAT**: Boolean satisfiability with k variables per clause
- **SAT**: General boolean satisfiability

#### **2. Constraint Satisfaction Problems**
- **CSP**: Constraint satisfaction problems
- **Logic Programming**: Programming with logical constraints
- **Rule-based Systems**: Systems based on logical rules
- **Expert Systems**: Systems using logical inference

#### **3. Graph Theory Problems**
- **Strongly Connected Components**: Find SCCs in directed graphs
- **Implication Graphs**: Graphs representing logical implications
- **Transitive Closure**: Find reachability in graphs
- **Graph Algorithms**: Various graph algorithms

#### **4. Logic Problems**
- **Propositional Logic**: Logic with propositions
- **First-order Logic**: Logic with quantifiers
- **Modal Logic**: Logic with modalities
- **Temporal Logic**: Logic with time operators

#### **5. Algorithmic Techniques**
- **Kosaraju's Algorithm**: Find strongly connected components
- **Tarjan's Algorithm**: Another SCC algorithm
- **DFS**: Depth-first search for graph traversal
- **Graph Algorithms**: Various graph algorithms

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    preferences = []
    for _ in range(n):
        a, b = map(int, input().split())
        preferences.append((a, b))
    
    result = check_giant_pizza(n, m, preferences)
    print(result)
```

#### **2. Range Queries on Giant Pizza**
```python
def range_giant_pizza_queries(n, m, preferences, queries):
    # queries = [(start_pref, end_pref), ...] - check satisfiability using preferences in range
    
    results = []
    for start, end in queries: subset_preferences = preferences[
start: end+1]
        result = check_giant_pizza(len(subset_preferences), m, subset_preferences)
        results.append(result)
    
    return results
```

#### **3. Interactive Giant Pizza Problems**
```python
def interactive_giant_pizza():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter preferences (a b):")
    preferences = []
    for _ in range(n):
        a, b = map(int, input().split())
        preferences.append((a, b))
    
    result = check_giant_pizza(n, m, preferences)
    print(f"Pizza satisfiable: {result}")
    
    if result == "YES":
        assignment = find_satisfying_assignment(n, m, preferences)
        print(f"Topping assignment: {assignment}")
```

### 🧮 **Mathematical Extensions**

#### **1. Logic Theory**
- **Boolean Algebra**: Mathematical structure of boolean logic
- **Propositional Logic**: Logic of propositions
- **First-order Logic**: Logic with quantifiers
- **Model Theory**: Study of mathematical structures

#### **2. Graph Theory**
- **Strongly Connected Components**: Properties of SCCs
- **Implication Graphs**: Properties of implication graphs
- **Transitive Closure**: Properties of transitive closure
- **Graph Algorithms**: Mathematical foundations of graph algorithms

#### **3. Complexity Theory**
- **NP-Complete Problems**: Complexity of SAT problems
- **P vs NP**: Fundamental complexity question
- **Reduction Theory**: Theory of problem reductions
- **Approximation Algorithms**: Approximate solutions

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **SAT Algorithms**: Various SAT solving algorithms
- **SCC Algorithms**: Kosaraju's, Tarjan's algorithms
- **Graph Algorithms**: DFS, BFS, connectivity algorithms
- **Logic Algorithms**: Logical inference algorithms

#### **2. Mathematical Concepts**
- **Logic Theory**: Mathematical foundations of logic
- **Graph Theory**: Properties and theorems about graphs
- **Complexity Theory**: Computational complexity
- **Algebra**: Boolean algebra and structures

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Logical Programming**: Programming with logic
- **Constraint Programming**: Programming with constraints
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient 2-SAT techniques and shows various extensions for boolean satisfiability problems.* 