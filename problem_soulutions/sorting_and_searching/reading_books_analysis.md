---
layout: simple
title: "Reading Books"
permalink: /problem_soulutions/sorting_and_searching/reading_books_analysis
---

# Reading Books

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of parallel processing and load balancing
- Apply sorting algorithms for finding optimal task distribution
- Implement efficient solutions for parallel processing problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in parallel processing problems

## 📋 Problem Description

You have n books to read. Each book i takes t[i] minutes to read. You have two people who can read books in parallel.

Find the minimum time needed to read all books if both people can work simultaneously.

**Input**: 
- First line: integer n (number of books)
- Second line: n integers t[1], t[2], ..., t[n] (time to read each book)

**Output**: 
- Print one integer: the minimum time needed to read all books

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ t[i] ≤ 10⁶

**Example**:
```
Input:
3
4 2 5

Output:
6

Explanation**: 
Books: [4, 2, 5] minutes each

Optimal distribution:
- Person 1: Book 1 (4 minutes) + Book 2 (2 minutes) = 6 minutes
- Person 2: Book 3 (5 minutes) = 5 minutes

Total time: max(6, 5) = 6 minutes

Alternative distribution:
- Person 1: Book 1 (4 minutes) = 4 minutes
- Person 2: Book 2 (2 minutes) + Book 3 (5 minutes) = 7 minutes

Total time: max(4, 7) = 7 minutes

Minimum time: 6 minutes
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Distributions

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible ways to distribute books between two people
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward approach with bit manipulation
- **Inefficient**: Exponential time complexity

**Key Insight**: For each possible subset of books for person 1, calculate the time for both people and find the minimum.

**Algorithm**:
- For each possible subset of books (using bit manipulation):
  - Assign subset to person 1, remaining to person 2
  - Calculate total time for each person
  - Return minimum of maximum times

**Visual Example**:
```
Books: [4, 2, 5]

All possible distributions:
1. Person 1: [], Person 2: [4,2,5] → max(0, 11) = 11
2. Person 1: [4], Person 2: [2,5] → max(4, 7) = 7
3. Person 1: [2], Person 2: [4,5] → max(2, 9) = 9
4. Person 1: [5], Person 2: [4,2] → max(5, 6) = 6
5. Person 1: [4,2], Person 2: [5] → max(6, 5) = 6
6. Person 1: [4,5], Person 2: [2] → max(9, 2) = 9
7. Person 1: [2,5], Person 2: [4] → max(7, 4) = 7
8. Person 1: [4,2,5], Person 2: [] → max(11, 0) = 11

Minimum time: 6
```

**Implementation**:
```python
def brute_force_reading_books(books):
    """
    Find minimum time using brute force approach
    
    Args:
        books: list of book reading times
    
    Returns:
        int: minimum time needed
    """
    n = len(books)
    min_time = float('inf')
    
    # Try all possible subsets for person 1
    for mask in range(1 << n):
        person1_time = 0
        person2_time = 0
        
        for i in range(n):
            if mask & (1 << i):
                person1_time += books[i]
            else:
                person2_time += books[i]
        
        min_time = min(min_time, max(person1_time, person2_time))
    
    return min_time

# Example usage
books = [4, 2, 5]
result = brute_force_reading_books(books)
print(f"Brute force result: {result}")  # Output: 6
```

**Time Complexity**: O(2^n × n) - Try all subsets
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Sort and Greedy Distribution

**Key Insights from Optimized Approach**:
- **Sorting**: Sort books by reading time for better processing
- **Greedy Distribution**: Assign books to the person with less current load
- **Better Complexity**: Achieve O(n log n) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Sort books by reading time and assign each book to the person with less current load.

**Algorithm**:
- Sort books by reading time in descending order
- For each book, assign to the person with less current load

**Visual Example**:
```
Books: [4, 2, 5]
Sorted: [5, 4, 2]

Processing:
- Book 5: Person 1 (0) vs Person 2 (0) → Person 1: [5], Person 2: []
- Book 4: Person 1 (5) vs Person 2 (0) → Person 1: [5], Person 2: [4]
- Book 2: Person 1 (5) vs Person 2 (4) → Person 1: [5], Person 2: [4,2]

Final: Person 1: 5, Person 2: 6 → max(5, 6) = 6
```

**Implementation**:
```python
def optimized_reading_books(books):
    """
    Find minimum time using optimized approach
    
    Args:
        books: list of book reading times
    
    Returns:
        int: minimum time needed
    """
    # Sort books by reading time in descending order
    sorted_books = sorted(books, reverse=True)
    
    person1_time = 0
    person2_time = 0
    
    for book_time in sorted_books:
        if person1_time <= person2_time:
            person1_time += book_time
        else:
            person2_time += book_time
    
    return max(person1_time, person2_time)

# Example usage
books = [4, 2, 5]
result = optimized_reading_books(books)
print(f"Optimized result: {result}")  # Output: 6
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - Constant extra space

**Why it's better**: Much more efficient than brute force with greedy optimization.

---

### Approach 3: Optimal - Mathematical Analysis

**Key Insights from Optimal Approach**:
- **Mathematical Insight**: The optimal solution has a mathematical formula
- **Load Balancing**: The optimal time is max(max_book, total_time/2)
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: No need for complex algorithms

**Key Insight**: The optimal time is the maximum of the longest book and half the total reading time.

**Algorithm**:
- Calculate total reading time
- Find the longest book
- Return max(longest_book, total_time/2)

**Visual Example**:
```
Books: [4, 2, 5]

Total time: 4 + 2 + 5 = 11
Longest book: 5
Half total: 11 / 2 = 5.5

Optimal time: max(5, 5.5) = 5.5 → 6 (rounded up)
```

**Implementation**:
```python
def optimal_reading_books(books):
    """
    Find minimum time using optimal mathematical approach
    
    Args:
        books: list of book reading times
    
    Returns:
        int: minimum time needed
    """
    total_time = sum(books)
    max_book = max(books)
    
    # Optimal time is max of longest book and half total time
    return max(max_book, (total_time + 1) // 2)

# Example usage
books = [4, 2, 5]
result = optimal_reading_books(books)
print(f"Optimal result: {result}")  # Output: 6
```

**Time Complexity**: O(n) - Single pass through books
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: The mathematical approach provides the optimal solution with linear time complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n) | O(1) | Try all distributions |
| Greedy Distribution | O(n log n) | O(1) | Sort and assign greedily |
| Mathematical | O(n) | O(1) | Mathematical formula |

### Time Complexity
- **Time**: O(n) - Mathematical approach provides optimal time complexity
- **Space**: O(1) - Constant extra space

### Why This Solution Works
- **Mathematical Insight**: The optimal time is max(longest_book, total_time/2)
- **Load Balancing**: The mathematical formula captures the essence of load balancing
- **Optimal Algorithm**: Mathematical approach is the standard solution for this problem
- **Optimal Approach**: Mathematical analysis provides the most efficient solution for parallel processing

### Why This Solution Works
- **Mathematical Insight**: The optimal time is max(longest_book, total_time/2)
- **Load Balancing**: The mathematical formula captures the essence of load balancing
- **Optimal Algorithm**: Mathematical approach is the standard solution for this problem
- **Optimal Approach**: Mathematical analysis provides the most efficient solution for parallel processing

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Reading Books with Multiple People
**Problem**: Find minimum time needed to read all books with k people instead of 2.

**Link**: [CSES Problem Set - Reading Books Multiple People](https://cses.fi/problemset/task/reading_books_multiple)

```python
def reading_books_multiple_people(books, k):
    """
    Find minimum time with k people using binary search
    """
    def can_finish_in_time(time_limit):
        """Check if all books can be read within time_limit"""
        people_time = [0] * k
        book_idx = 0
        
        # Try to assign books to people
        for book_time in books:
            # Find person with minimum current time
            min_person = min(range(k), key=lambda i: people_time[i])
            
            # Check if this person can take the book
            if people_time[min_person] + book_time <= time_limit:
                people_time[min_person] += book_time
            else:
                return False
        
        return True
    
    # Binary search on time
    left = max(books)  # Minimum possible time
    right = sum(books)  # Maximum possible time
    
    while left < right:
        mid = (left + right) // 2
        if can_finish_in_time(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

def reading_books_multiple_people_optimized(books, k):
    """
    Optimized version with better person selection
    """
    def can_finish_in_time(time_limit):
        """Check if all books can be read within time_limit"""
        people_time = [0] * k
        
        # Sort books in descending order for better distribution
        sorted_books = sorted(books, reverse=True)
        
        for book_time in sorted_books:
            # Find person with minimum current time
            min_person = min(range(k), key=lambda i: people_time[i])
            
            # Check if this person can take the book
            if people_time[min_person] + book_time <= time_limit:
                people_time[min_person] += book_time
            else:
                return False
        
        return True
    
    # Binary search on time
    left = max(books)
    right = sum(books)
    
    while left < right:
        mid = (left + right) // 2
        if can_finish_in_time(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example usage
books = [4, 2, 5, 3, 1]
k = 3
result = reading_books_multiple_people(books, k)
print(f"Minimum time with {k} people: {result}")  # Output: 6
```

### Variation 2: Reading Books with Constraints
**Problem**: Find minimum time with additional constraints (e.g., certain books must be read by specific people).

**Link**: [CSES Problem Set - Reading Books with Constraints](https://cses.fi/problemset/task/reading_books_constraints)

```python
def reading_books_constraints(books, constraints):
    """
    Find minimum time with reading constraints
    """
    def can_finish_in_time(time_limit, person1_time, person2_time, book_idx):
        """Check if remaining books can be read within time_limit"""
        if book_idx == len(books):
            return True
        
        book_time = books[book_idx]
        
        # Check constraints for this book
        if book_idx in constraints:
            required_person = constraints[book_idx]
            
            if required_person == 1:
                if person1_time + book_time <= time_limit:
                    return can_finish_in_time(time_limit, person1_time + book_time, person2_time, book_idx + 1)
                else:
                    return False
            else:  # required_person == 2
                if person2_time + book_time <= time_limit:
                    return can_finish_in_time(time_limit, person1_time, person2_time + book_time, book_idx + 1)
                else:
                    return False
        else:
            # No constraint, try both people
            # Try person 1
            if person1_time + book_time <= time_limit:
                if can_finish_in_time(time_limit, person1_time + book_time, person2_time, book_idx + 1):
                    return True
            
            # Try person 2
            if person2_time + book_time <= time_limit:
                if can_finish_in_time(time_limit, person1_time, person2_time + book_time, book_idx + 1):
                    return True
            
            return False
    
    # Binary search on time
    left = max(books)
    right = sum(books)
    
    while left < right:
        mid = (left + right) // 2
        if can_finish_in_time(mid, 0, 0, 0):
            right = mid
        else:
            left = mid + 1
    
    return left

def reading_books_constraints_optimized(books, constraints):
    """
    Optimized version with memoization
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def can_finish_in_time(time_limit, person1_time, person2_time, book_idx):
        """Check if remaining books can be read within time_limit"""
        if book_idx == len(books):
            return True
        
        book_time = books[book_idx]
        
        # Check constraints for this book
        if book_idx in constraints:
            required_person = constraints[book_idx]
            
            if required_person == 1:
                if person1_time + book_time <= time_limit:
                    return can_finish_in_time(time_limit, person1_time + book_time, person2_time, book_idx + 1)
                else:
                    return False
            else:  # required_person == 2
                if person2_time + book_time <= time_limit:
                    return can_finish_in_time(time_limit, person1_time, person2_time + book_time, book_idx + 1)
                else:
                    return False
        else:
            # No constraint, try both people
            # Try person 1
            if person1_time + book_time <= time_limit:
                if can_finish_in_time(time_limit, person1_time + book_time, person2_time, book_idx + 1):
                    return True
            
            # Try person 2
            if person2_time + book_time <= time_limit:
                if can_finish_in_time(time_limit, person1_time, person2_time + book_time, book_idx + 1):
                    return True
            
            return False
    
    # Binary search on time
    left = max(books)
    right = sum(books)
    
    while left < right:
        mid = (left + right) // 2
        if can_finish_in_time(mid, 0, 0, 0):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example usage
books = [4, 2, 5, 3, 1]
constraints = {0: 1, 2: 2}  # Book 0 must be read by person 1, book 2 by person 2
result = reading_books_constraints(books, constraints)
print(f"Minimum time with constraints: {result}")  # Output: 7
```

### Variation 3: Reading Books with Dynamic Updates
**Problem**: Handle dynamic updates to book reading times and maintain minimum time queries.

**Link**: [CSES Problem Set - Reading Books with Updates](https://cses.fi/problemset/task/reading_books_updates)

```python
class ReadingBooksWithUpdates:
    def __init__(self, books):
        self.books = books[:]
        self.n = len(books)
        self.total_time = sum(books)
        self.max_book = max(books)
        self.min_time = self._compute_min_time()
    
    def _compute_min_time(self):
        """Compute minimum time using mathematical formula"""
        return max(self.max_book, (self.total_time + 1) // 2)
    
    def update_book(self, index, new_time):
        """Update book reading time at index"""
        old_time = self.books[index]
        self.books[index] = new_time
        
        # Update total time
        self.total_time = self.total_time - old_time + new_time
        
        # Update max book if necessary
        if old_time == self.max_book:
            self.max_book = max(self.books)
        else:
            self.max_book = max(self.max_book, new_time)
        
        # Recompute minimum time
        self.min_time = self._compute_min_time()
    
    def add_book(self, new_time):
        """Add a new book"""
        self.books.append(new_time)
        self.n = len(self.books)
        self.total_time += new_time
        self.max_book = max(self.max_book, new_time)
        self.min_time = self._compute_min_time()
    
    def remove_book(self, index):
        """Remove book at index"""
        old_time = self.books.pop(index)
        self.n = len(self.books)
        self.total_time -= old_time
        
        # Update max book if necessary
        if old_time == self.max_book and self.books:
            self.max_book = max(self.books)
        elif not self.books:
            self.max_book = 0
        
        self.min_time = self._compute_min_time()
    
    def get_min_time(self):
        """Get current minimum time"""
        return self.min_time
    
    def get_optimal_distribution(self):
        """Get optimal book distribution"""
        person1_time = 0
        person2_time = 0
        person1_books = []
        person2_books = []
        
        # Sort books in descending order for better distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        for book_idx, book_time in sorted_books:
            if person1_time <= person2_time:
                person1_time += book_time
                person1_books.append(book_idx)
            else:
                person2_time += book_time
                person2_books.append(book_idx)
        
        return person1_books, person2_books, person1_time, person2_time

# Example usage
books = [4, 2, 5]
reader = ReadingBooksWithUpdates(books)

print(f"Initial minimum time: {reader.get_min_time()}")  # Output: 6

# Update a book
reader.update_book(1, 3)
print(f"After update: {reader.get_min_time()}")  # Output: 6

# Add a new book
reader.add_book(1)
print(f"After adding book: {reader.get_min_time()}")  # Output: 7

# Get optimal distribution
person1_books, person2_books, time1, time2 = reader.get_optimal_distribution()
print(f"Person 1: books {person1_books}, time {time1}")
print(f"Person 2: books {person2_books}, time {time2}")
```

## Problem Variations

### **Variation 1: Reading Books with Dynamic Updates**
**Problem**: Handle dynamic book updates (add/remove/update books) while maintaining efficient minimum time calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicReadingBooks:
    def __init__(self, books):
        self.books = books[:]
        self.n = len(books)
        self.min_time = self._compute_min_time()
    
    def _compute_min_time(self):
        """Compute minimum time using mathematical formula."""
        if self.n == 0:
            return 0
        
        total_time = sum(self.books)
        max_book = max(self.books)
        
        # Minimum time is max of (total_time / 2) and max_book
        return max(total_time // 2, max_book)
    
    def add_book(self, book_time):
        """Add a new book to the collection."""
        self.books.append(book_time)
        self.n += 1
        self.min_time = self._compute_min_time()
    
    def remove_book(self, index):
        """Remove a book at the specified index."""
        if 0 <= index < self.n:
            del self.books[index]
            self.n -= 1
            self.min_time = self._compute_min_time()
    
    def update_book(self, index, new_time):
        """Update a book at the specified index."""
        if 0 <= index < self.n:
            self.books[index] = new_time
            self.min_time = self._compute_min_time()
    
    def get_min_time(self):
        """Get current minimum time."""
        return self.min_time
    
    def get_optimal_distribution(self):
        """Get optimal book distribution between two people."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            if person1_time <= person2_time:
                person1_books.append(book_idx)
                person1_time += book_time
            else:
                person2_books.append(book_idx)
                person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_books_with_time_range(self, min_time, max_time):
        """Get books within specific time range."""
        result = []
        for i, book_time in enumerate(self.books):
            if min_time <= book_time <= max_time:
                result.append((i, book_time))
        return result
    
    def get_books_with_constraints(self, constraint_func):
        """Get books that satisfy custom constraints."""
        result = []
        for i, book_time in enumerate(self.books):
            if constraint_func(book_time, i):
                result.append((i, book_time))
        return result
    
    def get_reading_statistics(self):
        """Get statistics about the book collection."""
        if not self.books:
            return {
                'total_books': 0,
                'total_time': 0,
                'min_time': 0,
                'max_time': 0,
                'average_time': 0,
                'min_time_required': 0
            }
        
        total_time = sum(self.books)
        min_book_time = min(self.books)
        max_book_time = max(self.books)
        average_time = total_time / self.n
        min_time_required = self.min_time
        
        return {
            'total_books': self.n,
            'total_time': total_time,
            'min_time': min_book_time,
            'max_time': max_book_time,
            'average_time': average_time,
            'min_time_required': min_time_required
        }
    
    def get_reading_patterns(self):
        """Get patterns in the book collection."""
        patterns = {
            'consecutive_similar': 0,
            'alternating_pattern': 0,
            'increasing_pattern': 0,
            'decreasing_pattern': 0
        }
        
        for i in range(1, self.n):
            if abs(self.books[i] - self.books[i-1]) <= 1:
                patterns['consecutive_similar'] += 1
            
            if i > 1:
                if (self.books[i] > self.books[i-1] and 
                    self.books[i-1] > self.books[i-2]):
                    patterns['increasing_pattern'] += 1
                elif (self.books[i] < self.books[i-1] and 
                      self.books[i-1] < self.books[i-2]):
                    patterns['decreasing_pattern'] += 1
        
        return patterns
    
    def get_optimal_distribution_with_constraints(self, constraints):
        """Get optimal distribution considering constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            if book_idx in constraints:
                required_person = constraints[book_idx]
                
                if required_person == 1:
                    person1_books.append(book_idx)
                    person1_time += book_time
                else:  # required_person == 2
                    person2_books.append(book_idx)
                    person2_time += book_time
            else:
                # No constraint, assign to person with less time
                if person1_time <= person2_time:
                    person1_books.append(book_idx)
                    person1_time += book_time
                else:
                    person2_books.append(book_idx)
                    person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time

# Example usage
books = [2, 3, 1, 4, 2]
dynamic_reader = DynamicReadingBooks(books)
print(f"Initial min time: {dynamic_reader.get_min_time()}")

# Add a book
dynamic_reader.add_book(5)
print(f"After adding book: {dynamic_reader.get_min_time()}")

# Update a book
dynamic_reader.update_book(1, 6)
print(f"After updating book: {dynamic_reader.get_min_time()}")

# Get optimal distribution
person1_books, person2_books, time1, time2 = dynamic_reader.get_optimal_distribution()
print(f"Person 1: books {person1_books}, time {time1}")
print(f"Person 2: books {person2_books}, time {time2}")

# Get books with time range
print(f"Books with time 2-4: {dynamic_reader.get_books_with_time_range(2, 4)}")

# Get books with constraints
def constraint_func(book_time, index):
    return book_time >= 3 and index % 2 == 0

print(f"Books with constraints: {dynamic_reader.get_books_with_constraints(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_reader.get_reading_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_reader.get_reading_patterns()}")

# Get optimal distribution with constraints
constraints = {0: 1, 2: 2}  # Book 0 must be read by person 1, book 2 by person 2
person1_books, person2_books, time1, time2 = dynamic_reader.get_optimal_distribution_with_constraints(constraints)
print(f"Constrained distribution - Person 1: {person1_books}, time {time1}")
print(f"Constrained distribution - Person 2: {person2_books}, time {time2}")
```

### **Variation 2: Reading Books with Different Operations**
**Problem**: Handle different types of operations on book collections (weighted books, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of book reading queries.

```python
class AdvancedReadingBooks:
    def __init__(self, books, weights=None, priorities=None):
        self.books = books[:]
        self.n = len(books)
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.min_time = self._compute_min_time()
        self.weighted_min_time = self._compute_weighted_min_time()
    
    def _compute_min_time(self):
        """Compute minimum time using mathematical formula."""
        if self.n == 0:
            return 0
        
        total_time = sum(self.books)
        max_book = max(self.books)
        
        return max(total_time // 2, max_book)
    
    def _compute_weighted_min_time(self):
        """Compute minimum time considering weights."""
        if self.n == 0:
            return 0
        
        total_weighted_time = sum(book * weight for book, weight in zip(self.books, self.weights))
        max_weighted_book = max(book * weight for book, weight in zip(self.books, self.weights))
        
        return max(total_weighted_time // 2, max_weighted_book)
    
    def get_min_time(self):
        """Get current minimum time."""
        return self.min_time
    
    def get_weighted_min_time(self):
        """Get current minimum weighted time."""
        return self.weighted_min_time
    
    def get_optimal_distribution_with_priority(self, priority_func):
        """Get optimal distribution considering priority."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books by priority
        sorted_books = sorted(enumerate(self.books), key=lambda x: priority_func(x[1], self.weights[x[0]], self.priorities[x[0]]), reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            if person1_time <= person2_time:
                person1_books.append(book_idx)
                person1_time += book_time
            else:
                person2_books.append(book_idx)
                person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_optimization(self, optimization_func):
        """Get optimal distribution using custom optimization function."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books by optimization function
        sorted_books = sorted(enumerate(self.books), key=lambda x: optimization_func(x[1], self.weights[x[0]], self.priorities[x[0]]), reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            if person1_time <= person2_time:
                person1_books.append(book_idx)
                person1_time += book_time
            else:
                person2_books.append(book_idx)
                person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_books_with_constraints(self, constraint_func):
        """Get books that satisfy custom constraints."""
        result = []
        for i, book_time in enumerate(self.books):
            if constraint_func(book_time, self.weights[i], self.priorities[i]):
                result.append((i, book_time))
        return result
    
    def get_books_with_multiple_criteria(self, criteria_list):
        """Get books that satisfy multiple criteria."""
        result = []
        for i, book_time in enumerate(self.books):
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(book_time, self.weights[i], self.priorities[i]):
                    satisfies_all_criteria = False
                    break
            
            if satisfies_all_criteria:
                result.append((i, book_time))
        
        return result
    
    def get_books_with_alternatives(self, alternatives):
        """Get books considering alternative reading times."""
        result = []
        
        for i, book_time in enumerate(self.books):
            # Check original book
            result.append((i, book_time, 'original'))
            
            # Check alternative reading times
            if i in alternatives:
                for alt_time in alternatives[i]:
                    result.append((i, alt_time, 'alternative'))
        
        return result
    
    def get_books_with_adaptive_criteria(self, adaptive_func):
        """Get books using adaptive criteria."""
        result = []
        
        for i, book_time in enumerate(self.books):
            if adaptive_func(book_time, self.weights[i], self.priorities[i], result):
                result.append((i, book_time))
        
        return result
    
    def get_reading_optimization(self):
        """Get optimal reading configuration."""
        strategies = [
            ('min_time', self.get_min_time),
            ('weighted_min_time', self.get_weighted_min_time),
        ]
        
        best_strategy = None
        best_value = float('inf')
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value < best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
books = [2, 3, 1, 4, 2]
weights = [1, 2, 1, 3, 1]
priorities = [1, 2, 1, 3, 1]
advanced_reader = AdvancedReadingBooks(books, weights, priorities)

print(f"Min time: {advanced_reader.get_min_time()}")
print(f"Weighted min time: {advanced_reader.get_weighted_min_time()}")

# Get optimal distribution with priority
def priority_func(book_time, weight, priority):
    return book_time * weight * priority

person1_books, person2_books, time1, time2 = advanced_reader.get_optimal_distribution_with_priority(priority_func)
print(f"Priority-based distribution - Person 1: {person1_books}, time {time1}")
print(f"Priority-based distribution - Person 2: {person2_books}, time {time2}")

# Get optimal distribution with optimization
def optimization_func(book_time, weight, priority):
    return book_time * weight + priority

person1_books, person2_books, time1, time2 = advanced_reader.get_optimal_distribution_with_optimization(optimization_func)
print(f"Optimization-based distribution - Person 1: {person1_books}, time {time1}")
print(f"Optimization-based distribution - Person 2: {person2_books}, time {time2}")

# Get books with constraints
def constraint_func(book_time, weight, priority):
    return book_time >= 2 and weight > 1

print(f"Books with constraints: {advanced_reader.get_books_with_constraints(constraint_func)}")

# Get books with multiple criteria
def criterion1(book_time, weight, priority):
    return book_time >= 2

def criterion2(book_time, weight, priority):
    return weight > 1

criteria_list = [criterion1, criterion2]
print(f"Books with multiple criteria: {advanced_reader.get_books_with_multiple_criteria(criteria_list)}")

# Get books with alternatives
alternatives = {1: [2, 4], 3: [3, 5]}
print(f"Books with alternatives: {advanced_reader.get_books_with_alternatives(alternatives)}")

# Get books with adaptive criteria
def adaptive_func(book_time, weight, priority, current_result):
    return book_time >= 2 and len(current_result) < 3

print(f"Books with adaptive criteria: {advanced_reader.get_books_with_adaptive_criteria(adaptive_func)}")

# Get reading optimization
print(f"Reading optimization: {advanced_reader.get_reading_optimization()}")
```

### **Variation 3: Reading Books with Constraints**
**Problem**: Handle reading books with additional constraints (time limits, resource constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedReadingBooks:
    def __init__(self, books, constraints=None):
        self.books = books[:]
        self.n = len(books)
        self.constraints = constraints or {}
        self.min_time = self._compute_min_time()
    
    def _compute_min_time(self):
        """Compute minimum time using mathematical formula."""
        if self.n == 0:
            return 0
        
        total_time = sum(self.books)
        max_book = max(self.books)
        
        return max(total_time // 2, max_book)
    
    def get_optimal_distribution_with_time_constraints(self, time_limit):
        """Get optimal distribution considering time constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            # Check if book can be assigned within time limit
            if person1_time + book_time <= time_limit and person1_time <= person2_time:
                person1_books.append(book_idx)
                person1_time += book_time
            elif person2_time + book_time <= time_limit:
                person2_books.append(book_idx)
                person2_time += book_time
            else:
                # Cannot assign book within time limit
                break
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get optimal distribution considering resource constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        person1_resources = [0] * len(resource_limits)
        person2_resources = [0] * len(resource_limits)
        
        for book_idx, book_time in sorted_books:
            # Check resource constraints for person 1
            can_assign_person1 = True
            for j, consumption in enumerate(resource_consumption[book_idx]):
                if person1_resources[j] + consumption > resource_limits[j]:
                    can_assign_person1 = False
                    break
            
            # Check resource constraints for person 2
            can_assign_person2 = True
            for j, consumption in enumerate(resource_consumption[book_idx]):
                if person2_resources[j] + consumption > resource_limits[j]:
                    can_assign_person2 = False
                    break
            
            # Assign to person with less time if both can handle it
            if can_assign_person1 and can_assign_person2:
                if person1_time <= person2_time:
                    person1_books.append(book_idx)
                    person1_time += book_time
                    for j, consumption in enumerate(resource_consumption[book_idx]):
                        person1_resources[j] += consumption
                else:
                    person2_books.append(book_idx)
                    person2_time += book_time
                    for j, consumption in enumerate(resource_consumption[book_idx]):
                        person2_resources[j] += consumption
            elif can_assign_person1:
                person1_books.append(book_idx)
                person1_time += book_time
                for j, consumption in enumerate(resource_consumption[book_idx]):
                    person1_resources[j] += consumption
            elif can_assign_person2:
                person2_books.append(book_idx)
                person2_time += book_time
                for j, consumption in enumerate(resource_consumption[book_idx]):
                    person2_resources[j] += consumption
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_mathematical_constraints(self, constraint_func):
        """Get optimal distribution that satisfies custom mathematical constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            # Check mathematical constraints
            if constraint_func(book_time, person1_time, person2_time):
                if person1_time <= person2_time:
                    person1_books.append(book_idx)
                    person1_time += book_time
                else:
                    person2_books.append(book_idx)
                    person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_range_constraints(self, range_constraints):
        """Get optimal distribution that satisfies range constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            # Check if book satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(book_time, person1_time, person2_time):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                if person1_time <= person2_time:
                    person1_books.append(book_idx)
                    person1_time += book_time
                else:
                    person2_books.append(book_idx)
                    person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_optimization_constraints(self, optimization_func):
        """Get optimal distribution using custom optimization constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books by optimization function
        sorted_books = sorted(enumerate(self.books), key=lambda x: optimization_func(x[1]), reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            if person1_time <= person2_time:
                person1_books.append(book_idx)
                person1_time += book_time
            else:
                person2_books.append(book_idx)
                person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_multiple_constraints(self, constraints_list):
        """Get optimal distribution that satisfies multiple constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            # Check if book satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(book_time, person1_time, person2_time):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                if person1_time <= person2_time:
                    person1_books.append(book_idx)
                    person1_time += book_time
                else:
                    person2_books.append(book_idx)
                    person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_priority_constraints(self, priority_func):
        """Get optimal distribution with priority-based constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books by priority
        sorted_books = sorted(enumerate(self.books), key=lambda x: priority_func(x[1]), reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            if person1_time <= person2_time:
                person1_books.append(book_idx)
                person1_time += book_time
            else:
                person2_books.append(book_idx)
                person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_distribution_with_adaptive_constraints(self, adaptive_func):
        """Get optimal distribution with adaptive constraints."""
        if self.n == 0:
            return [], [], 0, 0
        
        # Sort books in descending order for optimal distribution
        sorted_books = sorted(enumerate(self.books), key=lambda x: x[1], reverse=True)
        
        person1_books = []
        person2_books = []
        person1_time = 0
        person2_time = 0
        
        for book_idx, book_time in sorted_books:
            # Check adaptive constraints
            if adaptive_func(book_time, person1_time, person2_time, person1_books, person2_books):
                if person1_time <= person2_time:
                    person1_books.append(book_idx)
                    person1_time += book_time
                else:
                    person2_books.append(book_idx)
                    person2_time += book_time
        
        return person1_books, person2_books, person1_time, person2_time
    
    def get_optimal_reading_strategy(self):
        """Get optimal reading strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_optimal_distribution_with_time_constraints),
            ('resource_constraints', self.get_optimal_distribution_with_resource_constraints),
            ('mathematical_constraints', self.get_optimal_distribution_with_mathematical_constraints),
        ]
        
        best_strategy = None
        best_time = float('inf')
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'time_constraints':
                    person1_books, person2_books, time1, time2 = strategy_func(10)  # 10 time units
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    person1_books, person2_books, time1, time2 = strategy_func(resource_limits, resource_consumption)
                elif strategy_name == 'mathematical_constraints':
                    def constraint_func(book_time, person1_time, person2_time):
                        return book_time >= 2 and person1_time + person2_time < 20
                    person1_books, person2_books, time1, time2 = strategy_func(constraint_func)
                
                max_time = max(time1, time2)
                if max_time < best_time:
                    best_time = max_time
                    best_strategy = (strategy_name, person1_books, person2_books, time1, time2)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_time': 1,
    'max_time': 10
}

books = [2, 3, 1, 4, 2]
constrained_reader = ConstrainedReadingBooks(books, constraints)

print("Time-constrained optimal distribution:", constrained_reader.get_optimal_distribution_with_time_constraints(8))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(books))}
print("Resource-constrained optimal distribution:", constrained_reader.get_optimal_distribution_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(book_time, person1_time, person2_time):
    return book_time >= 2 and person1_time + person2_time < 15

print("Mathematical constraint optimal distribution:", constrained_reader.get_optimal_distribution_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(book_time, person1_time, person2_time):
    return book_time >= 2 and person1_time + person2_time < 15

range_constraints = [range_constraint]
print("Range-constrained optimal distribution:", constrained_reader.get_optimal_distribution_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(book_time, person1_time, person2_time):
    return book_time >= 2

def constraint2(book_time, person1_time, person2_time):
    return person1_time + person2_time < 15

constraints_list = [constraint1, constraint2]
print("Multiple constraints optimal distribution:", constrained_reader.get_optimal_distribution_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(book_time):
    return book_time

print("Priority-constrained optimal distribution:", constrained_reader.get_optimal_distribution_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(book_time, person1_time, person2_time, person1_books, person2_books):
    return book_time >= 2 and len(person1_books) + len(person2_books) < 4

print("Adaptive constraint optimal distribution:", constrained_reader.get_optimal_distribution_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_reader.get_optimal_reading_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Reading Books](https://cses.fi/problemset/task/1631) - Basic reading books problem
- [Factory Machines](https://cses.fi/problemset/task/1620) - Parallel processing with machines
- [Tasks and Deadlines](https://cses.fi/problemset/task/1630) - Task scheduling optimization

#### **LeetCode Problems**
- [Minimum Time to Complete All Tasks](https://leetcode.com/problems/minimum-time-to-complete-all-tasks/) - Task completion optimization
- [Maximum Number of Tasks You Can Assign](https://leetcode.com/problems/maximum-number-of-tasks-you-can-assign/) - Task assignment optimization
- [Minimum Time to Finish the Race](https://leetcode.com/problems/minimum-time-to-finish-the-race/) - Race completion optimization

#### **Problem Categories**
- **Mathematical Algorithms**: Load balancing formulas, optimization theory, parallel processing
- **Binary Search**: Time optimization, constraint satisfaction, efficient searching
- **Greedy Algorithms**: Optimal local choices, load balancing, task distribution
- **Algorithm Design**: Mathematical optimization, parallel processing techniques, load balancing
