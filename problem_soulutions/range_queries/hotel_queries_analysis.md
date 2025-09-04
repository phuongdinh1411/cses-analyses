---
layout: simple
title: "Hotel Queries - First Hotel with Sufficient Rooms"
permalink: /problem_soulutions/range_queries/hotel_queries_analysis
---

# Hotel Queries - First Hotel with Sufficient Rooms

## 📋 Problem Description

There are n hotels along a highway. For each group of tourists, you want to assign a hotel with the minimum number of rooms that can accommodate the group. Process q queries where each query asks for the first hotel that can accommodate a group of size x.

This is a classic range query problem that requires efficiently finding the first hotel with sufficient capacity. The solution involves using data structures like Segment Tree or Binary Indexed Tree to achieve O(log n) query time.

**Input**: 
- First line: n and q (number of hotels and queries)
- Second line: n integers (number of rooms in each hotel)
- Next q lines: x (size of each group)

**Output**: 
- Print the answer to each query (1-indexed hotel number, or 0 if no hotel can accommodate)

**Constraints**:
- 1 ≤ n, q ≤ 2×10⁵
- 1 ≤ hi ≤ 10⁹
- 1 ≤ x ≤ 10⁹

**Example**:
```
Input:
5 3
2 1 4 1 2
4
2
1

Output:
3
1
1

Explanation**: 
- Query 1: group size 4, first hotel with ≥4 rooms is hotel 3 (4 rooms)
- Query 2: group size 2, first hotel with ≥2 rooms is hotel 1 (2 rooms)
- Query 3: group size 1, first hotel with ≥1 room is hotel 1 (2 rooms)
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Efficiently find the first hotel with sufficient capacity for each group
- **Key Insight**: Use data structures like Segment Tree for O(log n) query time
- **Challenge**: Avoid O(q×n) complexity with naive linear search

### Step 2: Initial Approach
**Linear search for each query (inefficient but correct):**

```python
def hotel_queries_naive(n, q, hotels, queries):
    results = []
    
    for x in queries:
        found = False
        for i in range(n):
            if hotels[i] >= x:
                results.append(i + 1)  # Convert to 1-indexed
                found = True
                break
        if not found:
            results.append(0)
    
    return results
```

**Why this is inefficient**: For each query, we need to iterate through all hotels, leading to O(q × n) time complexity.

### Improvement 1: Segment Tree with Range Maximum - O(n + q log n)
**Description**: Use Segment Tree to find the first hotel with sufficient rooms efficiently.

```python
def hotel_queries_segment_tree(n, q, hotels, queries):
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
        
        def find_first_ge(self, target):
            # Find the first position with value >= target
            return self._find_first_ge(1, 0, self.size - 1, target)
        
        def _find_first_ge(self, node, left, right, target):
            if left >= self.n:
                return -1
            
            if self.tree[node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            if self.tree[2 * node] >= target:
                result = self._find_first_ge(2 * node, left, mid, target)
                if result != -1:
                    return result
            
            # Check right child
            return self._find_first_ge(2 * node + 1, mid + 1, right, target)
    
    # Initialize Segment Tree
    st = SegmentTree(hotels)
    
    results = []
    for x in queries:
        pos = st.find_first_ge(x)
        if pos != -1:
            results.append(pos + 1)  # Convert to 1-indexed
        else:
            results.append(0)
    
    return results
```

**Why this improvement works**: Segment Tree allows us to find the first hotel with sufficient rooms in O(log n) time per query.

### Step 3: Optimization/Alternative
**Binary Indexed Tree approach (alternative to Segment Tree):**

### Step 4: Complete Solution

```python
n, q = map(int, input().split())
hotels = list(map(int, input().split()))

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
    
    def find_first_ge(self, target):
        # Find the first position with value >= target
        return self._find_first_ge(1, 0, self.size - 1, target)
    
    def _find_first_ge(self, node, left, right, target):
        if left >= self.n:
            return -1
        
        if self.tree[node] < target:
            return -1
        
        if left == right:
            return left if left < self.n else -1
        
        mid = (left + right) // 2
        
        # Check left child first
        if self.tree[2 * node] >= target:
            result = self._find_first_ge(2 * node, left, mid, target)
            if result != -1:
                return result
        
        # Check right child
        return self._find_first_ge(2 * node + 1, mid + 1, right, target)

# Initialize Segment Tree
st = SegmentTree(hotels)

# Process queries
for _ in range(q):
    x = int(input())
    pos = st.find_first_ge(x)
    if pos != -1:
        print(pos + 1)  # Convert to 1-indexed
    else:
        print(0)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic queries (should return correct hotel indices)
- **Test 2**: No available hotels (should return 0)
- **Test 3**: Multiple hotels with same capacity (should return first one)
- **Test 4**: Large number of queries (should handle efficiently)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(1) | Linear search for each query |
| Segment Tree | O(n + q log n) | O(n) | Use Segment Tree for range queries |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Segment Tree**: Efficient data structure for range queries and updates
- **First Greater/Equal**: Find first element satisfying a condition
- **Range Queries**: Efficiently answer multiple queries on static data
- **Data Structure Choice**: Choose appropriate structure based on operation types

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Hotel Queries with Dynamic Updates**
```python
def hotel_queries_dynamic(n, q, hotels, operations):
    # Handle hotel queries with dynamic room updates
    
    class DynamicSegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, pos, val):
            pos += self.size
            self.tree[pos] = val
            pos //= 2
            while pos >= 1:
                self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])
                pos //= 2
        
        def find_first_ge(self, target):
            return self._find_first_ge(1, 0, self.size - 1, target)
        
        def _find_first_ge(self, node, left, right, target):
            if left >= self.n:
                return -1
            
            if self.tree[node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            if self.tree[2 * node] >= target:
                result = self._find_first_ge(2 * node, left, mid, target)
                if result != -1:
                    return result
            
            # Check right child
            return self._find_first_ge(2 * node + 1, mid + 1, right, target)
    
    st = DynamicSegmentTree(hotels)
    results = []
    
    for op in operations:
        if op[0] == 'U':  # Update
            pos, val = op[1], op[2]
            st.update(pos - 1, val)  # Convert to 0-indexed
            hotels[pos - 1] = val
        else:  # Query
            x = op[1]
            pos = st.find_first_ge(x)
            if pos != -1:
                results.append(pos + 1)  # Convert to 1-indexed
            else:
                results.append(0)
    
    return results
```

#### **2. Hotel Queries with Multiple Criteria**
```python
def hotel_queries_multiple_criteria(n, q, hotels, criteria, queries):
    # Handle hotel queries with multiple criteria (rooms, price, rating)
    
    class MultiCriteriaSegmentTree:
        def __init__(self, hotels, prices, ratings):
            self.n = len(hotels)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            
            # Separate trees for each criteria
            self.rooms_tree = [0] * (2 * self.size)
            self.prices_tree = [float('inf')] * (2 * self.size)
            self.ratings_tree = [0] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.rooms_tree[self.size + i] = hotels[i]
                self.prices_tree[self.size + i] = prices[i]
                self.ratings_tree[self.size + i] = ratings[i]
            
            for i in range(self.size - 1, 0, -1):
                self.rooms_tree[i] = max(self.rooms_tree[2 * i], self.rooms_tree[2 * i + 1])
                self.prices_tree[i] = min(self.prices_tree[2 * i], self.prices_tree[2 * i + 1])
                self.ratings_tree[i] = max(self.ratings_tree[2 * i], self.ratings_tree[2 * i + 1])
        
        def find_first_suitable(self, min_rooms, max_price, min_rating):
            return self._find_first_suitable(1, 0, self.size - 1, min_rooms, max_price, min_rating)
        
        def _find_first_suitable(self, node, left, right, min_rooms, max_price, min_rating):
            if left >= self.n:
                return -1
            
            if (self.rooms_tree[node] < min_rooms or 
                self.prices_tree[node] > max_price or 
                self.ratings_tree[node] < min_rating):
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            result = self._find_first_suitable(2 * node, left, mid, min_rooms, max_price, min_rating)
            if result != -1:
                return result
            
            # Check right child
            return self._find_first_suitable(2 * node + 1, mid + 1, right, min_rooms, max_price, min_rating)
    
    st = MultiCriteriaSegmentTree(hotels, criteria['prices'], criteria['ratings'])
    results = []
    
    for query in queries:
        min_rooms, max_price, min_rating = query
        pos = st.find_first_suitable(min_rooms, max_price, min_rating)
        if pos != -1:
            results.append(pos + 1)  # Convert to 1-indexed
        else:
            results.append(0)
    
    return results
```

#### **3. Hotel Queries with Persistence**
```python
def hotel_queries_persistent(n, q, hotels, operations):
    # Handle hotel queries with persistent data structures
    
    class PersistentSegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.versions = []
            self.build_initial(arr)
        
        def build_initial(self, arr):
            tree = [0] * (2 * self.size)
            for i in range(self.n):
                tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                tree[i] = max(tree[2 * i], tree[2 * i + 1])
            self.versions.append(tree)
        
        def update(self, version, pos, val):
            new_tree = self.versions[version].copy()
            pos += self.size
            new_tree[pos] = val
            pos //= 2
            while pos >= 1:
                new_tree[pos] = max(new_tree[2 * pos], new_tree[2 * pos + 1])
                pos //= 2
            self.versions.append(new_tree)
            return len(self.versions) - 1
        
        def find_first_ge(self, version, target):
            return self._find_first_ge(version, 1, 0, self.size - 1, target)
        
        def _find_first_ge(self, version, node, left, right, target):
            if left >= self.n:
                return -1
            
            if self.versions[version][node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            if self.versions[version][2 * node] >= target:
                result = self._find_first_ge(version, 2 * node, left, mid, target)
                if result != -1:
                    return result
            
            # Check right child
            return self._find_first_ge(version, 2 * node + 1, mid + 1, right, target)
    
    persistent_st = PersistentSegmentTree(hotels)
    current_version = 0
    results = []
    
    for op in operations:
        if op[0] == 'U':  # Update
            pos, val = op[1], op[2]
            current_version = persistent_st.update(current_version, pos - 1, val)
        else:  # Query
            version, x = op[1], op[2]
            pos = persistent_st.find_first_ge(version, x)
            if pos != -1:
                results.append(pos + 1)  # Convert to 1-indexed
            else:
                results.append(0)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Range Queries**: First greater/equal, range minimum queries
- **Data Structures**: Segment trees, binary indexed trees
- **Search Problems**: Binary search, first occurrence
- **Optimization**: Efficient query answering

## 📚 Learning Points

### Key Takeaways
- **Segment Tree** is optimal for range queries and updates
- **First greater/equal** is a common pattern in range queries
- **Data structure choice** depends on operation types and requirements
- **Logarithmic complexity** is achievable for range query problems

## Key Insights for Other Problems

### 1. **First Occurrence Queries**
**Principle**: Use tree-based data structures to find first occurrence efficiently.
**Applicable to**: Search problems, range queries, tree-based algorithms

### 2. **Segment Tree for Range Queries**
**Principle**: Use Segment Tree to answer range queries and find first occurrence in O(log n) time.
**Applicable to**: Range problems, search problems, tree-based data structures

### 3. **Binary Search on Tree**
**Principle**: Use binary search traversal on tree to find first occurrence.
**Applicable to**: Search problems, tree traversal, optimization problems

## Notable Techniques

### 1. **Segment Tree with First Occurrence**
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
    
    def find_first_ge(self, target):
        return self._find_first_ge(1, 0, self.size - 1, target)
    
    def _find_first_ge(self, node, left, right, target):
        if left >= self.n or self.tree[node] < target:
            return -1
        
        if left == right:
            return left if left < self.n else -1
        
        mid = (left + right) // 2
        
        # Check left child first
        if self.tree[2 * node] >= target:
            result = self._find_first_ge(2 * node, left, mid, target)
            if result != -1:
                return result
        
        # Check right child
        return self._find_first_ge(2 * node + 1, mid + 1, right, target)
```

### 2. **First Occurrence Pattern**
```python
def find_first_occurrence(segment_tree, target):
    return segment_tree.find_first_ge(target)
```

### 3. **Binary Search Traversal**
```python
def binary_search_tree(node, left, right, target):
    if left >= n or tree[node] < target:
        return -1
    
    if left == right:
        return left if left < n else -1
    
    mid = (left + right) // 2
    
    # Check left child first
    if tree[2 * node] >= target:
        result = binary_search_tree(2 * node, left, mid, target)
        if result != -1:
            return result
    
    # Check right child
    return binary_search_tree(2 * node + 1, mid + 1, right, target)
```

## Problem-Solving Framework

1. **Identify query type**: This is a first occurrence query problem
2. **Choose data structure**: Use Segment Tree for efficient range queries
3. **Build Segment Tree**: Create tree from hotel capacities
4. **Process queries**: Find first hotel with sufficient rooms using tree traversal
5. **Handle indexing**: Convert between 0-indexed and 1-indexed as needed

---

*This analysis shows how to efficiently find the first hotel with sufficient rooms using Segment Tree technique.*

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Hotel Queries with Updates**
**Problem**: Allow updates to hotel capacities while still answering queries efficiently.
```python
def hotel_queries_with_updates(n, q, hotels, operations):
    # Use Segment Tree with updates
    class DynamicSegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, pos, val):
            pos += self.size
            self.tree[pos] = val
            pos //= 2
            while pos >= 1:
                self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])
                pos //= 2
        
        def find_first_ge(self, target):
            return self._find_first_ge(1, 0, self.size - 1, target)
        
        def _find_first_ge(self, node, left, right, target):
            if left >= self.n:
                return -1
            
            if self.tree[node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            if self.tree[2 * node] >= target:
                result = self._find_first_ge(2 * node, left, mid, target)
                if result != -1:
                    return result
            
            # Check right child
            return self._find_first_ge(2 * node + 1, mid + 1, right, target)
    
    st = DynamicSegmentTree(hotels)
    results = []
    
    for op in operations:
        if op[0] == 'Q':  # Query
            x = op[1]
            pos = st.find_first_ge(x)
            results.append(pos + 1 if pos != -1 else 0)
        else:  # Update
            pos, val = op[1], op[2]
            st.update(pos - 1, val)  # Convert to 0-indexed
            hotels[pos - 1] = val
    
    return results
```

#### **Variation 2: Hotel Queries with Range Updates**
**Problem**: Support range updates (modify capacities of hotels in a range) and queries.
```python
def hotel_queries_range_updates(n, q, hotels, operations):
    # Use Segment Tree with lazy propagation
    class LazySegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            self.lazy = [0] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
        
        def push(self, node, left, right):
            if self.lazy[node] != 0:
                self.tree[node] += self.lazy[node]
                if left != right:
                    self.lazy[2 * node] += self.lazy[node]
                    self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[node] = 0
        
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
            self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])
        
        def find_first_ge(self, target):
            return self._find_first_ge(1, 0, self.size - 1, target)
        
        def _find_first_ge(self, node, left, right, target):
            self.push(node, left, right)
            if left >= self.n:
                return -1
            
            if self.tree[node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            self.push(2 * node, left, mid)
            if self.tree[2 * node] >= target:
                result = self._find_first_ge(2 * node, left, mid, target)
                if result != -1:
                    return result
            
            # Check right child
            return self._find_first_ge(2 * node + 1, mid + 1, right, target)
    
    st = LazySegmentTree(hotels)
    results = []
    
    for op in operations:
        if op[0] == 'Q':  # Query
            x = op[1]
            pos = st.find_first_ge(x)
            results.append(pos + 1 if pos != -1 else 0)
        else:  # Range Update
            l, r, val = op[1], op[2], op[3]
            st.range_update(1, 0, st.size - 1, l - 1, r - 1, val)
    
    return results
```

#### **Variation 3: Hotel Queries with Multiple Criteria**
**Problem**: Find the first hotel that satisfies multiple criteria (capacity, price, rating, etc.).
```python
def hotel_queries_multiple_criteria(n, q, hotels, prices, ratings, operations):
    # Use multiple Segment Trees for different criteria
    class MultiCriteriaSegmentTree:
        def __init__(self, capacities, prices, ratings):
            self.n = len(capacities)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            
            # Separate trees for each criterion
            self.capacity_tree = [0] * (2 * self.size)
            self.price_tree = [float('inf')] * (2 * self.size)
            self.rating_tree = [0] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.capacity_tree[self.size + i] = capacities[i]
                self.price_tree[self.size + i] = prices[i]
                self.rating_tree[self.size + i] = ratings[i]
            
            for i in range(self.size - 1, 0, -1):
                self.capacity_tree[i] = max(self.capacity_tree[2 * i], self.capacity_tree[2 * i + 1])
                self.price_tree[i] = min(self.price_tree[2 * i], self.price_tree[2 * i + 1])
                self.rating_tree[i] = max(self.rating_tree[2 * i], self.rating_tree[2 * i + 1])
        
        def find_first_suitable(self, min_capacity, max_price, min_rating):
            return self._find_first_suitable(1, 0, self.size - 1, min_capacity, max_price, min_rating)
        
        def _find_first_suitable(self, node, left, right, min_cap, max_price, min_rating):
            if left >= self.n:
                return -1
            
            # Check if current node can satisfy all criteria
            if (self.capacity_tree[node] < min_cap or 
                self.price_tree[node] > max_price or 
                self.rating_tree[node] < min_rating):
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            result = self._find_first_suitable(2 * node, left, mid, min_cap, max_price, min_rating)
            if result != -1:
                return result
            
            # Check right child
            return self._find_first_suitable(2 * node + 1, mid + 1, right, min_cap, max_price, min_rating)
    
    st = MultiCriteriaSegmentTree(hotels, prices, ratings)
    results = []
    
    for op in operations:
        min_capacity, max_price, min_rating = op[1], op[2], op[3]
        pos = st.find_first_suitable(min_capacity, max_price, min_rating)
        results.append(pos + 1 if pos != -1 else 0)
    
    return results
```

#### **Variation 4: Hotel Queries with Booking Simulation**
**Problem**: Simulate booking by reducing hotel capacity after assignment and handle cancellations.
```python
def hotel_queries_booking_simulation(n, q, hotels, operations):
    # Use Segment Tree with booking simulation
    class BookingSegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            self.original = arr.copy()
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
        
        def book_rooms(self, pos, rooms):
            # Reduce capacity after booking
            pos += self.size
            if self.tree[pos] >= rooms:
                self.tree[pos] -= rooms
                pos //= 2
                while pos >= 1:
                    self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])
                    pos //= 2
                return True
            return False
        
        def cancel_booking(self, pos, rooms):
            # Restore capacity after cancellation
            pos += self.size
            self.tree[pos] = min(self.tree[pos] + rooms, self.original[pos - self.size])
            pos //= 2
            while pos >= 1:
                self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])
                pos //= 2
        
        def find_first_ge(self, target):
            return self._find_first_ge(1, 0, self.size - 1, target)
        
        def _find_first_ge(self, node, left, right, target):
            if left >= self.n:
                return -1
            
            if self.tree[node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            if self.tree[2 * node] >= target:
                result = self._find_first_ge(2 * node, left, mid, target)
                if result != -1:
                    return result
            
            # Check right child
            return self._find_first_ge(2 * node + 1, mid + 1, right, target)
    
    st = BookingSegmentTree(hotels)
    results = []
    
    for op in operations:
        if op[0] == 'BOOK':
            x = op[1]  # Required rooms
            pos = st.find_first_ge(x)
            if pos != -1:
                if st.book_rooms(pos, x):
                    results.append(pos + 1)
                else:
                    results.append(0)
            else:
                results.append(0)
        elif op[0] == 'CANCEL':
            pos, rooms = op[1], op[2]
            st.cancel_booking(pos - 1, rooms)
            results.append("Cancelled")
    
    return results
```

#### **Variation 5: Hotel Queries with Optimal Assignment**
**Problem**: Find the optimal hotel assignment that minimizes total cost or maximizes satisfaction.
```python
def hotel_queries_optimal_assignment(n, q, hotels, costs, operations):
    # Use Segment Tree for optimal assignment
    class OptimalSegmentTree:
        def __init__(self, capacities, costs):
            self.n = len(capacities)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.capacity_tree = [0] * (2 * self.size)
            self.cost_tree = [float('inf')] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.capacity_tree[self.size + i] = capacities[i]
                self.cost_tree[self.size + i] = costs[i]
            
            for i in range(self.size - 1, 0, -1):
                self.capacity_tree[i] = max(self.capacity_tree[2 * i], self.capacity_tree[2 * i + 1])
                self.cost_tree[i] = min(self.cost_tree[2 * i], self.cost_tree[2 * i + 1])
        
        def find_optimal_hotel(self, required_rooms):
            # Find all hotels that can accommodate the group
            suitable_hotels = []
            self._find_suitable_hotels(1, 0, self.size - 1, required_rooms, suitable_hotels)
            
            if not suitable_hotels:
                return -1
            
            # Find the one with minimum cost
            min_cost = float('inf')
            best_hotel = -1
            for hotel in suitable_hotels: if costs[hotel] < 
min_cost: min_cost = costs[hotel]
                    best_hotel = hotel
            
            return best_hotel
        
        def _find_suitable_hotels(self, node, left, right, target, suitable):
            if left >= self.n:
                return
            
            if self.capacity_tree[node] < target:
                return
            
            if left == right: if left < self.n and self.capacity_tree[node] >= 
target: suitable.append(left)
                return
            
            mid = (left + right) // 2
            self._find_suitable_hotels(2 * node, left, mid, target, suitable)
            self._find_suitable_hotels(2 * node + 1, mid + 1, right, target, suitable)
    
    st = OptimalSegmentTree(hotels, costs)
    results = []
    
    for op in operations:
        required_rooms = op[1]
        optimal_hotel = st.find_optimal_hotel(required_rooms)
        if optimal_hotel != -1:
            results.append((optimal_hotel + 1, costs[optimal_hotel]))
        else:
            results.append((0, 0))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. First Occurrence Data Structures**
- **Segment Tree**: O(log n) first occurrence queries
- **Binary Indexed Tree**: Not suitable for first occurrence
- **Sparse Table**: O(1) queries but static
- **Binary Search Tree**: O(log n) dynamic queries

#### **2. Search Query Types**
- **First Occurrence**: Find first element >= target
- **Last Occurrence**: Find last element <= target
- **K-th Occurrence**: Find k-th occurrence of element
- **Range Occurrences**: Count occurrences in range

#### **3. Advanced Search Techniques**
- **Binary Search on Answer**: Find optimal value
- **Parallel Binary Search**: Handle multiple queries
- **Fractional Cascading**: Optimize multiple searches
- **Persistent Search**: Handle historical queries

#### **4. Optimization Problems**
- **Optimal Assignment**: Minimize cost or maximize satisfaction
- **Resource Allocation**: Efficiently allocate resources
- **Scheduling**: Optimal scheduling of tasks
- **Matching**: Optimal matching problems

#### **5. Competitive Programming Patterns**
- **Binary Search**: Find optimal solutions
- **Greedy**: Optimize local choices
- **Two Pointers**: Efficient range processing
- **Sliding Window**: Optimize consecutive queries

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    hotels = list(map(int, input().split()))
    
    st = SegmentTree(hotels)
    for _ in range(q):
        x = int(input())
        pos = st.find_first_ge(x)
        print(pos + 1 if pos != -1 else 0)
```

#### **2. Hotel Queries with Aggregation**
```python
def hotel_queries_aggregation(n, q, hotels, queries):
    # Support multiple aggregation functions
    class AggregationSegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            self.min_tree = [float('inf')] * (2 * self.size)
            self.max_tree = [-float('inf')] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
                self.min_tree[self.size + i] = arr[i]
                self.max_tree[self.size + i] = arr[i]
            
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
                self.min_tree[i] = min(self.min_tree[2 * i], self.min_tree[2 * i + 1])
                self.max_tree[i] = max(self.max_tree[2 * i], self.max_tree[2 * i + 1])
        
        def find_first_ge(self, target):
            return self._find_first_ge(1, 0, self.size - 1, target)
        
        def _find_first_ge(self, node, left, right, target):
            if left >= self.n:
                return -1
            
            if self.tree[node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            if self.tree[2 * node] >= target:
                result = self._find_first_ge(2 * node, left, mid, target)
                if result != -1:
                    return result
            
            return self._find_first_ge(2 * node + 1, mid + 1, right, target)
    
    st = AggregationSegmentTree(hotels)
    results = []
    
    for query in queries:
        x, op = query[1], query[2]
        if op == 'FIRST_GE':
            pos = st.find_first_ge(x)
            results.append(pos + 1 if pos != -1 else 0)
        elif op == 'COUNT_GE':
            # Count hotels with capacity >= x
            count = 0
            for i in range(n):
                if hotels[i] >= x:
                    count += 1
            results.append(count)
    
    return results
```

#### **3. Interactive Hotel Queries**
```python
def interactive_hotel_queries(n, hotels):
    # Handle interactive queries
    st = SegmentTree(hotels)
    
    while True: 
try: query = input().strip()
            if query == 'END':
                break
            
            x = int(query)
            pos = st.find_first_ge(x)
            if pos != -1:
                print(f"Hotel {pos + 1} can accommodate {x} people")
            else:
                print(f"No hotel can accommodate {x} people")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. First Occurrence Properties**
- **Monotonicity**: If a[i] >= x, then a[j] >= x for all j > i (in sorted arrays)
- **Binary Search**: Use binary search for first occurrence in sorted arrays
- **Tree Traversal**: Use tree traversal for first occurrence in trees
- **Optimality**: First occurrence is optimal for greedy strategies

#### **2. Optimization Techniques**
- **Early Termination**: Stop when first occurrence is found
- **Binary Search**: Find optimal first occurrence
- **Caching**: Store frequently accessed first occurrences
- **Compression**: Handle sparse first occurrences efficiently

#### **3. Advanced Mathematical Concepts**
- **Order Statistics**: Find k-th smallest element
- **Selection Algorithms**: Efficient selection of elements
- **Randomized Algorithms**: Probabilistic first occurrence finding
- **Approximation**: Approximate first occurrence for large datasets

#### **4. Algorithmic Improvements**
- **Block Decomposition**: Divide array into blocks
- **Lazy Propagation**: Efficient updates with lazy propagation
- **Compression**: Handle sparse arrays efficiently
- **Parallel Processing**: Use multiple cores for large datasets

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Segment Tree**: Efficient range queries and first occurrence
- **Binary Search**: Find first occurrence in sorted arrays
- **Binary Search Tree**: Dynamic first occurrence queries
- **Order Statistics**: Find k-th element efficiently

#### **2. Mathematical Concepts**
- **First Occurrence**: Understanding search properties
- **Binary Search**: Efficient search algorithms
- **Optimization**: Finding optimal solutions
- **Complexity Analysis**: Understanding time/space trade-offs

#### **3. Programming Concepts**
- **Data Structures**: Choosing appropriate search structures
- **Algorithm Design**: Optimizing for search constraints
- **Problem Decomposition**: Breaking complex search problems
- **Code Optimization**: Writing efficient search implementations

---

**Practice these variations to master first occurrence query techniques and search algorithms!** 🎯 