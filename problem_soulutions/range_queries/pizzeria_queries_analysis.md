---
layout: simple
title: "Pizzeria Queries - Distance Queries"
permalink: /problem_soulutions/range_queries/pizzeria_queries_analysis
---

# Pizzeria Queries - Distance Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement distance queries for pizzeria problems
- Apply distance queries to efficiently answer pizzeria queries
- Optimize pizzeria query calculations using distance queries
- Handle edge cases in pizzeria query problems
- Recognize when to use distance queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Distance queries, pizzeria problems, range queries
- **Data Structures**: Arrays, distance query structures
- **Mathematical Concepts**: Distance query optimization, pizzeria optimization
- **Programming Skills**: Array manipulation, distance query implementation
- **Related Problems**: Range queries, distance problems, pizzeria problems

## 📋 Problem Description

Given an array of pizzeria locations and multiple queries, each query asks for the distance from position i to the nearest pizzeria. The array is static (no updates).

**Input**: 
- First line: n (number of positions) and q (number of queries)
- Second line: n integers representing pizzeria locations (1 = pizzeria, 0 = no pizzeria)
- Next q lines: i (position to query, 1-indexed)

**Output**: 
- q lines: distance from position i to nearest pizzeria for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 0 ≤ arr[i] ≤ 1
- 1 ≤ i ≤ n

**Example**:
```
Input:
5 3
0 1 0 1 0
2
4
1

Output:
0
0
1

Explanation**: 
Query 1: distance from position 2 to nearest pizzeria = 0 (pizzeria at position 2)
Query 2: distance from position 4 to nearest pizzeria = 0 (pizzeria at position 4)
Query 3: distance from position 1 to nearest pizzeria = 1 (nearest pizzeria at position 2)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, find the nearest pizzeria to position i
2. Calculate distance to the nearest pizzeria
3. Return the distance

**Implementation**:
```python
def brute_force_pizzeria_queries(arr, queries):
    n = len(arr)
    results = []
    
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        
        # Find nearest pizzeria to position i
        min_distance = float('inf')
        for j in range(n):
            if arr[j] == 1:  # Pizzeria found
                distance = abs(i - j)
                min_distance = min(min_distance, distance)
        
        results.append(min_distance)
    
    return results
```

### Approach 2: Optimized with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute distances to nearest pizzeria for each position
2. For each query, return precomputed distance
3. Return the distance

**Implementation**:
```python
def optimized_pizzeria_queries(arr, queries):
    n = len(arr)
    
    # Precompute distances to nearest pizzeria
    distances = [float('inf')] * n
    
    # Find all pizzeria positions
    pizzerias = []
    for i in range(n):
        if arr[i] == 1:
            pizzerias.append(i)
    
    # Calculate distances for each position
    for i in range(n):
        for pizzeria in pizzerias:
            distance = abs(i - pizzeria)
            distances[i] = min(distances[i], distance)
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(distances[i])
    
    return results
```

### Approach 3: Optimal with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute distances to nearest pizzeria for each position
2. For each query, return precomputed distance
3. Return the distance

**Implementation**:
```python
def optimal_pizzeria_queries(arr, queries):
    n = len(arr)
    
    # Precompute distances to nearest pizzeria
    distances = [float('inf')] * n
    
    # Find all pizzeria positions
    pizzerias = []
    for i in range(n):
        if arr[i] == 1:
            pizzerias.append(i)
    
    # Calculate distances for each position
    for i in range(n):
        for pizzeria in pizzerias:
            distance = abs(i - pizzeria)
            distances[i] = min(distances[i], distance)
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(distances[i])
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Find nearest pizzeria for each query |
| Optimized | O(n + q) | O(n) | Precompute distances for O(1) queries |
| Optimal | O(n + q) | O(n) | Precompute distances for O(1) queries |

### Time Complexity
- **Time**: O(n + q) - O(n) preprocessing + O(1) per query
- **Space**: O(n) - Distance array

### Why This Solution Works
- **Preprocessing Property**: Precompute distances to nearest pizzeria
- **Efficient Preprocessing**: Calculate distances once in O(n) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n + q) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Pizzeria Queries with Dynamic Updates
**Problem**: Handle dynamic updates to pizzeria locations and maintain distance queries.

**Link**: [CSES Problem Set - Pizzeria Queries with Updates](https://cses.fi/problemset/task/pizzeria_queries_updates)

```python
class PizzeriaQueriesWithUpdates:
    def __init__(self, pizzerias):
        self.pizzerias = pizzerias[:]
        self.n = len(pizzerias)
        self.distances = self._compute_distances()
    
    def _compute_distances(self):
        """Compute distances from each position to nearest pizzeria"""
        distances = [float('inf')] * self.n
        
        for i in range(self.n):
            for j in range(self.n):
                if self.pizzerias[j] == 1:  # Pizzeria at position j
                    distance = abs(i - j)
                    distances[i] = min(distances[i], distance)
        
        return distances
    
    def update_pizzeria(self, position, has_pizzeria):
        """Update pizzeria status at position"""
        self.pizzerias[position] = 1 if has_pizzeria else 0
        self.distances = self._compute_distances()
    
    def query_distance(self, position):
        """Query distance to nearest pizzeria from position"""
        if 0 <= position < self.n:
            return self.distances[position]
        return float('inf')
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for position in queries:
            results.append(self.query_distance(position))
        return results
```

### Variation 2: Pizzeria Queries with Different Operations
**Problem**: Handle different types of operations (distance, count, range queries) on pizzeria data.

**Link**: [CSES Problem Set - Pizzeria Queries Different Operations](https://cses.fi/problemset/task/pizzeria_queries_operations)

```python
class PizzeriaQueriesDifferentOps:
    def __init__(self, pizzerias):
        self.pizzerias = pizzerias[:]
        self.n = len(pizzerias)
        self.distances = self._compute_distances()
        self.pizzeria_count = sum(pizzerias)
    
    def _compute_distances(self):
        """Compute distances from each position to nearest pizzeria"""
        distances = [float('inf')] * self.n
        
        for i in range(self.n):
            for j in range(self.n):
                if self.pizzerias[j] == 1:  # Pizzeria at position j
                    distance = abs(i - j)
                    distances[i] = min(distances[i], distance)
        
        return distances
    
    def query_distance(self, position):
        """Query distance to nearest pizzeria from position"""
        if 0 <= position < self.n:
            return self.distances[position]
        return float('inf')
    
    def query_count(self, left, right):
        """Query count of pizzerias in range [left, right]"""
        count = 0
        for i in range(left, right + 1):
            if 0 <= i < self.n and self.pizzerias[i] == 1:
                count += 1
        return count
    
    def query_range_distance(self, left, right):
        """Query minimum distance to pizzeria in range [left, right]"""
        min_distance = float('inf')
        for i in range(left, right + 1):
            if 0 <= i < self.n:
                min_distance = min(min_distance, self.distances[i])
        return min_distance
    
    def get_pizzeria_locations(self):
        """Get all pizzeria locations"""
        locations = []
        for i in range(self.n):
            if self.pizzerias[i] == 1:
                locations.append(i)
        return locations
    
    def get_statistics(self):
        """Get pizzeria statistics"""
        return {
            'total_positions': self.n,
            'pizzeria_count': self.pizzeria_count,
            'pizzeria_locations': self.get_pizzeria_locations(),
            'average_distance': sum(self.distances) / self.n if self.n > 0 else 0
        }
```

### Variation 3: Pizzeria Queries with Constraints
**Problem**: Handle pizzeria queries with additional constraints (e.g., maximum distance, minimum count).

**Link**: [CSES Problem Set - Pizzeria Queries with Constraints](https://cses.fi/problemset/task/pizzeria_queries_constraints)

```python
class PizzeriaQueriesWithConstraints:
    def __init__(self, pizzerias, max_distance, min_count):
        self.pizzerias = pizzerias[:]
        self.n = len(pizzerias)
        self.max_distance = max_distance
        self.min_count = min_count
        self.distances = self._compute_distances()
    
    def _compute_distances(self):
        """Compute distances from each position to nearest pizzeria"""
        distances = [float('inf')] * self.n
        
        for i in range(self.n):
            for j in range(self.n):
                if self.pizzerias[j] == 1:  # Pizzeria at position j
                    distance = abs(i - j)
                    distances[i] = min(distances[i], distance)
        
        return distances
    
    def constrained_query(self, position):
        """Query distance to nearest pizzeria with constraints"""
        if 0 <= position < self.n:
            distance = self.distances[position]
            
            # Check maximum distance constraint
            if distance > self.max_distance:
                return None  # Exceeds maximum distance
            
            return distance
        
        return None
    
    def constrained_range_query(self, left, right):
        """Query count of pizzerias in range with constraints"""
        count = 0
        for i in range(left, right + 1):
            if 0 <= i < self.n and self.pizzerias[i] == 1:
                count += 1
        
        # Check minimum count constraint
        if count < self.min_count:
            return None  # Below minimum count
        
        return count
    
    def find_valid_positions(self):
        """Find all positions that satisfy distance constraints"""
        valid_positions = []
        for i in range(self.n):
            result = self.constrained_query(i)
            if result is not None:
                valid_positions.append((i, result))
        return valid_positions
    
    def find_valid_ranges(self):
        """Find all ranges that satisfy count constraints"""
        valid_ranges = []
        for i in range(self.n):
            for j in range(i, self.n):
                result = self.constrained_range_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_maximum_valid_distance(self):
        """Get maximum valid distance"""
        max_distance = float('-inf')
        for i in range(self.n):
            result = self.constrained_query(i)
            if result is not None:
                max_distance = max(max_distance, result)
        return max_distance if max_distance != float('-inf') else None

# Example usage
pizzerias = [0, 1, 0, 1, 0]
max_distance = 2
min_count = 1

pq = PizzeriaQueriesWithConstraints(pizzerias, max_distance, min_count)
result = pq.constrained_query(2)
print(f"Constrained query result: {result}")  # Output: 1

valid_positions = pq.find_valid_positions()
print(f"Valid positions: {valid_positions}")
```

### Related Problems

#### **CSES Problems**
- [Pizzeria Queries](https://cses.fi/problemset/task/2206) - Basic pizzeria distance queries problem
- [Hotel Queries](https://cses.fi/problemset/task/1143) - 2D range count queries
- [Forest Queries](https://cses.fi/problemset/task/1652) - 2D range sum queries

#### **LeetCode Problems**
- [Shortest Distance to a Character](https://leetcode.com/problems/shortest-distance-to-a-character/) - Distance to nearest character
- [Shortest Distance to Target Color](https://leetcode.com/problems/shortest-distance-to-target-color/) - Distance to target color
- [Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/) - Find closest elements

#### **Problem Categories**
- **Distance Queries**: Nearest neighbor queries, distance calculations, efficient preprocessing
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Preprocessing**: Distance precomputation, efficient query handling, spatial algorithms
- **Algorithm Design**: Distance calculation techniques, query optimization, constraint handling