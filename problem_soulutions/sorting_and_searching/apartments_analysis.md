---
layout: simple
title: "Apartments - Maximum Matching with Two Pointers"
permalink: /problem_soulutions/sorting_and_searching/apartments_analysis
---

# Apartments - Maximum Matching with Two Pointers

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the maximum matching problem with size constraints
- Apply two-pointer technique for efficient matching
- Implement greedy algorithms for optimization problems
- Optimize matching algorithms using sorting and two pointers
- Handle edge cases in matching problems (no valid matches, all matches valid)

## 📋 Problem Description

Given n applicants and m apartments, each with a desired size, find the maximum number of applicants that can be assigned to apartments. An applicant can be assigned to an apartment if the apartment size is within their acceptable range [desired_size - k, desired_size + k].

This is a classic maximum matching problem that can be solved efficiently using the two-pointer technique after sorting.

**Input**: 
- First line: three integers n, m, k (number of applicants, apartments, and tolerance)
- Second line: n integers (desired apartment sizes)
- Third line: m integers (available apartment sizes)

**Output**: 
- Print one integer: the maximum number of assignments

**Constraints**:
- 1 ≤ n, m ≤ 2×10⁵
- 0 ≤ k ≤ 10⁹
- 1 ≤ desired_size, apartment_size ≤ 10⁹

**Example**:
```
Input:
4 3 5
60 45 80 60
30 60 75

Output:
2

Explanation**: 
Applicant 1 (desired: 60) can get apartment 2 (size: 60) or apartment 3 (size: 75)
Applicant 2 (desired: 45) can get apartment 1 (size: 30) or apartment 2 (size: 60)
Applicant 3 (desired: 80) can get apartment 3 (size: 75)
Applicant 4 (desired: 60) can get apartment 2 (size: 60) or apartment 3 (size: 75)

Optimal assignment: Applicant 1 → Apartment 2, Applicant 3 → Apartment 3
Total assignments: 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Assignments

**Key Insights from Brute Force Approach**:
- **Exhaustive Matching**: Try all possible ways to assign applicants to apartments
- **Constraint Checking**: For each assignment, check if size constraints are satisfied
- **Maximum Tracking**: Keep track of the maximum number of valid assignments
- **Complete Coverage**: Guaranteed to find the optimal solution

**Key Insight**: Generate all possible assignments and find the one with maximum valid matches.

**Algorithm**:
- Generate all possible combinations of applicant-apartment assignments
- For each combination, check if all assignments satisfy size constraints
- Return the maximum number of valid assignments

**Visual Example**:
```
Applicants: [60, 45, 80, 60], Apartments: [30, 60, 75], k = 5

Try all possible assignments:
1. Assign all to first apartment (30): 
   - 60: [25, 35] ✗ (30 not in range)
   - 45: [40, 50] ✗ (30 not in range)
   - 80: [75, 85] ✗ (30 not in range)
   - 60: [55, 65] ✗ (30 not in range)
   → 0 assignments

2. Assign first to apartment 1, rest to apartment 2:
   - 60 → 30: ✗
   - 45 → 60: ✓ (60 in [40, 50])
   - 80 → 60: ✗
   - 60 → 60: ✓
   → 2 assignments

... (continue for all combinations)

Maximum assignments: 2
```

**Implementation**:
```python
def brute_force_apartments(applicants, apartments, k):
    """
    Find maximum assignments using brute force approach
    
    Args:
        applicants: list of desired sizes
        apartments: list of available apartment sizes
        k: tolerance value
    
    Returns:
        int: maximum number of assignments
    """
    from itertools import permutations
    
    n, m = len(applicants), len(apartments)
    max_assignments = 0
    
    # Try all possible assignments
    for perm in permutations(apartments, min(n, m)):
        assignments = 0
        for i in range(len(perm)):
            desired = applicants[i]
            apartment_size = perm[i]
            if abs(desired - apartment_size) <= k:
                assignments += 1
        max_assignments = max(max_assignments, assignments)
    
    return max_assignments

# Example usage
applicants = [60, 45, 80, 60]
apartments = [30, 60, 75]
k = 5
result = brute_force_apartments(applicants, apartments, k)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(n! × m! × n) - All permutations with validation
**Space Complexity**: O(n + m) - For storing permutations

**Why it's inefficient**: Factorial time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Greedy with Sorting

**Key Insights from Optimized Approach**:
- **Greedy Strategy**: Assign each applicant to the smallest suitable apartment
- **Sorting Benefit**: Sort both lists to enable efficient matching
- **Optimal Greedy Choice**: Always choose the smallest available apartment that satisfies constraints
- **Efficient Matching**: Use two pointers to find suitable apartments

**Key Insight**: Sort both applicants and apartments, then greedily assign each applicant to the smallest suitable apartment.

**Algorithm**:
- Sort applicants and apartments
- For each applicant, find the smallest apartment that satisfies size constraints
- Mark used apartments to avoid double assignment

**Visual Example**:
```
Applicants: [60, 45, 80, 60], Apartments: [30, 60, 75], k = 5

Step 1: Sort
Sorted applicants: [45, 60, 60, 80]
Sorted apartments: [30, 60, 75]

Step 2: Greedy assignment
1. Applicant 45: Find apartment in range [40, 50]
   - Apartment 30: Not in range ✗
   - Apartment 60: Not in range ✗
   - Apartment 75: Not in range ✗
   → No assignment

2. Applicant 60: Find apartment in range [55, 65]
   - Apartment 30: Not in range ✗
   - Apartment 60: In range ✓ → Assign
   → Used apartments: [60]

3. Applicant 60: Find apartment in range [55, 65]
   - Apartment 30: Not in range ✗
   - Apartment 60: Already used ✗
   - Apartment 75: Not in range ✗
   → No assignment

4. Applicant 80: Find apartment in range [75, 85]
   - Apartment 30: Not in range ✗
   - Apartment 60: Already used ✗
   - Apartment 75: In range ✓ → Assign
   → Used apartments: [60, 75]

Total assignments: 2
```

**Implementation**:
```python
def optimized_apartments(applicants, apartments, k):
    """
    Find maximum assignments using greedy approach
    
    Args:
        applicants: list of desired sizes
        apartments: list of available apartment sizes
        k: tolerance value
    
    Returns:
        int: maximum number of assignments
    """
    # Sort both lists
    applicants.sort()
    apartments.sort()
    
    assignments = 0
    apartment_index = 0
    
    for desired in applicants:
        # Find smallest suitable apartment
        while apartment_index < len(apartments):
            if abs(desired - apartments[apartment_index]) <= k:
                assignments += 1
                apartment_index += 1
                break
            elif apartments[apartment_index] < desired - k:
                apartment_index += 1
            else:
                break
    
    return assignments

# Example usage
applicants = [60, 45, 80, 60]
apartments = [30, 60, 75]
k = 5
result = optimized_apartments(applicants, apartments, k)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n + m log m) - Sorting dominates
**Space Complexity**: O(1) - If sorting in-place

**Why it's better**: Much more efficient than brute force, but can be further optimized.

---

### Approach 3: Optimal - Two Pointer Technique

**Key Insights from Optimal Approach**:
- **Two Pointers**: Use two pointers to efficiently match applicants with apartments
- **Sorted Processing**: Process applicants and apartments in sorted order
- **Optimal Matching**: Always match with the smallest suitable apartment
- **Linear Complexity**: Achieve linear time complexity after sorting

**Key Insight**: Use two pointers to efficiently find the optimal matching between sorted applicants and apartments.

**Algorithm**:
- Sort both applicants and apartments
- Use two pointers: one for applicants, one for apartments
- For each applicant, find the smallest suitable apartment
- Move pointers efficiently to avoid redundant checks

**Visual Example**:
```
Applicants: [60, 45, 80, 60], Apartments: [30, 60, 75], k = 5

Step 1: Sort
Sorted applicants: [45, 60, 60, 80]
Sorted apartments: [30, 60, 75]

Step 2: Two pointer matching
Applicant pointer: 0, Apartment pointer: 0

1. Applicant 45 (range [40, 50]):
   - Apartment 30: 30 < 40, move apartment pointer
   - Apartment 60: 60 > 50, no match
   → Move applicant pointer

2. Applicant 60 (range [55, 65]):
   - Apartment 60: 60 in [55, 65] ✓ → Match!
   → Move both pointers

3. Applicant 60 (range [55, 65]):
   - Apartment 75: 75 > 65, no match
   → Move applicant pointer

4. Applicant 80 (range [75, 85]):
   - Apartment 75: 75 in [75, 85] ✓ → Match!
   → Move both pointers

Total matches: 2
```

**Implementation**:
```python
def optimal_apartments(applicants, apartments, k):
    """
    Find maximum assignments using two pointer technique
    
    Args:
        applicants: list of desired sizes
        apartments: list of available apartment sizes
        k: tolerance value
    
    Returns:
        int: maximum number of assignments
    """
    # Sort both lists
    applicants.sort()
    apartments.sort()
    
    assignments = 0
    i = j = 0  # Two pointers
    
    while i < len(applicants) and j < len(apartments):
        desired = applicants[i]
        apartment_size = apartments[j]
        
        # Check if apartment is suitable
        if abs(desired - apartment_size) <= k:
            assignments += 1
            i += 1  # Move to next applicant
            j += 1  # Move to next apartment
        elif apartment_size < desired - k:
            j += 1  # Apartment too small, try next
        else:
            i += 1  # Apartment too large, try next applicant
    
    return assignments

# Example usage
applicants = [60, 45, 80, 60]
apartments = [30, 60, 75]
k = 5
result = optimal_apartments(applicants, apartments, k)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n + m log m) - Sorting dominates, matching is O(n + m)
**Space Complexity**: O(1) - If sorting in-place

**Why it's optimal**: Efficient two-pointer technique with optimal time complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × m! × n) | O(n + m) | Try all assignments |
| Greedy with Sorting | O(n log n + m log m) | O(1) | Greedy matching |
| Two Pointers | O(n log n + m log m) | O(1) | Efficient matching |

### Time Complexity
- **Time**: O(n log n + m log m) - Sorting dominates, matching is linear
- **Space**: O(1) - If sorting in-place

### Why This Solution Works
- **Greedy Choice**: Always choose the smallest suitable apartment
- **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
- **Two Pointer Efficiency**: Avoid redundant comparisons
- **Optimal Approach**: Two-pointer technique provides best practical performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Apartments with Multiple Preferences
**Problem**: Each applicant has multiple apartment size preferences with different priorities.

**Link**: [CSES Problem Set - Apartments Multiple Preferences](https://cses.fi/problemset/task/apartments_multiple_preferences)

```python
def apartments_multiple_preferences(applicants, apartments, k):
    """
    Find maximum assignments with multiple preferences per applicant
    """
    # Sort apartments by size
    apartments.sort()
    
    # Create preference lists for each applicant
    assignments = 0
    used_apartments = set()
    
    # Sort applicants by number of preferences (fewer preferences first)
    applicants.sort(key=lambda x: len(x['preferences']))
    
    for applicant in applicants:
        for preferred_size in applicant['preferences']:
            # Find suitable apartment using binary search
            left, right = 0, len(apartments) - 1
            best_apartment = -1
            
            while left <= right:
                mid = (left + right) // 2
                if apartments[mid] >= preferred_size - k:
                    if apartments[mid] <= preferred_size + k:
                        best_apartment = mid
                    right = mid - 1
                else:
                    left = mid + 1
            
            # Assign if found and not used
            if best_apartment != -1 and best_apartment not in used_apartments:
                used_apartments.add(best_apartment)
                assignments += 1
                break
    
    return assignments
```

### Variation 2: Apartments with Cost Constraints
**Problem**: Each apartment has a cost, and applicants have budget constraints.

**Link**: [CSES Problem Set - Apartments Cost Constraints](https://cses.fi/problemset/task/apartments_cost_constraints)

```python
def apartments_cost_constraints(applicants, apartments, k):
    """
    Find maximum assignments considering cost constraints
    """
    # Sort apartments by cost (ascending)
    apartments.sort(key=lambda x: x['cost'])
    
    assignments = 0
    used_apartments = set()
    
    # Sort applicants by budget (ascending)
    applicants.sort(key=lambda x: x['budget'])
    
    for applicant in applicants:
        for apartment in apartments:
            if (apartment['id'] not in used_apartments and
                abs(apartment['size'] - applicant['desired_size']) <= k and
                apartment['cost'] <= applicant['budget']):
                
                used_apartments.add(apartment['id'])
                assignments += 1
                break
    
    return assignments
```

### Variation 3: Apartments with Time Windows
**Problem**: Apartments are available only during specific time windows, and applicants have availability periods.

**Link**: [CSES Problem Set - Apartments Time Windows](https://cses.fi/problemset/task/apartments_time_windows)

```python
def apartments_time_windows(applicants, apartments, k):
    """
    Find maximum assignments considering time window constraints
    """
    # Create events for apartment availability and applicant requests
    events = []
    
    for apartment in apartments:
        events.append((apartment['start_time'], 'apartment_available', apartment))
        events.append((apartment['end_time'], 'apartment_unavailable', apartment))
    
    for applicant in applicants:
        events.append((applicant['arrival_time'], 'applicant_arrives', applicant))
    
    # Sort events by time
    events.sort()
    
    available_apartments = []
    assignments = 0
    
    for time, event_type, data in events:
        if event_type == 'apartment_available':
            available_apartments.append(data)
            available_apartments.sort(key=lambda x: x['size'])
        
        elif event_type == 'apartment_unavailable':
            if data in available_apartments:
                available_apartments.remove(data)
        
        elif event_type == 'applicant_arrives':
            # Find suitable apartment using two pointers
            for apartment in available_apartments:
                if abs(apartment['size'] - data['desired_size']) <= k:
                    available_apartments.remove(apartment)
                    assignments += 1
                    break
    
    return assignments
```

## Problem Variations

### **Variation 1: Apartments with Multiple Criteria**
**Problem**: Assign apartments to applicants considering both size and price constraints.

**Approach**: Sort by multiple criteria and use advanced matching algorithms.

```python
def apartments_multiple_criteria(apartments, applicants, size_tolerance, price_tolerance):
    """
    Assign apartments considering both size and price constraints.
    
    Args:
        apartments: List of (size, price) tuples
        applicants: List of (desired_size, max_price) tuples
        size_tolerance: Maximum size difference allowed
        price_tolerance: Maximum price difference allowed
    
    Returns:
        Maximum number of assignments
    """
    # Sort apartments by size, then by price
    apartments.sort(key=lambda x: (x[0], x[1]))
    applicants.sort(key=lambda x: (x[0], x[1]))
    
    assignments = 0
    used_apartments = set()
    
    for desired_size, max_price in applicants:
        for i, (size, price) in enumerate(apartments):
            if i in used_apartments:
                continue
            
            size_diff = abs(size - desired_size)
            price_diff = abs(price - max_price)
            
            if size_diff <= size_tolerance and price_diff <= price_tolerance:
                used_apartments.add(i)
                assignments += 1
                break
    
    return assignments

# Example usage
apartments = [(50, 1000), (60, 1200), (70, 1100), (80, 1300)]
applicants = [(55, 1150), (65, 1250), (75, 1050)]
assignments = apartments_multiple_criteria(apartments, applicants, 10, 100)
print(f"Maximum assignments: {assignments}")
```

### **Variation 2: Apartments with Dynamic Updates**
**Problem**: Handle dynamic apartment availability and applicant arrivals.

**Approach**: Use balanced binary search trees for efficient updates and queries.

```python
import bisect
from collections import defaultdict

class DynamicApartmentSystem:
    def __init__(self, k):
        self.k = k
        self.available_apartments = []  # Sorted list
        self.assignments = 0
    
    def add_apartment(self, size):
        """Add a new apartment to the system."""
        bisect.insort(self.available_apartments, size)
    
    def remove_apartment(self, size):
        """Remove an apartment from the system."""
        if size in self.available_apartments:
            self.available_apartments.remove(size)
    
    def assign_apartment(self, desired_size):
        """Try to assign an apartment to an applicant."""
        # Find the best apartment using binary search
        left = 0
        right = len(self.available_apartments)
        best_apartment = None
        best_diff = float('inf')
        
        # Binary search for the closest apartment
        while left < right:
            mid = (left + right) // 2
            size = self.available_apartments[mid]
            diff = abs(size - desired_size)
            
            if diff <= self.k:
                if diff < best_diff:
                    best_diff = diff
                    best_apartment = size
                
                # Try to find a better match
                if size < desired_size:
                    left = mid + 1
                else:
                    right = mid
            elif size < desired_size:
                left = mid + 1
            else:
                right = mid
        
        if best_apartment is not None:
            self.available_apartments.remove(best_apartment)
            self.assignments += 1
            return True
        
        return False
    
    def get_assignments(self):
        """Get the total number of assignments made."""
        return self.assignments

# Example usage
system = DynamicApartmentSystem(5)
system.add_apartment(50)
system.add_apartment(60)
system.add_apartment(70)

print(system.assign_apartment(55))  # True
print(system.assign_apartment(65))  # True
print(system.assign_apartment(80))  # False
print(f"Total assignments: {system.get_assignments()}")
```

### **Variation 3: Apartments with Constraints**
**Problem**: Assign apartments with additional constraints like location preferences.

**Approach**: Use constraint satisfaction with backtracking or advanced matching algorithms.

```python
def apartments_with_constraints(apartments, applicants, size_tolerance, constraints):
    """
    Assign apartments with additional constraints.
    
    Args:
        apartments: List of (size, location, amenities) tuples
        applicants: List of (desired_size, preferred_locations, required_amenities) tuples
        size_tolerance: Maximum size difference allowed
        constraints: Dictionary of additional constraints
    
    Returns:
        List of (applicant_index, apartment_index) assignments
    """
    n_applicants = len(applicants)
    n_apartments = len(apartments)
    
    # Create compatibility matrix
    compatibility = [[False] * n_apartments for _ in range(n_applicants)]
    
    for i, (desired_size, preferred_locations, required_amenities) in enumerate(applicants):
        for j, (size, location, amenities) in enumerate(apartments):
            # Check size constraint
            if abs(size - desired_size) > size_tolerance:
                continue
            
            # Check location preference
            if preferred_locations and location not in preferred_locations:
                continue
            
            # Check required amenities
            if required_amenities and not all(amenity in amenities for amenity in required_amenities):
                continue
            
            compatibility[i][j] = True
    
    # Use maximum bipartite matching
    def dfs(applicant, visited, match):
        for apartment in range(n_apartments):
            if compatibility[applicant][apartment] and apartment not in visited:
                visited.add(apartment)
                if match[apartment] == -1 or dfs(match[apartment], visited, match):
                    match[apartment] = applicant
                    return True
        return False
    
    # Find maximum matching
    match = [-1] * n_apartments
    assignments = []
    
    for applicant in range(n_applicants):
        visited = set()
        if dfs(applicant, visited, match):
            apartment = match.index(applicant)
            assignments.append((applicant, apartment))
    
    return assignments

# Example usage
apartments = [
    (50, "downtown", ["parking", "gym"]),
    (60, "suburb", ["parking"]),
    (70, "downtown", ["gym", "pool"]),
    (80, "suburb", ["parking", "gym", "pool"])
]

applicants = [
    (55, ["downtown"], ["parking"]),
    (65, ["suburb", "downtown"], ["gym"]),
    (75, ["downtown"], ["gym", "pool"])
]

assignments = apartments_with_constraints(apartments, applicants, 10, {})
print(f"Assignments: {assignments}")
```

### Related Problems

#### **CSES Problems**
- [Apartments](https://cses.fi/problemset/task/1084) - Basic apartment assignment problem
- [Ferris Wheel](https://cses.fi/problemset/task/1090) - Similar two-pointer problem
- [Stick Lengths](https://cses.fi/problemset/task/1074) - Optimization with sorting

#### **LeetCode Problems**
- [Two Sum](https://leetcode.com/problems/two-sum/) - Find pairs with target sum
- [3Sum](https://leetcode.com/problems/3sum/) - Find triplets with zero sum
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) - Two-pointer optimization
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) - Two-pointer water trapping

#### **Problem Categories**
- **Two Pointers**: Efficient array processing, sorted array algorithms, matching problems
- **Greedy Algorithms**: Optimal local choices, sorting-based optimization, assignment problems
- **Sorting**: Array sorting, binary search, efficient searching algorithms
- **Algorithm Design**: Two-pointer techniques, greedy strategies, optimization algorithms