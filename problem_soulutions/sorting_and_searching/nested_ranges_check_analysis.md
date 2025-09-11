---
layout: simple
title: "Nested Ranges Check"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_check_analysis
---

# Nested Ranges Check

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of range nesting and interval relationships
- Apply sorting and coordinate compression techniques for range problems
- Implement efficient solutions for range checking problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in range intersection problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, coordinate compression, range queries, interval scheduling
- **Data Structures**: Arrays, sorted arrays, coordinate compression
- **Mathematical Concepts**: Range theory, interval relationships, coordinate compression
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting algorithms
- **Related Problems**: Nested Ranges Count (counting), Range Queries (queries), Interval Scheduling (scheduling)

## 📋 Problem Description

You are given n ranges [a[i], b[i]]. For each range, determine if it contains any other range or is contained by any other range.

A range [a[i], b[i]] contains range [a[j], b[j]] if a[i] ≤ a[j] and b[j] ≤ b[i].
A range [a[i], b[i]] is contained by range [a[j], b[j]] if a[j] ≤ a[i] and b[i] ≤ b[j].

**Input**: 
- First line: integer n (number of ranges)
- Next n lines: two integers a[i] and b[i] (range endpoints)

**Output**: 
- Print n lines: for each range, print "YES" if it contains or is contained by another range, "NO" otherwise

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ b[i] ≤ 10⁹

**Example**:
```
Input:
4
1 6
2 4
3 5
7 8

Output:
YES
YES
YES
NO

Explanation**: 
Ranges: [1,6], [2,4], [3,5], [7,8]

Range 1 [1,6]: Contains [2,4] and [3,5] → YES
Range 2 [2,4]: Contained by [1,6] → YES
Range 3 [3,5]: Contained by [1,6] → YES
Range 4 [7,8]: No nesting relationship → NO
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: [Description]
- **Complete Coverage**: [Description]
- **Simple Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def brute_force_nested_ranges_check(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's inefficient**: [Reason]

---

### Approach 2: Optimized

**Key Insights from Optimized Approach**:
- **Optimization Technique**: [Description]
- **Efficiency Improvement**: [Description]
- **Better Complexity**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimized_nested_ranges_check(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's better**: [Reason]

---

### Approach 3: Optimal

**Key Insights from Optimal Approach**:
- **Optimal Algorithm**: [Description]
- **Best Complexity**: [Description]
- **Efficient Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimal_nested_ranges_check(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's optimal**: [Reason]

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O([complexity]) | O([complexity]) | [Insight] |
| Optimized | O([complexity]) | O([complexity]) | [Insight] |
| Optimal | O([complexity]) | O([complexity]) | [Insight] |

### Time Complexity
- **Time**: O([complexity]) - [Explanation]
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **[Reason 1]**: [Explanation]
- **[Reason 2]**: [Explanation]
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
