---
layout: simple
title: "Ferris Wheel"
permalink: /problem_soulutions/sorting_and_searching/ferris_wheel_analysis
---

# Ferris Wheel

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the two-pointer technique and its applications
- Apply greedy algorithms for optimization problems
- Implement efficient sorting and searching algorithms
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in pairing problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, two-pointer technique, greedy algorithms, binary search
- **Data Structures**: Arrays, sorting algorithms
- **Mathematical Concepts**: Optimization, pairing problems, constraint satisfaction
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting
- **Related Problems**: Apartments (two-pointer), Sum of Two Values (two-pointer), Collecting Numbers (greedy)

## 📋 Problem Description

There are n children who want to go to a Ferris wheel, and your task is to find a gondola for each child. Each gondola has a maximum weight capacity of x, and the weight of the i-th child is w[i].

Find the minimum number of gondolas needed to accommodate all children, where each gondola can carry at most two children and the total weight cannot exceed x.

**Input**: 
- First line: two integers n and x (number of children and maximum weight)
- Second line: n integers w[1], w[2], ..., w[n] (weights of children)

**Output**: 
- Print one integer: the minimum number of gondolas needed

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ x ≤ 10⁹
- 1 ≤ w[i] ≤ x

**Example**:
```
Input:
4 10
7 2 3 9

Output:
3

Explanation**: 
Children weights: [7, 2, 3, 9], capacity: 10

Optimal pairing:
- Gondola 1: child with weight 7 (alone, since 7+2=9≤10 but 7+3=10≤10, but 7+9=16>10)
- Gondola 2: children with weights 2 and 3 (2+3=5≤10)
- Gondola 3: child with weight 9 (alone, since 9+any other>10)

Total gondolas: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Pairings

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible ways to pair children
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward recursive approach
- **Inefficient**: Exponential time complexity

**Key Insight**: Generate all possible ways to pair children and find the minimum number of gondolas.

**Algorithm**:
- Generate all possible pairings of children
- For each pairing, check if it's valid (total weight ≤ capacity)
- Find the pairing that uses the minimum number of gondolas

**Visual Example**:
```
Weights: [7, 2, 3, 9], Capacity: 10

All possible pairings:
1. All alone: [7], [2], [3], [9] → 4 gondolas
2. Pair (2,3): [7], [2,3], [9] → 3 gondolas ✓
3. Pair (2,7): [2,7], [3], [9] → 3 gondolas ✓
4. Pair (3,7): [3,7], [2], [9] → 3 gondolas ✓
5. Pair (2,9): [2,9], [7], [3] → 3 gondolas ✓
6. Pair (3,9): [3,9], [7], [2] → 3 gondolas ✓
7. Pair (7,9): Invalid (7+9=16>10)

Minimum: 3 gondolas
```

**Implementation**:
```python
def brute_force_ferris_wheel(weights, capacity):
    """
    Find minimum gondolas using brute force approach
    
    Args:
        weights: list of child weights
        capacity: maximum weight per gondola
    
    Returns:
        int: minimum number of gondolas needed
    """
    from itertools import combinations
    
    n = len(weights)
    min_gondolas = n  # Worst case: all children alone
    
    # Try all possible ways to pair children
    for k in range(n // 2 + 1):
        for pairs in combinations(range(n), 2 * k):
            # Check if this pairing is valid
            used = set(pairs)
            remaining = [i for i in range(n) if i not in used]
            
            # Check if all pairs are valid
            valid = True
            for i in range(0, len(pairs), 2):
                if weights[pairs[i]] + weights[pairs[i+1]] > capacity:
                    valid = False
                    break
            
            if valid:
                gondolas = k + len(remaining)
                min_gondolas = min(min_gondolas, gondolas)
    
    return min_gondolas

# Example usage
weights = [7, 2, 3, 9]
capacity = 10
result = brute_force_ferris_wheel(weights, capacity)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(2^n × n) - Exponential in number of children
**Space Complexity**: O(n) - For storing combinations

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Greedy Pairing

**Key Insights from Optimized Approach**:
- **Greedy Strategy**: Always try to pair the heaviest child with the lightest available child
- **Efficient Processing**: Process children in sorted order
- **Better Complexity**: Achieve O(n²) time complexity
- **Not Always Optimal**: Greedy approach may not always give the optimal solution

**Key Insight**: Use a greedy approach to pair children, always trying to pair the heaviest child with the lightest available child.

**Algorithm**:
- Sort children by weight
- For each child from heaviest to lightest:
  - Try to pair with the lightest available child
  - If pairing is valid, use one gondola for both
  - Otherwise, use one gondola for the heavy child alone

**Visual Example**:
```
Weights: [7, 2, 3, 9], Capacity: 10
Sorted: [2, 3, 7, 9]

Greedy pairing:
1. Heaviest: 9, try to pair with lightest: 2 → 9+2=11>10 ✗
2. Heaviest: 9, try to pair with next: 3 → 9+3=12>10 ✗
3. Heaviest: 9, try to pair with next: 7 → 9+7=16>10 ✗
4. Child 9 goes alone → 1 gondola
5. Heaviest: 7, try to pair with lightest: 2 → 7+2=9≤10 ✓
6. Children 7 and 2 paired → 1 gondola
7. Heaviest: 3, no one left to pair → 1 gondola

Total: 3 gondolas
```

**Implementation**:
```python
def optimized_ferris_wheel(weights, capacity):
    """
    Find minimum gondolas using greedy approach
    
    Args:
        weights: list of child weights
        capacity: maximum weight per gondola
    
    Returns:
        int: minimum number of gondolas needed
    """
    weights = sorted(weights)
    used = [False] * len(weights)
    gondolas = 0
    
    # Process from heaviest to lightest
    for i in range(len(weights) - 1, -1, -1):
        if used[i]:
            continue
        
        # Try to pair with lightest available child
        paired = False
        for j in range(len(weights)):
            if not used[j] and i != j and weights[i] + weights[j] <= capacity:
                used[i] = used[j] = True
                gondolas += 1
                paired = True
                break
        
        if not paired:
            used[i] = True
            gondolas += 1
    
    return gondolas

# Example usage
weights = [7, 2, 3, 9]
capacity = 10
result = optimized_ferris_wheel(weights, capacity)
print(f"Optimized result: {result}")  # Output: 3
```

**Time Complexity**: O(n²) - For each child, check all other children
**Space Complexity**: O(n) - For used array

**Why it's better**: Much more efficient than brute force, but still not optimal.

---

### Approach 3: Optimal - Two Pointer Technique

**Key Insights from Optimal Approach**:
- **Two Pointer Technique**: Use two pointers to efficiently find valid pairs
- **Optimal Strategy**: Always pair the heaviest child with the lightest available child
- **Linear Time**: Achieve O(n log n) time complexity (due to sorting)
- **Mathematically Optimal**: This approach is proven to be optimal

**Key Insight**: Sort the weights and use two pointers to efficiently find the optimal pairing.

**Algorithm**:
- Sort children by weight
- Use two pointers: one at the beginning (lightest) and one at the end (heaviest)
- Try to pair the heaviest child with the lightest child
- If pairing is valid, use one gondola for both and move both pointers
- Otherwise, use one gondola for the heavy child alone and move only the right pointer

**Visual Example**:
```
Weights: [7, 2, 3, 9], Capacity: 10
Sorted: [2, 3, 7, 9]

Two pointer approach:
1. left=0, right=3: weights[0]=2, weights[3]=9 → 2+9=11>10 ✗
   - Child 9 goes alone, right=2
2. left=0, right=2: weights[0]=2, weights[2]=7 → 2+7=9≤10 ✓
   - Children 2 and 7 paired, left=1, right=1
3. left=1, right=1: weights[1]=3, weights[1]=3 → 3+3=6≤10 ✓
   - Child 3 goes alone, left=2, right=0

Total: 3 gondolas
```

**Implementation**:
```python
def optimal_ferris_wheel(weights, capacity):
    """
    Find minimum gondolas using two pointer technique
    
    Args:
        weights: list of child weights
        capacity: maximum weight per gondola
    
    Returns:
        int: minimum number of gondolas needed
    """
    weights.sort()
    left, right = 0, len(weights) - 1
    gondolas = 0
    
    while left <= right:
        if left == right:
            # Only one child left
            gondolas += 1
            break
        
        if weights[left] + weights[right] <= capacity:
            # Can pair the lightest and heaviest
            gondolas += 1
            left += 1
            right -= 1
        else:
            # Heaviest child must go alone
            gondolas += 1
            right -= 1
    
    return gondolas

# Example usage
weights = [7, 2, 3, 9]
capacity = 10
result = optimal_ferris_wheel(weights, capacity)
print(f"Optimal result: {result}")  # Output: 3
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: Achieves the best possible time complexity and is mathematically proven to be optimal.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n) | O(n) | Try all pairings |
| Greedy | O(n²) | O(n) | Pair heaviest with lightest |
| Two Pointer | O(n log n) | O(1) | Optimal pairing strategy |

### Time Complexity
- **Time**: O(n log n) - Two pointer technique provides optimal time complexity
- **Space**: O(1) - Constant extra space for two pointers

### Why This Solution Works
- **Greedy Choice**: Always pairing heaviest with lightest is optimal
- **Two Pointer Efficiency**: Eliminates redundant checks
- **Mathematical Proof**: This approach is proven to be optimal
- **Optimal Approach**: Two pointer technique provides the best balance of efficiency and correctness

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Ferris Wheel with Multiple Cars
**Problem**: Ferris wheel has multiple cars, each with different capacity limits.

**Link**: [CSES Problem Set - Ferris Wheel Multiple Cars](https://cses.fi/problemset/task/ferris_wheel_multiple_cars)

```python
def ferris_wheel_multiple_cars(weights, car_capacities):
    """
    Handle ferris wheel with multiple cars of different capacities
    """
    # Sort weights in descending order
    weights.sort(reverse=True)
    
    # Sort car capacities in descending order
    car_capacities.sort(reverse=True)
    
    # Use two pointers for each car
    result = 0
    used_weights = [False] * len(weights)
    
    for capacity in car_capacities:
        # Find pairs for this car
        left = 0
        right = len(weights) - 1
        car_pairs = 0
        
        while left < right:
            # Skip used weights
            while left < len(weights) and used_weights[left]:
                left += 1
            while right >= 0 and used_weights[right]:
                right -= 1
            
            if left >= right:
                break
            
            # Check if pair fits in car
            if weights[left] + weights[right] <= capacity:
                used_weights[left] = True
                used_weights[right] = True
                car_pairs += 1
                left += 1
                right -= 1
            else:
                # Heaviest person alone
                used_weights[left] = True
                car_pairs += 1
                left += 1
        
        result += car_pairs
    
    return result
```

### Variation 2: Ferris Wheel with Time Constraints
**Problem**: Each person has a time limit, and the ferris wheel takes time to complete a ride.

**Link**: [CSES Problem Set - Ferris Wheel Time Constraints](https://cses.fi/problemset/task/ferris_wheel_time)

```python
def ferris_wheel_time_constraints(people, capacity, ride_time):
    """
    Handle ferris wheel with time constraints for each person
    """
    # Sort people by time limit (ascending)
    people.sort(key=lambda x: x['time_limit'])
    
    result = 0
    used = [False] * len(people)
    
    for i in range(len(people)):
        if used[i]:
            continue
        
        # Find best partner for this person
        best_partner = -1
        best_weight_sum = float('inf')
        
        for j in range(i + 1, len(people)):
            if used[j]:
                continue
            
            # Check if both can ride together
            if (people[i]['time_limit'] >= ride_time and 
                people[j]['time_limit'] >= ride_time):
                
                weight_sum = people[i]['weight'] + people[j]['weight']
                if weight_sum <= capacity and weight_sum < best_weight_sum:
                    best_partner = j
                    best_weight_sum = weight_sum
        
        if best_partner != -1:
            # Pair them together
            used[i] = True
            used[best_partner] = True
            result += 1
        else:
            # Single person ride
            if people[i]['weight'] <= capacity:
                used[i] = True
                result += 1
    
    return result
```

### Variation 3: Ferris Wheel with Priority Queues
**Problem**: People have different priorities, and we want to maximize total priority.

**Link**: [CSES Problem Set - Ferris Wheel Priority Queues](https://cses.fi/problemset/task/ferris_wheel_priority)

```python
def ferris_wheel_priority_queues(people, capacity):
    """
    Handle ferris wheel with priority optimization
    """
    # Sort people by priority (descending)
    people.sort(key=lambda x: x['priority'], reverse=True)
    
    result = 0
    used = [False] * len(people)
    
    for i in range(len(people)):
        if used[i]:
            continue
        
        # Find best partner for this person
        best_partner = -1
        best_priority_sum = 0
        
        for j in range(i + 1, len(people)):
            if used[j]:
                continue
            
            # Check if they can ride together
            if people[i]['weight'] + people[j]['weight'] <= capacity:
                priority_sum = people[i]['priority'] + people[j]['priority']
                if priority_sum > best_priority_sum:
                    best_partner = j
                    best_priority_sum = priority_sum
        
        if best_partner != -1:
            # Pair them together
            used[i] = True
            used[best_partner] = True
            result += best_priority_sum
        else:
            # Single person ride
            if people[i]['weight'] <= capacity:
                used[i] = True
                result += people[i]['priority']
    
    return result
```

### Related Problems

#### **CSES Problems**
- [Ferris Wheel](https://cses.fi/problemset/task/1090) - Basic ferris wheel problem
- [Apartments](https://cses.fi/problemset/task/1084) - Similar two-pointer problem
- [Concert Tickets](https://cses.fi/problemset/task/1091) - Binary search optimization

#### **LeetCode Problems**
- [Two Sum](https://leetcode.com/problems/two-sum/) - Find pairs with target sum
- [3Sum](https://leetcode.com/problems/3sum/) - Find triplets with zero sum
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) - Two-pointer optimization
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) - Two-pointer water trapping

#### **Problem Categories**
- **Two Pointers**: Efficient array processing, sorted array algorithms, pairing problems
- **Greedy Algorithms**: Optimal local choices, sorting-based optimization, matching problems
- **Sorting**: Array sorting, two-pointer techniques, efficient pairing algorithms
- **Algorithm Design**: Two-pointer techniques, greedy strategies, optimization algorithms
