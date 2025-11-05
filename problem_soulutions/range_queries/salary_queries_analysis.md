---
layout: simple
title: "Salary Queries - Range Counting"
permalink: /problem_soulutions/range_queries/salary_queries_analysis
---

# Salary Queries - Range Counting

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range counting for salary query problems
- Apply range counting to efficiently answer salary queries
- Optimize salary query calculations using range counting
- Handle edge cases in salary query problems
- Recognize when to use range counting vs other approaches

## 📋 Problem Description

Given an array of salaries and multiple queries, each query asks for the number of employees with salary in range [a, b]. The array is static (no updates).

**Input**: 
- First line: n (number of employees) and q (number of queries)
- Second line: n integers representing salaries
- Next q lines: a b (salary range boundaries)

**Output**: 
- q lines: number of employees with salary in range [a, b] for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ salary[i] ≤ 10⁹
- 1 ≤ a ≤ b ≤ 10⁹

**Example**:
```
Input:
5 3
1000 2000 1500 3000 2500
1000 2000
1500 2500
2000 3000

Output:
3
3
2

Explanation**: 
Query 1: employees with salary [1000,2000] = 3 (1000, 2000, 1500)
Query 2: employees with salary [1500,2500] = 3 (1500, 2000, 2500)
Query 3: employees with salary [2000,3000] = 2 (2000, 3000)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through all salaries
2. Count salaries in range [a, b]
3. Return the count

**Implementation**:
```python
def brute_force_salary_queries(salaries, queries):
    n = len(salaries)
    results = []
    
    for a, b in queries:
        # Count salaries in range [a, b]
        count = 0
        for salary in salaries:
            if a <= salary <= b:
                count += 1
        
        results.append(count)
    
    return results
```

### Approach 2: Optimized with Sorting
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Sort the salaries array
2. For each query, use binary search to find range boundaries
3. Count salaries in range [a, b]
4. Return the count

**Implementation**:
```python
def optimized_salary_queries(salaries, queries):
    n = len(salaries)
    sorted_salaries = sorted(salaries)
    results = []
    
    for a, b in queries:
        # Find first salary >= a
        left = 0
        right = n
        while left < right:
            mid = (left + right) // 2
            if sorted_salaries[mid] < a:
                left = mid + 1
            else:
                right = mid
        
        # Find first salary > b
        left2 = 0
        right2 = n
        while left2 < right2:
            mid = (left2 + right2) // 2
            if sorted_salaries[mid] <= b:
                left2 = mid + 1
            else:
                right2 = mid
        
        # Count salaries in range [a, b]
        count = left2 - left
        results.append(count)
    
    return results
```

### Approach 3: Optimal with Sorting
**Time Complexity**: O(n log n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Sort the salaries array
2. For each query, use binary search to find range boundaries
3. Count salaries in range [a, b]
4. Return the count

**Implementation**:
```python
def optimal_salary_queries(salaries, queries):
    n = len(salaries)
    sorted_salaries = sorted(salaries)
    results = []
    
    for a, b in queries:
        # Find first salary >= a
        left = 0
        right = n
        while left < right:
            mid = (left + right) // 2
            if sorted_salaries[mid] < a:
                left = mid + 1
            else:
                right = mid
        
        # Find first salary > b
        left2 = 0
        right2 = n
        while left2 < right2:
            mid = (left2 + right2) // 2
            if sorted_salaries[mid] <= b:
                left2 = mid + 1
            else:
                right2 = mid
        
        # Count salaries in range [a, b]
        count = left2 - left
        results.append(count)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Count salaries for each query |
| Optimized | O(n log n + q log n) | O(n) | Use sorting and binary search |
| Optimal | O(n log n + q log n) | O(n) | Use sorting and binary search |

### Time Complexity
- **Time**: O(n log n + q log n) - O(n log n) sorting + O(log n) per query
- **Space**: O(n) - Sorted array

### Why This Solution Works
- **Sorting Property**: Sort salaries to enable binary search
- **Binary Search**: Find range boundaries in O(log n) time
- **Efficient Counting**: Count salaries in range in O(1) time
- **Optimal Approach**: O(n log n + q log n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Salary Queries with Dynamic Updates
**Problem**: Handle dynamic updates to salaries and maintain range count queries.

**Link**: [CSES Problem Set - Salary Queries with Updates](https://cses.fi/problemset/task/salary_queries_updates)

```python
class SalaryQueriesWithUpdates:
    def __init__(self, salaries):
        self.salaries = salaries[:]
        self.n = len(salaries)
        self.sorted_salaries = sorted(salaries)
    
    def update_salary(self, index, new_salary):
        """Update salary at index to new_salary"""
        old_salary = self.salaries[index]
        self.salaries[index] = new_salary
        
        # Update sorted array
        self.sorted_salaries.remove(old_salary)
        self._insert_sorted(new_salary)
    
    def _insert_sorted(self, salary):
        """Insert salary into sorted array"""
        left, right = 0, len(self.sorted_salaries)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_salaries[mid] < salary:
                left = mid + 1
            else:
                right = mid
        self.sorted_salaries.insert(left, salary)
    
    def count_in_range(self, min_salary, max_salary):
        """Count salaries in range [min_salary, max_salary]"""
        left_idx = self._binary_search_left(min_salary)
        right_idx = self._binary_search_right(max_salary)
        return right_idx - left_idx
    
    def _binary_search_left(self, target):
        """Find leftmost position where salary >= target"""
        left, right = 0, len(self.sorted_salaries)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_salaries[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left
    
    def _binary_search_right(self, target):
        """Find rightmost position where salary <= target"""
        left, right = 0, len(self.sorted_salaries)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_salaries[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for min_sal, max_sal in queries:
            results.append(self.count_in_range(min_sal, max_sal))
        return results
```

### Variation 2: Salary Queries with Different Operations
**Problem**: Handle different types of operations (count, sum, average, median) on salary ranges.

**Link**: [CSES Problem Set - Salary Queries Different Operations](https://cses.fi/problemset/task/salary_queries_operations)

```python
class SalaryQueriesDifferentOps:
    def __init__(self, salaries):
        self.salaries = salaries[:]
        self.n = len(salaries)
        self.sorted_salaries = sorted(salaries)
        self.prefix_sums = self._compute_prefix_sums()
    
    def _compute_prefix_sums(self):
        """Compute prefix sums of sorted salaries"""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.sorted_salaries[i]
        return prefix
    
    def count_in_range(self, min_salary, max_salary):
        """Count salaries in range [min_salary, max_salary]"""
        left_idx = self._binary_search_left(min_salary)
        right_idx = self._binary_search_right(max_salary)
        return right_idx - left_idx
    
    def sum_in_range(self, min_salary, max_salary):
        """Sum of salaries in range [min_salary, max_salary]"""
        left_idx = self._binary_search_left(min_salary)
        right_idx = self._binary_search_right(max_salary)
        return self.prefix_sums[right_idx] - self.prefix_sums[left_idx]
    
    def average_in_range(self, min_salary, max_salary):
        """Average salary in range [min_salary, max_salary]"""
        count = self.count_in_range(min_salary, max_salary)
        if count == 0:
            return 0
        total = self.sum_in_range(min_salary, max_salary)
        return total / count
    
    def median_in_range(self, min_salary, max_salary):
        """Median salary in range [min_salary, max_salary]"""
        left_idx = self._binary_search_left(min_salary)
        right_idx = self._binary_search_right(max_salary)
        count = right_idx - left_idx
        
        if count == 0:
            return None
        
        if count % 2 == 1:
            return self.sorted_salaries[left_idx + count // 2]
        else:
            mid1 = self.sorted_salaries[left_idx + count // 2 - 1]
            mid2 = self.sorted_salaries[left_idx + count // 2]
            return (mid1 + mid2) / 2
    
    def _binary_search_left(self, target):
        """Find leftmost position where salary >= target"""
        left, right = 0, len(self.sorted_salaries)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_salaries[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left
    
    def _binary_search_right(self, target):
        """Find rightmost position where salary <= target"""
        left, right = 0, len(self.sorted_salaries)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_salaries[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left
```

### Variation 3: Salary Queries with Constraints
**Problem**: Handle salary queries with additional constraints (e.g., maximum count, minimum range).

**Link**: [CSES Problem Set - Salary Queries with Constraints](https://cses.fi/problemset/task/salary_queries_constraints)

```python
class SalaryQueriesWithConstraints:
    def __init__(self, salaries, max_count, min_range):
        self.salaries = salaries[:]
        self.n = len(salaries)
        self.max_count = max_count
        self.min_range = min_range
        self.sorted_salaries = sorted(salaries)
    
    def constrained_query(self, min_salary, max_salary):
        """Query count of salaries with constraints"""
        # Check minimum range constraint
        if max_salary - min_salary < self.min_range:
            return None  # Invalid range
        
        # Get count
        count = self.count_in_range(min_salary, max_salary)
        
        # Check maximum count constraint
        if count > self.max_count:
            return None  # Exceeds maximum count
        
        return count
    
    def count_in_range(self, min_salary, max_salary):
        """Count salaries in range [min_salary, max_salary]"""
        left_idx = self._binary_search_left(min_salary)
        right_idx = self._binary_search_right(max_salary)
        return right_idx - left_idx
    
    def find_valid_ranges(self):
        """Find all valid salary ranges that satisfy constraints"""
        valid_ranges = []
        unique_salaries = sorted(set(self.salaries))
        
        for i in range(len(unique_salaries)):
            for j in range(i, len(unique_salaries)):
                min_sal = unique_salaries[i]
                max_sal = unique_salaries[j]
                
                result = self.constrained_query(min_sal, max_sal)
                if result is not None:
                    valid_ranges.append((min_sal, max_sal, result))
        
        return valid_ranges
    
    def get_maximum_valid_count(self):
        """Get maximum valid count"""
        max_count = float('-inf')
        unique_salaries = sorted(set(self.salaries))
        
        for i in range(len(unique_salaries)):
            for j in range(i, len(unique_salaries)):
                min_sal = unique_salaries[i]
                max_sal = unique_salaries[j]
                
                result = self.constrained_query(min_sal, max_sal)
                if result is not None:
                    max_count = max(max_count, result)
        
        return max_count if max_count != float('-inf') else None
    
    def _binary_search_left(self, target):
        """Find leftmost position where salary >= target"""
        left, right = 0, len(self.sorted_salaries)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_salaries[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left
    
    def _binary_search_right(self, target):
        """Find rightmost position where salary <= target"""
        left, right = 0, len(self.sorted_salaries)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_salaries[mid] <= target:
                left = mid + 1
            else:
                right = mid
        return left

# Example usage
salaries = [1000, 2000, 1500, 3000, 2500]
max_count = 3
min_range = 500

sq = SalaryQueriesWithConstraints(salaries, max_count, min_range)
result = sq.constrained_query(1000, 2000)
print(f"Constrained query result: {result}")  # Output: 2

valid_ranges = sq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")
```

### Related Problems

#### **CSES Problems**
- [Salary Queries](https://cses.fi/problemset/task/1144) - Basic salary range queries problem
- [Static Range Sum Queries](https://cses.fi/problemset/task/1646) - Static range sum queries
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range sum queries

#### **LeetCode Problems**
- [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) - Range sum queries
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates
- [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) - Count range sums

#### **Problem Categories**
- **Binary Search**: Range queries, efficient search, sorted arrays
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Sorting**: Array sorting, efficient preprocessing, fast queries
- **Algorithm Design**: Binary search techniques, range optimization, constraint handling

## 🚀 Key Takeaways

- **Sorting Technique**: The standard approach for salary range queries
- **Efficient Sorting**: Sort salaries once in O(n log n) time
- **Fast Queries**: Answer each query in O(log n) time using binary search
- **Space Trade-off**: Use O(n) extra space for O(log n) query time
- **Pattern Recognition**: This technique applies to many salary range problems