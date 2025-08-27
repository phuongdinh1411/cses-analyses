# CSES Distinct Numbers - Problem Analysis

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

1. **Start with brute force**: Understand the problem completely
2. **Identify bottlenecks**: What's causing the inefficiency?
3. **Look for patterns**: Can sorting or hashing help?
4. **Consider trade-offs**: Time vs space complexity
5. **Handle edge cases**: Empty, single element, duplicates

---

*This analysis shows how to systematically improve from O(n²) to O(n) and extracts reusable insights for similar problems.* 