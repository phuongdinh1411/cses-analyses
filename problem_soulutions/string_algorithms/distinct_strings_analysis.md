---
layout: simple
title: "Distinct Strings"
permalink: /problem_soulutions/string_algorithms/distinct_strings_analysis
---

# Distinct Strings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of string hashing and its applications
- Apply rolling hash technique for efficient string comparison
- Implement efficient solutions for string counting problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in string hashing problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String hashing, rolling hash, hash collision handling, string comparison
- **Data Structures**: Hash maps, strings, rolling hash arrays
- **Mathematical Concepts**: Hash functions, modular arithmetic, polynomial hashing, collision probability
- **Programming Skills**: String manipulation, hash function implementation, complexity analysis
- **Related Problems**: String Matching (hashing), Pattern Positions (hashing), Finding Borders (hashing)

## 📋 Problem Description

You are given a string s of length n. Count the number of distinct substrings in the string.

A substring is a contiguous sequence of characters within a string.

**Input**: 
- One string s (the input string)

**Output**: 
- Print one integer: the number of distinct substrings

**Constraints**:
- 1 ≤ n ≤ 10⁵
- String contains only lowercase English letters

**Example**:
```
Input:
abc

Output:
6

Explanation**: 
String: "abc"

All substrings:
1. "a" (position 0)
2. "b" (position 1)  
3. "c" (position 2)
4. "ab" (positions 0-1)
5. "bc" (positions 1-2)
6. "abc" (positions 0-2)

Total distinct substrings: 6
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
def brute_force_distinct_strings(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
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
def optimized_distinct_strings(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
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
def optimal_distinct_strings(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
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
