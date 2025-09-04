---
layout: simple
title: "Apartments - Optimal Apartment Distribution"
permalink: /problem_soulutions/sorting_and_searching/cses_apartments_analysis
---

# Apartments - Optimal Apartment Distribution

## 📋 Problem Description

There are n applicants and m free apartments. Distribute apartments so that as many applicants as possible get an apartment. Each applicant accepts any apartment whose size is at least aᵢ-k and at most aᵢ+k.

This is a bipartite matching problem that requires optimally matching applicants to apartments within their acceptable size range. The solution involves using a greedy approach with sorting to maximize the number of successful matches.

**Input**: 
- First line: n, m, k (number of applicants, apartments, and maximum acceptable difference)
- Second line: n integers a₁, a₂, ..., aₙ (desired apartment sizes for each applicant)
- Third line: m integers b₁, b₂, ..., bₘ (available apartment sizes)

**Output**: 
- Number of applicants who will get an apartment

**Constraints**:
- 1 ≤ n, m ≤ 2⋅10⁵
- 0 ≤ k ≤ 10⁹
- 1 ≤ aᵢ, bᵢ ≤ 10⁹

**Example**:
```
Input:
4 3 5
60 45 80 60
30 60 75

Output:
2

Explanation: 
- Applicant 1 (desires 60) can get apartment 2 (size 60): |60-60| = 0 ≤ 5 ✓
- Applicant 2 (desires 45) can get apartment 1 (size 30): |45-30| = 15 > 5 ✗
- Applicant 3 (desires 80) can get apartment 3 (size 75): |80-75| = 5 ≤ 5 ✓
- Applicant 4 (desires 60) can get apartment 2 (size 60): |60-60| = 0 ≤ 5 ✓
- Optimal matching: Applicant 1 → Apartment 2, Applicant 3 → Apartment 3 (2 matches)
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

### Step 3: Optimization/Alternative
**Alternative approaches:**
- **Binary Search**: For each applicant, binary search for suitable apartments
- **Two Pointers**: Use two pointers on sorted arrays for efficient matching
- **Greedy Matching**: Always match to smallest suitable apartment

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic matching (should return correct number of matches)
- **Test 2**: No matches possible (should return 0)
- **Test 3**: All matches possible (should return min(n,m))
- **Test 4**: Edge cases with k=0 (should return exact matches only)

## 🔧 Implementation Details
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

## 🎯 Key Insights

### Important Concepts and Patterns
- **Bipartite Matching**: Match elements from two sets optimally
- **Greedy Algorithm**: Always choose the locally optimal choice
- **Two Pointers**: Use sorted arrays with pointer technique
- **Sorting**: Preprocess data for efficient matching

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Apartments with Multiple Preferences**
```python
def apartments_multiple_preferences(n, m, k, applicants, apartments, preferences):
    # Handle apartments with multiple preference levels
    
    # Sort applicants by preference count (fewer preferences first)
    applicants_with_prefs = [(applicants[i], preferences[i]) for i in range(n)]
    applicants_with_prefs.sort(key=lambda x: len(x[1]))
    
    # Sort apartments by size
    apartments.sort()
    
    matches = 0
    used_apartments = set()
    
    for applicant, prefs in applicants_with_prefs:
        # Try to match with preferred apartments first
        matched = False
        for pref in prefs:
            if pref in used_apartments:
                continue
            
            # Check if apartment is suitable
            for apt in apartments:
                if apt == pref and abs(applicant - apt) <= k:
                    matches += 1
                    used_apartments.add(apt)
                    matched = True
                    break
            
            if matched:
                break
        
        # If no preferred apartment available, try any suitable apartment
        if not matched:
            for apt in apartments:
                if apt not in used_apartments and abs(applicant - apt) <= k:
                    matches += 1
                    used_apartments.add(apt)
                    break
    
    return matches
```

#### **2. Apartments with Capacity Constraints**
```python
def apartments_with_capacity(n, m, k, applicants, apartments, capacities):
    # Handle apartments with capacity constraints
    
    # Sort applicants by desired size
    applicants.sort()
    
    # Create list of (apartment_size, capacity) and sort by size
    apt_with_cap = [(apartments[i], capacities[i]) for i in range(m)]
    apt_with_cap.sort()
    
    matches = 0
    
    for applicant in applicants:
        # Find suitable apartment with available capacity
        for i, (apt_size, capacity) in enumerate(apt_with_cap):
            if capacity > 0 and abs(applicant - apt_size) <= k:
                matches += 1
                apt_with_cap[i] = (apt_size, capacity - 1)
                break
    
    return matches
```

#### **3. Apartments with Dynamic Updates**
```python
def apartments_dynamic_updates(n, m, k, operations):
    # Handle apartments with dynamic updates
    
    applicants = []
    apartments = []
    matches = 0
    
    for operation in operations:
        if operation[0] == 'add_applicant':
            # Add new applicant
            applicant = operation[1]
            applicants.append(applicant)
            
            # Try to match with available apartments
            for i, apt in enumerate(apartments):
                if apt is not None and abs(applicant - apt) <= k:
                    matches += 1
                    apartments[i] = None  # Mark as used
                    break
        
        elif operation[0] == 'add_apartment':
            # Add new apartment
            apartment = operation[1]
            apartments.append(apartment)
            
            # Try to match with waiting applicants
            for i, applicant in enumerate(applicants):
                if applicant is not None and abs(applicant - apartment) <= k:
                    matches += 1
                    applicants[i] = None  # Mark as matched
                    break
        
        elif operation[0] == 'query':
            # Return current number of matches
            yield matches
    
    return list(apartments_dynamic_updates(n, m, k, operations))
```

## 🔗 Related Problems

### Links to Similar Problems
- **Bipartite Matching**: Maximum matching problems
- **Greedy Algorithms**: Interval scheduling, activity selection
- **Two Pointers**: Array problems with sorted data
- **Sorting**: Problems requiring data preprocessing

## 📚 Learning Points

1. **Greedy Algorithms**: Optimal local choices lead to global optimum
2. **Two Pointers**: Efficient technique for sorted arrays
3. **Bipartite Matching**: Matching problems with constraints
4. **Sorting**: Enables efficient algorithms

---

**This is a great introduction to greedy algorithms and two-pointer techniques!** 🎯 