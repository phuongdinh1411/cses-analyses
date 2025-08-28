---
layout: simple
title: "Apartments"permalink: /problem_soulutions/sorting_and_searching/cses_apartments_analysis
---


# Apartments

## Problem Statement
There are n applicants and m free apartments. Your task is to distribute the apartments so that as many applicants as possible will get an apartment.

Each applicant has a desired apartment size, and they will accept any apartment whose size is at least ai−k and at most ai+k.

### Input
The first input line has three integers n, m, and k: the number of applicants, the number of apartments, and the maximum allowed difference.

The next line contains n integers a1,a2,…,an: the desired apartment size of each applicant.

The last line contains m integers b1,b2,…,bm: the size of each apartment.

### Output
Print one integer: the number of applicants who will get an apartment.

### Constraints
- 1 ≤ n,m ≤ 2⋅10^5
- 0 ≤ k ≤ 10^9
- 1 ≤ ai,bi ≤ 10^9

### Example
```
Input:
4 3 5
60 45 80 60
30 60 75

Output:
2
```

## Solution Progression

### Approach 1: Brute Force - O(m^n)
**Description**: Try all possible combinations of assignments using backtracking.

```python
def apartments_brute_force(applicants, apartments, k):
    n, m = len(applicants), len(apartments)
    max_matches = 0
    
    def backtrack(applicant_idx, used_apartments, current_matches):
        nonlocal max_matches
        
        if applicant_idx == n:
            max_matches = max(max_matches, current_matches)
            return
        
        # Try to assign current applicant to each available apartment
        for apt_idx in range(m):
            if not used_apartments[apt_idx]:
                # Check if apartment is acceptable
                if abs(applicants[applicant_idx] - apartments[apt_idx]) <= k:
                    used_apartments[apt_idx] = True
                    backtrack(applicant_idx + 1, used_apartments, current_matches + 1)
                    used_apartments[apt_idx] = False
        
        # Skip current applicant
        backtrack(applicant_idx + 1, used_apartments, current_matches)
    
    backtrack(0, [False] * m, 0)
    return max_matches
```
**Why this is inefficient**: We're trying all possible combinations, which is exponential. For each applicant, we have m choices, leading to O(m^n) complexity.

### Improvement 1: Greedy with Sorting - O(n log n + m log m)
**Description**: Sort both arrays and use a greedy approach to match applicants with the smallest suitable apartment.

```python
def apartments_greedy_sorting(applicants, apartments, k):
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

**Why this improvement works**: By sorting and always choosing the smallest suitable apartment, we ensure that we don't waste larger apartments on applicants who could have taken smaller ones. This greedy strategy maximizes future matching opportunities.

### Improvement 2: Two Pointers Optimization - O(n log n + m log m)
**Description**: Use two pointers to efficiently match applicants and apartments in sorted order.

```python
def apartments_two_pointers(applicants, apartments, k):
    applicants.sort()
    apartments.sort()
    
    i = j = matches = 0
    
    while i < len(applicants) and j < len(apartments):
        # Check if current apartment matches current applicant
        if abs(applicants[i] - apartments[j]) <= k:
            matches += 1
            i += 1
            j += 1
        elif applicants[i] < apartments[j]:
            # Applicant wants smaller apartment, move to next applicant
            i += 1
        else:
            # Apartment is too small, move to next apartment
            j += 1
    
    return matches
```

**Why this improvement works**: Two pointers allow us to process both arrays in a single pass after sorting. We move the pointer that would give us the best chance of future matches.

### Alternative: Binary Search Approach - O(m log m + n log m)
**Description**: Sort apartments and use binary search to find suitable apartments for each applicant.

```python
import bisect

def apartments_binary_search(applicants, apartments, k):
    apartments.sort()
    used = [False] * len(apartments)
    matches = 0
    
    for applicant in applicants:
        # Find range of acceptable apartments
        min_size = applicant - k
        max_size = applicant + k
        
        # Binary search for leftmost apartment >= min_size
        left = bisect.bisect_left(apartments, min_size)
        
        # Find suitable apartment
        while left < len(apartments) and apartments[left] <= max_size:
            if not used[left]:
                used[left] = True
                matches += 1
                break
            left += 1
    
    return matches
```

**Why this works**: Binary search reduces the search time for suitable apartments from O(m) to O(log m) per applicant.

## Final Optimal Solution

```python
n, m, k = map(int, input().split())
applicants = list(map(int, input().split()))
apartments = list(map(int, input().split()))

# Sort both arrays
applicants.sort()
apartments.sort()

# Two pointers approach
i = j = matches = 0
while i < n and j < m:
    if abs(applicants[i] - apartments[j]) <= k:
        matches += 1
        i += 1
        j += 1
    elif applicants[i] < apartments[j]:
        i += 1
    else:
        j += 1

print(matches)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(m^n) | O(n) | Try all combinations |
| Greedy + Sorting | O(n log n + m log m) | O(1) | Sort and match greedily |
| Two Pointers | O(n log n + m log m) | O(1) | Single pass after sorting |
| Binary Search | O(m log m + n log m) | O(m) | Binary search for matches |

## Key Insights for Other Problems

### 1. **Greedy Matching Strategy**
**Principle**: Always match with the smallest/best available option to maximize future opportunities.
**Applicable to**:
- Resource allocation problems
- Scheduling problems
- Matching problems
- Assignment problems

**Example Problems**:
- Activity selection
- Job scheduling
- Room allocation
- Task assignment

### 2. **Two Pointers Technique**
**Principle**: Use two pointers to process two sorted arrays simultaneously.
**Applicable to**:
- Merging sorted arrays
- Finding pairs in sorted arrays
- Range-based problems
- Matching problems

**Example Problems**:
- Merge sorted arrays
- Two sum in sorted array
- Intersection of arrays
- Container with most water

### 3. **Sorting for Efficiency**
**Principle**: Sort data to enable efficient matching or searching.
**Applicable to**:
- Matching problems
- Range queries
- Binary search applications
- Greedy algorithms

**Example Problems**:
- Meeting rooms
- Merge intervals
- Find pairs with given sum
- Closest pair of points

### 4. **Binary Search for Range Matching**
**Principle**: Use binary search to find elements within a range efficiently.
**Applicable to**:
- Range-based queries
- Finding closest values
- Matching within constraints
- Optimization problems

**Example Problems**:
- Find first/last occurrence
- Search in rotated array
- Find peak element
- Capacity planning

## Notable Techniques

### 1. **Two Pointers Pattern**
```python
# Common pattern for matching
left, right = 0, len(arr2) - 1
while left < len(arr1) and right >= 0:
    if condition(arr1[left], arr2[right]):
        # Process match
        left += 1
        right -= 1
    elif arr1[left] < arr2[right]:
        left += 1
    else:
        right -= 1
```

### 2. **Greedy Matching**
```python
# Sort and match greedily
data.sort()
matches = 0
for item in data:
    if can_match(item):
        matches += 1
        # Update available resources
```

### 3. **Binary Search for Ranges**
```python
# Find elements in range [min_val, max_val]
left = bisect.bisect_left(arr, min_val)
right = bisect.bisect_right(arr, max_val)
# Elements in range: arr[left:right]
```

## Edge Cases to Remember

1. **No matches possible**: k = 0 and no exact matches
2. **All can match**: k is very large
3. **More applicants than apartments**: n > m
4. **More apartments than applicants**: m > n
5. **Same desired sizes**: Multiple applicants want same size

## Problem-Solving Framework

1. **Identify the matching nature**: This is a bipartite matching problem
2. **Consider greedy approach**: Always match with best available option
3. **Sort for efficiency**: Enable linear-time matching
4. **Use two pointers**: Process both arrays simultaneously
5. **Handle edge cases**: Consider boundary conditions

---

*This analysis shows how to systematically improve from exponential brute force to optimal greedy solution and extracts reusable insights for matching problems.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Matching**
**Problem**: Each assignment has a weight. Find maximum weight matching.
```python
def weighted_apartment_matching(applicants, apartments, k, weights):
    # weights[i][j] = weight of assigning applicant i to apartment j
    n, m = len(applicants), len(apartments)
    
    # Create bipartite graph and use Hungarian algorithm
    # For simplicity, use greedy approach with weights
    matches = []
    used_apartments = set()
    
    for i, applicant in enumerate(applicants):
        best_apartment = None
        best_weight = -1
        
        for j, apartment in enumerate(apartments):
            if j not in used_apartments and abs(applicant - apartment) <= k:
                if weights[i][j] > best_weight:
                    best_weight = weights[i][j]
                    best_apartment = j
        
        if best_apartment is not None:
            matches.append((i, best_apartment, best_weight))
            used_apartments.add(best_apartment)
    
    return matches
```

#### **Variation 2: Multiple Preferences**
**Problem**: Each applicant has multiple acceptable ranges. Find maximum matching.
```python
def multiple_preferences_matching(applicants_prefs, apartments, k):
    # applicants_prefs[i] = list of acceptable ranges for applicant i
    n, m = len(applicants_prefs), len(apartments)
    matches = 0
    used_apartments = set()
    
    for i, preferences in enumerate(applicants_prefs):
        for low, high in preferences:
            # Find smallest apartment in this range
            for j, apartment in enumerate(apartments):
                if j not in used_apartments and low <= apartment <= high:
                    matches += 1
                    used_apartments.add(j)
                    break
    
    return matches
```

#### **Variation 3: Dynamic Apartment Availability**
**Problem**: Apartments become available over time. Find optimal assignment.
```python
def dynamic_apartment_matching(applicants, apartment_schedule, k):
    # apartment_schedule[j] = (size, available_time) for apartment j
    n = len(applicants)
    matches = 0
    used_apartments = set()
    
    # Sort apartments by availability time
    apartment_schedule.sort(key=lambda x: x[1])
    
    for time, (size, available_time) in enumerate(apartment_schedule):
        if available_time <= time:
            # Find best applicant for this apartment
            best_applicant = None
            best_diff = float('inf')
            
            for i, applicant in enumerate(applicants):
                if i not in used_apartments and abs(applicant - size) <= k:
                    diff = abs(applicant - size)
                    if diff < best_diff:
                        best_diff = diff
                        best_applicant = i
            
            if best_applicant is not None:
                matches += 1
                used_apartments.add(best_applicant)
    
    return matches
```

#### **Variation 4: Capacity Constraints**
**Problem**: Each apartment can accommodate multiple applicants. Find maximum assignment.
```python
def capacity_constrained_matching(applicants, apartments, capacities, k):
    # capacities[j] = number of applicants apartment j can accommodate
    n, m = len(applicants), len(apartments)
    matches = 0
    apartment_usage = [0] * m
    
    applicants.sort()
    apartments_with_capacity = [(apartments[i], i) for i in range(m)]
    apartments_with_capacity.sort()
    
    for applicant in applicants:
        for size, apt_idx in apartments_with_capacity:
            if (apartment_usage[apt_idx] < capacities[apt_idx] and 
                abs(applicant - size) <= k):
                matches += 1
                apartment_usage[apt_idx] += 1
                break
    
    return matches
```

#### **Variation 5: Fair Assignment**
**Problem**: Assign apartments fairly, minimizing maximum dissatisfaction.
```python
def fair_apartment_assignment(applicants, apartments, k):
    n, m = len(applicants), len(apartments)
    
    # Binary search on maximum dissatisfaction
    def can_assign(max_dissatisfaction):
        # Try to assign all applicants with max dissatisfaction limit
        used_apartments = set()
        assigned = 0
        
        for applicant in applicants:
            for j, apartment in enumerate(apartments):
                if j not in used_apartments and abs(applicant - apartment) <= max_dissatisfaction:
                    used_apartments.add(j)
                    assigned += 1
                    break
        
        return assigned == n
    
    # Binary search
    left, right = 0, max(max(apartments), max(applicants))
    while left < right:
        mid = (left + right) // 2
        if can_assign(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### 🔗 **Related Problems & Concepts**

#### **1. Matching Problems**
- **Bipartite Matching**: Maximum matching in bipartite graphs
- **Weighted Matching**: Maximum weight bipartite matching
- **Stable Marriage**: Stable matching problem
- **Assignment Problem**: Hungarian algorithm applications

#### **2. Greedy Algorithm Problems**
- **Activity Selection**: Select maximum activities
- **Interval Scheduling**: Schedule non-overlapping intervals
- **Fractional Knapsack**: Fill knapsack optimally
- **Huffman Coding**: Build optimal prefix codes

#### **3. Sorting and Searching Problems**
- **Two Pointers**: Efficient array processing
- **Binary Search**: Find optimal solutions
- **Custom Sorting**: Sort based on multiple criteria
- **Range Queries**: Query ranges efficiently

#### **4. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Network Flow**: Maximum flow applications
- **Combinatorial Optimization**: Discrete optimization
- **Approximation Algorithms**: Find approximate solutions

#### **5. Resource Allocation Problems**
- **Job Scheduling**: Assign jobs to machines
- **Resource Management**: Allocate limited resources
- **Load Balancing**: Distribute load evenly
- **Capacity Planning**: Plan resource capacity

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    applicants = list(map(int, input().split()))
    apartments = list(map(int, input().split()))
    
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
    
    print(matches)
```

#### **2. Range Queries**
```python
# Precompute matching possibilities for different ranges
def precompute_matching_ranges(applicants, apartments, k):
    n, m = len(applicants), len(apartments)
    matching_matrix = [[False] * m for _ in range(n)]
    
    for i, applicant in enumerate(applicants):
        for j, apartment in enumerate(apartments):
            if abs(applicant - apartment) <= k:
                matching_matrix[i][j] = True
    
    return matching_matrix

# Answer queries about matching possibilities
def matching_query(matching_matrix, applicant_range, apartment_range):
    count = 0
    for i in applicant_range:
        for j in apartment_range:
            if matching_matrix[i][j]:
                count += 1
    return count
```

#### **3. Interactive Problems**
```python
# Interactive apartment assignment game
def interactive_apartment_assignment():
    n = int(input("Enter number of applicants: "))
    m = int(input("Enter number of apartments: "))
    k = int(input("Enter tolerance k: "))
    
    applicants = []
    for i in range(n):
        pref = int(input(f"Enter preference for applicant {i+1}: "))
        applicants.append(pref)
    
    apartments = []
    for i in range(m):
        size = int(input(f"Enter size for apartment {i+1}: "))
        apartments.append(size)
    
    print(f"Applicants: {applicants}")
    print(f"Apartments: {apartments}")
    
    # Solve using greedy approach
    applicants.sort()
    apartments.sort()
    
    matches = 0
    apt_idx = 0
    
    for applicant in applicants:
        while apt_idx < m and apartments[apt_idx] < applicant - k:
            apt_idx += 1
        
        if apt_idx < m and apartments[apt_idx] <= applicant + k:
            print(f"Assigned applicant {applicant} to apartment {apartments[apt_idx]}")
            matches += 1
            apt_idx += 1
        else:
            print(f"Could not assign applicant {applicant}")
    
    print(f"Total matches: {matches}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Bipartite Graphs**: Model as bipartite matching
- **Network Flow**: Maximum flow formulation
- **Matching Theory**: Hall's marriage theorem
- **Graph Algorithms**: BFS/DFS for matching

#### **2. Optimization Theory**
- **Linear Programming**: Formulate as LP problem
- **Duality**: Study dual problems
- **Integer Programming**: Discrete optimization
- **Approximation**: Find approximate solutions

#### **3. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Correctness Proofs**: Prove algorithm correctness
- **Optimality**: Prove optimality of solutions
- **Lower Bounds**: Establish problem lower bounds

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Hungarian Algorithm**: Optimal assignment algorithm
- **Ford-Fulkerson**: Maximum flow algorithm
- **Hopcroft-Karp**: Bipartite matching algorithm
- **Greedy Algorithms**: Local optimal choices

#### **2. Mathematical Concepts**
- **Graph Theory**: Bipartite graphs and matching
- **Linear Programming**: Optimization formulations
- **Combinatorics**: Counting and arrangement
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Two Pointers**: Efficient array processing
- **Sorting**: Custom sorting techniques
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies

---

*This analysis demonstrates efficient matching algorithms and shows various extensions for resource allocation problems.* 