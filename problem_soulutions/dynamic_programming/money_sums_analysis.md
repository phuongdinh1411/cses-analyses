---
layout: simple
title: "Money Sums - Find All Possible Sums"
permalink: /problem_soulutions/dynamic_programming/money_sums_analysis
---

# Money Sums - Find All Possible Sums

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand subset sum problems and achievable sum calculations in DP
- Apply DP techniques to find all possible sums using boolean DP arrays
- Implement efficient DP solutions for subset sum enumeration and tracking
- Optimize DP solutions using space-efficient techniques and sum enumeration
- Handle edge cases in subset sum DP (empty subsets, single coins, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, subset sum problems, boolean DP, sum enumeration
- **Data Structures**: Arrays, boolean DP tables, sum tracking structures
- **Mathematical Concepts**: Subset theory, sum enumeration, boolean logic, modular arithmetic
- **Programming Skills**: Array manipulation, boolean operations, iterative programming, DP implementation
- **Related Problems**: Coin Combinations I (counting DP), Minimizing Coins (optimization DP), Two Sets II (partition problems)

## Problem Description

Given n coins with different values, find all possible sums that can be formed using any subset of the coins.

**Input**: 
- First line: integer n (number of coins)
- Second line: n integers a1, a2, ..., an (values of the coins)

**Output**: 
- First line: number of different sums
- Second line: the sums in ascending order

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ ai ≤ 1000
- Each coin can be used at most once
- Find all possible sums using subsets of coins
- Output sums in ascending order
- Include sum 0 (empty subset)

**Example**:
```
Input:
4
4 2 5 2

Output:
9
0 2 4 5 6 7 8 9 11

Explanation**: 
All possible sums using subsets of coins:
- {} → 0, {2} → 2, {4} → 4, {5} → 5
- {2,2} → 4, {2,4} → 6, {2,5} → 7, {4,5} → 9
- {2,2,4} → 8, {2,2,5} → 9, {2,4,5} → 11
- {2,2,4,5} → 13 (but this exceeds the maximum possible sum)
```
