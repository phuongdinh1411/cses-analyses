# CSES Apartments - Problem Analysis

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