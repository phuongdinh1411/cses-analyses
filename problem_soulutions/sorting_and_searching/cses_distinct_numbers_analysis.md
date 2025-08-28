---
layout: simple
title: "Distinct Numbers
permalink: /problem_soulutions/sorting_and_searching/cses_distinct_numbers_analysis/"
---


# Distinct Numbers

## Problem Statement
You are given a list of n integers, and your task is to calculate the number of distinct values in the list.

### Input
The first input line has an integer n: the number of values.
The second line has n integers x1,x2,…,xn.

### Output
Print one integer: the number of distinct values.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9

### Example
```
Input:
5
2 3 2 2 3

Output:
2
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: For each element, check if it appears before in the array.

```python
def count_distinct_brute_force(arr):
    n = len(arr)
    distinct_count = 0
    
    for i in range(n):
        is_unique = True
        # Check if this element appears before
        for j in range(i):
            if arr[i] == arr[j]:
                is_unique = False
                break
        
        if is_unique:
            distinct_count += 1
    
    return distinct_count
```

**Why this is inefficient**: For each element, we scan all previous elements, leading to O(n²) time complexity.

### Improvement 1: Sorting - O(n log n)
**Description**: Sort the array first, then count distinct elements by checking when adjacent elements differ.

```python
def count_distinct_sorting(arr):
    if not arr:
        return 0
    
    arr.sort()  # O(n log n)
    distinct_count = 1  # First element is always distinct
    
    for i in range(1, len(arr)):
        if arr[i] != arr[i-1]:
            distinct_count += 1
    
    return distinct_count
```

**Why this improvement works**: After sorting, identical elements are grouped together, so we only need to check adjacent elements. This reduces the comparison complexity from O(n) per element to O(1) per element.

### Improvement 2: Hash Set - O(n)
**Description**: Use a hash set to automatically handle duplicates in a single pass.

```python
def count_distinct_optimal(arr):
    unique_elements = set(arr)
    return len(unique_elements)
```

**Why this improvement works**: Hash sets have O(1) average insertion and lookup time. By inserting all elements into a set, duplicates are automatically removed, and we get the count of unique elements directly.

### Alternative: Dictionary Approach - O(n)
**Description**: Use a dictionary to count frequencies, then count unique keys.

```python
def count_distinct_dict(arr):
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    
    return len(frequency)
```

**Why this works**: Similar to hash set, but also provides frequency information if needed.

## Final Optimal Solution

```python
n = int(input())
numbers = list(map(int, input().split()))

# Optimal solution using set
distinct_count = len(set(numbers))
print(distinct_count)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Compare each element with all previous |
| Sorting | O(n log n) | O(1) | Group identical elements together |
| Hash Set | O(n) | O(n) | Automatic duplicate removal |
| Dictionary | O(n) | O(n) | Frequency tracking capability |

## Key Insights for Other Problems

### 1. **Hash-Based Deduplication**
**Principle**: Use hash sets/dictionaries to automatically handle duplicates.
**Applicable to**: 
- Finding unique elements in arrays
- Removing duplicates from lists
- Counting distinct values
- Checking for duplicates in streams

**Example Problems**:
- Remove duplicates from sorted array
- Find first duplicate in array
- Count frequency of elements

### 2. **Sorting for Grouping**
**Principle**: Sort to group similar elements together, then process in single pass.
**Applicable to**:
- Finding duplicates
- Counting occurrences
- Grouping similar items
- Range-based problems

**Example Problems**:
- Find all duplicates in array
- Group anagrams
- Merge intervals

### 3. **Trade-off Between Time and Space**
**Principle**: Often you can trade space for time efficiency.
**Applicable to**:
- Caching results
- Precomputing values
- Using auxiliary data structures

**Example Problems**:
- Two sum problem
- Subarray sum problems
- Frequency counting

### 4. **Single Pass Optimization**
**Principle**: Process data in a single pass when possible to achieve O(n) time.
**Applicable to**:
- Counting problems
- Finding min/max with conditions
- Validation problems

**Example Problems**:
- Find missing number
- Find majority element
- Validate array properties

## Notable Techniques

### 1. **Hash Set Operations**
```python
# Common patterns
seen = set()
for item in data:
    if item in seen:  # O(1) lookup
        # Handle duplicate
    seen.add(item)    # O(1) insertion
```

### 2. **Sorting for Efficiency**
```python
# Sort first, then process
data.sort()
for i in range(1, len(data)):
    if data[i] != data[i-1]:
        # Process unique element
```

### 3. **Dictionary for Counting**
```python
# Count frequencies
count = {}
for item in data:
    count[item] = count.get(item, 0) + 1
```

## Edge Cases to Remember

1. **Empty input**: Return 0
2. **Single element**: Return 1
3. **All duplicates**: Return 1
4. **All unique**: Return n
5. **Large numbers**: Hash sets handle large integers efficiently

## Problem-Solving Framework

1. **Start with brute force**: Understand the problem completely"
2. **Identify bottlenecks**: What's causing the inefficiency?
3. **Look for patterns**: Can sorting or hashing help?
4. **Consider trade-offs**: Time vs space complexity
5. **Handle edge cases**: Empty, single element, duplicates

---

*This analysis shows how to systematically improve from O(n²) to O(n) and extracts reusable insights for similar problems.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Count Distinct Elements in Range**
**Problem**: Count distinct elements in subarray [l, r].
```python
def distinct_in_range(arr, l, r):
    # Using set for O(r-l+1) time
    unique_elements = set(arr[l:r+1])
    return len(unique_elements)
```

#### **Variation 2: Find Most Frequent Element**
**Problem**: Find the element that appears most frequently.
```python
def most_frequent_element(arr):
    frequency = {}
    max_freq = 0
    most_frequent = None
    
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
        if frequency[num] > max_freq:
            max_freq = frequency[num]
            most_frequent = num
    
    return most_frequent, max_freq
```

#### **Variation 3: Distinct Elements with Constraints**
**Problem**: Count distinct elements that satisfy a condition (e.g., even numbers only).
```python
def distinct_with_condition(arr, condition):
    unique_elements = set()
    for num in arr:
        if condition(num):
            unique_elements.add(num)
    return len(unique_elements)

# Example: Count distinct even numbers
distinct_even = lambda arr: distinct_with_condition(arr, lambda x: x % 2 == 0)
```

#### **Variation 4: K-th Most Frequent Element**
**Problem**: Find the k-th most frequent element.
```python
def kth_most_frequent(arr, k):
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    
    # Sort by frequency (descending) and then by value
    sorted_items = sorted(frequency.items(), 
                         key=lambda x: (-x[1], x[0]))
    
    return sorted_items[k-1][0] if k <= len(sorted_items) else None
```

#### **Variation 5: Distinct Elements in Multiple Arrays**
**Problem**: Count distinct elements that appear in all k arrays.
```python
def distinct_in_all_arrays(arrays):
    if not arrays:
        return 0
    
    # Start with first array
    common_elements = set(arrays[0])
    
    # Intersect with each subsequent array
    for arr in arrays[1:]:
        common_elements &= set(arr)
    
    return len(common_elements)
```

### 🔗 **Related Problems & Concepts**

#### **1. Sorting Problems**
- **Array Sorting**: Sort array in ascending/descending order
- **Custom Sorting**: Sort based on custom criteria
- **Stable Sorting**: Maintain relative order of equal elements
- **In-place Sorting**: Sort without extra space

#### **2. Search Problems**
- **Binary Search**: Find element in sorted array
- **Linear Search**: Find element in unsorted array
- **Interpolation Search**: Search in uniformly distributed data
- **Exponential Search**: Search in unbounded arrays

#### **3. Hash Table Problems**
- **Hash Table Implementation**: Custom hash table design
- **Collision Resolution**: Handle hash collisions
- **Load Factor**: Optimize hash table performance
- **Hash Functions**: Design good hash functions

#### **4. Frequency Analysis Problems**
- **Mode Finding**: Find most frequent element
- **Frequency Counting**: Count occurrences of each element
- **Top K Elements**: Find k most frequent elements
- **Rare Elements**: Find least frequent elements

#### **5. Set Operations Problems**
- **Set Union**: Combine elements from multiple sets
- **Set Intersection**: Find common elements
- **Set Difference**: Find elements in one set but not another
- **Set Symmetric Difference**: Find elements in exactly one set

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    
    distinct_count = len(set(arr))
    print(distinct_count)
```

#### **2. Range Queries with Updates**
```python
# Using segment tree for range distinct queries
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [set() for _ in range(4 * self.n)]
        self.build(arr, 0, 0, self.n - 1)
    
    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = {arr[start]}
        else:
            mid = (start + end) // 2
            self.build(arr, 2*node + 1, start, mid)
            self.build(arr, 2*node + 2, mid + 1, end)
            self.tree[node] = self.tree[2*node + 1] | self.tree[2*node + 2]
    
    def query(self, node, start, end, l, r):
        if r < start or l > end:
            return set()
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left = self.query(2*node + 1, start, mid, l, r)
        right = self.query(2*node + 2, mid + 1, end, l, r)
        return left | right

# Usage
def distinct_range_query(arr, l, r):
    st = SegmentTree(arr)
    return len(st.query(0, 0, len(arr)-1, l, r))
```

#### **3. Interactive Problems**
```python
# Interactive distinct element counter
def interactive_distinct_counter():
    print("Enter numbers one by one (enter 'done' to finish):")
    numbers = set()
    
    while True:
        user_input = input("Enter number: ")
        if user_input.lower() == 'done':
            break
        
        try:
            num = int(user_input)
            numbers.add(num)
            print(f"Current distinct count: {len(numbers)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'done'.")
    
    print(f"Final distinct count: {len(numbers)}")
    print(f"Distinct elements: {sorted(numbers)}")
```

### 🧮 **Mathematical Extensions**

#### **1. Probability and Statistics**
- **Expected Distinct Count**: Calculate expected distinct elements in random samples
- **Variance Analysis**: Analyze distribution of distinct counts
- **Sampling Theory**: Estimate distinct elements from samples
- **Confidence Intervals**: Estimate population distinct count

#### **2. Information Theory**
- **Entropy**: Calculate information content of element distribution
- **Compression**: Compress data based on frequency
- **Redundancy**: Measure duplicate information
- **Uniqueness**: Quantify how unique elements are

#### **3. Combinatorics**
- **Permutations**: Count arrangements of distinct elements
- **Combinations**: Count selections of distinct elements
- **Partitions**: Count ways to partition distinct elements
- **Derangements**: Count arrangements with no fixed points

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sorting Algorithms**: QuickSort, MergeSort, HeapSort, etc.
- **Search Algorithms**: Binary search, linear search, interpolation search
- **Hash Table Algorithms**: Separate chaining, open addressing
- **Set Data Structures**: HashSet, TreeSet implementations

#### **2. Mathematical Concepts**
- **Set Theory**: Union, intersection, difference operations
- **Combinatorics**: Counting principles and arrangements
- **Probability**: Random sampling and distributions
- **Information Theory**: Entropy and data compression

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Analysis**: Time and space complexity
- **Memory Management**: Optimizing space usage
- **Performance Optimization**: Trade-offs between time and space

---

*This analysis demonstrates efficient techniques for counting distinct elements and shows various extensions for sorting and searching problems.* 