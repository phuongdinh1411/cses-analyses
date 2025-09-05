---
layout: simple
title: "Distinct Numbers"
permalink: /problem_soulutions/sorting_and_searching/cses_distinct_numbers_analysis
---

# Distinct Numbers

## Problem Description

**Problem**: You are given a list of n integers. Calculate the number of distinct values in the list.

**Input**: 
- First line: n (number of values)
- Second line: n integers x₁, x₂, ..., xₙ

**Output**: Number of distinct values.

**Example**:
```
Input:
5
2 3 2 2 3

Output:
2

Explanation: The distinct values are 2 and 3.
```

## 📊 Visual Example

### Input Array
```
Array: [2, 3, 2, 2, 3]
Index:  0  1  2  3  4
```

### Distinct Values Identification
```
Step 1: Process element 2 (index 0)
┌─────────────────────────────────────┐
│ Seen: {2}                           │
│ Distinct count: 1                   │
└─────────────────────────────────────┘

Step 2: Process element 3 (index 1)
┌─────────────────────────────────────┐
│ Seen: {2, 3}                        │
│ Distinct count: 2                   │
└─────────────────────────────────────┘

Step 3: Process element 2 (index 2)
┌─────────────────────────────────────┐
│ Seen: {2, 3} (already seen)         │
│ Distinct count: 2 (unchanged)       │
└─────────────────────────────────────┘

Step 4: Process element 2 (index 3)
┌─────────────────────────────────────┐
│ Seen: {2, 3} (already seen)         │
│ Distinct count: 2 (unchanged)       │
└─────────────────────────────────────┘

Step 5: Process element 3 (index 4)
┌─────────────────────────────────────┐
│ Seen: {2, 3} (already seen)         │
│ Distinct count: 2 (unchanged)       │
└─────────────────────────────────────┘

Final Result: 2 distinct values
```

### Sorting Approach Visualization
```
Original: [2, 3, 2, 2, 3]
Sorted:   [2, 2, 2, 3, 3]

Count distinct by comparing adjacent:
- 2 ≠ 2? No, same value
- 2 ≠ 2? No, same value  
- 2 ≠ 3? Yes, new distinct value
- 3 ≠ 3? No, same value

Distinct values: 2, 3
Count: 2
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Count how many unique values are in the array
- Ignore duplicates
- Return the count of distinct elements

**Key Observations:**
- Need to identify unique elements
- Can use data structures to track seen elements
- Multiple approaches: sorting, hash set, dictionary
- Hash set is most efficient

### Step 2: Sorting Approach
**Idea**: Sort the array and count when adjacent elements differ.

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

**Why this works:**
- Sort groups identical elements together
- Check adjacent elements for differences
- Count transitions between different values
- Simple and intuitive approach

### Step 3: Hash Set Approach
**Idea**: Use a hash set to automatically handle duplicates.

```python
def count_distinct_hashset(arr):
    unique_elements = set(arr)
    return len(unique_elements)
```

**Why this is better:**
- Hash sets automatically remove duplicates
- O(1) average insertion time
- Single line solution
- Most efficient approach

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_distinct_numbers():
    n = int(input())
    arr = list(map(int, input().split()))
    
    # Use hash set for optimal solution
    unique_elements = set(arr)
    result = len(unique_elements)
    
    print(result)

# Main execution
if __name__ == "__main__":
    solve_distinct_numbers()
```

**Why this works:**
- Most efficient approach
- Handles all edge cases
- Simple and readable

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([2, 3, 2, 2, 3], 2),
        ([1, 2, 3, 4, 5], 5),
        ([1, 1, 1, 1], 1),
        ([], 0),
        ([1, 2, 1, 2, 1], 2),
    ]
    
    for arr, expected in test_cases:
        result = solve_test(arr)
        print(f"Array: {arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(arr):
    unique_elements = set(arr)
    return len(unique_elements)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(n) - hash set storage

### Why This Solution Works
- **Hash Set**: Automatically handles duplicates
- **Efficient**: O(1) average insertion time
- **Simple**: Clean and readable implementation

## 🎯 Key Insights

### 1. **Hash Set Properties**
- Automatically removes duplicates
- O(1) average insertion and lookup
- Perfect for counting unique elements
- Built-in length function

### 2. **Alternative Approaches**
- Sorting: O(n log n) time, O(1) space
- Dictionary: O(n) time, O(n) space
- Hash set: O(n) time, O(n) space (optimal)

### 3. **Data Structure Choice**
- Hash set is optimal for this problem
- Simple and efficient
- Handles all edge cases automatically

## 🎯 Problem Variations

### Variation 1: Count Frequencies
**Problem**: Count frequency of each distinct element.

```python
def count_frequencies(arr):
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    
    return frequency

def print_frequencies(arr):
    freq = count_frequencies(arr)
    for num, count in sorted(freq.items()):
        print(f"{num}: {count} times")
```

### Variation 2: Find Most Frequent Element
**Problem**: Find the element that appears most frequently.

```python
def most_frequent_element(arr):
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = 0
    most_frequent = None
    
    for num, freq in frequency.items():
        if freq > max_freq:
            max_freq = freq
            most_frequent = num
    
    return most_frequent, max_freq
```

### Variation 3: Elements Appearing K Times
**Problem**: Find elements that appear exactly k times.

```python
def elements_with_frequency_k(arr, k):
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    
    result = []
    for num, freq in frequency.items():
        if freq == k:
            result.append(num)
    
    return result
```

### Variation 4: Range Queries
**Problem**: Answer queries about distinct elements in ranges.

```python
def distinct_in_range(arr, queries):
    # queries[i] = (left, right) - find distinct elements in arr[left:right+1]
    results = []
    
    for left, right in queries:
        subarray = arr[left:right+1]
        distinct_count = len(set(subarray))
        results.append(distinct_count)
    
    return results
```

### Variation 5: Dynamic Updates
**Problem**: Support adding/removing elements dynamically.

```python
class DynamicDistinctCounter:
    def __init__(self):
        self.arr = []
        self.frequency = {}
        self.distinct_count = 0
    
    def add_element(self, num):
        self.arr.append(num)
        if num in self.frequency:
            self.frequency[num] += 1
        else:
            self.frequency[num] = 1
            self.distinct_count += 1
        return self.distinct_count
    
    def remove_element(self, num):
        if num in self.frequency:
            self.frequency[num] -= 1
            if self.frequency[num] == 0:
                del self.frequency[num]
                self.distinct_count -= 1
            self.arr.remove(num)
        return self.distinct_count
    
    def get_distinct_count(self):
        return self.distinct_count
```

## 🔗 Related Problems

- **[Distinct Values Subarrays](/cses-analyses/problem_soulutions/sorting_and_searching/distinct_values_subarrays_analysis)**: Subarray distinct counting
- **[Subarray Distinct Values](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_distinct_values_analysis)**: Range queries for distinct values
- **[Collecting Numbers](/cses-analyses/problem_soulutions/sorting_and_searching/cses_collecting_numbers_analysis)**: Array processing

## 📚 Learning Points

1. **Hash Sets**: Efficient data structure for unique elements
2. **Data Structure Choice**: Selecting appropriate structures for problems
3. **Frequency Counting**: Using dictionaries for counting
4. **Array Processing**: Efficient array manipulation techniques

---

**This is a great introduction to hash sets and frequency counting!** 🎯 