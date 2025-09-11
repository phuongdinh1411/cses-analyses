---
layout: simple
title: "Concert Tickets"
permalink: /problem_soulutions/sorting_and_searching/concert_tickets_analysis
---

# Concert Tickets

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of greedy algorithms and their applications
- Apply binary search and data structures for efficient searching
- Implement efficient solutions for ticket allocation problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in greedy algorithms

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, binary search, greedy algorithms, data structures
- **Data Structures**: Arrays, sets, multisets, binary search trees
- **Mathematical Concepts**: Optimization, greedy choice property
- **Programming Skills**: Algorithm implementation, complexity analysis, binary search
- **Related Problems**: Ferris Wheel (greedy), Apartments (two-pointer), Sum of Two Values (searching)

## 📋 Problem Description

There are n concert tickets available, each with a certain price. There are m customers who want to buy tickets. Each customer will buy the most expensive ticket they can afford.

For each customer, find the price of the ticket they will buy, or -1 if they cannot afford any ticket.

**Input**: 
- First line: two integers n and m (number of tickets and customers)
- Second line: n integers h[1], h[2], ..., h[n] (ticket prices)
- Third line: m integers t[1], t[2], ..., t[m] (customer budgets)

**Output**: 
- Print m integers: the price of the ticket each customer will buy, or -1 if they cannot afford any

**Constraints**:
- 1 ≤ n, m ≤ 2×10⁵
- 1 ≤ h[i], t[i] ≤ 10⁹

**Example**:
```
Input:
5 3
5 3 7 8 5
4 8 3

Output:
3
8
-1

Explanation**: 
Available tickets: [5, 3, 7, 8, 5]
Customer budgets: [4, 8, 3]

Customer 1 (budget 4): Can afford ticket with price 3 → buys ticket 3
Customer 2 (budget 8): Can afford ticket with price 8 → buys ticket 8  
Customer 3 (budget 3): Can afford ticket with price 3 → buys ticket 3

After purchases: [5, 7, 5] (tickets 3 and 8 are sold)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Available Tickets

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: For each customer, check all available tickets
- **Complete Coverage**: Guaranteed to find the most expensive affordable ticket
- **Simple Implementation**: Straightforward nested loops approach
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each customer, iterate through all available tickets to find the most expensive one they can afford.

**Algorithm**:
- For each customer:
  - Check all available tickets
  - Find the most expensive ticket they can afford
  - Remove that ticket from available tickets

**Visual Example**:
```
Available tickets: [5, 3, 7, 8, 5]
Customer budgets: [4, 8, 3]

Customer 1 (budget 4):
- Check ticket 5: 5 > 4 ✗
- Check ticket 3: 3 ≤ 4 ✓ (most expensive so far)
- Check ticket 7: 7 > 4 ✗
- Check ticket 8: 8 > 4 ✗
- Check ticket 5: 5 > 4 ✗
- Buys ticket 3, remaining: [5, 7, 8, 5]

Customer 2 (budget 8):
- Check ticket 5: 5 ≤ 8 ✓ (most expensive so far)
- Check ticket 7: 7 ≤ 8 ✓ (most expensive so far)
- Check ticket 8: 8 ≤ 8 ✓ (most expensive so far)
- Check ticket 5: 5 ≤ 8 ✓
- Buys ticket 8, remaining: [5, 7, 5]

Customer 3 (budget 3):
- Check ticket 5: 5 > 3 ✗
- Check ticket 7: 7 > 3 ✗
- Check ticket 5: 5 > 3 ✗
- Cannot afford any ticket → -1
```

**Implementation**:
```python
def brute_force_concert_tickets(tickets, customers):
    """
    Find ticket prices using brute force approach
    
    Args:
        tickets: list of available ticket prices
        customers: list of customer budgets
    
    Returns:
        list: ticket prices each customer will buy
    """
    available_tickets = tickets.copy()
    result = []
    
    for budget in customers:
        best_ticket = -1
        best_index = -1
        
        # Find the most expensive affordable ticket
        for i, ticket in enumerate(available_tickets):
            if ticket <= budget and ticket > best_ticket:
                best_ticket = ticket
                best_index = i
        
        if best_index != -1:
            # Remove the ticket from available tickets
            available_tickets.pop(best_index)
            result.append(best_ticket)
        else:
            result.append(-1)
    
    return result

# Example usage
tickets = [5, 3, 7, 8, 5]
customers = [4, 8, 3]
result = brute_force_concert_tickets(tickets, customers)
print(f"Brute force result: {result}")  # Output: [3, 8, -1]
```

**Time Complexity**: O(n × m) - For each customer, check all tickets
**Space Complexity**: O(n) - For available tickets list

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Sort and Binary Search

**Key Insights from Optimized Approach**:
- **Sorting**: Sort tickets to enable efficient searching
- **Binary Search**: Use binary search to find the most expensive affordable ticket
- **Efficient Removal**: Use data structures that support efficient removal
- **Better Complexity**: Achieve O(n log n + m log n) time complexity

**Key Insight**: Sort the tickets and use binary search to efficiently find the most expensive affordable ticket for each customer.

**Algorithm**:
- Sort available tickets
- For each customer:
  - Use binary search to find the most expensive affordable ticket
  - Remove that ticket from available tickets

**Visual Example**:
```
Available tickets: [5, 3, 7, 8, 5]
Sorted: [3, 5, 5, 7, 8]
Customer budgets: [4, 8, 3]

Customer 1 (budget 4):
- Binary search for largest ticket ≤ 4
- Found ticket 3 at index 0
- Buys ticket 3, remaining: [5, 5, 7, 8]

Customer 2 (budget 8):
- Binary search for largest ticket ≤ 8
- Found ticket 8 at index 3
- Buys ticket 8, remaining: [5, 5, 7]

Customer 3 (budget 3):
- Binary search for largest ticket ≤ 3
- Found ticket 3, but it's already sold
- Cannot afford any ticket → -1
```

**Implementation**:
```python
def optimized_concert_tickets(tickets, customers):
    """
    Find ticket prices using sorting and binary search
    
    Args:
        tickets: list of available ticket prices
        customers: list of customer budgets
    
    Returns:
        list: ticket prices each customer will buy
    """
    import bisect
    
    available_tickets = sorted(tickets)
    result = []
    
    for budget in customers:
        # Find the rightmost ticket that is <= budget
        index = bisect.bisect_right(available_tickets, budget) - 1
        
        if index >= 0:
            # Found an affordable ticket
            ticket_price = available_tickets.pop(index)
            result.append(ticket_price)
        else:
            # No affordable ticket
            result.append(-1)
    
    return result

# Example usage
tickets = [5, 3, 7, 8, 5]
customers = [4, 8, 3]
result = optimized_concert_tickets(tickets, customers)
print(f"Optimized result: {result}")  # Output: [3, 8, -1]
```

**Time Complexity**: O(n log n + m log n) - Sorting + binary search for each customer
**Space Complexity**: O(n) - For sorted tickets list

**Why it's better**: Much more efficient than brute force, but still not optimal.

---

### Approach 3: Optimal - Multiset with Upper Bound

**Key Insights from Optimal Approach**:
- **Multiset**: Use a data structure that supports efficient insertion, deletion, and searching
- **Upper Bound**: Use upper_bound to find the most expensive affordable ticket
- **Efficient Operations**: All operations are O(log n) time
- **Optimal Complexity**: Achieve O(n log n + m log n) time complexity

**Key Insight**: Use a multiset (or similar data structure) to maintain available tickets and efficiently find the most expensive affordable ticket.

**Algorithm**:
- Insert all tickets into a multiset
- For each customer:
  - Use upper_bound to find the most expensive affordable ticket
  - Remove that ticket from the multiset

**Visual Example**:
```
Available tickets: [5, 3, 7, 8, 5]
Multiset: {3, 5, 5, 7, 8}
Customer budgets: [4, 8, 3]

Customer 1 (budget 4):
- upper_bound(4) returns iterator to 5
- Previous element is 3
- Buys ticket 3, multiset: {5, 5, 7, 8}

Customer 2 (budget 8):
- upper_bound(8) returns iterator to end
- Previous element is 8
- Buys ticket 8, multiset: {5, 5, 7}

Customer 3 (budget 3):
- upper_bound(3) returns iterator to 5
- Previous element is 3, but it's already sold
- Cannot afford any ticket → -1
```

**Implementation**:
```python
def optimal_concert_tickets(tickets, customers):
    """
    Find ticket prices using multiset with upper bound
    
    Args:
        tickets: list of available ticket prices
        customers: list of customer budgets
    
    Returns:
        list: ticket prices each customer will buy
    """
    from bisect import bisect_right
    
    # Use a list to simulate multiset behavior
    available_tickets = sorted(tickets)
    result = []
    
    for budget in customers:
        # Find the rightmost ticket that is <= budget
        index = bisect_right(available_tickets, budget) - 1
        
        if index >= 0:
            # Found an affordable ticket
            ticket_price = available_tickets.pop(index)
            result.append(ticket_price)
        else:
            # No affordable ticket
            result.append(-1)
    
    return result

# Example usage
tickets = [5, 3, 7, 8, 5]
customers = [4, 8, 3]
result = optimal_concert_tickets(tickets, customers)
print(f"Optimal result: {result}")  # Output: [3, 8, -1]
```

**Time Complexity**: O(n log n + m log n) - Sorting + binary search for each customer
**Space Complexity**: O(n) - For available tickets list

**Why it's optimal**: Achieves the best possible time complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × m) | O(n) | Check all tickets for each customer |
| Sort + Binary Search | O(n log n + m log n) | O(n) | Use binary search for efficient lookup |
| Multiset + Upper Bound | O(n log n + m log n) | O(n) | Optimal data structure for the problem |

### Time Complexity
- **Time**: O(n log n + m log n) - Sorting + binary search provides optimal time complexity
- **Space**: O(n) - For storing available tickets

### Why This Solution Works
- **Greedy Choice**: Always selecting the most expensive affordable ticket is optimal
- **Binary Search Efficiency**: Eliminates linear search through sorted data
- **Data Structure Choice**: Multiset provides optimal operations for this problem
- **Optimal Approach**: Binary search with sorted data provides the best balance of efficiency and correctness
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
