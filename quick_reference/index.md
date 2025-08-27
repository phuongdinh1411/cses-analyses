# 📚 Quick Reference Index

## 🚀 Getting Started
- **[Main README](../README.md)**: Complete overview and navigation
- **[Learning Paths](../study_materials/learning_paths.md)**: Choose your study path
- **[Weekly Guides](../study_materials/weekly_guides.md)**: Structured weekly plans

## 🎯 Quick Reference Guides
- **[Algorithm Cheatsheet](algorithm_cheatsheet.md)**: All algorithms at a glance
- **[Decision Tree](decision_tree.md)**: Choose the right algorithm
- **[Common Mistakes](common_mistakes.md)**: Avoid common pitfalls
- **[Visual Aids](visual_aids.md)**: Diagrams and flowcharts
- **[Problem Template](problem_template.md)**: Standard analysis format

## 📖 Study Materials
- **[Self Assessment](../study_materials/self_assessment.md)**: Track your progress
- **[3 Month Learning Plan](../3_month_learning_plan.md)**: Structured study plan

## 🎯 Problem Categories
- **[Introductory Problems](../introductory_problems/)**: 25 problems
- **[Sorting and Searching](../sorting_and_searching/)**: 35 problems
- **[Dynamic Programming](../dynamic_programming/)**: 17 problems
- **[Graph Algorithms](../graph_algorithms/)**: 36 problems
- **[Tree Algorithms](../tree_algorithms/)**: 15 problems
- **[String Algorithms](../string_algorithms/)**: 14 problems
- **[Sliding Window](../sliding_window/)**: 15 problems
- **[Range Queries](../range_queries/)**: 20 problems
- **[Advanced Graph Problems](../advanced_graph_problems/)**: 28 problems
- **[Counting Problems](../counting_problems/)**: 19 problems
- **[Geometry](../geometry/)**: 16 problems

## 🎯 Quick Navigation

### 🚀 Need to solve a problem quickly?
1. Check **[Algorithm Cheatsheet](algorithm_cheatsheet.md)**
2. Use **[Decision Tree](decision_tree.md)**
3. Follow **[Problem Template](problem_template.md)**

### 🚀 Learning a new algorithm?
1. Find it in **[Algorithm Cheatsheet](algorithm_cheatsheet.md)**
2. Check **[Visual Aids](visual_aids.md)** for diagrams
3. Practice with problems in relevant category

### 🚀 Avoiding mistakes?
1. Review **[Common Mistakes](common_mistakes.md)**
2. Check **[Problem Template](problem_template.md)** for edge cases
3. Use **[Self Assessment](../study_materials/self_assessment.md)**

### 🚀 Planning your study?
1. Choose path in **[Learning Paths](../study_materials/learning_paths.md)**
2. Follow **[Weekly Guides](../study_materials/weekly_guides.md)**
3. Track progress with **[Self Assessment](../study_materials/self_assessment.md)**

## 🎯 Emergency Quick Reference

### 🔍 Problem Type Identification
- **"maximum/minimum"** → Dynamic Programming
- **"shortest path"** → Graph Algorithms
- **"subtree/ancestor"** → Tree Algorithms
- **"range/query"** → Range Queries
- **"pattern/substring"** → String Algorithms
- **"find/search"** → Binary Search
- **"subarray/window"** → Sliding Window

### 📏 Constraint-Based Algorithm Choice
- **n ≤ 10⁶** → O(n) or O(n log n) required
- **n ≤ 10³** → O(n²) acceptable
- **n ≤ 20** → O(2ⁿ) acceptable (bitmask)
- **queries ≤ 10⁵** → O(log n) per query

### ⚠️ Common Pitfalls
- **Nested loops** = O(n²) not O(n)
- **String operations** = O(n) not O(1)
- **List operations** = O(n) not O(1)
- **Always check edge cases**
- **Handle integer overflow**

## 🎯 Quick Code Templates

### 🔍 Binary Search
```python
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

### 🌊 DFS
```python
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

### 🎯 DP Template
```python
def dp_solution(n):
    dp = [0] * (n + 1)
    dp[0] = 1  # base case
    for i in range(1, n + 1):
        # fill dp[i] based on subproblems
        pass
    return dp[n]
```

### 🔢 Modular Arithmetic
```python
MOD = 10**9 + 7
result = (result + value) % MOD
```

## 🎯 Success Checklist

### 📋 Before Solving
- [ ] Read problem carefully
- [ ] Identify keywords and constraints
- [ ] Choose appropriate algorithm
- [ ] Plan implementation approach

### 📋 During Solving
- [ ] Start with brute force if needed
- [ ] Optimize step by step
- [ ] Handle edge cases
- [ ] Test with examples

### 📋 After Solving
- [ ] Verify time complexity
- [ ] Check space complexity
- [ ] Test edge cases
- [ ] Review solution

## 🚀 Quick Tips

### 🎯 Problem-Solving
- **Start simple**: Don't overcomplicate
- **Test examples**: Always verify with small cases
- **Check constraints**: Choose algorithm accordingly
- **Handle edge cases**: Empty input, single element, etc.

### 🎯 Implementation
- **Use appropriate data structures**: Lists, sets, heaps, etc.
- **Optimize when needed**: Don't optimize prematurely
- **Write clean code**: Readable and maintainable
- **Add comments**: Explain complex logic

### 🎯 Learning
- **Practice regularly**: Consistency is key
- **Review solutions**: Understand why they work
- **Learn patterns**: Recognize common techniques
- **Build intuition**: Develop problem-solving sense

---

**Happy Problem Solving! 🚀**
