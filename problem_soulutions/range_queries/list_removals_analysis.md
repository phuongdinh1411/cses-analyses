---
layout: simple
title: "List Removals"
permalink: /cses-analyses/problem_soulutions/range_queries/list_removals_analysis
---


# List Removals

## Problem Statement
Given an array of n integers, process q queries. Each query asks for the k-th smallest element in the current array, and then removes that element from the array.

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x1,x2,…,xn: the contents of the array.
Finally, there are q lines describing the queries. Each line has one integer k: the position of the element to find and remove.

### Output
Print the answer to each query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9
- 1 ≤ k ≤ current array size

### Example
```
Input:
5 3
1 2 3 4 5
3
1
2

Output:
3
1
2
```

## Solution Progression

### Approach 1: Sort and Remove for Each Query - O(q × n log n)
**Description**: For each query, sort the current array, find the k-th element, remove it, and return the result.

```python
def list_removals_naive(n, q, arr, queries):
    results = []
    current_arr = arr.copy()
    
    for k in queries:
        # Sort the current array
        current_arr.sort()
        # Get the k-th element (1-indexed)
        element = current_arr[k-1]
        results.append(element)
        # Remove the element
        current_arr.pop(k-1)
    
    return results
```

**Why this is inefficient**: For each query, we need to sort the entire array, leading to O(q × n log n) time complexity.

### Improvement 1: Order Statistic Tree (PBDS) - O(n log n + q log n)
**Description**: Use an order statistic tree to efficiently find and remove the k-th smallest element.

```python
def list_removals_order_statistic_tree(n, q, arr, queries):
    from sortedcontainers import SortedList
    
    # Create a sorted list with elements and their indices
    elements = [(arr[i], i) for i in range(n)]
    sorted_list = SortedList(elements)
    
    results = []
    for k in queries:
        # Get the k-th smallest element (1-indexed)
        element, index = sorted_list[k-1]
        results.append(element)
        # Remove the element
        sorted_list.remove((element, index))
    
    return results
```

**Why this improvement works**: Order statistic tree allows us to find and remove the k-th smallest element in O(log n) time per operation.

## Final Optimal Solution

```python
n, q = map(int, input().split())
arr = list(map(int, input().split()))

from sortedcontainers import SortedList

# Create a sorted list with elements and their indices
elements = [(arr[i], i) for i in range(n)]
sorted_list = SortedList(elements)

# Process queries
for _ in range(q):
    k = int(input())
    # Get the k-th smallest element (1-indexed)
    element, index = sorted_list[k-1]
    print(element)
    # Remove the element
    sorted_list.remove((element, index))
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n log n) | O(n) | Sort and remove for each query |
| Order Statistic Tree | O(n log n + q log n) | O(n) | Use sorted data structure |

## Key Insights for Other Problems

### 1. **Dynamic Order Statistics**
**Principle**: Use data structures that support dynamic order statistics efficiently.
**Applicable to**: Dynamic problems, order statistics, tree-based data structures

### 2. **Sorted Data Structures**
**Principle**: Use sorted data structures to maintain order and support efficient operations.
**Applicable to**: Sorting problems, order problems, tree-based algorithms

### 3. **Element Removal and Order Maintenance**
**Principle**: Use data structures that can efficiently remove elements while maintaining order.
**Applicable to**: Dynamic problems, order maintenance, tree-based data structures

## Notable Techniques

### 1. **Order Statistic Tree Implementation**
```python
from sortedcontainers import SortedList

def order_statistic_tree(arr):
    elements = [(arr[i], i) for i in range(len(arr))]
    return SortedList(elements)

def find_and_remove_kth(sorted_list, k):
    element, index = sorted_list[k-1]  # 1-indexed
    sorted_list.remove((element, index))
    return element
```

### 2. **Dynamic Order Statistics Pattern**
```python
def dynamic_order_statistics(arr, queries):
    sorted_list = SortedList([(arr[i], i) for i in range(len(arr))])
    results = []
    
    for k in queries:
        element, index = sorted_list[k-1]
        results.append(element)
        sorted_list.remove((element, index))
    
    return results
```

### 3. **Element Removal Pattern**
```python
def remove_element(sorted_list, element, index):
    sorted_list.remove((element, index))
```

## Problem-Solving Framework

1. **Identify query type**: This is a dynamic order statistics problem with element removal
2. **Choose data structure**: Use order statistic tree for efficient operations
3. **Initialize data structure**: Create sorted list from array elements
4. **Process queries**: Find and remove k-th smallest element for each query
5. **Handle indexing**: Convert between 0-indexed and 1-indexed as needed

---

*This analysis shows how to efficiently handle dynamic order statistics with element removal using order statistic tree technique.*

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: List Removals with Insertions**
**Problem**: Support both removals and insertions while maintaining order statistics.
```python
def list_removals_with_insertions(n, q, arr, operations):
    from sortedcontainers import SortedList
    
    # Create a sorted list with elements and their indices
    elements = [(arr[i], i) for i in range(n)]
    sorted_list = SortedList(elements)
    next_index = n
    
    results = []
    for op in operations:
        if op[0] == 'REMOVE':  # Remove k-th element
            k = op[1]
            element, index = sorted_list[k-1]
            results.append(element)
            sorted_list.remove((element, index))
        else:  # Insert new element
            val = op[1]
            sorted_list.add((val, next_index))
            next_index += 1
    
    return results
```

#### **Variation 2: List Removals with Range Queries**
**Problem**: Support range queries (sum, min, max) in addition to removals.
```python
def list_removals_with_range_queries(n, q, arr, operations):
    from sortedcontainers import SortedList
    
    # Create a sorted list with elements and their indices
    elements = [(arr[i], i) for i in range(n)]
    sorted_list = SortedList(elements)
    
    # Build prefix sum for range queries
    def build_prefix_sum():
        prefix = [0] * (len(sorted_list) + 1)
        for i, (val, _) in enumerate(sorted_list):
            prefix[i + 1] = prefix[i] + val
        return prefix
    
    results = []
    for op in operations:
        if op[0] == 'REMOVE':  # Remove k-th element
            k = op[1]
            element, index = sorted_list[k-1]
            results.append(element)
            sorted_list.remove((element, index))
        else:  # Range query
            l, r, query_type = op[1], op[2], op[3]
            if query_type == 'SUM':
                # Calculate sum of elements from position l to r
                prefix = build_prefix_sum()
                result = prefix[r] - prefix[l-1]
            elif query_type == 'MIN':
                # Find minimum in range
                result = min(sorted_list[i][0] for i in range(l-1, r))
            elif query_type == 'MAX':
                # Find maximum in range
                result = max(sorted_list[i][0] for i in range(l-1, r))
            results.append(result)
    
    return results
```

#### **Variation 3: List Removals with Duplicates**
**Problem**: Handle arrays with duplicate elements and maintain stable ordering.
```python
def list_removals_with_duplicates(n, q, arr, operations):
    from sortedcontainers import SortedList
    
    # Create a sorted list with elements, indices, and occurrence count
    elements = []
    count = {}
    for i in range(n):
        val = arr[i]
        if val not in count:
            count[val] = 0
        count[val] += 1
        elements.append((val, i, count[val]))
    
    sorted_list = SortedList(elements)
    
    results = []
    for k in operations:
        # Get the k-th smallest element (1-indexed)
        element, index, occurrence = sorted_list[k-1]
        results.append(element)
        # Remove the element
        sorted_list.remove((element, index, occurrence))
    
    return results
```

#### **Variation 4: List Removals with Weighted Elements**
**Problem**: Each element has a weight, and queries ask for weighted k-th smallest element.
```python
def list_removals_weighted(n, q, arr, weights, operations):
    from sortedcontainers import SortedList
    
    # Create a sorted list with weighted elements
    elements = [(arr[i], weights[i], i) for i in range(n)]
    sorted_list = SortedList(elements)
    
    # Build weighted prefix sum
    def build_weighted_prefix():
        prefix = [0] * (len(sorted_list) + 1)
        for i, (val, weight, _) in enumerate(sorted_list):
            prefix[i + 1] = prefix[i] + weight
        return prefix
    
    results = []
    for op in operations:
        if op[0] == 'REMOVE_KTH':  # Remove k-th element
            k = op[1]
            element, weight, index = sorted_list[k-1]
            results.append(element)
            sorted_list.remove((element, weight, index))
        else:  # Find k-th weighted element
            k = op[1]
            prefix = build_weighted_prefix()
            # Find position where cumulative weight >= k
            for i in range(len(sorted_list)):
                if prefix[i + 1] >= k:
                    element, weight, index = sorted_list[i]
                    results.append(element)
                    break
            else:
                results.append(-1)  # Not found
    
    return results
```

#### **Variation 5: List Removals with Multiple Arrays**
**Problem**: Handle multiple arrays and support operations across them.
```python
def list_removals_multiple_arrays(n, m, q, arrays, operations):
    from sortedcontainers import SortedList
    
    # Create sorted lists for each array
    sorted_lists = []
    for arr in arrays:
        elements = [(arr[i], i) for i in range(n)]
        sorted_lists.append(SortedList(elements))
    
    results = []
    for op in operations:
        if op[0] == 'REMOVE':  # Remove k-th element from specific array
            array_idx, k = op[1], op[2]
            element, index = sorted_lists[array_idx][k-1]
            results.append(element)
            sorted_lists[array_idx].remove((element, index))
        else:  # Find k-th smallest across all arrays
            k = op[1]
            # Merge all sorted lists and find k-th element
            all_elements = []
            for i, sorted_list in enumerate(sorted_lists):
                for val, idx in sorted_list:
                    all_elements.append((val, i, idx))
            all_elements.sort()
            
            if k <= len(all_elements):
                element, array_idx, idx = all_elements[k-1]
                results.append(element)
                # Remove from the specific array
                sorted_lists[array_idx].remove((element, idx))
            else:
                results.append(-1)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Dynamic Order Statistics Data Structures**
- **Order Statistic Tree**: O(log n) find and remove k-th element
- **Binary Indexed Tree**: O(log n) operations with coordinate compression
- **Segment Tree**: O(log n) operations with lazy propagation
- **Treap**: Randomized balanced tree with order statistics

#### **2. Dynamic Operations**
- **Insertions**: Add new elements while maintaining order
- **Removals**: Remove elements while maintaining order
- **Updates**: Modify existing elements
- **Range Operations**: Query ranges of elements

#### **3. Advanced Order Statistics**
- **Weighted Order Statistics**: Elements have weights
- **Stable Ordering**: Maintain order for duplicate elements
- **Persistent Order Statistics**: Handle historical queries
- **Parallel Order Statistics**: Use multiple cores

#### **4. Optimization Problems**
- **Optimal Removal Order**: Find optimal sequence of removals
- **K-th Largest Element**: Find k-th largest instead of smallest
- **Range Order Statistics**: Find k-th element in range
- **Weighted Selection**: Select based on weights

#### **5. Competitive Programming Patterns**
- **Binary Search**: Find optimal k-th element
- **Two Pointers**: Efficient range processing
- **Sliding Window**: Optimize consecutive operations
- **Greedy**: Optimize removal order

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    
    from sortedcontainers import SortedList
    elements = [(arr[i], i) for i in range(n)]
    sorted_list = SortedList(elements)
    
    for _ in range(q):
        k = int(input())
        element, index = sorted_list[k-1]
        print(element)
        sorted_list.remove((element, index))
```

#### **2. List Removals with Aggregation**
```python
def list_removals_aggregation(n, q, arr, operations):
    from sortedcontainers import SortedList
    
    elements = [(arr[i], i) for i in range(n)]
    sorted_list = SortedList(elements)
    
    results = []
    for op in operations:
        if op[0] == 'REMOVE':
            k = op[1]
            element, index = sorted_list[k-1]
            results.append(element)
            sorted_list.remove((element, index))
        elif op[0] == 'COUNT_LESS':
            x = op[1]
            # Count elements less than x
            count = 0
            for val, idx in sorted_list: if val < 
x: count += 1
                else:
                    break
            results.append(count)
        elif op[0] == 'MEDIAN':
            # Find median of remaining elements
            n_remaining = len(sorted_list)
            if n_remaining % 2 == 1:
                median = sorted_list[n_remaining // 2][0]
            else:
                median = (sorted_list[n_remaining // 2 - 1][0] + 
                         sorted_list[n_remaining // 2][0]) / 2
            results.append(median)
    
    return results
```

#### **3. Interactive List Removals**
```python
def interactive_list_removals(n, arr):
    from sortedcontainers import SortedList
    
    elements = [(arr[i], i) for i in range(n)]
    sorted_list = SortedList(elements)
    
    while True: 
try: query = input().strip()
            if query == 'END':
                break
            
            if query.startswith('REMOVE'):
                k = int(query.split()[1])
                element, index = sorted_list[k-1]
                print(f"Removed {element} (k={k})")
                sorted_list.remove((element, index))
            elif query.startswith('FIND'):
                k = int(query.split()[1])
                if k <= len(sorted_list):
                    element, index = sorted_list[k-1]
                    print(f"K-th element: {element}")
                else:
                    print("Invalid k")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Order Statistics Properties**
- **Selection**: Finding k-th element is selection problem
- **Partitioning**: Use partitioning for efficient selection
- **Randomized Selection**: Probabilistic selection algorithms
- **Deterministic Selection**: Deterministic selection algorithms

#### **2. Optimization Techniques**
- **Early Termination**: Stop when k-th element is found
- **Binary Search**: Find optimal k-th element
- **Caching**: Store frequently accessed elements
- **Compression**: Handle sparse elements efficiently

#### **3. Advanced Mathematical Concepts**
- **Selection Algorithms**: Efficient selection techniques
- **Order Statistics**: Understanding order properties
- **Randomized Algorithms**: Probabilistic selection
- **Approximation**: Approximate selection for large datasets

#### **4. Algorithmic Improvements**
- **Block Decomposition**: Divide array into blocks
- **Lazy Propagation**: Efficient updates with lazy propagation
- **Compression**: Handle sparse arrays efficiently
- **Parallel Processing**: Use multiple cores for large datasets

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Order Statistic Tree**: Efficient dynamic order statistics
- **Selection Algorithms**: Find k-th element efficiently
- **Binary Search Tree**: Dynamic order statistics
- **Treap**: Randomized balanced tree

#### **2. Mathematical Concepts**
- **Order Statistics**: Understanding selection properties
- **Selection Algorithms**: Efficient selection techniques
- **Optimization**: Finding optimal selections
- **Complexity Analysis**: Understanding time/space trade-offs

#### **3. Programming Concepts**
- **Data Structures**: Choosing appropriate order statistics structures
- **Algorithm Design**: Optimizing for selection constraints
- **Problem Decomposition**: Breaking complex selection problems
- **Code Optimization**: Writing efficient selection implementations

---

**Practice these variations to master dynamic order statistics and selection algorithms!** 🎯 