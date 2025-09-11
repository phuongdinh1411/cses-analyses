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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Range counting, salary query problems, range queries
- **Data Structures**: Arrays, range query structures
- **Mathematical Concepts**: Salary query optimization, range counting optimization
- **Programming Skills**: Array manipulation, range counting implementation
- **Related Problems**: Range queries, salary problems, range counting problems

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

## 🚀 Key Takeaways

- **Sorting Technique**: The standard approach for salary range queries
- **Efficient Sorting**: Sort salaries once in O(n log n) time
- **Fast Queries**: Answer each query in O(log n) time using binary search
- **Space Trade-off**: Use O(n) extra space for O(log n) query time
- **Pattern Recognition**: This technique applies to many salary range problems