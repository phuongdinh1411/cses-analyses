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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Playlist with Range Queries
**Problem**: Answer multiple queries about longest subarray with distinct elements in different ranges.

**Link**: [CSES Problem Set - Playlist Range Queries](https://cses.fi/problemset/task/playlist_range)

```python
def playlist_range_queries(songs, queries):
    """
    Answer range queries about longest subarray with distinct elements
    """
    results = []
    
    for query in queries:
        left, right = query['left'], query['right']
        
        # Extract subarray
        subarray = songs[left:right+1]
        
        # Find longest subarray with distinct elements
        max_length = find_longest_distinct_subarray(subarray)
        results.append(max_length)
    
    return results

def find_longest_distinct_subarray(songs):
    """
    Find longest subarray with distinct elements using sliding window
    """
    n = len(songs)
    if n == 0:
        return 0
    
    seen = set()
    left = 0
    max_length = 0
    
    for right in range(n):
        # Remove elements from left until current element is unique
        while songs[right] in seen:
            seen.remove(songs[left])
            left += 1
        
        # Add current element to the window
        seen.add(songs[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

def find_longest_distinct_subarray_optimized(songs):
    """
    Optimized version with early termination
    """
    n = len(songs)
    if n == 0:
        return 0
    
    seen = set()
    left = 0
    max_length = 0
    
    for right in range(n):
        # Remove elements from left until current element is unique
        while songs[right] in seen:
            seen.remove(songs[left])
            left += 1
        
        # Add current element to the window
        seen.add(songs[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
        
        # Early termination if we can't improve
        if max_length == n:
            break
    
    return max_length
```

### Variation 2: Playlist with Updates
**Problem**: Handle dynamic updates to the playlist and maintain longest subarray queries.

**Link**: [CSES Problem Set - Playlist with Updates](https://cses.fi/problemset/task/playlist_updates)

```python
class PlaylistWithUpdates:
    def __init__(self, songs):
        self.songs = songs[:]
        self.n = len(songs)
        self.max_length = self._compute_max_length()
    
    def _compute_max_length(self):
        """Compute initial longest subarray with distinct elements"""
        if self.n == 0:
            return 0
        
        seen = set()
        left = 0
        max_length = 0
        
        for right in range(self.n):
            # Remove elements from left until current element is unique
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            # Add current element to the window
            seen.add(self.songs[right])
            
            # Update maximum length
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def update(self, index, new_song):
        """Update song at index to new_song"""
        self.songs[index] = new_song
        self.max_length = self._compute_max_length()
    
    def add_song(self, new_song):
        """Add a new song to the playlist"""
        self.songs.append(new_song)
        self.n = len(self.songs)
        self.max_length = self._compute_max_length()
    
    def remove_song(self, index):
        """Remove song at index"""
        self.songs.pop(index)
        self.n = len(self.songs)
        self.max_length = self._compute_max_length()
    
    def get_max_length(self):
        """Get current maximum length of distinct subarray"""
        return self.max_length
    
    def get_max_length_range(self, left, right):
        """Get maximum length of distinct subarray in range [left, right]"""
        # Extract subarray
        subarray = self.songs[left:right+1]
        
        # Find longest subarray with distinct elements
        return find_longest_distinct_subarray(subarray)
    
    def get_all_distinct_subarrays(self):
        """Get all subarrays with distinct elements"""
        result = []
        n = len(self.songs)
        
        for i in range(n):
            seen = set()
            for j in range(i, n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                result.append(self.songs[i:j+1])
        
        return result
```

### Variation 3: Playlist with Constraints
**Problem**: Find longest subarray with distinct elements that satisfy additional constraints (e.g., minimum length, maximum sum).

**Link**: [CSES Problem Set - Playlist with Constraints](https://cses.fi/problemset/task/playlist_constraints)

```python
def playlist_constraints(songs, min_length, max_sum):
    """
    Find longest subarray with distinct elements that satisfy constraints
    """
    n = len(songs)
    if n == 0:
        return 0
    
    seen = set()
    left = 0
    max_length = 0
    
    for right in range(n):
        # Remove elements from left until current element is unique
        while songs[right] in seen:
            seen.remove(songs[left])
            left += 1
        
        # Add current element to the window
        seen.add(songs[right])
        
        # Check if current window satisfies constraints
        current_length = right - left + 1
        current_sum = sum(songs[left:right+1])
        
        if current_length >= min_length and current_sum <= max_sum:
            max_length = max(max_length, current_length)
    
    return max_length

def playlist_constraints_optimized(songs, min_length, max_sum):
    """
    Optimized version with early termination
    """
    n = len(songs)
    if n == 0:
        return 0
    
    seen = set()
    left = 0
    max_length = 0
    
    for right in range(n):
        # Remove elements from left until current element is unique
        while songs[right] in seen:
            seen.remove(songs[left])
            left += 1
        
        # Add current element to the window
        seen.add(songs[right])
        
        # Check if current window satisfies constraints
        current_length = right - left + 1
        
        # Early termination if length is too short
        if current_length < min_length:
            continue
        
        current_sum = sum(songs[left:right+1])
        
        if current_sum <= max_sum:
            max_length = max(max_length, current_length)
    
    return max_length

def playlist_constraints_multiple(songs, constraints_list):
    """
    Find longest subarray with distinct elements for multiple constraint sets
    """
    results = []
    
    for min_length, max_sum in constraints_list:
        result = playlist_constraints(songs, min_length, max_sum)
        results.append(result)
    
    return results

# Example usage
songs = [1, 2, 1, 3, 2, 1, 3, 4]
min_length = 2
max_sum = 10

result = playlist_constraints(songs, min_length, max_sum)
print(f"Longest distinct subarray with constraints: {result}")  # Output: 4
```

## Problem Variations

### **Variation 1: Playlist with Dynamic Updates**
**Problem**: Handle dynamic playlist updates (add/remove/update songs) while maintaining efficient longest distinct subarray queries.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicPlaylist:
    def __init__(self, songs):
        self.songs = songs[:]
        self.n = len(songs)
        self.max_length = self._compute_max_length()
    
    def _compute_max_length(self):
        """Compute longest subarray with distinct elements using sliding window."""
        if self.n == 0:
            return 0
        
        seen = set()
        left = 0
        max_length = 0
        
        for right in range(self.n):
            # Remove elements from left until current element is unique
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            # Add current element to the window
            seen.add(self.songs[right])
            
            # Update maximum length
            max_length = max(max_length, right - left + 1)
            
            # Early termination if we can't improve
            if max_length == self.n:
                break
        
        return max_length
    
    def add_song(self, song):
        """Add a new song to the playlist."""
        self.songs.append(song)
        self.n += 1
        self.max_length = self._compute_max_length()
    
    def remove_song(self, index):
        """Remove a song at the specified index."""
        if 0 <= index < self.n:
            del self.songs[index]
            self.n -= 1
            self.max_length = self._compute_max_length()
    
    def update_song(self, index, new_song):
        """Update a song at the specified index."""
        if 0 <= index < self.n:
            self.songs[index] = new_song
            self.max_length = self._compute_max_length()
    
    def get_max_length(self):
        """Get current maximum length of distinct subarray."""
        return self.max_length
    
    def get_longest_distinct_subarray(self):
        """Get the actual longest distinct subarray."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_length = 0
        best_left = 0
        best_right = 0
        
        for right in range(self.n):
            # Remove elements from left until current element is unique
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            # Add current element to the window
            seen.add(self.songs[right])
            
            # Update maximum length and best indices
            if right - left + 1 > max_length:
                max_length = right - left + 1
                best_left = left
                best_right = right
        
        return self.songs[best_left:best_right + 1]
    
    def get_distinct_subarrays_count(self):
        """Get count of all distinct subarrays."""
        if self.n == 0:
            return 0
        
        count = 0
        for i in range(self.n):
            seen = set()
            for j in range(i, self.n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                count += 1
        
        return count
    
    def get_distinct_subarrays_with_length(self, target_length):
        """Get all distinct subarrays with specific length."""
        result = []
        
        for i in range(self.n - target_length + 1):
            subarray = self.songs[i:i + target_length]
            if len(set(subarray)) == target_length:
                result.append(subarray)
        
        return result
    
    def get_distinct_subarrays_with_constraints(self, constraint_func):
        """Get distinct subarrays that satisfy custom constraints."""
        result = []
        
        for i in range(self.n):
            seen = set()
            for j in range(i, self.n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                
                if constraint_func(self.songs[i:j + 1]):
                    result.append(self.songs[i:j + 1])
        
        return result
    
    def get_playlist_statistics(self):
        """Get statistics about the playlist."""
        if not self.songs:
            return {
                'total_songs': 0,
                'unique_songs': 0,
                'max_distinct_length': 0,
                'average_distinct_length': 0,
                'song_frequency': {}
            }
        
        unique_songs = len(set(self.songs))
        song_frequency = {}
        for song in self.songs:
            song_frequency[song] = song_frequency.get(song, 0) + 1
        
        # Calculate average distinct length
        total_distinct_length = 0
        count = 0
        
        for i in range(self.n):
            seen = set()
            for j in range(i, self.n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                total_distinct_length += len(seen)
                count += 1
        
        average_distinct_length = total_distinct_length / count if count > 0 else 0
        
        return {
            'total_songs': self.n,
            'unique_songs': unique_songs,
            'max_distinct_length': self.max_length,
            'average_distinct_length': average_distinct_length,
            'song_frequency': song_frequency
        }
    
    def get_playlist_patterns(self):
        """Get patterns in the playlist."""
        patterns = {
            'consecutive_distinct': 0,
            'alternating_pattern': 0,
            'repetitive_pattern': 0,
            'unique_pattern': 0
        }
        
        for i in range(1, self.n):
            if self.songs[i] != self.songs[i-1]:
                patterns['consecutive_distinct'] += 1
            
            if i > 1:
                if (self.songs[i] == self.songs[i-2] and 
                    self.songs[i] != self.songs[i-1]):
                    patterns['alternating_pattern'] += 1
        
        return patterns

# Example usage
songs = [1, 2, 1, 3, 2, 1, 3, 4]
dynamic_playlist = DynamicPlaylist(songs)
print(f"Initial max length: {dynamic_playlist.get_max_length()}")

# Add a song
dynamic_playlist.add_song(5)
print(f"After adding song: {dynamic_playlist.get_max_length()}")

# Update a song
dynamic_playlist.update_song(1, 6)
print(f"After updating song: {dynamic_playlist.get_max_length()}")

# Get longest distinct subarray
print(f"Longest distinct subarray: {dynamic_playlist.get_longest_distinct_subarray()}")

# Get distinct subarrays count
print(f"Distinct subarrays count: {dynamic_playlist.get_distinct_subarrays_count()}")

# Get distinct subarrays with length
print(f"Distinct subarrays with length 3: {dynamic_playlist.get_distinct_subarrays_with_length(3)}")

# Get distinct subarrays with constraints
def constraint_func(subarray):
    return len(subarray) >= 2 and sum(subarray) > 5

print(f"Distinct subarrays with constraints: {dynamic_playlist.get_distinct_subarrays_with_constraints(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_playlist.get_playlist_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_playlist.get_playlist_patterns()}")
```

### **Variation 2: Playlist with Different Operations**
**Problem**: Handle different types of operations on playlists (weighted songs, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of playlist queries.

```python
class AdvancedPlaylist:
    def __init__(self, songs, weights=None, priorities=None):
        self.songs = songs[:]
        self.n = len(songs)
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.max_length = self._compute_max_length()
        self.weighted_max_length = self._compute_weighted_max_length()
    
    def _compute_max_length(self):
        """Compute longest subarray with distinct elements."""
        if self.n == 0:
            return 0
        
        seen = set()
        left = 0
        max_length = 0
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def _compute_weighted_max_length(self):
        """Compute longest subarray with distinct elements considering weights."""
        if self.n == 0:
            return 0
        
        seen = set()
        left = 0
        max_weighted_length = 0
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            current_weighted_length = sum(self.weights[left:right + 1])
            max_weighted_length = max(max_weighted_length, current_weighted_length)
        
        return max_weighted_length
    
    def get_max_length(self):
        """Get current maximum length of distinct subarray."""
        return self.max_length
    
    def get_weighted_max_length(self):
        """Get current maximum weighted length of distinct subarray."""
        return self.weighted_max_length
    
    def get_longest_distinct_subarray_with_priority(self, priority_func):
        """Get longest distinct subarray considering priority."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_priority = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            priority = priority_func(subarray, self.weights[left:right + 1], self.priorities[left:right + 1])
            
            if priority > max_priority:
                max_priority = priority
                best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_optimization(self, optimization_func):
        """Get longest distinct subarray using custom optimization function."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_score = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            score = optimization_func(subarray, self.weights[left:right + 1], self.priorities[left:right + 1])
            
            if score > max_score:
                max_score = score
                best_subarray = subarray
        
        return best_subarray
    
    def get_distinct_subarrays_with_constraints(self, constraint_func):
        """Get distinct subarrays that satisfy custom constraints."""
        result = []
        
        for i in range(self.n):
            seen = set()
            for j in range(i, self.n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                
                subarray = self.songs[i:j + 1]
                if constraint_func(subarray, self.weights[i:j + 1], self.priorities[i:j + 1]):
                    result.append(subarray)
        
        return result
    
    def get_distinct_subarrays_with_multiple_criteria(self, criteria_list):
        """Get distinct subarrays that satisfy multiple criteria."""
        result = []
        
        for i in range(self.n):
            seen = set()
            for j in range(i, self.n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                
                subarray = self.songs[i:j + 1]
                satisfies_all_criteria = True
                
                for criterion in criteria_list:
                    if not criterion(subarray, self.weights[i:j + 1], self.priorities[i:j + 1]):
                        satisfies_all_criteria = False
                        break
                
                if satisfies_all_criteria:
                    result.append(subarray)
        
        return result
    
    def get_distinct_subarrays_with_alternatives(self, alternatives):
        """Get distinct subarrays considering alternative songs."""
        result = []
        
        for i in range(self.n):
            seen = set()
            for j in range(i, self.n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                
                # Check original subarray
                subarray = self.songs[i:j + 1]
                result.append((subarray, 'original'))
                
                # Check alternative subarrays
                if j in alternatives:
                    for alt_song in alternatives[j]:
                        alt_subarray = self.songs[i:j] + [alt_song]
                        if len(set(alt_subarray)) == len(alt_subarray):
                            result.append((alt_subarray, 'alternative'))
        
        return result
    
    def get_distinct_subarrays_with_adaptive_criteria(self, adaptive_func):
        """Get distinct subarrays using adaptive criteria."""
        result = []
        
        for i in range(self.n):
            seen = set()
            for j in range(i, self.n):
                if self.songs[j] in seen:
                    break
                seen.add(self.songs[j])
                
                subarray = self.songs[i:j + 1]
                if adaptive_func(subarray, self.weights[i:j + 1], self.priorities[i:j + 1], result):
                    result.append(subarray)
        
        return result
    
    def get_playlist_optimization(self):
        """Get optimal playlist configuration."""
        strategies = [
            ('max_length', self.get_max_length),
            ('weighted_max_length', self.get_weighted_max_length),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
songs = [1, 2, 1, 3, 2, 1, 3, 4]
weights = [2, 1, 3, 1, 2, 1, 3, 2]
priorities = [1, 2, 1, 3, 2, 1, 3, 1]
advanced_playlist = AdvancedPlaylist(songs, weights, priorities)

print(f"Max length: {advanced_playlist.get_max_length()}")
print(f"Weighted max length: {advanced_playlist.get_weighted_max_length()}")

# Get longest distinct subarray with priority
def priority_func(subarray, weights, priorities):
    return len(subarray) * sum(priorities)

print(f"Longest distinct subarray with priority: {advanced_playlist.get_longest_distinct_subarray_with_priority(priority_func)}")

# Get longest distinct subarray with optimization
def optimization_func(subarray, weights, priorities):
    return len(subarray) * sum(weights) + sum(priorities)

print(f"Longest distinct subarray with optimization: {advanced_playlist.get_longest_distinct_subarray_with_optimization(optimization_func)}")

# Get distinct subarrays with constraints
def constraint_func(subarray, weights, priorities):
    return len(subarray) >= 2 and sum(weights) > 5

print(f"Distinct subarrays with constraints: {advanced_playlist.get_distinct_subarrays_with_constraints(constraint_func)}")

# Get distinct subarrays with multiple criteria
def criterion1(subarray, weights, priorities):
    return len(subarray) >= 2

def criterion2(subarray, weights, priorities):
    return sum(weights) > 5

criteria_list = [criterion1, criterion2]
print(f"Distinct subarrays with multiple criteria: {advanced_playlist.get_distinct_subarrays_with_multiple_criteria(criteria_list)}")

# Get distinct subarrays with alternatives
alternatives = {2: [5, 6], 5: [7, 8]}
print(f"Distinct subarrays with alternatives: {advanced_playlist.get_distinct_subarrays_with_alternatives(alternatives)}")

# Get distinct subarrays with adaptive criteria
def adaptive_func(subarray, weights, priorities, current_result):
    return len(subarray) >= 2 and len(current_result) < 5

print(f"Distinct subarrays with adaptive criteria: {advanced_playlist.get_distinct_subarrays_with_adaptive_criteria(adaptive_func)}")

# Get playlist optimization
print(f"Playlist optimization: {advanced_playlist.get_playlist_optimization()}")
```

### **Variation 3: Playlist with Constraints**
**Problem**: Handle playlist with additional constraints (time limits, resource constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedPlaylist:
    def __init__(self, songs, constraints=None):
        self.songs = songs[:]
        self.n = len(songs)
        self.constraints = constraints or {}
        self.max_length = self._compute_max_length()
    
    def _compute_max_length(self):
        """Compute longest subarray with distinct elements."""
        if self.n == 0:
            return 0
        
        seen = set()
        left = 0
        max_length = 0
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def get_longest_distinct_subarray_with_time_constraints(self, time_limit):
        """Get longest distinct subarray considering time constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_length = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            
            # Simulate time constraint (length represents time)
            if len(subarray) <= time_limit and len(subarray) > max_length:
                max_length = len(subarray)
                best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get longest distinct subarray considering resource constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_length = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            
            # Check resource constraints
            can_use_subarray = True
            for j, consumption in enumerate(resource_consumption[left:right + 1]):
                if consumption > resource_limits[j]:
                    can_use_subarray = False
                    break
            
            if can_use_subarray and len(subarray) > max_length:
                max_length = len(subarray)
                best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_mathematical_constraints(self, constraint_func):
        """Get longest distinct subarray that satisfies custom mathematical constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_length = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            
            if constraint_func(subarray, len(subarray)):
                if len(subarray) > max_length:
                    max_length = len(subarray)
                    best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_range_constraints(self, range_constraints):
        """Get longest distinct subarray that satisfies range constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_length = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            
            # Check if subarray satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(subarray, len(subarray)):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints and len(subarray) > max_length:
                max_length = len(subarray)
                best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_optimization_constraints(self, optimization_func):
        """Get longest distinct subarray using custom optimization constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_score = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            score = optimization_func(subarray, len(subarray))
            
            if score > max_score:
                max_score = score
                best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_multiple_constraints(self, constraints_list):
        """Get longest distinct subarray that satisfies multiple constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_length = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            
            # Check if subarray satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(subarray, len(subarray)):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints and len(subarray) > max_length:
                max_length = len(subarray)
                best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_priority_constraints(self, priority_func):
        """Get longest distinct subarray with priority-based constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_priority = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            priority = priority_func(subarray, len(subarray))
            
            if priority > max_priority:
                max_priority = priority
                best_subarray = subarray
        
        return best_subarray
    
    def get_longest_distinct_subarray_with_adaptive_constraints(self, adaptive_func):
        """Get longest distinct subarray with adaptive constraints."""
        if self.n == 0:
            return []
        
        seen = set()
        left = 0
        max_length = 0
        best_subarray = []
        
        for right in range(self.n):
            while self.songs[right] in seen:
                seen.remove(self.songs[left])
                left += 1
            
            seen.add(self.songs[right])
            subarray = self.songs[left:right + 1]
            
            # Check adaptive constraints
            if adaptive_func(subarray, len(subarray), best_subarray):
                if len(subarray) > max_length:
                    max_length = len(subarray)
                    best_subarray = subarray
        
        return best_subarray
    
    def get_optimal_playlist_strategy(self):
        """Get optimal playlist strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_longest_distinct_subarray_with_time_constraints),
            ('resource_constraints', self.get_longest_distinct_subarray_with_resource_constraints),
            ('mathematical_constraints', self.get_longest_distinct_subarray_with_mathematical_constraints),
        ]
        
        best_strategy = None
        best_length = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'time_constraints':
                    current_result = strategy_func(5)  # 5 time units
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    current_result = strategy_func(resource_limits, resource_consumption)
                elif strategy_name == 'mathematical_constraints':
                    def constraint_func(subarray, length):
                        return length >= 2 and sum(subarray) > 5
                    current_result = strategy_func(constraint_func)
                
                if len(current_result) > best_length:
                    best_length = len(current_result)
                    best_strategy = (strategy_name, current_result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 2,
    'max_length': 10
}

songs = [1, 2, 1, 3, 2, 1, 3, 4]
constrained_playlist = ConstrainedPlaylist(songs, constraints)

print("Time-constrained longest distinct subarray:", constrained_playlist.get_longest_distinct_subarray_with_time_constraints(5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(songs))}
print("Resource-constrained longest distinct subarray:", constrained_playlist.get_longest_distinct_subarray_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(subarray, length):
    return length >= 2 and sum(subarray) > 5

print("Mathematical constraint longest distinct subarray:", constrained_playlist.get_longest_distinct_subarray_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(subarray, length):
    return length >= 2 and sum(subarray) > 5

range_constraints = [range_constraint]
print("Range-constrained longest distinct subarray:", constrained_playlist.get_longest_distinct_subarray_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(subarray, length):
    return length >= 2

def constraint2(subarray, length):
    return sum(subarray) > 5

constraints_list = [constraint1, constraint2]
print("Multiple constraints longest distinct subarray:", constrained_playlist.get_longest_distinct_subarray_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(subarray, length):
    return length * sum(subarray)

print("Priority-constrained longest distinct subarray:", constrained_playlist.get_longest_distinct_subarray_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(subarray, length, current_best):
    return length >= 2 and (not current_best or length > len(current_best))

print("Adaptive constraint longest distinct subarray:", constrained_playlist.get_longest_distinct_subarray_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_playlist.get_optimal_playlist_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Playlist](https://cses.fi/problemset/task/1141) - Basic playlist problem
- [Distinct Values Subarrays](https://cses.fi/problemset/task/2108) - Distinct values subarrays
- [Subarray Distinct Values](https://cses.fi/problemset/task/2428) - Subarray distinct values queries

#### **LeetCode Problems**
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) - Longest substring with distinct characters
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) - Longest substring with at most k distinct characters
- [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) - Subarrays with exactly k distinct values
- [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) - Sliding window with at most 2 distinct values

#### **Problem Categories**
- **Sliding Window**: Two-pointer technique, window contraction, efficient subarray processing
- **Hash Sets**: Distinct element tracking, efficient lookups, set operations
- **Array Processing**: Subarray analysis, distinct value counting, constraint handling
- **Algorithm Design**: Sliding window algorithms, hash-based techniques, subarray optimization
