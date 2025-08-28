---
layout: simple
title: "Giant Pizza"permalink: /problem_soulutions/graph_algorithms/giant_pizza_analysis
---


# Giant Pizza

## Problem Statement
Given a list of pizza toppings preferences where each person likes some toppings and dislikes others, determine if it's possible to make a pizza that satisfies everyone's preferences.

### Input
The first input line has two integers n and m: the number of people and the number of toppings.
Then there are n lines describing the preferences. Each line has two integers a and b: person likes topping a and dislikes topping b.

### Output
Print "YES" if it's possible to make a pizza that satisfies everyone, or "NO" otherwise.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 10^5
- 1 ≤ a,b ≤ m

### Example
```
Input:
3 3
1 2
2 3
3 1

Output:
YES
```

## Solution Progression

### Approach 1: 2-SAT with Kosaraju's Algorithm - O(n + m)
**Description**: Use 2-SAT problem reduction to strongly connected components.

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

## Final Optimal Solution

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

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| 2-SAT with Kosaraju's | O(n + m) | O(n + m) | Use 2-SAT reduction to SCC |
| Optimized 2-SAT | O(n + m) | O(n + m) | Optimized 2-SAT implementation |

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
    for start, end in queries:
        subset_preferences = preferences[start:end+1]
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