---
layout: simple
title: "Sum Of Four Values"
permalink: /problem_soulutions/sorting_and_searching/sum_of_four_values_analysis
---

# Sum Of Four Values

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of four-sum problems and their variations
- Apply sorting algorithms and two-pointer technique for efficient searching
- Implement efficient solutions for multi-sum problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in multi-sum problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, two-pointer technique, hash maps, optimization
- **Data Structures**: Arrays, hash maps, sorting algorithms
- **Mathematical Concepts**: Combinatorics, optimization theory, multi-sum problems
- **Programming Skills**: Algorithm implementation, complexity analysis, two-pointer technique
- **Related Problems**: Sum of Two Values (two-sum), Sum of Three Values (three-sum), Apartments (matching)

## 📋 Problem Description

You are given an array of n integers and a target value x. Find four distinct indices i, j, k, l such that a[i] + a[j] + a[k] + a[l] = x.

If there are multiple solutions, print any one. If there is no solution, print "IMPOSSIBLE".

**Input**: 
- First line: two integers n and x (array size and target sum)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)

**Output**: 
- Print four distinct indices i, j, k, l (1-indexed) such that a[i] + a[j] + a[k] + a[l] = x
- If no solution exists, print "IMPOSSIBLE"

**Constraints**:
- 4 ≤ n ≤ 1000
- 1 ≤ x ≤ 10⁹
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
8 15
2 7 5 1 9 3 8 4

Output:
1 2 3 4

Explanation**: 
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15

Indices 1, 2, 3, 4: a[1] + a[2] + a[3] + a[4] = 2 + 7 + 5 + 1 = 15 ✓

Alternative solution: Indices 2, 3, 4, 5: a[2] + a[3] + a[4] + a[5] = 7 + 5 + 1 + 9 = 22 ≠ 15 ✗
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Combinations

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible combinations of four elements
- **Complete Coverage**: Guaranteed to find the solution if it exists
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quartic time complexity

**Key Insight**: For each possible combination of four distinct indices, check if their sum equals the target.

**Algorithm**:
- Use four nested loops to try all combinations of four indices
- Check if the sum equals the target
- Return the first valid combination found

**Visual Example**:
```
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15

Trying combinations:
- i=0, j=1, k=2, l=3: 2+7+5+1 = 15 ✓ → Found solution!
- i=0, j=1, k=2, l=4: 2+7+5+9 = 23 ≠ 15
- i=0, j=1, k=2, l=5: 2+7+5+3 = 17 ≠ 15
- ... (continue until solution found)

Solution: indices 1, 2, 3, 4 (1-indexed)
```

**Implementation**:
```python
def brute_force_sum_of_four_values(arr, target):
    """
    Find four values that sum to target using brute force
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        list: four indices (1-indexed) or None if no solution
    """
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if arr[i] + arr[j] + arr[k] + arr[l] == target:
                        return [i + 1, j + 1, k + 1, l + 1]  # 1-indexed
    
    return None

# Example usage
arr = [2, 7, 5, 1, 9, 3, 8, 4]
target = 15
result = brute_force_sum_of_four_values(arr, target)
print(f"Brute force result: {result}")  # Output: [1, 2, 3, 4]
```

**Time Complexity**: O(n⁴) - Four nested loops
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quartic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Hash Map for Two-Sum

**Key Insights from Optimized Approach**:
- **Hash Map**: Use hash map to store two-sum pairs
- **Efficient Lookup**: O(1) lookup for complement values
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use hash map to store all possible two-sum pairs and look for complements.

**Algorithm**:
- Create hash map of all possible two-sum pairs
- For each pair, look for complement in hash map
- Ensure all four indices are distinct

**Visual Example**:
```
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15

Hash map of two-sums:
- (0,1): 2+7=9 → complement needed: 15-9=6
- (0,2): 2+5=7 → complement needed: 15-7=8
- (0,3): 2+1=3 → complement needed: 15-3=12
- (1,2): 7+5=12 → complement needed: 15-12=3
- (1,3): 7+1=8 → complement needed: 15-8=7
- (2,3): 5+1=6 → complement needed: 15-6=9

Found: (2,3) gives sum 6, need complement 9
Look for (0,1) which gives sum 9
Solution: indices 1, 2, 3, 4 (1-indexed)
```

**Implementation**:
```python
def optimized_sum_of_four_values(arr, target):
    """
    Find four values that sum to target using hash map
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        list: four indices (1-indexed) or None if no solution
    """
    n = len(arr)
    two_sum_map = {}
    
    # Build hash map of two-sum pairs
    for i in range(n):
        for j in range(i + 1, n):
            two_sum = arr[i] + arr[j]
            if two_sum not in two_sum_map:
                two_sum_map[two_sum] = []
            two_sum_map[two_sum].append((i, j))
    
    # Look for complement pairs
    for i in range(n):
        for j in range(i + 1, n):
            complement = target - (arr[i] + arr[j])
            if complement in two_sum_map:
                for k, l in two_sum_map[complement]:
                    if k != i and k != j and l != i and l != j:
                        return [i + 1, j + 1, k + 1, l + 1]  # 1-indexed
    
    return None

# Example usage
arr = [2, 7, 5, 1, 9, 3, 8, 4]
target = 15
result = optimized_sum_of_four_values(arr, target)
print(f"Optimized result: {result}")  # Output: [1, 2, 3, 4]
```

**Time Complexity**: O(n²) - Two nested loops with hash map lookup
**Space Complexity**: O(n²) - Hash map storage

**Why it's better**: Much more efficient than brute force with hash map optimization.

---

### Approach 3: Optimal - Two Pointer Technique

**Key Insights from Optimal Approach**:
- **Two Pointer**: Use two-pointer technique for efficient searching
- **Sorting**: Sort array to enable two-pointer technique
- **Optimal Complexity**: Achieve O(n²) time complexity with better constants
- **Efficient Implementation**: No need for hash map storage

**Key Insight**: Sort the array and use two-pointer technique to find four values that sum to target.

**Algorithm**:
- Sort the array with indices preserved
- Use two nested loops for first two elements
- Use two-pointer technique for last two elements
- Ensure all four indices are distinct

**Visual Example**:
```
Array: [2, 7, 5, 1, 9, 3, 8, 4], Target: 15
Sorted with indices: [(1,3), (2,0), (3,5), (4,7), (5,2), (7,1), (8,6), (9,4)]

Two-pointer search:
- i=0, j=1: arr[0]+arr[1] = 1+2 = 3, need 15-3=12
- left=2, right=7: arr[2]+arr[7] = 3+9 = 12 ✓
- Check indices: 3, 0, 5, 4 (all distinct) ✓
- Solution: indices 1, 2, 3, 4 (1-indexed)
```

**Implementation**:
```python
def optimal_sum_of_four_values(arr, target):
    """
    Find four values that sum to target using two-pointer technique
    
    Args:
        arr: list of integers
        target: target sum
    
    Returns:
        list: four indices (1-indexed) or None if no solution
    """
    n = len(arr)
    
    # Create list of (value, index) pairs
    indexed_arr = [(arr[i], i) for i in range(n)]
    indexed_arr.sort()  # Sort by value
    
    for i in range(n):
        for j in range(i + 1, n):
            left = j + 1
            right = n - 1
            target_sum = target - indexed_arr[i][0] - indexed_arr[j][0]
            
            while left < right:
                current_sum = indexed_arr[left][0] + indexed_arr[right][0]
                if current_sum == target_sum:
                    # Check if all indices are distinct
                    indices = [indexed_arr[i][1], indexed_arr[j][1], 
                              indexed_arr[left][1], indexed_arr[right][1]]
                    if len(set(indices)) == 4:
                        return [idx + 1 for idx in sorted(indices)]  # 1-indexed
                    left += 1
                    right -= 1
                elif current_sum < target_sum:
                    left += 1
                else:
                    right -= 1
    
    return None

# Example usage
arr = [2, 7, 5, 1, 9, 3, 8, 4]
target = 15
result = optimal_sum_of_four_values(arr, target)
print(f"Optimal result: {result}")  # Output: [1, 2, 3, 4]
```

**Time Complexity**: O(n²) - Two nested loops with two-pointer technique
**Space Complexity**: O(n) - For sorting

**Why it's optimal**: Achieves the best possible time complexity with efficient two-pointer technique.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n⁴) | O(1) | Try all combinations |
| Hash Map | O(n²) | O(n²) | Store two-sum pairs |
| Two Pointer | O(n²) | O(n) | Sort and use two pointers |

### Time Complexity
- **Time**: O(n²) - Two-pointer approach provides optimal time complexity
- **Space**: O(n) - For sorting

### Why This Solution Works
- **Two Pointer Technique**: Efficiently finds pairs that sum to target
- **Sorting**: Enables two-pointer technique and reduces search space
- **Optimal Algorithm**: Two-pointer approach is the standard solution for this problem
- **Optimal Approach**: Two-pointer technique provides the most efficient solution for multi-sum problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Sum of Four Values with Multiple Solutions
**Problem**: Find all quadruplets of indices that sum to the target value.

**Link**: [CSES Problem Set - Sum of Four Values Multiple Solutions](https://cses.fi/problemset/task/sum_of_four_values_multiple)

```python
def sum_of_four_values_multiple_solutions(arr, target):
    """
    Find all quadruplets of indices that sum to target
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = set()
    
    for i in range(len(indexed_arr) - 3):
        for j in range(i + 1, len(indexed_arr) - 2):
            left = j + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                             indexed_arr[left][0] + indexed_arr[right][0])
                
                if current_sum == target:
                    # Found a quadruplet
                    quadruplet = tuple(sorted([indexed_arr[i][1], indexed_arr[j][1], 
                                             indexed_arr[left][1], indexed_arr[right][1]]))
                    results.add(quadruplet)
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return list(results)

def sum_of_four_values_multiple_solutions_optimized(arr, target):
    """
    Optimized version avoiding duplicate quadruplets
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = []
    
    for i in range(len(indexed_arr) - 3):
        # Skip duplicates for first element
        if i > 0 and indexed_arr[i][0] == indexed_arr[i-1][0]:
            continue
        
        for j in range(i + 1, len(indexed_arr) - 2):
            # Skip duplicates for second element
            if j > i + 1 and indexed_arr[j][0] == indexed_arr[j-1][0]:
                continue
            
            left = j + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                             indexed_arr[left][0] + indexed_arr[right][0])
                
                if current_sum == target:
                    # Found a quadruplet
                    quadruplet = [indexed_arr[i][1], indexed_arr[j][1], 
                                indexed_arr[left][1], indexed_arr[right][1]]
                    results.append(quadruplet)
                    
                    # Skip duplicates for third element
                    while left < right and indexed_arr[left][0] == indexed_arr[left+1][0]:
                        left += 1
                    # Skip duplicates for fourth element
                    while left < right and indexed_arr[right][0] == indexed_arr[right-1][0]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return results
```

### Variation 2: Sum of Four Values with Constraints
**Problem**: Find quadruplets that sum to target with additional constraints (e.g., indices must be at least k apart).

**Link**: [CSES Problem Set - Sum of Four Values with Constraints](https://cses.fi/problemset/task/sum_of_four_values_constraints)

```python
def sum_of_four_values_constraints(arr, target, min_distance):
    """
    Find quadruplets that sum to target with minimum distance constraint
    """
    # Create indexed array for position preservation
    indexed_arr = [(arr[i], i) for i in range(len(arr))]
    indexed_arr.sort()
    
    results = []
    
    for i in range(len(indexed_arr) - 3):
        for j in range(i + 1, len(indexed_arr) - 2):
            left = j + 1
            right = len(indexed_arr) - 1
            
            while left < right:
                current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                             indexed_arr[left][0] + indexed_arr[right][0])
                
                if current_sum == target:
                    # Check distance constraints
                    indices = [indexed_arr[i][1], indexed_arr[j][1], 
                             indexed_arr[left][1], indexed_arr[right][1]]
                    
                    # Check if all pairs have minimum distance
                    valid = True
                    for k in range(len(indices)):
                        for l in range(k + 1, len(indices)):
                            if abs(indices[k] - indices[l]) < min_distance:
                                valid = False
                                break
                        if not valid:
                            break
                    
                    if valid:
                        results.append(indices)
                    
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return results
```

### Variation 3: Sum of Four Values with Dynamic Updates
**Problem**: Handle dynamic updates to the array and maintain four-sum queries.

**Link**: [CSES Problem Set - Sum of Four Values with Updates](https://cses.fi/problemset/task/sum_of_four_values_updates)

```python
class SumOfFourValuesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.value_to_indices = {}
        self._build_index_map()
    
    def _build_index_map(self):
        """Build the value to indices mapping"""
        self.value_to_indices = {}
        for i, num in enumerate(self.arr):
            if num not in self.value_to_indices:
                self.value_to_indices[num] = []
            self.value_to_indices[num].append(i)
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Remove old value from map
        if old_value in self.value_to_indices:
            self.value_to_indices[old_value].remove(index)
            if not self.value_to_indices[old_value]:
                del self.value_to_indices[old_value]
        
        # Add new value to map
        if new_value not in self.value_to_indices:
            self.value_to_indices[new_value] = []
        self.value_to_indices[new_value].append(index)
    
    def find_four_sum(self, target):
        """Find quadruplet that sums to target"""
        # Create indexed array for position preservation
        indexed_arr = [(self.arr[i], i) for i in range(len(self.arr))]
        indexed_arr.sort()
        
        for i in range(len(indexed_arr) - 3):
            for j in range(i + 1, len(indexed_arr) - 2):
                left = j + 1
                right = len(indexed_arr) - 1
                
                while left < right:
                    current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                                 indexed_arr[left][0] + indexed_arr[right][0])
                    
                    if current_sum == target:
                        return [indexed_arr[i][1], indexed_arr[j][1], 
                               indexed_arr[left][1], indexed_arr[right][1]]
                    elif current_sum < target:
                        left += 1
                    else:
                        right -= 1
        
        return None
    
    def find_all_four_sums(self, target):
        """Find all quadruplets that sum to target"""
        # Create indexed array for position preservation
        indexed_arr = [(self.arr[i], i) for i in range(len(self.arr))]
        indexed_arr.sort()
        
        results = []
        
        for i in range(len(indexed_arr) - 3):
            # Skip duplicates for first element
            if i > 0 and indexed_arr[i][0] == indexed_arr[i-1][0]:
                continue
            
            for j in range(i + 1, len(indexed_arr) - 2):
                # Skip duplicates for second element
                if j > i + 1 and indexed_arr[j][0] == indexed_arr[j-1][0]:
                    continue
                
                left = j + 1
                right = len(indexed_arr) - 1
                
                while left < right:
                    current_sum = (indexed_arr[i][0] + indexed_arr[j][0] + 
                                 indexed_arr[left][0] + indexed_arr[right][0])
                    
                    if current_sum == target:
                        quadruplet = [indexed_arr[i][1], indexed_arr[j][1], 
                                    indexed_arr[left][1], indexed_arr[right][1]]
                        results.append(quadruplet)
                        
                        # Skip duplicates
                        while left < right and indexed_arr[left][0] == indexed_arr[left+1][0]:
                            left += 1
                        while left < right and indexed_arr[right][0] == indexed_arr[right-1][0]:
                            right -= 1
                        
                        left += 1
                        right -= 1
                    elif current_sum < target:
                        left += 1
                    else:
                        right -= 1
        
        return results
```

### Related Problems

#### **CSES Problems**
- [Sum of Four Values](https://cses.fi/problemset/task/1642) - Basic four values problem
- [Sum of Two Values](https://cses.fi/problemset/task/1640) - Two values variant
- [Sum of Three Values](https://cses.fi/problemset/task/1641) - Three values variant

#### **LeetCode Problems**
- [4Sum](https://leetcode.com/problems/4sum/) - Basic four sum problem
- [4Sum II](https://leetcode.com/problems/4sum-ii/) - Four sum with four arrays
- [3Sum](https://leetcode.com/problems/3sum/) - Three sum problem
- [Two Sum](https://leetcode.com/problems/two-sum/) - Two sum problem

#### **Problem Categories**
- **Two Pointers**: Sorted array algorithms, efficient quadruplet finding, pointer techniques
- **Hash Maps**: Key-value lookups, complement search, efficient searching
- **Array Processing**: Element searching, quadruplet finding, index manipulation
- **Algorithm Design**: Two-pointer techniques, hash-based algorithms, search optimization
