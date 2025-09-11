---
layout: simple
title: "Playlist"
permalink: /problem_soulutions/sorting_and_searching/playlist_analysis
---

# Playlist

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of sliding window technique and its applications
- Apply two-pointer technique for efficient subarray processing
- Implement efficient solutions for finding longest subarrays with unique elements
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in sliding window problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sliding window technique, two-pointer technique, hash maps, set operations
- **Data Structures**: Arrays, hash maps, sets, two pointers
- **Mathematical Concepts**: Subarray properties, unique element counting
- **Programming Skills**: Algorithm implementation, complexity analysis, sliding window
- **Related Problems**: Subarray Distinct Values (sliding window), Longest Substring Without Repeating (sliding window), Maximum Subarray Sum (sliding window)

## 📋 Problem Description

You have a playlist with n songs. Each song has a genre. You want to find the longest continuous sequence of songs where no song genre is repeated.

Find the length of the longest subarray where all elements are distinct.

**Input**: 
- First line: integer n (number of songs)
- Second line: n integers a[1], a[2], ..., a[n] (genres of songs)

**Output**: 
- Print one integer: the length of the longest subarray with all distinct elements

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
8
1 2 1 3 2 1 3 4

Output:
4

Explanation**: 
Songs: [1, 2, 1, 3, 2, 1, 3, 4]

Longest subarray with distinct elements: [1, 3, 2, 1, 3, 4]
- Subarray [1, 3, 2, 1, 3, 4] has length 4
- All elements in this subarray are distinct: 1, 3, 2, 4

Other subarrays:
- [1, 2, 1, 3] has length 4 but contains duplicate 1
- [2, 1, 3, 2] has length 4 but contains duplicate 2
- [1, 3, 2, 1, 3, 4] has length 6 and all elements are distinct ✓
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Subarrays

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays
- **Complete Coverage**: Guaranteed to find the longest subarray with distinct elements
- **Simple Implementation**: Straightforward nested loops approach
- **Inefficient**: Cubic time complexity

**Key Insight**: For each possible subarray, check if all elements are distinct.

**Algorithm**:
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Check if subarray from i to j has all distinct elements
    - Keep track of the maximum length

**Visual Example**:
```
Songs: [1, 2, 1, 3, 2, 1, 3, 4]

Check all subarrays:
- [1]: distinct ✓, length = 1
- [1, 2]: distinct ✓, length = 2
- [1, 2, 1]: duplicate 1 ✗
- [1, 2, 1, 3]: duplicate 1 ✗
- [2]: distinct ✓, length = 1
- [2, 1]: distinct ✓, length = 2
- [2, 1, 3]: distinct ✓, length = 3
- [2, 1, 3, 2]: duplicate 2 ✗
- [1]: distinct ✓, length = 1
- [1, 3]: distinct ✓, length = 2
- [1, 3, 2]: distinct ✓, length = 3
- [1, 3, 2, 1]: duplicate 1 ✗
- [3]: distinct ✓, length = 1
- [3, 2]: distinct ✓, length = 2
- [3, 2, 1]: distinct ✓, length = 3
- [3, 2, 1, 3]: duplicate 3 ✗
- [2]: distinct ✓, length = 1
- [2, 1]: distinct ✓, length = 2
- [2, 1, 3]: distinct ✓, length = 3
- [2, 1, 3, 4]: distinct ✓, length = 4
- [1]: distinct ✓, length = 1
- [1, 3]: distinct ✓, length = 2
- [1, 3, 4]: distinct ✓, length = 3
- [3]: distinct ✓, length = 1
- [3, 4]: distinct ✓, length = 2
- [4]: distinct ✓, length = 1

Maximum length: 4
```

**Implementation**:
```python
def brute_force_playlist(songs):
    """
    Find longest subarray with distinct elements using brute force
    
    Args:
        songs: list of song genres
    
    Returns:
        int: length of longest subarray with distinct elements
    """
    max_length = 0
    
    # Check all possible subarrays
    for i in range(len(songs)):
        for j in range(i, len(songs)):
            # Check if subarray from i to j has all distinct elements
            subarray = songs[i:j+1]
            if len(subarray) == len(set(subarray)):
                max_length = max(max_length, len(subarray))
    
    return max_length

# Example usage
songs = [1, 2, 1, 3, 2, 1, 3, 4]
result = brute_force_playlist(songs)
print(f"Brute force result: {result}")  # Output: 4
```

**Time Complexity**: O(n³) - For each subarray, check distinctness
**Space Complexity**: O(n) - For subarray creation

**Why it's inefficient**: Cubic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Use Hash Set

**Key Insights from Optimized Approach**:
- **Hash Set**: Use a set to efficiently check for duplicates
- **Efficient Checking**: Check distinctness in O(1) time per element
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use a hash set to efficiently check if all elements in a subarray are distinct.

**Algorithm**:
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Use a set to check if subarray from i to j has all distinct elements
    - Keep track of the maximum length

**Visual Example**:
```
Songs: [1, 2, 1, 3, 2, 1, 3, 4]

Check all subarrays with set:
- [1]: set = {1}, distinct ✓, length = 1
- [1, 2]: set = {1, 2}, distinct ✓, length = 2
- [1, 2, 1]: set = {1, 2}, duplicate 1 ✗
- [2]: set = {2}, distinct ✓, length = 1
- [2, 1]: set = {2, 1}, distinct ✓, length = 2
- [2, 1, 3]: set = {2, 1, 3}, distinct ✓, length = 3
- [2, 1, 3, 2]: set = {2, 1, 3}, duplicate 2 ✗
- [1]: set = {1}, distinct ✓, length = 1
- [1, 3]: set = {1, 3}, distinct ✓, length = 2
- [1, 3, 2]: set = {1, 3, 2}, distinct ✓, length = 3
- [1, 3, 2, 1]: set = {1, 3, 2}, duplicate 1 ✗
- [3]: set = {3}, distinct ✓, length = 1
- [3, 2]: set = {3, 2}, distinct ✓, length = 2
- [3, 2, 1]: set = {3, 2, 1}, distinct ✓, length = 3
- [3, 2, 1, 3]: set = {3, 2, 1}, duplicate 3 ✗
- [2]: set = {2}, distinct ✓, length = 1
- [2, 1]: set = {2, 1}, distinct ✓, length = 2
- [2, 1, 3]: set = {2, 1, 3}, distinct ✓, length = 3
- [2, 1, 3, 4]: set = {2, 1, 3, 4}, distinct ✓, length = 4
- [1]: set = {1}, distinct ✓, length = 1
- [1, 3]: set = {1, 3}, distinct ✓, length = 2
- [1, 3, 4]: set = {1, 3, 4}, distinct ✓, length = 3
- [3]: set = {3}, distinct ✓, length = 1
- [3, 4]: set = {3, 4}, distinct ✓, length = 2
- [4]: set = {4}, distinct ✓, length = 1

Maximum length: 4
```

**Implementation**:
```python
def optimized_playlist(songs):
    """
    Find longest subarray with distinct elements using hash set
    
    Args:
        songs: list of song genres
    
    Returns:
        int: length of longest subarray with distinct elements
    """
    max_length = 0
    
    # Check all possible subarrays
    for i in range(len(songs)):
        seen = set()
        for j in range(i, len(songs)):
            if songs[j] in seen:
                break
            seen.add(songs[j])
            max_length = max(max_length, len(seen))
    
    return max_length

# Example usage
songs = [1, 2, 1, 3, 2, 1, 3, 4]
result = optimized_playlist(songs)
print(f"Optimized result: {result}")  # Output: 4
```

**Time Complexity**: O(n²) - For each starting position, check all ending positions
**Space Complexity**: O(n) - For the set

**Why it's better**: Much more efficient than brute force with hash set optimization.

---

### Approach 3: Optimal - Sliding Window Technique

**Key Insights from Optimal Approach**:
- **Sliding Window**: Use two pointers to maintain a window of distinct elements
- **Efficient Processing**: Process each element at most twice
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: No need for nested loops

**Key Insight**: Use sliding window technique with two pointers to efficiently find the longest subarray with distinct elements.

**Algorithm**:
- Use two pointers: left and right
- Expand the window by moving the right pointer
- If a duplicate is found, shrink the window by moving the left pointer
- Keep track of the maximum window size

**Visual Example**:
```
Songs: [1, 2, 1, 3, 2, 1, 3, 4]

Sliding window approach:
- left=0, right=0: window=[1], distinct ✓, length=1
- left=0, right=1: window=[1,2], distinct ✓, length=2
- left=0, right=2: window=[1,2,1], duplicate 1 ✗
  - Move left to 1: window=[2,1], distinct ✓, length=2
- left=1, right=3: window=[2,1,3], distinct ✓, length=3
- left=1, right=4: window=[2,1,3,2], duplicate 2 ✗
  - Move left to 2: window=[1,3,2], distinct ✓, length=3
- left=2, right=5: window=[1,3,2,1], duplicate 1 ✗
  - Move left to 3: window=[3,2,1], distinct ✓, length=3
- left=3, right=6: window=[3,2,1,3], duplicate 3 ✗
  - Move left to 4: window=[2,1,3], distinct ✓, length=3
- left=4, right=7: window=[2,1,3,4], distinct ✓, length=4

Maximum length: 4
```

**Implementation**:
```python
def optimal_playlist(songs):
    """
    Find longest subarray with distinct elements using sliding window
    
    Args:
        songs: list of song genres
    
    Returns:
        int: length of longest subarray with distinct elements
    """
    left = 0
    max_length = 0
    seen = set()
    
    # Use sliding window technique
    for right in range(len(songs)):
        # If current element is already in the window, shrink from left
        while songs[right] in seen:
            seen.remove(songs[left])
            left += 1
        
        # Add current element to the window
        seen.add(songs[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
songs = [1, 2, 1, 3, 2, 1, 3, 4]
result = optimal_playlist(songs)
print(f"Optimal result: {result}")  # Output: 4
```

**Time Complexity**: O(n) - Each element is processed at most twice
**Space Complexity**: O(n) - For the set

**Why it's optimal**: Achieves the best possible time complexity with sliding window technique.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all subarrays |
| Hash Set | O(n²) | O(n) | Use set for efficient checking |
| Sliding Window | O(n) | O(n) | Two-pointer technique |

### Time Complexity
- **Time**: O(n) - Sliding window technique provides optimal time complexity
- **Space**: O(n) - For the set to track seen elements

### Why This Solution Works
- **Sliding Window**: Two pointers efficiently maintain a window of distinct elements
- **Efficient Processing**: Each element is processed at most twice
- **Optimal Algorithm**: Sliding window technique is the standard approach for this problem
- **Optimal Approach**: Sliding window provides the most efficient solution for finding longest subarray with distinct elements
