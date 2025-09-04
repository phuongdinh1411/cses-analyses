---
layout: simple
title: "Sorting And Searching Summary"
permalink: /problem_soulutions/sorting_and_searching/summary
---

# Sorting and Searching

Welcome to the Sorting and Searching section! This category covers fundamental algorithms for organizing and finding data efficiently.

## Problem Categories

### Basic Sorting
- [CSES Distinct Numbers](cses_distinct_numbers_analysis) - Count unique elements
- [CSES Apartments](cses_apartments_analysis) - Matching problem with sorting
- [CSES Stick Lengths](cses_stick_lengths_analysis) - Minimize differences
- [CSES Towers](cses_towers_analysis) - Building towers with constraints

### Two-Pointer Technique
- [CSES Sum of Two Values](cses_sum_of_two_values_analysis) - Find pair with given sum
- [Sum of Three Values](sum_of_three_values_analysis) - Find triplet with given sum
- [Sum of Four Values](sum_of_four_values_analysis) - Find quadruplet with given sum
- [Nearest Smaller Values](nearest_smaller_values_analysis) - Find nearest smaller elements

### Sliding Window
- [CSES Playlist](cses_playlist_analysis) - Maximum unique elements window
- [Subarray Sums I](subarray_sums_i_analysis) - Find subarrays with given sum
- [Subarray Sums II](subarray_sums_ii_analysis) - Advanced subarray sum problems
- [Subarray Divisibility](subarray_divisibility_analysis) - Divisible subarrays

### Binary Search
- [Factory Machines](factory_machines_analysis) - Binary search on answer
- [Array Division](array_division_analysis) - Divide array optimally
- [Sliding Median](sliding_median_analysis) - Maintain median in window

### Greedy Algorithms
- [CSES Movie Festival](cses_movie_festival_analysis) - Activity selection
- [Tasks and Deadlines](tasks_and_deadlines_analysis) - Optimal task scheduling
- [Reading Books](reading_books_analysis) - Minimize reading time

### Advanced Problems
- [Collecting Numbers](collecting_numbers_analysis) - Array traversal order
- [Collecting Numbers II](collecting_numbers_ii_analysis) - Dynamic array traversal
- [Collecting Numbers III](collecting_numbers_iii_analysis) - Complex array traversal
- [Collecting Numbers IV](collecting_numbers_iv_analysis) - Advanced array traversal
- [Collecting Numbers V](collecting_numbers_v_analysis) - Expert array traversal

### Range Problems
- [Nested Ranges Check](nested_ranges_check_analysis) - Check range containment
- [Nested Ranges Count](nested_ranges_count_analysis) - Count contained ranges
- [Room Allocation](room_allocation_analysis) - Minimize room allocations

### Specialized Problems
- [Josephus Problem I](josephus_problem_i_analysis) - Circular elimination game
- [Josephus Problem II](josephus_problem_ii_analysis) - Advanced elimination game
- [Traffic Lights](traffic_lights_analysis) - Dynamic range maintenance

## Learning Path

### For Beginners (Start Here)
1. Start with **CSES Distinct Numbers** for basic sorting
2. Move to **CSES Apartments** for simple matching
3. Try **CSES Sum of Two Values** for two-pointer technique
4. Learn sliding window with **CSES Playlist**

### Intermediate Level
1. Master binary search with **Factory Machines**
2. Practice greedy algorithms with **CSES Movie Festival**
3. Explore range problems with **Nested Ranges Check**
4. Study array traversal with **Collecting Numbers**

### Advanced Level
1. Challenge yourself with **Josephus Problems**
2. Master advanced array problems with **Collecting Numbers V**
3. Solve complex range problems with **Traffic Lights**
4. Tackle optimization with **Tasks and Deadlines**

## Key Concepts & Techniques

### Sorting Techniques

#### Comparison-Based Sorting
- **Quick Sort**: General-purpose sorting
  - *When to use*: General sorting, average case performance
  - *Time*: O(n log n) average, O(n²) worst case
  - *Space*: O(log n)
  - *Applications*: General sorting, in-place sorting
- **Merge Sort**: Stable sorting
  - *When to use*: When stability is required, guaranteed O(n log n)
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Stable sorting, external sorting
- **Heap Sort**: In-place sorting
  - *When to use*: When you need in-place O(n log n) sorting
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: In-place sorting, priority queues

#### Non-Comparison Sorting
- **Counting Sort**: Integer sorting
  - *When to use*: Small integer ranges, linear time needed
  - *Time*: O(n + k) where k is range
  - *Space*: O(k)
  - *Applications*: Integer sorting, frequency counting
- **Radix Sort**: Multi-digit sorting
  - *When to use*: Multi-digit numbers, strings
  - *Time*: O(d(n + k)) where d is digits
  - *Space*: O(n + k)
  - *Applications*: String sorting, multi-key sorting

#### Custom Sorting
- **Custom Comparators**: Special sorting criteria
  - *When to use*: When default ordering not suitable
  - *Implementation*: Define comparison function
  - *Applications*: Multi-criteria sorting, complex objects
- **Stable Sorting**: Preserve relative order
  - *When to use*: When relative order of equal elements matters
  - *Implementation*: Use stable algorithms (merge sort, counting sort)
  - *Applications*: Multi-key sorting, user experience

### Searching Algorithms

#### Binary Search
- **Standard Binary Search**: Find exact element
  - *When to use*: Sorted array, find specific value
  - *Time*: O(log n)
  - *Space*: O(1)
  - *Applications*: Element search, duplicate detection
- **Lower/Upper Bound**: Find insertion points
  - *When to use*: Find first/last occurrence, insertion position
  - *Time*: O(log n)
  - *Space*: O(1)
  - *Applications*: Range queries, insertion operations
- **Binary Search on Answer**: Find optimal value
  - *When to use*: Optimization problems, monotonic functions
  - *Time*: O(log n) per search
  - *Space*: O(1)
  - *Applications*: Optimization, decision problems

#### Two-Pointer Technique
- **Opposite Direction**: Start from ends
  - *When to use*: Sorted array, find pairs
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Two sum, palindrome checking
- **Same Direction**: Both pointers move forward
  - *When to use*: Sliding window, subarray problems
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Subarray sum, window problems
- **Fast and Slow**: Different speeds
  - *When to use*: Cycle detection, middle finding
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Cycle detection, linked list problems

#### Sliding Window
- **Fixed Size Window**: Constant window size
  - *When to use*: Fixed-size subarray problems
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Subarray sum, window statistics
- **Variable Size Window**: Dynamic window size
  - *When to use*: Optimization problems, constraint satisfaction
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Longest subarray, minimum window
- **Two-Pointer Window**: Expand/contract window
  - *When to use*: When window size depends on content
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Substring problems, optimization

### Data Structures for Sorting & Searching

#### Priority Queues (Heaps)
- **Min-Heap**: Smallest element at top
  - *When to use*: When you need minimum element
  - *Time*: O(log n) insert/extract
  - *Space*: O(n)
  - *Applications*: Dijkstra's algorithm, top-k problems
- **Max-Heap**: Largest element at top
  - *When to use*: When you need maximum element
  - *Time*: O(log n) insert/extract
  - *Space*: O(n)
  - *Applications*: Priority scheduling, max-k problems
- **Custom Heaps**: Custom comparison
  - *When to use*: When default ordering not suitable
  - *Time*: O(log n) insert/extract
  - *Space*: O(n)
  - *Applications*: Multi-criteria priority, complex objects

#### Sets and Maps
- **Hash Set/Map**: Fast lookup
  - *When to use*: When you need fast lookup/insertion
  - *Time*: O(1) average, O(n) worst case
  - *Space*: O(n)
  - *Applications*: Duplicate detection, frequency counting
- **Tree Set/Map**: Ordered data
  - *When to use*: When you need ordered data
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Range queries, ordered statistics
- **Multi-Set/Map**: Allow duplicates
  - *When to use*: When duplicates are allowed
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Frequency counting, multi-sets

#### Advanced Data Structures
- **Segment Tree**: Range queries
  - *When to use*: Range queries with updates
  - *Time*: O(log n) per query/update
  - *Space*: O(n)
  - *Applications*: Range sum/min/max, range updates
- **Binary Indexed Tree**: Point updates, range queries
  - *When to use*: Point updates with range queries
  - *Time*: O(log n) per query/update
  - *Space*: O(n)
  - *Applications*: Range sum, inversion counting
- **Ordered Set**: Dynamic ordered data
  - *When to use*: When you need dynamic ordered data
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Dynamic ranking, order statistics

### Specialized Techniques

#### Greedy Algorithms
- **Activity Selection**: Choose optimal activities
  - *When to use*: When you need to select non-overlapping activities
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: Scheduling, resource allocation
- **Huffman Coding**: Optimal prefix codes
  - *When to use*: When you need optimal compression
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Data compression, encoding
- **Fractional Knapsack**: Greedy knapsack
  - *When to use*: When you can take fractions of items
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: Resource allocation, optimization

#### Range Problems
- **Interval Scheduling**: Schedule non-overlapping intervals
  - *When to use*: When you need to schedule intervals
  - *Time*: O(n log n)
  - *Space*: O(1)
  - *Applications*: Meeting scheduling, resource allocation
- **Range Merging**: Merge overlapping ranges
  - *When to use*: When you need to merge overlapping intervals
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Calendar merging, interval analysis
- **Range Containment**: Check if ranges contain each other
  - *When to use*: When you need to check range relationships
  - *Time*: O(n log n)
  - *Space*: O(n)
  - *Applications*: Range analysis, containment queries

### Optimization Techniques

#### Time Optimization
- **Precomputation**: Compute values once
  - *When to use*: When same calculations repeated
  - *Example*: Precompute prefix sums for range queries
- **Caching**: Store computed results
  - *When to use*: When calculations are expensive
  - *Example*: Cache sorted arrays for multiple searches
- **Early Termination**: Stop when condition met
  - *When to use*: When exact result not needed
  - *Example*: Stop binary search when range is small enough

#### Space Optimization
- **In-place Sorting**: Sort without extra space
  - *When to use*: When memory is limited
  - *Example*: Heap sort, quick sort
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy sorting, on-demand computation
- **Compression**: Reduce memory usage
  - *When to use*: When data has patterns
  - *Example*: Run-length encoding, delta compression

#### Algorithm Selection
- **Choose Right Algorithm**: Based on problem constraints
  - *When to use*: When multiple algorithms available
  - *Example*: Use counting sort for small ranges, merge sort for stability
- **Hybrid Approaches**: Combine multiple techniques
  - *When to use*: When single approach not optimal
  - *Example*: Introsort (quick sort + heap sort + insertion sort)
- **Adaptive Algorithms**: Adjust based on input
  - *When to use*: When input characteristics vary
  - *Example*: Adaptive quick sort, timsort

## Detailed Examples and Implementations

### Classic Sorting Algorithms with Code

#### 1. Comparison-Based Sorting
```python
def quick_sort(arr, low=0, high=None):
    """Quick Sort - Average O(n log n), Worst O(n²)"""
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition the array
        pivot_index = partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

def partition(arr, low, high):
    """Lomuto partition scheme"""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def merge_sort(arr):
    """Merge Sort - O(n log n) guaranteed"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr):
    """Heap Sort - O(n log n) guaranteed"""
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Swap
        heapify(arr, i, 0)

def heapify(arr, n, i):
    """Heapify subtree rooted at index i"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

#### 2. Non-Comparison Sorting
```python
def counting_sort(arr, max_val=None):
    """Counting Sort - O(n + k) where k is range"""
    if max_val is None:
        max_val = max(arr)
    
    count = [0] * (max_val + 1)
    
    # Count occurrences
    for num in arr:
        count[num] += 1
    
    # Reconstruct sorted array
    result = []
    for i in range(max_val + 1):
        result.extend([i] * count[i])
    
    return result

def radix_sort(arr):
    """Radix Sort - O(d * (n + k)) where d is number of digits"""
    if not arr:
        return arr
    
    # Find maximum number to determine number of digits
    max_num = max(arr)
    exp = 1
    
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10

def counting_sort_by_digit(arr, exp):
    """Counting sort for specific digit position"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Count occurrences of each digit
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    # Change count[i] to position of next occurrence
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    # Copy output back to original array
    for i in range(n):
        arr[i] = output[i]

def bucket_sort(arr):
    """Bucket Sort - O(n + k) average case"""
    if not arr:
        return arr
    
    # Create buckets
    n = len(arr)
    max_val = max(arr)
    min_val = min(arr)
    bucket_range = (max_val - min_val) / n
    buckets = [[] for _ in range(n)]
    
    # Distribute elements into buckets
    for num in arr:
        bucket_index = min(int((num - min_val) / bucket_range), n - 1)
        buckets[bucket_index].append(num)
    
    # Sort individual buckets and concatenate
    result = []
    for bucket in buckets:
        bucket.sort()  # Use any sorting algorithm
        result.extend(bucket)
    
    return result
```

#### 3. Binary Search Variations
```python
def binary_search(arr, target):
    """Standard binary search"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def lower_bound(arr, target):
    """Find first position where target can be inserted"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left

def upper_bound(arr, target):
    """Find last position where target can be inserted"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left

def binary_search_on_answer(arr, condition_func):
    """Binary search on answer space"""
    left, right = 0, len(arr) - 1
    answer = -1
    
    while left <= right:
        mid = (left + right) // 2
        if condition_func(arr[mid]):
            answer = mid
            left = mid + 1  # or right = mid - 1, depending on problem
        else:
            right = mid - 1  # or left = mid + 1
    
    return answer

def find_peak_element(arr):
    """Find peak element using binary search"""
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] > arr[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Advanced Searching Techniques

#### 1. Two Pointers Technique
```python
def two_sum_sorted(arr, target):
    """Find two numbers that sum to target in sorted array"""
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return [-1, -1]

def remove_duplicates(arr):
    """Remove duplicates from sorted array in-place"""
    if not arr:
        return 0
    
    write_index = 1
    for read_index in range(1, len(arr)):
        if arr[read_index] != arr[read_index - 1]:
            arr[write_index] = arr[read_index]
            write_index += 1
    
    return write_index

def three_sum(arr, target):
    """Find all triplets that sum to target"""
    arr.sort()
    result = []
    
    for i in range(len(arr) - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        
        left, right = i + 1, len(arr) - 1
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            if current_sum == target:
                result.append([arr[i], arr[left], arr[right]])
                
                # Skip duplicates
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result

def container_with_most_water(heights):
    """Find two lines that together with x-axis forms container with most water"""
    left, right = 0, len(heights) - 1
    max_area = 0
    
    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        area = width * height
        max_area = max(max_area, area)
        
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_area
```

#### 2. Sliding Window Technique
```python
def sliding_window_maximum(arr, k):
    """Find maximum in each sliding window of size k"""
    from collections import deque
    
    dq = deque()
    result = []
    
    # Process first window
    for i in range(k):
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        dq.append(i)
    
    result.append(arr[dq[0]])
    
    # Process remaining windows
    for i in range(k, len(arr)):
        # Remove elements outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove elements smaller than current element
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        dq.append(i)
        result.append(arr[dq[0]])
    
    return result

def longest_substring_without_repeating(s):
    """Find length of longest substring without repeating characters"""
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

def minimum_window_substring(s, t):
    """Find minimum window in s that contains all characters in t"""
    from collections import Counter
    
    if not s or not t:
        return ""
    
    dict_t = Counter(t)
    required = len(dict_t)
    
    left = right = 0
    formed = 0
    window_counts = {}
    
    ans = float('inf'), None, None
    
    while right < len(s):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1
        
        while left <= right and formed == required:
            char = s[left]
            
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            
            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1
            
            left += 1
        
        right += 1
    
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]
```

#### 3. Greedy Algorithms
```python
def activity_selection(activities):
    """Select maximum number of non-overlapping activities"""
    # Sort by finish time
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_finish_time = activities[0][1]
    
    for start, finish in activities[1:]:
        if start >= last_finish_time:
            selected.append((start, finish))
            last_finish_time = finish
    
    return selected

def fractional_knapsack(weights, values, capacity):
    """Fractional knapsack using greedy approach"""
    items = list(zip(weights, values))
    # Sort by value per unit weight (descending)
    items.sort(key=lambda x: x[1] / x[0], reverse=True)
    
    total_value = 0
    remaining_capacity = capacity
    
    for weight, value in items:
        if remaining_capacity >= weight:
            # Take the whole item
            total_value += value
            remaining_capacity -= weight
        else:
            # Take fraction of item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            break
    
    return total_value

def huffman_coding(frequencies):
    """Build Huffman tree for optimal prefix codes"""
    import heapq
    
    # Create min heap
    heap = [[freq, [char, ""]] for char, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        # Extract two nodes with minimum frequency
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        # Add '0' to left subtree and '1' to right subtree
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        for pair in right[1:]:
            pair[1] = '1' + pair[1]
        
        # Create new node
        new_node = [left[0] + right[0]] + left[1:] + right[1:]
        heapq.heappush(heap, new_node)
    
    return heap[0][1:]

def interval_scheduling(intervals):
    """Schedule maximum number of non-overlapping intervals"""
    # Sort by finish time
    intervals.sort(key=lambda x: x[1])
    
    selected = [intervals[0]]
    last_finish = intervals[0][1]
    
    for start, finish in intervals[1:]:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return selected
```

### Advanced Data Structures

#### 1. Custom Comparators and Sorting
```python
def custom_sort_examples():
    """Examples of custom sorting"""
    
    # Sort by multiple criteria
    students = [
        ("Alice", 85, "A"),
        ("Bob", 90, "B"),
        ("Charlie", 85, "A"),
        ("David", 90, "A")
    ]
    
    # Sort by grade (descending), then by name (ascending)
    students.sort(key=lambda x: (-x[1], x[0]))
    
    # Sort strings by length, then alphabetically
    words = ["apple", "pie", "banana", "cat"]
    words.sort(key=lambda x: (len(x), x))
    
    # Sort points by distance from origin
    points = [(3, 4), (1, 1), (5, 2), (0, 0)]
    points.sort(key=lambda x: x[0]**2 + x[1]**2)
    
    return students, words, points

def stable_sort_example():
    """Demonstrate stable sorting"""
    # Merge sort is stable, quick sort is not
    arr = [(3, 'a'), (1, 'b'), (3, 'c'), (1, 'd')]
    
    # Stable sort preserves relative order of equal elements
    stable_sorted = merge_sort(arr.copy())
    
    return stable_sorted

def in_place_sorting():
    """Examples of in-place sorting"""
    arr1 = [64, 34, 25, 12, 22, 11, 90]
    arr2 = arr1.copy()
    arr3 = arr1.copy()
    
    # Quick sort (in-place)
    quick_sort(arr1)
    
    # Heap sort (in-place)
    heap_sort(arr2)
    
    # Selection sort (in-place)
    for i in range(len(arr3)):
        min_idx = i
        for j in range(i + 1, len(arr3)):
            if arr3[j] < arr3[min_idx]:
                min_idx = j
        arr3[i], arr3[min_idx] = arr3[min_idx], arr3[i]
    
    return arr1, arr2, arr3
```

## Tips for Success

1. **Master Binary Search**: Essential for many problems
2. **Understand Two Pointers**: Key technique for arrays
3. **Practice Sliding Window**: Important pattern
4. **Learn Greedy Strategies**: Optimal local choices
5. **Study Sorting Algorithms**: Know when to use each
6. **Handle Edge Cases**: Empty arrays, single elements

## Common Pitfalls to Avoid

1. **Off-by-One Errors**: Be careful with array indices
2. **Integer Overflow**: Use appropriate data types
3. **Time Complexity**: Watch for inefficient solutions
4. **Edge Cases**: Consider boundary conditions

---

Ready to start? Begin with [CSES Distinct Numbers](cses_distinct_numbers_analysis) and work your way through the problems in order of difficulty!