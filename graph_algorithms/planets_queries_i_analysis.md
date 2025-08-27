# CSES Planets Queries I - Problem Analysis

## Problem Statement
Given a directed graph with n planets and q queries, for each query find the k-th planet in the path starting from planet a.

### Input
The first input line has two integers n and q: the number of planets and queries.
The second line has n integers t1,t2,…,tn: for each planet, there is a teleporter from planet i to planet ti.
Then there are q lines describing the queries. Each line has two integers a and k: find the k-th planet in the path starting from planet a.

### Output
For each query, print the k-th planet in the path.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ ti ≤ n
- 1 ≤ a ≤ n
- 1 ≤ k ≤ 10^9

### Example
```
Input:
4 3
2 1 4 1
1 1
1 2
1 3

Output:
2
1
2
```

## Solution Progression

### Approach 1: Naive Simulation - O(q * k)
**Description**: Simulate the path for each query.

```python
def planets_queries_i_naive(n, q, teleporters, queries):
    results = []
    
    for a, k in queries:
        current = a
        for _ in range(k):
            current = teleporters[current - 1]
        results.append(current)
    
    return results
```

**Why this is inefficient**: For large k values, this approach becomes too slow.

### Improvement 1: Binary Lifting - O(n log n + q log k)
**Description**: Use binary lifting to answer queries efficiently.

```python
def planets_queries_i_optimized(n, q, teleporters, queries):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Answer queries
    results = []
    for a, k in queries:
        current = a - 1
        for j in range(log_n):
            if k & (1 << j):
                current = up[j][current]
        results.append(current + 1)
    
    return results
```

**Why this improvement works**: We use binary lifting to precompute the 2^j-th ancestor for each node, allowing us to answer queries in O(log k) time.

## Final Optimal Solution

```python
n, q = map(int, input().split())
teleporters = list(map(int, input().split()))

def answer_planets_queries(n, q, teleporters, queries):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Answer queries
    results = []
    for a, k in queries:
        current = a - 1
        for j in range(log_n):
            if k & (1 << j):
                current = up[j][current]
        results.append(current + 1)
    
    return results

# Read queries
queries = []
for _ in range(q):
    a, k = map(int, input().split())
    queries.append((a, k))

result = answer_planets_queries(n, q, teleporters, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Simulation | O(q * k) | O(1) | Simulate path for each query |
| Binary Lifting | O(n log n + q log k) | O(n log n) | Precompute ancestors for efficient queries |

## Key Insights for Other Problems

### 1. **Binary Lifting**
**Principle**: Precompute 2^j-th ancestors to answer queries efficiently.
**Applicable to**: Tree problems, ancestor queries, path problems

### 2. **Ancestor Queries**
**Principle**: Use binary lifting to find k-th ancestor in logarithmic time.
**Applicable to**: Tree problems, ancestor problems, query problems

### 3. **Path Simulation**
**Principle**: Use precomputed data structures to simulate paths efficiently.
**Applicable to**: Path problems, simulation problems, query problems

## Notable Techniques

### 1. **Binary Lifting Implementation**
```python
def build_binary_lifting(n, teleporters):
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    return up
```

### 2. **Query Answering**
```python
def answer_query(up, start, k):
    current = start - 1
    for j in range(20):
        if k & (1 << j):
            current = up[j][current]
    return current + 1
```

### 3. **Binary Lifting Table**
```python
def build_lifting_table(n, teleporters):
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    return up
```

## Problem-Solving Framework

1. **Identify problem type**: This is a binary lifting problem for ancestor queries
2. **Choose approach**: Use binary lifting to precompute ancestors
3. **Build lifting table**: Create 2^j-th ancestor table
4. **Initialize table**: Set up first row with direct teleporters
5. **Fill table**: Use recurrence to fill remaining rows
6. **Answer queries**: Use binary representation of k to find k-th ancestor
7. **Return results**: Output answers for all queries

---

*This analysis shows how to efficiently answer ancestor queries using binary lifting technique.* 