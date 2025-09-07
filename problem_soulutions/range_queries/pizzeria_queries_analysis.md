---
layout: simple
title: "Pizzeria Queries"
permalink: /problem_soulutions/range_queries/pizzeria_queries_analysis
---


# Pizzeria Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand dynamic range query problems with point updates and range minimum queries
- Apply Segment Trees to handle point updates and range minimum queries efficiently
- Implement efficient dynamic range query algorithms with O(log n) time for updates and minimum queries
- Optimize dynamic range queries using Segment Trees and efficient range minimum algorithms
- Handle edge cases in dynamic range queries (empty ranges, large updates, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Segment Trees, range minimum queries, point updates, dynamic range queries, range optimization
- **Data Structures**: Segment trees, range query data structures, update tracking, minimum tracking
- **Mathematical Concepts**: Range queries, minimum finding, update operations, query optimization
- **Programming Skills**: Segment tree implementation, range minimum queries, point updates, algorithm implementation
- **Related Problems**: Dynamic Range Sum Queries (range queries), Range minimum problems, Update problems

## 📋 Problem Description

Given n buildings in a line, each with a pizzeria, process q queries. Each query is either:
1. Update the price of pizzeria at building k to x
2. Find the minimum price of a pizzeria in range [a,b]

This is a dynamic range query problem where we need to efficiently handle both point updates and range minimum queries. We can solve this using a Segment Tree for efficient range minimum queries and point updates.

**Input**: 
- First line: n q (number of buildings and number of queries)
- Second line: n integers p₁, p₂, ..., pₙ (the initial prices of pizzerias)
- Next q lines: queries of the form:
  - "1 k x": update the price of pizzeria at building k to x
  - "2 a b": find the minimum price of a pizzeria in range [a,b]

**Output**: 
- Print the answer to each minimum query

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ pᵢ ≤ 10⁹
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ n

**Example**:
```
Input:
5 3
1 2 3 4 5
2 1 3
1 2 0
2 1 3

Output:
1
0
```

**Explanation**: 
- Initial prices: [1, 2, 3, 4, 5]
- Query 1: Minimum price in range [1,3] → 1 (minimum of 1, 2, 3)
- Update: Change price at building 2 from 2 to 0 → [1, 0, 3, 4, 5]
- Query 2: Minimum price in range [1,3] → 0 (minimum of 1, 0, 3)

### 📊 Visual Example

**Input Buildings and Prices:**
```
Building: 1  2  3  4  5
Price:   [1, 2, 3, 4, 5]
```

**Query Processing Visualization:**
```
Query 1: Minimum price in range [1,3]
┌─────────────────────────────────────┐
│ Range [1,3]: min(1, 2, 3) = 1     │
│ Highlighted: [1, 2, 3, 4, 5]      │
│           ↑  ↑  ↑                  │
│           min                      │
└─────────────────────────────────────┘
Result: 1

Update: Change building 2 price from 2 to 0
┌─────────────────────────────────────┐
│ Before: [1, 2, 3, 4, 5]           │
│ After:  [1, 0, 3, 4, 5]           │
│              ↑                     │
└─────────────────────────────────────┘

Query 2: Minimum price in range [1,3]
┌─────────────────────────────────────┐
│ Range [1,3]: min(1, 0, 3) = 0     │
│ Highlighted: [1, 0, 3, 4, 5]      │
│           ↑  ↑  ↑                  │
│              min                   │
└─────────────────────────────────────┘
Result: 0
```

**Segment Tree Construction:**
```
Original Array: [1, 2, 3, 4, 5]

Segment Tree:
┌─────────────────────────────────────┐
│               1                     │
│        /              \             │
│       1                4            │
│    /    \            /    \         │
│   1      3          4      5        │
│  / \    / \        / \    / \       │
│ 1  2   3  4       4  5   5  5       │
└─────────────────────────────────────┘

Update (building 2: 2 → 0):
┌─────────────────────────────────────┐
│               0                     │
│        /              \             │
│       0                4            │
│    /    \            /    \         │
│   0      3          4      5        │
│  / \    / \        / \    / \       │
│ 1  0   3  4       4  5   5  5       │
└─────────────────────────────────────┘
```

**Range Query Processing:**
```
Query [1,3]: Find minimum in range [1,3]
┌─────────────────────────────────────┐
│ Query covers nodes:                 │
│ - Node [1,2]: min = 0              │
│ - Node [3,3]: min = 3              │
│ Result: min(0, 3) = 0              │
└─────────────────────────────────────┘
```

**Binary Indexed Tree for Range Minimum:**
```
Note: BIT is not suitable for range minimum queries
┌─────────────────────────────────────┐
│ BIT works well for:                 │
│ - Range sum queries                 │
│ - Point updates                     │
│                                     │
│ BIT does NOT work for:              │
│ - Range minimum queries             │
│ - Range maximum queries             │
│                                     │
│ Reason: BIT uses prefix operations  │
│ which don't preserve min/max        │
│ properties across ranges            │
└─────────────────────────────────────┘
```

**Sparse Table Alternative:**
```
Original Array: [1, 2, 3, 4, 5]

Sparse Table (for static queries):
┌─────────────────────────────────────┐
│ Level 0: [1, 2, 3, 4, 5]          │
│ Level 1: [1, 2, 3, 4]             │
│ Level 2: [1, 2]                   │
└─────────────────────────────────────┘

Query [1,3]: Length = 3, k = 1
┌─────────────────────────────────────┐
│ Compare:                           │
│ - ST[1][1] = min(arr[1], arr[2]) = 1│
│ - ST[1][3-2^1+1] = ST[1][2] = 2   │
│ Result: min(1, 2) = 1              │
└─────────────────────────────────────┘
```

**Time Complexity Analysis:**
```
Naive Approach: O(q × n)
┌─────────────────────────────────────┐
│ Each minimum query: O(n) scan      │
│ Each update: O(1)                  │
│ Total: O(q × n)                    │
└─────────────────────────────────────┘

Segment Tree: O(log n) per operation
┌─────────────────────────────────────┐
│ Each update: O(log n)              │
│ Each query: O(log n)               │
│ Total: O(q × log n)                │
└─────────────────────────────────────┘

Sparse Table: O(n log n + q) - Static only
┌─────────────────────────────────────┐
│ Preprocessing: O(n log n)           │
│ Each query: O(1)                   │
│ Updates: Not supported             │
│ Total: O(n log n + q)              │
└─────────────────────────────────────┘
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct array updates and minimum calculations.

```python
def pizzeria_queries_naive(n, q, prices, queries):
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            prices[k-1] = x  # 1-indexed to 0-indexed
        else:  # Minimum query
            a, b = query[1], query[2]
            # Find minimum in range [a,b] (1-indexed)
            min_price = min(prices[a-1:b])
            result.append(min_price)
    
    return result
```

**Why this is inefficient**: Each minimum query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Segment Tree - O(log n) per operation
**Description**: Use segment tree for efficient point updates and range minimum queries.

```python
def pizzeria_queries_segment_tree(n, q, prices, queries):
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result
    
    # Initialize segment tree
    st = SegmentTree(prices)
    result = []
    
    for query in queries: if query[0] == 1:  # Update 
query: 1 k x
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else: # Minimum 
query: 2 a b
            a, b = query[1], query[2]
            min_price = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_price)
    
    return result
```

**Why this improvement works**: Segment tree provides O(log n) time for both updates and range minimum queries.

## Final Optimal Solution

```python
n, q = map(int, input().split())
prices = list(map(int, input().split()))
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

def process_pizzeria_queries(n, q, prices, queries):
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result
    
    # Initialize segment tree
    st = SegmentTree(prices)
    result = []
    
    for query in queries: if query[0] == 1:  # Update 
query: 1 k x
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else: # Minimum 
query: 2 a b
            a, b = query[1], query[2]
            min_price = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_price)
    
    return result

result = process_pizzeria_queries(n, q, prices, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(1) | Direct array operations |
| Segment Tree | O(log n) per operation | O(n) | Efficient point updates and range minimum queries |

## Key Insights for Other Problems

### 1. **Segment Tree**
**Principle**: Use segment tree for efficient point updates and range queries.
**Applicable to**: Range minimum/maximum problems, point update problems, dynamic range queries

### 2. **Range Minimum Queries**
**Principle**: Use segment tree to find minimum value in any range efficiently.
**Applicable to**: Range minimum problems, optimization problems, query problems

### 3. **Point Updates with Range Queries**
**Principle**: Use data structures that support both point updates and range queries efficiently.
**Applicable to**: Dynamic range problems, update-query problems, array problems

## Notable Techniques

### 1. **Segment Tree Implementation**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [float('inf')] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
    
    def update(self, index, value):
        index += self.size
        self.tree[index] = value
        index //= 2
        while index >= 1:
            self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
            index //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = float('inf')
        
        while left < right:
            if left % 2 == 1:
                result = min(result, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                result = min(result, self.tree[right])
            left //= 2
            right //= 2
        
        return result
```

### 2. **Point Update and Range Query**
```python
def point_update_range_min(n, array, queries):
    st = SegmentTree(array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            st.update(k-1, x)
        else:  # Range minimum query
            a, b = query[1], query[2]
            result.append(st.query(a-1, b))
    
    return result
```

### 3. **Efficient Range Operations**
```python
def efficient_range_min_queries(n, operations):
    st = SegmentTree([0] * n)
    result = []
    
    for op in operations:
        if op[0] == 1:  # Point update
            st.update(op[1]-1, op[2])
        else:  # Range minimum query
            result.append(st.query(op[1]-1, op[2]))
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range minimum problem with point updates
2. **Choose approach**: Use segment tree for efficient operations
3. **Initialize data structure**: Build segment tree from initial array
4. **Process queries**: Handle updates and range minimum queries using segment tree
5. **Update operations**: Use point updates in segment tree
6. **Range queries**: Use range minimum query method in segment tree
7. **Return result**: Output answers for all range minimum queries

---

*This analysis shows how to efficiently handle dynamic range minimum queries using segment tree.*

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Pizzeria Queries with Range Updates**
**Problem**: Support range updates (modify prices of pizzerias in a range) and point queries.
```python
def pizzeria_queries_range_updates(n, q, prices, operations):
    # Use Segment Tree with lazy propagation
    class LazySegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            self.lazy = [None] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def push(self, node, left, right):
            if self.lazy[node] is not None:
                self.tree[node] = self.lazy[node]
                if left != right:
                    self.lazy[2 * node] = self.lazy[node]
                    self.lazy[2 * node + 1] = self.lazy[node]
                self.lazy[node] = None
        
        def range_update(self, node, left, right, l, r, val):
            self.push(node, left, right)
            if r < left or l > right:
                return
            if l <= left and right <= r:
                self.lazy[node] = val
                self.push(node, left, right)
                return
            mid = (left + right) // 2
            self.range_update(2 * node, left, mid, l, r, val)
            self.range_update(2 * node + 1, mid + 1, right, l, r, val)
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
        
        def point_query(self, node, left, right, index):
            self.push(node, left, right)
            if left == right:
                return self.tree[node]
            mid = (left + right) // 2
            if index <= mid:
                return self.point_query(2 * node, left, mid, index)
            else:
                return self.point_query(2 * node + 1, mid + 1, right, index)
    
    st = LazySegmentTree(prices)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Range Update
            l, r, val = op[1], op[2], op[3]
            st.range_update(1, 0, st.size - 1, l-1, r-1, val)
        else:  # Point Query
            k = op[1]
            result = st.point_query(1, 0, st.size - 1, k-1)
            results.append(result)
    
    return results
```

#### **Variation 2: Pizzeria Queries with Multiple Criteria**
**Problem**: Each pizzeria has price and rating, find minimum price with minimum rating threshold.
```python
def pizzeria_queries_multiple_criteria(n, q, prices, ratings, operations):
    # Use Segment Tree with multiple criteria
    class MultiCriteriaSegmentTree:
        def __init__(self, prices, ratings):
            self.n = len(prices)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.price_tree = [float('inf')] * (2 * self.size)
            self.rating_tree = [0] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.price_tree[self.size + i] = prices[i]
                self.rating_tree[self.size + i] = ratings[i]
            for i in range(self.size - 1, 0, -1):
                self.price_tree[i] = min(self.price_tree[2 * i], self.price_tree[2 * i + 1])
                self.rating_tree[i] = max(self.rating_tree[2 * i], self.rating_tree[2 * i + 1])
        
        def update(self, index, price, rating):
            index += self.size
            self.price_tree[index] = price
            self.rating_tree[index] = rating
            index //= 2
            while index >= 1:
                self.price_tree[index] = min(self.price_tree[2 * index], self.price_tree[2 * index + 1])
                self.rating_tree[index] = max(self.rating_tree[2 * index], self.rating_tree[2 * index + 1])
                index //= 2
        
        def query_with_rating(self, left, right, min_rating):
            return self._query_with_rating(1, 0, self.size - 1, left, right, min_rating)
        
        def _query_with_rating(self, node, left, right, l, r, min_rating):
            if r < left or l > right:
                return float('inf')
            if l <= left and right <= r: if self.rating_tree[node] >= 
min_rating: return self.price_tree[node]
                return float('inf')
            mid = (left + right) // 2
            return min(
                self._query_with_rating(2 * node, left, mid, l, r, min_rating),
                self._query_with_rating(2 * node + 1, mid + 1, right, l, r, min_rating)
            )
    
    st = MultiCriteriaSegmentTree(prices, ratings)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, price, rating = op[1], op[2], op[3]
            st.update(k-1, price, rating)
        else:  # Query with rating threshold
            l, r, min_rating = op[1], op[2], op[3]
            result = st.query_with_rating(l-1, r-1, min_rating)
            results.append(result if result != float('inf') else -1)
    
    return results
```

#### **Variation 3: Pizzeria Queries with Distance Constraints**
**Problem**: Find minimum price pizzeria within a certain distance from a given point.
```python
def pizzeria_queries_with_distance(n, q, prices, positions, operations):
    # Use Segment Tree with distance constraints
    class DistanceSegmentTree:
        def __init__(self, prices, positions):
            self.n = len(prices)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.price_tree = [float('inf')] * (2 * self.size)
            self.positions = positions
            
            # Build tree
            for i in range(self.n):
                self.price_tree[self.size + i] = prices[i]
            for i in range(self.size - 1, 0, -1):
                self.price_tree[i] = min(self.price_tree[2 * i], self.price_tree[2 * i + 1])
        
        def update(self, index, price):
            index += self.size
            self.price_tree[index] = price
            index //= 2
            while index >= 1:
                self.price_tree[index] = min(self.price_tree[2 * index], self.price_tree[2 * index + 1])
                index //= 2
        
        def query_within_distance(self, center, max_distance):
            # Find all positions within distance and query their minimum price
            min_price = float('inf')
            for i in range(self.n):
                if abs(self.positions[i] - center) <= max_distance:
                    min_price = min(min_price, self.price_tree[self.size + i])
            return min_price if min_price != float('inf') else -1
    
    st = DistanceSegmentTree(prices, positions)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, price = op[1], op[2]
            st.update(k-1, price)
        else:  # Query within distance
            center, max_distance = op[1], op[2]
            result = st.query_within_distance(center, max_distance)
            results.append(result)
    
    return results
```

#### **Variation 4: Pizzeria Queries with Time Windows**
**Problem**: Each pizzeria has different prices at different times, handle time-based queries.
```python
def pizzeria_queries_time_windows(n, q, prices, time_slots, operations):
    # Use Segment Tree with time-based pricing
    class TimeSegmentTree:
        def __init__(self, prices, time_slots):
            self.n = len(prices)
            self.time_slots = time_slots  # List of (start_time, end_time, price) for each pizzeria
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.trees = {}  # Separate tree for each time slot
        
        def get_price_at_time(self, pizzeria, time):
            # Find the price for pizzeria at given time
            for start, end, price in self.time_slots[pizzeria]:
                if start <= time <= end:
                    return price
            return float('inf')
        
        def build_tree_for_time(self, time):
            if time in self.trees:
                return self.trees[time]
            
            tree = [float('inf')] * (2 * self.size)
            for i in range(self.n):
                tree[self.size + i] = self.get_price_at_time(i, time)
            for i in range(self.size - 1, 0, -1):
                tree[i] = min(tree[2 * i], tree[2 * i + 1])
            
            self.trees[time] = tree
            return tree
        
        def query_at_time(self, left, right, time):
            tree = self.build_tree_for_time(time)
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, tree[right])
                left //= 2
                right //= 2
            
            return result if result != float('inf') else -1
    
    st = TimeSegmentTree(prices, time_slots)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update time slot
            k, start, end, price = op[1], op[2], op[3], op[4]
            st.time_slots[k-1].append((start, end, price))
            st.trees.clear()  # Invalidate cached trees
        else:  # Query at specific time
            l, r, time = op[1], op[2], op[3]
            result = st.query_at_time(l-1, r-1, time)
            results.append(result)
    
    return results
```

#### **Variation 5: Pizzeria Queries with Multiple Pizzerias**
**Problem**: Each building can have multiple pizzerias, find minimum price across all pizzerias in range.
```python
def pizzeria_queries_multiple_pizzerias(n, q, pizzeria_lists, operations):
    # Use Segment Tree with multiple pizzerias per building
    class MultiPizzeriaSegmentTree:
        def __init__(self, pizzeria_lists):
            self.n = len(pizzeria_lists)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build tree with minimum price per building
            for i in range(self.n):
                min_price = min(pizzeria_lists[i]) if pizzeria_lists[i] else float('inf')
                self.tree[self.size + i] = min_price
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, building, pizzeria_index, new_price):
            building += self.size
            # Update the specific pizzeria price
            pizzeria_lists[building - self.size][pizzeria_index] = new_price
            # Update building's minimum price
            min_price = min(pizzeria_lists[building - self.size])
            self.tree[building] = min_price
            
            building //= 2
            while building >= 1:
                self.tree[building] = min(self.tree[2 * building], self.tree[2 * building + 1])
                building //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result if result != float('inf') else -1
    
    st = MultiPizzeriaSegmentTree(pizzeria_lists)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update specific pizzeria
            building, pizzeria_idx, price = op[1], op[2], op[3]
            st.update(building-1, pizzeria_idx-1, price)
        else:  # Query minimum across range
            l, r = op[1], op[2]
            result = st.query(l-1, r-1)
            results.append(result)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Dynamic Range Query Data Structures**
- **Segment Tree**: O(log n) point updates and range queries
- **Binary Indexed Tree**: O(log n) operations but limited to specific queries
- **Sparse Table**: O(1) queries but static
- **Lazy Segment Tree**: Efficient range updates

#### **2. Range Query Types**
- **Range Minimum**: Find minimum in range
- **Range Maximum**: Find maximum in range
- **Range Sum**: Find sum in range
- **Range Count**: Count elements in range

#### **3. Advanced Range Techniques**
- **Lazy Propagation**: Efficient range updates
- **Persistent Segment Tree**: Handle historical queries
- **2D Range Queries**: Extend to multiple dimensions
- **Offline Processing**: Process queries in optimal order

#### **4. Optimization Problems**
- **Optimal Range Selection**: Find optimal range for queries
- **Range with Constraints**: Add additional constraints to queries
- **Weighted Range Queries**: Elements have weights
- **Time-based Queries**: Handle temporal data

#### **5. Competitive Programming Patterns**
- **Binary Search**: Find optimal ranges
- **Two Pointers**: Efficient range processing
- **Sliding Window**: Optimize consecutive ranges
- **Greedy**: Optimize range selection

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    prices = list(map(int, input().split()))
    
    st = SegmentTree(prices)
    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            st.update(k-1, x)
        else:  # Query
            a, b = query[1], query[2]
            result = st.query(a-1, b)
            print(result)
```

#### **2. Pizzeria Queries with Aggregation**
```python
def pizzeria_queries_aggregation(n, q, prices, operations):
    # Support multiple aggregation functions
    class AggregationSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.min_tree = [float('inf')] * (2 * self.size)
            self.max_tree = [-float('inf')] * (2 * self.size)
            self.sum_tree = [0] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.min_tree[self.size + i] = data[i]
                self.max_tree[self.size + i] = data[i]
                self.sum_tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.min_tree[i] = min(self.min_tree[2 * i], self.min_tree[2 * i + 1])
                self.max_tree[i] = max(self.max_tree[2 * i], self.max_tree[2 * i + 1])
                self.sum_tree[i] = self.sum_tree[2 * i] + self.sum_tree[2 * i + 1]
        
        def update(self, index, value):
            index += self.size
            self.min_tree[index] = value
            self.max_tree[index] = value
            self.sum_tree[index] = value
            index //= 2
            while index >= 1:
                self.min_tree[index] = min(self.min_tree[2 * index], self.min_tree[2 * index + 1])
                self.max_tree[index] = max(self.max_tree[2 * index], self.max_tree[2 * index + 1])
                self.sum_tree[index] = self.sum_tree[2 * index] + self.sum_tree[2 * index + 1]
                index //= 2
        
        def query(self, left, right, op):
            if op == 'MIN':
                return self._query_min(left, right)
            elif op == 'MAX':
                return self._query_max(left, right)
            elif op == 'SUM':
                return self._query_sum(left, right)
        
        def _query_min(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.min_tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.min_tree[right])
                left //= 2
                right //= 2
            return result
    
    st = AggregationSegmentTree(prices)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Query
            l, r, query_type = op[1], op[2], op[3]
            result = st.query(l-1, r-1, query_type)
            results.append(result)
    
    return results
```

#### **3. Interactive Pizzeria Queries**
```python
def interactive_pizzeria_queries(n, prices):
    # Handle interactive queries
    st = SegmentTree(prices)
    
    while True: 
try: query = input().strip()
            if query == 'END':
                break
            
            parts = query.split()
            if parts[0] == 'UPDATE':
                k, x = int(parts[1]), int(parts[2])
                st.update(k-1, x)
                print(f"Updated pizzeria {k} to price {x}")
            elif parts[0] == 'QUERY':
                a, b = int(parts[1]), int(parts[2])
                result = st.query(a-1, b-1)
                print(f"Minimum price in range [{a},{b}]: {result}")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Range Query Properties**
- **Idempotency**: min(min(a,b), min(c,d)) = min(a,b,c,d)
- **Commutativity**: min(a,b) = min(b,a)
- **Associativity**: min(min(a,b), c) = min(a, min(b,c))
- **Monotonicity**: If a ≤ b, then min(a,c) ≤ min(b,c)

#### **2. Optimization Techniques**
- **Early Termination**: Stop if minimum is found
- **Binary Search**: Find ranges with specific minimums
- **Caching**: Store frequently accessed ranges
- **Compression**: Handle sparse ranges efficiently

#### **3. Advanced Mathematical Concepts**
- **Monotonic Stack**: Efficient minimum tracking
- **Cartesian Tree**: Alternative minimum representation
- **LCA Reduction**: Reduce range minimum to LCA problem
- **Fourier Transform**: Fast range operations using FFT

#### **4. Algorithmic Improvements**
- **Block Decomposition**: Divide array into blocks
- **Lazy Propagation**: Efficient range updates
- **Compression**: Handle sparse arrays efficiently
- **Parallel Processing**: Use multiple cores for large datasets

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(log n) per query and update
- **Space Complexity**: O(n) for segment tree
- **Why it works**: Segment tree enables efficient range minimum queries and point updates in O(log n) time

### Key Implementation Points
- Use segment tree for efficient range minimum queries
- Handle point updates efficiently
- Segment tree supports both range queries and point updates
- Lazy propagation for range updates if needed

## 🎯 Key Insights

### Important Concepts and Patterns
- **Segment Tree**: Essential for efficient range minimum queries
- **Range Minimum**: Most efficient way to find minimum in a range
- **Point Updates**: Update single elements efficiently
- **Range Queries**: Query minimum value in any range

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Pizzeria Queries with Range Updates**
```python
class RangeUpdatePizzeriaQueries:
    def __init__(self, prices):
        self.n = len(prices)
        self.prices = prices.copy()
        
        # Segment tree with lazy propagation
        self.tree = [float('inf')] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        
        self.build(1, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.prices[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node, start, mid)
            self.build(2 * node + 1, mid + 1, end)
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
    
    def push_lazy(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node]
            
            if start != end:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            
            self.lazy[node] = 0
    
    def range_update(self, node, start, end, l, r, val):
        self.push_lazy(node, start, end)
        
        if start > end or start > r or end < l:
            return
        
        if start >= l and end <= r:
            self.lazy[node] += val
            self.push_lazy(node, start, end)
            return
        
        mid = (start + end) // 2
        self.range_update(2 * node, start, mid, l, r, val)
        self.range_update(2 * node + 1, mid + 1, end, l, r, val)
        
        self.push_lazy(2 * node, start, mid)
        self.push_lazy(2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
    
    def range_minimum(self, node, start, end, l, r):
        self.push_lazy(node, start, end)
        
        if start > end or start > r or end < l:
            return float('inf')
        
        if start >= l and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_min = self.range_minimum(2 * node, start, mid, l, r)
        right_min = self.range_minimum(2 * node + 1, mid + 1, end, l, r)
        
        return min(left_min, right_min)
    
    def point_update(self, node, start, end, pos, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if pos <= mid:
                self.point_update(2 * node, start, mid, pos, val)
            else:
                self.point_update(2 * node + 1, mid + 1, end, pos, val)
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
```

#### **2. Pizzeria Queries with Multiple Operations**
```python
class MultiOperationPizzeriaQueries:
    def __init__(self, prices):
        self.n = len(prices)
        self.prices = prices.copy()
        
        # Segment trees for different operations
        self.min_tree = [float('inf')] * (4 * self.n)
        self.max_tree = [float('-inf')] * (4 * self.n)
        self.sum_tree = [0] * (4 * self.n)
        
        self.build(1, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.min_tree[node] = self.prices[start]
            self.max_tree[node] = self.prices[start]
            self.sum_tree[node] = self.prices[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node, start, mid)
            self.build(2 * node + 1, mid + 1, end)
            
            self.min_tree[node] = min(self.min_tree[2 * node], self.min_tree[2 * node + 1])
            self.max_tree[node] = max(self.max_tree[2 * node], self.max_tree[2 * node + 1])
            self.sum_tree[node] = self.sum_tree[2 * node] + self.sum_tree[2 * node + 1]
    
    def range_minimum(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return float('inf')
        
        if start >= l and end <= r:
            return self.min_tree[node]
        
        mid = (start + end) // 2
        left_min = self.range_minimum(2 * node, start, mid, l, r)
        right_min = self.range_minimum(2 * node + 1, mid + 1, end, l, r)
        
        return min(left_min, right_min)
    
    def range_maximum(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return float('-inf')
        
        if start >= l and end <= r:
            return self.max_tree[node]
        
        mid = (start + end) // 2
        left_max = self.range_maximum(2 * node, start, mid, l, r)
        right_max = self.range_maximum(2 * node + 1, mid + 1, end, l, r)
        
        return max(left_max, right_max)
    
    def range_sum(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return 0
        
        if start >= l and end <= r:
            return self.sum_tree[node]
        
        mid = (start + end) // 2
        left_sum = self.range_sum(2 * node, start, mid, l, r)
        right_sum = self.range_sum(2 * node + 1, mid + 1, end, l, r)
        
        return left_sum + right_sum
    
    def get_range_stats(self, a, b):
        # Get comprehensive statistics for range [a, b]
        min_price = self.range_minimum(1, 0, self.n - 1, a - 1, b - 1)
        max_price = self.range_maximum(1, 0, self.n - 1, a - 1, b - 1)
        total_cost = self.range_sum(1, 0, self.n - 1, a - 1, b - 1)
        count = b - a + 1
        avg_price = total_cost / count if count > 0 else 0
        
        return {
            'min_price': min_price,
            'max_price': max_price,
            'total_cost': total_cost,
            'count': count,
            'average_price': avg_price
        }
```

#### **3. Pizzeria Queries with Distance Constraints**
```python
class DistanceConstrainedPizzeriaQueries:
    def __init__(self, prices, distances):
        self.n = len(prices)
        self.prices = prices.copy()
        self.distances = distances.copy()  # Distance from building 1
        
        # Segment tree for prices
        self.price_tree = [float('inf')] * (4 * self.n)
        self.build_price_tree(1, 0, self.n - 1)
        
        # Segment tree for distances
        self.distance_tree = [0] * (4 * self.n)
        self.build_distance_tree(1, 0, self.n - 1)
    
    def build_price_tree(self, node, start, end):
        if start == end:
            self.price_tree[node] = self.prices[start]
        else:
            mid = (start + end) // 2
            self.build_price_tree(2 * node, start, mid)
            self.build_price_tree(2 * node + 1, mid + 1, end)
            self.price_tree[node] = min(self.price_tree[2 * node], self.price_tree[2 * node + 1])
    
    def build_distance_tree(self, node, start, end):
        if start == end:
            self.distance_tree[node] = self.distances[start]
        else:
            mid = (start + end) // 2
            self.build_distance_tree(2 * node, start, mid)
            self.build_distance_tree(2 * node + 1, mid + 1, end)
            self.distance_tree[node] = max(self.distance_tree[2 * node], self.distance_tree[2 * node + 1])
    
    def range_minimum_price(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return float('inf')
        
        if start >= l and end <= r:
            return self.price_tree[node]
        
        mid = (start + end) // 2
        left_min = self.range_minimum_price(2 * node, start, mid, l, r)
        right_min = self.range_minimum_price(2 * node + 1, mid + 1, end, l, r)
        
        return min(left_min, right_min)
    
    def range_maximum_distance(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return 0
        
        if start >= l and end <= r:
            return self.distance_tree[node]
        
        mid = (start + end) // 2
        left_max = self.range_maximum_distance(2 * node, start, mid, l, r)
        right_max = self.range_maximum_distance(2 * node + 1, mid + 1, end, l, r)
        
        return max(left_max, right_max)
    
    def find_cheapest_within_distance(self, start_building, max_distance):
        # Find cheapest pizzeria within max_distance from start_building
        start_pos = start_building - 1
        start_distance = self.distances[start_pos]
        
        # Binary search for range
        left = start_pos
        right = self.n - 1
        
        # Find rightmost building within distance
        while left <= right:
            mid = (left + right) // 2
            if self.distances[mid] - start_distance <= max_distance:
                left = mid + 1
            else:
                right = mid - 1
        
        if right >= start_pos:
            return self.range_minimum_price(1, 0, self.n - 1, start_pos, right)
        else:
            return float('inf')
```

## 🔗 Related Problems

### Links to Similar Problems
- **Range Queries**: Static Range Minimum Queries, Range Update Queries
- **Segment Tree**: Range Sum Queries, Range XOR Queries
- **Minimum Queries**: Range minimum, Point updates
- **Data Structures**: Segment tree, Sparse table

## 📚 Learning Points

### Key Takeaways
- **Segment tree** is essential for efficient range minimum queries
- **Range minimum** can be computed efficiently using segment trees
- **Point updates** are handled efficiently in segment trees
- **Range queries** are fundamental operations in competitive programming

---

**Practice these variations to master dynamic range query techniques and segment tree operations!** 🎯 