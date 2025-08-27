# 🎯 Problem-Solving Decision Tree

## 🚀 Quick Algorithm Selection Guide

### 📋 Step 1: Read Problem Carefully
- **Identify keywords** in the problem statement
- **Note constraints** (n ≤ 10⁵, etc.)
- **Understand what's being asked**

### 🔍 Step 2: Problem Classification

#### 🤔 Is it an optimization problem?
- **Keywords**: "maximum", "minimum", "optimal", "best"
- **→ Dynamic Programming**

#### 🌐 Is it about connections/paths?
- **Keywords**: "shortest path", "connected", "reachable", "route"
- **→ Graph Algorithms**

#### 🌳 Is it hierarchical/tree-like?
- **Keywords**: "parent", "child", "subtree", "ancestor"
- **→ Tree Algorithms**

#### 📊 Is it about ranges/queries?
- **Keywords**: "range", "query", "sum", "minimum in range"
- **→ Range Queries**

#### 📝 Is it about strings?
- **Keywords**: "pattern", "substring", "palindrome", "match"
- **→ String Algorithms**

#### 🔍 Is it about searching?
- **Keywords**: "find", "search", "binary search"
- **→ Binary Search**

#### 👆 Is it about subarrays/windows?
- **Keywords**: "subarray", "window", "consecutive", "k elements"
- **→ Two Pointers/Sliding Window**

#### 🔢 Is it about counting?
- **Keywords**: "count", "number of ways", "how many"
- **→ Combinatorics/Counting**

## 🎯 Algorithm Selection Flowchart

```
Problem Statement
       ↓
Read Constraints
       ↓
Identify Keywords
       ↓
Choose Algorithm Category
       ↓
Select Specific Algorithm
       ↓
Implement Solution
       ↓
Test & Optimize
```

## 📏 Constraint-Based Algorithm Selection

### 🚀 For n ≤ 10⁶ (Large Input)
- **O(n) or O(n log n) required**
- **Avoid O(n²) algorithms**
- **Use efficient data structures**

### 🔍 For n ≤ 10⁵ (Medium Input)
- **O(n log n) acceptable**
- **Can use sorting + binary search**
- **Segment trees, BIT acceptable**

### 🎯 For n ≤ 10³ (Small Input)
- **O(n²) acceptable**
- **Can use brute force with optimization**
- **DP with 2D state space**

### 🔢 For n ≤ 20 (Very Small Input)
- **O(2ⁿ) acceptable**
- **Bitmask DP**
- **Backtracking**

## 💡 Quick Decision Rules

### 🎯 Dynamic Programming
- **"Find maximum/minimum"** + **"choices/decisions"**
- **"Count ways"** + **"constraints"**
- **"Optimal substructure"** (subproblems)

### 🌐 Graph Algorithms
- **"Shortest path"** → Dijkstra/Bellman-Ford
- **"All pairs shortest"** → Floyd-Warshall
- **"Connected components"** → DFS/BFS
- **"Topological order"** → Kahn's Algorithm

### 🌳 Tree Algorithms
- **"Lowest common ancestor"** → Binary Lifting
- **"Tree diameter"** → DFS twice
- **"Subtree queries"** → Euler Tour + Segment Tree

### 🔍 Range Queries
- **"Static queries"** → Prefix Sum/Sparse Table
- **"Dynamic queries"** → Segment Tree/BIT
- **"Range updates"** → Lazy Propagation

### 📝 String Algorithms
- **"Pattern matching"** → KMP
- **"Palindrome"** → Manacher
- **"Suffix operations"** → Suffix Array

## 🚨 Common Mistakes to Avoid

### ⏰ Wrong Algorithm Choice
- **Using O(n²) for n ≤ 10⁶**
- **Using DP for simple greedy problems**
- **Using complex algorithms for simple problems**

### 🔍 Misreading Problem
- **Not checking constraints carefully**
- **Missing edge cases**
- **Misunderstanding problem requirements**

### 💻 Implementation Errors
- **Off-by-one errors**
- **Integer overflow**
- **Incorrect base cases**

## 🎯 Practice Strategy

### 📚 For Beginners
1. **Start with Introductory Problems**
2. **Focus on understanding patterns**
3. **Practice implementing from scratch**
4. **Review solutions after solving**

### 🚀 For Intermediate
1. **Practice algorithm identification**
2. **Work on time management**
3. **Focus on optimization**
4. **Learn advanced techniques**

### 🏆 For Advanced
1. **Master all algorithm categories**
2. **Practice contest-style problems**
3. **Focus on speed and accuracy**
4. **Learn problem-solving intuition**
