# CSES List Removals - Problem Analysis

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