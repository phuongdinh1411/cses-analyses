# CSES Sum of Two Values - Problem Analysis

## Problem Statement
You are given an array of n integers, and your task is to find two values (at distinct positions) whose sum is x.

### Input
The first input line has two integers n and x: the array size and the target sum.

The second line has n integers a1,a2,…,an: the array values.

### Output
Print two integers: the positions of the values. If there are several solutions, you may print any of them. If there are no solutions, print "IMPOSSIBLE".

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ x,ai ≤ 10^9

### Example
```
Input:
4 8
2 7 5 1

Output:
2 4
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: Check all possible pairs of positions using nested loops.

```python
def two_sum_brute_force(arr, target):
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):  # j > i to avoid same position
            if arr[i] + arr[j] == target:
                return (i + 1, j + 1)  # Convert to 1-indexed
    
    return "IMPOSSIBLE"
```

**Why this is inefficient**: For each element, we check all remaining elements, leading to O(n²) time complexity. This is too slow for large arrays.

### Improvement 1: Sorting and Two Pointers - O(n log n)
**Description**: Sort the array and use two pointers to find the target sum, while tracking original positions.

```python
def two_sum_sorting(arr, target):
    # Create pairs of (value, original_position)
    pairs = [(arr[i], i + 1) for i in range(len(arr))]
    pairs.sort()  # Sort by value
    
    left, right = 0, len(pairs) - 1
    
    while left < right:
        current_sum = pairs[left][0] + pairs[right][0]
        
        if current_sum == target:
            return (pairs[left][1], pairs[right][1])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return "IMPOSSIBLE"
```

**Why this improvement works**: After sorting, we can use two pointers to efficiently find pairs that sum to the target. If the current sum is too small, we move the left pointer right. If it's too large, we move the right pointer left.

### Improvement 2: Hash Map - O(n)
**Description**: Use a hash map to store values and their positions, then check for complements in a single pass.

```python
def two_sum_optimal(arr, target):
    seen = {}  # value -> position
    
    for i in range(len(arr)):
        complement = target - arr[i]
        
        if complement in seen:
            return (seen[complement], i + 1)  # Convert to 1-indexed
        
        seen[arr[i]] = i + 1
    
    return "IMPOSSIBLE"
```

**Why this improvement works**: For each element, we calculate what complement we need to reach the target sum. We check if that complement exists in our hash map. If found, we return both positions. If not, we add the current element to the hash map. This gives us O(n) time complexity.

### Alternative: Binary Search Approach - O(n log n)
**Description**: For each element, binary search for its complement in the sorted array.

```python
import bisect

def two_sum_binary_search(arr, target):
    # Create pairs of (value, position) and sort
    pairs = [(arr[i], i + 1) for i in range(len(arr))]
    pairs.sort()
    values = [pair[0] for pair in pairs]
    
    for i, (val, pos) in enumerate(pairs):
        complement = target - val
        # Binary search for complement
        idx = bisect.bisect_left(values, complement)
        
        if idx < len(values) and values[idx] == complement:
            # Found complement, but check it's not the same element
            if idx != i:
                return (pos, pairs[idx][1])
    
    return "IMPOSSIBLE"
```

**Why this works**: Binary search reduces the search time for complements from O(n) to O(log n) per element.

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

# Hash map approach
seen = {}

for i in range(n):
    complement = x - arr[i]
    
    if complement in seen:
        print(seen[complement], i + 1)
        exit()
    
    seen[arr[i]] = i + 1

print("IMPOSSIBLE")
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all pairs |
| Sorting + Two Pointers | O(n log n) | O(n) | Sort and use two pointers |
| Hash Map | O(n) | O(n) | Store complements for lookup |
| Binary Search | O(n log n) | O(n) | Binary search for complements |

## Key Insights for Other Problems

### 1. **Hash Map for Pair Finding**
**Principle**: Use hash maps to store values and look up complements efficiently.
**Applicable to**:
- Finding pairs that sum to target
- Checking for duplicates
- Frequency counting
- Caching results

**Example Problems**:
- Three sum
- Four sum
- Subarray sum equals k
- Find all pairs with given sum

### 2. **Two Pointers on Sorted Arrays**
**Principle**: Sort array and use two pointers to find pairs efficiently.
**Applicable to**:
- Finding pairs in sorted arrays
- Merging sorted arrays
- Range-based problems
- Container problems

**Example Problems**:
- Container with most water
- Three sum
- Merge sorted arrays
- Remove duplicates from sorted array

### 3. **Complement Strategy**
**Principle**: Instead of finding a pair, find the complement of each element.
**Applicable to**:
- Sum-based problems
- Difference-based problems
- Product-based problems
- Any binary operation problems

**Example Problems**:
- Two sum
- Find pair with given difference
- Find pair with given product
- Find pair with given XOR

### 4. **Binary Search for Range Queries**
**Principle**: Use binary search to find elements within a range or with specific properties.
**Applicable to**:
- Finding elements in sorted arrays
- Range-based queries
- Optimization problems
- Search problems

**Example Problems**:
- Search in rotated array
- Find first/last occurrence
- Find peak element
- Capacity planning

## Notable Techniques

### 1. **Hash Map Pattern**
```python
# Common pattern for pair finding
seen = {}
for i, val in enumerate(arr):
    complement = target - val
    if complement in seen:
        return [seen[complement], i]
    seen[val] = i
```

### 2. **Two Pointers Pattern**
```python
# Common pattern for sorted arrays
left, right = 0, len(arr) - 1
while left < right:
    current_sum = arr[left] + arr[right]
    if current_sum == target:
        return [left, right]
    elif current_sum < target:
        left += 1
    else:
        right -= 1
```

### 3. **Binary Search Pattern**
```python
# Common pattern for finding elements
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## Edge Cases to Remember

1. **No solution exists**: Array doesn't contain any pair that sums to target
2. **Same element twice**: [3, 3] with target 6 should return (1, 2)
3. **Single element**: Array with one element can't have a pair
4. **Large numbers**: Hash map handles large integers efficiently
5. **Negative numbers**: Algorithm works with negative numbers
6. **Zero target**: Need to find two elements that sum to zero

## Problem-Solving Framework

1. **Identify the pair-finding nature**: This is a classic two sum problem
2. **Consider hash map approach**: Most efficient for unsorted arrays
3. **Consider sorting approach**: Good for multiple queries or when order matters
4. **Handle edge cases**: Same element, no solution, etc.
5. **Choose optimal approach**: Hash map for single query, sorting for multiple

---

*This analysis shows how to systematically improve from O(n²) to O(n) and extracts reusable insights for pair-finding problems.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Three Sum Problem**
**Problem**: Find three values whose sum equals target.
```python
def three_sum(arr, target):
    n = len(arr)
    arr.sort()
    
    for i in range(n - 2):
        left, right = i + 1, n - 1
        
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            
            if current_sum == target:
                return (i + 1, left + 1, right + 1)
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return "IMPOSSIBLE"
```

#### **Variation 2: K Sum Problem**
**Problem**: Find K values whose sum equals target.
```python
def k_sum(arr, target, k):
    n = len(arr)
    
    def backtrack(start, k_left, current_sum, current_indices):
        if k_left == 0:
            if current_sum == target:
                return current_indices
            return None
        
        for i in range(start, n):
            if current_sum + arr[i] <= target:
                result = backtrack(i + 1, k_left - 1, 
                                 current_sum + arr[i], 
                                 current_indices + [i + 1])
                if result:
                    return result
        
        return None
    
    return backtrack(0, k, 0, [])
```

#### **Variation 3: Closest Sum**
**Problem**: Find two values whose sum is closest to target.
```python
def closest_sum(arr, target):
    n = len(arr)
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()
    
    left, right = 0, n - 1
    closest_diff = float('inf')
    closest_pair = None
    
    while left < right:
        current_sum = pairs[left][0] + pairs[right][0]
        current_diff = abs(current_sum - target)
        
        if current_diff < closest_diff:
            closest_diff = current_diff
            closest_pair = (pairs[left][1], pairs[right][1])
        
        if current_sum < target:
            left += 1
        else:
            right -= 1
    
    return closest_pair
```

#### **Variation 4: Sum with Constraints**
**Problem**: Find two values with sum x, where values differ by at least d.
```python
def sum_with_difference_constraint(arr, target, min_diff):
    n = len(arr)
    pairs = [(arr[i], i + 1) for i in range(n)]
    pairs.sort()
    
    left, right = 0, n - 1
    
    while left < right:
        current_sum = pairs[left][0] + pairs[right][0]
        current_diff = abs(pairs[right][0] - pairs[left][0])
        
        if current_sum == target and current_diff >= min_diff:
            return (pairs[left][1], pairs[right][1])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return "IMPOSSIBLE"
```

#### **Variation 5: Multiple Solutions**
**Problem**: Find all pairs that sum to target.
```python
def all_pairs_sum(arr, target):
    seen = {}
    all_pairs = []
    
    for i in range(len(arr)):
        complement = target - arr[i]
        
        if complement in seen:
            for pos in seen[complement]:
                all_pairs.append((pos, i + 1))
        
        if arr[i] not in seen:
            seen[arr[i]] = []
        seen[arr[i]].append(i + 1)
    
    return all_pairs
```

### 🔗 **Related Problems & Concepts**

#### **1. Two Pointers Problems**
- **Two Sum**: Find pair with given sum
- **Three Sum**: Find triplet with given sum
- **Container With Most Water**: Find maximum area
- **Trapping Rain Water**: Calculate trapped water

#### **2. Hash Table Problems**
- **Hash Table Implementation**: Custom hash table design
- **Collision Resolution**: Handle hash collisions
- **Load Factor**: Optimize hash table performance
- **Hash Functions**: Design good hash functions

#### **3. Search Problems**
- **Binary Search**: Find element in sorted array
- **Linear Search**: Find element in unsorted array
- **Interpolation Search**: Search in uniformly distributed data
- **Exponential Search**: Search in unbounded arrays

#### **4. Array Manipulation Problems**
- **Array Sorting**: Sort array efficiently
- **Array Rotation**: Rotate array by k positions
- **Array Partitioning**: Partition array based on conditions
- **Array Merging**: Merge sorted arrays

#### **5. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Convex Optimization**: Optimize convex functions
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    seen = {}
    found = False
    
    for i in range(n):
        complement = x - arr[i]
        if complement in seen:
            print(seen[complement], i + 1)
            found = True
            break
        seen[arr[i]] = i + 1
    
    if not found:
        print("IMPOSSIBLE")
```

#### **2. Range Queries**
```python
# Precompute sum pairs for different ranges
def precompute_sum_pairs(arr):
    n = len(arr)
    sum_pairs = {}
    
    for i in range(n):
        for j in range(i + 1, n):
            pair_sum = arr[i] + arr[j]
            if pair_sum not in sum_pairs:
                sum_pairs[pair_sum] = []
            sum_pairs[pair_sum].append((i + 1, j + 1))
    
    return sum_pairs

# Answer queries about sum pairs
def sum_query(sum_pairs, target):
    return sum_pairs.get(target, [])
```

#### **3. Interactive Problems**
```python
# Interactive two sum game
def interactive_two_sum():
    n = int(input("Enter array size: "))
    arr = list(map(int, input("Enter array: ").split()))
    target = int(input("Enter target sum: "))
    
    print(f"Array: {arr}")
    print(f"Target: {target}")
    
    # Solve using hash map
    seen = {}
    found = False
    
    for i in range(n):
        complement = target - arr[i]
        print(f"Looking for complement {complement} for {arr[i]}")
        
        if complement in seen:
            print(f"Found! {arr[i]} + {complement} = {target}")
            print(f"Positions: {seen[complement]} and {i + 1}")
            found = True
            break
        
        seen[arr[i]] = i + 1
        print(f"Added {arr[i]} at position {i + 1}")
    
    if not found:
        print("No solution found")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Divisibility**: Properties of numbers
- **Prime Factorization**: Breaking numbers into primes
- **GCD/LCM**: Greatest common divisor and least common multiple
- **Modular Arithmetic**: Working with remainders

#### **2. Optimization Theory**
- **Linear Programming**: Formulate as LP problem
- **Convex Optimization**: Analyze convexity properties
- **Duality Theory**: Study dual problems
- **Sensitivity Analysis**: Analyze parameter changes

#### **3. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Amortized Analysis**: Average case analysis
- **Probabilistic Analysis**: Expected performance
- **Worst Case Analysis**: Upper bounds

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Two Pointers**: Efficient array processing
- **Hash Tables**: Efficient lookup data structures
- **Binary Search**: Search in sorted arrays
- **Sorting Algorithms**: Various sorting techniques

#### **2. Mathematical Concepts**
- **Number Theory**: Properties of integers
- **Optimization**: Mathematical optimization theory
- **Combinatorics**: Counting and arrangement
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Array Manipulation**: Efficient array operations
- **Search Techniques**: Various search algorithms
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies

---

*This analysis demonstrates efficient search techniques and shows various extensions for sum-based problems.* 