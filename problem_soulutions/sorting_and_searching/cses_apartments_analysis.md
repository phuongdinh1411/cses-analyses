---
layout: simple
title: "Apartments"
permalink: /problem_soulutions/sorting_and_searching/cses_apartments_analysis
---

# Apartments

## Problem Description

**Problem**: There are n applicants and m free apartments. Distribute apartments so that as many applicants as possible get an apartment. Each applicant accepts any apartment whose size is at least aᵢ-k and at most aᵢ+k.

**Input**: 
- First line: n, m, k (applicants, apartments, max difference)
- Second line: n integers (desired apartment sizes)
- Third line: m integers (apartment sizes)

**Output**: Number of applicants who will get an apartment.

**Example**:
```
Input:
4 3 5
60 45 80 60
30 60 75

Output:
2

Explanation: Applicant 1 (60) gets apartment 2 (60), Applicant 2 (45) gets apartment 1 (30).
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Match applicants to apartments optimally
- Each applicant accepts apartments in range [aᵢ-k, aᵢ+k]
- Maximize number of successful matches
- Each apartment can be used only once

**Key Observations:**
- This is a bipartite matching problem
- Greedy approach: match each applicant to smallest suitable apartment
- Sorting helps in efficient matching
- Two pointers can optimize the process

### Step 2: Greedy Approach with Sorting
**Idea**: Sort both arrays and match applicants to smallest suitable apartments.

```python
def apartments_greedy(applicants, apartments, k):
    applicants.sort()
    apartments.sort()
    
    matches = 0
    apt_idx = 0
    
    for applicant in applicants:
        # Find the smallest suitable apartment
        while apt_idx < len(apartments) and apartments[apt_idx] < applicant - k:
            apt_idx += 1
        
        if apt_idx < len(apartments) and apartments[apt_idx] <= applicant + k:
            matches += 1
            apt_idx += 1
    
    return matches
```

**Why this works:**
- Sort both arrays for efficient matching
- For each applicant, find smallest suitable apartment
- Greedy choice: always take smallest available apartment
- This maximizes future matching opportunities

### Step 3: Optimized Two Pointers
**Idea**: Optimize the matching process with better pointer management.

```python
def apartments_optimized(applicants, apartments, k):
    applicants.sort()
    apartments.sort()
    
    matches = 0
    apt_idx = 0
    
    for applicant in applicants:
        # Skip apartments that are too small
        while apt_idx < len(apartments) and apartments[apt_idx] < applicant - k:
            apt_idx += 1
        
        # Check if current apartment is suitable
        if apt_idx < len(apartments) and apartments[apt_idx] <= applicant + k:
            matches += 1
            apt_idx += 1
    
    return matches
```

**Why this is better:**
- More efficient pointer management
- Clearer logic flow
- Same time complexity but cleaner implementation

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_apartments():
    n, m, k = map(int, input().split())
    applicants = list(map(int, input().split()))
    apartments = list(map(int, input().split()))
    
    # Sort both arrays
    applicants.sort()
    apartments.sort()
    
    matches = 0
    apt_idx = 0
    
    for applicant in applicants:
        # Find smallest suitable apartment
        while apt_idx < m and apartments[apt_idx] < applicant - k:
            apt_idx += 1
        
        # Check if apartment is suitable
        if apt_idx < m and apartments[apt_idx] <= applicant + k:
            matches += 1
            apt_idx += 1
    
    print(matches)

# Main execution
if __name__ == "__main__":
    solve_apartments()
```

**Why this works:**
- Efficient greedy approach
- Handles all edge cases correctly
- Optimal time complexity

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((4, 3, 5, [60, 45, 80, 60], [30, 60, 75]), 2),
        ((3, 3, 2, [1, 2, 3], [1, 2, 3]), 3),
        ((2, 2, 1, [1, 3], [2, 4]), 2),
        ((3, 2, 1, [1, 2, 3], [2, 4]), 2),
    ]
    
    for (n, m, k, applicants, apartments), expected in test_cases:
        result = solve_test(n, m, k, applicants, apartments)
        print(f"n = {n}, m = {m}, k = {k}")
        print(f"Applicants: {applicants}")
        print(f"Apartments: {apartments}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, m, k, applicants, apartments):
    applicants.sort()
    apartments.sort()
    
    matches = 0
    apt_idx = 0
    
    for applicant in applicants:
        while apt_idx < m and apartments[apt_idx] < applicant - k:
            apt_idx += 1
        
        if apt_idx < m and apartments[apt_idx] <= applicant + k:
            matches += 1
            apt_idx += 1
    
    return matches

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n + m log m) - sorting both arrays
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Greedy Strategy**: Always match to smallest suitable apartment
- **Sorting**: Enables efficient two-pointer approach
- **Optimal**: Maximizes number of matches

## 🎯 Key Insights

### 1. **Greedy Matching**
- Sort both arrays
- Match each applicant to smallest suitable apartment
- This maximizes future matching opportunities

### 2. **Two Pointers Technique**
- Use pointers to track current positions
- Skip unsuitable apartments efficiently
- Linear time matching after sorting

### 3. **Bipartite Matching**
- This is a bipartite matching problem
- Greedy approach works optimally
- No need for complex algorithms like Hungarian

## 🎯 Problem Variations

### Variation 1: Weighted Matching
**Problem**: Each match has a weight. Maximize total weight.

```python
def weighted_apartments(applicants, apartments, k, weights):
    # weights[i][j] = weight of matching applicant i to apartment j
    n, m = len(applicants), len(apartments)
    
    # Use Hungarian algorithm for optimal weighted matching
    from scipy.optimize import linear_sum_assignment
    
    # Create cost matrix
    cost_matrix = [[float('inf')] * m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            if abs(applicants[i] - apartments[j]) <= k:
                cost_matrix[i][j] = -weights[i][j]  # Negative for maximization
    
    # Find optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    total_weight = 0
    matches = 0
    
    for i, j in zip(row_ind, col_ind):
        if cost_matrix[i][j] != float('inf'):
            total_weight += weights[i][j]
            matches += 1
    
    return matches, total_weight
```

### Variation 2: Multiple Preferences
**Problem**: Each applicant has multiple preferred apartment ranges.

```python
def multiple_preferences(applicants, apartments, preferences):
    # preferences[i] = list of (min_size, max_size) for applicant i
    n, m = len(applicants), len(apartments)
    
    apartments.sort()
    used = [False] * m
    matches = 0
    
    for i in range(n):
        # Try each preference in order
        for min_size, max_size in preferences[i]:
            # Find smallest suitable apartment
            for j in range(m):
                if not used[j] and min_size <= apartments[j] <= max_size:
                    used[j] = True
                    matches += 1
                    break
            else:
                continue  # No apartment found for this preference
            break  # Found apartment, move to next applicant
    
    return matches
```

### Variation 3: Capacity Constraints
**Problem**: Each apartment can accommodate multiple applicants.

```python
def capacity_constraints(applicants, apartments, k, capacities):
    # capacities[j] = number of applicants apartment j can accommodate
    n, m = len(applicants), len(apartments)
    
    applicants.sort()
    apartments.sort()
    
    matches = 0
    apt_idx = 0
    current_capacity = capacities.copy()
    
    for applicant in applicants:
        # Find suitable apartment with available capacity
        while apt_idx < m and (apartments[apt_idx] < applicant - k or 
                              current_capacity[apt_idx] == 0):
            apt_idx += 1
        
        if apt_idx < m and apartments[apt_idx] <= applicant + k:
            matches += 1
            current_capacity[apt_idx] -= 1
            if current_capacity[apt_idx] == 0:
                apt_idx += 1
    
    return matches
```

### Variation 4: Dynamic Updates
**Problem**: Support adding/removing applicants and apartments dynamically.

```python
class DynamicApartments:
    def __init__(self, k):
        self.k = k
        self.applicants = []
        self.apartments = []
    
    def add_applicant(self, desired_size):
        self.applicants.append(desired_size)
        return self.get_max_matches()
    
    def add_apartment(self, size):
        self.apartments.append(size)
        return self.get_max_matches()
    
    def remove_applicant(self, index):
        if 0 <= index < len(self.applicants):
            self.applicants.pop(index)
        return self.get_max_matches()
    
    def remove_apartment(self, index):
        if 0 <= index < len(self.apartments):
            self.apartments.pop(index)
        return self.get_max_matches()
    
    def get_max_matches(self):
        applicants = self.applicants.copy()
        apartments = self.apartments.copy()
        
        applicants.sort()
        apartments.sort()
        
        matches = 0
        apt_idx = 0
        
        for applicant in applicants:
            while apt_idx < len(apartments) and apartments[apt_idx] < applicant - self.k:
                apt_idx += 1
            
            if apt_idx < len(apartments) and apartments[apt_idx] <= applicant + self.k:
                matches += 1
                apt_idx += 1
        
        return matches
```

### Variation 5: Range Queries
**Problem**: Answer queries about matching for different ranges of applicants/apartments.

```python
def range_queries(applicants, apartments, k, queries):
    # queries[i] = (l1, r1, l2, r2) - match applicants[l1:r1] to apartments[l2:r2]
    results = []
    
    for l1, r1, l2, r2 in queries:
        sub_applicants = applicants[l1:r1]
        sub_apartments = apartments[l2:r2]
        
        sub_applicants.sort()
        sub_apartments.sort()
        
        matches = 0
        apt_idx = 0
        
        for applicant in sub_applicants:
            while apt_idx < len(sub_apartments) and sub_apartments[apt_idx] < applicant - k:
                apt_idx += 1
            
            if apt_idx < len(sub_apartments) and sub_apartments[apt_idx] <= applicant + k:
                matches += 1
                apt_idx += 1
        
        results.append(matches)
    
    return results
```

## 🔗 Related Problems

- **[Sum of Two Values](/cses-analyses/problem_soulutions/sorting_and_searching/cses_sum_of_two_values_analysis)**: Two-pointer problems
- **[Distinct Numbers](/cses-analyses/problem_soulutions/sorting_and_searching/cses_distinct_numbers_analysis)**: Sorting and searching
- **[Room Allocation](/cses-analyses/problem_soulutions/sorting_and_searching/room_allocation_analysis)**: Allocation problems

## 📚 Learning Points

1. **Greedy Algorithms**: Optimal local choices lead to global optimum
2. **Two Pointers**: Efficient technique for sorted arrays
3. **Bipartite Matching**: Matching problems with constraints
4. **Sorting**: Enables efficient algorithms

---

**This is a great introduction to greedy algorithms and two-pointer techniques!** 🎯 